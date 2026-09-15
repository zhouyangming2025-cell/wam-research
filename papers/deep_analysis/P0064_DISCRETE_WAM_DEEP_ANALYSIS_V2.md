# P0064 Discrete-WAM — Dimension-first Deep Analysis V2

Last updated: 2026-09-15

Status: **COMPLETE FIRST PASS — arXiv v2 audited; official implementation repository not identified**

Paper: **Discrete-WAM: Unified Discrete Vision-Action Token Editing for World-Policy Learning**

Canonical research role in this repository:

```text
SHARED-BACKBONE MULTI-TASK DISCRETE WORLD-POLICY PRETRAINING
→ HIERARCHICAL DECISION-CONDITIONED ACTION TOKEN EDITING
→ POLICY-ONLY PLANNING INFERENCE
```

Do **not** summarize Discrete-WAM as either:

```text
one shared world/action codebook
```

or:

```text
online future-world rollout → action selection
```

Both are scientifically inaccurate for the audited paper.

---

# 0. Source and version contract

Primary source:

```text
arXiv:2606.05645v2
v1: 2026-06-04
v2: 2026-06-09
```

Current source boundary:

```text
paper / appendix / arXiv HTML/PDF     PAPER-VERIFIED
official implementation repository    NOT IDENTIFIED as of 2026-09-15
exact code-level scheduler / detach / task sampling SOURCE-UNVERIFIED
```

Searches for an official Discrete-WAM GitHub implementation did not identify a repository attributable to the paper/authors. Do not infer implementation details from similarly named projects.

---

# 1. Executive verdict

The strongest scientifically defensible interpretation is:

> Discrete-WAM places discretized visual future states, discrete high-level decisions and discretized ego actions under a shared decoder-only Transformer and a unified token-editing/multitask training interface; however visual and action tokens use **separate vocabularies/codebooks**, and the downstream NAVSIM planner can generate decisions/actions without first generating future visual tokens.

The mechanism should therefore be decomposed into two layers.

## Layer A — unified world/policy pretraining capability

```text
current context
→ shared Transformer

world task:
context + future actions
→ future visual tokens

policy task:
context + decision
→ action tokens

world-policy task:
context
→ interleaved future action / visual tokens
```

## Layer B — deployed planning policy

```text
current context
→ decision token
→ parallel / iterative action-token editing
→ trajectory

future visual-token generation = NOT REQUIRED
```

Thus:

```text
training/model capability can be joint world+policy
while
planning execution graph can remain action-only
```

This distinction is central to the paper's placement relative to Metis, Epona, World4Drive and WoTE.

---

# 2. What exactly is discrete?

Discrete-WAM discretizes at least three semantically different objects:

```text
visual/world state tokens
high-level decision tokens
ego action tokens
```

But they are **not one homogeneous vocabulary**.

## 2.1 Visual/world tokens

The visual path uses a VQ-style visual tokenizer and a large visual vocabulary.

Audited paper setting:

```text
visual codebook size K_V = 16,384
visual patch/token granularity built from image/video patches
```

The continuous visual feature is quantized to discrete indices, embedded/projected into the shared Transformer hidden dimension, and trained with token classification/reconstruction objectives.

Scientific meaning:

```text
visual token = quantized visual/world-state symbol
```

but the paper does not establish that one token has a clean object-level or physical meaning such as `front vehicle braking` or `lane boundary`. Its semantics are learned through reconstruction/generation and downstream multitask training.

Therefore:

```text
discrete visual token
!= explicit object / occupancy / risk token
```

## 2.2 Action tokens

Action discretization is physically much more explicit.

The future ego trajectory is fitted/interpreted through a smooth trajectory representation, and the paper discretizes ego-centric planar acceleration:

```text
(a_x, a_y)
```

using approximately:

```text
range: [-4, 4] m/s^2 per axis
60 bins on x
60 bins on y
→ 60 × 60 = 3,600 action prototypes
```

Rather than relying only on a hard nearest-bin label, the method constructs soft labels over neighboring acceleration prototypes via bilinear interpolation.

Scientific meaning:

```text
action token
≈ discrete local acceleration prototype
```

This is materially different from the learned VQ visual token semantics.

## 2.3 Decision tokens

The policy also predicts a high-level decision token before dense action editing.

The paper constructs about 400 decision candidates from combinations of lateral/path alternatives and longitudinal/speed profiles. A decision label is selected using an EPDMS-style evaluation over candidate decisions.

Thus:

```text
decision token
= high-level behavioral / planning skeleton
```

rather than a world-state token.

---

