# Phase C.5 Epona Source Audit

Last updated: 2026-09-15

Status: **SOURCE-CODE VERIFIED — core planning/world-generation interfaces audited at locked upstream commit**

Paper: `Epona: Autoregressive Diffusion World Model for Autonomous Driving` (ICCV 2025)

Official source:

```text
repo: Kevin-thu/Epona
branch: main
audited upstream commit: 69b24c55f5ab8b3ffde8fa55e9f833bfe64d2c68
```

Local/imported snapshot record:

```text
repos/Epona/
wam-research import commit: a9926b905247505df01ddc4ce28fb71b193303d9
```

This audit is about mechanism evidence, not runtime reproduction.

---

# 1. Stable source-level verdict

Epona is source-verified as a **shared spatiotemporal-history representation feeding two separate generative branches**:

```text
historical visual latents + historical ego pose/yaw
→ SpatialTemporalTransformer (paper MST)
→ shared stt_features

stt_features → TrajDiT → future ego trajectory

stt_features + ego-motion condition → FluxDiT / visual branch → future visual latent
```

The key lifecycle distinction is now code-verified:

```text
PLANNING-ONLY:
history → STT/MST → TrajDiT → trajectory
VisDiT/FluxDiT = SKIPPED

SELF-GENERATED WORLD ROLLOUT:
history → STT/MST → TrajDiT → predicted ego motion
predicted ego motion + same STT/MST feature → VisDiT/FluxDiT → next visual latent
next visual latent + predicted ego motion → next outer rollout step
```

Therefore Epona is **not** an online `future visual → trajectory selection` planner.

---

# 2. Source/version boundary

Decision-critical source files:

```text
models/model.py
models/stt.py
models/traj_dit.py
models/flux_dit.py
models/modules/tokenizer.py
scripts/train_deepspeed.py
scripts/test/test_traj.py
scripts/test/test_free.py
scripts/test/test_ctrl.py
configs/dit_config_dcae_nuplan.py
```

All facts below are bound to upstream commit:

```text
69b24c55f5ab8b3ffde8fa55e9f833bfe64d2c68
```

---

# 3. Shared MST/STT representation

`TrainTransformersDiT` instantiates:

```text
SpatialTemporalTransformer  → self.model
FluxDiT                     → self.dit
TrajDiT                     → self.traj_dit
```

The STT input combines:

```text
visual latent patch embeddings
+ relative pose-x embeddings
+ relative pose-y embeddings
+ yaw embeddings
+ temporal embeddings
```

and applies causal temporal + spatial transformer blocks.

Its planner/world-facing output is:

```text
stt_features / auto_regressive_token_embeddings
```

This exact same `stt_features` tensor is consumed by both:

```text
TrajDiT.training_losses(... cond=stt_features ...)
FluxDiT.training_losses(... cond=stt_features ...)
```

and at evaluation by both trajectory and visual sampling branches.

Source fact:

> The paper's shared historical latent `F` is implemented as the shared STT feature tensor rather than two independently recomputed branch representations.

---

# 4. Exact planning inference graph

In `models/model.py::step_eval`:

```text
latents + pose/yaw history
→ self.model.evaluate(...)
→ stt_features
→ self.traj_dit.sample(..., stt_features, ...)
→ predict_traj
```

Only after `predict_traj` is already available does the function decide whether to enter the visual branch.

The branch gate is explicit:

```text
if traj_only:
    predict_latents = None
else:
    ... visual generation ...
```

Official `scripts/test/test_traj.py` calls:

```text
model.step_eval(..., traj_only=True)
```

and evaluates/saves the returned trajectory.

## SOURCE FACT verdict

```text
planning trajectory can be generated with VisDiT skipped entirely
future visual latent is not required by the trajectory path
trajectory exists before visual generation begins
```

Therefore:

```text
visual-future → current trajectory forward dependency = ABSENT
```

for the audited planning path.

---

# 5. Trajectory → visual conditioning is mode-dependent

A broad statement such as `TrajDiT output conditions VisDiT` is only partly correct. Source distinguishes three cases.

## 5.1 Training

During `model_forward`, STT receives factual/logged pose-yaw context and constructs `pose_emb` from the target ego motion. Visual diffusion is then trained as:

```text
GT/factual future ego pose-yaw embedding
+ stt_features
→ FluxDiT visual loss
```

The visual training branch does **not** depend on `traj_predict` produced by TrajDiT.

Thus training uses teacher-forced/factual ego-motion conditioning for the visual branch.

## 5.2 Self-generated rollout

In `step_eval(... self_pred_traj=True)`:

```text
TrajDiT → predict_traj
→ take first predicted pose/yaw step
→ self.model.get_pose_emb(...)
→ use that pose_emb as FluxDiT condition
```

Thus in autonomous generation:

```text
predicted trajectory/motion → visual future
```

is an actual forward path.

## 5.3 User-controlled rollout

`scripts/test/test_ctrl.py` bypasses TrajDiT for visual control and calls `generate_gt_pose_gt_yaw(...)` with externally specified future pose/yaw.

Thus VisDiT can also be conditioned by user-provided motion.

## Canonical action→world statement

```text
training:        factual/logged ego motion → visual world generation
self rollout:    TrajDiT-predicted ego motion → visual world generation
controlled mode: external ego motion → visual world generation
```

Do not collapse these into one action-provenance label.

---

# 6. Gradient topology

Training computes:

```text
yaw_pose_loss = TrajDiT trajectory loss
diff_loss     = FluxDiT visual/world loss
loss_all      = diff_loss + yaw_pose_loss
```

The training script backpropagates `loss_all` through the full `TrainTransformersDiT` model. Default NuPlan config uses:

```text
fix_stt = False
```

so the shared STT/MST is trainable by default.

This yields:

```text
L_traj → TrajDiT = YES
L_traj → shared STT/MST = YES

L_vis  → FluxDiT = YES
L_vis  → shared STT/MST = YES
L_vis  → TrajDiT parameters directly = NO in the audited training graph
```

The reason for the last line is structural: the visual loss consumes `stt_features` and factual pose embedding, not TrajDiT output.

Canonical distinction:

```text
world→planning gradient influence through shared STT/MST = YES
future-world→trajectory forward information flow          = NO
```

This source-verifies the project's earlier Epona interpretation.

---

# 7. Trainability / freeze topology

## VAE/DCAE tokenizer

`VAETokenizer` loads the DCAE, switches it to `.eval()`, and wraps both encode/decode in `@torch.no_grad()` / `torch.no_grad()`.

Therefore for the audited world-model training path:

```text
DCAE/VAE = frozen feature/image codec
```

## STT/MST + TrajDiT + FluxDiT

The training script builds an optimizer over the main model parameter groups. Default NuPlan config has:

```text
fix_stt=False
```

An optional `fix_stt=True` path freezes parameters whose names contain `causal_time_space_blocks`, but this is not the default config.

Default interpretation:

```text
STT/MST   trainable
TrajDiT   trainable
FluxDiT   trainable
DCAE/VAE  frozen/no-grad
```

---

# 8. Autoregressive rollout semantics

Official `scripts/test/test_free.py` implements self-generated long rollout.

At every outer generation step:

```text
current latent history + current ego-motion history
→ step_eval(self_pred_traj=True)
→ predicted trajectory + predicted next visual latent

predicted first ego-motion step
→ appended into pose/yaw conditioning history

predicted next visual latent
→ appended directly into latent history
→ oldest history latent removed
→ next step
```

Important source fact:

> The generated latent is fed directly to the next rollout step. It is decoded to RGB for visualization/saving, but it is not required to be decoded and re-encoded before model recurrence.

Therefore the rollout carrier is:

```text
GENERATED VISUAL LATENT + PREDICTED EGO MOTION
```

not RGB pixels.

## Two time axes

Default NuPlan config reports:

```text
num_sampling_steps = 100
```

This creates two distinct notions of iteration:

```text
outer rollout step
= advances predicted physical/video frame time

inner flow/diffusion sampling step
= generative solver/denoising coordinate
```

Binding control:

```text
100 denoising steps != 100 future driving timesteps
```

This is consistent with Ontology F08/J08.

---

# 9. Training rollout: not purely teacher forcing

Base single-step training uses logged/factual next latent and pose/yaw supervision.

