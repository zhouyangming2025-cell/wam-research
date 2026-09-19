# WAM Mechanism Families V2

Last updated: 2026-09-15

Status: **HISTORICAL ELEVEN-ANCHOR MAP — retained for comparison; not current 12-paper authority. DriveLaW and later additions are outside this snapshot.**

Anchors:

```text
LAW | WoTE | Epona | WorldDrive | World4Drive | SeerDrive
Drive-JEPA | Metis | DynFlowDrive | Discrete-WAM | GraphWorld
```

This taxonomy deliberately does **not** organize papers primarily by substrate (`RGB / BEV / latent / token / graph`). Representation substrate is secondary. The primary question is:

> **At what interface does world knowledge change the planning decision?**

---

# 1. Canonical mechanism families

## Family A — Future as training signal / representation shaper

Canonical pattern:

```text
current observation / planner state
→ predict factual future representation during training
→ future loss shapes current representation
→ future predictor/output not required for deployed action
```

Anchor:

```text
LAW
```

Key property:

```text
world knowledge influences planning through gradient-mediated representation shaping,
not online future consumption.
```

Boundary:

```text
future prediction present during training
!= online model-based decision making
```

---

## Family B — Predictive representation pretraining / transfer

Canonical pattern:

```text
predictive/self-supervised pretraining task
→ transfer/retain encoder representation
→ downstream planner/scorer
→ predictive head not on deployment path
```

Anchor:

```text
Drive-JEPA
```

Key property:

```text
predictive objective learns a representation prior;
deployment planner is separate from the predictive training geometry.
```

Boundary:

```text
predictive representation
!= causal future dynamics model
```

---

## Family C — Shared world representation + direct policy

Canonical pattern:

```text
shared history/world representation
       /                \
world-generation branch  direct trajectory/action branch
```

Anchor:

```text
Epona
```

Key property:

```text
world and planning branches share representation and gradients;
future visual output need not be consumed by the planner.
```

Source-verified Epona refinement:

```text
planning-only: history → shared STT/MST → TrajDiT → trajectory
visual branch can be skipped
```

Boundary:

```text
shared world representation
!= future-world→action forward feedback
```

---

## Family D — World-loss-shaped direct policy / shared world-policy co-training

Canonical pattern:

```text
action/policy representation → world generation objective
world loss backpropagates into policy/shared parameters
→ action-only deployment
```

Anchors:

```text
Metis
Discrete-WAM
```

They are not identical:

```text
Metis:
asymmetric experts; forward action→world, backward world-loss→action

Discrete-WAM:
shared Transformer hidden/backbone + mixed world/policy token tasks;
primary planning still decision→action without mandatory future visual generation
```

Key property:

```text
stronger training-time jointness
!= stronger deployment-time model-basedness
```

---

## Family E — Training-only world consequence teacher / label generator

Canonical pattern:

```text
candidate/action alternatives
→ world/consequence model during training
→ derive mode preference / score target
→ train compact planner/scorer
→ remove world model at deployment
```

Anchor:

```text
DynFlowDrive
```

Key property:

```text
world model transfers consequence knowledge into a deployed score head.
```

Boundary:

```text
candidate-conditioned world teacher
!= online candidate consequence evaluator
```

---

## Family F — Online world-state-conditioned direct policy

Canonical pattern:

```text
current/history interaction state
→ compact online world state
→ directly modulate planning/motion queries
→ direct trajectory decoding
```

Anchor:

```text
GraphWorld
```

Key property:

```text
online world dependence through representation conditioning,
not candidate→future→utility selection.
```

Boundary:

```text
long-horizon policy conditioning
!= long-horizon explicit world rollout
```

---

## Family G — Online distilled future consequence representation

Canonical pattern:

```text
heavy future/world teacher during training
→ distill/inherit compact future representation
→ retain lightweight future-aware module online
→ rank/select trajectory candidates
```

Anchor:

```text
WorldDrive
```

Key property:

```text
future knowledge lifecycle includes explicit compression from expensive teacher to deployed surrogate.
```

Boundary:

```text
foundation/video prior contribution
must be separated from WAM-specific future-distillation contribution
```

---

## Family H — Online compact future-mode selector

Canonical pattern:

```text
multiple intentions / candidate trajectories
→ candidate-conditioned future latent hypotheses
→ factual future assigns one branch during training
→ online score selects one mode
```

Anchor:

```text
World4Drive
```

Key property:

```text
future latent is used online,
but the score is factual-future consistency / mode matching rather than explicit utility.
```

