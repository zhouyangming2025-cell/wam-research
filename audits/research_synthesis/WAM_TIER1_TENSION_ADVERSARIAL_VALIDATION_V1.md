# WAM Tier-1 Tension Adversarial Validation V1

Last updated: 2026-09-15

Status: **BROADER-LITERATURE ADVERSARIAL VALIDATION — COMPLETE FIRST PASS**

Scope:

```text
T2 explicit consequence rollout vs compact world-state conditioning
T3 training-time world modeling vs deployment-time model-basedness
T5 factual-future learning vs intervention-correct consequence modeling
T6 structured interaction semantics vs true reactive dynamics
```

This audit deliberately searches outside the eleven WAM anchors. It uses adjacent literature from model-based RL, decision-focused representation learning, interactive prediction/planning, reactive traffic simulation, causal imitation learning, and counterfactual driving world models.

Verdict vocabulary:

```text
RESOLVED
PARTIALLY RESOLVED
SURVIVES
INSUFFICIENT EVIDENCE
```

A verdict applies to the scientific tension, not to novelty of a proposed method.

---

# Executive verdict

| Tension | Verdict | Main update |
|---|---|---|
| T2 rollout vs compact conditioning | **SURVIVES — narrowed** | Value-equivalence/bisimulation literature shows full environmental fidelity is unnecessary, but no matched autonomous-driving comparison establishes when direct compact conditioning can replace online action-conditioned branching. |
| T3 training-time WM vs online model-basedness | **PARTIALLY RESOLVED** | Dreamer/MBPO and especially WPT show substantial world-model reasoning can be amortized/distilled into a policy; online planning remains strongly useful in MuZero/TD-MPC2. The unresolved question is conditional: which information must be recomputed online under shift/hard interaction? |
| T5 factual future vs intervention correctness | **PARTIALLY RESOLVED — H2 strengthened** | Causal theory and a 2026 matched-counterfactual driving-WM benchmark directly invalidate the universal assumption that action-conditioned factual prediction is automatically counterfactual. Reactive intervention validity remains open. |
| T6 interaction representation vs reactive dynamics | **SURVIVES — prior-art scope narrowed** | Reactive/conditional interaction modeling is established prior art (M2I, GameFormer, TrafficBots, WOSAC/Waymax, reaction-uncertainty planning). What remains unresolved is the matched marginal value of reactive response modeling over strong structured interaction representations. |

---

# T2 — Explicit consequence rollout vs compact world-state conditioning

## Original competing hypotheses

```text
H1 explicit action-conditioned rollout is necessary for hard interactive decisions
H2 compact decision-relevant world state is sufficient for most decisions
```

## Strong external evidence against a naive H1

### Value Equivalence Principle — Grimm et al., NeurIPS 2020

The value-equivalence principle argues that limited model capacity is better spent learning a model directly useful for planning rather than accurately reproducing full state transitions. Two models can be decision-equivalent if they induce the same Bellman updates even when their environmental predictions differ.

Scientific implication:

```text
accurate full-world reconstruction is NOT universally necessary for planning
```

This gives a formal foundation for GraphWorld-like / decision-relevant compact modeling, although value-equivalent models can still be used inside lookahead planning.

### Value-Aware Model Learning / Iterative VAML

Decision-aware model-learning literature predating modern WAMs explicitly optimizes transition models according to their downstream value/planning effect instead of maximum-likelihood state prediction.

Scientific implication:

```text
decision relevance can be a stronger model-learning target than generic dynamics fidelity
```

### Bisimulation / DeepMDP / DBC

DeepMDP and bisimulation-based representation learning show that task-irrelevant observation variation can be discarded while retaining control-relevant transition/reward structure. DBC even demonstrates this in a highway-driving control setting.

Scientific implication:

```text
compact control-sufficient state is a mature theoretical/empirical idea,
not a GraphWorld-specific novelty
```

## Strong external evidence that online rollout can remain useful

### MuZero

MuZero learns only reward/value/policy-relevant dynamics rather than reconstructing observations, but still performs online lookahead tree search. More search computation can substantially improve performance.

