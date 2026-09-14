# Future-Aware End-to-End Driving: Bidirectional Modeling of Trajectory Planning and Scene Evolution

Bozhou Zhang<sup>1,2</sup>, Nan Song<sup>1,2</sup>, Jingyu Li<sup>1,2</sup>, Xiatian Zhu<sup>3</sup>\*, Jiankang Deng<sup>4</sup>, Li Zhang<sup>1,2</sup>\*

<sup>1</sup>School of Data Science, Fudan University <sup>2</sup>Shanghai Innovation Institute

<sup>3</sup>University of Surrey <sup>4</sup>Imperial College London

https://github.com/LogosRoboticsGroup/SeerDrive

## Abstract

End-to-end autonomous driving methods aim to directly map raw sensor inputs to future driving actions such as planned trajectories, bypassing traditional modular pipelines. While these approaches have shown promise, they often operate under a one-shot paradigm that relies heavily on the current scene context, potentially underestimating the importance of scene dynamics and their temporal evolution. This limitation restricts the model’s ability to make informed and adaptive decisions in complex driving scenarios. We propose a new perspective: the future trajectory of an autonomous vehicle is closely intertwined with the evolving dynamics of its environment, and conversely, the vehicle’s own future states can influence how the surrounding scene unfolds. Motivated by this bidirectional relationship, we introduce SeerDrive, a novel end-to-end framework that jointly models future scene evolution and trajectory planning in a closed-loop manner. Our method first predicts future bird’s-eye view (BEV) representations to anticipate the dynamics of the surrounding scene, then leverages this foresight to generate future-context-aware trajectories. Two key components enable this: (1) future-aware planning, which injects predicted BEV features into the trajectory planner, and (2) iterative scene modeling and vehicle planning, which refines both future scene prediction and trajectory generation through collaborative optimization. Extensive experiments on the NAVSIM and nuScenes benchmarks show that SeerDrive significantly outperforms existing state-of-the-art methods.

## 1 Introduction

End-to-end autonomous driving [1] has emerged as a promising paradigm by jointly learning perception [2, 3, 4], prediction [5, 6, 7, 8], and planning [9, 10, 11] in a unified framework. Compared to traditional modular pipelines, this approach simplifies system design and enables planning-oriented optimization through holistic training. Recent advances [12, 13, 14, 15, 16] have demonstrated that directly generating future trajectories from raw sensor inputs can achieve strong performance, highlighting the potential of end-to-end methods for building scalable and efficient driving systems. These methods have been widely evaluated in both open-loop [17] and closed-loop [18] settings, across real-world datasets [19] and simulation platforms [20].

Despite these successes, most existing methods adopt a one-shot paradigm, in which sensor observations, typically from the current time step, are used to directly predict a trajectory several seconds into the future. In this setup, the model must rely heavily on the scene’s current situation to infer the ego vehicle’s future motion (Figure 1(a)). While effective in structured environments, this approach tends to underestimate the importance ofhow the scene may evolve over time, a crucial factor in dynamic and interactive driving contexts. Furthermore, the ego vehicle’s ownfuture actions can significantly influence how the surrounding scene unfolds. These two aspects, the future scene and the agent’s future behavior, are inherently coupled and should be modeled together. However, this bidirectional dependency remains underexplored in current end-to-end systems.

![](images/131e0944fb7413b46a7da6d7fd92ba8866a596601585e44fb3c19cc1d9e2ea4b.jpg)  
Figure 1: Paradigm comparison. (a) Prior end-to-end methods follow a one-shot paradigm, directly mapping sensor inputs to planned trajectories based only on the current scene. (b) In contrast, Seer-Drive predicts scene evolution with a world model and plans trajectories with a planning model, enabling iterative interaction between the two in a closed-loop process.

To address this gap, we draw inspiration from the emerging concept of world models, which offer the ability to learn environment dynamics and simulate future observations. We propose to leverage this capability not only to foresee how the driving scene will change, but also to coordinate it with the ego vehicle’s planned actions through mutual interaction.

In this paper, we present SeerDrive, a novel end-to-end driving framework that introduces a paradigm shift by explicitly modeling the bidirectional relationship between scene evolution and trajectory planning (Figure 1(b)). To implement this paradigm, we design two key components. Future-Aware Planning injects predicted future bird’s-eye view (BEV) features into the planner, enabling trajectory generation informed by both current perception and anticipated dynamics. Iterative Scene Modeling and Vehicle Planning refines both the predicted scene and the planned trajectory through mutual feedback, supporting adaptive and temporally consistent decision-making. Together, these components enable context-aware planning in complex, dynamic environments.

Our contributions are threefold. (I) We propose a new paradigm for end-to-end driving that explicitly captures the bidirectional interaction between scene dynamics and the ego vehicle’s future actions, challenging the conventional one-shot planning approach. (II) We instantiate this paradigm through a unified framework, SeerDrive, which jointly models future BEV scene representations and vehicle trajectories through future-aware and iterative interaction mechanisms. (III) We conduct extensive experiments on both the NAVSIM and nuScenes benchmarks, demonstrating that SeerDrive achieves state-of-the-art performance and validates the effectiveness of our proposed design.

## 2 Related work

End-to-end autonomous driving. End-to-end autonomous driving [12, 13, 14, 15] has attracted increasing attention, as it contrasts with traditional modular methods by integrating perception [2, 4], prediction [5, 7], and planning [9, 11] into a unified, differentiable framework that enables end-to-end optimization. Early methods [21, 22, 23, 24] often bypass intermediate tasks and directly infer planning trajectories or actions from sensor data, both in open-loop [17] and closed-loop [20] settings. UniAD [12] unifies perception, prediction, and planning into a differentiable framework and leverages a transformer architecture to optimize the entire pipeline in a planning-oriented manner, achieving strong performance across all tasks. VAD [13] adopts a vectorized representation to improve the efficiency of the end-to-end pipeline. VADv2 [25] introduces a probabilistic planning paradigm with a large vocabulary and demonstrates impressive performance in closed-loop settings. SparseDrive [14] leverages a sparse scene representation to make better use of temporal information. Several other studies [26, 27] explore self-supervised learning to simplify the complex end-to-end pipeline.

Recent efforts have focused increasingly on more challenging end-to-end planning benchmarks [18, 19]. DiffusionDrive [15] proposes a truncated diffusion policy to achieve more accurate and diverse planning. GoalFlow [28] incorporates flow matching and goal-point guidance into end-to-end autonomous driving. DriveTransformer [16] investigates the scaling law within a unified transformerbased architecture. Different from previous methods that focus solely on improving the planning process itself, our approach aims to jointly optimize future world modeling and planning in an adaptive manner to achieve better planning performance.

World model in autonomous driving. World models aim to predict future scene dynamics conditioned on the current environment and ego state. Some studies [29, 30, 31] address world modeling by training models to generate realistic videos that are consistent with physical principles. Drive-Dreamer [32] employs a latent diffusion model guided by 3D boxes, HD maps, and ego states, and introduces an additional decoder for future action prediction. Drive-WM [33] generalizes this setup to multi-camera inputs and explores its application in the end-to-end planning task. Some other methods explore improving the generalization of dynamic world modeling by scaling up both data and model architecture. GAIA-1 [34] models token sequences using an autoregressive transformer conditioned on past states, followed by a diffusion-based decoder for realistic video synthesis. Vista [35] is trained on diverse web-collected driving videos and utilizes latent diffusion to produce high-resolution, long-horizon video outputs.

In contrast to methods that focus on generating complex and realistic images, some approaches generate driving scenes in the bird’s-eye view. SLEDGE [36] introduces the first generative simulator designed for agent motion planning. GUMP [37] builds upon generative modeling to capture dynamic traffic interactions, enabling diverse and realistic future scenario simulations. UMGen [38] generates ego-centric, multimodal driving scenes in an autoregressive, frame-by-frame manner. Scenario Dreamer [39] employs a vectorized latent diffusion model that directly operates on structured scene elements, coupled with an autoregressive Transformer for simulating agent behaviors in a data-driven way. Following the simplicity and structured nature of BEV, we likewise adopt it for modeling future scene evolution.

Joint world modeling and planning. Several works [27, 40, 41, 42, 43] explore joint modeling and collaborative optimization of world models and planning models, employing various strategies. In the field of autonomous driving, some works extend the world model by introducing an action token. OccWorld [44] employs an occupancy-based representation and jointly generates future occupancy and ego actions in an autoregressive manner. Drive-OccWorld [45] further extends this pipeline to operate directly from images, enabling 4D occupancy forecasting and planning. In contrast, some works start from the end-to-end autonomous driving pipeline and aim to enhance planning through world modeling. Existing methods either leverage world modeling as an additional supervision signal during training [26, 27], or use it to assist in selecting the best trajectory among multiple candidates [43]. Our approach conducts an in-depth exploration of world modeling and end-to-end planning design, enabling deep interaction between the two processes and significantly improving planning performance.

