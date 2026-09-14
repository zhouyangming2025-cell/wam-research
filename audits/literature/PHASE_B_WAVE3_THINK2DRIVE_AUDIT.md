# PHASE_B_WAVE3_THINK2DRIVE_AUDIT — World Model as an Imagination Training Environment

Last updated: 2026-09-14

Status: **ANCHOR DEEP READ COMPLETE — primary paper cross-checked against ECCV 2024 official PDF**

Primary sources:

- Local/GitHub derivative: `papers/raw_md/P0027_Think2Drive/P0027_Think2Drive.raw.md`
- Official venue paper: ECCV 2024, *Think2Drive: Efficient Reinforcement Learning by Thinking with Latent World Model for Autonomous Driving (in CARLA-v2)*

Purpose: determine exactly where the world model sits in Think2Drive, what is learned in imagination, what remains on the deployed policy path, and what the experiments do and do not establish about world-model value for autonomous-driving planning.

---

## 1. Historical role

Think2Drive represents a lineage that is fundamentally different from most recent planning-centric WAM papers.

The central use of the world model is not:

```text
candidate action
→ predicted future
→ score candidate online
```

and not:

```text
future-prediction auxiliary loss
→ better direct planner representation
```

Instead it follows the Dreamer model-based RL paradigm:

```text
real CARLA experience
→ learn latent environment dynamics + reward + termination
→ start from encoded real states
→ perform many latent imagined rollouts
→ train actor / critic inside imagination
→ deploy learned actor in CARLA closed loop
```

Thus the primary planning role of the WM is **policy learning through imagined experience**.

---

## 2. Input and action representation

Think2Drive explicitly removes perception as the target problem. The planner receives privileged simulator information including surrounding-agent/obstacle boxes, HD map and traffic-light state, converted to BEV semantic masks. Dynamic objects are represented over history; additional state includes ego speed, previous control and relative height.

The output is low-level vehicle control. The implementation discretizes the continuous control space into 30 actions.

Therefore Think2Drive should be classified as:

```text
planning/control-focused model-based RL expert
```

rather than a raw-sensor end-to-end perception-to-planning policy.

This distinction matters when comparing it with DriveLaW, LAW, Auto-JEPA, DA-WAM, etc.

---

## 3. Exact latent world model

The world model follows DreamerV3-style RSSM structure. The latent state is:

```text
s_t = (h_t, z_t)
```

where:

- `h_t` is a deterministic recurrent hidden state;
- `z_t` is a stochastic latent state.

The core transition is action conditioned:

```text
h_t = f(h_{t-1}, z_{t-1}, a_{t-1})
```

and the model contains:

```text
posterior encoder      q(z_t | h_t, x_t)
latent dynamics prior  p(z_t | h_t)
reward predictor       p(r_t | h_t, z_t)
termination predictor  p(c_t | h_t, z_t)
decoder                p(x_t | h_t, z_t)
```

The world-model loss combines:

```text
observation / reward / termination prediction
+ dynamics KL
+ representation KL
```

with stop-gradient placement following DreamerV3.

### Key distinction from Wave-2 / Wave-3 WAMs

The model is not trying to produce a decision-relevant future only at one fixed horizon. It learns a recurrent transition model that can be rolled repeatedly under policy-generated actions.

That is a stronger **dynamics-model semantics** than LAW/Auto-JEPA, whose predictive objectives need not support repeated environment simulation.

---

## 4. Planner learning happens in imagined latent rollouts

Given a real recorded state `x_t`, the world model first infers `s_t`. The actor then chooses actions and the learned transition model generates an imagined sequence:

```text
<s_hat_1:T, a_0:T, r_hat_0:T, c_hat_0:T>
```

The paper uses an imagination horizon of:

```text
T = 15
```

The actor maximizes expected discounted return predicted by the learned reward model, while a critic estimates continuation return. This is standard Dreamer-style actor-critic learning adapted to driving.

The key causal path during training is therefore:

```text
actor action
→ learned latent transition
→ learned reward / termination
→ imagined return
→ actor / critic gradient
```

This is genuine model-based policy improvement: the learned dynamics are not merely an auxiliary representation target.

---

## 5. What remains at deployment?

The paper-level formulation says the actor acts from the latent state `s_t` inferred from the current observation/history. Thus the learned world-model representation / recurrent state estimator remains part of the state path used by the actor.

However, the paper does **not** describe test-time control as performing a fresh multi-step rollout over alternative actions and optimizing among them at every control cycle.

The supported interpretation is:

```text
training:
WM recurrent dynamics + reward + termination
→ multi-step latent imagination
→ actor/critic learning

execution:
current privileged observation/history
→ inferred latent state s_t
→ actor π(a | s_t)
→ control
```

Therefore:

```text
imagined multi-step rollout = TRAINING-TIME planning/policy-learning mechanism
online candidate rollout search = NOT ESTABLISHED
```

An implementation-level audit would be needed to make a stronger statement about the exact optimized runtime graph, but no such audit is necessary for the current field-level distinction.

---

## 6. Driving-specific modifications are not incidental

The paper does not show that vanilla DreamerV3 directly solves CARLA-v2. It introduces multiple driving-specific engineering / optimization mechanisms:

```text
Brick 1: planner reset to escape local optima
Brick 2: automated dense scenario generation / CornerCaseRepo
Brick 3: termination-priority replay
Brick 4: steering smoothness cost
Brick 5: warm-up curriculum
Brick 6: increasing planner/world-model training ratio
Brick 7: asynchronous / parallel CARLA environment engineering
```

The paper's own ablation over 500K steps reports that removing any tested brick degrades performance; planner reset and warm-up have particularly large effects.

