# SGDrive: Scene-to-Goal Hierarchical World Cognition for Autonomous Driving

Jingyu Li<sup>1,2∗</sup> Junjie Wu<sup>3∗</sup> Dongnan Hu<sup>4,2</sup> Xiangkai Huang<sup>3</sup> Bin Sun<sup>3†</sup> Zhihui Hao<sup>3†</sup> Xianpeng Lang<sup>3</sup> Xiatian Zhu<sup>5</sup> Li Zhang<sup>1,2</sup> <sup>B</sup>

<sup>1</sup> Fudan University <sup>2</sup> Shanghai Innovation Institute <sup>3</sup> Li Auto Inc. <sup>4</sup> Tongji University <sup>5</sup> University of Surrey

github.com/LogosRoboticsGroup/SGDrive

## Abstract

Recent end-to-end autonomous driving approaches have leveraged Vision-Language Models (VLMs) to enhance planning capabilities in complex driving scenarios. However, VLMs are inherently trained as generalist models, lacking specialized understanding of driving-specific reasoning in 3D space and time. When applied to autonomous driving, these models struggle to establish structured spatial-temporal representations that capture geometric relationships, scene context, and motion patterns critical for safe trajectory planning. To address these limitations, we propose SGDrive, a novel framework that explicitly structures the VLM’s representation learning around driving-specific knowledge hierarchies. Built upon a pretrained VLM backbone, SGDrive decomposes driving understanding into a scene-agent-goal hierarchy that mirrors human driving cognition: drivers first perceive the overall environment (scene context), then attend to safety-critical agents and their behaviors, and finally formulate short-term goals before executing actions. This hierarchical decomposition provides the structured spatial-temporal representation that generalist VLMs lack, integrating multi-level in formation into a compact yet comprehensiveformatfor trajectory planning. Extensive experiments on the NAVSIM benchmark demonstrate that SGDrive achieves state-ofthe-art performance among camera-only methods on both PDMS and EPDMS, validating the effectiveness of hierarchical knowledge structuringfor adapting generalist VLMs to autonomous driving.

![](images/2775cb3a1d322375903b34dd9d89b4ebbe739fcad42f54b029b747a5b3c83061.jpg)  
Figure 1. (a) directly produces driving actions in textual form. (b) VLM generates action embeddings that decoded to produce the final trajectory. (c) Our SGDrive explicitly learns and forecasts scene, agent, and goal knowledge, providing structured drivingworld understanding that strengthens action reasoning and improves generalization.

## 1. Introduction

In recent years, end-to-end (E2E) autonomous driving techniques have achieved significant strides. However, these methods [13, 14, 20, 45] often lack explicit causal reasoning and high-level scene understanding, exhibiting limitations in complex, long-tail traffic scenarios. The advent of large language models [1, 49], particularly Vision-Language Models (VLMs) [7, 51], have spurred efforts to integrate their rich prior knowledge and sophisticated reasoning capabilities into the driving tasks, aiming to mitigate these shortcomings and prevent unsafe maneuvers. However, how to effectively translate a VLM’s powerful cognitive understanding into physically safe and reliable driving actions remains an open challenge.

To transfer pretrained VLM knowledge to autonomous driving, several methods [15, 43, 52] create domain-specific datasets that adapt the model’s knowledge to driving scenarios. Building upon this foundation, some works [8, 16, 55] attempt to directly generate trajectories in textual form Figure1(a). Subsequent methods [12, 27] draw inspiration from embodied intelligence researches [3, 23] and employ diffusion-based decoder to produce driving trajectories Figure1(b). While the aforementioned methods have achieved impressive results, they still suffer from several key limitations: (1) Lack of spatial perception: VLMs are inherently focused on semantic understanding and lack foundational spatial and geometric knowledge [39, 43, 56]. (2) Difficulty in discerning critical information: Current methods [28, 33] often focus on the entire scene and lack the extraction of important information, leading to sub-optimal driving performance. (3) Lack offuture world state forecast: Lack of temporal modeling of future world state evolution., such as how the surrounding scene will change. Therefore, we argue that previous methods fail to sufficiently represent the world and forecast its future state, thus hindering the realization of safe and reliable driving.

To address the aforementioned issues, we propose SG-Drive, a novel framework that integrates structured and hierarchical world knowledge into VLMs, thereby enhancing the model’s capability to understand and represent drivingrelevant world knowledge. As shown in Figure1(c), we introduce a set of special tokens, called 〈world〉, which are explicitly trained to extract comprehensive driving-relevant world knowledge. This structured knowledge captures geometric and semantic information as well as high-level driving objectives. By explicitly activating the model’s ability to perceive and represent this structured, world knowledge, we fundamentally enhance its 3D spatial perception, enabling the VLM to better guide trajectory generation and avoid potential collisions.

We guide the model to acquire comprehensive driving relevant world knowledge from three complementary aspects: (1) Scene geometric layout: Our method leverages occupancy supervision [57, 66] to learn the overall geometric structure of the scene, enabling the model to perceive and predict holistic spatial variations while removing redundant semantic dependencies. (2) Perceiving driving relevant agents: By incorporating an agent detection mod ule [4, 33], the model focuses on identifying agents that are likely to influence ego-vehicle motion, instead of all visible objects, aligning better with human driving behavior. (3) Inferring driving goal: The model learns to reason about feasible driving goal that reflect human-like driving intentions and are consistent with the current scene context. Together, these components provide the model with a comprehensive prior over both the current and future world states, facilitating safer trajectory planning. To ensure disentangled representation across these knowledge, we further apply a block-wise masked attention mechanism to prevent information leakage between different knowledge. Finally, to effectively translate the driving-relevant world knowledge into trajectory outputs, we employ a diffusion-based transformer [37] (DiT) as the trajectory generator. This design enables the model to progressively refine trajectory predictions conditioned on the extracted world knowledge, ensuring coherent trajectory generation.

Our main contributions are summarized as follows: (i) We propose a novel framework that guides the VLM to learn comprehensive world knowledge from different aspects, enhancing its spatial perception and world representation for safe autonomous driving. (ii) We design a blockwise masked attention mechanism to prevent knowledge leakage and noise interference, and couple it with a DiT decoder to generate trajectories conditioned on hierarchical world knowledge. (iii) Our method achieves state-of-the-art performance on the NAVSIM benchmark among cameraonly methods, demonstrating its effectiveness through extensive experiments.

## 2. Related works

## 2.1. End-to-end autonomous driving

Recent advancements in autonomous driving have shifted from isolated task pipelines to unified end-to-end planning frameworks that jointly address scene perception and egotrajectory generation [5, 13, 54, 60, 61], with further efforts have incorporated multi-modal inputs and transformerbased architectures for enhanced global reasoning [17, 18, 38, 42]. UniAD [14] extends the scope by integrating a wide range of subtasks into a cohesive system, while VAD [20] further improves it with vectorized representations and refined modular design. SparseAD [63] and SparseDrive [45] explore sparse representations to improve the efficiency and scalability of end-to-end planning systems. VADv2 [6] pioneers the integration of probabilistic planning into end-toend autonomous driving. DiffusionDrive [30] leverages a truncated diffusion policy to improve the accuracy and diversity of planned trajectories. WoTE [26] builds a worldmodel-based autonomous driving system upon the BEV representation. Although these methods have achieved remarkable success, their imitation-learning nature inherently limits generalization to long-tail and complex scenarios, while lacking reasoning and deliberative capabilities.

## 2.2. Vision-language-model in autonomous driving

Within autonomous driving, LLMs [1] and VLMs [24, 31, 70] have revealed strong reasoning and multi-modal capabilities. Concurrently, the introduction of large-scale driving datasets [10, 19, 22] with natural language annotations [35, 36, 40, 68] has facilitated research. Notably, DriveLM [43] introduces a Chain-of-Thought reasoning paradigm spanning perception to planning, while DriveMM [15] integrates diverse language-driving datasets to build a universal VLM. Inspired by advancements in the field of robotic manipulation [3, 23, 65], a new class of Vision-Language-Action (VLA) models based on VLMs has emerged to autonomous driving [21, 25, 34, 48]. EMMA [16], built upon Gemini [46], maps raw camera inputs to driving decisions and demonstrates high accuracy in perception and strong performance in motion planning. SimLingo [41] introduces a VLM-based architecture that unifies driving, vision-language understanding, and language-action alignment. OpenDriveVLA [67] employs hierarchical vision-language alignment and agentenvironment-ego interaction to produce reliable driving actions, excelling in planning and driving-related question answering tasks. ORION [12] proposes a framework that integrates QT-Former, a large language model (LLM), and a generative planner, achieving strong performance in closedloop evaluations. FSDrive [59] reformulates CoT reasoning into a spatio-temporal visual CoT, where a VLM generates a future frame and subsequently predicts the trajectory via inverse dynamics. ReCogDrive [27] proposes a framework that integrates a VLM with a diffusion planner, utilizing Diffusion Group Relative Policy Optimization to enhance trajectory generation. In contrast to previous work, SG-Drive represents and forecasts world knowledge in a hierarchical (scene-agent-goal) and effective manner, enabling safe and reliable driving.

