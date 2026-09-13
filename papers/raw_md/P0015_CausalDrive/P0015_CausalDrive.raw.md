# CausalDrive: Real-time Causal World Models for Autonomous Driving

Tianyi Yan<sup>‡1</sup>, Huan Zheng<sup>1</sup>, Dubing Chen<sup>1</sup>, Meizhi Qu<sup>3</sup>, Yingying Shen<sup>2</sup>, Lijun Zhou<sup>2</sup>, Mingfei Tu<sup>2</sup>, Bing Wang<sup>2</sup>, Guang Chen<sup>2</sup>, Hangjun Ye<sup>2</sup>, Haiyang Sun<sup>†2</sup>, Cheng-zhong Xu<sup>1</sup>, and Jianbing Shen<sup>♠1⋆</sup>

<sup>1</sup> SKL-IOTSC, CIS, University of Macau <sup>2</sup> Xiaomi EV <sup>3</sup> CASIA

Abstract. World models have emerged as a promising paradigm for scaling autonomous driving (AD) data, yet existing video generative models fall short as interactive simulators. Layout-conditioned renderers rely on "oracle" future trajectories of all background agents, rendering them strictly non-reactive. Conversely, pure action-conditioned predictors lack semantic control over complex interactions and sufer from prohibitive difusion latencies, hindering closed-loop policy learning. To bridge this gap, we present CausalDrive, a controllable, real-time foundation driving world renderer. CausalDrive operates solely on the initial front-view frame, the ego-vehicle’s trajectory, and a macroscopic text prompt. By excluding future NPC layouts, we compel the model to intrinsically predict causal interactions, enabling text-driven control over Driving Sociology—allowing users to dynamically orchestrate diverse counterfactual reactions to identical ego-actions. To overcome the eficiency bottleneck and address the covariate shift in autoregressive generation, we propose a novel Context-Forced DMD architecture. This combines continuous flow-matching with a self-correcting distillation objective, achieving interactive speeds of 12 FPS. This breakthrough transforms the passive video generator into a playable neural simulator. We demonstrate its versatility across three downstream applications: (1) generative closed-loop evaluation with significantly mitigated collision artifacts, (2) large-scale Reinforcement Learning (RL) post-training driven by a Video2Reward module, and (3) real-time human-in-the-loop simulation. Extensive experiments validate that policies trained within CausalDrive’s reactive scenarios exhibit superior interaction capabilities in the real world.

Keywords: World Model · Simulation · Video Difusion

## 1 Introduction

The paradigm of Autonomous Driving (AD) is shifting from modular pipelines to end-to-end learning [4, 13, 16, 19, 22]. Within this transition, learning a world model [7, 8, 30, 32, 34, 35, 40] capable of simulating plausible future outcomes is envisioned as a key milestone toward high-level machine intelligence. Recent advances [2,11] in generative AI have achieved remarkable success in high-fidelity visual synthesis, precise instruction controllability [7, 8, 21], and the simulation of safety-critical corner cases [28, 33].

However, a critical dichotomy remains. Existing models [7, 8, 20, 35] primarily function as "ofline data engines" for augmentation, rather than interactive environments. SOTA driving world models [7,8,17,21,32] exhibit stunning photorealism but largely operate as "open-loop" video predictors. Relying heavily on log-replay, these models often ignore the ego-vehicle’s novel actions or fail to model the causal reactions of surrounding agents (e.g., a neighbor yielding when the ego merges). Consequently, the generated environment remains a passive "background" rather than an active participant. Furthermore, the prohibitive inference latency of difusion-based architectures (often seconds per frame) renders them impractical for computationally intensive tasks like online Reinforcement Learning (RL).

To serve as a viable alternative to real-world data collection and casual-aware simulators, we argue that the next generation of models must evolve into Foundation Driving World Renderers, holistic systems that are not just "dreamers" of video, but real-time, reactive, and physically grounded. Inspired by recent discussions on driving simulation [34,36,38], we identify four essential pillars required to unlock the full potential of world models for downstream applications: (1)High-Fidelity Visual Synthesis (Photorealism): To minimize the domain gap, the model must produce sensor-realistic outputs where perception networks can generalize directly from simulation to reality. (2) Strict Action-Controllability: The generated dynamics must faithfully reflect control signals (steering, throttle) to prevent "action-ignoring" or posterior collapse, ensuring a "left turn" command results in a physically accurate visual transition. (3) Data-Driven Reactive Agents (Driving Sociology): Unlike rigid "log-replay" systems, the model must implicitly capture the "sociology" of driving, the causal, reactive interactions between the ego-vehicle and surrounding agents (e.g., yielding, merging, or reacting to hazards) (4) Real-Time Inference Eficiency: Simulation-based applications, such as large-scale reinforcement learning (RL) or human-in-the-loop testing, require interactive frame rates (> 10 FPS) to be computationally feasible.

Despite individual advancements [9,17,36], integrating these four pillars into a unified framework remains an open challenge. Current models often trade latency for quality or sacrifice interactivity for stability. In this work, we propose CausalDrive, a Foundation Driving World Renderer designed to satisfy these desiderata simultaneously.

To systematically address the challenges of driving sociology and real-time inference, we introduce CausalDrive, an Interactive Driving World Model designed to unify photo-realistic generation with closed-loop reactive logic. Our framework encompasses three core innovations across data curation, model architecture, and acceleration. To cultivate predictive driving sociology without relying on "oracle" layout leaks, we establish SocioDrive-Bench. Unlike layoutconditioned models that passively render future bounding boxes, CausalDrive predicts futures strictly conditioned on the initial frame, ego-trajectory, and semantic prompts. By leveraging a vision-language pipeline to extract explicit causal interaction labels—such as active pressure, defensive driving, and complex negotiation—we transform raw geometric logs into sociologically-aware training curricula. Architecturally, directly converting a bidirectional video difusion model into an autoregressive (AR) streaming simulator causes expectation collapse due to the violation of probability flow injectivity. We bridge this gap by constructing a Sociology-Aware Causal AR Teacher. Conditioned via adaptive layer normalization for geometric poses and cross-attention for semantic sociology prompts, this continuous flow-matching teacher ensures mathematically sound and dynamically accurate step-by-step rollouts.

Finally, to overcome exposure bias and achieve real-time simulation speeds, we propose Self-Corrective Forcing (SCF) for difusion distillation. Autoregressive generation over long horizons inherently accumulates errors. Standard distillation fails in this regime due to a context mismatch between the teacher’s perfect history and the student’s flawed history. By explicitly forcing the AR teacher to evaluate gradients based on the student’s imperfect self-rollout, SCF teaches the student to auto-correct temporal compounding errors. This reduces the required function evaluations to $\leq 4$ steps, achieving a throughput of $\geq 1 2$ FPS with sub-second latency.