## 3 Methodology

## 3.1 Preliminary

Task formulation. End-to-end autonomous driving maps sensor inputs (e.g., camera and LiDAR) to future ego trajectories, often using multi-modal outputs to capture diverse possible futures. Auxiliary tasks like detection, map segmentation, and agent motion prediction are commonly integrated to enhance scene understanding and support safer planning. World models in autonomous driving aim to predict future scene evolution based on current observations, enabling agents to simulate and evaluate future outcomes. They offer structured representations of the environment, which help improve planning accuracy and decision reliability.

![](images/5c5f8cff02411a19251cd534d5c2d9e5d27157ff5d67006753c3b5a925e369f0.jpg)

（a) SeerDrive pipeline  
![](images/3efdf8eb7ffe2bc64ec65c095f4f9671fcdf27ada668b91af2ae10a9fc5ddd3a.jpg)  
(b) Future-aware End-to-end Planning Network  
Figure 2: Overview of SeerDrive. (a) Multi-view images and LiDAR inputs are encoded to obtain the current BEV feature, while ego status is encoded to produce the current ego feature. These are then used to predict the future BEV feature. All three types of features are subsequently used for trajectory planning. (b) The end-to-end planning network generates future trajectories based on the current ego feature, current BEV feature, and future BEV feature. (c) The BEV world modeling network and the end-to-end planning network operate iteratively, updating the current ego feature to progressively improve planning performance.

Framework overview. As illustrated in Figure 2, the SeerDrive framework consists of two key components. (a) shows the overall pipeline, where multi-view images and LiDAR inputs are fused to obtain the current BEV feature, and the ego status is encoded as the current ego feature. These features are fed into the BEV world modeling and end-to-end planning networks, which operate iteratively to predict the future BEV map and generate planned trajectories. (b) details the end-to-end planning network, which incorporates the future BEV feature—produced by the world modeling network—to enhance trajectory planning. (c) depicts the iterative interaction between world modeling and planning, enabling gradual refinement and improved planning performance.

## 3.2 Feature encoding

As illustrated in Figure 2 (a), multiple types of features are encoded. Given multi-view images I, and LiDAR features ${ \mathcal P } ,$ , the encoder transforms these multi-modal sensor inputs into a current BEV feature map $F _ { \mathrm { b e v } } ^ { \mathrm { c u r r } } \in \mathbb { R } ^ { \mathit { H } \times W \times C }$ , where H and W are the spatial dimensions of the BEV feature, and C is the number of feature channels. Following prior works [15, 43, 46], we adopt TransFuser [21] to obtain a unified BEV representation. Subsequently, a lightweight BEV decoder is employed to generate the current BEV semantic map $B _ { \mathrm { c u r r } }$ for supervision. Following prior works [14, 15, 43], the anchored multi-modal trajectories $\dot { \tau }$ and ego status $\mathcal { E }$ are encoded with a simple multi-layer perceptron (MLP) encoder to produce the multi-modal ego feature $F _ { \mathrm { e g o } } ^ { \mathrm { c u r r } } \in \mathbb { R } ^ { M \times C }$ , where M denotes the number of trajectory modes. The process is shown below:

$$
\begin{array} { r l } & { F _ { \mathrm { b e v } } ^ { \mathrm { c u r r } } = \mathrm { T r a n s F u s e r } ( \mathcal { T } , \mathcal { P } ) , } \\ & { F _ { \mathrm { e g o } } ^ { \mathrm { c u r r } } = \mathrm { E g o E n c o d e r } ( \mathcal { T } , \mathcal { E } ) , } \\ & { \mathcal { B } _ { \mathrm { c u r r } } = \mathrm { B E V D e c o d e r } ( F _ { \mathrm { b e v } } ^ { \mathrm { c u r r } } ) . } \end{array}\tag{1}
$$

## 3.3 Future BEV world modeling

Given the current BEV feature and ego feature obtained above, a BEV world model is employed to predict the future BEV representation. Instead of modeling future images, which is both challenging and computationally intensive, we follow recent works [27, 36, 43] that model structured and simplified BEV representations as a more efficient alternative. The current BEV feature $F _ { \mathrm { b e v } } ^ { \mathrm { c u r r } }$ is first flattened along the spatial dimensions and then repeated across the modality dimension, resulting in an updated $F _ { \mathrm { b e v } } ^ {  \mathrm { u r r } } \in \dot { \mathbb { R } } ^ { M \times H W \times C }$ . It is then concatenated with the current ego feature $F _ { \mathrm { e g o } } ^ { \mathrm { c u r r } }$ to form the scene feature $F _ { \mathrm { s c e n e } } ^ { \mathrm { c u r r } } \in \mathbb { R } ^ { M \times ( H W + 1 ) \times C }$ . The BEV world model, implemented as a Transformer encoder, produces the future scene feature $F _ { \mathrm { s c e n e } } ^ { \mathrm { f u t } } \in \mathbb { R } ^ { M \times ( H W + 1 ) \times C }$ . From this, the future BEV feature $F _ { \mathrm { b e v } } ^ { \mathrm { f u t } }$ is extracted. A lightweight BEV decoder is then applied to generate the future BEV semantic map $\boldsymbol { B } _ { \mathrm { f u t } }$ for supervision. The overall process is illustrated below:

$$
\begin{array} { r } { F _ { \mathrm { s c e n e } } ^ { \mathrm { f u t } } = \mathrm { B E V W o r l d M o d e l } ( F _ { \mathrm { s c e n e } } ^ { \mathrm { c u r r } } ) , } \\ { \mathcal { B } _ { \mathrm { f u t } } = \mathrm { B E V D e c o d e r } ( F _ { \mathrm { b e v } } ^ { \mathrm { f u t } } ) . \qquad } \end{array}\tag{2}
$$

## 3.4 Future-aware end-to-end planning

After obtaining the current BEV feature, current ego feature, and future BEV feature, the end-to-end planning network jointly reasons over the present scene and its future evolution to generate the planned trajectories. However, enabling the planning network to simultaneously consider both the current and future BEV features is non-trivial. Directly interacting the ego feature with both can lead to entangled representations, causing confusion in ego planning and degrading performance. To address this, we adopt a decoupled strategy, where the ego feature interacts with the current and future BEV features independently, and the results are subsequently fused for final trajectory planning.

As illustrated in Figure 2 (b), the current ego feature $F _ { \mathrm { e g o } } ^ { \mathrm { c u r r } }$ interacts with the current BEV feature $F _ { \mathrm { b e v } } ^ { \mathrm { c u r r } }$ through a Transformer decoder. The updated ego feature is then passed through an MLP decoder to generate the planned trajectories $\mathcal { T } _ { \mathrm { a } }$ for supervision. Since the future BEV feature represents the future scene and corresponds to the future ego state, we initialize the future ego feature $F _ { \mathrm { e g o } } ^ { \mathrm { f u t } }$ using the endpoints of the anchored trajectories. It then interacts with the future BEV feature $F _ { \mathrm { b e v } } ^ { \mathrm { f u t } }$ through a Transformer decoder. Similarly, an MLP decoder is applied to produce the planned trajectories $\bar { \tau } _ { \mathrm { b } }$ for supervision. The process is shown below:

$$
\begin{array} { r l } & { F _ { \mathrm { e g o } } ^ { \mathrm { c u r r } } = \mathrm { T r a n s f o r m e r D e c o d e r } ( F _ { \mathrm { e g o } } ^ { \mathrm { c u r r } } , F _ { \mathrm { b e v } } ^ { \mathrm { c u r r } } ) , } \\ & { F _ { \mathrm { e g o } } ^ { \mathrm { f u t } } = \mathrm { T r a n s f o r m e r D e c o d e r } ( F _ { \mathrm { e g o } } ^ { \mathrm { f u t } } , F _ { \mathrm { b e v } } ^ { \mathrm { f u t } } ) , } \\ & { \quad \mathcal { T } _ { \mathrm { a } } = \mathrm { E g o D e c o d e r } ( F _ { \mathrm { e g o } } ^ { \mathrm { c u r r } } ) , } \\ & { \quad \mathcal { T } _ { \mathrm { b } } = \mathrm { E g o D e c o d e r } ( F _ { \mathrm { e g o } } ^ { \mathrm { f u t } } ) . } \end{array}\tag{3}
$$

To incorporate the future ego feature into the current ego feature, we adopt motion-aware layer normalization (MLN) [4] to obtain a future-aware ego representation. This representation is then passed through an MLP decoder to generate the final planned trajectories $\mathcal { T } _ { \mathrm { f i n a l } }$

