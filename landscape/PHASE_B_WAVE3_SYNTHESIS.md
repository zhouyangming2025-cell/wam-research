# PHASE_B_WAVE3_SYNTHESIS — What Does World–Action Unification Actually Mean?

Last updated: 2026-09-14

Status: **FIRST COMPARATIVE BLOCK COMPLETE — Epona ↔ DrivingGPT**

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

## 1. First result: Epona and DrivingGPT are both “unified,” but in fundamentally different senses

The first two anchors already invalidate a single bucket called `unified world-action model`.

```text
Epona:
shared historical latent F
→ separate continuous diffusion generation heads
   ├─ TrajDiT → future ego trajectory
   └─ VisDiT  → next visual frame

DrivingGPT:
interleaved discrete sequence
z1, q1, z2, q2, ...
→ one causal autoregressive transformer
→ next visual/action tokens under one next-token objective
```

The relevant distinction is:

```text
SHARED-LATENT / MODULAR GENERATION
!=
SHARED-SEQUENCE / TOKEN-LEVEL AUTOREGRESSION
```

Both couple world modeling and planning during learning, but the location and strength of the coupling are different.

---

## 2. Epona — joint world/action learning through a shared historical latent, not through online visual rollout evaluation

### 2.1 Exact representation and data flow

Historical observations are compressed into continuous visual latents `Z_t`; historical ego motion is represented as relative pose change `(Δθ, Δx, Δy)`. The Multimodal Spatiotemporal Transformer (MST) concatenates projected visual-latent patches and action embeddings, processes them with causal temporal and multimodal spatial attention, and retains the final-frame embedding:

```text
{past visual latents, past ego motion}
→ MST
→ F = compact historical latent
```

Two specialized diffusion transformers then consume the same `F`:

```text
F + noisy future trajectory
→ TrajDiT
→ denoised 3 s future trajectory

F + noisy next-frame latent + action condition
→ VisDiT
→ next visual latent/frame
```

The two branches use rectified-flow losses:

```text
L = L_traj + L_vis
```

The visual branch may be conditioned on the action predicted by TrajDiT or on an externally supplied action.

### 2.2 What is actually unified?

Epona unifies:

```text
historical world/action representation in MST
+ end-to-end joint optimization of trajectory and visual prediction
+ a common latent F feeding both generation branches
```

It does **not** unify trajectory and visual output into one autoregressive token stream. TrajDiT and VisDiT remain separate modality-specific generators.

### 2.3 Deployed planning path

The paper explicitly states that `MST + TrajDiT` can serve as the real-time planner while video prediction is deactivated.

Therefore the deployed planning path can be:

```text
history
→ MST latent F
→ TrajDiT
→ trajectory
```

without:

```text
VisDiT → generated future image → trajectory scoring/refinement
```

This is a crucial Wave-3 classification result:

```text
Epona world modeling affects planning primarily through the shared learned latent/training objective.
A generated visual future is not required online for trajectory selection.
```

VisDiT can consume the trajectory/action for controllable visual rollout, but the paper-level planning path does not show the generated visual future feeding back into TrajDiT in the same decision step.

### 2.4 Strongest planning evidence

On NAVSIM the paper reports `86.2 PDMS` for Epona with camera input. On nuScenes it reports competitive planning with front-camera input and no auxiliary labels.

More important than the headline SOTA comparison is the paper’s internal ablation: disabling video prediction and training only trajectory prediction causes a noticeable NAVSIM planning drop. This directly supports:

```text
joint visual-prediction supervision + shared latent
> trajectory-only training
```

inside the same Epona family.

The raw Markdown does not preserve the numeric cells of that Table-5 image, so the direction of the ablation is source-supported but exact values should be read from the canonical PDF before quoting.

### 2.5 Strongest limitation / competing explanation

The ablation establishes benefit from **joint visual future supervision**, but does not prove that the benefit comes from an online imagined future. The generated future image is not needed by the planner path. Competing explanations include:

```text
richer multi-task supervision
better historical representation F
regularization from visual prediction
more useful temporal dynamics features
```

Thus Epona is stronger evidence for:

```text
world prediction can shape a better shared planning representation
```

than for:

```text
planning improves because the deployed planner explicitly evaluates imagined visual consequences
```

### 2.6 Evaluation boundary

NAVSIM is non-reactive pseudo-simulation. The paper also reports nuScenes open-loop-style trajectory metrics. These results establish planning quality under those protocols, not reactive social-world correctness.

---

## 3. DrivingGPT — world and action become one causal token language

### 3.1 Exact numerical representation

DrivingGPT deliberately discretizes both modalities.

Visual observation:

```text
front camera image
→ VQ-VAE
→ discrete image tokens z_t
```

Action:

```text
frame-to-frame relative motion (Δx, Δy, Δθ)
→ clamp to 1st–99th percentile
→ component-wise uniform quantization
→ three action-token vocabularies q_t
```

The driving sequence is then:

```text
z1, q1, z2, q2, ..., zT, qT
```

with a unified vocabulary and a Llama-like causal transformer trained by standard cross-entropy next-token prediction.

### 3.2 Why actions are framewise rather than long-horizon trajectory tokens

The paper explicitly argues that placing a whole long-horizon action sequence after every observation would leak future actions into later prediction positions and encourage copying. It therefore models framewise relative ego motion.

This creates a different planning semantics from Epona:

```text
Epona     = one diffusion process generates a multi-second continuous trajectory
DrivingGPT = future driving unfolds as sequential relative-action tokens
```

### 3.3 What is actually unified?

DrivingGPT unifies more aggressively at the sequence-model level:

```text
one vocabulary space
one interleaved causal sequence
one transformer
one next-token objective
```

Image and action are treated as modalities of the same “driving language.”

This is not merely two losses attached to a shared backbone.

### 3.4 Inference-path interpretation — important but not yet source-code audited

The paper’s formal sequence order is interleaved and causal. Predicted image tokens are decoded to images and predicted action tokens are unbinned to trajectories. Therefore the paper-level formulation implies that future visual and action tokens are generated within the same autoregressive context rather than through independent heads.

However, the primary text reviewed in this first pass does not provide a sufficiently explicit implementation-level statement about whether NAVSIM planning inference must generate every intervening future visual token before every later action token, or uses an optimized planning-only decoding path.

Current status:

```text
paper-level shared-sequence coupling = ESTABLISHED
exact optimized planning decode path  = TO VERIFY only if decision-critical
```

Do not yet upgrade this into a source-code fact.

### 3.5 Direct planning evidence

On NAVSIM navmini under the paper’s stated 4-second non-reactive scoring setup:

```text
Constant Velocity          24.2 PDMS
ResNet-50 + MLP            77.8
LAW                        82.7
DrivingGPT                 82.4
```

All of the paper’s core no-auxiliary-supervision planning baselines use front-camera input; DrivingGPT uses VAE tokens and explicitly omits ego status.

The copy-action ablation is useful:

```text
all predicted x/y/yaw      82.4 PDMS
copy longitudinal x        53.5
copy lateral y             79.4
copy yaw                   73.1
```

This is evidence that the planner is not merely extrapolating/copying the last observed action, especially for longitudinal and yaw behavior.

The paper also reports position embeddings for action tokens as critical (`65.3 → 82.4 PDMS` when action positional embedding is enabled in the shown ablation), indicating that **how action tokens are represented inside the sequence model materially affects planning**.

### 3.6 What the paper does not isolate

The most important missing matched control is:

```text
same DrivingGPT architecture + same action tokens
BUT no future visual-token modeling
```

versus full joint world/action modeling.

The reported `77.8 → 82.4` gain over ResNet-50+MLP simultaneously changes:

```text
visual representation (pixels/encoder vs VQ tokens)
model family (CNN+MLP vs autoregressive Transformer)
action representation
autoregressive objective
joint visual/action sequence modeling
```

Therefore it does **not** causally isolate:

```text
joint world modeling itself → +4.6 PDMS
```

Likewise, video-generation FID/FVD gains do not establish the source of planning gains.

### 3.7 Evaluation boundary

The paper states that NAVSIM metrics are computed after a 4-second **non-reactive** simulation. Thus strong planning scores do not validate whether generated visual futures contain correct behavioral responses of surrounding agents to ego intervention.

---

## 4. Epona ↔ DrivingGPT — first Wave-3 comparison matrix

| axis | Epona | DrivingGPT |
|---|---|---|
| world state | continuous compressed visual latent | discrete VQ image tokens |
| action state | continuous relative pose trajectory | discretized framewise `(Δx, Δy, Δθ)` tokens |
| history/world-action fusion | MST shared latent `F` | one interleaved causal token sequence |
| future visual generator | separate VisDiT | same autoregressive transformer/token language |
| trajectory generator | separate TrajDiT | same autoregressive transformer/token language |
| training coupling | shared `F` + `L_traj + L_vis` | one next-token objective over image+action tokens |
| action→world coupling | TrajDiT/external action conditions VisDiT | actions and images occur in same causal sequence |
| world→current action coupling | through shared learned `F`; generated image not required by planner | paper formulation suggests token-level causal context; exact planning-only decode path not yet implementation-verified |
| can visual generation be disabled for planning? | **yes, explicitly stated** | not established in first-pass paper text |
| cleanest planning evidence for joint WM | trajectory-only vs joint video+trajectory training ablation (direction clear; exact table value needs PDF) | no same-model action-only vs joint visual/action matched ablation found |
| planning evaluation | nuScenes + NAVSIM | NAVSIM navmini; non-reactive |
| main attribution confound | multi-task visual supervision vs “world imagination” | architecture/action-token/objective changes vs world co-modeling |

---

## 5. First Wave-3 field correction

A useful hierarchy is emerging:

```text
Epona:
world and action are jointly LEARNED,
but trajectory and visual future remain modular at inference.

DrivingGPT:
world and action are jointly SEQUENCED,
so unification is stronger at the autoregressive modeling level.
```

Yet stronger architectural unification does **not** automatically mean stronger evidence that world modeling causes planning gain.

In fact, on causal attribution:

```text
Epona has the cleaner joint-vs-trajectory-only training ablation.
DrivingGPT has the stronger token-level unification, but a weaker matched isolation of the world-model contribution to planning.
```

This distinction should remain central for the rest of Wave 3.

---

## 6. Do not numerically rank Epona and DrivingGPT from headline PDMS

The papers report different NAVSIM setups/splits and model details; DrivingGPT explicitly reports navmini planning, while Epona reports NAVSIM test-set performance. Their `86.2` and `82.4` headline PDMS values are therefore **not a clean matched comparison**.

Use each paper’s internal controls to infer mechanism, not cross-paper score ordering.

---

## 7. Next comparison block

Add **DriveLaW** next because it provides a third coupling pattern:

```text
Epona:
shared world/action latent → separate trajectory generator

DrivingGPT:
interleaved world/action tokens → one autoregressive generator

DriveLaW:
video/world-model hidden feature → Action DiT
```

The next audit must determine exactly which video-DiT hidden representation conditions the action model, whether a completed visual future is needed, and which ablations isolate the hidden-world-feature contribution from video pretraining/data scale.

After DriveLaW, bring in Auto-JEPA to test whether **deliberately compressed planning-oriented predictive state** can outperform the assumption that richer future reconstruction is preferable.

---

## 8. Current Wave-3 status

```text
Epona primary-text comparative audit       = COMPLETE first pass
DrivingGPT primary-text comparative audit  = COMPLETE first pass
Epona ↔ DrivingGPT mechanism comparison    = COMPLETE
DriveLaW                                   = NEXT
Auto-JEPA                                  = PENDING
DA-WAM                                     = PENDING
Think2Drive                                = PENDING
Wave 3                                     = OPEN
```

No gap or method inference is authorized from this partial wave.