By integrating these innovations, CausalDrive efectively transforms a passive video generator into a playable neural simulator. We demonstrate its versatility across three downstream applications: closed-loop evaluation with highly consistent kinematic dynamics, eficient RL training utilizing a Video-to-Reward (V2R) module, and human-in-the-loop simulation with real-time WASD control.

Our main contributions are summarized as follows:

– We propose CausalDrive, a real-time foundation world model that strictly avoids future-layout conditioning, unifying photo-realistic generation with closed-loop reactive logic for autonomous driving.

– We introduce SocioDrive-Bench, establishing a novel VLM/LLM-driven taxonomy to extract and formalize causal driving sociology (e.g., yielding, negotiating), enabling semantic control over multi-agent interactions.

We identify the architectural and context-mismatch bottlenecks in streaming video generation, and propose a novel Context-Forced DMD framework over a Causal AR Flow-Matching Teacher. This enables robust, infinitehorizon generation at $\geq 1 2 ~ \mathrm { F P S }$

– Extensive experiments demonstrate that CausalDrive acts as a superior neural simulator. RL policies trained safely within its hallucinated, safety-critical scenarios exhibit significantly improved interaction capabilities.

![](images/da305d91987a8dc1b413573069ebcfdb6127552e99873fa1d7273106cc5eb35d.jpg)  
Fig. 1: Top: Semantic Control of Driving Sociology: Unlike layout-conditioned renderers that require "oracle" future boxes of all agents, CausalDrive generates interactive futures. Given the exact same initial state and ego-trajectory (nudging into an intersection), modifying the prompt allows us to dynamically simulate diverse counterfactual reactions from surrounding agents (e.g., politely yielding vs. aggressively rushing). Down: The reactive API that powers three distinct downstream applications: (1) Playable Interactive World, ofering a playable, low-latency virtual world controlled via WASD/steering wheels. (2) Closed-Loop Evaluation, providing a "zero-ghosting" proving ground for planners; and (3) RL Post-Training, where an agent safely learns from simulated safety-critical scenarios via a Video2Reward (V2R) module.

## 2 Related Work

## 2.1 Generative World Models for Autonomous Driving

The advent of large-scale generative models has catalyzed the development of world models for autonomous driving (AD), aiming to synthesize infinite driving scenarios for data augmentation and policy learning [12, 30, 40]. Current video-based driving models broadly fall into two paradigms based on their conditioning strategies. The first paradigm, Layout-Conditioned Renderers (e.g., MagicDrive [7, 8], UniScene [17], Panacea [32]), synthesizes high-fidelity videos conditioned on the complete future trajectories or 3D bounding boxes of all trafic participants. While producing stable visuals, these models act as "oracles" rather than simulators; they are fundamentally non-reactive because the future states of surrounding agents are hard-coded inputs rather than dynamically inferred responses. The second paradigm, Action-Conditioned Predictors (e.g., Vista [9], Orbis [24], Drive-WM [31]), predicts future frames based solely on the ego-vehicle’s action and past context. While conceptually closer to true world models, they often sufer from "posterior collapse" (ignoring ego-actions) and lack macroscopic semantic control over the diverse, long-tail behaviors of surrounding agents. In contrast, CausalDrive takes a hybrid approach: we strictly omit future NPC layouts to compel genuine causal prediction, while introducing a macroscopic sociology prompt to semantically orchestrate the predicted interactions, achieving both strict action-controllability and semantic diversity.

## 2.2 Reactive Simulation and Driving Sociology

Closed-loop policy evaluation and Reinforcement Learning (RL) require environments where non-player characters (NPCs) react logically to the ego-vehicle. Traditional graphics-based simulators (e.g., CARLA [6], MetaDrive [18]) provide interactivity but sufer from a severe visual sim-to-real gap and utilize rigid, rulebased NPCs that fail to capture human-like stochasticity. To address the visual gap, data-driven approaches often rely on Log-Replay from real-world datasets (e.g., nuPlan [3,5]). However, log-replay is inherently open-loop; if the ego-vehicle deviates from the logged trajectory, surrounding vehicles fail to react, leading to the unrealistic "ghost efect" (false-positive collisions) [34, 38]. While eliminating these artifacts entirely remains an open challenge, CausalDrive significantly mitigates them by strictly enforcing causal dependencies. We introduce SocioDrive-Bench, shifting the focus from geometric trajectories to Driving Sociology. By leveraging Large Vision-Language Models (VLMs), we explicitly extract causal interaction labels (e.g., yielding, negotiating), bridging the gap between raw perceptual logs and cognitive reactive simulation.

## 2.3 Eficient Video Generation and Distillation

Transforming video difusion models into real-time interactive simulators remains a formidable challenge due to the high Number of Function Evaluations (NFE) required by iterative solvers. While generalized distillation techniques like Consistency Models [27] and Distribution Matching Distillation (DMD) [39] have accelerated text-to-image and short-video generation, applying them to open-ended, streaming driving simulation introduces unique bottlenecks. Stateof-the-art video Difusion Transformers (DiTs) [25] rely on bidirectional temporal attention. Directly distilling a bidirectional teacher into an Autoregressive (AR) streaming student violates Probability Flow ODE (PF-ODE) injectivity—where multiple valid futures collapse into blurred predictions [14, 41]. Furthermore, long-horizon AR generation sufers from exposure bias, where small student errors compound over time. To systematically resolve this, we propose a mathematically sound pipeline: we first train a Causal AR Teacher via Continuous Flow Matching to guarantee conditional alignment, and then introduce Context-Forced DMD. By forcing the teacher to evaluate gradients on the student’s flawed autoregressive rollouts, we explicitly correct exposure bias, successfully compressing high-fidelity reactive generation to ≤ 4 steps (≥ 12 FPS).

## 3 Methodology

Our ultimate goal is to construct a real-time, interactive driving world model capable of modeling the causal interactions among various trafic participants (agents). Let $\mathbf { x } \in \mathbb { R } ^ { H \times W \times 3 }$ denote a visual observation. Instead of passively predicting video continuations, the model must act as a reactive simulator, approximating the transition dynamics $p _ { \theta } ( C _ { 1 : K } \mid C _ { 0 } , \mathcal { A } _ { 1 : K } )$ , where $C _ { k }$ represents a temporal chunk of latent visual states, and $\mathcal { A } _ { 1 : K }$ denotes a streaming sequence of external control signals.

