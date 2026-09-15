# PHASE_C5_GRAPHWORLD_AUDIT

Last updated: 2026-09-15

Status: **COMPLETE FIRST PASS — paper-level mechanism/evidence audit; implementation SOURCE-UNVERIFIED**

Paper: `GraphWorld: Long-Horizon Planning with World Models for End-to-End Autonomous Driving`

Version boundary:

```text
arXiv:2606.16274v1
2026-06-15
raw paper: papers/raw_md/P0065_GraphWorld/P0065_GraphWorld.raw.md
```

Code boundary:

```text
project manifest: no official code repository identified
live GitHub search on 2026-09-15: no attributable GraphWorld autonomous-driving implementation found
```

Therefore:

```text
paper equations / tables / architecture = PAPER-VERIFIED
exact implementation / tensor routing / detach / solver loop = SOURCE-UNVERIFIED
```

---

# 1. Decision-critical source facts

## 1.1 GraphWorld explicitly rejects explicit long-horizon world rollout

The paper states that it does not aim to extend the prediction horizon through explicit multi-step rollout. Instead it learns:

```text
W_cur = f_theta(O_<=t)
```

as a compact ego-centric latent world state for future-aware planning.

SOURCE FACT verdict:

```text
long-horizon planning claim != explicit 6-second world rollout claim
```

---

## 1.2 ECIG is an ego-centered sparse star graph

Nodes:

```text
ego + selected surrounding agents
```

Neighbor selection:

```text
spatial distance threshold τ
→ PAD-OR-TRIM to fixed K
```

Interaction propagation:

```text
Q_ego cross-attends F_nbr
→ Q_tilde_ego
```

Directed topology focuses neighbor context on ego/planning rather than modeling a dense all-agent graph.

---

## 1.3 Current world state is interaction/history representation

History path:

```text
past ego/agent states H_t
+ pooled map M
→ GRU recurrent context s_t
```

Interaction integration:

```text
s_t cross-attends Q_tilde_ego ∪ F_nbr
→ c_int
```

Node states:

```text
w_i   = f_i + phi_a(c_int, r_i)
w_ego = f_ego + phi_e(c_int)
```

Thus `W_cur` is a current planning-time structured latent, not a decoded future environment.

---

## 1.4 W_tgt is not a directly encoded factual future observation

The paper defines:

```text
W_tgt = phi_tgt(
    concat(
        mean(Q_motion),
        mean(Q_tilde_ego),
        map
    )
)
```

This target comes from aggregated future motion/planning hypotheses and static context.

SOURCE FACT verdict:

```text
flow target contains future-oriented planning/motion semantics
but
flow target != encoder(real future scene) by definition
```

---

## 1.5 Flow coordinate is internal transport time

The flow objective uses:

```text
W(s) = (1-s) W_cur + s W_tgt
v*(s) = W_tgt - W_cur
```

where the paper uses symbol `t` but the scientific meaning is an internal interpolation coordinate.

SOURCE FACT verdict:

```text
flow/interpolation coordinate != physical future seconds
```

No real intermediate future world state is specified at every interpolation value.

---

## 1.6 Online world machinery remains on the planning path

After flow refinement:

```text
agent W → motion-query residual update + mode importance weighting
ego W   → ego planning-query residual update
```

Then agent and ego trajectory heads decode multi-modal futures.

Thus unlike DynFlowDrive/Metis, GraphWorld does not discard all world-state machinery at deployment.

But unlike WoTE/World4Drive, it also does not evaluate one candidate-specific future world per ego candidate.

---

## 1.7 Real t+1 information enters only via separate temporal consistency stage

Stage II:

```text
L_world = || W_t - stopgrad(W_{t+1}) ||^2
```

where `W_{t+1}` is inferred from input at physical time `t+1`.

This is factual future information, but the objective is direct latent consistency rather than explicit action-conditioned transition prediction.

---

# 2. Canonical training graph

```text
STAGE I
current sensor/perception features
+ historical states
+ map
→ ECIG / GRU / W_cur
→ flow target/refinement from motion+planning hypotheses
→ world-conditioned motion queries + ego planning queries
→ motion / planning / perception losses

STAGE II
input at t   → W_t
input at t+1 → W_{t+1} (stop-grad target)

L_world = ||W_t - SG(W_{t+1})||²

Total:
L = L_percep + L_motion + L_plan + lambda L_world
```

Important negative fact:

```text
no paper-level evidence of:
T(W_t, ego_action_t) = predicted factual W_{t+1}
```

---

# 3. Canonical inference graph

```text
current/history observations
→ perception instance features
→ distance-based neighbor selection
→ ECIG interaction representation
→ W_cur

current motion/planning hypotheses + map
→ W_tgt

W_cur → 2-step flow refinement → W_refined

W_refined(agent)
→ reweight/refine agent motion modes

W_refined(ego)
→ condition ego planning query

→ multimodal trajectories
```