![](images/dc85c16bf99ca63194e9006c2e99a7586c6b4b16624333fda60c522cc08b3dc9.jpg)  
Figure 2. The SGDrive pipeline introduces hierarchical 〈world〉 queries (scene, agent, and goal) for world modeling and trajectory generation. A key component is our world query encoder, which initializes these queries by integrating multi-modal priors from the ego state, historical trajectory, and visual features. These “prior-informed” queries are then processed by the VLM, alongside text and visua embeddings, to fuse all signals into a compact, hierarchical world representation.

## 3. Method

## 3.1. Problem definition and notation

We aim to enhance the safety of autonomous driving through the guidance of multi-level driving-relevant world knowledge. Accordingly, we formulate our framework as tackling two complementary sub-problems: extracting representative world knowledge and extrapolating future world states. At each time step t, the ego-vehicle receives heterogeneous signals: a natural language instruction $L _ { i n s } ,$ the ego-vehicle state $S _ { e g o } ,$ , and camera sensor inputs $I _ { c a m } .$ These inputs together constitute the world knowledge of the driving system. To direct the model’s attention toward driving cues and facilitate forecasting of future world states, we introduce a set of special tokens, denoted as 〈world〉 , and adopt a VLM to transform the comprehensive world knowledge into compact latent representations:

$$
O _ { \mathrm { w o r l d } } = V L M \big ( I _ { c a m } , L _ { i n s } , S _ { e g o } | < \mathrm { w o r l d } > \big ) .\tag{1}
$$

The resulting representation $O _ { \mathrm { w o r l d } }$ encapsulates the driving-related world knowledge and serves as the foundation for forecasting the future evolution of the world state. We then introduce a set of hierarchical world heads D that extract structured world knowledge across geometric details, motion cues, and high-level cognition, and further extrapolate the world state at future time t+n:

$$
w = \mathcal { D } \big ( O _ { w o r l d } \big ) = \{ w _ { g e o } ^ { t , t + n } , w _ { a g t } ^ { t , t + n } , w _ { g o a l } \} ,\tag{2}
$$

where $w _ { g e o }$ represents the layout of the scene, $w _ { a g t }$ captures the state of the safety-critical agents, and $w _ { g o a l }$ encodes the short-term driving objective.

Based on the learned world knowledge, we utilize DiT [37] to generate trajectory. This design effectively translates the forecast world knowledge into coherent and safe future trajectories, completing the reasoning chain from scene understanding to motion planning.

## 3.2. Model architecture

As illustrated in Figure 2, our SGDrive builds on a foundational VLM with two core modules. SGDrive accepts heterogeneous inputs and processes each modality separately. Specifically, we use a standard text tokenizer encodes the driving instruction, while a ViT-based visual encoder [71] extracts features from the camera image. We further introduce a set of 〈world〉 queries, which are appended to the multimodal embeddings. And these queries consist of three subqueries (scene, agent, and goal), which is used for predicting hierarchical driving world knowledge. The world queries are initialized via a world query encoder, which integrates multi-modal priors from the ego state, historical trajectory, and visual embeddings (Figure 2). These priorinformed queries effectively capture contextual information from the scene. Combined with the VLM’s strong priors, our method fuses visual and ego-vehicle signals into a compact hierarchical representation that encodes the scene geometry, dynamic agent states, short-term driving objectives, and predicted future world states, providing a structured and interpretable foundation for subsequent world modeling and trajectory generation.

In the decoding stage, task-specific heads process the corresponding subqueries, transforming the unified world embedding into explicit representations (scene context, agent states, and short-term goals). The latent world embedding implicitly conveys hierarchical driving knowledge, enabling downstream trajectory generation without requiring explicit decoding of the 〈world〉 queries, thereby reducing computational cost while preserving semantic richness.

## 3.3. Hierarchical world knowledge representation

Safe driving requires anticipating how the surrounding environment will evolve. Our method mirrors human driving cognition by explicitly forecasting future world knowledge along three complementary aspects: scene geometry, safety-critical agents, and short-term driving goals. This structured scene-agent-goal representation supplements the missing depth information in images and provides predictive context to support safe trajectory generation.

Geometric scene layout perception. Perceiving and forecasting the geometric layout of the driving scene provides essential spatial cues for safe driving. Our model does not predict high-level semantic distributions; instead, it focuses on the overall geometric structure. When occupancy annotations are available in the dataset, we supervise the model with ground-truth labels; otherwise, we generate occupancy from the point clouds. Since a VAE decoder excels at reconstructing features from latent representations [32, 47, 50], we treat the VLM output $W _ { \mathrm { g e o } }$ as the latent embedding and employ a standard VAE decoder for geometric reconstruction. Considering the high sparsity of driving scenes with a large number of negative samples [32], we follow prior work [44] and adopt a resampling strategy, supervised by two classification losses to ensure balanced learning of occupied and unoccupied regions:

$$
\begin{array} { l } { \displaystyle \mathcal { L } _ { \mathrm { g e o } } ^ { t , t + n } = \frac { 1 } { M } \sum _ { i = 1 } ^ { M } \mathrm { C E } ( o _ { i } ^ { t , t + n } , \hat { o } _ { i } ^ { t , t + n } ) } \\ { \displaystyle \qquad + \frac { 1 } { N } \sum _ { j = 1 } ^ { N } \mathrm { B C E } ( p _ { j } ^ { t , t + n } , \hat { p } _ { j } ^ { t , t + n } ) , } \end{array}\tag{3}
$$

where $\mathcal { L } _ { \mathrm { g e o } }$ combines the standard cross-entropy loss over all spatial locations with a resampled binary cross-entropy term to handle sparse occupancy distribution. $o _ { i } \in \{ 0 , 1 \}$ indicates whether location $j$ is occupied in the ground truth, and $p _ { i }$ denotes resampled candidate positions.

Safety-critical agents detection. To handle complex driving interactions, our SGDrive focuses on safety-critical road users that directly influence driving behavior, encouraging collision-avoidant reasoning and deeper understanding of safety-critical interactions. Specifically, we select target agents (vehicle, pedestrian and cyclist) based on egovehicle trajectory and visibility from the front-view camera frustum. This strategy compels the model to allocate its finite representational capacity to agents most relevant to the ego-vehicle’s decisions, rather than exhaustively perceiving all objects in the scene. For these selected agents, the model predicts their 3D states at both the current and future time steps (t and t + n). To supervise these agent predictions, we adopt the set-based loss paradigm from DETR [4], which finds an optimal bipartite matching σˆ between the $N _ { q }$ predictions and the set of ground-truth objects. The total loss $\mathcal { L } _ { \mathrm { a g e n t } }$ is then computed as a weighted sum of classification and regression losses for the matched pairs:

$$
\begin{array} { r l } & { \mathcal { L } _ { \mathrm { a g e n t } } ^ { t , t + n } = \displaystyle \sum _ { i = 1 } ^ { N _ { q } } \left[ \lambda _ { \mathrm { c l s } } \mathcal { L } _ { \mathrm { c l s } } ( \hat { c } _ { i } ^ { t , t + n } , c _ { \hat { \sigma } ( i ) } ^ { t , t + n } ) \right. } \\ & { \qquad \left. + \mathbf { 1 } _ { c _ { \hat { \sigma } ( i ) } t , t + n \neq \emptyset } \mathcal { L } _ { \mathrm { r e g } } ( \hat { b } _ { i } ^ { t , t + n } , b _ { \hat { \sigma } ( i ) } ^ { t , t + n } ) \right] , } \end{array}\tag{4}
$$