$$
\begin{array} { r l } & { F _ { \mathrm { e g o } } ^ { \mathrm { c u r r } } = \mathrm { M L N } ( F _ { \mathrm { e g o } } ^ { \mathrm { c u r r } } , F _ { \mathrm { e g o } } ^ { \mathrm { f u t } } ) , } \\ & { \mathcal { T } _ { \mathrm { f i n a l } } = \mathrm { E g o D e c o d e r } ( F _ { \mathrm { e g o } } ^ { \mathrm { c u r r } } ) . } \end{array}\tag{4}
$$

## 3.5 Iterative scene modeling and vehicle planning

As illustrated in Figure 2 (c), the BEV world modeling network and the end-to-end planning network operate in an iterative manner to progressively improve planning performance. This is motivated by the mutual dependency between future scene evolution and ego trajectories—future traffic dynamics influence the ego’s motion plans, while the ego’s planned actions, in turn, shape the future scene. In the end-to-end planning network, the future BEV feature $F _ { \mathrm { b e v } } ^ { \mathrm { f u t } }$ serves as a reference for generating the planned trajectories. Meanwhile, the refined ego feature F<sup>curr</sup><sub>ego</sub> is fed back into the BEV world modeling network to produce an updated future BEV feature. This iterative process is repeated N times, yielding N pairs of predicted future semantic maps and ego trajectories, denoted as $( \mathcal { B } _ { \mathrm { f u t } } ^ { ( 1 ) } , \mathcal { T } _ { \mathrm { a } } ^ { ( 1 ) } , \mathcal { T } _ { \mathrm { b } } ^ { ( 1 ) } , \mathcal { T } _ { \mathrm { f i n a l } } ^ { ( 1 ) } ) , \ldots , ( \hat { \mathcal { B } _ { \mathrm { f u t } } ^ { ( N ) } } , \mathcal { T } _ { \mathrm { a } } ^ { ( N ) } , \mathcal { T } _ { \mathrm { b } } ^ { ( N ) } , \mathcal { T } _ { \mathrm { f i n a l } } ^ { ( N ) } )$ , which are all supervised during training.

## 3.6 End-to-end learning

The model is trained in an end-to-end manner with a loss function comprising two components: the BEV semantic map loss ${ \mathcal { L } } _ { \mathrm { m a p } }$ and the planned trajectory loss $\dot { \mathcal { L } } _ { \mathrm { t r a j } }$ The semantic map loss includes the current BEV map loss $\mathcal { L } _ { \mathrm { m a p } } ^ { \mathrm { c u r r } }$ and the future BEV map losses from N iterations, denoted as $\mathcal { L } _ { \mathrm { m a p } } ^ { \mathrm { f u t \ ( 1 ) } } , \ldots , \mathcal { L } _ { \mathrm { m a p } } ^ { \mathrm { f u t \ ( N ) } }$ . The trajectory loss consists of N sets of trajectory planning losses, each containing three terms as described in the end-to-end planning network: $\begin{array} { r l } & { \mathbf { \Phi } _ { \mathrm { ( \mathcal { L } _ { t r a j } ^ { a } ) } } ^ { \star } , \mathbf { \Phi } _ { \mathrm { , t r a j } } ^ { \mathrm { b } \ ( 1 ) } , \mathbf { \Phi } _ { \mathrm { , t r a j } } ^ { \mathrm { f i n a l \ ( 1 ) } } ) , \ldots , \mathbf { \Phi } ( \mathbf { \Xi } _ { \mathrm { t r a j } } ^ { \sim } , \mathbf { \Phi } _ { \mathrm { , t r a j } } ^ { \mathrm { b } \ ( \mathrm { N } ) } , \mathbf { \Phi } _ { \mathrm { , t r a j } } ^ { \mathrm { f i n a l \ ( N ) } } ) } \end{array}$ . The overall loss function for end-to-end training is as follows:

$$
\begin{array} { r l } & { \mathcal { L } _ { \mathrm { m a p } } = \lambda _ { 1 } \mathcal { L } _ { \mathrm { m a p } } ^ { \mathrm { c u r r } } + \lambda _ { 2 } ( \mathcal { L } _ { \mathrm { m a p } } ^ { \mathrm { f u t } } ( 1 ) + \cdot \cdot \cdot + \mathcal { L } _ { \mathrm { m a p } } ^ { \mathrm { f u t } } ( \mathrm { N } ) ) , } \\ & { \mathcal { L } _ { \mathrm { t r a j } } = \lambda _ { 3 } ( ( \mathcal { L } _ { \mathrm { t r a j } } ^ { \mathrm { a } } + \mathcal { L } _ { \mathrm { t r a j } } ^ { \mathrm { b } } + \mathcal { L } _ { \mathrm { t r a j } } ^ { \mathrm { f u a l } } ( 1 ) ) + \cdot \cdot \cdot + ( \mathcal { L } _ { \mathrm { t r a j } } ^ { \mathrm { a } } + \mathcal { L } _ { \mathrm { t r a j } } ^ { \mathrm { b } } + \mathcal { L } _ { \mathrm { t r a j } } ^ { \mathrm { f u a l } } ( \mathrm { N } ) ) ) , } \\ & { \mathcal { L } _ { \mathrm { t o t a l } } = \mathcal { L } _ { \mathrm { m a p } } + \mathcal { L } _ { \mathrm { t r a j } } . } \end{array}\tag{5}
$$

where $\lambda _ { 1 } , \lambda _ { 2 } .$ , and $\lambda _ { 3 }$ are the balancing factors.

## 4 Experiments

## 4.1 Datasets and metrics

Datasets. We conduct experiments on two large-scale real-world autonomous driving datasets: NAVSIM [19] and nuScenes [17]. NAVSIM, built upon nuPlan [47], is designed for non-reactive simulation in complex scenarios with dynamic intention changes. It contains 1,192 training/validation (navtrain) and 136 testing (navtest) scenarios, with 8-camera and LiDAR data at 2 Hz. nuScenes includes 1,000 scenes with 6-camera and LiDAR data at 2 Hz. We follow the standard 700/150 train/validation split and evaluate planning in an open-loop setting.

Evaluation metrics. For the NAVSIM dataset, we use the PDM Score (PDMS), which comprises multiple sub-metrics: No At-Fault Collisions (NC), Drivable Area Compliance (DAC), Time-to-Collision (TTC), Comfort (Comf.), and Ego Progress (EP). For the nuScenes dataset, we follow the VAD [13] setting and report the L2 Displacement Error and Collision Rate.

## 4.2 Implementation details

Model settings. The model for the NAVSIM dataset uses both images and LiDAR as input, whereas the nuScenes model relies solely on images. For backbone networks, ResNet34 is employed for NAVSIM and ResNet50 for nuScenes. Regarding the number of camera views, 3 views are used in NAVSIM and 6 in nuScenes. The input image resolution is 1024×256 following TransFuser for NAVSIM, and 640×360 for nuScenes. The number of trajectory modes is set to 256 for NAVSIM and 6 for nuScenes. For NAVSIM, the planning horizon is 4 seconds with 8 future steps, and for nuScenes, it is 3 seconds with 6 steps. In both settings, we predict the future BEV semantic map corresponding to the final planning step.

Training settings. The model is trained on 8 NVIDIA GeForce RTX 3090 GPUs. For NAVSIM, the batch size is 16 per GPU, with 30 training epochs and a total training time of around 5 hours. For nuScenes, the batch size is 1 per GPU, with 12 epochs and a training time of about 12 hours. The learning rate is set to $2 \times 1 0 ^ { - \hat { 4 } }$ for NAVSIM and $\bar { 1 } \times 1 0 ^ { - 4 }$ for nuScenes, both optimized using AdamW [48]. The loss balancing factors are set to $\lambda _ { 1 } = 1 0 , \lambda _ { 2 } = 0 . 1$ , and $\lambda _ { 3 } = 1$ for NAVSIM, and all set to 1 for nuScenes.

## 4.3 Comparison with state of the art

As shown in Table 1, we compare SeerDrive with several state-of-the-art methods on the NAVSIM dataset. Our approach achieves the highest PDM Score of 88.9. Under the same ResNet34 [49] backbone, SeerDrive outperforms recent methods, including the trajectory refinement model Hydra-NeXt [50], the online trajectory evaluation method WoTE [43], and the truncated diffusion policy method DiffusionDrive [15], demonstrating the effectiveness of our iterative world modeling and planning strategy. Furthermore, when replacing the ResNet-34 backbone with V2-99 [51], as done in GoalFlow [28], our method achieves better performance with significantly lower computational cost while supporting end-to-end training.

