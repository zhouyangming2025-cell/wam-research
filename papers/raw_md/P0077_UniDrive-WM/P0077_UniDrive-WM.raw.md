# UniDrive-WM: Unified Understanding, Planning and Generation World Model for Autonomous Driving

Zhexiao Xiong<sup>1,2⋆</sup>, Xin Ye<sup>1</sup>, Burhan Yaman<sup>1</sup>, Sheng Cheng<sup>3</sup>, Yiren Lu<sup>1,4</sup>, Jingru Luo<sup>1</sup>, Nathan Jacobs<sup>2</sup>, and Liu Ren<sup>1</sup>

<sup>1</sup> Bosch Research North America & Bosch Center for Artificial Intelligence (BCAI) <sup>2</sup> Washington University in St. Louis <sup>3</sup> Arizona State University Case Western Reserve University

![](images/bfdb3f1668e81328420e87b31ee9f4ee94dce3682f7719c6867f99ab8637e489.jpg)  
Fig. 1: Top Left: trajectory-conditioned visual generation. Top Right: VLM-instructed E2E Planning. Bottom: our unified future world modeling method. Compared with conditioned future image generation models and VLM-instructed planning method, our framework establishes the connection among the reasoning, action and visual generation spaces via joint VLM-guided trajectory planner and future frame generation.

Abstract. World models have become central to autonomous driving, where accurate scene understanding and future prediction are crucial for safe control. Recent work has explored using vision–language models (VLMs) for planning, yet existing approaches typically treat perception, prediction, and planning as separate modules. We propose UniDrive-WM, a unified VLM-based world model that jointly performs drivingscene understanding, trajectory planning, and trajectory-conditioned future image generation within a single architecture. UniDrive-WM’s trajectory planner predicts a future trajectory, which conditions a VLMbased image generator to produce plausible future frames. These predictions provide additional supervisory signals that enhance scene understanding and iteratively refine trajectory generation. We further compare

discrete and continuous output representations for future image prediction, analyzing their influence on downstream driving performance. Experiments on the challenging Bench2Drive benchmark show that UniDrive WM produces high-fidelity future images and improves planning performance by 7.3% in L2 trajectory error and 10.4% in collision rate over the previous best method. These results demonstrate the advantages of tightly integrating VLM-driven reasoning, planning, and generative world modeling for autonomous driving. The project page is available at https://unidrive-wm.github.io/UniDrive-WM.

Keywords: World Models · VLM · Autonomous Driving

## 1 Introduction

Recent progress in multimodal large language models (MLLMs) has been propelled by the strong perception, reasoning, and instruction-following capabilities of vision–language models (VLMs). In parallel, visual generation has advanced along two complementary lines: autoregressive (AR) token prediction and difusion-based continuous generation—enabling high-fidelity image synthesis across diverse tasks. Motivated by these trends, a growing body of unified models seeks to couple understanding and generation within a single VLM, allowing the system to “think and generate” in a shared semantic space [5, 28, 55].

In autonomous driving, world models [35, 66, 66] are typically defined as learned models that infer a latent representation of the current scene and predict future states conditioned on actions, ideally enabling robust planning and control. While several VLM-based approaches have been explored, many rely on text-only intermediates, first producing natural-language descriptions of future trajectories or scenes, and then invoking a separate stage to decode trajectories or render images. This pipeline introduces an information bottleneck: rich visual–geometric cues are abstracted into text, incurring inevitable loss and compounding errors across stages. Meanwhile, generative models can generate visually plausible frames, but they typically lack explicit state estimation and reasoning. In particular, they do not maintain structured representations of the scene and cannot reliably condition on multi-view cues or high-level instructions, which provides no diferentiable bridge to the action space for verifiable planning. Consequently, they struggle to answer causal queries (e.g., “what if the pedestrian accelerates?”), to enforce safety constraints, or to propagate plan-consistent signals back into perception. In reality, a driver’s cognition is inherently joint: perceive the current scene, anticipate the future trajectory, and imagine the next visual scene. This motivates a unified formulation in which understanding, planning, and visual prediction are learned end-to-end within a single VLM framework, allowing information to flow bidirectionally between reasoning, action, and generation.

We present UniDrive-WM, a unified world model that jointly performs scene understanding, trajectory planning, and future image generation within a VLM-centric architecture. As illustrated in Fig. 1, multi-view observations, temporal history, and perception cues (e.g., subject bounding boxes) are encoded and projected into an LLM reasoning space. A trajectory planner then produces a diferentiable latent distribution over waypoints, bridging the reasoning (language–vision) space and the numeric action space. Conditioning on the predicted trajectory, UniDrive-WM further performs trajectory-conditioned future image prediction via two complementary designs: (i) a discrete AR pathway that expands the visual codebook and detokenizes with MoVQGAN, and (ii) an AR+difusion pathway that predicts continuous latent features with a flow-matching objective before pixel decoding. This design alleviates text-only bottlenecks and enables bidirectional coupling—both information flow and gradient flow—between reasoning, action, and generation. Extensive experiments on the challenging Bench2Drive and nuScenes datasets show that UniDrive-WM generates high-fidelity future image frames and outperforms counterpart methods on planning tasks across both open-loop and closed-loop metrics.

Our main contributions are summarized as follows:

– We present UniDrive-WM, a unified vision–language world model (VLM) that seamlessly integrates scene understanding, trajectory planning, and future image generation, enabling direct visual reasoning from spatio–temporal observations.

– We develop and analyze two complementary decoding paradigms for trajectoryconditioned future image prediction: a discrete autoregressive (AR) pathway and a continuous AR+difusion pathway, revealing their respective advantages and trade-ofs for autonomous driving.

– Extensive experiments demonstrate that our unified framework achieves high-fidelity, planning-conditioned visual generation and significantly improves both planning accuracy and perception performance on standard driving benchmarks, verifying the efectiveness of the proposed framework.

## 2 Related Work

World Models for Autonomous Driving. The commonly accepted description of world models is understanding the current state and predicting the future state. For autonomous driving tasks, recent world-modeling-based methods aim to infer the ego status and dynamic environments from past observations to enable future planning and prediction, reducing human control in autonomous driving systems. Existing methods can be broadly categorized by their output modality: some focus on visual scene generation or urban view synthesis [13, 14, 15, 17, 58], others emphasize future trajectory planning, including difusion-based planning [12, 30, 32, 54], while several works address 3D scene reconstruction and simulation in the form of occupancy [34, 43, 48], LiDAR [36, 47, 51, 68], or point clouds [59, 60]. However, most of these approaches focus on a single prediction modality. Recent world models have also been studied for visual navigation [8, 9] and driver-centric dynamics rollout [6]. In contrast, our model jointly performs trajectory planning and future image generation within a unified world-model framework, coupling planned motion with predicted visual futures under a shared VLM backbone.

Unified Image Understanding and Generation. Recent studies have emphasized the importance of unifying image understanding and image generation within a single framework. Early works such as Chameleon [40], Show-o [52], Transfusion [67], and Janus [49] adopt discrete visual representations and treat visual synthesis as autoregressive token prediction, where images are quantized into discrete tokens analogous to text, enabling LLMs to interpret and generate visual content in a unified token space. More recent models, including Metamorph [42] and the BLIP-3o family [3, 4], integrate autoregressive generation with difusion-based continuous decoding, often relying on additional visual encoders such as CLIP [37] or SigLIP [57] to enhance visual understanding. In contrast to these general-purpose unified models, our work advances this paradigm in the autonomous driving domain by jointly predicting future frames and planning trajectories within a single VLM-based world model.

Vision–Language–Action Models. Recently, large vision–language–action (VLA) models have emerged as powerful frameworks for embodied decisionmaking. Built upon pretrained multimodal large language models (MLLMs), these systems typically predict future actions through either discrete action decoders [2, 26, 61] or continuous difusion-based policy heads [16, 29]. By leveraging large-scale and diverse training corpora, MLLMs provide strong semantic grounding and generalization capabilities for downstream embodied tasks. Recent driving-oriented $\mathrm { { V L A } } _ { \prime }$ /action models further explore video-action priors and geometry-aware action modeling for autonomous driving [33, 53]. In the autonomous driving setting, we treat ego-vehicle trajectories as the continuous action representation. Unlike standard manipulation or navigation environments, however, driving scenes are highly dynamic and visually complex, requiring the VLM to integrate richer contextual information—including temporal history, perception features, and multi-view observations to generate reliable and sceneconsistent trajectory plans.

## 3 Method

In this section, we present our unified understanding, generation and planning framework for autonomous driving. The pipeline is shown in Fig. 2. We begin with the formulation of our method, followed by a detailed analysis of the system architecture. We then analyze the model architecture for planning and image generation. For image generation, we explore both (1) autoregressive image generation in a discrete visual representation and (2) difusion-based generation in a continuous visual representation, and discuss their performance and impact on autonomous driving tasks. The task is defined as jointly predicting the future scene state and planning trajectory:

$$
\begin{array} { r } { \{ \hat { \mathbf { s } } _ { t + n } , \hat { \mathbf { a } } _ { t : t + m } \} \sim P _ { \theta } \big ( \mathbf { s } _ { 1 : t } , \mathbf { a } _ { 1 : t - 1 } , l \big ) , } \end{array}\tag{1}
$$

![](images/ce3b80800d473139324f0d1ba944b42c0e0f44f7accf144831141b94bf4f5792.jpg)  
Fig. 2: The pipeline of our UniDrive-WM framework. The pipeline consists of: (1) a QT-Former-based encoder to extract historical context and multi-view visual input; (2) the LLM for performing a reasoning task; and (3) the output layer, which generates the planning trajectory and future image prediction and bridges the gaps between the planning space, image space and reasoning space. For the output layer, we provide a detailed analysis in Fig. 3.

which can be further decomposed as:

$$
\begin{array} { r l r } & { } & { \left\{ \hat { \bf a } _ { t } , \ldots , \hat { \bf a } _ { t + m } \right\} \sim P _ { \theta } ( \left\{ { \bf a } _ { t } , \ldots , { \bf a } _ { t + m } \right\} \mid { \bf s } _ { t } , l ) , } \\ & { } & { \hat { \bf s } _ { t + n } \sim P _ { \theta } ( { \bf s } _ { t + n } \mid { \bf s } _ { t } , \hat { \bf a } _ { t } , \ldots , \hat { \bf a } _ { t + m } , l ) , \quad } \end{array}\tag{2}
$$

where $\mathbf { s } _ { t }$ represents the multi-modal state information at time $t ,$ including multiview images, historical context, and perception features; the model predicts the future front-view image $\hat { \mathbf { I } } _ { t + n }$ as part of the future state $\hat { \bf s } _ { t + n } ,$ and $\mathbf { a } _ { t + m }$ denotes the predicted trajectory waypoint at time $t + m ; l$ is the high-level language or instruction condition. The model therefore aims to jointly reason about the future world state and plan consistent trajectories under a unified vision–language world model.

## 3.1 Vision Language Model

A key component of a world model is understanding the current state and predicting the future state. Therefore, leveraging the Vision Language Model’s reasoning and understanding ability, UniDrive-WM understands the current scene and instructs the trajectory planner and image generation module. We build our model upon ORION [12], a VLM-based model for the autonomous driving planning task.

Vision Encoder For the vision encoder, we adopt the QT-Former used by previous methods [12]. Specifically, two sets of learnable queries are processed through self-attention (SA) to exchange information and interact with image features $F _ { m }$ with 3D positional encoding in the cross-attention module. After that, the perception queries are fed into multiple auxiliary heads for object detection, including critical objects, lanes, trafic states and motion prediction of dynamic objects. Additionally, we use a set of history queries $Q _ { h } \in \mathbb { R } ^ { ( N _ { h } \times C _ { q } ) }$ where $N _ { h }$ denotes the number of history queries and $C _ { q }$ represents the feature dimension, and a memory bank $M \in \mathbb { R } ^ { ( N _ { h } \times n ) \times C _ { q } }$ to retrieve and store historical information from the past n frames. The QT-Former is formulated as:

$$
\begin{array} { r } { Q _ { h } = \mathrm { C A } \left( Q _ { h } , M + P _ { t } , M + P _ { t } \right) , \quad \hat { Q } _ { h } = \mathrm { C A } \left( Q _ { h } , Q _ { s } , Q _ { s } \right) . } \end{array}\tag{3}
$$

where CA denotes the Cross-Attention operation, and $P _ { t }$ denotes the relative timestamp embedding at the current timestep t. The updated history queries $\hat { Q } _ { h }$ are stored in the memory bank M, formulated as:

$$
M = \left[ \hat { Q } _ { h } ^ { t - n + 1 } , \cdots , \hat { Q } _ { h } ^ { t - 1 } , \hat { Q } _ { h } ^ { t } \right]\tag{4}
$$

Finally, a two-layer Multi-layer Perceptron (MLP) is used to convert the updated history queries $\hat { Q } _ { h }$ and current scene features $Q _ { s }$ to history tokens $x _ { h }$ and scene tokens $x _ { s }$ in the reasoning space of the LLM.

Large Language Model. The large language model (LLM) serves as the reasoning core of our framework, enabling text-based understanding and high-level reasoning tasks such as scene description, visual question answering, and action reasoning. We fine-tune the LLM using LoRA [18] to eficiently adapt it to domain-specific reasoning and instruction-following within autonomous driving scenarios.

## 3.2 Trajectory Planner

The trajectory planner establishes a diferentiable connection between the semantic reasoning space of the VLM and the numerical action space of trajectory prediction through distribution learning in a latent space. We formulate trajectory generation as a conditional distribution problem, where the planner models a multi-modal distribution over future trajectories conditioned on high-level reasoning embeddings from the VLM:

$$
p _ { \theta } ( \mathbf { a } _ { t : t + m } \mid \mathbf { s } _ { t } , \mathbf { h } _ { \mathrm { V L M } } ) ,\tag{5}
$$

where $\mathbf { a } _ { t : t + m }$ denotes the predicted trajectory waypoints, $\mathbf { s } _ { t }$ represents the current state embedding, and h<sub>VLM</sub> denotes the high-level reasoning embedding (hidden representation) extracted from the VLM, which encodes the fused multiview observations, temporal history, and textual instructions. A latent variable ${ \bf z } _ { a }$ is introduced to capture the stochasticity of future motion in a Gaussian latent space, and the planner learns to decode diverse yet semantically consistent trajectories from ${ \bf z } _ { a }$ . In practice, we omit the explicit KL regularization term used in conventional VAE objectives, as we empirically find it may destabilize training in large-scale multimodal setups. This design provides a stable and differentiable bridge between language-based reasoning and continuous trajectory prediction.

## 3.3 Future Image Generation

Since driving scenes are continuous in nature, autonomous driving datasets naturally contain dense future frames, allowing us to leverage abundant video data to improve image generation quality. Inspired by recent advances in unifying image understanding and generation, we adopt two diferent image generation architectures for future image prediction, as illustrated in Fig. 3. We discuss the design choices involved in building the understanding, planning, and image generation modules within a unified VLM framework, and analyze their impact on planning performance.

![](images/f9d735c0a78591f0b4fab09e51ec4584e0b481d809b98ae3f54f3fd9e71a40d0.jpg)  
Fig. 3: The two design choices for image generation in a unified multimodal model. For future image prediction, we use both Autoregressive and Autoregressive+Difusion architectures. (a) Left: Autoregressive architecture; (b) Right: AR+Difusion architecture.

Formally, the future image prediction task can be formulated as:

$$
p _ { \theta } ( \hat { \mathbf { I } } _ { t + n } \mid \mathbf { s } _ { t } , \mathbf { h } _ { \mathrm { V L M } } ) ,\tag{6}
$$

where $\mathbf { s } _ { t }$ denotes the multi-modal state information (including multi-view observations, temporal history, and perception features), and $\mathbf { h } _ { \mathrm { V L M } }$ is the highlevel reasoning embedding extracted from the VLM that encodes both visual and textual context. The model aims to predict the future front-view frame $\hat { \mathbf { I } } _ { t + n }$ conditioned on these multi-modal context embeddings. This unified probabilistic formulation covers both the discrete autoregressive (AR) and the continuous AR+Difusion architectures, which instantiate diferent parameterizations of the same conditional distribution $p _ { \theta } ( \cdot )$ . We next describe the two paradigms instantiated under this formulation.

Autoregressive Generation(Discrete Representation). As shown in $\mathrm { F i g . 3 ( a ) }$ for discrete image generation, we first activate the VLM’s visual generation ability by enlarging its codebook. Assume that the language–vision model uses a joint codebook $Z = Z _ { L } + Z _ { I }$ . Through enlarging this codebook, the VLM can autoregressively perform multi-modal next-token prediction in both language and vision spaces. We introduce special tokens $\langle i m a g e \_ s t a r t \rangle$ and $\langle i m a g e \_ e n d \rangle$ to indicate the boundaries of visual token sequences and when to use the vision head. Specifically, based on the input visual tokens and the planning token $\mathbf { a } _ { t : t + m } ,$ the model autoregressively performs next-token prediction, represented

as:

$$
P _ { \theta } ( q _ { 1 : H : W } \mid \mathbf { s } _ { t } , \mathbf { a } _ { t : t + m } ) = \prod _ { i = 1 } ^ { H : W } P _ { \theta } ( q _ { i } \mid q _ { < i } , \mathbf { s } _ { t } , \mathbf { a } _ { t : t + m } ) ,\tag{7}
$$

where $q _ { i }$ are the visual tokens, $\mathbf { s } _ { t }$ represents the current multi-modal state (including visual observations, temporal history, and perception features), and $\mathbf { a } _ { t : t + m }$ denotes the corresponding planning token that conditions the generation of subsequent visual tokens.

AR+Difusion Generation (Continuous Representation). Apart from fully autoregressive generation, we also design an Autoregressive + Difusion architecture for improved visual quality, as shown in Fig. 3(b).

The difusion-based generation can be formulated as a conditional denoising process:

$$
p _ { \theta } ( \hat { \mathbf { I } } _ { t + n } \mid \mathbf { s } _ { t } , \mathbf { h } _ { \mathrm { V L M } } ) ,\tag{8}
$$

where the decoder is conditioned on the high-level reasoning embedding h<sub>VLM</sub> and the latent image features produced by the autoregressive module. Starting from Gaussian noise $\mathbf { X } _ { 0 } \sim \mathcal { N } ( 0 , 1 )$ , the difusion process gradually refines $\mathbf { X } _ { 0 }$ toward the latent embedding $\mathbf { X } _ { 1 }$ of the ground-truth future image.

After extracting continuous visual embeddings, we employ an autoregressive transformer to generate corresponding latent image features conditioned on $\mathbf { h } _ { \mathrm { V L M } }$ . Given an input instruction, the prompt is tokenized and mapped into a sequence of text embeddings $\mathbf { C } = [ c _ { 1 } , \ldots , c _ { n } ]$ before the LM head. To enable visual latent inference, we append a learnable query token $\mathbf { Q }$ to the sequence, where Q is randomly initialized and updated throughout training. The transformer processes the combined sequence $[ \mathbf { C } ; \mathbf { Q } ]$ , during which $\mathbf { Q }$ attends to the semantic context encoded in h<sub>VLM</sub> and aggregates features relevant for image synthesis. The output query token, denoted as $\mathbf { Q } ^ { * }$ , serves as the predicted visual latent representation and is supervised to match the ground-truth image embedding X extracted by the vision encoder. To align $\mathbf { Q } ^ { * }$ with X, we use a flow-matching objective that models the continuous feature distribution. Given the ground-truth image feature $\mathbf { X } _ { 1 }$ and the text-conditioned latent query $\mathbf { Q } ,$ we sample a timestep $t \sim \mathcal { U } ( 0 , 1 )$ and a noise vector $\mathbf { X } _ { 0 } \sim \mathcal { N } ( 0 , 1 )$ . A latent point along the interpolation path is computed as