where $\hat { \sigma } ( i )$ is the index of the ground-truth object matched to the i-th prediction. ${ \mathcal L } _ { \mathrm { c l s } }$ is a cross-entropy loss, $\lambda _ { \mathrm { c l s } }$ takes 10, and $\mathcal { L } _ { \mathrm { r e g } }$ is an $L _ { 1 }$ loss. The indicator term $\mathbf { 1 } _ { c _ { \hat { \sigma } ( i ) } \neq \varnothing }$ ensures the regression loss is applied only to positive matches. Short-term driving goal forecasting. Predicting shortterm driving goals provides high-level semantic guidance for the ego-vehicle, indicating the intended trajectory over the immediate future. Without such predictions, egovehicle may exhibit incomplete or suboptimal maneuvers, such as covering only part of the planned path—potentially reducing task efficiency and safety. At the apex of the cognitive hierarchy, multi-modal interactions between visual and textual embeddings are used to infer the ego-vehicle’s intended objective. Rather than being directly conditioned on the previously established world representations (e.g., scene geometric layout or safety-critical agents), this goal reasoning emerges implicitly from a holistic understanding of the scene and task instructions. Building upon this implicit goal reasoning, SGDrive predicts a short-term driving goal, $\hat { p } _ { \mathrm { g o a l } }$ , defined as the target ego-pose approximately 4 seconds into the future. This prediction is decoded via a lightweight mlp head and supervised using an $L _ { 1 }$ loss against the ground-truth pose $p _ { \mathrm { g o a l } } \mathrm { . }$

$$
\mathcal { L } _ { \mathrm { g o a l } } = | | \hat { p } _ { \mathrm { g o a l } } - p _ { \mathrm { g o a l } } | | _ { 1 } .\tag{5}
$$

The predicted goal is more than a single trajectory point; it encodes high-level driving intentions informed by the model’s understanding of scene constraints and potential interactions. By explicitly predicting this goal, we effectively disentangle high-level decision-making from low-level trajectory planning.

Structured block-wise attention mask for driving-world knowledge. Our SGDrive employs specialized 〈world〉 queries to decode anticipatory knowledge, capturing both current state and future evolution. A key challenge in this multi-task design is representational contamination: if queries freely attend to each other (Figure 3(a)), information can leak across cognitive levels, compromising the integrity of specialized representations.

To address this, we introduce a block-wise structured attention mask (Figure 3(b)). The 〈world〉 queries are divided into five subqueries: the first three encode current world knowledge, and the remaining two focus on forecasting future states. The mask blocks attention across different knowledge categories while allowing temporal attention within each category, enabling subqueries to access relevant historical context. All subqueries remain free to cross-attend to the primary input modalities (visual and text embeddings), ensuring each representation gathers necessary evidence. This structured attention effectively prevents cross-level leakage, maintaining specialized and accurate hierarchical representations, which is essential for safe and precise driving.

![](images/694499a8cea9f3de8d5f75b04f9c43e7c42718ff06e13dc567f721379a8c120a.jpg)  
Figure 3. (a) Causal attention mask: input tokens are allowed to attend to tokens before. (b) Structure attention mask: prevents leakage by prohibiting all mutual attention between the different subquery sets (scene, agent, goal).

## 3.4. Diffusion planner

A key challenge in autonomous driving is bridging the gap between high-level semantic reasoning and low-level continuous actions. To address this, we employ a diffusion planner [3, 23, 37] that generates safe and context-aware action trajectories. Our 〈world〉 queries, which encode a hierarchical and anticipatory understanding of the driving world, are directly used as the latent condition for the planner. This avoids intermediate, lossy representations and enables access to the VLM’s full world knowledge while reducing inference overhead.

The planner denoises a sequence of future waypoints $\mathbf { A } = \left( a _ { 1 } , \ldots , a _ { N } \right)$ from a noisy initialization ${ \bf A } _ { T }$ to the ground-truth trajectory ${ \bf A } _ { 0 }$ over $T$ steps. The per-step denoising is conditioned on the hierarchical world knowledge and ego-vehicle state, injected via the DiT’s cross-attention layers. Instead of starting from pure Gaussian noise, ${ \bf A } _ { T }$ is initialized by adding noise ϵ to a learned prior, generated from a linear projection of the 〈world〉 queries and historical ego-trajectory, grounding the process in the VLM’s world understanding. The diffusion model $\epsilon _ { \theta }$ is trained with a standard $L _ { 2 }$ objective:

$$
\begin{array} { r } { \mathcal { L } _ { \mathrm { d i f f } } = \mathbb { E } _ { t , \mathbf { A } _ { 0 } , \epsilon } \left[ \left| \left| \epsilon - \epsilon _ { \theta } ( \mathbf { A } _ { t } , t , c ) \right| \right| _ { 2 } ^ { 2 } \right] , } \end{array}\tag{6}
$$

where ${ \bf A } _ { t }$ is the noisy trajectory at step t and c denotes the per-step condition.

Table 1. Performance comparison on NAVSIM v1 navtest using closed-loop metrics. We additionally report results with reinforcemen learning fine-tuning (RFT) to enable fair comparison with methods that adopt such training strategies. <sup>†</sup> denotes models fine-tuned on the NAVSIM trajectory dataset. Bold indicates the best results under SFT and RFT settings, respectively.
<table><tr><td>Method</td><td>Image</td><td>Lidar</td><td>NC↑</td><td>DAC↑</td><td>TTC↑</td><td>Comf. ↑</td><td>EP↑</td><td>PDMS↑</td></tr><tr><td>Constant Velocity</td><td></td><td></td><td>68.0</td><td>57.8</td><td>50.0</td><td>100</td><td>19.4</td><td>20.6</td></tr><tr><td>Ego Status MLP</td><td></td><td></td><td>93.0</td><td>77.3</td><td>83.6</td><td>100</td><td>62.8</td><td>65.6</td></tr><tr><td>VADv2-V8192 [6]</td><td>V</td><td></td><td>97.2</td><td>89.1</td><td>91.6</td><td>100</td><td>76.0</td><td>80.9</td></tr><tr><td>Hydra-MDP-V8192 [29]</td><td>√</td><td>√</td><td>97.9</td><td>91.7</td><td>92.9</td><td>100</td><td>77.6</td><td>83.0</td></tr><tr><td>UniAD [14]</td><td>V</td><td></td><td>97.8</td><td>91.9</td><td>92.9</td><td>100</td><td>78.8</td><td>83.4</td></tr><tr><td>LTF [38]</td><td>V</td><td></td><td>97.4</td><td>92.8</td><td>92.4</td><td>100</td><td>79.0</td><td>83.8</td></tr><tr><td>BevDrive [54]</td><td>√</td><td>V</td><td>97.7</td><td>92.5</td><td>92.9</td><td>100</td><td>78.7</td><td>83.8</td></tr><tr><td>TransFuser [38]</td><td>√</td><td>V</td><td>97.7</td><td>92.8</td><td>92.8</td><td>100</td><td>79.2</td><td>84.0</td></tr><tr><td>PARA-Drive [53]</td><td>√</td><td></td><td>97.9</td><td>92.4</td><td>93.0</td><td>99.8</td><td>79.3</td><td>84.0</td></tr><tr><td>DRAMA [58]</td><td>V</td><td>V</td><td>98.0</td><td>93.1</td><td>94.8</td><td>100</td><td>80.1</td><td>85.5</td></tr><tr><td>Epona [64]</td><td>√</td><td></td><td>97.9</td><td>95.1</td><td>93.8</td><td>99.9</td><td>80.4</td><td>86.2</td></tr><tr><td>Hydra-MDP-V8192-W-EP [29]</td><td>√</td><td>√</td><td>98.3</td><td>96.0</td><td>94.6</td><td>100</td><td>78.7</td><td>86.5</td></tr><tr><td>ARTEMIS [11]</td><td>V</td><td>V</td><td>98.3</td><td>95.1</td><td>94.3</td><td>100</td><td>81.4</td><td>87.0</td></tr><tr><td>DiffusionDrive [30]</td><td>V</td><td>V</td><td>98.2 98.5</td><td>96.2</td><td>94.7</td><td>100</td><td>82.2</td><td>88.1</td></tr><tr><td>WoTE [26] SeerDrive [62]</td><td>√ V</td><td>√ V</td><td>98.4</td><td>96.8 97.0</td><td>94.9 94.9</td><td>99.9 99.9</td><td>81.9</td><td>88.3</td></tr><tr><td>VLMs-based Methods (SFT)</td><td></td><td></td><td></td><td></td><td></td><td></td><td>83.2</td><td>88.9</td></tr><tr><td colspan="9"></td></tr><tr><td>AutoVLA-3B [69]</td><td>V</td><td></td><td>96.9</td><td>92.4</td><td>88.1</td><td>99.1</td><td>75.8</td><td>80.5</td></tr><tr><td>QwenVL2.5-8B† [2]</td><td>√</td><td></td><td>97.8</td><td>92.1</td><td>92.8</td><td>100</td><td>78.3</td><td>83.3</td></tr><tr><td>InternVL3-8B† [71]</td><td>V</td><td></td><td>97.0</td><td>92.4</td><td>91.8</td><td>100</td><td>78.9</td><td>83.3</td></tr><tr><td>ReCogDrive-2B [27]</td><td>V</td><td></td><td>98.1</td><td>94.7</td><td>94.2</td><td>100</td><td>80.9</td><td>86.5</td></tr><tr><td>ReCogDrive-8B [27]</td><td>√</td><td></td><td>98.3</td><td>95.1</td><td>94.3</td><td>100</td><td>81.1</td><td>86.8</td></tr><tr><td>SGDrive-2B (ours)</td><td>√</td><td></td><td>98.6</td><td>95.1</td><td>95.4</td><td>100</td><td>81.2</td><td>87.4</td></tr><tr><td colspan="9">VLMs-based Methods (RFT)</td></tr><tr><td>AutoVLA-3B [69]</td><td>√</td><td></td><td>98.4</td><td>95.6</td><td>98.0</td><td>99.9</td><td>81.9</td><td>89.1</td></tr><tr><td>ReCogDrive-2B [27]</td><td>√</td><td></td><td>97.9</td><td>97.3</td><td>94.9</td><td>100</td><td>87.3</td><td>90.8</td></tr><tr><td>ReCogDrive-8B [27]</td><td>V</td><td></td><td>97.8</td><td>97.7</td><td>94.9</td><td>100</td><td>86.3</td><td>90.5</td></tr><tr><td>SGDrive-2B (ours)</td><td>√</td><td></td><td>98.6</td><td>97.8</td><td>96.2</td><td>100</td><td>85.8</td><td>91.1</td></tr></table>

