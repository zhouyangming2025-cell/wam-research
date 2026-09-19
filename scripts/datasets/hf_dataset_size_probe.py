#!/usr/bin/env python3
"""
Metadata-only size probe for a public Hugging Face dataset repository.

No dataset file bodies are downloaded. The script calls the public Hub tree API,
reads file paths + sizes, filters them locally, and writes a CSV/JSON summary.

Primary use in this project:
- estimate a 123D nuPlan CAM_F0-only research subset without installing hf CLI;
- compare that metadata-derived size against Motional raw archive sizes before
  approving any TB-scale transfer.

Example:
    python scripts/datasets/hf_dataset_size_probe.py \
      --repo kesai-labs/nuplan \
      --pattern "logs/nuplan_train/*/camera.pcam_f0.arrow" \
      --pattern "logs/nuplan_train/*/ego_state_se3.arrow" \
      --pattern "logs/nuplan_train/*/sync.arrow" \
      --out manifests/123d_nuplan_train_minimal.csv

The API response itself is metadata JSON only.
"""

from __future__ import annotations

import argparse
import csv
import fnmatch
import json
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path


def parse_next(link_header: str | None) -> str | None:
    if not link_header:
        return None
    for part in link_header.split(","):
        bits = [x.strip() for x in part.split(";")]
        if len(bits) >= 2 and bits[1] == 'rel="next"':
            url = bits[0].strip()
            if url.startswith("<") and url.endswith(">"):
                return url[1:-1]
    return None


def get_json(url: str, timeout: int) -> tuple[list[dict], str | None]:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "wam-research-hf-metadata-audit/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        payload = json.loads(r.read().decode("utf-8"))
        nxt = parse_next(r.headers.get("Link"))
    if not isinstance(payload, list):
        raise RuntimeError(f"Unexpected API payload type: {type(payload).__name__}")
    return payload, nxt


def list_repo_tree(repo: str, revision: str, timeout: int) -> list[dict]:
    repo_q = "/".join(urllib.parse.quote(x, safe="") for x in repo.split("/", 1))
    rev_q = urllib.parse.quote(revision, safe="")
    url = (
        f"https://huggingface.co/api/datasets/{repo_q}/tree/{rev_q}"
        "?recursive=true&expand=false"
    )
    rows: list[dict] = []
    page = 0
    while url:
        page += 1
        payload, url = get_json(url, timeout)
        rows.extend(payload)
        print(f"page={page} entries={len(rows)}", file=sys.stderr)
    return rows


def group_name(path: str) -> str:
    base = path.rsplit("/", 1)[-1]
    return base


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repo", default="kesai-labs/nuplan")
    p.add_argument("--revision", default="main")
    p.add_argument(
        "--pattern",
        action="append",
        default=[],
        help="fnmatch glob; may be repeated. If omitted, lists all files.",
    )
    p.add_argument("--timeout", type=int, default=60)
    p.add_argument("--out", default="hf_dataset_size_probe.csv")
    p.add_argument("--summary", default=None)
    args = p.parse_args()

    try:
        entries = list_repo_tree(args.repo, args.revision, args.timeout)
    except Exception as e:
        print(
            "ERROR: Hugging Face metadata API probe failed. "
            "No dataset file bodies were requested.\n"
            f"Reason: {type(e).__name__}: {e}",
            file=sys.stderr,
        )
        return 2

    files = []
    for item in entries:
        if item.get("type") != "file":
            continue
        path = item.get("path") or ""
        if args.pattern and not any(fnmatch.fnmatch(path, pat) for pat in args.pattern):
            continue
        size = item.get("size")
        if size is None:
            size = (item.get("lfs") or {}).get("size")
        size = int(size or 0)
        files.append(
            {
                "path": path,
                "size_bytes": size,
                "group": group_name(path),
                "blob_id": item.get("oid") or item.get("blobId") or item.get("blob_id") or "",
            }
        )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["path", "size_bytes", "group", "blob_id"])
        w.writeheader()
        w.writerows(files)

    groups = defaultdict(lambda: {"files": 0, "bytes": 0})
    for row in files:
        g = groups[row["group"]]
        g["files"] += 1
        g["bytes"] += row["size_bytes"]

    total = sum(r["size_bytes"] for r in files)
    summary = {
        "repo": args.repo,
        "revision": args.revision,
        "metadata_only": True,
        "patterns": args.pattern,
        "matched_files": len(files),
        "bytes": total,
        "GB_decimal": round(total / 1e9, 3),
        "TiB": round(total / (1024 ** 4), 6),
        "groups": {
            k: {
                **v,
                "GB_decimal": round(v["bytes"] / 1e9, 3),
                "TiB": round(v["bytes"] / (1024 ** 4), 6),
            }
            for k, v in sorted(groups.items())
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
