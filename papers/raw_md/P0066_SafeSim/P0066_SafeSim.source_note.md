# P0066 SAFE-SIM — Verified Source Note

Last updated: 2026-09-16

Status: **PAPER VERIFIED + OFFICIAL CODE VERIFIED + FULL LOCAL MINERU RAW-MD EXTRACTION INGESTED**

Stable ID:

```text
P0066
```

Canonical paper:

```text
SAFE-SIM: Safety-Critical Closed-Loop Traffic Simulation with Diffusion-Controllable Adversaries
Wei-Jer Chang, Francesco Pittaluga, Masayoshi Tomizuka, Wei Zhan, Manmohan Chandraker
ECCV 2024
arXiv:2401.00391
```

Canonical publication source:

```text
ECVA ECCV 2024 paper page / PDF
```

Official implementation:

```text
https://github.com/jxmmy7777/safe-sim
```

Audited code snapshot:

```text
main HEAD = 27c96a84e7bf5fbca4b47f6edde386811d76c6e7
commit date = 2025-05-01
```

Repository README explicitly identifies itself as the official implementation.

Primary code paths inspected:

```text
docs/code_structure.md
docs/simulation_doc.md
tbsim/utils/env_utils.py
tbsim/policies/wrappers.py
tbsim/utils/guidance_utils.py
tbsim/models/diffusion.py
tbsim/envs/env_trajdata.py
```

## Source-level mechanism facts

Paper and source agree on the following core closed-loop topology:

```text
current environment observation
→ ego planner produces ego future plan
→ ego plan is inserted into non-ego agent observation as `ego_plan`
→ reactive diffusion policy generates non-ego trajectories
→ guidance explicitly evaluates those trajectories against the ego plan
→ environment executes the first `n_step_action` steps
→ simulated agent states are updated
→ a new observation is built
→ ego and non-ego policies are queried again
→ repeat
```

The paper reports both planner and reactive agents update at 2 Hz.

The code verifies that:

```text
RolloutWrapper.get_action(...)
  first queries ego_policy
  then writes ego_action.positions into obs["agents"]["ego_plan"]
  then queries agents_policy
```

and `rollout_episodes(...)` repeatedly performs:

```text
obs = env.get_observation(...)
action = policy.get_action(obs,...)
env.step(action, num_steps_to_take=n_step_action)
```

Thus SAFE-SIM is operationally reactive in the simulator sense: changed ego plans can change non-ego generated behavior at the next replanning cycle.

## Guidance semantics verified in source

`CauseCollisionLossCalculator` defaults to:

```text
prediction_mode = "ego_plan"
```

and substitutes the current ego planner trajectory into pairwise future-distance computation. TTC guidance similarly inserts `ego_plan` into the ego future path before computing pairwise TTC costs.

Guidance gradients update sampled non-ego action trajectories during diffusion sampling. They do not update the ego planner parameters.

`n_step_guided_p_sample(...)`:

```text
sampled action
→ forward dynamics
→ guidance loss gradient
→ action-space update inside denoising
```

This is **test-time trajectory guidance**, not planner training.

## Physical-state update verified in source

`EnvUnifiedSimulation.step(...)` converts selected planned positions/yaws into new world-frame states and advances each `SimulationScene` using `scene.step(...)`.

Therefore physical simulation time and diffusion denoising time must remain distinct:

```text
K=100 diffusion denoising steps
!=
100 physical simulation timesteps
```

The simulator may execute multiple physical steps from one planned sequence according to `n_step_action`, then re-query policies.

## Partial diffusion

Paper/source mechanism:

```text
rule/domain-generated collision trajectory proposal
→ add Gaussian noise at a selected diffusion step / noise level
→ guided denoising from that partially noised proposal
→ realistic but proposal-biased adversarial trajectory
```

This controls collision type / scenario diversity and is not a physical partial rollout.

## Training / inference boundary

Behavior diffusion model:

```text
trained on real driving trajectory data
```

Safety-critical adversarial behavior:

```text
primarily created at inference by guidance + filtering + optional partial diffusion
```

The evaluated ego planner remains a separate system.

## Evidence caveat

SAFE-SIM provides:

```text
endogenous learned response to updated ego/environment state
```

but the audited paper/source does not provide paired real-world ground-truth responses to the same scene under alternative ego interventions.

Therefore:

```text
reactive closed-loop behavior model        YES
causally identified counterfactual truth   NO
```

## Raw text status

The complete local MinerU/raw-Markdown extraction is now available at:

```text
papers/raw_md/P0066_SafeSim/P0066_SafeSim.raw.md
papers/raw_md/P0066_SafeSim/images/
```

Acquisition and conversion record:

```text
source PDF: ECVA ECCV 2024 paper PDF
pages: 17
MinerU return code: 0
PDF SHA256: 7a092e02de9f03031ff51660966d0a94c66635682cda2e6970375f6c21f92b2e
```

The source PDF remains local and is not tracked in Git; the repository stores the generated Markdown and referenced images only.