## 3.5. Training objectives

Our SGDrive is trained in a two-stage procedure to effectively manage the distinct task spaces of world representation and action generation. In the first stage, we perform Supervised Fine-Tuning (SFT) to train the core VLM for both visual question answering (VQA) and comprehensive world knowledge acquisition. The model processes multi-frame front-view camera inputs, ego-vehicle states, and languagebased driving commands, and is supervised to jointly predict: (1) textual answers for VQA $\mathcal { L } _ { t e x t }$ , (2) the spatiotemporal scene geometry layout, (3) safety-critical agent detection, and (4) the short-term driving goal. The total loss is defined as:

$$
{ \mathcal { L } } _ { \mathrm { S t a g e 1 } } = { \mathcal { L } } _ { \mathrm { t e x t } } + { \mathcal { L } } _ { \mathrm { o c c } } ^ { t , t + n } + \lambda _ { \mathrm { a g e n t } } { \mathcal { L } } _ { \mathrm { a g e n t } } ^ { t , t + n } + { \mathcal { L } } _ { \mathrm { g o a l } } ,\tag{7}
$$

where $\lambda _ { \mathrm { a g e n t } }$ takes 0.1.

In the second stage, we freeze the pre-trained VLM from stage 1 to serve as a high-fidelity world model, and train the diffusion planner with the same inputs but a single optimization target, the trajectory diffusion loss ${ \mathcal { L } } _ { \mathrm { d i f f } }$ . This staged strategy enables the VLM to first learn a robust, general-purpose representation of the driving world, which is then exploited by the diffusion planner to generate safe and realistic trajectories.

## 4. Experiments

## 4.1. Experimental setup

Implementation Details. We use InternVL3-2B [71] as our VLM backbone, which is integrated a 300M-parameter InternViT visual encoder [7] with the Qwen2.5 largelanguage-model [2]. In stage 1, we first perform domain adaptation to align the base VLM with the driving modality, following [27]. We use over 3.1 million questionanswer (QA) pairs covering perception, prediction, and planning, and train for 1 epoch. Subsequently, we fine-tune the VLM on 85k trajectory-specific QA pairs while concurrently training the world knowledge heads for 3 epoches. In Stage 2, we freeze the VLM parameters and train the diffusion planner exclusively for 220 epochs. All experiments are conducted on 4 nodes, each equipped with 8 NVIDIA H20 GPUs (32 GPUs total). Additional details are provided in the supplementary material.

Table 2. Performance comparison on NAVSIM v2 navtest with extended metrics. Our SGDrive-2B is evaluated using the model trained with the proposed two-stage SFT strategy.
<table><tr><td>Method</td><td>NC↑</td><td>DAC↑</td><td>EP↑</td><td>TTC↑</td><td>HC↑</td><td>TL↑</td><td>DDC↑</td><td>LK↑</td><td>EC↑</td><td>EPDMS↑</td></tr><tr><td>Transfuser [38]</td><td>97.7</td><td>92.8</td><td>79.2</td><td>92.8</td><td>100</td><td>99.9</td><td>98.3</td><td>67.6</td><td>95.3</td><td>77.8</td></tr><tr><td>VADv2 [6]</td><td>97.3</td><td>91.7</td><td>77.6</td><td>92.7</td><td>100</td><td>99.9</td><td>98.2</td><td>66.0</td><td>97.4</td><td>76.6</td></tr><tr><td>Hydra-MDP [29]</td><td>97.5</td><td>96.3</td><td>80.1</td><td>93.0</td><td>100</td><td>99.9</td><td>98.3</td><td>65.5</td><td>97.4</td><td>79.8</td></tr><tr><td>Hydra-MDP++ [29]</td><td>97.9</td><td>96.5</td><td>79.2</td><td>93.4</td><td>100</td><td>100.0</td><td>98.9</td><td>67.2</td><td>97.7</td><td>80.6</td></tr><tr><td>ARTEMIS [11]</td><td>98.3</td><td>95.1</td><td>81.5</td><td>97.4</td><td>100</td><td>99.8</td><td>98.6</td><td>96.5</td><td>98.3</td><td>83.1</td></tr><tr><td>ReCogDrive-8B [27]</td><td>98.3</td><td>95.2</td><td>87.1</td><td>97.5</td><td>98.3</td><td>99.8</td><td>99.5</td><td>96.6</td><td>86.5</td><td>83.6</td></tr><tr><td>DiffusionDrive [30]</td><td>98.0</td><td>96.0</td><td>87.7</td><td>97.1</td><td>98.3</td><td>99.8</td><td>99.5</td><td>97.2</td><td>87.6</td><td>84.3</td></tr><tr><td>SGDrive-2B (ours)</td><td>98.6</td><td>94.3</td><td>86.0</td><td>97.9</td><td>98.3</td><td>99.9</td><td>99.5</td><td>96.1</td><td>85.9</td><td>86.2</td></tr></table>

Dataset and evaluation metrics. NAVSIM [9] is a largescale real-world autonomous driving dataset designed for non-reactive simulation and benchmarking. It focuses on challenging scenarios involving dynamic intention changes, while filtering out trivial cases such as stationary or constant-speed driving. It is split into two subsets: navtrain (1,192 scenarios) for training and validation, and navtest (136 scenarios) for testing. As for the evaluation metrics, we evaluate our method using the Predictive Driver Model Score (PDMS) and the Extended PDMS (EPDMS), as defined in the official benchmark. PDMS consists of several sub-scores, including No At-Fault Collisions (NC), Drivable Area Compliance (DAC), Time-to-Collision (TTC), Comfort (Comf.), and Ego Progress (EP). EPDMS further introduces Traffic Light Compliance (TL), Lane Keeping Ability (LK), and Extended Comfort (EC), providing a more comprehensive evaluation.

## 4.2. Main result.

## Results on NAVSIM v1 with SFT.