Table 1: Performance comparison of planning on the NAVSIM navtest split with closed-loop metrics. “C & L” represents the use of both camera and LiDAR as sensor inputs. ResNet34 [49] is employed as the backbone for BEV feature extraction, following TransFuser [21]. The best and second best results are highlighted in bold and underline, respectively. † denotes the use of V2-99 [51] as the image backbone.
<table><tr><td>Method</td><td>Input</td><td>NC↑</td><td>DAC ↑</td><td>TTC ↑</td><td>Comf. ↑</td><td>EP↑</td><td>PDMS ↑</td></tr><tr><td>VADv2-V8192 [25] Hydra-MDP-V8192 [46] UniAD [12] LTF [21] PARA-Drive [55] TransFuser [21]</td><td>C&amp;L C&amp;L Camera Camera Camera C&amp;L</td><td>97.2 97.9 97.8 97.4 97.9</td><td>89.1 91.7 91.9 92.8</td><td>91.6 92.9 92.9</td><td>100 100 100</td><td>76.0 77.6 78.8</td><td>80.9 83.0</td></tr><tr><td></td><td></td><td>97.7</td><td>92.4 92.8</td><td>92.4 93.0 92.8</td><td>100 99.8 100</td><td>79.0 79.3 79.2</td><td>83.4 83.8 84.0 84.0</td></tr><tr><td>LAW [26]</td><td>Camera</td><td>96.4</td><td>95.4</td><td>88.7</td><td>99.9</td><td>81.7</td><td>84.6</td></tr><tr><td>DRAMA [56]</td><td>C&amp;L</td><td>98.0</td><td>93.1</td><td>94.8</td><td>100</td><td>80.1</td><td>85.5</td></tr><tr><td>Hydra-MDP++ [57]</td><td>Camera</td><td>97.6</td><td>96.0</td><td>93.1</td><td>100</td><td>80.4</td><td>86.6</td></tr><tr><td>DiffusionDrive [15]</td><td>C&amp;L</td><td>98.2</td><td>96.2</td><td>94.7</td><td>100</td><td>82.2</td><td>88.1</td></tr><tr><td>WoTE [43]</td><td>C&amp;L</td><td>98.5</td><td>96.8</td><td>94.9</td><td>99.9</td><td>81.9</td><td>88.3</td></tr><tr><td>Hydra-NeXt [50]</td><td>C&amp;L</td><td>98.1</td><td>97.7</td><td>94.6</td><td>100</td><td>81.8</td><td>88.6</td></tr><tr><td>SeerDrive</td><td>C&amp;L</td><td>98.4</td><td>97.0</td><td>94.9</td><td>99.9</td><td>83.2</td><td>88.9</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>GoalFlow† [28] SeerDrive†</td><td>C&amp;L C&amp;L</td><td>98.4 98.8</td><td>98.3 98.6</td><td>94.6 95.8</td><td>100 100</td><td>85.0</td><td>90.3</td></tr></table>

Table 2: Performance comparison of planning on the nuScenes validation split. ResNet50 [49] is used as the backbone for all methods, except for UniAD [12], which adopts ResNet101. “w/o bev” indicates without future BEV injection, and “w/o iter” indicates without iterative world modeling and planning.
<table><tr><td rowspan="2">Method</td><td colspan="4">L2 (m) ↓</td><td colspan="4">Col. Rate (%) ↓</td></tr><tr><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td></tr><tr><td>ST-P3 [22]</td><td>1.33</td><td>2.11</td><td>2.90</td><td>2.11</td><td>0.23</td><td>0.62</td><td>1.27</td><td>0.71</td></tr><tr><td>BEV-Planner [54]</td><td>0.28</td><td>0.42</td><td>0.68</td><td>0.46</td><td>0.04</td><td>0.37</td><td>1.07</td><td>0.49</td></tr><tr><td>VAD-Tiny [13]</td><td>0.46</td><td>0.76</td><td>1.12</td><td>0.78</td><td>0.21</td><td>0.35</td><td>0.58</td><td>0.38</td></tr><tr><td>LAW [26]</td><td>0.26</td><td>0.57</td><td>1.01</td><td>0.61</td><td>0.14</td><td>0.21</td><td>0.54</td><td>0.30</td></tr><tr><td>PARA-Drive [55]</td><td>0.25</td><td>0.46</td><td>0.74</td><td>0.48</td><td>0.14</td><td>0.23</td><td>0.39</td><td>0.25</td></tr><tr><td>VAD-Base [13]</td><td>0.41</td><td>0.70</td><td>1.05</td><td>0.72</td><td>0.07</td><td>0.17</td><td>0.41</td><td>0.22</td></tr><tr><td>GenAD [58]</td><td>0.28</td><td>0.49</td><td>0.78</td><td>0.52</td><td>0.08</td><td>0.14</td><td>0.34</td><td>0.19</td></tr><tr><td>UniAD [12]</td><td>0.44</td><td>0.67</td><td>0.96</td><td>0.69</td><td>0.04</td><td>0.08</td><td>0.23</td><td>0.12</td></tr><tr><td>BridgeAD [53]</td><td>0.29</td><td>0.57</td><td>0.92</td><td>0.59</td><td>0.01</td><td>0.05</td><td>0.22</td><td>0.09</td></tr><tr><td>MomAD [52]</td><td>0.31</td><td>0.57</td><td>0.91</td><td>0.60</td><td>0.01</td><td>0.05</td><td>0.22</td><td>0.09</td></tr><tr><td>SparseDrive [14]</td><td>0.29</td><td>0.58</td><td>0.96</td><td>0.61</td><td>0.01</td><td>0.05</td><td>0.18</td><td>0.08</td></tr><tr><td>SeerDrive w/o bev</td><td>0.22</td><td>0.49</td><td>0.73</td><td>0.48</td><td>0.02</td><td>0.05</td><td>0.16</td><td>0.08</td></tr><tr><td>SeerDrive w/o iter</td><td>0.28</td><td>0.47</td><td>0.81</td><td>0.52</td><td>0.02</td><td>0.07</td><td>0.20</td><td>0.10</td></tr><tr><td>SeerDrive</td><td>0.20</td><td>0.39</td><td>0.69</td><td>0.43</td><td>0.00</td><td>0.05</td><td>0.14</td><td>0.06</td></tr></table>

As shown in Table 2, we further evaluate our method on the nuScenes dataset. It achieves notable performance gains compared with recent state-of-the-art methods, including SparseDrive [14], MomAD [52], and BridgeAD [53]. Although the nuScenes dataset contains relatively simple scenarios and imperfect evaluation metrics [54], our method still achieves clear improvements, demonstrating the effectiveness of the two main designs.

## 4.4 Ablation study

Effects of components. As shown in Table 3, we conduct an ablation study on the key components of our method, including Future-Aware Planning and Iterative Scene Modeling and Vehicle Planning. In the first row, both modules are removed, so the planned trajectories rely only on the current BEV feature and no iterative process is applied. This leads to a drop in PDMS from 88.9 to 87.1. In the second row, we remove the future BEV injection for planning, which also results in decreased performance, showing the importance of future BEV features for planning. In the third row, we remove the iterative process, and performance drops as well, indicating its role in refining the results. The last row presents the full SeerDrive model with both modules included, achieving the highest performance.

Table 3: Ablation study on the key components of our model. “Iter. S&V” refers to Iterative Scene Modeling and Vehicle Planning.
<table><tr><td>Future-aware plan</td><td>Iter. S&amp;V</td><td>NC↑</td><td>DAC ↑</td><td>TTC ↑</td><td>Comf. ↑</td><td>EP↑</td><td>PDMS ↑</td></tr><tr><td></td><td></td><td>98.3</td><td>95.6</td><td>94.5</td><td>100</td><td>81.1</td><td>87.1</td></tr><tr><td></td><td>√</td><td>98.2</td><td>96.6</td><td>94.3</td><td>100</td><td>82.0</td><td>87.9</td></tr><tr><td>V</td><td></td><td>98.2</td><td>96.5</td><td>94.4</td><td>100</td><td>82.5</td><td>88.1</td></tr><tr><td>√</td><td>√</td><td>98.4</td><td>97.0</td><td>94.9</td><td>99.9</td><td>83.2</td><td>88.9</td></tr></table>

Effects of Future-Aware Planning. As shown in Table 4, we conduct an ablation study on the design of the future-aware end-to-end planning. The first two rows analyze different strategies for incorporating the future BEV feature. In the first row, future BEV injection is removed entirely. In the second row, the decoupled strategy is omitted, and the network learns jointly from current and future BEV features. Both settings lead to notable performance degradation, highlighting the effectiveness of our proposed design. In the third and fourth rows, we analyze how the current and future ego features are combined. In the third row, the Motion-aware Layer Normalization (MLN) is removed, and the two features are concatenated and passed through an MLP for dimension alignment. In the fourth row, MLN is also removed, and the features are directly added. Both variations lead to a notable drop in performance, demonstrating the effectiveness of MLN in producing a future-aware ego feature.

