# PHASE_C5_WORLDDRIVE_AUDIT

Last updated: 2026-09-14

Status: **COMPLETE — primary-paper deep read + official-code interface audit**

Paper: `Bridging Scene Generation and Planning: Driving with World Model via Unifying Vision and Motion Representation`

Identity:

```text
arXiv:2603.14948 (2026)
Authors: Xingtai Gui, Meijie Zhang, Tianyi Yan, Wencheng Han, Jiahao Gong, Feiyang Tan, Cheng-zhong Xu, Jianbing Shen
Institutions: University of Macau + Afari Intelligent Drive
Official repo: TabGuigui/WorldDrive
Audited repo commit: c375ee1e1fe86ace175609db1ed90fd6db89673b
```

Role in Phase C.5: **mandatory core WAM + one-stage/end-to-end planning anchor**.

---

## 1. Executive verdict

WorldDrive is not best described as a planner that explicitly rolls out a full future world for every candidate at deployment.

Its actual planning mechanism is hybrid:

```text
Phase 1: trajectory-aware visual world modeling
→ learn vision representation + motion representation

Phase 2A: inherit/freeze those representations
→ multi-modal planner generates/scored trajectory candidates

Phase 2B: during FAR training only,
frozen TA-DWM generates candidate-conditioned future latents
→ lightweight Future-aware Rewarder distills those future latents

Inference:
current visual latent + candidate trajectory embedding
→ lightweight distilled future-scene representation
→ scalar future-aware reward
→ select trajectory
```

Thus the deployment path is:

```text
observation
→ transferred WM representation
→ candidate planner
→ candidate-conditioned distilled future representation
→ reward
→ selected trajectory
```

and **not**:

```text
candidate
→ full TA-DiT diffusion rollout/video
→ reward
→ select
```

The paper explicitly states that the TA-DiT future generator is used only during FAR training and explicit future-scene generation is removed at inference. Official code is consistent with this design.

Scientific placement:

```text
P1-style training/predictive representation inheritance
+
P4/P5-like candidate-conditioned future-aware scoring
+
reward/value distillation from a frozen generative WM
```

This mechanism is materially different from Epona, LAW, DriveLaW, WoTE and DA-WAM and therefore expands the core-WAM taxonomy.

---

## 2. Exact Phase-1 TA-DWM representation

### Input

Historical observation:

```text
x ∈ R^{T × 3 × H × W}
```

A pretrained/frozen CogVideoX 3D Causal VAE encodes historical/future frames. Historical latent is adapted by a lightweight learnable visual adapter:

```text
f = E_vis(x)
```

The world model also receives an ego trajectory condition.

### Trajectory vocabulary

WorldDrive builds a vocabulary:

```text
V ∈ R^{N × F × 3}
N = 256 trajectory anchors on NAVSIM
```

from driving logs via K-means.

For expert trajectory `Y`, the nearest top-K anchors are retrieved and residual offsets are encoded:

```text
c = E_a(V_K) + E_o(Y - V_K)
```

Hence the motion condition has two parts:

```text
coarse discrete motion prior = anchor identity / anchor geometry
fine motion detail           = residual to expert trajectory
```

`c` conditions TA-DiT analogously to a prompt.

### World-model target

Ground-truth future frames are encoded as latent target `z_0`; diffusion noise is applied and TA-DiT learns noise prediction conditioned on:

```text
historical visual context f
+ diffusion timestep t
+ motion embedding c
```

Loss:

```text
L_world = E || ε - ε_θ(z_t ; f,t,c) ||²
```

### Meaning

The key Phase-1 object is not simply “future video.” It is a latent space where motion-anchor representation and visual dynamics are jointly optimized under trajectory-conditioned future generation.

---

## 3. Representation inheritance into planning

The paper's central claim is not merely that TA-DWM can generate videos. The planner **inherits the visual and motion encoders learned by TA-DWM**.

Paper-level implementation:

```text
visual adapter / visual representation from TA-DWM  → frozen in planner stage
trajectory / motion encoder from TA-DWM             → frozen in planner stage
planner-specific transformer / heads                 → trained downstream
```

