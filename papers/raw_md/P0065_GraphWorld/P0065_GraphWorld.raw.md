# GraphWorld: Long-Horizon Planning with World Models for End-to-End Autonomous Driving

Ziying Song, Caiyan Jia, Lin Liu, Lei Yang, Shengkai Zhang, Feiyang Jia, Fengda Zhao, Peiliang Wu, Shaoqing Xu, Chen Lv, Yadan Luo

Abstract—End-to-end autonomous driving has made significant progress by unifying perception, prediction, and planning within a single learning framework, achieving strong performance in short-horizon decision making. However, most existing E2E-AD methods remain confined to short-horizon planning and lack the ability to model long-term temporal dependencies, which severely limits their generalization and security in complex and highly interactive driving scenarios. In this work, we propose GraphWorld, an E2E-AD framework that explicitly enhances long-horizon planning through latent world modeling. We introduce an Ego-Centric Interaction Graph, which adaptively models critical neighboring agents based on spatial proximity, and propagates relational context to planning queries via cross-node cross-attention. We present a World-State-Conditioned Planning that learns ego-centric latent world representations by modeling interactions between an ego vehicle and surrounding agents. This latent world state captures key interaction dynamics and safety-relevant semantics, and serves as a conditioning signal to guide long-horizon, safety-aware trajectory planning. Extensive experiments on Bench2Drive, NAVSIMv1/2, and nuScenes demonstrate that GraphWorld significantly reduces collision rates and improves long-horizon planning performance, validating its effectiveness in complex driving environments.

Index Terms—Autonomous Driving, End-to-End Autonomous Driving, World Models.

## 1 INTRODUCTION

diction, and planning within a single framework. Among these tasks, planning serves as the core component of E2E-AD, directly governing the ego vehicle’s decision-making and generating future trajectory outputs for the controlled vehicle [3, 4, 5, 6].

E2E-AD has seen continuous innovation in trajectory planning task. Early E2E-AD methods such as UniAD [3], VAD [5], TransFuser [7]and UAD [8] primarily adopt singlemodal trajectory outputs, while subsequent works including VADv2 [9], MomAD [4], SparseDrive [6], DiffusionDrive [10], and DIVER [11] extend this line of research toward multi-modal trajectory generation. And anchor-based multimodal E2E-AD methods, Hydra-MDP [12], GTRS [13], GoalFlow [14], MindDrive [15], and GuideFlow [16] employ more effective trajectory selection. Despite these advances, as shown in Figure 2 (a), current E2E-AD methods remain fundamentally constrained by their limited longhorizon planning capability. Existing architectures typically process temporal information in a short-sighted manner, lacking mechanisms for modeling and reasoning over extended temporal horizons. Long-horizon planning performance enables multi-step rollout execution at test time, thereby reducing the frequency of online inference and, consequently, lowering the required hardware compute.

![](images/b8197016a5d28720e121c2fffd647957763510cd0f4727cd1a921d9fc5abf8e9.jpg)  
Fig. 1: Performance comparison of SOTA methods on NAVSIMv1. Compared with representative world-modelbased and end-to-end autonomous driving methods, our approach achieves a favorable balance between computational efficiency and prediction accuracy.

Parallel to these E2E-AD developments, world models [17, 18, 19] have rapidly progressed and demonstrated strong potential in learning environment dynamics and predicting future states through imagination-based inference. Analogous to human cognitive processes, world models possess the ability to simulate and reconstruct possible future scenarios, offering a promising path toward longhorizon reasoning in autonomous driving. When combined with E2E architectures, world models can provide richer temporal context, enhance spatiotemporal understanding, and strengthen anticipation of future events. However, as shown in Figure 2 (b), current methods [20, 21, 22, 23] that attempt to incorporate world models into E2E-AD largely rely on diffusion-based future scene generation, which is computationally intensive and unsuitable for real-time applications. Moreover, some methods like WoTE [24] and LAW [25] focus primarily on pixel-level future prediction rather than long-horizon trajectory reasoning, leaving the long-range planning problem essentially underexplored.

![](images/27ff79b699a29d4255569f54d9530452f4f708384590b18b1393668f9ee6ccd8.jpg)  
Fig. 2: Motivation of GraphWorld. (a) E2E-AD methods are constrained by short-horizon reasoning, limiting long-term robustness. (b) World-model approaches enable long-horizon imagination but suffer from low efficiency. (c) GraphWorld combines Ego-Centric Interaction Graph with latent world representations for efficient long-horizon planning.

In this work, we propose GraphWorld, an E2E-AD framework that explicitly enhances long-horizon planning through latent world modeling. Instead of generating future scenes, GraphWorld, as shown in Figure 2 (c), learns compact ego-centric relational world representations by modeling interactions between an ego vehicle and its surrounding agents. Importantly, rather than relying on explicit multistep rollout, GraphWorld improves long-horizon planning by learning a latent world state that implicitly encodes future interaction dynamics and safety-relevant evolution. To this end, we introduce a dynamically constructed Ego-Centric Interaction Graph, which adaptively captures critical neighboring agents based on spatial proximity. By focusing on decision-relevant neighbors, ECIG filters out irrelevant interactions and produces a more informative and stable representation. Relational context is propagated to planning queries via cross-node cross-attention, enabling effective long-horizon reasoning. Furthermore, we propose a World-

State-Conditioned Planning that leverages the inferred egocentric latent world state to guide trajectory generation. The learned world state encodes key interaction dynamics and safety-relevant semantics, and is used to condition multi-modal trajectory queries through a learnable importance network. This design allows the planner to emphasize safer and more consistent long-term behaviors while suppressing implausible trajectories. We first perform E2E pretraining to obtain a stable initialization, and then impose explicit temporal supervision on the world state to encourage temporally consistent and semantically meaningful latent dynamics. Extensive experiments on the closedloop Bench2Drive benchmark and the open-loop nuScenes dataset demonstrate that GraphWorld significantly reduces long-range collision rates and consistently improves longhorizon planning performance, validating its effectiveness in complex environments. Our contributions are summarized as follows.

• We introduce GraphWorld, a novel E2E-AD framework that shifts the paradigm from pixel-space generation to agent-centric relational graph imagination, specifically optimized for long-horizon E2E-AD.

• We propose a dynamically constructed Ego-Centric Interaction Graph (ECIG) together with a World-State-Conditioned Planning (WSCP), which jointly extract stable interaction cues and apply them to guide multi-modal trajectory planning via an importancereweighting network.

• We evaluate GraphWorld across a comprehensive collection of closed-loop (Bench2Drive, NAVSIM) and open-loop (nuScenes, Adv-nuScenes, nuScenes-C) benchmarks, achieving consistent gains in long-horizon planning and safety. Notably, on the nuScenes 6-second long-horizon planning task, it reduces the average collision rate by 19.5% over the latent world-model World4Drive [26]. Furthermore, it achieves 13.3% faster speed over DiffusionDrive [10] on the NAVSIMv1, highlighting its suitability for real-time deployment.

## 2 RELATED WORK

## 2.1 End-to-end Autonomous Driving

E2E-AD methods [3, 5, 6, 7, 8, 9, 10, 27] map raw sensor inputs to vehicle control commands or planned trajectories. UniAD[3] is a comprehensive framework that integrates full-stack driving tasks into a single network. VAD [5] presents a fully vectorized scene representation for end-to-end driving. MomAD [4] introduces trajectory and perception momentum to stabilize and refine trajectory outputs. DiffusionDrive [10] learns denoising transitions from an anchored Gaussian distribution to multi-modal action distributions. DIVER [11] combines reinforcement learning with diffusion-based generation to produce diverse and feasible trajectories. Hydra-MDP [12] employs a multiteacher student paradigm. GTRS [13] proposes generalized trajectory scoring for coarse-to-fine trajectory evaluation. GoalFlow [14] constrains diffusion-generated trajectories through goal-point supervision to address trajectory divergence. GuideFlow [16] explicitly models the flow-matching process to mitigate mode collapse and enable flexible conditioning. Despite these advances, existing E2E-AD frameworks remain fundamentally constrained by limited longhorizon planning capability.

## 2.2 World Models for Autonomous Driving

The development of world models [18, 28, 29, 30, 31, 32] have been rapid. They are increasingly becoming a key component of autonomous driving, supporting mechanisms for scene dynamic modeling, future event prediction, and downstream decision-making. Driving world models [17, 18, 19, 33] have evolved into integrated processes that unify perception, world rule modeling, generation, reconstruction, and multi-task generalization. A major research direction is the world model optimized through explicit generation. DriveDreamer [22], Vista [20], UniFuture [34], Epona [35], and DriveX [36] are capable of high-fidelity video synthesis and controllable policy generation. Other methods [37, 38] focus on agent-level generation . AdaptiveDriver [37] predicts the parameters of the agent’s motion controller, rather than directly predicting its spatiotemporal trajectory. Due to their efficiency and abstraction capability, latent world models [26, 39, 40] have attracted significant attention . However, most driving world models prioritize explicit generation or reconstruction, limiting their ability to capture spatial semantics and multi-modal driving intentions. Only a few E2E-AD works [24, 41] directly leverage latent world models for planning, and their long-term reasoning capabilities are still an area that requires further investigation.

## 3 RETHINKING LONG-HORIZON PLANNING

In practical autonomous driving systems, planning is typically performed in a receding-horizon manner, where trajectories are iteratively updated at high frequency. At each time step t, the planner predicts a future trajectory $\tau _ { t } ,$ but only a short prefix is executed before replanning with updated observations. Therefore, long-horizon planning should not be interpreted as executing a fixed long trajectory, but rather as the ability to make foresighted decisions under iterative replanning.

Formally, the planner solves

$$
\tau _ { t } ^ { * } = \arg \operatorname* { m a x } _ { \tau _ { t } } p ( \tau _ { t } \mid \mathcal { O } _ { \leq t } ) ,\tag{1}
$$

where ${ \mathcal { O } } _ { \leq t }$ denotes historical observations. Although replanning is frequent, the quality of $\tau _ { t } ^ { * }$ depends on whether the model can anticipate future interaction risks beyond immediate observations. A short-sighted planner may produce locally optimal but globally unsafe decisions under complex multi-agent interactions.

In this work, we do not aim to extend the prediction horizon via explicit multi-step rollout. Instead, GraphWorld enhances long-horizon capability by learning a compact ego-centric latent world state

$$
\mathbf { W } ^ { \mathrm { c u r } } = f _ { \theta } ( { \mathcal { O } } _ { \leq t } ) ,\tag{2}
$$

which encodes interaction dynamics and future-relevant semantics. This latent representation enables the planner to reason about the long-term consequences of current actions, even under short-term replanning.

To ensure that the learned representation focuses on decision-relevant structure, we construct an ego-centric interaction graph that selectively models neighboring agents:

$$
\begin{array} { r } { \mathcal { N } = \left\{ i \mid \| \mathbf { p } _ { i } - \mathbf { p } _ { \mathrm { e g o } } \| _ { 2 } < \tau \right\} . } \end{array}\tag{3}
$$

By filtering out irrelevant interactions, the resulting latent world state becomes more stable and informative, which is critical for robust long-horizon reasoning.

Furthermore, instead of performing explicit multi-step prediction, we model world evolution in a latent space via a continuous transformation between current and target states:

$$
\begin{array} { r } { \mathbf { W } ( t ) = ( 1 - t ) \mathbf { W } ^ { \mathrm { c u r } } + t \mathbf { W } ^ { \mathrm { t g t } } , \quad t \sim \mathcal { U } ( 0 , 1 ) , } \end{array}\tag{4}
$$

which avoids error accumulation commonly observed in autoregressive rollout while preserving future-aware structure.

Regarding evaluation, although we follow standard benchmarks with prediction horizons up to 6 seconds, performance at later timestamps $( \mathrm { e . g . } , \ 5 \mathrm { - } 6 \mathrm { s } )$ reflects robustness under compounding uncertainty. Improvements in this regime indicate stronger capability in handling long-term interactions and safety-critical scenarios.

Overall, we argue that long-horizon planning should be understood as the ability to learn future-aware representations that support robust decision-making under iterative replanning, rather than merely extending the prediction horizon.

![](images/3a645f2ae8f8d6c6fec6daa80be87bee1bbdaaa756ebc74e748c31d29bc37ca8.jpg)  
Fig. 3: The proposed long-horizon E2E-AD Framework of GraphWorld. It first encodes sensor data into instancelevel representations, and then constructs an ego-centric latent world model through a dynamically built ECIG that selectively captures critical neighboring agents and their interactions. Based on this interaction-aware world representation, GraphWorld further performs WSCP module by jointly modulating agent motion hypotheses and ego planning queries, enabling interaction-consistent and safety-aware trajectory generation.

## 4 METHOD

GraphWorld is an E2E-AD framework designed to enhance long-horizon planning through latent world modeling. As shown in Figure 3, GraphWorld constructs an ego-centric latent world representation from multi-agent instance features extracted from perception by dynamically modeling interactions between the ego vehicle and surrounding agents. The framework consists of two key components: (1) an Ego-Centric Interaction Graph (ECIG) that encodes ego–agent interactions in a structured relational space, and (2) a World-State-Conditioned Planning (WSCP) that leverages the inferred world state to enable long-horizon, safety-aware trajectory planning.

## 4.1 Ego-Centric Interaction Graph (ECIG)

We introduce an ECIG that explicitly encodes salient ego– agent interactions and injects structured relational context into ego planning queries via cross-attention, enabling effective long-horizon reasoning.

Ego-centric Neighbor Selection. At each planning step, an ego vehicle and its surrounding agents are represented as graph nodes. Let $\mathbf { F } ~ = ~ \{ \mathbf { f } _ { 1 } , \dots , \mathbf { f } _ { N } , \mathbf { f } _ { \mathrm { e g o } } \} , \mathbf { f } _ { i } ~ \in ~ \mathbb { R } ^ { C }$ denote instance-level features at a single planning step for N selected agents and the ego vehicle. The ego node is explicitly included as the center of interaction modeling. To construct a sparse interaction graph, ECIG dynamically selects a fixed number of neighboring agents based on spatial proximity. Let $\mathbf { p } _ { i } ~ \in ~ \mathbb { R } ^ { 2 }$ denote the predicted 2D center of agent i and $\mathbf { p } _ { \mathrm { e g o } }$ the ego center. We define an ego-centric neighbor set $\bar { \mathcal { N } } \overset {  } { = } \{ i \ \lvert \lvert \bf p \rvert - p _ { \mathrm { e g o } } \lvert \lvert 2 < \tau \}$ , where τ is a distance threshold. As the cardinality of the neighbor set may vary across scenes, we apply a PADORTRIM operation to obtain a fixed-size K-neighbor set:

$$
\begin{array} { r } { \mathcal { N } _ { K } = \mathrm { P A D O R T R I M } ( \mathcal { N } , K ) . } \end{array}\tag{5}
$$

Ego-centric Interaction Graph. The resulting interaction graph is defined as $\mathcal { G } ~ = ~ ( \nu , \mathcal { E } )$ with $\gamma = \{ \mathbf { e g o } \} \cup \mathcal { N } _ { K } .$

where directed edges E connect each neighbor node to the ego node, forming an ego-centered star topology. Let $\mathbf { Q } _ { \mathrm { e g o } } \in \mathbb { R } ^ { M \times C }$ denote M multi-modal ego planning queries, and $\mathbf { F } _ { \mathrm { n b r } } ~ = ~ \{ \mathbf { f } _ { i } ~ | ~ i ~ \in ~ \mathcal { N } _ { K } \} ~ \in ~ \mathbb { R } ^ { K \times C }$ denote neighbor features. ECIG propagates interaction information through cross-attention:

$$
\begin{array} { r } { \tilde { \mathbf { Q } } _ { \mathrm { e g o } } = \mathrm { C R O S S A T T N } \big ( \mathbf { Q } _ { \mathrm { e g o } } , \mathbf { F } _ { \mathrm { n b r } } , \mathbf { F } _ { \mathrm { n b r } } \big ) , } \end{array}\tag{6}
$$

where ego queries attend to neighboring agent features, enabling each planning hypothesis to selectively aggregate interaction-aware context.

Interaction-aware World Representation. To construct a structured and temporally grounded latent world state, we condition world representation learning on multisource contextual cues, including interaction structure, motion history, and static map semantics. Specifically, given interaction-enhanced ego queries $\tilde { \mathbf { Q } } _ { \mathrm { e g o } } ,$ neighbor features $\mathbf { F } _ { \mathrm { n b r } } ,$ , historical ego-agent states $\mathbf { H } _ { t } = \left\{ \mathbf { h } _ { t - L } , \ldots , \mathbf { h } _ { t } \right\}$ of $L _ { - }$ step horizon, and local map embeddings M, we first model temporal dynamics using a recurrent world encoder:

$$
\begin{array} { r } { \mathbf { s } _ { t } = \mathrm { G R U } ( \mathbf { s } _ { t - 1 } , \mathrm { C O N C A T } ( \mathbf { H } _ { t } , \mathbf { M } ) ) , } \end{array}\tag{7}
$$

where $\mathbf { H } _ { t }$ is constructed by temporally stacking the motion states $( \mathrm { e . g . , }$ position, velocity, and heading) of the ego vehicle and its neighbors over the past (L) frames ${ \mathbf { } } , { \mathbf { s } } _ { t }$ denotes the temporally accumulated world context at time t. Here, map features M are first pooled into a compact embedding before concatenation with the historical state sequence. We then integrate interaction-aware information via cross-attention:

$$
{ \bf c } _ { \mathrm { i n t } } = \mathrm { C R O S S A T T N } \left( { \bf s } _ { t } , \ \tilde { \bf Q } _ { \mathrm { e g o } } \cup { \bf F } _ { \mathrm { n b r } } , \ \tilde { \bf Q } _ { \mathrm { e g o } } \cup { \bf F } _ { \mathrm { n b r } } \right) .\tag{8}
$$

Based on the resulting context, we update node-level latent world states through conditioned residual injection:

$$
\mathbf { w } _ { i } = \mathbf { f } _ { i } + \phi _ { a } ^ { \mathrm { i n t } } ( \mathbf { c } _ { \mathrm { i n t } } , \mathbf { r } _ { i } ) , \quad \mathbf { w } _ { \mathrm { e g o } } = \mathbf { f } _ { \mathrm { e g o } } + \phi _ { e } ^ { \mathrm { i n t } } ( \mathbf { c } _ { \mathrm { i n t } } ) ,\tag{9}
$$

where the ego-centric relational geometry of agent i is denoted by $\mathbf { r } _ { i } = \mathrm { M L P } \left( \left[ \mathbf { f } _ { i } , \mathbf { p } _ { i } - \mathbf { p } _ { \mathrm { e g o } } \right] \right)$ , and lightweight conditional projection networks are $\phi _ { a } ^ { \mathrm { i n t } } ( \cdot ) , \phi _ { e } ^ { \mathrm { i n t } } ( \cdot )$ . The resulting latent world state $\mathbf { W } = \{ \mathbf { w } _ { 1 } , \dots , \mathbf { w } _ { K } , \dots , \mathbf { w } _ { N } , \mathbf { w } _ { \mathrm { e g o } } \}$ captures temporally consistent ego-agent interaction dynamics under map constraints and conditions downstream longhorizon planning. Here, K denotes the number of selected neighbors and N denotes the total number of agent anchors (set to 900 in nuScenes); the anchors $\mathbf { w } _ { K + 1 : N } = \mathbf { 0 }$ are zeropadded.

## 4.2 World-State-Conditioned Planning (WSCP)

Given the interaction-aware world representation inferred by ECIG, we propose a WSCP module to enable longhorizon, safety-aware trajectory generation. Instead of decoding trajectories solely from planning queries, WSCP explicitly conditions both agent motion hypotheses and ego planning on the latent world dynamics, allowing interaction-consistent reasoning over extended horizons.

Flow-Matching for Dynamic World-State. To explicitly model long-horizon world evolution in a principled continuous-time manner, we formulate world-state dynamics using a conditional Flow-Matching framework [42]. Rather than performing discrete autoregressive updates or iterative diffusion sampling, Flow-Matching directly learns a time-dependent velocity field that transports latent world states along interaction-consistent trajectories.

For clarity, we distinguish between a current latent world state $\mathbf { W } ^ { \mathrm { c u r } }$ inferred from present observations, and a conditioned target world state $\hat { \mathbf { W } } ^ { \mathrm { t g t } }$ constructed from future agent motion hypotheses, ego planning context, and static map semantics. The current world state is given by ${ \bf W } ^ { \mathrm { c u r } } = \left\{ { \bf w } _ { 1 } , \ldots , { \bf w } _ { N } , { \bf w } _ { \mathrm { e g o } } \right\}$ , as inferred by the ECIG.

The target world state $\mathbf { \bar { W } } ^ { \mathrm { { t g t } } }$ is constructed by conditioning on multi-modal agent motion hypotheses, ego planning context, and optional map embeddings, and is used solely as a supervision signal for world-state evolution rather than an explicit rollout target. Formally, we define

$$
\begin{array} { r } { { \bf W } ^ { \mathrm { t g t } } = \phi _ { \mathrm { t g t } } \left( \mathrm { C O N C A T } \left( \bar { \bf Q } _ { \mathrm { m o t i o n } } , \bar { \bf Q } _ { \mathrm { e g o } } , { \bf M } \right) \right) , } \end{array}\tag{10}
$$

where the mode-aggregated agent motion latents and ego planning representations are denoted by $\bar { \bf Q } _ { \mathrm { m o t i o n } } =$ $\begin{array} { r } { \mathbf { M } \mathbf { E } \mathbf { A } \mathbf { \bar { N } } _ { m } \big ( \mathbf { Q } _ { \mathrm { m o t i o n } } \big ) } \end{array}$ and $\bar { \bf Q } _ { \mathrm { e g o } } = { \bf M } \mathrm { E A N } _ { m } ( \tilde { \bf Q } _ { \mathrm { e g o } } ) .$ , respectively. M denotes optional map embeddings, and $\phi _ { \mathrm { t g t } } ( \cdot )$ is a lightweight projection network mapping contextual cues to the latent world space.

We define a continuous interpolation between the current and target world states:

$$
\mathbf { W } ( t ) = \left( 1 - t \right) \mathbf { W } ^ { \mathrm { c u r } } + t \mathbf { W } ^ { \mathrm { t g t } } , \quad t \sim \mathcal { U } ( 0 , 1 ) ,\tag{11}
$$

where t denotes a randomly sampled continuous time. The corresponding ground-truth velocity along this path is

$$
\mathbf { v } ^ { \star } ( t ) = \frac { d \mathbf { W } ( t ) } { d t } = \mathbf { W } ^ { \mathrm { t g t } } - \mathbf { W } ^ { \mathrm { c u r } } .\tag{12}
$$

We parameterize a conditional velocity field

$$
\begin{array} { r } { { \bf v } _ { \theta } ( t ) = f _ { \theta } ( { \bf W } ( t ) , t , \bar { \bf Q } _ { \mathrm { e g o } } , \bar { \bf F } _ { \mathrm { n b r } } , { \bf M } ) , } \end{array}\tag{13}
$$

where $f _ { \theta } ( \cdot )$ is a lightweight neural network, $\begin{array} { r l } { \bar { \bf Q } _ { \mathrm { e g o } } } & { { } = } \end{array}$ $\mathbf { M E A N } _ { m } \bigl ( \tilde { \mathbf { Q } } _ { \mathrm { e g o } } \bigr )$ aggregates multi-modal ego planning hypotheses, $\bar { \mathbf { F } } _ { \mathrm { n b r } } = \mathbf { M } \mathbf { E } \mathbf { A } \mathbf { N } ( \mathbf { F } _ { \mathrm { n b r } } )$ summarizes the surrounding

agent context, and M denotes optional local map embeddings. In this way, the learned flow is explicitly conditioned on ego–agent interactions and static scene constraints.

Training is performed using the Flow-Matching objective:

$$
\begin{array} { r } { \mathcal { L } _ { \mathrm { F M } } = \mathbb { E } _ { t , \mathbf { W } ^ { \mathrm { c u r } } , \mathbf { W } ^ { \mathrm { t g t } } } \left[ \left\| \mathbf { v } _ { \theta } ( t ) - \mathbf { v } ^ { \star } ( t ) \right\| _ { 2 } ^ { 2 } \right] , } \end{array}\tag{14}
$$

which enforces the predicted velocity field to match the true transport direction at arbitrary intermediate world states. At inference time, the learned velocity field defines a continuous-time dynamical system:

$$
\frac { d { \bf W } ( t ) } { d t } = { \bf v } _ { \theta } ( t ) ,\tag{15}
$$

which is approximated using a single-step Euler update:

$$
\mathbf { W } _ { t } \gets \mathbf { W } _ { t } + \Delta t \cdot \mathbf { v } _ { \theta } ( t ) .\tag{16}
$$

This Flow-Matching formulation enables stable and interaction-consistent refinement of the latent world state, serving as a temporally grounded conditioning signal for long-horizon, safety-aware planning. And during generation, the number of sampling steps is set to 2.

## Importance Reweighting for Motion Modeling.

Let $\mathbf { W } _ { t } ~ = ~ \{ \mathbf { W } _ { 1 : N } , \mathbf { W } _ { \mathrm { e g o } } \}$ denote the refined latent world state at time t. To inject long-horizon world dynamics into trajectory hypotheses, we condition agent motion queries on the updated agent world state:

$$
\begin{array} { r } { \mathbf { C } = \phi _ { c } ( \mathbf { W } _ { 1 : N } ) \in \mathbb { R } ^ { B \times N \times C } , } \end{array}\tag{17}
$$

$$
\begin{array} { r } { \mathbf { Q } _ { \mathrm { m o t i o n } } ^ { \prime } = \mathrm { L N } ( \mathbf { Q } _ { \mathrm { m o t i o n } } + \mathbf { C } [ : , : , \mathrm { N o n e } , : ] ) . } \end{array}\tag{18}
$$

Long-horizon planning is sensitive to the reliability of surrounding-agent predictions. We therefore perform modewise importance re-weighting using ego-conditioned world dynamics. Specifically,

$$
\begin{array} { r } { \pmb { \alpha } = \sigma \Big ( f _ { \mathrm { i m p } } \left( \mathrm { C O N C A T } \Big ( \mathbf { Q } _ { \mathrm { m o t i o n } } ^ { \prime } + \mathbf { W } _ { 1 : N } ^ { \uparrow } , \mathbf { f } _ { \mathrm { e g o } } ^ { \uparrow } \Big ) \right) \Big ) , } \end{array}\tag{19}
$$

where $f _ { \mathrm { i m p } } ( \cdot )$ denotes a lightweight two-layer ML $\mathrm { . } \mathrm { \mathrm { P } } , \sigma ( \cdot )$ is the sigmoid function and ↑ denotes broadcast along agent and mode dimensions. The re-weighted motion queries are

$$
\hat { \bf Q } _ { \mathrm { m o t i o n } } = { \pmb \alpha } \odot { \bf Q } _ { \mathrm { m o t i o n } } ^ { \prime } ,\tag{20}
$$

where α reflects the world-conditioned reliability of each motion mode. World-to-Ego Feedback for Planning Queries. The refined world state further conditions ego planning via residual modulation:

$$
\mathbf { Q } _ { \mathrm { p l a n } } ^ { \prime } = \mathbf { Q } _ { \mathrm { p l a n } } + \mathbf { W } _ { \mathrm { e g o } } .\tag{21}
$$

Multi-modal Motion and Ego Trajectory Decoding. Finally, the re-weighted agent motion queries and worldconditioned ego planning queries are jointly decoded by task-specific heads:

$$
\begin{array} { r } { \left\{ \begin{array} { l l } { \{ \pi _ { n , m } , \hat { \mathbf { Y } } _ { n , m } \} = f _ { \mathrm { m o t i o n } } \Big ( \hat { \mathbf { Q } } _ { \mathrm { m o t i o n } } \Big ) , } \\ { \{ \pi _ { m } ^ { \mathrm { e g o } } , \hat { \mathbf { Y } } _ { m } ^ { \mathrm { e g o } } \} = f _ { \mathrm { p l a n } } \Big ( \mathbf { Q } _ { \mathrm { p l a n } } ^ { \prime } \Big ) , } \end{array} \right. } \end{array}\tag{22}
$$

where $\hat { \mathbf Y } _ { n , m } ~ \in ~ \mathbb R ^ { T \times 2 }$ denotes the m-th predicted future trajectory of agent $n ,$ and $\pi _ { n , m }$ is its corresponding mode probability. Similarly, $\hat { \mathbf { Y } } _ { m } ^ { \mathrm { e g o } } \in \mathbb { R } ^ { T \times 2 }$ denotes the m-th ego trajectory hypothesis, with $\pi _ { m } ^ { \mathrm { { e g o } } }$ indicating its corresponding confidence score.

TABLE 1: Planning results for 6-second long-horizon planning on the nuScenes validation set.
<table><tr><td rowspan="2">Method</td><td colspan="7">L2 (m) ↓</td><td colspan="7">Col. Rate (%) ↓</td></tr><tr><td>1s</td><td>2s</td><td>3s</td><td>4s</td><td>5s</td><td>6s</td><td>Avg.</td><td>1s</td><td>2s</td><td>3s</td><td>4s</td><td>5s</td><td>6s</td><td>Avg.</td></tr><tr><td>UniAD [3]</td><td>0.47</td><td>0.91</td><td>1.35</td><td>1.91</td><td>2.47</td><td>3.07</td><td>1.70</td><td>0.25</td><td>0.36</td><td>0.61</td><td>0.99</td><td>1.64</td><td>2.51</td><td>1.06</td></tr><tr><td>SparseDrive [6]</td><td>0.43</td><td>0.87</td><td>1.23</td><td>1.75</td><td>2.32</td><td>2.95</td><td>1.59</td><td>0.19</td><td>0.31</td><td>0.56</td><td>0.87</td><td>1.54</td><td>2.33</td><td>0.97</td></tr><tr><td>MomAD [4]</td><td>0.41</td><td>0.85</td><td>1.13</td><td>1.67</td><td>1.98</td><td>2.45</td><td>1.42</td><td>0.17</td><td>0.30</td><td>0.54</td><td>0.83</td><td>1.43</td><td>2.13</td><td>0.90</td></tr><tr><td>LAW [41]</td><td>0.40</td><td>0.87</td><td>1.16</td><td>1.71</td><td>2.03</td><td>2.61</td><td>1.46</td><td>0.19</td><td>0.33</td><td>0.57</td><td>0.86</td><td>1.51</td><td>2.31</td><td>0.96</td></tr><tr><td>Epona [35]</td><td>0.39</td><td>0.91</td><td>1.17</td><td>1.73</td><td>2.02</td><td>2.75</td><td>1.50</td><td>0.14</td><td>0.18</td><td>0.45</td><td>0.74</td><td>1.48</td><td>2.23</td><td>0.87</td></tr><tr><td>World4Drive [26]</td><td>0.42</td><td>0.92</td><td>1.21</td><td>1.75</td><td>2.06</td><td>2.79</td><td>1.53</td><td>0.16</td><td>0.20</td><td>0.47</td><td>0.76</td><td>1.50</td><td>2.14</td><td>0.87</td></tr><tr><td>GraphWorld(Ours)</td><td>0.38</td><td>0.70</td><td>1.12</td><td>1.64</td><td>1.88</td><td>2.29</td><td>1.34</td><td>0.03</td><td>0.06</td><td>0.25</td><td>0.65</td><td>1.29</td><td>1.95</td><td>0.70</td></tr></table>

## 4.3 Two-Stage Temporal World-State Supervision

To encourage the world state to learn a genuine representation of future state evolution, we adopt a two-stage training strategy. In the first stage, we perform standard end-to-end training of the overall model. In the second stage, we apply explicit supervision to the world state of the world model. Stage I: Single-step world state learning. In the first stage, the model is trained using inputs at time t only. Given multiview observations at time t, GraphWorld infers a latent world state $\mathbf { W } _ { t }$ through the ECIG and WSCP modules. The network is optimized with standard perception, motion prediction, and ego planning losses, allowing the world state to encode interaction-aware and safety-relevant scene semantics.

Stage II: Temporal world state consistency learning. In the second stage, we introduce temporal supervision by leveraging observations at time t+1. Specifically, the model predicts the next-step world state $\mathbf { W } _ { t + 1 }$ from inputs at time t+1, while the world state inferred at time t is encouraged to be temporally consistent with $\mathbf { W } _ { t + 1 }$ . We enforce this consistency using an $\ell _ { 2 }$ regression loss:

$$
\mathcal { L } _ { \mathrm { w o r l d } } = \Vert \mathbf { W } _ { t } - \mathrm { S T O P G R A D } ( \mathbf { W } _ { t + 1 } ) \Vert _ { 2 } ^ { 2 } ,\tag{23}
$$

where STOPGRAD(·) prevents gradient backpropagation through the t+1 branch.

Training objective. The final training loss is a weighted combination of task-specific losses and the temporal worldstate consistency loss:

$$
\begin{array} { r } { \mathcal { L } = \mathcal { L } _ { \mathrm { p e r c e p } } + \mathcal { L } _ { \mathrm { m o t i o n } } + \mathcal { L } _ { \mathrm { p l a n } } + \lambda \mathcal { L } _ { \mathrm { w o r l d } } , } \end{array}\tag{24}
$$

where λ balances temporal consistency and task performance.

## 5 EXPERIMENTS

## 5.1 Dataset

Bench2Drive (Close-Loop). We conduct training and evaluation of GraphWorld on the Bench2Drive [71], a closedloop evaluation protocol based on the CARLA Leaderboard 2.0 [72] for E2E-AD. It provides a base training set of 1000 clips, with 950 used for training and 50 for open-loop validation. Each clip captures approximately 150 meters of continuous driving in a specific traffic scenario. For closedloop evaluation, we use the official 220 routes, covering 44 interactive scenarios with 5 routes each.

NAVSIMv1/2 (Close-Loop). We conduct training and evaluation of GraphWorld on the NAVSIMv1 [73] dataset. NAVSIMv1 is a real-world, planning-oriented dataset that builds upon OpenScene, a compact redistribution of nuPlan [74], the largest publicly available annotated driving dataset. It leverages eight cameras to achieve a full 360° field of view, along with a merged LiDAR point cloud derived from five sensors. Annotations are provided at 2 Hz and include both HD maps and object bounding boxes. The dataset is specifically designed to emphasize challenging driving scenarios involving dynamic changes in driving intentions, while deliberately excluding trivial cases such as stationary scenes or constant-speed cruising.

NuScenes (Open-Loop). We conduct extensive open-loop experiments on the nuScenes dataset [75], which consists of 1000 driving scenes (700 for training, 150 for validation and 150 for test). Each scene lasts 20 seconds and includes around 40 key-frames annotated at 2 Hz. Each sample contains six images from surround-view cameras (covering 360° FOV), and point clouds from both LiDAR and radar sensors.

Turning-nuScenes (Open-Loop). We conduct extensive open-loop experiments on the Turning-nuScenes dataset [4], a challenging subset of NuScenes proposed by MomAD [4] to evaluate trajectory consistency in non-trivial maneuvers. While most planning tasks in the original nuScenes dataset primarily involve go-straight commands, TurningnuScenes specifically focuses on turning scenarios to assess the temporal coherence of predicted trajectories. To construct this subset, samples are selected based on a displacement threshold of 25 meters between the predicted positions at 0.5s and 3.0s in the GT ego trajectory. The resulting validation set comprises 680 samples across 17 scenes, accounting for approximately one-tenth of the full nuScenes validation set.

Adv-nuSc (Open-Loop). To evaluate adversarial robustness, we conduct extensive open-loop experiments on the AdvnuSc [76] dataset. It contains 156 scenes (6,115 samples) and is specifically crafted to challenge the ego vehicle by introducing adversarial traffic participants.It is built upon the validation split of the nuScenes dataset [75], which contains 150 scenes, each with 20 seconds of driving data. For each scene, we randomly select up to 10 background vehicles (if there are that many) that come close to the ego vehicle at any point in time and designate them as candidate adversarial agents. Challenger is then used to generate adversarial trajectories for these vehicles, creating diverse and challenging driving scenarios.

NuScenes-C (Open-Loop). NuScenes-C [77] is a corrupted benchmark derived from the nuScenes validation set, introducing various types of noise to assess the robustness of planning models. It includes 27 corruption types applied at 5 severity levels. To evaluate robustness under adverse weather conditions, we select three representative weather corruptions — Rain, Snow, and Fog — as our test scenarios.

TABLE 2: Open-Loop, Closed-Loop results and Multi-Ability results on Bench2Drive (V0.0.3) under base training set. ‘mmt’ refers multi-mode trajectory variant of VAD and <sup>†</sup> denotes the re-implementation. \* denotes expert feature distillation. ‘DS’ denotes Driving Score. ‘SR’ denotes Success Rate. ‘Effi’ denotes Efficiency. ‘Comf’ denotes Comfortness. ‘Merg.’ denotes Merging. ‘Overta.’ denotes Overtaking. ‘Emerge.’ denotes Emergency Brake.
<table><tr><td rowspan="2">Method</td><td rowspan="2">Venue</td><td>Open-loop Metric</td><td colspan="4">Closed-loop Metric</td><td colspan="6">Multi-Ability(%) ↑</td></tr><tr><td>Avg. L2 ↓</td><td>DS ↑SR (%) ↑Effi ↑Comf ↑Merg. ↑Overta. Emerge. Give Way Traffic Sign Mean</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>ThinkTwice* [43]</td><td>CVPR2023</td><td>0.95</td><td>62.44</td><td>31.23</td><td>69.33</td><td>16.22</td><td>27.38</td><td>18.42</td><td>35.82</td><td>50.00</td><td>54.23 56.43</td><td>37.17</td></tr><tr><td>DriveAdapter* [44]</td><td>ICCV2023</td><td>1.01</td><td>64.22</td><td>33.08</td><td>70.22</td><td>16.01</td><td>28.82</td><td>26.38</td><td>48.76</td><td>50.00</td><td></td><td>42.08</td></tr><tr><td>DriveDPO [45]</td><td>NeurIPS2025</td><td></td><td>62.02</td><td>30.62</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Raw2Drive [46] DriveTrans*</td><td>NeurIPS2025 ICLR2025</td><td>0.62</td><td>71.36 63.46</td><td>50.24 35.01</td><td></td><td></td><td>43.35</td><td>51.11</td><td>60.00</td><td>50.00</td><td>62.26</td><td>53.34</td></tr><tr><td>[47] WoTE* [24]</td><td>ICCV2025</td><td></td><td>61.71</td><td>31.36</td><td></td><td>100.64 20.78</td><td>17.57</td><td>35.00</td><td>48.36</td><td>40.00</td><td>52.10</td><td>38.60</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>ThinkTwicemmt *† GraphWorld (Ours)</td><td>[43]CVPR2023</td><td>0.93 0.81</td><td>63.34 76.71</td><td>33.23 44.22</td><td>71.56</td><td>18.32</td><td>31.31</td><td>21.23</td><td>38.33</td><td>50.00</td><td>57.45</td><td>39.66</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td>80.48</td><td>29.74</td><td>42.85</td><td>32.57</td><td>49.09</td><td>50.00</td><td>67.16</td><td>48.33</td></tr><tr><td>UniAD-Base [3]</td><td>CVPR2023</td><td>0.73</td><td>45.81</td><td>16.36</td><td>129.21</td><td>43.58</td><td>14.10</td><td>17.78</td><td>21.67</td><td>10.00</td><td>14.21</td><td>15.55</td></tr><tr><td>VAD [5]</td><td>ICCV2023</td><td>0.91</td><td>42.35</td><td>15.00</td><td>157.94</td><td>46.01</td><td>8.11</td><td>24.44</td><td>18.64</td><td>20.00</td><td>19.15</td><td>18.07</td></tr><tr><td>GenAD [48]</td><td>ECCV2024 CVPR2025</td><td>0.82</td><td>44.81 47.91</td><td>15.90</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>MomAD(SD) [4]</td><td></td><td></td><td></td><td>18.11</td><td>174.91</td><td>51.20</td><td>13.21</td><td>21.02</td><td>18.01</td><td>20.00</td><td>21.07</td><td>18.66</td></tr><tr><td>VADmmt † [5]</td><td>ICCV 2023</td><td>0.89</td><td>42.87</td><td>15.91</td><td>158.12</td><td>47.22</td><td>9.43</td><td>25.31</td><td>19.91</td><td>20.00</td><td>20.09</td><td>18.95</td></tr><tr><td>GraphWorid (Ours)</td><td></td><td>0.81</td><td>50.78</td><td>22.59</td><td>168.11</td><td>54.04</td><td>16.84</td><td>32.31</td><td>28.46</td><td>20.00</td><td>27.61</td><td>25.04</td></tr><tr><td>SparseDrive† [6]</td><td>ICRA2025</td><td>0.87</td><td>44.54</td><td>16.71</td><td>170.21</td><td>48.63</td><td>12.18</td><td>23.19</td><td>17.91</td><td>20.00</td><td>20.98</td><td>18.85</td></tr><tr><td>GraphWorld (Ours)</td><td></td><td>0.79</td><td>51.55</td><td>25.47</td><td>181.12</td><td>56.59</td><td>18.74</td><td>31.66</td><td>25.30</td><td>20.00</td><td>26.66</td><td>24.47</td></tr></table>

TABLE 3: Comparison on planning-oriented NAVSIMv1 navtest split with Closed-Loop metrics. ‘mmt’ refers multimodal trajectory variant of TransFuser and <sup>∗</sup> denotes the re-implementation.
<table><tr><td colspan="6">Method NC↑ DAC↑ TTC↑ Conf.↑ EP↑ PDMS↑</td></tr><tr><td colspan="6">E2E-based Methods</td></tr><tr><td>VADv2 [9] TransFuser [7]</td><td>97.2 89.1 97.7 92.8</td><td>91.6 92.8</td><td>100 100</td><td>76.0 79.2 80.7</td><td>80.9 84.0</td></tr><tr><td>TransFusermmt * [7] UniAD [3]</td><td>96.2</td><td>95.4 91.9</td><td>90.7 92.9</td><td>100 100 78.8</td><td>85.1 83.4</td></tr><tr><td>PARA-Drive [49]</td><td>97.8 97.9</td><td>92.4</td><td>93.0</td><td>99.8</td><td>84.0</td></tr><tr><td></td><td></td><td></td><td></td><td>79.3</td><td></td></tr><tr><td>DRAMA [50]</td><td>98.0 93.1</td><td>94.8</td><td>100</td><td>80.1</td><td>85.5</td></tr><tr><td>GoalFlow [14]</td><td>98.3 93.8</td><td>94.3</td><td>100</td><td>79.8</td><td>85.7</td></tr><tr><td>Hydra-MDP [12]</td><td>98.3 96.0</td><td>94.6</td><td>100</td><td>78.7</td><td>86.5</td></tr><tr><td>FÚMP [51]</td><td>98.1 96.2</td><td>94.2</td><td>100</td><td>82.0</td><td>87.8</td></tr><tr><td>DiffusionDrive [10]</td><td>98.2 96.2</td><td>94.7</td><td></td><td>100 82.2</td><td>88.1</td></tr><tr><td>DIVER [11]</td><td>98.5 96.5</td><td>94.9</td><td></td><td>100 82.6</td><td>88.3</td></tr><tr><td>DriveSuprim [52]</td><td>97.8 97.3</td><td>93.6</td><td></td><td>100 86.7</td><td>89.9</td></tr><tr><td>GoalFlow [14]</td><td>98.4 98.3</td><td>94.6</td><td></td><td>100 85.0</td><td>90.3</td></tr><tr><td>ReCogDrive-IL[53]</td><td>98.1 94.7</td><td></td><td>94.2</td><td>100 80.9</td><td>86.5</td></tr><tr><td colspan="6">VLA-based Methods</td></tr><tr><td></td><td>98.4</td><td>95.6</td><td>98.0</td><td>99.9</td><td></td></tr><tr><td>AutoVLA [54]</td><td>98.2</td><td></td><td></td><td>81.9</td><td>89.1</td></tr><tr><td>Recogdrive [53]</td><td>97.8</td><td>95.2</td><td>99.8</td><td>83.5</td><td>89.6</td></tr><tr><td>DriveVLA-W0 [55] DriveWorld-VLA [56]</td><td>98.7 99.1</td><td>95.3</td><td></td><td>99.3 83.3</td><td>90.2 91.3</td></tr><tr><td></td><td>99.1</td><td>98.2</td><td>96.1</td><td>100</td><td>85.9</td></tr><tr><td colspan="6">World-Model-based Methods</td></tr><tr><td>DrivingGPT[57]</td><td>98.9</td><td>90.7 94.9</td><td>95.6</td><td>79.7</td><td>82.4</td></tr><tr><td>Resim[58]</td><td></td><td></td><td></td><td></td><td>86.6</td></tr><tr><td>DriveVLA-W0 [55]</td><td>98.4</td><td>95.3</td><td>95.2</td><td>100 80.9</td><td>87.2</td></tr><tr><td>PWM[59]</td><td>98.6</td><td>95.9</td><td>95.4</td><td>100 81.8</td><td>88.1</td></tr><tr><td>LAW [41]</td><td>96.4</td><td>95.4</td><td>88.7</td><td>99.9 81.7</td><td>84.6</td></tr><tr><td>World4Drive [26]</td><td>97.4</td><td>94.3</td><td>92.8</td><td>100</td><td>79.9 85.1</td></tr><tr><td>Epona [35]</td><td>97.9</td><td>95.1</td><td>93.8</td><td>99.9</td><td>80.4 86.2</td></tr><tr><td>WoTE [24]</td><td>98.5</td><td>96.8</td><td>94.9</td><td>99.9</td><td>81.9 88.3</td></tr><tr><td>WorldRFT [60]</td><td>97.8</td><td>96.8</td><td>94.0</td><td>100</td><td>81.7 87.8</td></tr><tr><td>DriveLaW [61]</td><td>99.0</td><td>97.1</td><td>96.7</td><td>100</td><td>81.3 89.1</td></tr><tr><td>DriveX-S[36]</td><td>97.5</td><td>94.0</td><td>93.0</td><td>100</td><td>79.7 84.5</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td>83.2</td></tr><tr><td>GraphWorld (Ours)</td><td>99.0</td><td>97.1</td><td>95.5</td><td>100</td><td>90.1</td></tr></table>

## 5.2 Evaluation Metrics

Close-Loop (Bench2Drive). The Bench2Drive [71] includes five metrics for closed-loop evaluation: Driving Score (DS), Success Rate (SR), Efficiency, Comfortness, and Multi-Ability. The Success Rate quantifies the proportion of routes successfully completed within the allotted time. The Driving Score follows CARLA [11], incorporating both route completion status and violation penalties, where infractions reduce the score via discount factors. Efficiency and Comfortness are used to measure the speed performance and comfort of the autonomous driving system during the driving process, respectively. Multi-Ability measures 5 advanced skills, including ‘Merging, Overtaking, Emergency Brake, Give Way, and Traffic Sign’, independently for urban driving.

Close-Loop (NAVSIMv1). NAVSIMv1[73] metrics include No at-fault Collision (NC), Drivable Area Compliance (DAC), Time-to-Collision (TTC), Comfort (C.), and Ego Progress (EP). NAVSIMv1 uses the Predictive Driver Model Score (PDMS) to evaluate model performance.

Close-Loop (NAVSIMv2). NAVSIMv2 [62] evaluates planners using the Extended Predictive Driver Model Score (EPDMS), which aggregates penalties and weighted subscores including no at-fault collision (NC), drivable area compliance (DAC), driving direction compliance (DDC), traffic light compliance (TLC), ego progress (EP), time to collision (TTC), lane keeping (LK), history comfort (HC), and extended comfort (EC). It also introduces a Navhard split with a two-stage protocol: (i) the planner is scored on real observations, and (ii) it is re-evaluated under perturbed future observations synthesized via 3D Gaussian Splatting around the stage-1 endpoint. The final EPDMS is obtained by Gaussian-weighted aggregation of the two-stage scores.

Open-Loop. For the nuScenes dataset [75], Adv-nuSc [76], Turning-nuScenes [4], and nuScenes-C [77], we employ conventional $L _ { 2 }$ error and CR (collision rate) as metrics, aligning with the computation method of SparseDrive [6].

TABLE 4: Comparison with SOTA methods on the NAVSIMv2 navhard split [62].
<table><tr><td>Method</td><td>Backbone</td><td>Stage</td><td>NC↑</td><td>DAC↑</td><td>DDC↑</td><td>TL↑</td><td>EP↑</td><td>TTC↑</td><td>LK↑</td><td>HC↑</td><td>EC↑</td><td>EPDMS↑</td></tr><tr><td colspan="9">E2E-based Methods</td><td colspan="3"></td></tr><tr><td>TransFuser [7]</td><td>ResNet-34</td><td>Stage 1 Stage 2</td><td>96.2 77.7</td><td>79.5 70.2</td><td>99.1 84.2</td><td>99.5 98.0</td><td>84.1 85.1</td><td>95.1 75.6</td><td>94.2 45.4</td><td>97.5 95.7</td><td>79.1 75.9</td><td>23.1</td></tr><tr><td>DiffusionDrive [10]</td><td>ResNet-34</td><td>Stage 1 Stage 2</td><td>96.0 82.1</td><td>79.7 72.2</td><td>97.4 88.5</td><td>99.5 98.7</td><td>81.3 85.1</td><td>93.1 78.8</td><td>90.8 49.2</td><td>96.8 89.3</td><td>73.8 71.2</td><td>24.2</td></tr><tr><td>GuideFlow [16]</td><td>ResNet-34</td><td>Stage 1 Stage 2</td><td>96.6 87.3</td><td>80.5 76.7</td><td>96.3 88.8</td><td>99.3 99.2</td><td>82.3 84.3</td><td>94.9 85.1</td><td>91.5 49.7</td><td>97.7 93.1</td><td>67.8 44.5</td><td>27.1</td></tr><tr><td>RAP-DINO</td><td>VIT</td><td>Stage 1 Stage 2</td><td>97.1 83.2</td><td>94.4 83.9</td><td>98.8 87.4</td><td>99.8 98.0</td><td>83.9 86.9</td><td>96.9 80.4</td><td>94.7 52.3</td><td>96.4 95.2</td><td>66.2 52.4</td><td>36.9</td></tr><tr><td>DriveSuprim [52]</td><td>V2-99</td><td>Stage 1 Stage 2</td><td>98.9 87.9</td><td>95.1 88.8</td><td>99.2 89.6</td><td>99.6 98.8</td><td>76.1 80.3</td><td>99.1 86.0</td><td>94.7 53.5</td><td>97.6 97.1</td><td>54.2 56.1</td><td>42.1</td></tr><tr><td colspan="9">VLA-based Methods</td><td colspan="2"></td></tr><tr><td>SpanVLA [63]</td><td>Qwen2.5-VL-3B</td><td>Stage 1 Stage 2</td><td>98.4 86.9</td><td>94.3 84.3</td><td>97.8 87.1</td><td>99.9 98.2</td><td>85.7 85.5</td><td>97.2 82.7</td><td>94.2 62.3</td><td>97.6 96.8</td><td>72.1 67.4</td><td>40.1</td></tr><tr><td>DiffVLA [64]</td><td>V2-99 + ViT-L/14</td><td>Stage 1 Stage 2</td><td>95.7 81.2</td><td>99.2 88.8</td><td>100.0 94.6</td><td>100.0 99.0</td><td>85.9 86.0</td><td>96.4 76.4</td><td>97.1 59.8</td><td>95.0</td><td>84.2</td><td>45.0</td></tr><tr><td colspan="9"></td><td rowspan="2">98.6 80.4</td></tr><tr><td>MindDrive [15]</td><td>ResNet-34</td><td>Stage 1</td><td>96.1</td><td>86.0</td><td>World-Model-based Methods 98.8</td><td>99.3</td><td>83.3</td><td>95.6</td><td>94.4</td><td>97.6</td><td></td></tr><tr><td colspan="10"></td><td></td><td>74.7 71.0</td><td>30.9</td></tr><tr><td>World4Drive [26]</td><td>ResNet-34</td><td>Stage 2 Stage 1</td><td>82.6 97.3</td><td>79.1 89.1</td><td>86.4 97.6</td><td>98.0 99.7</td><td>85.3 60.5</td><td>79.4 96.8</td><td>49.2 87.7</td><td>96.5 93.1</td><td>60.0</td><td></td></tr><tr><td></td><td></td><td>Stage 2 Stage 1</td><td>91.4</td><td>82.0</td><td>91.0</td><td>98.5 98.0</td><td>53.1 83.9</td><td>90.6 97.8</td><td>52.3</td><td>93.3</td><td>62.8</td><td>34.9</td></tr><tr><td>GraphWorld (Ours)</td><td>ResNet-34</td><td>Stage 2</td><td>98.1 88.6</td><td>97.9 85.9</td><td>97.9 92.2</td><td>97.6</td><td>82.4</td><td>87.0</td><td>97.2 56.6</td><td>95.4 91.4</td><td>64.5 44.0</td><td>53.6</td></tr></table>

TABLE 5: Comparison with SOTA methods on the NAVSIMv2 navtest split [62]. EPDMS<sup>∗</sup> denotes results computed with the original NAVSIMv2 evaluation code before the human-behavior filtering fix, while EPDMS denotes the corrected official implementation.
<table><tr><td>Method</td><td>NC↑</td><td>DAC↑</td><td>DDC↑</td><td>TL↑</td><td>EP↑</td><td>TTC↑</td><td>LK↑</td><td>HC↑</td><td>EC↑</td><td>EPDMS↑</td></tr><tr><td colspan="9">E2E-based Methods</td></tr><tr><td>TransFuser [7]</td><td>96.9</td><td>89.9</td><td>97.8</td><td>99.7</td><td>87.1</td><td>95.4</td><td>92.7</td><td>98.3</td><td>87.2</td><td>76.7</td></tr><tr><td>DiffusionDrive [10]</td><td>98.2</td><td>95.9</td><td>99.4</td><td>99.8</td><td>87.5</td><td>97.3</td><td>96.8</td><td>98.3</td><td>87.7</td><td>84.5</td></tr><tr><td>Hydra-MDP++ [65]</td><td>97.2</td><td>97.5</td><td>99.4</td><td>99.6</td><td>83.1</td><td>96.5</td><td>94.4</td><td>98.2</td><td>70.9</td><td>81.4</td></tr><tr><td>DriveSuprim [52]</td><td>97.5</td><td>96.5</td><td>99.4</td><td>99.6</td><td>88.4</td><td>96.6</td><td>95.5</td><td>98.3</td><td>77.0</td><td>83.1</td></tr><tr><td>DiffusionDriveV2 [66]</td><td>97.7</td><td>96.6</td><td>99.2</td><td>99.8</td><td>88.9</td><td>97.2</td><td>96.0</td><td>97.8</td><td>91.0</td><td>87.5</td></tr><tr><td colspan="9"></td></tr><tr><td>DriveWorld-VLA [56]</td><td>98.6</td><td>99.1</td><td>99.6</td><td>VLA-based Methods 99.8</td><td>87.4</td><td>97.9</td><td>97.0</td><td>97.8</td><td>78.6</td><td>86.8</td></tr><tr><td>DriveVLA-W0 [55]</td><td>98.5</td><td>99.1</td><td>98.0</td><td>99.7</td><td>86.4</td><td>98.1</td><td>93.2</td><td>97.9</td><td>58.9</td><td>86.1</td></tr><tr><td>Recogdrive [53]</td><td>98.3</td><td>95.2</td><td>98.3</td><td>99.8</td><td>87.1</td><td>97.5</td><td>96.6</td><td>99.5</td><td>86.5</td><td>83.6</td></tr><tr><td colspan="9"></td></tr><tr><td>Latent-WAM [67]</td><td></td><td></td><td></td><td>World-Model-based Methods</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>GraphWorld (Ours)</td><td>98.1 98.4</td><td>97.3 98.8</td><td>99.6 99.1</td><td>99.8 99.1</td><td>87.7 85.9</td><td>97.3 97.9</td><td>97.6 96.0</td><td>98.1 97.8</td><td>87.3 74.6</td><td>89.3 89.5</td></tr></table>

TABLE 6: Planning results for 3-second short-horizon planning on the nuScenes validation set.
<table><tr><td rowspan="2">Method</td><td colspan="4">L2 (m) ↓</td><td colspan="4">Col. Rate (%) ↓</td></tr><tr><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td></tr><tr><td>UniAD[3]</td><td>0.48</td><td>0.96</td><td>1.65</td><td>1.03</td><td>0.10</td><td>0.15</td><td>0.61</td><td>0.29</td></tr><tr><td>VAD [5]</td><td>0.41</td><td>0.70</td><td>1.05</td><td>0.72</td><td>0.11</td><td>0.24</td><td>0.42</td><td>0.26</td></tr><tr><td>DiffusionDrive [10]</td><td>0.29</td><td>0.58</td><td>0.96</td><td>0.61</td><td>0.02</td><td>0.05</td><td>0.22</td><td>0.09</td></tr><tr><td>DIVER [11]</td><td></td><td></td><td></td><td></td><td>0.01</td><td>0.05</td><td>0.15</td><td>0.07</td></tr><tr><td>FocalAD [68]</td><td>0.27</td><td>0.57</td><td>0.96</td><td>0.60</td><td>0.00</td><td>0.04</td><td>0.24</td><td>0.09</td></tr><tr><td>SparseDrive [6]</td><td>0.30</td><td>0.58</td><td>0.96</td><td>0.61</td><td>0.01</td><td>0.05</td><td>0.23</td><td>0.10</td></tr><tr><td>LAW [41]</td><td>0.26</td><td>0.57</td><td>1.01</td><td>0.61</td><td>0.14</td><td>0.21</td><td>0.54</td><td>0.30</td></tr><tr><td>GenAD [48]</td><td>0.28</td><td>0.49</td><td>0.78</td><td>0.52</td><td>0.08</td><td>0.14</td><td>0.34</td><td>0.19</td></tr><tr><td>Drive-OccWorld [69]</td><td>0.25</td><td>0.44</td><td>0.72</td><td>0.47</td><td>0.03</td><td>0.08</td><td>0.22</td><td>0.11</td></tr><tr><td>SSR [70]</td><td>0.19</td><td>0.36</td><td>0.62</td><td>0.39</td><td>0.10</td><td>0.10</td><td>0.24</td><td>0.15</td></tr><tr><td>MomAD [4]</td><td>0.31</td><td>0.57</td><td>0.91</td><td>0.60</td><td>0.01</td><td>0.05</td><td>0.22</td><td>0.09</td></tr><tr><td>GraphWorld(Ours)</td><td>0.29</td><td>0.55</td><td>0.89</td><td>0.57</td><td>0.00</td><td>0.04</td><td>0.20</td><td>0.08</td></tr></table>

## 5.3 Implementation Details

To demonstrate the generalization capability of Graph-World, we evaluate it against several strong E2E-AD baselines, including SparseDrive [6] and TransFuser [7].

TABLE 7: Motion prediction results on the nuScenes dataset.
<table><tr><td>Method</td><td>minADE↓</td><td>minFDE↓</td><td>MR↓</td><td>EPA↑</td></tr><tr><td>UniAD [3]</td><td>0.71</td><td>1.02</td><td>0.151</td><td>0.456</td></tr><tr><td>VAD [5]</td><td>0.68</td><td>0.88</td><td>0.083</td><td></td></tr><tr><td>SparseDrive [6]</td><td>0.62</td><td>0.99</td><td>0.136</td><td>0.482</td></tr><tr><td>GraphWorld(Ours)</td><td>0.55</td><td>0.86</td><td>0.112</td><td>0.512</td></tr></table>

On the Bench2Drive [71], nuScenes [75], and AdvnuScenes [76] datasets, we compare GraphWorld with SparseDrive. For nuScenes and Adv-nuScenes, we adopt a ResNet-50 [78] backbone with an input resolution of 256 × 704. The detection module operates within a circular range of 55 meters, while the online mapping module covers a 60 × 30 meter area (longitudinal × lateral). The motion prediction module generates 6 trajectory modes.

For Bench2Drive, we use a ResNet-50 backbone with 6 decoder layers and an input resolution of $6 4 0 \times 3 5 2 .$ . We define fixed numbers of hybrid task queries, including 900 agent queries, 100 map queries, and 480 planning queries, following the standard benchmark configuration.

TABLE 8: Robustness study of planning performance on Adv-nuSc under adversarial driving scenarios.
<table><tr><td rowspan="2">Method</td><td colspan="4">Col. Rate (%) ↓</td></tr><tr><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td></tr><tr><td>UniAD [3]</td><td>0.800</td><td>4.100</td><td>6.960</td><td>3.950</td></tr><tr><td>VAD [5]</td><td>4.460</td><td>7.590</td><td>9.080</td><td>7.050</td></tr><tr><td>SparseDrive [6]</td><td>0.029</td><td>0.618</td><td>2.430</td><td>1.026</td></tr><tr><td>DiffusionDrive [10]</td><td>0.068</td><td>1.299</td><td>3.646</td><td>1.671</td></tr><tr><td>DIVER [11]</td><td>0.033</td><td>0.423</td><td>1.798</td><td>0.752</td></tr><tr><td>GraphWorld (Ours)</td><td>0.028</td><td>0.420</td><td>1.780</td><td>0.742</td></tr></table>

TABLE 9: Robustness study of planning performance on nuScenes-C.
<table><tr><td rowspan="2">Scene</td><td rowspan="2">Method</td><td colspan="4">Col. Rate (%) ↓</td></tr><tr><td>1s</td><td>2s</td><td>3s</td><td> $\operatorname { A v g } .$ </td></tr><tr><td rowspan="4">Clean</td><td>SparseDrive [6]</td><td>0.01</td><td>0.05</td><td>0.18</td><td>0.08</td></tr><tr><td>MomAD [4]</td><td>0.01</td><td>0.05</td><td>0.22</td><td>0.09</td></tr><tr><td>DiffusionDrive [10]</td><td>0.03</td><td>0.05</td><td>0.16</td><td>0.08</td></tr><tr><td>GraphWorld (Ours)</td><td>0.00</td><td>0.04</td><td>0.20</td><td>0.08</td></tr><tr><td rowspan="4">Snow</td><td>SparseDrive [6]</td><td>0.13</td><td>0.27</td><td>0.50</td><td>0.30</td></tr><tr><td>MomAD [4]</td><td>0.08</td><td>0.16</td><td>0.30</td><td>0.18</td></tr><tr><td>DiffusionDrive [10]</td><td>0.09</td><td>0.24</td><td>0.39</td><td>0.24</td></tr><tr><td>GraphWorld (Ours)</td><td>0.07</td><td>0.15</td><td>0.28</td><td>0.17</td></tr><tr><td rowspan="4">Rain</td><td>SparseDrive [6]</td><td>0.11</td><td>0.27</td><td>0.55</td><td>0.31</td></tr><tr><td>MomAD [4]</td><td>0.06</td><td>0.17</td><td>0.31</td><td>0.18</td></tr><tr><td>DiffusionDrive [10]</td><td>0.07</td><td>0.18</td><td>0.35</td><td>0.20</td></tr><tr><td>GraphWorld (Ours)</td><td>0.05</td><td>0.15</td><td>0.29</td><td>0.16</td></tr><tr><td rowspan="4">Fog</td><td>SparseDrive [6]</td><td>0.14</td><td>0.36</td><td>0.58</td><td></td></tr><tr><td>MomAD [4]</td><td>0.06</td><td>0.19</td><td>0.32</td><td>0.36 0.19</td></tr><tr><td>DiffusionDrive [10]</td><td>0.06</td><td>0.18</td><td>0.30</td><td></td></tr><tr><td>GraphWorld (Ours)</td><td>0.05</td><td>0.17</td><td>0.29</td><td>0.18 0.17</td></tr></table>

On the NAVSIM [73] dataset, we adopt TransFuser as the baseline and follow the official Navtrain split for training. For fair comparison, we use the same perception modules and a ResNet-34 backbone as in TransFuser. All experiments are conducted on 8 NVIDIA RTX 4090 GPUs. We use a batch size of 48 for nuScenes and Bench2Drive, and 64 for NAVSIM.

The models are trained for 20 epochs on nuScenes (∼10.2h), 2 epochs on Bench2Drive (∼49.2h), and 100 epochs on NAVSIM (∼3.1h). We adopt the AdamW optimizer with a learning rate of $3 \times 1 0 ^ { - 4 }$ and weight decay of $1 0 ^ { - 3 }$ , together with a cosine annealing schedule and linear warmup. The training objective consists of standard multi-task losses for detection, mapping, motion prediction, and planning. We apply common data augmentations, including resizing, cropping, flipping, and photometric distortion, along with BEV-consistent transformations. Additional training techniques include gradient clipping (max norm 25), FP16 training, and a temporal queue length of 4.

## 5.4 Main Results

Long-Horizon Planning on nuScenes (Open-Loop). Table 1 reports open-loop long-horizon planning results on the nuScenes validation set. While existing E2E-AD methods perform competitively at short horizons, their errors and collision rates increase significantly as the planning horizon extends. In contrast, GraphWorld consistently outperforms all baselines across all future timestamps, achieving the lowest average L2 error of 1.34m. More importantly, it reduces the average collision rate to 0.70%, corresponding to over 22% relative improvement over the strongest prior method. The advantage becomes more pronounced at longer horizons (5–6s), demonstrating GraphWorld’s superior longterm interaction modeling and safety-aware planning capability.

TABLE 10: Robustness study of planning results on the Turning-nuScenes [4] validation dataset. <sup>∗</sup> denotes the reimplementation.
<table><tr><td rowspan="2">Method</td><td colspan="4">Col. Rate (%) ↓</td></tr><tr><td>1s</td><td>2s</td><td>3s</td><td> $\operatorname { A v g } .$ </td></tr><tr><td>SparseDrive [6]</td><td>0.04</td><td>0.17</td><td>0.98</td><td>0.40</td></tr><tr><td>DiffusionDrive* [10]</td><td>0.03</td><td>0.14</td><td>0.85</td><td>0.34</td></tr><tr><td>MomAD [4]</td><td>0.03</td><td>0.13</td><td>0.79</td><td>0.32</td></tr><tr><td>GraphWorld (Ours)</td><td>0.03</td><td>0.12</td><td>0.72</td><td>0.28</td></tr></table>

Bench2Drive (Closed-Loop). Table 2 reports results on Bench2Drive. GraphWorld achieves the best closed-loop performance, significantly improving Driving Score (DS) and Success Rate (SR) over prior methods. Compared with SparseDrive, it increases DS from 44.54% to 51.55% and SR from 16.71% to 25.47%, while also improving efficiency and comfort, indicating more stable driving behavior. It further shows strong advantages in interaction-critical scenarios such as merging, overtaking, and emergency braking, demonstrating effective multi-agent interaction modeling. Although open-loop improvements are moderate, the substantial closed-loop gains highlight the importance of interaction and long-horizon modeling beyond trajectory fitting. Overall, GraphWorld provides more balanced improvements across accuracy, safety, and decision-making quality.

NAVSIMv1 navtest (Closed-Loop). Table 3 reports closedloop planning results on the NAVSIM v1 navtest split. While recent E2E-based and VLA-based methods achieve strong performance, GraphWorld remains highly competitive across all metrics. In particular, it achieves 99.0 in NC and 97.1 in DAC, matching or surpassing most prior world-model-based approaches, while maintaining strong performance in safety-critical metrics such as TTC and EP. Compared with existing world-model-based methods, GraphWorld consistently improves interaction-related performance, achieving higher EP (83.2) and PDMS (90.1), indicating better decision quality and robustness in complex driving scenarios. Although some VLA-based methods obtain slightly higher scores on individual metrics, GraphWorld provides a more balanced performance across safety, interaction, and planning stability. Overall, these results demonstrate that GraphWorld effectively captures multi-agent dynamics and enables robust closed-loop planning, achieving competitive performance while maintaining strong generalization and consistency across metrics.

NAVSIMv2 navhard (Closed-Loop). Table 4 reports closedloop results on the challenging NAVSIMv2 navhard split. While existing E2E-based and VLA-based methods achieve strong performance in Stage 1, their performance drops significantly in Stage 2, reflecting the difficulty of long-horizon and interaction-heavy scenarios. In contrast, GraphWorld remains highly competitive and achieves the best overall performance with an EPDMS score of 53.6, outperforming all prior methods by a clear margin. More importantly, GraphWorld maintains strong performance across safetycritical and interaction-related metrics, including EP, TTC, and DAC, demonstrating its robustness in complex driving situations. Compared with prior world-model-based methods, it consistently improves both stability and decision quality, especially under long-horizon closed-loop evaluation. The advantage becomes more pronounced in Stage 2, where accumulated errors and interaction complexity are more severe, highlighting the effectiveness of our agentcentric relational world modeling and flow-based refinement. These results demonstrate that GraphWorld enables more robust long-horizon planning and better handles complex multi-agent interactions in challenging scenarios.

TABLE 11: Ablation study of different modules across nuScenes (open-loop), NAVSIMv1 (closed-loop), and Bench2Drive.
<table><tr><td></td><td></td><td></td><td colspan="5">nuScenes (Open-loop)</td><td colspan="5">NAVSIMv1 (Closed-loop)</td><td colspan="5"></td></tr><tr><td>ECIG WSCP | L2@4s↓</td><td></td><td></td><td>L2@5s↓</td><td>L2@6s↓</td><td>Col.@4s↓</td><td>Col.@5s↓</td><td></td><td>Col.@6s↓ | NC↑</td><td>DAC↑</td><td>TTC↑</td><td>Comf.↑</td><td>EP↑</td><td>PDMS↑</td><td>DS↑</td><td>SR↑</td><td>Effi↑</td><td>Comf↑</td></tr><tr><td></td><td></td><td>1.75</td><td>2.32</td><td>2.95</td><td>0.87</td><td>1.54</td><td>2.33</td><td>96.2</td><td>95.4 90.7</td><td>100</td><td>80.7</td><td></td><td>85.1</td><td>44.54</td><td>16.71</td><td>170.21</td><td>48.63</td></tr><tr><td>√</td><td></td><td>1.71</td><td>2.28</td><td>2.76</td><td>0.79</td><td>1.47</td><td>2.19</td><td>97.2</td><td>96.0</td><td>91.6 100</td><td></td><td>81.1</td><td>85.5</td><td>49.44</td><td>23.89</td><td>177.92</td><td>53.07</td></tr><tr><td></td><td></td><td>1.64</td><td>1.88</td><td>2.29</td><td>0.65</td><td>1.29</td><td>1.95</td><td>99.0</td><td>97.1</td><td>95.5</td><td>100</td><td>83.2</td><td>90.1</td><td>51.55</td><td>25.47</td><td>181.12</td><td>56.59</td></tr></table>

TABLE 12: Ablation study on different graph structures across NAVSIMv1 and nuScenes. Fully-connected denotes a dense graph, while ego→nbrs denotes an ego-centric star graph.
<table><tr><td rowspan="2">Structure</td><td colspan="5">NAVSIMv1</td><td rowspan="2"></td><td colspan="6">nuScenes</td></tr><tr><td>NC↑</td><td>DAC↑</td><td>TTC↑</td><td>Comf.↑</td><td>EP↑</td><td>PDMS↑</td><td>L2@4s↓</td><td>L2@5s↓</td><td>L2@6s↓ Col.@4s↓</td><td>Col.@5s↓</td><td>Col.@6s↓</td></tr><tr><td>Fully-connected</td><td>96.1</td><td>95.2</td><td>90.3</td><td>100</td><td>80.6</td><td>85.0</td><td>1.73</td><td>1.98</td><td>2.45</td><td>0.68</td><td>1.40</td><td>2.23</td></tr><tr><td>ego→nbrs</td><td>99.0</td><td>97.1</td><td>95.5</td><td>100</td><td>83.2</td><td>90.1</td><td>1.64</td><td>1.88</td><td>2.29</td><td>0.65</td><td>1.29</td><td>1.95</td></tr></table>

TABLE 13: Comparison of Diffusion and Flow-Matching across different datasets.
<table><tr><td rowspan="2">Strategies</td><td colspan="6">一 nuScenes</td><td colspan="4">一 Bench2Drive</td><td colspan="6">NAVSIMv1</td></tr><tr><td colspan="3">L2 (m)↓</td><td colspan="3">一 Col. Rate (%)↓</td><td colspan="3">DS↑ SR↑ Effi↑</td><td colspan="3">Comf↑ NC↑</td><td colspan="3">TTC↑ Comf↑</td></tr><tr><td></td><td>4s</td><td>5s</td><td>6s</td><td>4s</td><td>5s</td><td>6s</td><td></td><td></td><td></td><td></td><td></td><td>DAC↑</td><td></td><td></td><td>EP↑</td><td>PDMS↑</td></tr><tr><td>Diffusion</td><td>1.79</td><td>2.07</td><td>2.46</td><td>0.75</td><td>1.45</td><td>2.23</td><td>73.22</td><td>40.74</td><td>77.92</td><td>25.81</td><td>98.0</td><td>96.6</td><td>94.8</td><td>100</td><td>82.6</td><td>88.1</td></tr><tr><td>Flow-Matching</td><td>1.64</td><td>1.88</td><td>2.29</td><td>0.65</td><td>1.29</td><td>1.95</td><td>76.71</td><td>44.22</td><td>80.48</td><td>29.74</td><td>99.0</td><td>97.1</td><td>95.5</td><td>100</td><td>83.2</td><td>90.1</td></tr></table>

TABLE 14: Ablation study of different stages on the nuScenes set.
<table><tr><td rowspan="2">Stage</td><td colspan="3">L2 (m) ↓</td><td colspan="3">Col. Rate (%) ↓</td></tr><tr><td>4s</td><td>5s</td><td>6s</td><td>4s</td><td>5s</td><td>6s</td></tr><tr><td>One</td><td>1.68</td><td>1.96</td><td>2.40</td><td>0.68</td><td>1.35</td><td>2.04</td></tr><tr><td>Two</td><td>1.64</td><td>1.88</td><td>2.29</td><td>0.65</td><td>1.29</td><td>1.95</td></tr></table>

TABLE 15: Ablation study of neighbor selection strategies on the nuScenes validation set. The upper rows use distance-based selection, while the lower rows adopt Top-K neighbors. We use SparseDrive as the baseline.
<table><tr><td rowspan="2">H-Param</td><td colspan="3">L2 (m) ↓</td><td colspan="3">Col. Rate (%) ↓</td></tr><tr><td>4s</td><td>5s</td><td>6s</td><td>4s</td><td>5s</td><td>6s</td></tr><tr><td>5m</td><td>1.70</td><td>1.95</td><td>2.35</td><td>0.72</td><td>1.36</td><td>2.02</td></tr><tr><td>8m</td><td>1.68</td><td>1.91</td><td>2.33</td><td>0.68</td><td>1.33</td><td>1.98</td></tr><tr><td>10m</td><td>1.64</td><td>1.88</td><td>2.29</td><td>0.65</td><td>1.29</td><td>1.95</td></tr><tr><td>12m</td><td>1.65</td><td>1.90</td><td>2.31</td><td>0.67</td><td>1.32</td><td>1.96</td></tr><tr><td>15m</td><td>1.66</td><td>1.91</td><td>2.32</td><td>0.68</td><td>1.34</td><td>1.99</td></tr><tr><td></td><td>1.71</td><td>1.93</td><td>2.35</td><td>0.70</td><td>1.34</td><td>2.01</td></tr><tr><td>48</td><td>1.66</td><td>1.90</td><td>2.32</td><td>0.68</td><td>1.31</td><td>1.99</td></tr><tr><td>16</td><td>1.73</td><td>2.02</td><td>2.43</td><td>0.75</td><td>1.44</td><td>2.09</td></tr><tr><td>32</td><td>1.75</td><td>2.22</td><td>2.72</td><td>0.82</td><td>1.50</td><td>2.23</td></tr></table>

TABLE 16: Ablation study of different times on the nuScenes set.
<table><tr><td rowspan="2">Stage</td><td colspan="3">L2 (m) ↓</td><td colspan="3">Col. Rate (%) ↓</td></tr><tr><td>4s</td><td>5s</td><td>6s</td><td>4s</td><td>5s</td><td>6s</td></tr><tr><td>t + 1</td><td>1.64</td><td>1.88</td><td>2.29</td><td>0.65</td><td>1.29</td><td>1.95</td></tr><tr><td>t + 2</td><td>1.75</td><td>1.99</td><td>2.44</td><td>0.69</td><td>1.38</td><td>2.09</td></tr><tr><td>t + 3</td><td>1.81</td><td>2.06</td><td>2.57</td><td>0.74</td><td>1.47</td><td>2.26</td></tr></table>

TABLE 17: Ablation on sampling steps on NAVSIM.
<table><tr><td>Steps</td><td>NC↑</td><td>DAC↑</td><td>TTC↑</td><td>Comf.↑</td><td>EP↑</td><td>PDMS↑</td><td>FPS↑</td></tr><tr><td>1</td><td>98.6</td><td>96.7</td><td>94.9</td><td>100</td><td>82.4</td><td>88.3</td><td>51</td></tr><tr><td>2</td><td>99.0</td><td>97.1</td><td>95.5</td><td>100</td><td>83.2</td><td>90.1</td><td>51</td></tr><tr><td></td><td>99.1</td><td>97.2</td><td>95.6</td><td>100</td><td>83.3</td><td>89.2</td><td>46</td></tr><tr><td>34</td><td>99.1</td><td>97.2</td><td>95.7</td><td>100</td><td>83.3</td><td>89.3</td><td>42</td></tr></table>

TABLE 18: Ablation on solver choice on NAVSIM.
<table><tr><td>Solver</td><td>NC↑</td><td>DAC↑</td><td>TTC↑</td><td>Comf.↑</td><td>EP↑</td><td>PDMS↑</td><td>FPS↑</td></tr><tr><td>Euler</td><td>99.0</td><td>97.1</td><td>95.5</td><td>100</td><td>83.2</td><td>90.1</td><td>51</td></tr><tr><td>Heun</td><td>99.1</td><td>97.2</td><td>95.6</td><td>100</td><td>83.3</td><td>89.2</td><td>46</td></tr></table>

NAVSIMv2 navtest (Closed-Loop). Table 5 reports results on the NAVSIMv2 navtest split. While recent E2E-based and VLA-based methods achieve strong performance, Graph-World remains highly competitive and achieves the best overall performance with an EPDMS of 89.5. Compared with prior world-model-based methods, it slightly improves over Latent-WAM (89.3) while maintaining balanced performance across all metrics. Notably, GraphWorld achieves strong results on safety-critical and interaction-related metrics such as DAC and TTC, demonstrating robust decisionmaking in complex driving scenarios. Although some methods obtain higher scores on individual metrics, GraphWorld provides more consistent performance across safety, stability, and interaction dimensions. These results indicate that GraphWorld effectively captures multi-agent dynamics and enables reliable closed-loop planning.

Short-Horizon Planning on nuScenes (Open-Loop). Table 6 reports 3s open-loop planning results on nuScenes val. GraphWorld achieves competitive performance, with 0.57m average L2 error and a 0.08% collision rate, on par with SOTA methods.

Motion Results on NuScenes. In Table 7, GraphWorld achieves the best overall motion prediction performance on nuScenes, reducing minADE from 0.62 to 0.55 (11.3%) compared with SparseDrive. Although VAD yields the lowest miss rate, GraphWorld achieves the highest EPA, suggesting more interaction-aware multi-modal predictions.

## 5.5 Robustness Study

Adv-nuSc (Open-Loop). Table 8 reports robustness under adversarial driving scenarios. Compared to prior methods, GraphWorld consistently achieves the lowest collision rates across all horizons, reducing the average collision rate to 0.738%. These results demonstrate GraphWorld’s superior robustness and stability when facing aggressive and highly interactive driving behaviors.

NuScenes-C. We evaluate robustness on nuScenes-C [77], a corrupted benchmark derived from the nuScenes validation set with 27 corruption types at 5 severity levels. Focusing on three representative adverse-weather corruptions (Snow, Rain, and Fog) in the open-loop setting (Table 9), GraphWorld achieves the best overall robustness, yielding the lowest average collision rates of 0.17/0.16/0.17 under Snow/Rain/Fog, respectively, substantially improving over the SparseDrive baseline (Avg. 0.30/0.31/0.36). The advantage becomes more pronounced as the horizon increases, where GraphWorld maintains lower 3s collision rates (0.28/0.29/0.29) than all baselines, indicating stronger resistance to error accumulation under weather-induced perception degradation. Meanwhile, on the Clean split, GraphWorld remains competitive (Avg. 0.08) and achieves the best short-horizon safety (1s/2s: 0.00/0.04), suggesting that the robustness gains under corruptions are obtained without sacrificing performance in normal conditions.

Turning-nuScenes. We further evaluate planning robustness on Turning-nuScenes [4], a challenging subset of nuScenes curated to emphasize non-trivial turning maneuvers and trajectory temporal coherence. Unlike the original nuScenes validation set that is dominated by go-straight commands, Turning-nuScenes selects samples whose GT ego trajectory exhibits a large directional change, implemented via a 25 m displacement threshold between the GT positions at 0.5s and 3.0s. This yields a compact but difficult validation set with 680 samples across 17 scenes, specifically designed to stress-test planners under highcurvature, interaction-heavy motions. As shown in Table 10, GraphWorld achieves the lowest collision rate across all horizons and the best overall average (0.28), outperforming SparseDrive (Avg. 0.40), DiffusionDrive<sup>∗</sup> (Avg. 0.34), and MomAD (Avg. 0.32). Notably, the gain becomes increasingly significant at longer horizons, where GraphWorld reduces the 3s collision rate to 0.72 compared with 0.98/0.85/0.79 of the baselines, indicating stronger resistance to error accumulation in turning trajectories. These results suggest that explicitly modeling ego-centric interactions and maintaining temporally consistent world states benefits planning stability in turning-dominant scenarios, where one-shot prediction is more prone to drift and unstable control.

## 5.6 Ablation Study

Roles of Different Modules in GraphWorld. Table 11 shows that both ECIG and WSCP contribute consistently to performance improvements across all datasets. ECIG alone already improves both open-loop and closed-loop metrics, reducing long-horizon L2 errors and collision rates on nuScenes while increasing NAVSIMv1 PDMS and Bench2Drive scores. Further incorporating WSCP leads to the largest gains, achieving the best overall performance across all benchmarks. In particular, the full model attains the highest NAVSIMv1 PDMS (90.1) and significantly improves Bench2Drive DS and SR, demonstrating enhanced decision-making and stability. These results highlight the complementary roles of ECIG in interaction modeling and WSCP in world-state refinement.

Ablation on Different Graph Structures in ECIG. As shown in Table 12, the ego-centric star graph (ego→nbrs) consistently outperforms the fully-connected design across both NAVSIMv1 and nuScenes. It significantly improves NC from 96.1 to 99.0 and PDMS from 85.0 to 90.1, while also reducing long-horizon L2 errors and collision rates. These results suggest that focusing on ego-centered interactions effectively captures critical dependencies, while avoiding noisy neighbor–neighbor connections and improving overall stability.

Ablation on Diffusion vs. Flow-Matching. Table 13 compares Diffusion and Flow-Matching across multiple datasets. Flow-Matching consistently outperforms Diffusion in both open-loop and closed-loop settings. On nuScenes, it reduces long-horizon L2 errors from 1.79/2.07/2.46 to 1.64/1.88/2.29 and lowers collision rates from 0.75/1.45/2.23 to 0.65/1.29/1.95, with improvements maintained at longer horizons, indicating better stability against error accumulation. On Bench2Drive, it improves the driving score from 73.22 to 76.71 and success rate from 40.74% to 44.22%, while also enhancing efficiency and comfort, suggesting safer and smoother behaviors in interactive scenarios. On NAVSIMv1, Flow-Matching further improves all key metrics, including NC (98.0 → 99.0), DAC (96.6 → 97.1), and PDMS (88.1 → 90.1). These consistent gains across diverse benchmarks demonstrate that Flow-Matching provides stronger robustness and generalization for trajectory generation.

Ablation on Neighbor Selection in ECIG. Table 15 shows that an ego-centric, distance-based neighbor selection with a moderate radius (5m) achieves the best trade-off, reducing L2 error from 2.35m to 2.29m at 6s and collision rate from 2.02% to 1.95%. Both overly sparse and overly dense neighbor sets degrade long-horizon accuracy and safety.

Ablation on Training Stages for World-State Learning. Table 14 shows that introducing the second training stage consistently reduces long-horizon L2 errors and collision rates on nuScenes, indicating that explicit temporal supervision effectively improves the stability and quality of the learned world state.

Ablation Study of Different Times on the nuScenes Set. Table 16 investigates the impact of using different temporal stages (t+1, t+2, t+3) for long-horizon planning on nuScenes. We observe a clear trend that earlier stages consistently achieve better planning quality and safety. Specifically, t+1 yields the lowest L2 errors at all horizons (1.64/1.88/2.29 at {4s, 5s, 6s}) and the lowest collision rates (0.65/1.29/1.95), while performance gradually degrades as the stage shifts to t+2 and t+3. This degradation is more evident for longer horizons (e.g., 6s L2: 2.29 → 2.44 → 2.57; 6s collision: 1.95 → 2.09 → 2.26), indicating that laterstage rollouts suffer from increased uncertainty and error accumulation. Overall, these results suggest that leveraging earlier temporal information provides more accurate and safer trajectory generation for long-horizon planning.

![](images/3a4c13a07465219d0678acd1a9f3afe12a8aeb68b96e0a19f9caa011e413be2d.jpg)  
Fig. 4: Visualization of GraphWorld’s 6-second long-horizon planning on the nuScenes dataset.

![](images/998e78c76e110cea57fce8570e4069709cdeca6b734508b7a97b0d47b1216529.jpg)  
Fig. 5: The visualization of GraphWorld on NAVSIMv1 dataset.

Ablation on Sampling Steps. Table 17 shows that increasing sampling steps yields only marginal gains. PDMS improves slightly from 88.3 to 89.3, while performance largely saturates after 2 steps. In contrast, inference speed drops significantly (51 FPS to 42 FPS). Therefore, we adopt 2 steps as a better trade-off between accuracy and efficiency.

Ablation on Solver Choice. Table 18 shows that Heun provides only marginal improvements over Euler (e.g., PDMS: 90.1 → 89.2), while reducing inference speed (51

FPS to 46 FPS). This indicates that the learned dynamics are sufficiently smooth, making Euler a more efficient and practical choice.

## 5.7 Visualizations

Visualization of GraphWorld’s 6-second long-horizon planning on the nuScenes dataset. As shown in Fig. 4, on nuScenes we visualize 6-second long-horizon planning. GraphWorld produces longer-range and temporally coherent trajectories, maintaining stable headings and smooth curvature variations in complex segments such as turning maneuvers. This capability stems from the ECIG, which explicitly captures key relations between the ego vehicle and surrounding traffic participants, together with a consistent latent world state that encodes multi-agent dynamics, thereby providing more reliable conditioning information for 6-second planning.

Visualization of GraphWorld on NAVSIMv1 dataset. Using the official implementation of the representative latent world model approach World4Drive, we visualize its behavior on NAVSIMv1 and conduct a qualitative comparison, as shown in Fig. 5. The results show that GraphWorld maintains a more appropriate safety distance from leading vehicles, effectively reducing potential collision risks. Meanwhile, its generated trajectories are better constrained within drivable areas. Overall, GraphWorld demonstrates stronger long-horizon planning capability, enabling more stable and safety-aware decision-making over extended time horizons.

## 6 CONCLUSION

We propose GraphWorld, an end-to-end autonomous driving framework that enhances long-horizon planning via ego-centric latent world modeling. By combining an ECIG with WSCP module and a two-stage temporal supervision strategy, GraphWorld enables efficient, interaction-aware, and safety-oriented trajectory generation. Extensive experiments on both open-loop and closed-loop benchmarks demonstrate consistent improvements in long-horizon accuracy and collision reduction, validating the effectiveness of ego-centric relational world modeling for robust autonomous driving.

Limitations and Future Work. While GraphWorld improves long-horizon planning, it relies on fixed neighbor selection and single-step world-state prediction. Future work will explore adaptive graph evolution and multi-step world modeling for more complex scenarios.

## ACKNOWLEDGMENTS

This work was supported by the National Natural Science Foundation of China (NSFC) under Grants No. 62536001 (Key Program) and No. 62576026.

## REFERENCES

[1] L. Chen, P. Wu, K. Chitta, B. Jaeger, A. Geiger, and H. Li, “End-to-end autonomous driving: Challenges and frontiers,” IEEE Transactions on Pattern Analysis and Machine Intelligence, 2024.

[2] Z. Song, L. Liu, F. Jia, Y. Luo, C. Jia, G. Zhang, L. Yang, and L. Wang, “Robustness-aware 3d object detection in autonomous driving: A review and outlook,” IEEE Transactions on Intelligent Transportation Systems, pp. 1–30, 2024.

[3] Y. Hu, J. Yang, L. Chen, K. Li, C. Sima, X. Zhu, S. Chai, S. Du, T. Lin, W. Wang, L. Lu, X. Jia, Q. Liu, J. Dai, Y. Qiao, and H. Li, “Planning-oriented autonomous driving,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), June 2023, pp. 17 853– 17 862.

