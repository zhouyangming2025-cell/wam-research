# Auto-JEPA: A Latent World Model of Continuous Intent for End-to-End Autonomous Driving

Jiwei Yang<sup>1</sup>, Zhengxian Chen<sup>1,2†</sup>, Chaosheng Huang<sup>1</sup>, Jun Li<sup>1</sup>

<sup>1</sup>School of Vehicle and Mobility, Tsinghua University

<sup>2</sup>State Key Laboratory of Intelligent Green Vehicle and Mobility, Tsinghua University chenzhengxian@tsinghua.vin

## Abstract

Existing autonomous-driving world models typically perform dense prediction of future videos, occupancy states, BEV representations, or agent motion. We argue that planning need not reconstruct the complete future world, but only focus on scene features that afect future ego action. Based on this perspective, we propose Auto-JEPA, an action-oriented latent world model that learns continuous future driving intent through joint-embedding prediction. Given visual observations, egomotion history, and navigation commands, Auto-JEPA predicts an intent embedding aligned with the latent representation of the future ego trajectory. The predicted intent retrieves executable trajectories from a fixed trajectory memory, which are then ranked by a scene-conditioned candidate selection module. Auto-JEPA keeps the visual encoder frozen, requires no explicit perception annotations, and uses no learned trajectory generator. By optimizing only task-specific modules for trajectory representation, intent prediction, and candidate selection, Auto-JEPA achieves 91.3 PDMS on NAVSIM v1 and 89.1 EPDMS on NAVSIM v2. Semantic occlusion experiments show that masking dynamic-agent regions induces an average intent change 2.97× that of equal-area random masking. Moreover, occluding vehicles that afect future driving substantially changes the predicted intent and selected trajectory, whereas both remain essentially unchanged when non-influential vehicles are occluded. These results show that future-intent prediction encourages the model to focus on planning-relevant visual features and supports high-quality planning without dense future-world modeling. Code & Models: https://github.com/NoctYang/Auto-JEPA.

## Introduction

World models ofer a compelling route toward autonomous driving systems that can reason about how a scene may evolve before committing to an action. Many driving world models, however, formulate this objective as dense future prediction, generating future multiview observations, occupancy fields, or latent states that describe the evolution of the surrounding scene (Wang et al. 2023b; Zheng et al. 2023; Zhang et al. 2026; Jia et al. 2026). A parallel line of work explicitly forecasts the future trajectories and interactions of multiple trafic participants (Sef et al. 2023). Although these objectives preserve rich information about the environment, they require the model to allocate substantial capacity to scene elements whose dynamics may have little influence on the ego vehicle’s immediate decision. Predicting all observable entities without regard to their planning relevance can therefore increase computation and propagate perception and forecasting errors into downstream planning.

![](images/34a77169b501b9a3b92d4790bb8f291166a71b7b45f1c458f85a83968248e253.jpg)  
Figure 1: Selective response to action-relevant scene information. Occluding a non-interacting vehicle causes little change in the predicted intent and plan, whereas occluding the interacting lead vehicle shifts the intent and selected trajectory. Annotations are used only for analysis.

We argue that a planning-oriented predictive model need not reconstruct the complete future state of a scene, but only focus on scene features that afect future ego action. Based on this perspective, we introduce Auto-JEPA, an actionoriented latent world model that learns continuous future driving intent through joint-embedding prediction. Given visual observations, ego-motion history, and a navigation command, it predicts a future ego-trajectory latent whose temporal tokens encode motion geometry and dynamics. Recent work explores planning-aligned latent prediction (Li et al. 2025b; Zheng et al. 2025; Wang et al. 2026; Xie et al. 2026), primarily for representation pretraining, auxiliary supervision, or action distillation. Auto-JEPA uses future egotrajectory latents for trajectory retrieval.

Auto-JEPA first trains a trajectory encoder and then freezes it to define the future-trajectory target space. Following joint-embedding predictive learning (Assran et al. 2023;

Bardes et al. 2024), a visual predictor infers the corresponding future-trajectory latent from the current scene context, ego-motion history, and route command. Latent alignment and contrastive objectives train the predictor without futureimage reconstruction. Because its prediction target is defined solely by future ego motion, the model need not preserve all observable scene content and is encouraged to prioritize planning-relevant visual features. At inference, the predicted intent directly serves as the retrieval key of a fixed trajectory memory, and a scene-conditioned module selects the final executable candidate.

The trajectory memory contains recorded, kinematically plausible trajectory geometries encoded by the same trajectory encoder. A scene-conditioned scorer ranks the retrieved candidates, and a learned drivable-area gate screens candidates likely to violate drivable-area constraints before final selection. This design separates complementary responsibilities: the latent predictor determines what kind offuture motion is appropriate, retrieval provides explicit trajectory geometry, the scorer estimates scene-level driving quality, and the gate reduces drivable-area violations. Although these components are optimized in stages, Auto-JEPA preserves an end-to-end sensor-to-trajectory planning interface without intermediate perception outputs or a learned trajectory generator.

We evaluate Auto-JEPA on NAVSIM v1 and NAVSIM v2 (Dauner et al. 2024). Under this lightweight setting, Auto-JEPA achieves 91.3 PDMS on NAVSIM v1 and 89.1 EPDMS on NAVSIM v2. Figure 1 illustrates the diferent efects of individual vehicles within the same scene: occluding the interacting lead vehicle substantially changes the predicted intent and selected trajectory, whereas both remain essentially unchanged when the non-interacting adjacent vehicle is occluded. To quantify sensitivity to trafic-participant information at the dataset level, we further conduct controlled semantic occlusions on the full validation split. Masking dynamicagent regions induces an average intent change 2.97× that of equal-area random masking and a larger change in 71.1% of scenes.

Our main contributions are summarized as follows:

• We formulate planning-oriented latent world modeling as future ego-trajectory latent prediction. Using continuous driving intent as the prediction target encourages the model to focus on visual features relevant to ego action, thereby avoiding dense future-scene reconstruction.

• We propose Auto-JEPA, which maps visual context into a future-trajectory latent space through joint-embedding prediction. The predicted intent directly retrieves executable candidates from a fixed trajectory memory, followed by scene-conditioned selection.

• Auto-JEPA achieves 91.3 PDMS on full NAVSIM v1 navtest and 89.1 EPDMS on NAVSIM v2; controlled semantic occlusion experiments further show that the model selectively focuses on more critical scene features.

## Related Work

## World Models for Autonomous Driving

Driving world models predict scene evolution in pixel or structured spaces for simulation, representation learning, and planning. Generative approaches synthesize controllable future driving videos from observations, actions, or language (Hu et al. 2023; Wang et al. 2023a,b; Gao et al. 2024), while structured alternatives forecast future occupancy or point clouds (Zheng et al. 2023; Yang et al. 2023). Although these representations capture rich appearance and geometry, they require dense prediction over broad scene content, including details that need not determine the immediate ego plan.

Latent world models reduce explicit reconstruction by forecasting compact future features. LAW, World4Drive, DeepSight, and DriveWorld-VLA predict future scene features, BEV states, or action-conditioned scene evolution for downstream planning (Li et al. 2025b; Zheng et al. 2025; Zhang et al. 2026; Jia et al. 2026). Their targets nevertheless primarily describe how the surrounding scene evolves. Auto-JEPA instead predicts the representation of future ego motion itself, retaining scene dynamics through their implications for the planned trajectory.

## Joint-Embedding Predictive Learning

Joint-embedding predictive architectures learn by predicting target representations rather than reconstructing observations. I-JEPA establishes this principle for images (Assran et al. 2023), V-JEPA extends it to video (Bardes et al. 2024), and V-JEPA 2 further demonstrates that self-supervised video representations can support understanding, prediction, and planning (Assran et al. 2025). Drive-JEPA adapts this family to driving-video pretraining and trajectory distillation (Wang et al. 2026). Auto-JEPA difers in the operational role of prediction: the future ego-trajectory latent directly serves as the planner’s retrieval key and therefore participates in trajectory planning at inference rather than only supporting training-time representation learning.

## End-to-End Trajectory Planning