![](images/67e2f69ac7bb8de664175c8ef67f9613767d45c376e41192a9d411c0abb5f9ff.jpg)  
Fig. 2: Architecture and Training Pipeline of CausalDrive. (a) Stage 0: The base model employs Block Causal Attention for O(1) streaming. Ego-trajectories (P) and sociology prompts (B) are injected via AdaLN and cross-attention, respectively. (b) Stage 1: To prevent probability flow injectivity violations, we train a continuous flow-matching Autoregressive (AR) teacher using strict Teacher Forcing on groundtruth history $\left( C _ { < k } \right)$ . (c) Stage 2: Self-Corrective DMD. To mitigate exposure bias during long-horizon rollouts, the student performs an AR self-rollout to generate a flawed memory context $( \hat { C } _ { \mathrm { s t u } } )$ . The distillation gradient $\nabla \mathcal { L } _ { \mathrm { D M D } }$ is evaluated by forcing the frozen teacher to condition on this flawed context, thereby teaching the student to auto-correct accumulated temporal errors.

Transforming a powerful but slow bidirectional video generative model into an ultra-fast autoregressive (AR) interactive simulator presents two fundamental challenges: (1) the architectural gap, where distilling a bidirectional teacher into a causal student violates PF-ODE injectivity, causing blurry generation; and (2) the context mismatch, where error accumulates over long-horizon autoregressive rollouts (exposure bias). To systematically address these issues, we formulate our method into three parts. We first provide the preliminaries in Sec. 3.1. Then, we introduce the construction of a driving sociology-aware causal autoregressive teacher in Sec. 3.2. Finally, we detail the few-step distillation framework via Causal ODE and Context-Forced DMD in Sec. 3.3.

## 3.1 Preliminaries

Bidirectional Video Difusion Models. Recent large-scale video generation heavily relies on continuous-time difusion models parameterized by Difusion Transformers (DiTs). Let $\mathbf { z } _ { 0 } \sim \ p _ { \mathrm { d a t a } }$ denote a real video chunk in the latent space, and ${ \bf z } _ { 1 } \sim \mathcal { N } ( { \bf 0 } , { \bf I } )$ denote standard Gaussian noise. Under the Flow Matching (FM) framework [23], the PF-ODE governing the marginal distributions is defined as d $\mathbf { \boldsymbol { \mathsf { z } } } _ { t } = v _ { \theta } ( \mathbf { \boldsymbol { \mathsf { z } } } _ { t } , t ) \mathrm { d } t$ , for $t \in [ 0 , 1 ]$ . The optimal transport path corresponds to linear interpolation: $\psi _ { t } ( \mathbf { z } _ { 0 } ) = t \mathbf { z } _ { 1 } + ( 1 - t ) \mathbf { z } _ { 0 }$ . The network $v _ { \theta }$ is trained to

regress the velocity field:

$$
\mathcal { L } _ { \mathrm { F M } } ( \theta ) = \mathbb { E } _ { \mathbf { z } _ { 0 } , \mathbf { z } _ { 1 } , t } [ | | v _ { \theta } ( \psi _ { t } ( \mathbf { z } _ { 0 } ) , t ) - ( \mathbf { z } _ { 1 } - \mathbf { z } _ { 0 } ) | | ^ { 2 } ]\tag{1}
$$

Standard video DiTs employ $v _ { \theta }$ employs Bidirectional Attention across the temporal dimension. When denoising frame $\boldsymbol { x } _ { t } ^ { ( i ) }$ , the model attends to all other frames, including the future. While excelling at fixed-length generation, this non-causal nature prevents real-time, open-ended interactivity.

Chunk-wise Autoregressive Generation. To enable streaming generation, we factorize the joint distribution of a video into non-overlapping temporal chunks $C _ { 1 } , C _ { 2 } , \dots , C _ { K }$

$$
p _ { \theta } ( C _ { 1 : K } ) = \prod _ { k = 1 } ^ { K } p _ { \theta } ( C _ { k } \mid C _ { < k } , { \mathcal { A } } _ { \leq k } )\tag{2}
$$

We adopt a Block Causal Attention mask: tokens within the same chunk $C _ { k }$ attend to each other bidirectionally to preserve local spatio-temporal dynamics, while attention to past chunks $C _ { < k }$ is strictly causal and cached via a Key-Value (KV) mechanism to ensure $O ( 1 )$ streaming complexity.

## 3.2 Driving Sociology-Aware Causal Autoregressive Teacher

Directly distilling a bidirectional model into an AR student causes conditional expectation collapse[casual forcing]. Therefore, we first construct a mathematically sound Causal Autoregressive Teacher, denoted as $v _ { \theta ^ { * } } ^ { \mathrm { A R } }$

Crucially, driving is not merely following geometric trajectories; it is a highly interactive multi-agent social process. Thus, we condition our AR teacher on a hybrid control signal $\mathcal { A } = ( \mathcal { P } , \mathcal { B } )$ , establishing a causal hierarchy between lowlevel ego-mechanics and high-level sociology.

Given the ego-vehicle trajectory P, we encode the continuous camera poses into Plücker coordinates and process them via a Multi-Layer Perceptron (MLP) to obtain spatial modulation parameters $\mathbf { h } _ { \mathrm { g e o } }$ . Simultaneously, the discrete behavioral description B (e.g., "ego vehicle yields to an aggressive pedestrian") is mapped into continuous semantic embeddings $\mathbf { E } _ { \mathrm { s o c i o } }$ via a pre-trained text encoder. It is important to note that B serves as a global "sociological prior" (e.g., a "Polite" scene implies a higher probability of yielding across all agents) rather than a rigid script for specific instance-level control.

Within each DiT block, we explicitly decouple these conditions to model causal interactions. Let z denote the intermediate latent feature. The geometric action imposes a hard spatial constraint via Adaptive Layer Normalization (AdaLN), while the sociology prompt modulates the multi-agent reaction via Cross-Attention:

$$
\hat { \mathbf { z } } = \mathbf { z } + \mathrm { S e l f A t t n } \big ( \mathrm { A d a L N } ( \mathbf { z } , \mathbf { h } _ { \mathrm { g e o } } ) \big )\tag{3}
$$

$$
{ \bf z } ^ { \prime } = \hat { \bf z } + \mathrm { C r o s s A t t n } \big ( \mathrm { Q } = \hat { \bf z } , \mathrm { K } , \mathrm { V } = { \bf E } _ { \mathrm { s o c i o } } \big )\tag{4}
$$

