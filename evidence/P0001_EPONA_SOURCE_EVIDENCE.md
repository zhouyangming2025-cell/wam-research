# P0001 Epona — Source Evidence Pointers

Last updated: 2026-09-15

Official source:

```text
Kevin-thu/Epona@69b24c55f5ab8b3ffde8fa55e9f833bfe64d2c68
```

This file intentionally stores **minimal evidence pointers**, not copied source files.

## 1. Planning inference does not require visual generation

```text
File: models/model.py
Function: TrainTransformersDiT.step_eval
```

Source fact:

```text
STT/MST evaluate
→ TrajDiT.sample
→ predict_traj
→ if traj_only: predict_latents=None
```

Official caller:

```text
scripts/test/test_traj.py
model.step_eval(..., traj_only=True)
```

Scientific implication:

```text
future visual latent is not on the mandatory planning inference path.
```

## 2. Shared STT/MST feature feeds both branches

```text
File: models/model.py
Function: model_forward
```

Source fact:

```text
stt_features = self.model(...)["logits"]
TrajDiT.training_losses(... cond=stt_features ...)
FluxDiT.training_losses(... cond=stt_features ...)
```

Scientific implication:

```text
trajectory and visual losses share an upstream spatiotemporal representation.
```

## 3. Visual training condition is factual ego motion, not TrajDiT prediction

```text
Files:
models/model.py
models/stt.py
```

Source fact:

`pose_emb` used by visual training is constructed from target/logged future pose-yaw embeddings produced by STT. `traj_predict` is not an input to visual `training_losses`.

Scientific implication:

```text
training action→world carrier = factual/logged ego motion.
```

## 4. Self-generated rollout uses predicted trajectory to condition visual generation

```text
File: models/model.py
Function: step_eval
```

Source fact:

When `self_pred_traj=True`, the first predicted trajectory pose/yaw is embedded and passed as the visual DiT conditioning vector.

Scientific implication:

```text
self-rollout action→world carrier = TrajDiT-predicted ego motion.
```

## 5. User-controlled visual generation bypasses TrajDiT

```text
File: scripts/test/test_ctrl.py
```

Source fact:

External pose/yaw sequences are passed to `generate_gt_pose_gt_yaw(...)`, which generates visual latents directly.

Scientific implication:

```text
Epona visual generation supports external trajectory control independently of planning.
```

## 6. Visual loss shapes shared STT/MST but not TrajDiT directly

```text
Files:
models/model.py
scripts/train_deepspeed.py
configs/dit_config_dcae_nuplan.py
```

Source fact:

```text
loss_all = diff_loss + yaw_pose_loss
backward(loss_all)
fix_stt=False by default
```

The visual branch depends on `stt_features` and factual `pose_emb`, not on TrajDiT outputs.

Scientific implication:

```text
L_vis → shared STT/MST = YES
L_vis → TrajDiT parameters directly = NO
future-world→trajectory forward path = NO
```

## 7. DCAE/VAE is frozen in world-model training

```text
File: models/modules/tokenizer.py
```

Source fact:

The tokenizer sets the VAE to eval mode and wraps encode/decode in no-grad.

Scientific implication:

```text
visual codec is a frozen representation substrate for this training path.
```

## 8. Long rollout recurs in latent space

```text
File: scripts/test/test_free.py
```

Source fact:

Each generated visual latent is appended directly to the latent-history window; predicted ego motion is appended to pose/yaw history. RGB decoding is used for saving/visualization, not recurrence.

Scientific implication:

```text
outer recurrent carrier = generated visual latent + predicted ego motion.
```

## 9. Training mixes factual and self-generated context

```text
File: scripts/train_deepspeed.py
Config: configs/dit_config_dcae_nuplan.py
```

Source fact:

Default config uses `forward_iter=3`, `multifw_perstep=10`. On multi-forward iterations, detached predicted latents and predicted trajectories become conditioning for later internal passes.

Scientific implication:

```text
training != pure teacher forcing;
periodic chain-of-forward/self-generated conditioning is implemented.
```

## 10. Time-axis control

```text
Config: num_sampling_steps=100
File: scripts/test/test_free.py
```

Scientific implication:

```text
outer rollout step = predicted physical/video time advancement
inner diffusion/flow step = solver coordinate
```

Do not equate the two.