End-to-end driving maps sensor observations and navigation context directly to an ego trajectory, but a single logged future provides limited coverage of multiple feasible maneuvers. Existing methods score candidates from ofline trajectory vocabularies (Jiang et al. 2024; Li et al. 2024; Sun et al. 2026), generate or refine proposals (Liao et al. 2025; Xing et al. 2025; Guo et al. 2025), or combine a learned generator with a trajectory scorer (Ang et al. 2026). Latent trajectory nearest-neighbor search has also been explored for motion forecasting rather than ego planning (Biktairov et al. 2020).

Recent VLA planners tokenize or decode ego actions from visual and language context (Zhou et al. 2025b,a; Li et al. 2026a). They learn parametric action decoders, whereas Auto-JEPA predicts a continuous future-ego-motion intent latent for non-parametric trajectory retrieval.

## Method

## Overview

Auto-JEPA predicts a continuous future ego-motion representation and uses it to retrieve executable trajectories. Given four front-camera frames, four historical ego positions, and a route command, a frozen V-JEPA 2 encoder (Assran et al. 2025) extracts visual tokens, and a Transformer predictor fuses visual, motion, and route context to produce eight temporal latent tokens representing one continuous driving intent. Figure 3 presents the complete training and inference pipeline.

During training, the predicted intent is aligned with the representation of the ground-truth future trajectory produced by a frozen trajectory encoder. At inference, it retrieves the 300 most similar trajectories from a non-parametric memory; a scene-conditioned scorer ranks these candidates and a learned drivable-area gate filters infeasible proposals. This separates intent prediction, trajectory instantiation, quality ranking, and feasibility filtering without reconstructing future observations or directly regressing waypoint coordinates.

## Future Ego-Motion Intent Representation

Figure 2 details the two-stage learning process: trajectoryspace pretraining followed by visual intent prediction. For each driving scene, we represent the ground-truth future ego trajectory as eight two-dimensional waypoints,

$$
\mathbf { Y } = [ ( x _ { 1 } , y _ { 1 } ) , \ldots , ( x _ { 8 } , y _ { 8 } ) ] \in \mathbf { R } ^ { 8 \times 2 } .\tag{1}
$$

Before training the visual intent predictor, we learn the target space with a trajectory autoencoder composed of a trajectory encoder $E _ { \mathrm { t r a j } }$ and a lightweight decoder $D _ { \mathrm { t r a j } }$ . The encoder maps a future trajectory to a sequence of latent tokens, and the decoder reconstructs the trajectory from this representation,

$$
\mathbf { Z } ^ { + } = E _ { \mathrm { t r a j } } ( \mathbf { Y } ) \in \mathbf { R } ^ { 8 \times 1 0 2 4 } , \qquad \hat { \mathbf { Y } } = D _ { \mathrm { t r a j } } ( \mathbf { Z } ^ { + } ) .\tag{2}
$$

The autoencoder is optimized using a trajectory reconstruction objective,

$$
\mathcal { L } _ { \mathrm { t r a j } } = \mathcal { L } _ { \mathrm { x y } } + \lambda _ { e } \mathcal { L } _ { \mathrm { e n d } } + \lambda _ { v } \mathcal { L } _ { \mathrm { v e l } } + \lambda _ { a } \mathcal { L } _ { \mathrm { a c c } } ,\tag{3}
$$

where the four terms supervise waypoint coordinates, the final endpoint, velocity, and acceleration, respectively. After this pretraining stage, the decoder is discarded and $E _ { \mathrm { t r a j } }$ is frozen. The frozen encoder then defines the target latent $\mathbf { Z } ^ { + }$ for intent prediction and encodes every trajectory in the retrieval memory, ensuring that prediction targets and retrieval candidates occupy the same latent space.

The eight latent tokens preserve trajectory time, geometry, and motion and jointly describe one continuous future realization rather than eight maneuver classes. We refer to this representation as the driving intent. Using the same encoder for supervision and memory construction places predicted intents and executable trajectories in a shared space, allowing the intent latent to serve directly as the retrieval key.

![](images/d4054b64a6282d4d733bb3cb258af458318836f6d5130d12b4e162db711f4732.jpg)  
Figure 2: Trajectory-space pretraining and visual intent prediction in Auto-JEPA. Stage 1 learns the future-trajectory target space with a trajectory autoencoder; the decoder is then discarded and the trajectory encoder is frozen. Stage 2 predicts a continuous future driving-intent latent from visual observations, ego-motion history, and navigation commands, and aligns it with the frozen trajectory target representation.

## Visual Intent Prediction

Given the current visual observation, ego-motion history, and navigation command, Auto-JEPA predicts the corresponding future ego-motion latent. We denote the model input as

$$
\mathbf { X } = ( \mathbf { I } , \mathbf { H } , \mathbf { C } ) ,\tag{4}
$$

where I contains four historical frames from the front-facing camera, H $\mathbf { \Lambda } \in \mathbf { \Lambda } \mathbf { R } ^ { 4 \times 2 }$ contains four historical ego positions, and $\mathbf { C } \in \mathbf { R } ^ { 4 }$ denotes the route command. A frozen V-JEPA 2 visual encoder $E _ { \mathrm { v i s } }$ extracts visual tokens,

$$
\mathbf { F } _ { v } = E _ { \mathrm { v i s } } ( \mathbf { I } ) .\tag{5}
$$

The history encoder $E _ { \mathrm { h i s t } }$ and command encoder $E _ { \mathrm { c m d } }$ map the remaining inputs to the predictor feature dimension,

$$
\mathbf { F } _ { h } = E _ { \mathrm { h i s t } } ( \mathbf { H } ) , \qquad \mathbf { F } _ { c } = E _ { \mathrm { c m d } } ( \mathbf { C } ) .\tag{6}
$$

The visual, history, and command features condition a JEPA predictor $P _ { \theta }$ composed of 24 Transformer blocks (Vaswani et al. 2017) with a hidden dimension of 1024 and 16 attention heads. The predictor outputs eight future latent tokens,

$$
\begin{array} { r } { \hat { \mathbf { Z } } = P _ { \theta } ( \mathbf { F } _ { v } , \mathbf { F } _ { h } , \mathbf { F } _ { c } ) \in \mathbf { R } ^ { 8 \times 1 0 2 4 } . } \end{array}\tag{7}
$$

The prediction $\hat { \mathbf { Z } }$ matches the temporal organization and feature dimension of $\mathbf { Z } ^ { + }$ . During driving-domain training, the visual encoder remains frozen, while the history encoder, command encoder, and JEPA predictor are optimized to aggregate visual evidence, ego dynamics, and navigation constraints without explicitly predicting intermediate scene states.

![](images/152141358ab3df6136ace27194821088c4bb7dcbba03965d201e139759ed167f.jpg)  
Figure 3: Overview of Auto-JEPA. During training, the predictor learns a continuous future ego-motion intent by aligning its predicted latent with the representation of the ground-truth future trajectory. During inference, the predicted intent retrieves 300 candidates from a ground-truth-only latent trajectory memory; a scene-conditioned scorer ranks candidate quality and an independent feasibility gate filters drivable-area violations before final selection. Snowflake symbols indicate frozen modules.

## Joint-Embedding Training Objectives

Rather than directly supervising waypoint coordinates with ADE or FDE, Auto-JEPA optimizes predictions in the frozen trajectory latent space using feature alignment, token-wise cosine alignment, and batch-level InfoNCE (van den Oord, Li, and Vinyals 2018).

Feature alignment. We first normalize the predicted and target latents and apply a Smooth L1 loss to their feature values,

$$
\mathcal { L } _ { \mathrm { f e a t } } = \mathrm { S m o o t h L 1 } \Big ( \mathrm { N o r m } ( \hat { \mathbf { Z } } ) , \mathrm { N o r m } ( \mathbf { Z } ^ { + } ) \Big ) .\tag{8}
$$

Token-wise cosine alignment. For the eight future time positions, we minimize the cosine distance between corresponding predicted and target tokens,

$$
\mathcal { L } _ { \mathrm { c o s } } = \frac { 1 } { 8 } \sum _ { t = 1 } ^ { 8 } \left( 1 - \frac { \hat { \mathbf { z } } _ { t } ^ { \top } \mathbf { z } _ { t } ^ { + } } { \Vert \hat { \mathbf { z } } _ { t } \Vert _ { 2 } \Vert \mathbf { z } _ { t } ^ { + } \Vert _ { 2 } } \right) .\tag{9}
$$

Batch-level InfoNCE. Positive alignment alone may map distinct driving scenes to similar representations. We therefore flatten and normalize each complete latent sequence,