Official code confirms this transfer is explicit rather than rhetorical.

`worlddrive_agent.py::initialize(from_world_model=True)` remaps pretrained TA-DWM keys into planner modules, including:

```text
traj_encoder     → trajencoder / planner trajectory-related modules
adapters         → visual adapters
TA-DiT patch projection      → trajplanner.wm_proj
TA-DiT condition projection  → trajplanner.traj_wm_proj
```

`_freeze_model()` freezes the transferred adapter / trajectory encoder / WM projection pieces.

Therefore the planning backbone is intentionally initialized in the same vision-motion feature space used for trajectory-conditioned scene generation.

---

## 4. Multi-modal Planner — candidate generation and first-stage scoring

The planner treats all 256 trajectory anchors as motion queries.

Paper form:

```text
Q_a = E_a(V)
Q_p = D_plan(Q_a, [f,e], [f,e])
```

where ego-status embedding `e` contains velocity, acceleration and driving command.

The planner predicts for every anchor:

```text
1. imitation score
2. simulator-derived reward metrics
3. trajectory offset
```

The code implements `TrajWorldPlanner` with:

```text
traj_vocab_size = 256
traj_vocab_dim  = 512
traj_len        = 8
troj_dim        = 3
```

The 256 anchor embeddings cross-attend to visual tokens + ego token. Each anchor gets an offset and scores.

Supervision follows the WoTE/NAVSIM-style candidate-scoring paradigm:

```text
imitation target  = softmax(-distance(anchor, expert))
simulation target = NC / DAC / TTC / comfort / progress metrics
offset target     = positive/expert-nearest anchor residual
```

The initial planner then outputs the top-K refined trajectories for FAR.

This matters because WorldDrive's planning improvement is not attributable only to the world model. Candidate vocabulary, learned simulation-reward heads, offset regression and ranking already constitute a strong planner before FAR.

---

## 5. Future-aware Rewarder (FAR) — the key mechanism

### 5.1 Why FAR exists

TA-DWM *can* generate candidate-conditioned future latents for each candidate trajectory, but running full diffusion denoising for every candidate would be too slow.

Instead FAR distills the WM's future representations into a lightweight candidate-conditioned future-scene decoder.

### 5.2 Training-time teacher target

For candidate `k`, frozen TA-DWM supplies target future latent:

```text
z^k = frozen TA-DWM future latent conditioned on candidate k
```

The lightweight FAR predicts:

```text
z_hat^k = D_scene(Q_s, [f,c^k], [f,c^k])
```

where `Q_s` are learnable Future Scene Queries and `c^k` is the candidate trajectory embedding.

Alignment loss:

```text
L_align = E_k || z_hat^k - SG(z^k) ||²
```

This is genuinely candidate-conditioned future-representation distillation.

### 5.3 Reward learning

The distilled future feature is queried by the trajectory representation:

```text
h_f^k = D_future(c^k, z_hat^k, z_hat^k)
```

then mapped to scalar reward `r_k`.

FAR is also trained with Bradley-Terry pairwise ranking using an oracle driving score / PDMS-derived candidate ordering:

```text
L_reward = - E log σ(r_pos - r_neg)
```

Therefore FAR has **two supervision sources**:

```text
world-model latent teacher  → future representation alignment
NAVSIM/PDM oracle score     → candidate preference/ranking
```

This distinction is important: FAR is neither a pure distilled world model nor a pure reward model.

---

## 6. CODE VERIFIED: what happens at FAR inference

Official code commit:

```text
TabGuigui/WorldDrive@c375ee1e1fe86ace175609db1ed90fd6db89673b
```

### `worlddrive_refiner.py::TrajWorldRefiner.forward`

Inputs:

```text
topk_traj
topk_traj_embed
visual_token
```

The refiner creates learnable future-scene queries and predicts:

```text
future_scene_embed = refine_decoder(
    future_query,
    concat(current_visual_token, candidate_traj_token)
)
```

Then candidate trajectory token queries this distilled future representation:

```text
traj_pos_embed = traj_refine_decoder(traj_pos_token, future_scene_embed)
```

