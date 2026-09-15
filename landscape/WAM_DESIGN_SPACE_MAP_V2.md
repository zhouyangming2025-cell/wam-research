# WAM Design Space Map V2

Last updated: 2026-09-15

Status: **ELEVEN-ANCHOR CONSOLIDATED SCIENTIFIC MAP**

Anchors:

```text
LAW | WoTE | Epona | WorldDrive | World4Drive | SeerDrive
Drive-JEPA | Metis | DynFlowDrive | Discrete-WAM | GraphWorld
```

Purpose: build a planning-centric WAM map that remains stable when representation substrate changes.

---

# 1. Primary design-space axes

## Axis A — Where does world knowledge enter planning?

```text
TRAINING-ONLY
  A1 future auxiliary loss                 LAW
  A2 predictive pretraining / transfer     Drive-JEPA
  A3 joint world-action gradient shaping   Metis / Discrete-WAM
  A4 world consequence teacher             DynFlowDrive

ONLINE DIRECT CONDITIONING
  A5 shared world/history representation   Epona
  A6 structured compact world state        GraphWorld

ONLINE CONSEQUENCE-AWARE SELECTION
  A7 distilled future representation       WorldDrive
  A8 compact future-mode hypothesis         World4Drive
  A9 recurrent consequence + utility        WoTE

ONLINE INTERNAL CO-REFINEMENT
  A10 future/planner hidden feedback         SeerDrive
```

This is the highest-level planning mechanism axis.

---

## Axis B — What is the world object?

| Anchor | World object |
|---|---|
| LAW | factual future visual latent |
| Drive-JEPA | masked predictive video representation |
| Epona | shared historical multimodal latent + optional future visual latent |
| Metis | future video latent/feature during co-training |
| DynFlowDrive | flow-transported future latent teacher |
| Discrete-WAM | discrete visual/world tokens |
| GraphWorld | ego-centric agent/node interaction latent |
| WorldDrive | generative and distilled future scene representation |
| World4Drive | intention-conditioned future endpoint latent |
| WoTE | recurrent structured BEV future sequence |
| SeerDrive | mode-conditioned future BEV feature |

Important control:

```text
world substrate
!= world role in decision making
```

Two models can both predict a latent future while using it in fundamentally different ways.

---

## Axis C — Training-time jointness

Separate:

```text
representation sharing
parameter sharing
gradient sharing
sequence sharing
causal forward coupling
```

Approximate ordering must not be collapsed to one scalar:

```text
LAW          shared planner representation + auxiliary future gradient
Epona        shared MST/F + separate TrajDiT and VisDiT
Metis        separate experts + asymmetric forward attention + backward gradient coupling
Discrete-WAM same Transformer backbone/hidden sequence, separate vocabularies
GraphWorld   shared direct planner/world-state graph
```

Binding rule:

```text
more shared parameters
!= more online world dependence
```

---

## Axis D — Deployment-time model-basedness

A useful deployment map:

```text
NO FUTURE/WORLD OBJECT REQUIRED ONLINE
LAW
Drive-JEPA predictive head
Metis future-video branch
DynFlowDrive world teacher
Discrete-WAM future visual generation

SHARED/CURRENT WORLD REPRESENTATION ONLINE
Epona shared historical F
GraphWorld refined interaction W

COMPACT PREDICTED FUTURE ONLINE
WorldDrive
World4Drive

RECURRENT / ITERATIVE FUTURE ONLINE
WoTE
SeerDrive
```

This is independent of training-time jointness.

---

# 2. Future-truth taxonomy

## Type T1 — Direct factual future observation/representation

```text
LAW
Epona visual branch
Metis
World4Drive factual assignment target
DynFlowDrive endpoint target
Discrete-WAM logged future visual tokens
```

## Type T2 — Predictive/self-supervised representation target

```text
Drive-JEPA
```

Important: masked same-window completion is not identical to chronologically unseen future prediction.

## Type T3 — Teacher-generated candidate consequence

```text
WorldDrive FAR teacher path
```

## Type T4 — Structured future / pseudo-simulation target

```text
WoTE
```

Audited limitation: surrounding-agent futures in the NAVSIM/PDM path are not reactive per ego alternative.

## Type T5 — Hypothesis-derived target latent

```text
GraphWorld W_tgt
```

It is produced from aggregated motion/planning hypotheses + map rather than direct future observation encoding.

## Type T6 — Mode-conditioned future with one factual branch assignment

```text
World4Drive
SeerDrive
```

Control:

```text
K predicted future hypotheses
!= K factual/counterfactual future truths
```

---

# 3. Counterfactuality map

Four mandatory questions:

```text
1 candidate/action-specific future output?
2 candidate/action-specific alternative-future supervision?
3 reactive surrounding-agent intervention truth?
4 intervention-response validation?
```

| Anchor | Specific output | Alternative truth | Reactive truth | Intervention validation |
|---|---:|---:|---:|---:|
| LAW | limited/single | NO | NO | NO |
| Epona | controllable future | NO matched alternatives | NOT ESTABLISHED | NO |
| Metis | action-conditioned | NO | NOT ESTABLISHED | NO |
| DynFlowDrive | YES training branches | NO | NO | NO |
| Discrete-WAM | YES perturbable generations | NO | NOT ESTABLISHED | NO |
| GraphWorld | NO candidate world branch | NO | NO WM truth | NO |
| WorldDrive | YES teacher/surrogate | learned teacher output, not observed alternatives | NOT ESTABLISHED | NO |
| World4Drive | YES | NO | NO | NO |
| WoTE | YES | pseudo/simulator candidate target | NO in audited path | NO |
| SeerDrive | YES modes | NO | NO | NO |
| Drive-JEPA | N/A world branch | N/A | NO | NO |

Main result:

> **None of the eleven anchors provides strong intervention-validated reactive multi-agent counterfactual truth for alternative ego actions.**

That is a boundary of the current evidence set, not yet a declared research gap.

---

# 4. Deployment lifecycle map

| Anchor | Training graph | Knowledge transformation | Deployment graph |
|---|---|---|---|
| LAW | planner + future latent predictor | auxiliary gradient shaping | direct waypoint planner |
| Drive-JEPA | JEPA masked predictor + target encoder | transfer encoder | proposal/refinement/scorer planner |
| Epona | shared MST → trajectory + visual branches | shared representation | MST→TrajDiT; visual branch optional |
| Metis | action expert conditions future-video expert | world loss shapes action expert | action-only policy |
| DynFlowDrive | candidate→flow WM→mode preference | distill into score head | candidates→score→argmax |
| Discrete-WAM | shared world/policy token tasks | shared backbone + policy adaptation | decision→action-token editing |
| GraphWorld | ECIG + flow world-state + task losses | compact W retained | W→motion/planning query conditioning |
| WorldDrive | generative WM + planner + FAR teacher | representation inheritance/distillation | candidate + lightweight future → ranking |
| World4Drive | intentions→candidate future hypotheses + factual assignment | ScoreNet learns branch identity | generate future hypotheses→score→select |
| WoTE | candidate-conditioned transition + reward learning | retained directly | rollout→reward→utility→argmax |
| SeerDrive | future BEV/planner iterative training | retained directly | internal co-refinement→trajectory |

---

# 5. Temporal-coordinate map

Do not use a generic word `step` without a qualifier.

| Anchor | Physical future axis | Internal non-physical axis |
|---|---|---|
| LAW | current→future latent target | model layers only |
| Drive-JEPA | video-window temporal positions | masking/reconstruction operation |
| Epona | autoregressive future frame index | diffusion/flow denoising steps |
| Metis | future action/video horizon | flow/denoising steps |
| DynFlowDrive | current→future endpoint | rectified-flow transport coordinate s |
| Discrete-WAM | A_h/V_h future sequence positions | token-edit refinement rounds |
| GraphWorld | physical t and t+1 consistency; 6s trajectory output | flow interpolation coordinate / Euler steps |
| WorldDrive | future scene/video time | generative teacher sampling steps |
| World4Drive | future endpoint/horizon | diffusion/generative solver iterations if used |
| WoTE | recurrent future rollout time | little separation: rollout step advances predicted scene time |
| SeerDrive | fixed future target/horizon | planner↔world refinement iteration |

Binding rule:

```text
more denoising / flow / editing / refinement steps
!= longer physical future horizon
```

---

# 6. Long-horizon taxonomy

A `long-horizon` claim must specify which object is long.

| Anchor | Longer output trajectory | Longer history/context | Persistent memory/state | Explicit multi-step world prediction | Reactive closed-loop evidence |
|---|---:|---:|---:|---:|---:|
| GraphWorld | **YES 6s** | YES | GRU/context state | **NO** | Bench2Drive final policy YES |
| WoTE | YES | YES | rollout-local | **YES** | NAVSIM path non-reactive |
| Epona | planning + long visual rollout capability | YES | generated visual context | **YES visual** | planning eval depends benchmark |
| World4Drive | finite horizon | limited | NO | endpoint only | NAVSIM non-reactive |
| SeerDrive | finite horizon | BEV context | iterative hidden state | no physical multi-step rollout | released evaluation not proof of reactive WM |
| Discrete-WAM | action/world sequence capability | YES | sequence context | optional generative sequence | NAVSIM planning non-reactive |
| DynFlowDrive | finite candidate horizon | current context | NO deployment WM | endpoint flow, not physical rollout | NAVSIM non-reactive |