$$
\hat { \mathrm { \bf q } } _ { i } = \mathrm { N o r m } ( \mathrm { v e c } ( \hat { \mathrm { \bf Z } } _ { i } ) ) , \qquad \mathrm { \bf k } _ { j } = \mathrm { N o r m } ( \mathrm { v e c } ( \mathrm { \bf Z } _ { j } ^ { + } ) ) .\tag{10}
$$

For scene $i ,$ its target latent is the positive and target latents from other scenes serve as negatives,

$$
\mathcal { L } _ { \mathrm { N C E } } = - \frac { 1 } { B } \sum _ { i = 1 } ^ { B } \log \frac { \exp ( \hat { \mathbf { q } } _ { i } ^ { \top } \mathbf { k } _ { i } / \tau ) } { \sum _ { j = 1 } ^ { B } \exp ( \hat { \mathbf { q } } _ { i } ^ { \top } \mathbf { k } _ { j } / \tau ) } ,\tag{11}
$$

where $\tau = 0 . 0 7$ . During distributed training, target latents are gathered across GPUs to enlarge the negative set.

The complete intent-prediction objective is

$$
\mathcal { L } _ { \mathrm { i n t e n t } } = 0 . 1 \mathcal { L } _ { \mathrm { f e a t } } + 2 . 0 \mathcal { L } _ { \mathrm { c o s } } + \mathcal { L } _ { \mathrm { N C E } } .\tag{12}
$$

Together, these objectives align local features and temporaltoken semantics while preserving discrimination across driving scenes, making the predicted latent suitable for trajectory retrieval.

## Non-Parametric Trajectory Retrieval

To ground the predicted continuous intent into explicit trajectory geometry, we construct a non-parametric trajectory memory using only ground-truth driving trajectories. Each memory trajectory ${ \bf Y } _ { n }$ is encoded by the same frozen trajectory encoder used to define the training targets,

$$
{ \bf { Z } } _ { n } = E _ { \mathrm { { t r a j } } } ( { \bf { Y } } _ { n } ) \in { \bf { R } } ^ { 8 \times 1 0 2 4 } .\tag{13}
$$

The resulting memory is

$$
\mathcal { M } = \{ ( \mathbf { Z } _ { n } , \mathbf { Y } _ { n } ) \} _ { n = 1 } ^ { N } , \qquad N = 1 1 0 , 3 3 5 .\tag{14}
$$

Each entry retains its latent and waypoint coordinates, directly providing candidate geometry.

For a predicted intent $\hat { \mathbf { Z } } ,$ , we flatten and L2-normalize the query and memory latents,

$$
\begin{array} { r } { \mathbf q = \mathrm { N o r m } ( \mathrm { v e c } ( \hat { \mathbf Z } ) ) , \qquad \mathbf m _ { n } = \mathrm { N o r m } ( \mathrm { v e c } ( \mathbf Z _ { n } ) ) . } \end{array}\tag{15}
$$

Their retrieval similarity is the flat cosine similarity

$$
r _ { n } = \mathbf { q } ^ { \top } \mathbf { m } _ { n } .\tag{16}
$$

We rank the complete memory by $r _ { n }$ and retrieve the $K =$ 300 most similar trajectories,

$$
\mathcal { C } = \mathrm { T o p K } \big ( \{ r _ { n } \} _ { n = 1 } ^ { N } , K \big ) .\tag{17}
$$

Retrieval identifies intent-compatible geometry, while subsequent modules handle scene-level safety. Because candidates come from recorded trajectories, inference requires neither an additional learned trajectory generator nor iterative waypoint sampling.

## Scene Scoring and Feasibility Gating

Latent similarity measures intent compatibility but not scenelevel safety. We therefore use a scene-conditioned quality scorer and an independently trained drivable-area feasibility gate.

Scene-conditioned utility branch. Given scene features $\mathbf { F } _ { \mathrm { s c e n e } } ,$ , ego context e, and a candidate trajectory ${ \bf Y } _ { k }$ , the scorer predicts a quality score

$$
s _ { k } = S _ { \phi } ( { \bf F } _ { \mathrm { s c e n e } } , { \bf e } , { \bf Y } _ { k } ) .\tag{18}
$$

We initialize $S _ { \phi }$ from the publicly released CLOVER trajectory scorer (Ang et al. 2026) and re-optimize its trainable modules on the ground-truth-only candidates retrieved by Auto-JEPA. Training uses collision, drivable-area, timeto-collision, comfort, and ego-progress supervision (Dauner et al. 2024), together with a within-scene ranking objective. The scorer and gate are trained exclusively on candidates from the NAVSIM training split, using labels generated ofline by the NAVSIM/CLOVER get\_sub\_score evaluator with the batched navsim\_v1\_style relabeling protocol. This protocol disables per-proposal two-way rollout during label generation; the final benchmark results are evaluated separately under the oficial NAVSIM protocols. Scorer training is separate from intent prediction, with no gradients propagated to the visual encoder, JEPA predictor, or trajectory memory.

Drivable-area feasibility gate. To explicitly reject candidates at risk of leaving the drivable region, the independently trained feasibility gate predicts

$$
\begin{array} { r } { p _ { k } ^ { \mathrm { D A C } } = G _ { \psi } ( \mathbf { F } _ { \mathrm { s c e n e } } , \mathbf { e } , \mathbf { Y } _ { k } ) , } \end{array}\tag{19}
$$

where $p _ { k } ^ { \mathrm { D A C } }$ is the predicted probability of a DAC failure. At inference, we form a safety mask using τ<sub>DAC</sub> = 0.2,

$$
m _ { k } = { \bf 1 } \big [ p _ { k } ^ { \mathrm { D A C } } \leq \tau _ { \mathrm { D A C } } \big ] .\tag{20}
$$

Only candidates that pass the gate participate in final selection. If all are rejected, the system falls back to ungated utility ranking. Evaluator labels are unavailable to the gate at inference time.

The final trajectory is selected by a masked argmax over utility scores,

$$
k ^ { * } = \arg \operatorname* { m a x } _ { k : m _ { k } = 1 } s _ { k } , \qquad { \bf Y } ^ { * } = { \bf Y } _ { k ^ { * } } .\tag{21}
$$

Thus, intent prediction supplies the retrieval query, memory provides trajectory geometry, and the scorer–gate cascade performs scene-conditioned selection.

## Experiments

We evaluate the complete retrieval-based planner under the oficial NAVSIM v1 and v2 protocols. Unless otherwise stated, all experiments use the same intent predictor, groundtruth-only trajectory memory, scene-conditioned scorer, and feasibility gate. We first report benchmark results, then isolate the efects of intent prediction and candidate selection, followed by analyses of candidate-pool size and visual dependence.

## Dataset and Metrics

NAVSIM v1. NAVSIM is a data-driven, non-reactive benchmark for autonomous-driving planning that provides large-scale trainval data and simulation-based evaluation on navtest (Dauner et al. 2024). The v1 benchmark evaluates each predicted ego trajectory through a simulator and reports no-at-fault collision (NC), drivable-area compliance (DAC), time to collision (TTC), comfort (C), and ego progress (EP). These terms are aggregated into the Predictive Driver Model Score (PDMS):

$$
\mathrm { P D M S } = \mathrm { N C D A C } \frac { 5 ( \mathrm { E P + T T C } ) + 2 \mathrm { C } } { 1 2 } .\tag{22}
$$

We train on NAVSIM trainval and report results on the complete navtest split of 12,146 scenarios.

NAVSIM v2. NAVSIM v2 extends the evaluation to a broader set of driving-quality and rule-compliance properties. In addition to NC and DAC, it measures drivingdirection compliance (DDC), trafic-light compliance (TL), ego progress (EP), time to collision (TTC), lane keeping (LK), history comfort (HC), and extended comfort (EC), and aggregates them into EPDMS. We evaluate v2 with the updated oficial implementation and human-behavior filtering enabled. Since v1 and v2 use diferent rollout and aggregation protocols, we report them separately without converting scores between the two metrics.

## Implementation Details