No explicit long-horizon world sequence is rolled out.

---

# 4. Strongest matched evidence

## 4.1 Component ladder

From Table 11:

```text
baseline
6s L2 / Col: 2.95 / 2.33
NAVSIM PDMS: 85.1

+ ECIG
2.76 / 2.19
PDMS: 85.5

+ ECIG + WSCP
2.29 / 1.95
PDMS: 90.1
```

Scientific interpretation:

```text
ECIG alone helps
but most NAVSIM gain appears after WSCP bundle
```

Do not attribute the full gain to graph construction alone.

## 4.2 Flow vs tested diffusion alternative

```text
NAVSIM PDMS: 88.1 → 90.1
nuScenes 6s L2: 2.46 → 2.29
nuScenes 6s Col: 2.23 → 1.95
```

Supports flow choice inside this architecture; does not prove more physically correct world dynamics.

## 4.3 Stage-II temporal supervision

```text
Stage I → Stage II
6s L2:       2.40 → 2.29
6s collision 2.04 → 1.95
```

Positive but smaller effect than full WSCP bundle.

## 4.4 Graph topology

```text
fully connected → ego-star
NAVSIM PDMS 85.0 → 90.1
```

Strong evidence for ego-focused interaction filtering in the tested architecture.

---

# 5. Evaluation-regime correction

## Bench2Drive

```text
CARLA reactive closed-loop
```

This is the strongest interactive deployment evidence in the paper.

## NAVSIM v1/v2

Paper terminology:

```text
Closed-Loop
```

Project-normalized terminology:

```text
non-reactive data-driven / pseudo-simulation planning benchmark
```

Do not use NAVSIM alone as evidence of behaviorally correct surrounding-agent response to ego interventions.

## nuScenes / Adv-nuScenes / nuScenes-C / Turning-nuScenes

Open-loop planning/robustness evaluations.

---

# 6. Counterfactual / reactive truth audit

```text
candidate-specific ego action branch                NO
candidate-specific predicted future world           NO
candidate-specific alternative future ground truth  NO
reactive surrounding-agent truth in world target    NO
reactive final-policy evaluation                     YES on Bench2Drive
WM intervention-validity benchmark                   ABSENT
```

Binding interpretation:

```text
explicit multi-agent representation
!= reactive multi-agent counterfactual dynamics
```

---

# 7. Safety semantics audit

Paper claims:

```text
safety-relevant semantics
safety-aware long-horizon planning
```

Method facts:

```text
explicit risk field/state              NO
explicit future collision probability  NO
explicit online utility/risk scorer    NO
interaction graph / map / motion state YES
collision reductions                   YES
```

Therefore GraphWorld provides safety-relevant planning evidence but is not an explicit risk-modeling method.

---

# 8. Internal paper inconsistencies to preserve

## 8.1 Neighbor radius

Table 15 indicates best shown 6s numbers at **10 m**, but text says **5 m** is the best trade-off.

Status:

```text
PAPER INTERNAL NUMERIC/NARRATIVE MISMATCH
```

## 8.2 Euler vs Heun

Table 18:

```text
Euler PDMS 90.1
Heun  PDMS 89.2
```

Text calls Heun a marginal improvement.

Status:

```text
PAPER INTERNAL NARRATIVE ERROR
```

## 8.3 Sampling depth

Two steps produce best shown PDMS; more steps do not monotonically improve planning and reduce FPS.

Binding rule:

```text
more latent-flow solver steps != longer physical reasoning horizon
```

---

# 9. Proves / does not prove

## PROVES / strongly supports

```text
ego-centric sparse interaction structure helps planning in matched tests;
world-state-conditioned query modulation materially improves long-horizon planning;
flow matching outperforms the tested diffusion alternative;
extra t+1 latent consistency improves planning modestly;
reactive final-policy performance improves on Bench2Drive;
longer-horizon open-loop collision/L2 improve on nuScenes.
```

## DOES NOT PROVE

```text
explicit 6-second world rollout;
action-conditioned factual future environment transition;
candidate-specific counterfactual world prediction;
reactive other-agent intervention truth for the world model;
explicit learned risk state;
flow solver coordinate is physical time;
world-state fidelity causes planning gain monotonically.
```

---

# 10. Source/code status

As of 2026-09-15:

```text
paper/raw MD        PRESENT
implementation repo NOT IDENTIFIED
source audit         BLOCKED
```

Do not substitute the unrelated `google-research/graphworld` repository; that project is a synthetic graph-learning benchmark and is not this autonomous-driving paper.

Final source label:

```text
PAPER-COMPLETE
SOURCE-BLOCKED / MONITOR
```
