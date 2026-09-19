# P0001 Epona — Dimension-first Deep Analysis v2

> Paper: **Epona: Autoregressive Diffusion World Model for Autonomous Driving**  
> Purpose: determine whether Epona is online imagined-future planning, joint world/action generation, predictive representation learning, or a distinct hybrid; pressure-test LAW/WoTE dimensions rather than accepting the paper's “world model as planner” phrasing at face value.  
> Source inspected: `papers/raw_md/P0001_Epona/P0001_Epona.raw.md` (ICCV 2025 camera-ready text layer in repo).  
> Existing card `papers/cards/P0001_Epona.md` was only a skeleton and is not treated as scientific evidence.

---

# 0. Executive verdict

Epona is best classified as a **shared-history-latent joint world/action generative model whose deployed planning mode is a direct generative policy, not an online consequence evaluator**.

Its key architecture is:

```text
historical front-camera observations O_1:T
+ historical ego motions/actions a_0:T
→ Multimodal Spatiotemporal Transformer (MST)
→ compact shared historical latent F

F → TrajDiT → generate future 3-s ego trajectory

F + action (TrajDiT-predicted or user-provided)
→ VisDiT → generate next-frame visual latent/image
```

Training:

```text
L = L_traj + L_vis
```

Both diffusion/flow branches backpropagate through the shared historical representation.

Planning inference, however, can be:

```text
history → MST → F → TrajDiT → trajectory
```

with **VisDiT deactivated**.

Therefore Epona is *not* WoTE-like:

```text
candidate action → predicted visual future → score → select
```

and it is *not* World4Drive-like:

```text
K candidate trajectories → K future world latents → ScoreNet → select
```

The visual future does not need to be generated to produce the deployed trajectory. Its planning value is primarily established through **joint representation learning / shared-latent supervision**, not online visual-future evaluation.

At the same time, Epona is more tightly unified than LAW because trajectory generation is itself a generative branch of the world-model architecture and the shared historical latent is trained jointly by both visual-future and trajectory objectives.

---

# 1. What problem does Epona actually solve?

Epona targets two limitations that the paper argues are usually separated:

```text
A. driving world models
   → high-fidelity visual generation
   → but fixed/short horizon and poor planning integration

B. autoregressive token world models
   → flexible temporal generation
   → but discretization hurts visual/trajectory precision
```

Its proposed solution is a factorized architecture:

```text
causal temporal dynamics modeling
separated from
fine-grained modality generation
```

and then two modality-specific generative heads:

```text
trajectory generation
visual generation
```

sharing the same historical latent.

The paper therefore does **not** start from WoTE's question “how should I score multiple trajectories?” It starts from:

> Can one world-model representation support both long-horizon visual dynamics and direct trajectory generation without forcing both into the same tokenization/generation process?

That difference in problem definition matters for every later comparison.

---

# 2. World-model formulation: Epona factorizes time from modality detail

## 2.1 Conventional video diffusion according to Epona

The paper criticizes fixed-window video diffusion for modeling a joint distribution over a block of future frames, which the authors argue does not impose the desired frame-wise causal temporal structure and makes variable-length autoregression awkward.

## 2.2 GPT-style world models according to Epona

The paper criticizes discrete token autoregression for quantization error and token-by-token spatial fragmentation.

## 2.3 Epona's factorization

Epona instead models:

```text
historical dynamics/context
→ compact causal latent F

then
F → continuous trajectory distribution
F + action → continuous visual next-frame distribution
```

The visual world is rolled forward one frame at a time, while the trajectory branch directly predicts a multi-step 3-second future trajectory.

### New comparison dimension: temporal factorization level

`dynamics architecture` is too coarse. We need to ask whether a method models:

- fixed-window future jointly;
- token-autoregressive future;
- frame-autoregressive world state;
- latent recurrent state;
- long-horizon trajectory in one shot;
- different temporal factorization for different modalities.

Epona is especially important because **visual time and trajectory time are factorized differently inside one model**.

---

# 3. MST: the shared historical world representation

## 3.1 Inputs

Epona takes historical:

```text
visual latents Z_1:T
historical ego motions a_0:T
```

The action/motion at each step is represented by relative pose change:

```text
(Δθ, Δx, Δy)
```

Visual patches and action tokens are projected into one embedding space.

## 3.2 Interleaved temporal and multimodal-spatial attention

MST alternates:

```text
causal temporal attention
↕
multimodal spatial attention
```

