# PHASE_B_WAVE3_SYNTHESIS — What Does World–Action Unification Actually Mean?

Last updated: 2026-09-14

Status: **SECOND COMPARATIVE BLOCK COMPLETE — Epona ↔ DrivingGPT ↔ DriveLaW**

Wave 3:

```text
Epona
DrivingGPT
DriveLaW
Auto-JEPA
DA-WAM
Think2Drive
```

Purpose: move beyond the generic label `world-action model` and identify the exact coupling among world representation, future prediction, action generation, training supervision, and deployed planning.

Binding controls from Waves 1–2:

```text
matched controls > headline SOTA
generation quality != planning value
world fidelity != decision utility
joint prediction != candidate consequence evaluation
action-conditioned != reactively supervised
WM-assisted planning != online model-based planning
```

---

## 1. Executive result so far: “unified world-action” already means three different things

```text
Epona
= shared historical world/action latent
→ separate continuous trajectory + visual diffusion heads

DrivingGPT
= image/action converted into one interleaved discrete language
→ one causal autoregressive next-token model

DriveLaW
= generative Video-DiT latent is exposed directly to the Action DiT
→ chained world-representation → action generation
```

Thus:

```text
SHARED-LATENT / MODULAR GENERATION
!= SHARED-SEQUENCE / TOKEN-LEVEL AUTOREGRESSION
!= CHAINED GENERATIVE-LATENT → ACTION MODEL
```

Architectural “tightness” and causal evidence for planning value are separate questions.

---

## 2. Epona — joint world/action learning through a shared historical latent, not online visual rollout evaluation

### Exact representation and data flow

Historical observations are compressed into continuous visual latents `Z_t`; historical ego motion is represented by relative pose `(Δθ, Δx, Δy)`. The Multimodal Spatiotemporal Transformer (MST) combines projected visual patches and ego-motion embeddings with causal temporal + multimodal spatial attention and retains the final-frame embedding:

```text
{past visual latents, past ego motion}
→ MST
→ F = compact historical latent
```

Two specialized diffusion transformers consume the same `F`:

```text
F + noisy future trajectory
→ TrajDiT
→ denoised multi-second ego trajectory

F + noisy next-frame visual latent + action condition
→ VisDiT
→ next visual latent/frame
```

Training uses rectified-flow losses:

```text
L = L_traj + L_vis
```

VisDiT may be conditioned on the action predicted by TrajDiT or an externally provided action.

### What is actually unified?

Epona unifies historical world/action representation and joint optimization, but retains modality-specific future generators. It is not one world/action token stream.

### Deployed planning path

The paper explicitly states that `MST + TrajDiT` can run as the real-time planner while video prediction is deactivated:

```text
history → MST/F → TrajDiT → trajectory
```

A generated future image is therefore not required for current trajectory selection. The direction `trajectory/action → VisDiT` exists for controllable rollout, but the paper does not show `generated image → TrajDiT` feedback in the same planning step.

### Strongest planning evidence

Epona reports `86.2 PDMS` on its NAVSIM test setup and competitive nuScenes planning without auxiliary perception labels. More important is its internal ablation: disabling video prediction and training trajectory prediction alone causes a noticeable planning degradation. This supports:

```text
joint visual-future supervision + shared F
> trajectory-only training
```

The raw Markdown stores that Table-5 result as an image, so exact cells should be checked from the canonical PDF before quoting numbers.

### Evidence boundary

This is evidence that visual future prediction helps shape the shared planning representation. It is not evidence that the deployed planner improves because it explicitly scores imagined visual consequences. Alternative mechanisms include multi-task regularization, richer temporal representation, and better historical latent learning.

NAVSIM remains non-reactive pseudo-simulation; nuScenes planning remains open-loop-style.

---

## 3. DrivingGPT — world and action become one causal token language

### Exact numerical representation

Visual observation:

```text
front image → VQ-VAE → discrete image tokens z_t
```

