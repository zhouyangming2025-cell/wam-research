# RESEARCH_LEDGER

Running factual ledger of assets, research-state transitions and scientific gates.

## Current research stage

```text
FIELD RECONSTRUCTION — PHASE C FIRST PASS COMPLETE
NEXT: PHASE D ADVERSARIAL PROBLEM DISCOVERY
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
- `landscape/PHASE_B_WAVE3_CLOSEOUT.md`
- `landscape/PHASE_B_WAVE4_SYNTHESIS.md`
- `audits/literature/RESEARCH_QA_GATE_CLOSEOUT.md`
- `landscape/PHASE_C_WAVES1_4_FIELD_SYNTHESIS.md`

## Hypotheses

| hypothesis | status | role | file |
|---|---|---|---|
| P1_RETIRED — Planner-Induced Model Exploitation / Search-Support Gap | RETIRED | historical hypothesis / robustness evidence | `hypotheses/P1_RETIRED.md` |
| P2R_PRIMARY — Reactive Action-Ordering Gap | PARKED PROBE | diagnostic lens only; not active search target | `hypotheses/P2R_PRIMARY.md` |
| P3_HOLD — Decision Sufficiency of World Representations | PARKED BACKUP PROBE | possible later synthesis question | `hypotheses/P3_HOLD.md` |

No historical hypothesis is automatically revived by Phase C.

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
| 2026-09-14 | Phase-A Census / corpus closeout | P0001–P0060 + F1–F11 atlas | **PASS**; broad expansion frozen; representative anchors selected |
| 2026-09-14 | Phase-B Wave 1 | M2I, GameFormer, What Truly Matters, UniAD, nuPlan, NAVSIM, DiffusionDrive, DriveSuprim | **CLOSED**; historical/non-WM/evaluation control baseline stable |
| 2026-09-14 | Phase-B Wave 2 | GAIA-1, Drive-WM, OccWorld, WoTE, ViDAR, LAW | **CLOSED**; world/future→planning interface taxonomy + attribution/supervision boundaries stable |
| 2026-09-14 | Phase-B Wave 3 | Epona, DrivingGPT, DriveLaW, Auto-JEPA, DA-WAM, Think2Drive | **CLOSED**; six world/action planning interfaces mapped |
| 2026-09-14 | Research QA Gate | Priority-A A1–A8 | **CLOSED**; DriveLaW Stage-3 semantics corrected; DrivingGPT runtime path explicitly unresolved |
| 2026-09-14 | Phase-B Wave 4 | Bench2Drive, HUGSIM, ORION, ReactSim-Bench, CausalDrive | **CLOSED**; feedback/realism/reactivity coordinate system established |
| 2026-09-14 | Phase C | Waves 1–4 cross-family synthesis | **FIRST PASS COMPLETE**; ten reconstruction questions answered; Phase D authorized |

## Wave-1 ledger result

Wave 1 established binding controls:

```text
interaction-conditioned prediction already existed
joint prediction/planning already existed
prediction metrics can mis-rank driving performance
planning-oriented multi-task representation already existed
multimodal direct action generation can be strong without WM
candidate ranking can be strong without WM
OL / non-reactive / reactive evaluation are different claims
```

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

Stable evidence conclusions:

1. Generation quality is not planning evidence.
2. Better world reconstruction is not monotonic with planning utility.
3. Future-state input can add value beyond scorer-only in matched WoTE ablation.
4. Candidate-specific prediction is not reactive oracle supervision.
5. Predictive pretraining can help without an online WM.
6. Auxiliary future prediction can help without online rollout.
7. Longer future horizon is not monotonically better.

## Wave-3 ledger result

Six planning interfaces:

```text
Epona       shared predictive representation / modular heads
DrivingGPT  shared world-action causal sequence
DriveLaW    online world hidden state → action generator
Auto-JEPA   future ego-intent latent → retrieval / selection
DA-WAM      action candidate → future latent → score
Think2Drive learned world → imagination → actor/critic policy learning
```

Stable conclusions:

```text
architectural coupling strength != evidence strength
future information has no universal positive sign
planning-oriented compression is a legitimate WM branch
candidate-specific future output exceeds available candidate-specific observed supervision
WM value can come through policy training, not only deployed candidate evaluation
```

QA correction:

```text
DriveLaW Stage-3 planner training updates both Video DiT and Planning/Action DiT.
```

## Wave-4 ledger result

Feedback decomposition:

```text
F_e = ego-state / dynamics feedback
F_s = sensor / viewpoint feedback
F_a = surrounding-agent state feedback
F_b = surrounding-agent behavioral-response feedback
```

Stable placements:

```text
Bench2Drive    interactive CARLA E2E policy benchmark
HUGSIM         reconstructed photorealistic closed-loop simulator; actor behavior external/controller-defined
ORION          VLA semantic/reasoning planner; no explicit world rollout
ReactSim-Bench learned behavior-WM reactivity benchmark under externally deviated ego behavior
CausalDrive    real-time learned action-conditioned reactive visual simulator
```

Stable distinctions:

```text
sensor photorealism != behavioral realism
log realism != reactive robustness
reactive feasibility != counterfactual behavioral truth
action conditioning != causal identification
simulator quality != planner quality
```

## Phase-C ledger result

Canonical synthesis:

`landscape/PHASE_C_WAVES1_4_FIELD_SYNTHESIS.md`

Planning-centric WAM is now represented by seven main interfaces:

```text
I1 training-only predictive shaping
I2 online predictive state → direct planner
I3 joint world-action generation
I4 planning-oriented future compression
I5 candidate consequence evaluation
I6 imagined environment for policy learning
I7 learned interactive simulator
```

Project-wide stable field principles now include:

```text
world-prediction quality != planning evidence
future information is interface-conditional
candidate-specific output != candidate-specific observed counterfactual supervision
WM-assisted planning != online model-based planning
world completeness != decision relevance
closed-loop must be decomposed by feedback channels
sensor realism != behavioral realism
log realism != reactive robustness
reactive feasibility != counterfactual truth
simulator evidence and planner evidence require separate chains
```

Phase C identified ten **evidence gaps**, not research gaps, including alternative-action behavioral GT, simulator→planner decision linkage, calibrated intervention-conditioned uncertainty, long-horizon coupled feedback, compute-normalized benefit and world-model-error robustness.

Phase D is authorized to attack these as possible research problems. `NONE / EVIDENCE INSUFFICIENT` remains valid.

## Integrity notes

- Raw-MD conversion ledger race was detected, repaired from stored artifacts, and the writer was changed to re-read before final write.
- P0028 ViDAR has a known Markdown omission: the code URL visible on PDF page 1 is absent from extracted Markdown; provenance is preserved in the manifest/report.
- Canonical content hashes use Python logical-byte I/O, not the host’s framed native view.
- LAW source facts are pinned to `BraveGroup/LAW@b2f6a784247072923c477ab92324d3aa5a9759bf`.
- WoTE source facts are pinned to `liyingyanUCAS/WoTE@298957c128a91d41a1c6075bd0bb6e7e845e093f`.
- DrivingGPT optimized NAVSIM runtime path remains explicitly unresolved because the official code link is unavailable.

## Existing cross-session evidence

- `evidence/CORE_EVIDENCE_SNAPSHOT.md`
- `evidence/LEGACY_EXPERTISE_ASSETS.md`
- `audits/literature/P2R_TARGETED_FAILURE_DEEP_READ_ROUND1.md`
- `audits/literature/RESEARCH_QA_GATE_CLOSEOUT.md`

Use these as prior evidence, not substitutes for field reconstruction.

## Division of labor

- **GPT-5.6 Sol:** comparative anchor deep reads, cross-family synthesis, problem-discovery/falsification, atlas/cards/state maintenance, targeted source audit when scientifically necessary.
- **Local corpus agent:** on-demand acquisition/extraction, MinerU/QC, local source-code execution, datasets/checkpoints/experiments.

Broad corpus acquisition remains frozen unless Phase D identifies a concrete missing prior-art or measurement link.