and finally takes the last-frame latent embedding as:

```text
F ∈ R^{B × (L+3) × D}
```

which summarizes historical scene/action context.

### What `F` is scientifically

`F` is not a predicted future world state.

It is a **compressed historical context state** trained so that two different future tasks can be decoded from it:

```text
future trajectory
future image
```

This forces a distinction that LAW/WoTE did not make explicit enough:

> **current/historical world representation** and **predicted future world representation** are different objects and should occupy separate dimensions.

Epona's planner uses the former (`F`) at inference; it does not require the latter (VisDiT output).

---

# 4. TrajDiT: trajectory prediction is a direct generative policy

## 4.1 Target

Ground-truth future trajectory:

```text
a_bar ∈ R^{B × N × 3}
```

is noised according to the rectified-flow formulation.

TrajDiT predicts the flow/velocity conditioned on `F`:

```text
noise → iterative denoising conditioned on F → future trajectory
```

Loss:

```text
L_traj = E ||v_traj(a_t,t | F) - (a_bar - ε)||²
```

## 4.2 Decision semantics

This is not:

```text
produce candidate set
→ world-model each candidate
→ score candidates
```

Instead:

```text
F
→ sample/denoise from learned trajectory distribution
→ trajectory output
```

There is no explicit consequence evaluator or reward/value model in the planning path described by the paper.

### New dimension: action-selection mechanism

LAW and WoTE reveal that `planning interface` is still too broad. We must distinguish:

```text
direct regression policy
direct autoregressive policy
direct diffusion/flow generative policy
candidate generation + rule scorer
candidate generation + learned value scorer
candidate generation + world consequence + scorer
search/planning over learned dynamics
```

Epona = **direct diffusion/flow generative policy from shared world representation**.

## 4.3 Multimodality

Because the trajectory is generated from noise through a flow model, the architecture is distributional/stochastic rather than a single deterministic regression head.

But the paper does not present a WoTE-like explicit set of `N` candidates all scored against predicted consequences.

Therefore:

```text
trajectory multimodality
!=
candidate-set evaluation
```

This is another mandatory distinction.

---

# 5. VisDiT: visual future is action-conditioned, but one-way at the same decision step

VisDiT predicts the next future image latent with flow matching:

```text
F + action a_{T→T+1}
→ VisDiT
→ Z_hat_{T+1}
→ DCAE decoder
→ O_hat_{T+1}
```

The action can be:

```text
TrajDiT-predicted action
or
externally provided action
```

This gives Epona controllable video generation.

## 5.1 Exact coupling direction

At a single planning step:

```text
F → TrajDiT → action
F + action → VisDiT → visual future
```

The paper does **not** define:

```text
visual future → trajectory rescoring/refinement
```

Therefore the coupling is structurally **action→visual future**, not a WoTE-style future→action evaluation loop.

## 5.2 Why the phrase “joint modeling” can mislead

The two branches are jointly trained and share `F`, but they are not symmetric online peers.

We should distinguish at least three notions of jointness:

```text
parameter/shared-representation jointness
loss/gradient jointness
online causal feedback jointness
```

Epona has strong first/second forms but no demonstrated same-step visual-future→trajectory feedback in its planning mode.

This becomes a new ontology axis.

---

# 6. Training coupling: where visual world modeling helps planning

The total training loss is:

```text
L = L_traj + L_vis
```

Because both branches depend on `F`, the shared MST representation is optimized by both trajectory and visual-future prediction.

The paper's key planning ablation removes joint video prediction and trains trajectory only:

```text
w/o joint training   PDMS 78.1
full Epona           PDMS 86.2
```

The component metrics also improve substantially.

## 6.1 What this directly supports

Within the reported configuration:

> adding visual next-frame prediction as a joint objective materially improves the trajectory-planning system that consumes the shared latent.

This is strong evidence for **cross-modal predictive representation shaping**.

## 6.2 What it does NOT prove

It does not prove:

```text
higher FID/FVD quality → better planning
```

Nor does it prove:

```text
online visual imagination → better action selection
```

because VisDiT can be deactivated during trajectory planning.

The ablation combines at least:

```text
extra visual predictive supervision
+ shared-latent regularization
+ additional gradient signal to MST
```

It does not isolate which semantic property learned from video prediction is responsible for the planning gain.

### Horizontal relation to LAW

LAW:

```text
planner representation
+ predicted action
→ auxiliary future-latent loss
→ shared representation/planner improved
```

Epona:

```text
shared history latent F
→ visual future generative loss
+ trajectory generative loss
→ shared representation improved
```

Both provide evidence that future prediction can improve planning **without the predicted future being consumed by planning inference**.

But Epona differs because trajectory generation is itself a native generative branch of the same world-model architecture rather than a conventional waypoint head augmented by an auxiliary WM.

---

# 7. Planning mode vs simulation mode: one model has multiple deployed graphs

Epona explicitly advertises modular execution.

## 7.1 Planning mode

```text
history
→ MST
→ F
→ TrajDiT
→ trajectory
```

VisDiT disabled.

## 7.2 Controllable simulation mode

```text
history
→ MST
→ F
+ external action or TrajDiT action
→ VisDiT
→ next frame
→ append generated frame to history
→ autoregressive continuation
```

## 7.3 Joint world/action rollout mode conceptually

If actions come from TrajDiT while generated frames are recursively fed forward, the model can create an autoregressive world/action sequence. But the paper's planning benchmark does not demonstrate that such visual rollout is used to choose the benchmark trajectory.

### New dimension: task-mode-dependent inference graph

A single yes/no field such as `uses world model online` is insufficient for modular models.

Record computational graph separately for:

```text
planning mode
simulation mode
controllable generation mode
training mode
```

Epona is the clearest anchor so far showing why this is necessary.

---

# 8. Chain-of-Forward: training explicitly for rollout distribution shift

Epona's visual autoregression faces:

```text
training: ground-truth historical frames
inference: model-generated historical frames
```

The Chain-of-Forward strategy periodically replaces clean history with self-predicted states using several forward passes, approximating inference-time errors during training.

This is conceptually related to scheduled sampling / rollout-noise robustness, but implemented for diffusion/flow prediction with an approximate one-step denoised latent.

## 8.1 New dimension: rollout-distribution robustness training

For any autoregressive WAM, record:

```text
teacher-forcing only?
noise augmentation?
self-generated context training?
scheduled sampling?
latent corruption?
multi-step consistency loss?
```

LAW does not require long free-running deployment rollouts.
WoTE recurrently rolls compact BEV states online but the paper's highlighted training design is not a Chain-of-Forward-style explicit self-prediction robustness strategy.
Epona makes this a first-class design problem.

## 8.2 Evidence boundary

Chain-of-Forward is supported by long-video FID/qualitative degradation comparisons. The evidence primarily supports **visual rollout stability**, not planning performance.

Therefore world-generation robustness and planning robustness must remain separate dimensions unless an experiment links them.

---

# 9. Temporal-aware decoder: visual quality module with weak direct planning relevance

DCAE compresses image latents aggressively (32× spatial downsampling) to reduce tokens and make long-context world modeling feasible.

Because frame-wise decoding flickers, Epona adds spatiotemporal self-attention before the decoder while keeping the encoder frozen during fine-tuning.

This is an important example of the user's requested rule:

> When a paper adds a module, immediately ask whether it belongs to the planning comparison space or only to a modality-specific quality path.

For Epona:

```text
temporal-aware decoder
→ improves generated-video temporal consistency
→ NOT part of planning-only inference graph
```

So it should be recorded under **modality-specific auxiliary capability/cost**, not mistaken for a planning mechanism.

---

# 10. Compute and deployment: “real-time” depends on sampling steps and active branches

Epona has about 2.5B parameters:

```text
MST      ~1.3B
VisDiT   ~1.2B
TrajDiT  ~50M
```

Reported single RTX 4090 timings:

```text
10 DiT steps:
MST      ~0.02 s
TrajDiT  ~0.03 s
VisDiT   ~0.3 s

100 DiT steps:
MST      ~0.02 s
TrajDiT  ~0.3 s
VisDiT   ~2 s
```

The paper says all experiments use 100 sampling steps, while also noting that MST + TrajDiT can reach real-time rates such as ~20 Hz under reduced sampling steps.

## 10.1 Evidence boundary

We must distinguish:

```text
reported best benchmark operating point
vs
reported fastest module operating point
```

The text does not, in the inspected main paper, provide a matched planning-quality table for 10-step versus 100-step TrajDiT.

Therefore “20 Hz planner” is a **speed capability claim**, but the exact quality retained at that fastest setting is not established by the planning tables inspected here.

### New dimension: quality–latency operating curve

