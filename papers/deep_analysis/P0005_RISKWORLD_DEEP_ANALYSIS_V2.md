# P0005 RiskWorld — Dimension-first Deep Analysis V2

Last updated: 2026-09-15

Status: **COMPLETE FIRST PASS — PAPER VERIFIED; OFFICIAL IMPLEMENTATION NOT IDENTIFIED**

Paper: **RiskWorld: Object-Centric Latent World Modeling for Autonomous Driving Risk Identification**

Canonical research role in this repository:

```text
HISTORY-CONDITIONED OBJECT-CENTRIC LATENT WORLD MODEL
→ PHYSICAL-FUTURE EGO–OBJECT RELATION ROLLOUT
→ EXPLICIT OBJECT/TIME RISK STATE
→ RISK-SOURCE IDENTIFICATION

NOT a trajectory planner
NOT an action-conditioned candidate world model
NOT a value/reward evaluator
```

The most important boundary is:

```text
explicit predicted risk state          YES
multi-step physical future rollout     YES
hypothetical ego action conditioning   NO
online planning trajectory selection   NO
```

---

# 0. Source / version contract

Primary in-repo text:

```text
papers/raw_md/P0005_RiskWorld/P0005_RiskWorld.raw.md
```

Canonical public paper:

```text
arXiv:2608.21414v1
submitted 2026-08-12
```

The raw paper title/authors/abstract match arXiv v1.

## Source-code status

No attributable official RiskWorld implementation was identified in the first-pass source audit.

A GitHub repository named:

```text
KevinWjk/RiskWorld
```

is a **false positive**: its README is an Alpamayo 1.5 release and is unrelated to this paper. It must not be used as RiskWorld source evidence.

Therefore:

```text
PAPER-VERIFIED
SOURCE-BLOCKED / MONITOR
```

---

# 1. What scientific problem does RiskWorld actually solve?

RiskWorld does **not** ask:

```text
which trajectory should ego execute?
```

It asks:

```text
among the currently observed objects,
which one is likely to become safety-critical to ego?
```

At current time `t`, for every valid observed object `i` it predicts:

```text
r_t^i = P(object i is the ego-relevant risk object | observed history)
```

The paper's key modeling claim is that risk should not be treated as a static current-frame attribute. Instead:

```text
current ego–object relation
→ imagined future ego–object relation sequence
→ object-level risk
```

This makes RiskWorld a useful **risk-state boundary anchor** for the planning-centric WAM atlas, but it must not be promoted into a planner paper merely because the representation is called a world model.

---

# 2. Exact observation and current-state representation

## 2.1 Inputs

The model observes a `K=16` frame history containing:

```text
front-view RGB
+ current object boxes
+ tracked object histories
+ ego-motion history
```

It supports at most 64 object candidates.

## 2.2 Frozen predictive-video features

A frozen V-JEPA2 ViT-L encoder processes the observed clip. Current boxes are used to pool object-aligned features.

It extracts two levels:

```text
global scene feature s_t
object-aligned visual feature v_t^i
```

Important attribution warning:

```text
V-JEPA2 predictive prior
!=
RiskWorld RSSM rollout
```

The paper's `w/o world features` ablation removes the imported V-JEPA2 features and therefore measures a large representation-prior change, not only the incremental contribution of RiskWorld's own future dynamics.

## 2.3 Explicit structured object state

For each object, an MLP encodes current ego-relative state including:

```text
relative position
motion
box geometry
category
```

A masked GRU summarizes the observed track history. An equivalent structured encoder represents ego motion.

The structured object feature, object-aligned V-JEPA feature, and global scene feature are fused into object token `x_t^i`.

## 2.4 Relation attention

Masked multi-head self-attention operates over:

```text
ego token + all valid object tokens
```

and produces a relation-aware token `x~_t^i` for every object.

Thus the current world representation is not a dense scene latent. It is an **object-indexed set of interaction-aware tokens**.

---

# 3. The world-model core: object-wise RSSM-style rollout

This is the most important distinction from risk classifiers that directly score the current frame.

For each object `i`:

```text
relation-aware token x~_t^i
→ deterministic initializer h_init^i
→ initial stochastic latent z_0^i
→ GRU deterministic state h_0^i
→ recursively sample/predict z_1...z_H from prior
→ h_1...h_H
```

The latent state contains:

```text
deterministic recurrent state h
+ stochastic state z
```

At the observed boundary, a posterior `q_phi` is grounded by the observed object token, while a prior `p_theta` predicts from the deterministic state. Future steps use only the learned prior:

```text
z_k^i ~ p_theta(z_k^i | h_{k-1}^i)
h_k^i = GRU(z_k^i, h_{k-1}^i)
```

Implementation/evaluation setting reported by the paper:

```text
H = 60 future steps
20 FPS
physical future horizon = 3 s
```

This is a **real physical-time recurrent rollout**. Unlike DynFlowDrive/GraphWorld flow coordinates, here `k=1...60` indexes future temporal steps.

At inference:

```text
initial posterior mean
→ future prior means
```

are used deterministically; stochastic samples are used during training.

---

# 4. What exactly is being predicted?

RiskWorld's latent future is not left completely implicit. Every future state `h_k^i` is decoded into:

```text
future ego-relative position p_hat_{t+k}^i
future ego-object distance d_hat_{t+k}^i
future temporal risk probability R_hat_{t+k}^i
```

The mean of the H latent future states is also pooled into the final object-risk score:

```text
mean(h_1...h_H)
→ r_t^i
```

Therefore the paper has two explicit risk objects:

1. **horizon object-risk score** `r_t^i`: which object is the risk source;
2. **time-indexed risk curve** `R_hat_{t+k}^i`: when risk emerges over the future horizon.

Minimum distance and time-to-risk are derived from the decoded future sequences rather than predicted by independent heads.

This is scientifically different from:

```text
SafeDrive: world → learned safety evaluator → trajectory selection
DA-WAM: future latent → factorized utility scorer
WoTE: future consequence → utility/reward
```

RiskWorld makes **risk itself an explicitly predicted task state**, but it does not convert risk into action utility or planner selection.

---

# 5. Where does risk supervision come from?

This point must remain explicit because `risk` is not a naturally observed physical scalar.

## 5.1 Final object-risk label

RiskBench provides an annotated risk object. For each current object:

```text
y_t^i ∈ {0,1}
```

supervises the final object-risk score with class-balanced BCE:

```text
L_obj
```

## 5.2 Future relation truth

Logged future **ego and object tracks** produce factual future ego-relative targets:

```text
p^*_{t+k}
d^*_{t+k}
min_k d^*_{t+k}
```

which supervise:

```text
L_xy
L_dist
L_min
```

These are logged factual futures under the actually executed episode trajectory.

They are **not** matched alternative futures under hypothetical ego actions.

## 5.3 Temporal-risk curve

For the annotated risk object `i*` and event interval `[a,b]`, the paper constructs an engineered future risk target that rises exponentially as the event is approached and stays at one during the annotated event interval.

Thus:

```text
temporal-risk truth
=
event-annotation-derived supervisory curve
```

not:

```text
directly measured physical collision probability
```

This curve supervises:

```text
L_curve
```

## 5.4 Latent regularization

The initial posterior is regularized toward the prior using:

```text
L_KL
```

Final objective:

```text
L
= λ_obj L_obj
+ λ_xy L_xy
+ λ_dist L_dist
+ λ_min L_min
+ λ_curve L_curve
+ β L_KL
```

So RiskWorld is jointly shaped by:

```text
risk-object identity
+ future physical relation geometry
+ event-timing semantics
+ latent stochastic regularization
```

---

# 6. The crucial action-conditioning boundary

RiskWorld does **not** receive a future ego candidate trajectory as input.

Its causal input is:

```text
past/current RGB
past/current tracked objects
past/current ego motion
```

and it predicts a future relative evolution based on the learned factual distribution.

Therefore:

```text
risk = f(observed history)
```

rather than:

```text
risk = f(observed history, hypothetical ego action)
```

This is the single most important comparison with SafeDrive / DA-WAM / WoTE / World4Drive.

RiskWorld can learn correlations between current interaction state and how ego/objects usually evolve, but it does not answer:

```text
if ego chooses candidate A, how does object i respond?
if ego instead chooses candidate B, how does object i respond?
```

Consequently:

```text
action-conditioned future output                 NO
candidate-specific alternative future truth      NO
reactive ego→other-agent intervention truth       NO
```

Its future rollout is best described as:

> **history-conditioned factual-distribution imagination**.

---

# 7. Is risk part of the world state or an evaluator?

The answer is nuanced.

RiskWorld's latent transition state `h_k^i` is not itself defined as a scalar risk state. It is a relation-oriented world state that is decoded into:

```text
physical relation
+ temporal risk
```

