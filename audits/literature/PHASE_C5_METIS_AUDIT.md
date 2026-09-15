# PHASE C.5 — Metis Audit

Last updated: 2026-09-15

Status: **COMPLETE FIRST PASS — PAPER/README VERIFIED; IMPLEMENTATION SOURCE UNAVAILABLE**

Paper:

```text
Metis: A Generalizable and Efficient World-Action Model for Autonomous Driving and Urban Navigation
arXiv:2606.15869 v1
```

Official repository:

```text
LogosRoboticsGroup/Metis
latest observed public commit:
7677b62d786cff8bb2044b489bd41f3d59514b43
```

Canonical deep read:

```text
papers/deep_analysis/P0062_METIS_DEEP_ANALYSIS_V2.md
```

---

# 1. Audit verdict

Metis is a legitimate planning-centric WAM anchor, but its deployed mechanism must be described precisely:

```text
TRAINING:
action expert predicts action chunk
→ action tokens condition future-video expert
→ future-video flow loss backpropagates into action expert

INFERENCE:
current context → action expert → trajectory
future-video generation bypassed
```

Thus Metis is **not** an online `predict future → inspect future → choose action` planner.

Canonical label:

```text
TRAINING-ONLY ASYMMETRIC WORLD-ACTION CO-TRAINING
→ ACTION-ONLY FLOW POLICY
```

---

# 2. Source/version audit

## Paper

Primary research copy:

```text
papers/raw_md/P0062_Metis/P0062_Metis.raw.md
```

The paper contains method equations, attention-mask semantics, ablations, latency comparisons and appendix discussion sufficient for a paper-level mechanism reconstruction.

## Official repository state

As of 2026-09-15 the official repository still exposes README/assets/license material but no runnable implementation. The README marks:

```text
Inference code      [ ]
Training code       [ ]
Evaluation scripts  [ ]
```

although the original project announcement planned an August 2026 release.

Therefore:

```text
paper graph        verified from paper
README claims      verified from official repo
code execution     unavailable
implementation     SOURCE-UNVERIFIED
```

Do not write `source-verified` for attention implementation, gradient routing, inference pruning or exact runtime path until code is released.

## Reporting inconsistency to preserve

The method text/official README identify the main VGE as Wan2.2-5B, while an expert-capacity ablation table labels Wan2.2-14B variants. This is unresolved without code/configs and must remain an explicit uncertainty rather than being silently normalized.

---

# 3. Reconstructed training graph

Inputs:

```text
current front RGB observation
ego/agent state
language instruction
logged future action chunk
logged future video
```

Experts:

```text
VGE = pretrained video generation expert
AE  = smaller action diffusion/flow Transformer
```

Training tokens:

```text
current-observation latent tokens
noisy future-video tokens
noisy future-action tokens
```

Attention dependency:

```text
action tokens → current observation only
future-video tokens → current observation + future-action tokens
```

Hence forward causal graph:

```text
action → world
world future → action = MASKED
```

Losses:

```text
L_action = action flow-matching loss
L_video  = future-video flow-matching loss conditioned on action
L_total  = L_action + L_video
```

Appendix states VGE loss gradients can backpropagate into AE. Therefore training coupling is:

```text
forward:   AE/action → VGE/world
backward:  L_video → AE
```

This is the key mechanism to preserve in all cross-paper comparisons.

---

# 4. Reconstructed inference graph

Paper deployment formulation:

```text
current observation + language + ego state
→ current-context latent
→ action expert denoising
→ action chunk / trajectory
```

Not required online:

```text
future-video tokens
future-video denoising
explicit future image/video output
future-video→action forward attention
```

Therefore:

```text
online predicted future object = NONE
online future consumption      = NO
online world rollout           = NO
```

The predictive knowledge survives only through current-context representation and parameters shaped during co-training.

---

# 5. Supervision and ground-truth lineage

## Action supervision

NAVSIM-v2:

```text
factual ego trajectory
8 waypoints
4 s horizon
0.5 s interval
(x,y,heading)
```

Action loss is flow matching toward the logged factual action chunk.

## Future-world supervision

```text
logged factual future video
→ VAE/video latent
→ future-video flow target
```

The VGE is conditioned on the predicted/future action representation.

Important boundary:

```text
one logged action + one factual future
!=
K observed alternative-action futures
```

No intervention-valid alternative-agent response supervision is established.

---

# 6. Strongest matched evidence

## A. Video co-training on/off

```text
w/o video co-training   87.4 PDMS / 87.9 EPDMS
w/  video co-training   89.1 PDMS / 89.5 EPDMS
```

**Supports:** world/video auxiliary co-training helps the action-policy family.

**Does not isolate:** world-prediction fidelity, causal dynamics accuracy, action-conditioned counterfactual correctness, imported video prior, or generic multi-task regularization.

## B. Attention topology at matched resolution

320×384:

```text
Joint       87.4 navtest / 28.0 navhard EPDMS
Isolated    88.3         / 29.4
Asymmetric  88.8         / 31.6
```

