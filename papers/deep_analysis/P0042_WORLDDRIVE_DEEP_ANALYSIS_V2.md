# P0042 WorldDrive — Dimension-first Deep Analysis v2

> Paper: **Bridging Scene Generation and Planning: Driving with World Model via Unifying Vision and Motion Representation**  
> Purpose: re-project the existing paper+code audit into the shared LAW/WoTE/Epona dimension framework; separate generic pretraining, TA-DWM-specific representation inheritance, candidate generation, future-representation distillation, reward learning and final action selection.  
> Primary evidence: `papers/raw_md/P0042_WorldDrive/P0042_WorldDrive.raw.md`; `audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md`; official-code audit recorded in that audit (`TabGuigui/WorldDrive@c375ee1e1fe86ace175609db1ed90fd6db89673b`).

---

# 0. Executive verdict

WorldDrive is best classified as a **two-level hybrid WAM planner**:

```text
LEVEL 1 — predictive/generative representation inheritance
trajectory-aware video world model (TA-DWM)
→ learn driving-specialized vision + motion representations
→ transfer/freeze them into a downstream candidate planner

LEVEL 2 — distilled candidate consequence evaluation
base planner → top-K trajectory candidates
→ frozen heavy TA-DWM provides candidate-conditioned future latent TEACHER during FAR training
→ lightweight Future-aware Rewarder learns a candidate-conditioned future representation
→ PDMS/oracle preference supervision teaches ranking

DEPLOYMENT
current scene + candidate trajectory
→ lightweight distilled future representation
→ scalar future-aware reward
→ argmax trajectory
```

The crucial negative statement is equally important:

```text
inference ≠ candidate → full TA-DiT diffusion rollout/video → reward
```

The heavy generative world model is removed from the deployed candidate-evaluation path. What survives online is a **distilled surrogate of the world model's foresight**.

Therefore WorldDrive is neither:

- LAW-style training-only predictive regularization;
- Epona-style direct generative policy from a shared historical latent;
- WoTE-style deployment of the learned transition/world model itself for recurrent candidate rollout.

It combines a representation-pretraining role with a distilled online consequence/value role.

---

# 1. The single phrase “world model improves planning” hides at least five mechanisms

WorldDrive forces the full planning stack to be decomposed as:

```text
A. generic video prior
B. TA-DWM driving-specific vision representation
C. TA-DWM driving-specific motion representation
D. multi-modal candidate planner + first-stage scorer/refiner
E. FAR distilled future representation + preference ranker
```

These mechanisms have different supervision, parameters, deployment status and causal evidence.

A scientifically valid attribution cannot collapse them into one `WM gain`.

The paper's strongest internal decomposition is:

```text
No pretrained representation                  31.4 PDMS
+ CogVideoX 3D VAE pretrain                   84.9
+ TA-DWM vision representation                85.8
+ TA-DWM motion representation                86.9
+ trajectory-only extra rewarder              87.0
+ distilled future representation in FAR      88.1
```

This immediately yields a central conclusion:

> The huge `31.4 → 84.9` jump is a generic pretrained visual prior effect. The evidence specifically attributable to TA-DWM representation learning is the smaller `84.9 → 85.8 → 86.9` increment; the online distilled-future contribution is isolated more cleanly by `87.0 → 88.1`.

WorldDrive is valuable precisely because the paper contains enough step-wise ablations to stop us from narrating all gains as one monolithic world-model effect.

---

# 2. Phase 1 TA-DWM: what representation is actually learned?

## 2.1 Visual side

Historical driving video is encoded by a pretrained/frozen CogVideoX 3D Causal VAE, then adapted to driving by a learnable visual adapter:

```text
historical frames x
→ frozen 3D Causal VAE
→ generic video latent
→ driving-domain visual adapter
→ f
```

`f` is not merely a rendering latent. It later becomes a transferred planner representation.

### Cross-paper dimension: representation origin stack

Do not label WorldDrive simply as `video latent`.

Its planner-facing state has a lineage:

```text
large generic video prior
→ driving-specific predictive adaptation
→ frozen transferred planning representation
```

This creates a dimension that LAW/WoTE did not expose strongly enough:

> **How much of a WAM representation comes from generic foundation pretraining versus task-specific future modeling?**

The paper provides unusually strong evidence that this distinction matters quantitatively.

## 2.2 Motion side

WorldDrive builds a trajectory vocabulary:

```text
V ∈ R^{N × F × 3}
N = 256 on NAVSIM
```

