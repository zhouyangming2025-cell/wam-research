# DynFlowDrive: Flow-Based Dynamic World Modeling for Autonomous Driving

Xiaolu Liu<sup>1,2</sup>, Yicong Li<sup>2</sup>, Song Wang<sup>1</sup>, Junbo Chen<sup>3</sup>\*, Angela Yao<sup>2</sup>, and Jianke Zhu<sup>1⋆</sup>

<sup>1</sup>Zhejiang University, <sup>2</sup>National University of Singapore, <sup>3</sup>Udeer.AI {xialuliu, jkzhu}@zju.edu.cn

![](images/4396fb4820801e7e204206e0316016839d19287d3d0bb11c71bf547b915da901.jpg)  
(a) Performance Comparison on Various Methods

![](images/365991a01c7a0375cb25f5a6c0e0a0a9a0fc669d5d63501f291b3491d789ab28.jpg)  
(b) Visualization of Planning Results  
Fig. 1: (a) Comparisons of perception-based and latent world model-based approaches on nuScenes and NavSim benchmarks. (b) Planning visualization on the front view and bird’s-eye-view (BEV) space. Our DynFlowDrive achieves comparable performance.

Abstract. Recently, world models have been incorporated into the autonomous driving systems to improve the planning reliability. Existing approaches typically predict future states through appearance generation or deterministic regression, which limits their ability to capture trajectory-conditioned scene evolution and leads to unreliable action planning. To address this, we propose DynFlowDrive, a latent world model that leverages flow-based dynamics to model the transition of world states under diferent driving actions. By adopting the rectifiedflow formulation, the model learns a velocity field that describes how the scene state changes under diferent driving actions, enabling progressive prediction of future latent states. Building upon this, we further introduce a stability-aware multi-mode trajectory selection strategy that evaluates candidate trajectories according to the stability of the induced scene transitions. Extensive experiments on the nuScenes and NavSim benchmarks demonstrate consistent improvements across diverse driving frameworks without introducing additional inference overhead. Source code will be available at https://github.com/xiaolul2/DynFlowDrive.

Keywords: Autonomous Driving · Latent World Model · Trajectory Planning

<sup>⋆</sup> Corresponding authors.

## 1 Introduction

End-to-end autonomous driving has emerged as a promising paradigm for building driving systems [3, 7, 10, 18]. Given the data captured by onboard sensors, it aims to predict safe and reliable future trajectories for planning and control [4, 18, 50]. However, trajectory planning is a highly interactive process with the surroundings. A planned trajectory represents the intended action whose safety depends on how the environment responds after it is executed. Therefore, achieving reliable and safe planning requires anticipating future scene evolution, which remains a key challenge for autonomous driving systems.

To equip the vehicle with such foresight capabilities, a new line of research introduces world models [1,22] for the end-to-end methods [14,49]. By enabling action-conditioned future simulations, these approaches allow the system to foresee the consequences of candidate trajectories and anticipate potential risks, thereby supporting safer and more reliable driving decisions. World models mainly follow two approaches: one line of work predicts future scenes explicitly, for example, by generating pixel-level images or 3D occupancy grids [47,56, 58,60]. In contrast, another line of work models the scene prediction of the world in a latent space [24, 55, 62], without explicitly reconstructing the full scenes.

Despite the advances, existing world models still sufer from critical limitations. For explicit scene-level prediction, many approaches rely on difusion [12, 40] or autoregressive models [16, 58] to synthesize future observations. While produced visually pleasing results, these methods primarily focus on appearance details such as textures and lighting. The emphasis on high-frequency visual patterns overlooks the underlying geometry and dynamics, which introduces extra computational overhead without improving action-oriented reasoning.

On the other hand, latent-space world models shift the focus from appearance synthesis to inner features [24, 62]. As illustrated in Figure 2 (a), most works adopt the one-step regression that directly maps the current latent state to the next timestep. Such a static formulation simplifies the prediction as a rigid mapping and neglects the dynamic transition process, making it hard to assess the safety and feasibility of candidate actions. For instance, when a vehicle approaches pedestrians, it may either gradually slow down to yield or maintain speed and brake abruptly at the last moment. Although both actions may lead to a similar stopping position, the underlying scene evolution and safety implications are fundamentally diferent. Without modeling this transition process, the world model cannot faithfully capture trajectory-dependent dynamics or assess whether the induced evolution is smooth and physically plausible.

To bridge this gap, we argue that efective world modeling must move beyond discrete endpoint regression and explicitly formulate trajectory-conditioned scene evolution as a continuous dynamical system. Motivated by this, we propose DynFlowDrive, a latent world model that leverages flow-based dynamics to model the transition of world states under diferent driving actions. Specifically, based on the extracted latent features, DynFlowDrive adopts a rectified-flow formulation to model the transition dynamics in latent space and predict future latent states conditioned on the current observation and multiple candidate trajectories. The learned velocity field explicitly captures the rate of change of the scene during state transitions, enabling the model to capture how the environment progressively evolves under diferent driving actions. Building upon the learned flow dynamics, we further introduce the stability-aware multi-mode trajectory selection mechanism. By exploiting the velocity field produced by the flow-based world model, we derive a stability measure that reflects the smoothness of trajectory-conditioned scene transitions. Combined with trajectory error measured with the ground truth and latent reconstruction discrepancy, this dynamics-aware stable criterion enables more reliable planning assessment and trajectory selection for safer autonomous driving systems.

![](images/d7439b7ca32a8b3c403bd5b993b166307bdb17b1764219adbf06711a5dff0610.jpg)  
Fig. 2: Comparison between (a) the existing static world model and (b) the dynamic latent world model of our DynFlowDrive. Instead of the static regression of next-frame latents, we propose the dynamic modeling that learns a continuous velocity field v to capture the evolution of world transitions.

For evaluation, DynFlowDrive achieves comparable performance on challenging benchmarks, including nuScenes [2] and NavSim [9]. As shown in Figure 1, our method consistently improves planning accuracy for BEV-based and w/o BEV approaches. Without auxiliary tasks, DynFlowDrive is still comparable to perception-based models. In particular, compared with SSR [23], DynFlowDrive reduces the average $L _ { 2 }$ displacement error from 0.39m to 0.31m and achieves 88.7 PDMS on NavSim. Our main contributions are summarized as follows:

– We propose DynFlowDrive, a dynamic latent world model that leverages rectified flow to explicitly model dynamic world evolution, enabling the progressive next-frame latent prediction conditioned on candidate trajectories.

– We introduce the stability-aware multi-mode selection strategy that leverages the flow-based stability for more reliable trajectory selection.

– Extensive experiments demonstrate the consistent and stable performance improvements across autonomous driving paradigms, without introducing additional computational overhead during inference.

## 2 Related Work

End-to-End Autonomous Driving. Conventional autonomous systems decompose the whole paradigm into three stages: perception [29, 35, 36, 45, 46], prediction [34, 42, 51], and planning [13, 32]. Such modular designs often lead to error accumulation and substantial engineering overhead. To address these limitations, recent works explore end-to-end autonomous driving, which learns a direct mapping from sensory observations to driving actions or trajectories [19, 20, 30, 44]. Existing methods can be broadly categorized based on the form of action outputs, including regression-based methods [17,20], generation-based approaches [31, 61], and reinforcement-based methods [11, 53]. In regression-based approaches, UniAD [19], VAD [20], and SparseDrive [44] construct end-to-end architectures by leveraging BEV representations and vectorized or sparse queries. For generative methods, GenAD [61] leverages generative models for trajectory regression. DifusionDrive [31] and GoalFlow [52] utilize flow matching [33] and difusion policy [5] paradigms to sample multi-mode actions. For reinforcement learning-based approaches, recent studies [21,26,27] formulate autonomous driving as a sequential decision-making problem, which optimizes driving policies through reward design and interaction with the environment. In addition, some recent approaches incorporate large language models (LLMs) into visionlanguage-action (VLA) frameworks by injecting language context as high-level guidance for reasoning and decision-making [6, 26, 63].

However, most existing end-to-end driving methods lack the ability to reason about future scene dynamics under diferent driving actions. This limitation motivates the development of world models that simulate future world evolution to support more informed decision-making.