[4] Z. Song, C. Jia, L. Liu, H. Pan, Y. Zhang, J. Wang, X. Zhang, S. Xu, L. Yang, and Y. Luo, “Don’t shake the wheel: Momentum-aware planning in end-to-end autonomous driving,” in Proceedings of the Computer Vision and Pattern Recognition Conference, 2025, pp. 22 432–22 441.

[5] B. Jiang, S. Chen, Q. Xu, B. Liao, J. Chen, H. Zhou, Q. Zhang, W. Liu, C. Huang, and X. Wang, “Vad: Vectorized scene representation for efficient autonomous driving,” in Proceedings of the IEEE/CVF International Conference on Computer Vision, 2023, pp. 8340–8350.

[6] W. Sun, X. Lin, Y. Shi, C. Zhang, H. Wu, and S. Zheng, “Sparsedrive: End-to-end autonomous driving via sparse scene representation,” arXiv preprint arXiv:2405.19620, 2024.

[7] K. Chitta, A. Prakash, B. Jaeger, Z. Yu, K. Renz, and A. Geiger, “Transfuser: Imitation with transformer-based sensor fusion for autonomous driving,” IEEE Transactions

on Pattern Analysis and Machine Intelligence, vol. 45, no. 11, pp. 12 878–12 895, 2023.

