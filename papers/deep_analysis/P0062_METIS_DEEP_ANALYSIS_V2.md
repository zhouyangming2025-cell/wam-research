# P0062 Metis — Deep Analysis V2

Last updated: 2026-09-15

Status: **COMPLETE FIRST PASS — paper + official repository state audited; source implementation unavailable**

Paper: **Metis: A Generalizable and Efficient World-Action Model for Autonomous Driving and Urban Navigation**

Canonical research role in this repository:

```text
TRAINING-ONLY ASYMMETRIC WORLD-ACTION CO-TRAINING
→ WORLD-LOSS-SHAPED ACTION EXPERT
→ ACTION-ONLY FLOW POLICY AT DEPLOYMENT
```

Do **not** summarize Metis as “future video is generated and then used to plan.” That is exactly what its asymmetric mask is designed to avoid.

---

# 0. Source and version contract

Primary paper source:

```text
papers/raw_md/P0062_Metis/P0062_Metis.raw.md
arXiv: 2606.15869
paper version audited: v1, 2026-06-14
```

Official repository:

```text
LogosRoboticsGroup/Metis
latest public commit observed:
7677b62d786cff8bb2044b489bd41f3d59514b43
2026-06-16
```

As of **2026-09-15**, the official repository still contains only README/assets/license-level material. The README continues to mark inference code, training code and evaluation scripts as unreleased although the original release plan said August 2026.

Therefore the evidence status is:

```text
paper mechanism           PAPER-VERIFIED
official README claims    OFFICIAL-REPO VERIFIED
training/inference code   SOURCE-UNVERIFIED
```

This boundary is binding. Tensor-level claims below come from the paper equations/attention diagram unless explicitly labeled source-verified.

An unresolved reporting inconsistency also remains:

```text
method / README main setting: Wan2.2-5B VGE
expert-capacity ablation table: Wan2.2-14B VGE labels
```

Without released source/configs, do not silently reconcile these labels.

---

# 1. One-sentence scientific position

Metis does not make the planner consume an imagined future at test time. It co-trains an action expert with an action-conditioned future-video generation expert under an **asymmetric attention graph** in which action can influence future-video prediction but action cannot read future-video tokens; the future-video loss can nevertheless backpropagate into the action expert during training, after which explicit future-video generation is bypassed and the action expert denoises a trajectory directly from current context.

The minimal mechanism is:

```text
current observation + language + ego state
→ action expert
→ future action chunk
         ↓
         conditions
         ↓
future-video generation expert
→ factual future-video flow loss
         ↓ backward gradient
         └──────────────→ action expert

DEPLOYMENT:
current observation + language + ego state
→ action-only flow denoising
→ trajectory
```

The central scientific distinction is therefore:

```text
FORWARD training coupling:   action → world
BACKWARD training coupling:  world loss → action expert
DEPLOYED coupling:            current context → action only
```

This is neither online consequence evaluation nor ordinary two-head multitask learning with symmetric feature exchange.

---

# 2. What problem does Metis actually attack?

Metis combines three problems that should not be collapsed into one WAM claim.

## 2.1 Inference-efficiency problem

Many WAMs explicitly sample/generate future observations during action inference. Metis argues this is unnecessarily expensive for deployment.

Its design target is:

```text
learn future-world dynamics during training
but
remove explicit future-video sampling from the deployed planning path
```

This is a **future-knowledge lifecycle / deployment** problem.

## 2.2 Heterogeneous representation-interference problem

The paper argues that high-dimensional visual generation and low-dimensional action generation have different distributions. Fully mixing them can inject generative noise into the action representation.

Metis therefore uses a Mixture-of-Transformers structure:

```text
Video Generation Expert (VGE)
Action Expert (AE)
expert-specific projections / FFNs / heads
controlled token interaction
```

This is a **task-decoupling / gradient-routing** problem.

## 2.3 Generalization problem

The same broad model is evaluated on:

```text
NAVSIM-v2 / NAVSIM-v1 autonomous driving
CityWalker urban navigation
Unitree Go2 real-robot navigation
```

The authors interpret this as evidence that video-world priors plus action specialization transfer across tasks/embodiments. This is a generalization claim, but it should be kept separate from the narrower causal claim that future-video co-training improves planning.

---

# 3. Architecture: what is actually shared and what is not?

## 3.1 Video Generation Expert

The paper describes the VGE as inheriting a pretrained Wan2.2 video-generation backbone. Reused components include a video VAE and T5-based text conditioning. Its scientific role is:

```text
current visual context
+ language
+ future action condition
→ denoise/generate future-video latent
```

The VGE carries a large imported video-generation prior; therefore any planning gain cannot automatically be interpreted as newly learned driving dynamics.

## 3.2 Action Expert

The AE is a smaller diffusion/flow Transformer, approximately 1B parameters with hidden dimension 1024 in the reported main setting. It predicts a continuous action chunk.

NAVSIM-v2 action representation:

```text
8 waypoints
4 s horizon
0.5 s interval
waypoint = (x, y, heading)
```

CityWalker uses 5 `(x,y)` waypoints.

## 3.3 “Shared latent space” does not mean shared model

Metis says both experts interact in a shared latent space, but the paper also emphasizes expert-specific projections, FFNs and output heads.

Therefore the correct jointness decomposition is:

```text
same task graph / co-training              YES
controlled token interaction               YES
common conditioning context                YES
shared latent interaction dimension        YES
identical full parameter stack              NO
single undifferentiated output space        NO
symmetric world↔action forward exchange     NO
both future branches required at inference  NO
```

This is exactly why `joint world-action modeling` must not be a single binary ontology field.

---

# 4. The asymmetric attention mask is the core mechanism

Three token groups are used during training:

```text
current-observation latent tokens
noisy future-video tokens
noisy action tokens
```

All are language-conditioned; the structured self-attention then imposes a directional graph.

## 4.1 What action tokens can see

The paper states that action tokens are restricted to current visual observation/context. Crucially:

```text
action tokens CANNOT attend future-video tokens
```

Therefore the action predictor cannot cheat by reading ground-truth-correlated noisy future-video latents during training, and it is not dependent on generated future frames at inference.

## 4.2 What future-video tokens can see

Future-video tokens can attend:

```text
current observation
+
future action tokens
```

Hence the world branch is action-conditioned:

```text
action → future video
```

This gives the VGE an obligation to generate a future consistent with the proposed/predicted ego action.

## 4.3 Where does “world → action” happen then?

Not in the forward attention graph.

The paper appendix explicitly states that the generation loss can backpropagate through the action-conditioned connection into the AE. Thus the world branch influences the policy by **training gradients**:

```text
future-video target
→ L_video
→ VGE
→ gradient through dependence on action representation
→ AE
```

This distinction is one of the most important Metis results for the WAM ontology:

```text
world→action forward information flow = NO
world-loss→action gradient influence = YES
```

Calling both simply “world-action interaction” would erase the mechanism.

---

# 5. Training objective

Metis uses flow matching for both action and video.

## 5.1 Action flow loss

The action chunk is interpolated between Gaussian noise and the factual action target. The AE predicts the velocity field conditioned on current observation/context and language.

Conceptually:

```text
noise + current context
→ AE velocity field
→ factual action trajectory
```

## 5.2 Future-video flow loss

Future video latents are also flow-matched, conditioned on:

```text
current observation
+ language
+ predicted/future action representation
```

The target is the factual future video latent from the logged sequence.

## 5.3 Joint objective

The paper uses:

```text
L = L_action + λ L_video
λ = 1
```

The important scientific point is not merely “two losses exist.” Because future-video prediction depends on the action representation, `L_video` has a gradient route into AE. The auxiliary world task therefore shapes the policy itself.