World Models for Autonomous Driving In autonomous driving systems, the world model aims to predict the future evolution of scenes following various actions [14,22,24,49,62]. Combining with the next state prediction, existing world models can be categorized into two types: future scene prediction [48, 49, 58–60] and feature-level world models in latent space [23–25, 55]. Representative works of future scene prediction focus on directly forecasting future observations or structured scene representations. For instance, GenAD [54], DrivingFuture [49], and Epona [58] predict future pixel-level scenes conditioned on actions, while DriveDreamer4D [59] extends this paradigm to 4D dynamic scene generation with 4D Gaussian Splatting reconstruction. Other approaches like UniOcc [48] and OccWorld [60] operate in voxelized or occupancy space, predicting future 3D occupancy or semantic fields to model scene evolution. Complementary to explicit scene forecasting, another line of research eforts learns the world model in a compact latent space, where the model predicts action-conditioned transitions over intermediate features rather than reconstructing full observations. LAW [24] and World4Drive [62] construct the world model in latent feature space for planning-oriented prediction, while SSR [23] and WoTE [25] further explore latent modeling in BEV space, moving beyond perspective-view representations.

For our design, DynFlowDrive avoids explicit pixel-level scene generation and instead operates in latent space, focusing on modeling the underlying dynamics of world evolution for action-conditioned prediction.

![](images/be52db43d62fcd4bd9824fcfa65713d959eb2e59876b53c852d7308b019da451.jpg)  
Stability-aware Fig. 3: Overview of DynFlowDrive. Given current observations, multi-mode tra-Multi-Mode Selector<sub>jectories are firstly generated by the standard planning module. A flow-based dynamic</sub> latent world model is incorporated to simulate the progressive future evolution in la-"tent space. The resulting dynamics are used by a stability-aware multi-mode selection Dynamic Latent World Model,-./. +module, which assess the trajectory based on reconstruction quality and flow-based <sub>Sup.</sub>\$stability, enabling reliable supervision and improved planning robustness.

## 3 Method

Grad.As illustrated in Figure 3, DynFlowDrive is built upon a standard end-to-end 𝑛∗ = arg𝑚! z+Trajectory Planning planning framework together with a flow-based latent world modeling. Given Conditio<sup>Paradigm</sup> the surrounding N-view camera images $\mathbf { I } _ { t } = \{ I _ { t } ^ { i } \} _ { i = } ^ { N }$ and a high-level navigation command cmd at current timestep t, a vision-based approach aims to predict the planning trajectory T that consists of a set of future points in BEV space. DynFlowDrive comprises three key parts: 1) Trajectory Planning Paradigm (Sec. 3.1), which produces multi-mode trajectories based on the observations following the standard planning paradigm in end-to-end autonomous driving; 2) Dynamic World Model Prediction (Sec. 3.2), that simulates latent scenes’ evolution conditioned on the planning trajectory with the flow-based dynamic model, and 3) Stability-aware Multi-mode Selection (Sec. 3.3), which selects trajectory modes with respect to the dynamic stability for reliable supervision. These modules work in a complementary manner, coupling dynamic world simulation with multi-mode trajectory selection.

## 3.1 Trajectory Planning Paradigm

As shown in the yellow part of Figure 3, the trajectory planning paradigm predicts multiple candidate trajectories. It first encodes the sensor inputs into a unified scene representation, a trajectory decoder then attends to the scene queries to iteratively refine the trajectory queries into final trajectory proposals.

Scene Encoder. Given multi-view images $\mathbf { I } _ { t } = \{ I _ { t } ^ { i } \} _ { i = 1 } ^ { V }$ at the current timestep t, each view is encoded into perspective-view features $\mathbf { \bar { F } } _ { t } ^ { \mathrm { p v } } = \{ \mathbf { F } _ { t } ^ { i } \} _ { i = 1 } ^ { V }$ . A set of learnable scene queries $\mathbf { Q } _ { t } ^ { s }$ is then introduced to aggregate multi-view information via cross-attention, which is formulated as:

$$
{ \bf Q } _ { t } ^ { \mathrm { s c e n e } } = \mathrm { C r o s s A t t n } ( { \bf Q } _ { t } ^ { \mathrm { s c e n e } } , { \bf F } _ { t } ^ { \mathrm { i } } ) .\tag{1}
$$

It yields a unified scene representation that captures the spatial layout and context from the driving scenes of the current time step.

Multi-modal Trajectory Decoder. Since $\mathbf { Q } _ { t } ^ { \mathrm { s c e n e } }$ contains relevant scene information, following $\left\lceil 1 9 , 2 0 \right\rceil$ , we initialize a set of candidate waypoint queries ${ \bf Q } _ { t } ^ { \mathrm { t r a j } } = \{ q _ { t } ^ { i } \} _ { n = 1 } ^ { N } \in \mathbb { R } ^ { N _ { m } \times N \times D }$ to extract multi-mode planning trajectories, where $N _ { m }$ denotes the number of driving commands, N denotes the number of trajectory modes, and D is the dimensions of query feature.

Then, scene-level context $\mathbf { Q } _ { t } ^ { \mathrm { s c e n e } }$ is incorporated into the trajectory queries through cross-attention with the scene queries:

$$
\mathbf { Q } _ { t } ^ { \mathrm { t r a j } } = \mathrm { C r o s s A t t n } ( \mathbf { Q } _ { t } ^ { \mathrm { t r a j } } , \mathbf { Q } _ { t } ^ { \mathrm { s c e n e } } ) .\tag{2}
$$

Following the context-enhanced trajetcory queries, two diiferent MLP heads are applied for trajectory refinement and mode scoring. The trajectory head $\mathrm { M L P _ { t r a j } }$ predicts a residual update to refine the waypoints, while the score head $\mathrm { M L P _ { s } }$ estimates a confidence score for each mode, which can be formulated as:

$$
\begin{array} { r } { \hat { \mathbf { T } } _ { t } = \mathbf { T } _ { t } + \mathrm { M L P } _ { \mathrm { t r a j } } ( \mathbf { Q } _ { t } ^ { \mathrm { t r a j } } ) , \quad \mathbf { c } _ { t } = \mathrm { M L P } _ { \mathrm { s } } ( \mathbf { Q } _ { t } ^ { \mathrm { t r a j } } ) , } \end{array}\tag{3}
$$

where $\hat { \mathbf { T } } _ { t } = \{ \hat { T } _ { t } ^ { n } \} _ { n = 1 } ^ { N }$ denotes the refined trajectories, and $\mathbf { c } _ { t } = \{ c _ { t } ^ { n } \} _ { n = 1 } ^ { N }$ represents their corresponding mode scores. These $( \hat { \mathbf { T } } _ { t } , \mathbf { c } _ { t } )$ pairs are treated as the multi-modal trajectory proposals for subsequent selection and training supervision.

This formulation provides a set of diverse trajectory hypotheses while maintaining a unified query-based decoding structure, which serves as the foundation for subsequent trajectory selection and dynamic world modeling.

## 3.2 Dynamic Latent World Model

To explicitly characterize planning quality through trajectory-induced world evolution, we introduce a dynamic latent world model that simulates how the environment evolves under diferent trajectory hypotheses. Given the current latent state and candidate trajectories, the model predicts future latent states via, which are used to evaluate the resulting trajectory outputs in latent space.

World Feature Extraction. For the dynamic world simulator, directly reusing the driving encoder may lead to representation shifts and unstable features for modeling temporal evolution. Rather than follow prior works [23,24], we employ a pretrained foundation encoder to obtain more stable and dynamics-aligned latent representations.

Given the surrounding V -view images ${ \mathbf { I } _ { t } } = \{ I _ { t } ^ { i } \} _ { i = 1 } ^ { V } ,$ we firstly encode each view into a latent representation using a pretrained VAE encoder $\mathbf { E } _ { \mathrm { v a e } }$ followed by the lightweight MLP :

$$
\begin{array} { r } { \mathbf { z } _ { t } ^ { i } = \mathrm { M L P } ( \mathbf { E } _ { \mathrm { v a e } } ( I _ { t } ^ { i } ) ) , \quad i = 1 , \ldots , V . } \end{array}\tag{4}
$$

where $\tilde { \mathbf { z } } _ { t } ^ { i }$ denotes the dynamics-aware latent feature for the i-th view. Such representation benefits from the diverse training data and strong generalizationPlanning Decoder𝐼 Q\$ capability of foundation models to obtain dynamics-oriented features. r

To incorporate global scene contexts, we aggregate the multi-view latent<sub>e</sub><sup>n</sup> o features by interacting them with the scene queries<sup>S</sup> E<sup>n</sup> $\bar { \mathbf { Q } } _ { t } ^ { \mathrm { s c e n e } }$ via cross-attention:

