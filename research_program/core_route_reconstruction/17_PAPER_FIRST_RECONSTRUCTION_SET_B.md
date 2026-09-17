# Paper-first reconstruction — Set B

Status: evidence reconstruction only; **no route naming, no ontology update, no M0–M4 assignment**.

Branch context: `research/core-route-reconstruction`

Papers in this set:

1. Epona — *Autoregressive Diffusion World Model for Autonomous Driving*
2. DriveLaW — *Unifying Planning and Video Generation in a Latent Driving World*
3. Metis — *A Generalizable and Efficient World-Action Model for Autonomous Driving and Urban Navigation*
4. ReWorld — *Representation Learning for World Action Models*
5. SimWAM — *A Simple World Action Model for End-to-End Autonomous Driving*

Primary evidence:

- `papers/raw_md/P0001_Epona/P0001_Epona.raw.md`
- `papers/raw_md/P0009_DriveLaW/P0009_DriveLaW.raw.md`
- `papers/raw_md/P0062_Metis/P0062_Metis.raw.md`
- `papers/raw_md/P0052_ReWorld/P0052_ReWorld.raw.md`
- SimWAM arXiv full text: `arXiv:2608.07468` (local raw paper was not available on the branch at audit start)

This document follows the paper-first reset established in `00C_LIVING_FIRST_PRINCIPLES_AUDIT_PAPER_FIRST_RESET.md` and the discipline used in `16_PAPER_FIRST_RECONSTRUCTION_SET_A.md`.

---

## 0. Audit contract

The apparent relation among these five papers is intentionally **not assumed**.

A tempting preconception is that they form a one-dimensional spectrum of “world/action coupling”:

```text
parallel -> chained -> tightly coupled -> decoupled
```

This audit does not accept that picture in advance.

For every paper, the reconstruction asks only factual questions first:

- what scientific problem do the authors say they are solving?
- what state is computed from historical/current observations?
- what does the action module actually read at deployment?
- is a future visual/world output generated before action?
- does the action module consume the future output, an internal generator state, a shared historical state, or only a current observation representation?
- which parameters/representations are shared?
- where can the future-video/world loss send gradients?
- what computation disappears at deployment?
- if the claimed core contribution is removed, what does the method become?

Only after all five reconstructions are complete are cross-paper observations permitted.

---

# 1. Epona

## 1.1 Author-stated problem

Epona is not primarily introduced as a planning-interface paper.

Its starting problem is that two dominant world-model formulations each fail in a different way:

- fixed-window video diffusion has strong visual fidelity but poor temporal decomposition and weak support for flexible long-horizon autoregression;
- GPT-style autoregressive models support temporal causality but quantization harms visual and trajectory precision, and next-token action generation is not naturally suited to long-horizon continuous trajectory planning.

Epona therefore aims to build one continuous autoregressive-diffusion world model that can support:

- long-horizon video generation;
- trajectory-controlled simulation;
- world knowledge learning;
- real-time trajectory planning.

This is broader than “make video generation help planning.”

## 1.2 The actual shared state

Epona first uses a Multimodal Spatiotemporal Transformer (MST) to encode historical visual latents and historical ego motion into a compact latent `F`.

Conceptually:

```text
past observations + past ego motion
→ MST
→ shared historical temporal latent F
```

The important point is that `F` is produced **before** either future output head.

Two separate diffusion transformers then consume `F`:

```text
F -> TrajDiT -> future ego trajectory
F -> VisDiT  -> next future image latent
```

The trajectory and visual heads therefore share an upstream temporal representation but do not require one another’s future output.

## 1.3 Training computation

Trajectory and video generation are jointly optimized:

```text
L = L_traj + L_vis
```

The shared MST receives learning pressure from both tasks.

The video branch is additionally trained for autoregressive long-horizon stability through chain-of-forward training.

The paper’s ablation removes video prediction and trains only trajectory prediction. Planning performance drops. The authors interpret this as evidence that the shared latent `F` learns richer driving dynamics when visual future prediction is present.

