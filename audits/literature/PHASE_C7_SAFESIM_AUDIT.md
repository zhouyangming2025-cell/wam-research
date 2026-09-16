# Phase C.7 SAFE-SIM Audit

Last updated: 2026-09-16

Status: **COMPLETE FIRST PASS — PAPER + OFFICIAL SOURCE VERIFIED**

Paper:

```text
SAFE-SIM: Safety-Critical Closed-Loop Traffic Simulation with Diffusion-Controllable Adversaries
ECCV 2024
arXiv:2401.00391
```

Official source:

```text
jxmmy7777/safe-sim
ref 27c96a84e7bf5fbca4b47f6edde386811d76c6e7
```

Canonical analysis:

```text
papers/deep_analysis/P0066_SAFESIM_DEEP_ANALYSIS_V2.md
audits/literature/P0066_SAFESIM_SOURCE_CODE_AUDIT.md
```

---

# 1. Stable mechanism judgment

SAFE-SIM is a:

```text
REACTIVE CLOSED-LOOP TRAFFIC BEHAVIOR SIMULATOR
+
PLANNER-CONDITIONED ADVERSARIAL DIFFUSION GENERATOR
```

It is not primarily an ego-planning WAM.

Core cycle:

```text
scene observation
→ ego planner
→ current ego future plan
→ reactive diffusion agents + adversarial guidance
→ selected joint actions
→ environment state update
→ new scene observation
→ replan all relevant actors
→ repeat
```

---

# 2. What actually closes the loop?

Code-verified feedback:

```text
F_e  ego physical state feedback                 PRESENT
F_a  surrounding-agent physical state feedback  PRESENT
F_b  surrounding behavioral-response feedback   PRESENT
F_s  sensor/viewpoint rendering feedback         NOT CORE / ABSENT as photorealistic sensor loop
```

Most important code fact:

```text
current ego planner trajectory
→ obs["agents"]["ego_plan"]
→ non-ego policy / guidance
```

Therefore surrounding behavior is regenerated against the currently planned ego path rather than replayed from one fixed logged future.

---

# 3. Reactivity truth boundary

SAFE-SIM has genuine simulator-level reactivity:

```text
changed ego/environment state
→ changed non-ego policy input
→ regenerated non-ego behavior
```

But it lacks the stronger truth object:

```text
same factual scene
+ alternative real ego intervention
+ observed real surrounding response
```

Canonical vector:

```text
candidate/intervention-conditioned generated response   YES
closed-loop endogenous surrounding response             YES
paired real intervention-response supervision           NO
causal counterfactual identification                    NO
```

This distinction is central to Wave C.7.

---

# 4. Training vs inference

Training:

```text
real-world traffic trajectories
→ diffusion behavior prior
```

Inference:

```text
base diffusion sample
+ planner-conditioned guidance
+ optional partial-diffusion proposal
+ sample filtering
→ simulated reactive trajectory
```

The most safety-critical behavior therefore comes from a combination of learned prior and test-time optimization.

Do not attribute all behavior to the learned diffusion model itself.

---

# 5. Planner-gradient boundary

The planner produces a trajectory used by the simulator's guidance objective.

Audited source shows guidance gradients update sampled reactive-agent actions.

No path was identified that updates planner parameters through the simulator.

Thus:

```text
planner → simulator condition      YES
simulator guidance → planner grad  NO
```

SAFE-SIM is a planner-evaluation environment, not differentiable joint planner training in the audited configuration.

---

# 6. Internal diffusion time vs physical time

Paper setting:

```text
K = 100 diffusion steps
```

Closed-loop planner/agent update:

```text
2 Hz in reported experiments
```

These must never be conflated.

```text
diffusion k
= denoising coordinate

physical t
= environment trajectory time
```

Partial diffusion `k_p = γK` is likewise an internal generative/noise location, not a future-world timestep.

---

# 7. Partial diffusion audit

Mechanism:

```text
rule/domain proposal targeting collision type
→ add configured diffusion noise
→ guided denoise
→ proposal-biased but data-prior-regularized trajectory
```

Reported evidence:

```text
Jadv + Jreg, no partial    collision-point var 1.62
Jadv + Jreg + partial      collision-point var 5.44
```

Main supported conclusion:

```text
partial diffusion improves adversarial outcome diversity / collision-type controllability
```

It is not evidence of more accurate future prediction.

---