GraphWorld is the key negative control:

```text
6s planning competence
without
6s explicit world rollout
```

---

# 7. Safety / risk / value map

| Anchor | Explicit risk state/field | Explicit utility/value | Safety enters through | Safety primarily proved by |
|---|---:|---:|---|---|
| LAW | NO | NO | representation + planning supervision | planning metrics |
| Drive-JEPA | NO | simulator-trained scorer | simulator/PDM teacher | planning metrics |
| Epona | NO | NO | joint representation | planning metrics |
| Metis | NO | NO | action/world co-training | planning metrics |
| DynFlowDrive | NO | score target | world-derived mode preference | NAVSIM metrics |
| Discrete-WAM | NO | decision/RL reward | post-training/value target | EPDMS |
| GraphWorld | NO | NO explicit utility | interaction representation | collision reduction + Bench2Drive |
| WorldDrive | NO | ranking/value-like | PDMS/PDM preference teacher | ranking/planning metrics |
| World4Drive | NO | factual-mode score, not utility | branch consistency | planning metrics |
| WoTE | NO field | **YES explicit utility** | collision/DAC/TTC/comfort/progress/imitation | online selection + planning metrics |
| SeerDrive | NO | NO | future-aware refinement | planning metrics |

Binding rule:

```text
lower collision
!= explicit learned risk representation
```

---

# 8. Evaluation-regime normalization

## Open-loop offline

Examples:

```text
nuScenes trajectory evaluation
future-video/world-generation metrics
```

Can support:

```text
prediction/planning accuracy on logged data
```

Cannot directly support:

```text
reactive policy-environment competence
intervention-correct world dynamics
```

## Non-reactive pseudo-simulation / data-driven planning

Canonical example:

```text
NAVSIM v1/v2
```

Can support:

```text
planning quality under standardized logged-agent/pseudo-sim semantics
candidate evaluation quality in that protocol
```

Cannot automatically support:

```text
reactive surrounding-agent response validity
```

## Reactive simulator closed loop

Canonical example:

```text
Bench2Drive / CARLA
```

Can support:

```text
final policy competence under interactive execution
```

Still does not automatically prove:

```text
internal world model is intervention-valid
```

## Visual autoregressive rollout

Examples:

```text
Epona long video rollout
Discrete-WAM optional world generation
```

Can support:

```text
generative temporal consistency
```

Does not equal:

```text
policy-environment closed loop
```

---

# 9. The four most important orthogonal maps

## Map 1 — Training-time world dependence

```text
weak ← auxiliary/pretraining ───── joint co-training/shared backbone → strong
```

## Map 2 — Deployment-time world dependence

```text
none ← current/shared W ← compact predicted future ← recurrent consequence rollout
```

## Map 3 — Value explicitness

```text
implicit planning loss ← mode score/ranker ← explicit utility decomposition
```

## Map 4 — Counterfactual truth strength

```text
one factual future
→ candidate-specific model hypotheses
→ candidate-specific pseudo/simulator targets
→ reactive intervention truth [not achieved by current anchor set]
```

These maps should replace any single scalar notion of `WAM maturity`.

---

# 10. Stable eleven-anchor scientific labels

```text
LAW
= Predictive Training Signal

Drive-JEPA
= Predictive Representation Pretraining + Simulator-Distilled Proposal/Selection

Epona
= Shared World Representation + Direct Generative Policy

Metis
= Asymmetric World-Action Co-Training + Action-Only Inference

DynFlowDrive
= Training-Only Flow-Dynamics Mode/Score Supervision

Discrete-WAM
= Shared Discrete World-Policy Backbone + Planning-Only Action Token Deployment

GraphWorld
= Online Interaction-Structured Future-Aware Latent State + Direct Multimodal Planning

WorldDrive
= Predictive Representation Inheritance + Distilled Online Consequence Evaluation

World4Drive
= Online Compact Latent Foresight + Factual-Mode Matching

WoTE
= Online Learned Consequence Model + Explicit Utility

SeerDrive
= Online Bidirectional Future/Planner Feature Co-Refinement
```

---

# 11. Design-space conclusion

Across these anchors, the strongest scientific organizing principle is not `what world representation is predicted`, but:

> **what transformation connects world knowledge to the final action, at what lifecycle stage, under what future truth, and under what evaluation regime.**

Any future WAM paper should be placed first on:

```text
planning interface
→ future truth
→ deployment lifecycle
→ temporal geometry
→ value/safety semantics
→ evaluation regime
```

and only then by visual/BEV/latent/token/graph substrate.
