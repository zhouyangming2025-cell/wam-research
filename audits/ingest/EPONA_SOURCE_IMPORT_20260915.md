# Epona Source Import

> Infrastructure record only. This file records the source snapshot boundary; it is not a scientific review of Epona.

Checked: 2026-09-15  
Upstream: https://github.com/Kevin-thu/Epona  
Upstream commit: `69b24c55f5ab8b3ffde8fa55e9f833bfe64d2c68`  
Local source: `D:\zym_information\ZYM\wam\workspace\Epona`  
Project destination: `repos/Epona/`

## Included

The snapshot contains the 69 files tracked by the upstream repository at the pinned commit, including:

- Python source under `dataset/`, `models/`, `scripts/`, and `utils/`;
- configuration and data-preparation instructions under `configs/` and `data_preparation/`;
- `README.md`, `LICENSE`, `.gitignore`, `requirements.txt`;
- `assets/teaser.png`.

## Excluded

The following local working-copy material was deliberately not copied into the project repository:

- nested `.git/` history and objects;
- `Epona.pdf` and `Epona.md`;
- `Epona_mineru/` conversion outputs;
- any other untracked local artifacts;
- model checkpoints, datasets, logs, and runtime outputs.

The paper PDF/raw Markdown remain governed by the existing `papers/` and corpus manifest workflow. The source snapshot is recorded as code repository `R0009` in `manifests/CODE_REPO_MANIFEST.csv`, and `P0001` points to `R0009` in `manifests/CORPUS_MANIFEST.csv`.

## Verification

- source repository status: clean tracked source at the pinned commit; local paper/MinerU artifacts remain outside the snapshot;
- destination contains no nested `.git/`;
- destination file count: 69;
- source and destination file paths and bytes are checked before commit;
- no secrets/checkpoint extensions were found in the imported source snapshot.