For expert trajectory `Y`, it retrieves top-K anchors and encodes coarse anchor geometry plus residual motion:

```text
c = E_a(V_K) + E_o(Y - V_K)
```

Thus the motion representation explicitly decomposes:

```text
coarse motion mode / prior
+
fine continuous correction
```

The same motion encoding family is deliberately reused by the downstream planner.

### Cross-paper dimension: representation identity across tasks

Epona shares a history representation `F` between visual and trajectory branches.
WorldDrive instead makes **motion representation itself inheritable** across generation and planning.

We therefore need separate fields for:

```text
shared visual representation?
shared motion/action representation?
shared parameters?
transferred parameters?
frozen after transfer?
```

The broad label `unified representation` is insufficient.

---

# 3. TA-DWM dynamics: trajectory-conditioned generative teacher

Ground-truth future video is encoded into latent target `z_0`; diffusion noise is added; TA-DiT predicts noise conditioned on:

```text
historical visual representation f
+ diffusion timestep t
+ motion representation c
```

Formally, the learned object is approximately:

```text
p(future visual latent | history latent, trajectory condition)
```

This establishes **motion sensitivity** and controllable future generation.

The paper's motion-sensitivity analysis shows future representation similarity changes with trajectory geometric deviation, supporting that motion conditioning is not ignored.

However:

```text
candidate-conditioned generated futures
≠
behaviorally validated real counterfactual futures
```

The model is trained from logged video/expert motion and later extrapolated to non-expert/candidate trajectory conditions. Qualitative counterfactual generations demonstrate controllability/plausibility, but not a ground-truth reactive response oracle for every unexecuted action.

### Provisional counterfactual placement

WorldDrive needs three separate placements:

```text
model output form:          CF2-ish — multiple candidate-conditioned futures can be produced
WM training supervision:   mainly factual logged future under observed/expert motion
planning value supervision: NAVSIM/PDM oracle preference semantics
```

The three must not be collapsed.

---

# 4. Representation inheritance: the first path from WM to planning

After TA-DWM training, WorldDrive transfers vision/motion modules into the planner and freezes them.

Paper/code audit confirms transfer of components including:

```text
visual adapters
trajectory encoder
TA-DiT-related visual/motion projection modules used by planner
```

The planner is therefore not trained from scratch in an unrelated latent space.

## 4.1 Scientific interpretation

The causal hypothesis is:

```text
future-generation task
→ shapes vision/motion representation
→ transferred representation is more planning-useful
```

This is closer to LAW/Epona's representation-shaping role than to WoTE's online rollout role.

## 4.2 Strongest evidence

Planner representation ablation:

```text
none                           31.4
CogVideoX VAE                  84.9
+ TA-DWM vision                85.8
+ TA-DWM motion                86.9
```

Interpretation:

- generic video prior is dominant;
- TA-DWM vision specialization contributes +0.9;
- TA-DWM motion specialization contributes +1.1;
- the paper therefore supports both generic-pretraining and future-modeling-specific representation effects, but at very different magnitudes.

### New dimension: attribution baseline ladder

For representation-transfer papers, record the full ladder:

```text
random/no pretrain
foundation visual pretrain
future-model pretrain
motion-aware future-model pretrain
planner fine-tuning
```

Without this ladder, a WAM can be credited for gains actually caused by a generic foundation model.

---

# 5. Multi-modal Planner: WorldDrive already has a strong decision system before FAR

WorldDrive treats all 256 anchor embeddings as motion queries:

```text
Q_a = E_a(V)
Q_p = D_plan(Q_a, [f,e], [f,e])
```

where ego state includes velocity, acceleration and driving command.

For each anchor, the base planner predicts:

```text
imitation score
simulation-related scores
trajectory residual/offset
```

Then it selects top-K candidates by combined score and refines them.

This matters because FAR does not operate on arbitrary raw trajectories; it receives candidates already shaped by:

```text
trajectory vocabulary
+ scene-conditioned cross-attention
+ imitation supervision
+ simulator-reward supervision
+ offset refinement
+ top-K pruning
```

### Cross-paper consequence

Candidate quality and future evaluator quality must be separate dimensions.

WorldDrive exposes an additional axis beyond WoTE:

> **At what stage is branching pruned before expensive consequence reasoning?**

WoTE can evaluate a large candidate set with a compact BEV world model. WorldDrive instead uses a first-stage planner/scorer to reduce 256 anchors to top-K before future-aware re-ranking.

This is a classic coarse-to-fine planning architecture hidden inside an end-to-end/WAM framing.

