# M1 World-First Mediation Audit

Status: **SUB-BRANCH RECONSTRUCTION + CORRECTION — NOT AN ONTOLOGY SPEC**  
Branch: `research/core-route-reconstruction`  
Date: 2026-09-17  
Target: determine whether `M1: O -> Z -> A` is a real route family or an over-broad merger.

## 0. Immediate correction: OccWorld was provisionally misprojected

`07_MINIMAL_CAUSAL_SPINE_PROJECTION.md` placed OccWorld under M1 based on the D01 neutral skeleton:

`occupancy future -> planning`.

Full-paper re-reading changes this judgment.

Primary source: `papers/raw_md/P0043_OccWorld/P0043_OccWorld.raw.md`.

OccWorld explicitly formulates one autoregressive world model that predicts **future scene tokens and ego tokens / ego movement together**. The paper states that it simultaneously predicts surrounding-scene evolution and ego motion; Eq. (3) writes the world model as predicting both next scene representation and next ego position.

Therefore OccWorld is not clean evidence for a serial:

`future occupancy -> separate planner`.

It is better treated as **M3 joint world-action / world-ego future generation evidence**, subject to the M3 strict jointness gate.

### Consequence

The OccWorld row in `07_MINIMAL_CAUSAL_SPINE_PROJECTION.md` is **SUPERSEDED** by this full-paper audit.

This is an important methodological result:

> Neutral skeletons are good census evidence, but CoreRoute adjudication must return to the paper's actual generative factorization before accepting a branch assignment.

No existing historical census file is modified; the correction is recorded here.

---

## 1. What M1 is supposed to mean

General causal program:

`O -> Z -> A`

where:

- `Z` is a separately traceable online world/future/model state;
- `Z` is formed before the final action computation;
- the planner directly consumes `Z`;
- `Z` is not indexed by a provisional ego alternative in the M2 sense;
- world/action are not co-generated in one M3 process.

The danger is obvious: if every “feature used by planner” qualifies as Z, M1 degenerates into ordinary representation learning.

A strict **online mediator gate** is therefore required.

---

## 2. Strict online world-mediator gate

A state `Z` should count as M1 only if all are supported:

1. **runtime localization** — a state/object can be identified on the deployed causal path;
2. **world/dynamics operation** — its runtime computation includes predictive, temporal-dynamics, generative-model-state, interaction-world-state, or comparable world-model operation beyond ordinary visual encoding;
3. **planning mediation** — planner/action generation causally reads this state;
4. **online indispensability** — the paper's WAM-specific bridge would materially change if `Z` were removed while leaving generic perception features available;
5. **not merely inherited parameters** — predictive pretraining alone does not create M1 if only an ordinary encoder feature survives;
6. **not action-indexed consequence** — if each ego alternative creates its own `Z(A_k)`, use M2;
7. **not joint co-generation** — if `Z` and action are generated as coupled targets in one future process, test M3 first.

This gate separates M1 from both M0-R and M3.

---

## 3. Sublineage A — explicit future forecast used as planning rationale

### Core form

```text
history/current state
    -> predicted future world state(s)
    -> planning/action decoder
```

The future state is explicitly materialized as an intermediate planning object before action.

### Strong anchor: Policy World Model

Primary source: `papers/raw_md/P0041_PolicyWM/P0041_PolicyWM.raw.md`.

PWM explicitly criticizes unified models in which world modeling and action generation are only architecturally co-located but planning does not use generated future states.

Its proposed sequence is:

- learn world modeling through action-free video forecasting;
- at fine-tuning/inference, roll out plausible future states;
- use current description + forecast future states as multimodal rationales;
- predict action after considering those forecasts.

This is almost canonical M1:

`world forecast -> action`.

### Other evidence / pressure cases

- DriveDreamer action path: recurrent predicted structural future + world-model features -> action decoder;
- some occupancy/prediction-conditioned planning systems if full paper confirms serial forecast->planner rather than joint co-generation;
- UniAD / BeTop / VAD as adjacent/control examples of predicted future structure -> direct planning, though their WAM-domain qualification is separate.

### Working description

`M1-F`: explicit future/world forecast is a planning intermediate.

Status: **mature sublineage candidate**, but strict target-domain membership must be checked paper-by-paper.

---

## 4. Sublineage B — internal model/world state directly mediates planning

### Core form

```text
history/current observation
    -> internal world-model state Z
    -> planner
```

The planner consumes a state produced by an online world/generative/dynamics process, without requiring an explicit decoded future as its input.

### DriveLaW

Primary source: `papers/raw_md/P0009_DriveLaW/P0009_DriveLaW.raw.md`.

DriveLaW's paper-level thesis is exactly to stop treating video generation and planning as parallel tasks and instead feed the video generator's internal representation into Action DiT.

The mid-denoising video/generative latent is therefore an online model state, not merely a pretrained encoder feature.

Deleting this latent-to-planner chain destroys the paper's central mechanism.

Strong M1-state anchor.

### GraphWorld

Primary source: `papers/raw_md/P0065_GraphWorld/...`.

GraphWorld explicitly avoids explicit multi-step rollout and instead constructs a compact ego-centric relational world state encoding interaction dynamics and safety-relevant future structure. This world state directly modulates/plans ego trajectories.

This is also M1-state mediation, although the state is relational rather than a video-generator latent.

### Epona

Primary source: `papers/raw_md/P0001_Epona/P0001_Epona.raw.md`.

Epona learns a causal temporal latent dynamics model and specialized video/trajectory diffusion decoders. Planning-only inference can disable expensive video rendering while retaining the shared temporal world representation used by the trajectory generator.

Current judgment: M1-state is plausible and remains **medium/high confidence**, but exact runtime state boundaries should be rechecked if this becomes normative.