For diffusion/generative planners, one latency number is inadequate. Record:

```text
sampling steps
quality at those steps
active modules
hardware
end-to-end vs module latency
```

---

# 11. Evaluation evidence must be split by capability

## 11.1 Visual-generation evidence

The paper reports:

```text
FVD 82.8 on NuScenes comparison
up to ~120s / 600-frame plausible rollout claim
trajectory-controlled qualitative generation
Chain-of-Forward long-video quality evidence
```

These support visual-world capability.

They do **not** directly prove planning improvement.

## 11.2 Planning evidence

NuScenes:

- front-camera-only setup;
- competitive rather than best trajectory L2;
- relatively low collision in reported comparison.

NAVSIM:

```text
Epona PDMS 86.2
```

and the crucial internal ablation:

```text
trajectory-only training 78.1
joint visual+trajectory   86.2
```

The latter is the strongest evidence relevant to our WAM/planning question.

## 11.3 Missing evidence relative to WoTE

Epona does not provide a WoTE-style control:

```text
same generated candidate/actions
same evaluator
with vs without online future consequence
```

because Epona does not use such an evaluator architecture.

This is not a flaw by itself; it means Epona addresses a different planning mechanism.

---

# 12. Counterfactual and interaction analysis

## 12.1 Action control

VisDiT can be conditioned on externally provided trajectories/actions, and the paper shows trajectory-controlled videos.

This demonstrates **controllability of generated ego-view future**.

## 12.2 What remains unproven

Controllable output is not sufficient evidence that surrounding agents respond behaviorally correctly to altered ego interventions.

The inspected main paper does not provide a reactive counterfactual benchmark analogous to:

```text
same initial scene
+ alternative ego intervention
→ oracle surrounding-agent responses
→ compare predicted responses
```

Therefore visual controllability should not be conflated with validated interactive counterfactual dynamics.

## 12.3 Counterfactual ladder placement

Provisional:

```text
Epona visual generator output form:
multiple/external-action controllable future generation → at least CF2-form capability

supervision/evidence:
factual logged trajectory/video training; no matched reactive alternative-action oracle established in inspected main paper
```

As with World4Drive, output branching and supervision level must be stored separately.

---

# 13. LAW → WoTE → Epona: three fundamentally different roles of “future”

| Axis | LAW | WoTE | Epona |
|---|---|---|---|
| primary problem | improve representation | evaluate candidates | unify visual world generation + direct planning |
| current/historical state | planner PV/BEV latent | compact BEV state | causal multimodal historical latent `F` |
| action mechanism | one predicted waypoint sequence | 256 candidate trajectories | trajectory generated directly by TrajDiT |
| future world | one latent target prediction | recurrent candidate-specific BEV sequence | next-frame visual diffusion branch |
| future consumed to select current action? | no | yes | no in planning-only mode |
| explicit value/scorer | none | learned multi-reward evaluator | none |
| planning mechanism | conventional planner shaped by auxiliary WM loss | candidate consequence→value→argmax | direct flow/diffusion policy from `F` |
| visual/world prediction helps planning how? | predictive auxiliary gradients | online consequence input | joint visual prediction shapes shared `F` |
| multiple actions | no | explicit candidate set | stochastic generative trajectory distribution, not explicit ranked set |
| alternative-world supervision | one factual future | simulator labels for ego alternatives, non-reactive agents in audited path | factual video/trajectory; action-controllable generation but no reactive alt-world oracle shown |
| deployment world generation | not needed/consumed | compact BEV rollout required | VisDiT can be disabled for planning |
| long-rollout issue | not central | recurrent BEV compounding possible | explicit visual autoregressive drift; Chain-of-Forward addresses it |

This table demonstrates why a single category such as `world-model-assisted planning` is scientifically insufficient.

---

# 14. Dimensions Epona adds or sharpens

The following were treated as residue candidates during this read and are now consolidated in `landscape/WAM_DIMENSION_ONTOLOGY_V1.md`; they are not a separate projection artifact.

## New dimensions