### TD-MPC2

TD-MPC2 performs online local trajectory optimization in a learned decoder-free latent world model and achieves strong continuous-control results over many tasks.

### Imagination-Augmented Agents

I2A learns how to interpret model rollouts as context for its policy and can ignore unreliable imagination when appropriate. This is conceptually between direct conditioning and fixed model-based planning.

## Adversarial conclusion

External literature falsifies the strongest version of:

```text
"good decisions require accurate/full future reconstruction"
```

but it does **not** resolve:

```text
compact direct state conditioning
vs
online action-conditioned branching / rollout
```

under matched data, backbone, compute and interaction difficulty in autonomous driving.

### Verdict

```text
T2 = SURVIVES — NARROWED
```

### New canonical question

> **When does online action-conditional branching provide decision information that cannot be adequately amortized into a compact world state or policy representation at the same compute/data budget?**

### Falsification target

One architecture / one dataset / one training budget:

```text
A compact W → direct policy
B candidate → endpoint latent → select
C candidate → recurrent consequence rollout → select
```

Match deployment FLOPs/latency and stratify by interaction response dependence and distribution shift.

---

# T3 — Training-time world modeling vs deployment-time model-basedness

## Original competing hypotheses

```text
H1 world modeling is mainly useful as a training regularizer/representation teacher
H2 online world inference is necessary for rare/OOD/interaction-heavy decisions
```

## Evidence that world knowledge can be amortized into a policy

### MBPO — Janner et al., NeurIPS 2019

MBPO uses short world-model rollouts to generate policy-training data while ultimately optimizing a model-free policy. It explicitly studies the trade-off between model use and compounding rollout error.

Key control:

```text
short model use during training can be beneficial
without requiring long online model rollout at deployment
```

### Dreamer family / DreamerV3

Dreamer learns a latent world model and trains actor-critic behavior on imagined trajectories. At action time the actor acts from the learned latent state; it does not run an MPC-style branch search over alternative future rollouts for each action decision.

Important precision:

```text
no online lookahead rollout
!=
no online learned state model / latent filtering
```

### WPT — World-to-Policy Transfer via Online World Model Distillation, CVPR 2026

WPT is particularly direct for autonomous driving. A world-model-guided teacher evaluates future dynamics; policy distillation and world-reward distillation transfer this reasoning to a lightweight student. The reported student has up to 4.9x faster inference while retaining most gains.

Scientific implication:

```text
at least a substantial fraction of online world reasoning CAN be compressed into a deployable policy
```

This is a direct prior-art warning against framing `world teacher → policy-only deployment` itself as novel.

## Evidence that online model use can still matter

### MuZero

Online search over the learned model provides clear performance gains as planning compute increases.

### TD-MPC2

Online latent MPC remains the core action-selection mechanism and performs strongly over diverse continuous-control tasks.

### WAM anchors

WoTE / WorldDrive / World4Drive provide autonomous-driving evidence that retaining an online future/consequence object can improve planning relative to matched weaker/no-future variants.

## What is NOT resolved

No identified work cleanly trains the same autonomous-driving system and then compares:

```text
full online consequence reasoning
vs
perfectly matched distilled/action-only policy
```

while separately testing:

```text
in-distribution easy scenes
rare interactions
OOD shifts
novel negotiation patterns
```

### Verdict

```text
T3 = PARTIALLY RESOLVED
```

The universal claim `online WM is necessary` is false. The remaining scientific question is conditional.

### New canonical question

> **Which future/consequence computations are amortizable into policy weights, and which must be recomputed online because they depend on scene-specific alternatives, uncertainty or interaction response?**

### Falsification target

Train an online teacher and a distilled student from identical data. Match student capacity/latency controls and test the teacher-student gap against scene rarity, interaction dependence, OOD distance and candidate ambiguity.

---

# T5 — Factual-future learning vs intervention-correct consequence modeling

## Original competing hypotheses