$$
\begin{array} { r } { \mathbf { X } _ { t } = t \mathbf { X } _ { 1 } + ( 1 - t ) \mathbf { X } _ { 0 } , } \end{array}\tag{9}
$$

and the corresponding target velocity is

$$
\mathbf { V } _ { t } = \mathbf { X } _ { 1 } - \mathbf { X } _ { 0 } .\tag{10}
$$

The difusion transformer predicts the velocity ${ \bf V } _ { \theta } ( { \bf X } _ { t } , { \bf Q } , t )$ , and the flow-matching loss is

$$
\mathcal { L } _ { \mathrm { F M } } = \mathbb { E } \left[ \| \mathbf { V } _ { \theta } ( \mathbf { X } _ { t } , \mathbf { Q } , t ) - \mathbf { V } _ { t } \| ^ { 2 } \right] .\tag{11}
$$

Notably, we freeze the vision encoder weights and fine-tune only the difusion decoder. Although the decoder adopts a difusion architecture, it is trained with a deterministic reconstruction loss rather than probabilistic sampling objectives. Consequently, during inference, the model performs deterministic reconstruction, which reduces diversity but ensures stable and accurate prediction of future frames in autonomous driving scenarios. We additionally apply CLIP-based supervision between the decoded future image and the ground-truth image to maintain semantic alignment, represented as:

$$
\mathcal { L } _ { \mathrm { C L I P } } = 1 - \frac { \langle E _ { \mathrm { c l i p } } ( I _ { \mathrm { p r e d } } ) , E _ { \mathrm { c l i p } } ( I _ { \mathrm { g t } } ) \rangle } { \Vert E _ { \mathrm { c l i p } } ( I _ { \mathrm { p r e d } } ) \Vert _ { 2 } \ \Vert E _ { \mathrm { c l i p } } ( I _ { \mathrm { g t } } ) \Vert _ { 2 } } ,\tag{12}
$$

where $\langle \cdot , \cdot \rangle$ denotes the Euclidean inner product, $E _ { \mathrm { c l i p } } ( \cdot )$ denotes the embedding produced by the CLIP image encoder, $I _ { \mathrm { p r e d } }$ is the predicted image, and $I _ { \mathrm { g t } }$ is the ground-truth image. This difusion pathway complements the discrete autoregressive generation branch by providing a continuous, geometry-aware latent space for future frame synthesis, leading to stable and semantically consistent visual predictions within the unified world-model framework.

## 3.4 Joint Image Generation and Planning

To achieve joint image generation and planning, we place the planning token immediately before the image tokens, so that the generation of each image token is conditioned on the generated planning representation. In this way, image generation is jointly conditioned on the current-state visual embeddings and the predicted trajectory of the future state, enabling the synthesis of consistent future frames aligned with planned motion.

For the autoregressive generation, image token prediction is treated analogously to language generation and supervised through teacher-forcing with a cross-entropy loss. We adopt the pretrained QT-Former from ORION [12] and freeze its detection head during training. For the planning branch, following the implementations of VAD [25] and ORION [12], we train only the planning head with:

$$
\mathcal { L } _ { \mathrm { p l a n } } = \mathcal { L } _ { \mathrm { c o l } } + \mathcal { L } _ { \mathrm { b d } } + \mathcal { L } _ { \mathrm { m s e } } ,\tag{13}
$$

where ${ \mathcal { L } } _ { \mathrm { c o l } }$ denotes the collision loss, $\mathcal { L } _ { \mathrm { b d } }$ the boundary loss, and $\mathcal { L } _ { \mathrm { m s e } }$ the mean squared error loss.

For the autoregressive architecture, the overall objective is represented as:

$$
\begin{array} { r } { \mathcal { L } = \mathcal { L } _ { \mathrm { C E } } + \mathcal { L } _ { \mathrm { p l a n } } , } \end{array}\tag{14}
$$

while for the autoregressive + difusion architecture, where a learnable latent query in the latent space serves as the conditional embedding for image generation, the full objective becomes:

$$
\mathcal { L } = \mathcal { L } _ { \mathrm { C E } } + \mathcal { L } _ { \mathrm { p l a n } } + \mathcal { L } _ { \mathrm { F M } } + \mathcal { L } _ { \mathrm { C L I P } } ,\tag{15}
$$

where $\mathcal { L } _ { \mathrm { F M } }$ is the flow-matching loss and ${ \mathcal { L } } _ { \mathrm { C L I P } }$ is the CLIP-based semantic alignment loss.

## 4 Experiments

## 4.1 Training Details

We follow ORION [12] for the detection training setup and conduct all experiments on 8×NVIDIA H200 GPUs. Following OmniDrive [44], we use EVA-02-L [11] as the vision encoder and adopt Vicuna 1.5 [62] as the base LLM, fine-tuned with LoRA (rank=16, α=16). The numbers of scene, perception, and history queries are set to 512, 600, and 16, respectively, with a memory bank size of 16 frames.

Input images are augmented and resized to 640×640. For future frame prediction, we use a 192 × 128 resolution for the autoregressive branch and 512 × 1024 for the AR+Difusion branch to balance quality and speed. The difusion decoder uses 64 latent learnable query tokens. Additional hyperparameters and implementation details are provided in the Appendix.

## 4.2 Dataset

We train and evaluate UniDrive-WM on the Bench2Drive [23] dataset and the nuScenes [1] dataset. For Bench2Drive, following prior work, we use the base split of 1000 driving scenes: 950 for training and 50 for open-loop validation. Each scene covers roughly 150 m of continuous driving in a distinct trafic scenario. For closed-loop evaluation, we follow the oficial protocol consisting of 220 short routes spanning 44 interactive scenarios (five routes per scenario). For nuScenes, we adopt the oficial train/validation split for all experiments.

## 4.3 Training Pipeline

To enable planning and image generation while preserving the VQA capability of the underlying VLM, we adopt a two-stage training strategy.

Stage 1: Joint Planning and Image Generation We train the full model end-to-end, with the LLM updated via LoRA. For the autoregressive generator, the image-start token is placed immediately after the planning token to enforce planning-conditioned autoregressive decoding. For the AR+Difusion architecture, the 64 learnable latent query tokens are appended after the planning features in the latent space to condition the difusion decoder.

Stage 2: Joint Planning, Image Generation, and VQA We continue training with mixed VQA and driving data while keeping the same architectural setup as Stage 1. This stage reinforces the alignment of the vision–language–planning space by jointly optimizing VQA, trajectory planning, and future image prediction, enabling unified multimodal reasoning within a single framework.

## 4.4 Results

Evaluation of Trajectory Planning Results We evaluate our results on the base validation set of Bench2Drive and nuScenes. We report both open-loop and closed-loop evaluation results. As shown in Tab. 1, for closed-loop evaluation results on Bench2Drive, our method outperforms all the other methods that rely on target point and navigation command as conditions. Results show that our method achieves better performance compared with previous end-to-end methods and VLM-guided planning methods, which demonstrates the efectiveness of the image generation modality in boosting the performance of the planning task.

Table 1: Closed-loop and Open-loop Results of E2E-AD Methods on the Bench2Drive base set. C/L refers to camera/LiDAR. Avg. L2 is averaged over a 2-second prediction horizon sampled at 2 Hz, similar to UniAD. \* denotes expert feature distillation. NC: navigation command, TP: target point, DS: Driving Score, SR: Success Rate.
<table><tr><td rowspan="2">Method</td><td rowspan="2">Condition Modality</td><td rowspan="2"></td><td colspan="4">Closed-loop Metric</td><td>Open-loop Metric</td></tr><tr><td>DS↑</td><td></td><td>SR(%)↑ Efficiency↑ Comfortness↑</td><td></td><td>Avg. L2 ↓</td></tr><tr><td>TCP* [50]</td><td>TP</td><td>C</td><td>40.70</td><td>15.00</td><td>54.26</td><td>47.80</td><td>1.70</td></tr><tr><td>TCP-ctrl*</td><td>TP</td><td>C</td><td>30.47</td><td>7.27</td><td>55.97</td><td>51.51</td><td></td></tr><tr><td>TCP-traj*</td><td>TP</td><td>C</td><td>59.90</td><td>30.00</td><td>76.54</td><td>18.08</td><td>1.70</td></tr><tr><td>TCP-traj w/o distillation</td><td>TP</td><td>C</td><td>49.30</td><td>20.45</td><td>78.78</td><td>22.96</td><td>1.96</td></tr><tr><td>ThinkTwice* [22]</td><td>TP</td><td>C</td><td>62.44</td><td>31.23</td><td>69.33</td><td>16.22</td><td>0.95</td></tr><tr><td>DriveAdapter* [21]</td><td>TP</td><td>C&amp;L</td><td>64.22</td><td>33.08</td><td>70.22</td><td>16.01</td><td>1.01</td></tr><tr><td>AD-MLP [56]</td><td>NC</td><td>C</td><td>18.05</td><td>0.00</td><td>48.45</td><td>22.63</td><td>3.64</td></tr><tr><td>UniAD-Tiny [19]</td><td>NC</td><td>C</td><td>40.73</td><td>13.18</td><td>123.92</td><td>47.04</td><td>0.80</td></tr><tr><td>UniAD-Base [19]</td><td>NC</td><td>C</td><td>45.81</td><td>16.36</td><td>129.21</td><td>43.58</td><td>0.73</td></tr><tr><td>VAD [25]</td><td>NC</td><td>C</td><td>42.35</td><td>15.00</td><td>157.94</td><td>46.01</td><td>0.91</td></tr><tr><td>MomÀD [39]</td><td>NC</td><td>C</td><td>44.54</td><td>16.71</td><td>170.21</td><td>48.63</td><td>0.87</td></tr><tr><td>GenAD [64]</td><td>NC</td><td>C</td><td>44.81</td><td>15.90</td><td></td><td></td><td></td></tr><tr><td>DriveTransformer-Large [24]</td><td>NC</td><td>C</td><td>63.46</td><td>35.01</td><td>100.64</td><td>20.78</td><td>0.62</td></tr><tr><td>ORION [12]</td><td>NC</td><td>C</td><td>77.74</td><td>54.62</td><td>151.48</td><td>17.38</td><td>0.68</td></tr><tr><td>Ours(AR)</td><td>NC</td><td>C</td><td>79.22</td><td>56.36</td><td>158.44</td><td>28.01</td><td>0.64</td></tr><tr><td>Ours(AR+Diffusion)</td><td>NC</td><td>C</td><td>79.31</td><td>56.42</td><td>158.65</td><td>27.93</td><td>0.63</td></tr></table>