However `scripts/train_deepspeed.py` periodically performs multi-forward training:

```text
forward_iter = 3
multifw_perstep = 10
```

On those iterations, predicted latents and predicted trajectories are detached and reused as conditioning for the next internal forward pass.

Thus Epona training includes a periodic self-generated-context / chain-of-forward component.

Canonical statement:

```text
training is neither pure teacher forcing nor pure free rollout;
it mixes factual one-step supervision with periodic detached self-generated multi-forward conditioning.
```

This is more precise than a binary teacher-forcing label.

---

# 10. Execution modes

| Mode | STT/MST | TrajDiT | FluxDiT/VisDiT | Motion source | Output |
|---|---:|---:|---:|---|---|
| planning / `test_traj.py` | YES | YES | **NO** | TrajDiT prediction | trajectory |
| self-generated long rollout / `test_free.py` | YES | YES | YES | TrajDiT prediction | trajectory + visual latent/video |
| trajectory-controlled rollout / `test_ctrl.py` | YES | NO required for control path | YES | external user pose/yaw | visual latent/video |
| training | YES | YES | YES | factual/logged pose-yaw for visual condition; factual trajectory target for TrajDiT | joint losses |

This task-mode dependence is scientifically important: Epona does not have one universal inference graph.

---

# 11. Paper ↔ code consistency

| Claim | Source verdict |
|---|---|
| shared history representation feeds trajectory and visual branches | **CONSISTENT** |
| trajectory and visual generation are separate DiT branches | **CONSISTENT** |
| predicted trajectory can condition visual generation | **CONSISTENT in self-generated rollout; not the visual-training condition** |
| visual future feeds back into same-step trajectory planning | **ABSENT in source** |
| joint visual + trajectory losses shape shared representation | **CONSISTENT** |
| pure planning can omit visual generation | **DIRECTLY SOURCE-VERIFIED** |
| autoregressive long visual rollout exists | **DIRECTLY SOURCE-VERIFIED** |
| generated rollout advances by latent recurrence | **SOURCE-VERIFIED** |
| training is purely teacher-forced | **NOT ACCURATE; periodic multi-forward self-generated conditioning exists** |

No source evidence was found that requires overturning the project's core Epona classification.

The main correction is finer action provenance:

```text
paper-level shorthand:
trajectory/action → VisDiT

source-accurate:
training VisDiT condition = factual/logged future ego motion
self-rollout VisDiT condition = TrajDiT predicted ego motion
controlled mode = externally specified ego motion
```

---

# 12. Scientific placement after source audit

Canonical Epona label remains:

```text
SHARED WORLD REPRESENTATION + DIRECT GENERATIVE POLICY
+ SIBLING ACTION-CONTROLLABLE VISUAL GENERATOR
```

Planning value is supported primarily by:

```text
joint visual/trajectory supervision
→ shared STT/MST representation shaping
→ direct TrajDiT policy
```

not by:

```text
future visual prediction
→ online future interpretation/evaluation
→ trajectory selection
```

Horizontal controls strengthened:

```text
shared representation != shared decoder
world-loss gradient influence != future-world forward consumption
trajectory→world control can be task-mode dependent
world branch optionality must be checked at execution-graph level
autoregressive physical rollout != diffusion denoising iteration
```

---

# 13. Remaining boundaries

This audit is static-source verification, not a full runtime reproduction. Remaining non-blocking questions include:

```text
exact checkpoint/config used for every headline paper table;
empirical effect of optional fix_stt variants;
runtime numerical parity with paper-reported planning/video metrics;
full checkpoint provenance for every released model.
```

These do not block classification of the core architecture/interface.

---

# 14. Final completeness verdict

```text
PAPER-COMPLETE   YES
SOURCE EXISTS    YES
SOURCE LOCKED    YES — 69b24c55f5ab8b3ffde8fa55e9f833bfe64d2c68
CORE INTERFACE   SOURCE-VERIFIED
PLANNING PATH    SOURCE-VERIFIED
WORLD PATH       SOURCE-VERIFIED
GRADIENT TOPOLOGY SOURCE-VERIFIED
ROLLOUT PATH     SOURCE-VERIFIED

FINAL: SOURCE-COMPLETE FOR CORE MECHANISM
```
