# P0009 DriveLaW — Dimension-first Deep Analysis V2

Last updated: 2026-09-15

Status: **COMPLETE FIRST PASS — arXiv v3 + official-source implementation audited**

Paper: **DriveLaW: Unifying Planning and Video Generation in a Latent Driving World**

Canonical research role in this repository:

```text
ONLINE GENERATIVE-BACKBONE REPRESENTATION CONDITIONING
→ VIDEO-DIT INTERNAL HIDDEN STATES DIRECTLY CONDITION ACTION-DIT
→ FULL FUTURE VIDEO ROLLOUT / RGB DECODE NOT REQUIRED FOR PLANNING
```

Do **not** summarize DriveLaW as either:

```text
"generate a future video, then plan from the generated video"
```

or:

```text
"video generation is only an auxiliary training loss"
```

The source-audited planning path is more specific: the deployed planner runs the Video DiT for the first video denoising iteration, caches hidden states from its Transformer blocks, and lets corresponding Action-DiT blocks cross-attend those cached world/generative features throughout action-flow refinement. The final RGB future is not required.

---

# 0. Source and version contract

Primary paper source:

```text
papers/raw_md/P0009_DriveLaW/P0009_DriveLaW.raw.md
arXiv:2512.23421v3
v3 date: 2026-04-17
CVPR 2026
```

Official repository:

```text
xiaomi-research/drivelaw
main commit audited:
243e0e41148bdb1ae39ce1adf17d026e7cbd4348
commit date: 2026-08-24
```

Release timeline from the official README:

```text
2025-12-30  arXiv release
2026-02-21  CVPR 2026 acceptance announced
2026-03-25  DriveLaW-Video / DriveLaW-Act code and weights released
2026-04-17  arXiv v3
```

Source hierarchy for this analysis:

```text
architecture / equations / tables     arXiv v3
training/inference control flow        official repo current main
exact paper-benchmark implementation  NOT FULLY PINNED TO A PAPER TAG/COMMIT
```

Important source-version warning:

The current repository is later than the paper submission and contains experimental / auxiliary code paths. Canonical claims below use the paper's stated method plus the official evaluation/training path (`videodrive_agent.py`, `run_training_videodrive.py`, `transformer_ltx.py`, `pipeline_ltx_condition.py`, and the released NAVSIM configs). Optional scorer code is not treated as part of the paper's main DriveLaW planner unless the canonical config enables it.

---

# 1. Executive verdict

DriveLaW should be decomposed into four scientific mechanisms:

```text
A. large-scale driving-video generative pretraining
B. online Video-DiT internal representation extraction
C. blockwise world-feature → Action-DiT conditioning
D. action-only task adaptation that can update the Video DiT
```

The deployed planning graph is:

```text
4 historical camera frames
+ text / ego-motion-derived prompt
+ future latent noise slots
        ↓
spatiotemporal VAE conditioning latents
        ↓
Video DiT — FIRST video denoising iteration only
        ↓
cache hidden state after every Video-DiT block
        ↓
Action DiT flow refinement
(each action block cross-attends the corresponding cached video hidden state)
        ↓
future ego trajectory

full video denoising rollout = NOT REQUIRED
VAE RGB future decode        = NOT REQUIRED
trajectory scorer / argmax   = NOT REQUIRED in the paper's canonical planner
```

Thus DriveLaW is not an online action-conditioned consequence evaluator like WoTE / World4Drive. The world representation is produced **before** a candidate action is known and is shared as the conditioning state for direct trajectory generation.

Canonical subtype:

```text
ONLINE GENERATIVE-LATENT DIRECT-POLICY WAM
```

More explicit mechanism label:

```text
VIDEO-GENERATOR INTERNAL REPRESENTATION
→ ONLINE BLOCKWISE WORLD→ACTION CONDITIONING
→ DIRECT DIFFUSION/FLOW TRAJECTORY POLICY
```

---

# 2. What exactly is the "world latent" used for planning?

The paper speaks broadly about `video latents` / `latent features from the Video DiT`. The source makes the interface much more precise.

## 2.1 It is not simply the VAE latent

The VAE encodes historical frames into compact spatiotemporal latent tokens. However, Action DiT does not merely consume the raw VAE encoding.