Table 2: Open-Loop Planning and perception metrics on Bench2Drive. Lower is better for planning errors; higher is better for mAP/NDS.
<table><tr><td rowspan="2">Method</td><td colspan="3">L2 (m)↓</td><td colspan="3">Box +</td><td rowspan="2"></td><td rowspan="2">Collision(%)↓|mAP↑ mATE↓ mASE↓ mAOE↓ mAVE↓ NDS↑</td><td rowspan="2"></td><td rowspan="2"></td><td rowspan="2"></td><td rowspan="2"></td></tr><tr><td>1s</td><td>2s</td><td>3s</td><td>1s</td><td>2s</td><td>3s</td></tr><tr><td>BEVFormer [31]</td><td></td><td></td><td></td><td></td><td></td><td></td><td>0.616</td><td>0.372</td><td>0.079</td><td>0.044</td><td>0.808</td><td></td><td>0.642</td></tr><tr><td>UniAD [19]</td><td>0.521</td><td>1.265</td><td>2.140</td><td></td><td>0.770</td><td>3.87</td><td>7.91</td><td>0.121</td><td>0.518</td><td>0.170</td><td>0.096</td><td>0.977</td><td>0.316</td></tr><tr><td>VAD [25]</td><td>0.454</td><td>0.912</td><td>1.477</td><td>0.102</td><td>0.202</td><td>0.296</td><td></td><td>0.509</td><td>0.385</td><td>0.0854</td><td>0.0308</td><td>0.594</td><td>0.604</td></tr><tr><td>Orion [12]</td><td>0.268</td><td>0.631</td><td>1.129</td><td>0.213</td><td>0.467</td><td>0.743</td><td></td><td>0.646</td><td>0.366</td><td>0.0765</td><td>0.0271</td><td>0.258</td><td>0.723</td></tr><tr><td>Ours(AR)</td><td></td><td></td><td>0.247 0.598 1.079</td><td></td><td>0.198 0.435</td><td>0.668</td><td></td><td>0.663</td><td>0.335</td><td>0.0740</td><td>0.0262</td><td>0.249</td><td>0.746</td></tr><tr><td>Ours(AR+Diff)</td><td></td><td></td><td>0.241 0.589 1.066</td><td></td><td>0.192 0.426</td><td></td><td>0.657</td><td>0.675</td><td>0.328</td><td>0.0733</td><td>0.0254</td><td>0.243</td><td>0.755</td></tr></table>

We also evaluate the open-loop performance on Bench2Drive in Tab. 2 and nuScenes in Tab. 3. Notably, UniAD [19] computes L2 metrics and collision rate at each timestep, whereas VAD [25] and ORION [12] consider the average of all previous time steps. We follow the evaluation method of VAD and ORION to evaluate our performance. Compared with previous methods that perform either VLM-guided planning or end-to-end planning, our unified method achieves better performance on both the planning and detection tasks, which shows the efectiveness of future image prediction in improving the performance of the planning task. These consistent gains across both Bench2Drive (synthetic) and

Table 3: Further Open-Loop evaluation on nuScenes.
<table><tr><td>Metric</td><td>VAD-Base [25] Doe-1 [65] Drive-VLM [41] OmniDrive [44] ORION [12] FSDrive [55] Ours(AR) Ours(AR+Diff)</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Avg. L2 (m)↓</td><td>1.25</td><td>0.70</td><td>0.40</td><td>0.84</td><td>0.34</td><td>0.60</td><td>0.30</td><td>0.29</td></tr><tr><td>Avg. col (%)↓</td><td>1.09</td><td>0.21</td><td>0.27</td><td>0.94</td><td>0.37</td><td>0.19</td><td>0.31</td><td>0.31</td></tr></table>

Table 4: Future frame generation results on the Bench2Drive [23] and nuScenes [1] datasets. AR: Autoregressive. AR+Dif: Autoregressive+Difusion. Lower FID indicates better visual fidelity.
<table><tr><td>Method Dataset</td><td></td><td>[CVPR21]</td><td>DriveGAN [27] DriveDreamer [45] Drive-WM [46] [ECCV24]</td><td>[CVPR24]</td><td>GEM [15] [CVPR25]</td><td>Doe-1 [65] [arXiv24]</td><td>FSDrive [55] [NeurIPS25]</td><td>Ours(AR) Ours (AR+Diff)</td><td></td></tr><tr><td>Type</td><td></td><td>GAN</td><td>Diffusion</td><td>Diffusion</td><td>Diffusion</td><td>AR</td><td>AR</td><td>AR</td><td>AR+Diffusion</td></tr><tr><td rowspan="2">FID ↓</td><td>Bench2Drive</td><td>62.3</td><td>42.8</td><td>17.8</td><td>13.2</td><td>18.6</td><td>9.3</td><td>7.2</td><td>6.6</td></tr><tr><td>nuScenes</td><td>73.4</td><td>52.6</td><td>15.8</td><td>10.5</td><td>15.9</td><td>10.1</td><td>7.8</td><td>7.3</td></tr></table>

NuScenes (real-world) further indicate the strong generalization ability of our method.

Evaluation of Image Generation Results We evaluate UniDrive-WM on both the autoregressive and AR+Difusion image generation branches. Qualitative results are shown in Fig. 4 and Fig. 5, and quantitative results are provided in Tab. 4. Across both settings, our method produces visually coherent future frames that closely match the ground-truth scene evolution and remain consistent with the predicted trajectory. These properties translate into competitive or superior image generation quality, as reflected by low FID scores.

A particularly relevant comparison is FSDrive [55], a recent unified vision– planning framework that conditions planning on image features. Unlike FS-Drive, our approach conditions image generation directly on the planning tokens, enabling planning-conditioned future frame prediction in both the AR and AR+Difusion branches. This tighter coupling between planning and visual prediction improves trajectory alignment and yields future frames that more accurately follow the intended motion, contributing to our improved FID performance.

Evaluation on VQA Following prior work, we report our Visual Question Answering (VQA) results in Tab. 5, using DriveLM’s GVQA [38] dataset. Our model achieves competitive performance against prior state-of-the-art methods on the understanding task, demonstrating its efectiveness in driving-domainspecific understanding.

## 4.5 Comparison of AR and AR+Difusion Architecture

Speed The AR branch is intentionally lightweight (discrete tokens, shallow decoder); the AR+Dif branch is heavier (difusion decoder) and mainly intended for high-fidelity generation. In open-loop evaluation on Bench2Drive, the inference speed of AR is 2 fps and AR+Dif is 0.4 fps on an A100. We regard speeding up the AR+Dif inference as future work.

Current Frame  
Future Frame  
Predicted Future Image  
![](images/929055b8f516601bf99343faebc91696f870e94a54f6a758f236b3f08b74a2f0.jpg)

Current Frame  
Future Frame  
Predicted Future Image  
![](images/919b33a1c1a62110d13100b8f55eb5c7d4e8afd19591148484ea5b015b9ff61f.jpg)

Fig. 4: Qualitative future image prediction results on Bench2Drive and nuScenes using the autoregressive (AR) architecture.  
![](images/1a68caf542b52d27f37e5dd68666bcd9bea4e3d0a4459054fbde5c05d36706bf.jpg)  
Fig. 5: Qualitative future image prediction results on nuScenes using the AR+Difusion architecture.

Resolution and Compression Trade-ofs In the AR architecture, spatial resolution is tightly coupled to sequence length. Generating an $H \times W$ image with a downsampling factor f requires ${ \frac { H } { f } } \times { \frac { W } { f } } \quad$ discrete tokens. Scaling up resolution quadratically increases the token count, which not only hits the LLM’s $O ( N ^ { 2 } )$ context limit but also severely slows down training convergence. In contrast, our AR+Difusion branch decouples resolution from token length. The VLM only needs to predict a compact sequence of continuous latents, which the difusion decoder maps to high-resolution outputs (e.g., 512×1024). This enables high-fidelity geometric forecasting without overwhelming the reasoning context window or hindering training eficiency.

Image Generation and Complementary Roles Beyond resolution constraints, the two paradigms exhibit distinct characteristics in representation learning (Tab. 4). The discrete quantization in the AR branch acts as an information bottleneck that provides strong semantic regularization. This makes its lightweight decoder highly robust for real-time, latency-sensitive closed-loop control. In contrast, the continuous pathway of the AR+Difusion branch avoids token-by-token exposure bias and inherently preserves high-frequency geometric details. This yields higher-fidelity future frames and more precise long-term trajectory alignment (e.g., lower L2 errors and higher NDS). Implemented as parallel decoding heads on top of the same VLM planning backbone, the two branches ofer a natural deployment split: AR is suited to fast, reactive planning where semantic stability is critical, while AR+Difusion is preferable for ofline evaluation or high-fidelity geometric forecasting in complex scenes. Overall, the two heads are complementary rather than competing, and together broaden the applicability of UniDrive-WM.

