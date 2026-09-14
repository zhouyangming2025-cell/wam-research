# PHASE_C5_WORLD4DRIVE_AUDIT

Last updated: 2026-09-14

Status: **COMPLETE — primary-paper deep read + released-code interface audit**

Paper: `World4Drive: End-to-End Autonomous Driving via Intention-aware Physical Latent World Model`

Identity:

```text
ICCV 2025 / arXiv:2507.00603
Authors: Yupeng Zheng et al.
Institutions: CASIA, Li Auto, PCL, NUS, Tsinghua
Official repo: ucaszyp/World4Drive
Audited repo commit: cffb51adeb1f7d02b49c4b74d7262ded62a33ac8
```

Role in Phase C.5: **core WAM + one-stage/end-to-end planning anchor**.

---

## 1. Executive verdict

World4Drive is a genuine **online intention-conditioned latent-world candidate selector**.

Its deployed logic is:

```text
current multi-view image/history
→ physical world latent L_t
+ trajectory-vocabulary intention queries
→ K multimodal ego trajectories T^k
→ encode each trajectory as action token A^k
→ predict K intention-conditioned future world latents L_{t+n}^k
→ ScoreNet scores the K predicted future latents
→ select trajectory corresponding to highest future-latent score
```

Unlike LAW, its predicted future latent is not only an auxiliary training target: **future-latent scores directly determine the selected trajectory at inference**.

Unlike WorldDrive, it does not use a heavy generative WM only as a teacher and then distill the future representation away. The latent future predictor/selector itself remains in the deployed planner.

However, the selector's supervision is still factual/offline:

```text
K predicted intention-conditioned future latents
vs
one actually observed future latent
```

During training, the predicted mode whose latent is closest to the single factual future becomes the target class. Thus:

```text
intention-specific future output = YES
intention-specific real alternative-action future ground truth = NO
```

This is a clean new example of the project's existing principle:

```text
candidate-specific output != candidate-specific observed counterfactual supervision
```

---

## 2. Driving World Encoding

World4Drive deliberately avoids perception-label supervision and instead constructs a latent physical-world representation from vision-foundation priors.

### 2.1 Intention encoder

The system builds a trajectory vocabulary from logged ego trajectories. The paper groups trajectories by high-level command and clusters trajectory endpoints.

Reported setup:

```text
trajectory vocabulary V ∈ R^{N × S × 2}
N = 8192
K = 6 intentions per driving command
commands = left / right / straight
```

The intent query is combined with the ego planning query through self-attention to form intention-aware planning query `Q_plan`.

This is not merely a route-command embedding: the intentions encode multiple plausible motion modes under the same high-level command.

### 2.2 Physical world latent encoder

Image features are enriched using two kinds of pretrained vision priors:

```text
spatial prior  ← metric-depth foundation model
semantic prior ← vision-language model
```

The current frame's features are augmented with positional/depth information, semantic supervision/features, and then temporally aggregated against the previous timestamp:

```text
L_t = CrossAttention(F_hat_t, F_hat_{t-1})
```

Thus `L_t` is intended to retain:

```text
visual appearance
+ spatial/depth structure
+ semantic prior
+ short temporal context
```

without manual 3D box/map supervision.

Important attribution boundary: improvements from this encoder are not automatically evidence for world dynamics. Metric-depth/VLM priors can improve the current scene representation even before any future prediction is used.

---

## 3. Exact action→future→selection path

### Step 1 — generate K ego trajectories

Given `Q_plan` and current latent `L_t`:

```text
T = MLP(CrossAttention(Q_plan, L_t))
```

with:

```text
T = {T^1,...,T^K} ∈ R^{K × S × 2}
```

Thus trajectory candidates are produced **before** candidate-specific future latents are predicted.

### Step 2 — convert trajectories into action tokens

Each trajectory is encoded by an MLP:

```text
A = E_action(T)
A ∈ R^{K × D}
```

### Step 3 — predict one future world latent per intention/action

The model uses learned future queries and cross-attention:

```text
L_{t+n} = CrossAttention(Q_future, Concat(A, L_t))
```

producing:

```text
{L_{t+n}^1,...,L_{t+n}^K}
```

Default paper setting:

```text
n = 3 timestamps
```

This is a direct online action-conditioned future-latent path.

