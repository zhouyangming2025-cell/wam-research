# DriveWorld-VLA: Unified Latent-Space World Modeling with Vision–Language–Action for Autonomous Driving

Feiyang jia <sup>\*</sup> <sup>1</sup> <sup>2</sup> Lin Liu <sup>\*</sup> <sup>1</sup> <sup>2</sup> Ziying Song <sup>1</sup> Caiyan Jia <sup>†</sup> <sup>1</sup> Hangjun Ye <sup>2</sup> Xiaoshuai Hao <sup>†</sup> <sup>2</sup> Long Chen <sup>‡</sup> <sup>2</sup>

![](images/3b34fe8894518753cdded1e6c5569de9967ab7fe5fb1d2a05be19931a13da712.jpg)

![](images/1aabb8e44a21a184c9acd236cee5e335cbbe12bf532697d8180f034db0f07578.jpg)

![](images/8457c5603e62b3dd77740d418686d4b4925f44d02bf8bffe39c1c508b3434c9e.jpg)

![](images/6b4606dd3eb11034ed060683ce4d419bd26b8aaa56eb90340376972faa6bc6da.jpg)  
Figure 1. Comparison of VLA & World Model Coupling Strategies. (a) Disentangled Interaction: The world model acts as an externa simulator, but its structural isolation from the VLA prevents effective latent knowledge transfer. (b) Feature Sharing: Despite sharing representations, these models lack action-conditioned causal reasoning, which limits their counterfactual imagination and long-horizon planning. (c) Our DriveWorld-VLA: By optimizing world model latents as decision variables, we enable unified causal “what-if” reasoning through controllable imagination in a shared latent space. (d) Performance: DriveWorld-VLA achieves SOTA results—91.3 PDMS on NAVSIMv1, 86.8 EPDMS on NAVSIMv2, and 0.16 CR on nuScenes—significantly outperforming specialized baselines like LAW (L et al., 2024a), Epona (Zhang et al., 2025), and HERMES-p (Zhou et al., 2025b).

## Abstract

End-to-end (E2E) autonomous driving has recently attracted increasing interest in unifying Vision–Language–Action (VLA) with World Models to enhance decision-making and forwardlooking imagination. However, existing methods fail to effectively unify future scene evolution and action planning within a single architecture due to inadequate sharing of latent states, limiting the impact of visual imagination on action decisions. To address this limitation, we propose DriveWorld-VLA, a novel framework that fiunifies world modeling and planning within a la-

tent space by tightly integrating VLA and world models at the representation level, which enables the VLA planner to benefit directly from holistic scene-evolution modeling and reducing reliance on dense annotated supervision. Additionally, DriveWorld-VLA incorporates the latent states of the world model as core decision-making states for the VLA planner, facilitating the planner to assess how candidate actions impact future scene evolution. By conducting world modeling entirely in the latent space, DriveWorld-VLA supports controllable, action-conditioned imagination at the feature level, avoiding expensive pixellevel rollouts. Extensive open-loop and closedloop evaluations demonstrate the effectiveness of DriveWorld-VLA, which achieves state-of-the-art performance with 91.3 PDMS on NAVSIMv1, 86.8 EPDMS on NAVSIMv2, and 0.16 3-second average collision rate on nuScenes. Code and models will be released in the DriveWorld-VLA.

## 1. Introduction

Autonomous driving is undergoing a transformative paradigm shift from modular pipelines toward End-to-End (E2E) learning (Cui et al., 2024). Despite their success in mapping sensor inputs to control signals (Song et al., 2025a; Liu et al., 2025; Liao et al., 2025; Song et al., 2025b), these models often lack the capacity for long-horizon reasoning and fail to comprehend the causal consequences of their actions. In response, the integration of Vision-Language-Action (VLA) models with World Models (WM) has emerged as a promising frontier to bridge this gap. In this synergy, VLA models provide sophisticated multimodal perception and linguistic reasoning, while World Models empower agents with “prospective imagination” by explicitly modeling environmental dynamics and actionconditioned future states.

Despite this potential synergy, existing attempts to unify these paradigms remain loosely coupled, typically falling into two suboptimal categories. The first class includes Disentangled Interaction methods (Yan et al., 2025; Yang et al., 2025a), as shown in Figure 1.(a), which treat the world model merely as an external simulator or data source. However, these methods create a structural bottleneck that prevents the VLA from internalizing fundamental physical laws and environment dynamics. The second category is composed of Feature-Sharing approaches (Zhang et al., 2025; Li et al., 2025b; Zhou et al., 2025b), depicted in Figure 1.(b), which employ shared representations for joint prediction but fail to leverage the world model’s most critical capability: explicit causal reasoning and prospective “what-if” imagination. Consequently, by neglecting the action-outcome causal chain, these models remain restricted to reactive planning rather than proactive, long-horizon optimization through counterfactual simulation.

To address these limitations, we propose DriveWorld-VLA (as shown in Figure 1.(c)), a unified framework that integrates VLA and World Models across both representation and decision-making through three core innovations. First, Feature-Level Sharing utilizes Large Language Model (LLM) hidden states as a shared latent space for both imagination and action prediction, enabling the model to internalize fundamental physical laws and environmental dynamics within its core reasoning engine. Second, Action-Conditioned “What-If” Reasoning leverages a Diffusion Transformer (DiT) architecture to perform prospective rollouts of multiple candidate actions; this empowers the agent to transition from reactive planning to proactive optimization by explicitly evaluating the long-term consequences of distinct trajectories. Third, a Three-Stage Progressive Training paradigm stabilizes joint optimization by sequentially aligning multi-modal perception with BEV generation, enforcing action-conditioned controllability via flowmatching, and finally retroactively refining VLA decisions through a closed-loop reward mechanism. Extensive evaluations across open-loop and closed-loop benchmarks demonstrate that DriveWorld-VLA achieves state-of-the-art performance, significantly outperforming specialized baselines in both reasoning accuracy and safety-critical planning.

In summary, our main contributions are as follows:

• We propose DriveWorld-VLA, a tightly coupled framework where a world model serves as the reasoning engine bridging action and prospective imagination.

• We introduce Feature-Level Sharing that uses LLM hidden states as shared latent space for both imagination and action prediction, helping internalize physical laws and environment dynamics.

• We develop action-conditioned “what-if” reasoning to generate and evaluate candidate trajectories for proactive, consequence-aware decision-making.

• We conduct extensive evaluations on both closed-loop (NAVSIM) and open-loop (nuScenes) benchmarks, demonstrating feature-level sharing and causal rollout guidance are critical for robust decision-making.

## 2. Related Works

World Models for Autonomous Driving World models (WMs) have emerged as a cornerstone for autonomous driving, providing a technical foundation for modeling complex environmental evolutions (Jia et al., 2025; Tu et al., 2025; Guan et al., 2024; Feng et al., 2025b). Early efforts such as DriveWorld (Min et al., 2024) and Vista (Gao et al., 2024b) focus on generating spatiotemporally consistent video sequences, while LidarDM (Zyrianov et al., 2025) and Copilot4D (Zhang et al., 2023) explore driving-conditioned point cloud synthesis. Other works, including ViDAR (Yang et al., 2024) and Occ-LLM (Xu et al., 2025), treat occupancy prediction as a foundational representation for world dynamics. Beyond pixel-level generation, some models map observations into latent spaces to forecast agent behaviors and motion (Li et al., 2024a; Hu et al., 2022), partially bridging the gap between conventional pipelines and holistic traffic modeling. Despite these advances, the community lacks a unified objective, with research often split between highfidelity future prediction and trajectory modeling. Only a few pioneering studies, such as HERMES (Zhou et al., 2025b) and Epona (Zhang et al., 2025), explicitly connect generative imagination with downstream planning. In this context, DriveWorld-VLA unifies these paradigms by integrating generative modeling and decision-making within a single framework.

