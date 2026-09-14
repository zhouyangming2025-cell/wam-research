# PHASE_B_WAVE3_AUTOJEPA_AUDIT — Continuous Intent as a Planning-Oriented Predictive State

Last updated: 2026-09-14

Status: **PRIMARY-TEXT FIRST PASS COMPLETE**

Role in Wave 3: test whether a world model can deliberately discard most future-world content and predict only a compressed future representation tied directly to ego action.

Comparative baseline:

```text
OccWorld  — richer reconstruction can be worse for forecast/planning
LAW       — future prediction can help as auxiliary representation shaping; longer horizon is not monotonic
DriveLaW  — planner quality depends strongly on which generative latent is exposed online
```

Auto-JEPA's central move is different from all three:

```text
future target = latent representation of the FUTURE EGO TRAJECTORY itself
```

rather than future image / occupancy / scene latent.

---

## 1. Exact problem and historical role

Auto-JEPA argues that planning does not need a complete future-world reconstruction. Dense video/occupancy/scene prediction spends capacity on future content that may not affect the ego decision. The proposed alternative is to predict a continuous future-driving-intent latent aligned with the future ego trajectory.

Historical transition:

```text
dense future-world reconstruction
→ planning-oriented compressed predictive target
→ target is future ego-motion latent
```

This is not simply `latent WM instead of pixel WM`; it changes **what counts as the future state**.

---

## 2. Stage 1 — trajectory target space

Ground-truth future trajectory:

```text
Y ∈ R^(8×2)
= eight future ego waypoints
```

A trajectory autoencoder learns:

```text
Y
→ E_traj
→ Z+ ∈ R^(8×1024)
→ D_traj
→ reconstructed Y
```

The trajectory autoencoder is trained with geometry/dynamics losses covering waypoint position, endpoint, velocity, and acceleration.

After this stage:

```text
trajectory decoder D_traj = DISCARDED
trajectory encoder E_traj = FROZEN
```

The frozen trajectory encoder defines both:

1. the target latent `Z+` used to train visual intent prediction;
2. the latent representation of all trajectories stored in the retrieval memory.

This is important: the target latent and executable candidate memory occupy the **same learned trajectory space**.

---

## 3. Stage 2 — visual intent prediction

Inputs:

```text
I = four historical front-camera frames
H = four historical ego positions
C = route command
```

Visual path:

```text
I
→ frozen V-JEPA 2 visual encoder E_vis
→ visual tokens F_v
```

Additional encoders:

```text
H → history encoder → F_h
C → command encoder → F_c
```

A 24-block Transformer predictor receives these features and outputs:

```text
Zhat ∈ R^(8×1024)
```

The eight tokens match the temporal organization of the future trajectory latent `Z+`.

Training optimizes alignment in the frozen trajectory-latent space using:

```text
feature Smooth-L1 alignment
+ token-wise cosine alignment
+ batch-level InfoNCE
```

The visual encoder and target trajectory encoder remain frozen while the history encoder, command encoder and JEPA predictor are optimized.

### Important correction to the generic word “JEPA”

There is no moving target encoder trained by EMA in the driving stage described here. The target is a **frozen trajectory encoder learned beforehand**. Thus the operational target is not a future scene embedding from a second visual encoder; it is a pre-established ego-trajectory latent.

---

## 4. What future information is intentionally preserved and discarded?

Preserved by design:

```text
future ego-motion geometry
future trajectory temporal structure
velocity / acceleration information encoded by trajectory pretraining
scene information insofar as it changes the appropriate ego future
route-conditioned maneuver preference
```

Not explicitly preserved/predicted:

```text
future RGB appearance
future occupancy field
per-agent future trajectories
future semantic map
explicit interaction graph
full environment state
```

This is the most aggressive planning-oriented compression in the current atlas: the world model does not try to preserve environment future state for its own sake; it preserves only enough current-scene information to predict the ego-motion latent.

Scientific consequence:

```text
Auto-JEPA predicts a DECISION-SUFFICIENT TARGET hypothesis,
not a full environment-transition target.
```

That hypothesis still requires evidence; the architecture alone does not prove sufficiency.

---

## 5. Inference path — the predicted latent survives and becomes a retrieval key

This is where Auto-JEPA differs from LAW and ViDAR.

At inference:

```text
current scene/history/route
→ predicted intent Zhat
→ cosine retrieval from fixed trajectory memory
→ Top-K executable trajectory candidates
→ scene-conditioned scorer
→ drivable-area feasibility gate
→ final trajectory
```

