# P0066 SAFE-SIM — Source / Code Audit

Last updated: 2026-09-16

Status: **SOURCE VERIFIED — OFFICIAL IMPLEMENTATION AUDITED AT MAIN HEAD**

Paper:

```text
SAFE-SIM: Safety-Critical Closed-Loop Traffic Simulation with Diffusion-Controllable Adversaries
ECCV 2024
arXiv:2401.00391
```

Official implementation:

```text
jxmmy7777/safe-sim
```

Audited ref:

```text
27c96a84e7bf5fbca4b47f6edde386811d76c6e7
```

---

# 1. Official-source attribution

The repository README explicitly states that it is the official implementation of SAFE-SIM and lists the paper authors / citation. The repository also exposes pretrained-checkpoint instructions and experiment commands.

Final source status:

```text
PAPER VERIFIED
OFFICIAL CODE VERIFIED
CODE SNAPSHOT PINNED
```

---

# 2. Closed-loop control graph — code verified

The main rollout loop is implemented in:

```text
tbsim/utils/env_utils.py::rollout_episodes
```

Per cycle:

```text
obs = env.get_observation(include_ego_obs=True)
→ policy.get_action(obs, step_index=counter)
→ env.step(action, num_steps_to_take=n_step_action)
→ obtain next observation
→ repeat until done
```

This is not trajectory replay after a single prediction.

The policy wrapper is:

```text
tbsim/policies/wrappers.py::RolloutWrapper
```

Its ordering is scientifically important:

```text
1. query ego planner
2. obtain ego_action
3. write ego_action.positions into obs["agents"]["ego_plan"]
4. query non-ego agents policy
5. return joint rollout action
```

Therefore the current ego planner output is an explicit input to the reactive-agent generation path.

Canonical feedback graph:

```text
current scene
→ ego planner π
→ ego plan
→ non-ego diffusion/guidance model g
→ joint actions
→ environment state update
→ new scene
→ π and g queried again
```

---

# 3. Feedback-channel audit

Using the project feedback coordinates:

```text
F_e = ego-state / dynamics feedback
F_s = sensor / viewpoint feedback
F_a = surrounding-agent state feedback
F_b = surrounding-agent behavioral-response feedback
```

SAFE-SIM:

```text
F_e  PRESENT
F_a  PRESENT
F_b  PRESENT
F_s  NOT A PRIMARY SENSOR-RENDERING LOOP
```

Reasoning:

- ego actions are executed into the shared simulation state;
- non-ego states are also advanced;
- each subsequent non-ego policy call observes the changed context and the latest ego plan;
- the simulator operates primarily on rasterized maps / agent histories rather than photorealistic camera feedback.

Boundary:

```text
behaviorally reactive simulator
!=
sensor-realistic closed-loop simulator
```

---

# 4. Environment-state transition — code verified

`tbsim/envs/env_trajdata.py::EnvUnifiedSimulation.step` / `_step` converts selected agent-relative trajectory points into world-frame next states and advances each `SimulationScene`.

For each agent, the implementation:

```text
current centroid + current yaw
+ selected relative position/yaw action
→ next world-frame x/y/yaw
→ scene.step(...)
```

Thus the environment itself owns physical state progression after policy outputs are chosen.

This also means:

```text
diffusion denoising coordinate
!=
physical simulator time
```

---

# 5. Ego-plan use inside adversarial guidance — code verified

Guidance implementation:

```text
tbsim/utils/guidance_utils.py
```

`CauseCollisionLossCalculator` uses:

```text
prediction_mode = "ego_plan"
```

and obtains:

```text
ego_plan = data_batch_for_guidance["ego_plan"]
```

The ego plan is transformed to world coordinates and substituted into future pairwise-distance computations between the ego and selected controllable/adversarial agent.

TTC guidance also inserts the current ego plan before pairwise TTC computation.

Therefore the adversarial trajectory is not merely conditioned on static historical ego state; its guidance objective explicitly references the ego planner's current proposed future path.

---

# 6. Guidance gradient path — code verified

`tbsim/models/diffusion.py::n_step_guided_p_sample` performs:

```text
current sampled non-ego action
→ differentiable forward dynamics
→ guidance.calculate_grad(...)
→ gradient step on sampled action
→ continue denoising
```

The guidance gradient changes the sampled reactive-agent trajectory during inference.

No audited path sends this gradient into the ego planner's parameters.

Canonical gradient boundary:

```text
planner output → guidance objective
planner parameters ← NO gradient update
reactive sampled action ← guidance gradient
```

SAFE-SIM is therefore planner-conditioned adversarial generation, not joint planner/simulator training.

---

# 7. Multi-sample generation and filtering

The paper and source describe generating multiple future trajectory samples for reactive agents and selecting a low-guidance-cost sample.

The generic `Guidance.filter(...)` path computes loss over samples and chooses the argmin trajectory.

Thus SAFE-SIM combines:

```text
diffusion sampling
+ gradient guidance
+ sample filtering / selection
```

The final simulated behavior is not simply the mean trajectory of the base diffusion model.

---

# 8. Partial diffusion — code verified

Partial diffusion support appears in:

```text
tbsim/models/diffusion.py
```

Mechanism:

```text
structured adversarial trajectory proposal
→ add diffusion noise at configured `partial_t`
→ inject proposal-derived noisy sample into denoising chain
→ guided denoising continues
```

The amount of injected noise controls the trade-off between explicit proposal control and return toward the learned trajectory distribution.

Important semantic boundary:

```text
partial diffusion step
=
internal generative/noise coordinate
!=
partial physical-time simulation rollout
```

---

# 9. Planner and reactive-policy update semantics

The paper reports both planner and reactive agents replan at 2 Hz.

The source exposes `n_step_action`, which controls how many environment actions are executed before policies are queried again.

Therefore the exact closed-loop cadence is conceptually:

```text
model query
→ execute n_step_action environment steps
→ re-observe
→ query again
```

The 2 Hz paper configuration is an experiment setting, not a universal property of the source framework.

---

# 10. What source verification strengthens

The code directly strengthens these claims:

1. SAFE-SIM is a genuine repeated closed-loop behavior simulator rather than a one-shot future predictor followed by replay.
2. The current ego planner trajectory explicitly enters non-ego adversarial/reactive generation.
3. Adversarial guidance modifies non-ego sampled actions at test time.
4. Physical simulator state is updated between policy queries.
5. Partial diffusion is a generative-control device, not a physical-time mechanism.

---

# 11. What source verification does NOT establish

The code does not establish:

1. that generated responses equal real-world responses under the same alternative ego intervention;
2. causal identification from intervention data;
3. calibrated uncertainty of agent response;
4. camera/sensor-realistic closed-loop feedback;
5. that a high induced collision rate means the tested ego planner is intrinsically worse;
6. that the simulator is unbiased for ranking different planners;
7. that adversarial guidance samples only physically/socially valid behaviors in all cases.

The paper itself reports failure cases involving unrealistic adversarial collisions with other agents and scenarios where the ego planner is not at fault.

---

# Final source-audit verdict

```text
SAFE-SIM
=
learned diffusion behavior prior
+ explicit current-ego-plan conditioning in guidance
+ repeated closed-loop scene updates
+ adversarial test-time trajectory guidance
+ optional partial diffusion for collision-type control

reactive closed-loop behavior            CODE VERIFIED
planner-conditioned adversary            CODE VERIFIED
paired intervention-response truth       ABSENT / NOT ESTABLISHED
sensor-photorealistic feedback           NOT THE CORE MECHANISM
planner-gradient-through-simulator       NOT IDENTIFIED
```