[8] M. Guo, Z. Zhang, Y. He, K. Wang, L. Jing, and H. Ling, “End-to-end autonomous driving without costly modularization and 3d manual annotation,” IEEE Transactions on Pattern Analysis and Machine Intelligence, 2025.

[9] S. Chen, B. Jiang, H. Gao, B. Liao, Q. Xu, Q. Zhang, C. Huang, W. Liu, and X. Wang, “Vadv2: End-to-end vectorized autonomous driving via probabilistic planning,” arXiv preprint arXiv:2402.13243, 2024.

[10] B. Liao, S. Chen, H. Yin, B. Jiang, C. Wang, S. Yan, X. Zhang, X. Li, Y. Zhang, Q. Zhang et al., “Diffusiondrive: Truncated diffusion model for end-to-end autonomous driving,” arXiv preprint arXiv:2411.15139, 2024.

[11] Z. Song, L. Liu, H. Pan, B. Liao, M. Guo, L. Yang, Y. Zhang, S. Xu, C. Jia, and Y. Luo, “Breaking imitation bottlenecks: Reinforced diffusion powers diverse trajectory generation,” arXiv preprint arXiv:2507.04049, 2025.

[12] Z. Li, K. Li, S. Wang, S. Lan, Z. Yu, Y. Ji, Z. Li, Z. Zhu, J. Kautz, Z. Wu et al., “Hydra-mdp: End-to-end multimodal planning with multi-target hydra-distillation,” arXiv preprint arXiv:2406.06978, 2024.