VLAs for Autonomous Driving The rapid evolution of VLA models in autonomous driving is primarily fueled by the profound semantic understanding and reasoning capabilities of VLMs. Early research predominantly utilized VLMs as high-level semantic interpreters to process textualized driving logic and rule-based constraints (Xu et al., 2024; Zhou et al., 2025a; Yang et al., 2025b; Hao et al., 2025b;a). However, with the emergence of multi-modal foundation models, the paradigm has shifted toward end-toend VLA architectures that directly map multi-sensor inputs and linguistic instructions to control trajectories (Shao et al., 2024; Renz et al., 2025; Jiang et al., 2025). Recent frontiers have explored the deep integration of VLAs with world models to enable future-aware reasoning and latent state prediction (Zhou et al., 2025b; Li et al., 2025b; Zhou et al., 2025c; Wang et al., 2025; Zheng et al., 2025; Gao et al., 2024a; Gu et al., 2024). For instance, HERMES (Zhou et al., 2025b) jointly models scene interpretation and evolution, while DriveVLA-W0 (Li et al., 2025b) employs future image prediction as a self-supervised signal for VLA refinement. DriveWorld-VLA advances this trajectory by unifying future visual prediction and action generation within a shared latent space, systematically bridging the gap between generative imagination and proactive decision-making.

![](images/bceba3c79c5e1e559935823b8e5db8b2c44165aa479f286fad13beffd74f2877.jpg)  
Figure 2. DriveWorld-VLA pipeline. DriveWorld-VLA unifies action and prospective imagination through a progressive training scheme. Stage 1 jointly learns future BEV imagination and action prediction from a shared latent representation. Stage 2 conditions the generative branch on future actions, enabling controllable imagination that maps a given action sequence to its corresponding future. Stage 3 closes the loop: first predicts actions, then imagines the resulting future, and finally uses reward feedback to refine action prediction.

## 3. Method

DriveWorld-VLA is designed to tightly integrate VLA model with World Model in a unified architecture that supports both multi-modal reasoning and prospective imagination. To progressively align representation learning, action controllability, and consequence-aware decision making, we adopt a three-stage training paradigm. Each stage incrementally unlocks a key capability of the world model, while ensuring stable joint optimization with the VLA. Specifically, the training process is organized into three sequential stages: VLA & WM Joint Training, Action Controllability Fine-Tuning and Guided Evaluation & Refinement. Figure 2 shows the pipeline of DriveWorld-VLA.

## 3.1. VLA & WM Joint Training

DriveWorld-VLA supports multi-modal inputs, including multi-view images $\mathcal { T } _ { t } .$ , textual prompts $\mathcal { T } _ { t } .$ , historical actions $\mathcal { A } _ { t - 1 }$ , and BEV representations $B _ { t } .$ All modalities are independently tokenized before being fed into the Vision-Language Model (VLM). Image and text tokenization follow InternVL (Zhu et al., 2025), while dedicated tokenizers are introduced for BEV features and historical actions. BEV features $\boldsymbol { B } _ { t } \in \mathbb { R } ^ { H \times W \times C }$ are extracted by BEVFormer (Li et al., 2024c), flattened spatially, and projected into the VLM embedding space as BEV tokens. Historical ego actions are serialized into natural language prompts and concatenated with textual instructions, then encoded using the same text tokenizer as InternVL.

After tokenization, $\mathcal { T } _ { t } , \ \mathcal { T } _ { t } , \ \mathcal { A } _ { t - 1 }$ , and $B _ { t }$ are jointly fed into the VLM. The VLM aggregates information across all modalities and produces a sequence of hidden states. We extract the hidden states from the final VLM layer as a shared latent representation, denoted as $\mathcal { H } _ { t }$

$$
\mathcal { H } _ { t } = \mathbf { V } \mathbf { L M } _ { \theta } ^ { \circ } ( \mathcal { T } _ { t } , \mathcal { B } _ { t } , \mathcal { A } _ { t - 1 } , \mathcal { T } _ { t } ) ,\tag{1}
$$

where $\mathcal { H } _ { t }$ serves as the common feature space for both future imagination and future action prediction. During this stage, DriveWorld-VLA is trained to jointly perform future imagination and action prediction based on shared latent representation, facilitating the transfer of world model knowledge into the VLA.

Future imagination is modeled in the BEV space. Denoiser takes $\mathcal { H } _ { t }$ and $B _ { t }$ as input to predict future BEV states $\boldsymbol { B } _ { t + \Delta t }$ as below,

$$
\begin{array} { r l } & { ~ \mathcal { B } _ { t } ^ { \prime } = \mathrm { C R o s s A T T N } _ { \theta } ^ { \diamond } \big ( \mathcal { B } _ { t } , \mathcal { H } _ { t } , \mathcal { H } _ { t } \big ) , } \\ & { \mathcal { B } _ { t + \Delta t } = \mathrm { D E N o I s E R } _ { \theta } ^ { 1 } \big ( \mathcal { H } _ { t } , \mathcal { B } _ { t } ^ { \prime } , \mathcal { A } _ { t - 1 } \big ) , } \end{array}\tag{2}
$$

which are then decoded by a lightweight segmentation head SEG,

$$
\begin{array} { r } { S _ { t + \Delta t } = \mathrm { S E G } _ { \theta } ( \mathcal { B } _ { t + \Delta t } ) , S _ { t } = \mathrm { S E G } _ { \theta } ( \mathcal { B } _ { t } ^ { \prime } ) . } \end{array}\tag{3}
$$

DENOISER comprises a history-conditioned branch and a future action-conditioned branch. At this stage, only historyconditioned branch is activated and enforce reasoning from historical observations. This lightweight branch provides dense future supervision, enabling predictive representation learning and effective training of images to BEV tokenizers. The future action-conditioned branch follows a generative paradigm to model controllable future evolution under different action sequences.

Action prediction is formulated as trajectory forecasting. A lightweight action decoder takes $\mathcal { H } _ { t } , B _ { t }$ , and $\mathcal { A } _ { t - 1 }$ as input, and outputs the predicted future actions $\boldsymbol { \mathcal { A } } _ { t + \Delta t } ^ { \prime } \mathrm { : }$

$$
\begin{array} { r } { \mathcal { A } _ { t + \Delta t } ^ { \prime } = \mathrm { A c T } _ { \theta } ( \mathcal { H } _ { t } , \mathcal { B } _ { t } , \mathcal { A } _ { t - 1 } ) , } \end{array}\tag{4}
$$

where ACT denotes an action decoder.

Supervision. The future BEV state is supervised by decoding a semantic BEV map, while the action decoder is supervised via imitation learning on expert actions. The overall loss at this stage is defined as:

$$
\mathcal { L } _ { s _ { 1 } } = \mathcal { L } _ { s e g } + \mathcal { L } _ { a c t } ,\tag{5}
$$

where $\mathcal { L } _ { s e g }$ supervises the semantic BEV map decoding and $\mathcal { L } _ { a c t }$ supervises the predicted actions.

## 3.2. Action Controllability Fine-Tuning

During co-training, DriveWorld-VLA is not conditioned on future actions, which prevents it from imagining outcomes based on prospective actions. As a result, DriveWorld-VLA cannot form a closed-loop reasoning between actions and future scene generation. Ideally, DriveWorld-VLA should be aware of how its actions affect the future evolution of the environment to evaluate action quality, rather than solely extrapolating from historical observations.

![](images/4604e5b89b49eb2c44b516542b2e19b383b66ab466d0d3eba7a96675e149386a.jpg)  
Figure 3. The structure of Action-conditioned Flow-matching Denoiser. The Denoiser conditions the flow-matching process on the BEV state and GT future actions. The BEV state is processed through LayerNorm, followed by scaling and Embedding. These features are then passed through DiT blocks to perform denoising and generate the future BEV states.

Motivated by this limitation, this stage focuses on endowing DriveWorld-VLA with the capability of action-conditioned future imagination. Due to the absence of sensor observations in the BEV space, we adopt an explicit feature-level supervision strategy for BEV prediction, which fundamentally differs from downstream-task supervision used in prior works such as WoTE (Li et al., 2025c) and LAW (Li et al., 2024a). After co-training, $B _ { t } ^ { \prime }$ produced by the BEV tokenizer and VLM can be reliably decoded into a semantic BEV map. We therefore treat this BEV latent space as a pretrained variational representation. Given future multiview images $\mathcal { T } _ { t + \delta t }$ , we reuse the Stage 1 encoding pipeline to obtain the corresponding ground truth (GT) BEV latent representation $B _ { t + \Delta t } ^ { \prime }$ as follows:

$$
\mathcal { H } _ { t + \Delta t } = \mathrm { V L M } _ { \theta } ^ { * } ( \mathcal { T } _ { t + \Delta t } , \mathcal { B } _ { t + \Delta t } , \mathcal { A } _ { t + \Delta t } , \mathcal { T } _ { t + \Delta t } ) ,\tag{6}
$$

$$
\mathcal { B } _ { t + \Delta t } ^ { \prime } = \mathrm { C R o s s A T T N } _ { \theta } ^ { * } \big ( \mathcal { B } _ { t + \Delta t } , \mathcal { H } _ { t + \Delta t } , \mathcal { H } _ { t + \Delta t } \big ) .\tag{7}
$$

Subsequently, the second branch of the denoiser employs a DiT-based architecture to learn an action-conditioned flowmatching denoising process, using the BEV state $B _ { t } ^ { \prime }$ and the GT future action $\boldsymbol { A } _ { t + \Delta t }$ as conditions, as shown in Figure 3. The supervision is defined as:

$$
\mathcal { L } _ { F M } = | | \mathrm { D t T } _ { \theta } ( \boldsymbol { B } _ { t } ^ { \prime } , \boldsymbol { A } _ { t + \Delta t } , \boldsymbol { x } _ { k } , \frac { k } { N } ) - ( \boldsymbol { B } _ { t + \Delta t } ^ { \prime } - \boldsymbol { x } _ { 0 } ) | | ^ { 2 } ,\tag{8}
$$

where $\mathrm { D I T } = \mathrm { D E N O I S E R } ^ { 2 }$ denotes the second branch of the denoiser and $x _ { 0 } \sim \mathcal { N } ( \mathbf { 0 } , \mathbf { I } )$ , k represents timestep in the flow matching process and is uniformly sampled from the interval [1,N].

Supervision. In Action Controllablity Fine-Tuning stage, the overall loss $\mathcal { L } _ { s _ { 2 } }$ consists solely of the loss $\mathcal { L } _ { F M }$

## 3.3. Future-Guided Evaluation & Refinement

This stage aims to establish a closed-loop interaction between action prediction and future imagination based on the highly shared representation $\mathcal { H } _ { t }$ between the VLA and the world model. DriveWorld-VLA is required not only to predict actions but also to effectively imagine the corresponding future outcomes induced by those actions, and to evaluate and refine actions according to the imagined future states. Given the $B _ { t }$ , H<sub>t</sub> and $\mathcal { A } _ { t - 1 }$ , DriveWorld-VLA first predicts future actions $\boldsymbol { \mathcal { A } ^ { \prime } } _ { t + \Delta t }$ and generates future imagination $\boldsymbol { B } _ { t + \Delta t }$ via the first denoising branch. The predicted actions are subsequently used to condition the second denoising branch, where Euler-based sampling is performed to produce action-conditioned future imagination $B _ { t + \Delta t } ^ { \prime } \mathrm { : }$

$$
\mathcal { B } _ { t + \Delta t } ^ { k + 1 } = \mathcal { B } _ { t + \Delta t } ^ { k } + \frac { 1 } { N } ( \operatorname { D I T } _ { \theta } ( \mathcal { B } _ { t } ^ { \prime } , \mathcal { A } _ { t + \Delta t } , x _ { k } , \frac { k } { N } ) ) ,\tag{9}
$$

where $B _ { t + \Delta t } ^ { \prime } = B _ { t + \Delta t } ^ { k + 1 }$ , and N denotes the sampling steps and is set to 25.

To evaluate the quality of predicted actions, we jointly consider the consistency between the action-conditioned imagination $B _ { t + \Delta t } ^ { \prime }$ and the corresponding future BEV representation $\boldsymbol { B } _ { t + \Delta t }$ . A learned reward function R assigns a scalar score $\hat { r } _ { t + \Delta t }$ to each predicted trajectory, with ground-truth rewards obtained by executing the predicted trajectories in a simulator and performing online evaluation. This process can be formulated as,

$$
\hat { r } _ { t + \Delta t } = \mathcal { R } ( B _ { t + \Delta t } ^ { \prime } , B _ { t + \Delta t } , A _ { t + \Delta t } ^ { \prime } ) .\tag{10}
$$

Beyond trajectory quality assessment, this reward-driven design promotes close-loop between future imagination and action generation. Rather than uniformly supervising all multi-modal predictions, training prioritizes trajectories with higher predicted rewards, reinforcing those that lead to more favorable imagined outcomes and enabling consequence-aware action refinement,

$$
\begin{array} { r } { \boldsymbol { \mathcal { L } } _ { a c t } ^ { \prime } = \boldsymbol { \hat { r } } _ { t + \Delta t } \cdot \lVert \boldsymbol { \mathcal { A } } _ { t + \Delta t } ^ { \prime } - \boldsymbol { \mathcal { A } } _ { t + \Delta t } \rVert ^ { 2 } . } \end{array}\tag{11}
$$

Supervision. During this stage, DENOISER and VLM are frozen. Training focuses on refining the reward function and the action head. The future BEV latents generated by the two denoising branches are fused and fed into the segmentation decoder for supervised BEV decoding, resulting in three complementary supervision signals:

$$
\mathcal { L } _ { s _ { 3 } } = \mathcal { L } _ { a c t } ^ { \prime } + \mathcal { L } _ { s e g } + \mathcal { L } _ { r e w } ,\tag{12}
$$

where $\mathcal { L } _ { s e g }$ also supervises the semantic BEV map decoding, $\mathcal { L } _ { a c t } ^ { \prime }$ supervises the predicted actions weighted by rewards and $\mathcal { L } _ { r e w }$ supervises the reward function R.

## 4. Experiments

## 4.1. Details

Dataset and Metrics. We evaluate DriveWorld-VLA on NAVSIMv1 (Dauner et al., 2024), NAVSIMv2 (Cao et al., 2025) and nuScenes (Caesar et al., 2020). NAVSIMv1 is an autonomous driving planning benchmark built on the Open-Scene (Contributors, 2023) dataset, providing 120 hours of driving data at 2 Hz with multi-camera inputs and fused LiDAR point clouds. NAVSIMv1 adopts a non-reactive open-loop simulation protocol, where the core metric Predictive Driver Model Score (PDMS) is defined as the product of a penalty term and a weighted average score. The penalty term reflects constraint satisfaction such as No Collision (NC) and Drivable Area Compliance (DAC), while the weighted average combines Ego Progress (EP), Time-To-Collision (TTC), and Comfort (C) with weights of 5:5:2. NAVSIMv2 proposes a two-stage pseudo-simulation evaluation. Its core metric is called the Extended Predictive Driver Model Score (EPDMS), which is constructed from the following metrics: No at-fault Collision (NC), Drivable Area Compliance (DAC), Driving Direction Compliance (DDC), Traffic Light Compliance (TLC), Ego Progress (EP), Time to Collision (TTC), Lane Keeping (LK), History Comfort (HC), and Extended Comfort (EC). For open-loop planning, nuScenes is a large-scale outdoor driving dataset with 1000 multi-modal scenes. Each scene lasts 20 s, is annotated at 2 Hz, and includes six synchronized camera images and LiDAR point clouds. We use L2 and Collision Rate (CR) as evaluation metrics. See Appendix A for more details.

Implementation. For NAVSIM, we concatenate the leftfront view, front view, and right-front view in the order to form a 256×1024 composite image as the model input. We use ResNet-34 (He et al., 2016) as the BEV encoder. Training is performed with the AdamW optimizer using an initial learning rate of 1e-4 and a batch size of 16. Each stage is trained for 20 epochs on 8 NVIDIA H20 GPUs, with a total training time of approximately 120 hours. For the nuScenes open-loop evaluation, the 6-view input images are resized to 640×384. We adopt a Swin-T (Liu et al., 2021) backbone initialized with pretrained weights and follow BEV-Planner (Li et al., 2024d) to encode the BEV feature map. We train with AdamW using an initial learning rate of 7e-5 and a batch size of 1. Each stage is trained for 24 epochs on 8 NVIDIA H20 GPUs, for a total training time of approximately 93 hours. Note that, for a fair comparison, none of the nuScenes-based experiments uses ego-state information.

## 4.2. Main Results