Instead:

```text
VAE latent/noise canvas
→ Video-DiT block 1 → h_video^1
→ Video-DiT block 2 → h_video^2
...
→ Video-DiT block B → h_video^B
```

and Action-DiT block `i` receives `h_video^i` as cross-attention context.

The released Video DiT uses 28 Transformer blocks. With the released default dimensions:

```text
Video inner dimension  = 32 heads × 64 = 2048
Action inner dimension = 16 heads × 32 = 512
```

The action cross-attention is therefore structurally:

```text
Q = action hidden state (512-d action space)
K,V = corresponding Video-DiT hidden tokens (2048-d source projected by cross-attention)
```

This is stronger than a single final-feature concatenation.

## 2.2 It is a denoising-state representation, not a finalized rendered future

At planning inference the latent canvas contains:

```text
observed history-conditioned latent slots
+
unobserved future/noise latent slots
```

The Video DiT performs one generative denoising pass over this canvas and exposes its internal block activations.

Therefore the planning state is best described as:

```text
an internal generative / predictive denoising representation
```

rather than:

```text
an observed historical feature only
```

or:

```text
a completed predicted future video
```

This distinction is central to DriveLaW.

---

# 3. Exact world→action information flow

The source `ActionTransformerBlock` contains:

```text
action self-attention
→ cross-attention to encoder_hidden_states
→ feed-forward
```

Within `LTXVideoTransformer3DModel.forward`, each video block is executed (or its cached state is loaded), then:

```text
final_hidden_states = hidden_states
ActionBlock_i(
    hidden_states       = action_hidden_states,
    encoder_hidden_states = final_hidden_states,
    ...
)
```

Hence the forward dependency is unambiguous:

```text
Video-DiT hidden state → Action-DiT hidden state
```

In the canonical architecture there is no symmetric action→video attention in the same inference step.

So:

```text
forward causal carrier:
WORLD / GENERATIVE HIDDEN → ACTION

not:
ACTION → WORLD → ACTION EVALUATION
```

This is one of the most important differences from candidate-conditioned WAMs.

---

# 4. Planning inference: only one Video-DiT iteration is needed

The released NAVSIM agent invokes the pipeline with:

```text
return_action = True
return_video  = False
output_type   = "latent"
```

Inside the pipeline:

```text
compute_video = (i == 0) or return_video
store_buffer  = (i == 0) and not return_video
```

Therefore when `return_video=False`:

```text
video solver iteration 1:
    run Video DiT
    cache blockwise hidden states
    optionally form one-step denoised latent state

action solver iteration 1:
    consume live video block states

action solver iterations 2...K:
    DO NOT rerun Video DiT
    reuse cached blockwise video states
```

The Action DiT continues to refine the trajectory while the world/generative representation remains fixed.

This means deployed planning cost is not:

```text
K_action × K_video full joint denoising
```

but approximately:

```text
1 × Video-DiT pass
+
K_action × Action-DiT pass using cached world features
```

The final VAE decode is skipped for planning.

Binding interpretation:

```text
DriveLaW uses the video generator online
but does not require online full video generation.
```

---

# 5. The first-denoise-step result is scientifically important

Paper Table 6 varies which Video-DiT denoising step provides the planning representation:

```text
video denoise step   PDMS
1                    89.1
5                    86.9
10                   23.2
```

The later state does not improve planning; it collapses badly at step 10.

This is strong evidence against a naive interpretation:

```text
"the more completely the model imagines the future,
 the better the planner becomes"
```

The reported result instead supports:

```text
early exposed generative hidden representations
can be more decision-useful than later denoising states
```

The paper explains this as later/pixel-oriented information becoming redundant for decision making. Regardless of the exact explanation, the matched ablation establishes that **planning value is not monotonic in generative denoising depth**.

This is a key cross-paper control for Epona / WorldDrive / future-video-based narratives.

---

# 6. Three-stage training — the actual optimization topology

DriveLaW's three stages must not be compressed into "joint video + action training".

## Stage 1 — long-horizon low-resolution video pretraining

```text
740 × 352 × 121 frames
Video DiT / video generation objective
focus: long temporal span / motion patterns
```