As shown in Table 1, we compare SGDrive against stateof-the-art approaches on the NAVSIM test split. Our approach, built upon an InternVL3-2B backbone and trained using our proposed two-stage supervised fine-tuning strategy, achieves a new state-of-the-art PDMS score of 87.4. This result is notable for several reasons. First, it surpasses larger general-purpose VLMs like InternVL3-8B and QwenVL2.5-8B by a significant 4.1 PDMS, demonstrating the superior performance of our specialized architecture. Second, SGDrive-2B model outperforms the previous state-of-the-art driving VLM method, Recogdrive-8B [27], by 0.6 PDMS. This highlights the profound effectiveness of guiding the VLM to learn and forecast hierarchical world knowledge, as this enables a more compact model to achieve superior planning performance. Third, SGDrive relay on image-only input outperforms the vast majority of listed end-to-end methods that rely on both image and Li-DAR inputs.

Crucially, our method achieves the best scores on the key collision-related metrics, NC and TTC. This strongly validates our core hypothesis: by explicitly forecasting the spatio-temporal layout, dynamic agent interactions, and short-term goals, the model gains a superior spatialtemporal awareness that is paramount for anticipating and avoiding potential collisions.

Results on NAVSIM v1 with RFT. Although our method primarily aims to learn hierarchical driving-world knowledge to improve driving safety, it can be seamlessly integrated with existing RL frameworks. Under the same RL training configuration as RecogDrive [27], our approach achieves substantially better results, as shown in Table 1. By incorporating structured world knowledge features into the RL pipeline, our method achieves a PDMS of 91.1, outperforming all existing methods, including those using Li-DAR inputs. Compared with other RL-based approaches, our model achieves the best performance on NC and DAC, indicating that the learned driving-world knowledge effectively reduces collision risk and improves compliance with drivable regions. In future work, we plan to explore RL algorithms specifically tailored to our hierarchical world knowledge forecasting framework to further improve driving efficiency and smoothness.

Results on NAVSIM v2 with SFT. To comprehensively evaluate our approach, we also follow prior work [29] and adopt the Extended PDMS metric on the NAVSIM [9] benchmark. As shown in Table 2, SGDrive achieves the best overall performance with an EPDMS of 86.2, outperforming the previous state-of-the-art ReCogDrive-8B by 2.6 points. Our method also delivers the strongest results on the safety-critical NC and TTC metrics, while maintaining competitive performance on the newly introduced TL, LK, and EC metrics. These results collectively demonstrate the effectiveness and robustness of SGDrive in modeling driving-relevant world knowledge under the extended eval-

![](images/16057aeb9b27193198c57219a9df1008deb5ae5763be291beec8709c4a230fc5.jpg)  
Figure 4. Comparisons with state-of-the-art method on the Navtest benchmark.

Table 3. Ablation study on the proposed components of SGDrive.
<table><tr><td colspan="8">Exp. Base Current Future NC↑ DAC↑ TTC↑ EP↑ PDMS↑</td></tr><tr><td>a</td><td>√</td><td>x</td><td>x</td><td>97.3</td><td>91.1</td><td>92.9</td><td>76.8 82.2</td></tr><tr><td>b</td><td>√</td><td>√</td><td>X</td><td>98.3</td><td>93.0</td><td>94.9 78.2</td><td>84.7</td></tr><tr><td>c</td><td>√</td><td>√</td><td>√</td><td>98.4</td><td>93.6</td><td>94.9 79.3</td><td>85.5</td></tr></table>

uation protocol.

## 4.3. Ablation study

## Effect of our driving-world knowledge forecast.

We first evaluate the effectiveness of our proposed driving-world knowledge learning in stage 1, where trajectories are produced in text form and the result is shown in Table 3. When the model is trained only to represent the multi-level structure of the current world state, as in Exp.(b), it achieves a 2.5 points improvement in PDMS over Exp.(a). This notable gain demonstrates that our hierarchical world representation successfully activates the model’s understanding of the 3D driving environment, leading to more accurate trajectory predictions. When we further incorporatefuture world forecasting in Exp.(c), the performance increases to 85.5 PDMS, along with additional improvements in the NC and EP metrics compared with Exp.(b). These results show that enabling the VLM to forecast future world evolution provides stronger safety awareness and planning efficiency, ultimately producing reliable autonomous driving behavior.

## Ablation of world query for downstream planning.

To assess the effectiveness of each subquery within our 〈world〉queries, we conduct ablation studies on the downstream trajectory planning task using the stage 2 diffusion planner, and the result is shown in Table 4. Exp.(a) employs only the scene-geometry layout to modulate trajectory generation, achieving a PDMS of 86.0. When safetycritical agents information is added, notable improvements are observed in key metrics such as NC and DAC, Exp.(b). Exp.(c) add driving goals into condition further leads to a significant enhancement in EP, indicating that activating high-level semantic intent effectively improves driving efficiency. Finally, incorporating future world-state predictions to guide the planner yields consistent gains across multiple metrics, resulting in a PDMS of 87.4. The additional improvements in TTC and NC further demonstrate that modeling the evolution of future scenes and road-user motions enables the planner to better anticipate potential hazards and avoid collisions. These comprehensive results demonstrate that our proposed scene-agent-goal hierarchical cognition framework provides effective world knowledge guidance and substantially enhances overall driving performance.

Table 4. Ablation study on the world query of SGDrive.
<table><tr><td colspan="7">Exp. Scene Agent Goal Furture NC↑ DAC↑ TTC↑ EP↑ PDMS↑</td></tr><tr><td>a</td><td>√</td><td>x</td><td>x</td><td>x</td><td>98.2 94.1</td><td>94.4 80.2 86.0</td></tr><tr><td>b</td><td>√</td><td>√</td><td>x</td><td>x</td><td>98.3 94.5 94.8</td><td>80.4 86.3</td></tr><tr><td>c</td><td>√</td><td>√</td><td>√</td><td>x</td><td>98.5 94.9 95.1</td><td>81.2 87.0</td></tr><tr><td>d</td><td>√</td><td>√</td><td>√</td><td>√</td><td>98.6 95.1</td><td>95.4 81.2 87.4</td></tr></table>

Table 5. Ablation study on the attention mask of SGDrive.
<table><tr><td>Method</td><td>NC↑</td><td>TTC↑</td><td>EP↑</td><td>PDMS↑</td></tr><tr><td>Causal</td><td>98.4</td><td>95.6</td><td>80.1</td><td>87.1</td></tr><tr><td>Structure</td><td>98.6</td><td>95.4</td><td>81.2</td><td>87.4</td></tr></table>

## Effect of structured attention masking.

We compare our attention mechanism with default causal-attention method, as shown in Figure 3. Causalattention exposes each world query to all preceding tokens, introducing cross-category noise and semantic leakage; this corrupts world representations and causes the vehicle to adopt overly conservative behaviors (e.g., slowing excessively to avoid potential collisions), thereby reducing driving efficiency. By contrast, our structured attention restricts visibility to same-type information, producing cleaner, task-specific embeddings. As shown in Table 5, this design yields a favorable trade-off: it improves EP, yielding a higher overall PDMS and more realistic driving behavior.

![](images/2e1f6551d6fc04e300f4cd5a65e048b9b21384ebefc1bf9ff04b321a2b767749.jpg)  
Figure 5. Qualitative visualization of our model’s predictions (top row) versus the ground truth (bottom row). The visualization shows our model accurately forecasts these hierarchical states, which closely align with the ground truth.

![](images/80f6407a5f10025042e83572bc00a375601be8cb1d93d3fc6559a2b962cd9d8c.jpg)  
Figure 6. Ego-motion based adaptive geometric scene perception.

## 4.4. Qualitative Results.

Compare with previous method. We select two representative scenarios to qualitatively compare our method with the previous state-of-the-art, RecogDrive [27], as shown in Figure 4. In the first scenario, involving multiple road users, RecogDrive’s predicted trajectory deviates significantly from the ground truth, leading to a potential collision. In contrast, our SGDrive empowered by explicit safety-critical agent detection, generates an optimal and collision-free trajectory. In the second, relatively open yet curved-road scenario, RecogDrive’s prediction drifts out of the lane and collides with the roadside barrier. Our model, however, accurately perceives the scene’s geometric layout and successfully avoids the collision. These results demonstrate that SGDrive effectively learns structured drivingworld knowledge and can extrapolate it reasonably to ensure safe and rational driving behavior.

Explicit world knowledge representation. In Figure 5, we provide a qualitative comparison between our model’s predictions and the ground-truth annotations. The visualizations show a strong alignment across the scene-agent– goal hierarchy. This consistency indicates that our model has learned rich driving-world knowledge, enabling reliable perception and representation of both the current state and its short-horizon future evolution.