NAVSIMv1. Table 1 reports the closed-loop planning performance on NAVSIMv1. Our DriveWorld-VLA achieves a PDMS of 91.3, outperforming top methods across different paradigms, including DiffusionDrive (Liao et al., 2025), WoTE (Li et al., 2025c), and DriveVLA-W0 (Li et al., 2025b). Notably, DriveWorld-VLA attains an NC of 99.1 and an EP of 85.9, suggesting that our policy effectively enforces safety constraints while sustaining efficient forward progress.

Table 1. Comparison with state-of-the-art methods on the NAVSIMv1 (Dauner et al., 2024). Abbreviations: 1×C (front single-view camera), N×C (surround multi-view cameras), L (LiDAR), NC (No Collision), DAC (Drivable Area Compliance), TTC (Time-To Collision), EP (Ego Process), C (Comfort), PDMS (Predictive Driver Model Score).
<table><tr><td>Methods</td><td>Venue</td><td>Sensors</td><td>NC↑</td><td>DAC↑</td><td>TTC↑</td><td>C↑</td><td>EP↑</td><td>PDMS↑</td></tr><tr><td>Human</td><td></td><td></td><td>100.0</td><td>100.0</td><td>100.0</td><td>99.9</td><td>87.5</td><td>94.8</td></tr><tr><td colspan="9">E2E-based Methods</td></tr><tr><td>TransFuser (Chitta et al., 2022)</td><td>TPAMI 2023</td><td>3×C + L</td><td>97.7</td><td>92.8</td><td>92.8</td><td>100.0</td><td>79.2</td><td>84.0</td></tr><tr><td>PARA-Drive (Weng et al., 2024)</td><td>CVPR 2024</td><td>6×C</td><td>97.9</td><td>92.4</td><td>93.0</td><td>99.8</td><td>79.3</td><td>84.0</td></tr><tr><td>Hydra-MDP (Li et al., 2024b)</td><td>arXiv 2024</td><td>3×C+L</td><td>98.3</td><td>96.0</td><td>94.6</td><td>100.0</td><td>78.7</td><td>86.5</td></tr><tr><td>DiffusionDrive (Liao et al., 2025)</td><td>CVPR 2025</td><td>3×C+L</td><td>98.2</td><td>96.2</td><td>94.7</td><td>100.0</td><td>82.2</td><td>88.1</td></tr><tr><td colspan="9">World-Model-based Methods</td></tr><tr><td>LAW (Li et al., 2024a)</td><td>ICLR 2024</td><td>1×C</td><td>96.4</td><td>95.4</td><td>88.7</td><td>99.9</td><td>81.7</td><td>84.6</td></tr><tr><td>DrivingGPT (Chen et al., 2025)</td><td>ICCV 2025</td><td>1×C</td><td>98.9</td><td>90.7</td><td>94.9</td><td>95.6</td><td>79.7</td><td>82.4</td></tr><tr><td>WoTE (Li et àl., 2025c)</td><td>ICCV 2025</td><td></td><td>98.5</td><td>96.8</td><td>94.4</td><td>99.9</td><td>81.9</td><td>88.3</td></tr><tr><td>Epona (Zhang et al., 2025)</td><td>ICCV 2025</td><td> $^ 3 { ^ 3 \times } _ { 3 \times } \mathrm { C } + \mathrm { L }$ </td><td>97.9</td><td>95.1</td><td>93.8</td><td>99.9</td><td>80.4</td><td>86.2</td></tr><tr><td colspan="9">VLA-based Methods</td></tr><tr><td>AutoVLA (Zhou et al., 2025c)</td><td>NeurIPS 2025</td><td>3×C</td><td>98.4</td><td>95.6</td><td>98.0</td><td>99.9</td><td>81.9</td><td>89.1</td></tr><tr><td>Recogdrive (Li et al., 2025d)</td><td>ICLR 2026</td><td>3×C</td><td>98.2</td><td>97.8</td><td>95.2</td><td>99.8</td><td>83.5</td><td>89.6</td></tr><tr><td>DriveVLA-W0 (Li et al., 2025b)</td><td>ICLR 2026</td><td>1×C</td><td>98.7</td><td>99.1</td><td>95.3</td><td>99.3</td><td>83.3</td><td>90.2</td></tr><tr><td>DriveWorld-VLA (Ours)</td><td></td><td>3×C</td><td>99.1</td><td>98.2</td><td>96.1</td><td>100.0</td><td>85.9</td><td>91.3</td></tr></table>

Table 2. Comparison with state-of-the-art methods on the NAVSIMv2 (Cao et al., 2025). Abbreviations: NC (No at-fault Collision), DAC (Drivable Area Compliance), DDC (Driving Direction Compliance), TLC (Traffic Light Compliance), EP (Ego Progress), TTC (Time to Collision), LK (Lane Keeping), HC (History Comfort), EC (Extended Comfort), EPDMS (Extended Predictive Driver Model Score).
<table><tr><td>Methods</td><td>NC↑</td><td>DAC↑</td><td>DDC↑</td><td>TLC↑</td><td>EP↑</td><td>TTC↑</td><td>LK↑</td><td>HC↑</td><td>EC↑</td><td>EPDMS↑</td></tr><tr><td>E2E-based Methods</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>TransFuser (Chitta et al., 2022)</td><td>96.9</td><td>89.9</td><td>97.8</td><td>99.7</td><td>87.1</td><td>95.4</td><td>92.7</td><td>98.3</td><td>87.2</td><td>76.7</td></tr><tr><td>DiffusionDrive (Liao et al., 2025)</td><td>98.2</td><td>95.9</td><td>99.4</td><td>99.8</td><td>87.5</td><td>97.3</td><td>96.8</td><td>98.3</td><td>87.7</td><td>84.5</td></tr><tr><td>HydraMDP++ (Li et al., 2025a)</td><td>97.2</td><td>97.5</td><td>99.4</td><td>99.6</td><td>83.1</td><td>96.5</td><td>94.4</td><td>98.2</td><td>70.9</td><td>81.4</td></tr><tr><td>Drivesuprim (Yao et al., 2025)</td><td>97.5</td><td>96.5</td><td>99.4</td><td>99.6</td><td>88.4</td><td>96.6</td><td>95.5</td><td>98.3</td><td>77.0</td><td>83.1</td></tr><tr><td>ARTEMIS (Feng et al., 2025a)</td><td>98.3</td><td>95.1</td><td>98.6</td><td>99.8</td><td>81.5</td><td>97.4</td><td>96.5</td><td>98.3</td><td></td><td>83.1</td></tr><tr><td>VLA-based Methods</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>DriveVLA-W0 (Li et al., 2025b)</td><td>98.5</td><td>99.1</td><td>98.0</td><td>99.7</td><td>86.4</td><td>98.1</td><td>93.2</td><td>97.9</td><td>58.9</td><td>86.1</td></tr><tr><td>DriveWorld-VLA (Ours)</td><td>98.6</td><td>99.1</td><td>99.6</td><td>99.8</td><td>87.4</td><td>97.9</td><td>97.0</td><td>97.8</td><td>78.6</td><td>86.8</td></tr></table>

NAVSIMv2. Table 2 reports the closed-loop planning performance on NAVSIMv2. DriveWorld-VLA achieves an EPDMS of 86.8, again outperforming all compared methods. Particularly, it performs excellently in DAC, DDC, and LK, achieving 99.1, 99.6, and 97.0, respectively.

nuScenes. Table 3 reports the 3-second planning results on the nuScenes (Caesar et al., 2020) validation dataset. The performance of recent methods suggests that short-horizon planning has been extensively studied. Compared with E2E-based methods and world-model-based methods, our DriveWorld-VLA demonstrates a clear advantage, achieving an average L2 of 0.61m and a collision rate as low as 0.16%. Even relative to the state-of-the-art approaches FSDrive (Zeng et al., 2025) and HERMES-p (Zhou et al., 2025b), DriveWorld-VLA still maintains a decisive advantage in terms of collision rate. These results indicate that the policy of DriveWorld-VLA is beneficial throughout the entire short-horizon planning process. We reiterate that ego-state information is disabled.

## 4.3. Ablation Study