Action:

```text
relative motion (Δx, Δy, Δθ)
→ clamp 1st–99th percentile
→ component-wise bins
→ discrete action tokens q_t
```

Unified sequence:

```text
z1, q1, z2, q2, ..., zT, qT
```

A Llama-like causal transformer with a unified vocabulary is trained by standard cross-entropy next-token prediction.

### Why framewise actions?

The paper argues that inserting a whole future trajectory at each frame would leak future action information and encourage copying. It therefore predicts frame-to-frame relative actions. Thus:

```text
Epona      = continuous multi-second trajectory generated as one diffusion object
DrivingGPT = trajectory unfolds through sequential relative-action tokens
```

### What is actually unified?

DrivingGPT unifies:

```text
vocabulary
sequence
Transformer
next-token objective
```

This is stronger sequence-level coupling than simply attaching two task heads to a shared backbone.

### Inference-path interpretation

The paper formulation establishes that future image and action tokens live in one causal sequence; generated image tokens can therefore become causal context for later tokens. However, the reviewed paper text does not make the optimized NAVSIM planning decode path explicit enough to establish whether every intervening visual token must actually be generated at deployment or whether a planning-specific shortcut is used.

Current status:

```text
paper-level shared-sequence coupling = ESTABLISHED
exact optimized planning decode path  = NOT SOURCE-CODE VERIFIED
```

### Planning evidence

On the paper’s NAVSIM navmini setup:

```text
Constant Velocity       24.2 PDMS
ResNet-50 + MLP         77.8
LAW                     82.7
DrivingGPT              82.4
```

The copy-action experiment is useful evidence against trivial history extrapolation:

```text
all predicted x/y/yaw   82.4
copy longitudinal x     53.5
copy lateral y          79.4
copy yaw                73.1
```

Action-token positional embedding is also material in the shown ablation (`65.3 → 82.4 PDMS`).

### Main attribution weakness

The missing control is:

```text
same DrivingGPT architecture + same action-token formulation
but without future visual-token modeling
```

The ResNet-MLP comparison changes representation, architecture, objective, action modeling and world/action coupling simultaneously. Therefore it does not isolate `joint world modeling → planning gain`.

The paper states its NAVSIM planning score comes from a 4-second non-reactive simulation, so it is not reactive behavioral evidence.

---

## 4. DriveLaW — generation becomes a representation provider for the planner

DriveLaW introduces a third coupling type. Instead of having a visual generator run in parallel with a planner, or placing world/action in the same discrete sequence, it exposes the **internal denoising representation of the video world model directly to the action generator**.

### 4.1 Exact representation path

The video model encodes historical observations with a spatiotemporal VAE and runs a Video DiT in latent diffusion/rectified-flow space. From the denoising trajectory it extracts an intermediate feature:

```text
past driving observations
→ spatiotemporal VAE / Video DiT
→ denoising latent state z_t
→ mid-level feature h_t = φ(z_t)
→ choose t* → planning representation h
```

The planner receives this latent together with action noise and driving context:

```text
video-generator latent h
+ noised action
+ ego status
+ high-level command
→ Action DiT
→ future trajectory
```

The key architectural move is therefore:

```text
Video-DiT INTERNAL STATE
→ DIRECT CONDITION FOR Action DiT
```

not:

```text
fully decoded future RGB video
→ perception module
→ planner
```

A completed rendered video is not required as the planning representation; the planner consumes the generator’s latent activation before pixel decoding.

### 4.2 What is actually unified?

DriveLaW’s “unification” is best described as **chained latent-space coupling**:

```text
video generator learns world representation
→ its latent becomes planner state
→ Action DiT generates trajectory
```

This differs from Epona, where both TrajDiT and VisDiT consume the shared historical latent `F` but visual-generation output is not upstream of planning. It also differs from DrivingGPT, where both modalities are outputs of one causal token process.

### 4.3 Training structure

