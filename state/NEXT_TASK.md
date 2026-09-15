# NEXT_TASK

## 唯一下一任务

> **Deep-read P0009 DriveLaW under the existing WAM reading stack, as the first paper in a broader literature-expansion phase. Do not promote research directions from the first 11 anchors.**

Canonical expansion plan:

```text
landscape/WAM_DEEP_READ_EXPANSION_QUEUE_V1.md
```

Current phase:

```text
broad WAM literature expansion     ACTIVE
research-direction convergence     PAUSED
candidate-problem promotion        PAUSED
method design                      FORBIDDEN
```

---

# Why DriveLaW is next

DriveLaW introduces a world→planning interface that is materially different from several first-wave anchors:

```text
DriveLaW-Video
→ internal / mid-denoising video latent
→ DriveLaW-Act diffusion planner
→ trajectory
```

The key question is not whether DriveLaW is strong, but exactly what planning information is transferred from the generative video model and how this differs from:

```text
Epona       shared historical F + sibling trajectory/visual branches
WorldDrive  world-model pretraining + teacher/distilled future representation
LAW         future latent as auxiliary training signal
Metis       action→world co-training + action-only deployment
Discrete-WAM shared world/policy backbone but planning-only task path
```

---

# Mandatory reconstruction

## 1. Source/version boundary

Resolve:

```text
canonical paper version
official repo attribution: xiaomiresearch/drivelaw
code-release state
paper↔code version relation
```

Lock a commit if implementation is available.

## 2. Exact representation path

Trace:

```text
historical observations
→ spatiotemporal VAE
→ Video DiT denoising states
→ selected latent / hidden feature h_t*
→ Action DiT conditioning
→ trajectory
```

Determine whether the planner consumes:

```text
encoded history latent
predicted future latent
mid-denoising hidden state
final denoised video latent
multiple denoising stages
```

Do not call all of these `future latent` interchangeably.

## 3. Temporal semantics

Separate:

```text
physical video time
video prediction horizon
diffusion / rectified-flow solver time t
selected denoising timestep t*
Action-DiT flow/denoising iteration
planning trajectory horizon
```

Use F07/F08/J08.

## 4. Training topology

Reconstruct the three-stage curriculum exactly:

```text
what is trained first?
what is frozen?
what is fine-tuned?
when does planner see video-model latent?
does planner loss update the video generator?
does video-generation loss update the planner?
```

This is critical because the paper explicitly motivates its training strategy as avoiding gradient interference.

## 5. Inference graph

Determine exactly what runs during planning inference:

```text
VAE encoder?
Video DiT partial denoising?
full future video generation?
video decoder?
Action DiT?
```

Key question:

> Does planning require generating a future video, or only extracting an internal generative representation?

## 6. Coupling direction

Force separate answers:

```text
video/world → planner forward information flow?
planner/action → video world conditioning?
planner loss → video model gradient?
video loss → planner gradient?
```

Do not equate shared latent interface with bidirectional coupling.

## 7. Evidence / attribution

Find strongest matched controls for:

```text
video-generator latent vs BEV/VLM/current visual feature
which denoising timestep is best
pretrained video prior contribution
three-stage curriculum contribution
world-generation objective contribution
Action-DiT contribution
```

Do not attribute final NAVSIM score to `world model` as one monolithic factor.

## 8. Generation fidelity → planning

The paper reports strong FID/FVD and planning results. Check whether it actually demonstrates:

```text
better video fidelity
→ better planning
```

or only that both are strong in the same model.

## 9. Deployment compute

Record:

```text
number of active video denoising steps during planning
Action-DiT steps
FPS / latency
whether RGB decoding is skipped
whether full future video synthesis is skipped
```

## 10. Full Ontology V1.3 projection

Force-fill A–P including explicit:

```text
ABSENT
NOT REPORTED
NOT EVALUATED
NOT APPLICABLE
SOURCE-UNVERIFIED
```

if needed.

---

# Required immediate cross-paper comparisons

For every major DriveLaW mechanism, compare immediately:

```text
DriveLaW vs Epona
DriveLaW vs WorldDrive
DriveLaW vs LAW
DriveLaW vs Metis
DriveLaW vs Discrete-WAM
```

Especially answer:

```text
Is DriveLaW really more tightly coupled than Epona?
Is its video latent an online future object or a generative feature extractor?
Is this closer to WorldDrive representation inheritance or online future use?
Does the planning loss shape the video model?
What remains active at deployment?
```

---

# Required artifacts

After the deep read create at minimum:

```text
papers/deep_analysis/P0009_DRIVELAW_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_DRIVELAW_AUDIT.md
landscape/P0009_DRIVELAW_ONTOLOGY_PROJECTION.md
```

Extend the cross-paper matrix only after the mechanism is stable.

If source code is public and sufficiently complete, perform a commit-locked source audit rather than relying only on README claims.

---

# After DriveLaW

Current core queue:

```text
P0012 DA-WAM
P0002 SafeDrive
P0005 RiskWorld
P0007 DriveReward
```

Then proceed into simulation/reactivity/evaluation and WAM+VLA control waves defined in the expansion queue.

---

# Guardrail

Do not use DriveLaW to revive any parked research candidate.

This phase asks:

```text
What does the field contain?
How do mechanisms differ?
What evidence supports them?
```

not:

```text
What should our method be?
```