Ablation on training process. Table 4 presents the performance of different stages of the DriveWorld-VLA training process across various datasets. For NAVSIMv1 (Dauner et al., 2024), each training stage significantly improves the model’s performance, with PDMS achieving increases of +1.9 and +1.8, respectively. For nuScenes (Caesar et al., 2020), the positive impact of Stage 2 is more pronounced. Short-term planning in the 2nd and 3rd seconds shows almost no improvement from Stage 3, with only -0.01 and -0.02 changes. We propose two hypotheses to explain this phenomenon. First, open-loop planning tasks do not necessarily benefit from generative supervision at all times. Second, the Reward Model has a greater effect on closed-loop planning than on open-loop planning. From an engineering perspective, DriveWorld-VLA uses different baselines (Li et al., 2025c; 2024a) and Reward Models across the two benchmarks. From a theoretical standpoint, the integration of generative tasks and planning tasks is constrained by the feedback mechanism within the inference process.

Table 3. Comparison with state-of-the-art methods on the nuScenes (Caesar et al., 2020) validation dataset. <sup>∗</sup> denotes results reproduced with the official checkpoint. Abbreviations: C (surround multi-view cameras), CR (Collision Rate).
<table><tr><td rowspan="2">Methods</td><td rowspan="2">Venue</td><td rowspan="2">Sensors</td><td colspan="4">L2(m)↓</td><td colspan="4">CR(%)↓</td></tr><tr><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td></tr><tr><td colspan="10">E2E-based Methods</td></tr><tr><td>UniAD (Hu et al., 2023)</td><td>CVPR 2023</td><td></td><td>0.48</td><td>0.96</td><td>1.65</td><td>1.03</td><td>0.05</td><td>0.17</td><td>0.71</td><td>0.31</td></tr><tr><td>VAD (Jiang et al., 2023)</td><td>ICCV 2023</td><td></td><td>0.41</td><td>0.70</td><td>1.05</td><td>0.72</td><td>0.07</td><td>0.17</td><td>0.41</td><td>0.22</td></tr><tr><td>MomAD (Song et al., 2025a)</td><td>CVPR 2025</td><td>CCC</td><td>0.43</td><td>0.88</td><td>1.62</td><td>0.98</td><td>0.06</td><td>0.16</td><td>0.68</td><td>0.30</td></tr><tr><td colspan="10"></td></tr><tr><td>World-Model-based Methods LAW* (Li et al., 2024a)</td><td></td><td></td><td></td><td></td><td></td><td></td><td>0.27</td><td></td><td></td><td>0.34</td></tr><tr><td>GenAD (Zheng et al., 2024)</td><td>ICLR 2024 ECCV 2024</td><td></td><td>0.31 0.36</td><td>0.61 0.83</td><td>1.02 1.55</td><td>0.65 0.91</td><td>0.06</td><td>0.21 0.23</td><td>0.54 1.00</td><td>0.43</td></tr><tr><td>Epona (Żhang et al., 2025)</td><td>ICCV 2025</td><td></td><td>0.61</td><td>1.17</td><td>1.98</td><td>1.25</td><td>0.01</td><td>0.22</td><td>0.85</td><td>0.36</td></tr><tr><td>FŠDrive (Zeng et al., 2025)</td><td>NeurIPS 2025</td><td>CCCC</td><td>0.28</td><td>0.52</td><td>0.80</td><td>0.53</td><td>0.06</td><td>0.13</td><td>0.32</td><td>0.17</td></tr><tr><td colspan="10">VLA-based Methods</td></tr><tr><td>HERMES-p (Zhou et al., 2025b)</td><td>ICCV 2025</td><td>C</td><td>0.16</td><td>0.32</td><td>0.59</td><td>0.36</td><td>0.00</td><td>0.14</td><td>0.82</td><td></td></tr><tr><td>DriveWorÍd-VLA (Ours)</td><td></td><td>C</td><td>0.28</td><td>0.58</td><td>0.99</td><td>0.61</td><td>0.00</td><td>0.10</td><td>0.38</td><td>0.32 0.16</td></tr></table>

Table 4. Ablation study of training process on NAVSIMv1 (Dauner et al., 2024) and nuScenes (Caesar et al., 2020) validation dataset.
<table><tr><td colspan="3">Training Process</td><td colspan="6">NAVSIMv1 (Closed-Loop)</td><td colspan="4">nuScenes (Open-Loop)</td></tr><tr><td>Stage 1</td><td>Stage 2</td><td>Stage 3</td><td>NC↑</td><td>DAC↑</td><td>TTC↑</td><td>C↑</td><td>EP↑</td><td>PDMS↑</td><td>CR↓@1s</td><td>CR↓@2s</td><td>CR↓@3s</td><td>CR↓@Avg.</td></tr><tr><td>×</td><td>X</td><td>X</td><td>98.5</td><td>95.8</td><td>94.4</td><td>99.9</td><td>80.9</td><td>87.1</td><td>0.27</td><td>0.21</td><td>0.54</td><td>0.34</td></tr><tr><td>√</td><td>×</td><td>X</td><td>98.6</td><td>96.1</td><td>95.1</td><td>99.9</td><td>81.0</td><td>87.6</td><td>0.09</td><td>0.19</td><td>0.48</td><td>0.25</td></tr><tr><td>√</td><td>√</td><td>×</td><td>98.9</td><td>97.3</td><td>94.4</td><td>100.0</td><td>84.5</td><td>89.5</td><td>0.05</td><td>0.11</td><td>0.40</td><td>0.19</td></tr><tr><td>√</td><td>√</td><td>√</td><td>99.1</td><td>98.2</td><td>96.1</td><td>100.0</td><td>85.9</td><td>91.3</td><td>0.00</td><td>0.10</td><td>0.38</td><td>0.16</td></tr></table>

Table 5. Ablation study of training strategies on NAVSIMv1 (Dauner et al., 2024). ‘Non-progressive’ denotes that Stage 2 and Stage 3 are trained simultaneously after the completion of Stage 1, while ‘Progressive’ denotes the strategy adopted in our work.
<table><tr><td>Training Strategies | NC↑</td><td></td><td>DAC↑</td><td>TTC↑</td><td>C↑</td><td>EP↑</td><td>PDMS↑</td></tr><tr><td>Non-progressive</td><td>97.8</td><td>94.5</td><td>93.5</td><td>99.9</td><td>75.6</td><td>83.6</td></tr><tr><td>Progressive</td><td>99.1</td><td>98.2</td><td>96.1</td><td>100.0</td><td>85.9</td><td>91.3</td></tr></table>

Table 6. Ablation study of VLM Strategies on NAVSIMv1 (Dauner et al., 2024). ‘Freeze’ denotes whether the parameters of VLM are also frozen during Stage 1. ‘Pre-train’ denotes whether the pre-training strategy aligned with RecogDrive (Li et al., 2025d) is adopted.
<table><tr><td colspan="2">VLM Strategies</td><td rowspan="2"></td><td rowspan="2">NC↑ DAC↑ TTC↑ C↑</td><td rowspan="2"></td><td rowspan="2"></td><td rowspan="2"></td><td rowspan="2">EP↑ PDMS↑</td></tr><tr><td>Freeze</td><td>Pre-train</td></tr><tr><td>√</td><td></td><td>98.4</td><td>95.7</td><td>96.2</td><td>99.9</td><td>80.4</td><td>87.2</td></tr><tr><td>√</td><td>X √</td><td>98.6</td><td>96.1</td><td>95.1</td><td>99.9</td><td>81.0</td><td>87.6</td></tr><tr><td>X</td><td>√</td><td>98.7</td><td>96.7</td><td>95.6</td><td>99.9</td><td>83.1</td><td>88.3</td></tr></table>

Ablation on training strategies. Table 5 shows the performance of DriveWorld-VLA under different training strategies. The ‘Non-progressive’ strategy refers to updating the parameters of both the future imagination branch and the action prediction branch after Stage 1, enabling the reward model, and using double the training length for a fair comparison. The ‘Progressive’ strategy follows the training scheme outlined in Figure 2. Clearly, the ‘Non-progressive strategy results in a significant performance drop, achieving -7.7 PDMS, which indicates that our strategy is effective and non-redundant. The model must first learn from the GT action and enhance the latent feature space before benefiting from action prediction. Additionally, this further demonstrates that even within the same feature space, generative and planning tasks need to be asynchronously unified.