DriveLaW uses three progressive stages:

```text
Stage 1: lower spatial resolution + long clips → learn long-horizon motion patterns
Stage 2: higher spatial resolution + shorter clips → refine visual detail
Stage 3: condition DriveLaW-Act on DriveLaW-Video latent → train trajectory planner
```

The paper motivates the staged design as avoiding optimization interference between generation and planning. The reviewed primary text does not explicitly establish from the quoted section whether every Video-DiT parameter is frozen during Stage 3; do not assume this without implementation/source confirmation.

### 4.4 Strongest planning evidence is not the 89.1 headline alone

The headline NAVSIM Navtest result is `89.1 PDMS`, but the more informative evidence is internal.

**Video-pretraining scale:**

```text
0 video-pretrain samples   85.9 PDMS
76k                         87.0
3.8M                        87.8
7.6M                        89.1
```

Within the DriveLaW setup, more driving-video pretraining correlates monotonically with planning improvement. This is stronger than comparing against unrelated planners, although data scale can improve representation quality for reasons broader than “world dynamics understanding.”

**Representation comparison under the diffusion planner:**

```text
BEV features        84.1 PDMS
VLM hidden state    86.5
Video latents       89.1
```

This directly supports the usefulness of the chosen video-generator representation in the authors’ planner setup. It still does not perfectly equalize encoder scale, pretraining data and representation capacity, so it is not a pure semantic-variable experiment.

### 4.5 Denoising-step result: the exact internal world state matters enormously

The Action DiT conditioning ablation reports:

```text
t = 1   → 89.1 PDMS
t = 5   → 86.9
t = 10  → 23.2
```

This is unusually strong evidence that:

```text
“use a world-model latent”
```

is scientifically too vague. Planning quality depends sharply on **which internal generative state** is exposed.

The authors interpret the result as decision making preferring useful intermediate latent structure over information that can become redundant/non-essential for action. A conservative interpretation is:

```text
planning utility is representation-state-specific;
visual-generation pipeline stage is not interchangeable.
```

Do not overstate this ablation as proving that lower visual fidelity is always better; the table varies denoising step, not a clean scalar fidelity variable.

### 4.6 Strongest alternative explanation

DriveLaW’s results support generative-latent transfer, but several components co-vary:

```text
large video-pretraining corpus
video-generator architecture
latent compression / denoising representation
ego status + high-level command
Action DiT trajectory model
progressive training curriculum
```

The representation ablation narrows this more than a SOTA table, but it does not fully prove that physical world prediction — rather than strong self-supervised/generative representation learning — is the unique causal mechanism.

This is the same distinction already exposed by ViDAR and LAW:

```text
world prediction may help planning by learning a representation,
without requiring an explicit decoded future to be evaluated online.
```

DriveLaW differs because the **online planner actually consumes the running world-model hidden state**, whereas ViDAR/LAW can improve planning with their future-prediction outputs absent from the deployed decision path.

### 4.7 Evaluation boundary correction

The DriveLaW paper describes NAVSIM results using “closed-loop metrics,” but NAVSIM’s benchmark semantics remain non-reactive pseudo-simulation. Therefore:

```text
89.1 PDMS = strong NAVSIM planning evidence
```

but not:

```text
89.1 PDMS = reactive closed-loop behavioral validation
```

The paper also reports nuScenes open-loop planning metrics.

---

## 5. Three-way interface matrix