### Step 4 — World Model Selector

A classification network/ScoreNet reads each predicted future latent:

```text
S = Softmax(C(L_{t+n}))
```

During inference, the trajectory whose future latent has the highest ScoreNet score is selected.

Therefore the deployed planner really contains:

```text
candidate trajectory
→ predicted future world latent
→ learned score
→ final trajectory
```

This places World4Drive firmly in the candidate-consequence-evaluation family, although the “consequence” is a compact latent rather than a decoded RGB/BEV future.

---

## 4. Supervision: the most important evidence boundary

World4Drive extracts an actual future latent `Lhat_{t+n}` from the one future that occurred in the logged episode.

For the K candidate/intention futures, it computes latent distance:

```text
d_k = || L_{t+n}^k - Lhat_{t+n} ||²
```

and chooses:

```text
j = argmin_k d_k
```

The selected mode `j` is used in three ways:

```text
1. L_recon = latent reconstruction/alignment for selected mode
2. j becomes the target class for ScoreNet (focal loss)
3. trajectory T^j is supervised against the expert ego trajectory with L1
```

Total loss:

```text
L = α L_sem + β L_recon + γ L_score + η L_traj
α=.2, β=.2, γ=.5, η=1.0
```

### What this means scientifically

The K alternatives are **not** supervised with K real alternative futures.

The learning signal is closer to:

```text
Among the K model-predicted future latents,
which one best explains the one factual future that actually happened?
```

This supports modal/intention discovery and future-aware selection around the expert/log distribution.

It does not establish:

```text
if ego had executed each T^k,
then L_{t+n}^k is the real surrounding-world consequence of that intervention.
```

So World4Drive is action-conditioned and candidate-specific, but not counterfactually identified from logged data.

---

## 5. CODE VERIFIED implementation facts

Official released code audited at:

```text
ucaszyp/World4Drive@cffb51adeb1f7d02b49c4b74d7262ded62a33ac8
```

Primary implementation files include:

```text
projects/mmdet3d_plugin/W4D/W4D.py
projects/mmdet3d_plugin/W4D/dense_heads/waypoint_query_decoder_simple.py
```

### Candidate/modal count

`SimpleWayDecoderHead` config shows:

```text
num_mode = 6
num_proposals = 6
hidden_channel = 256
use_wm = True
```

and loads a K-means planning-mode reference (`kmeans_plan_6.npy`).

### Future-world branch

The head defines:

```text
_wm_query_embedding
_wm_decoder
wm_cls_head
```

and produces candidate-specific predicted image/world features. The code stacks per-mode predictions and obtains:

```text
pred_img_feat    # multiple mode-specific predicted future features
pred_img_cls_feat = mean(pred_img_feat, ...)
pred_img_cls = wm_cls_head(pred_img_cls_feat)
```

This is consistent with the paper's “one latent future per intention + ScoreNet” path.

### Reconstruction / selector supervision

The code contains:

```text
loss_plan_rec = MSELoss()
loss_wm_cls   = FocalLoss(...)
```

and the training path explicitly passes `best_wm_idx` together with GT ego future trajectory to the trajectory loss. The implementation therefore matches the paper's latent-nearest-mode → selector-class target logic.

### Released-code boundary

The public repository clearly contains a W4D implementation derived from the nuScenes/MMDetection3D stack. The paper also reports NAVSIM results, but a separate clearly identifiable NAVSIM implementation path was not established in this source audit. Therefore architecture semantics are source-verified for the released W4D implementation, while NAVSIM branch implementation equivalence should not be assumed beyond the paper-level description.

---

## 6. Strongest matched ablation: world model vs intention vs physical priors

The paper's Table 3 is unusually informative because it separates several ingredients.

```text
ID  depth  semantic  WM  intentions   L2    collision
1                       ✓             0.61   0.30
2                       ✓      ✓      0.55   0.25
3    ✓                  ✓      ✓      0.51   0.29
4    ✓       ✓          ✓             0.49   0.26
5    ✓       ✓                 ✓      0.61   0.36
6    ✓       ✓          ✓      ✓      0.50   0.16
```

Several different conclusions follow.

### A. intentions improve a WM baseline

```text
row1 → row2:
0.61/0.30 → 0.55/0.25
```