Table 7. Ablation study of Supervision on NAVSIMv1 (Dauner et al., 2024).
<table><tr><td colspan="2">Supervision</td><td rowspan="2">NC↑</td><td rowspan="2">DAC↑</td><td rowspan="2">TTC↑</td><td rowspan="2">C↑</td><td rowspan="2">EP↑</td><td rowspan="2">PDMS↑</td></tr><tr><td>Task</td><td>Features</td></tr><tr><td>了</td><td>X</td><td>98.7</td><td>96.3</td><td>94.0</td><td>100.0</td><td>82.9</td><td>87.9</td></tr><tr><td></td><td>」</td><td>99.1</td><td>98.2</td><td>96.1</td><td>100.0</td><td>85.9</td><td>91.3</td></tr></table>

Ablation on VLM strategies. Table 6 shows the different VLM strategies used during the training of DriveWorld-VLA. ‘Freeze’ indicates whether the VLM parameters are frozen during Stage 1, and ‘Pre-Train’ indicates whether the VLM is pre-trained and fine-tuned following the settings in Recog-Drive (Li et al., 2025d) (conducting 3 epochs of SFT using the dataset constructed by the hierarchical data pipeline). The optimal strategy is shown in the third row of the table. Both omitting pre-training and fully freezing the VLM parameters limit the model’s performance. This indicates that while non-targeted pre-training can contribute, it does not fully unlock the VLM’s potential. The VLM parameters must undergo optimization through a learning process during the initial stage to accurately model shared space features and enhance the model’s performance. Considering the future need for lightweight design, we believe that completely abandoning VLM updates is also acceptable.

![](images/474b6d45c2e149c830a56c0c86ea4190b697437b28e3ee9071cc0a2e8cd4aaa4.jpg)  
Figure 4. The 4s trajectory planning visualization examples from NAVSIM (Dauner et al., 2024) for DriveWorld-VLA. Stage 2 generates predictions similar to the GTs, but with a higher collision risk. In contrast, Stage 3 introduces future imagination, resulting in more robust predictions and significantly reducing the collision risk. The changes observed across the training stages confirm the accuracy of world modeling and its understanding of physical dynamics. Left label: sample tokens. Top label: source of trajectory.

Ablation on Supervision. Table 7 shows the impact of task-level supervision and feature-level supervision on DriveWorld-VLA. Lseg and Lact are considered task-level supervision, while the supervision from the denoising process is considered feature-level supervision. We introduce noise that follows the distribution N(0, 5) into the latent variables during the inference phase, in order to mitigate the constraining effect of feature-level supervision. The results show that weakening feature-level supervision leads to a decline in model performance. Relying solely on task-level supervision causes the model to lack fine-grained feature guidance, which in turn affects performance.

## 4.4. Visualization

As shown in Figure 4, we provide some visual examples stemming from NAVSIM (Dauner et al., 2024) for DriveWorld-VLA. By the Figure, DriveWorld-VLA with three-stage training scheme empowered by future imagination demonstrates excellent and progressive planning results.

See Appendix B for more illustration samples (Figures S2- S6 for NAVSIM and Figures S7-S8 for nuScenes).

## 5. Conclusion

In this study, we introduce DriveWorld-VLA, a novel framework designed to enhance autonomous driving decisionmaking and forward-looking reasoning by tightly integrating VLA and world models. DriveWorld-VLA shares scene representations within the latent space, allowing the VLA to benefit more effectively from the world model. This integration enables direct access to global information regarding the future evolution of scenes, which is then applied to the decision-making process. Unlike existing approaches, DriveWorld-VLA uses the latent states of the world model as the basis for decision-making, assisting the system in evaluating the long-term impact of actions on future scenarios. We conduct extensive closed-loop and open-loop planning evaluations of DriveWorld-VLA across multiple benchmarks. The results demonstrate that DriveWorld-VLA significantly outperforms current state-of-the-art methods, showcasing its immense potential in decision-making.

## Impact Statement

This paper presents work aimed at advancing the field of end-to-end autonomous driving by integrating Vision-Language-Action (VLA) and World Models to enhance decision-making and forward-looking imagination. The datasets and references used in this work are publicly available, and the goal is to improve the safety of autonomous driving systems. We believe this work has positive societal implications, particularly in the context of autonomous vehicle technology, by contributing to safer transportation systems. Additionally, there are no specific ethical concerns that we feel must be highlighted here at this stage.

## References

Caesar, H., Bankiti, V., Lang, A. H., Vora, S., Liong, V. E., Xu, Q., Krishnan, A., Pan, Y., Baldan, G., and Beijbom, O. nuscenes: A multimodal dataset for autonomous driving. In Proceedings ofthe IEEE/CVF conference on computer vision and pattern recognition, pp. 11621–11631, 2020.

Cao, W., Hallgarten, M., Li, T., Dauner, D., Gu, X., Wang, C., Miron, Y., Aiello, M., Li, H., Gilitschenski, I., et al. Pseudo-simulation for autonomous driving. arXiv preprint arXiv:2506.04218, 2025.

Chen, Y., Wang, Y., and Zhang, Z. Drivinggpt: Unifying driving world modeling and planning with multimodal autoregressive transformers. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pp. 26890–26900, 2025.

Chitta, K., Prakash, A., Jaeger, B., Yu, Z., Renz, K., and Geiger, A. Transfuser: Imitation with transformer-based sensor fusion for autonomous driving. IEEE transactions on pattern analysis and machine intelligence, 45(11): 12878–12895, 2022.

Contributors, O. Openscene: The largest up-to-date 3d occupancy prediction benchmark in autonomous driving. In Proceedings of the Conference on Computer Vision and Pattern Recognition, Vancouver, Canada, pp. 18–22, 2023.

Cui, C., Ma, Y., Cao, X., Ye, W., Zhou, Y., Liang, K., Chen, J., Lu, J., Yang, Z., Liao, K.-D., et al. A survey on multimodal large language models for autonomous driving. In Proceedings of the IEEE/CVF Winter Conference on Applications ofComputer Vision, pp. 958–979, 2024.

Dauner, D., Hallgarten, M., Li, T., Weng, X., Huang, Z., Yang, Z., Li, H., Gilitschenski, I., Ivanovic, B., Pavone, M., et al. Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking. Advances in Neural Information Processing Systems, 37:28706–28719, 2024.

Feng, R., Xi, N., Chu, D., Wang, R., Deng, Z., Wang, A., Lu, L., Wang, J., and Huang, Y. Artemis: Autoregressive end-to-end trajectory planning with mixture of experts for autonomous driving. arXiv preprint arXiv:2504.19580, 2025a.

Feng, T., Wang, W., and Yang, Y. A survey of world models for autonomous driving. arXiv preprint arXiv:2501.11260, 2025b.

Gao, D., Cai, S., Zhou, H., Wang, H., Soltani, I., and Zhang, J. Cardreamer: Open-source learning platform for world model based autonomous driving. IEEE Internet ofThings Journal, 2024a.

Gao, S., Yang, J., Chen, L., Chitta, K., Qiu, Y., Geiger, A., Zhang, J., and Li, H. Vista: A generalizable driving world model with high fidelity and versatile controllability. Advances in Neural Information Processing Systems, 37: 91560–91596, 2024b.

Gu, S., Yin, W., Jin, B., Guo, X., Wang, J., Li, H., Zhang, Q., and Long, X. Dome: Taming diffusion model into high-fidelity controllable occupancy world model. arXiv preprint arXiv:2410.10429, 2024.

Guan, Y., Liao, H., Li, Z., Hu, J., Yuan, R., Li, Y., Zhang, G., and Xu, C. World models for autonomous driving: An initial survey. IEEE Transactions on Intelligent Vehicles, 2024.

Hao, X., Diao, Y., Wei, M., Yang, Y., Hao, P., Yin, R., Zhang, H., Li, W., Zhao, S., and Liu, Y. Mapfusion: A novel bev feature fusion network for multi-modal map construction. Information Fusion, 119:103018, 2025a.

Hao, X., Zhou, L., Huang, Z., Hou, Z., Tang, Y., Zhang, L., Li, G., Lu, Z., Ren, S., Meng, X., et al. Mimo-embodied: X-embodied foundation model technical report. arXiv preprint arXiv:2511.16518, 2025b.

He, K., Zhang, X., Ren, S., and Sun, J. Deep residual learning for image recognition. In Proceedings of the IEEE conference on computer vision and pattern recognition, pp. 770–778, 2016.