---

# 6. FAR training: two teachers supervise two different scientific objects

This is the most important part of WorldDrive.

For each top-K candidate `k`, FAR learns two things from two different oracles.

## 6.1 Consequence teacher = frozen TA-DWM

The heavy world model produces candidate-conditioned future latent:

```text
z^k = frozen TA-DWM(candidate k, current history)
```

The lightweight Future-scene Decoder predicts:

```text
z_hat^k = D_scene(Q_s, [f,c^k], [f,c^k])
```

and aligns via:

```text
L_align = E_k ||z_hat^k - SG(z^k)||²
```

Thus the lightweight future representation is **teacher-generated**, not directly supervised against a real observed future for each candidate.

## 6.2 Value teacher = oracle driving score / PDMS semantics

The candidate trajectory representation queries the distilled future representation:

```text
h_f^k = D_future(c^k, z_hat^k, z_hat^k)
→ scalar r_k
```

Candidate ranking is trained using Bradley-Terry preference pairs constructed from an oracle driving score.

Therefore FAR learns:

```text
what future feature should look like?      ← TA-DWM teacher
which candidate should rank higher?        ← driving-score/value oracle
```

### New dimension: teacher-role factorization

This is more precise than WoTE's `state truth vs value truth` split.

For distillation-based WAMs, record:

```text
consequence teacher
value teacher
policy teacher
representation teacher
```

These teachers can be different systems with different biases.

WorldDrive's consequence teacher is a learned generative model; its value teacher is an external planning oracle.

---

# 7. Distillation changes the deployment object

WorldDrive is the clearest anchor showing why `uses world model online?` is too coarse.

Training graph:

```text
candidate
 ├─→ frozen heavy TA-DWM → teacher future latent z^k ─┐
 └─→ lightweight FAR     → student future latent z_hat^k
                                                │
                                      L_align ──┘

student future latent + candidate
→ scalar reward
← PDMS/oracle preference target
```

Inference graph:

```text
current visual tokens + candidate trajectory embedding
→ lightweight future-scene queries/decoder
→ distilled future representation
→ candidate-conditioned reward
→ argmax
```

No heavy diffusion denoising is invoked in the audited FAR inference path.

### New dimension: future-knowledge transformation lifecycle

A useful WAM taxonomy must describe not only where future prediction appears, but how predictive knowledge changes across stages:

```text
LAW:
full auxiliary predictor during training
→ future output not consumed for action selection

Epona:
visual future branch during joint training
→ visual branch can be disabled for planning

WoTE:
learned compact world transition
→ remains as online recurrent consequence model

WorldDrive:
heavy generative future teacher
→ distilled compact candidate-conditioned future surrogate
→ online evaluator
```

This dimension is likely fundamental.

---

# 8. What exactly is “future-aware” at inference?

The online FAR future representation is not:

```text
an RGB future
an explicitly decoded semantic BEV
full TA-DiT latent diffusion rollout
```

It is a learned compact representation produced from:

```text
current visual tokens + candidate trajectory embedding
```

and trained to match a frozen world-model latent.

Hence its semantics are **teacher-defined and planning-distilled**.

### New dimension: explicitness / observability of imagined consequence

We should distinguish:

```text
explicit decoded world consequence
structured semantic consequence
opaque but directly predicted future latent
teacher-distilled future latent surrogate
value-only latent with no consequence target
```

WorldDrive occupies the fourth category.

This matters for interpretability and for failure diagnosis: a bad final reward can arise from the teacher, distillation, future decoder, value head, candidate set or oracle labels.

---

# 9. FAR is not “just a better scorer” — but it is also not pure world-model evidence

The strongest matched ablation is:

```text
base planner                      86.9 PDMS
+ trajectory feature rewarder     87.0
+ trajectory + future feature     88.1
```

This is strong evidence against the simplest explanation:

```text
“adding any second-stage rewarder causes the gain”
```

because trajectory-feature-only rewarder gives only +0.1 while future feature adds another +1.1.

However, it still does not establish:

```text
better physical world-model fidelity → better ranking
```

because FAR simultaneously depends on:

```text
TA-DWM teacher representation
+ lightweight student distillation quality
+ PDMS preference targets
+ candidate trajectory embedding
+ reward head
```

The +1.1 is best called **distilled future-representation value for ranking under this oracle/training setup**, not pure proof of physical dynamics fidelity.

---

# 10. Candidate-set quality remains an independent bottleneck

Top-K ablation:

```text
K=1    86.9
K=3    87.9
K=5    88.1
K=10   87.6
```