Thus Think2Drive's success cannot be attributed to the latent world model alone.

---

## 7. Strongest planning evidence

### Official CARLA Leaderboard v2 test routes

The official ECCV paper reports:

```text
PPO expert:
Driving Score 0.7
Weighted Driving Score 0.6
Route Completion 1.0%

Think2Drive:
Driving Score 56.8
Weighted Driving Score 91.7
Route Completion 98.6%
```

This is much stronger behavioral evidence than NAVSIM-style non-reactive pseudo-simulation: the learned policy is evaluated by repeatedly acting inside CARLA.

The paper also reports about three days of training on one A6000 GPU and substantial gains over the model-free expert on CornerCaseRepo.

### Why this is meaningful

Think2Drive therefore provides direct evidence that a learned latent simulator can support policy learning for difficult closed-loop driving tasks much more efficiently/effectively than the compared model-free setup.

It is one of the strongest anchors in the atlas for:

```text
WM → imagined RL training → closed-loop policy
```

rather than `WM → inference-time trajectory scorer`.

---

## 8. Evidence boundary: what is *not* cleanly isolated

### 8.1 No pure world-model-only matched ablation

The strongest baseline replaces the model-based RL setup with PPO / Roach-style model-free learning while retaining other driving techniques as much as possible. This is useful system evidence, but it simultaneously changes the RL algorithm and learning process.

There is no clean table of the form:

```text
same actor
same critic
same exact optimization
same sampled states
only remove learned dynamics imagination
```

Therefore the enormous CARLA-v2 delta should not be interpreted as a pure causal estimate of `world-model dynamics` alone.

### 8.2 World-model fidelity is mainly qualitative

The paper visualizes long latent/open-loop BEV prediction and shows plausible futures, including a failure case after termination. It does not provide a modern quantitative calibration study tying transition error to policy return.

Therefore:

```text
high policy performance
!= quantitative proof that the learned world model is uniformly accurate
```

### 8.3 Reward design is substantial

The learned reward predictor imitates a hand-shaped driving reward composed of speed, route-travel, lane-deviation and steering-smoothness terms.

Thus policy quality depends on:

```text
world dynamics
+ learned reward prediction
+ reward shaping
+ replay/scenario curriculum
+ actor/critic optimization
```

The WM is central, but not the only causal mechanism.

### 8.4 Privileged input limits E2E comparability

The expert planner operates on simulator-derived structured state rather than raw cameras/LiDAR. A TCP student trained from Think2Drive demonstrations with raw sensors performs substantially worse in the paper.

Therefore Think2Drive establishes model-based RL planning capability, not a solved raw-sensor E2E stack.

---

## 9. Evaluation regime

Think2Drive is evaluated in CARLA Leaderboard v1/v2 and CornerCaseRepo with repeated policy-environment interaction.

For the project taxonomy this is:

```text
interactive simulator closed-loop planning/control evidence
```

It is categorically stronger for policy feedback / recovery / sequential control than NAVSIM E3 non-reactive pseudo-simulation.

However, CARLA behavioral realism is still simulator realism, not real-vehicle closed-loop validation. In addition, some traffic flows are scripted/aggressive and need not represent human intervention responses.

Therefore:

```text
CARLA closed loop
!= real-world reactive social validity
```

---

## 10. Relation to the other Wave-3 anchors

Think2Drive completes a sixth distinct WM→planning interface:

```text
Epona:
shared historical latent → modular trajectory / visual generation

DrivingGPT:
interleaved world/action tokens → one causal autoregressive model

DriveLaW:
online video-WM hidden state → Action DiT

Auto-JEPA:
predicted ego-intent latent → trajectory retrieval → scorer/gate

DA-WAM:
candidate_i → future latent_i → score_i

Think2Drive:
learned latent transition/reward model → imagined RL rollouts → learned actor
```

The key axis introduced by Think2Drive is:

```text
WORLD MODEL AS DEPLOYED DECISION INPUT
vs
WORLD MODEL AS POLICY-TRAINING ENVIRONMENT
```

The latter can improve deployed behavior even when explicit multi-step future rollouts are not performed for online action selection.

---

## 11. AUTHOR CLAIM / DIRECT EVIDENCE / OUR INFERENCE

### AUTHOR CLAIM

A compact latent world model can act as a neural simulator and make model-based RL sufficiently efficient to learn a strong neural planner for CARLA-v2 corner cases.

### DIRECT EXPERIMENTAL EVIDENCE

- official CARLA-v2 closed-loop result strongly exceeds the compared PPO expert;
- 98.6% route completion on official CARLA-v2 test routes is reported;
- scenario-wise CornerCaseRepo results cover the 39 CARLA-v2 scenarios;
- removal of individual driving-specific bricks degrades learning;
- the learned WM qualitatively produces plausible BEV future rollouts.

### OUR INFERENCE

Think2Drive is strongest evidence in the current atlas for **world model as an imagination-based policy-learning substrate**, not for online model-predictive candidate evaluation. Its contribution also shows that a planning WM can matter primarily because it changes **where policy-training data/returns come from**, rather than because a future representation is explicitly exposed to a deployed trajectory head.

---

## 12. Stable verdict

```text
Think2Drive = WM-AS-IMAGINATION-ENVIRONMENT / MODEL-BASED RL
```

It proves that latent dynamics can be operationally useful for difficult autonomous-driving policy learning under interactive simulation.

It does **not** prove that:

```text
online future rollout is necessary for deployed planning;
raw-sensor end-to-end driving is solved;
world-model fidelity alone explains the gain;
CARLA success establishes real-world reactive behavioral correctness.
```

This anchor closes the main Wave-3 interface taxonomy.