The model takes four 256 × 256 front-camera frames, four historical ego positions, and a route command. Its 24-layer Transformer predictor has 16 heads and a hidden dimension of 1024, and outputs eight temporal latent tokens. We train with a per-GPU batch size of 8, learning rate $1 0 ^ { - 5 }$ , weight decay 0.05, BF16 arithmetic, and an InfoNCE temperature of 0.07. The visual and target trajectory encoders remain frozen during predictor training. No object boxes, occupancy, semantic-map, or surrounding-agent motion labels are used. The scorer and gate use 75,823 training scenes and 8,459 validation scenes under a scene-prefix split; the validation and navtest sets have zero overlap in metric tokens. At inference, flat-cosine retrieval selects 300 candidates from a memory of 110,335 ground-truth trajectory–latent pairs; the scene scorer and feasibility gate then select the final trajectory using a DAC-failure threshold of 0.2.

## Results on NAVSIM v1

As shown in Table 1, Auto-JEPA achieves 91.3 PDMS using only a front camera, with 98.4 NC, 98.3 DAC, and 100.0 comfort.

Table 1: Comparison with representative methods on NAVSIM v1 navtest. C and L denote camera and LiDAR input, respectively. NC, DAC, TTC, C, EP, and PDMS denote no-at-fault collision, drivable-area compliance, time to collision, comfort, ego progress, and the Predictive Driver Model Score.
<table><tr><td>Method</td><td>Venue</td><td>Sensors</td><td>NC↑</td><td>DAC ↑</td><td>TTC↑</td><td>C↑</td><td>EP↑</td><td>PDMS ↑</td></tr><tr><td>Human</td><td></td><td></td><td>100.0</td><td>100.0</td><td>100.0</td><td>99.9</td><td>87.5</td><td>94.8</td></tr><tr><td colspan="9">End-to-End Planning Methods</td></tr><tr><td>TransFuser (Chitta et al. 2023)</td><td>TPAMI 2023</td><td>3×C+L</td><td>97.7</td><td>92.8</td><td>92.8</td><td>100.0</td><td>79.2</td><td>84.0</td></tr><tr><td>PARA-Drive (Weng et al. 2024)</td><td>CVPR 2024</td><td>6×C</td><td>97.9</td><td>92.4</td><td>93.0</td><td>99.8</td><td>79.3</td><td>84.0</td></tr><tr><td>Hydra-MDP (Li et al. 2024)</td><td>CVPR 2024</td><td>3×C+L</td><td>98.3</td><td>96.0</td><td>94.6</td><td>100.0</td><td>78.7</td><td>86.5</td></tr><tr><td>DiffusionDrive (Liao et al. 2025)</td><td>CVPR 2025</td><td>3×C+L</td><td>98.2</td><td>96.2</td><td>94.7</td><td>100.0</td><td>82.2</td><td>88.1</td></tr><tr><td colspan="9">World-Model-Based Methods</td></tr><tr><td>LAW (Li et al. 2025b)</td><td>ICLR 2025</td><td>1×C</td><td>96.4</td><td>95.4</td><td>88.7</td><td>99.9</td><td>81.7</td><td>84.6</td></tr><tr><td>DrivingGPT (Chen, Wang, and Zhang 2025)</td><td>ICCV 2025</td><td>1×C</td><td>98.9</td><td>90.7</td><td>94.9</td><td>95.6</td><td>79.7</td><td>82.4</td></tr><tr><td>WoTE (Li et al. 2025c)</td><td>ICCV 2025</td><td>3×C+L</td><td>98.5</td><td>96.8</td><td>94.4</td><td>99.9</td><td>81.9</td><td>88.3</td></tr><tr><td>Epona (Zhang et al. 2025)</td><td>ICCV 2025</td><td>3×C</td><td>97.9</td><td>95.1</td><td>93.8</td><td>99.9</td><td>80.4</td><td>86.2</td></tr><tr><td colspan="9">VLA-Based Methods</td></tr><tr><td>AutoVLA (Zhou et al. 2025b)</td><td>NeurIPS 2025</td><td>3×C</td><td>98.4</td><td>95.6</td><td>98.0</td><td>99.9</td><td>81.9</td><td>89.1</td></tr><tr><td>RecogDrive (Li et al. 2026b)</td><td>ICLR 2026</td><td>3×C</td><td>98.2</td><td>97.8</td><td>95.2</td><td>99.8</td><td>83.5</td><td>89.6</td></tr><tr><td>AdaThinkDrive (Luo et al. 2025)</td><td>ICRA 2026</td><td>1×C</td><td>98.4</td><td>97.8</td><td>95.2</td><td>100.0</td><td>84.4</td><td>90.3</td></tr><tr><td>DriveVLA-W0 (Li et al. 2026a)</td><td>ICLR 2026</td><td>1×C</td><td>98.7</td><td>99.1</td><td>95.3</td><td>99.3</td><td>83.3</td><td>90.2</td></tr><tr><td>Curious-VLA (Chen et al. 2026)</td><td>CVPR 2026 Findings</td><td>1×C</td><td>98.4</td><td>96.9</td><td>97.9</td><td>98.1</td><td>88.5</td><td>90.3</td></tr><tr><td>Auto-JEPA (Ours)</td><td></td><td>1×C</td><td>98.4</td><td>98.3</td><td>95.0</td><td>100.0</td><td>87.1</td><td>91.3</td></tr></table>

Table 2: Comparison with representative methods on NAVSIM v2. When multiple backbones are reported, we use the strongest source-reported configuration. For Auto-JEPA, the unmarked result uses the original evaluation implementation, while the result marked with <sup>†</sup> uses the updated oficial implementation. Results for other methods are source-reported.
<table><tr><td>Method</td><td>NC↑</td><td>DAC ↑</td><td>DDC ↑</td><td>TL↑</td><td>EP↑</td><td>TTC↑</td><td>LK↑</td><td>HC↑</td><td>EC↑</td><td>EPDMS ↑</td></tr><tr><td colspan="9">End-to-End Planning Methods</td></tr><tr><td>TransFuser (Chitta et al. 2023)</td><td>96.9</td><td>89.9</td><td>97.8</td><td>99.7</td><td>87.1</td><td>95.4</td><td>92.7</td><td>98.3</td><td>87.2</td><td>76.7</td></tr><tr><td>VADv2 (Jiang et al. 2024)</td><td>97.3</td><td>91.7</td><td>98.2</td><td>99.9</td><td>77.6</td><td>92.7</td><td>66.0</td><td>100.0</td><td>97.4</td><td>76.6</td></tr><tr><td>DiffusionDrive (Liao et al. 2025)</td><td>98.2</td><td>95.9</td><td>99.4</td><td>99.8</td><td>87.5</td><td>97.3</td><td>96.8</td><td>98.3</td><td>87.7</td><td>84.5</td></tr><tr><td>HydraMDP++ (ViT-L) (Li et al. 2025a)</td><td>98.5</td><td>98.5</td><td>99.5</td><td>99.7</td><td>87.4</td><td>97.9</td><td>95.8</td><td>98.2</td><td>75.7</td><td>85.6</td></tr><tr><td>DriveSuprim (ViT-L) (Yao et al. 2025)</td><td>98.4</td><td>98.6</td><td>99.6</td><td>99.8</td><td>90.5</td><td>97.8</td><td>97.0</td><td>98.3</td><td>78.6</td><td>87.1</td></tr><tr><td colspan="9">VLA-Based Methods</td></tr><tr><td>DriveVLA-W0 (Li et al. 2026a)</td><td>98.5</td><td>99.1</td><td>98.0</td><td>99.7</td><td>86.4</td><td>98.1</td><td>93.2</td><td>97.9</td><td>58.9</td><td>86.1</td></tr><tr><td>ReCogDrive (Li et al. 2026b)</td><td>98.3</td><td>95.2</td><td>99.5</td><td>99.8</td><td>87.1</td><td>97.5</td><td>96.6</td><td>98.3</td><td>86.5</td><td>83.6</td></tr><tr><td>Curious-VLA (Chen et al. 2026)</td><td>98.4</td><td>96.9</td><td>99.2</td><td>99.8</td><td>88.5</td><td>97.9</td><td>96.9</td><td>98.1</td><td>81.5</td><td>85.3</td></tr><tr><td>DriveWorld-VLA (Jia et al. 2026)</td><td>98.6</td><td>99.1</td><td>99.6</td><td>99.8</td><td>87.4</td><td>97.9</td><td>97.0</td><td>97.8</td><td>78.6</td><td>86.8</td></tr><tr><td>Auto-JEPA (Ours)</td><td>98.5</td><td>98.7</td><td>98.2</td><td>97.2</td><td>90.5</td><td>97.9</td><td>84.0</td><td>97.8</td><td>75.4</td><td>85.6</td></tr><tr><td>Auto-JEPA (Ours)†</td><td>98.5</td><td>98.7</td><td>98.3</td><td>99.7</td><td>90.5</td><td>97.9</td><td>94.7</td><td>97.8</td><td>75.2</td><td>89.1</td></tr></table>