Thus future-video learning affects planning **through the shared upstream state/training program**, not because the planner must read the generated next frame.

## 1.4 Deployment computation

For trajectory planning, Epona explicitly states that video prediction can be deactivated.

Planning uses:

```text
history
→ MST
→ F
→ TrajDiT denoising
→ trajectory
```

VisDiT is not required to produce a future image for the trajectory to be generated.

This distinction is critical:

```text
future-video OUTPUT online      NO
shared temporal/world latent F  YES
```

Therefore “video generation is off at inference” does **not** imply that Epona has become an ordinary action-only network. The online planning path still passes through MST, whose intended role is to encode multimodal temporal driving dynamics and whose representation was shaped jointly by visual and trajectory prediction.

## 1.5 Action-to-world relation inside Epona

For simulation mode, VisDiT can be conditioned on an action predicted by TrajDiT or on a user-provided action.

This gives Epona an additional capability:

```text
F -> TrajDiT -> action
          \
           -> VisDiT-conditioned future image
```

But this action-conditioned video branch is not required for the planner-only runtime path.

This is a warning against conflating all capabilities of the paper with the planning mechanism actually used at deployment.

## 1.6 Core-deletion test

Deleting VisDiT **only at deployment** does not destroy Epona’s planning mode; the paper explicitly supports this.

Deleting visual-prediction training altogether is more serious: the matched ablation shows a planning decline, and the shared-world-learning thesis is weakened.

Deleting the MST/shared temporal latent would break the architectural bridge through which the video and trajectory objectives jointly shape planning.

The strongest current interpretation is therefore not “planner consumes predicted future video,” but:

> a shared causal temporal representation is jointly trained to support world prediction and trajectory generation, while the expensive visual output head is optional during planning deployment.

This is a paper-level reconstruction, not a route label.

---

# 2. DriveLaW

## 2.1 Author-stated problem

DriveLaW explicitly argues that existing “unified” world models still fail to transfer the video generator’s internal world understanding tightly enough into planning.

The paper specifically criticizes designs such as Epona for having generation and planning as parallel output modules: both may be trained in one system, but the planner does not directly consume the internal state used by the video generator.

DriveLaW’s central proposal is therefore not merely joint training. It is an explicit **generator-internal-latent -> planner** interface.

## 2.2 Video generator as planning-state producer

DriveLaW first trains a large Video DiT on driving videos.

During denoising, it exposes intermediate generator states:

```text
z_t -> Video DiT -> h_t
```

A selected mid-denoising representation is passed directly to the Action DiT.

The planner path is therefore approximately:

```text
historical observations
→ Video-DiT generative computation
→ intermediate Video-DiT latent h
→ Action DiT
→ trajectory
```

The decoded/generated video itself is not the object that the planner needs. The **internal state of the generative model** is.

This is a much more precise statement than “DriveLaW imagines the future then acts.”

## 2.3 Training program

DriveLaW uses a progressive curriculum:

1. long low-resolution video training for temporal dynamics;
2. shorter high-resolution video training for visual detail;
3. action fine-tuning in which DriveLaW-Act is conditioned on Video-DiT latents.

The paper reports that during trajectory fine-tuning both Video DiT and Planning DiT are updated.

Thus the final planning-facing generator state is not merely a frozen off-the-shelf representation; it can adapt under planning training.

## 2.4 Deployment computation

The paper states separate sampling budgets for video generation and trajectory planning. The exact planning-only low-level execution is more clearly spelled out by the successor ReWorld paper, which instantiates the DriveLaW chained architecture and states that the planner reads Video-DiT block features from the **first discrete video denoising step** in the current forward pass; those features are cached across action-flow steps rather than precomputed offline.

This successor evidence clarifies an important point:

```text
full decoded future video required?       no
online Video-DiT internal computation?    yes
planner reads Video-DiT internal state?   yes
```