and reward heads produce scalar ranking weights, followed by `argmax` trajectory selection.

### Crucial deployment fact

At inference, `TrajWorldRefiner` predicts its own future-scene embedding directly from:

```text
current visual tokens + candidate trajectory embedding
```

There is **no call to full TA-DiT diffusion denoising inside this refiner path**.

During FAR training, `worlddrive_agent.py::forward_wm` separately invokes the frozen world model under `torch.no_grad()` to produce the teacher future latent, then computes MSE consistency with the refiner's predicted future-scene embedding.

Therefore the exact interpretation is:

```text
training:
candidate → frozen TA-DWM future latent
         ↘ lightweight FAR future latent
           align + ranking

inference:
candidate + current scene
→ lightweight FAR future latent
→ reward
→ select
```

This resolves the central ambiguity.

---

## 7. Training schedule and frozen/trainable components

### Phase 1 — TA-DWM

Train trajectory-conditioned diffusion world model on driving video data from nuPlan + nuScenes.

### Phase 2A — planner

Paper states:

```text
freeze inherited encoders
train planner 50 epochs on NAVSIM navtrain
```

### Phase 2B — FAR

Paper states:

```text
freeze trajectory planner
freeze world model / use TA-DWM as teacher
train FAR 10 epochs
PDMS used as oracle for preference supervision
```

At inference:

```text
no explicit future-scene generation
```

The public repo's stage-2 evaluation config uses the FAR/refiner agent path and the released stage-2 checkpoint.

---

## 8. Planning evidence — what is actually isolated

### 8.1 Representation inheritance ablation

NAVSIM table:

```text
no pretrain                               31.4 PDMS
CogVideoX VAE pretrain                    84.9
+ TA-DWM vision representation            85.8
+ TA-DWM motion representation            86.9
```

This is useful step-wise evidence:

```text
large generic video prior        = dominant jump
TA-DWM vision specialization     = +0.9
TA-DWM motion specialization     = +1.1
```

Important interpretation:

The total world-model story must not hide that the largest increase (`31.4 → 84.9`) comes from generic CogVideoX VAE initialization, not TA-DWM-specific future modeling.

The TA-DWM-specific incremental evidence is roughly:

```text
84.9 → 85.8 → 86.9
```

which supports planner-shared representation learning, but with a much smaller effect than the generic pretrained visual prior.

### 8.2 FAR ablation

Matched NAVSIM result:

```text
base planner / no extra rewarder future feat     86.9
+ trajectory feature rewarder only               87.0
+ trajectory + distilled future feature FAR      88.1
```

This is stronger causal evidence for the future representation than a headline SOTA table.

It implies:

```text
rewarder/scoring architecture alone ≈ +0.1
adding distilled future representation ≈ +1.1
```

within this matched setup.

Unlike some WAM papers, this ablation partially survives the alternative explanation “it is just a better scorer.”

But it does **not** isolate whether the +1.1 comes specifically from accurate environment dynamics versus a useful candidate-conditioned teacher representation + PDMS ranking supervision.

### 8.3 Candidate-count ablation

FAR top-K:

```text
K=1   86.9
K=3   87.9
K=5   88.1
K=10  87.6
```

This reinforces an existing field principle:

```text
more candidate diversity is useful only until low-quality distractors begin to hurt ranking.
```

It also means FAR performance is inseparable from candidate-set quality.

---

## 9. Main planning results and evaluation semantics

### NAVSIM navtest

Paper reports:

```text
WorldDrive single-view: 88.1 PDMS
full-navtrain setting:  89.0 PDMS
best-of-6 oracle:        93.6 PDMS
```

The best-of-6 number is explicitly an oracle upper-bound probe, not deployment performance.

### NAVSIM-v2 navhard

Paper reports:

```text
WorldDrive EPDMS 34.9
DiffusionDrive   27.5
```

The paper describes NAVSIM-v2 as reactive-traffic + pseudo-closed-loop evaluation. Keep this distinct from fully sensor-policy-agent interactive simulation such as Bench2Drive.

### nuScenes

Open-loop planning:

```text
3 s L2  = 0.68 m
avg L2  = 0.42 m
3 s CR  = 0.38%
avg CR  = 0.16%
```

This is supplementary open-loop evidence, not closed-loop behavioral validation.

---

## 10. Runtime / deployment

Paper reports on one NVIDIA A800:

```text
WorldDrive complete planning pipeline: 53 ms
PWM without future forecast:          570 ms
PWM with future forecast:             850 ms
```

The key architectural reason is that TA-DiT diffusion generation is removed from the deployed planning path and only the lightweight distilled FAR remains.

Public README currently provides updated checkpoints with approximately:

```text
stage1 planner       87.7
stage2 planner + FAR 89.2
```

These repository checkpoint numbers are post-paper release artifacts and should not silently replace the paper's table values when making scientific comparisons.

---

## 11. Scene-generation evidence

TA-DWM reports nuScenes generation quality:

```text
FID 12.8
FVD 131.7
```

The motion-sensitivity analysis shows latent similarity decreases as conditioning trajectories deviate geometrically from the expert trajectory; top-5 trajectory conditioning is more discriminative than top-1 in the reported analysis.

This supports:

```text
TA-DWM is genuinely sensitive to motion condition
```

but not by itself:

```text
generated counterfactual environment response is behaviorally correct for unexecuted ego actions.
```

The latter remains subject to the same alternative-action supervision limits identified elsewhere in the project.

---

## 12. Strongest evidence for WorldDrive

The strongest evidence is not the headline 88.1/89.0 PDMS.

It is the pair of matched decompositions:

```text
A. TA-DWM representation inheritance:
84.9 generic VAE
→ 85.8 + TA-DWM vision
→ 86.9 + TA-DWM motion

B. future-aware scoring:
86.9 base planner
→ 87.0 trajectory-only rewarder
→ 88.1 + distilled future feature
```

Together they support two different roles for world modeling:

```text
1. predictive/generative pretraining creates useful planner-shared representation;
2. candidate-conditioned future representation adds value to ranking beyond trajectory feature alone.
```

This is unusually relevant to our WAM+one-stage scope because both effects remain inside a real-time end-to-end planning stack.

---

## 13. Strongest limitations / competing explanations

### L1 — generic pretraining explains most of the representation jump

The huge `31.4 → 84.9` increase comes from CogVideoX VAE initialization. TA-DWM-specific vision/motion inheritance adds much smaller incremental gains.

Therefore it would be incorrect to narrate the full jump as “future world modeling teaches planning.”

### L2 — FAR is jointly world-distilled and reward-supervised

FAR is trained with:

```text
future-latent alignment
+
PDMS preference/ranking
```

Hence its gain cannot be attributed purely to latent world prediction. The learned reward target is tied to NAVSIM/PDM semantics.

### L3 — alternative candidate future truth is learned, not observed

TA-DWM can generate `z^k` for multiple alternative ego candidates, but ordinary logs still contain only one realized physical future. Candidate-conditioned alternative futures are model-generated extrapolations rather than real multi-intervention ground truth.

### L4 — deployment is not explicit model-predictive rollout

WorldDrive removes the expensive generative future rollout at deployment. The online future state used by FAR is a lightweight distilled prediction.

This is a strength for efficiency but means WorldDrive should not be used as evidence that explicit online visual imagination is necessary for strong planning.

### L5 — evaluation remains mostly NAVSIM-family / open-loop nuScenes

The paper is strong on NAVSIM/NAVSIM-v2 and open-loop nuScenes, but it does not establish real-vehicle or fully sensor-realistic behaviorally validated closed-loop performance.

---

## 14. Relation to existing core anchors

### vs Epona

```text
Epona:
shared historical latent → TrajDiT / VisDiT
visual future task improves planner representation
visual rollout can be disabled for planning

WorldDrive:
TA-DWM pretraining → explicitly inherited frozen vision+motion encoders
+ separate distilled candidate-future rewarder
```

WorldDrive therefore makes the representation-transfer mechanism more explicit and adds candidate selection based on future-distilled features.

### vs LAW