However, supervision still comes from **one realized factual future**. The model does not receive matched real futures for many alternative ego actions.

Thus:

```text
action-conditioned future generation
!=
observed interventional/counterfactual future supervision
```

---

# 6. Inference: what remains and what disappears?

The paper’s deployment equation is effectively:

```text
a_future ~ p(a_future | z(current observation, language, ego state))
```

Explicit future observations are absent.

At inference:

```text
current observation
+ language instruction
+ ego state
→ current-context representation
→ action expert flow denoising
→ action chunk
```

Removed/bypassed from planning inference:

```text
future-video denoising
future-video tokens
explicit future-video output
future-video→action attention (already absent during training)
```

Retained knowledge:

```text
pretrained/current visual representation
AE parameters shaped by action loss
AE parameters additionally shaped by video-generation loss during co-training
```

Therefore Metis’s world knowledge has a lifecycle best summarized as:

```text
future-video auxiliary world task
→ asymmetric gradient shaping of policy
→ world-generation computation removed at deployment
```

This is not online imagination.

---

# 7. Strongest matched evidence

## 7.1 Co-training ablation: most direct world-related evidence

Appendix reports:

```text
without video co-training   87.4 PDMS / 87.9 EPDMS
with video co-training      89.1 PDMS / 89.5 EPDMS
```

This is the strongest direct evidence for the core claim:

> Under the reported action-policy family, adding future-video co-training improves planning.

It does **not** prove which property of the world task causes the gain.

Still unresolved:

```text
accurate future dynamics?
action-conditioned consistency?
auxiliary-task regularization?
extra gradient signal?
video-foundation prior?
more effective representation learning?
```

No matched experiment directly establishes that lower future-video prediction error monotonically improves planning.

## 7.2 Attention-mask ablation: directional coupling matters

At matched 320×384 resolution:

```text
Joint attention       87.4 navtest / 28.0 navhard EPDMS
Isolated              88.3         / 29.4
Asymmetric            88.8         / 31.6
```

Two scientifically useful facts follow.

First:

```text
Isolated > Joint
```

Full bidirectional/tight forward coupling is not automatically beneficial; it can harm the action policy.

Second:

```text
Asymmetric > Isolated
```

Some controlled coupling is beneficial. Given the mask semantics, this evidence is most consistent with **action-conditioned world-task gradient shaping**, not with action reading an imagined future.

The 640×768 asymmetric row reaches 89.5/32.2, but resolution changes simultaneously, so it is not part of the clean attention-mechanism comparison.

## 7.3 Expert-capacity ablation: policy and imported world prior both matter

Reported rows include:

```text
smaller VGE + ~0.24B AE      88.8 navtest / 28.8 navhard
larger VGE + ~0.21B AE       88.2         / 31.2
larger VGE + ~1.04B AE       89.5         / 32.2
```

This is not a clean monotonic “better world model → better planner” result. Larger VGE appears more useful on navhard while AE capacity also materially improves performance.

The correct attribution is therefore multi-factor:

```text
video foundation prior
+ world-task co-training
+ attention topology
+ AE capacity
+ input resolution
+ action denoising compute
```

---

# 8. Quality–latency frontier

Action-only denoising-step ablation:

```text
steps   navtest EPDMS   navhard EPDMS
1       87.2            30.4
2       89.2            31.2
5       89.4            31.4
10      89.5            32.2
```

This is a useful deployment curve: 2 steps recover most navtest quality, while harder navhard cases benefit more from extra denoising.

The cross-method latency table reports approximately:

```text
Metis with video       1.38 s
Metis action-only      0.17 s
```

on a single RTX 4090 in the reported comparison.

But the paper states the video setting uses 10 denoising steps while the action-only efficiency setting uses 2. Therefore:

```text
1.38 → 0.17 s
```

is a valid practical operating-point comparison, but **not a pure matched ablation isolating only removal of the video branch**. Part of the speedup also comes from fewer denoising steps.

