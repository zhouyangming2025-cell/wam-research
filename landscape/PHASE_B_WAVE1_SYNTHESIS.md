# PHASE_B_WAVE1_SYNTHESIS — Historical / Non-WM / Evaluation Baseline

Last updated: 2026-09-14

Status: **IN PROGRESS — first comparative pass completed on the eight Wave-1 primary texts**

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

---

## 1. First comparative result: the pre-WAM field already contained most of the *conceptual verbs*

Modern WAM language frequently uses verbs such as `condition`, `interact`, `respond`, `jointly model`, `imagine alternatives`, and `evaluate downstream consequences`. Wave 1 shows that several of these concepts predate the current WAM wave.

### M2I — conditional future dependence already explicit

**AUTHOR CLAIM.** Scene-consistent multi-agent prediction can be factorized into an influencer marginal and a reactor conditional distribution:

```text
P(Y_I, Y_R | X)
≈ P(Y_I | X) P(Y_R | X, Y_I)
```

The reactor is therefore predicted **conditioned on a future trajectory of another agent**, not merely on its history.

**DIRECT EXPERIMENTAL EVIDENCE.** On vehicle reactors at 8 s, using the ground-truth influencer future improves M2I’s conditional predictor over the marginal predictor (`mAP 0.41` vs `0.30`, with lower minADE/minFDE/miss rate). But when conditioning on only the best *predicted* influencer trajectory, performance becomes worse than the marginal predictor (`mAP 0.26`). The full system recovers performance by retaining multiple influencer samples and selecting joint samples.

**Strongest interpretation.** The paper directly demonstrates that future behavior of one agent contains useful information for another agent’s future.

**Strongest limitation.** The same experiment shows the cost of conditioning on an uncertain predicted future: a conditional-response model can degrade when the conditioned trajectory is wrong. Its influencer/reactor relation is also derived through a heuristic supervision scheme, and the paper explicitly notes driving causality remains open.

**Historical role.** “Future of A → predicted response of B” is not a 2025–26 WAM invention. What later WAMs add must be more specific than conditional response itself.

### GameFormer — iterative mutual future reasoning already coupled to ego planning

GameFormer advances beyond one-way conditional prediction by making level-`k` agent futures respond to level-`k-1` futures of other agents, while jointly producing the AV plan and surrounding-agent trajectories.

**DIRECT EXPERIMENTAL EVIDENCE.** In its selected WOMD planning experiment, raw GameFormer reaches `73.16%` closed-loop success versus `68.12%` for DIPP; with the paper’s cost-based motion refinement the values become `94.50%` and `92.16%`. Its interaction decoder ablation also improves prediction as reasoning depth increases to `K=6`; removing future-interaction input degrades the reported interaction-prediction metrics.

On nuPlan, GameFormer is evaluated in OL, CL non-reactive and CL reactive modes, but its overall benchmark result (`0.8288`) is **not** the best table entry: Hoplan (`0.8745`) and Multi_path (`0.8477`) are higher. This is important negative evidence against reading the paper as “interaction modeling solves planning.”

**Strongest limitation / alternative explanation.** The selected WOMD closed-loop simulation replays other agents’ logged trajectories and is explicitly non-reactive. Moreover, the cost-based refinement planner produces a very large absolute gain; therefore the learned interaction decoder is not solely responsible for the final closed-loop performance.

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

**Strongest boundary.** NAVSIM cannot measure policy recovery after observation shift, long-horizon compounding, or intervention-dependent other-agent behavior because those are removed by design.

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

UniAD’s core design claim is that perception/prediction modules should be organized around the final planning objective rather than simply stacked as independent heads. Track/map/motion/occupancy queries form explicit task interfaces; an ego query carries information into planning; occupancy is used to reduce collision risk.

**DIRECT EXPERIMENTAL EVIDENCE.** Its planner ablation shows that adding BEV attention, collision loss and occupancy-based optimization progressively lowers collision rate (e.g. at 3 s from `1.64` in the base planner to `1.05` with all components), while the corresponding L2 imitation error can worsen (`1.71` to `1.81`). This is useful evidence that planning quality and trajectory imitation are already partially misaligned inside a strong E2E stack.

**Strongest limitation for current WAM comparisons.** UniAD’s future motion/occupancy tasks are explicit, but this is not an inference-time generative world model in the modern sense. Its primary planning evaluation is the nuScenes open-loop ecosystem. Thus it is best used as a control for **planning-oriented representation/task coordination**, not as a closed-loop world-model baseline.

### DiffusionDrive — multimodal action generation can be strong without modeling a future world

DiffusionDrive targets the action distribution directly. It replaces single-mode regression / huge discrete trajectory vocabularies with an efficient truncated diffusion policy initialized around multi-mode trajectory anchors.

**DIRECT EXPERIMENTAL EVIDENCE.** The paper reports `88.1 PDMS` on NAVSIM with a ResNet-34 backbone and `45 FPS`, using only two denoising steps; it also reports improved nuScenes L2/collision metrics over VAD with aligned backbones.

**What this controls for.** Diversity, generative modeling and a diffusion architecture are not evidence of a world model. A strong planner can gain from learning a better multimodal **action distribution** while predicting no future environment state.

