# PHASE_B_WAVE3_PLAN — Unified, Compressed, Candidate-Specific, and RL World-Action Modeling

Last updated: 2026-09-14

Status: **ACTIVE — Wave 3 authorized after Wave-2 closeout**

Wave 3 anchors:

```text
Epona
DrivingGPT
DriveLaW
Auto-JEPA
DA-WAM
Think2Drive
```

Purpose: understand how the role of the world model changes after the Wave-2 families of controllable generation, joint occupancy/ego modeling, predictive pretraining, auxiliary latent prediction, and online candidate evaluation. This wave is not a gap search. It compares **what is actually unified, what future information survives at inference, and how planning consumes world knowledge**.

## 1. Reading order

```text
1. Epona
2. DrivingGPT
3. DriveLaW
4. Auto-JEPA
5. DA-WAM
6. Think2Drive
```

The order follows a deliberate interface progression:

```text
shared history latent + separate world/action generative branches
→ interleaved world/action token sequence
→ hidden world-model feature directly conditioning action generation
→ compressed planning-oriented predictive target
→ per-candidate future latent used for scoring
→ latent world model used as an RL training simulator
```

## 2. Binding controls from Waves 1–2

For every paper, preserve these distinctions:

```text
conditional future != causal/interventional response
candidate ranking != world modeling
better reconstruction != better decision utility
longer horizon != better planning
generation quality != planning value
WM-assisted planning != online model-based planning
candidate-specific model output != candidate-specific oracle supervision
joint world-action generation != candidate consequence evaluation
```

Strong non-WM controls remain active: UniAD, DiffusionDrive, DriveSuprim. Evaluation semantics remain explicit: nuScenes open-loop, NAVSIM non-reactive pseudo-simulation, nuPlan OL/CL-NR/CL-R, Bench2Drive interactive closed loop, HUGSIM reconstructed closed loop.

## 3. Common comparison axes

Each anchor must answer the same questions before cross-paper synthesis.

### A. What is actually unified?

Distinguish:

```text
shared backbone / shared latent
shared conditioning only
joint loss
joint token sequence
joint generative process
planner consuming WM hidden state
candidate-specific predictive state
policy trained inside a learned world
```

Do not call a system “unified world-action” merely because world and action losses coexist.

### B. Exact world/future representation

Record:

```text
RGB/video latent
visual hidden state
discrete token sequence
continuous latent / JEPA target
candidate-specific latent
RSSM / Dreamer-style latent dynamics
```

Ask what information the representation is required to preserve and what it intentionally discards.

### C. Training supervision

For each future/world target, label the source:

```text
factual logged future
future visual/latent target from another encoder
ego expert trajectory
alternative-action proxy
simulator-derived target/reward
self-supervised predictive target
RL return/value
```

For alternative actions, explicitly ask whether a direct future oracle exists.

### D. Inference-time path

Write the deployed data flow exactly:

```text
observation
→ representation
→ [future/world computation?]
→ planner / action generator / scorer
→ final trajectory/action
```

Classify the WM role as one or more of:

```text
training-only representation shaping
online hidden feature provider
online future rollout
candidate evaluator
joint action-world generator
policy-training simulator
```

### E. Planning attribution

Prefer matched ablations. Decompose gains from:

```text
world prediction
representation quality
shared parameters
trajectory/action modeling
candidate coverage
scoring/reward
post-processing/refinement
extra data / pretraining
RL/post-training
```

Do not use headline SOTA as causal attribution.

### F. Multimodality / uncertainty

Record whether multiple futures/actions exist and whether the final planner actually consumes their probability/uncertainty or only chooses one branch/sample.

### G. Evaluation regime

State exactly what is demonstrated and what is not. A strong NAVSIM number is not reactive evidence; a video rollout is not closed-loop planning evidence; CARLA/Bench2Drive closed loop is not real-vehicle validation.

## 4. Paper-specific questions

### 4.1 Epona

Primary comparison role: shared latent history with trajectory and visual diffusion branches.

Questions:

- What exactly does MST encode from history and ego motion?
- Are TrajDiT and VisDiT merely conditioned on a common latent, or do their generated outputs feed each other at inference?
- When trajectory conditions visual generation, does generated visual future feed back to trajectory choice?
- Which losses couple the two tasks versus simply train them jointly?
- What part of any planning gain can be attributed to world modeling rather than shared representation / multi-task learning?
- What evaluation demonstrates planning value beyond video generation quality?