Table 5: Results on the DriveLM [38] GVQA benchmark.
<table><tr><td>Method</td><td>Accuracy ↑ ChatGPT ↑BLEU</td><td></td><td>1 ↑ROUGE</td><td></td><td>L ↑ CIDEr ↑ Match ↑ Final Score ↑</td><td></td><td></td></tr><tr><td>DriveLM baseline [38]</td><td>0.00</td><td>0.65</td><td>0.05</td><td>0.08</td><td>0.10</td><td>0.28</td><td>0.32</td></tr><tr><td>Cube-LLM [7]</td><td>0.39</td><td>0.89</td><td>0.16</td><td>0.20</td><td>0.31</td><td>0.39</td><td>0.50</td></tr><tr><td>TrackingMeetsLMM [20]</td><td>0.60</td><td>0.58</td><td>0.72</td><td>0.72</td><td>0.04</td><td>0.36</td><td>0.52</td></tr><tr><td>SimpleLLM4AD [63]</td><td>0.66</td><td>0.57</td><td>0.76</td><td>0.73</td><td>0.15</td><td>0.35</td><td>0.53</td></tr><tr><td>OmniDrive [44]</td><td>0.70</td><td>0.65</td><td>0.52</td><td>0.73</td><td>0.13</td><td>0.37</td><td>0.56</td></tr><tr><td>FSDrive [55]</td><td>0.72</td><td>0.63</td><td>0.76</td><td>0.74</td><td>0.17</td><td>0.39</td><td>0.57</td></tr><tr><td>UniDrive-WM(ours)</td><td>0.73</td><td>0.67</td><td>0.77</td><td>0.76</td><td>0.20</td><td>0.40</td><td>0.59</td></tr></table>

Table 6: Ablation study of the detection head, planning head, and image generation module for our AR architecture on Bench2Drive [23].
<table><tr><td rowspan="2">Detection head Planning head Image Gen</td><td rowspan="2"></td><td rowspan="2"></td><td colspan="3">L2 (m)↓</td><td colspan="3">|Box + Collision (%)↓|mAP↑ mATE↓ mASE↓ mAOE↓ mAVE↓ NDS↑</td><td colspan="7"></td></tr><tr><td>1s</td><td>2s</td><td>3s</td><td>1s</td><td>2s</td><td>3s</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td>√</td><td>√</td><td>0.482</td><td>1.135</td><td>2.146</td><td>0.387</td><td>0.898</td><td>1.77</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>√</td><td></td><td>√</td><td></td><td></td><td></td><td></td><td></td><td></td><td>0.638</td><td>0.336</td><td></td><td>0.0726</td><td>0.0289</td><td>0.283</td><td>0.718</td></tr><tr><td>√</td><td>√</td><td></td><td></td><td>0.269 0.632 1.130</td><td></td><td></td><td>0.214 0.469</td><td>0.746</td><td>0.642</td><td>0.367</td><td></td><td>0.0767</td><td>0.0274</td><td>0.258</td><td>0.721</td></tr><tr><td>√</td><td>√</td><td>√</td><td>0.247 0.598 1.079</td><td></td><td></td><td></td><td>0.1980.435</td><td>0.668</td><td>0.663</td><td>0.335</td><td></td><td>0.0740 0.0262</td><td></td><td>0.249</td><td>0.746</td></tr></table>

Table 7: Ablation study on open-loop evaluation on Bench2Drive. For the AR architecture, we analyze the efect of swapping the order of the planning and generation heads.
<table><tr><td>Future Image Prediction</td><td>Avg. L2 (m)↓ Avg. col(%)↓|FID↓</td><td></td><td></td></tr><tr><td>Generation + Planning</td><td>0.67</td><td>0.45</td><td>9.1</td></tr><tr><td>Planning + Generation (Ours)</td><td>0.64</td><td>0.43</td><td>7.2</td></tr></table>

## 4.6 Ablation Study

We ablate the detection supervision and the image generation module to assess their contributions to planning, shown in Tab. 6. Removing the image generation head noticeably degrades trajectory accuracy and increases collision cases, indicating that

Table 8: Additional ablation of VQA score on Chat-B2D.
<table><tr><td colspan="4">Image Generation CIDEr ↑ BLEU ↑ ROUGE-L↑</td></tr><tr><td>=</td><td>65.7</td><td>52.4</td><td>77.5</td></tr><tr><td>√</td><td>66.7</td><td>53.5</td><td>78.6</td></tr></table>

future frame prediction provides useful auxiliary signals for planning. Disabling detection supervision further harms planning performance by weakening perception quality. Together, these findings show that both perception and future frame prediction play complementary roles, and that jointly optimizing all components within a unified world model yields more reliable driving behavior.

We show experiments regarding changing the order of the planning and image generation modules in the AR architecture in Tab. 7. Planning → Generation (Ours) shows improvements over Generation → Planning on planningrelated metrics and a much larger gain in visual quality, suggesting that the prediction order matters; conditioning future prediction on planned trajectories aligns with the action→observation causal direction and provides a natural mechanism to produce plan-consistent futures that better support planning.

We evaluate VQA performance on Bench2Drive [23] using the Chat-B2D QA annotations [12], shown in Tab. 8. Compared with the model variant without the image-generation module, incorporating image generation consistently improves all VQA metrics. This indicates that the future frame prediction provides additional structural cues that benefit question answering. Intuitively, better modeling of future visual states enhances the model’s understanding of the current scene, which aligns with human perception. We also show the visualization of the VQA result in open-loop evaluation in the supplementary material. These results demonstrate that our model not only comprehends the current scene, but also performs efective future-state reasoning, enabling it to produce reliable, decision-oriented answers even in complex driving scenarios and challenging weather conditions.

## 5 Conclusion and Future Work

We presented UniDrive-WM, a unified framework that integrates scene understanding, trajectory planning, and visual generation into a single worldmodel–driven pipeline. Leveraging a vision–language model (VLM) as the backbone, our method predicts future image frames from current and historical multi-view observations together with the planning tokens, and the planningconditioned visual predictions in turn enhance trajectory planning by providing a visual forecast of the expected future scene. Experimental results demonstrate that our approach not only achieves high-fidelity, planning-conditioned image generation, but also yields significant gains in planning accuracy and collision reduction. By conditioning the VLM on rich multi-view inputs, temporal history, and perception features, UniDrive-WM establishes a coherent bridge between reasoning, action, and visual imagination. Looking ahead, we plan to extend the framework to more interactive and long-horizon driving scenarios, paving the way toward next-generation world models for autonomous driving.

[1] Caesar, H., Bankiti, V., Lang, A.H., Vora, S., Liong, V.E., Xu, Q., Krishnan, A., Pan, Y., Baldan, G., Beijbom, O.: nuscenes: A multimodal dataset for autonomous driving. In: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. pp. 11621–11631 (2020)

[2] Cen, J., Yu, C., Yuan, H., Jiang, Y., Huang, S., Guo, J., Li, X., Song, Y., Luo, H., Wang, F., et al.: Worldvla: Towards autoregressive action world model. arXiv preprint arXiv:2506.21539 (2025)

[3] Chen, J., Xu, Z., Pan, X., Hu, Y., Qin, C., Goldstein, T., Huang, L., Zhou, T., Xie, S., Savarese, S., Xue, L., Xiong, C., Xu, R.: Blip3-o: A family of fully open unified multimodal models-architecture, training and dataset (2025), https://arxiv.org/abs/2505.09568

[4] Chen, J., Xue, L., Xu, Z., Pan, X., Yang, S., Qin, C., Yan, A., Zhou, H., Chen, Z., Huang, L., et al.: Blip3o-next: Next frontier of native image generation. arXiv preprint arXiv:2510.15857 (2025)

[5] Chern, E., Hu, Z., Chern, S., Kou, S., Su, J., Ma, Y., Deng, Z., Liu, P.: Thinking with generated images. arXiv preprint arXiv:2505.22525 (2025)

[6] Chi, H., Qiu, D., Su, H., Liu, H., Li, Z., Zhang, H., Lv, C.: Driver-wm: A driver-centric trafic-conditioned latent world model for in-cabin dynamics rollout. arXiv preprint arXiv:2605.05092 (2026)

[7] Cho, J.H., Ivanovic, B., Cao, Y., Schmerling, E., Wang, Y., Weng, X., Li, B., You, Y., Krähenbühl, P., Wang, Y., et al.: Language-image models with 3d understanding. arXiv preprint arXiv:2405.03685 (2024)

[8] Dong, Y., Wu, F., Chen, G., Cheng, Z.Q., Hu, Q., Zhou, Y., Sun, J., He, J.Y., Dai, Q., Hauptmann, A.G.: Unified world models: Memoryaugmented planning and foresight for visual navigation. arXiv preprint arXiv:2510.08713 (2025)

[9] Dong, Y., Wu, F., Dai, Y., Kong, L., Chen, G., Zhu, X., Hu, Q., Wang, T., Garnica, J., Liu, F., et al.: Language-conditioned world modeling for visual navigation. arXiv preprint arXiv:2603.26741 (2026)

[10] Dosovitskiy, A., Ros, G., Codevilla, F., Lopez, A., Koltun, V.: Carla: An open urban driving simulator. In: Conference on robot learning. pp. 1–16. PMLR (2017)

[11] Fang, Y., Sun, Q., Wang, X., Huang, T., Wang, X., Cao, Y.: Eva-02: A visual representation for neon genesis. Image and Vision Computing 149, 105171 (2024)

[12] Fu, H., Zhang, D., Zhao, Z., Cui, J., Liang, D., Zhang, C., Zhang, D., Xie, H., Wang, B., Bai, X.: Orion: A holistic end-to-end autonomous driving framework by vision-language instructed action generation. arXiv preprint arXiv:2503.19755 (2025)

[13] Gao, S., Yang, J., Chen, L., Chitta, K., Qiu, Y., Geiger, A., Zhang, J., Li, H.: Vista: A generalizable driving world model with high fidelity and

versatile controllability. Advances in Neural Information Processing Systems 37, 91560–91596 (2024)

[14] Han, X., Jia, Z., Li, B., Wang, Y., Ivanovic, B., You, Y., Liu, L., Wang, Y., Pavone, M., Feng, C., et al.: Extrapolated urban view synthesis benchmark. In: Proceedings of the IEEE/CVF International Conference on Computer Vision. pp. 28718–28728 (2025)

[15] Hassan, M., Stapf, S., Rahimi, A., Rezende, P., Haghighi, Y., Brüggemann, D., Katircioglu, I., Zhang, L., Chen, X., Saha, S., et al.: Gem: A generalizable ego-vision multimodal world model for fine-grained ego-motion, object dynamics, and scene composition control. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 22404–22415 (2025)

[16] He, H., Zhang, Y., Lin, L., Xu, Z., Pan, L.: Pre-trained video generative models as world simulators. arXiv preprint arXiv:2502.07825 (2025)

