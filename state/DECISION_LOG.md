# DECISION_LOG

Newest entry first.

---

## 2026-09-14 — Phase-A field census closed; Phase-B representative deep reads authorized

**Decision**

Phase A is closed at census depth.

```text
F1–F11 coverage audit = PASS
broad acquisition = FROZEN
Phase-B anchors = 25 representative works
research-gap selection = still CLOSED
method design = still CLOSED
```

Canonical artifacts:

- `landscape/CENSUS_PHASE_A_ROUND2.md`
- `landscape/FIELD_ATLAS.md`
- `landscape/PHASE_B_ANCHORS.md`

**Evidence integrated in closeout**

The newly ingested P0021–P0034 coverage set was scientifically placed from repo-hosted primary text:

- Hydra-MDP, DriveSuprim, iPad — strong non-WM planning/scoring/proposal controls;
- DriveVLM, OmniDrive, ORION — VLM/VLA planning and supervision controls, not automatically world models;
- Think2Drive — latent WM as Dreamer-style RL training simulator;
- ViDAR — future prediction as pretraining objective;
- GenAD — joint ego/agent trajectory-generation precursor;
- nuScenes, nuPlan, NAVSIM, Bench2Drive, HUGSIM — benchmark/evaluation lineage.

**Why Phase A is sufficient**

The project can now place representative methods across visual/video, occupancy/BEV, latent/JEPA, direct WM-assisted planning, candidate-conditioned futures, unified world-action, historical interaction/prediction-planning, reactive/WM-RL, value/safety interfaces, strong non-WM planners, and benchmark/evaluation families.

The remaining weaknesses are comparative questions rather than missing census families:

1. standardized real-vehicle closed-loop evidence is sparse;
2. multimodality/uncertainty reaches the planner in heterogeneous ways;
3. visual simulator fidelity and behavioral-agent realism are separate dimensions.

Adding papers indiscriminately would now reduce, not increase, scientific efficiency.

**Key corrections earned by the closeout**

- The original nuScenes paper is a multimodal scene/perception benchmark, not an end-to-end planning benchmark; later literature retrofits open-loop planning protocols onto the logs.
- VLA/VLM planning is adjacent to WAM but not synonymous with environment transition modeling.
- Future prediction can serve pretraining, inference representation, candidate evaluation, joint world-action modeling, or RL policy learning; these are distinct scientific roles.
- Strong planning without an explicit WM must remain a first-class control branch.

**Phase-B strategy**

Read in comparative waves rather than producing 25 isolated summaries.

Wave 1 establishes the historical/non-WM/evaluation baseline:

```text
M2I
GameFormer
What Truly Matters
UniAD
nuPlan
NAVSIM
DiffusionDrive
DriveSuprim
```

Required artifact: `landscape/PHASE_B_WAVE1_SYNTHESIS.md`.

**What would reopen breadth acquisition**

Only a named Phase-B comparison that cannot be resolved from the existing corpus and identifies a specific missing historical or technical link. Corpus size itself is no reason to add papers.

---

## 2026-09-14 — Phase-A breadth target reached; stop bulk acquisition and close by scientific placement

**Decision**

The corpus reached the planned Phase-A breadth scale at infrastructure level:

```text
P0001–P0060 registered
58 RAW_MD_READY
2 lawful-source blockers
```

Broad acquisition was paused pending scientific placement, F1–F11 coverage audit and anchor selection. This gate is now completed by the decision above.

---

## 2026-09-14 — Field-reconstruction reset: stop hypothesis-first gap hunting

**Decision**

The project will no longer organize literature review around finding, rescuing, or killing a preselected gap.

Active program:

```text
reconstruct field
→ representative anchor deep reads
→ cross-family synthesis
→ only then research-problem discovery
```

P1/P2-R/P3 are retained only as historical probes. The previous analyses remain useful evidence, but they are not sufficient basis for choosing a research problem.

---

## 2026-09-13 — Planning-centric scope + problem-first rule

**Decision**

Research identity:

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Risk/predictive-risk expertise is optional prior knowledge, not a required destination. Every paper must be treated symmetrically for strongest evidence, strongest limitation, what it proves, what it does not prove, and evaluation boundary.

---

## 2026-09-13 — P2-R Round-1 adjudication (historical)

The earlier targeted audit found no direct observed reaction-induced action-order inversion in the reviewed set. P2-R is now parked and no longer organizes reading.

Full audit: `audits/literature/P2R_TARGETED_FAILURE_DEEP_READ_ROUND1.md`.

---

## 2026-09-13 — Scientific workflow takeover

The private GitHub repo is the canonical cross-session Research Brain. GPT-5.6 Sol handles scientific reading/synthesis/state; the local corpus agent handles acquisition/conversion/QC/local execution.

---

## 2026-09-13 — Long-term source architecture

Canonical PDFs remain local/NAS when archived; raw Markdown + figures are the GPT-readable cross-session primary-text layer; exact wording/formulas/figures are verified against canonical/official PDFs when needed. Canonical hashes use Python logical-byte I/O; the Windows native +1024 framed view is a known host quirk.