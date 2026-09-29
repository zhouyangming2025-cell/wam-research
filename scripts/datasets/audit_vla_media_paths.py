#!/usr/bin/env python3
"""Stream public VLA annotation JSONL files and inventory referenced media paths.

This reads annotation text only. It does not request or download image/video
media. A full scan transfers the JSONL annotation objects listed by the pinned
Hugging Face revisions (about 4.7 GB at the revisions used for the 2026-09-29
audit). Path equality is used for logical-path deduplication; media bytes or
content hashes are not fetched or inferred.

Example:
    python scripts/datasets/audit_vla_media_paths.py \
        --out-json audits/datasets/WAM_VLA_MEDIA_PATH_AUDIT_2026-09-29.json

Use --limit-rows for a small parser smoke test. A limited scan is always marked
incomplete and must not be used as a dataset inventory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import sqlite3
import sys
import tempfile
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterator


RECODRIVE_REPO = "owl10/ReCogDrive_Pretraining"
RECODRIVE_REVISION = "f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf"
SGDRIVE_REPO = "SII-Whaleice/SGDrive"
SGDRIVE_REVISION = "c6379bea8aaf635883b33fcc99499b59d42aad1e"
MEDIA_KEYS = {
    "image", "images", "video", "videos", "image_path", "image_paths",
    "video_path", "video_paths", "frame_path", "frame_paths", "clip_path",
    "clip_paths", "media_path", "media_paths",
}


def get_json(url: str, timeout: int) -> Any:
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "wam-research-vla-path-audit/1.0"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def repo_tree(repo: str, revision: str, kind: str, timeout: int) -> list[dict[str, Any]]:
    encoded_repo = "/".join(urllib.parse.quote(piece, safe="") for piece in repo.split("/", 1))
    encoded_revision = urllib.parse.quote(revision, safe="")
    url = f"https://huggingface.co/api/{kind}/{encoded_repo}/tree/{encoded_revision}?recursive=true&expand=true"
    result = get_json(url, timeout)
    if not isinstance(result, list):
        raise RuntimeError(f"Unexpected tree response for {repo}: {type(result).__name__}")
    return result


def file_sources(timeout: int) -> list[dict[str, Any]]:
    specs = [
        ("ReCogDrive", RECODRIVE_REPO, RECODRIVE_REVISION, "datasets"),
        ("SGDrive", SGDRIVE_REPO, SGDRIVE_REVISION, "models"),
    ]
    sources: list[dict[str, Any]] = []
    for annotation_set, repo, revision, kind in specs:
        entries = repo_tree(repo, revision, kind, timeout)
        for item in entries:
            path = item.get("path", "")
            if item.get("type") != "file" or not path.lower().endswith(".jsonl"):
                continue
            resolve_prefix = f"https://huggingface.co/datasets/{repo}" if kind == "datasets" else f"https://huggingface.co/{repo}"
            source_url = f"{resolve_prefix}/resolve/{revision}/" + urllib.parse.quote(path, safe="/")
            sources.append(
                {
                    "annotation_set": annotation_set,
                    "repo": repo,
                    "revision": revision,
                    "path": path,
                    "source_url": source_url,
                    "bytes_expected": int(item.get("size") or (item.get("lfs") or {}).get("size") or 0),
                    "repo_blob_oid": item.get("oid"),
                    "lfs_sha256_expected": (item.get("lfs") or {}).get("oid"),
                    "xet_hash": item.get("xetHash"),
                    "last_commit": (item.get("lastCommit") or {}).get("id"),
                }
            )
    return sorted(sources, key=lambda row: (row["annotation_set"], row["path"]))


def source_context(source: dict[str, Any]) -> str:
    path = source["path"].lower()
    if source["annotation_set"] == "SGDrive":
        return "NAVSIM/OpenScene"
    if "bench2drive" in path:
        return "Bench2Drive"
    if "navsim" in path:
        return "NAVSIM/OpenScene"
    if "drivelm" in path or "nuinstruct" in path or "nuscenes-qa" in path or "omnidrive" in path or "senna" in path:
        return "nuScenes"
    for marker, family in (
        ("lingoqa", "LingoQA"), ("drama", "DRAMA"), ("sutd", "SUTD TrafficQA"),
        ("coda-lm", "CODA-LM"), ("maplm", "MAPLM"), ("drivegpt4", "DriveGPT4/BDD-X"),
        ("talk2car", "Talk2Car"),
    ):
        if marker in path:
            return family
    return "UNKNOWN"


def clean_path(value: str) -> str:
    value = value.strip().replace("\\", "/")
    if value.startswith("file://"):
        value = value[7:]
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme in {"http", "https", "s3", "gs"}:
        value = parsed.netloc + parsed.path
    else:
        value = parsed.path
    value = urllib.parse.unquote(value)
    value = re.sub(r"/+/", "/", value)
    return posixpath.normpath(value).lstrip("/") if value else ""


def classify_path(raw_path: str, context: str) -> tuple[str, str, str]:
    normalized = clean_path(raw_path)
    lower = normalized.lower()
    segments = [part for part in normalized.split("/") if part not in {"", "."}]
    lower_segments = [part.lower() for part in segments]

    def after(marker: str) -> str | None:
        marker = marker.lower()
        if marker not in lower_segments:
            return None
        index = lower_segments.index(marker)
        return "/".join(segments[index + 1 :])

    b2d = after("bench2drive")
    if b2d is not None:
        return "Bench2Drive", b2d, "PATH_PREFIX"

    navsim = after("sensor_blobs")
    if navsim is not None and ("navsim" in lower or "sensor_blobs" in lower):
        return "NAVSIM/OpenScene", "sensor_blobs/" + navsim, "PATH_PREFIX"

    nuscenes = after("nuscenes")
    if nuscenes and (nuscenes.startswith("samples/") or nuscenes.startswith("sweeps/")):
        return "nuScenes", nuscenes, "PATH_PREFIX"
    sample_index = next(
        (i for i, part in enumerate(lower_segments[:-1]) if part == "samples" and lower_segments[i + 1].startswith("cam_")),
        None,
    )
    if sample_index is not None:
        return "nuScenes", "/".join(segments[sample_index:]), "PATH_PATTERN"

    markers = (
        ("lingoqa", "LingoQA"), ("drama", "DRAMA"), ("sutd", "SUTD TrafficQA"),
        ("coda-lm", "CODA-LM"), ("maplm", "MAPLM"), ("drivegpt4", "DriveGPT4/BDD-X"),
        ("talk2car", "Talk2Car"), ("llava", "LLaVA general VQA"),
    )
    for marker, family in markers:
        relative = after(marker)
        if relative is not None:
            return family, relative, "PATH_PREFIX"

    if context != "UNKNOWN":
        return context, normalized, "ANNOTATION_CONTEXT"

    host = urllib.parse.urlsplit(raw_path).hostname
    if host:
        return "UNKNOWN", f"URL_HOST:{host}/{normalized}", "UNMAPPED_URL"
    return "UNKNOWN", normalized, "UNMAPPED_PATH"


def path_prefix(family: str, canonical_path: str) -> str:
    parts = canonical_path.split("/") if canonical_path else []
    if family == "NAVSIM/OpenScene":
        return "/".join(parts[:2])
    if family == "Bench2Drive":
        return "/".join(parts[:1])
    if family == "nuScenes":
        return "/".join(parts[:2])
    if family == "LingoQA":
        return "/".join(parts[:3])
    if family == "DRAMA":
        return "/".join(parts[:2])
    if family == "SUTD TrafficQA":
        return "/".join(parts[:1])
    if family == "CODA-LM":
        return "/".join(parts[:1])
    if family == "MAPLM":
        return "/".join(parts[:2])
    if family in {"DriveGPT4/BDD-X", "Talk2Car"}:
        return "/".join(parts[:1]) if len(parts) > 1 else "(flat-root)"
    return "/".join(parts[:2])


def extract_media_values(obj: Any, inherited_key: str = "") -> Iterator[tuple[str, str]]:
    """Yield string media references under recognized media field names."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            key_norm = str(key).lower()
            if key_norm in MEDIA_KEYS:
                yield from extract_media_values(value, key_norm)
            elif inherited_key in MEDIA_KEYS and key_norm in {"path", "uri", "url", "file", "filename"}:
                yield from extract_media_values(value, inherited_key)
    elif isinstance(obj, list):
        for value in obj:
            yield from extract_media_values(value, inherited_key)
    elif isinstance(obj, str) and inherited_key in MEDIA_KEYS:
        value = obj.strip()
        if value and value.lower() not in {"none", "null"}:
            modality = "video" if "video" in inherited_key or "clip" in inherited_key else "image"
            yield modality, value


