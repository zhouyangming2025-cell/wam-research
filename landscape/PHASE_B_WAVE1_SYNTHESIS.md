# PHASE_B_WAVE1_SYNTHESIS — Historical / Non-WM / Evaluation Baseline

Last updated: 2026-09-14

Status: **COMPLETE — Wave-1 comparative + comparability gates closed**

Wave 1:

```text
M2I
GameFormer
What Truly Matters in Trajectory Prediction?
UniAD
nuPlan
NAVSIM
DiffusionDrive
DriveSuprim
```

Purpose: establish what interaction, planning, multimodality, planner coupling and evaluation already meant before interpreting modern planning-centric WAM gains. This memo is explicitly not a gap document.

Detailed quantitative/method comparability audit:

`landscape/PHASE_B_WAVE1_COMPARABILITY_AUDIT.md`

---

## 1. First comparative result: the pre-WAM field already contained most of the *conceptual verbs*

Modern WAM language frequently uses verbs such as `condition`, `interact`, `respond`, `jointly model`, `imagine alternatives`, and `evaluate downstream consequences`. Wave 1 shows that several of these concepts predate the current WAM wave.

### M2I — conditional future dependence already explicit

**AUTHOR CLAIM.** Scene-consistent multi-agent prediction can be factorized into an influencer marginal and a reactor conditional distribution:

```text
P(Y_I, Y_R | X)
≈ P(Y_I | X) P(Y_R | X, Y_I)
```

The reactor is therefore predicted **conditioned on a future trajectory of another agent**, not merely on its history. M2I forms `N^2` influencer/reactor joint samples and retains the top-`K` by joint likelihood.

**DIRECT EXPERIMENTAL EVIDENCE.** On vehicle reactors at 8 s, using the ground-truth influencer future improves M2I’s conditional predictor over the marginal predictor (`mAP 0.41` vs `0.30`, with lower minADE/minFDE/miss rate). But when conditioning on only the best *predicted* influencer trajectory, performance becomes worse than the marginal predictor (`mAP 0.26`). The full system recovers performance by retaining multiple influencer samples and selecting joint samples.

**Strongest interpretation.** The paper directly demonstrates that future behavior of one agent contains useful information for another agent’s future.

**Strongest limitation.** The same experiment shows the cost of conditioning on an uncertain predicted future: a conditional-response model can degrade when the conditioned trajectory is wrong. Its influencer/reactor relation is derived through heuristic supervision, and the paper explicitly notes driving causality remains open. The paper says varying influencer trajectories enables counterfactual reasoning, but this is not equivalent to experimentally identified causal intervention effects.

**Historical role.** “Future of A → predicted response of B” is not a 2025–26 WAM invention. What later WAMs add must be more specific than conditional response itself.

### GameFormer — iterative mutual future reasoning already coupled to ego planning

GameFormer advances beyond one-way conditional prediction by making level-`k` agent futures respond to level-`k-1` futures of other agents, while jointly producing the AV plan and surrounding-agent trajectories.

**DIRECT EXPERIMENTAL EVIDENCE.** In its selected WOMD planning experiment, raw GameFormer reaches `73.16%` closed-loop success versus `68.12%` for DIPP. With the paper’s cost-based motion refinement, the values become `94.50%` and `92.16%`.

This decomposition is crucial:

```text
raw GameFormer advantage over DIPP = +5.04 percentage points
GameFormer refinement gain         = +21.34 percentage points
DIPP refinement gain               = +24.04 percentage points
```

Therefore the final `94.50%` cannot be attributed to hierarchical interaction modeling alone; the explicit refinement planner contributes a much larger absolute change.

Its interaction decoder ablation also improves prediction as reasoning depth increases to `K=6`; removing future-interaction input degrades the reported interaction-prediction metrics.

On nuPlan, GameFormer is evaluated in OL, CL non-reactive and CL reactive modes, but its overall benchmark result (`0.8288`) is **not** the best table entry: Hoplan (`0.8745`) and Multi_path (`0.8477`) are higher.

**Strongest limitation / alternative explanation.** The selected WOMD closed-loop simulation replays other agents’ logged trajectories and is explicitly non-reactive. The nuPlan reactive result is a separate benchmark regime and must not be conflated with the WOMD experiment.