This architectural design strictly enforces causality: Eq. 3 guarantees that the visual perspective precisely shifts according to the ego-vehicle’s steering and throttle, preventing "action-ignoring." Concurrently, Eq. 4 allows the semantic prior $\mathbf { E } _ { \mathrm { s o c i o } }$ to query the spatially-anchored features, hallucinating logical reactions from surrounding agents (e.g., synthesizing a braking neighbor) without interfering with the ego-trajectory’s geometric fidelity.

We train this causal AR teacher $v _ { \theta } ^ { \mathrm { A R } }$ using Teacher Forcing. Specifically, when training the k-th chunk, the attention mechanism is strictly conditioned on the clean, ground-truth historical prefix $C _ { < k }$ , rather than a noisy prefix. This guarantees that the training objective perfectly aligns with the inference distribution, establishing a mathematically sound and dynamically accurate AR teacher.

## 3.3 Few-Step Distillation

While the AR teacher achieves high fidelity, it requires numerous ODE solver steps (e.g., 50 steps), violating the latency constraints of a real-time interactive world model. We compress the generation to 1-4 steps via a two-stage distillation process.

Causal ODE Distillation. A fundamental requirement for ODE distillation is frame-level injectivity: each noisy frame must map to a unique clean frame. Distilling an AR student from a bidirectional teacher violates this, as the absence of future frames causes one noisy state to map to multiple possible clean outcomes, resulting in blurred predictions. To bridge this architectural gap, we perform distillation strictly using trajectories generated by our Causal AR Teacher $v _ { \theta } ^ { \mathrm { A R } }$ Given a clean history $C _ { < k }$ and actions $\scriptstyle A \leq _ { k }$ , we sample exact PF-ODE trajectories from noise to data. The AR student $G _ { \phi }$ is trained to regress the clean target $C _ { k } ^ { ( 0 ) }$ from intermediate noisy states $C _ { k } ^ { ( t ) }$

$$
\phi ^ { * } = \arg \operatorname* { m i n } _ { \phi } \mathbb { E } _ { C _ { < k } , t } \left[ \left\| G _ { \phi } ( C _ { k } ^ { ( t ) } , C _ { < k } , \boldsymbol { A } _ { \le k } , t ) - C _ { k } ^ { ( 0 ) } \right\| ^ { 2 } \right]\tag{5}
$$

Since both the teacher and student are causal, frame-level injectivity perfectly holds, allowing the student to correctly learn the flow map without detail degradation.

Context-Forced DMD for Infinite Horizon. To further reduce sampling to 1-4 steps, we apply Distribution Matching Distillation (DMD). However, in autoregressive long-horizon generation, the student accumulates errors and deviates from the training distribution (Exposure Bias). Standard DMD fails here because it creates a Context Mismatch: the teacher evaluates gradients based on perfect ground-truth history, while the student generates based on its own flawed history. This phenomenon is akin to the "Covariate Shift" problem in imitation learning.

To resolve this, we propose Context Forcing. During training, the student performs an N-chunk Self-Rollout to construct a flawed memory context $\hat { C } _ { s t u }$ When computing the real score using the AR Teacher, we explicitly force the Teacher to condition on this student-generated history $\hat { C } _ { s t u }$ , rather than the ground truth:

$$
\nabla _ { \phi } \mathcal { L } _ { \mathrm { D M D } } \approx \mathbb { E } \left[ s _ { \mathrm { r e a l } } \big ( \hat { C } _ { k } ^ { ( t ) } , t \mid \hat { C } _ { s t u } , A \big ) - s _ { \mathrm { f a k e } } \big ( \hat { C } _ { k } ^ { ( t ) } , t \mid \hat { C } _ { s t u } , A \big ) \right] \frac { \partial \hat { C } } { \partial \phi }\tag{6}
$$

By forcing the teacher to “clean up the student’s mess,” the distillation gradient explicitly teaches the student how to recover from its own errors. Furthermore, to preserve high-frequency road textures (e.g., lane markings) over long simulations, we attach an adversarial discriminator to the fake score network, pushing the few-step generated driving chunks to be indistinguishable from real trafic videos.

## 3.4 Downstream Applications Formulation

By satisfying real-time (≥ 12 FPS) and reactive requirements, CausalDrive naturally serves as a universal interactive API. We formulate three specific downstream integrations:

Generative Closed-loop Simulation. We formulate CausalDrive as an OpenAI Gym environment. At step k, a planner $\pi _ { \mathrm { p l a n } }$ observes the generated visual state $\mathbf { x } _ { k }$ and outputs geometric action $\mathcal { P } _ { k }$ . ForceDrive acts as the transition function: $\mathbf { x } _ { k + 1 } = \mathrm { F o r c e D r i v e } ( \mathbf { x } _ { k } , \mathcal { P } _ { k } , \mathcal { B } _ { \mathrm { p r o m p t } } )$ . This eliminates the "ghost efect" found in standard log-replay, as neighbors dynamically react based on sociology priors B.

Eficient Policy Post-training via RL. CausalDrive functions as a safe, infinite RL hallucination. We define a continuous MDP where state $s _ { k } = \mathbf { x } _ { k }$ and action $a _ { k } = \mathcal { P } _ { k }$ . To provide dense feedback, we append a diferentiable Videoto-Reward (V2R) module $R _ { \psi }$ that maps generated chunks to scalar rewards: $r _ { k } = R _ { \psi } ( { \bf x } _ { k + 1 } ) = w _ { 1 } r _ { \mathrm { c o l } } + w _ { 2 } r _ { \mathrm { l a n e } }$ . The policy $\pi _ { \omega }$ is optimized to maximize expected returns entirely within the simulated domain.

Human-in-the-Loop Simulation. The sub-100ms latency of our Context-Forced distillation enables human drivers to inject streaming control signals $\mathcal { A } _ { k }$ via hardware (e.g., steering wheels), facilitating real-time counterfactual safety testing and high-quality DAgger (Dataset Aggregation) collection.

## 4 SocioDrive-Bench: A Benchmark for Driving Sociology

Current autonomous driving datasets (e.g., nuScenes, Waymo) primarily function as open-loop geometric logs. While they provide precise trajectories, they lack explicit annotations of causal interactions—the underlying social contracts and reactive negotiations among trafic participants. To train and evaluate the sociology-aware world model proposed in Section 3, we introduce SocioDrive-Bench, a large-scale, multimodal benchmark explicitly annotated with driving sociology and causal reactions.

SocioDrive-Bench comprises 20K video clips, which is sourced heterogeneously: 80% of the data is mined from real-world logs (nuPlan [3]) to capture nominal, photorealistic human interactions, while the remaining 20% is generated via the CARLA simulator [6] to inject safety-critical and collision events, thus mitigating the "survival bias" inherent in expert datasets.

## 4.1 Taxonomy of Causal Interactions