Table 4: Ablation study on the design of future-aware end-to-end planning.
<table><tr><td>Type</td><td>NC↑</td><td>DAC ↑</td><td>TTC ↑</td><td>Comf. ↑</td><td>EP↑</td><td>PDMS ↑</td></tr><tr><td>w/o Future BEV w/o Decouple</td><td>98.2 98.0</td><td>96.6 96.0</td><td>94.3 94.0</td><td>100 99.5</td><td>82.0</td><td>87.9</td></tr><tr><td>MLN2Cat</td><td>98.3</td><td>96.6</td><td>94.7</td><td>100</td><td>81.6</td><td>87.3 88.3</td></tr><tr><td>MLN2Add</td><td>98.2</td><td>97.0</td><td>94.1</td><td>100</td><td>82.4 82.9</td><td>88.5</td></tr><tr><td>SeerDrive</td><td>98.4</td><td>97.0</td><td>94.9</td><td>99.9</td><td>83.2</td><td>88.9</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>

Effects of the number of iterations. As shown in Table 5, a moderate number of iterations for scene modeling and vehicle planning achieves a good balance between efficiency and performance. We observe that using two iterations yields the best trade-off.

Table 5: Ablation study on the number of iterations for scene modeling and vehicle planning.
<table><tr><td>Number</td><td>NC↑</td><td>DAC ↑</td><td>TTC↑</td><td>Comf. ↑</td><td>EP↑</td><td>PDMS ↑</td></tr><tr><td>1</td><td>98.4</td><td>96.6</td><td>94.5</td><td>100</td><td>82.2</td><td>88.1</td></tr><tr><td>2</td><td>98.4</td><td>97.0</td><td>94.9</td><td>99.9</td><td>83.2</td><td>88.9</td></tr><tr><td>3</td><td>98.4</td><td>97.2</td><td>94.9</td><td>100</td><td>82.5</td><td>88.7</td></tr></table>

Prediction steps of future BEV. We predict the future BEV only at the final planning step, as the last frame provides the most informative reference for determining the trajectory direction. This design yields an effective and efficient planning reference. As shown in Table 6, we further analyze this choice by predicting a sequence of intermediate BEV representations and concatenating them as planner inputs. However, incorporating intermediate predictions brings no significant performance gains while increasing model complexity. Therefore, predicting only the final future BEV at the last planning step proves to be the more effective and efficient strategy.

Table 6: Ablation study on the number of prediction steps for future BEV.
<table><tr><td>Prediction steps</td><td>NC↑</td><td>DAC ↑</td><td>TTC↑</td><td>Comf. ↑</td><td>EP↑</td><td>PDMS ↑</td></tr><tr><td>1s-2s-3s-4s</td><td>98.3</td><td>97.0</td><td>94.6</td><td>100</td><td>83.0</td><td>88.8</td></tr><tr><td>2s-4s</td><td>98.4</td><td>97.2</td><td>94.8</td><td>100</td><td>83.1</td><td>88.9</td></tr><tr><td>4s (Origin)</td><td>98.4</td><td>97.0</td><td>94.9</td><td>99.9</td><td>83.2</td><td>88.9</td></tr></table>

The performance of $\mathcal { T } _ { \mathrm { a } } , \mathcal { T } _ { \mathrm { b } } ,$ and $\tau _ { \mathrm { f i n a l } } .$ As shown in Table 7, we conduct an ablation study to separately evaluate the performance of $\mathcal { T } _ { \mathrm { a } } , \mathcal { T } _ { \mathrm { b } }$ , and $\mathcal { T } _ { \mathrm { f i n a l } }$ . The results show that $\mathcal { T } _ { \mathrm { f i n a l } }$ significantly outperforms both $\mathcal { T } _ { \mathrm { a } }$ and $\mathcal { T } _ { \mathrm { b } }$ , indicating that each contributes meaningfully to the superior performance of the final trajectory.

Table 7: Ablation study on the performance of $\mathcal { T } _ { \mathrm { a } } .$ , ${ \mathcal { T } } _ { \mathrm { b } } .$ , and $\mathcal { T } _ { \mathrm { f i n a l } }$
<table><tr><td></td><td>NC↑</td><td>DAC ↑</td><td>TTC↑</td><td>Comf. ↑</td><td>EP↑</td><td>PDMS ↑</td></tr><tr><td> $\mathcal { T } _ { \mathrm { a } }$ </td><td>98.3</td><td>96.6</td><td>94.4</td><td>100</td><td>82.7</td><td>88.3</td></tr><tr><td> $\mathcal { T } _ { \mathrm { b } }$ </td><td>98.2</td><td>96.4</td><td>94.2</td><td>99.9</td><td>83.0</td><td>88.2</td></tr><tr><td>Tfinal</td><td>98.4</td><td>97.0</td><td>94.9</td><td>99.9</td><td>83.2</td><td>88.9</td></tr></table>

The use of the anchored endpoints to initialize the future ego feature. The future BEV corresponds to the final planning step. Thus, we initialize the future ego feature using the anchored endpoints, allowing it to encode prior knowledge of the ego vehicle’s future state at the final planning step. For more extensive evaluation, we analyze different initialization strategies for the future ego feature. As shown in Table 8, using anchored endpoints as a prior yields the best performance.

Table 8: Ablation study on the use of the anchored endpoints to initialize the future ego feature.
<table><tr><td></td><td>NC↑</td><td>DAC↑</td><td>TTC ↑</td><td>Comf. ↑</td><td>EP↑</td><td>PDMS ↑</td></tr><tr><td>Random</td><td>98.3</td><td>96.9</td><td>94.5</td><td>100</td><td>82.8</td><td>88.6</td></tr><tr><td>Anchored trajectories</td><td>98.3</td><td>96.8</td><td>94.0</td><td>100</td><td>83.7</td><td>88.7</td></tr><tr><td>Anchored endpoints (Origin)</td><td>98.4</td><td>97.0</td><td>94.9</td><td>99.9</td><td>83.2</td><td>88.9</td></tr></table>

## 4.5 Qualitative results

As shown in Figure 3, we visualize two cases: a right turn and a left turn. In the bottom middle figure, the final planned trajectory generated by our model closely aligns with the ground-truth trajectory. The bottom right figure presents the planned multi-modal trajectories, capturing multiple possible future motions. The bottom left figure shows the predicted future BEV semantic maps, which reflect how the scene evolves and how the ego vehicle’s position changes after the turning behaviors.

## 5 Conclusion

This paper presents SeerDrive, a unified end-to-end framework that combines future scene modeling and trajectory planning. Unlike traditional one-shot approaches that rely only on the current scene, SeerDrive predicts future BEV representations to guide planning. It introduces two core components: Future-Aware Planning, which incorporates predicted future context into trajectory generation, and Iterative Scene Modeling and Vehicle Planning, which refines both scene predictions and plans through repeated interaction. This design enables more informed and adaptive decisions. Extensive experiments on NAVSIM and nuScenes show our approach achieves state-of-the-art results.

![](images/84e3d92c3b3650c76801cddc80485a65922e583e1c53326d82d1931098c2c393.jpg)  
(a) Right-turn case

![](images/6fea2e95432f5eb263cd5cd5de5ca0924fca65432fcc031e9ca4398b0027907d.jpg)  
(b) Left-turn case  
Figure 3: Qualitative results on the NAVSIM dataset. The visualization includes three front-facing camera views: front left, front, and front right, as well as model outputs including the predicted future BEV semantic map, the planned trajectory, and multi-modal predicted trajectories.

Limitations and future work. The BEV world model adopts a transformer architecture specifically tailored to our framework, making it both effective and efficient for planning. However, it does not benefit from the generalization capabilities of foundation models. On the other hand, using off-theshelf foundation models as world models often suffers from slow inference speed and challenges in joint optimization with the planner. Therefore, developing a tightly integrated paradigm of planning and world modeling represents a promising direction for future work.

## Acknowledgments

This work was supported in part by National Natural Science Foundation of China (Grant No.   
62376060).

## References

[1] Li Chen, Penghao Wu, Kashyap Chitta, Bernhard Jaeger, Andreas Geiger, and Hongyang Li. End-to-end autonomous driving: Challenges and frontiers. IEEE TPAMI, 2024. 1

[2] Zhiqi Li, Wenhai Wang, Hongyang Li, Enze Xie, Chonghao Sima, Tong Lu, Yu Qiao, and Jifeng Dai. Bevformer: Learning bird’s-eye-view representation from multi-camera images via spatiotemporal transformers. In ECCV, 2022. 1, 2

[3] Chenyu Yang, Yuntao Chen, Hao Tian, Chenxin Tao, Xizhou Zhu, Zhaoxiang Zhang, Gao Huang, Hongyang Li, Yu Qiao, Lewei Lu, et al. Bevformer v2: Adapting modern image backbones to bird’s-eye view recognition via perspective supervision. In CVPR, 2023. 1