So risk is an **explicit prediction head over the learned world rollout**, not a post-hoc geometric rule.

This is stronger than:

```text
predict trajectories → manually compute TTC/collision
```

but different from saying that the latent dynamics itself evolves a hand-defined risk field.

Canonical classification:

```text
OBJECT-CENTRIC LATENT WORLD
→ EXPLICIT LEARNED RISK STATE
```

not:

```text
RISK FIELD AS DYNAMICAL STATE VARIABLE
```

---

# 8. Training graph vs inference graph

## Training

```text
16-frame observed history
→ frozen V-JEPA2 global/object features
+ structured ego/object histories
→ relation-aware object tokens
→ RSSM latent rollout 60 steps
→ step relation heads + temporal-risk head
→ pooled final object-risk head

logged future ego/object tracks
→ L_xy / L_dist / L_min

RiskBench risk object + event time
→ L_obj / L_curve

initial posterior/prior
→ L_KL
```

## Inference

```text
observed history only
→ relation-aware current object state
→ posterior-mean initialization
→ prior-mean 60-step latent rollout
→ future relation + temporal-risk evidence
→ object risk score r_t^i
→ threshold / rank risky objects
```

No logged future enters inference.

But also:

```text
no ego trajectory candidate
no planner query
no reward/value head
no trajectory selection
```

---

# 9. Strongest experimental evidence

## 9.1 Main task

On RiskBench:

```text
FLaRA*     61.8 overall F1, 4.1% FA
RiskWorld  63.0 overall F1, 2.1% FA
```

Thus the strongest learned baseline gap is modest:

```text
+1.2 F1
-2.0 percentage points FA
```

RiskWorld's advantage is primarily the precision/recall/false-alarm trade-off, not universal dominance on every submetric.

## 9.2 Representation attribution is large

Ablations:

```text
RiskWorld                 63.0 F1 / 2.1 FA
w/o world features        50.6 / 21.3
w/o object visual token   54.6 / 3.3
w/o relation attention    54.3 / 1.2
```

The largest drops are representation/context effects.

Important attribution rule:

```text
63.0 - 50.6
!= pure RSSM world-model gain
```

because the ablation removes frozen V-JEPA2 predictive features.

## 9.3 Incremental future-modeling evidence is smaller but positive

```text
Deterministic GRU        62.0 / 6.0
w/o future rollout      60.2 / 5.9
w/o future supervision  61.6 / 4.4
RiskWorld               63.0 / 2.1
```

Therefore:

```text
recursive rollout vs multi-horizon decoder: +2.8 F1
future supervision:                    +1.4 F1
stochastic RSSM vs deterministic GRU: +1.0 F1 overall
```

But even here effects are not monotonic across categories: the deterministic GRU has higher collision F1 than the full model. The paper supports a better **aggregate trade-off**, not superiority on every type of event.

## 9.4 Temporal prediction evidence

Against a persistence baseline that repeats current risk into the future, RiskWorld has lower Brier error across the 3 s horizon and reports a 59.8% error reduction at 3 s on annotated risk-source objects.

This is useful direct evidence that the temporal-risk rollout contains nontrivial future structure.

---

# 10. Planning-aware evaluation: what it proves and does NOT prove

RiskWorld uses an LBC planner only for a **filtered-observation diagnostic**.

The planner receives:

```text
all objects
vs
only ground-truth risk object
vs
objects selected by a risk method
```

Unselected actors are masked. Metrics measure how much the resulting plan changes and collision behavior under that filtered observation.

RiskWorld obtains, for example:

```text
Interactive: IR 0.09, CR 1.1%
Obstacle:    IR 0.08, CR 24.2%
```

The paper explicitly states this evaluates the **planning relevance of selected objects**, not improvement to the planner itself.

Therefore:

```text
RiskWorld output preserves planning-critical information   SUPPORTED
RiskWorld improves an integrated planner                   NOT EVALUATED
risk rollout is on a planning decision path                ABSENT
```

This is a boundary/control paper for planning-centric WAM, not a core online-planning WAM.

---

# 11. Immediate cross-paper comparison

## RiskWorld vs SafeDrive

```text
SafeDrive:
ego candidate
→ candidate-specific sparse world
→ explicit safety heads
→ trajectory score
→ selection

RiskWorld:
observed history
→ object-specific factual-distribution rollout
→ explicit risk state
→ risk-object identification
```

Key distinction:

```text
SafeDrive safety is action/candidate conditioned and decision-facing.
RiskWorld risk is history conditioned and monitoring-facing.
```