**Historical role.** Mutual future reasoning, multi-agent multimodality and joint prediction/planning were already an active design space before generative driving WMs became the organizing label.

---

## 2. Second result: evaluation mismatch was already a first-class scientific problem

### What Truly Matters — prediction quality is planner- and dynamics-dependent

The paper’s key contribution is not another predictor; it changes the evaluation question.

**DIRECT EXPERIMENTAL EVIDENCE.** Static ADE/minADE on fixed data is reported as poorly correlated with downstream driving performance. When prediction is re-evaluated dynamically in an interactive simulator, correlation becomes substantially stronger. The authors quantify the dynamics gap as accounting for `77.0%` of the inconsistency for the RVO planner and `70.3%` for DESPOT under their analysis. They also show prediction runtime matters: under tighter planner tick budgets, the ranking of driving performance tracks predictor inference time strongly.

**What it establishes.** Predictor usefulness is not a function of prediction error alone; the downstream planner, interaction-induced state distribution and computation budget are part of the effective system.

**Strongest limitation.** The paper itself notes that experiments use selected sampling/reactive planners and simulator oracle perception; optimization/geometric planners and raw-sensor system effects are not comprehensively covered. Therefore its exact percentages should not be universalized.

**Historical role.** Long before current WAM benchmark debates, the literature already contained evidence that “better future prediction metric → better driving” is not generally valid.

### nuPlan — planning requires goals, planning metrics and closed-loop protocols

nuPlan explicitly argues that motion-prediction datasets and open-loop L2 metrics are insufficient for long-horizon planning. It introduces planning goals, traffic-rule / comfort / progress / scenario metrics, and distinct:

```text
Open-loop
Closed-loop non-reactive
Closed-loop reactive
```

protocols.

A particularly important boundary is documented by nuPlan itself: if the ego deviates from the logged route, it does **not** synthesize/warp new camera or LiDAR views in the described setup. Thus, its lightweight closed-loop abstraction is powerful for planning but not equivalent to a fully sensor-realistic closed-loop world.

### NAVSIM — deliberate retreat from reactivity to gain real-data scale

NAVSIM is not “weak closed loop”; it is a deliberately different compromise. It queries the sensor-based policy only at the initial frame, fixes the planned trajectory over a `4 s` horizon, and explicitly assumes policy actions do not affect other-agent futures. This allows real sensor inputs plus simulation-derived safety/progress/comfort metrics without synthetic sensor rendering.

**DIRECT EVIDENCE / historical consequence.** The paper reports that these non-reactive simulation metrics align better with closed-loop outcomes than conventional displacement error, and the CVPR challenge showed simple/moderate-compute planners could match much larger E2E architectures under this protocol.

**Terminology correction.** Later papers sometimes describe NAVSIM as using “closed-loop metrics.” In this project, NAVSIM remains `E3 non-reactive pseudo-simulation`: simulation-derived metrics do not make the environment reactive.

**Strongest boundary.** NAVSIM cannot measure policy recovery after observation shift, long-horizon compounding, intervention-dependent other-agent behavior, or sensor-view shift after ego deviation because those are removed by design.

### Evaluation lineage after Wave 1

The field did not monotonically move from “bad open loop” to “good closed loop.” It explored different compromises:

```text
prediction/open-loop logs
    ↓
nuPlan: planning-specific closed loop on abstract/logged scene state
    ↓
NAVSIM: return to non-reactive short horizon to preserve real sensor inputs + scale
    ↓
later Bench2Drive/HUGSIM/reactive-WM work: recover different forms of interaction or sensor realism
```

This means benchmark choice is part of the method’s evidentiary claim, not a neutral reporting detail.

---

## 3. Third result: strong planning progress already came from representation and action-space design without a WM

### UniAD — planning-oriented task coordination predates planning WMs

UniAD’s core design claim is that perception/prediction modules should be organized around the final planning objective rather than simply stacked as independent heads.

The exact future→planner path is mixed:

```text
MotionFormer future reasoning
→ expressive ego query
→ planner trajectory

OccFormer future occupancy
→ occupancy-aware collision avoidance / optimization
→ trajectory adjustment
```