Adaptive geometric scene perception. As shown in the Figure 6, SGDrive adaptively perceives the driving scene according to the ego-vehicle’s motion state and navigation command. For instance, at high speeds, it expands its perceptual horizon, whereas during turning maneuvers, it redirects its perceptual focus toward the turning direction. This demonstrates a more structured and effective representation of driving-relevant world knowledge, providing strong evidence that SGDrive successfully elicits the VLM’s worldmodeling ability.

## 5. Conclusion

We introduce SGDrive, a novel framework that explicitly structures a VLM’s representation learning around a driving-specific knowledge hierarchy, enabling safer and more reliable autonomous driving. Our method leverages a scene-agent-goal hierarchical cognition scheme that disentangles the understanding of driving environments: it models the current world through scene geometry, road users, and driving goals, and further extrapolates their evolution into the future. To support this, we design a structured attention-mask mechanism that prevents information leakage and suppresses cross-category noise. Finally, by integrating a DiT-based planner, our approach uses the inferred driving-world knowledge to regulate trajectory generation. Comprehensive experiments on NAVSIM demonstrate the effectiveness of our method and show that it achieves stateof-the-art performance in safe driving.

## References

[1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. arXiv preprint arXiv:2303.08774, 2023. 1, 2

[2] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, Humen Zhong, Yuanzhi Zhu, Mingkun Yang, Zhaohai Li, Jianqiang Wan, Pengfei Wang, Wei Ding, Zheren Fu, Yiheng Xu, Jiabo Ye, Xi Zhang, Tianbao Xie, Zesen Cheng, Hang Zhang, Zhibo Yang, Haiyang Xu, and Junyang Lin. Qwen2.5-vl technical report, 2025. 6

[3] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. π<sub>0</sub>: A vision-languageaction flow model for general robot control. arXiv preprint arXiv:2410.24164, 2024. 2, 5

[4] Nicolas Carion, Francisco Massa, Gabriel Synnaeve, Nicolas Usunier, Alexander Kirillov, and Sergey Zagoruyko. End-toend object detection with transformers, 2020. 2, 4

[5] Sergio Casas, Abbas Sadat, and Raquel Urtasun. Mp3: A unified model to map, perceive, predict and plan. In CVPR, 2021. 2

[6] Shaoyu Chen, Bo Jiang, Hao Gao, Bencheng Liao, Qing Xu, Qian Zhang, Chang Huang, Wenyu Liu, and Xinggang Wang. Vadv2: End-to-end vectorized autonomous driving via probabilistic planning. arXiv preprint arXiv:2402.13243, 2024. 2, 6, 7

[7] Zhe Chen, Jiannan Wu, Wenhai Wang, Weijie Su, Guo Chen, Sen Xing, Muyan Zhong, Qinglong Zhang, Xizhou Zhu, Lewei Lu, et al. Internvl: Scaling up vision foundation models and aligning for generic visual-linguistic tasks. In CVPR, 2024. 1, 6

[8] Haohan Chi, Huan ang Gao, Ziming Liu, Jianing Liu, Chenyu Liu, Jinwei Li, Kaisen Yang, Yangcheng Yu, Zeda Wang, Wenyi Li, Leichen Wang, Xingtao Hu, Hao Sun, Hang Zhao, and Hao Zhao. Impromptu vla: Open weights and open data for driving vision-language-action models, 2025. 1

[9] Daniel Dauner, Marcel Hallgarten, Tianyu Li, Xinshuo Weng, Zhiyu Huang, Zetong Yang, Hongyang Li, Igor Gilitschenski, Boris Ivanovic, Marco Pavone, et al. Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking. In NeurIPS, 2024. 7, 1

[10] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. Carla: An open urban driving simulator. In CoRL, 2017. 2

[11] Renju Feng, Ning Xi, Duanfeng Chu, Rukang Wang, Zejian Deng, Anzheng Wang, Liping Lu, Jinxiang Wang, and Yanjun Huang. Artemis: Autoregressive end-to-end trajectory planning with mixture of experts for autonomous driving, 2025. 6, 7

[12] Haoyu Fu, Diankun Zhang, Zongchuang Zhao, Jianfeng Cui, Dingkang Liang, Chong Zhang, Dingyuan Zhang, Hongwei Xie, Bing Wang, and Xiang Bai. Orion: A holistic end-toend autonomous driving framework by vision-language in-

structed action generation. arXiv preprint arXiv:2503.19755, 2025. 2, 3

[13] Shengchao Hu, Li Chen, Penghao Wu, Hongyang Li, Junch Yan, and Dacheng Tao. St-p3: End-to-end vision-based autonomous driving via spatial-temporal feature learning. In ECCV, 2022. 1, 2

[14] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, et al. Planning-oriented autonomous driving. In CVPR, 2023. 1, 2, 6

[15] Zhijian Huang, Chengjian Feng, Feng Yan, Baihui Xiao, Zequn Jie, Yujie Zhong, Xiaodan Liang, and Lin Ma. Drivemm: All-in-one large multimodal model for autonomous driving. arXiv preprint arXiv:2412.07689, 2024. 1, 2

[16] Jyh-Jing Hwang, Runsheng Xu, Hubert Lin, Wei-Chih Hung, Jingwei Ji, Kristy Choi, Di Huang, Tong He, Paul Covington, Benjamin Sapp, et al. Emma: End-to-end multimodal model for autonomous driving. arXiv preprint arXiv:2410.23262, 2024. 1, 3

[17] Bernhard Jaeger, Kashyap Chitta, and Andreas Geiger. Hidden biases of end-to-end driving models. In Proceedings ofthe IEEE/CVF International Conference on Computer Vi sion, pages 8240–8249, 2023. 2

[18] Xiaosong Jia, Penghao Wu, Li Chen, Jiangwei Xie, Conghui He, Junchi Yan, and Hongyang Li. Think twice before driving: Towards scalable decoders for end-to-end autonomous driving. In CVPR, 2023. 2

[19] Xiaosong Jia, Zhenjie Yang, Qifeng Li, Zhiyuan Zhang, and Junchi Yan. Bench2drive: Towards multi-ability benchmarking of closed-loop end-to-end autonomous driving. In NeurIPS, 2024. 2

[20] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. Vad: Vectorized scene representation for efficient autonomous driving. In ICCV, 2023. 1, 2

[21] Bo Jiang, Shaoyu Chen, Bencheng Liao, Xingyu Zhang, Wei Yin, Qian Zhang, Chang Huang, Wenyu Liu, and Xinggang Wang. Senna: Bridging large vision-language mod els and end-to-end autonomous driving. arXiv preprint arXiv:2410.22313, 2024. 3

[22] Napat Karnchanachari, Dimitris Geromichalos, Kok Seang Tan, Nanxiang Li, Christopher Eriksen, Shakiba Yaghoubi, Noushin Mehdipour, Gianmarco Bernasconi, Whye Kit Fong, Yiluan Guo, et al. Towards learning-based planning: The nuplan benchmark for real-world autonomous driving. In ICRA, 2024. 2

[23] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. arXiv preprint arXiv:2406.09246, 2024. 2, 5

[24] Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. BLIP-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. In ICML, 2023. 2

[25] Jingyu Li, Bozhou Zhang, Xin Jin, Jiankang Deng, Xiatian Zhu, and Li Zhang. Imagidrive: A unified imagination-andplanning framework for autonomous driving. arXiv preprint arXiv:2508.11428, 2025. 3

[26] Yingyan Li, Yuqi Wang, Yang Liu, Jiawei He, Lue Fan, and Zhaoxiang Zhang. End-to-end driving with online trajectory evaluation via bev world model, 2025. 2, 6

[27] Yongkang Li, Kaixin Xiong, Xiangyu Guo, Fang Li, Sixu Yan, Gangwei Xu, Lijun Zhou, Long Chen, Haiyang Sun, Bing Wang, Kun Ma, Guang Chen, Hangjun Ye, Wenyu Liu, and Xinggang Wang. Recogdrive: A reinforced cognitive framework for end-to-end autonomous driving, 2025. 2, 3, 6, 7, 9

[28] Zhiqi Li, Wenhai Wang, Hongyang Li, Enze Xie, Chonghao Sima, Tong Lu, Yu Qiao, and Jifeng Dai. Bevformer: Learning bird’s-eye-view representation from multi-camera images via spatiotemporal transformers. In ECCV, 2022. 2

[29] Zhenxin Li, Kailin Li, Shihao Wang, Shiyi Lan, Zhiding Yu, Yishen Ji, Zhiqi Li, Ziyue Zhu, Jan Kautz, Zuxuan Wu, et al. Hydra-mdp: End-to-end multimodal planning with multitarget hydra-distillation. arXiv preprint arXiv:2406.06978, 2024. 6, 7, 1

[30] Bencheng Liao, Shaoyu Chen, Haoran Yin, Bo Jiang, Cheng Wang, Sixu Yan, Xinbang Zhang, Xiangyu Li, Ying Zhang, Qian Zhang, and Xinggang Wang. Diffusiondrive: Truncated diffusion model for end-to-end autonomous driving. In CVPR, 2025. 2, 6, 7

[31] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. In NeurIPS, 2024. 2

[32] Ruixun Liu, Lingyu Kong, Derun Li, and Hang Zhao. Occvla: Vision-language-action model with implicit 3d occupancy supervision. arXiv preprint arXiv:2509.05578, 2025. 4

[33] Yingfei Liu, Tiancai Wang, Xiangyu Zhang, and Jian Sun. Petr: Position embedding transformation for multi-view 3d object detection. In ECCV, 2022. 2

[34] Zhe Liu, Runhui Huang, Rui Yang, Siming Yan, Zining Wang, Lu Hou, Di Lin, Xiang Bai, and Hengshuang Zhao. Drivepi: Spatial-aware 4d mllm for unified autonomous driving understanding, perception, prediction and planning. arXiv preprint arXiv:2512.12799, 2025. 3

[35] Ana-Maria Marcu, Long Chen, Jan Hunermann, Alice Karn-¨ sund, Benoit Hanotte, Prajwal Chidananda, Saurabh Nair, Vijay Badrinarayanan, Alex Kendall, Jamie Shotton, et al. Lingoqa: Visual question answering for autonomous driving. In ECCV, 2024. 2

[36] Ming Nie, Renyuan Peng, Chunwei Wang, Xinyue Cai, Jianhua Han, Hang Xu, and Li Zhang. Reason2drive: Towards interpretable and chain-based reasoning for autonomous driving. In ECCV, 2024. 2

[37] William Peebles and Saining Xie. Scalable diffusion models with transformers. In CVPR, 2023. 2, 4, 5

[38] Aditya Prakash, Kashyap Chitta, and Andreas Geiger. Multimodal fusion transformer for end-to-end autonomous driving. In CVPR, 2021. 2, 6, 7

[39] Zekun Qi, Runpei Dong, Guofan Fan, Zheng Ge, Xiangyu Zhang, Kaisheng Ma, and Li Yi. Contrast with reconstruct:

Contrastive 3d representation learning guided by generative pretraining. In International Conference on Machine Learning, pages 28223–28243. PMLR, 2023. 2

[40] Tianwen Qian, Jingjing Chen, Linhai Zhuo, Yang Jiao, and Yu-Gang Jiang. Nuscenes-qa: A multi-modal visual question answering benchmark for autonomous driving scenario. In AAAI, 2024. 2

[41] Katrin Renz, Long Chen, Elahe Arani, and Oleg Sinavski. Simlingo: Vision-only closed-loop autonomous driving with language-action alignment. In CVPR, 2025. 3

[42] Hao Shao, Letian Wang, Ruobing Chen, Hongsheng Li, and Yu Liu. Safety-enhanced autonomous driving using interpretable sensor fusion transformer. In CoRL, pages 726–737, 2023. 2

[43] Chonghao Sima, Katrin Renz, Kashyap Chitta, Li Chen, Hanxue Zhang, Chengen Xie, Ping Luo, Andreas Geiger, and Hongyang Li. Drivelm: Driving with graph visual question answering. In ECCV, 2024. 1, 2

[44] Shuran Song, Fisher Yu, Andy Zeng, Angel X Chang, Manolis Savva, and Thomas Funkhouser. Semantic scene comple tion from a single depth image. In CVPR, 2017. 4

[45] Wenchao Sun, Xuewu Lin, Yining Shi, Chuang Zhang, Hao ran Wu, and Sifa Zheng. Sparsedrive: End-to-end autonomous driving via sparse scene representation. In ICRA, 2025. 1, 2

[46] Gemini Team, Rohan Anil, Sebastian Borgeaud, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican, et al. Gemini: a family of highly capable multimodal models. arXiv preprint arXiv:2312.11805, 2023. 3

[47] Xiaoyu Tian, Tao Jiang, Longfei Yun, Yucheng Mao, Huitong Yang, Yue Wang, Yilun Wang, and Hang Zhao. Occ3d: A large-scale 3d occupancy prediction benchmark for autonomous driving. NeurIPS, 2023. 4

[48] Xiaoyu Tian, Junru Gu, Bailin Li, Yicheng Liu, Yang Wang, Zhiyong Zhao, Kun Zhan, Peng Jia, Xianpeng Lang, and Hang Zhao. Drivevlm: The convergence of autonomous driving and large vision-language models. In CoRL, 2024. 3

[49] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothee Lacroix, Baptiste´ Roziere, Naman Goyal, Eric Hambro, Faisal Azhar, et al.\` Llama: Open and efficient foundation language models. arXiv preprint arXiv:2302.13971, 2023. 1

[50] Aaron Van Den Oord, Oriol Vinyals, et al. Neural discrete representation learning. NeurIPS, 2017. 4

[51] Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, et al. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution. arXiv preprint arXiv:2409.12191, 2024. 1

[52] Shihao Wang, Zhiding Yu, Xiaohui Jiang, Shiyi Lan, Min Shi, Nadine Chang, Jan Kautz, Ying Li, and Jose M Alvarez. Omnidrive: A holistic vision-language dataset for autonomous driving with counterfactual reasoning. In CVPR, 2025. 1

[53] Xinshuo Weng, Boris Ivanovic, Yan Wang, Yue Wang, and Marco Pavone. Para-drive: Parallelized architecture for realtime autonomous driving. In CVPR, 2024. 6

[54] Katharina Winter, Mark Azer, and Fabian B. Flohr. Bevdriver: Leveraging bev maps in llms for robust closed-loop driving, 2025. 2, 6

[55] Shuo Xing, Chengyuan Qian, Yuping Wang, Hongyuan Hua, Kexin Tian, Yang Zhou, and Zhengzhong Tu. Openemma: Open-source multimodal model for end-to-end autonomous driving. In WACV, 2025. 1

[56] Lihe Yang, Bingyi Kang, Zilong Huang, Xiaogang Xu, Jiashi Feng, and Hengshuang Zhao. Depth anything: Unleashing the power of large-scale unlabeled data. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 10371–10381, 2024. 2

[57] Yu Yang, Jianbiao Mei, Yukai Ma, Siliang Du, Wenqing Chen, Yijie Qian, Yuxiang Feng, and Yong Liu. Driving in the occupancy world: Vision-centric 4d occupancy forecasting and planning via world models for autonomous driving. In AAAI, 2025. 2

[58] Chengran Yuan, Zhanqi Zhang, Jiawei Sun, Shuo Sun, Zefan Huang, Christina Dao Wen Lee, Dongen Li, Yuhang Han, Anthony Wong, Keng Peng Tee, et al. Drama: An efficient end-to-end motion planner for autonomous driving with mamba. arXiv preprint, 2024. 6

[59] Shuang Zeng, Xinyuan Chang, Mengwei Xie, Xinran Liu, Yifan Bai, Zheng Pan, Mu Xu, and Xing Wei. FutureSight-Drive: Thinking visually with spatio-temporal CoT for autonomous driving, 2025. 3

[60] Bozhou Zhang, Jingyu Li, Nan Song, and Li Zhang. Perception in plan: Coupled perception and planning for end-to-end autonomous driving. In AAAI, 2025. 2

[61] Bozhou Zhang, Nan Song, Xin Jin, and Li Zhang. Bridging past and future: End-to-end autonomous driving with historical prediction and planning. In CVPR, 2025. 2

[62] Bozhou Zhang, Nan Song, Jingyu Li, Xiatian Zhu, Jiankang Deng, and Li Zhang. Future-aware end-to-end driving: Bidirectional modeling of trajectory planning and scene evolution. In NeurIPS, 2025. 6

[63] Diankun Zhang, Guoan Wang, Runwen Zhu, Jianbo Zhao, Xiwu Chen, Siyu Zhang, Jiahao Gong, Qibin Zhou, Wenyuan Zhang, Ningzi Wang, et al. Sparsead: Sparse query-centric paradigm for efficient end-to-end autonomous driving. arXiv preprint arXiv:2404.06892, 2024. 2

[64] Kaiwen Zhang, Zhenyu Tang, Xiaotao Hu, Xingang Pan, Xiaoyang Guo, Yuan Liu, Jingwei Huang, Li Yuan, Qian Zhang, Xiao-Xiao Long, et al. Epona: Autoregressive diffusion world model for autonomous driving. arXiv preprint arXiv:2506.24113, 2025. 6

[65] Wenyao Zhang, Hongsi Liu, Zekun Qi, Yunnan Wang, Xinqiang Yu, Jiazhao Zhang, Runpei Dong, Jiawei He, Fan Lu, He Wang, Zhizheng Zhang, Li Yi, Wenjun Zeng, and Xin Jin. Dreamvla: A vision-language-action model dreamed with comprehensive world knowledge, 2025. 2

[66] Wenzhao Zheng, Weiliang Chen, Yuanhui Huang, Borui Zhang, Yueqi Duan, and Jiwen Lu. Occworld: Learning a 3d occupancy world model for autonomous driving. In ECCV, 2024. 2

[67] Xingcheng Zhou, Xuyuan Han, Feng Yang, Yunpu Ma, and Alois C Knoll. Opendrivevla: Towards end-to-end autonomous driving with large vision language action model. arXiv preprint arXiv:2503.23463, 2025. 3

[68] Xin Zhou, Dingkang Liang, Sifan Tu, Xiwu Chen, Yikang Ding, Dingyuan Zhang, Feiyang Tan, Hengshuang Zhao, and Xiang Bai. Hermes: A unified self-driving world model for simultaneous 3d scene understanding and generation. In ICCV, 2025. 2

[69] Zewei Zhou, Tianhui Cai, Yun Zhao, Seth Z.and Zhang, Zhiyu Huang, Bolei Zhou, and Jiaqi Ma. Autovla: A visionlanguage-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning. NeurIPS, 2025. 6

[70] Deyao Zhu, Jun Chen, Xiaoqian Shen, Xiang Li, and Mohamed Elhoseiny. Minigpt-4: Enhancing vision-language understanding with advanced large language models. arXiv preprint arXiv:2304.10592, 2023. 2

[71] Jinguo Zhu, Weiyun Wang, Zhe Chen, Zhaoyang Liu, Shenglong Ye, Lixin Gu, Hao Tian, Yuchen Duan, Weijie Su, Jie Shao, Zhangwei Gao, Erfei Cui, Xuehui Wang, Yue Cao, Yangzhou Liu, Xingguang Wei, Hongjie Zhang, Haomin Wang, Weiye Xu, Hao Li, Jiahao Wang, Nianchen Deng, Songze Li, Yinan He, Tan Jiang, Jiapeng Luo, Yi Wang, Con ghui He, Botian Shi, Xingcheng Zhang, Wenqi Shao, Junjun He, Yingtong Xiong, Wenwen Qu, Peng Sun, Penglong Jiao, Han Lv, Lijun Wu, Kaipeng Zhang, Huipeng Deng, Jiaye Ge, Kai Chen, Limin Wang, Min Dou, Lewei Lu, Xizhou Zhu, Tong Lu, Dahua Lin, Yu Qiao, Jifeng Dai, and Wenhai Wang. Internvl3: Exploring advanced training and test-time recipes for open-source multimodal models, 2025. 4, 6

# SGDrive: Scene-to-Goal Hierarchical World Cognition for Autonomous Driving Supplementary Material

Table 6. Comparison of hidden state fusion methods in diffusion planner.
<table><tr><td>Exp.</td><td>NC↑</td><td>TTC↑</td><td>EP↑</td><td>PDMS↑</td></tr><tr><td>(a)</td><td>98.2</td><td>95.0</td><td>80.6</td><td>87.1</td></tr><tr><td>(b)</td><td>98.1</td><td>95.1</td><td>79.7</td><td>86.9</td></tr><tr><td>(c)</td><td>98.6</td><td>95.4</td><td>81.2</td><td>87.4</td></tr></table>

## 6. More experiments

## 6.1. Comparison of hidden state fusion methods in diffusion planner

As shown in Table 6, we compare several strategies for fusing hidden states within the diffusion planner. Exp. (a) incrementally injects the hidden states of different subqueries across successive cross-attention layers. Exp. (b) assigns distinct cross-attention layers to different subqueries. Exp. (c), which corresponds to our proposed design, concatenates all subquery hidden states and enables interaction at every cross-attention layer. All fusion strategies achieve strong performance, confirming that our subqueries encode rich driving-world knowledge and can effectively guide the trajectory generation process.

NAVSIM metric. NAVSIM [9] scores driving agents in two steps. First, subscores in range [0, 1] are computed after simulation. Second, these subscores are aggregated into the PDM Score $\mathbf { ( P D M S ) } \in [ 0 , 1 ]$ . We use the following aggregation of subscores based on the official definition:

$$
\begin{array} { r } { \mathrm { P D M S } = \underbrace { \left( \underset { m \in \{ \mathrm { N C } , \mathrm { D i C } \} } { \prod } \mathrm { s c o r e } _ { m } \right) } _ { \mathrm { p e n a l i e s } } \times } \\ { \underbrace { \left( \frac { \sum _ { w \in \{ \mathrm { E P } , \mathrm { T T C } , \mathrm { c } \} } w \in \mathrm { i g h t } _ { w } \times \mathrm { s c o r e } _ { w } } { \sum _ { w \in \{ \mathrm { E P } , \mathrm { T T C } , \mathrm { c } \} } w \in \mathrm { i g h t } _ { w } } \right) } _ { \mathrm { w e t a h e d u e n c e } } . } \end{array}\tag{8}
$$

Subscores are categorized by their importance as penalties or terms in a weighted average. A penalty punishes inadmissible behavior such as collisions with a factor < 1. The weighted average aggregates subscores for other objectives such as progress and comfort.

NAVSIM metric with extended PDMS. Hydra-MDP++ [29] extends the original PDMS metric by incorporating additional aspects of driving performance, including Traffic Lights Compliance (TL), Lane Keeping Ability (LK), and Extended Comfort (EC), providing a more comprehensive evaluation of a method’s effectiveness. Formally, the Extended PDM Score (EPDMS) is computed as:

$$
\begin{array} { r l } { \mathrm { E P D M S } = } & { \underbrace { \prod _ { m \in \{ \mathrm { N C , D A C , D D C , T L } \} } } _ { \mathrm { p e n a l y ~ t e r m s } } } \\ & { \times \underbrace { \sum _ { w \in \{ \mathrm { E P , T T C , C , L K , E C } \} } \mathrm { w e i g h t } _ { w } \cdot S ^ { w } } _ { \mathrm { w e \ ' { E } \in \{ \mathrm { E P , T T C , C , L K , E C } \} } } . } \end{array}\tag{9}
$$

Here, the first term accumulates multiplicative penalties for safety-critical violations, while the second term computes a weighted average over positive performance indicators, providing a balanced assessment of driving quality and comfort.

## 7. Additional visualizations

## 7.1. Qualitative results

We provide additional qualitative results in Figure 7 and Figure 8. For both straight-driving and turning scenarios, our predicted trajectories closely follow the ground truth. We also include several failure cases.

## 7.2. Failure cases

As illustrated in Figure 9, when relying solely on a single front-view image, the model may exhibit slight deviations under extreme turning conditions. In such scenarios, due to the absence of corresponding viewpoints, accurately predicting long-horizon trajectories becomes challenging, sometimes leading to lane-change errors. Incorporating multi-view inputs is a promising direction to mitigate these limitations in future work.

![](images/65b380b3afff2d18b43eac110aa2cd6a12c3fb5d87b7c697c079d608431c3b2c.jpg)  
Go straight  
Figure 7. Qualitative results on the Navtest benchmark.

![](images/690164090755541a5c851dd54a14969a380992a979a53b6469923961fb218a95.jpg)  
Turn left

![](images/c3bc767ed509695549e63d966a89f92048722682baf4227a09d1e37046829f89.jpg)  
Turn right  
Figure 8. Qualitative results on the Navtest benchmark.

![](images/492991c195173f36073e5d578f63f139c17fba6e84f6f00fc9151b2294a9f4ba.jpg)  
Failure cases  
Figure 9. Qualitative analysis of representative failure cases on the Navtest benchmark.