# PHASE_B_WAVE1_COMPARABILITY_AUDIT — What the Numbers Actually Mean

Last updated: 2026-09-14

Status: **COMPLETE — closes the Wave-1 quantitative/comparability gate**

Scope: M2I, GameFormer, What Truly Matters, UniAD, nuPlan, NAVSIM, DiffusionDrive, DriveSuprim.

Purpose: determine which apparent planning gains can be attributed to the stated mechanism, which are confounded by downstream refinement / supervision / backbone / benchmark changes, and which numerical results are legitimately comparable. This is not a ranking table and not a gap analysis.

---

## 1. Audit rule

Every number is interpreted through the tuple

```text
(model mechanism,
 input / backbone,
 training supervision,
 candidate/action representation,
 post-processing,
 benchmark version,
 interaction regime,
 metric)
```

Two results are treated as quantitative controls only when the relevant dimensions are sufficiently matched. Same metric name alone is not enough.

---

## 2. M2I — conditional response is real, but not equivalent to causal intervention

### Mechanism verified

M2I factorizes a two-agent future as

```text
P(Y_I, Y_R | X)
≈ P(Y_I | X) P(Y_R | X, Y_I)
```

and explicitly feeds the influencer's **future trajectory** into the reactor predictor. For each of `N` influencer samples it predicts `N` conditional reactor samples, forms `N^2` joint samples, scores each by marginal-probability × conditional-probability, and retains the top-`K` joint samples.

### Strongest matched evidence

For vehicle reactors at 8 s:

```text
M2I Marginal        mAP 0.30
Conditional + GT YI mAP 0.41
Conditional + P1 YI mAP 0.26
```

The GT-conditioned result demonstrates that another agent's future trajectory contains useful response information. The P1 result demonstrates the opposite side of the same mechanism: **conditioning on a wrong predicted future can be worse than not conditioning at all**.

### Boundary

The paper states that varying the influencer trajectory enables counterfactual reasoning in simulation applications, but its core supervision is still observational logged interaction data with heuristic influencer/reactor labels. Therefore:

```text
conditional future response
!= identified causal effect of intervention
!= validated ego-action counterfactual world rollout
```

For later WAM reading, M2I is a historical control for `future-conditioned response`, not proof that modern action-conditioned WMs are redundant.

---

## 3. GameFormer — separate learned interaction gain from refinement-planner gain

### Learned interaction component

GameFormer iteratively predicts each level-`k` agent policy conditioned on the level-`k-1` futures of other agents. The ego trajectory and neighboring-agent trajectories are jointly decoded.

The interaction-prediction ablation supports the mechanism: performance improves up to `K=6`, and `K=6 w/o future` degrades relative to full `K=6`. This is direct evidence that predicted future-interaction input contributes to the forecasting task.

### Planning result decomposition

On the selected WOMD non-reactive closed-loop experiment:

| method | raw success | + cost-based refinement |
|---|---:|---:|
| DIPP | 68.12% | 92.16% |
| GameFormer | 73.16% | 94.50% |

Two distinct effects are visible:

```text
raw learned-model advantage:
73.16 - 68.12 = +5.04 percentage points

refinement gain inside GameFormer:
94.50 - 73.16 = +21.34 percentage points

refinement gain inside DIPP:
92.16 - 68.12 = +24.04 percentage points
```

The final `94.50%` therefore cannot be used as evidence that hierarchical future interaction alone produces the closed-loop result. The learned model improves the pre-refinement plan, while the explicit cost-based refinement is responsible for a much larger absolute change.

### Interaction-regime correction

The selected WOMD closed-loop experiment is **non-reactive**: other agents follow logged trajectories. Hence it evaluates ego rollout/replanning under distribution shift, not intervention-dependent social response.

GameFormer is also reported on nuPlan OL / CL non-reactive / CL reactive. Its table score is:

```text
Overall 0.8288
OL      0.8400
CL-NR   0.8087
CL-R    0.8376
```