SafeDrive has candidate-specific PDM consequence labels but lacks reactive alternative-agent truth. RiskWorld does not even branch on alternative ego actions.

## RiskWorld vs DA-WAM

```text
DA-WAM:
ego trajectory candidate → 0.5s latent future → utility → argmax

RiskWorld:
object candidate → 3s relative-state rollout → object risk → risk-source threshold/rank
```

`candidate` means completely different things:

```text
DA-WAM candidate = ego action
RiskWorld candidate = observed object
```

Do not confuse their branch semantics.

## RiskWorld vs WoTE

```text
WoTE:
action candidate → multi-step consequence rollout → utility → select action

RiskWorld:
object identity → multi-step relation rollout → risk → identify object
```

Both use real multi-step future reasoning, but only WoTE places it inside an action-selection loop.

## RiskWorld vs GraphWorld

GraphWorld's future-aware world state directly conditions a planner but does not perform an explicit 3 s environment rollout. RiskWorld does perform a 60-step physical-time rollout, yet has no planner coupling.

Thus:

```text
world-rollout depth
and
planning coupling
are orthogonal axes.
```

## RiskWorld vs trajectory-geometric risk methods

Conventional trajectory methods:

```text
forecast motion
→ distance/collision rule
→ risky object
```

RiskWorld:

```text
learn relation dynamics
→ jointly supervise geometry + temporal risk
→ learned object-risk score
```

Risk is therefore learned jointly with future relation, rather than being only a deterministic post-processing rule.

---

# 12. Counterfactual / reactivity vector

Use the project-wide vector carefully because RiskWorld branches over **objects**, not ego actions.

```text
object-specific future output                         YES
action-candidate-specific future output               NO
alternative-ego-action future supervision             NO
reactive other-agent intervention truth               NO
intervention-response validation                      NO
```

The paper itself appropriately lists future `planner-conditioned counterfactual rollouts` as future work.

---

# 13. Evaluation semantics

Primary dataset:

```text
RiskBench
6,916 CARLA scenarios
map-based split
interactive / collision / obstacle / non-interactive
```

Primary task evaluation:

```text
frame-wise object-level risk identification / anticipation
```

Planning-aware diagnostic:

```text
LBC planner with filtered observations
```

This is not evidence of:

```text
RiskWorld-controlled reactive closed-loop planning
```

Current paper limitation states evaluation is simulation-only; long-tail interactions, severe occlusion and real-world generalization remain open.

---

# 14. Strongest conclusions vs non-conclusions

## DIRECTLY SUPPORTED

- object-level risk can be predicted from a learned multi-step latent ego–object relation rollout;
- explicit future relation + temporal-risk supervision improves overall risk-localization trade-off;
- recursive future rollout beats the matched no-rollout multihorizon decoder on overall F1;
- predicted risk sources retain planning-relevant information under filtered-observation diagnostics;
- predictive V-JEPA2 context, object visual grounding and relational contextualization are major contributors.

## NOT ESTABLISHED

- hypothetical ego actions cause correctly predicted alternative risk futures;
- surrounding agents react correctly to an ego intervention;
- risk prediction improves an integrated planner;
- better future relation fidelity monotonically produces better planning;
- the latent dynamics is a calibrated physical simulator;
- RiskWorld is a candidate-scoring or value model.

---

# 15. Final normalized identity

```text
RiskWorld
=
16-frame RGB + tracked objects + ego motion
→ frozen V-JEPA2 global/object features
+ structured ego-relative object histories
→ masked relation attention
→ one relation-aware token per object
→ object-wise RSSM-style recurrent latent rollout
   60 physical future steps / 3 s
→ future relative position + distance + temporal-risk curve
→ pooled object-risk score
→ risk-source identification

TRAINING TRUTH:
logged factual future ego/object tracks supervise future relation;
RiskBench risk-object/event annotations supervise object risk and temporal-risk curve;
no alternative ego-action branch or intervention-specific future truth exists.

PLANNING ROLE:
risk monitor / planning-relevance boundary anchor,
not an integrated planning WAM.
```

Canonical subtype:

```text
OBJECT-CENTRIC FACTUAL-RELATION ROLLOUT RISK WORLD MODEL
```

Ontology decision expectation:

```text
V1.3 RETAINED
NO V1.4 REQUIRED
```

Existing ontology already separates:

```text
explicit risk state
vs safety/value evaluator
vs world→planning coupling
vs action-conditioned future truth
```