```text
H1 large factual datasets + action conditioning are sufficient to learn useful intervention consequences
H2 without intervention-diverse/reactive supervision, action-conditioned predictions can be plausible but wrong under alternative ego actions
```

## Causal-learning prior: Causal Confusion in Imitation Learning — de Haan et al., 2019

This work shows that passive imitation can learn the wrong causal relationship under distribution shift and that targeted interventions/environment interaction can identify the correct causal structure. The paper includes realistic driving experiments.

Scientific implication:

```text
observational fit does not guarantee correct action→outcome causal structure
```

## Direct driving-world-model evidence: How Can Driving World Models Do Counterfactual Prediction? — Zhang et al., arXiv:2608.11601, 2026-08

This paper directly attacks a common driving-WM claim. It distinguishes:

```text
direct action-conditioned prediction:
p(Y | history, alternative_action)

from episode-specific counterfactual prediction:
p(Y_alternative | history, factual_continuation)
```

Using CARLA, it builds matched factual and counterfactual outcomes for the same underlying world. Across representative diffusion and autoregressive driving world models, direct action-conditioned generation fails to match the counterfactual ground truth. A simple abduction-inspired method that carries factual evidence into the alternate view improves recovery.

This is particularly important because it provides the type of **matched counterfactual ground truth** missing from our eleven WAM anchors.

### What this falsifies

It falsifies the universal statement:

```text
alternative action condition + shared history
⇒ true episode-specific counterfactual
```

Action controllability alone is insufficient.

### Important boundary

The study intentionally uses a short horizon where surrounding agents do **not** react to the changed ego action. Therefore it addresses factual-vs-counterfactual episode identity, not full reactive multi-agent intervention dynamics.

## Reactive simulator prior

TrafficBots explicitly defines counterfactual simulation where a player/ego can deviate from logged behavior and learned bot agents should react naturally. Waymax and WOSAC provide infrastructure/metrics for interactive multi-agent simulation.

These works show that the field already recognizes `reactive alternative-action simulation` as a separate problem from ordinary forecasting.

### Verdict

```text
T5 = PARTIALLY RESOLVED — H2 SUBSTANTIALLY STRENGTHENED
```

We should no longer present `candidate-specific output != counterfactual truth` merely as our synthesis insight; it is now directly supported by causal theory and controlled driving-WM evidence.

### New canonical question

> **How should a planning-centric WAM identify and validate intervention-correct consequence distributions when both episode-specific latent state and surrounding-agent reactions change under ego alternatives?**

This remaining question combines rung-2 intervention response and rung-3 episode-specific counterfactual identification; current direct action-conditioned WAM training does not establish either automatically.

---

# T6 — Structured interaction semantics vs true reactive dynamics

## Original competing hypotheses

```text
H1 most practical safety gains come from better interaction representation; explicit reactive dynamics add diminishing returns
H2 negotiation-heavy scenarios require modeling how other agents respond to ego alternatives
```

## Prior art showing reactive interaction modeling is established

### M2I — CVPR 2022

M2I explicitly decomposes interacting pairs into influencer and reactor, then predicts the reactor conditionally on the influencer trajectory. This is stronger than independent/marginal agent prediction, but it is primarily a prediction benchmark rather than ego-plan intervention validation.

### GameFormer — ICCV 2023

GameFormer uses hierarchical game-theoretic decoding where each level responds to behavior from the preceding level, jointly reasoning about ego planning and surrounding agents. It reports gains on interaction prediction and planning.

### DIPP / planning-centric prediction

DIPP shows joint prediction-planning training improves over separately trained prediction in open- and closed-loop tests. It establishes that downstream planning relevance changes what a useful prediction model should learn.

### TrafficBots — ICRA 2023

TrafficBots is explicitly recurrent and closed-loop. At inference, TrafficBots agents process non-player/player states so that they can react to deviations. The paper distinguishes non-reactive log replay, scripted behavior and learned reactive agents.

### WOSAC / Waymax

Waymo's Sim Agents Challenge and Waymax explicitly target realistic interactive agents and closed-loop simulation. This makes reactive-agent behavior an established evaluation object rather than a hypothetical missing concept.