[17] Hu, A., Russell, L., Yeo, H., Murez, Z., Fedoseev, G., Kendall, A., Shotton, J., Corrado, G.: Gaia-1: A generative world model for autonomous driving. arXiv preprint arXiv:2309.17080 (2023)

[18] Hu, E.J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., Chen, W., et al.: Lora: Low-rank adaptation of large language models. ICLR 1(2), 3 (2022)

[19] Hu, Y., Yang, J., Chen, L., Li, K., Sima, C., Zhu, X., Chai, S., Du, S., Lin, T., Wang, W., Lu, L., Jia, X., Liu, Q., Dai, J., Qiao, Y., Li, H.: Planningoriented autonomous driving. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (2023)

[20] Ishaq, A., Lahoud, J., Khan, F.S., Khan, S., Cholakkal, H., Anwer, R.M.: Tracking meets large multimodal models for driving scenario understanding. arXiv preprint arXiv:2503.14498 (2025)

[21] Jia, X., Gao, Y., Chen, L., Yan, J., Liu, P.L., Li, H.: Driveadapter: Breaking the coupling barrier of perception and planning in end-to-end autonomous driving. In: ICCV (2023)

[22] Jia, X., Wu, P., Chen, L., Xie, J., He, C., Yan, J., Li, H.: Think twice before driving: Towards scalable decoders for end-to-end autonomous driving. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). pp. 21983–21994 (June 2023)

[23] Jia, X., Yang, Z., Li, Q., Zhang, Z., Yan, J.: Bench2drive: Towards multiability benchmarking of closed-loop end-to-end autonomous driving. Advances in Neural Information Processing Systems 37, 819–844 (2024)

[24] Jia, X., You, J., Zhang, Z., Yan, J.: Drivetransformer: Unified transformer for scalable end-to-end autonomous driving. arXiv preprint arXiv:2503.07656 (2025)

[25] Jiang, B., Chen, S., Xu, Q., Liao, B., Chen, J., Zhou, H., Zhang, Q., Liu, W., Huang, C., Wang, X.: Vad: Vectorized scene representation for eficient autonomous driving. ICCV (2023)

[26] Kim, M.J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al.: Openvla: An open-source vision-language-action model. arXiv preprint arXiv:2406.09246 (2024)

[27] Kim, S.W., Philion, J., Torralba, A., Fidler, S.: Drivegan: Towards a controllable high-quality neural simulation. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 5820–5829 (2021)

[28] Li, C., Wu, W., Zhang, H., Xia, Y., Mao, S., Dong, L., Vulić, I., Wei, F.: Imagine while reasoning in space: Multimodal visualization-of-thought. arXiv preprint arXiv:2501.07542 (2025)

[29] Li, S., Gao, Y., Sadigh, D., Song, S.: Unified video action model. arXiv preprint arXiv:2503.00200 (2025)

[30] Li, Y., Shang, S., Liu, W., Zhan, B., Wang, H., Wang, Y., Chen, Y., Wang, X., An, Y., Tang, C., et al.: Drivevla-w0: World models amplify data scaling law in autonomous driving. arXiv preprint arXiv:2510.12796 (2025)

[31] Li, Z., Wang, W., Li, H., Xie, E., Sima, C., Lu, T., Qiao, Y., Dai, J.: Bevformer: Learning bird’s-eye-view representation from multi-camera images via spatiotemporal transformers. arXiv preprint arXiv:2203.17270 (2022)

[32] Liao, Y., Sun, Z., Qiu, X., Zhao, Z., Tang, W., He, X., Zheng, X., Zhang, T., Huang, X., Han, X.: Work zones challenge vlm trajectory planning: Toward mitigation and robust autonomous driving. arXiv preprint arXiv:2510.02803 (2025)

[33] Liu, M., Zhang, D., Liu, J., Cui, J., Xie, H., Chen, G., Ye, H., Yang, M.Y., Nex, F., Cheng, H.: Driveva: Video action models are zero-shot drivers. arXiv preprint arXiv:2604.04198 (2026)

[34] Liu, T., Zhao, S., Pourkeshavarz, M., Li, W., Rhinehart, N.: Occsim: Multikilometer simulation with long-horizon occupancy world models. arXiv preprint arXiv:2603.28887 (2026)

[35] Liu, T., Zhao, S., Rhinehart, N.: Towards foundational lidar world models with eficient latent flow matching. arXiv preprint arXiv:2506.23434 (2025)

[36] Liu, T., Zhao, S., Rhinehart, N.: Towards foundational lidar world models with eficient latent flow matching. Advances in Neural Information Processing Systems 38, 155959–155994 (2026)

[37] Radford, A., Kim, J.W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., et al.: Learning transferable visual models from natural language supervision. In: International conference on machine learning. pp. 8748–8763. PmLR (2021)

[38] Sima, C., Renz, K., Chitta, K., Chen, L., Zhang, H., Xie, C., Beißwenger, J., Luo, P., Geiger, A., Li, H.: Drivelm: Driving with graph visual question answering. In: European conference on computer vision. pp. 256–274. Springer (2024)

[39] Song, Z., Jia, C., Liu, L., Pan, H., Zhang, Y., Wang, J., Zhang, X., Xu, S., Yang, L., Luo, Y.: Don’t shake the wheel: Momentum-aware planning in end-to-end autonomous driving. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 22432–22441 (2025)

[40] Team, C.: Chameleon: Mixed-modal early-fusion foundation models. arXiv preprint arXiv:2405.09818 (2024)

[41] Tian, X., Gu, J., Li, B., Liu, Y., Wang, Y., Zhao, Z., Zhan, K., Jia, P., Lang, X., Zhao, H.: Drivevlm: The convergence of autonomous driving and large vision-language models. arXiv preprint arXiv:2402.12289 (2024)

[42] Tong, S., Fan, D., Zhu, J., Xiong, Y., Chen, X., Sinha, K., Rabbat, M., LeCun, Y., Xie, S., Liu, Z.: Metamorph: Multimodal understanding and generation via instruction tuning. arXiv preprint arXiv:2412.14164 (2024)

[43] Wang, L., Zheng, W., Ren, Y., Jiang, H., Cui, Z., Yu, H., Lu, J.: Occsora: 4d occupancy generation models as world simulators for autonomous driving. arXiv preprint arXiv:2405.20337 (2024)

[44] Wang, S., Yu, Z., Jiang, X., Lan, S., Shi, M., Chang, N., Kautz, J., Li, Y., Alvarez, J.M.: Omnidrive: A holistic vision-language dataset for autonomous driving with counterfactual reasoning. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 22442–22452 (2025)

[45] Wang, X., Zhu, Z., Huang, G., Chen, X., Zhu, J., Lu, J.: Drivedreamer: Towards real-world-driven world models for autonomous driving. arXiv preprint arXiv:2309.09777 (2023)

[46] Wang, Y., He, J., Fan, L., Li, H., Chen, Y., Zhang, Z.: Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving. arXiv preprint arXiv:2311.17918 (2023)

[47] Wei, H., Lu, F., Zhu, Y., Zheng, Z., Xue, W., Shao, L., Zhang, X., Wu, Y., Fu, R., Chen, G.: Lidardraft: Generating lidar point cloud from versatile inputs. arXiv preprint arXiv:2512.20105 (2025)

[48] Wei, J., Yuan, S., Li, P., Hu, Q., Gan, Z., Ding, W.: Occllama: An occupancy-language-action generative world model for autonomous driving. arXiv preprint arXiv:2409.03272 (2024)

[49] Wu, C., Chen, X., Wu, Z., Ma, Y., Liu, X., Pan, Z., Liu, W., Xie, Z., Yu, X., Ruan, C., et al.: Janus: Decoupling visual encoding for unified multimodal understanding and generation. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 12966–12977 (2025)

[50] Wu, P., Jia, X., Chen, L., Yan, J., Li, H., Qiao, Y.: Trajectory-guided control prediction for end-to-end autonomous driving: A simple yet strong baseline. Advances in Neural Information Processing Systems 35, 6119–6132 (2022)

[51] Wu, Z., Ni, J., Wang, X., Guo, Y., Chen, R., Lu, L., Dai, J., Xiong, Y.: Holodrive: Holistic 2d-3d multi-modal street scene generation for autonomous driving. arXiv preprint arXiv:2412.01407 (2024)

[52] Xie, J., Mao, W., Bai, Z., Zhang, D.J., Wang, W., Lin, K.Q., Gu, Y., Chen, Z., Yang, Z., Shou, M.Z.: Show-o: One single transformer to unify multimodal understanding and generation. arXiv preprint arXiv:2408.12528 (2024)

[53] Yao, J., Kurra, D.D., Lampo, T., Cheng, Z., Guo, D., Yaman, B.: Vlga: Vision-language-geometry-action models for autonomous driving. arXiv preprint arXiv:2606.12396 (2026)

[54] Yu, H., Jin, Y., Canevaro, A., Schmidt, J., Jordan, J., Li, P., Kaufeld, M., Lindner, S., Betz, J., Stork, W.: G2dp: Difusion planning with spatiotemporal grid guidance. arXiv preprint arXiv:2606.26017 (2026)

[55] Zeng, S., Chang, X., Xie, M., Liu, X., Bai, Y., Pan, Z., Xu, M., Wei, X.: Futuresightdrive: Thinking visually with spatio-temporal cot for autonomous driving. arXiv preprint arXiv:2505.17685 (2025)

[56] Zhai, J.T., Feng, Z., Du, J., Mao, Y., Liu, J.J., Tan, Z., Zhang, Y., Ye, X., Wang, J.: Rethinking the open-loop evaluation of end-to-end autonomous driving in nuscenes. arXiv preprint arXiv:2305.10430 (2023)

[57] Zhai, X., Mustafa, B., Kolesnikov, A., Beyer, L.: Sigmoid loss for language image pre-training. In: Proceedings of the IEEE/CVF international conference on computer vision. pp. 11975–11986 (2023)

[58] Zhang, K., Tang, Z., Hu, X., Pan, X., Guo, X., Liu, Y., Huang, J., Yuan, L., Zhang, Q., Long, X.X., et al.: Epona: Autoregressive difusion world model for autonomous driving. arXiv preprint arXiv:2506.24113 (2025)