The planner also attends to BEV features and uses collision loss. Therefore UniAD is not a clean “future prediction on/off” experiment.

**DIRECT EXPERIMENTAL EVIDENCE.** At 3 s, adding BEV attention, collision loss and occupancy-based optimization lowers collision rate from `1.64` to `1.05`, while L2 changes from `1.71` to `1.81`. This is useful evidence that planning safety and trajectory imitation are already partially misaligned inside a strong E2E stack.

**Correct control role.** UniAD is a control for **planning-oriented structured representation + future auxiliary tasks + explicit collision-aware planning**, not a matched baseline for an inference-time generative world model.

### DiffusionDrive — multimodal action generation can be strong without modeling a future world

DiffusionDrive targets the action distribution directly. Its strongest causal evidence is not the SOTA table but the matched Transfuser roadmap using aligned perception/backbone settings:

```text
Transfuser       84.0 PDMS, 60 FPS
Transfuser_DP    84.6 PDMS,  7 FPS
Transfuser_TD    85.7 PDMS, 27 FPS
DiffusionDrive   88.1 PDMS, 45 FPS
```

The decoder ablation further shows `85.7 → 87.1 → 87.4 → 88.1` as scene-conditioned spatial interaction, agent/map interaction and cascade decoding are added. One/two/three denoising steps give `87.9 / 88.1 / 88.1`, so the gain should not be narrated as deep iterative generative reasoning.

**What this controls for.** Diversity, generative modeling and a diffusion architecture are not evidence of a world model. A strong planner can gain from learning a better multimodal **action distribution** and better scene-conditioned trajectory decoder while predicting no future environment state.

**Strongest limitation.** NAVSIM evidence is non-reactive and the nuScenes planning evidence is open-loop. The paper demonstrates strong action modeling under those regimes, not interactive consequence prediction.

### DriveSuprim — candidate evaluation can be the bottleneck even without a future model

DriveSuprim operates over a large trajectory vocabulary and focuses on hard-negative discrimination, directional imbalance, and brittle binary safety labels. It uses coarse-to-fine filtering, rotation augmentation and self-distillation rather than an explicit future world rollout.

For a fair NAVSIM v1 comparison with DiffusionDrive, the matched ResNet-34 rows are:

```text
DiffusionDrive  88.1 PDMS
DriveSuprim     89.9 PDMS
```

The headline `93.5 PDMS` DriveSuprim result uses ViT-Large and must not be treated as a method-only delta over R34 DiffusionDrive.

On NAVSIM v2, PDMS is replaced by EPDMS with additional direction, traffic-light, lane-keeping and revised comfort terms, so v1 and v2 scores are not numerically interchangeable. With ResNet-34, DriveSuprim moves from the HydraMDP++ baseline `81.4` to `83.1 EPDMS`; the paper decomposes this as approximately `+1.0` from multi-stage refinement, `+0.3` from augmentation and `+0.4` from self-distillation.

Its top-K oracle study is especially important:

```text
best top-1     91.9 PDMS
best top-4     94.5
best top-16    96.1
best top-256   98.7
human          94.8
```

This shows substantial planning headroom can already exist inside the candidate set and be lost purely by ranking.

**Bench2Drive boundary.** Its `83.02 DS / 60.00 SR` result is an important interactive closed-loop system result, but the paper states that the Bench2Drive version is built on CARLA-Garage / TF++ and uses two-stage trajectory prediction for longitudinal control. It should not be assumed to be an identical deployment of the NAVSIM model.

---

## 4. Wave-1 comparative matrix

