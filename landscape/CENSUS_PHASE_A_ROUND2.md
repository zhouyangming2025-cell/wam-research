# CENSUS_PHASE_A_ROUND2 — Coverage-Hole Scientific Placement

Last updated: 2026-09-14

Status: **CENSUS DEPTH — FIELD PLACEMENT, NOT GAP ANALYSIS**

Purpose: scientifically place the 14 coverage works `P0021–P0034` that were acquired by the local corpus agent after Census Round 1. This pass uses the common taxonomy in `landscape/PLANNING_WAM_TAXONOMY.md` and the repo-hosted primary-paper raw Markdown. It does not issue novelty/gap verdicts and does not treat every work as a world model.

## 1. Placement rules

Three distinctions are enforced throughout this pass:

```text
future prediction used for pretraining
!= future model used at planning inference
!= world model used as an RL training environment
```

```text
multimodal / generative trajectory planning
!= world modeling
```

```text
counterfactual language/rule supervision
!= intervention-dependent reactive world prediction
```

Evaluation labels follow the project taxonomy: `E2` open-loop ego planning, `E3` NAVSIM-style non-reactive pseudo-simulation, `E4/E5` closed-loop non-reactive/reactive data-driven simulation, `E6` CARLA/Bench2Drive interactive simulation, `E7` real-vehicle closed loop. Decision-evidence labels are about evidence for planning claims, not overall paper quality.

---

## 2. Compact placement matrix