Memory:

```text
110,335 ground-truth trajectory–latent pairs
```

Final configuration retrieves:

```text
Top-300 candidates
```

Therefore:

```text
future predictive representation survives at inference = YES
```

but it is not a predicted world state used to simulate consequences. It is a **query into an action memory**.

This creates a fourth Wave-3 interface type:

```text
PREDICTIVE LATENT → NONPARAMETRIC ACTION RETRIEVAL → SCORING
```

---

## 6. What exactly is “world-model-like” here?

Auto-JEPA calls itself a latent world model because it learns a mapping from current observations/history/route to a future latent state. But that future latent is not an environment state; it is the latent of future ego motion.

So its transition model is effectively:

```text
(observation, ego history, route)
→ future ego-intent latent
```

not:

```text
(world state, action)
→ next world state
```

and not:

```text
candidate action_i
→ candidate-specific future world_i
```

Hence Auto-JEPA sits at the boundary between:

```text
planning-oriented predictive representation
and
world modeling in the classical environment-dynamics sense
```

This boundary should remain explicit rather than being resolved by terminology alone.

---

## 7. Component evidence — what actually drives 91.3 PDMS?

The full planner reaches:

```text
91.3 PDMS on NAVSIM v1
89.1 EPDMS on NAVSIM v2 with the updated official evaluator
```

But the headline score combines several mechanisms:

```text
intent predictor
trajectory memory
candidate retrieval
scene-conditioned scorer
drivable-area gate
```

The component ablation is unusually informative.

Using the same Top-300 memory:

```text
fixed codebook medoid instead of predicted intent  52.6 PDMS
intent retrieval + gate, no scorer                87.6
intent + scorer, no gate                          91.0
full intent + scorer + gate                       91.3
```

The appendix clarifies that these are conditional ablations rather than a simple sequential-addition chain:

```text
scorer contributes about +3.7 PDMS when gate retained
gate contributes about +0.3 PDMS when scorer retained
```

Candidate-pool sensitivity:

```text
K=1    87.6
K=200  91.1
K=300  91.3
```

Thus Auto-JEPA's final performance is not attributable to the intent latent alone. Strong candidate ranking matters materially, and much of the gain from K=1 to K=200 comes from having a larger candidate pool plus selection.

---

## 8. Strongest evidence that compression is planning-oriented

The paper's most relevant evidence is not the SOTA table but the semantic-occlusion analysis.

Across 15,364 validation samples:

```text
mask dynamic-agent regions:
mean intent change = 0.080

matched equal-area random masks:
mean intent change = 0.027

ratio = 2.97×
```

Dynamic-agent masking induces the larger change in:

```text
71.1% of samples
```

Individual-vehicle examples further show that masking vehicles that affect future driving changes the predicted intent/selected trajectory more than masking lower-impact vehicles.

This is meaningful because the predictor receives no object boxes, agent identities, interaction labels, or surrounding-agent motion annotations.

### What this supports

It supports:

```text
future-ego-trajectory supervision can make the learned intent representation selectively sensitive to scene elements correlated with planning relevance
```

### What it does not prove

It does not prove:

```text
the latent contains all decision-critical information
or
all discarded future-world information is irrelevant
or
selective sensitivity is causal interaction understanding
```

Occlusion sensitivity is evidence of dependence, not a complete sufficiency test.

---

## 9. Critical alternative explanations

### 9.1 The target is extremely close to the planning label

Unlike future-scene prediction, Auto-JEPA predicts a latent produced directly from the future ego trajectory.

Therefore one alternative interpretation is:

```text
this is a sophisticated trajectory-supervision / action-retrieval representation
rather than learned environment dynamics
```

That does not make the method weak; it changes what its success establishes. It demonstrates the power of a planning-aligned predictive target, not necessarily the need to model the world transition.

### 9.2 Frozen V-JEPA 2 visual prior is strong

The front-camera representation comes from a pretrained frozen V-JEPA 2 encoder. Therefore planning quality reflects:

```text
strong general video representation
+ trajectory-latent target
+ predictor
+ memory retrieval
+ scorer/gate
```

The paper's component ablation isolates intent prediction versus fixed medoid and scorer/gate contributions, but it does not provide a fully matched study of:

```text
same visual encoder + same retrieval/scorer
with ordinary direct trajectory regression
vs trajectory-latent prediction
```

sufficient to assign the entire gain specifically to the JEPA formulation.

### 9.3 Offline trajectory memory is a major planning prior