This shows a non-monotonic trade-off:

```text
more candidates
→ more behavioral coverage
but eventually
→ more low-quality distractors / harder ranking
```

The best-of-6 oracle result gives a separate signal:

```text
normal deployed score    ~88.1 (paper setting)
best-of-6 oracle         93.6
```

These numbers are not directly identical experimental controls in every respect, but conceptually they expose a **candidate-quality vs ranking gap**.

### New dimension: candidate-set oracle ceiling

Whenever available, record:

```text
planner achieved score
oracle best-candidate score
ranking gap = candidate support available but not correctly selected
```

This is particularly valuable for WAM research because it tells us whether the next bottleneck is better imagination, better value estimation, or simply better candidate generation.

---

# 11. WorldDrive vs WoTE: same high-level loop, different location of dynamics cost

Both eventually implement:

```text
candidate → future-informed representation → reward → select
```

But the dynamics object is different.

## WoTE

```text
candidate
→ deployed compact BEV transition model
→ recurrent future BEV sequence
→ reward model
→ select
```

Properties:

- explicit learned transition stays online;
- multi-step recurrent future sequence;
- structured BEV supervision;
- many candidate branches are processed in parallel.

## WorldDrive

```text
candidate
→ deployed lightweight distilled future decoder
→ compact teacher-aligned future representation
→ reward
→ select
```

Properties:

- heavy world model only teaches offline;
- no full diffusion rollout online;
- consequence surrogate can be one-shot/lightweight;
- top-K candidates are pruned before second-stage evaluation.

### Core distinction

WorldDrive moves the expensive dynamics reasoning into **teacher precomputation/distillation**, whereas WoTE makes the learned transition itself efficient enough to deploy.

This gives two different engineering/scientific answers to the same WAM problem:

```text
How can multiple candidate futures influence real-time action selection?
```

---

# 12. WorldDrive vs LAW/Epona: representation shaping is only half of the story

## LAW

```text
current planner latent + single predicted action
→ auxiliary factual future-latent prediction
→ shared representation improved
future output not used for deployed ranking
```

## Epona

```text
shared historical latent F
→ trajectory generative branch
→ visual future generative branch
joint visual loss improves F
visual future not required by planning inference
```

## WorldDrive Phase 1

```text
trajectory-aware visual generation
→ vision + motion representations specialized
→ representations transferred/frozen into planner
```

This is in the same broad family: **future modeling improves representation before online decision**.

But WorldDrive then adds a second mechanism:

```text
candidate-specific future knowledge
→ distilled online
→ directly changes final action selection
```

So WorldDrive bridges the two previously separated roles of world modeling:

```text
representation teacher
+
consequence-informed evaluator
```

This hybrid role is its most important position in the emerging ontology.

---

# 13. Training-stage topology becomes a first-class dimension

WorldDrive uses a staged curriculum:

```text
Stage 1
train TA-DWM

Stage 2A
freeze transferred encoders
train multi-modal planner

Stage 2B
freeze planner + frozen TA-DWM teacher
train FAR
```

The final planner is therefore not an end-to-end jointly optimized monolith in the optimization sense, even though its deployed sensor-to-action graph is end-to-end.

### New dimension: optimization topology

Record separately:

```text
joint end-to-end training
sequential pretrain→freeze→head training
teacher/student distillation
alternating optimization
RL fine-tuning
```

This matters because “end-to-end autonomous driving” describes the input/output interface, not necessarily the training graph.

---

# 14. Evaluation regimes and evidence boundaries

WorldDrive reports three planning regimes:

```text
nuScenes        → open-loop trajectory metrics
NAVSIM          → PDM/non-reactive data-driven planning evaluation in the canonical benchmark semantics
NAVSIM-v2       → reactive-traffic + pseudo-closed-loop evaluation
```

These should not be merged into one `closed-loop evidence` label.

The strongest claims supported are:

1. transferred TA-DWM-specific representations improve a strong pretrained planner incrementally;
2. candidate-conditioned distilled future features improve ranking beyond trajectory features alone;
3. the deployment design is much cheaper than full future-generation planners in the reported latency comparison.

Still not established:

1. behaviorally correct counterfactual response for all alternative ego interventions;
2. monotonic link from video-generation fidelity to planning quality;
3. that FAR improvement comes from physically accurate dynamics rather than a useful teacher feature combined with PDMS preference learning;
4. that the same distilled reward generalizes unchanged outside the NAVSIM/PDM value semantics.

---