[4] Shihao Wang, Yingfei Liu, Tiancai Wang, Ying Li, and Xiangyu Zhang. Exploring object-centric temporal modeling for efficient multi-view 3d object detection. In ICCV, 2023. 1, 2, 5

[5] Shaoshuai Shi, Li Jiang, Dengxin Dai, and Bernt Schiele. Motion transformer with global intention localization and local movement refinement. In NeurIPS, 2022. 1, 2

[6] Shaoshuai Shi, Li Jiang, Dengxin Dai, and Bernt Schiele. Mtr++: Multi-agent motion prediction with symmetric scene modeling and guided intention querying. IEEE TPAMI, 2024. 1

[7] Zikang Zhou, Jianping Wang, Yung-Hui Li, and Yu-Kai Huang. Query-centric trajectory prediction. In CVPR, 2023. 1, 2

[8] Bozhou Zhang, Nan Song, and Li Zhang. Decoupling motion forecasting into directional intentions and dynamic states. In NeurIPS, 2024. 1

[9] Jie Cheng, Yingbing Chen, Xiaodong Mei, Bowen Yang, Bo Li, and Ming Liu. Rethinking imitation-based planners for autonomous driving. In ICRA, 2024. 1, 2

[10] Jie Cheng, Yingbing Chen, and Qifeng Chen. Pluto: Pushing the limit of imitation learning-based planning for autonomous driving. arXiv preprint, 2024. 1

[11] Yinan Zheng, Ruiming Liang, Kexin ZHENG, Jinliang Zheng, Liyuan Mao, Jianxiong Li, Weihao Gu, Rui Ai, Shengbo Eben Li, Xianyuan Zhan, and Jingjing Liu. Diffusion-based planning for autonomous driving with flexible guidance. In ICLR, 2025. 1, 2

[12] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, et al. Planning-oriented autonomous driving. In CVPR, 2023. 1, 2, 7, 16

[13] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. Vad: Vectorized scene representation for efficient autonomous driving. In ICCV, 2023. 1, 2, 3, 6, 7, 16

[14] Wenchao Sun, Xuewu Lin, Yining Shi, Chuang Zhang, Haoran Wu, and Sifa Zheng. Sparsedrive: End-toend autonomous driving via sparse scene representation. In ICRA, 2025. 1, 2, 3, 4, 7, 14

[15] Bencheng Liao, Shaoyu Chen, Haoran Yin, Bo Jiang, Cheng Wang, Sixu Yan, Xinbang Zhang, Xiangyu Li, Ying Zhang, Qian Zhang, and Xinggang Wang. Diffusiondrive: Truncated diffusion model for end-to-end autonomous driving. In CVPR, 2025. 1, 2, 3, 4, 6, 7, 14

[16] Xiaosong Jia, Junqi You, Zhiyuan Zhang, and Junchi Yan. Drivetransformer: Unified transformer for scalable end-to-end autonomous driving. In ICLR, 2025. 1, 3

[17] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multimodal dataset for autonomous driving. In CVPR, 2020. 1, 2, 6, 14

[18] Xiaosong Jia, Zhenjie Yang, Qifeng Li, Zhiyuan Zhang, and Junchi Yan. Bench2drive: Towards multiability benchmarking of closed-loop end-to-end autonomous driving. In NeurIPS, 2024. 1, 3, 15, 16

[19] Daniel Dauner, Marcel Hallgarten, Tianyu Li, Xinshuo Weng, Zhiyu Huang, Zetong Yang, Hongyang Li, Igor Gilitschenski, Boris Ivanovic, Marco Pavone, et al. Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking. In NeurIPS, 2024. 1, 3, 6, 14, 15, 16

[20] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. Carla: An open urban driving simulator. In CoRL, 2017. 1, 2

[21] Aditya Prakash, Kashyap Chitta, and Andreas Geiger. Multi-modal fusion transformer for end-to-end autonomous driving. In CVPR, 2021. 2, 4, 7

[22] Shengchao Hu, Li Chen, Penghao Wu, Hongyang Li, Junchi Yan, and Dacheng Tao. St-p3: End-to-end vision-based autonomous driving via spatial-temporal feature learning. In ECCV, 2022. 2, 7

[23] Xiaosong Jia, Yulu Gao, Li Chen, Junchi Yan, Patrick Langechuan Liu, and Hongyang Li. Driveadapter: Breaking the coupling barrier of perception and planning in end-to-end autonomous driving. In ICCV, 2023. 2

[24] Xiaosong Jia, Penghao Wu, Li Chen, Jiangwei Xie, Conghui He, Junchi Yan, and Hongyang Li. Think twice before driving: Towards scalable decoders for end-to-end autonomous driving. In CVPR, 2023. 2

[25] Shaoyu Chen, Bo Jiang, Hao Gao, Bencheng Liao, Qing Xu, Qian Zhang, Chang Huang, Wenyu Liu, and Xinggang Wang. Vadv2: End-to-end vectorized autonomous driving via probabilistic planning. arXiv preprint, 2024. 3, 7

[26] Yingyan Li, Lue Fan, Jiawei He, Yuqi Wang, Yuntao Chen, Zhaoxiang Zhang, and Tieniu Tan. Enhancing end-to-end autonomous driving with latent world model. In ICLR, 2025. 3, 7, 15

[27] Peidong Li and Dixiao Cui. Navigation-guided sparse scene representation for end-to-end autonomous driving. In ICLR, 2025. 3, 5, 15

[28] Zebin Xing, Xingyu Zhang, Yang Hu, Bo Jiang, Tong He, Qian Zhang, Xiaoxiao Long, and Wei Yin. Goalflow: Goal-driven flow matching for multimodal trajectories generation in end-to-end autonomous driving. In CVPR, 2025. 3, 7

[29] Ruiyuan Gao, Kai Chen, Enze Xie, HONG Lanqing, Zhenguo Li, Dit-Yan Yeung, and Qiang Xu. Magicdrive: Street view generation with diverse 3d geometry control. In ICLR, 2024. 3

[30] Yuqing Wen, Yucheng Zhao, Yingfei Liu, Fan Jia, Yanhui Wang, Chong Luo, Chi Zhang, Tiancai Wang, Xiaoyan Sun, and Xiangyu Zhang. Panacea: Panoramic and controllable video generation for autonomous driving. In CVPR, 2024. 3

[31] Jiachen Lu, Ze Huang, Zeyu Yang, Jiahui Zhang, and Li Zhang. Wovogen: World volume-aware diffusion for controllable multi-camera driving scene generation. In ECCV, 2024. 3

[32] Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, Jiagang Zhu, and Jiwen Lu. Drivedreamer: Towards real-world-drive world models for autonomous driving. In ECCV, 2024. 3

[33] Yuqi Wang, Jiawei He, Lue Fan, Hongxin Li, Yuntao Chen, and Zhaoxiang Zhang. Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving. In CVPR, 2024. 3

[34] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. Gaia-1: A generative world model for autonomous driving. arXiv preprint, 2023. 3

[35] Shenyuan Gao, Jiazhi Yang, Li Chen, Kashyap Chitta, Yihang Qiu, Andreas Geiger, Jun Zhang, and Hongyang Li. Vista: A generalizable driving world model with high fidelity and versatile controllability. In NeurIPS, 2024. 3

[36] Kashyap Chitta, Daniel Dauner, and Andreas Geiger. Sledge: Synthesizing driving environments with generative models and rule-based traffic. In ECCV, 2024. 3, 5

[37] Yihan Hu, Siqi Chai, Zhening Yang, Jingyu Qian, Kun Li, Wenxin Shao, Haichao Zhang, Wei Xu, and Qiang Liu. Solving motion planning tasks with a scalable generative model. In ECCV, 2024. 3

[38] Yanhao Wu, Haoyang Zhang, Tianwei Lin, Lichao Huang, Shujie Luo, Rui Wu, Congpei Qiu, Wei Ke, and Tong Zhang. Generating multimodal driving scenes via next-scene prediction. In CVPR, 2025. 3

[39] Luke Rowe, Roger Girgis, Anthony Gosselin, Liam Paull, Christopher Pal, and Felix Heide. Scenario dreamer: Vectorized latent diffusion for generating driving simulation environments. In CVPR, 2025. 3

[40] Jingyu Li, Bozhou Zhang, Xin Jin, Jiankang Deng, Xiatian Zhu, and Li Zhang. Imagidrive: A unified imagination-and-planning framework for autonomous driving. arXiv preprint, 2025. 3

[41] Ruijie Zheng, Jing Wang, Scott Reed, Johan Bjorck, Yu Fang, Fengyuan Hu, Joel Jang, Kaushil Kundalia, Zongyu Lin, Loic Magne, et al. Flare: Robot learning with implicit world modeling. arXiv preprint, 2025. 3