# 3. First major correction: `shared discrete token space` does not mean shared codebook

The paper's high-level language emphasizes aligned/shared discrete vision-action tokens. The appendix, however, defines visual and action token vocabularies separately.

Canonical decomposition:

```text
same codebook / same token vocabulary?       NO
separate visual vocabulary?                  YES
separate action vocabulary?                  YES
common Transformer hidden interface?         YES
same decoder-only backbone?                  YES
same multitask token-edit framework?         YES
same sequence can contain world+action?       YES
joint losses/gradients in world-policy stage? YES
```

This matters because the scientific hypothesis is not:

```text
world and action acquire identical discrete semantics
```

but rather:

```text
heterogeneous discrete symbols are mapped into one shared sequence/hidden-state model
```

Horizontal comparison:

```text
Epona
shared historical latent F
→ separate TrajDiT / VisDiT branches

Metis
shared task graph / interaction space
→ specialized Action Expert + Video Expert

Discrete-WAM
separate modality vocabularies
→ common decoder-only Transformer and token-edit machinery
```

Discrete-WAM therefore exhibits **stronger parameter/sequence sharing than Epona or Metis**, but not a literally shared world/action vocabulary.

---

# 4. Shared Transformer architecture

The common model is a decoder-only Transformer of roughly 1B parameters. The appendix reports a configuration around:

```text
hidden size ≈ 2048
18 Transformer layers
16 attention heads
8 KV heads
Qwen3-style MRoPE / positional treatment
```

Inputs include projected visual tokens, action tokens, context/navigation/ego information, task/special tokens and decision tokens depending on the task.

The key architectural hypothesis is:

```text
heterogeneous world/action/decision symbols
→ common hidden state space
→ one shared generative/editing backbone
```

The model is not best described as two independent heads joined only at the output. Yet task-dependent attention masks and token types still impose different information-flow rules.

Therefore:

```text
shared parameters
!= identical causal visibility
```

---

# 5. Three distinct generative tasks

The pretraining formulation is easiest to understand as three related conditional distributions.

## 5.1 World modeling

Conceptually:

```text
current context C_t
+ clean future ego actions A_future
→ predict future visual/world tokens V_future
```

or:

```text
p(V_future | C_t, A_future)
```

Thus the visual world model is **action-conditioned**.

But the action condition during this training task comes from the factual/teacher-forced future action sequence. This is not evidence that many alternative actions have matched future-world targets.

## 5.2 Policy modeling

The planning branch predicts:

```text
current context
→ high-level decision D_t
→ dense future action tokens A_future
```

Action tokens are edited/refined in parallel rather than decoded strictly one token at a time.

## 5.3 World-policy modeling

The joint task interleaves future action and world tokens over physical time, conceptually:

```text
[A_{t+1}, V_{t+1}, A_{t+2}, V_{t+2}, ..., A_{t+H}, V_{t+H}]
```

with a factorization approximately:

```text
p(A_h | C, previous world/action tokens)
×
p(V_h | C, previous world/action tokens, A_h)
```

This gives the model both:

```text
same-step action → world coupling
and
previous world → later action context
```

inside the **joint world-policy generation task**.

This is substantially deeper sequence-level coupling than Metis's asymmetric expert architecture.

However, do not jump from this training/generative capability to the claim that NAVSIM planning always executes the interleaved world-policy rollout online. It does not.

---

# 6. Token editing is not ordinary autoregressive generation

Discrete-WAM uses discrete diffusion / token editing.

Core logic:

```text
clean target token sequence X
→ corrupt selected positions to valid vocabulary tokens
→ obtain X_tilde
→ Transformer predicts clean token distributions
→ replace/refine tokens over several rounds
```

Important details:

```text
NO dedicated [MASK] symbol is required;
corrupted tokens are sampled from valid vocabulary;
visual corruption can affect random token subsets;
action corruption uses a causal suffix-style structure;
loss can be applied to all editable positions, including already-clean tokens.
```

The latter provides an identity/stopping signal: the model should learn when a token is already plausible and should remain stable.

## Planning-time editing schedules

The paper evaluates schedules such as:

```text
full_replace
replace_confidence
replace_js_entropy
replace_js_freeze
```

More editing rounds do **not** monotonically improve planning. Repeatedly overwriting every action token can degrade a reasonable trajectory, while selective schedules can preserve stable tokens and spend extra compute on unresolved ones.

Ontology interpretation:

```text
J08 = GENERATIVE / TOKEN-REFINEMENT ITERATION
F08 = INTERNAL EDITING / SOLVER COORDINATE, NOT PHYSICAL WORLD TIME
```