[13] Z. Li, W. Yao, Z. Wang, X. Sun, J. Chen, N. Chang, M. Shen, Z. Wu, S. Lan, and J. M. Alvarez, “Generalized trajectory scoring for end-to-end multimodal planning,” arXiv preprint arXiv:2506.06664, 2025.

[14] Z. Xing, X. Zhang, Y. Hu, B. Jiang, T. He, Q. Zhang, X. Long, and W. Yin, “Goalflow: Goal-driven flow matching for multimodal trajectories generation in end-to-end autonomous driving,” in Proceedings of the Computer Vision and Pattern Recognition Conference, 2025, pp. 1602–1611.

[15] B. Sun, Y. Cao, Y. Wang, R. Wang, J. Shang, X. Feng, J. Lu, J. Shi, S. Yang, X. Yan et al., “Minddrive: An all-in-one framework bridging world models and vision-language model for end-to-end autonomous driving,” arXiv preprint arXiv:2512.04441, 2025.

[16] L. Liu, C. Jia, G. Yu, Z. Song, J. Li, F. Jia, P. Wu, X. Hao, and Y. Luo, “Guideflow: Constraint-guided flow matching for planning in end-to-end autonomous driving,” arXiv preprint arXiv:2511.18729, 2025.

[17] T. Feng, W. Wang, and Y. Yang, “A survey of world models for autonomous driving,” arXiv preprint arXiv:2501.11260, 2025.

