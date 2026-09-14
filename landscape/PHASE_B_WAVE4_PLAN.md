# PHASE_B_WAVE4_PLAN — Closed Loop, Reactivity, Simulation Realism, and VLA

Last updated: 2026-09-14

Status: **ACTIVE**

Wave 4 begins only after the Waves 1–3 Research QA Gate was closed.

## 1. Purpose

Wave 4 is not a search for a gap. Its purpose is to reconstruct what different papers actually mean by:

```text
closed loop
interactive
reactive
realistic simulation
world-model evaluation
behavioral validity
VLA reasoning
```

The core scientific question is:

> What kind of evidence is required to claim that a planning/world model remains valid when ego actions alter the future environment?

This must be answered before any later research-problem discovery around reactivity, counterfactuals, simulation, or planning evaluation.

## 2. Anchors and order

```text
1. Bench2Drive
2. HUGSIM
3. ORION
4. ReactSim-Bench
5. CausalDrive
```

Reading logic:

```text
Bench2Drive
→ establish a genuinely interactive closed-loop benchmark baseline

HUGSIM
→ separate photorealistic sensor feedback / scene reconstruction from behavioral-agent reactivity

ORION
→ inspect VLA / semantic reasoning in a closed-loop-oriented planner

ReactSim-Bench
→ measure reactive behavior quality of world-agent simulation under ego deviation

CausalDrive
→ inspect a world model explicitly conditioned on ego trajectory to generate/react surrounding behavior
```

## 3. Binding controls from Waves 1–3

Every Wave-4 interpretation must respect:

```text
NAVSIM non-reactive pseudo-simulation != reactive closed loop
candidate-conditioned != reactively supervised
conditional prediction != intervention identification
world fidelity != decision utility
world/action architectural coupling != causal evidence
candidate-specific future output != candidate-specific oracle future
```

Also carry the historical predecessors:

```text
M2I
GameFormer
What Truly Matters in Trajectory Prediction?
nuPlan
```

A 2026 world model does not invent interaction merely by using action conditioning.

## 4. Common audit axes

For every anchor, record the following in one comparable table.

### A. Environment loop

```text
Does ego action alter next simulator state?
Does the next observation depend on the executed ego state?
Are surrounding-agent states replayed, rule-based, learned, or jointly generated?
Can surrounding agents respond to ego deviations?
```

### B. Sensor / scene realism

```text
real camera replay
rendered camera from reconstructed 3D scene
synthetic video generation
BEV / occupancy / symbolic state
privileged simulator state
```

Do not equate photorealistic rendering with behavioral realism.

### C. Other-agent behavior

```text
logged fixed trajectories
scripted/rule-based agents
behavior models
learned reactive agents
world-model-generated behavior
```

Trace whether the behavior is conditioned on the ego action/trajectory and whether it is validated against any behavioral target.

### D. Counterfactual validity

Ask separately:

```text
Does the system produce a different future for a different ego action?
Is that future plausible?
Is it consistent with the same episode/history?
Is the surrounding response behaviorally correct?
Is any alternative-action ground truth available?
```

These are different properties.

### E. Planner evaluation

Classify the evidence regime:

```text
open-loop logged trajectory
non-reactive pseudo-simulation
closed-loop non-reactive
interactive/reactive simulator
photorealistic reconstructed closed loop
real-vehicle closed loop
```

Record sensor feedback and traffic feedback separately.

### F. Decision relevance

```text
Does the paper only evaluate simulation fidelity?
Does it evaluate a planner inside the simulator?
Does a better simulator/world model change planner ordering/performance?
Does it show failure under ego deviation?
```

### G. Runtime/deployability

```text
simulation FPS / latency
planner FPS / control frequency
rollout horizon
number of generated branches/candidates
```

Runtime is part of planning usefulness, not an appendix detail.

## 5. Paper-specific questions

### 5.1 Bench2Drive

Must establish:

```text
- exact CARLA version / benchmark protocol;
- sensor input and policy output;
- whether traffic actors are interactive with ego;
- route/scenario composition;
- driving score / success metrics and infraction semantics;
- distinction from CARLA Leaderboard v1/v2;
- whether benchmark measures perception + planning jointly;
- what kinds of long-tail / safety-critical scenarios are represented.
```

Desired output:

```text
Bench2Drive = reference point for interactive closed-loop policy evaluation,
not a world-model paper.
```

### 5.2 HUGSIM

Must separate:

```text
photorealistic sensor feedback
3D scene reconstruction
novel-view rendering
vehicle dynamics / ego feedback
surrounding-agent trajectory model
reactivity of surrounding agents
```

Key question:

> Does HUGSIM's “closed loop” primarily solve sensor-feedback realism, behavioral traffic realism, or both?

### 5.3 ORION

Trace:

```text
visual/language input
reasoning representation
trajectory/action output
training supervision
whether reasoning is causal to action generation or auxiliary/distillation
closed-loop benchmark(s)
world-model component, if any
```

Use ORION as a VLA planning control, not as evidence that language reasoning is inherently necessary.

### 5.4 ReactSim-Bench

Must trace:

```text
how ego deviation/intervention is generated;
what world-agent simulator receives as conditioning;
what “reaction quality” means;
which response metrics compare generated vs reference behavior;
whether reference reactions are true counterfactual outcomes or proxies;
scenario count and interaction-critical subset;
which methods fail and why.
```

This paper is especially important for distinguishing:

```text
action-conditioned visual plausibility
from
behaviorally valid reactive simulation.
```

### 5.5 CausalDrive

Must trace:

```text
exact ego-trajectory condition
NPC/world representation
how action changes predicted NPC/world future
training target source
whether counterfactual alternatives have direct supervision
rollout mechanism
planner / RL coupling
closed-loop evaluation
runtime
```

Do not accept “causal” as a property solely from the title. Determine whether the method provides interventional identification, action conditioning, or a learned reactive simulator.

## 6. Cross-paper matrices required

### Matrix 1 — evaluation loop

| method | ego feedback | sensor feedback | surrounding-agent feedback | learned reactivity | photorealism | planning evaluated |
|---|---|---|---|---|---|---|

### Matrix 2 — counterfactual evidence

| method | action conditioned | alternative future generated | alternative future GT | episode consistency tested | behavioral response tested |
|---|---|---|---|---|---|

### Matrix 3 — what “closed loop” means

For each paper, write one exact sentence that can substitute for the phrase “closed loop” without ambiguity.

Example form:

```text
“The ego policy acts repeatedly in simulator X; the next rendered observation changes with ego pose, while surrounding traffic follows Y behavior model.”
```

## 7. Stop condition

Wave 4 closes only when we can answer, without generic terminology:

1. what feedback loop each benchmark/simulator closes;
2. whether sensor realism and behavioral realism are separately validated;
3. whether other-agent response is conditioned on ego intervention;
4. what supervision supports those responses;
5. how a planner is evaluated under the resulting dynamics;
6. which claims are simulator-quality claims vs planning-quality claims;
7. which modern “reactive WM” capabilities already existed in interactive prediction/planning predecessors.

At closeout, create:

```text
landscape/PHASE_B_WAVE4_SYNTHESIS.md
landscape/PHASE_B_WAVE4_COMPARABILITY_AUDIT.md
```

Only after Wave 4 should Phase-B-wide synthesis begin.

## 8. Forbidden during Wave 4

```text
no gap declaration
no method design
no broad paper search
no reactivation of P2-R as organizing hypothesis
no assumption that more realistic rendering means better interaction modeling
no assumption that action-conditioning means causal counterfactual validity
```
