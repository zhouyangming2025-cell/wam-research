#!/usr/bin/env python3
"""
Build an object manifest for the public Motional nuPlan S3 bucket without AWS credentials.

Why this exists:
- The public nuPlan download UI does not expose a stable static size catalog.
- WAM data planning should be based on exact object sizes before any TB-scale download.
- This script uses only the Python standard library.

Example:
    python scripts/datasets/nuplan_public_manifest.py \
        --out manifests/nuplan_s3_objects.csv

Optional prefix:
    python scripts/datasets/nuplan_public_manifest.py \
        --prefix public/nuplan-v1.1/ \
        --out manifests/nuplan_v1_1_objects.csv

If the current machine cannot reach AWS, run it on any machine with outbound HTTPS
access and bring the resulting CSV back to the research workspace.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path


BUCKET_ENDPOINT = "https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/"
S3_NS = "http://s3.amazonaws.com/doc/2006-03-01/"


def gib(n: int) -> float:
    return n / (1024 ** 3)


def tib(n: int) -> float:
    return n / (1024 ** 4)


def classify(key: str) -> str:
    k = key.lower()

    if "map" in k and "nuplan" in k:
        return "maps"

    split = None
    for name in ("train", "val", "test", "mini"):
        if f"{name}_set" in k or f"_{name}_" in k or f"/{name}/" in k:
            split = name
            break

    if "camera" in k or "/cam_" in k:
        return f"{split or 'unknown'}_camera"
    if "lidar" in k or "mergedpointcloud" in k:
        return f"{split or 'unknown'}_lidar"

    if key.endswith(".db") or (
        "nuplan-v1.1_" in k
        and key.endswith(".zip")
        and "camera" not in k
        and "lidar" not in k
        and "map" not in k
    ):
        return f"{split or 'unknown'}_db_or_split"

    return f"{split or 'other'}_other"


def text_of(parent: ET.Element, tag: str) -> str | None:
    el = parent.find(f"{{{S3_NS}}}{tag}")
    if el is None:
        el = parent.find(tag)
    return el.text if el is not None else None


def list_page(prefix: str, continuation: str | None, timeout: int) -> tuple[list[dict], str | None]:
    params = {
        "list-type": "2",
        "max-keys": "1000",
    }
    if prefix:
        params["prefix"] = prefix
    if continuation:
        params["continuation-token"] = continuation

    url = BUCKET_ENDPOINT + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "wam-research-nuplan-audit/1.0"})

    with urllib.request.urlopen(req, timeout=timeout) as response:
        payload = response.read()

    root = ET.fromstring(payload)
    contents = root.findall(f"{{{S3_NS}}}Contents")
    if not contents:
        contents = root.findall("Contents")

    rows = []
    for item in contents:
        key = text_of(item, "Key") or ""
        size = int(text_of(item, "Size") or "0")
        rows.append(
            {
                "key": key,
                "size_bytes": size,
                "last_modified": text_of(item, "LastModified") or "",
                "etag": (text_of(item, "ETag") or "").strip('"'),
                "category": classify(key),
            }
        )

    is_truncated = (text_of(root, "IsTruncated") or "false").lower() == "true"
    next_token = text_of(root, "NextContinuationToken") if is_truncated else None
    return rows, next_token


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", default="", help="Optional S3 key prefix")
    parser.add_argument("--out", default="nuplan_s3_objects.csv", help="CSV output path")
    parser.add_argument("--summary", default=None, help="Optional JSON summary path")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument(
        "--max-pages",
        type=int,
        default=0,
        help="Safety limit; 0 means no page limit",
    )
    args = parser.parse_args()

    rows: list[dict] = []
    token = None
    page = 0

    try:
        while True:
            page += 1
            batch, token = list_page(args.prefix, token, args.timeout)
            rows.extend(batch)
            total = sum(int(r["size_bytes"]) for r in rows)
            print(
                f"page={page} objects={len(rows)} "
                f"bytes={total} ({gib(total):.2f} GiB / {tib(total):.3f} TiB)",
                file=sys.stderr,
            )
            if not token:
                break
            if args.max_pages and page >= args.max_pages:
                print("Stopped at --max-pages safety limit.", file=sys.stderr)
                break
    except Exception as exc:
        print(
            "ERROR: Could not list the public nuPlan S3 bucket. "
            "This is usually an outbound-network / proxy / TLS issue rather than an AWS-account issue.\n"
            f"Endpoint: {BUCKET_ENDPOINT}\n"
            f"Reason: {exc}",
            file=sys.stderr,
        )
        return 2

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["key", "size_bytes", "last_modified", "etag", "category"],
        )
        writer.writeheader()
        writer.writerows(rows)

    category = defaultdict(lambda: {"objects": 0, "bytes": 0})
    for row in rows:
        item = category[row["category"]]
        item["objects"] += 1
        item["bytes"] += int(row["size_bytes"])

    total_bytes = sum(int(r["size_bytes"]) for r in rows)
    summary = {
        "bucket": "motional-nuplan",
        "region": "ap-northeast-1",
        "prefix": args.prefix,
        "objects": len(rows),
        "bytes": total_bytes,
        "GiB": round(gib(total_bytes), 3),
        "TiB": round(tib(total_bytes), 6),
        "categories": {
            k: {
                "objects": v["objects"],
                "bytes": v["bytes"],
                "GiB": round(gib(v["bytes"]), 3),
                "TiB": round(tib(v["bytes"]), 6),
            }
            for k, v in sorted(category.items())
        },
    }

    summary_path = Path(args.summary) if args.summary else out_path.with_suffix(".summary.json")
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"CSV: {out_path}")
    print(f"Summary: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
