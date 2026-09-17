# D01.3 Source and Artifact Freeze

This file was written only after the selected set and fixed seed were sealed in 01_BLIND_SELECTION_PREREGISTRATION.md. It freezes the source boundary and reconstructs deployment/learning objects in ordinary language. It intentionally does not assign any R/W/E, C/X/D/P/V/T/L, or other ontology code.

## 1. Frozen source boundary

| paper | exact source identity | local source | local Git blob | code boundary |
|---|---|---|---|---|
| GraphAD | *GraphAD: Interaction Scene Graph for End-to-end Autonomous Driving*; local paper record for arXiv 2403.19098 lineage | papers/raw_md/P0003_GraphAD/P0003_GraphAD.raw.md | f10b1b4c58cbea87420482bb631f56cdbe389f68 | No local implementation; paper says code will be released at github.com/zhangyp15/GraphAD. No code fact is asserted. |
| DriveDreamer | *DriveDreamer: Towards Real-world-driven World Models for Autonomous Driving*; arXiv 2309.09777 lineage, ECCV 2024 version represented by the local record | papers/raw_md/P0036_DriveDreamer/P0036_DriveDreamer.raw.md | b59066c13a92bc810b8423ef7b2a7fd8bca108ac | Project page is recorded in the paper. No local implementation/commit was inspected; code-level claims remain UNKNOWN. |
| DrivoR | *Driving on Registers* / DrivoR; CVPR 2026 camera-ready record | papers/raw_md/P0060_DrivoR/P0060_DrivoR.raw.md | 3f49601110eeb1a66970a2d703b5a2d2ceda529d | Paper reports code/checkpoints through its project page, but no local implementation/commit was inspected. |

The raw papers are sufficiently detailed to reconstruct the primary mechanism. The absence of a local code checkout is an evidence limitation, not a reason to replace a selected paper.

## 2. GraphAD deployment DAG

### Terminal path