## Results on NAVSIM v2

Table 2 reports 85.6 EPDMS under the original evaluator and 89.1 EPDMS under the updated oficial implementation with human-behavior filtering. CLOVER reports 90.4 EPDMS with a learned generator–scorer pipeline; Auto-JEPA remains competitive without parametric proposal generation. The evaluator change mainly afects TL and LK.

## Ablation Studies

Component ablation. We ablate each component using the same Top-300 memory. Replacing the predicted intent with a fixed codebook medoid reduces PDMS from 91.3 to

52.6, confirming scene-conditioned retrieval. Intent-based cosine retrieval with the gate already reaches 87.6; adding the scorer contributes 3.7 points. Removing the gate yields 91.0 PDMS and lowers DAC from 98.3 to 97.9.

Candidate-pool size sensitivity. The system obtains 87.6, 91.1, and 91.3 PDMS for K = 1, 200, and 300. Increasing K from 1 to 200 improves PDMS by 3.5 points, demonstrating the value of candidate selection, whereas the marginal gain from 200 to 300 indicates that performance is approaching saturation.

![](images/969713fbebad34cfd20e91f830a3c315fdf73d71dae9785cc63d3d8df0aa2200.jpg)

Figure 4: Selective responses to trafic participants. Cyan and rose denote occlusions of lower- and higher-impact vehicles, respectively. Curves show deviation from the unoccluded trajectory on a shared 0–4 m scale; $\Delta p _ { T }$ lists their terminal deviations in the same order. The smaller stop-and-go shift reflects its restricted motion range: the unoccluded plan moves only 0.17 m.  
![](images/38e26473cd043b039112d7c5d4250274f047099d7862ca102e944c07b700d40c.jpg)  
Figure 5: Representative controls from the full-validation semantic occlusion protocol. For each scene, dynamic-agent regions and independently sampled equal-area random regions are masked consistently across all four input frames. The bars report cosine similarity to the unoccluded intent.

## Analysis

Selective sensitivity to dynamic-agent information. Across 15,364 validation samples, masking all dynamic agents in all four frames produces a mean intent change (1−cosine similarity) of 0.080, compared with 0.027 for independently sampled equal-area masks, a 2.97× increase; the dynamic-agent intervention is larger in 71.1% of samples. Figure 5 shows matched controls, while Figure 4 isolates individual vehicles. Vehicles afecting future driving cause larger latent and trajectory changes than low-impact vehicles. Diferences grow with the horizon in the openroad and lead-interaction scenes, whereas the smaller stopand-go response reflects an unoccluded plan that advances only 0.17 m. Although the predictor receives no object boxes, agent identities, interaction labels, or surrounding-agent motion annotations, these responses emerge from future egotrajectory representation supervision. These results show that the model does not respond uniformly to all dynamic agents, but focuses more strongly on vehicles that may afect future driving decisions.

Table 3: Component ablation on full NAVSIM v1 navtest. Checkmarks indicate enabled components.
<table><tr><td>Intent Scorer</td><td></td><td>Gate</td><td>NC</td><td>DAC TTC</td><td></td><td>C EP</td><td>PDMS</td></tr><tr><td>x</td><td>√</td><td>√</td><td>83.1</td><td>85.3 76.2</td><td>86.3</td><td>37.8</td><td>52.6</td></tr><tr><td>√</td><td>x</td><td>√</td><td>98.1</td><td>96.4 94.0</td><td>100.0</td><td>81.7</td><td>87.6</td></tr><tr><td>√</td><td>√</td><td>x</td><td>98.5</td><td>97.9 95.0</td><td>99.9</td><td>86.9</td><td>91.0</td></tr><tr><td>√</td><td>√</td><td>√</td><td>98.4</td><td>98.3 95.0</td><td>100.0</td><td>87.1</td><td>91.3</td></tr></table>

## Conclusion

This paper introduced Auto-JEPA, an action-oriented latent world model that predicts continuous future driving intent. Joint-embedding prediction maps visual observations, ego-motion history, and navigation commands into the latent space of future ego trajectories; the predicted intent then retrieves executable candidates from a fixed memory for scene-conditioned selection. Auto-JEPA achieves 91.3 PDMS on NAVSIM v1 and 89.1 EPDMS on NAVSIM v2. Ablations and controlled occlusions validate the model’s selective focus on scene features, supporting future-trajectory latent as a decision-relevant prediction target without dense future-world modeling. The current system remains limited by memory coverage and selection calibration; intentconditioned trajectory generation or refinement provides a natural extension.

## References

Ang, S.; Yang, Y.; Chen, C.; and Wang, Y. 2026. CLOVER: Closed-Loop Value Estimation and Ranking for Endto-End Autonomous Driving Planning. arXiv preprint arXiv:2605.15120.

Assran, M.; Bardes, A.; Fan, D.; Garrido, Q.; Howes, R.; Muckley, M.; et al. 2025. V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning. arXiv preprint arXiv:2506.09985.

Assran, M.; Duval, Q.; Misra, I.; Bojanowski, P.; Vincent, P.; Rabbat, M.; LeCun, Y.; and Ballas, N. 2023. Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture. In Proceedings of the IEEE/CVF International Conference on Computer Vision.

Bardes, A.; Garrido, Q.; Ponce, J.; Chen, X.; Rabbat, M.; LeCun, Y.; Assran, M.; and Ballas, N. 2024. Revisiting Feature Prediction for Learning Visual Representations from Video. arXiv preprint arXiv:2404.08471.

Biktairov, Y.; Stebelev, M.; Rudenko, I.; Shliazhko, O.; and Yangel, B. 2020. PRANK: Motion Prediction Based on Ranking. In Advances in Neural Information Processing Systems.

Chen, C.; Yang, Y.; Tan, Z.; Wang, Y.; Zhan, R.; Liu, H.; Mao, X.; Bao, J.; Tang, X.; Yang, L.; Sun, B.; Wang, Y.; and Zhang, B. 2026. Devil Is in Narrow Policy: Unleashing Exploration in Driving VLA Models. arXiv preprint arXiv:2603.06049. Accepted to CVPR 2026 Findings.

Chen, Y.; Wang, Y.; and Zhang, Z. 2025. DrivingGPT: Unifying Driving World Modeling and Planning with Multi-Modal Autoregressive Transformers. In Proceedings of the IEEE/CVF International Conference on Computer Vision.

Chitta, K.; Prakash, A.; Jaeger, B.; Yu, Z.; Renz, K.; and Geiger, A. 2023. TransFuser: Imitation with Transformer-Based Sensor Fusion for Autonomous Driving. IEEE Transactions on Pattern Analysis and Machine Intelligence, 45(11): 12878–12895.

Dauner, D.; Hallgarten, M.; Li, T.; Weng, X.; Huang, Z.; Yang, Z.; Li, H.; Gilitschenski, I.; Ivanovic, B.; Pavone, M.; Geiger, A.; and Chitta, K. 2024. NAVSIM: Data-Driven Non-Reactive Autonomous Vehicle Simulation and Benchmarking. In Advances in Neural Information Processing Systems.

Gao, S.; Yang, J.; Chen, L.; Chitta, K.; Qiu, Y.; Geiger, A.; Zhang, J.; and Li, H. 2024. Vista: A Generalizable Driving World Model with High Fidelity and Versatile Controllability. In Advances in Neural Information Processing Systems.

Guo, K.; Liu, H.; Wu, X.; Pan, J.; and Lv, C. 2025. iPad: Iterative Proposal-Centric End-to-End Autonomous Driving. arXiv preprint arXiv:2505.15111.

Hu, A.; Russell, L.; Yeo, H.; Murez, Z.; Fedoseev, G.; Kendall, A.; Shotton, J.; and Corrado, G. 2023. GAIA-1: A Generative World Model for Autonomous Driving. arXiv preprint arXiv:2309.17080.