### Reaction-Uncertainty-Aware Motion Planning — Jang et al., IEEE Access 2026

This work is especially discriminative: it argues that even ego-conditioned prediction can be insufficient if it does not model **reaction uncertainty**. Its conditional multi-modal predictor + tree planner reports up to 32.39% planning improvement over a uni-modal conditional baseline, particularly in interactive scenarios.

Scientific implication:

```text
ego-conditioned mean response is not the end of the problem;
distribution over possible reactions can matter for planning
```

## What this does NOT establish

The literature does not provide the exact matched test we need:

```text
strong structured interaction representation only
vs
same representation + explicit ego-conditioned reactive transition
```

with identical perception, planner, data and compute, stratified by response dependence.

GraphWorld therefore remains a valid control showing structured representation alone can yield large gains; reactive-prediction literature shows response modeling can yield additional gains in interaction-heavy regimes.

### Verdict

```text
T6 = SURVIVES — NARROWED
```

### Novelty guard

Do NOT claim as novel:

```text
model surrounding-agent reactions to ego plans
conditional interaction prediction
reactive multi-agent simulation
reaction uncertainty
```

All are established prior art.

### New canonical question

> **What is the marginal planning value of explicit ego-conditioned reaction distributions beyond a strong interaction-aware latent representation, and how does that value scale with negotiation/response dependence?**

---

# Cross-tension synthesis

The broader literature changes the field picture in three important ways.

## 1. The real axis is not `world model vs no world model`

A mature control literature already distinguishes:

```text
full generative dynamics
value-equivalent / decision-aware model
compact bisimulation state
training-time imagination
online latent planning
reactive multi-agent simulator
```

WAM papers are rediscovering several of these choices under new visual/latent architectures.

## 2. `Counterfactual` needs stricter vocabulary

Going forward use:

```text
conditional future prediction
interventional prediction
episode-specific counterfactual prediction
reactive counterfactual simulation
```

as distinct terms.

Never infer a higher rung from action-conditioning alone.

## 3. The most promising scientific boundary is conditional computation

T2 + T3 + T6 converge on one high-level problem:

```text
What future reasoning must be computed online for THIS scene,
and what can be amortized into a compact representation/policy?
```

The likely answer is not all-or-nothing. Existing evidence suggests online reasoning value should depend on:

```text
interaction response dependence
uncertainty / multimodality
rarity / OOD distance
candidate ambiguity
irreversibility / safety cost
```

This is a scientific tension, not yet a research-gap claim.

---

# References used in this adversarial pass

Core external controls:

```text
Grimm et al. 2020 — The Value Equivalence Principle for Model-Based RL
Farahmand 2018 — Iterative Value-Aware Model Learning
Gelada et al. 2019 — DeepMDP
Zhang et al. 2021 — Learning Invariant Representations for RL without Reconstruction / bisimulation
Janner et al. 2019 — MBPO
Hafner et al. — Dreamer / DreamerV3
Schrittwieser et al. — MuZero
Hansen et al. 2024 — TD-MPC2
Jiang et al. 2026 — WPT: World-to-Policy Transfer via Online World Model Distillation
de Haan et al. 2019 — Causal Confusion in Imitation Learning
Zhang et al. 2026 — How Can Driving World Models Do Counterfactual Prediction?
Sun et al. 2022 — M2I
Huang et al. 2023 — GameFormer
Huang et al. 2023/2024 — DIPP
Zhang et al. 2023 — TrafficBots
Montali et al. 2023 — Waymo Open Sim Agents Challenge
Gulino et al. 2023 — Waymax
Jang et al. 2026 — Reaction-Uncertainty-Aware Motion Planning
```

---

# Gate decision

This adversarial pass does NOT authorize immediate method design.

Next required step:

```text
turn surviving/narrowed tensions into falsifiable problem statements
→ identify whether each has a clean experimental intervention
→ check nearest-neighbor 2025–2026 AD papers for overlap
→ only then declare candidate research gaps
```