So multimodal intention structure helps relative to the single-modal WM baseline.

### B. physical priors matter independently

Depth/semantic priors change the representation substantially; the final performance should not be attributed only to future modeling.

### C. the cleanest evidence for “WM evaluates intentions” is row5 vs row6

With depth+semantic+intentions held present:

```text
without WM: 0.61 / 0.36
with WM:    0.50 / 0.16
```

This is the strongest matched evidence that the world-model branch adds planning value beyond merely generating multiple intention-conditioned trajectories.

It attacks the simple explanation:

```text
“World4Drive only wins because it has multimodal trajectory proposals.”
```

However the WM branch includes both future-latent prediction and ScoreNet training, so it does not isolate pure dynamics prediction from learned future-mode classification.

### D. richer physical priors do not monotonically improve every metric

For example depth improves L2 but collision can move differently across rows. This reinforces that representation detail and planning safety remain partially decoupled.

---

## 7. Main results and protocol meaning

### nuScenes open-loop

World4Drive reports:

```text
1s/2s/3s L2: 0.23 / 0.47 / 0.81
avg L2:       0.50

1s/2s/3s collision: 0.02 / 0.12 / 0.33
avg collision:       0.16
```

The strongest relevant comparison is perception-free LAW:

```text
LAW perception-free: avg L2 0.61 / collision 0.30
World4Drive:          avg L2 0.50 / collision 0.16
```

But LAW uses a different image backbone according to the table note; do not read the entire delta as a clean method-only effect.

### NAVSIM

Paper reports:

```text
World4Drive       85.1 PDMS, camera only
LAW reimplemented 83.8 PDMS, camera only
DiffusionDrive    88.1 PDMS, camera+LiDAR in the shown table
```

The paper calls PDMS “closed-loop PDM score,” but project-wide semantics remain binding:

```text
NAVSIM = non-reactive data-driven pseudo-simulation / fixed-log environment semantics,
not reactive policy-environment closed loop.
```

Thus this is strong planning benchmark evidence, not reactive behavioral validation.

---

## 8. Scale / convergence evidence

The paper reports faster convergence relative to selected annotation-free baselines and argues spatial/semantic priors reduce the burden on latent world learning.

Scalability table:

```text
ResNet34, D=256   0.52 / 0.25
ResNet50, D=128   0.55 / 0.27
ResNet50, D=256   0.50 / 0.16
ResNet50, D=384   0.49 / 0.10
ResNet101,D=256   0.47 / 0.14
```

This is relevant to attribution: better backbone/capacity can materially change performance, so cross-paper SOTA comparisons must not be interpreted as pure world-model effects.

---

## 9. Strongest evidence for World4Drive

The strongest evidence is not the SOTA table. It is the component ablation, particularly:

```text
physical priors + intentions, no WM  0.61 / 0.36
physical priors + intentions + WM    0.50 / 0.16
```

This supports:

```text
future-latent world modeling + world-model selector
adds planning value beyond multimodal intentions alone
```

inside the authors' matched setup.

A second useful result is:

```text
single-modal WM → intention-aware WM
0.61/0.30 → 0.55/0.25
```

showing that action/intention diversity matters to the usefulness of the latent world model.

---

## 10. Strongest limitations / competing explanations

### L1 — one factual future supervises K candidate futures

This is the central structural limitation. The model predicts K intention-conditioned futures but only observes one real future. Nearest-latent modal assignment is a self-supervised proxy, not alternative-action ground truth.

### L2 — “physical understanding” is partly imported from foundation models

Metric-depth and VLM priors materially contribute. Therefore improved performance cannot be attributed solely to latent dynamics learned from driving video.

### L3 — selector combines prediction and classification

The world-model contribution consists of:

```text
future latent predictor
+
nearest-factual-future modal assignment
+
ScoreNet focal classification
```

The matched ablation establishes value of the whole WM selector mechanism, not a pure causal effect of future prediction accuracy.

### L4 — candidate set is small and intention-clustered

`K=6` candidate intentions are defined by a trajectory vocabulary/clustering scheme. Candidate coverage is therefore another independent bottleneck/control.

### L5 — NAVSIM is not reactive validation

No evidence in this paper establishes that surrounding-agent response to each ego intention is behaviorally correct under interactive ego interventions.