This is different from Epona, whose planner consumes a shared historical MST state upstream of the specialized visual future generator.

## 2.5 Core-deletion test

If the `Video DiT latent -> Action DiT` conditioning edge is removed, DriveLaW loses the specific contribution it claims over parallel generation/planning systems.

It would fall back toward:

- a video generator trained for world modeling;
- an action planner that does not directly use generator internals.

That is exactly the design gap the paper says it is closing.

By contrast, noise reinjection and the particular spatiotemporal VAE are important generation techniques but are not sufficient to define the paper’s world-to-planning claim.

---

# 3. Metis

## 3.1 Author-stated problem

Metis begins from almost the opposite practical concern from DriveLaW.

It argues that existing WAMs can fail because:

1. explicit future observation prediction at inference is expensive;
2. tightly coupling high-dimensional video generation and low-dimensional action prediction can create representational mismatch and inject generative noise into the action space.

Its goal is therefore **joint world/action learning without requiring future-video dependence during action inference**.

## 3.2 Two specialized experts, not one shared output stream

Metis uses a Mixture-of-Transformers design with:

- a Video Generation Expert (VGE);
- an Action Expert (AE).

The experts have task-specific projections/feed-forward components and interact through a structured shared latent/attention interface.

The key mechanism is not simply “two heads.” It is an asymmetric token-visibility rule.

## 3.3 Asymmetric attention is directional

Metis states:

- action tokens are allowed to attend only to the current visual observation tokens;
- action tokens cannot read future-video tokens;
- future-video tokens can attend to the current observation **and future action tokens**.

So the forward information structure during joint training is intentionally asymmetric:

```text
current observation -> action tokens
current observation + future action tokens -> future video tokens
```

The future-video process is conditioned by the intended action, but future-video tokens do not become an input to action prediction.

This matters because the paper’s appendix states that generation loss can backpropagate through this dependency into the action expert. In other words, the video task can shape action learning in training even though the action forward path never consumes future-video tokens.

## 3.4 Deployment computation

At inference, future video generation is bypassed.

The paper formalizes planning as:

```text
current observation/context z(o_t,l)
→ Action Expert
→ action/trajectory
```

The action path remains grounded in the current visual representation and the trained action expert, but no future-video sample is required.

This is a **training/deployment asymmetry by design**, not an accidental pruning step.

## 3.5 Matched attention-mask evidence

Metis compares:

- fully joint attention;
- isolated attention;
- its asymmetric attention.

The asymmetric design performs best in the reported study. The authors interpret this as a balance:

- fully joint future/action visibility contaminates or destabilizes action representation;
- completely isolated learning loses useful dynamics transfer;
- asymmetric visibility lets generation learn an action-consistent future while future-generation gradients still improve the action expert, without making action inference depend on future tokens.

This is stronger evidence than a purely architectural claim.

## 3.6 Core-deletion test

If future-video co-training is removed, Metis approaches an ordinary action expert and loses the central WAM claim.

If asymmetric visibility is replaced with full joint attention, the paper’s claimed generalization/stability advantage is weakened.

If future-video tokens are allowed to become required action inputs, the efficient “joint training, decoupled inference” proposition is broken.

Thus the important mechanism is not simply “video branch absent at runtime.” It is the deliberately controlled **forward and backward information flow** between generation and action during training.

---

# 4. ReWorld

## 4.1 Author-stated problem

ReWorld does not primarily propose another architecture for connecting world generation and planning.

It starts from DriveLaW’s chained architecture and argues:

> providing the planner access to Video-DiT latents is not enough; those intermediate states are only indirectly supervised by output losses and may not actually contain the future-predictive and behavior-sensitive information the planner needs.

Its target is the **quality of the world-to-action representation pathway itself**.

## 4.2 Baseline interface is inherited from DriveLaW

ReWorld explicitly instantiates the chained WAM:

```text
Video DiT intermediate states F
→ Action DiT
→ trajectory
```