**Supports:** full symmetric coupling is unnecessary/harmful here; controlled asymmetric coupling improves over full isolation.

**Mechanistic interpretation:** because action cannot read future-video tokens, the asymmetric gain cannot be described as action directly consuming imagined futures. The paper-level path is training-gradient influence.

## C. Action denoising compute

```text
steps  navtest  navhard
1      87.2     30.4
2      89.2     31.2
5      89.4     31.4
10     89.5     32.2
```

Provides a useful quality–compute operating curve.

## D. Expert capacity

The VGE/AE scale rows show that both world prior capacity and action-expert capacity can change scores. The evidence is not a clean monotonic world-quality→planning relation.

---

# 7. Efficiency audit

Paper table reports on RTX 4090:

```text
Metis with video        1.38 s
Metis action-only       0.17 s
```

But the comparison uses different practical denoising settings:

```text
video setting       10 steps
action-only setting  2 steps
```

Thus the reported ~8× speedup is a meaningful **operating-point** result, but not a matched ablation that removes only the video branch while keeping all other compute identical.

The official README also lists roughly 147 ms for action-only 2-step inference. Keep the measurement-scope discrepancy visible.

---

# 8. World-quality evidence audit

No dedicated quantitative future-video fidelity metric such as FVD/PSNR/SSIM was identified in the audited paper text. The paper provides qualitative generated-video examples and a failure discussion.

Therefore:

```text
better world-generation fidelity → better planning
```

is **NOT ESTABLISHED**.

O07 must remain ABSENT rather than inferred from the co-training planning gain.

---

# 9. Evaluation-regime audit

## NAVSIM

Use project terminology:

```text
NAVSIM v1/v2 = data-driven / non-reactive planning evaluation
```

The paper calls navhard closed-loop, but this wording should not be silently mapped to reactive environment execution-feedback in the cross-paper taxonomy.

## Unitree Go2

The paper reports real-robot execution-feedback obstacle-avoidance experiments in indoor/outdoor settings.

This supports:

```text
real-robot navigation feasibility / generalization
```

but not:

```text
real-car autonomous-driving closed-loop validation
```

---

# 10. Historical / prior-art audit

The paper cites Fast-WAM and explicitly says the decoupled inference paradigm is inspired by it.

Therefore the broad principle:

```text
world/video co-training during training
+ skip explicit future generation at inference
```

must not be attributed as uniquely introduced by Metis.

Metis's more specific mechanism contribution is:

```text
MoT specialized experts
+ asymmetric token visibility
+ action-conditioned world generation
+ video-loss gradient shaping of AE
+ action-only flow inference
```

---

# 11. Cross-anchor normalization

```text
LAW
world future = auxiliary latent target during planner training
world loss shapes shared representation
future object absent online

Epona
shared F feeds trajectory + visual generative branches
joint losses shape shared F
visual branch optional for planning

Drive-JEPA
predictive video pretraining is a prior stage
encoder transferred; predictor discarded

WorldDrive
heavy future teacher distilled into lightweight future surrogate
surrogate remains online

Metis
future-video task co-trained with policy
forward action→world; backward world-loss→AE
future-video computation removed online
```

This is a genuinely distinct lifecycle/mechanism combination, but it is expressible by the existing ontology.

---

# 12. Ontology residue verdict

Potential residue:

```text
forward coupling direction differs from gradient coupling direction
```

Existing ontology already separates:

```text
E01/E02 action→world forward condition
J04 causal coupling direction
L04 gradient coupling direction
M01-M03 lifecycle / model-class transformation
```

Therefore:

```text
NO ontology expansion required.
Ontology V1.2 survives Metis stress test.
```

---

# 13. Scientific evidence boundary

## AUTHOR CLAIM

World/video generation co-training teaches useful dynamics to the action expert; asymmetric attention prevents future-generation noise from polluting action inference; action-only deployment preserves planning quality with much lower latency.

## DIRECT EVIDENCE

```text
+1.6 EPDMS from video co-training in the reported ablation
asymmetric > isolated > joint at matched low resolution
quality improves with additional action denoising steps
strong NAVSIM results + real-robot navigation demonstrations
```

## OUR INFERENCE

The most precise mechanism is **world-loss-shaped policy learning**, not online world simulation. The action expert benefits from future-video supervision through gradient coupling, while its forward inference policy is intentionally future-video independent.

## DOES NOT PROVE

```text
online imagination
future-video→action forward reasoning
world fidelity→planning monotonicity
counterfactual/reactive action-conditioned future truth
unique historical novelty of training-only world co-training
```

## STRONGEST ALTERNATIVE EXPLANATION

A large pretrained video prior and action-conditioned auxiliary generation loss provide structured regularization/representation shaping to a capable direct action-flow model; AE scale, resolution and denoising compute materially contribute to final scores.

---

# 14. Final audit label

```text
Metis
=
ASYMMETRIC WORLD-LOSS-SHAPED ACTION POLICY

training lifecycle:
JOINT VIDEO/ACTION CO-TRAINING

inference lifecycle:
ACTION-ONLY FLOW DENOISING
```