We formalize driving sociology into three distinct behavioral categories. Let ${ \mathcal T } _ { \mathrm { e g o } } = ( { \bf p } , { \bf v } , { \bf a } , \theta )$ denote the ego-vehicle state, $\tau _ { \mathrm { { o b j } } }$ denote the state of surrounding agents, and M represent the map topology. Rather than relying on simple proximity, we systematically mine scenarios based on strict kinematic triggers to form explicit causal pairs.

Ego-Initiated Interactions (Active Pressure). This category encapsulates scenarios where the environment dynamically reacts to the ego-vehicle’s proactive maneuvers, providing crucial supervision for predicting yielding or evasion behaviors. For instance, an aggressive cut-in event is triggered when the ego crosses lane boundaries $\mathcal { M } _ { \mathrm { l a n e } }$ while a rear vehicle is within a 15m proximity. A valid interaction is recorded only if the rear vehicle exhibits significant deceleration $( a _ { \mathrm { o b j } } < - 1 . 5 ~ \mathrm { m / s } ^ { 2 } )$ or a sudden drop in Time-to-Collision (TTC) within ∆t seconds, forming the causal label: [Ego Cut-in] → [Forced Rear Car Brake]. Similarly, tailgating is identified when $v _ { \mathrm { e g o } } > 3 0$ km/h and the Time Headway (THW) to the lead vehicle remains under 1.0s for at least 3s, leading to a forced yield or acceleration from the leading agent.

Ego-Reactive Interactions (Defensive Driving). Conversely, this category captures environmental anomalies that force the ego-vehicle to alter its state. These scenarios are essential for providing the "negative rewards" required in downstream RL safety training. We identify hazard responses when a neighboring vehicle laterally invades the ego’s lane, or a Vulnerable Road User (VRU) intersects the future path, necessitating an emergency maneuver $\left( a _ { \mathrm { e g o } } < - 3 ~ \mathrm { m / s } ^ { 2 } \right.$ or excessive lateral jerk). Another common trigger is the lead car hard brake, recorded when $a _ { \mathrm { l e a d } } < - 3 ~ \mathrm { m / s } ^ { 2 }$ is followed by a corresponding deceleration from the ego with a reaction delay $\tau < 1$ .0s. These extract explicit defensive causalities, such as [Neighbor Cut-in] → [Forced Ego Emergency Brake].

Complex Negotiation and Game Theory. The highest density of driving sociology occurs during low-speed, mutual probing where right-of-way is ambiguous. Unprotected intersections are prime examples, triggered when the ego’s intended path conflicts with oncoming trafic. We detect "creeping" behaviors $( 0 < v _ { \mathrm { e g o } } < 5 $ km/h for > 2s), which branch into mutually exclusive outcomes: either the oncoming trafic yields, or the ego halts. Similarly, narrow passages restrict dual passage, forcing implicit negotiation until one party yields. These scenarios train the world model to synthesize the nuanced hesitation and game-theoretic resolutions inherent in human driving.

## 4.2 Automated Annotation Pipeline via Vision-Language Models

Extracting high-level semantic sociology from raw pixels and numeric trajectories is non-trivial. Rule-based scripts are notoriously brittle against the long-tail diversity of the real world. To automate the annotation of millions of frames, we propose a two-stage, Large Vision-Language Model (VLM) powered pipeline.

Phase 1: Clip-Level Micro-Analysis (VLM). We slice the multi-view (Left, Front, Right) video stream into 4-second clips (2Hz sampling). A VLM (e.g., GPT-4o) processes these frames alongside system prompts to output a strictly formatted JSON structure. Crucially, we enforce Feature Disentanglement at this stage: the VLM must separately parse road\_structure, and vulnerable\_road\_users (VRUs). For world modeling, decoupling VRUs from vehicles is essential, as pedestrian kinematics require entirely diferent attention priors than rigid bodies.

Phase 2: Sequence-Level Macro-Synthesis (LLM). Independent 4- second clip analysis often introduces temporal truncation (e.g., unnatural transitions between states). To resolve this, a Large Language Model (LLM) aggregates the sequential JSON annotations into a modular, macroscopic scene summary. This stage guarantees three functional properties for our world model: Temporal Smoothing: The LLM synthesizes an ego\_behavior\_narrative, linguistically smoothing the 2Hz sampling gaps to provide a continuous, chronological condition for the trajectory generation. Interaction Aggregation: By extracting a key\_interaction\_summary, we explicitly map the spatial awareness (Left/Front/Right views) to the dynamic agents, forming the precise sociology prior $\boldsymbol { B } _ { k }$ injected into our cross-attention blocks (Sec. 3). Queryability and Hard-Case Mining: The pipeline extracts critical\_events into structured arrays. This allows us to programmatically query our database for "safety-critical scenarios involving pedestrians," facilitating targeted curriculum generation for RL training without requiring repeated semantic processing.

Through this pipeline, SocioDrive-Bench transforms raw driving logs into a highly structured, sociologically-aware dataset, directly bridging the gap between perception data and cognitive driving simulation.

## 5 Experiments

Our empirical evaluation is designed to systematically validate CausalDrive across three progressive dimensions: (1) Simulation Reliability, ensuring the generated world is visually faithful, controllable, and real-time; (2) Driving Sociology & Reactivity, quantifying the model’s ability to synthesize causal multi-agent interactions via our proposed benchmark; and (3) Downstream Applications, demonstrating its eficacy as a closed-loop evaluation engine and a generative RL post-training environment.

## 5.1 Experimental Setup

Training Datasets and Curriculum. We employ a progressive, multi-stage data curriculum to train CausalDrive. For foundational pretraining, we utilize

1,700 hours of front-view driving videos from the large-scale OpenDV dataset [37] to learn robust real-world visual priors. Subsequently, we fine-tune the model using the nuPlan dataset [3] processed through our Phase-1 annotation pipeline, alongside the proposed SocioDrive-Bench to explicitly instill driving sociology priors. Crucially, following the insights from ReSim [36], we augment our training corpus with unsafe, safety-critical scenarios synthesized via Bench2Drive [15]. This out-of-distribution (OOD) augmentation is vital for enhancing the model’s action-controllability when conditioned on uncommon, non-expert trajectories (e.g., aggressive steering or imminent collisions) typically absent in expert logs.

Implementation Details. Our core flow-matching DiT backbone is initialized from the state-of-the-art Wan2.1-1.3B [29] video generation model. The Stage-0 training is distributed across 8 NVIDIA H20 GPUs with a total batch size of 4. We optimize the network using AdamW with a constant learning rate of $1 \times 1 0 ^ { - 5 }$ . Due to space constraints, the comprehensive hyperparameters for the Stage-1 Causal AR Teacher-Forcing and the Stage-2 Context-Forced DMD algorithms are detailed in the Supplementary Material.

