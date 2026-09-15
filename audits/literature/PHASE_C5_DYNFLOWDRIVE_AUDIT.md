# Phase C.5 DynFlowDrive Audit

Last updated: 2026-09-15

Status: **COMPLETE FIRST PASS — PAPER VERIFIED / SOURCE IMPLEMENTATION UNAVAILABLE**

Paper:

```text
DynFlowDrive: Flow-Based Dynamic World Modeling for Autonomous Driving
arXiv:2603.19675v2
```

Official repository:

```text
xiaolul2/DynFlowDrive
latest observed commit: c665dc577a0939543fa7abe64d28eadaec28283c
```

As of 2026-09-15 the repository still contains README/teaser only and states that code will be released once accepted.

Canonical deep read:

```text
papers/deep_analysis/P0063_DYNFLOWDRIVE_DEEP_ANALYSIS_V2.md
```

---

# 1. Stable mechanism judgment

DynFlowDrive is **not** an online model-based candidate evaluator at deployment.

Training:

```text
planner observation
→ candidate trajectories + score head

current world latent + candidate trajectory
→ training-only rectified-flow world model
→ predicted latent endpoint / transport velocities

GT trajectory error
+ future-latent reconstruction
+ flow-direction stability
→ candidate criterion C_n
→ n* training label
→ score-head supervision

trajectory + score + reconstruction + flow losses
→ joint optimization
```

Inference:

```text
observation
→ candidate trajectories + learned scores
→ highest-score candidate

world model = OFF
future latent = NOT COMPUTED
flow stability = NOT COMPUTED
```

Canonical subtype:

```text
TRAINING-ONLY FLOW-DYNAMICS MODE-SUPERVISION WAM
```

---

# 2. CLAIM → EVIDENCE → INTERPRETATION → UNPROVEN

## Claim A — rectified flow models continuous trajectory-conditioned world dynamics

**AUTHOR CLAIM**

The learned velocity field represents how the latent world progressively evolves under different ego trajectories.

**DIRECT PAPER EVIDENCE**

```text
current/factual-next latent pair
→ noised current anchor a
→ interpolation x_s=(1-s)a+s z_{t+1}
→ trajectory-conditioned Transformer velocity field F_theta
→ Euler integration over s
```

Ablation:

```text
Static WM  0.61 Avg L2 / 0.30 Avg CR
Flow WM    0.59        / 0.26
```

**OUR INTERPRETATION**

The paper demonstrates that a rectified-flow parameterization is more useful than the matched static-WM baseline for downstream planning inside this framework.

**REMAINS UNPROVEN**

```text
s is not directly identified with physical time;
intermediate s states have no observed intermediate-time targets;
vector-field direction consistency is not directly a physical-motion variable.
```

---

## Claim B — stability-aware flow dynamics improve trajectory selection

**AUTHOR CLAIM**

Lower angular change between successive normalized flow velocities indicates smoother, more physically plausible world evolution and supports safer candidate selection.

**DIRECT PAPER EVIDENCE**

Selection ablation:

```text
none              0.61 L2 / 0.30 CR
L2 only           0.59    / 0.24
+ reconstruction  0.58    / 0.22
+ flow stability  0.57    / 0.22
```

**OUR INTERPRETATION**

The full selection bundle helps substantially. The *incremental* flow-stability term itself contributes a small L2 gain and no further reported CR gain beyond reconstruction in Table 5b.

**REMAINS UNPROVEN**

The ablation does not show that the angular flow metric is a calibrated measure of physical safety or that it is the dominant source of final planning gain.

---

## Claim C — multiple candidate trajectories induce different world evolutions

**DIRECT PAPER EVIDENCE**

Each candidate trajectory is separately embedded and conditions the shared flow network.

**SUPERVISION AUDIT**

The future target is one factual `z_{t+1}` extracted from the actually observed next frame.

Therefore:

```text
candidate-specific output              YES
candidate-specific factual future GT   NO
reactive alternative-agent truth       NO / NOT ESTABLISHED
```

**BOUNDARY**

Action conditioning does not establish counterfactual correctness.

---

## Claim D — no additional inference overhead

**DIRECT PAPER EVIDENCE**

The paper explicitly removes the world model at inference and uses only the learned score head for candidate selection.

Table 3:

```text
baseline / WM-only rows  13.8 FPS
MS-containing rows       13.6 FPS
```

**INTERPRETATION**

Flow integration itself contributes zero deployment-time world-model depth. The remaining planner/score path still has ordinary multimodal-planner cost.

**BOUNDARY**

`no online world-model overhead` is stronger and more precise than `zero overhead of the whole method`.

---

# 3. Three-time-axis audit

DynFlowDrive forces separation of:

```text
physical time tau:
    actual t → t+1 scene evolution

flow time s:
    mathematical transport from anchor a → target latent

planner iteration k:
    internal query/candidate refinement
```

The paper's intermediate flow states are indexed by `s`, not by observed physical timestamps.

Binding control:

```text
more flow solver steps
!=
more future physical timesteps
```