Jia, F.; Liu, L.; Song, Z.; Jia, C.; Ye, H.; Hao, X.; and Chen, L. 2026. DriveWorld-VLA: Unified Latent-Space World Modeling with Vision-Language-Action for Autonomous Driving. arXiv preprint arXiv:2602.06521.

Jiang, B.; Chen, S.; Gao, H.; Liao, B.; Zhang, Q.; Liu, W.; and Wang, X. 2024. VADv2: End-to-End Vectorized Autonomous Driving via Probabilistic Planning. arXiv preprint arXiv:2402.13243.

Li, K.; Li, Z.; Lan, S.; Xie, Y.; Zhang, Z.; Liu, J.; Wu, Z.; Yu, Z.; and Alvarez, J. M. 2025a. Hydra-MDP++: Advancing End-to-End Driving via Expert-Guided Hydra-Distillation. arXiv preprint arXiv:2503.12820.

Li, Y.; Fan, L.; He, J.; Wang, Y.; Chen, Y.; Zhang, Z.; and Tan, T. 2025b. Enhancing End-to-End Autonomous Driving with Latent World Model. In International Conference on Learning Representations.

Li, Y.; Shang, S.; Liu, W.; Zhan, B.; Wang, H.; Wang, Y.; Chen, Y.; Wang, X.; An, Y.; Tang, C.; Hou, L.; Fan, L.; and Zhang, Z. 2026a. DriveVLA-W0: World Models Amplify Data Scaling Law in Autonomous Driving. In International Conference on Learning Representations.

Li, Y.; Wang, Y.; Liu, Y.; He, J.; Fan, L.; and Zhang, Z. 2025c. End-to-End Driving with Online Trajectory Evaluation via BEV World Model. In Proceedings ofthe IEEE/CVF International Conference on Computer Vision.

Li, Y.; Xiong, K.; Guo, X.; Li, F.; Yan, S.; Xu, G.; Zhou, L.; Chen, L.; Sun, H.; Wang, B.; et al. 2026b. RecogDrive: A Reinforced Cognitive Framework for End-to-End Autonomous Driving. In International Conference on Learning Representations.

Li, Z.; Li, K.; Wang, S.; Lan, S.; Yu, Z.; Ji, Y.; Li, Z.; Zhu, Z.; Kautz, J.; et al. 2024. Hydra-MDP: End-to-End Multimodal Planning with Multi-Target Hydra-Distillation. arXiv preprint arXiv:2406.06978.

Liao, B.; et al. 2025. DifusionDrive: Truncated Difusion Model for End-to-End Autonomous Driving. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 12037–12047.

Luo, Y.; Li, F.; Xu, S.; Lai, Z.; Yang, L.; Chen, Q.; Luo, Z.; Xie, Z.; Jiang, S.; Liu, J.; et al. 2025. AdaThinkDrive: Adaptive Thinking via Reinforcement Learning for Autonomous Driving. arXiv preprint arXiv:2509.13769.

Sef, A.; Cera, B.; Chen, D.; Ng, M.; Zhou, A.; Nayakanti, N.; Refaat, K. S.; Al-Rfou, R.; and Sapp, B. 2023. MotionLM: Multi-Agent Motion Forecasting as Language Modeling. In Proceedings of the IEEE/CVF International Conference on Computer Vision.

Sun, W.; Lin, X.; Chen, K.; Pei, Z.; Li, X.; Shi, Y.; and Zheng, S. 2026. SparseDriveV2: Scoring Is All You Need for End-to-End Autonomous Driving. arXivpreprint arXiv:2603.29163.

van den Oord, A.; Li, Y.; and Vinyals, O. 2018. Representation Learning with Contrastive Predictive Coding. arXiv preprint arXiv:1807.03748.

Vaswani, A.; Shazeer, N.; Parmar, N.; Uszkoreit, J.; Jones, L.; Gomez, A. N.; Kaiser, L.; and Polosukhin, I. 2017. Attention Is All You Need. In Advances in Neural Information Processing Systems.

Wang, L.; Yang, Z.; Bai, C.; Zhang, G.; Liu, X.; Zheng, X.; Long, X.-X.; Lu, C.-T.; and Lu, C. 2026. Drive-JEPA: Video JEPA Meets Multimodal Trajectory Distillation for End-to-End Driving. arXiv preprint arXiv:2601.22032.

Wang, X.; Zhu, Z.; Huang, G.; Chen, X.; Zhu, J.; and Lu, J. 2023a. DriveDreamer: Towards Real-World-Driven World Models for Autonomous Driving. arXiv preprint arXiv:2309.09777.

Wang, Y.; He, J.; Fan, L.; Li, H.; Chen, Y.; and Zhang, Z. 2023b. Driving into the Future: Multiview Visual Forecasting and Planning with World Model for Autonomous Driving. arXiv preprint arXiv:2311.17918.

Weng, X.; Ivanovic, B.; Wang, Y.; Wang, Y.; and Pavone, M. 2024. PARA-Drive: Parallelized Architecture for Real-Time Autonomous Driving. In Proceedings ofthe IEEE/CVF Conference on Computer Vision and Pattern Recognition.

Xie, C.; Sun, B.; Li, T.; Wu, J.; Hao, Z.; Lang, X.; and Li, H. 2026. LatentVLA: Eficient Vision-Language Models for Autonomous Driving via Latent Action Prediction. arXiv preprint arXiv:2601.05611.

Xing, Z.; Zhang, X.; Hu, Y.; Jiang, B.; He, T.; Zhang, Q.; Long, X.; and Yin, W. 2025. GoalFlow: Goal-Driven Flow Matching for Multimodal Trajectories Generation in End-to-End Autonomous Driving. In Proceedings ofthe IEEE/CVF Conference on Computer Vision and Pattern Recognition, 1602–1611.

Yang, Z.; Chen, L.; Sun, Y.; and Li, H. 2023. Visual Point Cloud Forecasting Enables Scalable Autonomous Driving. arXiv preprint arXiv:2312.17655.

Yao, W.; Li, Z.; Lan, S.; Wang, Z.; Sun, X.; Alvarez, J. M.; and Wu, Z. 2025. DriveSuprim: Towards Precise Trajectory Selection for End-to-End Planning. arXiv preprint arXiv:2506.06659. Accepted to AAAI 2026.

Zhang, K.; Tang, Z.; Hu, X.; Pan, X.; Guo, X.; Liu, Y.; Huang, J.; Yuan, L.; Zhang, Q.; Long, X.; et al. 2025. Epona: Autoregressive Difusion World Model for Autonomous Driving. In Proceedings of the IEEE/CVF International Conference on Computer Vision.

Zhang, L.; Wu, C.; Shi, L.; Li, J.; Liu, J.; Yang, L.; Zhang, H.; Xu, M.; and Wang, H. 2026. DeepSight: Long-Horizon World Modeling via Latent States Prediction for End-to-End Autonomous Driving. arXiv preprint arXiv:2605.10564.

Zheng, W.; Chen, W.; Huang, Y.; Zhang, B.; Duan, Y.; and Lu, J. 2023. OccWorld: Learning a 3D Occupancy World Model for Autonomous Driving. arXiv preprint arXiv:2311.16038.

Zheng, Y.; Yang, P.; Xing, Z.; Zhang, Q.; Zheng, Y.; Gao, Y.; Li, P.; Zhang, T.; Xia, Z.; Jia, P.; and Zhao, D. 2025. World4Drive: End-to-End Autonomous Driving via Intention-Aware Physical Latent World Model. In Proceedings ofthe IEEE/CVFInternational Conference on Computer Vision.

Zhou, X.; Han, X.; Yang, F.; Ma, Y.; Tresp, V.; and Knoll, A. 2025a. OpenDriveVLA: Towards End-to-End Autonomous Driving with Large Vision-Language-Action Model. arXiv preprint arXiv:2503.23463.

Zhou, Z.; Cai, T.; Zhao, S. Z.; Zhang, Y.; Huang, Z.; Zhou, B.; and Ma, J. 2025b. AutoVLA: A Vision-Language-Action Model for End-to-End Autonomous Driving with Adaptive Reasoning and Reinforcement Fine-Tuning. In Advances in Neural Information Processing Systems.

## Supplementary Material

This supplementary material provides additional implementation details, training protocols, and analysis settings for Auto-JEPA. The organization follows the staged training and inference pipeline described in the main paper.

## Additional Implementation Details

## Trajectory Latent-Space Pretraining