but Hoplan (`0.8745`) and Multi_path (`0.8477`) have higher overall scores. Thus the correct conclusion is not “game-theoretic interaction solves reactive planning”; it is that explicit iterative future interaction is a viable prediction/planning design with evidence across several evaluation regimes.

### Later-WAM control

Any modern WM claiming gains from interactive future reasoning must be compared against at least two alternative explanations already visible here:

```text
better learned interaction representation
vs
better downstream motion refinement / optimization
```

---

## 4. What Truly Matters — dynamic evaluation changes the object being measured

The central experiment compares static prediction metrics against prediction measured **inside** the planner/environment loop.

The paper reports that the dynamics gap accounts for approximately:

```text
77.0% of the static-vs-driving inconsistency for RVO
70.3% for DESPOT
```

under its specific simulator/analysis. It additionally shows that predictor runtime materially changes driving performance under constrained planner tick rates.

### What the percentages do and do not mean

They support:

```text
prediction usefulness is planner- and induced-dynamics-dependent
```

They do **not** support a universal constant saying that 70–77% of all planning error in modern E2E/WAM systems is caused by reactivity. The paper itself uses selected planners and simulator oracle perception.

### Consequence for WAM experiments

A future-model paper can improve ADE/FDE, image fidelity, occupancy IoU or latent prediction loss without establishing a planning gain. Conversely, a model with worse static prediction can still be better for planning if its induced dynamics, computation budget or decision-relevant errors are better.

---

## 5. UniAD — exact future-to-planner path is mixed representation + explicit safety optimization

UniAD should not be simplified to “future occupancy goes into planner.” There are two distinct paths:

```text
MotionFormer:
track/map queries + ego query
→ joint multi-agent future reasoning
→ expressive ego query
→ planner trajectory prediction

OccFormer:
future occupancy prediction
→ occupancy-aware collision avoidance / optimization
→ post-prediction trajectory adjustment
```

The planner also attends to BEV features and is trained with collision loss.

### Planning ablation

At 3 s:

```text
base planner:                    L2 1.71, collision 1.64
+ BEV attention:                 L2 1.81, collision 1.58
+ collision loss:                L2 1.76, collision 1.39
+ occupancy optimization:        L2 1.81, collision 1.05
```

This is direct evidence that the system trades imitation similarity for collision reduction. It is **not** a clean ablation of “future prediction vs no future prediction,” because BEV attention, collision loss and occupancy-based optimization change different parts of the planner objective/interface.

### Correct control role

UniAD is therefore a control for:

```text
planning-oriented structured representation
+ auxiliary future tasks
+ explicit collision-aware planning
```

not a matched baseline for asking whether an inference-time generative world model helps.

---

## 6. NAVSIM terminology audit — “closed-loop metrics” does not make it closed-loop interaction

NAVSIM deliberately queries the policy only once from the initial real sensor observation, fixes the 4 s planned trajectory, rolls ego dynamics with an LQR + kinematic bicycle model, and leaves other agents on fixed/logged futures. The environment does not respond to ego action.

Therefore this project keeps the label:

```text
E3 = non-reactive pseudo-simulation
```

Some later papers describe NAVSIM as using “closed-loop metrics” because PDMS originates from simulation-style planning metrics. That phrase must not be allowed to silently upgrade the evaluation regime to reactive closed loop.

NAVSIM supports claims about short-horizon trajectory quality under safety/progress/comfort metrics on real sensor inputs. It does not directly support claims about:

```text
policy recovery after new observations
long-horizon compounding
intervention-dependent agent response
sensor-view shift after ego deviation
```

---

## 7. DiffusionDrive — the cleanest quantitative control is its matched Transfuser roadmap

### Strong matched comparison

DiffusionDrive uses the same Transfuser perception modules and ResNet-34 backbone in its NAVSIM study. The clean internal roadmap is:

```text
Transfuser       84.0 PDMS, 60 FPS
Transfuser_DP    84.6 PDMS,  7 FPS   (vanilla diffusion)
Transfuser_TD    85.7 PDMS, 27 FPS   (truncated diffusion)
DiffusionDrive   88.1 PDMS, 45 FPS   (truncated policy + new decoder)
```