## Stage 2 — high-resolution shorter video training

```text
1280 × 704 × 25 frames
Video DiT / video generation objective
focus: spatial detail / visual quality
```

Stages 1–2 build the generative world prior.

## Stage 3 — trajectory task adaptation

Paper implementation details state that trajectory fine-tuning uses:

```text
past 4 camera frames
→ predict 2-Hz trajectory over next 4 s
```

The released NAVSIM config uses:

```text
train_mode: action_full
return_action: true
return_video: false
```

and `prepare_trainable_parameters()` sets:

```text
action_only : only parameters whose names contain action_
action_full : ALL diffusion-model parameters trainable
```

The released training loop then optimizes:

```text
loss = action flow-matching loss only
```

No video reconstruction / video-flow loss is added in the canonical stage-3 loop.

Therefore stage 3 is best described as:

```text
video-pretrained generative backbone
→ end-to-end task adaptation by action loss
```

not:

```text
frozen video feature extractor + planner head
```

and not:

```text
simultaneous video loss + action loss multitask optimization
```

---

# 7. Forward information flow vs backward gradient flow

DriveLaW exposes a useful asymmetry.

## Forward

```text
world/video representation → action
```

There is no main-path action-conditioned video future before the trajectory is generated.

## Backward during stage 3

Because:

```text
action_full → Video-DiT parameters trainable
Action-DiT cross-attends Video-DiT hidden states
no detach is applied to that hidden-state carrier
loss = action loss
```

we obtain:

```text
action loss
→ Action DiT
→ cross-attention dependence
→ Video-DiT hidden states
→ Video DiT parameters
```

Thus:

```text
FORWARD:   WORLD → ACTION
BACKWARD:  ACTION-LOSS → WORLD BACKBONE
```

The paper's statement that the staged training avoids `gradient interference` should therefore **not** be interpreted as "the planner does not update the video model". A more source-faithful reading is:

```text
video objectives are learned first;
then action optimization task-adapts the chained representation
without simultaneously optimizing a competing video loss in stage 3.
```

This is an important contrast with Metis:

```text
Metis:
forward  ACTION → WORLD
backward WORLD-LOSS → ACTION
inference world removed

DriveLaW:
forward  WORLD → ACTION
backward ACTION-LOSS → WORLD
inference world/generative backbone retained online
```

---

# 8. Stage-3 future-video supervision: what is and is not used

The released training loader reads both historical and logged future frames and encodes them with the VAE, but the canonical config sets:

```text
noisy_video: true
```

The training code constructs a latent/noise canvas in which historical memory slots are retained as conditioning while future slots are replaced by noise. The stage-3 loss is action-only.

Therefore the key task-adaptation signal is:

```text
history-conditioned generative representation
→ action loss
```

not a direct factual-future reconstruction target during the action stage.

The logged future-video tensors are present in the generic training pipeline, but under the audited `noisy_video: true` action configuration they do not establish a separate future-video loss for stage 3.

This matters because otherwise DriveLaW could be mistakenly grouped with LAW-style factual-future auxiliary supervision.

---

# 9. Action representation and policy generation

The action target is a continuous ego trajectory:

```text
L future points × (x, y, heading)
```

The released path normalizes each component and initializes action generation from Gaussian noise.

Action conditioning contains:

```text
noised action tokens
+ action solver timestep
+ ego velocity
+ ego acceleration
+ high-level command one-hot
+ blockwise Video-DiT hidden states
```

Action-DiT applies:

```text
self-attention across trajectory/action tokens
→ cross-attention to video-world tokens
→ feed-forward
```

and iteratively updates the action through a FlowMatch Euler scheduler.

There is no canonical proposal bank + explicit utility head + argmax selection in the main paper path.

So DriveLaW is a **direct generative policy**, not a candidate evaluator.

---

# 10. Paper/source equation audit — action-flow sign

The paper defines:

```text
a_t = (1-t) a_0 + t epsilon
```

which mathematically implies:

```text
da_t/dt = epsilon - a_0
```

But paper Eq. 9 writes the flow-matching target as:

```text
a_0 - epsilon
```

The official source trains:

```text
target_vel = noise_actions - actions
           = epsilon - a_0
```

Thus there is a paper↔source sign discrepancy.

Binding repository interpretation:

```text
paper Eq.9 sign as written     INCONSISTENT with the stated interpolation derivative
released source target         CONSISTENT with d[(1-t)a0+t epsilon]/dt
```

Do not silently rewrite the paper equation. Record the implementation as source evidence and the equation as a paper-level sign error / convention ambiguity.

---

# 11. Paper/source sampling-step discrepancy

Paper implementation details state:

```text
video generation: 30 sampling steps
action planning:    5 sampling steps
```

The released NAVSIM config also contains:

```text
num_inference_step: 5
```

and the validation routine uses 5.

However the current `VideoDriveAgent.forward_test()` calls the pipeline with:

```text
num_inference_steps = 10
```

hard-coded, despite reading a config value earlier.

Therefore:

```text
paper planning-step setting       5
released config / validation      5
current evaluation-agent code     10 hard-coded
```

The exact commit used for the paper's reported benchmark is not pinned in the repository.

Status:

```text
CURRENT-SOURCE / PAPER REPRODUCTION MISMATCH
```

Do not claim that the paper's 89.1 PDMS was necessarily produced with the current 10-step agent path.

---

# 12. Video-generation-specific mechanism: Noise Reinjection

DriveLaW-Video introduces targeted noise reinjection:

```text
current denoising latent
→ provisional clean estimate
→ VAE decode
→ pixel-space Laplacian high-frequency mask
→ downsample mask to latent resolution
→ inject noise only in high-frequency regions
→ rerun denoising update
```

Scientific role:

```text
improve video detail / structural consistency
```

It should **not** automatically be counted as the source of planning gain.

The planning evidence primarily concerns:

```text
video pretraining scale
representation source
which denoising state is tapped
```

There is no clean matched planning ablation in the audited main tables that isolates Noise Reinjection as a planning mechanism.

---

# 13. Strongest planning evidence

## 13.1 Video pretraining scale

Table 4:

```text
Video P.T. size   PDMS
0                 85.9
76k               87.0
3.8M              87.8
7.6M              89.1
```

This is strong within-framework evidence that larger driving-video pretraining improves downstream planning.

But the causal claim should be bounded:

```text
supports: more video-generative pretraining → better planning in DriveLaW

does not isolate:
video prediction fidelity itself
vs broader representation learning
vs additional driving-domain data exposure
vs scale/capacity interaction
```

## 13.2 Representation source

Table 5 under the same diffusion-planner framing:

```text
BEV feature        84.1 PDMS
VLM hidden state   86.5
Video latent       89.1
```

This supports the usefulness of the video-generator representation as the planner condition.

It does not prove that every video-generative representation is better than every BEV/VLM representation; the compared feature producers carry different priors/pretraining histories.

## 13.3 Video denoising tap point

Table 6:

```text
step 1   89.1
step 5   86.9
step 10  23.2
```

This is the most mechanistically diagnostic ablation in the paper.

It shows:

```text
generative representation quality for planning
!= later denoising / more image-like completion
```

---

# 14. Video-quality evidence must be separated from planning evidence

Video generation:

```text
FID  4.6
FVD 81.3
```

Planning:

```text
NAVSIM PDMS 89.1
```

Both are strong task-level results, but the paper does **not** provide a clean sample-wise or intervention-style relation:

```text
higher video fidelity
→ causally higher planning quality
```

The denoising-step ablation actually warns against equating these objectives: later generative states are worse for planning.

Therefore:

```text
video-generation quality and planning utility are correlated at the system level only weakly / indirectly;
planning usefulness of an internal generative state is a separate property.
```

---

# 15. Is DriveLaW an action-conditioned consequence model?

No, not in its canonical planning path.

World features are computed from:

```text
history observation
+ text/motion prompt
+ future noise canvas
```

before the final action trajectory is generated.

The action then cross-attends those features.

There is no main-path loop:

```text
candidate action_i
→ predicted world_i
→ evaluate world_i
→ choose action_i
```

Therefore the counterfactual vector is:

```text
candidate-specific world output?                 NO
per-candidate alternative-future supervision?    NO
reactive other-agent intervention truth?          NO
intervention-response validation?                 NO
```