It clarifies that `F` is taken at the first discrete video denoising step in the current forward pass. These activations remain online and are reused across action denoising steps.

Therefore ReWorld is important evidence that DriveLaW’s planning bridge is an online generator-state interface, not offline representation transfer.

## 4.3 Three-stage representation curriculum

ReWorld then adds three training interventions.

### Stage 1 — make intermediate video states future-predictive

Auxiliary heads force selected Video-DiT intermediate blocks to predict the generator’s future-flow target.

The goal is to make the exact states consumed by planning explicitly predictive rather than hoping useful dynamics emerge from final video reconstruction alone.

### Stage 2 — make action states retain attended world information

The Video DiT is frozen.

Post-cross-attention Action-DiT states are aligned with the video readouts they attended to, using stop-gradient targets.

This explicitly trains the action representation to preserve information retrieved from the world branch.

### Stage 3 — make the shared pathway decision-sensitive

Both branches are jointly fine-tuned using geometrically close but low-scoring hard-negative trajectories.

This lets behavior-quality gradients reshape planner-facing Video-DiT and Action-DiT states.

## 4.4 Deployment computation

ReWorld does not replace the DriveLaW deployment bridge.

Planning still requires:

```text
online Video-DiT intermediate state
→ Action DiT
→ trajectory
```

No test-time scorer or external teacher is added.

The difference is that the representations travelling through this bridge have been deliberately shaped for prediction, transfer and behavior discrimination.

## 4.5 Core-deletion test

This paper gives an unusually clean collapse test.

If all ReWorld representation objectives are removed while keeping the architecture, the method becomes the standard DriveLaW-style chained WAM trained with output-level objectives.

Therefore:

> ReWorld’s scientific contribution is primarily a **training/representation program on top of an existing world-to-action interface**, not evidence by itself for a new planning interface.

That does not make the contribution minor. It means the innovation and the architectural route should not be conflated.

---

# 5. SimWAM

## 5.1 Source note

No local raw-paper artifact was present on the working branch when Set B began. This reconstruction therefore uses the primary arXiv full text (`2608.07468`) rather than the older D01 mechanism skeleton.

This matters because the paper’s actual attention structure is more specific than the corpus summary.

## 5.2 Author-stated problem

SimWAM argues that WAM benefits do not require “imagine then act” at deployment.

Its explicit claim is:

> future-video generation can act purely as a training signal that teaches traffic dynamics to the planner; future scene generation need not remain in the real-time planning loop.

It additionally wants the video model to be replaceable and the action model independently scalable.

## 5.3 Two experts with no shared weights

SimWAM has:

- a pretrained video Diffusion Transformer expert;
- a lightweight action Diffusion Transformer expert.

The paper states that the two experts share no parameters and interact through a unified attention interface.

Both are trained with flow matching:

```text
L = L_FM_action + lambda * L_FM_video
```

## 5.4 Isolated attention is not Metis’s asymmetric attention

This distinction is essential.

SimWAM’s shared attention stream contains:

- current observation latents;
- future-frame latents;
- action tokens.

But the mask enforces:

```text
future-frame tokens -> may attend current observation
 action tokens      -> may attend current observation
future-frame tokens X action tokens   (mutually invisible)
```

So future action and future visual tokens do **not** directly attend one another.

The action expert learns from the current observation representation and joint training, but is structurally independent of future-frame tokens.

This differs from Metis, where future-video tokens are explicitly allowed to attend action tokens and the paper describes generation gradients backpropagating into the action expert through that directional dependency.

The two methods therefore should not be merged simply because both remove future generation at deployment.

## 5.5 What video co-training changes

The SimWAM paper reports:

```text
action-only: 86.6 PDMS
+ video co-training: 90.3 PDMS
+ RL: 91.5 PDMS
```

It interprets the large video-co-training gain as transfer of traffic-dynamics priors into the observation representation used by the action expert.

The paper also compares attention patterns and finds its isolated design best among the tested alternatives while retaining deployment independence from video generation.