1. **Historical-state representation vs predicted-future-state representation**
2. **Temporal factorization strategy per modality**
3. **Cross-modal shared latent ownership**
4. **Cross-modal parameter sharing vs representation sharing**
5. **Loss/gradient jointness**
6. **Online causal feedback jointness**
7. **Action-selection mechanism: direct generative policy vs candidate evaluator**
8. **Trajectory stochasticity/multimodality vs explicit candidate branching**
9. **Modality coupling direction** (`trajectory→vision`, `vision→trajectory`, bidirectional, siblings only)
10. **Modality-specific branch optionality at inference**
11. **Task-mode-dependent inference graph**
12. **Rollout-distribution-shift training**
13. **Teacher-forcing vs self-generated-context exposure**
14. **Modality-specific quality module vs planning-relevant module**
15. **Benchmark operating point vs fastest operating point**
16. **Sampling-step quality–latency curve**
17. **Visual-generation evidence vs planning evidence separation**
18. **Shared-latent auxiliary-task benefit attribution**
19. **World/action joint generation vs consequence-based planning**
20. **Visual controllability vs behavioral interaction validity**

## Existing dimensions sharpened

- `WM attachment depth`: Epona makes trajectory generation a native branch of the world model rather than an attached planner head.
- `inference-path future consumption`: must be capability/mode specific; simulation consumes visual futures autoregressively, planning-only mode does not.
- `decision semantics`: future visual generation and direct action distribution are siblings, not consequence/value stages.
- `deployment imagination cost`: active branch selection matters as much as model size.
- `counterfactual scope`: controllability evidence and behavioral reactivity evidence must be separate.

---

# 15. Strongest contribution vs strongest limitation

## Strongest contribution for our research question

Epona provides unusually strong evidence that **joint self-supervised visual-future modeling can substantially improve a direct trajectory-generative planner through a shared latent representation**, while retaining a modular planning-only deployment path.

This expands the WAM/planning space beyond both:

```text
LAW: future as auxiliary latent prediction
WoTE: future as online candidate consequence
```

into:

```text
Epona: future world generation + trajectory generation
       jointly shape one historical world state,
       but planning can decode action directly without rolling out vision
```

## Strongest limitation

The paper's broad phrase “world model serves as a planner” can hide the exact causal interface:

> **The planner does not need to inspect its generated visual future before choosing the trajectory.**

Thus Epona should not be used as evidence that high-fidelity visual imagination is directly necessary for online trajectory selection.

Its strongest planning evidence supports shared-representation/joint-training value, not visual-future consequence evaluation.

---

# 16. Claims ledger

| Claim | Evidence | Verdict | What remains unproven |
|---|---|---|---|
| Epona jointly models future scene and trajectory | MST + TrajDiT + VisDiT; `L=L_traj+L_vis` | supported | degree of semantic alignment between samples is not directly measured |
| trajectory can control visual future | VisDiT action conditioning + qualitative controlled generation | supported as controllability | reactive correctness of other agents not established |
| visual prediction helps planning | NAVSIM joint-training ablation 78.1→86.2 PDMS | strongly supported within configuration | whether gain tracks visual fidelity itself or representation regularization |
| visual rollout is required for planning | modular architecture + speed discussion | contradicted | planning uses MST+TrajDiT with VisDiT disabled |
| Epona performs online consequence-based action evaluation | architecture | not supported | no future→score→selection loop |
| Chain-of-Forward improves long rollout | Fig.7/8 long-video evidence | supported for visual rollout | planning benefit not established |
| Epona is real-time planner | module timings show MST+TrajDiT can be fast at reduced steps | partially supported | planning quality at fastest 10-step setting not matched to 100-step benchmark in inspected main text |
| long/high-fidelity video proves stronger planning | separate generation/planning tables | not supported | capability metrics are not causally linked |

---

# 17. Questions to carry into WorldDrive / World4Drive re-projection

1. Does visual/world generation shape planning only through training gradients, as in Epona/LAW, or through online consequence consumption?
2. Is the planner a direct generative policy or candidate generator + evaluator?
3. If an expensive generative world branch exists, is it active at deployment, removed, or distilled?
4. Is trajectory→future-world conditioning one-way, or does predicted future feed back into action?
5. Are trajectory vocabulary/intention modes explicit candidates or merely conditioning modes?
6. What representation is shared between generation and planning, and which parameters are frozen/transferred/jointly trained?
7. Does a shared-latent ablation isolate world-prediction value as cleanly as Epona's 78.1→86.2 result?
8. Do multiple future outputs correspond to true alternative-world supervision?
9. How are world consequence and value semantics separated?
10. What is the actual quality–latency operating point of the deployed planner?

These questions should now be used to re-project the already strong WorldDrive and World4Drive audits into the emerging ontology rather than re-reading them as isolated papers.