The memory contains 110k+ recorded, kinematically plausible training trajectories. Retrieval guarantees executable geometry is drawn from the training distribution.

This contributes a strong nonparametric action prior independent of any world-model interpretation.

The authors themselves note memory coverage as a limitation.

### 9.4 Scorer supervision uses NAVSIM offline evaluation semantics

The scorer/gate labels are generated offline from NAVSIM training metric cache. The paper explicitly uses a NAVSIM/CLOVER relabeling path and reports NAVSIM as a non-reactive benchmark.

Therefore the scorer improves decision quality under NAVSIM's offline/non-reactive target semantics; this is not reactive-agent behavioral validation.

---

## 10. Evaluation boundary

NAVSIM v1 and v2 are both planning benchmarks but have different rollout/aggregation protocols. The paper correctly reports them separately.

Important numbers:

```text
NAVSIM v1: 91.3 PDMS
NAVSIM v2 original evaluator: 85.6 EPDMS
NAVSIM v2 updated official implementation + human-behavior filtering: 89.1 EPDMS
```

This difference is a benchmark/evaluator effect, not a model change. It is another reminder that metric implementation belongs inside the scientific claim.

NAVSIM remains non-reactive pseudo-simulation; these results do not establish reactive closed-loop driving behavior.

---

## 11. Four-way Wave-3 interface comparison

```text
Epona
shared historical latent
→ separate trajectory + visual diffusion heads
→ visual generator can be disabled for planning

DrivingGPT
interleaved image/action tokens
→ one causal Transformer
→ world/action unified as one autoregressive language

DriveLaW
Video-DiT internal denoising state
→ direct condition for Action DiT
→ online world-model hidden state becomes planner representation

Auto-JEPA
current scene/history/route
→ predicted future ego-intent latent
→ trajectory-memory retrieval
→ scorer/gate
→ action
```

The new distinction introduced by Auto-JEPA is:

```text
WORLD/SCENE FUTURE REPRESENTATION
vs
EGO-ACTION FUTURE REPRESENTATION
```

It deliberately collapses the former into the latter.

---

## 12. What Auto-JEPA proves and does not prove

### Directly supported

```text
1. A compressed future-ego-trajectory latent can support strong NAVSIM planning.
2. The predicted intent must be scene-conditioned; replacing it with a fixed latent catastrophically degrades planning.
3. Large candidate retrieval plus scene-conditioned scoring materially improves over single-nearest retrieval.
4. The learned intent is more sensitive to dynamic-agent regions than matched random image regions.
5. Dense future scene reconstruction is not necessary for achieving strong planning in this particular NAVSIM setup.
```

### Not established

```text
1. Future ego-intent latent is universally sufficient for driving decisions.
2. Dense/scene-level future modeling can never add planning value beyond intent prediction.
3. The 91.3 PDMS gain is caused uniquely by JEPA prediction rather than strong V-JEPA features + memory + scorer.
4. The representation captures behaviorally correct counterfactual reactions.
5. Strong NAVSIM performance implies reactive closed-loop validity.
```

---

## 13. Scientific interpretation for the field atlas

Auto-JEPA strengthens a field-level pattern already emerging from OccWorld, ViDAR, LAW and DriveLaW:

```text
The useful object of prediction for planning need not be the most complete future-world reconstruction.
```

But it pushes this much further:

```text
representation target can be chosen by ACTION RELEVANCE,
not by world completeness.
```

This should not yet be converted into a research-gap claim. It is a design-axis conclusion:

```text
future-state richness
↔ planning alignment
↔ information compression
```

The next paper, DA-WAM, is the natural contrast because it reintroduces **candidate-specific future latents** for evaluating alternative actions rather than predicting one ego-intent latent and retrieving actions around it.

---

## 14. Evidence verdict

```text
future-intent representation exists and is used online:          STRONG
planning-oriented compression supports high NAVSIM performance: STRONG
intent predictor affects selected actions materially:            STRONG
scorer/candidate set are major independent contributors:         STRONG
compression universally preserves all decision-relevant info:   NOT ESTABLISHED
world-dynamics interpretation in classical sense:                AMBIGUOUS / BOUNDARY CASE
reactive/counterfactual behavioral validity:                     NOT ESTABLISHED
```

Wave-3 status after this audit:

```text
Epona       COMPLETE
DrivingGPT  COMPLETE
DriveLaW    COMPLETE
Auto-JEPA   COMPLETE
DA-WAM      NEXT
Think2Drive PENDING
```