The trajectory representation is learned before visual intent prediction. Each future ego trajectory is represented by eight planar waypoints,

$$
\mathbf { Y } \in \mathbf { R } ^ { 8 \times 2 } ,\tag{23}
$$

covering a four-second planning horizon at 0.5-second intervals. Coordinates are normalized by a scale factor of 64 before being processed by the trajectory autoencoder. The trajectory encoder contains four Transformer blocks with a hidden dimension of 1024, 16 attention heads, an MLP ratio of 4, and eight Fourier frequency bands for coordinate encoding. It produces eight temporally aligned latent tokens,

$$
{ \bf Z } ^ { + } = E _ { \mathrm { t r a j } } ( { \bf Y } ) \in { \bf R } ^ { 8 \times 1 0 2 4 } .\tag{24}
$$

The lightweight decoder contains four self-attention blocks with the same hidden dimension and number of attention heads. It predicts waypoint increments, which are cumulatively summed to obtain the reconstructed trajectory. The autoencoder is optimized with coordinate, endpoint, velocity, and acceleration consistency losses:

$$
\mathcal { L } _ { \mathrm { t r a j } } = \mathcal { L } _ { x y } + 2 . 0 \mathcal { L } _ { \mathrm { e n d } } + 0 . 5 \mathcal { L } _ { \mathrm { v e l } } + 0 . 2 \mathcal { L } _ { \mathrm { a c c } } .\tag{25}
$$

We use a batch size of 256, a learning rate of $2 \times 1 0 ^ { - 4 }$ weight decay of 0.05, dropout of 0.1, gradient clipping at 1.0, and BF16 arithmetic. The model is trained for up to 40 epochs, and the checkpoint with the lowest validation ADE is retained. After this stage, the decoder is discarded and the trajectory encoder is frozen for both intent supervision and trajectory-memory construction.

## Visual Intent Predictor

The visual intent predictor receives four front-camera frames, four historical ego positions, and a route command. The input images are resized to 256 × 256 and encoded by a frozen V-JEPA 2 visual encoder. The history and route inputs are projected into the same 1024-dimensional feature space. A 24-layer Transformer predictor with 16 attention heads fuses these inputs with eight learnable future-time query tokens and predicts

$$
\hat { \mathbf { Z } } \in \mathbf { R } ^ { 8 \times 1 0 2 4 } .\tag{26}
$$

The eight output tokens correspond to future time steps and jointly represent a single continuous driving intent; they are not separate maneuver queries.

The predictor is trained against the frozen target representation $\hat { \mathbf { Z } } ^ { + }$ using feature alignment, token-wise cosine alignment, and batch-level contrastive learning:

$$
\mathcal { L } _ { \mathrm { i n t e n t } } = 0 . 1 \mathcal { L } _ { \mathrm { f e a t } } + 2 . 0 \mathcal { L } _ { \mathrm { c o s } } + \mathcal { L } _ { \mathrm { N C E } } .\tag{27}
$$

The InfoNCE loss uses flattened trajectory latents and a temperature of 0.07. Training uses a per-GPU batch size of 8, learning rate $1 0 ^ { - 5 }$ , weight decay of 0.05, dropout of 0.1, BF16 arithmetic, and gradient clipping at 1.0. The image augmentation applies temporal frame masking with probability 0.3, masking between one and three input frames, and random image erasing with probability 0.2. When an image frame is masked, the corresponding historical ego position is masked as well.

## Trajectory Memory and Retrieval

The trajectory memory contains 110,335 ground-truth trajectory–latent pairs constructed from the NAVSIM training data. Every trajectory is encoded once with the frozen trajectory encoder. At inference, the predicted intent and memory latents are flattened and $\ell _ { 2 }$ normalized, and retrieval is performed by flat cosine similarity. The final configuration retrieves the Top-300 candidates. The memory is fixed during planner training and inference, and the NAVSIM navtest scenes are not included in memory construction.

## Dataset and Evaluation Protocol

## NAVSIM Benchmarks

NAVSIM provides a data-driven, non-reactive benchmark for autonomous-driving planning. NAVSIM v1 evaluates a predicted ego trajectory using no-at-fault collision, drivablearea compliance, time to collision, comfort, and ego progress, which are aggregated into PDMS. NAVSIM v2 extends the evaluation with additional rule-compliance and comfort terms and reports EPDMS. Because the two versions use diferent rollout and aggregation protocols, we report their results separately and do not convert one metric into the other.

For the main evaluation, the planner uses one front-camera stream and predicts an eight-point ego trajectory over a foursecond horizon. The final NAVSIM v1 result is obtained on the complete navtest split containing 12,146 scenarios. The NAVSIM v2 result is evaluated with the updated oficial implementation and human-behavior filtering enabled.

## Candidate-Label Generation and Data Split

The scene scorer and DAC gate are trained only on candidates retrieved for NAVSIM training scenes. Candidate labels are generated ofline from the NAVSIM training metric cache using the NAVSIM/CLOVER get\_sub\_score evaluator. We use the batched navsim\_v1\_style relabeling path, with per-proposal two-way rollout disabled during label generation. The resulting labels include no-at-fault collision, drivable-area compliance, ego progress, time to collision, comfort, and the aggregate utility target used for scorer training. Final benchmark results are computed separately with the oficial NAVSIM v1 or v2 evaluation pipeline rather than with these training labels.

The candidate dataset contains 75,823 training scenes and 8,459 validation scenes. We use a scene-prefix split to prevent temporally adjacent samples from the same scene sequence from appearing in both subsets. The validation set and NAVSIM navtest have zero overlap in metric tokens.

## Scene Scorer and Feasibility Gate

## Scene-Conditioned Scorer

The scorer is initialized from the publicly released CLOVER trajectory scorer and re-optimized on the ground-truth-only retrieval distribution of Auto-JEPA. Its input consists of scene features, ego context, and candidate trajectory features. The optimization objective combines trajectory-component regression with within-scene ranking:

$$
\mathcal { L } _ { \mathrm { s c o r e } } = \mathcal { L } _ { \mathrm { c o m p } } + 0 . 5 \mathcal { L } _ { \mathrm { r a n k } } .\tag{28}
$$

The ranking loss uses a temperature of 0.05 and treats candidates within 0.02 of the best target score as near-optimal. Comfort-failure candidates receive a weight of 5.0. The initial adaptation is trained for five epochs with a batch size of 32, learning rate $1 0 ^ { - 5 }$ for the scorer modules, learning rate $1 0 ^ { - 4 }$ for the ego adapter, and weight decay of 0.01. We then perform a three-epoch low-learning-rate continuation with learning rates $2 \times \mathrm { i } 0 ^ { - 6 }$ and $2 \times 1 0 ^ { - 5 }$ , respectively. The checkpoint with the highest validation selected score is used in the final planner.

## Drivable-Area Feasibility Gate

The feasibility gate predicts the probability that a candidate violates drivable-area constraints. It operates on the frozen candidate features used by the scorer, seven trajectorykinematic features, and candidate-set context. The kinematic vector contains the measured ego speed, the first two candidate speeds, their initial speed mismatch relative to the ego vehicle, the absolute mismatch, and two finite-diference acceleration terms. Candidate-set self-attention allows the gate to compare each proposal with alternative motions retrieved for the same scene. The prediction trunk has a hidden dimension of 256 and dropout of 0.1.

The gate is trained with weighted binary cross-entropy and a scene-wise pairwise ranking loss,

$$
\mathcal { L } _ { \mathrm { g a t e } } = \mathcal { L } _ { \mathrm { B C E } } + 0 . 3 \mathcal { L } _ { \mathrm { r a n k } } ,\tag{29}
$$

where DAC-failing candidates receive a positive-class weight of 8 and the ranking margin is 1.0. We use AdamW with a batch size of 32, learning rate $3 \times 1 0 ^ { - 4 }$ , weight decay $1 0 ^ { - 3 }$ gradient clipping at 1.0, and BF16 arithmetic. During inference, candidates with predicted failure probability above $\tau = 0 . 2$ are masked before the scorer argmax. If a scene has no remaining candidate, the system restores the ungated scorer ranking for that scene. Evaluator labels are never available to the gate during inference.

## Additional Ablation Details

## Full Component Ablation