### 4.2 DrivingGPT

Primary comparison role: interleaved autoregressive world-action token modeling.

Questions:

- What are the exact image/world tokens and action tokens?
- In what order are they generated, and what causal dependencies does the sequence impose?
- Does planning require generating future visual/world tokens first, or can actions be decoded directly from shared sequence state?
- Is world-action “unification” token-level, objective-level, and inference-level simultaneously?
- What matched evidence shows joint token modeling helps planning rather than language-model-style sequence capacity or extra data?

### 4.3 DriveLaW

Primary comparison role: hidden video/world-model features directly consumed by an Action DiT.

Questions:

- Which Video-DiT hidden state is exposed to the action branch, at which denoising step and layer?
- Is a fully generated future ever required for planning?
- Why does the paper’s denoising-step ablation degrade sharply for later/noisier generation steps?
- Does this imply decision-useful representation differs from visually faithful future reconstruction?
- Separate video pretraining/data-scale gains from the specific hidden-feature planner interface.

### 4.4 Auto-JEPA

Primary comparison role: intentionally compressed future prediction toward planning intent rather than dense reconstruction.

Questions:

- What is the JEPA target exactly?
- Which future information is deliberately not reconstructed?
- How is ego action/planning intent represented in the predictive objective?
- Is the target used only during training, or does a predicted future latent survive at inference?
- What matched evidence supports compression toward decision-relevant information rather than simply another auxiliary loss?
- Compare directly with OccWorld’s reconstruction counterexample and LAW’s horizon result.

### 4.5 DA-WAM

Primary comparison role: per-candidate future latent → candidate score.

Questions:

- For each candidate ego trajectory, what future latent is predicted and what information conditions it?
- Which candidate receives direct observed-future latent supervision?
- What supervision remains for non-executed / non-expert candidates?
- How does future latent enter the scorer?
- What matched ablation isolates action-conditioned future from shared/current latent alternatives?
- Does the experiment establish ranking utility, counterfactual correctness, both, or neither?
- Keep explicit the distinction between architecture-level candidate conditioning and reactive oracle supervision.

### 4.6 Think2Drive

Primary comparison role: latent WM as Dreamer-style policy-training environment.

Questions:

- What observation/state is encoded into the latent dynamics model?
- What action/control variable drives latent transitions?
- How are reward, continuation/termination, value and policy learned?
- Is the world model executed in the deployed driving loop, or mainly used to train the policy through imagined trajectories?
- What amount of real simulator interaction versus imagined experience is used?
- Which closed-loop evidence establishes benefit, and what simulator/model-bias boundaries remain?
- Compare this lineage with ViDAR/LAW: all can improve a policy without an online explicit future evaluator, but by different mechanisms.

## 5. Required Wave-3 artifacts

Create during/after reading:

```text
landscape/PHASE_B_WAVE3_SYNTHESIS.md
```

Optional source audit only if a decision-critical inference-path ambiguity remains:

```text
audits/literature/PHASE_B_WAVE3_INTERFACE_CODE_AUDIT.md
```

Do not audit source code merely because code exists.

## 6. Wave-3 synthesis questions

The final synthesis must answer:

1. Does “world-action unification” refer to shared representation, co-generation, token interleaving, or actual consequence-based decision making?
2. Which methods require a predicted future at deployment, and which use future prediction only to shape representations/policies during training?
3. Can compressed/hidden predictive state be more planning-useful than explicit visual reconstruction, and what direct evidence supports that statement?
4. When candidate-specific futures are used, how are unexecuted alternatives supervised?
5. Does joint modeling improve planning beyond stronger action modeling or shared multi-task representation?
6. Where does model-based RL sit relative to planning-centric WAM: online planner interface or policy-learning mechanism?
7. What claims remain unsupported after controlling for candidate quality, reward/scorer, representation, data, and evaluation regime?

## 7. Stop condition

Wave 3 closes only when the six anchors can be placed on one inference-interface map without using the generic phrase “uses a world model” as explanation.

Required stable taxonomy should be able to distinguish at least:

```text
shared-latent joint training
interleaved world-action generation
hidden-WM-feature action generation
compressed predictive representation shaping
candidate-specific predictive evaluation
WM-based imagined policy learning
```

No research gap or method proposal is authorized at Wave-3 closeout. Wave 4 must still test semantic reasoning, simulator realism, reactive-agent validity, and interactive closed-loop evidence.