However, a conservative audit should preserve one implementation-level question:

> given the stated “no shared weights” and mutual invisibility of future/action tokens, the exact parameter-level carrier by which the video objective enriches the action-used current-observation representation deserves code-level tracing before we make a stronger causal claim than the paper itself.

The ablation establishes that co-training matters. The exact gradient/parameter carrier should not be inferred beyond the documented shared-attention/current-observation interface without source tracing.

## 5.6 Deployment and RL

At inference, the video DiT is removed and the action expert directly predicts trajectories from the current observation representation, ego state and command.

SimWAM then performs a separate RL stage on the standalone action expert using NAVSIM compositional rewards.

This RL stage is important for final performance but is not necessary for the core WAM transfer claim:

- video co-training already improves the imitation planner from 86.6 to 90.3;
- RL subsequently improves it to 91.5.

Thus the paper combines two distinct programs:

1. video/world co-training as dynamics-prior transfer;
2. reward-based policy improvement after the video branch is gone.

## 5.7 Core-deletion test

Remove video co-training: the model becomes the action-only baseline and loses the main WAM improvement.

Remove the isolated mask / deployment-independence constraint: the defining “train with video, deploy direct action” proposition no longer holds cleanly.

Remove RL: SimWAM still retains its WAM identity and most of its paper-level architecture; performance drops but the central transfer mechanism remains.

---

# 6. Side-by-side reconstruction — facts only

| Question | Epona | DriveLaW | Metis | ReWorld | SimWAM |
|---|---|---|---|---|---|
| Planner-facing state at deployment | shared historical MST latent `F` | internal Video-DiT denoising state | current observation/context representation read by AE | same online Video-DiT state interface as DriveLaW, explicitly optimized | current observation representation read by standalone Action DiT |
| Must decoded future video be produced before action? | No | No | No | No | No |
| Must future-generation model computation remain on action forward path? | VisDiT no; MST yes | Yes, Video-DiT internal state is planner input | Future-video generation no | Yes, same as DriveLaW | Video DiT no |
| Training relation between world/video and action | shared MST + two specialized objectives | video pretraining then chained action conditioning; both branches update in planning stage | separate experts + asymmetric attention; future video sees action, action cannot see future video | DriveLaW bridge + explicit intermediate representation objectives | separate experts + isolated future/action visibility; joint losses via current-observation interface |
| Future-video output used at planning inference? | No | No | No | No | No |
| Main paper question | autoregressive diffusion WM with long video + planning | make generator internal latents directly useful to planning | get WAM learning benefits without future-video dependence/noise at inference | explicitly optimize the latent world→action representations | use video generation purely as training signal + direct planner (+ RL) |
| Collapse when paper-specific mechanism removed | shared-WM/planning thesis weakens toward trajectory-only model | collapses toward parallel/separate gen+plan | collapses toward ordinary action expert or unwanted joint-dependency variants | collapses to DriveLaW baseline | collapses to action-only DiT baseline |

This table is descriptive. It is **not** a five-way taxonomy.

---

# 7. What actually survives cross-paper comparison

## 7.1 The original “coupling strength” hypothesis is too crude

After independent reconstruction, these papers really do discuss a common broad scientific tension:

> how should knowledge learned by future/world generation become useful to an action planner?

But the answer is not a one-dimensional scale from “loose” to “tight.”

At least four different notions had previously been compressed into the word *coupling*:

1. **parameter/state sharing** — do world and action use one upstream representation or separate experts?
2. **forward dependency** — does action read a state produced inside future-generation computation?
3. **backward/gradient dependency** — can world/video losses reshape the action path, and through what edge?
4. **deployment dependency** — must world/future-generation computation remain active when action is produced?

Two papers can be “coupled” under one notion and “decoupled” under another.

Example:

- Metis deliberately decouples action from future-video tokens in the forward deployment path, but allows future-video learning to influence action during joint training through asymmetric information flow.
- DriveLaW keeps an explicit generator-internal state on the online action path.
- Epona shares an upstream temporal latent while allowing the visual output head to disappear at planning time.
- SimWAM uses separate experts and isolated future/action visibility, yet video co-training measurably improves the standalone planner.

Therefore a scalar “coupling axis” would likely repeat the project’s old error.

## 7.2 “Future video is disabled at inference” is nearly useless as a route criterion

Epona, Metis and SimWAM can all omit explicit future-video generation during planning inference.

Yet the learned/deployed programs are not the same:

### Epona

```text
history -> shared MST temporal latent F -> trajectory head
                            \
                             -> video head (optional at planning inference)
```

### Metis

```text
TRAIN:
current observation -> action
current observation + action -> future video
(video loss can shape action through asymmetric training dependency)

INFERENCE:
current observation -> action
```

### SimWAM

```text
TRAIN:
current observation -> action expert
current observation -> video expert
future action tokens X future video tokens
joint objectives / shared observation interface

INFERENCE:
current observation -> standalone action expert
```

So lifecycle facts matter, but they do not by themselves identify scientific sameness.

## 7.3 Epona vs DriveLaW: the disagreement is more precise than “parallel vs chained”

“Parallel vs chained” is a useful shorthand but still incomplete.

Epona’s action head already consumes a world-model temporal latent `F` that is jointly shaped by visual prediction.

DriveLaW’s stronger claim is narrower:

> the planner should consume the **internal representation of the video generator itself**, not merely a shared upstream temporal state that branches into specialized generation/planning heads.

This makes the disagreement about **which representation is trusted as the planner’s state**, not just whether modules are arranged in parallel boxes.

## 7.4 DriveLaW vs ReWorld: same bridge, different scientific problem

This pair is the cleanest evidence against treating every important paper as a new route.

ReWorld intentionally holds the DriveLaW-like architectural interface fixed and changes how the intermediate representations are trained.

Its deletion/collapse relation is explicit:

```text
ReWorld
- representation curriculum
= DriveLaW-style chained WAM
```

Therefore architecture-level mechanism and representation-learning innovation must be recorded separately.

## 7.5 Metis vs SimWAM: same deployment slogan, different training mechanism

Both can be summarized casually as:

> use video generation during training, remove it for action inference.

That summary is too coarse.

Metis makes future-video generation explicitly action-conditioned through asymmetric token visibility; the generation objective can backpropagate through the action-conditioned path.

SimWAM instead makes future-frame and action tokens mutually invisible and claims the video prior transfers through joint training around the common current-observation representation/interface.

This is exactly the kind of distinction that would disappear if the project prematurely created a “training-only world model” bucket.

## 7.6 No evidence yet for a single clean family tree

These five papers are scientifically related, but the relation is not a simple ancestry tree.

- DriveLaW explicitly argues against an Epona-like shared/parallel design.
- ReWorld is a direct methodological refinement of a DriveLaW-style interface.
- Metis and SimWAM both challenge the necessity/desirability of future-generation dependency at action inference, but choose different training information flows.
- Epona is neither simply “like DriveLaW” nor simply “like Metis/SimWAM”: it has a shared online temporal world state and optional specialized output heads.

The safer representation at this stage is a **local debate over world-knowledge transfer mechanisms**, not a route taxonomy.

---

# 8. A new audit lesson: forward graph alone is insufficient, training graph alone is insufficient

Set A warned that deployment topology alone can hide important training programs.

Set B makes the point sharper.

To understand how a world model changes planning, we may need both graphs:

```text
FORWARD / DEPLOYMENT GRAPH
what state does action actually read?

BACKWARD / LEARNING GRAPH
which world/future objectives can update which planner-facing parameters or representations?
```

For example, Metis is intentionally weakly connected in the forward inference graph but connected in the training/gradient graph.

DriveLaW is connected in both.

ReWorld additionally supervises the content of the transmitted representations.

SimWAM makes the future-token forward graph isolated, yet video co-training changes planner performance through the shared observation/training interface.