$$
\widetilde { \mathbf { z } } _ { t } ^ { \mathrm { w } } = \mathrm { C r o s s A t t n } ( \mathbf { Q } _ { t } ^ { \mathrm { s c e n e } } , \{ \mathbf { z } _ { t } ^ { i } \} _ { i = 1 } ^ { V } ) ,\tag{5}
$$

where $\tilde { \mathbf { z } } _ { t } ^ { \mathrm { w } }$ denotes the world latent that captures both multi-view spatial features and global scene context.

Following the same procedure, we extract the corresponding world features for the next timestep, denoted as $\tilde { \mathbf { z } } _ { t + 1 } ^ { \mathrm { w } } ,$ which serve as the supervision target for training the dynamic flow model.

Flow-based Latent World Model Simulation. Given the current world latent $\tilde { \mathbf { z } } _ { t } ^ { \mathrm { w } }$ and predicted trajectories $\hat { \mathbf { T } } _ { t } ,$ , we model trajectoryconditioned world evolution in latent space. As shown in Figure 4, instead of learning a generic mapping between noise and data, we aim to learn a trajectory-conditioned velocity field that describes how the latent state evolves under diferent motion hy-

![](images/e51a35fa148f760bcd69da1c38312f9ae586d2322b0a548e073217be3c53bf3b.jpg)  
Fig. 4: The architecture of our dynamic latent world model design, in which the velocity field v<sub>θ</sub> is learnt to capture the trajectory-conditioned dynamics transitions in the latent space.

potheses. Following the rectified flow formulation [37], we construct the noised anchor state a from the current latent to provide a stochastic starting point for modeling local state transitions:

$$
\begin{array} { r } { \mathbf { a } = ( 1 - \alpha ) \tilde { \mathbf { z } } _ { t } ^ { \mathrm { w } } + \alpha \epsilon , \quad \epsilon \sim \mathcal { N } ( \mathbf { 0 } , \mathbf { I } ) , } \end{array}\tag{6}
$$

where ϵ is the Gaussian noise with the same shape as ${ \bf z } _ { t } ^ { \mathrm { w } }$ , and $\alpha \in [ 0 , 1 ]$ controls the perturbation strength. Then the continuous interpolation between the anchor a and the target latent $\tilde { \mathbf { z } } _ { t + 1 } ^ { \mathrm { w } }$ is then defined as:

$$
\begin{array} { r } { \mathbf { x } _ { s } = ( 1 - s ) \mathbf { a } + s \tilde { \mathbf { z } } _ { t + 1 } ^ { \mathrm { w } } , \quad s \sim \mathcal { U } ( 0 , 1 ) , } \end{array}\tag{7}
$$

where s denotes the flow timestep.

To incorporate the trajectory conditions, planning modes $\{ \hat { T } _ { t } ^ { n } \} _ { i =  r } ^ { N }$ <sub>n</sub> are encoded into a trajectory embeddings by TrajEmb(·) and fused with the original VAE latent to obtain the condition features $\{ \mathbf { h } _ { t } ^ { n } \} _ { n = 1 } ^ { N } \colon$

$$
\begin{array} { r } { \mathbf h _ { t } ^ { n } = \mathrm { C o n c a t } \big ( [ \boldsymbol \lambda _ { z } \cdot \mathbf z _ { t } ^ { \mathrm { w } } , \boldsymbol \lambda _ { T } \cdot \mathrm { T r a j E m b } ( \hat { T } _ { t } ^ { n } ) ] \big ) , } \end{array}\tag{8}
$$

where $\lambda _ { z }$ and $\lambda _ { T }$ are scalar weights to balance the latent state and trajectory embeddings. Then, the velocity field can be predicted by a transformer-based flow model $\mathcal { F } _ { \theta } ( \cdot )$ , which is formulated as:

$$
v _ { \theta } = \mathcal { F } _ { \theta } ( \mathbf { x } _ { s } , s , \mathbf { h } _ { t } ^ { i } ) .\tag{9}
$$

This formulation models how the latent state evolves under the corresponding trajectory hypothesis.

Thus, during training, we adopt the flow matching objective that supervises the velocity along the interpolation path between the anchor state a and the target latent $\tilde { \mathbf { z } } _ { t + 1 } ^ { \mathrm { w } }$

$$
\mathcal { L } _ { f l o w } = \mathbb { E } \left[ \left\| \mathcal { F } _ { \theta } ( \mathbf { x } _ { s } , s , \mathbf { h } _ { t } ^ { i } ) - ( 1 - s ) ( \widetilde { \mathbf { z } } _ { t + 1 } ^ { \mathrm { w } } - \mathbf { a } ) \right\| _ { 2 } ^ { 2 } \right] ,\tag{10}
$$

where the target velocity corresponds to the displacement from the anchor state toward the future latent along the interpolation path.

For sampling integration, the learned velocity defines a trajectory-conditioned dynamical system so that the future world latent can be obtained via integration:<sup>Curr.</sup> Future

$$
\frac { d \tilde { \mathbf { z } } ^ { \mathrm { w } } } { d s } = \mathcal { F } _ { \boldsymbol { \theta } } \big ( \tilde { \mathbf { z } } ^ { \mathrm { w } } ( s ) , s , \mathbf { h } _ { t } ^ { i } \big ) .\tag{11}
$$

Each step corresponds to an integration step along the flow variable s, which simulates<sup>E</sup> a small portion of the latent evolution between the driving timesteps t and<sup>#\$%</sup> $t + 1$

Thus, starting from the current latentCross- $\tilde { \mathbf { z } } _ { t } ^ { \mathrm { w } }$ , the future world latent can be obtained by integrating the velocity field from<sup>Attn</sup> <sub>)\*+,+</sub> $s = 0$ to 1. In practice, we approximate this<sup>0.2</sup> integration using a discrete Euler solver:<sup>Planning</sup> <sup>Decod</sup>

$$
\tilde { \mathbf { z } } _ { s _ { k + 1 } } ^ { \mathrm { w } } = \tilde { \mathbf { z } } _ { s _ { k } } ^ { \mathrm { w } } + \varDelta s \mathcal { F } _ { \theta } ( \tilde { \mathbf { z } } _ { s _ { k } } ^ { \mathrm { w } } , s _ { k } , \mathbf { h } _ { t } ^ { i } ) ,\tag{12)<sub>…</sub>}
$$

where $s _ { k }$ is the corresponding flow timestep, and<sup>Self-Attn</sup> $\varDelta s$ is the integration step size.<sub>Multi-Mode</sub> <sub>a</sub><sup>b S</sup>

This formulation models how diferent trajectory hypotheses induce distinct latentTraj.𝐓!<sup>S</sup> state transitions, enabling dynamics-aware trajectory evaluation based on the progres-<sub>Training</sub> <sub>&</sub> <sub>Inference Training</sub> <sub>Only</sub> sive evolution dynamics.

## 3.3 Stability-aware Multi-mode Selection

Our multi-modal trajectory predictor generates a set of candidate trajectories $\{ \hat { \mathbf { T } } _ { t } ^ { n } \} _ { n = 1 } ^ { N }$ to capture the inz\$<sup>/herent</sup> <sup>uncertainty</sup> <sup>of</sup> <sup>future</sup> <sup>driving</sup> <sup>behaviors.</sup> <sup>Con-</sup> Sup. 𝒗<sub>𝜽</sub>ventional selection strategies typically rely on get<sup>t</sup>ometric or reconstruction criteria, such as trajec-Dynamic s<sup>-</sup>tory error (e.g., ADE/FDE) and latent reconstruction <sup>Add</sup> Flow Modelr<sup>o</sup> …loss. However, these metrics only measure spatial or <sup>Noise</sup>feature-level similarity and fail to reflect the quality of trajectory-induced world evolution.

![](images/a028dff7ca0547272f4a3af74c6a8c857f0583de882237cc221238abdfa94948.jpg)

𝐓! z<sup>/ajectory</sup> <sup>Planning</sup> In practice, diferent trajectory candidates may Condition produce similar geometric errors while leading to substantially diferent latent state evolutions. Selecting trajectories solely based on geometric criteria may therefore favor modes that are spatially accurate but induce unstable or unrealistic scene dynamics, which is undesirable for reliable planning.