\`\`\`text
multi-camera history + camera calibration + ego poses + ego status + route command
  → image encoder and temporal BEV aggregation
  → structured traffic-agent nodes and map-element nodes
  → interaction graph built from geometry and predicted future trajectories
  → graph aggregation updates dynamic-node features and trajectory predictions
  → processed ego node + ego status + command
  → planning head
  → one ego trajectory
  → optional occupancy-based post-optimization for collision avoidance
\`\`\`

### What is causally important

- **PAPER FACT:** dynamic nodes carry multi-modal future trajectory proposals; those proposals determine geometric neighbors in the dynamic/static interaction graphs.
- **PAPER FACT:** graph aggregation updates dynamic features, and updated dynamic features produce new trajectory points and modality probabilities in successive graph layers.
- **PAPER FACT:** the processed ego query is consumed by a planning head that predicts the ego trajectory.
- **PAPER FACT:** the paper describes an occupancy prediction head whose prediction can post-optimize the planning trajectory.
- **OUR INFERENCE:** the predicted surrounding-agent future is a future/consequence object that can qualify as a world carrier because it is localizable, temporally structured, explicitly motion-supervised, and connected to planning through the graph.
- **UNKNOWN:** whether the occupancy post-optimization is a pure refinement or internally enumerates and resolves identity-preserving ego candidates. The paper does not establish a common candidate resolver for the final ego action.
- **UNKNOWN:** exact implementation behavior of the released repository, because no code commit was inspected.

### Candidate and commitment facts

The six modalities described for each dynamic agent are prediction alternatives used to construct interactions. They are not, on the available paper evidence, six ego actions sent to one final selector. The final planning head is described as predicting an ego trajectory, and the occupancy post-optimization is described as trajectory optimization rather than a common candidate-bank resolver.

### Deployment fate

Retain the image/BEV encoder, structured node extraction, interaction graph, motion prediction, planning head, and the reported occupancy safety path when using the full paper model. No teacher, simulator, or heavy external consequence model is documented as being deleted after training.

## 3. GraphAD learning DAG

\`\`\`text
ImageNet-initialized image backbone
  → stage 1: detection + vectorized map training
  → freeze image backbone
  → stage 2: tracking + map + graph-based motion prediction
  → stage 3: add occupancy prediction + planning
  → summed depth + tracking + map + motion + occupancy + planning losses
  → retained end-to-end planning system
\`\`\`

- **PAPER FACT:** the paper states three training stages and explicitly freezes the image backbone in the second stage.
- **PAPER FACT:** motion, occupancy, and planning losses are part of the multi-task objective in the final stage.
- **PAPER FACT:** no detach/stop-gradient edge is specified for the graph-to-planning path.
- **OUR INFERENCE:** future motion supervision shapes the shared representation and the retained planning path through multi-task training.
- **UNKNOWN:** exact parameter scopes and whether the occupancy post-optimization has any separate training-time detach boundary.

## 4. DriveDreamer deployment artifacts

The paper contains two materially different terminal paths. They are frozen as separate artifacts rather than forcing one paper-level object.

### DD-VIS — controllable future-video generation

\`\`\`text
initial image + initial road structure + supplied action sequence + optional text
  → action-conditioned structural future prediction
  → diffusion-based future video generation
  → future driving video
\`\`\`

- **PAPER FACT:** the first output is a sequence of future driving videos conditioned by initial observation, structured traffic conditions, text, and supplied driving actions.
- **PAPER FACT:** the action-conditioned structural predictor recursively produces future structural conditions that are fed to the video generator.
- **PAPER FACT:** the terminal product of this mode is generated video; no final ego-action selector is described.
- **OUR INFERENCE:** the generated future video/structural sequence is a deployed world/consequence output in this mode.
- **UNKNOWN:** whether an external controller is always required in the project implementation and which hidden diffusion features, if any, are exposed to downstream planning.
- **Deployment fate:** retain the video-generation path for this mode; there is no action commitment path to retain.

### DD-ACT — future action generation from the world-model stack

\`\`\`text
initial image + initial road structure + past driving actions
  → recurrent action-conditioned future structural prediction
  → diffusion/world-model features for future visual states
  → action decoder using pooled world-model features + historical action features
  → predicted future driving-action trajectory
\`\`\`

The paper describes the video and future-action branches as jointly produced by the second-stage model, but evaluates the future action trajectory as the planning output.

- **PAPER FACT:** future actions are predicted from pooled multi-scale Auto-DM features and historical action features.
- **PAPER FACT:** the same second-stage training includes future-video prediction and future-action prediction losses.
- **PAPER FACT:** the paper reports open-loop trajectory evaluation, not a final common resolver over multiple candidate trajectories.
- **OUR INFERENCE:** the retained action path is conditioned by generated/intermediate future-world computation rather than merely by a static visual encoder.
- **UNKNOWN:** whether the paper's action-generation evaluation should be treated as a single joint world/action emission or as a world-conditioned action head in the exact deployed implementation.
- **UNKNOWN:** closed-loop control-cycle behavior and exact retain/drop boundaries for the video decoder versus its internal features.

### DriveDreamer learning DAG

\`\`\`text
single-frame structured-image diffusion training
  → multi-frame structured-video diffusion training
  → action-conditioned future structural prediction
  → joint future-video and future-action prediction
  → open-loop action evaluation and world/video generation
\`\`\`

- **PAPER FACT:** the first stage learns structured traffic constraints from images and videos.
- **PAPER FACT:** the second stage uses an initial observation, action sequence, future video targets, and future action targets.
- **PAPER FACT:** the paper states that the original Stable Diffusion parameters are frozen while trainable components are optimized; exact complete parameter scopes are not fully specified in the raw record.
- **OUR INFERENCE:** the two-stage predictive/generative program transfers world knowledge into both the video-generation and action-generation branches.
- **UNKNOWN:** exact stop-gradient/detach boundaries, the deployed status of the video decoder during action inference, and any official code commit.

## 5. DrivoR deployment DAG

\`\`\`text
multi-camera images + ego status + driving command
  → pretrained ViT with camera-aware register tokens
  → compact scene tokens
  → trajectory decoder with learned queries
  → multiple candidate ego trajectories
  → re-embed each decoded trajectory and detach it from trajectory-decoder gradients
  → scoring decoder attends to candidate trajectory and scene tokens
  → sub-scores for safety/comfort/progress/other driving outcomes
  → weighted score and argmax
  → committed ego trajectory
\`\`\`

- **PAPER FACT:** the model explicitly generates multiple candidate trajectories and scores them with a separate decoder.
- **PAPER FACT:** the final trajectory is selected from the proposal set by the maximum predicted score.
- **PAPER FACT:** the scorer predicts decomposed driving-quality components and allows inference-time weight changes.
- **PAPER FACT:** no future scene, transition model, occupancy rollout, or action-conditioned environment consequence is described as an input to the scorer.
- **OUR INFERENCE:** candidate identity persists from trajectory generation through scoring and the common maximum-score resolver.
- **OUR INFERENCE:** the future time points inside each candidate trajectory are actions/trajectory outputs, not a separately predicted world consequence.
- **UNKNOWN:** exact released-code behavior and project-page commit.

### DrivoR learning DAG

\`\`\`text
pretrained visual backbone
  → LoRA/backbone and register-token adaptation
  → winner-takes-all trajectory regression against human trajectory
  → oracle sub-score supervision for the scoring decoder
  → shared perception encoder receives both trajectory/scoring training
  → scoring gradients are blocked from the trajectory decoder
  → both proposal and scoring branches retained at inference
\`\`\`

- **PAPER FACT:** trajectory proposals use WTA/minimum-over-n supervision.
- **PAPER FACT:** scoring heads are trained with BCE against oracle sub-score components.
- **PAPER FACT:** scoring gradients reach the perception encoder but are prevented from flowing into the trajectory decoder.
- **PAPER FACT:** the final loss combines trajectory and scoring losses.
- **OUR INFERENCE:** the oracle scorer is training-time supervision for a deployed scorer; it is not itself an online world model.
- **UNKNOWN:** whether the project implementation contains any additional post-processing not described in the paper.

## 6. Evidence boundary summary

| artifact | paper fact sufficient for mechanism? | code fact | main unresolved boundary |
|---|---|---|---|
| GraphAD planning | yes for the high-level DAG | none | occupancy post-optimization and exact iterative deployment semantics |
| DriveDreamer future video | yes for the terminal generation path | none | controller/external-control and internal-feature exposure |
| DriveDreamer action generation | yes for the two-branch predictive training path | none | joint-emission versus world-conditioned action interpretation |
| DrivoR planning | yes for candidate generation, scoring, and commitment | none | released-code post-processing |