DriveLaW is predictive/generative representation conditioning, not candidate-specific consequence reasoning.

---

# 16. Time-axis audit

DriveLaW requires at least three time concepts:

```text
1. physical scene / trajectory time tau
   past frames → future 4-s driving horizon

2. video generative solver coordinate s_video
   Video-DiT denoising iteration 1, 5, 10, ...

3. action generative solver coordinate s_action
   Action-DiT flow-matching refinement steps
```

Neither solver axis is physical future time.

Binding controls:

```text
more Video-DiT denoising steps
!= predicting farther into physical future

more Action-DiT flow steps
!= longer trajectory horizon
```

This is fully covered by Ontology F08; DriveLaW adds a useful case with **two simultaneous solver clocks**.

---

# 17. Training graph vs deployment graph

## Video pretraining

```text
driving video
→ VAE latent
→ Video DiT flow/generative training
→ generative world backbone
```

## Planning task adaptation

```text
history frames → VAE conditioning latent
future latent slots → noise
→ Video DiT hidden states
→ Action DiT
→ action flow loss

backprop:
action loss → Action DiT → Video DiT
```

## Planning deployment

```text
history frames
→ VAE + one Video-DiT pass
→ cached blockwise generative hidden states
→ multi-step Action-DiT flow solver
→ one trajectory
```

No factual future, future RGB, reward oracle or candidate scorer is available at deployment.

---

# 18. Cross-paper comparison

## DriveLaW vs Epona

```text
Epona:
history → shared latent F
F → TrajDiT
F → VisDiT
visual future need not be consumed by planner

DriveLaW:
history/noise canvas → Video DiT internal hidden states
those exact generative hidden states → Action DiT
Video DiT therefore lies on the online planning path
```

Key difference:

```text
Epona = sibling tasks around shared history representation
DriveLaW = chained generative backbone → policy representation
```

## DriveLaW vs LAW

```text
LAW:
planner action → future latent prediction
future latent is auxiliary training target
current action chosen before that future is produced

DriveLaW:
generative world hidden state → planner action
world/generative backbone is online at inference
```

Thus directionality is nearly opposite.

## DriveLaW vs WorldDrive

```text
WorldDrive:
heavy generative WM pretraining/teacher
→ inherited encoders + distilled lightweight future representation
→ online candidate reranking

DriveLaW:
full Video-DiT generative backbone retained online for one pass
→ internal hidden states directly condition direct trajectory policy
```

DriveLaW does not distill the world prior into a separate lightweight future evaluator.

## DriveLaW vs Metis

```text
Metis:
forward  action → future video
backward video loss → action expert
world/video path removed at action-only inference

DriveLaW:
forward  video/world hidden → action
backward action loss → Video DiT in action_full stage
Video DiT retained online
```

This is a near-mirror coupling pattern.

## DriveLaW vs World4Drive / WoTE

```text
World4Drive / WoTE:
candidate action → candidate-specific future → score/evaluate → choose

DriveLaW:
one common generative world representation → directly generate trajectory
```

DriveLaW is not a counterfactual evaluator.

## DriveLaW vs Discrete-WAM

The commonality is tighter world/action integration than classical auxiliary-prediction systems. The key difference is representation/interface style:

```text
Discrete-WAM: discrete tokenized joint modeling / autoregressive world-action structure
DriveLaW: continuous latent diffusion world backbone + separate Action DiT cross-attending internal video features
```

Do not collapse "unified" into a single architecture class.

---

# 19. Evaluation regime correction

Training/evaluation resources:

```text
video pretraining: nuScenes + nuPlan driving videos
video generation evaluation: nuScenes
planning adaptation/evaluation: NAVSIM / OpenScene-derived data
```

Paper language calls NAVSIM planning metrics `closed-loop`.

Project-standard classification remains:

```text
NAVSIM v1 PDMS
= non-reactive data-driven / pseudo-simulation planning evaluation
!= reactive closed-loop environment interaction
```

Therefore DriveLaW's 89.1 PDMS does not establish:

```text
reactive other-agent response modeling
intervention-valid world dynamics
long-horizon endogenous environment interaction
```