To address this issue, as shown in Figure 5, we introduce a stability-aware selection strategy that evaluates each trajectory based on the induced dynamics. Given a trajectory candidate $\hat { \mathbf { T } } _ { t } ^ { n }$ , the flow-based world model simulates the latent evolution conditioned on

Fig. 5: Stability-aware Multimode Selection. For training, the score head is supervised by the stable criterion. For Inference, the best mode trajectory is selected according to the highest score index.

this trajectory and produces a sequence of velocities $\{ \mathbf { v } _ { k } ^ { n } \} _ { k = 1 } ^ { K }$ along the integration steps, where $K$ is the discrete steps during transitions. We measure the directional consistency of the evolution by computing the average angular deviation between consecutive normalized velocity directions $\hat { \mathbf { u } } _ { k - 1 } ^ { n }$ and $\hat { \mathbf { u } } _ { k } ^ { n } \mathrm { : }$

$$
\hat { \mathbf { u } } _ { k } ^ { n } = \frac { \mathbf { v } _ { k } ^ { n } } { \| \mathbf { v } _ { k } ^ { n } \| } , \quad S _ { \theta } ^ { n } = \frac { 1 } { K - 1 } \sum _ { k = 2 } ^ { K } \operatorname { a r c c o s } ( \hat { \mathbf { u } } _ { k } ^ { n } \cdot \hat { \mathbf { u } } _ { k - 1 } ^ { n } ) ,\tag{13}
$$

where smaller $S _ { \theta } ^ { n }$ value indicates smoother and more physically consistent dynamics.

Based on this, we define the unified selection criterion, combined with other commonly used metrics [62] for each trajectory mode assessment:

$$
\begin{array} { r } { \boldsymbol { \mathcal { C } } ^ { n } = \lambda _ { r e c } \mathcal { L } _ { r e c } ^ { n } + \lambda _ { t r a j } \mathcal { L } _ { t r a j } ^ { n } + \lambda _ { \theta } \boldsymbol { S } _ { \theta } ^ { n } , \quad n ^ { * } = \arg \operatorname* { m i n } _ { n } \boldsymbol { \mathcal { C } } ^ { n } , } \end{array}\tag{14}
$$

where $\mathcal { L } _ { t r a j } ^ { n }$ denotes the trajectory error between the predicted trajectory and the ground truth, and $\mathcal { L } _ { r e c } ^ { n }$ measures the reconstruction discrepancy of the predicted latent state. The selected optimal mode $n ^ { * }$ is employed to supervise the learning of the trajectory scoring head.

By explicitly incorporating trajectory-conditioned dynamical stability, the proposed strategy favors trajectories that induce smooth and physically consistent world evolution, leading to more reliable trajectory assessment beyond conventional criteria.

## 3.4 Training and Inference Settings

For model training, we jointly optimize trajectory prediction, scoring, latent reconstruction, and flow-based dynamics with a unified objective:

$$
\mathcal { L } = \mathcal { L } _ { t r a j } + \lambda _ { s c o r e } \mathcal { L } _ { s c o r e } + \lambda _ { r e c } \mathcal { L } _ { r e c } + \lambda _ { f l o w } \mathcal { L } _ { f l o w } .\tag{15}
$$

Here, $\mathcal { L } _ { t r a j }$ denotes the $L _ { 1 }$ loss between predicted trajectories and the ground-truth future trajectory. The scoring loss $\mathcal { L } _ { s c o r e }$ is supervised using the selected optimal mode $n ^ { * }$ defined in Sec. 3.3. $\mathcal { L } _ { r e c }$ enforces consistency between the predicted latent state and the target latent representation, while $\mathcal { L } _ { f l o w }$ corresponds to the flow matching objective used to learn the trajectory-conditioned velocity field. The coeficients $\lambda _ { s c o r e } , \lambda _ { r e c }$ and $\lambda _ { f l o w }$ balance the contributions of diferent objectives.

During inference, the world model is not involved, since the driving system has already acquired the capability to select the optimal trajectory. The planning module directly selects the trajectory with the highest predicted score as the final output, introducing no additional computational overhead compared with the standard trajectory prediction framework.

## 4 Experiment

## 4.1 Dataset and Metrics

For comprehensive evaluations, we train and evaluate our DynFlowDrive on two benchmarks, including the open-loop nuScenes [2] and the closed-loop NavSim [9].

Open-Loop nuScenes Benchmark. The nuScenes dataset contains 1000 driving scenes across diferent driving scenarios in Singapore and Boston. In line with previous studies [23, 24, 30], we make use of the calculated displacement error $\left( L _ { 2 } \right)$ with the ground truth and collision rate (CR) for performance evaluation. Displacement error is calculated by $L _ { 2 }$ error between the prediction and the GT trajectory, while CR quantifies the collision probability with surrounding objects following the predicted trajectories. All metrics are calculated within the 3s future with a 0.5s interval and evaluated at 1s, 2s, and 3s. We utilize the VAD evaluation metrics [20] that compute the average across all previous frames.

Closed-loop NavSim Benchmark. NavSim provides a closed-loop benchmark built on the OpenScene dataset. It contains 103K keyframes with 1192 training scenarios and 136 test scenarios. During evaluation, the predicted trajectories are interpolated using an LQR controller sampled at 2 Hz over a 4-second horizon. It is evaluated by a simulator to get the rule-based simulation metric score, which is calculated based on five key metrics, including No at-fault Collisions (NC), Drivable Area Compliance (DAC), Time to Collision with bounds (TTC), Ego Progress (EP), and Comfort (C). Thus, the final PDM Score (PDMS) is derived by aggregating these metrics as follows $\begin{array} { r } { \mathrm { P D M S } = \mathrm { N C } \times \mathrm { D A C } \times \frac { 5 \times ( \mathrm { E P } + \mathrm { T T C } ) + 2 \times \mathrm { C } } { 1 2 } } \end{array}$

## 4.2 Implementation Details

nuScenes. For open-loop evaluation, our DynFlowDrive is trained for 12 epochs on 8 NVIDIA RTX 4090 GPUs with a batch size of 1 per GPU, which is built on the open-sourced LAW [24], SSR [23]. The driving commands align with previous works [19], including left, right, and go straight. For the SSR-based approaches, we adopt ResNet50 [15] as image backbone operating at an image resolution of $6 4 0 \times 3 6 0$ We utilize the AdamW optimizer [39] with a learning rate set to $1 \times 1 0 ^ { - 4 }$ . The weights $\lambda _ { s c o r e }$ for scoring loss, $\lambda _ { r e c }$ for latent reconstruction loss, and $\lambda _ { f l o w }$ for flow loss are set to 0.5, 0.2, and 0.1, respectively.

NavSim. We further conduct the closed loop evaluation of DynFlowDrive on the NavSim benchmark. Our model is trained for 30 epochs with a batch size of 16 per GPU. Following the setting of WoTE [25], we concatenate the front-view image with center-cropped front-left and front-right images, resulting in a combined resolution of 256 × 1024 pixels. For LiDAR, the 64m × 64m point cloud surrounding the ego vehicle is used. For network architecture, we employ ResNet34 [15] as the backbone for image feature extraction. The number of trajectory anchors is set to $N = 2 5 6$ . We utilize the Adam optimizer with a learning rate of $1 \times 1 0 ^ { - 4 }$

## 4.3 Main Results

Open-Loop Evaluation. On the nuScenes [2] benchmark, we compare our proposed DynFlowDrive with the prior approaches following the evaluation metrics in VAD [20]. As shown in Table 1, our method consistently achieves superior results in both the $L _ { 2 }$ distance error and collision rate. We implement our DynFlowDrive based on two representative latent world model baselines. For the approaches without BEV representation, compared with LAW [24], our DynFlowDrive reduces the $L _ { 2 }$ displacement error by 0.4m and lowers the collision rate by 26%. Based on the BEV representation, we replace the latent world model in SSR [23] with our DynFlowDrive design, which yields nearly a 20% reduction on $L _ { 2 }$ distance by 0.08m and achieves 0.11% collision rate. It indicates that our approach can be seamlessly integrated into existing frameworks and consistently improve planning quality. Compared to the perception-based approaches, without the incorporation of any auxiliary tasks, our dynamic latent world model still achieves comparable performance.