One extra token-edit round does not mean one extra future second.

---

# 7. Training schedule and gradient topology

The paper uses a staged training schedule.

## Stage 1 — vision-oriented world/world-policy pretraining

Future actions are teacher-forced conditions and the training emphasizes visual/world prediction.

This stage primarily teaches:

```text
action-conditioned future visual/world structure
```

## Stage 2 — joint world + action training

The model activates both world/policy objectives and allows shared-Transformer parameters to be shaped by visual and action losses.

This is the stage that most directly supports the `unified world-policy training` claim.

## Stage 3 — downstream policy adaptation

LoRA-based supervised policy finetuning and later RL/post-training adapt planning behavior while attempting to preserve pretrained world-policy knowledge.

Canonical gradient statement:

```text
visual losses + action losses
→ shared Transformer parameters during joint training
```

but exact per-layer detach/task-sampling details remain source-unverified because official implementation source was not identified.

---

# 8. Objective: what is actually supervised?

The paper combines multiple objectives, conceptually:

```text
L
= lambda_v    L_visual_cls
+ lambda_a    L_action_cls
+ lambda_acc  L_acc
+ lambda_traj L_traj
+ lambda_pos  L_position_cls
+ lambda_s    L_special_cls
+ lambda_dec  L_decision
```

Scientific interpretation:

```text
visual token likelihood
+ action token likelihood
+ continuous acceleration/trajectory geometry
+ high-level decision behavior
```

all contribute to the shared model.

This is useful, but it creates an attribution problem:

```text
final planning gain
!= automatically joint world-modeling gain
```

because decision modeling, action discretization, token editing, LoRA adaptation and RL/post-training all contribute independently.

---

# 9. Decision-token supervision exposes a subtle semantic tension

The appendix's theoretical discussion motivates high-level latent/decision variables as an upstream behavioral skeleton rather than a downstream quality label.

But the implemented decision label is selected by evaluating candidate decisions with an EPDMS-style planning score:

```text
d* = argmax_d R_EPDMS(d)
```

and the model is trained to predict that winning decision.

Therefore the decision token is simultaneously:

```text
high-level planning skeleton
AND
supervised by downstream trajectory-quality evaluation
```

This does not invalidate the method, but it weakens a stronger causal/common-cause interpretation.

Canonical boundary:

```text
high-level latent variable learned from evaluator-selected labels
!= independently discovered causal behavioral state
```

This is also an important horizontal comparison with:

```text
World4Drive intentions
→ predefined/learned maneuver modes used for future-latent branching

Drive-JEPA decision/proposal supervision
→ simulator-derived utility labels

Discrete-WAM decision tokens
→ EPDMS-selected high-level behavioral skeleton
```

---

# 10. Downstream planning inference: the decisive lifecycle result

This is the most important correction to the phrase `unified world-policy model`.

For downstream planning, the paper explicitly decomposes policy generation into:

```text
current context
→ decision prediction
→ action-token editing/refinement
→ trajectory
```

The post-training/RL formulation optimizes:

```text
p(D | C)
p(A | D, C)
```

and samples/evaluates trajectories.

The deployed NAVSIM planning graph therefore does **not require**:

```text
future visual-token generation
future-world rollout
world-token→online scorer
```

Future visual generation remains a capability of the shared model and can be used for controlled world generation/counterfactual analysis, but it is not on the mandatory action-selection path for the reported planning result.

Canonical lifecycle:

```text
JOINT WORLD/POLICY PRETRAINING
→ shared weights/representations
→ DECISION-CONDITIONED ACTION TOKEN EDITING
→ POLICY-ONLY PLANNING EXECUTION GRAPH
```

This places Discrete-WAM surprisingly close to Metis/Drive-JEPA in **deployment lifecycle**, despite much stronger world/action sharing during training.

---

# 11. World-generation evidence

The paper separately reports future visual generation over a short horizon, including approximately:

```text
FID = 6.6
FVD = 80.0
4 s / 8-frame generation setting
```

This is genuine world-generation evidence.

However:

```text
better FID/FVD
→ better planning
```

is not directly established by a matched monotonic experiment.

Therefore:

```text
world-generation capability = DIRECTLY EVALUATED
world-fidelity→planning causality = NOT ESTABLISHED
```

---

# 12. Planning evidence and attribution

## 12.1 Headline results

Reported planning includes approximately:

```text
NAVSIM-v2: 90.4 EPDMS
NAVSIM-v1: 92.2 PDMS
```

These establish strong planning performance under NAVSIM's data-driven/non-reactive regime.