[18] J. Ding, Y. Zhang, Y. Shang, Y. Zhang, Z. Zong, J. Feng, Y. Yuan, H. Su, N. Li, N. Sukiennik et al., “Understanding world or predicting future? a comprehensive survey of world models,” ACM Computing Surveys, vol. 58, no. 3, pp. 1–38, 2025.

[19] F. Jia, C. Jia, Z. Song, Z. Bao, L. Liu, S. Xu, Y. Gong, L. Yang, X. Zhang, B. Sun et al., “Progressive robustnessaware world models in autonomous driving: A review and outlook,” Authorea Preprints, 2025.

[20] S. Gao, J. Yang, L. Chen, K. Chitta, Y. Qiu, A. Geiger, J. Zhang, and H. Li, “Vista: A generalizable driving world model with high fidelity and versatile controllability,” Advances in Neural Information Processing Systems, vol. 37, pp. 91 560–91 596, 2024.

[21] A. Hu, L. Russell, H. Yeo, Z. Murez, G. Fedoseev, A. Kendall, J. Shotton, and G. Corrado, “Gaia-1: A generative world model for autonomous driving,” arXiv preprint arXiv:2309.17080, 2023.

[22] X. Wang, Z. Zhu, G. Huang, X. Chen, J. Zhu, and J. Lu, “Drivedreamer: Towards real-world-drive world models for autonomous driving,” in European Conference on Computer Vision. Springer, 2024, pp. 55–72.

[23] Y. Wang, J. He, L. Fan, H. Li, Y. Chen, and Z. Zhang, “Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2024, pp. 14 749–14 759.

[24] Y. Li, Y. Wang, Y. Liu, J. He, L. Fan, and Z. Zhang, “Endto-end driving with online trajectory evaluation via bev world model,” arXiv preprint arXiv:2504.01941, 2025.

[25] Y. Li, L. Fan, J. He, Y. Wang, Y. Chen, Z. Zhang, and T. Tan, “Enhancing end-to-end autonomous driving with latent world model,” arXiv preprint arXiv:2406.08481, 2024.

[26] Y. Zheng, P. Yang, Z. Xing, Q. Zhang, Y. Zheng, Y. Gao, P. Li, T. Zhang, Z. Xia, P. Jia et al., “World4drive: Endto-end autonomous driving via intention-aware physical latent world model,” in Proceedings of the IEEE/CVF International Conference on Computer Vision, 2025, pp. 28 632– 28 642.

[27] D. Xu, H. Li, Q. Wang, Z. Song, L. Chen, and H. Deng, “M2da: Multi-modal fusion transformer incorporating driver attention for autonomous driving,” arXiv preprint arXiv:2403.12552, 2024.

[28] Y. Liu, W. Chen, Y. Bai, X. Liang, G. Li, W. Gao, and L. Lin, “Aligning cyber space with physical world: A comprehensive survey on embodied ai,” arXiv preprint arXiv:2407.06886, 2024.

[29] D. Ha and J. Schmidhuber, “Recurrent world models facilitate policy evolution,” Advances in neural information processing systems, vol. 31, 2018.

[30] M. Lin, X. Wang, Y. Wang, S. Wang, F. Dai, P. Ding, C. Wang, Z. Zuo, N. Sang, S. Huang et al., “Exploring the evolution of physics cognition in video generation: A survey,” arXiv preprint arXiv:2503.21765, 2025.

[31] D. Liu, J. Zhang, A.-D. Dinh, E. Park, S. Zhang, A. Mian, M. Shah, and C. Xu, “Generative physical ai in vision: A survey,” arXiv preprint arXiv:2501.10928, 2025.

[32] Y. LeCun, “A path towards autonomous machine intelligence version 0.9. 2, 2022-06-27,” Open Review, vol. 62, no. 1, pp. 1–62, 2022.

[33] Y. Guan, H. Liao, Z. Li, J. Hu, R. Yuan, G. Zhang, and C. Xu, “World models for autonomous driving: An initial survey,” IEEE Transactions on Intelligent Vehicles, 2024.

[34] D. Liang, D. Zhang, X. Zhou, S. Tu, T. Feng, X. Li, Y. Zhang, M. Du, X. Tan, and X. Bai, “Seeing the future, perceiving the future: A unified driving world model for future generation and perception,” arXiv preprint arXiv:2503.13587, 2025.

[35] K. Zhang, Z. Tang, X. Hu, X. Pan, X. Guo, Y. Liu, J. Huang, L. Yuan, Q. Zhang, X.-X. Long et al., “Epona: Autoregressive diffusion world model for autonomous driving,” arXiv preprint arXiv:2506.24113, 2025.

[36] C. Shi, S. Shi, K. Sheng, B. Zhang, and L. Jiang, “Drivex: Omni scene modeling for learning generalizable world knowledge in autonomous driving,” in Proceedings of the IEEE/CVF International Conference on Computer Vision, 2025, pp. 28 599–28 609.

[37] A. B. Vasudevan, N. Peri, J. Schneider, and D. Ramanan, “Planning with adaptive world models for autonomous driving,” arXiv preprint arXiv:2406.10714, 2024.

[38] G. Qiao, G. Quan, R. Qu, and G. Liu, “Modelling competitive behaviors in autonomous driving under generative world model,” in European Conference on Computer Vision. Springer, 2024, pp. 19–36.

[39] A. Hu, G. Corrado, N. Griffiths, Z. Murez, C. Gurau, H. Yeo, A. Kendall, R. Cipolla, and J. Shotton, “Modelbased imitation learning for urban driving,” Advances in Neural Information Processing Systems, vol. 35, pp. 20 703– 20 716, 2022.

[40] Y. Li, Y. Wang, Y. Liu, J. He, L. Fan, and Z. Zhang, “Endto-end driving with online trajectory evaluation via bev world model,” arXiv preprint arXiv:2504.01941, 2025.

[41] Y. Li, L. Fan, J. He, Y. Wang, Y. Chen, Z. Zhang, and T. Tan, “Enhancing end-to-end autonomous driving with latent world model,” arXiv preprint arXiv:2406.08481, 2024.

[42] Y. Lipman, R. T. Chen, H. Ben-Hamu, M. Nickel, and M. Le, “Flow matching for generative modeling,” arXiv

preprint arXiv:2210.02747, 2022.

[43] X. Jia, P. Wu, L. Chen, J. Xie, C. He, J. Yan, and H. Li, “Think twice before driving: Towards scalable decoders for end-to-end autonomous driving,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), June 2023, pp. 21 983–21 994.

[44] X. Jia, Y. Gao, L. Chen, J. Yan, P. L. Liu, and H. Li, “Driveadapter: Breaking the coupling barrier of perception and planning in end-to-end autonomous driving,” in Proceedings of the IEEE/CVF International Conference on Computer Vision, 2023, pp. 7953–7963.

[45] S. Shang, Y. Chen, Y. Wang, Y. Li, and Z. Zhang, “Drivedpo: Policy learning via safety dpo for end-toend autonomous driving,” arXiv preprint arXiv:2509.17940, 2025.

