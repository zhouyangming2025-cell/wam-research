# PHASE_B_WAVE2_INTERFACE_CODE_AUDIT — LAW and WoTE

Last updated: 2026-09-14

Status: **SOURCE-CODE VERIFIED**

Purpose: resolve two decision-critical ambiguities from the Wave-2 paper read:

1. Does LAW's predicted future latent actually feed the deployed planner at inference, or is the world-model branch an auxiliary training objective?
2. Are WoTE's multi-candidate future/reward targets generated under reactive traffic dynamics, or under NAVSIM/PDM non-reactive logged-agent semantics?

This audit records source facts only. Scientific interpretation is separated below.

---

## 1. LAW — inference-path audit

### Repository provenance

```text
repo:    BraveGroup/LAW
commit:  b2f6a784247072923c477ab92324d3aa5a9759bf
```

Primary files:

```text
projects/mmdet3d_plugin/LAW/LAW.py
projects/mmdet3d_plugin/LAW/dense_heads/waypoint_query_decoder.py
```

### 1.1 Exact forward ordering

In `WaypointHead.forward` (`waypoint_query_decoder.py`), the data flow is:

```text
image feature
→ spatial_view_feat
→ wp_attn(...)
→ waypoint_head(...)
→ cur_waypoint
→ wm_prediction(spatial_view_feat, cur_waypoint)
→ wm_next_latent
```

The code first computes `cur_waypoint`; only **afterward** does it call:

```python
wm_next_latent = self.wm_prediction(spatial_view_feat, cur_waypoint)
```

and returns:

```python
return cur_waypoint, spatial_view_feat, wm_next_latent
```

Inside `wm_prediction`, the predicted ego waypoint is repeated over visual tokens, concatenated with `view_query_feat`, encoded by `action_aware_encoder`, and passed through `_wm_decoder` to obtain `wm_next_latent`.

### 1.2 Training use of the world-model output

In `LAW.forward_pts_train` (`LAW.py`):

```python
preds_ego_future_traj, cur_img_feat, pred_img_feat = self.pts_bbox_head(...)
```

The world-model output is used in a reconstruction/prediction loss:

```python
loss_rec = self.pts_bbox_head.loss_reconstruction(
    prev_pred_img_feat,
    cur_img_feat.detach(),
)
losses['loss_rec'] = loss_rec * self.wm_loss_weight
```

Waypoint imitation is separately supervised by `loss_3d`.

The future target is detached in the reconstruction path, so the future-frame/current-target latent acts as a target rather than receiving gradient through that target branch.

### 1.3 Test-time planner use

In `LAW.simple_test_pts`:

```python
preds_ego_future_traj, _, _ = self.pts_bbox_head(...)
```

Both latent outputs are discarded. Planning metrics are computed from `preds_ego_future_traj` only.

There is no code path in these functions where `wm_next_latent` is fed back into `cur_waypoint` selection or a candidate scorer. Moreover, `cur_waypoint` is already computed before `wm_next_latent` exists in the forward call.

### SOURCE FACT verdict

```text
LAW's future-latent prediction branch shapes shared parameters through an auxiliary training loss.
The predicted future latent is not consumed to select/refine the current deployed trajectory in the audited inference path.
```

The branch may still execute during forward, but its returned future latent is ignored by the test-time planning path.

### Scientific implication

LAW is therefore best classified as:

```text
future prediction as action-aware self-supervised / auxiliary representation shaping
```

rather than:

```text
online model-based planning by rolling out a future latent and evaluating the current action through that rollout
```

This distinction is central to later cross-paper synthesis: **a world-model loss can improve planning without the world-model prediction being an online planning interface.**

---

## 2. WoTE — supervision-reactivity audit

### Repository provenance

```text
repo:    liyingyanUCAS/WoTE
commit:  298957c128a91d41a1c6075bd0bb6e7e845e093f
```

Primary files:

```text
scripts/miscs/gen_multi_trajs_pdm_score.py
navsim/evaluate/pdm_score.py
navsim/planning/metric_caching/metric_cache.py
navsim/planning/metric_caching/caching.py
navsim/planning/metric_caching/metric_cache_processor.py
```

### 2.1 Multi-candidate target generation

`gen_multi_trajs_pdm_score.py` loads predefined trajectory anchors and, for each cached scene, calls:

```python
pdm_score_multi_trajs(
    metric_cache=metric_cache,
    model_trajectory_list=predefined_trajectories,
    future_sampling=proposal_sampling,
    simulator=simulator,
    scorer=scorer,
)
```

The simulator is `PDMSimulator`; the scorer is `PDMScorer`.

### 2.2 What changes per candidate

In `pdm_score_multi_trajs` (`navsim/evaluate/pdm_score.py`), every candidate ego trajectory is independently converted and sent to:

```python
simulated_states = simulator.simulate_proposals(trajectory_states, initial_ego_state)
```

Those **ego** simulated states are then scored against the same cached environment object:

```python
scores = scorer.score_proposals(
    simulated_states,
    metric_cache.observation,
    metric_cache.centerline,
    metric_cache.route_lane_ids,
    metric_cache.drivable_area_map,
)
```

Thus candidate ego trajectories change; `metric_cache.observation` is shared across candidates.

### 2.3 Where `metric_cache.observation` comes from

`MetricCacheProcessor.compute_metric_cache` constructs:

```python
observation = self._interpolate_gt_observation(scenario)
```

`_interpolate_gt_observation` explicitly samples:

```python
scenario.get_tracked_objects_at_iteration(iteration=iteration)
```

from the recorded scenario future, then interpolates those tracks to 10 Hz and stores them in `PDMObservation`.

No candidate ego trajectory is an argument to `_interpolate_gt_observation`; the cached surrounding-agent future is created once from ground-truth/logged scenario tracks before candidate scoring.

### SOURCE FACT verdict

For the audited WoTE PDM target-generation path:

```text
candidate-specific ego trajectory     = YES
candidate-specific simulated ego state = YES
candidate-dependent other-agent future = NO in this cached target path
other-agent future source              = interpolated logged/GT scenario tracks
```

Therefore the multi-candidate reward supervision follows **NAVSIM-style non-reactive environment semantics**: each ego candidate is evaluated against the same logged surrounding-agent future rather than causing other agents to re-plan/respond.

### 2.4 What this does and does not say about WoTE's learned world model

This audit does **not** imply that all predicted BEV futures inside WoTE are identical across candidates. The learned model is explicitly action-conditioned and can output different candidate-specific future BEV states.

What the audit establishes is narrower and more important for supervision interpretation:

```text
those alternative action branches are not supervised by a reactive ground-truth traffic response generated separately for each ego intervention in this target-generation pipeline.
```

The supervision supplies candidate-specific ego simulation/reward under fixed logged-agent dynamics. Any candidate-specific change in surrounding-agent future learned by the WM is therefore not backed by a matched reactive oracle target in this path.

### Scientific implication

WoTE is a genuine inference-time candidate-specific world-model planner, but its training/evaluation evidence should be phrased as:

```text
candidate-conditioned future modeling + candidate evaluation under NAVSIM-style non-reactive supervision
```

not as demonstrated behaviorally-correct reactive counterfactual simulation.

---

## 3. Cross-paper consequence

The two audits resolve a major taxonomy ambiguity:

```text
LAW:
trajectory → auxiliary predicted future latent during training
future latent NOT used to choose the deployed action

WoTE:
candidate trajectory → candidate-specific predicted future BEV → learned reward → selection
future IS used online
but candidate supervision uses fixed logged surrounding-agent futures
```

Hence the label `action-aware world model` is insufficient. At minimum, later analysis must separately record:

```text
1. Is action an input to future prediction?
2. Is the predicted future consumed by the planner at inference?
3. Are alternative action branches directly supervised?
4. If supervised, do surrounding agents react differently to each intervention?
```

LAW and WoTE occupy different answers on all four axes.