<table><tr><td rowspan="2">一 Method 1</td><td rowspan="2">Pub.</td><td rowspan="2">BEV</td><td colspan="4">L2 (m) ↓</td><td colspan="4">Collision Rate (%) ↓</td></tr><tr><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td></tr><tr><td colspan="10">Perception-based Approaches</td></tr><tr><td>ST-P3 [17]</td><td>ECCV 2022</td><td>√</td><td>1.33</td><td>2.11</td><td>2.90</td><td>2.11</td><td>0.23</td><td>0.62</td><td>1.27</td><td>0.71</td></tr><tr><td>UniAD [19]</td><td>CVPR 2023</td><td>√</td><td>0.48</td><td>0.96</td><td>1.65</td><td>1.03</td><td>0.05</td><td>0.17</td><td>0.71</td><td>0.31</td></tr><tr><td>VAD-Tiny [20]</td><td>ICCV 2023</td><td>√</td><td>0.46</td><td>0.76</td><td>1.12</td><td>0.78</td><td>0.21</td><td>0.35</td><td>0.58</td><td>0.38</td></tr><tr><td>VAD-Base [20]</td><td>ICCV 2023</td><td>√</td><td>0.41</td><td>0.70</td><td>1.05</td><td>0.72</td><td>0.07</td><td>0.17</td><td>0.41</td><td>0.22</td></tr><tr><td>BEV-Planner [30]</td><td>CVPR 2024</td><td>√</td><td>0.28</td><td>0.42</td><td>0.68</td><td>0.46</td><td>0.04</td><td>0.37</td><td>1.07</td><td>0.49</td></tr><tr><td>PARA-Drive [50]</td><td>CVPR 2024</td><td>√</td><td>0.25</td><td>0.46</td><td>0.74</td><td>0.48</td><td>0.14</td><td>0.23</td><td>0.39</td><td>0.25</td></tr><tr><td>GenAD [61]</td><td>ECCV 2024</td><td>√</td><td>0.28</td><td>0.49</td><td>0.78</td><td>0.52</td><td>0.08</td><td>0.14</td><td>0.34</td><td>0.19</td></tr><tr><td>SparseDrive [44]</td><td>ICCV 2025</td><td>x</td><td>0.29</td><td>0.58</td><td>0.96</td><td>0.61</td><td>0.01</td><td>0.05</td><td>0.18</td><td>0.08</td></tr><tr><td>Drive-OccWorld [56]</td><td>AAAI 2025</td><td>x</td><td>0.25</td><td>0.44</td><td>0.72</td><td>0.47</td><td>0.03</td><td>0.08</td><td>0.22</td><td>0.11</td></tr><tr><td>MomAD [43]</td><td>CVPR 2025</td><td>x</td><td>0.31</td><td>0.57</td><td>0.91</td><td>0.60</td><td>0.01</td><td>0.05</td><td>0.22</td><td>0.09</td></tr><tr><td>DiffusionDrive [31]</td><td>CVPR 2025</td><td>x</td><td>0.27</td><td>0.54</td><td>0.90</td><td>0.57</td><td>0.03</td><td>0.05</td><td>0.16</td><td>0.08</td></tr><tr><td colspan="9">Latent World Model Approaches</td></tr><tr><td>LAW [24]</td><td>ICLR 2025</td><td>x</td><td>0.26</td><td>0.57</td><td>1.01</td><td>0.61</td><td>0.14</td><td>0.21</td><td>0.54</td><td>0.30</td></tr><tr><td>DynFlowDrive(LAW)</td><td></td><td>x</td><td>0.24</td><td>0.54</td><td>0.92</td><td>0.57</td><td>0.11</td><td>0.12</td><td>0.48</td><td>0.22</td></tr><tr><td>SSR* [23]</td><td>ICLR 2025</td><td>√</td><td>0.18</td><td>0.35</td><td>0.63</td><td>0.39</td><td>0.08</td><td>0.12</td><td>0.24</td><td>0.15</td></tr><tr><td>DynFlowDrive (SSR)</td><td></td><td>√</td><td>0.16</td><td>0.32</td><td>0.57</td><td>0.35</td><td>0.07</td><td>0.09</td><td>0.21</td><td>0.14</td></tr><tr><td>DynFlowDrive (SSR)</td><td>1</td><td>√</td><td>0.13</td><td>0.27</td><td>0.52</td><td>0.31</td><td>0.06</td><td>0.09</td><td>0.18</td><td>0.11</td></tr></table>

Table 1: Comparison of the SOTA methods on the nuScenes dataset. $^ { 6 6 } \ast ^ { 5 9 }$ denotes the re-implemented result from SSR [23] by oficial public codes. $" \bigcirc ^ { \prime \prime }$ denotes using ego status in the planning module following BEVPlanner++ [30]. Evaluations are conducted in the same way as the settings in VAD [20]. Our DynFLowDrive are implemented based on LAW [24] and SSR. LAW adopts Swin-Tiny [38] as image backbone, while others adopt ResNet-50 [15].

Qualitative Result. In Figure 6, we present the qualitative comparisons between our DynFlowDrive and the baseline SSR with three diferent commands. As illustrated in both the BEV space and front-view camera perspectives, our planning results exhibit stronger alignment with the ground truth of the scene structure. In particular, our method produces smoother and more coherent trajectories that better follow lane geometry and surrounding dynamics, indicating improved consistency between predicted motions and the underlying environment. More visualizations are provided in our supplementary materials.

Closed-Loop Evaluation. We further evaluate DynFlowDrive under closed-loop settings on the NavSim benchmark [9]. The comparison results are summarized in Table 2. As shown, DynFlowDrive achieves competitive performance across closed-loop metrics and reaches the state-of-the-art planning accuracy of 88.7% PDMS, surpassing the baseline world model approach WoTE [25]. Notably, without relying on auxiliary tasks such as object detection or online mapping, our method also outperforms previous world model-based approaches, including LAW [24] and World4Drive [62]. These results demonstrate that incorporating the flow-based latent world model together with the stability-aware selection mechanism enables the model to better capture trajectoryconditioned world dynamics, leading to safer and more reliable planning behavior in closed-loop driving scenarios.

![](images/9cfbe39cd7558b7f574a1c81eac8acc50a2eb96b8540f01bbaf0a186fd9140b5.jpg)  
(c) Go Straight  
Fig. 6: Visualization of Planning Results on nuScenese dataset. The perception representations are rendered from annotations. Surrounding light lines denote the maps of the scene, while black boxes represent the object detection. The ego vehicle is drawn by the green box in the center.

## 4.4 Ablation Study

In this section, we conduct comprehensive ablation studies to investigate the efectiveness of our DynFlowDrive designs. For fair comparison, all ablations are conducted on the nuScenes benchmark. More ablations and analyses on NavSim benchmark are provided in our supplementary materials.

Verification of Component Designs. In this section, we conduct ablation studies to evaluate the contribution of each component and the combinations. As shown in Table 3, starting from the vanilla end-to-end autonomous driving paradigm without BEV representation $\mathrm { o r }$ world modeling modules, incorporating the static transformerbased world model yields only marginal improvement. By introducing the proposed dynamic latent world model, we achieve an average $L _ { 2 }$ error reduction of 0.1 m and a 11% decrease in collision rate, demonstrating the benefit of dynamic simulation of world evolution. Furthermore, when combined with the stability-aware multi-mode selection, DynFlowDrive achieves the best overall performance, reaching an $L _ { 2 }$ error of 0.57 m and a collision rate of 0.22%. These results validate that dynamic evolution modeling and stability-guided mode selection jointly contribute to safer and more accurate trajectory planning. For inference, no additional computational burdens are introduced, as the flow-based world model is only used during training and does not participate in the forward prediction pipeline.