They do **not** by themselves isolate the effect of world modeling or prove reactive closed-loop world dynamics.

## 12.2 Pretraining ablation is weaker than the narrative suggests

Table 4:

```text
From scratch   89.8 EPDMS
FT             89.7
LoRA-SFT       90.0
```

The critical detail is that the `LoRA-SFT` pretraining setting is described as **vision-oriented world-policy pretraining**:

```text
future actions teacher-forced
only vision prediction losses applied
→ LoRA policy finetuning
```

This is not a clean ablation of the full Stage-2 joint world+action pretraining objective.

Therefore the strongest defensible conclusion is narrow:

```text
vision/world-oriented pretraining + LoRA adaptation
can improve 89.8 → 90.0 EPDMS in this setup
```

while:

```text
full finetuning of pretrained model = 89.7
```

is not better than from-scratch 89.8.

Thus the paper does **not cleanly isolate** the planning gain from full unified world-policy joint training.

## 12.3 Decision modeling is a larger clean contribution

Table 6:

```text
Base       84.7 EPDMS
Base-D_t   87.2
```

Decision modeling gives roughly:

```text
+2.5 EPDMS
```

which is much larger than the cleanest world-pretraining matched delta above.

Table 5 further shows:

```text
SFT       89.1
SFT-D_t   90.0
RL        90.4
```

So a substantial fraction of final performance should be attributed to:

```text
hierarchical decision prior
+
policy token editing
+
RL/post-training
```

not compressed into a monolithic `world-policy pretraining` gain.

---

# 13. Counterfactual / surprise analysis: useful but not causal validation

The paper perturbs ego action trajectories and observes how predicted future visual-token distributions change.

It defines a surprise-like signal based on divergence such as:

```text
S = KL(
    p(world | original action, current context)
    ||
    p(world | perturbed action, current context)
)
```

with complementary image-space differences.

Reported analysis finds surprise increases for more problematic/violating trajectories and correlates negatively with planning quality / PDMS-like scores.

This supports:

```text
the learned world generator is action sensitive;
world-model disagreement can provide a useful risk/quality proxy.
```

It does **not** establish:

```text
predicted alternative future = true consequence under intervention
```

because there is no matched real future for every perturbed action.

Counterfactual vector:

```text
candidate/action-specific generated output      YES
per-action observed alternative future truth    NO
reactive surrounding-agent truth                NO / NOT ESTABLISHED
external intervention-validity evidence         ABSENT
```

This keeps Discrete-WAM aligned with the counterfactual discipline already established for World4Drive, WorldDrive, WoTE and DynFlowDrive.

---

# 14. F07 / F08 temporal audit

## F07 — observability geometry

For future-world generation:

```text
CURRENT/HISTORY CONTEXT + ACTION
→ CHRONOLOGICALLY UNSEEN FUTURE VISUAL TOKENS
```

For world-policy joint generation, prior physical-time world/action pairs can condition later pairs.

This is a genuine future-directed obligation, unlike Drive-JEPA's random-mask same-window completion.

## F08 — internal coordinate vs physical time

Two clocks must remain separate:

```text
physical future index h
= t+1, t+2, ...

editing/refinement round r
= token solver iteration
```

Interleaving:

```text
A_{t+1}, V_{t+1}, A_{t+2}, V_{t+2}
```

has physical-time semantics across `h`.

Repeated token-edit rounds over the same action sequence do **not** advance physical time.

Binding control:

```text
more edit rounds
!= longer future horizon
```

---

# 15. Cross-paper mechanism comparison

## 15.1 vs Epona

```text
Epona:
shared history latent F
→ separate TrajDiT + VisDiT
→ visual branch optional for planning

Discrete-WAM:
separate visual/action vocabularies
→ shared Transformer hidden/backbone
→ task-specific token sequences/masks
→ planning path can still omit future visual generation
```

Discrete-WAM shares parameters/sequence machinery more deeply; both can deploy planning without generating future visuals.

## 15.2 vs Metis

```text
Metis:
separate world/action experts
forward action→world
backward world-loss→action
future world masked from action
planning inference action-only

Discrete-WAM:
shared decoder Transformer
world-policy sequence can expose prior world tokens to later actions
shared losses/gradients
planning inference nevertheless decision/action-only
```

Thus Discrete-WAM is more jointly parameterized, but not necessarily more world-dependent at deployed planning time.

## 15.3 vs World4Drive

```text
World4Drive:
candidate action
→ future latent
→ ScoreNet
→ future object explicitly required online

Discrete-WAM planning:
current context
→ decision
→ action editing
→ no mandatory future visual generation
```