**Strongest limitation.** NAVSIM evidence is non-reactive and the nuScenes planning evidence is open-loop. The paper demonstrates strong action modeling under those regimes, not interactive consequence prediction.

### DriveSuprim — candidate evaluation can be the bottleneck even without a future model

DriveSuprim operates over a large trajectory vocabulary and focuses on three selection failures: hard negatives drowned by easy negatives, directional imbalance, and brittle binary safety labels. It uses coarse-to-fine filtering, rotation augmentation and self-distillation rather than an explicit future world rollout.

**DIRECT EXPERIMENTAL EVIDENCE.** It reports `93.5% PDMS` on NAVSIM v1, `87.1% EPDMS` on NAVSIM v2, and `83.02` Driving Score / `60.00` Success Rate on Bench2Drive. Its oracle study shows substantial headroom between learned top-1 selection and best-of-top-K candidate quality.

**What this controls for.** When a WM-based planner improves candidate ranking, the improvement cannot automatically be attributed to “better imagined futures”; better discrimination/training of the scorer itself is a viable competing explanation.

**Strongest limitation.** The method remains tied to a predefined candidate vocabulary and learned metric/rule scores. Its success does not imply explicit world modeling is unnecessary in every setting; it shows only that candidate coverage/scoring is a powerful independent axis.

---

## 4. Wave-1 comparative matrix

| paper | primary scientific object | future representation | planner coupling | interaction level | evaluation meaning | strongest lesson for later WAM reading |
|---|---|---|---|---|---|---|
| M2I | interactive prediction | influencer/reactor trajectories | no ego planner in core benchmark | explicit conditional response | prediction benchmark | conditional future response predates WAM; conditioning error propagates |
| GameFormer | interactive prediction + planning | hierarchical multimodal agent/ego trajectories | joint decode + optional refinement | iterative level-k mutual response | WOMD OL/non-reactive CL + nuPlan OL/CL | interactive planning is not new; post-refinement contribution must be separated |
| What Truly Matters | predictor evaluation | predictor-dependent dynamic futures in simulator | predictor embedded in planner loop | interactive evaluation | SUMMIT dynamic evaluation | static prediction metrics can mis-rank downstream driving; compute matters |
| UniAD | planning-oriented E2E stack | motion + occupancy predictions | queries / occupancy → planner | joint scene prediction, not per-action reactive rollout | mainly nuScenes OL | representation/task coordination can improve planning without modern WM |
| nuPlan | planning benchmark | simulator agent state | evaluates arbitrary planner | NR and reactive modes defined | planning-specific OL/CL | closed-loop planning evaluation predates WAM and has sensor-view limitations |
| NAVSIM | scalable planner benchmark | short BEV non-reactive unroll | score fixed submitted trajectory | intentionally non-reactive | E3 | realistic sensors + scalable metrics obtained by sacrificing reactivity |
| DiffusionDrive | direct multimodal policy | ego action distribution | direct trajectory generation | no future-world response | NAVSIM + nuScenes | generative/diffusion planning can be strong without WM |
| DriveSuprim | trajectory candidate selection | candidate-score distribution | coarse→fine score/select | no future-world response | NAVSIM v1/v2 + Bench2Drive | scoring/training quality is a strong alternative cause of planning gains |

---

## 5. Initial synthesis: what problems existed before the modern WAM wave?

Wave 1 already separates at least five independent problem classes:

```text
A. Interaction prediction
   marginal futures ignore dependence between agents

B. Prediction→planning coupling
   future predictions useful to a predictor are not automatically useful to a planner

C. Planning representation / task coordination
   perception, prediction and occupancy can be organized around the planning objective

D. Action representation / selection
   single-mode regression, fixed vocabularies, hard-negative discrimination and multimodality create planner-specific bottlenecks

E. Evaluation
   static logs, non-reactive pseudo-simulation and interactive closed loop measure different system properties
```

Modern world models enter a field where **all five already existed**. Therefore a later WAM paper should be read as answering a more precise question:

> Which of these pre-existing problems does predicting a world/future state actually change, and is that change isolated from better representation, action modeling, scoring or evaluation?

This is a stronger baseline than asking merely whether “world modeling helps planning.”

---

## 6. Important cautions before Wave 1 is closed

This first pass is sufficient to establish the structural baseline, but the Wave-1 gate remains **open** until the following are tightened from the primary texts/cards:

1. M2I: exact joint-sample selection and the boundary between conditional prediction and causal intervention.
2. GameFormer: how much of planning benefit survives without the cost-based refinement stage, and what nuPlan reactive evaluation actually exercises.
3. UniAD: exact planner consumption of MotionFormer vs OccFormer and whether auxiliary-task gains can be disentangled cleanly.
4. DiffusionDrive vs DriveSuprim: matched NAVSIM conditions/backbone/data differences before using either as a quantitative control against a WAM.
5. nuPlan vs NAVSIM: protocol-version differences and which later papers actually use which implementation/metric variant.

No cross-paper numerical ranking should be made until these comparability checks are complete.

## 7. Current Wave-1 status

```text
comparative first pass: COMPLETE
historical/control structure: ESTABLISHED
quantitative comparability audit: PENDING
Wave-1 final synthesis gate: OPEN
```

Next work stays within these eight anchors; no new broad literature acquisition is justified yet.