<table><tr><td>Method</td><td></td><td>|Input|#Traj.|Traj. Eval. |NC ↑ DAC ↑ EP ↑ TTC ↑ Comf. ↑|PDMS ↑</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Human</td><td>-</td><td>-</td><td>-</td><td>100</td><td>100</td><td>87.5</td><td>100</td><td>99.9</td><td>94.8</td></tr><tr><td>Constant Velocity</td><td>-</td><td>1</td><td>x</td><td>69.9</td><td>58.8</td><td>49.3</td><td>49.3</td><td>100.0</td><td>21.6</td></tr><tr><td>Ego Status MLP</td><td>-</td><td>1</td><td>x</td><td>93.0</td><td>77.3</td><td>62.8</td><td>83.6</td><td>100.0</td><td>65.6</td></tr><tr><td>VADv2 [4]</td><td>C</td><td>8192</td><td>Rule-based</td><td>97.9</td><td>91.7</td><td>77.6</td><td>92.9</td><td>100.0</td><td>83.0</td></tr><tr><td>UniAD [19]</td><td>C</td><td>1</td><td>Rule-based</td><td>97.8</td><td>91.9</td><td>78.8</td><td>92.9</td><td>100.0</td><td>83.4</td></tr><tr><td>LTF [41]</td><td>C</td><td>1</td><td>x</td><td>97.4</td><td>92.8</td><td>79.0</td><td>92.4</td><td>100.0</td><td>83.8</td></tr><tr><td>PARA-Drive [50]</td><td>C</td><td>1</td><td>Rule-based</td><td>97.9</td><td>92.4</td><td>79.3</td><td>93.0</td><td>99.8</td><td>84.0</td></tr><tr><td>TransFuser [8]</td><td>C&amp;L</td><td>1</td><td>x</td><td>97.7</td><td>92.8</td><td>79.2</td><td>92.8</td><td>100.0</td><td>84.0</td></tr><tr><td>LAW [24]</td><td>C</td><td>1</td><td>x</td><td>96.4</td><td>95.4</td><td>81.7</td><td>88.7</td><td>99.9</td><td>84.6</td></tr><tr><td>World4Drive [62]</td><td>C</td><td>6</td><td>x</td><td>97.4</td><td>94.3</td><td>79.9</td><td>92.8</td><td>100.0</td><td>85.1</td></tr><tr><td>DRAMA [57]</td><td>C&amp;L</td><td>1</td><td>x</td><td>98.0</td><td>93.1</td><td>80.1</td><td>94.8</td><td>100.0</td><td>85.5</td></tr><tr><td>Hydra-MDP [28]</td><td>C&amp;L</td><td>8192</td><td>Model-free</td><td>98.3</td><td>96.0</td><td>78.7</td><td>94.6</td><td>100.0</td><td>86.5</td></tr><tr><td>DiffusionDrive [31]</td><td>C&amp;L</td><td>20</td><td>x</td><td>98.2</td><td>96.2</td><td>82.2</td><td>94.7</td><td>100.0</td><td>88.1</td></tr><tr><td>WoTE [25]</td><td>C&amp;L</td><td>256</td><td>[Model-based</td><td>98.5</td><td>96.8</td><td>81.9</td><td>94.9</td><td>99.9</td><td>88.3</td></tr><tr><td>DynFlowDrive (Ours)|C &amp; L|</td><td></td><td>256</td><td>|Model-based|</td><td>98.7</td><td>96.8</td><td>82.5</td><td>95.5</td><td>100.0</td><td>88.7</td></tr></table>

Table 2: Comparison with the SOTA approaches on the NavSim test set. C: Camera. L: LiDAR. Rule-based means that trajectory evaluation follows specific rules. Model-free represents the evaluation without world modeling. Model-based denotes evaluating the trajectory with the assistance of the world model.

<table><tr><td colspan="3">Modules</td><td colspan="4"> $L _ { 2 } ~ ( \mathrm { m } ) ~ \downarrow$ </td><td colspan="4">CR (%) ↓</td><td rowspan="2">FPS ↑</td></tr><tr><td>Static-WM</td><td>Dyn-WM</td><td>MS</td><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td></tr><tr><td>=</td><td>=</td><td></td><td>0.31</td><td>0.63</td><td>1.12</td><td>0.69</td><td>0.19</td><td>0.27</td><td>0.64</td><td>0.37</td><td>13.8</td></tr><tr><td>√</td><td>=</td><td></td><td>0.26</td><td>0.57</td><td>1.01</td><td>0.61</td><td>0.14</td><td>0.21</td><td>0.54</td><td>0.30</td><td>13.8</td></tr><tr><td>=</td><td>√</td><td>=</td><td>0.26</td><td>0.55</td><td>0.94</td><td>0.59</td><td>0.11</td><td>0.16</td><td>0.51</td><td>0.26</td><td>13.8</td></tr><tr><td></td><td>=</td><td>√</td><td>0.25</td><td>0.55</td><td>0.93</td><td>0.58</td><td>0.11</td><td>0.15</td><td>0.49</td><td>0.25</td><td>13.6</td></tr><tr><td></td><td>√</td><td>√</td><td>0.24</td><td>0.54</td><td>0.92</td><td>0.57</td><td>0.10</td><td>0.12</td><td>0.45</td><td>0.22</td><td>13.6</td></tr></table>

Table 3: Component-wise Ablation. Static-WM and Dyn-WM mean the existing stable world model design and our flow-based dynamic modeling. MS denotes the strategy of stability-aware multi-mode selection. FPS are measured on one RTX 4090.

Ablations on the Dynamic Latent World Model Design. We evaluate diferent world model designs in Table 4. Replacing the static transformer-based world model with the proposed flow-based formulation consistently improves long-horizon prediction. In particular, the 3s $L _ { 2 }$ error is reduced from 1.01 m to 0.94 m and the collision rate decreases from 0.54% to 0.51%. This improvement indicates that flow-based modeling better captures the dynamic evolution of the driving scene in latent space, resulting in smoother and more coherent trajectory predictions. Furthermore, applying the flow-based dynamics on world features extracted by the pretrained encoder brings additional gains. By decoupling representation learning from dynamic evolution modeling, the model achieves more stable latent transitions, reducing the average $L _ { 2 }$ error to 0.57 m and the collision rate to 0.22%. These results demonstrate that combining flow-based dynamics with stable latent representations leads to more reliable trajectory-conditioned world modeling.

<table><tr><td rowspan="2">World Model Design</td><td colspan="4">L2 (m) ↓</td><td colspan="4">CR (%) ↓</td></tr><tr><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td></tr><tr><td>Static WM</td><td>0.26</td><td>0.57</td><td>1.01</td><td>0.61</td><td>0.14</td><td>0.21</td><td>0.54</td><td>0.30</td></tr><tr><td>Flow WM</td><td>0.26</td><td>0.55</td><td>0.94</td><td>0.59</td><td>0.11</td><td>0.16</td><td>0.51</td><td>0.26</td></tr><tr><td>+ World Feat. Design</td><td>0.24</td><td>0.54</td><td>0.92</td><td>0.57</td><td>0.10</td><td>0.12</td><td>0.45</td><td>0.22</td></tr></table>

Table 4: Ablations on the Dynamic Latent World Model Design.

Ablations on Flow Integration Steps. We study the impact of the number of integration steps used to approximate the continuous flow dynamics. As shown in Table 5a, increasing the number of steps from 1 to 5 consistently improves both trajectory accuracy and safety, reducing the $L _ { 2 }$ error from 0.60 m to 0.57 m and the collision rate from 0.28% to 0.22%. This demonstrates that a finer discretization better captures the underlying trajectory-conditioned dynamics. However, further increasing the number of steps to 10 yields no additional gains and even slightly degrades performance. We attribute this to accumulated numerical errors and over-smoothing during integration. Overall, a moderate number of integration steps of 5 achieves the best trade-of between accuracy and stability.

<table><tr><td># Steps</td><td>1</td><td>3</td><td>5</td><td>10</td></tr><tr><td>L2 (m) Avg.↓</td><td>0.60</td><td>0.59</td><td>0.57</td><td>0.59</td></tr><tr><td>CR (%) Avg.↓</td><td>0.28</td><td>0.23</td><td>0.22</td><td>0.24</td></tr></table>

(a) Ablations on Flow Integration Steps.

<table><tr><td>Selection Strategy | L2 (m) Avg. ↓</td><td></td><td>CR (%) Avg. ↓</td></tr><tr><td></td><td>0.61</td><td>0.30</td></tr><tr><td>L2 Only</td><td>0.59</td><td>0.24</td></tr><tr><td>+ Recons.</td><td>0.58</td><td>0.22</td></tr><tr><td>+ Flow Stab.</td><td>0.57</td><td>0.22</td></tr></table>

(b) Ablations on Mode Selection Criteria.  
Table 5: Ablations on Flow Steps and Multi-Mode Selection Strategies.

Ablations on Multi-Mode Selection. We study diferent multi-mode selection strategies in Table 5b. Selecting modes solely based on $L _ { 2 }$ distance is suboptimal, as it emphasizes point-wise accuracy while neglecting temporal consistency and physical plausibility, leading to higher collision rates. Incorporating reconstruction similarity improves latent alignment and trajectory coherence, yielding consistent gains. Further introducing flow direction as a stability-aware criterion encourages modes to follow the learned dynamic evolution, resulting in the lowest collision rate of 0.22% with competitive $L _ { 2 }$ distance of 0.57 m. These results show that combined with the reconstruction similarity, flow-based stability provides a more reliable selection criterion for safe and robust trajectory planning.