| paper | primary scientific object | future representation | planner coupling | interaction level | evaluation meaning | strongest lesson for later WAM reading |
|---|---|---|---|---|---|---|
| M2I | interactive prediction | influencer/reactor trajectories | no ego planner in core benchmark | explicit conditional response | prediction benchmark | conditional future response predates WAM; conditioning error propagates |
| GameFormer | interactive prediction + planning | hierarchical multimodal agent/ego trajectories | joint decode + optional refinement | iterative level-k mutual response | WOMD OL/non-reactive CL + nuPlan OL/CL | interactive planning is not new; post-refinement contribution must be separated |
| What Truly Matters | predictor evaluation | predictor-dependent dynamic futures in simulator | predictor embedded in planner loop | interactive evaluation | SUMMIT dynamic evaluation | static prediction metrics can mis-rank downstream driving; compute matters |
| UniAD | planning-oriented E2E stack | motion + occupancy predictions | ego query + occupancy-aware optimization | joint scene prediction, not per-action reactive rollout | mainly nuScenes OL | representation/task coordination and explicit safety optimization can improve planning without modern WM |
| nuPlan | planning benchmark | simulator agent state | evaluates arbitrary planner | NR and reactive modes defined | planning-specific OL/CL | closed-loop planning evaluation predates WAM and has sensor-view limitations |
| NAVSIM | scalable planner benchmark | short BEV non-reactive unroll | score fixed submitted trajectory | intentionally non-reactive | E3 | real sensors + scalable metrics obtained by sacrificing reactivity |
| DiffusionDrive | direct multimodal policy | ego action distribution | direct trajectory generation | no future-world response | NAVSIM + nuScenes | generative action modeling + better decoder can be strong without WM |
| DriveSuprim | trajectory candidate selection | candidate-score distribution | coarse→fine score/select | no future-world response in NAVSIM branch | NAVSIM v1/v2 + adapted Bench2Drive system | scorer/training quality is a strong alternative cause of planning gains |

---

## 5. What problems existed before the modern WAM wave?

Wave 1 separates at least five independent problem classes:

```text
A. Interaction prediction
   marginal futures ignore dependence between agents

B. Prediction→planning coupling
   future predictions useful to a predictor are not automatically useful to a planner

C. Planning representation / task coordination
   perception, prediction and occupancy can be organized around the planning objective

D. Action representation / selection
   regression, diffusion, fixed vocabularies, candidate ranking and hard negatives create planner-specific bottlenecks

E. Evaluation
   static logs, non-reactive pseudo-simulation and interactive closed loop measure different properties
```

Modern world models enter a field where **all five already existed**. Therefore a later WAM paper should be read as answering a more precise question:

> Which of these pre-existing problems does predicting a world/future state actually change, and is that change isolated from better representation, action modeling, scoring, optimization or evaluation?

---

## 6. Wave-1 control rules carried into all later deep reads

1. **Future-conditioned response is not automatically causal response.** Ask what intervention changed and where supervision came from.
2. **Final planning score must be decomposed.** Separate learned future representation from scorer, refinement, optimizer and rule-based post-processing.
3. **Matched controls dominate SOTA tables.** Prefer same backbone/data/input/evaluator ablations over headline scores.
4. **Generative action ≠ world model.** Diffusion over ego trajectories is an action model unless environment future is explicitly modeled.
5. **Candidate ranking is an independent bottleneck.** A WM-based selector must beat the explanation “same candidate set, better scorer/training.”
6. **Evaluation regime is part of the claim.** E2/E3/E4/E5/E6/E7 cannot be collapsed into one “closed-loop” category.
7. **World-prediction accuracy is not planning evidence by itself.** Require an explicit future→planner path and planning-side evidence.

---

## 7. Wave-1 gate decision

The dedicated comparability audit resolves the five previously open questions sufficiently for field synthesis:

```text
M2I conditional-vs-causal boundary        RESOLVED FOR FIELD SYNTHESIS
GameFormer refinement contribution        RESOLVED
UniAD future→planner path                 RESOLVED AT ARCHITECTURAL LEVEL
DiffusionDrive vs DriveSuprim matching    RESOLVED WITH BACKBONE/VERSION FLAGS
nuPlan vs NAVSIM evidence meanings        RESOLVED AT PROTOCOL LEVEL
```

Current status:

```text
comparative first pass: COMPLETE
quantitative comparability audit: COMPLETE
historical/control coordinate system: ESTABLISHED
Wave-1 final synthesis gate: CLOSED
```

Next scientific task is Wave 2:

```text
GAIA-1
Drive-WM
OccWorld
WoTE
ViDAR
LAW
```

Wave 2 must use the same control questions established here rather than assuming that a world-model label explains a planning gain.