[46] Z. Yang, X. Jia, Q. Li, X. Yang, M. Yao, and J. Yan, “Raw2drive: Reinforcement learning with aligned world models for end-to-end autonomous driving (in carla v2),” arXiv preprint arXiv:2505.16394, 2025.

[47] X. Jia, J. You, Z. Zhang, and J. Yan, “Drivetransformer: Unified transformer for scalable end-to-end autonomous driving,” arXiv preprint arXiv:2503.07656, 2025.

[48] W. Zheng, R. Song, X. Guo, and L. Chen, “Genad: Generative end-to-end autonomous driving,” arXiv preprint arXiv:2402.11502, 2024.

[49] X. Weng, B. Ivanovic, Y. Wang, Y. Wang, and M. Pavone, “Para-drive: Parallelized architecture for real-time autonomous driving,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2024, pp. 15 449–15 458.

[50] C. Yuan, Z. Zhang, J. Sun, S. Sun, Z. Huang, C. D. W. Lee, D. Li, Y. Han, A. Wong, K. P. Tee et al., “Drama: An efficient end-to-end motion planner for autonomous driving with mamba,” arXiv preprint arXiv:2408.03601, 2024.

[51] L. Liu, C. Jia, Z. Song, H. Pan, B. Liao, W. Sun, Y. Zhang, L. Yang, and Y. Luo, “Fully unified motion planning for end-to-end autonomous driving,” arXiv preprint arXiv:2504.12667, 2025.

[52] W. Yao, Z. Li, S. Lan, Z. Wang, X. Sun, J. M. Alvarez, and Z. Wu, “Drivesuprim: Towards precise trajectory selection for end-to-end planning,” arXiv preprint arXiv:2506.06659, 2025.

[53] Y. Li, K. Xiong, X. Guo, F. Li, S. Yan, G. Xu, L. Zhou, L. Chen, H. Sun, B. Wang et al., “Recogdrive: A reinforced cognitive framework for end-to-end autonomous driving,” arXiv preprint arXiv:2506.08052, 2025.

[54] Z. Zhou, T. Cai, S. Z. Zhao, Y. Zhang, Z. Huang, B. Zhou, and J. Ma, “Autovla: A vision-language-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning,” arXiv preprint arXiv:2506.13757, 2025.

[55] Y. Li, S. Shang, W. Liu, B. Zhan, H. Wang, Y. Wang, Y. Chen, X. Wang, Y. An, C. Tang et al., “Drivevla-w0: World models amplify data scaling law in autonomous driving,” arXiv preprint arXiv:2510.12796, 2025.

[56] L. Liu, Z. Song, C. Jia, H. Ye, X. Hao, L. Chen et al., “Driveworld-vla: Unified latent-space world modeling with vision-language-action for autonomous driving, arXiv preprint arXiv:2602.06521, 2026.

[57] Y. Chen, Y. Wang, and Z. Zhang, “Drivinggpt: Unifying driving world modeling and planning with multimodal autoregressive transformers,” in Proceedings of the IEEE/CVF International Conference on Computer Vision, 2025, pp. 26 890–26 900.

[58] J. Yang, K. Chitta, S. Gao, L. Chen, Y. Shao, X. Jia, H. Li, A. Geiger, X. Yue, and L. Chen, “Resim: Reliable world simulation for autonomous driving,” Advances in Neural Information Processing Systems, vol. 38, pp. 167 710–167 741, 2026.

[59] I. Georgiev, V. Giridhar, N. Hansen, and A. Garg, “Pwm:

Policy learning with multi-task world models,” in International Conference on Learning Representations, vol. 2025, 2025, pp. 13 737–13 757.

[60] P. Yang, B. Lu, Z. Xia, C. Han, Y. Gao, T. Zhang, K. Zhan, X. Lang, Y. Zheng, and Q. Zhang, “Worldrft: Latent world model planning with reinforcement fine-tuning for autonomous driving,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 40, no. 14, 2026, pp. 11 649– 11 657.

[61] T. Xia, Y. Li, L. Zhou, J. Yao, K. Xiong, H. Sun, B. Wang, K. Ma, G. Chen, H. Ye et al., “Drivelaw: Unifying planning and video generation in a latent driving world,” arXiv preprint arXiv:2512.23421, 2025.

[62] W. Cao, M. Hallgarten, T. Li, D. Dauner, X. Gu, C. Wang, Y. Miron, M. Aiello, H. Li, I. Gilitschenski et al., “Pseudo-simulation for autonomous driving,” arXiv preprint arXiv:2506.04218, 2025.

[63] Z. Zhou, R. Yang, Y. Guo, S. X. Chen, T. Feng, K. Pistunova, Y. Shen, L. Su, J. Ma et al., “Spanvla: Efficient action bridging and learning from negative-recovery samples for vision-language-action model,” arXiv preprint arXiv:2604.19710, 2026.

[64] A. Jiang, Y. Gao, Z. Sun, Y. Wang, J. Wang, J. Chai, Q. Cao, Y. Heng, H. Jiang, Y. Dong et al., “Diffvla: Vision-language guided diffusion planning for autonomous driving,” arXiv preprint arXiv:2505.19381, 2025.

[65] K. Li, Z. Li, S. Lan, Y. Xie, Z. Zhang, J. Liu, Z. Wu, Z. Yu, and J. M. Alvarez, “Hydra-mdp++: Advancing end-toend driving via expert-guided hydra-distillation,” arXiv preprint arXiv:2503.12820, 2025.

[66] J. Zou, S. Chen, B. Liao, Z. Zheng, Y. Song, L. Zhang, Q. Zhang, W. Liu, and X. Wang, “Diffusiondrivev2: Reinforcement learning-constrained truncated diffusion modeling in end-to-end autonomous driving,” arXiv preprint arXiv:2512.07745, 2025.

[67] L. Wang, Y. Zheng, Q. Chen, S. Li, Y. Zhang, Z. Xing, Q. Zhang, X. Li, D. Qian et al., “Latent-wam: Latent world action modeling for end-to-end autonomous driving,” arXiv preprint arXiv:2603.24581, 2026.

[68] B. Sun, B. Zhang, J. Lu, X. Feng, J. Shang, R. Cao, M. Zheng, C. Wang, S. Yang, Y. Cao et al., “Focalad: Local motion planning for end-to-end autonomous driving,” arXiv preprint arXiv:2506.11419, 2025.

[69] W. Zheng, W. Chen, Y. Huang, B. Zhang, Y. Duan, and J. Lu, “Occworld: Learning a 3d occupancy world model for autonomous driving,” in European conference on computer vision. Springer, 2024, pp. 55–72.

[70] P. Li and D. Cui, “Navigation-guided sparse scene representation for end-to-end autonomous driving,” in International Conference on Learning Representations (ICLR), 2025.

[71] X. Jia, Z. Yang, Q. Li, Z. Zhang, and J. Yan, “Bench2drive: Towards multi-ability benchmarking of closed-loop end-to-end autonomous driving,” arXiv preprint arXiv:2406.03877, 2024.

[72] A. Dosovitskiy, G. Ros, F. Codevilla, A. Lopez, and V. Koltun, “CARLA: An open urban driving simulator,” in Proceedings of the 1st Annual Conference on Robot Learning, ser. Proceedings of Machine Learning Research, S. Levine, V. Vanhoucke, and K. Goldberg, Eds., vol. 78. PMLR, 13–15 Nov 2017, pp. 1–16. [Online]. Available: https://proceedings.mlr.press/v78/dosovitskiy17a.html

[73] D. Dauner, M. Hallgarten, T. Li, X. Weng, Z. Huang, Z. Yang, H. Li, I. Gilitschenski, B. Ivanovic, M. Pavone et al., “Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking,” Advances in Neural Information Processing Systems, vol. 37, pp. 28 706–28 719, 2024.

[74] H. Caesar, J. Kabzan, K. S. Tan, W. K. Fong, E. Wolff, A. Lang, L. Fletcher, O. Beijbom, and S. Omari, “nuplan: A closed-loop ml-based planning benchmark for au-

tonomous vehicles,” arXiv preprint arXiv:2106.11810, 2021.

[75] H. Caesar, V. Bankiti, A. H. Lang, S. Vora, V. E. Liong, Q. Xu, A. Krishnan, Y. Pan, G. Baldan, and O. Beijbom, “nuscenes: A multimodal dataset for autonomous driving,” in Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 2020, pp. 11 621–11 631.

[76] Z. Xu, B. Li, H.-a. Gao, M. Gao, Y. Chen, M. Liu, C. Yan, H. Zhao, S. Feng, and H. Zhao, “Challenger: Affordable adversarial driving video generation,” arXiv preprint arXiv:2505.15880, 2025.

[77] Y. Dong, C. Kang, J. Zhang, Z. Zhu, Y. Wang, X. Yang, H. Su, X. Wei, and J. Zhu, “Benchmarking robustness of 3d object detection to common corruptions,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), June 2023, pp. 1022–1032.

[78] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2016, pp. 770–778.

![](images/1016db329fb1823c404695f7ff449e79842a36e7f6126d1e2a3338ba65f7e0d6.jpg)

Ziying Song received the B.S. degree from Hebei Normal University of Science and Technology, China, in 2019, the M.S. degree from Hebei University of Science and Technology, China, in 2022, and the Ph.D. degree in computer science and technology from Beijing Jiaotong University, China, in March 2026. He is currently an Assistant Professor with the School of Artificial Intelligence, Yanshan University, China. His research interests include autonomous driving, end-to-end autonomous driving, world models, embodied intelligence, and VLA models.

![](images/1b4b7afe562074a5b419c45321548bf44e5b302ee6abe665432ef481944836fb.jpg)

Caiyan Jia received the B.S. degree in mathematics from Ningxia University in 1998, the M.S. degree in computational mathematics from Xiangtan University in 2001, and the Ph.D. degree in engineering from the Institute of Computing Technology, Chinese Academy of Sciences, in 2004. She is currently a Professor with the School of Computer Science and Technology, Beijing Jiaotong University, Beijing, China.

![](images/0d7d2f8af68269e1b5b03d84d268122cd3831cd4bdcbe1ee66132a2557841ffb.jpg)

Lin Liu was born in Jinzhou, Liaoning Province, in 2001. He received his bachelor’s degree from China University of Geosciences, Beijing in 2023, and is currently pursuing his master’s degree in Computer Science and Technology at Beijing Jiaotong University. Starting in September 2026, he will join Dalian University of Technology as a Ph.D. student, focusing his research on Embodied AI and Autonomous Driving.

![](images/69b678d0c4c415e08746895111b67bb1efe8474e2f9df6300b3470374b82a5f9.jpg)

Lei Yang (Member, IEEE) received the M.S. degree from the Robotics Institute, Beihang University, China, in 2018, and the Ph.D. degree from the School of Vehicle and Mobility, Tsinghua University, China, in 2024. From 2018 to 2020, he joined the Autonomous Driving R&D Department of JD.COM as an algorithm researcher. Currently, he is a research fellow with the School of Mechanical and Aerospace Engineering, Nanyang Technological University, Singapore. His current research interests include

autonomous driving, 3D scene understanding and world model.

![](images/a444277dec09b198d0a888093e93dbde9e96cfd3a32cf1abb97a4b9688e14984.jpg)

Shengkai Zhang studied for the B.S. degree in Computer Science and Technology at Hebei University, China, from 2022 to 2026. Since 2026, he has been pursuing the M.S. degree in Computer Science and Technology at Beijing Jiaotong University, China. His research interests include computer vision.

![](images/51269fc35b3a9322be827faa53ccbc0b03d25d3b21677b641e15682089ba425e.jpg)

![](images/d3c208c4d9653f62c77f36d7397d2b8918cf450d7378311894eaeeefe0984ffd.jpg)

Feiyang Jia was born in Yinchuan, Ningxia Province, China, in 1998. He received his B.S. degree from Beijing Jiaotong University (China) in 2020. He received a master’s degree from Beijing Technology and Business University (China) in 2023. He is now a Ph.D. student majoring in Computer Science and Technology at Beijing Jiaotong University (China), with research focus on Computer Vision.

![](images/d2c1edefd6d63ca917a88cb0a8fdcf4ec691e1725edd64af692ee831b8975693.jpg)

Fengda Zhao was born in March 1976, received his Ph.D. in Computer Software and Theory from Yanshan University. He is currently the Dean of the School of Artificial Intelligence at Yanshan University, where he also serves as a Professor and Ph.D. Supervisor. He holds additional positions as a Hebei Provincial Teaching Master, Vice Chairman of the Hebei Machine Learning Society, and a Senior Member of the China Computer Federation. His research interests include artificial intelligence applications, natural human-computer interaction, and intelligent robotics.

IEEE T-VT, and IEEE T-IV.

![](images/757d07d6d69c9adf1bc9c96e51482224dd677b680d7991382f85f28bf91faa70.jpg)

![](images/2c1ff0603434e3911747efb5d6afbe1bd258b478255fa487551febf992aa622a.jpg)

![](images/acf1eaae3308109ef64444961f62bf648dc26e22224689114f3c3a9c04cd9719.jpg)

Peiliang Wu received the B.Sc. and Ph.D. degrees from Yanshan University, Qinhuangdao, China, in 2004 and 2010, respectively. He is currently a Professor and Doctor Advisor with Yanshan University. He is a Member of the Academic Committee of Yanshan University, Member of the Standing Committee of the Youth Work Committee of the Chinese Artificial Intelligence Society, and the Vice Chairman of ACM Qinhuangdao. His research interests include robot learning and multi-agent systems.

Yadan Luo (Member, IEEE) received the BS degree in computer science from the University of Electronic Science and Technology of China, and the PhD degree from the University of Queensland. Her research interests include machine learning, computer vision, and multimedia data analysis. She is now a senior lecturer and ARC DECRA at the University of Queensland.

Shaoqing Xu received his M.S. degree in transportation engineering from the School of Transportation Science and Engineering in Beihang University. He is currently working toward the Ph.D. degree in electromechanical engineering with the State Key Laboratory of Internet of Things for Smart City, University of Macau, Macao SAR, China. His research interests include 3D Space Intelligence, End2End, World-Model, VLA, and its applications in Autonomous Driving and Robotics.

Chen Lv (Senior Member, IEEE) received the Ph.D. degree from Tsinghua University, China, in 2016. He is currently a Nanyang Associate Professor at Nanyang Technological University, Singapore, and Cluster Director of Future Mobility Solutions. His research interests include intelligent vehicles, automated driving, human–machine systems, and cyber-physical systems. He has authored two books, published over 100 papers, and holds 12 granted patents. He serves as an Associate Editor for IEEE T-ITS,