---

# 20. What DriveLaW proves reasonably well

```text
1. A video-generative backbone can provide a strong online planning representation.
2. Scaling driving-video pretraining improves downstream planning in the same framework.
3. Video-generator latents outperform the compared BEV/VLM conditions under the reported planner setup.
4. The full RGB future need not be generated for planning; internal Video-DiT states are sufficient.
5. The planning-optimal denoising state can be very early; later denoising is not automatically better.
6. A staged recipe can pretrain generation first and then task-adapt the same backbone through action loss.
```

---

# 21. What DriveLaW does NOT prove

```text
1. that high-fidelity RGB prediction itself causes the planning gain;
2. that the internal video hidden state is a calibrated future physical state;
3. that the planner evaluates action-conditioned consequences;
4. that unexecuted ego actions have valid alternative-agent futures;
5. that more complete video denoising yields better decision quality;
6. that Noise Reinjection contributes materially to planning;
7. that NAVSIM PDMS validates reactive closed-loop world dynamics;
8. that the exact current repository evaluation path reproduces the paper's 5-step action setting.
```

---

# 22. Strongest alternative explanation

A parsimonious explanation of the planning gains is:

```text
large-scale driving-video generative pretraining
→ strong spatiotemporal visual representation
+ online access to deep Video-DiT activations
+ task adaptation of that representation by action loss
→ better direct trajectory policy
```

This explanation does **not** require the planner to possess an accurate explicit counterfactual world simulator.

Thus DriveLaW is strong evidence for:

```text
world-model pretraining as a planning representation prior
```

and for:

```text
internal generative features as online policy state
```

but weaker evidence for:

```text
model-based planning through explicit consequence simulation.
```

---

# 23. Ontology residue test

Potential residue exposed by DriveLaW:

```text
Where along a generative solver should the planner tap the world representation?
```

The paper makes this scientifically meaningful through the strong `step 1 / 5 / 10` planning ablation.

However an immediate ontology amendment is **not yet authorized** because existing dimensions can encode most of it through:

```text
F08 — internal solver coordinate vs physical time
J01/J03 — world→planning interface and consumed representation
N — online computation depth
L/M — training/deployment lifecycle
```

Record as a candidate residue:

```text
GENERATIVE-STATE TAP LOCATION / SOLVER-DEPTH OF POLICY CONDITION
```

Require back-projection to Epona, WorldDrive, Metis, ReWorld / future anchors before adding a new dimension.

Ontology version therefore remains:

```text
V1.3 ACTIVE
NO V1.4 AMENDMENT FROM DRIVELAW FIRST PASS
```

---

# 24. Final normalized identity

```text
DriveLaW
=
large-scale driving-video generative pretraining
→ Video-DiT predictive/generative backbone

PLANNING TASK ADAPTATION:
historical frames + future noise canvas
→ Video-DiT blockwise hidden states
→ Action-DiT cross-attention
→ direct trajectory flow loss
→ action loss can task-adapt Video DiT

DEPLOYMENT:
historical frames
→ ONE online Video-DiT generative pass
→ cached blockwise hidden states
→ Action-DiT multi-step trajectory refinement
→ final direct trajectory

full future video rollout = NOT REQUIRED
RGB future decode        = NOT REQUIRED
candidate consequence evaluator = ABSENT
```

Primary ontology identity:

```text
A02  online predictive/generative representation provider
E01  action→world coupling absent in canonical planner
F08  video/action solver coordinates != physical time
I01  candidate-specific world branching absent
J02  partial online generative computation present; full future rollout absent
J03  internal Video-DiT hidden states directly consumed online
J04  forward world→action; backward action-loss→world during action_full fine-tuning
J05  direct generative policy, no canonical scorer
L01  staged video pretraining → action-only task adaptation
L04  action loss updates both Action DiT and Video DiT in action_full
M01  generative world backbone retained online
N01  one Video-DiT pass + K Action-DiT solver steps
O01  nuScenes generation + NAVSIM non-reactive planning evaluation
P01  no explicit risk/safety world state
```

Canonical subtype:

```text
ONLINE GENERATIVE-LATENT DIRECT-POLICY WAM
```