### L6 — released code does not fully close every paper branch

The audited public implementation establishes the core World4Drive mechanism, but a separate clear NAVSIM source path was not located. Keep paper-level NAVSIM evidence distinct from source-verified nuScenes-oriented implementation details.

---

## 11. Relation to existing core anchors

### vs LAW

```text
LAW:
trajectory prediction conditions auxiliary future latent prediction;
future latent not used for current test-time action selection.

World4Drive:
K trajectories → K future latents → ScoreNet → final trajectory;
future latent is directly on inference selection path.
```

World4Drive is therefore a real online latent consequence evaluator, not just representation shaping.

### vs WorldDrive

```text
WorldDrive:
heavy TA-DWM candidate future = training teacher;
deployment uses distilled lightweight future representation.

World4Drive:
latent world predictor + future-mode ScoreNet remain in deployed selection path.
```

This creates an important efficiency/interface contrast:

```text
DISTILLED FORESIGHT vs ONLINE LATENT FORESIGHT
```

### vs WoTE

```text
WoTE:
large candidate set → candidate-conditioned future BEV rollout → learned reward.

World4Drive:
6 intention modes → one compact latent future per mode → ScoreNet mode selection.
```

Both operationalize future-conditioned ranking, but with very different future representations and candidate-space size.

### vs DA-WAM

Both have:

```text
candidate/intention → future latent → score
```

but supervision differs in implementation details.

World4Drive assigns the one factual future to the closest of K predicted future modes and trains ScoreNet on that modal index. DA-WAM applies direct observed-future latent loss only to the expert-matched candidate and supplements all candidates with factor/ranking/hard-negative supervision.

Both independently expose the same alternative-action supervision bottleneck.

### vs Epona

Epona primarily supports shared predictive representation / joint visual+trajectory training, while its visual rollout is not needed for the deployed trajectory path. World4Drive puts future latent prediction directly upstream of final candidate selection.

---

## 12. Taxonomy placement

### World state

```text
LATENT_PREDICTIVE_STATE
+ MULTIMODAL_HYBRID physical priors
```

### Predictive mechanism

```text
Transformer/cross-attention latent future prediction
```

### WM role

```text
FUTURE_FEATURE_FOR_DIRECT_PLANNER
+
CANDIDATE_CONDITIONED_FUTURE
+
CANDIDATE_SCORER / EVALUATOR
```

### Action conditioning

```text
EGO_TRAJECTORY / INTENTION
```

### Planning interface

```text
P4: candidate future latent → learned selector
```

### Evaluation

```text
nuScenes E2 open-loop
NAVSIM E3 non-reactive planning evaluation
```

### Decision evidence

```text
D3 matched ablation strongly supports the full WM-selector contribution
```

Not D5: no reactive causal ground-truth validation.

---

## 13. Field-level correction introduced by World4Drive

World4Drive does not require a new top-level interface category beyond candidate consequence evaluation, but it sharpens an important subtype:

```text
ONLINE LATENT FORESIGHT

small multimodal intention set
→ predict compact future latent for each action/intention
→ learned future-mode classifier/selector
→ final trajectory
```

This sits between:

```text
WorldDrive  = distilled future foresight
WoTE        = richer online BEV future rollout
DA-WAM      = per-candidate future latent + factor/ranking supervision
```

It reinforces the idea that a planning-centric WAM may deliberately model **compact future decision states rather than reconstructing a full visual world**.

---

## 14. Deep-read verdict

```text
World4Drive identity                  VERIFIED
core WAM + one-stage relevance        HIGH
primary-paper mechanism               VERIFIED
released-code core path               SOURCE-AUDITED @ cffb51ad...
online future-latent selection        VERIFIED
alternative-action real future GT     NOT AVAILABLE
matched WM contribution               STRONGLY SUPPORTED within paper setup
reactive behavioral validity          NOT ESTABLISHED
anchor status                         KEEP — CORE ANCHOR
```

### One-sentence placement

> **World4Drive is an online latent-foresight WAM planner that first generates six intention-conditioned ego trajectories, predicts a compact future world latent for each trajectory, and uses a learned world-model selector—trained by matching those modes to the single factual future latent—to choose the final trajectory at inference.**

Next core anchor: **SeerDrive**.