Baselines and Evaluation Metrics. Our evaluation spans three dimensions: visual fidelity (FID, FVD), trajectory controllability (Average/Final Displacement Error: ADE/FDE), and our novel sociology metric—Yielding Compliance Rate (YCR). More details are included in supplementary materials

## 5.2 Simulation Reliability: Fidelity, Eficiency, and Controllability

Following the evaluation protocols of ReSim [36] and Orbis [24], a foundation world model must strictly adhere to the injected ego-trajectory while maintaining high-fidelity visuals at interactive speeds.

Visual Fidelity and Inference Speed. As shown in Table 1, we achieve an FVD of 121.6, outperforming or matching existing video difusion models (Vista, Orbis). This proves that our Context-Forced DMD efectively preserves spatial-temporal consistency without blurring. Crucially, CausalDrive achieves an inference throughput of 12.4 FPS on a single NVIDIA A100 GPU—an order of magnitude faster than baseline difusion simulators, successfully crossing the threshold required for human-in-the-loop and online RL operations.

Action Controllability. A reactive simulator must not sufer from "posterior collapse" (ignoring control signals). To quantify this, we deploy a pre-trained inverse dynamics model (tracker) to estimate the ego-vehicle’s trajectory directly from the generated video pixels, and compute the Average/Final Displacement Errors (ADE/Frechet) against the injected condition trajectory $\mathcal { P } _ { 1 : K }$ . Table 1 demonstrates that CausalDrive achieves best metrics, confirming that our continuous flow-matching and AdaLN conditioning precisely translate geometric actions into visual dynamics.

## 5.3 Evaluating Driving Sociology and Reactivity

Beyond trajectory following, a reactive simulator must synthesize logical multiagent interactions. We utilize SocioDrive-Bench to quantify this reactivity. We input aggressive ego-trajectories (e.g., forced cut-ins) and measure the Yielding Compliance Rate (YCR)—the frequency at which generated neighbors correctly decelerate.

Table 1: Simulation Reliability Comparison. We evaluate visual fidelity (FID, FVD), inference speed (FPS), and Action Controllability (ADE/FDE between the injected trajectory and the trajectory estimated from generated pixels) on nuplan dataset. CausalDrive achieves comparable visual quality and SOTA controllability while running at real-time speeds.
<table><tr><td>Method</td><td>|Fidelity ↓| FVD</td><td>ADE Prec. ↑ Rec. ↑Prec. ↑ Rec. ↑</td><td></td><td>Frechet</td><td>|Speed ↑| FPS</td><td>Real-time</td></tr><tr><td>Cosmos [1]</td><td>291.80</td><td></td><td></td><td></td><td>≈ 0.7</td><td>x</td></tr><tr><td>Vista [9]</td><td>323.37</td><td>0.25</td><td>0.48</td><td>0.39 0.45</td><td>≈ 0.3</td><td>x</td></tr><tr><td>GEM [10]</td><td>291.84</td><td>0.27</td><td>0.47</td><td>0.33 0.54</td><td>≈ 0.5</td><td>x</td></tr><tr><td>Orbis* [24]</td><td>196.21</td><td>0.39</td><td>0.48</td><td>0.46 0.55</td><td>≈ 1.2</td><td>x</td></tr><tr><td>CausalDrive+|</td><td>113.6</td><td>0.47</td><td>0.55</td><td>0.56 0.61</td><td>≈ 0.5</td><td>x</td></tr><tr><td>CausalDrive</td><td>121.6</td><td>0.45</td><td>0.52</td><td>0.53 0.59</td><td>12.4</td><td>√</td></tr></table>

As shown in Table 2, pure action-conditioned predictors like Vista often result in unrealistic collisions ("ghosting"), yielding only 12.5% of the time. In contrast, by conditioning on the semantic prompt B ("Polite"), CausalDrive explicitly models the causal reaction, achieving an 82.0% YCR and reducing the False-Collision Rate (FCR) to 18.0%. This confirms our model’s ability to synthesize diverse sociological behaviors controlled by language prompts.

Table 2: Reactivity Evaluation on SocioDrive-Bench. We measure the Yielding Compliance Rate (YCR) and False-Collision Rate (FCR) during aggressive egomaneuvers. CausalDriveeliminates the ghost efect and synthesizes highly reactive NPC behaviors.
<table><tr><td>Method</td><td>|Sociology Control|Yielding Rate (YCR) ↑ False-Collision (FCR) ↓</td><td></td><td></td></tr><tr><td>Log-Replay(GT)</td><td>x</td><td>0.0%</td><td>100.0% (Ghosting)</td></tr><tr><td>Vista [9]</td><td>x</td><td>12.5%</td><td>87.5%</td></tr><tr><td>CausalDrive</td><td>√(&quot;Polite&quot;)</td><td>82.0%</td><td>18.0%</td></tr></table>

## 5.4 Downstream Applications

Generative Closed-Loop Simulation. To prove CausalDriveis a reliable proving ground, we evaluate planners (e.g., UniAD [13]) inside our simulator. As shown in Table 3, evaluating under the PDM-Closed protocol reveals that planners tested in CausalDrive experience significantly fewer "ghost" collisions and achieve higher success rates compared to Log-Replay or other generative baselines, demonstrating our fidelity and reactive realism.

Table 3: Generative Closed-Loop Evaluation. Planner performance (e.g., UniAD) evaluated under the PDM-Closed protocol. CausalDrive provides a highly realistic closed-loop testbed, significantly reducing unrealistic "ghost" collisions compared to Log-Replay.
<table><tr><td>Simulation Env.</td><td>PDMS 个 RC ↑</td><td>ADS↓</td></tr><tr><td>DriveArena [38]</td><td>0.6901</td><td>0.0641 0.0508</td></tr><tr><td>DrivingSphere [34]</td><td>0.7281</td><td>0.1170 0.0851</td></tr><tr><td>CausalDrive(Ours)|</td><td>0.7792</td><td>0.1752 0.1365</td></tr></table>

Eficient RL Post-Training. Finally, we validate CausalDrive as a generative data engine for policy improvement. We benchmark our RL-post-trained agent against SOTA learning-based planners (e.g., UniAD, DifusionDrive) on the Navsim evaluation protocol. As shown in Table 4, our agent achieves stateof-the-art performance with a PDMS score of 90.7. More importantly, the agent trained in CausalDrive achieves a perfect Comfort score of 100 and the highest Time-to-Collision (TTC) of 94.7. The ability to safely experience "counterfactual crashes" inside CausalDrive allows the policy to discover emergent defensive driving strategies, leading to superior safety metrics compared to models trained purely on static expert datasets.