The official README separately lists ~147 ms for the 2-step action-only row; treat the small 147 ms vs 0.17 s discrepancy as reporting/measurement-scope variation rather than silently equating them.

---

# 9. Prediction geometry under F07

Metis differs sharply from Drive-JEPA.

Drive-JEPA:

```text
random-mask same-window spatiotemporal completion
```

Metis:

```text
current observation
+ action condition
→ chronologically unseen future-video latent chunk
```

Thus F07 is approximately:

```text
CURRENT-CONTEXT + ACTION → UNSEEN FUTURE VIDEO
(flow-matched fixed-window generation)
```

The target is a factual future clip, not a randomly hidden token from the same observed window.

However, the training target remains one realized future under the logged behavior. The system does not establish intervention-valid future responses for arbitrary alternative action chunks.

---

# 10. Relation to the existing anchors

## 10.1 Metis vs LAW

Commonality:

```text
future/world supervision helps training
future object not consumed to choose action at deployment
```

Difference:

```text
LAW:
planner action → future latent predictor
future-latent loss shapes shared planner representation during planner training

Metis:
action representation → future-video VGE
video flow loss backpropagates into AE
separate experts + asymmetric attention
```

LAW is an action-aware auxiliary latent predictor. Metis is asymmetric world-action co-training with an action-only deployed policy.

## 10.2 Metis vs Epona

Epona:

```text
history → shared F
F → TrajDiT
F + action → VisDiT
joint trajectory + visual losses shape F
VisDiT can be optional for planning
```

Metis:

```text
separate VGE / AE experts
future-video tokens can see action
future action cannot see future video
video loss shapes AE backward
future-video inference intentionally bypassed
```

Both use visual generation as a training signal, but Metis makes the directionality and deployment decoupling explicit.

## 10.3 Metis vs Drive-JEPA

Drive-JEPA:

```text
predictive video pretraining happens before planner training
JEPA predictor discarded
encoder transferred
```

Metis:

```text
world/video loss and action loss coexist in one task-training graph
world loss can shape AE directly through gradients
future-video branch bypassed only at deployment
```

Thus both are “no online future” systems, but their lifecycle is different.

## 10.4 Metis vs WorldDrive

WorldDrive transforms a heavy world teacher into a lightweight future surrogate that remains online for ranking.

Metis retains no explicit future surrogate:

```text
WorldDrive: heavy future → distill → lightweight online future feature
Metis:      future-video co-training → weight/representation shaping → no future object online
```

## 10.5 Metis vs online consequence planners

WoTE / World4Drive / SeerDrive retain predicted future information on the decision path. Metis does not.

Therefore Metis should not be grouped with them merely because all use future supervision.

---

# 11. Prior-art attack: Fast-WAM boundary

Metis itself cites **Fast-WAM: Do World Action Models Need Test-Time Future Imagination?** and says its decoupled inference paradigm is inspired by it.

Hence the broad idea:

```text
video/world co-training during training
+
skip explicit future generation at test time
```

is **not uniquely established by Metis**.

Metis’s more specific contribution is the mechanism by which this is achieved in its setting:

```text
Mixture-of-Transformers specialized experts
+
asymmetric attention
+
action-conditioned video task
+
training-gradient coupling without future-video→action forward dependence
+
autonomous-driving + urban-navigation evaluation
```

This historical control is important because otherwise “joint training, decoupled inference” could be mistaken for a wholly new WAM lifecycle.

---

# 12. Evaluation semantics

## Autonomous-driving evaluation

NAVSIM-v1/v2 results are data-driven planning evaluations. Under this project’s taxonomy, do not automatically upgrade NAVSIM into a fully reactive environment closed loop merely because the paper calls navhard a closed-loop benchmark.

The key automotive evidence remains planning quality under NAVSIM’s evaluation protocol.

## Real robot