[42] Wenyao Zhang, Hongsi Liu, Zekun Qi, Yunnan Wang, Xinqiang Yu, Jiazhao Zhang, Runpei Dong, Jiawei He, He Wang, Zhizheng Zhang, et al. Dreamvla: a vision-language-action model dreamed with comprehensive world knowledge. In NeurIPS, 2025. 3

[43] Yingyan Li, Yuqi Wang, Yang Liu, Jiawei He, Lue Fan, and Zhaoxiang Zhang. End-to-end driving with online trajectory evaluation via bev world model. arXiv preprint, 2025. 3, 4, 5, 6, 7, 14, 15

[44] Wenzhao Zheng, Weiliang Chen, Yuanhui Huang, Borui Zhang, Yueqi Duan, and Jiwen Lu. Occworld: Learning a 3d occupancy world model for autonomous driving. In ECCV, 2024. 3

[45] Yu Yang, Jianbiao Mei, Yukai Ma, Siliang Du, Wenqing Chen, Yijie Qian, Yuxiang Feng, and Yong Liu. Driving in the occupancy world: Vision-centric 4d occupancy forecasting and planning via world models for autonomous driving. In AAAI, 2025. 3

[46] Zhenxin Li, Kailin Li, Shihao Wang, Shiyi Lan, Zhiding Yu, Yishen Ji, Zhiqi Li, Ziyue Zhu, Jan Kautz, Zuxuan Wu, et al. Hydra-mdp: End-to-end multimodal planning with multi-target hydra-distillation. arXiv preprint, 2024. 4, 7

[47] Holger Caesar, Juraj Kabzan, Kok Seang Tan, Whye Kit Fong, Eric Wolff, Alex Lang, Luke Fletcher, Oscar Beijbom, and Sammy Omari. nuplan: A closed-loop ml-based planning benchmark for autonomous vehicles. arXiv preprint, 2021. 6

[48] I Loshchilov. Decoupled weight decay regularization. In ICLR, 2019. 6

[49] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In CVPR, 2016. 6, 7

[50] Zhenxin Li, Shihao Wang, Shiyi Lan, Zhiding Yu, Zuxuan Wu, and Jose M Alvarez. Hydra-next: Robust closed-loop driving with open-loop training. arXiv preprint, 2025. 6, 7

[51] Youngwan Lee and Jongyoul Park. Centermask: Real-time anchor-free instance segmentation. In CVPR, 2020. 7

[52] Ziying Song, Caiyan Jia, Lin Liu, Hongyu Pan, Yongchang Zhang, Junming Wang, Xingyu Zhang, Shaoqing Xu, Lei Yang, and Yadan Luo. Don’t shake the wheel: Momentum-aware planning in end-to-end autonomous driving. In CVPR, 2025. 7, 16

[53] Bozhou Zhang, Nan Song, Xin Jin, and Li Zhang. Bridging past and future: End-to-end autonomous driving with historical prediction and planning. In CVPR, 2025. 7, 16

[54] Zhiqi Li, Zhiding Yu, Shiyi Lan, Jiahan Li, Jan Kautz, Tong Lu, and Jose M Alvarez. Is ego status all you need for open-loop end-to-end autonomous driving? In CVPR, 2024. 7

[55] Xinshuo Weng, Boris Ivanovic, Yan Wang, Yue Wang, and Marco Pavone. Para-drive: Parallelized architecture for real-time autonomous driving. In CVPR, 2024. 7

[56] Chengran Yuan, Zhanqi Zhang, Jiawei Sun, Shuo Sun, Zefan Huang, Christina Dao Wen Lee, Dongen Li, Yuhang Han, Anthony Wong, Keng Peng Tee, et al. Drama: An efficient end-to-end motion planner for autonomous driving with mamba. arXiv preprint, 2024. 7

[57] Kailin Li, Zhenxin Li, Shiyi Lan, Yuan Xie, Zhizhong Zhang, Jiayi Liu, Zuxuan Wu, Zhiding Yu, and Jose M Alvarez. Hydra-mdp++: Advancing end-to-end driving via expert-guided hydra-distillation. arXiv preprint, 2025. 7

[58] Wenzhao Zheng, Ruiqi Song, Xianda Guo, Chenming Zhang, and Long Chen. Genad: Generative end-to-end autonomous driving. In ECCV, 2024. 7

## Appendix

## A Notations

As shown in Table 9, we provide a lookup table for notations used in the paper.

Table 9: Notations used in the paper.
<table><tr><td>Notation  $\mathcal { T }$ </td><td>Description</td></tr><tr><td> $\mathcal { P }$   $\tau$ </td><td>multi-view images LiDAR</td></tr><tr><td></td><td></td></tr><tr><td> $\mathcal { E }$   $H \& W$ </td><td>anchored multi-modal trajectories ego status spatial dimensions of the BEV feature</td></tr><tr><td></td><td></td></tr><tr><td> $M$ </td><td>the number of trajectory modes</td></tr><tr><td> $C$ </td><td>the number of feature channels</td></tr><tr><td> $N$   $_ { F } \mathrm { c u r r }$   $T _ { \mathrm { e g o } }$ </td><td>the number of iterations</td></tr><tr><td></td><td>current ego feature</td></tr><tr><td> $F _ { \cdot } ^ { \mathrm { c u r r } }$ </td><td>current BEV feature map</td></tr><tr><td> $\underline { { \mathbf { \Pi } } } \mathrm { b e v }$   $F ^ { \mathrm { { c u r r } } }$ </td><td></td></tr><tr><td> $\boldsymbol { { \cal T } } _ { \mathrm { s c e n e } }$   ${ \cal F } \mathrm { { u t } }$ </td><td>current scene feature</td></tr><tr><td> $F _ { \mathrm { e g o } } ^ { \mathrm { ~ \tiny ~ . ~ . ~ } }$ </td><td>future ego feature</td></tr><tr><td> $F _ { \mathrm { . } } ^ { \mathrm { f u t } }$   ${ \mathbf { \Delta } } ^ { \prime } \operatorname { b e v }$ </td><td>future BEV feature map</td></tr><tr><td> $F ^ { \mathrm { f u t } }$  T scene</td><td>future scene feature</td></tr><tr><td> $B _ { \mathrm { c u r r } }$ </td><td>predicted current BEV semantic map</td></tr><tr><td> $\boldsymbol { B } _ { \mathrm { f u t } }$ </td><td></td></tr><tr><td> $\mathcal { T } _ { \mathrm { a } }$ </td><td>predicted future BEV semantic map</td></tr><tr><td></td><td>planned multi-modal trajectories by current BEV</td></tr><tr><td> $\mathcal { T } _ { \mathrm { b } }$ </td><td>planned multi-modal trajectories by future BEV</td></tr><tr><td> $\mathcal { T } _ { \mathrm { f i n a l } }$ </td><td>final planned multi-modal trajectories</td></tr></table>

## B Implementation details

In addition to the implementation details provided in the main paper, we offer further clarifications here. The feature channels $C$ are set to 256 for both the NAVSIM [19] and nuScenes [17] datasets. Regarding the spatial dimensions $H \times W$ of the BEV features, they are $8 \times 8$ for NAVSIM and 100 × 100 for nuScenes. However, for future BEV map prediction, the features are uniformly downsampled to $8 \times 8$ in nuScenes. For the anchored multi-modal trajectories, we follow previous works [14, 15, 43] and use the K-Means algorithm to cluster them from the ground-truth trajectories.

## C Evaluation metrics

In the NAVSIM dataset, trajectories spanning 4 seconds at 2Hz are first produced and then upsampled to 10Hz using an LQR controller. These refined trajectories are evaluated using a set of closedloop metrics, which include No At-Fault Collisions $( S _ { \mathrm { { N C } } } )$ , Drivable Area Compliance $( S _ { \mathrm { D A C } } )$ Time to Collision with bounds $( S _ { \mathrm { { T T C } } } ) .$ , Ego Progress $( S _ { \mathrm { E P } } ) ,$ , Comfort $( S _ { \mathrm { C F } } )$ , and Driving Direction Compliance $( S _ { \mathrm { D D C } } )$ . The overall performance score is computed by aggregating these individual metrics. However, due to implementation limitations, S<sub>DDC</sub> is excluded from the final evaluation<sup>1</sup>.

$$
S _ { \mathrm { P D M } } = S _ { \mathrm { N C } } \times S _ { \mathrm { D A C } } \times s _ { \mathrm { T T C } } \times \nonumber\tag{6}
$$

## D Qualitative results

In addition to the qualitative results, we provide additional visualizations in Figure 4 and Figure 5 to further demonstrate the effectiveness of our model.