This supports a mechanism-level decomposition much better than broad SOTA tables:

1. merely replacing deterministic regression with vanilla diffusion gives a small planning gain but severe runtime cost;
2. anchor-centered truncation improves both quality and efficiency;
3. the environment-interacting diffusion decoder contributes substantial additional gain.

The architecture ablation is especially informative:

```text
Transfuser_TD / UNet        85.7
+ spatial cross-attention   87.1
+ agent/map interaction     87.4
+ cascade decoder           88.1
```

The paper therefore supports “better multimodal action generation + better scene-conditioned trajectory decoding,” not future-world prediction.

### Denoising-depth correction

The result is nearly saturated at very shallow sampling:

```text
1 step 87.9
2 step 88.1
3 step 88.1
```

and cascade stages similarly saturate (`87.4 → 88.1 → 88.2` for 1/2/4 stages). Thus the planning gain should not be narrated as coming from deep iterative generative reasoning.

### Benchmark boundary

NAVSIM evidence remains E3/non-reactive. The nuScenes experiment is open-loop. DiffusionDrive is a strong control for action-distribution modeling and planner decoding, not reactive consequence modeling.

---

## 8. DriveSuprim — headline SOTA numbers require backbone and benchmark normalization

### NAVSIM v1: matched ResNet-34 comparison

The fairest comparison with DiffusionDrive is not DriveSuprim's headline `93.5`; it is the matched ResNet-34 row:

```text
DiffusionDrive R34  88.1 PDMS
DriveSuprim   R34  89.9 PDMS
```

so the matched-backbone difference is `+1.8 PDMS`.

The `93.5 PDMS` headline uses a ViT-Large backbone, while the corresponding Hydra-MDP ViT-L row is `89.9`. It is scientifically valid as a system result, but it is not a clean direct comparison to R34 DiffusionDrive.

### NAVSIM v2: metric/version change

NAVSIM v2 changes the metric from PDMS to EPDMS and adds direction, traffic-light, lane-keeping and revised comfort terms. Therefore:

```text
PDMS v1 numbers
!=
EPDMS v2 numbers
```

and cannot be numerically ranked across versions.

Within v2 and ResNet-34:

```text
HydraMDP++   81.4 EPDMS
DriveSuprim  83.1 EPDMS
```

The paper's ablation decomposes this `81.4 → 83.1` gain approximately as:

```text
+ multi-stage refinement   → 82.4
+ rotation augmentation    → 82.7
+ self-distillation        → 83.1
```

A parameter-control experiment reports that merely deepening the decoder gives about `+0.3`, while layer-wise scoring/filtering gives the larger improvement, supporting the coarse-to-fine selection interpretation.

### Oracle/headroom result

The top-K oracle study is one of the strongest Wave-1 controls against over-attributing candidate-selection gains to a WM:

```text
best within top-1 ranked candidate:   91.9 PDMS
best within top-4:                    94.5
best within top-16:                   96.1
best within top-256:                  98.7
human trajectory:                     94.8
```

This demonstrates that a large part of potential planning improvement can exist **inside an already generated candidate set** and be lost purely by imperfect ranking.

It does not prove that a WM cannot improve the candidate set or ranking; it proves that scorer/selection error is a serious competing causal explanation.

### Bench2Drive boundary

DriveSuprim's Bench2Drive result (`DS 83.02`, `SR 60.00`) is important because it supplies an interactive closed-loop result. But the paper states that this version is built on the CARLA-Garage dataset and TF++ framework and uses two-stage trajectory prediction for longitudinal control. It should therefore be treated as a **Bench2Drive system adaptation**, not assumed to be an identical deployment of the NAVSIM model.

---

## 9. Quantitative comparability matrix