The Unitree Go2 experiments are genuine environment execution-feedback tests for robot navigation/obstacle avoidance. They provide useful evidence of cross-embodiment policy feasibility/generalization.

But:

```text
real-robot navigation closed loop
!=
real-car autonomous-driving closed loop
```

Keep the domain distinction explicit.

## World-generation evaluation

The paper provides qualitative future-video examples and discusses failures, but no strong dedicated quantitative world-fidelity benchmark was identified in the audited text.

Therefore world-generation quality should not be used as a quantitative causal explanation for the planning scores.

---

# 13. Evidence boundary

## AUTHOR CLAIM

Metis learns world dynamics through video generation during training, uses asymmetric attention to improve action learning while avoiding generation noise, and preserves strong planning/generalization with efficient action-only inference.

## DIRECT EXPERIMENTAL EVIDENCE

```text
co-training:      87.9 → 89.5 EPDMS
joint/isolated/asymmetric at same resolution:
                  87.4 / 88.3 / 88.8 navtest
                  28.0 / 29.4 / 31.6 navhard
action denoise:   1/2/5/10-step quality curve reported
latency:          action-only operating point far faster than video-generating operating point
```

Real-robot navigation also shows that the trained policy can execute closed-loop obstacle avoidance outside the automotive benchmark.

## WHAT THIS PROVES REASONABLY WELL

```text
1. Future-video co-training can improve the reported action policy even when future video is absent from deployed action inference.
2. Fully joint/symmetric token mixing is not necessary and is worse than the reported asymmetric design.
3. The asymmetric design provides a useful training-only coupling that preserves action-only deployment.
4. Explicit future-video generation is not necessary to retain strong planning performance in this architecture.
```

## WHAT IT DOES NOT PROVE

```text
1. The deployed policy performs online world-model imagination.
2. Action tokens consume predicted future-video features at inference.
3. Better video prediction fidelity causally or monotonically yields better planning.
4. Generated alternative futures are intervention-valid/reactive counterfactuals.
5. The full planning gain comes from world dynamics rather than auxiliary regularization, imported video priors, AE capacity or resolution.
6. “Joint training, decoupled inference” as a broad concept originates with Metis.
```

## STRONGEST ALTERNATIVE EXPLANATION

A powerful imported video prior plus an auxiliary action-conditioned generative loss acts as structured regularization/representation shaping for a large direct flow policy; the policy’s own capacity, current visual features, image resolution and denoising compute account for a substantial fraction of final performance.

---

# 14. Ontology residue test

Metis initially appears to introduce a new concept:

```text
forward action→world
but backward world-loss→action
with no future-world→action forward arrow
```

After ontology merge testing, this does **not** require a new axis.

It is already representable by:

```text
E01/E02  action→world conditioning
J02/J03  no online future computation/consumption
J04      causal coupling direction
L02/L03  representation vs parameter sharing
L04      gradient coupling direction
L06      joint-loss semantics
M01-M03  lifecycle and deployed model transformation
```

Therefore:

```text
Ontology V1.2 remains sufficient after Metis stress test.
NO V1.3 dimension added.
```

This is a positive result: the coordinate system survives a qualitatively different WAM without paper-specific expansion.

---

# 15. Final normalized identity

```text
Metis
=
pretrained video-generation expert
+ separate action flow expert

TRAINING:
current context → action expert → action chunk
                         ↓
                  conditions VGE
                         ↓
factual future video → video flow loss
                         ↓ gradient
                  shapes action expert

INFERENCE:
current context
→ action expert denoising
→ trajectory

explicit future-video generation = BYPASSED
```

Primary scientific subtype:

```text
TRAINING-ONLY ASYMMETRIC WORLD-ACTION CO-TRAINING
```

Deployment subtype:

```text
ACTION-ONLY FLOW POLICY
```

Most important stable control strengthened by this paper:

```text
world-task benefit
!=
online future consumption

joint training
!=
symmetric forward coupling

world→action gradient influence
!=
world→action inference information flow
```