Epona shares an upstream state whose parameters are jointly shaped by both objectives.

This suggests a future audit language may need to preserve **forward causal dependence and learning causal dependence separately**.

This is an observation, not a new ontology axis.

---

# 9. Core-mechanism deletion test results

## Epona

Most identity-sensitive deletion:

```text
remove world/video prediction from joint training
```

Planning still exists, but the shared-world-model claim and matched planning gain weaken.

Removing VisDiT only at deployment does not destroy the planning mechanism.

## DriveLaW

Most identity-sensitive deletion:

```text
remove Video-DiT-internal-state -> Action-DiT conditioning
```

The method loses the paper’s central answer to the generation/planning disconnect.

## Metis

Most identity-sensitive deletion:

```text
remove asymmetric training/inference information-flow design
```

The method either becomes an ordinary isolated action planner or reintroduces future-generation dependency/interference that the paper is specifically designed to avoid.

## ReWorld

Most identity-sensitive deletion:

```text
remove explicit representation curriculum
```

The method collapses cleanly into the underlying DriveLaW-style chained WAM.

This is strong evidence that ReWorld’s novelty is about **how a bridge is trained**, not a new bridge.

## SimWAM

Most identity-sensitive deletion:

```text
remove video co-training while retaining Action DiT
```

The model becomes the action-only baseline; the reported PDMS drops from 90.3 to 86.6 before RL.

Removing RL reduces final performance but does not erase the video-to-action transfer thesis.

---

# 10. What this set invalidates from previous work

### Invalidated simplification 1

> If the video/future generator is not executed at deployment, the paper is essentially the same kind of training-only WAM.

False.

Epona, Metis and SimWAM all avoid explicit future-video generation at planning inference, but their planner-facing state, parameter sharing and training information flow differ substantially.

### Invalidated simplification 2

> Epona is simply “parallel heads”; DriveLaW is simply “chained heads.”

Too crude.

Epona already has a shared multimodal temporal world state used by planning. DriveLaW’s specific novelty is using **video-generator internal denoising representation** as planning state.

### Invalidated simplification 3

> Representation learning is always merely a training profile.

Too crude.

ReWorld shows that representation learning can be the paper’s central contribution even while the underlying forward bridge remains unchanged.

That does not make it a new route; it does mean it must remain visible in scientific reconstruction.

### Invalidated simplification 4

> “Coupling” can be represented by one scalar or one category.

Unsupported.

Forward visibility, shared state, parameter sharing, gradient flow and deployment retention are distinct relations.

---

# 11. Current conservative judgment

Set B does **not** justify a new ontology or a new list of CoreRoutes.

It does justify a better paper-reading protocol.

For future WAM papers involving world/video learning plus planning, reconstruct at minimum:

```text
A. planner-facing state at deployment
B. whether that state is upstream shared context, generator-internal state, predicted future output, or current observation representation
C. future/world output requirement at deployment
D. parameter sharing between world/action modules
E. forward token/state visibility between world and action
F. backward/gradient influence of world objectives on the action path
G. whether a paper changes the bridge itself or only the training of an existing bridge
H. whether post-training (RL/reward/scoring) is identity-defining or additive
```

These are **questions**, not accepted axes.

The next research step should continue paper-first reconstruction on another small set that stresses a different scientific problem, rather than immediately abstracting Set A and Set B into a universal framework.

---

# 12. Evidence limitations

- Epona, DriveLaW, Metis and ReWorld were reconstructed from local full-paper raw Markdown.
- SimWAM was reconstructed from the primary arXiv full text because the working branch did not contain a raw-paper artifact at audit start.
- This Set B audit is primarily full-paper (R2-style) evidence, not a systematic source-code trace of all five implementations.
- In particular, the precise parameter-level path by which SimWAM’s video objective enriches the action-used current-observation representation should be source-audited before making a stronger claim than the paper’s documented co-training/attention mechanism.
- No historical ontology file was modified.