The component ablation in the main paper isolates the roles of intent prediction, scene-conditioned scoring, and feasibility filtering. The scorer-free row still uses the DAC gate, whereas the no-gate row still uses the scene-conditioned scorer. Therefore, the comparisons should be interpreted conditionally rather than as a sequential addition of modules. The scorer contributes 3.7 PDMS when feasibility filtering is retained, while the gate contributes 0.3 PDMS and improves DAC by 0.4 points when the scorer is retained.

<table><tr><td>Candidate pool size K</td><td>Selected PDMS ↑</td></tr><tr><td>1</td><td>87.6</td></tr><tr><td>200</td><td>91.1</td></tr><tr><td>300</td><td>91.3</td></tr></table>

Table 4: Sensitivity to the number of retrieved candidates on NAVSIM v1 navtest. All settings use the same intent predictor and trajectory memory. For $K > 1$ , the scorer and feasibility gate select the final candidate.

## Candidate-Pool Size Sensitivity

Table 4 reports the final planning score for the candidatepool sizes evaluated during development. Increasing the pool from one direct retrieval result to 200 candidates provides the main improvement, while increasing the pool from 200 to 300 yields a smaller additional gain.

## Semantic Occlusion Protocol

The semantic occlusion analysis is conducted on the complete validation split. For every valid scene, the dynamicagent mask is formed from the projected regions of visible trafic participants and applied consistently to all four input frames. The random control masks an equal total image area. Both interventions preserve the ego-motion history and navigation command, isolating the dependence of the predicted intent on visual information.

Let Z<sup>ˆ</sup> and $\hat { \mathbf { Z } } _ { m }$ denote the intent representations predicted from the original and masked inputs. We measure the intervention response as

$$
\Delta _ { \mathrm { { i n t e n t } } } = 1 - \cos \left( \hat { \bf { Z } } , \hat { \bf { Z } } _ { m } \right) ,\tag{30}
$$

where the eight temporal tokens are flattened before cosine similarity is computed. The analysis contains 15,364 valid scenes. Dynamic-agent masking produces a mean intent change of 0.080, compared with 0.027 for equal-area random masking, corresponding to a ratio of 2.97×. The dynamic-agent intervention produces the larger response in 71.1% of scenes.

## Randomness, Runs, and Computing Infrastructure

## Randomness Control

We use a global seed of 42 for trajectory-space pretraining, dataset subsampling, distributed sampling, and quantitative semantic occlusion. The trajectory pretraining code applies this seed to Python, NumPy, PyTorch, and all CUDA devices. Distributed samplers receive the same base seed and use the epoch index for deterministic epoch-specific shufling. Validation uses a fixed split and no shufled sampler. Equalarea random masks in the semantic occlusion experiment are sampled with a NumPy generator initialized with seed 42. The qualitative figure-generation scripts use seed 2027 and enable deterministic cuDNN behavior and deterministic PyTorch algorithms when supported.

All benchmark numbers in the main paper are obtained from one deterministic full-navtest evaluation of the selected checkpoint; they are not averages over independently retrained models. The semantic occlusion statistics aggregate paired interventions over 15,364 validation samples, with the dynamic-agent and random-mask responses computed from the same checkpoint and unoccluded input. We state the number of runs explicitly because full oficial NAVSIM evaluation is computationally expensive and the evaluation path does not natively support multi-seed aggregation.

## Computing Infrastructure

Training and NAVSIM evaluation were performed on Linux servers equipped with NVIDIA A100-SXM4 GPUs with 80 GB memory. Trajectory-space pretraining and intentpredictor training support distributed execution and used one or two GPUs depending on the run; scorer adaptation, feasibility-gate training, semantic occlusion, and final benchmark evaluation used one GPU. Training commands use Python 3.12, BF16 arithmetic where stated, and one CPU thread per numerical backend during distributed runs. The released code includes the environment and dependency files needed to reconstruct the software stack. Exact package versions distributed with the release should be used rather than versions inferred from the generic upstream NAVSIM environment file.

Distributed training uses data parallelism without changing the model architecture. The per-GPU batch sizes in Table 5 therefore correspond to efective global batch sizes of 256 or 512 for trajectory pretraining and 8 or 16 for intentpredictor training when one or two GPUs are used, respectively. Scorer and gate optimization remain single-GPU procedures because their candidate features are precomputed. Final benchmark evaluation is also executed on one GPU so that all reported planner configurations use the same inference protocol.

## Complete Final Hyperparameters

Table 5 consolidates the final settings used by the four optimized stages. The scene scorer uses the original single-head scorer attention; an eight-head continuation was evaluated during development but did not improve validation selection and is not part of the reported planner.

Frozen encoders and cached candidate features are excluded from the corresponding optimizers. Checkpoint selection uses only the validation criteria shown in the table: trajectory reconstruction uses validation ADE, the intent predictor uses the completed epoch-10 checkpoint, the scorer uses validation selected score, and the gate uses validation recall and utility. The NAVSIM navtest results are not used to choose epochs, learning rates, or thresholds.

<table><tr><td>Setting</td><td>Trajectory AE</td><td>Intent predictor</td></tr><tr><td>Epochs</td><td>up to 40</td><td>10 total</td></tr><tr><td>Batch size</td><td>256/GPU</td><td>8/GPU</td></tr><tr><td>Optimizer</td><td>AdamW</td><td>AdamW</td></tr><tr><td>Learning rate</td><td> $2 \times 1 0 ^ { - 4 }$ </td><td> $1 0 ^ { - 5 }$ </td></tr><tr><td>Weight decay</td><td>0.05</td><td>0.05</td></tr><tr><td>Dropout</td><td>0.1</td><td>0.1</td></tr><tr><td>Gradient clipping</td><td>1.0</td><td>1.0</td></tr><tr><td>Precision</td><td>BF16</td><td>BF16</td></tr><tr><td>Selection</td><td>lowest val ADE</td><td>epoch-10 checkpoint</td></tr><tr><td>Setting</td><td>Scene scorer</td><td>DAC gate</td></tr><tr><td>Epochs</td><td>5 + 3 continuation</td><td>selected checkpoint</td></tr><tr><td>Batch size</td><td>32</td><td>32</td></tr><tr><td>Optimizer</td><td>AdamW</td><td>AdamW</td></tr><tr><td>Learning rate</td><td> $1 0 ^ { - 5 } \substack {  } 2 \times 1 0 ^ { - 6 }$ </td><td> $3 \times 1 0 ^ { - 4 }$ </td></tr><tr><td>Auxiliary LR</td><td> $1 0 ^ { - 4 } \to 2 \times 1 0 ^ { - 5 }$ </td><td></td></tr><tr><td>Weight decay</td><td>0.01</td><td> $1 0 ^ { - 3 }$ </td></tr><tr><td>Dropout</td><td>pretrained</td><td>0.1</td></tr><tr><td>Gradient clipping</td><td>1.0</td><td>1.0</td></tr><tr><td>Precision</td><td>BF16</td><td>BF16</td></tr><tr><td></td><td></td><td></td></tr><tr><td>Selection</td><td>best val score</td><td>val recall/utility</td></tr></table>

Table 5: Final optimization settings. “Auxiliary $\mathrm { L R } ^ { , , }$ denotes the ego-adapter learning rate used by the scene scorer.

## Limitations and Failure Modes

Auto-JEPA predicts the implications of a scene for future ego motion rather than rolling out a complete future environment. The learned intent is therefore an action-oriented predictive representation, not an explicit reconstruction of surrounding-agent states. This design is suficient for the trajectory-planning interface studied here, but it does not provide the scene-level forecasts required by applications such as interactive simulation or counterfactual environment generation.

The retrieval-based planner is bounded by the coverage of its fixed trajectory memory and by the recall of the intent query. If no feasible maneuver is represented in the retrieved candidate pool, neither the scene scorer nor the feasibility gate can synthesize one. The observed saturation between K = 200 and $K = 3 0 0$ indicates that simply enlarging the candidate pool ofers diminishing returns under the current memory and predictor. A broader memory, adaptive retrieval, or intent-conditioned trajectory generation and local refinement could extend the reachable motion space while preserving the learned intent representation.

When a feasible candidate is available, selection errors can still arise from scorer calibration or distribution shift. A valid candidate may receive an inaccurately low scene score, while the gate may reject a legal borderline trajectory or retain one that violates the drivable area. The all-filtered fallback guarantees a non-empty output but cannot repair an erroneous ranking. These cases motivate uncertainty-aware scoring, stronger calibration, and targeted hard-negative training.