So World4Drive is less parameter-unified but more explicitly future-dependent during online selection.

## 15.4 vs WoTE

WoTE uses an online consequence model and explicit utility heads. Discrete-WAM planning uses neither online future-world computation nor a consequence utility scorer.

## 15.5 vs DynFlowDrive

Both can deploy without a world model execution path, but knowledge survives differently:

```text
DynFlowDrive
world-derived mode/ranking supervision
→ learned score head survives

Discrete-WAM
world/policy multitask pretraining
→ shared backbone/policy weights survive
→ decision/action generator executes
```

## 15.6 vs Drive-JEPA / LAW

All three can have no future object online:

```text
LAW        future auxiliary prediction shapes planner during training
Drive-JEPA predictive pretraining transfers encoder
Discrete-WAM world/policy joint pretraining shapes shared Transformer
```

Discrete-WAM differs mainly in joint sequence/parameter sharing and discrete generative interface, not in requiring online imagination.

---

# 16. What `unified` means after audit

The word must be represented as a vector:

```text
shared visual/action codebook           NO
shared token vocabulary                 NO
sequence-compatible discrete interface  YES
shared Transformer hidden space         YES
shared decoder/backbone parameters      YES
joint multitask training                YES
joint losses/gradients                  YES
world-policy interleaved sequence        YES
training action→world forward path       YES
training prior-world→later-action path   YES in world-policy task
future-world required for NAVSIM action selection NO
both modalities mandatory online planning NO
```

Therefore the most accurate label is:

> **shared-backbone unified discrete world-policy training with policy-only downstream planning**, not a one-codebook world-action language and not an online model-based planner.

---

# 17. Ontology residue test

Two tempting additions were tested.

## Candidate residue A — codebook / vocabulary sharing topology

Discrete-WAM exposes a real distinction:

```text
shared codebook
vs
separate vocabularies projected into a common hidden space
```

Existing B03/D02/L02/L03 can describe the representation and sharing approximately, but no single canonical field asks this exact question.

However, among the current nine prior core anchors, most are continuous-latent methods for which this axis is `NOT APPLICABLE`. Back-projection therefore has insufficient comparative support to authorize a stable ontology amendment.

Decision:

```text
RESIDUE WATCHLIST
DO NOT CREATE V1.4 YET
```

Re-evaluate after another discrete-token anchor such as DrivingGPT / Unified Driving Tokens / another discrete WAM.

## Candidate residue B — world/action generation order

This is already expressible by:

```text
F04 temporal factorization
E02 action injection mechanism
J04 coupling direction
F08 physical-time vs internal-generation semantics
```

No new axis is needed.

Therefore:

```text
Ontology V1.3 remains active.
```

---

# 18. Evidence boundary

## PROVES reasonably well

```text
Discrete-WAM can share one Transformer across discrete visual and action tasks;
action-conditioned discrete future visual generation is feasible;
world/policy joint token-sequence training is feasible;
hierarchical decision-conditioned action token editing yields strong NAVSIM planning;
short-horizon future generation achieves strong reported FID/FVD;
action perturbations produce systematic world-model surprise signals.
```

## DOES NOT prove

```text
visual and action symbols share one codebook;
world/action discrete tokens have identical semantics;
future visual generation is required for the reported online planning score;
full joint world+action pretraining is cleanly isolated as the source of planning gain;
world fidelity monotonically causes planning quality;
perturbed-action generated futures are intervention-correct counterfactual truths;
NAVSIM planning score validates reactive surrounding-agent world dynamics.
```

## Strongest alternative explanation for final planning gain

```text
high-level decision prior
+ action discretization
+ parallel token editing
+ LoRA adaptation
+ RL/post-training
+ large shared Transformer capacity
+ world-oriented pretraining/representation regularization
```

The paper demonstrates a strong integrated system, but its planning ablations do not assign most of the final gain uniquely to world modeling.

---

# 19. Source-audit queue if implementation is released

```text
exact visual tokenizer / view configuration
visual/action embedding tables and vocabulary offsets
task-mixing ratios by pretraining stage
attention-mask implementation for world-policy task
loss masks for clean vs corrupted tokens
action causal-suffix corruption implementation
stage-2 gradient routing
decision-candidate generation / EPDMS target construction
LoRA trainable module set
GRPO rollout/reward implementation
planning inference: confirm no future-visual forward pass
world-policy joint-generation inference path
token-edit scheduling exact thresholds
latency token counts / batch dimensions
```

Until source is available, keep these as paper-level rather than code-verified claims.