# 15. Compute frontier: WorldDrive changes *where* computation happens

Reported full WorldDrive planning pipeline on A800:

```text
encoders   17.9 ms
planner    18.9 ms
FAR        16.2 ms
total      53 ms
```

Compared paper numbers:

```text
PWM without future frame forecast   570 ms
PWM with future frame forecast      850 ms
WorldDrive                           53 ms
```

The scientific point is not only that WorldDrive is faster. It relocates computation:

```text
expensive generative consequence computation
→ training-time teacher

cheap candidate-conditioned surrogate
→ deployment
```

### New dimension: offline/online compute allocation

For deployment-oriented WAM comparison, record:

```text
foundation pretraining compute
WM pretraining compute
teacher-generation/distillation compute
planner training compute
online encoder compute
online dynamics/imagination compute
online evaluator compute
```

A method can be real-time online while paying very large offline teacher/pretraining cost.

---

# 16. New/refined dimensions revealed by WorldDrive

The following are provisional `WD-Dxx` discovery IDs.

| ID | Dimension | WorldDrive position | Why it matters |
|---|---|---|---|
| WD-D01 | **Representation origin stack** | generic CogVideoX prior → TA-DWM vision/motion specialization → planner transfer | Prevents assigning generic foundation gains to WM-specific future modeling. |
| WD-D02 | **Visual vs motion representation inheritance** | both inherited; motion has anchor+residual structure | `shared representation` must be split by modality/function. |
| WD-D03 | **Transfer policy** | transferred modules frozen in planner stage | Fine-tuned vs frozen transfer changes what evidence means. |
| WD-D04 | **Cross-task representation identity** | same trajectory encoder/motion space intentionally spans generation and planning | Stronger than vague feature reuse. |
| WD-D05 | **Optimization topology** | WM pretrain → frozen planner transfer → frozen-teacher FAR distillation | Training graph differs from deployed graph. |
| WD-D06 | **First-stage vs second-stage decision architecture** | base candidate scorer/refiner → top-K → FAR re-ranker | Consequence reasoning operates only after coarse pruning. |
| WD-D07 | **Branch-pruning location** | 256 anchors narrowed to top-K before future-aware reasoning | Controls compute and candidate coverage. |
| WD-D08 | **Candidate oracle ceiling / ranking gap** | best-of-6 oracle substantially above deployed score | Separates candidate-support bottleneck from ranking bottleneck. |
| WD-D09 | **Consequence teacher type** | frozen learned generative TA-DWM | Different from factual future, simulator state, or semantic label. |
| WD-D10 | **Value teacher type** | PDMS/oracle preference ordering | Consequence truth and utility truth originate from separate systems. |
| WD-D11 | **Teacher error inheritance** | student future representation is trained to imitate TA-DWM latent | Distillation transfers teacher inductive bias/errors, not ground-truth physical correctness. |
| WD-D12 | **Future-knowledge lifecycle** | heavy generated future → distilled compact future → online reward | Goes beyond online/offline yes/no. |
| WD-D13 | **Consequence explicitness** | opaque teacher-aligned future feature, not decoded future at deployment | Affects interpretability, verification and cost. |
| WD-D14 | **Teacher/student deployment mismatch** | teacher heavy diffusion; student lightweight query decoder | Same semantic role implemented by different model classes across train/test. |
| WD-D15 | **Future-feature bottleneck** | learnable Future Scene Queries compress planning-relevant teacher info | Explicit information bottleneck may discard visually irrelevant detail. |
| WD-D16 | **World-model vs reward-model attribution** | traj-only scorer +0.1; future feature adds ~+1.1 | Stronger isolation than headline SOTA. |
| WD-D17 | **Generic prior vs WM-specific attribution** | 31.4→84.9 generic prior; 84.9→86.9 TA-DWM-specific | Essential causal accounting. |
| WD-D18 | **Offline/online compute allocation** | expensive TA-DWM teacher offline; FAR online | Real-time inference can hide large offline imagination cost. |
| WD-D19 | **Distillation objective semantics** | latent alignment + BT preference ranking | Student learns both consequence representation and decision value. |
| WD-D20 | **Decision-stage future semantics** | candidate-specific compact future feature directly changes final argmax | Unlike LAW/Epona, future information is causally consumed online. |
| WD-D21 | **Future fidelity–decision link evidence** | not directly isolated | Good teacher/generation metrics do not prove the specific property driving planning gain. |
| WD-D22 | **Action-support extrapolation of teacher** | TA-DWM trained primarily on logged/expert motion, later used for alternative candidates | Candidate-conditioned output can exceed supervised action support. |
| WD-D23 | **Counterfactual supervision gap** | alternative candidate future latents are teacher-generated rather than matched real alternative futures | Candidate-specific imagination is not real intervention evidence. |
| WD-D24 | **Coarse-to-fine utility computation** | base imitation/simulation score then future-aware scalar re-ranking | Utility is composed across stages, not one evaluator. |
| WD-D25 | **Deployment future-object type** | distilled latent surrogate | Separate from video, BEV rollout, direct policy hidden state and auxiliary training target. |