| ID / work | family placement | state / mechanism | WM role | action / interaction | planner interface + output | supervision | evaluation / evidence | historical role + boundary |
|---|---|---|---|---|---|---|---|---|
| **P0021 Hydra-MDP** | F10 strong non-WM planner; F9 score/cost interface | current image+LiDAR environmental tokens + fixed trajectory vocabulary + learned metric subscores | **no explicit WM** | candidate ego trajectory; no modeled intervention-dependent response (`I0`) | learned imitation + rule-metric cost over candidates; `CANDIDATE_SET_AND_SCORE` | expert ego trajectory + offline simulation/rule metric distillation | NAVSIM `E3`; `D2` | Important early modern selection/distillation planner. Boundary: fixed vocabulary, learned scores from non-reactive metric teachers rather than imagined future world rollout. |
| **P0022 DriveSuprim** | F10 strong non-WM planner; F9 trajectory evaluator | image features + fixed trajectory vocabulary; coarse-to-fine hard-negative scoring | **no explicit WM** | candidate ego trajectory; no explicit reactive agent response (`I0`) | progressive candidate filtering/refinement + scorer; `CANDIDATE_SET_AND_SCORE` | expert trajectory + rule/safety metrics + self-distilled soft labels + rotation augmentation | NAVSIM v1/v2 `E3`; Bench2Drive `E6`; `D2` | Shows selection quality itself is a major planning axis: hard-negative discrimination, directional bias, and hard labels can dominate performance without a WM. |
| **P0023 iPad** | F10 strong non-WM planner; planning-centric representation boundary | sparse proposal-centric BEV queries iteratively refined from multi-view images; proposal-specific map/passability and relevant-agent auxiliary futures | **no full WM; auxiliary future prediction** | dynamic ego proposals; auxiliary prediction is proposal-relevant, not demonstrated intervention-response dynamics (`I2` boundary) | proposal-centric feature extraction → iterative proposal refinement → scorer; `CANDIDATE_SET_AND_SCORE` | expert trajectory + map/passability + agent-trajectory auxiliary supervision | NAVSIM `E3`; Bench2Drive `E6`; `D2` | Important control showing representation can be organized around planning proposals rather than dense world state. Boundary: proposal-conditioned relevance is not a candidate-specific reactive world model. |
| **P0024 DriveVLM / DriveVLM-Dual** | F10 VLM/VLA planning control | image sequence → language scene description / critical-object analysis → meta-action / decision text → waypoints; Dual adds 3D perception + fast conventional planner | **no WM** | route + ego pose/velocity; semantic reasoning about object influence, no learned action-conditioned scene dynamics | hierarchical semantic reasoning → low-frequency trajectory; Dual refines at high frequency; `HIERARCHICAL_INTENT_TRAJECTORY` | language/SUP annotations + planning waypoints + traditional 3D module signals | nuScenes/SUP open-loop `E2`; production-vehicle deployment reported qualitatively; `D2` plus non-standardized real-vehicle evidence | Early VLM planning / slow-fast hybrid anchor. Authors explicitly motivate Dual by VLM spatial-grounding and computational limitations. |
| **P0025 OmniDrive** | F10 VLM-data/agent branch; supervision/evaluation adjunct | 3D scene structure + simulated trajectories + rule checklist → counterfactual Q&A; Omni-L/Q vision-language agents | **no WM** | simulated trajectory prompts in data generation; no environment response to ego intervention (`I0`) | VLM reasoning + open-loop trajectory generation | `COUNTERFACTUAL_PROXY` language QA + rule checks + expert trajectory + 3D perception supervision | nuScenes open-loop `E2`; `D2` | Important distinction: counterfactual reasoning can be a **data/supervision strategy** without being a counterfactual world model. |
| **P0026 ORION** | F10 VLA/generative planner control | multi-view/history → QT-Former scene/history tokens → LLM planning token → generative multimodal trajectory planner | **no explicit WM** | instruction/route/ego context; motion-prediction auxiliaries but no ego-action-conditioned surrounding response | differentiable reasoning-space → action-space bridge; `TRAJECTORY_DISTRIBUTION` | VQA/reasoning + expert trajectory + perception/motion auxiliary losses | Bench2Drive `E6`; `D2` | Strong modern VLA control: semantic world knowledge and generative action can yield closed-loop gains without an explicit future WM. “Causal reasoning” is author framing, not evidence of causal environment dynamics. |
| **P0027 Think2Drive** | F3 latent dynamics; F8 WM-RL / policy-learning | privileged structured CARLA state → DreamerV3-style RSSM latent state; latent transition predicts next state/reward/termination | `RL_ENVIRONMENT / POLICY_IMPROVER` | policy/control action conditions latent transition; action-dependent environment model, but social-reaction correctness is not separately established | latent imagination → actor/critic/policy learning; `POLICY_ACTION / CONTROL_SEQUENCE` | environment transitions + reconstruction + reward + termination + closed-loop RL signal | CARLA-v2 `E6`; `D2` | Essential separate WM lineage: WM is mainly a **neural simulator for policy training**, not a raw-sensor future representation consumed by a deployed planner. Uses privileged state to remove perception. |
| **P0028 ViDAR** | F3 predictive-representation pretraining; representation→planning bridge | historical images → BEV latent → Latent Rendering → autoregressive future occupancy/point-cloud forecast | `PRETRAINING_REPRESENTATION` | history-only, no ego action conditioning (`I1` at most) | future decoder shapes encoder during pretraining; downstream planner consumes pretrained representation (`P1`) | future geometry from image–LiDAR sequences | forecasting `E1` + downstream nuScenes planning `E2`; matched pretraining evidence `D3` | Clean example where “world prediction” is a **training-time pretext task**. Boundary: future decoder need not survive in downstream planning inference; LiDAR supplies pretraining targets. |
| **P0029 GenAD** | F7 integrated prediction/planning; F6 trajectory-level world-action precursor | map-aware agent/ego tokens → VAE structural trajectory latent + temporal GRU → jointly generated ego and agent futures | reduced `UNIFIED_WORLD_ACTION_MODEL` precursor at trajectory/behavior level | ego and agents are co-generated; no explicit alternative ego intervention controlling other-agent response (`I2`) | joint future trajectory generation for motion prediction + ego planning; `TRAJECTORY_DISTRIBUTION` | agent trajectories + expert ego trajectory + detection/map tasks | nuScenes open-loop `E2`; `D2` | Important precursor to later world-action language: prediction and planning are jointly generated in one future latent. Boundary: joint generation is not reactive counterfactual rollout. |
| **P0030 nuScenes** | F11 dataset / evaluation ancestor | multimodal sensor dataset + 3D boxes/maps; original tasks are detection/tracking/scene understanding | none | none | no native planning interface | perception/tracking annotations | original paper: perception/prediction benchmark, **not a planning benchmark**; planning evidence `D0` | Critical correction to field history: later E2E literature retrofitted open-loop trajectory/L2 planning protocols onto nuScenes logs; that protocol is not the original paper’s benchmark design. |
| **P0031 nuPlan** | F11 planning benchmark | large real-log dataset + planning goals/metrics + lightweight closed-loop simulator | simulator/evaluation infrastructure, not planner WM | supports non-reactive logged agents and reactive agent planners | evaluates submitted planner trajectories through controller/simulation | benchmark data + scenario/metric definitions | `E2` OL + `E4` CL-NR + `E5` CL-R | Foundational benchmark transition from prediction-style OL metrics to planning-specific closed-loop evaluation. Boundary: deviated ego sensor views are not warped/generated, limiting raw-sensor closed-loop fidelity. |
| **P0032 NAVSIM** | F11 benchmark; F9 metric-teacher influence | real sensor initial frame + fixed planned 4s trajectory → non-reactive BEV rollout + PDMS | evaluation simulator, not learned WM | policy queried once; environment explicitly does **not** respond (`I0`) | no planner interface beyond scoring submitted trajectory | no model supervision in benchmark itself; PDMS later becomes supervision/teacher for many planners | `E3` non-reactive pseudo-simulation | Major benchmark transition: scalable real-data, simulation-based planning metrics without sensor generation. Its explicit non-reactivity and short horizon are defining assumptions, not implementation details. |
| **P0033 Bench2Drive** | F11 interactive E2E benchmark | CARLA-v2 sensor simulation + 44 interactive scenarios + standardized expert training dataset | simulator/evaluation infrastructure | ego actions influence environment; interactive scenario simulation (`I7`) | evaluates end-to-end policy/trajectory/control | standardized CARLA expert dataset; Think2Drive expert provides data | `E6` CARLA interactive closed loop | Establishes granular multi-ability closed-loop comparison for E2E driving and reduces long-route score variance. Boundary: synthetic CARLA domain and scenario-centric short routes are not real-world closed loop. |
| **P0034 HUGSIM** | F8 reactive/closed-loop simulation; F11 benchmark | reconstructed real scenes using dynamic 3D Gaussian Splatting + physical actor/ground priors; ego/actors updated online | `SIMULATOR_ONLY`, potential RL environment | ego waypoints/control affect simulation; normal actors use IDM, aggressive actors use attack strategy (`I7` by simulator design) | external planner queried in photorealistic sensor loop | reconstructed real scenes + physical/rule actor dynamics | photorealistic interactive closed-loop simulation (`E5`/simulator class, not `E7`) | Bridges game-engine synthetic simulation and log-based pseudo-simulation with real-scene photorealistic closed loop. Boundary: photorealistic rendering does not itself establish behavioral realism of traffic agents. |

