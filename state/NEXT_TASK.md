# NEXT_TASK

## 唯一下一任务

> **Ingest and deep-read P0066 SAFE-SIM as the first Wave C.7 simulation/reactivity control. Keep research-direction convergence paused.**

Canonical expansion plan:

```text
landscape/WAM_DEEP_READ_EXPANSION_QUEUE_V1.md
```

Integrity audit:

```text
audits/research_synthesis/REPO_STATE_INTEGRITY_AUDIT_20260916.md
```

Current phase:

```text
broad WAM literature expansion     ACTIVE
Wave C.6                           CLOSED
Wave C.7                           ACTIVE
research-direction convergence     PAUSED
candidate-problem promotion        PAUSED
method design                      FORBIDDEN
```

Current normalized count:

```text
16 anchors complete
DriveLaW     COMPLETE
DA-WAM       COMPLETE
SafeDrive    COMPLETE
RiskWorld    COMPLETE
DriveReward  COMPLETE
SAFE-SIM     NEXT / NOT YET INGESTED
```

---

# Why SAFE-SIM is next

The first 16 anchors have already shown that these are different scientific objects:

```text
future-world prediction
explicit risk prediction
direct value/reward modeling
candidate scoring
planner coupling
```

The next under-covered axis is **reactivity**.

SAFE-SIM is selected to force the project to distinguish:

```text
planning WAM
vs
generative traffic simulator
```

and:

```text
logged / factual future modeling
vs
closed-loop endogenous behavioral response
```

The target paper is:

```text
SAFE-SIM: Safety-Critical Closed-Loop Traffic Simulation with Diffusion-Controllable Adversaries
ECCV 2024
arXiv:2401.00391
```

Stable ID correction:

```text
P0003 is already GraphAD
SAFE-SIM therefore receives reserved ID P0066
```

---

# Pre-read source gate — mandatory

Before scientific normalization:

```text
1. register P0066 in corpus manifest
2. verify canonical paper/version
3. verify official project / attributable code repository
4. create papers/raw_md/P0066_SafeSim/ readable primary-text layer
5. record source status
```

Do not create a fake source-complete status if paper/code ingestion is partial.

---

# Mandatory reconstruction

## 1. Simulator state and agent representation

Reconstruct exactly:

```text
scenario history
+ map / agent states / planner state
→ simulated agent-policy representation
```

Determine whether the model predicts joint futures once or repeatedly replans each agent in closed loop.

## 2. What actually closes the loop?

Trace feedback carriers:

```text
F_e = ego-state / dynamics feedback
F_s = sensor / viewpoint feedback
F_a = surrounding-agent state feedback
F_b = surrounding-agent behavioral-response feedback
```

For each, answer:

```text
present?
source?
updated each step?
learned or simulator-owned?
```

## 3. Diffusion / adversarial control semantics

Separate:

```text
diffusion denoising coordinate
physical simulation time
closed-loop replanning frequency
adversarial guidance objective
partial diffusion control
```

Never interpret denoising steps as physical future time.

## 4. Reactivity truth

Force explicit answers:

```text
Do non-ego agents respond to changed ego behavior?
Are those responses generated autoregressively / closed-loop?
What evidence says they are realistic rather than merely collision-inducing?
Is there any ground-truth intervention-response pair?
```

Important boundary:

```text
reactive simulator behavior
!=
causally identified counterfactual truth
```

## 5. Safety-critical generation

Audit how the adversarial agent is controlled:

```text
collision objective
collision type
aggressiveness
plausibility / realism constraint
partial diffusion
```

Identify which constraints preserve data-likelihood realism and which explicitly optimize planner failure.

## 6. Training graph

Separate:

```text
behavior-model training
scenario diffusion training
guidance at inference
planner under evaluation
```

Track whether planner gradients enter the simulator or adversarial generation process.

## 7. Inference / rollout graph

Reconstruct one full closed-loop episode:

```text
initial logged scenario
→ generate / update traffic actions
→ planner acts
→ simulator advances
→ all relevant agents observe updated state
→ regenerate / react
→ repeat
```

Specify exact replanning/update cadence if reported.

## 8. Evaluation regime

Separate:

```text
realism / distribution metrics
controllability metrics
collision / safety-critical generation success
planner evaluation
closed-loop behavioral validity
```

Do not treat higher planner failure rate as proof of more realistic simulation.

## 9. Immediate cross-paper comparison

Mandatory:

```text
SAFE-SIM vs RiskWorld
SAFE-SIM vs SafeDrive
SAFE-SIM vs WoTE / DA-WAM
SAFE-SIM vs HUGSIM / Bench2Drive where relevant
SAFE-SIM vs ProSim (next Wave C.7 anchor)
```

Primary scientific distinction:

```text
WAM asks how future knowledge improves ego planning.
SAFE-SIM asks how to generate realistic/reactive traffic environments for planner evaluation.
```

But shared mechanisms such as action conditioning, rollout, feedback and counterfactuality must be compared symmetrically.

## 10. Full Ontology V1.3 projection

Force-fill A–P.

Residue watch:

```text
Does simulator-level reactivity expose an irreducible dimension not represented by I04/I05, J09, O01/O07 or P04?
```

Do not create V1.4 unless a true residue survives back-projection.

---

# Required artifacts

After ingestion:

```text
papers/deep_analysis/P0066_SAFESIM_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C7_SAFESIM_AUDIT.md
landscape/P0066_SAFESIM_ONTOLOGY_PROJECTION.md
landscape/WAM_COMPARISON_MATRIX_V1_3_SAFESIM_EXTENSION.md
```

If official code is usable, additionally create/update source audit under:

```text
audits/literature/
```

with exact source/commit boundary.

---

# Stop condition

SAFE-SIM is complete only when:

```text
source/version gate resolved
+
closed-loop feedback graph explicit
+
reactivity vs counterfactual-truth distinction explicit
+
strongest realism/controllability evidence attributed
+
full A–P ontology projection complete
+
comparison against planning WAM anchors complete
```

Then advance to:

```text
P0067 ProSim
```

---

# Guardrail

This is still field reconstruction / literature expansion.

Do not use SAFE-SIM to prematurely justify a research direction. Its role is to improve the coordinate system for reactivity, simulator truth and feedback semantics.
