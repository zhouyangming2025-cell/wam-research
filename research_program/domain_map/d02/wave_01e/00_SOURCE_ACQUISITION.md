# D02-W1E Source Acquisition

Status: evidence acquisition only. This file records the seven W1E source downloads and text conversions. It does not make a new route judgment and does not modify the ontology.

## Protocol

- Download the formal paper PDF from an arXiv or official proceedings URL.
- Verify the downloaded file begins with `%PDF-` and record byte size, page count, and SHA-256.
- Preserve the PDF under `papers/pdf/` as the authoritative source.
- Convert the PDF with local Poppler `pdftotext -layout -enc UTF-8`.
- Preserve the converted text as `papers/raw_md/<paper>/<paper>.pdftext.md`.
- Do not overwrite the existing MinerU `*.raw.md`; the new file is a second, independently traceable text layer.

The PDF remains authoritative for figures, equations, layout-dependent claims, and exact wording. `pdftext.md` is a searchable extraction, not a claim that all visual structure survived conversion.

## Download ledger

Acquisition date: 2026-09-17

| ID | Paper | Source URL | PDF bytes | Pages | SHA-256 | Converted Markdown | Result |
|---|---|---|---:|---:|---|---|---|
| P0004 | *Reasoning Multi-Agent Behavioral Topology for Interactive Autonomous Driving* (BeTop) | https://arxiv.org/pdf/2409.18031 | 7,062,095 | 26 | `55f8d3c248d315d4bb67b9ccb4b0692e811384816bf38d01048fa82e57d38047` | `papers/raw_md/P0004_BeTop/P0004_BeTop.pdftext.md` | DOWNLOADED + CONVERTED |
| P0010 | *Test-Time Trajectory Optimization for Autonomous Driving* (TOAD) | https://arxiv.org/pdf/2606.07170 | 3,007,062 | 15 | `552116bd40762e0e57b21ec8793187b1ec222ed107472814f126a167fc5dc1f2` | `papers/raw_md/P0010_TOAD/P0010_TOAD.pdftext.md` | DOWNLOADED + CONVERTED |
| P0021 | *Hydra-MDP: End-to-end Multimodal Planning with Multi-target Hydra-Distillation* | https://arxiv.org/pdf/2406.06978 | 1,596,072 | 5 | `8927b0ffbfb0d9d5e86e168420a504dc14365131d5d31a7ede1da96e4768a8d3` | `papers/raw_md/P0021_HydraMDP/P0021_HydraMDP.pdftext.md` | DOWNLOADED + CONVERTED |
| P0029 | *GenAD: Generative End-to-End Autonomous Driving* | https://arxiv.org/pdf/2402.11502 | 27,391,543 | 10 | `a12f2865bd6a6a817372b56cd7049880b5a6b5d9d3a7ae9edfe2a67e9c490b61` | `papers/raw_md/P0029_GenAD/P0029_GenAD.pdftext.md` | DOWNLOADED + CONVERTED |
| P0034 | *HUGSIM: A Real-Time, Photo-Realistic and Closed-Loop Simulator for Autonomous Driving* | https://arxiv.org/pdf/2412.01718 | 50,128,067 | 24 | `7b8534cb59af740bbe18ba2a56f1007dabb36ef2f06ef40fc8a523edf533d07e` | `papers/raw_md/P0034_HUGSIM/P0034_HUGSIM.pdftext.md` | DOWNLOADED + CONVERTED |
| P0038 | *Vista: A Generalizable Driving World Model with High Fidelity and Versatile Controllability* | https://arxiv.org/pdf/2405.17398 | 18,033,269 | 31 | `80bddfd98c754170d7ea8688e1be4dc76b2af87d7290254f6662570ff839e9f5` | `papers/raw_md/P0038_Vista/P0038_Vista.pdftext.md` | DOWNLOADED + CONVERTED |
| P0058 | *VAD: Vectorized Scene Representation for Efficient Autonomous Driving* | https://openaccess.thecvf.com/content/ICCV2023/papers/Jiang_VAD_Vectorized_Scene_Representation_for_Efficient_Autonomous_Driving_ICCV_2023_paper.pdf | 3,410,216 | 11 | `1fcc34f4fb0121212727fded9c0fb8ae0f38cb6aabd972680cc3838ba7d3c8b0` | `papers/raw_md/P0058_VAD/P0058_VAD.pdftext.md` | DOWNLOADED + CONVERTED |

## Coverage result

All seven requested W1E papers were found and downloaded successfully. No paper is currently blocked on missing PDF access.

This acquisition does not yet close the scientific questions in the W1E protocol. The next audit must read the full text and may still leave a case as `KEEP`, `REMAP`, or `REMAIN-UNKNOWN`. No code repository was inspected in this acquisition step.