## 5 Conclusion

In this work, we propose DynFlowDrive, a flow-based dynamic latent world modeling that explicitly models the progressive scene evolution in latent space via rectified flow. By conditioning on candidate trajectories, our approach enables dynamic simulation of future world states and supports more reliable trajectory evaluation through stability-aware multi-mode selection. Extensive experiments on nuScenes and NavSim demonstrate that DynFlowDrive consistently improves planning accuracy and safety across diferent end-to-end driving frameworks. These results highlight the importance of explicitly modeling world dynamics for robust and scalable autonomous driving systems. Future work includes integrating vision-language models (VLMs) for stronger semantic reasoning, improving robustness under rare corner cases, and ensuring scalability to diverse driving environments.

## References

1. Allen, J.F., Koomen, J.A.: Planning using a temporal world model. In: IJCAI. pp. 741–747 (1983) 2

2. Caesar, H., Bankiti, V., Lang, A.H., Vora, S., Liong, V.E., Xu, Q., Krishnan, A., Pan, Y., Baldan, G., Beijbom, O.: nuscenes: A multimodal dataset for autonomous driving. In: CVPR. pp. 11621–11631 (2020) 3, 9, 10

3. Chen, L., Wu, P., Chitta, K., Jaeger, B., Geiger, A., Li, H.: End-to-end autonomous driving: Challenges and frontiers. IEEE TPAMI (2024) 2

4. Chen, S., Jiang, B., Gao, H., Liao, B., Xu, Q., Zhang, Q., Huang, C., Liu, W., Wang, X.: Vadv2: End-to-end vectorized autonomous driving via probabilistic planning. arXiv preprint arXiv:2402.13243 (2024) 2, 13

5. Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., Song, S.: Difusion policy: Visuomotor policy learning via action difusion. The International Journal of Robotics Research 44(10-11), 1684–1704 (2025) 4

6. Chi, H., Gao, H.a., Liu, Z., Liu, J., Liu, C., Li, J., Yang, K., Yu, Y., Wang, Z., Li, W., et al.: Impromptu vla: Open weights and open data for driving visionlanguage-action models. arXiv preprint arXiv:2505.23757 (2025) 4

7. Chib, P.S., Singh, P.: Recent advancements in end-to-end autonomous driving using deep learning: A survey. TIV 9(1), 103–118 (2023) 2

8. Chitta, K., Prakash, A., Jaeger, B., Yu, Z., Renz, K., Geiger, A.: Transfuser: Imitation with transformer-based sensor fusion for autonomous driving. IEEE TPAMI 45(11), 12878–12895 (2022) 13

9. Dauner, D., Hallgarten, M., Li, T., Weng, X., Huang, Z., Yang, Z., Li, H., Gilitschenski, I., Ivanovic, B., Pavone, M., et al.: Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking. In: NeurIPS (2024) 3, 9, 11

10. Dong, W., Lu, S., Chen, X., Zhang, S., Liu, Q., Liu, Z., Chen, L., Wang, H., Cai, Y.: End-to-end autonomous driving: From classic paradigm to large model empowerment—a comprehensive survey. IEEE Internet of Things Journal 13(3), 3870–3898 (2025) 2

11. Gao, H., Chen, S., Jiang, B., Liao, B., Shi, Y., Guo, X., Pu, Y., Yin, H., Li, X., Zhang, X., Zhang, Y., Liu, W., Zhang, Q., Wang, X.: Rad: Training an end-to-end driving policy via large-scale 3dgs-based reinforcement learning. arXiv preprint arXiv:2502.13144 (2025) 4

12. Gao, R., Chen, K., Xie, E., Hong, L., Li, Z., Yeung, D.Y., Xu, Q.: Magicdrive: Street view generation with diverse 3d geometry control. In: ICLR (2024) 2

13. González, D., Pérez, J., Milanés, V., Nashashibi, F.: A review of motion planning techniques for automated vehicles. TITS 17(4), 1135–1145 (2015) 4

14. Guan, Y., Liao, H., Li, Z., Hu, J., Yuan, R., Zhang, G., Xu, C.: World models for autonomous driving: An initial survey. TIV (2024) 2, 4

15. He, K., Zhang, X., Ren, S., Sun, J.: Deep residual learning for image recognition. In: CVPR. pp. 770–778 (2016) 10, 11

16. Hu, A., Russell, L., Yeo, H., Murez, Z., Fedoseev, G., Kendall, A., Shotton, J., Corrado, G.: Gaia-1: A generative world model for autonomous driving. arXiv preprint arXiv:2309.17080 (2023) 2

17. Hu, S., Chen, L., Wu, P., Li, H., Yan, J., Tao, D.: St-p3: End-to-end vision-based autonomous driving via spatial-temporal feature learning. In: ECCV. pp. 533–549. Springer (2022) 4, 11

18. Hu, T., Liu, X., Wang, S., Zhu, Y., Liang, A., Kong, L., Zhao, G., Gong, Z., Cen, J., Huang, Z., et al.: Vision-language-action models for autonomous driving: Past, present, and future. arXiv preprint arXiv:2512.16760 (2025) 2

19. Hu, Y., Yang, J., Chen, L., Li, K., Sima, C., Zhu, X., Chai, S., Du, S., Lin, T., Wang, W., et al.: Planning-oriented autonomous driving. In: CVPR. pp. 17853– 17862 (2023) 4, 6, 10, 11, 13

20. Jiang, B., Chen, S., Xu, Q., Liao, B., Chen, J., Zhou, H., Zhang, Q., Liu, W., Huang, C., Wang, X.: Vad: Vectorized scene representation for eficient autonomous driving. In: ICCV. pp. 8340–8350 (2023) 4, 6, 10, 11

21. Jiao, S., Qian, K., Ye, H., Zhong, Y., Luo, Z., Jiang, S., Huang, Z., Fang, Y., Miao, J., Fu, Z., et al.: Evadrive: Evolutionary adversarial policy optimization for end-to-end autonomous driving. arXiv preprint arXiv:2508.09158 (2025) 4

22. Kong, L., Yang, W., Mei, J., Liu, Y., Liang, A., Zhu, D., Lu, D., Yin, W., Hu, X., Jia, M., et al.: 3d and 4d world modeling: A survey. arXiv preprint arXiv:2509.07996 (2025) 2, 4

23. Li, P., Cui, D.: Navigation-guided sparse scene representation for end-to-end autonomous driving. arXiv preprint arXiv:2409.18341 (2024) 3, 4, 6, 10, 11

24. Li, Y., Fan, L., He, J., Wang, Y., Chen, Y., Zhang, Z., Tan, T.: Enhancing end-toend autonomous driving with latent world model. arXiv preprint arXiv:2406.08481 (2024) 2, 4, 6, 10, 11, 13

25. Li, Y., Wang, Y., Liu, Y., He, J., Fan, L., Zhang, Z.: End-to-end driving with online trajectory evaluation via bev world model. arXiv preprint arXiv:2504.01941 (2025) 4, 10, 11, 13

26. Li, Y., Xiong, K., Guo, X., Li, F., Yan, S., Xu, G., Zhou, L., Chen, L., Sun, H., Wang, B., et al.: Recogdrive: A reinforced cognitive framework for end-to-end autonomous driving. arXiv preprint arXiv:2506.08052 (2025) 4

27. Li, Y., Tian, M., Zhu, D., Zhu, J., Lin, Z., Xiong, Z., Zhao, X.: Drive-r1: Bridging reasoning and planning in vlms for autonomous driving with reinforcement learning. arXiv preprint arXiv:2506.18234 (2025) 4

28. Li, Z., Li, K., Wang, S., Lan, S., Yu, Z., Ji, Y., Li, Z., Zhu, Z., Kautz, J., Wu, Z., et al.: Hydra-mdp: End-to-end multimodal planning with multi-target hydradistillation. arXiv preprint arXiv:2406.06978 (2024) 13

29. Li, Z., Wang, W., Li, H., Xie, E., Sima, C., Lu, T., Yu, Q., Dai, J.: Bevformer: learning bird’s-eye-view representation from lidar-camera via spatiotemporal transformers. IEEE TPAMI (2024) 3

30. Li, Z., Yu, Z., Lan, S., Li, J., Kautz, J., Lu, T., Alvarez, J.M.: Is ego status all you need for open-loop end-to-end autonomous driving? In: CVPR (2024) 4, 10, 11

