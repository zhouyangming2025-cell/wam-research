# P0067 ProSim — Dimension-first Deep Analysis V2

Last updated: 2026-09-19

Paper: **Promptable Closed-loop Traffic Simulation**  
Venue: **CoRL 2024**  
arXiv: **2409.05863v1**  
Official project: **ariostgx.github.io/ProSim**  
Official code ref: **Ariostgx/ProSim @ 78a398c1859b10fbabcc455f1266cf0103f51605**

Canonical source note:

~~~
papers/raw_md/P0067_ProSim/P0067_ProSim.source_note.md
~~~

Canonical phase audit:

~~~
audits/literature/PHASE_C7_PROSIM_AUDIT.md
~~~

This is the only per-paper synthesis artifact for ProSim. The A–P normalization and residue test are intentionally kept here; no projection, ontology extension or comparison-matrix add-on is created.

---

# 0. Executive verdict

ProSim is best understood as a **prompt-conditioned, learned, vector-state, closed-loop multi-agent traffic behavior simulator**.

It is not primarily:

~~~
an ego-planning world model
an online candidate scorer
a sensor-rendering simulator
paired real-world counterfactual evidence
~~~

Its intended mechanism is:

~~~
initial map + agent histories
        ↓
shared scene tokens
        ↓
per-agent policy tokens from static status + optional prompts
        ↓
all controlled agents predict a 10-step state chunk in parallel
        ↓
generated controlled-agent states become new observations
        ↓
dynamic scene tokens are refreshed
        ↓
the next chunk is generated
        ↓
repeat for an 8 s rollout
~~~

The strongest supported reactivity claim is:

~~~
one generated agent changes the shared scene representation;
other generated agents can change their next chunk in response.
~~~

The strongest unsupported claim would be:

~~~
the model has learned causally correct responses to arbitrary ego interventions.
~~~

The paper trains against one logged WOMD future per scene and derives prompts from that same logged behavior. No paired real intervention-response future is supplied. ProSim therefore establishes an endogenous learned response loop, not intervention-ground-truth identification.

Canonical subtype:

> **PROMPTABLE CLOSED-LOOP TRAFFIC BEHAVIOR SIMULATOR WITH SOFT MULTIMODAL CONTROL**

---

# 1. What problem does ProSim actually solve?

## 1.1 Bottleneck and role

The target bottleneck is controllable, realistic multi-agent behavior generation over a long rollout, with interaction between generated agents. The host decision-maker is not an external AV planner in the core model: ProSim controls the agents in the simulated scene.

Its scientific role is therefore:

~~~
behavior simulator / scenario generator
+ prompt-conditioned policy-token generator
+ closed-loop interaction model
~~~

The paper’s contribution is not a new planning objective. The planner-facing use is indirect: ProSim can generate or stress-test traffic scenarios, including prompted behaviors.

## 1.2 Historical position

ProSim sits on the closed-loop traffic-simulation line (TrafficSim/BITS/TrafficBots/WOSAC-style evaluation) and adds:

~~~
agent-centric numerical prompts
route and goal controls
categorical temporal action tags
scene-level natural-language instructions
~~~

The genuinely important mechanism is the persistent policy token plus refreshed dynamic scene tokens. The prompt modalities are interfaces around that simulator, not evidence of a new planning-world ontology.

---

# 2. Source and version contract

## 2.1 Paper gate

The canonical source is arXiv:2409.05863v1, submitted 2024-09-09 and accepted to CoRL 2024. The HTML/PDF formulation defines an initial scene σ=(M,A), per-agent prompts ρ_i, optional scene text L, and a chunked autoregressive rollout.

## 2.2 Official implementation gate

The official repository is:

~~~
https://github.com/Ariostgx/ProSim
~~~

The audited shallow clone is pinned to:

~~~
78a398c1859b10fbabcc455f1266cf0103f51605
Merge pull request #7: update readme
2024-10-22
~~~

