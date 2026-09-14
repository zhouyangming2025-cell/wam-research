# Phase C.5 — Core-WAM Batch Ingest

> Infrastructure/corpus record only. No innovation, gap, quality, method comparison, or research-direction judgment is included.

Checked: 2026-09-14  |  Authority: official paper/repository pages and local canonical assets

## Batch matrix

| Paper ID | Short name | Identity verified? | Canonical source | PDF acquired? | PDF hash | Raw MD ready? | Raw MD hash | QC status | Official code? | Pinned commit | Checkpoint status | Blocker / anomaly |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P0042 | WorldDrive | YES | arXiv_v1 (https://arxiv.org/pdf/2603.14948) | YES | 77aeebcb970deeae322e86cb082b9b4c6bf1c931cae124bc7b4b1420ad82c603 | YES | 36e71e4e721e5ef7fe26b7f85bfc45f0a23eb8dff664c9c4d13dc088fdbfa95c | RAW_MD_READY | YES | c375ee1e1fe86ace175609db1ed90fd6db89673b | AVAILABLE | NONE |
| P0046 | World4Drive | YES | ICCV2025_camera_ready (https://openaccess.thecvf.com/content/ICCV2025/papers/Zheng_World4Drive_End-to-End_Autonomous_Driving_via_Intention-aware_Physical_Latent_World_Model_ICCV_2025_paper.pdf) | YES | 43d1d6caeadf0b4e4c6c0ff49ea87bbcfda7a0c7753b72e82b5694d0a9d190d0 | YES | d7068c39686d11678c4e88a724a9e1f89da9eaad858b74035baa461e0807d395 | RAW_MD_READY | YES | cffb51adeb1f7d02b49c4b74d7262ded62a33ac8 | UNKNOWN | NONE |
| P0061 | SeerDrive | YES | arXiv_v1 (https://arxiv.org/pdf/2510.11092) | YES | 1b3bec090522191ba60d4b6584c677c56ecb14408dc40cda9d93bc74e8e89bb7 | YES | fe5ead6880b95b2d7e751f54b58253371a6b07efc28f3361ce5c875a35296851 | RAW_MD_READY | YES | b468651302f545f7e497da62cdee4d447f31ae54 | AVAILABLE | NONE |
| P0049 | Drive-JEPA | YES | arXiv_v2 (https://arxiv.org/pdf/2601.22032) | YES | d88c053a67aca11b7bbd4c5f9f000cbf95c3f5e94656b6bad89cc9a717ab3672 | YES | 2066c4d1a6ee4f8e289837918dba74a8a63967df390471ffd375a0971ffb3022 | RAW_MD_READY | YES | e21f47410b4d26b61f05f9bd23e169c0390cae2a | AVAILABLE | NONE |
| P0062 | Metis | YES | arXiv_v1 (https://arxiv.org/pdf/2606.15869) | YES | 34870523248f06c752b4639be40d1397ab63ec04f8487c6569315a6ce1508c6c | YES | 68e670e71677465d6e95de4f8ba9c9070affbc0a33a1edcab07b6b867c193277 | RAW_MD_READY | YES | 7677b62d786cff8bb2044b489bd41f3d59514b43 | ANNOUNCED | CODE_REPO_PLACEHOLDER;IMPLEMENTATION_UNRELEASED |
| P0063 | DynFlowDrive | YES | arXiv_v2 (https://arxiv.org/pdf/2603.19675) | YES | 0cc39301a65dc0ef3e3d13326fe8d2a583598266313bba0ae5913ecbe2aad2a6 | YES | d7cb716c22f894181e7aad9f09739878b536220b9fad0ab3b393dd98444faf36 | RAW_MD_READY | YES | c665dc577a0939543fa7abe64d28eadaec28283c | ANNOUNCED | CODE_REPO_PLACEHOLDER;IMPLEMENTATION_UNRELEASED |
| P0064 | Discrete-WAM | YES | arXiv_v2 (https://arxiv.org/pdf/2606.05645) | YES | d9271f650d32f93b60ab9d17c0d60264f6df13dff887065cef7e4cb16b85ea7a | YES | 7beba7c3dc65892c8db3fb9291f18d91a70f10502bffb5505b923c8020ed8c5f | RAW_MD_READY | NO | NONE | UNKNOWN | FRONTPAGE_AUTHOR_OMITTED; NOT_FOUND |
| P0065 | GraphWorld | YES | arXiv_v1 (https://arxiv.org/pdf/2606.16274) | YES | f07a51ecf6cbef54b56550824e02c5d818a3dd09459e7c7d690682959b535bd9 | YES | 503f8e05f01908dcc24e35b6c82717f275398d3236877281bd21e3f37fed2143 | RAW_MD_READY | NO | NONE | UNKNOWN | NOT_FOUND |

## BLOCKERS

- No paper-level ingest blocker. All 8 target identities, local PDFs, front pages, and raw Markdown layers are present.
- Discrete-WAM page 1 omits the author list and directs readers to Contributions/Acknowledgments; identity was checked against the official arXiv record and this is retained as `FRONTPAGE_AUTHOR_OMITTED`.
- Metis and DynFlowDrive official repositories are present but do not contain released implementation at the pinned commits. Discrete-WAM and GraphWorld have no official code URL found in the live check.

## QC WARNINGS

- Raw Markdown: all 8 passed infrastructure QC; no `TABLE_IMAGE_ONLY` or `FIGURE_TEXT_LOSS` was observed. HTML tables, figure captions, equations, references, and referenced images were retained in the extracted layer.
- Front page: `P0064 Discrete-WAM` — `FRONTPAGE_AUTHOR_OMITTED` as described above.

## CODE STATUS CHANGES

| Paper | Repository status | Check |
|---|---|---|
| P0042 WorldDrive | RELEASED_SOURCE_VERIFIED | https://github.com/TabGuigui/WorldDrive @ `c375ee1e1fe86ace175609db1ed90fd6db89673b` |
| P0046 World4Drive | RELEASED_SOURCE_VERIFIED | https://github.com/ucaszyp/World4Drive @ `cffb51adeb1f7d02b49c4b74d7262ded62a33ac8` |
| P0061 SeerDrive | RELEASED_SOURCE_VERIFIED | https://github.com/LogosRoboticsGroup/SeerDrive @ `b468651302f545f7e497da62cdee4d447f31ae54` |
| P0049 Drive-JEPA | RELEASED_SOURCE_VERIFIED | https://github.com/linhanwang/Drive-JEPA @ `e21f47410b4d26b61f05f9bd23e169c0390cae2a` |
| P0062 Metis | CODE_REPO_PLACEHOLDER;IMPLEMENTATION_UNRELEASED | https://github.com/LogosRoboticsGroup/Metis @ `7677b62d786cff8bb2044b489bd41f3d59514b43` |
| P0063 DynFlowDrive | CODE_REPO_PLACEHOLDER;IMPLEMENTATION_UNRELEASED | https://github.com/xiaolul2/DynFlowDrive @ `c665dc577a0939543fa7abe64d28eadaec28283c` |
| P0064 Discrete-WAM | NOT_FOUND | NONE @ `NONE` |
| P0065 GraphWorld | NOT_FOUND | NONE @ `NONE` |

## MANIFEST CHANGES

- Reused stable IDs `P0042` WorldDrive, `P0046` World4Drive, and `P0049` Drive-JEPA; no aliases were merged and no old ID was renumbered.
- Allocated `P0061`–`P0065` in target order: SeerDrive, Metis, DynFlowDrive, Discrete-WAM, GraphWorld.
- Updated `manifests/CORPUS_MANIFEST.csv` to 65 rows with the existing 25-column schema; target rows are capped at corpus ingestion status and do not claim deep-read status.
- Replaced the example code row in `manifests/CODE_REPO_MANIFEST.csv` with 8 target records, including default branch, pinned commit, license, checkpoint state, and source-release notes.
- Added batch evidence ledgers: `batch_phase_c5_download_results.json`, `batch_phase_c5_frontpage_verification.json`, `batch_phase_c5_rawmd_results.json`, and `batch_phase_c5_qc.json`.

## Local-only assets

- Canonical PDFs remain under `papers/pdf/` and are not part of the GitHub corpus push policy.
- Shallow-cloned third-party repositories remain under `repos/` and are not staged for this repository.
