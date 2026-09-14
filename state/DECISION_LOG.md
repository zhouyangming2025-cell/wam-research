# DECISION_LOG

Newest entry first.

---

## 2026-09-14 — Waves 1–4 field reconstruction synthesized; Phase D authorized

**Decision**

The representative-anchor field reconstruction is sufficiently complete at first-pass level to move from understanding the field into adversarial problem discovery.

```text
Wave 1            CLOSED
Wave 2            CLOSED
Wave 3            CLOSED
Research QA Gate  CLOSED
Wave 4            CLOSED
Phase C synthesis COMPLETE FIRST PASS
Phase D           AUTHORIZED
```

Canonical synthesis:

- `landscape/PHASE_C_WAVES1_4_FIELD_SYNTHESIS.md`
- `landscape/PHASE_B_WAVE4_SYNTHESIS.md`

**Stable field-level result**

Planning-centric WAM is not one architecture. The relevant scientific variable is where predictive/world information enters the decision process:

```text
training-only predictive shaping
online predictive state → direct planner
joint world-action generation
planning-oriented future compression
candidate action → predicted future → score
learned world → policy imagination
learned interactive simulator
```

The synthesis also fixes the main evidence distinctions:

```text
world completeness != decision relevance
action conditioning != reactive supervision != counterfactual truth
candidate-specific output != candidate-specific observed counterfactual supervision
closed-loop != one feedback regime
sensor photorealism != behavioral realism
log realism != reactive robustness
simulator quality != planner decision quality
```

**Problem-discovery authorization boundary**

Phase D may now evaluate recurring tensions/evidence gaps as candidate research problems, but no item is preselected. Every candidate must survive historical prior art, strong non-WM controls, simpler explanations, counterexamples, measurement feasibility and realistic closed-loop relevance.

Method design remains forbidden until a problem survives falsification.

---

## 2026-09-14 — Wave 2 closed; Wave 3 authorized

**Decision**

Wave 2 is scientifically stable enough to close after primary-text comparison plus decision-critical source-code audits.

```text
Wave-2 comparative first pass    = COMPLETE
planning-interface audit         = COMPLETE
comparability/attribution audit  = COMPLETE
supervision-source audit         = COMPLETE
Wave 2                            = CLOSED
Wave 3                            = AUTHORIZED
```

Canonical Wave-2 artifacts:

- `landscape/PHASE_B_WAVE2_SYNTHESIS.md`
- `landscape/PHASE_B_WAVE2_COMPARABILITY_AUDIT.md`
- `audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md`

**Stable Wave-2 interpretation**

The phrase `world model helps planning` is too coarse. The reviewed mechanisms include controllable generation (GAIA-1), visual-future candidate evaluation (Drive-WM), joint occupancy+ego generation (OccWorld), online BEV-future candidate evaluation (WoTE), predictive pretraining (ViDAR), and action-aware auxiliary latent prediction (LAW).

Evidence boundaries now explicit:

- Drive-WM: future-based selection is operational, but visual-generation fidelity is not isolated from perception/reward/candidate design.
- OccWorld: main SOTA rows are heterogeneous; internal representation/dynamics ablations are stronger evidence. Better reconstruction can coexist with worse forecasting/planning.
- WoTE: future-state-on/off is strong matched NAVSIM evidence, but the audited PDM supervision uses fixed logged surrounding-agent futures across ego candidates.
- ViDAR: predictive pretraining transfers the History/BEV encoder; the future decoder is not the deployed planning interface.
- LAW: source code shows the current waypoint is generated before future-latent prediction and test-time planning discards latent outputs; the mechanism is representation shaping, not online rollout evaluation.
- Longer horizon and higher world fidelity are not reliable monotonic proxies for planning value.

**Why Wave 3 now**

Wave 2 established the planning-interface taxonomy. Wave 3 can now compare tighter world/action coupling without treating all WAMs as equivalent.

Wave-3 anchors:

```text
Epona
DrivingGPT
DriveLaW
Auto-JEPA
DA-WAM
Think2Drive
```

Canonical plan: `landscape/PHASE_B_WAVE3_PLAN.md`.

Research-gap and method design remain closed.

---

## 2026-09-14 — Wave 1 closed after historical/control comparability audit

**Decision**

The historical/non-WM/evaluation baseline is stable enough to use as a control layer for modern WAM interpretation.

Canonical artifacts:

- `landscape/PHASE_B_WAVE1_SYNTHESIS.md`
- `landscape/PHASE_B_WAVE1_COMPARABILITY_AUDIT.md`

Binding controls:

```text
conditional future != intervention
matched controls > headline SOTA
candidate ranking is an independent planning bottleneck
multimodal action generation != world modeling
prediction accuracy != planning evidence
evaluation regime is part of the claim
```

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

The P0021–P0034 coverage set placed Hydra-MDP / DriveSuprim / iPad as non-WM controls; DriveVLM / OmniDrive / ORION as VLM/VLA planning controls; Think2Drive as latent-WM-for-RL; ViDAR as predictive pretraining; GenAD as joint ego/agent trajectory-generation precursor; and nuScenes / nuPlan / NAVSIM / Bench2Drive / HUGSIM as evaluation-history anchors.

**Why Phase A is sufficient**

Representative coverage exists across visual/video, occupancy/BEV, latent/JEPA, direct WM-assisted planning, candidate-conditioned futures, unified world-action, historical interaction/prediction-planning, reactive/WM-RL, value/safety interfaces, strong non-WM planners, and benchmark/evaluation families.

Remaining weaknesses are comparative questions rather than missing census families. New papers may be added only when a named Phase-B comparison exposes a concrete missing link.

---

## 2026-09-14 — Phase-A breadth target reached; stop bulk acquisition

The corpus reached:

```text
P0001–P0060 registered
58 RAW_MD_READY
2 lawful-source blockers
```

Broad acquisition was paused pending scientific placement; the later Phase-A closeout converted that pause into a freeze.

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

P1/P2-R/P3 are retained only as historical probes.

---

## 2026-09-13 — Planning-centric scope + problem-first rule

Research identity:

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Risk/predictive-risk expertise is optional prior knowledge, not a required destination. Every paper must be treated symmetrically for strongest evidence, strongest limitation, what it proves, what it does not prove, and evaluation boundary.

---

## 2026-09-13 — P2-R Round-1 adjudication (historical)

The earlier targeted audit found no direct observed reaction-induced action-order inversion in the reviewed set. P2-R is parked and no longer organizes reading.

Full audit: `audits/literature/P2R_TARGETED_FAILURE_DEEP_READ_ROUND1.md`.

---

## 2026-09-13 — Scientific workflow takeover

The private GitHub repo is the canonical cross-session Research Brain. GPT-5.6 Sol handles scientific reading/synthesis/state; the local corpus agent handles acquisition/conversion/QC/local execution.

---

## 2026-09-13 — Long-term source architecture

Canonical PDFs remain local/NAS when archived; raw Markdown + figures are the GPT-readable cross-session primary-text layer; exact wording/formulas/figures are verified against canonical/official PDFs when needed. Canonical hashes use Python logical-byte I/O; the Windows native +1024 framed view is a known host quirk.