Hu, A., Corrado, G., Griffiths, N., Murez, Z., Gurau, C., Yeo, H., Kendall, A., Cipolla, R., and Shotton, J. Model-based imitation learning for urban driving. Advances in Neural Information Processing Systems, 35:20703–20716, 2022.

Hu, Y., Yang, J., Chen, L., Li, K., Sima, C., Zhu, X., Chai, S., Du, S., Lin, T., Wang, W., et al. Planning-oriented autonomous driving. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pp. 17853–17862, 2023.

Jia, F., Jia, C., Song, Z., Bao, Z., Liu, L., Xu, S., Gong, Y., Yang, L., Zhang, X., Sun, B., et al. Progressive robustnessaware world models in autonomous driving: A review and outlook. Authorea Preprints, 2025.

Jiang, A., Gao, Y., Sun, Z., Wang, Y., Wang, J., Chai, J., Cao, Q., Heng, Y., Jiang, H., Dong, Y., et al. Diffvla: Visionlanguage guided diffusion planning for autonomous driving. arXiv preprint arXiv:2505.19381, 2025.

Jiang, B., Chen, S., Xu, Q., Liao, B., Chen, J., Zhou, H., Zhang, Q., Liu, W., Huang, C., and Wang, X. Vad: Vectorized scene representation for efficient autonomous driving. In Proceedings ofthe IEEE/CVF International Conference on Computer Vision, pp. 8340–8350, 2023.

Li, K., Li, Z., Lan, S., Xie, Y., Zhang, Z., Liu, J., Wu, Z., Yu, Z., and Alvarez, J. M. Hydra-mdp++: Advancing end-to-end driving via expert-guided hydra-distillation. arXiv preprint arXiv:2503.12820, 2025a.

Li, Y., Fan, L., He, J., Wang, Y., Chen, Y., Zhang, Z., and Tan, T. Enhancing end-to-end autonomous driving with latent world model. arXiv preprint arXiv:2406.08481, 2024a.

Li, Y., Shang, S., Liu, W., Zhan, B., Wang, H., Wang, Y., Chen, Y., Wang, X., An, Y., Tang, C., et al. Drivevla-w0: World models amplify data scaling law in autonomous driving. arXiv preprint arXiv:2510.12796, 2025b.

Li, Y., Wang, Y., Liu, Y., He, J., Fan, L., and Zhang, Z. Endto-end driving with online trajectory evaluation via bev world model. arXiv preprint arXiv:2504.01941, 2025c.

Li, Y., Xiong, K., Guo, X., Li, F., Yan, S., Xu, G., Zhou, L., Chen, L., Sun, H., Wang, B., et al. Recogdrive: A reinforced cognitive framework for end-to-end autonomous driving. arXiv preprint arXiv:2506.08052, 2025d.

Li, Z., Li, K., Wang, S., Lan, S., Yu, Z., Ji, Y., Li, Z., Zhu, Z., Kautz, J., Wu, Z., et al. Hydra-mdp: End-to-end multimodal planning with multi-target hydra-distillation. arXiv preprint arXiv:2406.06978, 2024b.

Li, Z., Wang, W., Li, H., Xie, E., Sima, C., Lu, T., Yu, Q., and Dai, J. Bevformer: learning bird’s-eye-view representation from lidar-camera via spatiotemporal transformers. IEEE Transactions on Pattern Analysis and Machine Intelligence, 2024c.

Li, Z., Yu, Z., Lan, S., Li, J., Kautz, J., Lu, T., and Alvarez, J. M. Is ego status all you need for open-loop end-to-end autonomous driving? In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pp. 14864–14873, 2024d.

Liao, B., Chen, S., Yin, H., Jiang, B., Wang, C., Yan, S., Zhang, X., Li, X., Zhang, Y., Zhang, Q., et al. Diffusiondrive: Truncated diffusion model for end-to-end autonomous driving. In Proceedings of the Computer Vision and Pattern Recognition Conference, pp. 12037–12047, 2025.

Liu, L., Jia, C., Yu, G., Song, Z., Li, J., Jia, F., Wu, P., Hao, X., and Luo, Y. Guideflow: Constraint-guided flow matching for planning in end-to-end autonomous driving. arXiv preprint arXiv:2511.18729, 2025.

Liu, Z., Lin, Y., Cao, Y., Hu, H., Wei, Y., Zhang, Z., Lin, S., and Guo, B. Swin transformer: Hierarchical vision transformer using shifted windows. In Proceedings of the IEEE/CVF international conference on computer vision, pp. 10012–10022, 2021.

Min, C., Zhao, D., Xiao, L., Zhao, J., Xu, X., Zhu, Z., Jin, L., Li, J., Guo, Y., Xing, J., et al. Driveworld: 4d pre-trained scene understanding via world models for autonomous driving. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pp. 15522–15533, 2024.

Renz, K., Chen, L., Arani, E., and Sinavski, O. Simlingo: Vision-only closed-loop autonomous driving with language-action alignment. In Proceedings of the Computer Vision and Pattern Recognition Conference, pp. 11993–12003, 2025.

Shao, H., Hu, Y., Wang, L., Song, G., Waslander, S. L., Liu, Y., and Li, H. Lmdrive: Closed-loop end-to-end driving with large language models. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pp. 15120–15130, 2024.

Song, Z., Jia, C., Liu, L., Pan, H., Zhang, Y., Wang, J., Zhang, X., Xu, S., Yang, L., and Luo, Y. Don’t shake the wheel: Momentum-aware planning in end-to-end autonomous driving. In Proceedings ofthe Computer Vision and Pattern Recognition Conference, pp. 22432–22441, 2025a.

Song, Z., Liu, L., Pan, H., Liao, B., Guo, M., Yang, L., Zhang, Y., Xu, S., Jia, C., and Luo, Y. Diver: Reinforced diffusion breaks imitation bottlenecks in end-to-end autonomous driving. arXiv preprint arXiv:2507.04049, 2025b.

Tu, S., Zhou, X., Liang, D., Jiang, X., Zhang, Y., Li, X., and Bai, X. The role of world models in shaping autonomous driving: A comprehensive survey. arXiv preprint arXiv:2502.10498, 2025.

Wang, H., Ye, X., Tao, F., Pan, C., Mallik, A., Yaman, B., Ren, L., and Zhang, J. Adawm: Adaptive world model

based planning for autonomous driving. arXiv preprint arXiv:2501.13072, 2025.

Weng, X., Ivanovic, B., Wang, Y., Wang, Y., and Pavone, M. Para-drive: Parallelized architecture for real-time autonomous driving. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pp. 15449–15458, 2024.

Xu, T., Lu, H., Yan, X., Cai, Y., Liu, B., and Chen, Y. Occ-llm: Enhancing autonomous driving with occupancy-based large language models. arXiv preprint arXiv:2502.06419, 2025.

Xu, Z., Zhang, Y., Xie, E., Zhao, Z., Guo, Y., Wong, K.- Y. K., Li, Z., and Zhao, H. Drivegpt4: Interpretable end-to-end autonomous driving via large language model. IEEE Robotics and Automation Letters, 2024.

Yan, T., Tang, T., Gui, X., Li, Y., Zhesng, J., Huang, W., Kong, L., Han, W., Zhou, X., Zhang, X., et al. Adr1: Closed-loop reinforcement learning for end-to-end autonomous driving with impartial world models. arXiv preprint arXiv:2511.20325, 2025.

Yang, J., Chitta, K., Gao, S., Chen, L., Shao, Y., Jia, X., Li, H., Geiger, A., Yue, X., and Chen, L. Resim: Reliable world simulation for autonomous driving. arXiv preprint arXiv:2506.09981, 2025a.

Yang, Z., Chen, L., Sun, Y., and Li, H. Visual point cloud forecasting enables scalable autonomous driving. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pp. 14673–14684, 2024.

Yang, Z., Chai, Y., Jia, X., Li, Q., Shao, Y., Zhu, X., Su, H., and Yan, J. Drivemoe: Mixture-of-experts for visionlanguage-action model in end-to-end autonomous driving. arXiv preprint arXiv:2505.16278, 2025b.

Yao, W., Li, Z., Lan, S., Wang, Z., Sun, X., Alvarez, J. M., and Wu, Z. Drivesuprim: Towards precise trajectory selection for end-to-end planning. arXiv preprint arXiv:2506.06659, 2025.

