# CURRENT_STATE

Last updated: 2026-09-14 — Waves 1–4 CLOSED; Phase-C field synthesis first pass COMPLETE

## Research north star

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Planning is the center of gravity. Risk/predictive-risk expertise is optional prior knowledge, not a required destination.

Canonical rules: `state/RESEARCH_PRINCIPLES.md`.

## Methodological rule in force

```text
FIELD UNDERSTANDING FIRST
→ comparative anchor deep reads
→ cross-family synthesis
→ evidence QA
→ adversarial problem discovery
→ falsification
→ only then method design
```

P1/P2-R/P3 remain historical probes. They did not organize the field reconstruction and must not be revived automatically.

## Current active stage

```text
FIELD RECONSTRUCTION — PHASE C FIRST PASS COMPLETE
NEXT = PHASE D ADVERSARIAL PROBLEM DISCOVERY
```

Phase A status:

```text
P0001–P0060 registered
58 RAW_MD_READY
F1–F11 census coverage PASS
broad acquisition FROZEN
```

Phase B anchor program:

```text
Wave 1 CLOSED
Wave 2 CLOSED
Wave 3 CLOSED
Research QA Gate CLOSED
Wave 4 CLOSED
```

Canonical full synthesis:

```text
landscape/PHASE_C_WAVES1_4_FIELD_SYNTHESIS.md
```

## Wave 1 — historical / non-WM controls

Anchors:

```text
M2I
GameFormer
What Truly Matters in Trajectory Prediction?
UniAD
nuPlan
NAVSIM
DiffusionDrive
DriveSuprim
```

Stable controls:

```text
conditional response != causal/interventional response
matched controls > headline SOTA
future prediction quality != planning evidence
generative action != world model
candidate ranking is an independent bottleneck
evaluation regime is part of the scientific claim
```

## Wave 2 — world prediction → planning interface

Anchors:

```text
GAIA-1
Drive-WM
OccWorld
WoTE
ViDAR
LAW
```

Stable distinctions:

```text
controllable generation != planning interface
joint world-action generation != candidate consequence evaluation
action-conditioned != reactively supervised
WM-assisted planning != online model-based planning
world fidelity != decision utility
longer horizon != better planning
candidate-specific output != candidate-specific oracle supervision
```

High-confidence implementation facts:

```text
LAW predicted future latent is not consumed for current test-time trajectory selection = CODE VERIFIED
WoTE audited candidate target path uses fixed logged surrounding futures              = CODE VERIFIED
```

## Wave 3 — world–action coupling

Anchors:

```text
Epona
DrivingGPT
DriveLaW
Auto-JEPA
DA-WAM
Think2Drive
```

Stable interface map:

```text
Epona      = shared predictive representation / modular visual+trajectory heads
DrivingGPT = shared interleaved world-action causal sequence
DriveLaW   = online Video-DiT hidden state → Action DiT
Auto-JEPA  = predicted future ego intent → retrieval / scorer/gate
DA-WAM     = candidate_i → candidate-specific future latent_i → score_i
Think2Drive= learned latent world → imagined actor/critic rollouts → policy learning
```

QA correction:

```text
DriveLaW Stage-3 planning fine-tuning updates both Video DiT and Planning/Action DiT.
Do NOT describe it as frozen-video-features + separately trained planner.
```

DrivingGPT boundary:

```text
shared world/action causal sequence = VERIFIED
exact optimized NAVSIM runtime decode path = UNRESOLVED after public-source exhaustion
```

## Wave 4 — feedback / realism / reactivity

Anchors:

```text
Bench2Drive
HUGSIM
ORION
ReactSim-Bench
CausalDrive
```

Canonical synthesis:

```text
landscape/PHASE_B_WAVE4_SYNTHESIS.md
```

Wave-4 feedback decomposition:

```text
F_e = ego-state / dynamics feedback
F_s = sensor / viewpoint feedback
F_a = surrounding-agent state feedback
F_b = surrounding-agent behavioral-response feedback
```

Stable distinctions:

```text
photorealistic sensor realism != behavioral realism
interactive simulator != learned real-driver response model
log realism != reactive robustness
reactive feasibility != counterfactual behavioral truth
action conditioning != causal identification
strong closed-loop planning does not require explicit world rollout
```