This motivates ontology amendment **F08**.

---

# 4. Mathematical ambiguity requiring code audit

Official arXiv v2 states:

```text
Eq.7:
x_s = (1-s)a + s z_{t+1}
```

which implies:

```text
dx_s/ds = z_{t+1}-a
```

but Eq.10 trains against:

```text
(1-s)(z_{t+1}-a)
```

The text then calls that target the displacement along the interpolation path.

This is mathematically inconsistent as written.

A second ambiguity:

```text
training path starts from noised anchor a
sampling text says integration starts from z_t
```

Code is unavailable, so both remain:

```text
PAPER EQUATION / PROCEDURE AMBIGUITY
SOURCE VERIFICATION BLOCKED
```

Do not infer the implementation.

---

# 5. Representation-prior attribution

Table 4:

```text
Static WM                    0.61 / 0.30
Flow WM                      0.59 / 0.26
Flow WM + World Feat Design  0.57 / 0.22
```

The final system therefore bundles:

```text
flow parameterization
+
pretrained/foundation VAE world features
```

The imported representation prior is a separate causal contribution.

---

# 6. Headline-result comparability attack

The paper highlights SSR improvement from:

```text
0.39 → 0.31 Avg L2
```

but Table 1 shows:

```text
SSR*                            0.39 / 0.15
DynFlowDrive(SSR)               0.35 / 0.14
DynFlowDrive(SSR) + ego status  0.31 / 0.11
```

The marked final row uses ego status according to the table footnote.

Therefore the more matched DynFlowDrive-vs-SSR delta is:

```text
0.39 → 0.35 L2
0.15 → 0.14 CR
```

The 0.31/0.11 headline row includes an extra input and should not be used as a pure world-model effect.

---

# 7. Evaluation-regime correction

Paper wording:

```text
"Closed-loop NavSim Benchmark"
```

Project-standard classification:

```text
NAVSIM v1
= NON-REACTIVE DATA-DRIVEN / PSEUDO-SIMULATION PLANNING EVALUATION
```

The paper itself cites NAVSIM's `non-reactive autonomous vehicle simulation and benchmarking` work.

Therefore:

```text
88.7 PDMS
supports non-reactive data-driven planning quality

NOT reactive behavioral-response validation
NOT counterfactual-agent-response validation
```

---

# 8. Strongest matched evidence

Primary flow mechanism control:

```text
Static WM → Flow WM
0.61/0.30 → 0.59/0.26
```

Primary representation-prior control:

```text
Flow WM → + World Feat Design
0.59/0.26 → 0.57/0.22
```

Primary selection-control ladder:

```text
none → L2 → +reconstruction → +flow stability
0.61/0.30
→ 0.59/0.24
→ 0.58/0.22
→ 0.57/0.22
```

Flow integration curve:

```text
1 step   0.60/0.28
3        0.59/0.23
5        0.57/0.22
10       0.59/0.24
```

These are stronger scientific evidence than the heterogeneous SOTA tables.

---

# 9. Cross-paper position

```text
LAW
future endpoint auxiliary loss
→ representation shaping
→ no future object online

Metis
future-video flow co-training
→ world-loss-shaped action expert
→ no future object online

DynFlowDrive
candidate-conditioned latent flow teacher
→ world-derived candidate-label / score supervision
→ no future object online

WorldDrive
heavy future teacher
→ distilled future representation
→ lightweight future surrogate online

World4Drive
candidate endpoint future
→ future ScoreNet online

WoTE
candidate recurrent future
→ utility model online

SeerDrive
future BEV ↔ planner hidden-state refinement online
```

DynFlowDrive therefore adds a distinct **training-only world-derived selector-teacher** lifecycle combination, but this is already expressible by existing J/K/L/M dimensions.

---

# 10. Evidence boundary

## PROVES

```text
rectified-flow WM beats the matched static-WM baseline in this framework;
pretrained world features add further planning gains;
world-derived candidate-selection supervision helps;
world model can be removed at inference while retaining learned ranking behavior.
```

## DOES NOT PROVE

```text
flow time = physical time;
intermediate flow state = real intermediate scene;
flow angular stability = calibrated physical stability;
multiple candidate paths = observed counterfactual futures;
NAVSIM = reactive closed loop;
flow fidelity monotonically explains planning quality.
```

## STRONGEST ALTERNATIVE EXPLANATION

```text
foundation latent quality
+ future-state auxiliary supervision
+ improved positive-mode assignment
+ learned scorer distillation
+ multimodal candidate training
+ generic flow regularization
```

may explain much of the observed planning gain without requiring the stronger interpretation that continuous physical scene dynamics have been identified.

---

# 11. Source audit queue when implementation is released

```text
Eq.10 target velocity implementation
sampling initial state: a vs z_t
alpha schedule/value
solver K/default
lambda_traj / lambda_theta
VAE freeze state
planner/world detach boundaries
per-candidate L_rec/L_flow coverage
future target construction
MS-only ablation implementation
NAVSIM surrounding-agent target semantics
```
