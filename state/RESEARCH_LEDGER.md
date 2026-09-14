# RESEARCH_LEDGER

Running factual ledger of assets, research-state transitions and scientific gates.

## Current research stage

```text
FIELD RECONSTRUCTION — PHASE B: WAVE 3 ACTIVE
```

Canonical documents:

- `landscape/FIELD_RECONSTRUCTION_PLAN.md`
- `landscape/PLANNING_WAM_TAXONOMY.md`
- `landscape/FIELD_ATLAS.md`
- `landscape/PHASE_B_ANCHORS.md`
- `landscape/PHASE_B_WAVE1_SYNTHESIS.md`
- `landscape/PHASE_B_WAVE1_COMPARABILITY_AUDIT.md`
- `landscape/PHASE_B_WAVE2_SYNTHESIS.md`
- `landscape/PHASE_B_WAVE2_COMPARABILITY_AUDIT.md`
- `landscape/PHASE_B_WAVE3_PLAN.md`

## Hypotheses

| hypothesis | status | role | file |
|---|---|---|---|
| P1_RETIRED — Planner-Induced Model Exploitation / Search-Support Gap | RETIRED | historical hypothesis / robustness evidence | `hypotheses/P1_RETIRED.md` |
| P2R_PRIMARY — Reactive Action-Ordering Gap | PARKED PROBE | diagnostic lens only; not active search target | `hypotheses/P2R_PRIMARY.md` |
| P3_HOLD — Decision Sufficiency of World Representations | PARKED BACKUP PROBE | possible later synthesis question | `hypotheses/P3_HOLD.md` |

## Research scope rule

```text
World Model + End-to-End + Planning-centric
```

Risk / predictive risk field is optional prior knowledge, not a required destination. Field understanding precedes gap hunting.

## Corpus inventory

| date | batch | IDs | state |
|---|---|---|---|
| 2026-09-13 | Batch 0A | P0001–P0012 | 11 `RAW_MD_READY`; P0008 NPPC blocked `PAYWALLED_NO_OPEN_SOURCE` |
| 2026-09-14 | interactive/reactive branch | P0013–P0020 | 7 `RAW_MD_READY`; P0020 Bahram 2016 blocked `PAYWALLED_NO_OPEN_SOURCE` |
| 2026-09-14 | Census Round-2 support | P0021–P0034 | 14/14 `DOCUMENT_VERIFIED` + `RAW_MD_READY` |
| 2026-09-14 | Census Round-1 text-layer completion | P0035–P0060 | 26/26 `DOCUMENT_VERIFIED` + `RAW_MD_READY` |

Current total:

```text
60 stable IDs registered: P0001–P0060
58 RAW_MD_READY
2 lawful-source blockers: P0008 NPPC, P0020 Bahram 2016
```

Broad corpus acquisition is frozen.

## Scientific / methodology gates

| date | gate | material | result |
|---|---|---|---|
| 2026-09-13 | P2-R Targeted Failure Deep Read — Round 1 | SafeDrive, BeTop, GraphAD, RiskWorld, DA-WAM | historical audit only; no direct observed reaction-induced action-order inversion established |
| 2026-09-14 | Field-Reconstruction Reset | methodology | gap-first search suspended; neutral census + anchors activated |
| 2026-09-14 | Phase-A Census / corpus closeout | P0001–P0060 + F1–F11 atlas | **PASS**; broad expansion frozen; 25 anchors selected |
| 2026-09-14 | Phase-B Wave 1 | M2I, GameFormer, What Truly Matters, UniAD, nuPlan, NAVSIM, DiffusionDrive, DriveSuprim | **CLOSED**; historical/non-WM/evaluation control baseline stable |
| 2026-09-14 | Phase-B Wave 2 | GAIA-1, Drive-WM, OccWorld, WoTE, ViDAR, LAW | **CLOSED**; world/future→planning interface taxonomy + attribution/supervision boundaries stable |
| 2026-09-14 | Phase-B Wave 3 | Epona, DrivingGPT, DriveLaW, Auto-JEPA, DA-WAM, Think2Drive | **ACTIVE** |

## Wave-1 ledger result

Wave 1 established that modern WAM planning claims must be interpreted against older capabilities and strong non-WM controls:

```text
interaction-conditioned prediction already existed
joint prediction/planning already existed
prediction metrics can mis-rank driving performance
planning-oriented multi-task representation already existed
multimodal direct action generation can be strong without WM
candidate ranking can be strong without WM
OL / non-reactive / reactive evaluation are different claims
```

Canonical artifacts:

- `landscape/PHASE_B_WAVE1_SYNTHESIS.md`
- `landscape/PHASE_B_WAVE1_COMPARABILITY_AUDIT.md`

## Wave-2 ledger result

Wave 2 separated six planning roles:

```text
GAIA-1   — controllable generative capability
Drive-WM — visual future as candidate evaluator
OccWorld — structured joint world+ego generation
WoTE     — online candidate-specific future BEV evaluation
ViDAR    — predictive pretraining / representation transfer
LAW      — action-aware auxiliary future-latent learning
```

Canonical artifacts:

- `landscape/PHASE_B_WAVE2_SYNTHESIS.md`
- `landscape/PHASE_B_WAVE2_COMPARABILITY_AUDIT.md`
- `audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md`

Stable evidence conclusions:

1. **Generation quality is not planning evidence.** Drive-WM operationalizes imagined futures for candidate selection, but the effect of better FID/FVD/KPM is not isolated from detector/map/reward/candidate effects.
2. **World reconstruction fidelity is not monotonic with planning utility.** OccWorld's higher-resolution tokenizer reconstructs better but forecasts/plans worse.
3. **Future-state input can add value beyond scorer-only.** WoTE's matched NAVSIM ablation is `81.0 → 83.2 → 85.6 PDMS` for trajectory-only → evaluator-only → evaluator+future-state.
4. **Candidate-specific prediction is not the same as reactive oracle supervision.** WoTE's audited PDM target path shares logged/GT surrounding-agent future across candidate ego trajectories.
5. **Predictive pretraining can help without an online WM.** ViDAR transfers the pretrained History/BEV encoder into downstream UniAD; its future decoder is not deployed.
6. **Auxiliary future prediction can help without online rollout.** LAW's audited test path discards future latent outputs; the prediction branch shapes representation/parameters during training.
7. **Longer horizon is not monotonically better.** LAW's 1.5 s future target outperforms 3 s and 10 s variants in the reported ablation.

## Active Wave-3 gate

Canonical plan:

`landscape/PHASE_B_WAVE3_PLAN.md`

Order:

```text
Epona → DrivingGPT → DriveLaW → Auto-JEPA → DA-WAM → Think2Drive
```

Wave 3 must map:

```text
shared-latent joint training
interleaved world-action generation
hidden-WM-feature action generation
compressed predictive representation shaping
candidate-specific predictive evaluation
WM-based imagined policy learning
```

No gap/method verdict is allowed at this gate.

## Integrity notes

- Raw-MD conversion ledger race was detected, repaired from stored artifacts, and the writer was changed to re-read before final write.
- P0028 ViDAR has a known Markdown omission: the code URL visible on PDF page 1 is absent from extracted Markdown; provenance is preserved in the manifest/report.
- Canonical content hashes use Python logical-byte I/O, not the host’s framed native view.
- LAW source facts are pinned to `BraveGroup/LAW@b2f6a784247072923c477ab92324d3aa5a9759bf`.
- WoTE source facts are pinned to `liyingyanUCAS/WoTE@298957c128a91d41a1c6075bd0bb6e7e845e093f`.

## Existing cross-session evidence

- `evidence/CORE_EVIDENCE_SNAPSHOT.md`
- `evidence/LEGACY_EXPERTISE_ASSETS.md`
- `audits/literature/P2R_TARGETED_FAILURE_DEEP_READ_ROUND1.md`

Use these as prior evidence, not substitutes for field reconstruction.

## Division of labor

- **GPT-5.6 Sol:** comparative anchor deep reads, cross-family synthesis, atlas/cards/state maintenance, targeted source audit when scientifically necessary.
- **Local corpus agent:** on-demand acquisition/extraction, MinerU/QC, local source-code execution, datasets/checkpoints/experiments.

Broad corpus acquisition remains frozen unless a Phase-B comparison identifies a concrete missing historical or technical link.