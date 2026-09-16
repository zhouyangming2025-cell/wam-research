# WAM Comparison Matrix V1.3 — SAFE-SIM Extension

Last updated: 2026-09-16

Status: **17-ANCHOR EXTENSION — SAFE-SIM NORMALIZED**

This file adds P0066 SAFE-SIM as the first Wave C.7 simulation/reactivity control without changing Ontology V1.3.

Canonical analysis:

```text
papers/deep_analysis/P0066_SAFESIM_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C7_SAFESIM_AUDIT.md
audits/literature/P0066_SAFESIM_SOURCE_CODE_AUDIT.md
landscape/P0066_SAFESIM_ONTOLOGY_PROJECTION.md
```

---

# 1. SAFE-SIM row

| Dimension | SAFE-SIM |
|---|---|
| Primary role | learned reactive traffic simulator / planner stress-test environment |
| World object | multi-agent kinematic state + generated non-ego future action/state trajectories |
| Ego planner interface | external planner acts in simulator; current ego plan explicitly conditions reactive/adversarial generation |
| Future dynamics | diffusion behavior generation + vehicle dynamics + repeated closed-loop state update |
| Reactive surrounding agents | **YES** |
| Planner→world feedback | **YES — ego plan + executed ego state** |
| World→planner feedback | **YES — changed simulated scene through next observation** |
| Sensor-photorealistic feedback | **NO / NOT CORE** |
| Alternative ego intervention response | model-generated |
| Ground-truth intervention response | **NO** |
| Adversarial control | collision / TTC / relative-speed / route-interaction guidance + partial diffusion |
| Training data | observational real driving trajectories (nuScenes behavior prior) |
| Test-time guidance | **YES** |
| Planner gradient through simulator | **NO audited path** |
| Evaluation | reactive closed-loop simulation; realism / collision / off-road / controllability / diversity |
| Official source | **YES — audited** |

Canonical subtype:

```text
REACTIVE CLOSED-LOOP TRAFFIC BEHAVIOR SIMULATOR
+
PLANNER-CONDITIONED ADVERSARIAL DIFFUSION GENERATOR
```

---

# 2. Reactivity ladder

The active anchors now expose at least four distinct levels:

| Mechanism | Example | Changed ego action can alter modeled surrounding future? | Surrounding response re-generated in sequential closed loop? | Paired intervention-response truth? |
|---|---|---:|---:|---:|
| factual logged future | RiskWorld | NO | NO | NO |
| candidate-conditioned evaluator with fixed/weak surrounding-response truth | WoTE / DA-WAM / SafeDrive | model may condition on candidate, but reactive GT is not established | generally NO external repeated interaction loop | NO |
| **reactive learned simulator** | **SAFE-SIM** | **YES** | **YES** | **NO** |
| intervention-grounded causal response model | not yet established in normalized anchors | YES | potentially YES | **would require YES** |

This is a major clarification:

```text
reactivity is not binary.
```

A method can be much more reactive than log replay while still lacking causal counterfactual truth.

---

# 3. SAFE-SIM vs RiskWorld

| Axis | RiskWorld | SAFE-SIM |
|---|---|---|
| Main purpose | future risk prediction | planner evaluation / safety-critical simulation |
| Future source | factual logged future supervision | learned behavior prior + guided generated alternatives |
| Ego action condition | no hypothetical ego candidate branch | current actual/planned ego trajectory explicitly used |
| Repeated environment interaction | no | **yes** |
| Surrounding behavioral response to ego | no intervention loop | **yes, model-generated** |
| Intervention GT | no | no |
| Planner consumes output online | no integrated planner result | via external simulated environment |

Core lesson:

```text
factual-future supervision
and
closed-loop behavioral reactivity
are orthogonal strengths.
```

RiskWorld is stronger on direct factual future target semantics.
SAFE-SIM is stronger on endogenous response feedback.
Neither establishes paired counterfactual truth.

---

# 4. SAFE-SIM vs SafeDrive

| Axis | SafeDrive | SAFE-SIM |
|---|---|---|
| Scientific role | online ego candidate safety evaluator | external reactive simulator |
| Ego alternatives | many candidates scored in one planning step | one operating planner repeatedly acts |
| Future object | sparse candidate-conditioned consequence/safety representation | non-ego behavior trajectories + environment state |
| Selection | chooses ego trajectory | does not directly choose ego trajectory |
| Reactive surrounding loop | not established as GT-reactive | **explicit generated closed-loop response** |
| Main safety signal | candidate-specific safety/value | adversarial environment behavior / collision stress |

Key distinction:

```text
candidate-conditioned safety reasoning
!=
interactive environment reactivity
```

---

# 5. SAFE-SIM vs WoTE / DA-WAM

```text
WoTE / DA-WAM
candidate_1...K
→ internal future/consequence estimate_1...K
→ score_1...K
→ choose ego action now
```

versus:

```text
SAFE-SIM
ego planner chooses/updates action
→ external traffic model responds
→ environment advances
→ planner observes result
→ choose again
```

The difference is not merely architecture.

It is **decision topology**:

```text
parallel hypothetical action evaluation
vs
sequential closed-loop environment interaction
```

SAFE-SIM therefore should not be inserted into a WAM-planner leaderboard as if it were another candidate scorer.

---

# 6. SAFE-SIM vs DriveReward

```text
DriveReward
candidate ego trajectory
→ compressed semantic reward/value
→ train / rank
```

```text
SAFE-SIM
ego trajectory / actual planner behavior
→ explicit generated surrounding response
→ physical episode evolution
→ stress-test planner
```

Thus the atlas now contains both extremes:

```text
DIRECT VALUE COMPRESSION                         DriveReward
EXPLICIT INTERACTIVE BEHAVIOR SIMULATION         SAFE-SIM
```

A future research comparison must ask whether planning needs:

```text
value only
future consequence representation
or
full interactive response simulation
```

rather than assuming one is always superior.

---

# 7. Feedback-channel comparison

| Method / regime | F_e ego dynamics | F_s sensor viewpoint | F_a agent state | F_b agent behavioral response |
|---|---:|---:|---:|---:|
| log open-loop evaluation | NO | NO | fixed log | NO |
| NAVSIM-style non-reactive pseudo-sim | partial / metric-owned | NO | largely logged/non-reactive | NO |
| candidate-internal WAM (typical) | hypothetical internal | internal representation only | predicted/conditioned | often not behaviorally validated |
| **SAFE-SIM** | **YES** | NO / not photorealistic core | **YES** | **YES** |
| sensor-rendering closed-loop simulator | YES | **YES** | depends on behavior backend | depends on behavior backend |

This table prevents the vague label `closed-loop` from hiding different feedback semantics.

---

# 8. Diffusion coordinate vs world time

SAFE-SIM gives another decisive example of Ontology V1.3 F08.

```text
K = 100 diffusion denoising steps
```

but physical environment/planner interaction is separate and reported at:

```text
2 Hz replanning in experiments
```

Therefore:

```text
denoising step k
!=
physical future timestep t
!=
closed-loop episode step
```

Partial diffusion `k_p = γK` controls how strongly a rule-based proposal anchors generation; it does not represent how far into the physical future the simulator has advanced.

---

# 9. Safety-criticality vs realism trade-off

TTC-guidance experiment:

```text
TTC weight       0.0    1.0    2.0
collision rate   48.2   53.6   60.7
realism          0.76   0.79   0.81  ↓ better
```

Ablation:

```text
Jadv+Jreg         collision 23.9 | adv offroad 13.8
Jadv only         collision 53.5 | adv offroad 23.1
```

Therefore:

```text
more planner failures
!=
better simulator
```

Adversarial strength must be judged jointly with plausibility / behavioral validity.

This is directly relevant to any future WAM-based safety evaluator: maximizing failure-inducing futures without validating future realism can create an adversarial artifact rather than meaningful planning robustness.

---

# 10. Realism truth decomposition

SAFE-SIM's main realism evidence is distributional:

```text
Wasserstein distance over acceleration / lateral acceleration / jerk profiles
```

This supports:

```text
marginal/aggregate motion-distribution similarity
```

It does not directly support:

```text
correct response of driver B to ego intervention A
```

So the field atlas should keep these separate:

```text
R1 log-distribution realism
R2 closed-loop stability / physical validity
R3 behavioral reactivity
R4 intervention-response validity
```

SAFE-SIM has evidence for R1–R3; R4 remains unestablished.

This refinement fits existing ontology dimensions and does not require V1.4 yet.

---

# 11. Planning-evidence boundary

SAFE-SIM reports planner-dependent collision rates across BC, IDM, Lane-Graph, BITS and PDM-Closed.

Correct use:

```text
DIRECT EVIDENCE:
simulator can adapt safety-critical interactions to multiple planner families.
```

Incorrect use:

```text
INFERENCE NOT AUTHORIZED:
planner with lower induced collision rate is globally safer/better.
```

Why:

```text
adversarial generator conditions on planner behavior
planner interfaces differ
attack success and fault responsibility differ
paper reports collisions where ego is not at fault
```

---

# 12. New cross-family synthesis after 17 anchors

The active corpus now supports a stronger decomposition of `world knowledge for planning`:

```text
A. training-only predictive shaping
B. online latent/world representation for policy
C. candidate-specific future consequence prediction
D. explicit risk/safety modeling
E. direct value/reward modeling
F. external reactive world simulation
```

SAFE-SIM establishes that F is a genuinely different mechanism from C.

Both may condition on ego action, but:

```text
C answers:
"If I consider action a, what consequence/value should I assign now?"

F answers:
"After I actually act and the world changes, how should other agents respond next?"
```

---

# 13. Counterfactual truth ladder after SAFE-SIM

A useful project-wide hierarchy is now:

```text
Level 0  logged factual future only
Level 1  model output changes with alternative ego action
Level 2  surrounding behavior is regenerated after actual simulated ego changes
Level 3  generated intervention responses are validated against real intervention data
```

Placements:

```text
RiskWorld        Level 0
many action-conditioned WAM branches  Level 1
SAFE-SIM         Level 2
Level 3          not established by current normalized anchors
```

This is not a quality ranking; it is a truth/feedback classification.

---

# 14. What Wave C.7 should test next

SAFE-SIM alone is not enough to generalize about reactive simulators.

Next anchors should test whether the same conclusions survive different simulator designs:

```text
P0067 ProSim
→ promptable / controllable multi-agent closed-loop simulation

P0013 BridgeSim
P0014 ReactSimBench
P0015 CausalDrive
→ progressively stronger controls on simulation, behavioral response and evaluation truth
```

Questions to carry forward:

```text
Does planner trajectory explicitly enter behavior generation?
How often are agents replanned?
What is re-generated vs replayed?
What metric validates behavioral response?
Does realism remain distributional or become intervention-specific?
What feedback channels are closed?
```

---

# Ontology decision

```text
V1.3 RETAINED
NO V1.4
```

SAFE-SIM strongly exercises:

```text
E action→world coupling
F07/F08 future geometry and internal-time semantics
G08 intervention-response supervision
I04/I05 reactivity/validity
J08/J09 nested iteration + planner→world feedback
O01/O07 evaluation-regime semantics
P04 interaction
```

No irreducible dimension survives back-projection.