31. Liao, B., Chen, S., Yin, H., Jiang, B., Wang, C., Yan, S., Zhang, X., Li, X., Zhang, Y., Zhang, Q., et al.: Difusiondrive: Truncated difusion model for end-to-end autonomous driving. In: CVPR. pp. 12037–12047 (2025) 4, 11, 13

32. Lim, W., Lee, S., Sunwoo, M., Jo, K.: Hybrid trajectory planning for autonomous driving in on-road dynamic scenarios. TITS 22(1), 341–355 (2019) 4

33. Lipman, Y., Chen, R.T., Ben-Hamu, H., Nickel, M., Le, M.: Flow matching for generative modeling. arXiv preprint arXiv:2210.02747 (2022) 4

34. Liu, J., Mao, X., Fang, Y., Zhu, D., Meng, M.Q.H.: A survey on deep-learning approaches for vehicle trajectory prediction in autonomous driving. In: ROBIO. pp. 978–985. IEEE (2021) 4

35. Liu, X., Wang, S., Li, W., Yang, R., Chen, J., Zhu, J.: Mgmap: Mask-guided learning for online vectorized hd map construction. In: CVPR. pp. 14812–14821 (2024) 3

36. Liu, X., Yang, R., Wang, S., Li, W., Chen, J., Zhu, J.: Uncertainty-instructed structure injection for generalizable hd map construction. In: CVPR. pp. 22359– 22368 (2025) 3

37. Liu, X., Gong, C., Liu, Q.: Flow straight and fast: Learning to generate and transfer data with rectified flow. arXiv preprint arXiv:2209.03003 (2022) 7

38. Liu, Z., Lin, Y., Cao, Y., Hu, H., Wei, Y., Zhang, Z., Lin, S., Guo, B.: Swin transformer: Hierarchical vision transformer using shifted windows. In: ICCV. pp. 10012–10022 (2021) 11

39. Loshchilov, I., Hutter, F.: Decoupled weight decay regularization. arXiv preprint arXiv:1711.05101 (2017) 10

40. Podell, D., English, Z., Lacey, K., Blattmann, A., Dockhorn, T., Müller, J., Penna, J., Rombach, R.: Sdxl: Improving latent difusion models for high-resolution image synthesis. In: ICLR (2024) 2

41. Prakash, A., Chitta, K., Geiger, A.: Multi-modal fusion transformer for end-to-end autonomous driving. In: CVPR. pp. 7077–7087 (2021) 13

42. Song, H., Ding, W., Chen, Y., Shen, S., Wang, M.Y., Chen, Q.: Pip: Planninginformed trajectory prediction for autonomous driving. In: ECCV. pp. 598–614. Springer (2020) 4

43. Song, Z., Jia, C., Liu, L., Pan, H., Zhang, Y., Wang, J., Zhang, X., Xu, S., Yang, L., Luo, Y.: Don’t shake the wheel: Momentum-aware planning in end-to-end autonomous driving. In: CVPR. pp. 22432–22441 (2025) 11

44. Sun, W., Lin, X., Shi, Y., Zhang, C., Wu, H., Zheng, S.: Sparsedrive: End-toend autonomous driving via sparse scene representation. In: ICRA. pp. 8795–8801. IEEE (2025) 4, 11

45. Wang, S., Liu, Y., Wang, T., Li, Y., Zhang, X.: Exploring object-centric temporal modeling for eficient multi-view 3d object detection. In: ICCV. pp. 3621–3631 (2023) 3

46. Wang, S., Yu, J., Li, W., Liu, W., Liu, X., Chen, J., Zhu, J.: Not all voxels are equal: Hardness-aware semantic scene completion with self-distillation. In: CVPR. pp. 14792–14801 (2024) 3

47. Wang, X., Zhu, Z., Huang, G., Chen, X., Zhu, J., Lu, J.: Drivedreamer: Towards real-world-drive world models for autonomous driving. In: ECCV. pp. 55–72 (2024) 2

48. Wang, Y., Huang, X., Sun, X., Yan, M., Xing, S., Tu, Z., Li, J.: Uniocc: A unified benchmark for occupancy forecasting and prediction in autonomous driving. arXiv preprint arXiv:2503.24381 (2025) 4

49. Wang, Y., He, J., Fan, L., Li, H., Chen, Y., Zhang, Z.: Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving. In: CVPR. pp. 14749–14759 (2024) 2, 4

50. Weng, X., Ivanovic, B., Wang, Y., Wang, Y., Pavone, M.: Para-drive: Parallelized architecture for real-time autonomous driving. In: CVPR. pp. 15449–15458 (2024) 2, 11, 13

51. Xin, L., Wang, P., Chan, C.Y., Chen, J., Li, S.E., Cheng, B.: Intention-aware long horizon trajectory prediction of surrounding vehicles using dual lstm networks. In: ITSC. pp. 1441–1446. IEEE (2018) 4

52. Xing, Z., Zhang, X., Hu, Y., Jiang, B., He, T., Zhang, Q., Long, X., Yin, W.: Goalflow: Goal-driven flow matching for multimodal trajectories generation in endto-end autonomous driving. In: CVPR. pp. 1602–1611 (2025) 4

53. Yan, T., Tang, T., Gui, X., Li, Y., Zhesng, J., Huang, W., Kong, L., Han, W., Zhou, X., Zhang, X., et al.: Ad-r1: Closed-loop reinforcement learning for end-to-end autonomous driving with impartial world models. arXiv preprint arXiv:2511.20325 (2025) 4

54. Yang, J., Gao, S., Qiu, Y., Chen, L., Li, T., Dai, B., Chitta, K., Wu, P., Zeng, J., Luo, P., et al.: Generalized predictive model for autonomous driving. In: CVPR. pp. 14662–14672 (2024) 4

55. Yang, P., Lu, B., Xia, Z., Han, C., Gao, Y., Zhang, T., Zhan, K., Lang, X., Zheng, Y., Zhang, Q.: Worldrft: Latent world model planning with reinforcement finetuning for autonomous driving. arXiv preprint arXiv:2512.19133 (2025) 2, 4

56. Yang, Y., Mei, J., Ma, Y., Du, S., Chen, W., Qian, Y., Feng, Y., Liu, Y.: Driving in the occupancy world: Vision-centric 4d occupancy forecasting and planning via world models for autonomous driving. In: AAAI. vol. 39, pp. 9327–9335 (2025) 2, 11

57. Yuan, C., Zhang, Z., Sun, J., Sun, S., Huang, Z., Lee, C.D.W., Li, D., Han, Y., Wong, A., Tee, K.P., et al.: Drama: An eficient end-to-end motion planner for autonomous driving with mamba. arXiv preprint arXiv:2408.03601 (2024) 13

58. Zhang, K., Tang, Z., Hu, X., Pan, X., Guo, X., Liu, Y., Huang, J., Yuan, L., Zhang, Q., Long, X.X., et al.: Epona: Autoregressive difusion world model for autonomous driving. arXiv preprint arXiv:2506.24113 (2025) 2, 4

59. Zhao, G., Ni, C., Wang, X., Zhu, Z., Zhang, X., Wang, Y., Huang, G., Chen, X., Wang, B., Zhang, Y., et al.: Drivedreamer4d: World models are efective data machines for 4d driving scene representation. In: CVPR. pp. 12015–12026 (2025) 4

60. Zheng, W., Chen, W., Huang, Y., Zhang, B., Duan, Y., Lu, J.: Occworld: Learning a 3d occupancy world model for autonomous driving. In: ECCV. pp. 55–72. Springer (2024) 2, 4

61. Zheng, W., Song, R., Guo, X., Zhang, C., Chen, L.: Genad: Generative end-to-end autonomous driving. In: ECCV. pp. 87–104. Springer (2024) 4, 11

62. Zheng, Y., Yang, P., Xing, Z., Zhang, Q., Zheng, Y., Gao, Y., Li, P., Zhang, T., Xia, Z., Jia, P., et al.: World4drive: End-to-end autonomous driving via intentionaware physical latent world model. In: ICCV. pp. 28632–28642 (2025) 2, 4, 9, 11, 13

63. Zhou, X., Han, X., Yang, F., Ma, Y., Tresp, V., Knoll, A.: Opendrivevla: Towards end-to-end autonomous driving with large vision language action model. arXiv preprint arXiv:2503.23463 (2025) 4