[59] Zhang, L., Xiong, Y., Yang, Z., Casas, S., Hu, R., Urtasun, R.: Copilot4d: Learning unsupervised world models for autonomous driving via discrete difusion. arXiv preprint arXiv:2311.01017 (2023)

[60] Zhang, Y., Gong, S., Xiong, K., Ye, X., Li, X., Tan, X., Wang, F., Huang, J., Wu, H., Wang, H.: Bevworld: A multimodal world simulator for autonomous driving via scene-level bev latents. arXiv preprint arXiv:2407.05679 (2024)

[61] Zhao, Q., Lu, Y., Kim, M.J., Fu, Z., Zhang, Z., Wu, Y., Li, Z., Ma, Q., Han, S., Finn, C., et al.: Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 1702–1713 (2025)

[62] Zheng, L., Chiang, W.L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E., et al.: Judging llm-as-a-judge with mt-bench and chatbot arena. Advances in neural information processing systems 36, 46595–46623 (2023)

[63] Zheng, P., Zhao, Y., Gong, Z., Zhu, H., Wu, S.: Simplellm4ad: An end-to-end vision-language model with graph visual question answering for autonomous driving. arXiv preprint arXiv:2407.21293 (2024)

[64] Zheng, W., Song, R., Guo, X., Zhang, C., Chen, L.: Genad: Generative endto-end autonomous driving. In: European Conference on Computer Vision. pp. 87–104. Springer (2024)

[65] Zheng, W., Xia, Z., Huang, Y., Zuo, S., Zhou, J., Lu, J.: Doe-1: Closedloop autonomous driving with large world model. arXiv preprint arXiv: 2412.09627 (2024)

[66] Zheng, Y., Yang, P., Xing, Z., Zhang, Q., Zheng, Y., Gao, Y., Li, P., Zhang, T., Xia, Z., Jia, P., et al.: World4drive: End-to-end autonomous driving via intention-aware physical latent world model. In: Proceedings of the IEEE/CVF International Conference on Computer Vision. pp. 28632–28642 (2025)

[67] Zhou, C., Yu, L., Babu, A., Tirumala, K., Yasunaga, M., Shamis, L., Kahn, J., Ma, X., Zettlemoyer, L., Levy, O.: Transfusion: Predict the next token and difuse images with one multi-modal model. arXiv preprint arXiv:2408.11039 (2024)

[68] Zyrianov, V., Che, H., Liu, Z., Wang, S.: Lidardm: Generative lidar simulation in a generated world. In: 2025 IEEE International Conference on Robotics and Automation (ICRA). pp. 6055–6062. IEEE (2025)

## Appendix

Table 9: Multi-ability results on the Bench2Drive base set. An asterisk denotes expert feature distillation. C/L refers to camera/LiDAR. NC: navigation command; TP: target point.
<table><tr><td rowspan="3">Method</td><td rowspan="3">Condition Modality</td><td rowspan="3"></td><td colspan="6">Ability (%) ↑</td></tr><tr><td>Merging Overtaking Emergency Brake Give Way Traffic Sign Mean</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>TCP* [50]</td><td>TP</td><td>C</td><td>16.18</td><td>20.00</td><td>20.00</td><td>10.00</td><td>6.99</td><td>14.63</td></tr><tr><td>TCP-ctrl*</td><td>TP</td><td>C</td><td>10.29</td><td>4.44</td><td>10.00</td><td>10.00</td><td>6.45</td><td>8.23</td></tr><tr><td>TCP-traj*</td><td>TP</td><td>C</td><td>8.89</td><td>24.29</td><td>51.67</td><td>40.00</td><td>46.28</td><td>34.22</td></tr><tr><td>TCP-traj w/o distillation</td><td>TP</td><td>C</td><td>17.14</td><td>6.67</td><td>40.00</td><td>50.00</td><td>28.72</td><td>28.51</td></tr><tr><td>ThinkTwice* [22]</td><td>TP</td><td>C</td><td>27.38</td><td>18.42</td><td>35.82</td><td>50.00</td><td>54.23</td><td>37.17</td></tr><tr><td>DriveAdapter* [21]</td><td>TP</td><td>C&amp;L</td><td>28.82</td><td>26.38</td><td>48.76</td><td>50.00</td><td>56.43</td><td>42.08</td></tr><tr><td>AD-MLP [56]</td><td>NC</td><td>C</td><td>0.00</td><td>0.00</td><td>0.00</td><td>0.00</td><td>4.35</td><td>0.87</td></tr><tr><td>UniAD-Tiny [19]</td><td>NC</td><td>C</td><td>8.89</td><td>9.33</td><td>20.00</td><td>20.00</td><td>15.43</td><td>14.73</td></tr><tr><td>UniAD-Base [19]</td><td>NC</td><td>C</td><td>14.10</td><td>17.78</td><td>21.67</td><td>10.00</td><td>14.21</td><td>15.55</td></tr><tr><td>VAD [25]</td><td>NC</td><td>C</td><td>8.11</td><td>24.44</td><td>18.64</td><td>20.00</td><td>19.15</td><td>18.07</td></tr><tr><td>DriveTransformer-Large [24]</td><td>NC</td><td>C</td><td>17.57</td><td>35.00</td><td>48.36</td><td>40.00</td><td>52.10</td><td>38.60</td></tr><tr><td>ORION</td><td>NC</td><td>C</td><td>25.00</td><td>71.11</td><td>78.33</td><td>30.00</td><td>69.15</td><td>54.72</td></tr><tr><td>Ours(AR)</td><td>NC</td><td>C</td><td>29.81</td><td>74.04</td><td>79.84</td><td>40.00</td><td>71.30</td><td>59.00</td></tr><tr><td>Ours(AR+Diffusion)</td><td>NC</td><td>C</td><td>29.97</td><td>74.64</td><td>79.98</td><td>40.00</td><td>71.54</td><td>59.23</td></tr></table>

## A Evaluation Metrics

For closed-loop evaluation, we follow the evaluation pipeline of Bench2Drive [23], which adopts four key metrics: Driving Score (DS), Success Rate (SR), Eficiency, and Comfortness. Success Rate measures the percentage of routes that are successfully completed within the designated time limit. Driving Score follows the CARLA [10] protocol and combines route completion with violation penalties, where infractions proportionally reduce the score through discount factors. Efficiency and Comfortness assess the speed performance and ride smoothness, respectively, of the autonomous driving policy throughout the episode.

For open-loop evaluation, we report L2 trajectory error and collision rate. We also evaluate 3D detection performance using standard nuScenes metrics, including mAP, mATE, mASE, mAOE, mAVE, and NDS, which measure detection accuracy, translation error, scale error, orientation error, velocity error, and overall detection quality, respectively. For future frame prediction, we use the Fréchet Inception Distance (FID) to evaluate how closely the distribution of generated frames matches that of the ground-truth future frames.

For VQA evaluation, we adopt the DriveLM GVQA [38] metrics, including BLEU, ROUGE-L, and CIDEr for language generation, ChatGPT score for open-ended question answering, and accuracy for multiple-choice questions.

## B More Results

## B.1 Additional Closed-Loop Evaluation Results

We provide additional closed-loop multi-ability evaluation results on Bench2Drive in Tab. 9. Compared with baseline methods, our approach achieves stronger performance in Merging, Overtaking, Emergency Brake, and Trafic Sign tasks. These gains suggest that leveraging the VLM’s reasoning capability together with future-image prediction improves overall multi-ability performance, as reflected in the higher mean score.

## B.2 Further Visualization

We present visualizations of the VQA results from open-loop evaluation in Fig. 6. These examples show that our model not only understands the current scene but also reasons efectively about future states, enabling reliable, decision-oriented responses even in complex driving scenarios and challenging weather conditions.

We further provide qualitative results for our AR and AR+Difusion architectures in Fig. 7 and Fig. 8, respectively. These visualizations indicate that both architectures can generate plausible future frames across diverse scenes and weather conditions.

## C Additional Details on Perception Module

## C.1 QT-Former Backbone

The perception module in UniDrive-WM builds on the QT-Former perception backbone [12]. As described in the main paper, QT-Former encodes multi-view observations and temporal history into structured visual representations. Specifically, we initialize learnable scene queries $Q _ { s } \in \mathbb { R } ^ { N _ { s } \times C _ { q } }$ and perception queries $Q _ { p } ~ \in ~ \mathbb { R } ^ { N _ { p } \times C _ { q } }$ , where $N _ { s }$ and $N _ { p }$ denote the numbers of scene and perception queries, and $C _ { q }$ is the query dimension. These queries interact with the current multi-view image features $F _ { m }$ and their associated 3D positional encodings through cross-attention to compress the visual observations into compact scene-aware representations. In addition, QT-Former maintains a set of history queries $Q _ { h } \in \bar { \mathbb { R } } ^ { N _ { h } \times C _ { q } }$ together with a long-term memory bank $M \in \mathbb { R } ^ { ( N _ { h } \times n ) \times \check { C } _ { q } }$ to retrieve temporally relevant information from previous frames. The updated history queries and current scene features are further projected into the LLM reasoning space, while the perception queries $Q _ { p }$ are connected to task-specific perception heads.

## C.2 Detection Heads and Supervision

Concretely, the perception branch contains multiple auxiliary multilayer perceptron (MLP) heads for 3D object detection (including critical objects and lanes), as well as trafic-state estimation and motion prediction for dynamic agents.

Among these heads, only the detection head is used to report the 3D detection metrics (e.g., mAP and NDS) in the main paper. The remaining heads are retained as auxiliary supervision to improve the quality of the shared perception features and preserve trafic-aware scene structure in the learned QT-Former representations.

Following ORION, the perception branch is pretrained as a set prediction problem with explicit supervision on these tasks. In particular, optimal queryto-object assignments are established via bipartite matching using the Hungarian algorithm. The 3D detection objective then consists of a focal loss for classification and an $\ell _ { 1 }$ loss for continuous bounding box regression (center coordinates, dimensions, yaw, and velocity). The trafic-state branch is supervised by a focal loss, and the motion-prediction branch is trained with a focal loss together with an $\ell _ { 1 }$ regression loss. These objectives provide explicit object-aware, traficaware, and motion-aware supervision for the QT-Former perception backbone.