# 8. Regularization trade-off

Ablation:

```text
Jadv + Jreg    collision 23.9% | adv offroad 13.8% | realism 0.58
Jadv only      collision 53.5% | adv offroad 23.1% | realism 0.58
```

Interpretation:

```text
removing regularization increases adversarial success
but also substantially increases invalid/off-road adversary behavior
```

Therefore:

```text
attack success != simulator quality
```

---

# 9. Realism evidence boundary

The main realism metric is Wasserstein distance between distributions of:

```text
longitudinal acceleration
lateral acceleration
jerk
```

This is useful distributional motion evidence.

It is not:

```text
paired trajectory error under the same intervention
social-response causal validity
episode-level fault realism
```

Thus claims of `realistic reactive behavior` should be read as supported by distributional/qualitative evidence, not by intervention-ground-truth validation.

---

# 10. Baseline evidence

Rule-based planner / nuScenes:

```text
SAFE-SIM   Collision 43.2 | Realism 0.38
STRIVE     Collision 36.4 | Realism 0.85
DiffScene  Collision 18.2 | Realism 0.52
```

nuPlan zero-shot:

```text
SAFE-SIM   Collision 80.0 | Realism 0.27
DiffScene  Collision 56.7 | Realism 0.42
```

This directly supports better adversarial collision generation plus better aggregate motion-profile distribution under the tested setups.

It does not establish causal-response fidelity.

---

# 11. Planner-specific evidence boundary

Reported ego-adversary collision rates differ across planners:

```text
BC          38.8
IDM         49.3
Lane-Graph  34.3
BITS        16.4
PDM-Closed  26.9
```

Use these only as evidence that SAFE-SIM can adapt scenarios across planner classes.

Do NOT use them as a standalone planner ranking because simulator attack dynamics and planner interfaces differ.

The paper itself reports cases where the ego is not at fault.

---

# 12. Comparison controls

## SAFE-SIM vs RiskWorld

```text
RiskWorld:
observational history → factual future rollout → risk
no changed-ego reactive loop

SAFE-SIM:
changed ego plan → generated surrounding response → state update → replan
```

Scientific axis:

```text
factual future supervision ⟂ intervention reactivity
```

## SAFE-SIM vs SafeDrive

```text
SafeDrive:
inside planner; evaluate candidate safety consequences

SAFE-SIM:
outside planner; generate reactive environment for planner evaluation
```

## SAFE-SIM vs WoTE / DA-WAM

```text
WoTE / DA-WAM:
multiple hypothetical candidates evaluated inside one planning decision

SAFE-SIM:
one acting planner interacts sequentially with a changing learned environment
```

## SAFE-SIM vs DriveReward

```text
DriveReward:
direct compressed candidate value

SAFE-SIM:
explicit interactive behavior generation
```

---

# 13. Strongest scientific contribution to the atlas

SAFE-SIM sharpens `reactivity` from a vague label into an operational feedback topology.

The field now needs at least three distinct truth objects:

```text
1. factual logged-future truth
2. model-generated response under changed action
3. observed intervention-response truth
```

SAFE-SIM possesses (2), is trained using observational evidence related to (1), but does not possess (3).

This is stronger than non-reactive action-conditioned WAMs while still falling short of causal counterfactual identification.

---

# 14. What SAFE-SIM proves

- repeated planner/agent closed-loop interaction is implemented;
- ego planner trajectory explicitly influences adversarial/reactive trajectory generation;
- inference-time guidance can target planner-specific safety-critical behavior;
- partial diffusion materially increases collision diversity;
- realism regularization prevents some pathological adversarial behavior;
- the reported behavior prior transfers to nuPlan evaluation without fine-tuning in the tested setup.

# 15. What SAFE-SIM does not prove

- paired real-world counterfactual responses;
- unbiased planner ranking from collision rate;
- sensor-photorealistic feedback;
- calibrated behavioral uncertainty;
- universal OOD validity under aggressive ego actions;
- differentiable planner improvement through the simulator;
- that all safety-critical generated episodes are fault-valid or socially realistic.

---

# Final audit verdict

```text
SAFE-SIM is a genuine reactive closed-loop learned traffic simulator,
not merely a static conditional future predictor.

Its strongest evidence establishes planner-conditioned behavioral feedback,
not causal counterfactual truth.
```

Ontology decision:

```text
V1.3 RETAINED
NO V1.4
```