```text
LAW:
action-aware future-latent prediction is an auxiliary training objective;
predicted future latent is not consumed for current test-time action selection.

WorldDrive:
future generator itself is absent at deployment,
but a distilled candidate-conditioned future representation IS consumed online by FAR.
```

Thus WorldDrive sits between training-only predictive shaping and online future-state evaluation.

### vs DriveLaW

```text
DriveLaW:
online Video-DiT hidden state directly conditions Action DiT.

WorldDrive:
full world generator removed at inference;
its representation is inherited and its candidate-future latents are distilled into a lightweight scorer.
```

This is a strong efficiency/interface contrast.

### vs WoTE

Both are candidate-based and use NAVSIM-style reward supervision.

```text
WoTE:
current BEV + candidate → online predicted future BEV → learned reward

WorldDrive:
candidate → TA-DWM future latent only as training teacher
→ distilled lightweight future feature at inference
→ reward
```

WorldDrive can be interpreted as a **distilled/offloaded model-based evaluator** rather than full online world rollout.

### vs DA-WAM

```text
DA-WAM:
per-candidate future latent is produced by the deployed planner/evaluator path;
observed-future supervision is expert-matched only.

WorldDrive:
per-candidate future latent teacher is frozen generative TA-DWM during training;
deployment uses a distilled future-scene predictor + ranking loss.
```

Both expose the same broader supervision question: candidate-specific outputs exceed candidate-specific real-world observed futures.

---

## 15. Taxonomy placement after deep read

### World state

```text
VIDEO_RGB / LATENT_PREDICTIVE_STATE / MULTIMODAL_HYBRID
```

### Predictive mechanism

```text
DIFFUSION_FLOW for TA-DWM teacher
+
lightweight transformer-decoder distillation for deployed future feature
```

### WM role

```text
PRETRAINING_REPRESENTATION
+
CANDIDATE_CONDITIONED_FUTURE teacher
+
CANDIDATE_SCORER / EVALUATOR via distilled future representation
```

### Planning interface

WorldDrive does not fit one old bucket cleanly. Best description:

```text
P1 predictive shaping / representation inheritance
+
P4 candidate future → learned scorer,
but the deployed candidate future is a distilled surrogate rather than full TA-DWM rollout
```

### Decision-evidence strength

```text
D3 = matched ablations showing TA-DWM representation + future-feature contributions
```

It approaches D4 architecturally because candidate-specific future representations are used for ranking, but no real alternative-action consequence oracle exists for behavioral validation.

---

## 16. Field-level correction introduced by WorldDrive

Our previous interface taxonomy should add an explicit sub-type:

```text
DISTILLED WORLD-MODEL FORESIGHT

heavy generative WM used as training teacher
→ distill candidate-conditioned future representation
→ lightweight future-aware scorer at deployment
```

This is different from:

```text
training-only auxiliary future prediction
online WM hidden state
full per-candidate WM rollout
joint world-action generation
```

WorldDrive therefore **does change the current core-WAM map**, although it does not overturn earlier stable principles.

It reinforces:

```text
world-model benefit can enter planning without explicit deployment-time scene generation;
future value depends on planner interface, not on visual generation alone;
candidate scoring remains an independent bottleneck;
representation pretraining and online future evaluation must be decomposed.
```

---

## 17. Deep-read verdict

```text
WorldDrive identity           VERIFIED
core WAM + one-stage relevance HIGH
paper method                  PRIMARY-SOURCE VERIFIED
official code                 SOURCE-AUDITED @ c375ee1e...
FAR inference semantics       RESOLVED
TA-DWM→planner inheritance    RESOLVED
world-model planning effect   PARTIALLY ISOLATED by matched ablations
reactive/counterfactual truth NOT ESTABLISHED
anchor status                 KEEP — CORE ANCHOR
```

### One-sentence placement

> **WorldDrive is a hybrid WAM planner that first transfers trajectory-aware generative world-model representations into a multimodal planner, then distills the frozen world model's candidate-conditioned future latents into a lightweight future-aware rewarder so deployment gains future-sensitive candidate scoring without running diffusion rollouts online.**

Next core anchor: **World4Drive**.