---

## 3. What Round 2 adds to the field map

### 3.1 Strong planning without an explicit world model is a first-class control branch

Hydra-MDP, DriveSuprim, iPad, DriveVLM/OmniDrive/ORION show multiple ways to improve planning without predicting a future world state at inference:

```text
metric distillation / candidate scoring
coarse-to-fine hard-negative selection
proposal-centric feature extraction
semantic VLM reasoning
counterfactual language supervision
generative trajectory decoding
```

Therefore later Phase-B comparisons must ask whether a WM contributes something beyond stronger planning representation, supervision, candidate generation, or scoring.

### 3.2 “World model” has at least three very different roles even inside the new coverage set

```text
ViDAR       = future prediction as PRETRAINING OBJECTIVE
Think2Drive = latent dynamics as RL TRAINING SIMULATOR
GenAD       = joint EGO+AGENT FUTURE TRAJECTORY GENERATION
```

None is interchangeable with an inference-time video/BEV/latent rollout used to select the deployed ego action.

### 3.3 VLA/VLM planning is adjacent to WAM, not synonymous with it

DriveVLM, OmniDrive and ORION bring language priors, reasoning, hierarchical actions, counterfactual supervision and generative trajectory decoding into E2E driving. These are important controls because strong semantic reasoning can improve planning without a learned environment transition model.

### 3.4 Benchmark evolution is part of the technical history, not a neutral backdrop

The sequence now becomes clearer:

```text
nuScenes
  original multimodal perception/scene dataset
  ↓ community later retrofits open-loop planning metrics
nuPlan
  planning goals + OL / CL-NR / CL-R protocols
  ↓
NAVSIM
  scalable real-sensor non-reactive pseudo-simulation + planning metrics
  ↓
Bench2Drive
  standardized CARLA interactive closed-loop, skill-disentangled scenarios
  ↓
HUGSIM
  reconstructed real-scene photorealistic closed-loop sensor simulation
```

A reported planning gain cannot be interpreted independently of which point on this evaluation ladder is used.

### 3.5 Multimodality also means different things across the field

Round 2 reinforces at least four non-equivalent meanings:

```text
multiple candidate trajectories              — Hydra-MDP / DriveSuprim
learned dynamic proposal distribution         — iPad
probabilistic joint ego/agent trajectory      — GenAD
semantic/generative trajectory alternatives   — ORION
```

This must not be collapsed into “models uncertainty” without checking whether the planner actually uses probabilities/branches in decision making.

---

## 4. Coverage implications for Phase-A closeout

After integrating Round 2 with Census Round 1, the field has representative coverage for:

- visual/video generative WMs;
- BEV/occupancy/geometric WMs;
- latent/JEPA/predictive representation WMs;
- inference-time WM-assisted planning;
- candidate/action-conditioned futures;
- unified world-action modeling;
- interactive prediction/planning predecessors;
- WM-RL/policy-improvement lineage;
- reactive and photorealistic simulation;
- reward/value/safety/cost interfaces;
- strong non-WM trajectory-selection, diffusion and VLA controls;
- benchmark evolution from open-loop logs to non-reactive and interactive closed-loop simulation.

Two weaknesses remain visible but do **not** justify another broad acquisition round:

1. **Standardized real-vehicle closed-loop evidence is sparse.** DriveVLM reports production-vehicle deployment, but this is not a common benchmark comparable to NAVSIM/Bench2Drive.
2. **Uncertainty consumption is under-standardized.** Many papers generate multiple futures/trajectories, but how probability/uncertainty reaches action selection differs widely and requires Phase-B comparative reading rather than more census accumulation.

`Hydra-MDP++` and `NAVSIM-v2` can be added later if a Phase-B comparison specifically requires them; neither is necessary to explain the current family structure.

## 5. Phase-A verdict

```text
COVERAGE AUDIT: PASS AT CENSUS DEPTH
BROAD EXPANSION: FREEZE
GAP DISCOVERY: STILL CLOSED
NEXT: SELECT + DEEP-READ REPRESENTATIVE PHASE-B ANCHORS
```

The pass means the map is sufficiently broad to choose representative deep reads. It does **not** mean the field is fully understood yet; that is the purpose of Phase B and cross-family synthesis.