Zeng, S., Chang, X., Xie, M., Liu, X., Bai, Y., Pan, Z., Xu, M., and Wei, X. Futuresightdrive: Thinking visually with spatio-temporal cot for autonomous driving. arXiv preprint arXiv:2505.17685, 2025.

Zhang, K., Tang, Z., Hu, X., Pan, X., Guo, X., Liu, Y., Huang, J., Yuan, L., Zhang, Q., Long, X.-X., et al. Epona: Autoregressive diffusion world model for autonomous driving. arXiv preprint arXiv:2506.24113, 2025.

Zhang, L., Xiong, Y., Yang, Z., Casas, S., Hu, R., and Urtasun, R. Copilot4d: Learning unsupervised world models for autonomous driving via discrete diffusion. arXiv preprint arXiv:2311.01017, 2023.

Zheng, W., Song, R., Guo, X., Zhang, C., and Chen, L. Genad: Generative end-to-end autonomous driving. In European Conference on Computer Vision, pp. 87–104. Springer, 2024.

Zheng, Y., Yang, P., Xing, Z., Zhang, Q., Zheng, Y., Gao, Y., Li, P., Zhang, T., Xia, Z., Jia, P., et al. World4drive: Endto-end autonomous driving via intention-aware physical latent world model. arXiv preprint arXiv:2507.00603, 2025.

Zhou, X., Han, X., Yang, F., Ma, Y., Tresp, V., and Knoll, A. Opendrivevla: Towards end-to-end autonomous driving with large vision language action model. arXiv preprint arXiv:2503.23463, 2025a.

Zhou, X., Liang, D., Tu, S., Chen, X., Ding, Y., Zhang, D., Tan, F., Zhao, H., and Bai, X. Hermes: A unified self-driving world model for simultaneous 3d scene understanding and generation. arXiv preprint arXiv:2501.14729, 2025b.

Zhou, Z., Cai, T., Zhao, S. Z., Zhang, Y., Huang, Z., Zhou, B., and Ma, J. Autovla: A vision-language-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning. arXiv preprint arXiv:2506.13757, 2025c.

Zhu, J., Wang, W., Chen, Z., Liu, Z., Ye, S., Gu, L., Tian, H., Duan, Y., Su, W., Shao, J., et al. Internvl3: Exploring advanced training and test-time recipes for open-source multimodal models. arXiv preprint arXiv:2504.10479, 2025.

Zyrianov, V., Che, H., Liu, Z., and Wang, S. Lidardm: Generative lidar simulation in a generated world. In 2025 IEEE International Conference on Robotics and Automation (ICRA), pp. 6055–6062. IEEE, 2025.

## A. More Experiment Details.

## A.1. Prompt

In the system prompt for InternVL (Zhu et al., 2025), we include a description of the task, metrics, input and output.   
Figure S1 is an example for the two benchmarks (Dauner et al., 2024; Cao et al., 2025; Caesar et al., 2020).

## A.2. Image Tokens

We explicitly inject visual information into the input sequence in the form of a ‘text-domain visual placeholder token sequence’. Given an input image (after view stitching), we first perform adaptive tiling to accommodate varying aspect ratios. Where the image is partitioned into $N _ { P }$ feature patches of size $4 4 8 \times 4 4 8$ . When multiple patches are used, an additional $4 4 8 \times 4 4 8$ thumbnail is appended to provide a global view. We then insert the textual prompts into a placeholder span delimited by special boundary markers $( \mathrm { e . g . } , < \mathrm { i } \mathrm { m g } > . ~ . ~ . < / \mathrm { i } \mathrm { m g } > )$ , within which a dedicated placeholder token <IMG CONTEXT> is repeated. We assign a fixed number of $K = 2 5 6 < \mathrm { I M G \_ C O N T E X T > }$ tokens to each patch. This design ensures that variations in image resolution or the number of patches are directly reflected in the number of text-side image tokens, while the overall sequence is subsequently tokenized and padded to a fixed maximum length.

## A.3. Vision-language Representation

On the vision side, we stack the normalized patches into a tensor in $\mathbb { R } ^ { P \times 3 \times 4 4 8 \times 4 4 8 }$ , together with an accompanying mask that indicates which patches are valid. During multi-modal fusion, the model first locates all occurrences of <IMG CONTEXT> in the text indices, and then applies a visual encoder to extract per-patch features and project them into the language hidden space. The resulting visual features and language tokens are jointly processed by the backbone network. This yields fused sequence hidden states $\mathbf { H } \in \mathbb { R } ^ { B \times L \times D }$ , where L denotes the maximum tokenized sequence length and D is the language backbone hidden dimension. The representation thus captures both textual context and visual information carried at the $< \mathrm { I M G \_ C O N T E X T } >$ positions. To obtain a fixed-length compact representation, we first linearly project the fused hidden states from $D = 1 5 3 6$ to a lower dimension $d = 2 5 6$ , producing $\tilde { \mathbf { H } } \in \mathbb { R } ^ { B \times L \times d }$ . We then introduce a set of learnable latent query vectors ${ \bf Z } _ { 0 } \in \mathbb { R } ^ { B \times N _ { L } \times d }$ , where we set the number of latents to $N _ { L } = 7 0 0$ . Using cross-attention with $\mathbf { Z } _ { 0 }$ as queries and H<sup>˜</sup> as keys/values, we aggregate information from a variable-length sequence into a fixed-length representation $\mathbf { Z } \in \mathbb { R } ^ { B \times N _ { L } \times d }$ , which serves as a compact vision–language representation for downstream tasks.

## B. More Visualization.

We have provided more visual examples showed in Figure S2, Figure S3, Figure S4, Figure S5 and Figure S6 for NAVSIM (Dauner et al., 2024), as well as Figure S7, Figure S8 for nuScenes (Caesar et al., 2020).

![](images/102e848ef2f9c5f538f7fe7d21cf1dbd5718a39e172d23e06dc823da3a05008f.jpg)  
Figure S1. InternVL system prompts. $\{ { \tt h i s t o r y } _ { - } \mathrm { s t r } \}$ denotes the ground-truth historical trajectory sequence, where each frame in the sequence is represented by a 2D coordinate. {command str} denotes navigation commands in text form, e.g., ‘turn left’, ‘go straight’ or ‘turn right’. The full prompt fed into the model is composed of each benchmark’s specific prompt and the common prompt.

![](images/98114ddeecd3c65daf06ac2ee4ab842650ec240d1bc19299176c9a4a270cdc97.jpg)  
Figure S2. Visualization examples of NAVSIM (Dauner et al., 2024). Left label: sample tokens. Top label: source of trajectory.

![](images/4887d8c7b518ae672c16525f88d5ab74facab46c9ebe2d039c77ffff4fa7cf14.jpg)  
Figure S3. Visualization examples (cont.) of NAVSIM (Dauner et al., 2024). Left label: sample tokens. Top label: source of trajectory.

![](images/ab8ac3a16f56c4163955c74d09a6e14483b0e74814e99a67f11d8005f509a7e2.jpg)  
Figure S4. Visualization examples (cont.) of NAVSIM (Dauner et al., 2024). Left label: sample tokens. Top label: source of trajectory.

![](images/e71333690abca316106da78d091f80b6e091895bd5b1394cc2be737c2e608a4a.jpg)  
Figure S5. Visualization examples (cont.) of NAVSIM (Dauner et al., 2024). Left label: sample tokens. Top label: source of trajectory.

![](images/99513dbe2b76e7e90767f331cff0c5546aeddc6ad0983533c01f2048665110ba.jpg)  
Figure S6. Visualization examples (cont.) of NAVSIM (Dauner et al., 2024). Left label: sample tokens. Top label: source of trajectory.

![](images/50c7770062759d7dba86da8f144b201e8e0a5cab6dbd539b69bc9e30dadefcda.jpg)  
Figure S7. Visualization examples of nuScenes (Caesar et al., 2020) validation dataset. Top label: source of trajectory.

6-view Camera  
Stage 3  
![](images/0bd38a4dda66adc4f17afe1285ba1eab332521c2b01fa92271889df85ce6e8fb.jpg)  
Figure S8. Visualization examples (cont.) of nuScenes (Caesar et al., 2020) validation dataset. Top label: source of trajectory.