Table 4: RL Post-Training Performance on Navsim. Learning from counterfactual interactions in our impartial environment using DifusionDrive [22] leads to superior safety (lower collision rates) and success rates.
<table><tr><td>Policy Method</td><td>|NC ↑ DAC ↑ TTC ↑ Comf. ↑ EP ↑ PDMS ↑</td><td></td><td></td><td></td><td></td></tr><tr><td>UniAD [13]</td><td>97.8 91.9</td><td>92.9</td><td>100</td><td>78.8</td><td>83.4</td></tr><tr><td>DriveDPO [26]</td><td>98.5 98.1</td><td>94.8</td><td>99.9</td><td>84.3</td><td>90.0</td></tr><tr><td>DiffusionDrive [22] [22]</td><td>98.2 96.2</td><td>94.7</td><td>100</td><td>82.2</td><td>88.1</td></tr><tr><td>AD-R1 [33]</td><td>98.5 97.5</td><td>94.6</td><td>100</td><td>84.8</td><td>89.8</td></tr><tr><td>DiffusionDrive-v2 [22]</td><td>98.4 98.3</td><td>94.6</td><td>100</td><td>85.0</td><td>90.3</td></tr><tr><td>RL in CausalDrive</td><td>98.7 98.2</td><td>94.7</td><td>100</td><td>85.1</td><td>90.7</td></tr></table>

## 6 Conclusion

In this paper, we presented CausalDrive, a real-time foundation driving world renderer that transforms passive video generation into a reactive neural simulator. By omitting "oracle" future layouts and leveraging our VLM-curated

SocioDrive-Bench, we compel the model to predict causal multi-agent interactions strictly from the initial frame, ego-trajectory, and semantic prompts. To overcome the latency and exposure bias of autoregressive generation, we proposed a novel Context-Forced DMD framework. This distillation strategy explicitly corrects temporal compounding errors, compressing inference to $\leq 4$ steps and achieving ≥ 12 FPS. Extensive experiments demonstrate that CausalDrive efectively eliminates the "ghost efect" in closed-loop evaluations and serves as a highly scalable generative environment for RL post-training, yielding policies with superior defensive driving capabilities. Extending this monocular paradigm to multi-camera surround-view systems remains our future work.

## Acknowledgements

We use publicly available datasets, models ,and code resources, including nuScenes, Bench2Drive, nuplan and other public research resources. We confirm that all such resources are used solely for academic research purposes and not for any commercial activity, in accordance with their respective licenses and terms of use.

## References

1. Agarwal, N., Ali, A., Bala, M., Balaji, Y., Barker, E., Cai, T., Chattopadhyay, P., Chen, Y., Cui, Y., Ding, Y., et al.: Cosmos world foundation model platform for physical ai. arXiv preprint arXiv:2501.03575 (2025)

2. Blattmann, A., Dockhorn, T., Kulal, S., Mendelevitch, D., Kilian, M., Lorenz, D., Levi, Y., English, Z., Voleti, V., Letts, A., et al.: Stable video difusion: Scaling latent video difusion models to large datasets. arXiv preprint arXiv:2311.15127 (2023)

3. Caesar, H., Kabzan, J., Tan, K.S., Fong, W.K., Wolf, E., Lang, A., Fletcher, L., Beijbom, O., Omari, S.: nuplan: A closed-loop ml-based planning benchmark for autonomous vehicles. arXiv preprint arXiv:2106.11810 (2021)

4. Chen, S., Jiang, B., Gao, H., Liao, B., Xu, Q., Zhang, Q., Huang, C., Liu, W., Wang, X.: Vadv2: End-to-end vectorized autonomous driving via probabilistic planning. arXiv preprint arXiv:2402.13243 (2024)

5. Dauner, D., Hallgarten, M., Li, T., Weng, X., Huang, Z., Yang, Z., Li, H., Gilitschenski, I., Ivanovic, B., Pavone, M., et al.: Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking. Advances in Neural Information Processing Systems 37, 28706–28719 (2024)

6. Dosovitskiy, A., Ros, G., Codevilla, F., Lopez, A., Koltun, V.: Carla: An open urban driving simulator. In: Conference on robot learning. pp. 1–16. PMLR (2017)

7. Gao, R., Chen, K., Xiao, B., Hong, L., Li, Z., Xu, Q.: Magicdrivedit: Highresolution long video generation for autonomous driving with adaptive control. arXiv preprint arXiv:2411.13807 (2024)

8. Gao, R., Chen, K., Xie, E., Hong, L., Li, Z., Yeung, D.Y., Xu, Q.: Magicdrive: Street view generation with diverse 3d geometry control. arXiv preprint arXiv:2310.02601 (2023)

9. Gao, S., Yang, J., Chen, L., Chitta, K., Qiu, Y., Geiger, A., Zhang, J., Li, H.: Vista: A generalizable driving world model with high fidelity and versatile controllability. Advances in Neural Information Processing Systems 37, 91560–91596 (2024)

10. Hassan, M., Stapf, S., Rahimi, A., Rezende, P., Haghighi, Y., Brüggemann, D., Katircioglu, I., Zhang, L., Chen, X., Saha, S., et al.: Gem: A generalizable ego-vision multimodal world model for fine-grained ego-motion, object dynamics, and scene composition control. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 22404–22415 (2025)

11. Ho, J., Jain, A., Abbeel, P.: Denoising difusion probabilistic models. Advances in neural information processing systems 33, 6840–6851 (2020)

12. Hu, A., Russell, L., Yeo, H., Murez, Z., Fedoseev, G., Kendall, A., Shotton, J., Corrado, G.: Gaia-1: A generative world model for autonomous driving. arXiv preprint arXiv:2309.17080 (2023)

13. Hu, Y., Yang, J., Chen, L., Li, K., Sima, C., Zhu, X., Chai, S., Du, S., Lin, T., Wang, W., et al.: Planning-oriented autonomous driving. In: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. pp. 17853– 17862 (2023)

14. Huang, X., Li, Z., He, G., Zhou, M., Shechtman, E.: Self forcing: Bridging the train-test gap in autoregressive video difusion. arXiv preprint arXiv:2506.08009 (2025)

15. Jia, X., Yang, Z., Li, Q., Zhang, Z., Yan, J.: Bench2drive: Towards multi-ability benchmarking of closed-loop end-to-end autonomous driving. Advances in Neural Information Processing Systems 37, 819–844 (2024)