Key placements:

```text
Bench2Drive    = standardized interactive CARLA policy benchmark
HUGSIM         = photorealistic reconstructed closed-loop simulator + external actor controllers
ORION          = VLA semantic/reasoning planner, not a world-model planner
ReactSim-Bench = learned behavior-WM reactivity measurement under external ego deviation
CausalDrive    = real-time learned action-conditioned reactive visual simulator
```

## Research QA Gate — CLOSED

Canonical artifact:

```text
audits/literature/RESEARCH_QA_GATE_CLOSEOUT.md
```

Priority-A outcome:

```text
A1 Epona      VERIFIED
A2 OccWorld   VERIFIED
A3 WoTE       VERIFIED + code boundary
A4 LAW        VERIFIED + code boundary
A5 DriveLaW   VERIFIED + CORRECTED Stage-3 semantics
A6 Auto-JEPA  VERIFIED
A7 DA-WAM     VERIFIED
A8 DrivingGPT paper-level VERIFIED / optimized runtime path UNRESOLVED
```

## Phase-C field synthesis — COMPLETE FIRST PASS

Canonical artifact:

```text
landscape/PHASE_C_WAVES1_4_FIELD_SYNTHESIS.md
```

The synthesis now answers the field-reconstruction completion questions at first-pass level:

```text
major families and historical transitions                       ANSWERED
observation→future→planner interfaces                            ANSWERED
supervision / alternative-action limitations                    ANSWERED
action-conditioning / reactivity / counterfactual distinctions  ANSWERED
evaluation-regime meanings                                      ANSWERED
strong non-WM controls                                          ANSWERED
recurring structural trade-offs                                 ANSWERED
counterexamples to broad claims                                 ANSWERED
under-measured evidence properties                              ANSWERED FIRST PASS
remaining contradictions / incomplete evidence                  MAPPED
```

## Project-wide stable field principles

```text
P-01 world-prediction quality is not itself planning evidence
P-02 future information is not automatically beneficial
P-03 candidate-specific output != candidate-specific observed counterfactual supervision
P-04 WM-assisted planning != online model-based planning
P-05 architectural coupling strength != causal-evidence strength
P-06 decision relevance != world completeness
P-07 generative action modeling != world modeling
P-08 candidate ranking/scoring is an independent bottleneck
P-09 closed-loop must be decomposed into feedback channels
P-10 sensor photorealism != behavioral realism
P-11 log realism != reactive robustness
P-12 reactive feasibility != counterfactual behavioral truth
P-13 action conditioning != causal validity
P-14 simulator quality and planner quality require separate evidence chains
P-15 semantic/VLA planning is a strong non-WM control for explicit-world-rollout claims
```

## Evidence gaps identified by Phase C — NOT research gaps yet

```text
1. real alternative-action surrounding-agent ground truth
2. reactive simulator quality → planner decision quality
3. simultaneous sensor-realistic + behaviorally validated closed loop
4. intervention-conditioned uncertainty calibration
5. long-horizon compounding under ego/sensor/agent/model feedback
6. compute-normalized planning benefit
7. representation semantics vs scale/capacity
8. real-vehicle closed-loop validation
9. standardized feedback-semantic reporting
10. planner robustness to world-model error
```

No item is selected as the research problem yet.

## Immediate next task

See `state/NEXT_TASK.md`.

Run **Phase D adversarial problem discovery** across the recurring tensions/evidence gaps. Every candidate must be attacked by prior art, non-WM controls, simpler explanations, counterexamples, measurement feasibility and realistic closed-loop relevance before it can survive.

## Still forbidden

```text
no method design
no forced risk-field insertion
no automatic P2-R/P3 revival
no choosing a gap because a module is absent
no treating an evidence gap as a research gap without showing planning consequence
```

## Research Brain architecture

GitHub is the Research Knowledge Authority. Raw MD + figures are the persistent GPT-readable primary-text layer; canonical PDFs remain source authority where archived/available.

A fresh session should read:

```text
START_HERE.md
state/CURRENT_STATE.md
state/NEXT_TASK.md
landscape/PHASE_C_WAVES1_4_FIELD_SYNTHESIS.md
audits/literature/RESEARCH_QA_GATE_CLOSEOUT.md
```