---

# 17. Four-paper mechanism map after WorldDrive

| Axis | LAW | WoTE | Epona | WorldDrive |
|---|---|---|---|---|
| primary WM role | training-time predictive representation shaping | online candidate consequence model | shared representation + direct generative trajectory policy | representation inheritance + distilled online future-aware ranking |
| action branching | single planner trajectory | many candidates | stochastic direct policy; no explicit scored candidate bank | 256 base anchors → top-K FAR candidates |
| deployed future object | none used for selection | recurrent future BEV sequence | visual future optional/off for planning | distilled candidate-conditioned future latent |
| heavy generator online? | no | no heavy visual generator; compact BEV WM online | TrajDiT online; VisDiT optional/off for planning | no; TA-DiT teacher removed online |
| consequence→value separation | absent | explicit WM → Reward Model | absent in planning path | distilled future decoder → scalar rewarder |
| representation transfer | shared within same host planner | not primary mechanism | joint shared latent | explicit WM→planner frozen inheritance |
| value oracle | N/A | imitation + simulator metrics | trajectory likelihood/data | PDMS preference + base imitation/simulation heads |
| strongest causal evidence | ± latent prediction/action condition | evaluator ± future states | trajectory-only vs joint visual+trajectory training | pretrain ladder + traj-only rewarder vs future-feature FAR |
| key unresolved issue | no online consequence use | non-reactive supervision semantics | no visual-future→action feedback | teacher-generated counterfactual futures + oracle-value dependence |

---

# 18. Updated historical hypothesis

After LAW, WoTE, Epona and WorldDrive, the field cannot be ordered along one axis such as `more world modeling`.

At least four independent transitions are visible:

```text
Transition A — future as representation supervision
LAW / Epona-like effect

Transition B — world/action representation becomes reusable across tasks
WorldDrive Phase 1

Transition C — future becomes a deployed decision variable
WoTE / WorldDrive FAR

Transition D — expensive world imagination is compressed into a decision-oriented surrogate
WorldDrive distillation
```

WorldDrive is especially important because it occupies **B + C + D simultaneously**.

This makes it a hybrid bridge, not merely another latent world model.

---

# 19. Strongest evidence, strongest alternative explanation, falsification experiment

## Strongest evidence

Two matched ladders:

```text
Representation:
84.9 generic prior
→ 85.8 + TA-DWM vision
→ 86.9 + TA-DWM motion

Decision:
86.9 base planner
→ 87.0 + trajectory-only rewarder
→ 88.1 + distilled future feature
```

Together they separately support representation inheritance and future-informed re-ranking.

## Strongest competing explanation

For representation gains:

```text
better generic/transfer representation
rather than learned physical foresight itself
```

For FAR gains:

```text
a teacher-shaped candidate embedding + PDMS preference learner
rather than physically accurate counterfactual dynamics
```

## Best next falsification experiment

A clean experiment would keep candidate set, planner, reward head and PDMS ranking labels fixed while changing only the future teacher:

```text
A. no future teacher
B. random/untrained teacher latent
C. current-scene teacher with matched dimensionality
D. factual-future predictive teacher
E. action-conditioned TA-DWM teacher
F. simulator/reactive oracle future if available
```

Then compare:

```text
ranking accuracy
PDMS/EPDMS
counterfactual sensitivity
out-of-support candidate generalization
```

This would test whether WorldDrive's gain specifically requires **action-conditioned predictive dynamics**, rather than merely an additional high-capacity privileged teacher representation.

---

# 20. One-sentence judgment

WorldDrive's real contribution is not “using generated future videos for planning”; it is a carefully staged transfer-and-distillation architecture that first **inherits vision/motion representations learned through trajectory-conditioned generation**, then **compresses the heavy world model's candidate-specific foresight into a lightweight future representation that directly re-ranks trajectories online**—with strong matched evidence for both effects, but without proving that the distilled benefit is equivalent to physically correct reactive counterfactual simulation.
