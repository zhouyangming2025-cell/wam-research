# CURRENT_STATE

Last updated: **2026-09-15 — GraphWorld stress test COMPLETE; Ontology V1.3 RETAINED; WAM 11-anchor consolidation NEXT**

## Research north star

```text
WAM / World Model + one-stage End-to-End + Planning-centric autonomous driving
```

Core WAM remains primary. WAM+VLA is secondary/control. Risk/predictive-risk remains optional prior knowledge, not a required destination.

## Methodology in force

```text
FIELD UNDERSTANDING FIRST
→ complete core-WAM coverage
→ comparative anchor deep reads
→ dimension-first normalization
→ evidence QA / comparability QA
→ only then adversarial problem discovery
→ falsification
→ method design
```

Phase D remains **PAUSED**.

Canonical reading stack:

```text
paper-deep-reader
→ mechanism / formula / figure reconstruction

academic-research-agent source/claim gate
→ source/version discipline + claim/evidence separation

literature-reading-and-synthesis
→ immediate cross-paper scientific comparison

WAM Ontology
→ full projection + residue/back-projection gate
```

Authority:

```text
landscape/WAM_READING_SKILL_STACK.md
```

---

# Dimension-first normalization status

```text
P0048 LAW           COMPLETE v2
P0045 WoTE          COMPLETE v2
P0001 Epona         COMPLETE v2 + source audit
P0042 WorldDrive    COMPLETE v2
P0046 World4Drive   COMPLETE v2
P0061 SeerDrive     COMPLETE v2 first pass + version/source audit
P0049 Drive-JEPA    COMPLETE v2 first pass + source audit
P0062 Metis         COMPLETE v2 first pass + paper/repo audit
P0063 DynFlowDrive  COMPLETE v2 first pass + paper/repo audit
P0064 Discrete-WAM  COMPLETE v2 first pass + paper/source-status audit
P0065 GraphWorld    COMPLETE v2 first pass + paper/source-status audit
```

Canonical coordinate system:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_3_AMENDMENT.md
```

Latest comparison layer:

```text
landscape/WAM_COMPARISON_MATRIX_V1_3_GRAPHWORLD_EXTENSION.md
```

GraphWorld artifacts:

```text
papers/deep_analysis/P0065_GRAPHWORLD_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_GRAPHWORLD_AUDIT.md
landscape/P0065_GRAPHWORLD_ONTOLOGY_PROJECTION.md
landscape/WAM_COMPARISON_MATRIX_V1_3_GRAPHWORLD_EXTENSION.md
```

---

# GraphWorld stable result

## Source/version boundary

```text
paper: GraphWorld: Long-Horizon Planning with World Models for End-to-End Autonomous Driving
arXiv:2606.16274v1
v1: 2026-06-15
```

As of 2026-09-15 no attributable official autonomous-driving implementation repository was identified.

Therefore:

```text
paper architecture / equations / tables   PAPER-VERIFIED
exact implementation                      SOURCE-UNVERIFIED / MONITOR
```

Do not confuse the unrelated archived `google-research/graphworld` graph-learning benchmark with this paper.

## Canonical mechanism

```text
instance-level agent features
+ historical ego/agent motion
+ local map
→ Ego-Centric Interaction Graph
→ current structured latent W_cur

motion hypotheses + ego planning hypotheses + map
→ hypothesis-derived W_tgt

W_cur → 2-step flow refinement → W_refined

W_refined(agent)
→ refine/reweight agent motion modes

W_refined(ego)
→ condition ego planning query

→ direct multimodal trajectory decoding
```

Best label:

```text
ONLINE INTERACTION-STRUCTURED FUTURE-AWARE LATENT STATE
+
DIRECT MULTIMODAL PLANNER
```

---

# `Long horizon` correction

GraphWorld explicitly states that it does **not** achieve long-horizon capability by explicit multi-step world rollout.

Its long-horizon mechanism is:

```text
historical recurrent context
+ future-oriented motion/planning hypotheses
+ compact world-state refinement
+ world-conditioned planning
+ 6-second trajectory output/evaluation
```

It does NOT provide:

```text
6-second explicit world-state sequence rollout
candidate-specific future world per ego action
reactive counterfactual traffic simulation
```

Binding rule:

```text
long-horizon planning
!=
long-horizon world simulation
```

The paper itself lists **single-step world-state prediction** as a limitation and multi-step world modeling as future work.

---

# World-state truth correction

GraphWorld has two distinct future-related targets.

## Flow target

```text
W_tgt = projection(
    aggregated agent-motion hypotheses,
    aggregated ego-planning hypotheses,
    map
)
```

Thus:

```text
future-aware / hypothesis-derived target = YES
factual future observation target         = NO for the flow endpoint
```

## Stage-II temporal target

```text
L_world = || W_t - STOPGRAD(W_{t+1}) ||²
```

where `W_{t+1}` is inferred from actual input at the next physical timestamp.

This introduces factual future information, but it is a **representation-consistency objective**, not an explicit learned transition:

```text
T(W_t, action_t) → W_{t+1}
```

Therefore:

```text
future representation shaping = YES
action-conditioned factual environment dynamics = NOT ESTABLISHED
```

---

# F08 / time semantics

GraphWorld contains three separate temporal notions:

```text
physical observation time:
physical t → physical t+1

