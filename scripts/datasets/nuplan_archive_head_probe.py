#!/usr/bin/env python3
"""
HEAD-only probe for known public nuPlan archive URLs.

This script does NOT download archive bodies. It issues HTTP HEAD requests only.

Use case:
- CloudFront paths may return 404 or differ from older published paths.
- The historical archive names are known (train camera 0..42, val camera 0..11, etc.).
- Before any TB-scale download, record whether each archive still resolves and its
  Content-Length / ETag / Last-Modified.

Example:
    python scripts/datasets/nuplan_archive_head_probe.py \
        --out manifests/nuplan_archive_head.csv

To probe only cameras:
    python scripts/datasets/nuplan_archive_head_probe.py \
        --kinds camera \
        --out manifests/nuplan_camera_head.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import ssl
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

BASES = {
    "regional": "https://motional-nuplan.s3-ap-northeast-1.amazonaws.com/public/nuplan-v1.1",
    "global": "https://motional-nuplan.s3.amazonaws.com/public/nuplan-v1.1",
    "cloudfront": "https://d1qinkmu0ju04f.cloudfront.net/public/nuplan-v1.1",
}

SENSOR_COUNTS = {
    "train": 43,
    "val": 12,
    "test": 12,
    "mini": 9,
}


def make_urls(base: str, splits: list[str], kinds: list[str]) -> list[dict]:
    rows = []
    for split in splits:
        count = SENSOR_COUNTS[split]
        set_name = {
            "train": "train_set",
            "val": "val_set",
            "test": "test_set",
            "mini": "mini_set",
        }[split]
        for kind in kinds:
            for i in range(count):
                filename = f"nuplan-v1.1_{split}_{kind}_{i}.zip"
                url = f"{base}/sensor_blobs/{set_name}/{filename}"
                rows.append(
                    {
                        "split": split,
                        "kind": kind,
                        "index": i,
                        "filename": filename,
                        "url": url,
                    }
                )
    return rows


def head(url: str, timeout: int) -> dict:
    req = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": "wam-research-nuplan-audit/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as r:
            headers = r.headers
            return {
                "status": getattr(r, "status", 200),
                "content_length": int(headers.get("Content-Length", "0") or 0),
                "etag": (headers.get("ETag") or "").strip('"'),
                "last_modified": headers.get("Last-Modified") or "",
                "content_type": headers.get("Content-Type") or "",
                "error": "",
            }
    except urllib.error.HTTPError as e:
        return {
            "status": e.code,
            "content_length": int(e.headers.get("Content-Length", "0") or 0),
            "etag": (e.headers.get("ETag") or "").strip('"'),
            "last_modified": e.headers.get("Last-Modified") or "",
            "content_type": e.headers.get("Content-Type") or "",
            "error": f"HTTPError: {e.reason}",
        }
    except Exception as e:
        return {
            "status": 0,
            "content_length": 0,
            "etag": "",
            "last_modified": "",
            "content_type": "",
            "error": f"{type(e).__name__}: {e}",
        }


def human(n: int) -> str:
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    x = float(n)
    for unit in units:
        if x < 1024 or unit == units[-1]:
            return f"{x:.3f} {unit}"
        x /= 1024
    return f"{n} B"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--host", choices=BASES, default="regional")
    p.add_argument(
        "--splits",
        nargs="+",
        choices=list(SENSOR_COUNTS),
        default=["train", "val"],
    )
    p.add_argument(
        "--kinds",
        nargs="+",
        choices=["camera", "lidar"],
        default=["camera", "lidar"],
    )
    p.add_argument("--timeout", type=int, default=20)
    p.add_argument("--out", default="nuplan_archive_head.csv")
    p.add_argument("--summary", default=None)
    args = p.parse_args()

    todo = make_urls(BASES[args.host], args.splits, args.kinds)
    out_rows = []

    for n, item in enumerate(todo, 1):
        result = head(item["url"], args.timeout)
        row = {**item, **result}
        out_rows.append(row)
        print(
            f"[{n:03d}/{len(todo):03d}] "
            f"{item['split']}/{item['kind']}/{item['index']:02d} "
            f"status={result['status']} size={human(result['content_length'])}"
            + (f" error={result['error']}" if result["error"] else ""),
            file=sys.stderr,
        )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "split",
        "kind",
        "index",
        "filename",
        "url",
        "status",
        "content_length",
        "etag",
        "last_modified",
        "content_type",
        "error",
    ]
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out_rows)

    agg = defaultdict(lambda: {"objects": 0, "ok": 0, "bytes": 0})
    for row in out_rows:
        key = f"{row['split']}_{row['kind']}"
        agg[key]["objects"] += 1
        if row["status"] in (200, 206):
            agg[key]["ok"] += 1
            agg[key]["bytes"] += int(row["content_length"] or 0)

    summary = {
        "host": args.host,
        "base": BASES[args.host],
        "head_only": True,
        "groups": {
            k: {
                **v,
                "GB_decimal": round(v["bytes"] / 1e9, 3),
                "TiB": round(v["bytes"] / (1024 ** 4), 6),
            }
            for k, v in sorted(agg.items())
        },
    }

    summary_path = Path(args.summary) if args.summary else out.with_suffix(".summary.json")
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"CSV: {out}")
    print(f"Summary: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