### Working description

`M1-S`: internal predictive/generative/relational world state directly conditions planning.

Status: **mature sublineage candidate**.

---

## 5. M1-S vs M0-R — the hardest boundary

This is a critical gate because both may use “predictive representation”.

### M0-R

Predictive/world learning shapes deployed parameters/features, but no separately traceable online world operation must run.

Examples:

- LAW after training;
- Drive-JEPA encoder transfer;
- ViDAR downstream transfer;
- Metis if action inference uses only current-observation representation and no stateful future/world computation.

### M1-S

A separately traceable online world/model-state computation remains and the planner reads its state.

Examples:

- DriveLaW Video DiT latent;
- GraphWorld interaction world state;
- Epona temporal world state (provisional).

### Metis stress case

Metis predicts actions from `z(o_t,l)` produced by the video backbone in one forward pass while explicit future observations are training-only/bypassed.

Question:

> Is `z(o_t,l)` a runtime world-model state or simply a world-pretrained current-observation representation?

Current answer: **M0-R remains the safer assignment**.

Reason:

- future observations are explicitly absent from action inference;
- action tokens are masked from future-video tokens;
- the paper's efficiency claim relies on direct action prediction from current observation latent;
- current evidence does not establish a distinct runtime transition/predictive operation whose state the action expert consumes.

This boundary should be code-verified if M1-S becomes normative.

### Gate lesson

> “Produced by a world-model backbone” is not enough for M1.

Otherwise every predictive-pretrained encoder would become an online world state and M0-R would disappear.

---

## 6. M1-F vs M1-S — route split or mediator profile?

This is the main unresolved question inside M1.

### Difference

`M1-F`:

- planner reads an explicitly forecast future state/object;
- forecast can often be decoded/inspected independently;
- scientific thesis often resembles “anticipate first, then plan”.

`M1-S`:

- planner reads an internal world/model state;
- no explicit future needs to be materialized for the planner;
- scientific thesis often resembles “use the model's internal dynamics representation as planning state”.

### Core-Bridge substitution test

Imagine replacing a decoded future forecast with an internal latent that carries the same decision-relevant predictive information, while preserving:

`world state -> action`.

The high-level causal direction remains unchanged.

Conversely, decoding an internal latent into an explicit future before feeding it to the same planner does not automatically alter the world-to-action bridge.

### Current judgment

The distinction is scientifically meaningful, but **not yet proven to deserve two top-level CoreRoutes**.

Best current representation:

- shared major ancestor: `M1 world-first mediation`;
- mediator subprofile/sublineage:
  - explicit forecast (`M1-F`);
  - internal world state (`M1-S`).

Promotion requires evidence that this choice repeatedly changes the causal planning program rather than only the representation/materialization of the mediator.

---

## 7. GraphWorld is not merely “latent future prediction”

GraphWorld deserves special attention because it challenges a simple forecast-centric worldview.

Its core claim is not “predict future and feed it to planner”. Instead:

- construct an ego-centric relational interaction world state;
- encode future-relevant dynamics / safety semantics in that state;
- directly condition long-horizon planning;
- avoid explicit multi-step rollout.

Thus GraphWorld supports M1-S but also creates a possible deeper fork:

> **world-as-predictive-state vs world-as-explicit-future-outcome**.

For now this is a mediator/state profile, not a new route.

If multiple independent papers explicitly make the same “predictive state is sufficient; explicit future forecast is unnecessary” argument, this branch should be reconsidered.

---

## 8. OccWorld correction strengthens M3, not M1

OccWorld is valuable because it shows why output ordering must be reconstructed from the actual generative factorization.

Its paper-level program jointly predicts:

- future scene occupancy tokens;
- future ego tokens / trajectory.

That is closer to:

`history -> joint future generative process -> (world, ego)`

than:

`history -> future occupancy -> independent planner`.

Therefore:

- remove OccWorld from strong M1 support;
- add it as a strong M3 pressure case;
- re-audit Drive-OccWorld before assuming the same correction applies there.

This correction is evidence **for** the audit methodology, not a failure: the point of first-principles reconstruction is to allow previous shallow assignments to be overturned.

---

## 9. Current M1 hierarchy

```text
Online world-first mediation (M1 ancestor)
|
|-- M1-F  explicit future/world forecast -> planner
|     |-- Policy World Model [strong anchor]
|     |-- DriveDreamer action path [support; some lifecycle UNKNOWN]
|     |-- structured forecast/planning systems [paper-by-paper domain gate]
|
|-- M1-S  internal online world/model state -> planner
      |-- DriveLaW generator latent [strong]
      |-- GraphWorld relational world state [strong]
      |-- Epona shared temporal world state [probable]
```

Current status:

- M1 ancestor: **strong**;
- M1-F / M1-S: **real sublineages**, but currently better treated as mediator profiles than final CoreRoute split.

---

## 10. Current verdict

High confidence:

- M1 requires a strict online mediator gate to avoid collapsing into M0-R.
- DriveLaW and GraphWorld are strong M1-S anchors.
- Policy World Model is a strong M1-F anchor.
- OccWorld should not remain a clean M1 anchor; full-paper evidence pushes it toward M3.
- “world-pretrained current feature” is not sufficient for M1.

Medium/high confidence:

- Epona's planning route is M1-state-like rather than M0-only or M3.

Medium confidence:

- explicit forecast vs internal model state is a useful sublineage distinction.

Low/medium confidence:

- M1-F and M1-S deserve separate final CoreRoute names.

Next priority:

> re-audit M3 with OccWorld added as a new hard case, then synthesize a revised minimal causal spine that explicitly records corrections from the full-paper sub-branch audits.