From the perspective of UniDrive-WM, the role of the perception module is not limited to box prediction. More importantly, it acts as a structured perception encoder that provides reliable visual grounding for downstream reasoning, trajectory planning, and future image generation. By maintaining explicit supervision on critical trafic elements and dynamic cues, the perception backbone supplies the VLM with more informative scene representations for unified world modeling.

During joint planning and image generation training in UniDrive-WM, we initialize the model with the pretrained QT-Former and freeze the detection head. Therefore, the joint optimization involves only the downstream planning and image-generation objectives, while the perception module mainly serves as a stable source of structured perception features rather than being jointly optimized as an end task. This design is also consistent with our ablation results, where disabling detection supervision degrades planning performance, indicating that explicit perception learning improves the quality of the shared representations and remains important for reliable driving behavior.

## D Additional Details on Trajectory Planner

The trajectory planner in UniDrive-WM serves as a diferentiable bridge between the semantic reasoning space of the VLM and the continuous action space of future trajectories. Given the current multimodal state representation $\mathbf { s } _ { t }$ and the high-level reasoning embedding $\mathbf { h } _ { \mathrm { V L M } }$ produced by the VLM, the planner models a conditional distribution over future waypoints:

$$
p _ { \theta } \big ( \mathbf { a } _ { t : t + m } \mid \mathbf { s } _ { t } , \mathbf { h } _ { \mathrm { V L M } } \big ) ,\tag{16}
$$

where $\mathbf { a } _ { t : t + m }$ denotes the predicted future trajectory over the planning horizon.

Following the generative-planning formulation in ORION, we introduce a latent variable to bridge the gap between the reasoning space and the action space. Specifically, the planner first projects the VLM reasoning embedding into

a Gaussian latent space using lightweight MLP layers:

$$
q _ { \phi } ( \mathbf { z } _ { a } \mid \mathbf { h } _ { \mathrm { V L M } } ) = \mathcal { N } ( \pmb { \mu } _ { h } , \pmb { \sigma } _ { h } ^ { 2 } ) ,\tag{17}
$$

where $\mathbf { z } _ { a }$ denotes the latent action variable, and the mean $\pmb { \mu } _ { h }$ and variance $\pmb { \sigma } _ { h } ^ { 2 }$ are predicted from the planning-related hidden representation. To allow backpropagation through the stochastic sampling process, we employ the reparameterization trick: $\mathbf { z } _ { a } = \pmb { \mu } _ { h } + \pmb { \sigma } _ { h } \odot \pmb { \epsilon }$ , where $\epsilon \sim \mathcal { N } ( 0 , \mathbf { I } )$

The latent code is then used to decode the future ego trajectory. In practice, following ORION, we use a lightweight recurrent waypoint decoder. This decoder directly regresses the future trajectory represented as a sequence of m continuous 2D waypoints in the ego vehicle’s bird’s-eye-view (BEV) coordinate system, i.e., $\hat { \mathbf { a } } _ { t : t + m } = \{ ( \hat { x } _ { i } , \hat { y } _ { i } ) \} _ { i = 1 } ^ { m }$ . Compared with directly regressing waypoints from language features, this latent-variable design provides a smoother and more diferentiable interface between reasoning and action. This allows the planner to preserve high-level semantic intent from the VLM while producing numerically precise trajectories in continuous space.

Unlike the original ORION formulation, which explicitly aligns the reasoning token and the ground-truth trajectory in a Gaussian latent space with a KLdivergence objective, we omit the explicit KL regularization term during our joint multimodal training. We empirically found that forcing the latent space to conform strictly to a standard normal distribution can destabilize the multimodal training process in large-scale, VLM-centric setups. Instead, we optimize the planning head using the composite objective defined in the main paper:

$$
\mathcal { L } _ { \mathrm { p l a n } } = \mathcal { L } _ { \mathrm { c o l } } + \mathcal { L } _ { \mathrm { b d } } + \mathcal { L } _ { \mathrm { m s e } } ,\tag{18}
$$

where the losses provide explicit, spatially aware supervision to ensure physical safety and perception-action coupling:

– Collision Loss $( \mathcal { L } _ { \mathbf { c o l } } )$ : To explicitly couple the action space with the perception outputs, $\mathcal { L } _ { \mathrm { c o l } }$ penalizes trajectories that intersect with the predicted 3D bounding boxes of dynamic agents (supplied by the frozen detection head). This ensures that the planner respects the occupancy of surrounding trafic.

– Boundary Loss $( { \mathcal { L } } _ { \mathbf { b d } } )$ : Similarly, $\mathcal { L } _ { \mathrm { b d } }$ penalizes trajectory points that fall outside the drivable area or cross the predicted solid lane boundaries, enforcing adherence to road topology.

– MSE Loss $\left( \mathcal { L } _ { \mathrm { m s e } } \right)$ : This term is the standard $\ell _ { 2 }$ distance between the predicted waypoints $\{ ( \hat { x } _ { i } , \hat { y } _ { i } ) \} _ { i = 1 } ^ { m }$ and the ground-truth expert trajectory. It provides the primary driving demonstration signal.

From the perspective of UniDrive-WM, the trajectory planner is not merely an output head for motion prediction. Rather, it is the key module that connects reasoning and visual imagination: the planned trajectory conditions future image generation, and the generated future frames in turn provide additional supervisory signals that improve planning quality. This is supported by our ablation results, where conditioning image generation on the planning trajectory yields better planning accuracy and visual quality, aligning with the causal direction from action to future observation.

A2: "Traffic light at <-1.33, 24.63> showing red, indicating the need to stop.."

Q1: "Could you describe the overall environment and objects captured in the images provided?"  
![](images/c2ef8f0c985866f5bdb2a0073e7f17354fbf58c79ab1076d7c44e1197f0a8545.jpg)  
A1: "The scene depicts an intersection during what appears to be early evening or late afternoon, given the dark sky. The road is clear with no visible obstacles, and the traffic lights are showing red. There are no pedestrians or other vehicles in the immediate vicinity. The surroundings include a billboard, some trees, and a few buildings, suggesting a suburban setting. The road surface looks smooth and well-maintained."  
Q2: "Which objects in the scene are critical, and what effects do they have on the ego vehicle's movement?"  
Q3: "Please describe your driving behavior and explain the reasons."  
A3: "You should keep and lanefollow. The decision to keep the current speed and follow the lane is influenced by the absence of any immediate obstacles or other vehicles requiring a chang in direction or speed. The red traffic light ahead requires the vehicle to come to a complete stop before proceeding."

![](images/02a4fba63d50ed282e1948273d8b15c3915dcf4efb40faac9c5047eaef09c9ae.jpg)  
Q1: "Could you describe the overall environment and objects captured in the images provided?"  
A1: "The scene depicts an urban street during daytime under clear weather conditions. The road is dry and well-maintained, with clearly marked lanes and a double yellow line dividing the opposing traffic directions. There are two vehicles ahead in the same lane as the ego vehicle, both traveling in the same direction. The traffic lights ahead are green, allowing for uninterrupted travel. The surrounding buildings are multi-story structures typical of a city environment, with storefronts and signage visible along the sidewalks." Q2: "Which objects in the scene are critical, and what effects do they have on the ego vehicle's movement?"  
A2: "Car at <-2.52, 17.73> is 17.73 meters ahead and 2.52 meters to the left of the ego vehicle, moving at a similar speed, may influence lane choice.."  
Q3: "Please describe your driving behavior and explain the reasons."  
A3: "You should maintain your current speed and follow the lane. The decision to maintain speed and follow the lane is influenced by the presence of the car ahead in the same lane, which is moving at a similar speed, suggesting a safe following distance. The green traffic light ahead indicates that there are no immediate stops required, allowing for continuous motion. The road conditions are favorable, with no visible obstacles or hazards."

![](images/84b45c08dd35463503c6a366bbe7e14fbcbfc4f983ddcee86682f4ae67f98a11.jpg)  
Q1: "Could you describe the overall environment and objects captured in the images provided?"  
A1: "The scene depicts a rainy highway with reduced visibility due to the weather conditions. The road surface appears wet, indicating recent or ongoing precipitation. A blue car is visible in the right lane, moving away from the viewer's perspective. The surrounding area includes a barrier on the right side and greenery beyond it, with overhead signs providing direction or exit information. The overall atmosphere suggests caution due to the slippery road conditions and limited visibility."  
Q2: "Which objects in the scene are critical, and what effects do they have on the ego vehicle's movement?"  
A2: "Blue car at <2.83, 24.21> in the right lane, moving at a speed of 5.44 m/s, heading away from the ego vehicle, and potentially influencing lane-changing decisions.." Q3: Please describe your driving behavior and explain the reasons." Q3: Please describe your driving behavior and explain the reasons.'  
A3: "You should maintain your current speed and prepare to change lanes to the left. The decision to change lanes is influenced by the need to navigate around the blue car in the right lane, which is moving at a different speed and trajectory. The wet road conditions require careful maneuvering to avoid skidding or losing control during the lane change. Ensure there is sufficient space in the left lane before initiating the lane change to maintain safety."

Fig. 6: Visualization of our VQA results on Bench2Drive open-loop evaluation. For each scene, we show the multi-view input images and the bird’s-eye view (BEV). The question-answer pair includes the model’s understanding of the current state and reasoning about the ego vehicle’s movement and driving behavior. Red text highlights our method’s scene comprehension and reasoning.

![](images/8bfa830e03591a48140c046880c88206196acb869ee188f12dba3a2f00298c5d.jpg)  
Fig. 7: Qualitative results on nuScenes using the AR architecture.

Current Frame  
Future Frame  
Predicted Future Image  
![](images/e2be9bed9994d31e416a1bd0c853f384ca96c5979dc1837734960b265d7f7223.jpg)  
Fig. 8: Qualitative results on nuScenes using the AR+Difusion architecture.