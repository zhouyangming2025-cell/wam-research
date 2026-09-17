# D01 Source and Reading-Depth Log

## Depth rubric used

- RD2: primary abstract/introduction, mechanism figure or method sections, planning/deployment path, and relevant evaluation/ablation inspected.
- RD3: the above plus an existing repository deep analysis/audit resolving lifecycle, topology, or evidence boundaries.
- No RD4 claim is made: the presence of an official repository is not equivalent to a code-path audit.

## Per-paper log

| work | primary evidence checked | repository evidence reused | achieved | main limitation |
|---|---|---|---|---|
| Drive-WM | CVPR 2024 paper | `papers/raw_md/P0037_DriveWM/`, Phase-A source register | RD2 | official code not audited; internal feature-to-cost path partly unclear |
| OccWorld | arXiv 2311.16038v1 | `papers/raw_md/P0043_OccWorld/`, Phase-B synthesis | RD2 | uncertainty consumption and exact planner resolver not fully specified |
| Think2Drive | arXiv 2402.16720v2 / ECCV paper | raw text plus `PHASE_B_WAVE3_THINK2DRIVE_AUDIT.md` | RD3 | optimized deployment graph not code-verified |
| DrivingGPT | ICCV 2025 paper | `papers/raw_md/P0040_DrivingGPT/`, Phase-A census | RD2 | public code and exact token dependency at planning time UNKNOWN |
| Drive-OccWorld | arXiv 2408.14197v3 / AAAI paper | `papers/raw_md/P0044_DriveOccWorld/` | RD2 | project/code parity not audited |
| ViDAR | CVPR 2024 paper | raw text plus `CENSUS_PHASE_A_ROUND2.md` | RD2 | downstream runtime retention inferred only where stated by paper |
| DriveWorld | CVPR 2024 paper | `papers/raw_md/P0047_DriveWorld/` | RD2 | precise downstream planning topology and retained pretraining heads remain partly unclear |
| Auto-JEPA | arXiv 2607.29031v1 | raw text plus `PHASE_B_WAVE3_AUTOJEPA_AUDIT.md` | RD3 | intent latent is action-adjacent; classical environment-dynamics interpretation remains ambiguous |
| WorldRFT | arXiv 2512.19133v1 | `papers/raw_md/P0050_WorldRFT/` | RD2 | exact runtime reward/scorer retention not code-verified |
| ReWorld | arXiv 2606.27504v2 | raw text and Phase-A register | RD2 | official repository not audited; title changed from discovery wording |
| WA-JEPA | arXiv 2608.20974v2 | raw text and Phase-A register | RD2 | target-encoder detach/drop boundaries not code-verified |
| DA-WAM | arXiv 2608.19085/local canonical PDF | raw text, deep analysis, two literature audits | RD3 | released-code status and some gradient boundaries remain UNKNOWN |
| SafeDrive | CVPR 2026/arXiv 2602.18887 | raw text, deep analysis, `PHASE_C6_SAFEDRIVE_AUDIT.md` | RD3 | counterfactual reaction validity limited by factual logged targets |
| Gen-Drive | arXiv 2410.05582 / ICRA 2025 | `papers/raw_md/P0006_GenDrive/` | RD2 | code unavailable/unverified; joint generation does not prove causal reaction |
| DriveReward | arXiv 2606.08525v1 | raw text, deep analysis, `PHASE_C6_DRIVEREWARD_AUDIT.md` | RD3 | external planner integrations do not establish a native future model |
| RiskWorld | arXiv 2608.21414v1 | raw text, deep analysis, `PHASE_C6_RISKWORLD_AUDIT.md` | RD3 | no online planner integration in paper |
| SimWAM | arXiv 2608.07468v4 and official GitHub README | none at D01 start | RD2 | repository existence checked, implementation path not audited |
| DriveFuture | arXiv 2605.09701v1 HTML/PDF | none at D01 start | RD2 | official code not found; scorer details incomplete |
| Policy World Model | arXiv 2510.19654v2 | `papers/raw_md/P0041_PolicyWM/`, Phase-A register | RD2 | project page found; official code UNKNOWN |
| CausalDrive | arXiv 2606.15341v1 | raw text, card, `PHASE_B_WAVE4_CAUSALDRIVE_AUDIT.md` | RD3 | real-world causal validity and final deployed policy graph remain limited |
| RaWMPC | arXiv 2602.23259v1 HTML/PDF | none at D01 start | RD2 | official code UNKNOWN; exact cost weights and stochastic treatment not audited |
| DiffusionDrive | CVPR 2025 paper | `papers/raw_md/P0059_DiffusionDrive/`, Phase-A register | RD2 | sufficient for negative world-object finding; code not needed for census verdict |
| DriveSuprim | arXiv 2506.06659v3 | raw text plus `CENSUS_PHASE_A_ROUND2.md` | RD2 | official code UNKNOWN |
| GameFormer | ICCV 2023 paper | `papers/raw_md/P0018_GameFormer/`, Phase-A register | RD2 | boundary depends on project domain definition, not lack of interactive prediction |
| GAIA-1 | arXiv 2309.17080v1 | `papers/raw_md/P0035_GAIA1/`, Phase-A register | RD2 | no planner integration found in checked version |
| DriveArena | arXiv 2408.00415v1 and official repository | `papers/raw_md/P0056_DriveArena/`, Phase-A register | RD2 | platform/policy boundary is conceptual; code not audited |

## Distribution and source constraints

- RD2: 19 papers.
- RD3: 7 papers.
- RD0/RD1/RD4: 0 papers.
- Primary identity and title verified for all 26.
- Three papers were absent from the local corpus and were read from primary arXiv pages: SimWAM, DriveFuture, and RaWMPC.
- Official code presence was recorded only where a primary project/repository link was verified. Any unverified code field remains `UNKNOWN`.