16. Jiang, B., Chen, S., Xu, Q., Liao, B., Chen, J., Zhou, H., Zhang, Q., Liu, W., Huang, C., Wang, X.: Vad: Vectorized scene representation for eficient autonomous driving. In: Proceedings of the IEEE/CVF International Conference on Computer Vision. pp. 8340–8350 (2023)

17. Li, B., Guo, J., Liu, H., Zou, Y., Ding, Y., Chen, X., Zhu, H., Tan, F., Zhang, C., Wang, T., et al.: Uniscene: Unified occupancy-centric driving scene generation. arXiv preprint arXiv:2412.05435 (2024)

18. Li, Q., Peng, Z., Feng, L., Zhang, Q., Xue, Z., Zhou, B.: Metadrive: Composing diverse driving scenarios for generalizable reinforcement learning. IEEE transactions on pattern analysis and machine intelligence 45(3), 3461–3475 (2022)

19. Li, Y., Xiong, K., Guo, X., Li, F., Yan, S., Xu, G., Zhou, L., Chen, L., Sun, H., Wang, B., et al.: Recogdrive: A reinforced cognitive framework for end-to-end autonomous driving. arXiv preprint arXiv:2506.08052 (2025)

20. Liang, A., Kong, L., Yan, T., Liu, H., Yang, W., Huang, Z., Yin, W., Zuo, J., Hu, Y., Zhu, D., et al.: Worldlens: Full-spectrum evaluations of driving world models in real world. arXiv preprint arXiv:2512.10958 (2025)

21. Liang, T., Xie, H., Yu, K., Xia, Z., Lin, Z., Wang, Y., Tang, T., Wang, B., Tang, Z.: Bevfusion: A simple and robust lidar-camera fusion framework. Advances in Neural Information Processing Systems 35, 10421–10434 (2022)

22. Liao, B., Chen, S., Yin, H., Jiang, B., Wang, C., Yan, S., Zhang, X., Li, X., Zhang, Y., Zhang, Q., et al.: Difusiondrive: Truncated difusion model for end-to-end autonomous driving. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 12037–12047 (2025)

23. Lipman, Y., Chen, R.T., Ben-Hamu, H., Nickel, M., Le, M.: Flow matching for generative modeling. arXiv preprint arXiv:2210.02747 (2022)

24. Mousakhan, A., Mittal, S., Galesso, S., Farid, K., Brox, T.: Orbis: Overcoming challenges of long-horizon prediction in driving world models. arXiv preprint arXiv:2507.13162 (2025)

25. Peebles, W., Xie, S.: Scalable difusion models with transformers. In: Proceedings o the IEEE/CVF international conference on computer vision. pp. 4195–4205 (2023)

26. Shang, S., Chen, Y., Wang, Y., Li, Y., Zhang, Z.: Drivedpo: Policy learning via safety dpo for end-to-end autonomous driving. arXiv preprint arXiv:2509.17940 (2025)

27. Song, Y., Dhariwal, P., Chen, M., Sutskever, I.: Consistency models (2023)

28. Tian, H., Li, T., Liu, H., Yang, J., Qiu, Y., Li, G., Wang, J., Gao, Y., Zhang, Z., Wang, L., et al.: Simscale: Learning to drive via real-world simulation at scale. arXiv preprint arXiv:2511.23369 (2025)

29. Wan, T., Wang, A., Ai, B., Wen, B., Mao, C., Xie, C.W., Chen, D., Yu, F., Zhao, H., Yang, J., et al.: Wan: Open and advanced large-scale video generative models. arXiv preprint arXiv:2503.20314 (2025)

30. Wang, X., Zhu, Z., Huang, G., Chen, X., Zhu, J., Lu, J.: Drivedreamer: Towards real-world-drive world models for autonomous driving. In: European Conference on Computer Vision. pp. 55–72. Springer (2024)

31. Wang, Y., He, J., Fan, L., Li, H., Chen, Y., Zhang, Z.: Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 14749–14759 (2024)

32. Wen, Y., Zhao, Y., Liu, Y., Jia, F., Wang, Y., Luo, C., Zhang, C., Wang, T., Sun, X., Zhang, X.: Panacea: Panoramic and controllable video generation for autonomous driving. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 6902–6912 (2024)

33. Yan, T., Tang, T., Gui, X., Li, Y., Zhesng, J., Huang, W., Kong, L., Han, W., Zhou, X., Zhang, X., et al.: Ad-r1: Closed-loop reinforcement learning for end-to-end autonomous driving with impartial world models. arXiv preprint arXiv:2511.20325 (2025)

34. Yan, T., Wu, D., Han, W., Jiang, J., Zhou, X., Zhan, K., Xu, C.z., Shen, J.: Drivingsphere: Building a high-fidelity 4d world for closed-loop simulation. arXiv preprint arXiv:2411.11252 (2024)

35. Yan, T., Yin, J., Lang, X., Yang, R., Xu, C.Z., Shen, J.: Olidm: Object-aware lidar difusion models for autonomous driving. In: Proceedings of the AAAI Conference on Artificial Intelligence. vol. 39, pp. 9121–9129 (2025)

36. Yang, J., Chitta, K., Gao, S., Chen, L., Shao, Y., Jia, X., Li, H., Geiger, A., Yue, X., Chen, L.: Resim: Reliable world simulation for autonomous driving. arXiv preprint arXiv:2506.09981 (2025)

37. Yang, J., Gao, S., Qiu, Y., Chen, L., Li, T., Dai, B., Chitta, K., Wu, P., Zeng, J., Luo, P., et al.: Generalized predictive model for autonomous driving. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 14662–14672 (2024)

38. Yang, X., Wen, L., Ma, Y., Mei, J., Li, X., Wei, T., Lei, W., Fu, D., Cai, P., Dou, M., et al.: Drivearena: A closed-loop generative simulation platform for autonomous driving. arXiv preprint arXiv:2408.00415 (2024)

39. Yin, T., Gharbi, M., Zhang, R., Shechtman, E., Durand, F., Freeman, W.T., Park, T.: One-step difusion with distribution matching distillation. In: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. pp. 6613– 6623 (2024)

40. Zhao, G., Wang, X., Zhu, Z., Chen, X., Huang, G., Bao, X., Wang, X.: Drivedreamer-2: Llm-enhanced world models for diverse driving video generation. In: Proceedings of the AAAI Conference on Artificial Intelligence. vol. 39, pp. 10412–10420 (2025)

41. Zhu, H., Zhao, M., He, G., Su, H., Li, C., Zhu, J.: Causal forcing: Autoregressive difusion distillation done right for high-quality real-time interactive video generation. arXiv preprint arXiv:2602.02214 (2026)