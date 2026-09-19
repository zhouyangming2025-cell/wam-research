# P0067 ProSim — Verified Source Note

Last updated: 2026-09-19

Status: **paper/version gate passed; official project and code verified; source audit pinned**

Stable ID:

```text
P0067
```

## Canonical paper

```text
Promptable Closed-loop Traffic Simulation
Shuhan Tan, Boris Ivanovic, Yuxiao Chen, Boyi Li, Xinshuo Weng,
Yulong Cao, Philipp Krähenbühl, Marco Pavone
CoRL 2024
arXiv:2409.05863v1
Submitted: 2024-09-09
```

Primary paper sources:

```text
https://arxiv.org/abs/2409.05863
https://arxiv.org/html/2409.05863v1
```

## Attributable project and source

```text
Project: https://ariostgx.github.io/ProSim/
Official repository: https://github.com/Ariostgx/ProSim
Audited ref: 78a398c1859b10fbabcc455f1266cf0103f51605
Audited ref date: 2024-10-22
```

The repository identifies itself as the official CoRL 2024 implementation and links the paper, project page, demos, pretrained checkpoint and ProSim-Instruct-520k data. The README states that the initial code/data release is available, while the full training pipeline remains a future item. The repository is not vendored into `wam-research`; no dataset, checkpoint or binary demo asset is copied here.

## Source paths inspected

```text
prosim/models/traj_sam.py
  ProSim.forward / encode_scene / encode_prompt / generate_policy
  rollout_batch / step_env / step_agent_traj / _process_rollout
prosim/models/scene_encoder/attn_fusion.py
  _scene_fusion / update_scene_emb / _replace_old_obs / _update_scene_emb_attn
prosim/models/scene_encoder/obs_encoder.py
prosim/models/scene_encoder/map_encoder.py
prosim/models/decoder/sym_coord.py
prosim/models/condition_transformer/condition_encoders.py
prosim/models/policy/temporal_ar.py
prosim/models/loss/loss_func.py
  paired_mse_k_way / rollout_temp_traj_preds / compute_rollout_loss
prosim/dataset/format_utils.py
  get_center_obs / get_future_obs / get_local_io_pairs_T_step_batch
prosim/dataset/condition_utils.py
prosim/models/prompt_generator/generators.py
prosim/rollout/gpu_utils.py
prosim/rollout/callbacks.py
prosim/rollout/utils.py
prosim/rollout/distributed_utils.py
prosim/config/default.py
prosim_demo/cfg/{no_text,with_text,waymo_demo}.yaml
```

## Minimum source-level identity

```text
map + agent history
→ shared scene tokens
→ per-agent policy tokens conditioned by prompts
→ 10-step relative state prediction for all controlled agents in parallel
→ generated histories replace controlled-agent observations
→ scene tokens are refreshed
→ next 10-step prediction
```

This is a learned vector-state traffic behavior simulator with multimodal soft prompting. It is not a sensor-rendering loop, not a planner-integrated world model, and not paired real intervention-response evidence.

## Reproducibility boundary

The source tree contains model, loss, trainer and data-loader code, but the README explicitly says “Stay tuned for the training pipeline.” The release therefore supports a source-level mechanism audit and demo/inference audit, not a claim that the public repository alone reproduces the paper’s complete training pipeline.