Boundary:

```text
multiple predicted futures
!= multiple counterfactual truths
```

---

## Family I — Online recurrent consequence model + explicit utility

Canonical pattern:

```text
candidate action/trajectory
→ recurrent predicted future state sequence
→ explicit reward/value semantics
→ utility aggregation
→ action selection
```

Anchor:

```text
WoTE
```

Key property:

```text
strongest anchor in the set for explicit consequence-model-based planning.
```

Boundary:

```text
candidate-specific predicted consequences
!= reactive other-agent intervention truth
```

Audited NAVSIM/PDM path uses logged/fixed surrounding-agent futures, so counterfactual reactivity remains limited.

---

## Family J — Online world/planner internal co-refinement

Canonical pattern:

```text
current world/planning modes
→ future world feature
→ planner refinement
→ feedback carrier to world predictor
→ repeat hidden-state refinement
→ final trajectory
```

Anchor:

```text
SeerDrive
```

Key property:

```text
world↔planner feedback is internal model iteration,
not ego↔environment closed-loop interaction.
```

Boundary:

```text
iteration count
!= physical future horizon
```

---

# 2. Eleven-anchor placement

| Anchor | Primary family | Secondary mechanism | World object required online? | Explicit consequence→utility? |
|---|---|---|---:|---:|
| LAW | A | auxiliary factual-future latent prediction | NO | NO |
| Drive-JEPA | B | predictive representation + simulator-distilled planner | NO predictive head | NO world utility |
| Epona | C | joint visual/trajectory generation | shared history state YES; future visual NO | NO |
| Metis | D | asymmetric action→world co-training | NO future world | NO |
| Discrete-WAM | D | shared discrete world/policy backbone | NO future visual for primary planning | NO online future utility |
| DynFlowDrive | E | candidate-conditioned flow teacher | NO WM | learned score only |
| GraphWorld | F | structured interaction state + flow refinement | YES compact W | NO |
| WorldDrive | G | teacher→distilled future feature | YES lightweight future | ranking/value-like |
| World4Drive | H | candidate future latent + factual-mode score | YES | NO explicit utility |
| WoTE | I | recurrent consequence + reward | YES | **YES** |
| SeerDrive | J | future-BEV/planner co-refinement | YES | NO explicit utility |

---

# 3. Six forms of `world helps planning`

A paper must be described using these six independent properties rather than the phrase `world model improves planning`.

| Anchor | Representation shaping | Shared params / gradients | Online world-state conditioning | Online candidate consequence prediction | Explicit consequence utility/value | Search/selection over alternatives |
|---|---:|---:|---:|---:|---:|---:|
| LAW | YES | YES | NO | NO | NO | NO |
| Drive-JEPA | YES via pretraining | transfer | NO | NO | scorer separate | YES proposals/scorer |
| Epona | YES | YES | shared history latent only | NO future visual consequence | NO | direct generation |
| Metis | YES | YES asymmetric | NO | NO deployment | NO | direct policy |
| Discrete-WAM | YES | strong shared backbone | NO future visual required | optional generation capability | NO online future utility | hierarchical decision/action generation |
| DynFlowDrive | YES via teacher labels | training coupling | NO | training-only | score target implicit | YES score/argmax |
| GraphWorld | YES | YES | **YES** | NO per-candidate branch | NO | multi-modal direct decode |
| WorldDrive | YES/inheritance | teacher→student | YES | **YES lightweight** | ranking/value-like | YES |
| World4Drive | YES | YES | YES | **YES** | factual-mode score, not utility | YES |
| WoTE | YES | YES | YES | **YES recurrent** | **YES explicit** | **YES** |
| SeerDrive | YES | YES | YES | mode-conditioned future | NO | internal refinement/final mode |

---

# 4. Main consolidation result

The 11 anchors do **not** lie on a single ladder from `weak world model` to `strong world model`.

At least four largely orthogonal axes exist:

```text
A. predictive/environmental modeling strength
B. decision-relevance of the learned world representation
C. training-time jointness / gradient coupling
D. deployment-time dependence on online world computation
```

Examples:

```text
Discrete-WAM: high training jointness, low mandatory deployment future dependence
WoTE: lower parameter unification, high deployment consequence dependence
GraphWorld: compact online representation dependence, low explicit rollout depth
Epona: shared representation + joint losses, visual future optional for planning
```

Therefore future comparisons must identify the axis being compared before claiming one method is `more model-based`, `more unified`, or `stronger world modeling`.