def scan_one(
    source: dict[str, Any],
    index: int,
    total: int,
    db: sqlite3.Connection,
    timeout: int,
    limit_rows: int | None,
) -> dict[str, Any]:
    annotation_id = f"{source['annotation_set']}:{source['path']}"
    context = source_context(source)
    req = urllib.request.Request(
        source["source_url"],
        headers={"User-Agent": "wam-research-vla-path-audit/1.0", "Accept-Encoding": "identity"},
    )
    print(
        f"[{index}/{total}] streaming {annotation_id} bytes_expected={source['bytes_expected']}",
        file=sys.stderr,
        flush=True,
    )
    streamed = 0
    rows = 0
    parse_errors = 0
    media_counts: Counter[tuple[str, str, str]] = Counter()
    digest = hashlib.sha256()
    progress_next = 128 * 1024 * 1024
    with urllib.request.urlopen(req, timeout=timeout) as response:
        content_length = response.headers.get("Content-Length")
        final_url_host = urllib.parse.urlsplit(response.geturl()).hostname
        for raw_line in response:
            streamed += len(raw_line)
            digest.update(raw_line)
            if not raw_line.strip():
                continue
            try:
                record = json.loads(raw_line)
            except (json.JSONDecodeError, UnicodeDecodeError):
                parse_errors += 1
                continue
            rows += 1
            for modality, raw_path in extract_media_values(record):
                family, canonical_path, confidence = classify_path(raw_path, context)
                if not canonical_path:
                    continue
                db.execute(
                    """INSERT INTO refs(family, canonical_path, annotation_id, modality, confidence, occurrences)
                       VALUES(?,?,?,?,?,1)
                       ON CONFLICT(family, canonical_path, annotation_id, modality, confidence)
                       DO UPDATE SET occurrences=occurrences+1""",
                    (family, canonical_path, annotation_id, modality, confidence),
                )
                db.execute(
                    """INSERT INTO prefix_refs(family, path_prefix, canonical_path, annotation_id, occurrences)
                       VALUES(?,?,?,?,1)
                       ON CONFLICT(family, path_prefix, canonical_path, annotation_id)
                       DO UPDATE SET occurrences=occurrences+1""",
                    (family, path_prefix(family, canonical_path), canonical_path, annotation_id),
                )
                media_counts[(family, modality, confidence)] += 1
            if streamed >= progress_next:
                print(
                    f"    streamed={streamed}/{source['bytes_expected']} rows={rows} media_refs={sum(media_counts.values())}",
                    file=sys.stderr,
                    flush=True,
                )
                progress_next += 128 * 1024 * 1024
            if limit_rows is not None and rows >= limit_rows:
                break
    db.commit()
    complete = limit_rows is None or rows < limit_rows
    result = {
        **source,
        "annotation_id": annotation_id,
        "context_family": context,
        "bytes_streamed": streamed,
        "response_content_length": int(content_length) if content_length and content_length.isdigit() else None,
        "final_host": final_url_host,
        "stream_sha256": digest.hexdigest(),
        "lfs_sha256_matches": (
            digest.hexdigest() == source["lfs_sha256_expected"]
            if source.get("lfs_sha256_expected") else None
        ),
        "rows_read": rows,
        "parse_errors": parse_errors,
        "media_uri_occurrences": sum(media_counts.values()),
        "media_by_family_modality_confidence": [
            {
                "family": family,
                "modality": modality,
                "mapping_basis": confidence,
                "uri_occurrences": count,
            }
            for (family, modality, confidence), count in sorted(media_counts.items())
        ],
        "complete": complete,
    }
    print(
        f"    done bytes={streamed} rows={rows} media_refs={result['media_uri_occurrences']} parse_errors={parse_errors} complete={complete}",
        file=sys.stderr,
        flush=True,
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-json", required=True, help="Write machine-readable summary JSON.")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--limit-rows", type=int, default=None, help="Smoke-test limit per JSONL; marks scan incomplete.")
    parser.add_argument("--include-path-substring", default=None, help="Scan only JSONL paths containing this substring; overall scope will be partial.")
    args = parser.parse_args()

    sources = file_sources(args.timeout)
    if args.include_path_substring:
        sources = [source for source in sources if args.include_path_substring.lower() in source["path"].lower()]
        if not sources:
            raise SystemExit(f"No JSONL source path contains {args.include_path_substring!r}")
    total_bytes = sum(source["bytes_expected"] for source in sources)
    print(f"objects={len(sources)} annotation_bytes_expected={total_bytes}", file=sys.stderr, flush=True)
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="wam_vla_media_paths_") as temp_dir:
        db = sqlite3.connect(str(Path(temp_dir) / "paths.sqlite"))
        db.execute(
            """CREATE TABLE refs(
                family TEXT NOT NULL,
                canonical_path TEXT NOT NULL,
                annotation_id TEXT NOT NULL,
                modality TEXT NOT NULL,
                confidence TEXT NOT NULL,
                occurrences INTEGER NOT NULL,
                PRIMARY KEY(family, canonical_path, annotation_id, modality, confidence)
            )"""
        )
        db.execute(
            """CREATE TABLE prefix_refs(
                family TEXT NOT NULL,
                path_prefix TEXT NOT NULL,
                canonical_path TEXT NOT NULL,
                annotation_id TEXT NOT NULL,
                occurrences INTEGER NOT NULL,
                PRIMARY KEY(family, path_prefix, canonical_path, annotation_id)
            )"""
        )
        for index, source in enumerate(sources, 1):
            results.append(scan_one(source, index, len(sources), db, args.timeout, args.limit_rows))

        family_rows = db.execute(
            """SELECT family, modality, confidence, SUM(occurrences) AS uri_occurrences,
                      COUNT(DISTINCT canonical_path) AS globally_unique_paths,
                      COUNT(DISTINCT annotation_id) AS annotation_files
               FROM refs GROUP BY family, modality, confidence
               ORDER BY family, modality, confidence"""
        ).fetchall()
        family_summary: list[dict[str, Any]] = []
        for family, modality, confidence, occurrences, globally_unique, files in family_rows:
            path_annotation_pairs = db.execute(
                "SELECT COUNT(*) FROM (SELECT DISTINCT canonical_path, annotation_id FROM refs WHERE family=? AND modality=? AND confidence=?)",
                (family, modality, confidence),
            ).fetchone()[0]
            cross_annotation_duplicates = path_annotation_pairs - globally_unique
            family_summary.append(
                {
                    "family": family,
                    "modality": modality,
                    "mapping_basis": confidence,
                    "uri_occurrences": occurrences,
                    "unique_paths_across_scanned_annotations": globally_unique,
                    "unique_path_annotation_pairs": path_annotation_pairs,
                    "cross_annotation_duplicate_path_pairs": cross_annotation_duplicates,
                    "annotation_files": files,
                }
            )

        per_annotation_rows = db.execute(
            """SELECT annotation_id, family, modality, confidence, SUM(occurrences),
                      COUNT(DISTINCT canonical_path)
               FROM refs GROUP BY annotation_id, family, modality, confidence
               ORDER BY annotation_id, family, modality, confidence"""
        ).fetchall()
        per_annotation_summary = [
            {
                "annotation_id": row[0], "family": row[1], "modality": row[2],
                "mapping_basis": row[3], "uri_occurrences": row[4],
                "unique_paths_in_annotation": row[5],
            }
            for row in per_annotation_rows
        ]
        global_family = db.execute(
            """SELECT family, COUNT(DISTINCT canonical_path) AS unique_paths,
                      SUM(occurrences) AS uri_occurrences,
                      COUNT(DISTINCT annotation_id) AS annotation_files
               FROM refs GROUP BY family ORDER BY family"""
        ).fetchall()
        unique_family_paths = [
            {"family": row[0], "unique_paths": row[1], "uri_occurrences": row[2], "annotation_files": row[3]}
            for row in global_family
        ]
        prefix_rows = db.execute(
            """SELECT family, path_prefix, SUM(occurrences), COUNT(DISTINCT canonical_path),
                      COUNT(DISTINCT annotation_id)
               FROM prefix_refs GROUP BY family, path_prefix ORDER BY family, path_prefix"""
        ).fetchall()
        path_prefix_summary = [
            {
                "family": row[0], "path_prefix": row[1], "uri_occurrences": row[2],
                "unique_paths": row[3], "annotation_files": row[4],
            }
            for row in prefix_rows
        ]
        pairwise_rows = db.execute(
            """SELECT left_ref.family, left_ref.annotation_id, right_ref.annotation_id,
                      COUNT(DISTINCT left_ref.canonical_path)
               FROM refs AS left_ref JOIN refs AS right_ref
                 ON left_ref.family = right_ref.family
                AND left_ref.canonical_path = right_ref.canonical_path
                AND left_ref.annotation_id < right_ref.annotation_id
               GROUP BY left_ref.family, left_ref.annotation_id, right_ref.annotation_id
               ORDER BY left_ref.family, left_ref.annotation_id, right_ref.annotation_id"""
        ).fetchall()
        pairwise_path_intersections = [
            {
                "family": row[0], "annotation_a": row[1], "annotation_b": row[2],
                "shared_canonical_paths": row[3],
            }
            for row in pairwise_rows
        ]
        unknown_unique_count = db.execute(
            "SELECT COUNT(DISTINCT canonical_path) FROM refs WHERE family='UNKNOWN'"
        ).fetchone()[0]
        unknown_paths = [
            row[0]
            for row in db.execute(
                "SELECT DISTINCT canonical_path FROM refs WHERE family='UNKNOWN' ORDER BY canonical_path LIMIT 1000"
            ).fetchall()
        ]
        path_digest = hashlib.sha256()
        for row in db.execute(
            "SELECT DISTINCT family, canonical_path FROM refs ORDER BY family, canonical_path"
        ):
            path_digest.update(row[0].encode("utf-8"))
            path_digest.update(b"\0")
            path_digest.update(row[1].encode("utf-8"))
            path_digest.update(b"\n")
        db.close()

    complete = all(row["complete"] for row in results) and args.limit_rows is None and len(sources) == 18
    report = {
        "audit_date": "2026-09-29",
        "method": {
            "annotation_only": True,
            "media_objects_requested": 0,
            "media_keys": sorted(MEDIA_KEYS),
            "deduplication": "Path-level only: (family, normalized relative path); no basename-only or media-byte/hash deduplication.",
            "normalization": "URL-decode, slash normalization, remove known dataset mount prefix by dataset marker; preserve case within relative path.",
            "complete_scan": complete,
            "selected_annotation_objects": len(sources),
            "include_path_substring": args.include_path_substring,
            "input_object_bytes_expected": total_bytes,
        },
        "source_objects": results,
        "per_annotation_family_modality": per_annotation_summary,
        "family_modality_summary": family_summary,
        "family_unique_path_summary": unique_family_paths,
        "family_path_prefix_summary": path_prefix_summary,
        "pairwise_path_intersections": pairwise_path_intersections,
        "unmapped_unique_path_count": unknown_unique_count,
        "unmapped_unique_path_examples_count": len(unknown_paths),
        "unmapped_unique_path_examples": unknown_paths,
        "canonical_path_set_sha256": path_digest.hexdigest(),
    }
    out_path = Path(args.out_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote={out_path} complete={complete} family_groups={len(family_summary)}", file=sys.stderr)
    return 0 if complete else 3


if __name__ == "__main__":
    raise SystemExit(main())