## E Failure cases

Although our SeerDrive demonstrates strong performance, it still encounters some failure cases.

As illustrated in Figure 6 (a), the model fails to choose the correct lane after a right turn. In the right subfigure of (a), which shows the multi-modal planning result, one of the predicted trajectories closely aligns with the ground truth. However, the classification score fails to select it, suggesting that the multi-modal trajectory selection process requires further improvement.

As illustrated in Figure 6 (b), the model fails to infer the correct driving intention for a right turn. Most of the planned trajectories instead tend to change lanes to the left and proceed straight. This suggests that incorporating high-level driving intentions, such as explicit driving commands, is necessary for achieving more accurate planning outcomes.

## F Discussions

Comparison with existing methods. Table 10 summarizes the differences between our work and prior approaches in terms of how predicted future scenes from world models are utilized.

Table 10: Comparison between SeerDrive and existing methods.
<table><tr><td>Method</td><td>Usage of predicted future scene from world model</td></tr><tr><td>LAW [26]</td><td>Used as an auxiliary supervision signal during training</td></tr><tr><td>SSR [27]</td><td>Used as an auxiliary supervision signal during training</td></tr><tr><td>WoTE [43]</td><td>Used to assist in selecting the best trajectory among multiple candidates</td></tr><tr><td>SeerDrive (Ours)</td><td>Used as feature-level reference for planning, enabling iterative interaction with planner</td></tr></table>

Experiment on complex scenarios. Following the reviewer’s valuable suggestions, we evaluate our model on the test split of NAVSIM [19] under scenarios with more than 10 agents. As shown in Table 11, our model still demonstrates strong performance.

Table 11: Experiment on complex scenarios.
<table><tr><td></td><td>NC↑</td><td>DAC ↑</td><td>TTC↑</td><td>Comf. ↑</td><td>EP↑</td><td>PDMS ↑</td></tr><tr><td>Complex scenarios</td><td>98.2</td><td>96.8</td><td>94.3</td><td>99.9</td><td>83.1</td><td>88.5</td></tr></table>

Experiment beyond NAVSIM and nuScenes. Following the reviewer’s valuable suggestions, we have further evaluated the more complex Bench2Drive [18] dataset with many rare and high-entropy scenarios such as emergency braking, merging, and overtaking, along with a longer planning horizon and closed-loop testing. As shown in Table 12, our model consistently achieves the best performance.

Uncertainty in future predictions and planning. To tackle the uncertainty caused by the multimodal characteristics of future trajectories, our framework performs prediction and planning while explicitly considering the multi-modal nature of the future. The predicted future BEV feature is multi-modal and shares the same modality as the ego feature used for planning. Accordingly, we also predict a multi-modal future BEV representation. For supervision, we adopt a winner-takes-all strategy: the best trajectory and the corresponding future BEV are selected using the same probability generated from the current ego feature, and the loss is computed based on the selected mode.

Parameter size and inference cost. We evaluate our model on the NAVSIM [19] dataset. The model has 66 M parameters, and the average inference time is 24 ms under the same configuration as in the main paper.

Table 12: Experiment on the Bench2Drive [18] dataset.The first metric corresponds to open-loop testing, while the latter two are used for closed-loop evaluation.
<table><tr><td>Method</td><td>Avg. L2 Error ↓</td><td>Driving Score ↑</td><td>Success Rate (%) ↑</td></tr><tr><td>VAD [13]</td><td>0.91</td><td>42.35</td><td>15.00</td></tr><tr><td>UniAD-Tiny [12]</td><td>0.80</td><td>40.73</td><td>13.18</td></tr><tr><td>UniAD-Base [12]</td><td>0.73</td><td>45.81</td><td>16.46</td></tr><tr><td>MomAD [52]</td><td>0.82</td><td>47.91</td><td>18.11</td></tr><tr><td>BridgeAD [53]</td><td>0.71</td><td>50.06</td><td>22.73</td></tr><tr><td>SeerDrive (Ours)</td><td>0.66</td><td>58.32</td><td>30.17</td></tr></table>

Quantitative metric for predicted future BEV. The mIoU of the predicted future BEV map on the NAVSIM [19] dataset is 38.87.

![](images/d5d82a437c878b534eca0c70f88fecc16d33333168b4ba664f51b4a50a50d22f.jpg)

![](images/bf977bb096a3c3b2ea1d15230002cf92cf2f52053966f031ecfe287fc8aeb85b.jpg)

![](images/3c0e7bfbc5085aa4ddd1d1e0afa9c3328bde77ff8d94a695d3fc59f87cbcc931.jpg)

![](images/cbd2bdbd93d68a70d35b7630faae9d0aabea38254e18da8e85e93789e4c1eb41.jpg)

![](images/7cbbe18fe9658989cd1f0c1783cb5167addbe1a13a5aa41e952e42c95d21951a.jpg)  
Predicted future BEV semantic map

GT trajectory

● Planned trajectory

![](images/15c55f25676f458188a0524fcbea470135d28ea518a202485008f3bcd1287389.jpg)

![](images/9dc85f2d3e91986d365d7954b8627be533f9f71d5659902349810f64856f54c7.jpg)  
(a)

![](images/d939c9d9db13fd1206d1b19e95da3d3d673612a0fc40793b705cfdbad1b08f6e.jpg)

![](images/c00fb7cf054ec857a2f868aa103e59695b52b599d2fbffe928cedb56c3f8afba.jpg)

![](images/2eec77e2836f4aca572bc73df5c8a6b817986b7334f52bdda102c1b18fe99eab.jpg)

![](images/50ed4426e6d3e413801d49e3fbcea1894ec4fc06f2272d443eb6154337675e21.jpg)

GT trajectory

O Planned trajectory

![](images/bb85cbfec1f895f08789ac4c40d9aecd4a3dd370fbf56c928c512ade05073135.jpg)  
(b)

![](images/0c5a290b58b5fcb432bbb5cae6e00f365dbc5d2b37362a20bce2dbacc6d33f78.jpg)  
Figure 4: Qualitative results 1 on the NAVSIM dataset. The visualization includes three front-facing camera views: front left, front, and front right, as well as model outputs including the predicted future BEV semantic map, the planned trajectory, and multi-modal predicted trajectories.

![](images/a868d9a2fcbb3a8386461db8b0fde2dfe9a45ae86b87a1d0992b064959a2425f.jpg)

![](images/af2bf6fe7850d6d2df4677d4f913f116657d1e8b5f4cef7636f69fb3e52367ad.jpg)

![](images/4384b9dee26a63aa302fe9aff4a4c8c35b395de131f096597b665a0d96585534.jpg)

![](images/410a7788a3ae299265fde473163cfbf7cf7e03fd200ddf41683b202506a8a720.jpg)  
Predicted future BEV semantic map

GT trajectory

Planned trajectory

![](images/aa190264e240c15431703de76c25f35645ad377277e4f25e3b3c3b82d0aab086.jpg)  
(c)

![](images/ca7ff8a9ac6ba3412bdf694ca6289f9285837134d3b52ecbfeefed546a1b8a76.jpg)

![](images/b74ae0842f8dddbc42327650df81e6044fd396077c87d9dc3449226d599190d8.jpg)

![](images/a48f247d4470f4da05cb128ca1c6c5c3d8486c3940e7b0b982b00065bea5996d.jpg)

![](images/c99f63a4bea5d0cc22a4e48e32434df7cae448be51f553da4bc67b1bfad7f972.jpg)

GT trajectory

Planned trajectory

![](images/be7734e408fce9e06bec48b2fe1374367cce7a34e6381ad4be8bb51173e3bf38.jpg)  
(d)

![](images/d82ff4a3dd7b8f2c363ee9a049e1bd649fdcde2eae9561aaa87ba24675fd17b7.jpg)  
Figure 5: Qualitative results 2 on the NAVSIM dataset. The visualization includes three front-facing camera views: front left, front, and front right, as well as model outputs including the predicted future BEV semantic map, the planned trajectory, and multi-modal predicted trajectories.

![](images/e8a8ad4ea74e8239f7bdfdaf9d3ed69605b82cb104cae52197d2293cbf49f112.jpg)

![](images/49a6f2a771960281edd672146a87b117bbe87594fd59db35671b48cffd5b2095.jpg)

![](images/15ad645c0ab5fa056f687fc4e786a9f38aa1998839edb6b62882acfed96d8449.jpg)

![](images/176ad23731b8d5b1d44a091d859ad604345509c14629b40f988dd7e1be2c9bb1.jpg)  
(b)  
Figure 6: Failure cases from the NAVSIM dataset. In the left figure, the ground-truth trajectory is shown in green, while the top-ranked planning trajectory, selected based on the classification score, is displayed in orange. The right figure illustrates the predicted multi-modal trajectories.