| axis | Epona | DrivingGPT | DriveLaW |
|---|---|---|---|
| world representation | continuous historical latent `F` | discrete VQ image tokens | Video-DiT denoising latent/hidden feature |
| action representation | continuous multi-step relative trajectory | discrete framewise relative-action tokens | continuous diffusion/flow-matched trajectory |
| unification unit | shared latent + joint loss | one causal multimodal token sequence | world-model hidden state becomes planner condition |
| world generator | VisDiT | same autoregressive Transformer | Video DiT |
| action generator | TrajDiT | same autoregressive Transformer | Action DiT |
| generated RGB needed for planning? | **no** | unclear whether visual-token generation can be bypassed in optimized planning path | **no pixel decode required; latent is consumed** |
| world-model computation online? | MST yes; visual generator can be off | yes at shared-sequence formulation level | **yes, Video-DiT latent feeds planner** |
| cleanest causal planning evidence | joint video+trajectory training > trajectory-only | no matched action-only-vs-joint visual/action control found | video-pretrain scaling + representation ablation + denoising-step ablation |
| candidate consequence evaluation? | no | no explicit candidate evaluator | no |
| evaluation | nuScenes + NAVSIM | NAVSIM navmini non-reactive | NAVSIM Navtest + nuScenes |

---

## 6. The field transition is not “more and more world-model-like”; it is a change in where world knowledge enters action

The three papers reveal a more useful historical axis:

```text
Epona:
world knowledge enters action through SHARED HISTORY REPRESENTATION

DrivingGPT:
world and action are learned as a SHARED CAUSAL LANGUAGE

DriveLaW:
world knowledge enters action through ONLINE GENERATOR HIDDEN STATE
```

This axis is more informative than labels such as `video WM`, `unified WM`, or `WAM`.

A second axis is now necessary:

```text
training coupling strength
vs
inference coupling strength
```

Epona has strong joint training but can disable visual generation for planning. DriveLaW explicitly keeps the world-generator latent on the planning path. DrivingGPT is maximally shared at the sequence/objective level, but its exact optimized planning decode path remains an implementation-level question.

---

## 7. Evidence-strength correction: stronger coupling is still not proof of the reason for better planning

The strongest matched evidence so far differs by paper:

```text
Epona:
remove visual-prediction task → planning worsens
⇒ joint future supervision helps the shared representation

DriveLaW:
scale video pretraining → planning improves
change representation under same planner → video latent strongest
change denoising step → planning changes sharply
⇒ generative hidden representation is materially tied to planner quality

DrivingGPT:
planning beats simple MLP baseline and action-copy variants
but no same-model “remove world-token prediction” control found
⇒ unified sequence works, causal contribution of world modeling less isolated
```

This is a much stronger conclusion than ranking their SOTA numbers.

---

## 8. Do not numerically rank Epona, DrivingGPT and DriveLaW from headline PDMS alone

DrivingGPT explicitly reports NAVSIM navmini in its planning section; Epona and DriveLaW report NAVSIM test/Navtest settings, and model inputs/training/data differ. Therefore `82.4 / 86.2 / 89.1` must not be read as a controlled historical progression.

Use internal ablations to understand mechanism.

---

## 9. Next comparison block — Auto-JEPA

Auto-JEPA is now the correct next anchor because Wave 2 + the first three Wave-3 papers have made one question unavoidable:

```text
If planning mainly benefits from a useful predictive representation,
why reconstruct/generate a rich visual future at all?
```

Auto-JEPA must be read against three established controls:

```text
OccWorld: better reconstruction can yield worse forecast/planning
LAW: longer future target is not monotonically better
DriveLaW: planning depends strongly on which generator latent is exposed
```

The Auto-JEPA audit should therefore focus on exactly what future information its JEPA target preserves/discards, whether its predictive target exists at inference, and whether matched evidence supports a planning-oriented compressed latent rather than simply another auxiliary loss.

---

## 10. Current Wave-3 status

```text
Epona primary-text comparative audit       = COMPLETE first pass
DrivingGPT primary-text comparative audit  = COMPLETE first pass
DriveLaW primary-text comparative audit    = COMPLETE first pass
three-way interface synthesis              = COMPLETE
Auto-JEPA                                  = NEXT
DA-WAM                                     = PENDING
Think2Drive                                = PENDING
Wave 3                                     = OPEN
```

No gap or method inference is authorized from this partial wave.