flow coordinate:
s ∈ [0,1] between W_cur and W_tgt

trajectory horizon:
future 1s ... 6s
```

Binding rule:

```text
flow solver step
!=
physical future timestep
```

Two flow steps produce the best reported NAVSIM PDMS; more steps do not monotonically improve planning.

---

# Interaction / safety boundary

GraphWorld gives the strongest anchor so far for an explicit structured interaction representation:

```text
nearby agents
→ ego-centered star graph
→ history/map-conditioned node world state
```

But:

```text
interaction-aware representation
!= reactive other-agent response model

safety-relevant latent semantics
!= explicit risk field / risk probability / deployed utility model
```

The method has no explicit risk field or candidate future-risk scorer.

Reactive evidence exists for the **final policy** on Bench2Drive, not for branch-wise world-model counterfactual truth.

---

# Strongest attribution controls

## Baseline → ECIG → full WSCP

```text
baseline
nuScenes 6s L2 / collision: 2.95 / 2.33
NAVSIM PDMS: 85.1

+ ECIG
2.76 / 2.19
PDMS: 85.5

+ full WSCP
2.29 / 1.95
PDMS: 90.1
```

Interpretation:

```text
ECIG helps
but the larger gain comes from the WSCP world-state refinement/conditioning bundle
```

## Flow vs diffusion

```text
NAVSIM PDMS: 88.1 → 90.1
nuScenes 6s L2: 2.46 → 2.29
6s collision: 2.23 → 1.95
```

This supports Flow Matching versus the tested diffusion alternative, not physical-time fidelity.

## Stage I → Stage II temporal supervision

```text
6s L2:       2.40 → 2.29
6s collision 2.04 → 1.95
```

Positive but smaller than the full WSCP gain.

---

# Evaluation regime

```text
Bench2Drive
= REACTIVE CARLA CLOSED LOOP

NAVSIM v1/v2
= NON-REACTIVE DATA-DRIVEN / PSEUDO-SIMULATION PLANNING

nuScenes / Adv-nuScenes / nuScenes-C / Turning-nuScenes
= OPEN LOOP
```

Do not inherit the paper's generic `NAVSIM closed-loop` phrasing into the project taxonomy.

---

# Paper-internal QA findings

Preserve as audit notes:

```text
1. Table 15: table values favor 10m radius; prose says 5m best.
2. Table 18: Euler PDMS 90.1 vs Heun 89.2; prose calls Heun an improvement.
3. More flow steps are not monotonic; 2 steps produce the best shown PDMS.
4. `t` notation overloads physical time and flow-interpolation time.
```

These do not overturn the main mechanism but reinforce equation/table-first evidence discipline.

---

# Ontology stress-test result

Potential GraphWorld residues:

```text
explicit graph topology / interaction structure
hypothesis-derived latent target vs factual-future target
```

are already expressible through:

```text
B03/B04/P04
F01/F02/F07
G01/G03
J04/J09
F08
```

Decision:

```text
Ontology V1.3 RETAINED
NO V1.4 AMENDMENT
```

---

# Eleven-anchor mechanism map

```text
LAW
future-latent auxiliary shaping
→ no future online

Drive-JEPA
masked predictive pretraining → encoder transfer
→ no predictor online

Metis
action-conditioned future-video co-training
→ world-loss-shaped policy
→ no future online

DynFlowDrive
candidate flow consequence teacher
→ world-derived score supervision
→ no world model online

Discrete-WAM
shared discrete world/policy multitask pretraining
→ direct decision/action token policy
→ future visual not required online

Epona
shared historical F
→ direct trajectory generator
+ optional visual generator

GraphWorld
structured interaction W
→ shallow online flow refinement
→ direct world-conditioned multimodal policy

WorldDrive
heavy future teacher → distilled lightweight future
→ future surrogate online

World4Drive
candidate endpoint future → factual-mode selector
→ future online

WoTE
candidate recurrent future → explicit utility
→ consequence rollout online

SeerDrive
future BEV ↔ planner hidden feature co-refinement
→ future online
```

Key synthesis after GraphWorld:

```text
CONSEQUENCE-BASED MODEL DEPENDENCE
candidate → future → value → select

and

REPRESENTATION-BASED MODEL DEPENDENCE
world/future-aware state → condition direct policy

are distinct planning families.
```

---

# Phase C.5 coverage queue

```text
LAW             COMPLETE
WoTE            COMPLETE
Epona           COMPLETE
WorldDrive      COMPLETE
World4Drive     COMPLETE
SeerDrive       COMPLETE
Drive-JEPA      COMPLETE
Metis           COMPLETE
DynFlowDrive    COMPLETE
Discrete-WAM    COMPLETE
GraphWorld      COMPLETE
```

Phase C.5 planned core-anchor stress tests are now **COMPLETE**.

## Immediate next task

See `state/NEXT_TASK.md`.

Next is **WAM 11-anchor Design Space Consolidation + comparability/evidence QA**, not another paper by default.

## Still forbidden

```text
no premature research-gap declaration
no method design yet
no forced risk-field insertion
no novelty conclusion from empty ontology cells
```

Phase D remains **PAUSED** until consolidation / comparability QA is complete.