| comparison | verdict | reason |
|---|---|---|
| M2I marginal vs GT-conditioned vs P1-conditioned | **STRONG MATCHED** | same task/model family; isolates conditioning-source quality |
| GameFormer vs DIPP before refinement | **USEFUL MATCHED** | same selected WOMD protocol; estimates learned-model advantage |
| GameFormer raw vs GameFormer + refinement | **STRONG MECHANISM DECOMPOSITION** | same model/protocol; directly exposes downstream planner contribution |
| GameFormer WOMD CL vs nuPlan CL-R | **NOT NUMERICALLY COMPARABLE** | different simulator/task/metrics and reactive assumptions |
| UniAD planner ablation | **USEFUL INTERNAL** | isolates planner ingredients, but not world-prediction-only effect |
| NAVSIM PDMS vs nuPlan CL score | **NOT COMPARABLE** | different interaction, rollout, input and aggregation regimes |
| DiffusionDrive vs Transfuser roadmap | **STRONG MATCHED** | aligned backbone/perception/training recipe; planning head changes are explicit |
| DiffusionDrive R34 88.1 vs DriveSuprim R34 89.9 on NAVSIM v1 | **REASONABLY COMPARABLE SYSTEM RESULT** | same benchmark/backbone class; still different supervision/input implementations |
| DiffusionDrive R34 88.1 vs DriveSuprim ViT-L 93.5 | **DO NOT USE AS METHOD-ONLY DELTA** | backbone capacity differs materially |
| NAVSIM v1 PDMS vs NAVSIM v2 EPDMS | **NOT COMPARABLE** | metric definition and required behaviors changed |
| DriveSuprim NAVSIM vs DriveSuprim Bench2Drive | **COMPLEMENTARY, NOT MATCHED** | different benchmark and system adaptation |

---

## 10. Wave-1 conclusions after comparability correction

### C1 — interaction modeling was already sophisticated before modern WAM

Supported by M2I and GameFormer, but the historical capability is best described as conditional/joint trajectory reasoning, not validated causal world simulation.

### C2 — better future prediction is not sufficient evidence for better planning

Supported by What Truly Matters and by the broader evaluation lineage. Planner coupling, induced dynamics and compute budget must be part of interpretation.

### C3 — future information can help through very different mechanisms

Already before WAM, future information reached planning through:

```text
conditional agent prediction
joint ego/agent trajectory reasoning
future occupancy
collision-aware optimization
```

So a WAM paper must specify exactly what new interface it adds.

### C4 — strong planning gains can arise entirely on the action/scoring side

DiffusionDrive and DriveSuprim establish two independent non-WM axes:

```text
better continuous/multimodal action generation
better candidate ranking / hard-negative discrimination
```

These are mandatory competing explanations for later WM improvements.

### C5 — benchmark labels must be treated as experimental assumptions

`open-loop`, `NAVSIM`, `closed-loop non-reactive`, `closed-loop reactive`, and `CARLA/Bench2Drive` are not interchangeable evidence levels. “Closed-loop metrics” is not synonymous with interactive closed-loop evaluation.

---

## 11. Gate decision

The five open comparability questions from the first Wave-1 synthesis are sufficiently resolved for the purpose of moving forward:

```text
M2I conditional-vs-causal boundary        RESOLVED FOR FIELD SYNTHESIS
GameFormer refinement contribution        RESOLVED
UniAD future→planner path                 RESOLVED AT ARCHITECTURAL LEVEL
DiffusionDrive vs DriveSuprim matching    RESOLVED WITH BACKBONE/VERSION FLAGS
nuPlan vs NAVSIM evidence meanings        RESOLVED AT PROTOCOL LEVEL
```

Wave 1 is therefore closed as a **historical/control baseline**. Exact implementation audits can still be reopened later if a Phase-B/C claim depends on one of these details.

Next scientific task: begin Wave 2 comparative deep read of `GAIA-1 → Drive-WM → OccWorld → WoTE → ViDAR → LAW`, using Wave 1 as the control coordinate system and refusing to attribute planning gains to “world modeling” until representation, supervision, action modeling, scorer and evaluation alternatives are separated.