The README releases demo/inference code and data-loading assets but states that the training pipeline is still to be released. Source files named trainer/loss/model are therefore evidence of implementation structure, not proof that the public tree alone reproduces the paper’s complete training run.

## 2.3 Code paths that decide the mechanism

~~~
prosim/models/traj_sam.py
  ProSim.forward, encode_scene, encode_prompt, generate_policy,
  rollout_batch, step_env, step_agent_traj, _process_rollout
prosim/models/scene_encoder/attn_fusion.py
  _scene_fusion, update_scene_emb, _replace_old_obs,
  _update_scene_emb_attn
prosim/models/scene_encoder/obs_encoder.py
prosim/models/scene_encoder/map_encoder.py
prosim/models/decoder/sym_coord.py
prosim/models/condition_transformer/condition_encoders.py
prosim/models/policy/temporal_ar.py
prosim/models/loss/loss_func.py
prosim/dataset/format_utils.py
prosim/dataset/condition_utils.py
prosim/rollout/gpu_utils.py
prosim/rollout/callbacks.py
prosim/rollout/utils.py
prosim/rollout/distributed_utils.py
prosim/config/default.py
prosim_demo/cfg/*.yaml
~~~

---

# 3. Simulator state and representation

## 3.1 Initial scene

The paper defines σ=(M,A):

~~~
M = lane-center/edge polyline map elements
A = agent type, size, position, heading and past trajectory
~~~

The stated benchmark setting is at most 128 agents, 1.1 s of history, 8 s of future, 10 FPS and k=10 states per policy chunk. The released demo YAML matches 0.1 s motion steps, history steps=11, target steps=10 and target sample rate=10.

The current vector state is not an image or camera view. Map polylines and agent history are locally normalized, then global position/heading are retained for position-aware attention.

## 3.2 Tokenization

The encoder creates:

~~~
F_m = map/polyline tokens
F_a = agent-history tokens
F   = [F_m, F_a] shared scene tokens
~~~

The map and agent encoders are PointNet-like MLP + pooling modules. Position-aware agent-agent and scene attention add metric relational information. Each agent’s static properties and scene interactions are used to form a per-agent policy query; prompt features are added to that query to obtain a policy token π_i.

## 3.3 Dynamic update

At each chunk after t=0:

~~~
generated trajectory history
→ relative history / velocity / acceleration
→ observation encoder
→ replace or fuse agent tokens
→ optional agent-agent and map-agent attention refresh
~~~

The demo configuration uses OBS_UPDATE.FUSION=replace and ATTN_UPDATE=False. Thus the recurrent carrier is a refreshed agent-token set, while map tokens remain fixed. The source supports an optional attention refresh, but the default demo does not recompute the full scene attention after each update.

## 3.4 What is predicted

The policy predicts relative state changes for k=10 future steps. The action decoder cumulatively integrates position and heading deltas; optional velocity channels are also predicted. In the demo configuration the trajectory head is K=1, anchor mode, PRED_VEL=True, so the demo is not evidence of a broad multimodal deployment distribution even though the general code supports K modes.

---

# 4. Prompt and control semantics

The following table separates user controls from always-present agent context.

| Control | Representation | Scope | Training source | Inference role | Hard/soft |
|---|---|---|---|---|---|
| Agent status | local velocity, extent, type | per agent | logged initial state | static prompt/context for every policy token | soft learned conditioning |
| Goal point | (x,y,t) | per agent | final logged goal | condition transformer / policy token | soft; no projection or exact constraint |
| Route sketch | noisy/subsampled point set | per agent | logged future trajectory | route-following policy token | soft |
| Action tag | categorical tag + start/end time | per agent | heuristic labels from logged motion | temporally encoded policy token | soft |
| Text instruction | LLM text, may mention agents and scene properties | scene level, then per-agent LLM features | Llama3-70B paraphrases of tags/metadata | Llama3-8B LoRA produces policy-token offsets | soft |
| Binary V2V tag (code path) | two-agent categorical tag + interval | pair of agents | motion-tag data when available | optional condition transformer | soft; not the headline paper evaluation |

Training prompts are not independent interventions:

~~~
goal = extracted from logged future
route = noisy/subsampled logged future
action tags = labels of logged future
text = generated from those tags and metadata
~~~

The paper’s prompt evaluation masks or samples a subset of those controls, but the target trajectory remains the same logged scenario. Prompt adherence is therefore a conditional imitation/controllability test, not alternate-world truth.

The paper explicitly notes that arbitrary complex relational commands remain future work. A sentence can describe interactions, but the released prompt encoders do not provide a formal hard constraint or a verified pairwise intervention target.

---

# 5. Closed-loop feedback graph

## 5.1 Full model loop

~~~
scene σ=(map, initial histories)
  → Encoder once
  → Generator once: per-agent policy tokens π_i
  → Policy at chunk t: π_i + refreshed scene tokens
  → relative state chunks for all controlled agents
  → append to generated histories
  → update scene observation/tokens
  → Policy at chunk t+10
  → ...
~~~

The paper’s model factorization is independent per agent at each t, but all agents read a shared scene/agent-token context. Therefore interaction is cross-agent through the next scene update, not an autoregressive ordering of agent outputs within the same chunk.

## 5.2 Feedback coordinates

| Coordinate | Judgment | Evidence | Boundary |
|---|---|---|---|
| F_e ego-state/dynamics feedback | YES | generated states are appended and re-encoded in step_env | no external planner-specific ego channel in the core model |
| F_s sensor/viewpoint feedback | NO / not core | vector map + state histories only | no camera/LiDAR rendering or viewpoint loop |
| F_a surrounding-agent state feedback | YES | scene agent tokens are rebuilt from current generated histories | non-controlled background agents may remain in the future-observation template |
| F_b surrounding behavioral-response feedback | YES, simulator-level | changed shared tokens change other agents’ next policy outputs | no paired real intervention-response supervision |

## 5.3 Joint interaction level

ProSim has:

~~~
joint scene representation        YES
agent-agent attention              YES
independent parallel action heads YES
same-chunk autoregressive ordering NO
endogenous next-chunk response    YES
game-theoretic or causal response  NOT ESTABLISHED
~~~

If two controlled agents are generated, changing one agent’s realized chunk changes the scene tokens consumed by the other at the next chunk. That is enough for operational behavioral reactivity. It is not enough to identify whether the generated response is the real response under an intervention.

---

# 6. Training truth and gradient boundary

## 6.1 What is factual

The training target is the logged WOMD trajectory τ. In the released data formatter:

~~~
get_local_io_pairs_T_step_batch
  builds relative targets from batch.agent_fut
get_future_obs
  builds future observation templates from the same batch.agent_fut
paired_mse_k_way
  compares generated rollout to those logged targets
~~~

The paper describes imitation loss over the full rollout plus collision and off-road losses. The source implements these losses, but the public demo YAML disables USE_COLLISION_LOSS and USE_OFFROAD_LOSS. The paper’s training hyperparameters and full data pipeline are therefore not reproduced by the demo configuration.

## 6.2 Prompt truth versus intervention truth

~~~
logged factual future                    YES
prompt labels aligned to logged future   YES
synthetic/noisy prompt variants          YES
alternative-action supervision          NO
reactive intervention-response truth     NO
~~~

Do not call the model-generated response to a changed agent state “counterfactual ground truth.”

## 6.3 Closed-loop training claim versus released default

The paper says the full rollout is theoretically differentiable through time. In the source:

~~~
step_agent_traj:
  if not config.MODEL.BPTT:
      pred_trajs = pred_trajs.detach()
~~~

The default config sets MODEL.BPTT=False, and the released demo YAML does not override it. Thus:

~~~
paper-level claim: differentiable closed-loop training is designed
released default: generated-state feedback is detached across chunks
~~~

The rollout loss still supervises the reconstructed full trajectory, but the default public configuration does not prove full BPTT through the recurrent scene update. A private training configuration could differ; the repository does not establish that configuration.

## 6.4 Background-template leakage boundary

step_env takes batch.extras.fut_obs[t], a future observation template constructed from logged agent data, and overwrites the controlled policy-agent entries with generated positions, headings and history. Other valid agents in that template are not overwritten by ProSim.

Therefore:

~~~
all agents in the selected target/control set → endogenous generated feedback
non-target valid background agents          → may remain log-replayed
~~~

The project page demonstrates scenes in which all agents are controlled, and the paper’s benchmark setting is intended to control all agents. The code path nevertheless permits a mixed generated/logged scene; this must be checked for every experiment before claiming fully endogenous interaction.

---

# 7. Inference-time generation and physical time

## 7.1 GPU batch rollout

The source path in gpu_utils.parallel_rollout_batch is:

~~~
encode_scene once
→ encode_prompt once
→ generate/decode policy tokens once
→ rollout_batch
→ at each all_t_indices entry:
     step_env
     decode_output
     step_agent_traj
→ transform generated trajectories to world coordinates
~~~

With sample rate 10 and motion dt=0.1 s, one model iteration predicts and appends a 1 s physical chunk. Eight chunks cover the stated 8 s scenario.

## 7.2 Decode time is not physical time

~~~
policy chunk k=10       = 1.0 s physical horizon
all_t_indices            = chunk boundaries
diffusion denoising     = not used by ProSim’s action head
physical rollout time   = 0.1 s state steps inside each chunk
~~~

There is no diffusion-step/physical-time confusion in ProSim itself; the important distinction is chunk decoding versus state execution.

## 7.3 Prompt update boundary

Policy embeddings are generated once per rollout in the main path. Dynamic scene tokens are refreshed, but the prompt token does not get regenerated from a new user instruction each physical step. A prompt can include temporal intervals, which are embedded into the initial policy token, but this is not the same as a new hard command at every step.

---

# 8. Evaluation semantics

## 8.1 Promptable evaluation

The paper reports:

~~~
realism = ADE against the same logged rollout
controllability = relative ADE gain with prompts versus without prompts
~~~

The headline table uses 50% of possible prompts as input. This measures conditional adherence and closeness to the prompt-aligned logged trajectory. It does not measure the correctness of a new reaction to a changed ego trajectory.

## 8.2 Unconditional simulation evaluation

The paper reports competitive 2024 Waymo Sim Agents Challenge performance:

~~~
Composite 0.718
Kinematic 0.401
Interactive 0.778
Map-based 0.822
~~~

The paper notes comparatively weak kinematic diversity and high interactive score. WOSAC is a distributional/benchmark realism regime; it is not a paired intervention-response benchmark.

## 8.3 Source-level evaluation caveats

The default config selects trajdata rollout mode, but rollout_scene_loop in prosim/rollout/utils.py is currently a TODO that returns None. The GPU/distributed path is the materially usable inference path in the audited source.

Additional release caveats:

~~~
distributed_utils.py contains a stale registry name in the standalone
rollout_scene_distributed path;
the trainer path and demo notebooks are not identical;
rollout split formatting creates an empty condition object, so the
trainer-level rollout path does not automatically reproduce all text/
motion-tag prompt experiments;
~~~

These are engineering/reproducibility boundaries, not reasons to discard the scientific mechanism.

---

# 9. Immediate cross-paper comparison

| Anchor | Primary role | Feedback/reactivity | Truth boundary | Evaluation meaning |
|---|---|---|---|---|
| ProSim | promptable traffic simulator | all controlled agents influence next chunk through shared tokens | logged future + generated response; no paired intervention truth | ADE/%Gain + WOSAC; interaction is distributional |
| SAFE-SIM | planner-evaluation adversarial simulator | ego plan explicitly conditions repeated reactive-agent generation | no paired real intervention truth | planner stress, collision/TTC controllability, distributional realism |
| RiskWorld | risk/world representation for planning | no endogenous alternative-agent response in audited path | logged/factual futures and risk labels | risk-aware planning, not reactive simulator |
| SafeDrive | candidate-specific safety/consequence world | candidate branches, but audited agent futures remain shared/logged | candidate-specific safety labels; no reactive alternative-agent truth | NAVSIM/PDM safety and planner scoring |
| WoTE | online candidate future evaluator | recurrent BEV futures per candidate; audited NAVSIM targets use fixed logged other agents | candidate-conditioned consequence, no reactive agent truth | reward/planning and separate reactive benchmark evidence |
| DA-WAM | planning WAM with future/latent decision support | planner-facing future branch, not a standalone all-agent simulator | factual/logged or teacher-derived future, not paired intervention response | planning benchmarks |
| BridgeSim | cross-simulator E2E evaluation platform | configurable log-replay, IDM and adversarial traffic modes | evaluation environment can impose behavior modes; not ProSim training truth | OL→CL gap, DS/EPDMS, reactive traffic modes |
| ReactSimBench | reactive-simulation benchmark | AV control is decoupled; surrounding agents must respond to deviated AV | benchmark supplies deviated AV inputs, not real paired response | collision/TTC/map/kinematic response metrics |

The most important distinction is:

~~~
ProSim and SAFE-SIM generate endogenous responses.
ReactSimBench directly tests whether such responses survive a deviated,
independently controlled AV.
WOSAC/ADE alone cannot establish that property.
~~~

BridgeSim and ReactSimBench remain queued as deeper anchors; this comparison uses their retained raw source text only and does not promote them prematurely.

---

# 10. Full A–P normalization (force-filled)

The following is the canonical per-paper audit. “Unknown” means unresolved by the paper/release, not a license to infer.

## A. Problem and role

~~~
A01  bottleneck = realistic, controllable, interactive multi-agent simulation
A02  world role = deployed behavior simulator + prompt-conditioned policy state
A03  host planner = none in core; simulator controls traffic agents
A04  historical position = closed-loop behavior simulation + multimodal controllable generation
~~~

## B. Observation and current state

~~~
B01  vector map + agent state/history; no camera/LiDAR input in core path
B02  fixed 1.1 s history in reported setting; 11 history steps in demo
B03  map polyline tokens + agent-history tokens
B04  metric geometry, heading, motion, type, extent and interaction context
B05  current/history state is encoded; predicted chunks are fed back as new state
~~~

## C. Representation provenance

~~~
C01  scratch task model plus optional Llama3-8B text backbone
C02  LLM/LoRA and MLP adaptors inject scene-level language into policy tokens
C03  Llama backbone is LoRA-tuned; README does not release a complete training pipeline
C04  gain attribution is mixed: architecture, prompts, data and training stages are not fully isolated in public release
~~~

## D. Action, intention and candidate space

~~~
D01  per-agent prompt/status and sampled policy output; no external ego planner action
D02  relative state deltas integrated into positions/headings (optional velocity)
D03  goal/route/action/text intentions; no route planner is required
D04  general code supports K motion modes; demo uses K=1
D05  reported policy chunk = 10 states; multimodality is configuration-dependent
D06  prompt variants are noisy/subsampled or masked; no explicit candidate pruning stage
~~~

## E. Action → world coupling

~~~
E01  agent state/prompt conditions next behavior; whole-scene effect emerges through shared tokens
E02  concatenated/additive policy-token conditioning plus cross-attention to scene tokens
E03  shared model with per-agent tokens/heads, not independent per-agent models
E04  generated state branch persists through recurrent chunk updates
E05  changed states can be out-of-support; no intervention-support certificate
~~~

## F. Dynamics and future time

~~~
F01  future object = per-agent trajectory/state sequence
F02  future semantics = motion/interaction behavior under prompt
F03  MLP/attention policy decoder with autoregressive scene refresh
F04  fixed k-step chunks, autoregressive across chunk boundaries
F05  0.1 s state step, k=10, 8 s reported horizon; intermediate states execute
F06  stochastic mode sampling/top-K exists in general code; calibration not established
~~~

## G. Future supervision and truth

~~~
G01  factual target = logged WOMD future
G02  target is data, not an explicit EMA target encoder
G03  imitation target and optional collision/off-road losses; no external reactive teacher
G04  no utility/value teacher in the core ProSim objective
G05  full-trajectory imitation/Huber-style losses plus optional auxiliary losses
G06  K-mode selection uses closest goal during training; eval samples top-K goal probability
G07  released demo K=1; general loss supervises selected/best reconstructed rollout
G08  other-agent truth = generated for controlled IDs, logged template may remain for non-target IDs
~~~

## H. Multimodal branch identity

~~~
H01  branch = prompt-conditioned behavior mode, not a verified counterfactual world
H02  identity = prompt modality and temporal tag; otherwise learned policy mode
H03  training assignment = closest goal / logged target compatibility
H04  no published candidate-bank oracle ceiling for reactive behavior
~~~

## I. Counterfactuality and reactivity

~~~
I01  candidate-specific output branching = yes when K>1 or prompts differ
I02  candidate-specific consequence supervision = no real alternative; logged target shared
I03  observed/simulated alternative-action truth = no
I04  reactive other-agent response = yes operationally among generated agents
I05  external intervention-validity evidence = no; qualitative interaction + aggregate metrics only
~~~

## J. World → planning interface

~~~
J01  world information enters simulator behavior generation, not an ego planner
J02  online future computation = yes, as recurrent policy chunks
J03  online future consumption by a planner = not applicable/core absent
J04  coupling = shared-state bidirectional across chunks; no external planner arrow
J05  action selection = learned per-agent policy output
J06  consequence and decision model are fused in the policy simulator
J07  demo, GPU rollout and trainer rollout activate different paths
~~~

## K. Scorer and decision semantics

~~~
K01  no explicit candidate scorer in the core ProSim simulator
K02  goal probability/mode probability selects a policy mode, not utility
K03  policy sees current scene tokens, prompts and its policy token
K04  no explicit reward decomposition in deployed ProSim decision
K05  ranking source = goal compatibility/probability and imitation losses
~~~

## L. Training topology

~~~
L01  paper describes two-stage pretrain/fine-tune; complete public training pipeline unavailable
L02  encoder/generator/policy share scene/policy representation
L03  modules share scene features but policy is a separate decoder
L04  BPTT direction is configurable; demo default detaches generated chunks
L05  text LLM uses LoRA/adaptors; checkpoint and training ownership are partial
L06  imitation + optional collision/off-road + prompt/goal auxiliary objectives
~~~

## M. Future-knowledge lifecycle

~~~
M01  online recurrent simulator state, not training-only future shaping
M02  deployed future object = generated trajectory chunks + refreshed agent tokens
M03  no teacher-to-light-student transformation in the core release
M04  compression = pooled agent/map tokens and policy token
M05  future state is vector/trajectory-readable, not photorealistic
M06  no sibling future branch required for inference
~~~

## N. Compute and latency

~~~
N01  8 chunks × 10 states; all controlled agents batched in parallel
N02  compact vector tokens; map fixed after initial encoding
N03  no major coarse-to-fine candidate pruning in the core path
N04  parallel per-agent policy decoding and batched scene updates
N05  project page claims 8 s/64 agents/text under 50 ms on one GPU; scope is project-level
N06  compute/quality curves depend on K, prompt count and rollout path; full public reproduction absent
~~~

## O. Evaluation and attribution

~~~
O01  promptable rollout + WOSAC closed-loop benchmark; not planner closed-loop evaluation
O02  ADE, prompt gain, WOSAC realism/interaction/kinematic/map metrics
O03  training targets are logged/non-reactive; some evaluation rollouts are endogenous
O04  strongest matched control = prompted versus unprompted same initial/logged scene
O05  attribution ladder is not fully isolated in the released artifacts
O06  comparisons mix architectures, prompts, data and release configs
O07  prompt ADE does not establish intervention-response planning relevance
O08  paper and official source verified at pinned commit; full training path unresolved
O09  no reactive candidate ceiling/oracle reported
O10  proves operational learned interaction and prompt controllability; does not prove causal response correctness
~~~

## P. Safety, uncertainty, interaction and validity

~~~
P01  explicit safety state = absent; safety is implicit/auxiliary
P02  explicit decision risk/value = absent in core policy
P03  stochastic/mode sampling exists; calibrated uncertainty absent
P04  interaction = shared scene tokens + agent-agent attention + next-chunk response
P05  kinematic/map constraints via data and optional losses; no full physics simulator in core
P06  recursively consumes self-generated states; detached default and rollout horizon bound drift evidence
P07  traffic-rule/rare-event semantics come from data/prompts/benchmark, not a proven internal rule field
~~~

---

# 11. Residue test

Candidate residue:

~~~
prompt-conditioned multi-agent simulator with scene-level language
and per-agent temporal controls
~~~

Back-projection:

~~~
prompt/control provenance      D01–D03, H01–H03
feedback/reactivity            E01–E05, I01–I05, J04, P04
truth-source boundary          G01–G08, O03, O10
deployment lifecycle           M01–M06, L01–L06
evaluation semantics           O01–O10
~~~

The apparent new feature is a composition of existing control, feedback, truth and evaluation dimensions. It does not require a V1.4 ontology. Decision:

~~~
V1.3 retained
no ontology extension
no separate projection
~~~

---

# 12. What ProSim proves

The audited evidence supports:

1. A prompt-conditioned traffic simulator can keep a persistent per-agent policy token while refreshing shared dynamic scene tokens.
2. All agents can be decoded in parallel while still interacting across chunk boundaries.
3. Goal, route, action-tag and text conditions can be combined as soft learned controls.
4. Full-rollout imitation against logged trajectories can train an operational closed-loop generator.
5. Prompt ADE/%Gain and WOSAC interaction metrics show controllability and distributional interaction quality.

# 13. What ProSim does not prove

It does not establish:

1. paired factual responses to alternative ego interventions;
2. causal correctness of an unobserved surrounding-agent reaction;
3. sensor/viewpoint closed-loop realism;
4. a planner consuming ProSim’s future internally;
5. full BPTT in the released default configuration;
6. absence of logged-background leakage in every rollout mode;
7. reproducibility of the complete paper training pipeline from the public repository alone;
8. calibrated uncertainty or a safety/value objective;
9. arbitrary relational language commands as hard constraints;
10. that aggregate interactive score equals reactive validity under an independently controlled AV.

---

# Final normalized identity

~~~
ProSim
= vector map + agent-history encoder
+ per-agent policy-token generator
+ soft numerical/categorical/text prompt conditioning
+ parallel k-step action/state decoder
+ refreshed scene-agent tokens
+ repeated closed-loop rollout
+ imitation against one logged future
+ optional collision/off-road training terms

operational generated-agent response              YES
shared-token interaction                          YES
sensor/viewpoint feedback                         NO / NOT CORE
paired intervention-response truth                NO
planner-facing online world-model interface       NO
prompt controllability                            YES, ADE/%Gain based
full public training reproducibility              NOT ESTABLISHED
~~~

Best role in the WAM atlas:

> **The second Wave C.7 control showing that interactive behavior generation can be made promptable and efficient, while retaining the same logged-future truth boundary that prevents aggregate realism from being read as causal intervention validity.**
