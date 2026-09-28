# CoT4AD: A Vision-Language-Action Model with Explicit Chain-of-Thought Reasoning for Autonomous Driving

Zhaohui Wang Tengbo Yu Hao Tang<sup>∗</sup>

Peking University

corresponding author: bjdxtanghao@gmail.com

## Abstract

Vision-Language-Action (VLA) models have recently attracted growing attention in end-to-end autonomous driving for their strong reasoning capabilities and rich world knowledge. However, existing VLAs often suffer from limited numerical reasoning ability and overly simplified input–output mappings, which hinder their performance in complex driving scenarios requiring step-by-step causal reasoning. To address these challenges, we propose CoT4AD, a novel VLA framework that introduces Chainof-Thought (CoT) reasoning for autonomous driving to enhance both numerical and causal reasoning in Vision-Language Models (VLMs). CoT4AD integrates visual observations and language instructions to perform semantic reasoning, scene understanding, and trajectory planning. During training, it explicitly models a perception–question–prediction–action CoT to align the reasoning space with the action space across multiple driving tasks. During inference, it performs implicit CoT reasoning to enable consistent numerical reasoning and robust decision-making in dynamic environments. Extensive experiments on both real-world and simulated benchmarks, including nuScenes and Bench2Drive, demonstrate that CoT4AD achieves state-of-the-art performance in both open-loop and closed-loop evaluations. Code will be released upon paper acceptance.

## 1. Introduction

Autonomous driving, as a core research direction in artificial intelligence and robotics, has attracted widespread attention in recent years. It not only holds the potential to improve traffic safety and travel efficiency but also plays a key role in the development of smart cities and intelligent transportation systems [33, 56]. Traditional autonomous driving systems typically adopt a modular pipeline architecture, decomposing perception [37, 48], prediction [7, 51] and planning [42] into separate modules. However, such methods often suffer from error accumulation, difficulties in crossmodule optimization, and limited generalization ability in practical applications, which constrain the performance of autonomous driving systems in complex environments [23].

To address these challenges, end-to-end autonomous driving paradigms have been proposed. These methods aim to leverage a unified learning framework to directly predict driving control signals or plan trajectories from raw sensor inputs, thereby avoiding the uncertainties introduced by multi-stage information propagation [9]. Meanwhile, with the rapid development of large-scale Vision-Language Models (VLMs), researchers have begun to explore the potential of Vision-Language-Action (VLA) models [34, 67] for end-to-end autonomous driving. VLA models are capable of handling multi-modal inputs and performing semantic reasoning through language instructions, demonstrating stronger interpretability and generalization capabilities compared with traditional end-to-end approaches [41, 65].

Through imitation learning on diverse datasets, VLAs inherit the strong ability of VLMs to understand heterogeneous scenes, objects, and language, enabling robust crosstask generalization. However, they also share VLMs’ weaknesses—particularly poor numerical reasoning in complex environments [17, 64]. Thus, applying VLMs to autonomous driving faces two key challenges: (1) limited numerical reasoning causes unreliable or hallucinatory predictions and (2) existing methods treat LLMs as monolithic mappers from perception to numerical outputs, neglecting their capability for multi-step reasoning.

Chain-of-Thought (CoT) reasoning enhances LLM reasoning by decomposing complex tasks into intermediate steps [20, 58]. While prior works introduce CoT via language descriptions, keypoints, or bounding boxes [15, 43], they mainly focus on embodied or robotic settings with constrained environments [44, 62]. However, autonomous driving presents fundamentally different challenges—it demands accurate numerical reasoning, long-horizon planning, and robust generalization in dynamic, large-scale and safety-critical environments. As shown in Figure 1(b), directly feeding all prompts into a VLM leads to unstable outputs, whereas incorporating CoT enables structured intermediate reasoning and more reliable results. This work try to address a key question: How can CoT reasoning be tailored for autonomous driving to enhance efficiency and performance?

![](images/88372d0e9365f6df43f83c722e2f7b505ba416928536b9dd71346a1c6137ba90.jpg)  
(a) Comparison with existing frameworks.  
(b) Comparison between vanilla prompting and CoTprompting.  
Figure 1. Comparison with existing frameworks. (a) Classic E2E methods map sensor inputs to control outputs with modular designs. (b) Classic VLA methods incorporate language reasoning and VLMs to map sensor inputs to action space for planning. (c) CoT4AD (Outs) incorporate CoT reasoning for VLMs to enable explicit mult-step reasoning of planning.

To this end, we propose CoT4AD, a novel VLA model that integrates CoT reasoning for end-to-end autonomous driving. As illustrated in Figure 1, CoT4AD differs from previous methods by finetuning open-source pretrained language models through a series of downstream tasks tailored for autonomous driving scenarios, while being able to explicitly or implicitly perform CoT reasoning. This enables the model to generate reliable and stable trajectories from multi-modal inputs.

Our unified framework integrates environmental perception, language reasoning, future prediction, and trajectory planning, enabling the model to produce explicit CoT reasoning steps. In perception reasoning, the model is trained on perception tasks using expert data to acquire scene understanding capabilities. In future prediction, the model learns to predict future scenes from expert data, enabling the reconstruction of these scenes. In VQA reasoning, the model is fine-tuned on Visual Question Answering (VQA) tasks using prompt-based supervision. In trajectory planning, the model performs imitation learning to generate high-quality driving trajectories. Through a multi-stage training process, CoT4AD develops CoT reasoning capabilities tailored to autonomous driving scenarios. During inference, CoT4AD can directly produce driving trajectories in a single forward pass without explicitly generating intermediate reasoning steps, achieving a balance between planning performance and computational efficiency.

We extensively evaluate CoT4AD using real-world dataset nuScenes [6] and simulation dataset Bench2Drive [28]. Experimental results demonstrate that CoT4AD achieves superior performance across various end-to-end autonomous driving benchmarks under both open-loop and closed-loop tests.

The main contributions are summarized as follows:

(1) We introduce CoT4AD, an end-to-end autonomous driving framework leveraging a pretrained VLM with multi-step finetunes, enabling CoT reasoning and multtask capabilities from raw visual observations and language instructions.

(2) We introduce an innovative approach to future prediction and trajectory planning for driving scenes. This diffusion-based framework integrates existing video generation and planning approaches and is seamlessly integrated CoT reasoning pipelines.

(3) Extensive experiments on NuScenes and Bench2Drive datasets show that CoT4AD establishes new state-ofthe-art results in both open-loop and closed-loop driving, consistently outperforming prior LLM-based and end-to-end autonomous driving approaches.

## 2. Related Work

## 2.1. End-to-End Autonomous Driving (E2E-AD)

E2E-AD directly predicts driving trajectories from raw sensor data without decomposing the pipeline into perception, prediction, and planning. Early works such as ALVINN [47] and PilotNet [4] pioneered this idea but suffered from poor generalization and interpretability in complex scenes. With large-scale datasets [6, 53] and advanced architectures [55], methods such as CIL [11], TransFuser [10], and LAV [8] improve behavioral control and robustness through multimodal fusion and spatial–temporal reasoning. Recent trajectory-based approaches [23, 31] jointly optimize perception, prediction, and planning for better safety and interpretability. Meanwhile, VLM-driven systems such as DriveGPT [24] and Talk2Drive [12] enable reasoning and explainability via natural language, and diffusion-based models [30, 39] capture trajectory uncertainty. Despite these advances, E2E-AD still struggles with robustness and interpretability in real-world scenarios.

## 2.2. Vision Language Models (VLMs)

VLMs aim to jointly model images and natural language, achieving a semantic understanding of images and text through cross-modal alignment learning. Early works such as VisualBERT [36] and ViLT [35] extended the BERT architecture to vision-language tasks, enabling unified modeling for image-text matching and visual question answering (VQA) through large-scale joint pretraining on paired image-text datasets. With the rise of Multimodal Large Language Models (MLLMs), VLMs have gradually acquired strong reasoning, comprehension, and generative capabilities. Models like Flamingo [2] and LLaVA [40] further integrate large language models (LLMs) with visual encoders, allowing for contextual understanding of complex scenes and supporting open visual question answering, caption generation, and reasoning tasks. Recently, generalpurpose VLMs such as GPT-4V [1]and Qwen-VL [3] have demonstrated remarkable cross-task generalization, effectively solving diverse vision-language understanding and reasoning tasks without task-specific fine-tuning.

## 2.3. Chain-of-Thought (CoT) Reasoning

CoT reasoning has recently emerged as a powerful paradigm for enhancing the reasoning capabilities of LLMs. Its core idea is to make the model explicitly generate intermediate reasoning steps before producing the final answer, thereby decomposing complex problems into a series of interpretable intermediate processes [58]. CoT reasoning has been proven effective in improving models’ numerical and logical reasoning abilities. In robotic domains, introducing CoT reasoning offers a new perspective for decisionmaking. CoT-VLA [62] predicts subgoal images as intermediate reasoning step and then generates action tokens to accomplish manipulation tasks. ECoT [60] increases the absolute success rate of OpenVLA [34] by performing multiple reasoning steps before task execution. Although CoT reasoning has shown great potential in robotic applications, its integration into VLAs for autonomous driving remains in the early stages of exploration.

## 3. The Proposed Method

## 3.1. 3D Environmental Perception

In existing VLAs, visual features are typically extracted using 2D encoders [34, 67], which perform well in planar tasks [45] but struggle to model 3D structures and spatial relationships. Due to the lack of multi-view depth and geometric consistency, these models are unbale to accurately perceive 3D environments. To address this limitation, CoT4AD employs feature-centric perception training, learning from multiple 3D perception tasks to generate 3D visual tokens.

As shown in Figure 2 (a), CoT4AD takes multi-view images $I = \{ I ^ { i } \} _ { i = 1 } ^ { N }$ as input. A 2D backbone extracts multiscale features $f _ { 2 D } ,$ , which are projected into BEV space using camera parameters to obtain BEV features f<sub>BEV</sub>. The PB-SSM framework is used for efficient multi-view fusion. Two visual modules then encode structured 3D semantics: MapTokenizer $T _ { m a p }$ for static elements (lanes, drivable areas) and ObjectTokenizer $T _ { o b j }$ for dynamic objects (vehicles, pedestrians). $T _ { m a p }$ produces map tokens $v _ { m a p }$ from BEV patches, while $T _ { o b j }$ applies ROI Align [21] on $f _ { B E V }$ to yield object tokens $v _ { o b j }$ To complement limited annotation-based learning, we further introduce BEVTokenizer, which directly partitions BEV features into $N _ { b e v } \times N _ { b e v }$ patches to generate comprehensive BEV tokens $v _ { b e v }$ . The final environmental representation is $\mathbf { V } _ { e n v } = \{ v _ { m a p } , v _ { o b j } , v _ { b e v } \}$ , serving as the perception stage for CoT reasoning.

## 3.2. Vision-Language Prompt Tuning

In existing VLAs, vision-language tuning is often limited to the adjustment of image tokens and language tokens [34], lacking joint optimization of perception tokens and other multi-modal representations. To address the limited environment representation capacity of multi-feature tokens extracted by perception models and the discretized embeddings of natural language, we introduce a VQA-based multi-modal vision-language finetuning framework.

During the fine-tuning stage, the model learns high-level perception capabilities and driving knowledge from VQA datasets, enabling the transfer from multi-modal tokens to numerical reasoning space. Inspired by soft prompt tuning [46], we introduce stage-irrelevant tokens denoted as $\mathbf { V } _ { s }$ These learnable and discretized tokens are used to encode visual details during training and serve as input across different stages of CoT reasoning. The effectiveness of soft prompt tuning has been demonstrated in various Transformer-based tasks, including image classification and numerical reasoning [5, 13]. Our experiments will show that this method is also effective for end-to-end autonomous driving tasks to improve the integration of multi-modal perception and language reasoning.

![](images/ff445d4d457e331c26c9afb7a8952e3bb64c6cbab661a62cbd77bee827a36bb8.jpg)  
Figure 2. (a) Architecture of CoT4AD. It consists of four stages of CoT reasoning including: 3D perception, VQA, VLM-conditioned diffusion and planning. (b) VLM-Conditioned Latent Diffusion. A conditional latent DiT model diffuses the latent of the current frame conditioned on VLM embeddings, and the future frame is reconstructed via a VAE decoder.

As illustrated in Figure 2 (b), we fomulate the VQA datasets as prompt-response pairs $\{ { \bf X } _ { i n p u t } , { \bf X } _ { a n s w e r } \}$ where ${ { \bf { X } } _ { i n p u t } } = { \{ { \bf { V } } _ { e n v } , { \bf { V } } _ { s } , { \bf { V } } _ { e g o } \} } , { \bf { V } } _ { e g o }$ encodes the ego vehicle state such as velociy, acceleration and yaw. During instruction tuning, visual tokenizers are frozen while the LLM is set trainable. The Vision-language prompt tuning state is as:

$$
\begin{array} { r } { \hat { \mathbf { X } } _ { a n s w e r } = \mathrm { L L M } \left( { \mathbf { V } } _ { e n v } , { \mathbf { V } } _ { s } , { \mathbf { V } } _ { e g o } \right) . } \end{array}\tag{1}
$$

## 3.3. VLM-Conditioned Latent Diffusion

Existing VLA systems are often constrained by text-level reasoning, overlooking the rich multimodal characteristics of the real world. Inspired by world models in autonomous driving, which learn physical laws by generating future frames, we leverage a VLM-conditioned diffusion model to generate high-fidelity future frames, enabling a deeper understanding of the world’s rich semantic information. As illustrated in the Figure 2 (b), our proposed VLMconditioned diffusion model operates as follows:

Following Latent diffusion models(LDMs) [50], we train an encoder E to compresses images $I _ { f }$ into smaller spatial representations $z _ { 0 } = E ( I _ { f } )$ and an decoder D to restore future frame $I _ { f } = D ( z _ { 0 } )$ . By performing diffusion modeling in the latent space, we avoid direct diffusion in the high-dimensional pixel space, thereby significantly accelerating the training process of the diffusion model. The LDM poses a forward process as gradually adding noise to the latent space, which can be defined as:

$$
q \left( z _ { t } \mid z _ { 0 } \right) = N \left( z _ { t } ; \sqrt { \bar { \alpha _ { t } } } z _ { 0 } , \left( 1 - \bar { \alpha _ { t } } \right) \mathbf { I } \right) ,\tag{2}
$$

where $z _ { \mathrm { 0 } }$ is the clean latent variable, and $z _ { t }$ is the noise frame at time t. The constants $\alpha _ { t }$ are hyperparameters. For the reverse process, we train a diffusion transformer $f _ { \theta }$ to reconstruct $z _ { \mathrm { 0 } }$ from the noise frame $z _ { t }$ and the conditional embedding c, where $c = \operatorname { L L M } { ( \mathbf { V } _ { e n v } , \mathbf { V } _ { s } , \mathbf { V } _ { e g o } ) }$ . Instead of sampling noise from a Gaussian distribution, we formulate the noise frame $z _ { t }$ from the current frame $I _ { c } \mathbf { \cdot }$

$$
z _ { i } = \sqrt { \bar { \alpha _ { i } } } D ( I _ { c } ) + \sqrt { 1 - \bar { \alpha } _ { i } } \epsilon , \quad \epsilon \sim \mathcal { N } ( 0 , \mathbf { I } ) ,\tag{3}
$$

where $i \in [ 1 , T ]$ . During training, the diffusion transformer $f _ { \theta }$ takes noise frame $z _ { t }$ and conditional embedding c as input to predict denoised latent variable $\hat { z } _ { 0 } = f _ { \theta } ( z _ { 0 } , c )$ . The training objective combines latent variable reconstruction and noise prediction losses:

$$
\mathcal { L } = \lambda \| z _ { 0 } - \hat { z } _ { 0 } \| _ { 2 } ^ { 2 } + \lambda _ { \epsilon } \| \epsilon - \hat { \epsilon } _ { \theta } ( z _ { t } , c ) \| _ { 2 } ^ { 2 } .\tag{4}
$$

During inference, we adopt a truncated denoising process starting from a noisy latent representation $z _ { t }$ sampled from the current frame-based Gaussian distribution and progressively denoise it conditioned on the conditional embedding c from VLM to obtain the final predicted image $\hat { z } _ { 0 }$ At each denoising step, the DDIM update rule is applied to iteratively refine the latent state toward the next time step. Decoder D is applied to decode $z _ { \mathrm { 0 } }$ to predicted future frame $\hat { I } _ { f } = D ( z _ { 0 } )$

Through this latent space VLM-conditioned diffusion generation approach, VLA model can learn future scene prediction, thereby developing a form of visual reasoning about scene changes and enhancing the understanding of environmental semantics and physical laws, rather than relying solely on text or single-frame information.

## 3.4. Chain-of-Thought Trajectory Planning

At this stage, CoT4AD performs CoT-based planning of future driving actions, represented by a sequence of waypoints $\mathbf { V } _ { e g o } ~ = ~ \{ w _ { 1 } , w _ { 2 } , . . . , w _ { T } \}$ . We adopt VLM-conditioned diffusion planning in Sec. 3.3. We follow vanilla diffusion models without latent space as illustrated in Figure 2 (b). We initialize the sampling noise from action anchors $a = \{ a _ { k } \} _ { k = 1 } ^ { N }$ which is clustered by K-Means on the dataset. The diffusion transformer $f _ { a }$ takes noisy actions z<sup>a</sup>and conditional embedding $c _ { a } = \mathrm { L L M } ( \mathbf { V } _ { e n v } , \mathbf { V } _ { f u t } , \mathbf { V } _ { s } , \mathbf { V } _ { e g o } )$ to predict denoised trajectories ${ \hat { z } } ^ { a }$ and classification scores ${ \hat { s } } ^ { a }$ as:

$$
\{ \hat { s } ^ { a } , \hat { z } ^ { a } \} = f _ { a } ( z _ { t } , c _ { a } , t ) ,\tag{5}
$$

where $c _ { a }$ represents the conditional embedding and t represents the timestamp. The whole model, including the visual encoder, visual diffusion transformer, planning diffusion transformer and the LLM is jointly optimized during training. To accelerate the forward process during inference, instead of explicitly generating intermediate steps and images, it directly produces $c _ { a }$ from environment tokens and prompts as conditional embeddings. At each denoising step, the diffusion transformer takes the predicted trajectory from the previous step as input and update predictions with DDIM for the next timestep.

## 4. Experiments

In this section, we first introduce two widely used datasets: nuScenes dataset [6] and Bench2Drive dataset [28]. Then we evaluate our method on both datasets and compare with state-of-the-art VLA models. Furthermore, the effectiveness of our methods is explained by visual analysis. Finally, ablation studies are conducted on the Bench2Drive dataset [28] to verify the effectiveness of each module.

## 4.1. Datasets

NuScenes. NuScenes is a widely used multimodal benchmark for perception and open-loop planning in autonomous driving, containing 1,000 20-second scenes collected in Boston and Singapore, annotated at 2 Hz (700/150/150 for train/val/test). Building on this, nuScenes-QA [49] extends it into a VQA benchmark by generating scene graphs and diverse question types (e.g., existence, counting, attribute, comparison), challenging models in multimodal reasoning.

Bench2Drive. Bench2Drive is a benchmark used for closed-loop E2E-AD, proposed by the Thinklab-SJTU team. It uses the CARLA V2 [14] simulation environment to comprehensively evaluate autonomous driving systems under interactive and dynamic scenarios. For a fair baseline comparison, Bench2Drive defines a base set of 1000 clips, typically split into 950 for training and 50 for openloop validation. Each clip corresponds to a continuous driving segment (roughly 150 meters) in a specific traffic scene. Chat-B2D is a VQA extension built on top of Bench2Drive, introduced in ORION [18]. It provides automatically generated question-answer pairs for each driving scene in the Bench2Drive dataset, enabling semantic reasoning evaluation within closed-loop simulation.

## 4.2. Evaluation Metrics

We conduct open-loop evaluations on the nuScenes dataset using L2 distance error and average collision rate as evaluation metrics. We conduct both open-loop and closed-loop evaluations on Bench2Drive dataset with metrics including Driving Score (DS), Success Rate (SR), Efficiency, Comfortness, and Multi-Ability.

## 4.3. Implementation Details

In experiments, we implemented our method using the Py-Torch deep learning framework on 8 NVIDIA RTX A800 GPUs with 80GB memory. The network was trained with a stochastic gradient descent (SGD) [19] optimizer, initialized with a learning rate of $1 e ^ { - 4 }$ , momentum of 0.9, and weight decay of $1 e ^ { - 4 }$ . For the backbone feature extraction, we adopted EVA-CLIP [16] with pretrained model. LLaMA-3 is employed in CoT4AD. The training diffusion schedule is truncated by 50/1000 to diffuse the latent images, while during inference, we use only 2 denoising steps for prediction. During training, data augmentations are applied to input images, which are first resized to a resolution of $6 4 0 \times 6 4 0$

Table 1. Results of E2E-AD methods on NuScenes. †: The ego status and planning trajectory are both processed by LLM in textua modality. ‡: The high-level command is not used during the training and testing phases.
<table><tr><td rowspan="2">Method</td><td rowspan="2">Reference</td><td rowspan="2">VLM-Based</td><td colspan="2">Ego Status</td><td colspan="4">L2 (m) ↓</td><td colspan="4">Collision (%) ↓</td></tr><tr><td>BEV</td><td>Planner</td><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td></tr><tr><td>ST-P3 [22]</td><td>ECCV’22</td><td></td><td></td><td></td><td>1.33</td><td>2.11</td><td>2.90</td><td>2.11</td><td>0.23</td><td>0.62</td><td>1.27</td><td>0.71</td></tr><tr><td>UniAD [23]</td><td>CVPR’23</td><td></td><td></td><td></td><td>0.48</td><td>0.96</td><td>1.65</td><td>1.03</td><td>0.05</td><td>0.17</td><td>0.71</td><td>0.31</td></tr><tr><td>UniAD [23]</td><td>CVPR’23</td><td></td><td>√</td><td>√</td><td>0.20</td><td>0.42</td><td>0.75</td><td>0.46</td><td>0.02</td><td>0.25</td><td>0.84</td><td>0.37</td></tr><tr><td>VAD-Base [31]</td><td>CVPR’23</td><td></td><td>-</td><td>-</td><td>0.69</td><td>1.22</td><td>1.83</td><td>1.25</td><td>0.06</td><td>0.68</td><td>2.52</td><td>1.09</td></tr><tr><td>VAD-Base [31]</td><td>CVPR&#x27;23</td><td></td><td>√</td><td>-</td><td>0.41</td><td>0.70</td><td>1.06</td><td>0.72</td><td>0.04</td><td>0.43</td><td>1.15</td><td>0.54</td></tr><tr><td>VAD-Base [31]</td><td>CVPR&#x27;23</td><td></td><td>√</td><td>√</td><td>0.17</td><td>0.34</td><td>0.60</td><td>0.37</td><td>0.04</td><td>0.27</td><td>0.67</td><td>0.33</td></tr><tr><td>Ego-MLP [61]</td><td>CVPR&#x27;24</td><td></td><td>-</td><td>√</td><td>0.15</td><td>0.32</td><td>0.59</td><td>0.35</td><td>0.00</td><td>0.27</td><td>0.85</td><td>0.37</td></tr><tr><td>BEV-Planner [38]</td><td>CVPR&#x27;24</td><td></td><td></td><td>-</td><td>0.30</td><td>0.52</td><td>0.83</td><td>0.55</td><td>0.10</td><td>0.37</td><td>1.30</td><td>0.59</td></tr><tr><td>BEV-Planner++ [38]</td><td>CVPR&#x27;24</td><td>=</td><td>√</td><td>√</td><td>0.16</td><td>0.32</td><td>0.57</td><td>0.35</td><td>0.00</td><td>0.29</td><td>0.73</td><td>0.34</td></tr><tr><td>DriveVLM† [54]</td><td>ECCV’24</td><td>√</td><td>-</td><td></td><td>0.18</td><td>0.34</td><td>0.68</td><td>0.40</td><td>0.10</td><td>0.22</td><td>0.45</td><td>0.27</td></tr><tr><td>DriveVLM-Dual [54]</td><td>ECCV’24</td><td>√</td><td>√</td><td></td><td>0.15</td><td>0.29</td><td>0.48</td><td>0.31</td><td>0.05</td><td>0.08</td><td>0.17</td><td>0.10</td></tr><tr><td>OmniDrive‡ [57]</td><td>CoRR&#x27;24</td><td>√</td><td></td><td></td><td>1.15</td><td>1.96</td><td>2.84</td><td>1.98</td><td>0.80</td><td>3.12</td><td>7.46</td><td>3.79</td></tr><tr><td>OmniDrive [57]</td><td>CoRR&#x27;24</td><td>√</td><td></td><td></td><td>0.40</td><td>0.80</td><td>1.32</td><td>0.84</td><td>0.04</td><td>0.46</td><td>2.32</td><td>0.94</td></tr><tr><td>OmniDrive++ [57]</td><td>CoRR&#x27;24</td><td>√</td><td>√</td><td>√</td><td>0.14</td><td>0.29</td><td>0.55</td><td>0.33</td><td>0.01</td><td>0.13</td><td>0.78</td><td>0.30</td></tr><tr><td>Senna [32]</td><td>arXiv&#x27;24</td><td>√</td><td>-</td><td></td><td>0.37</td><td>0.54</td><td>0.86</td><td>0.59</td><td>0.09</td><td>0.12</td><td>0.33</td><td>0.18</td></tr><tr><td>EMMA† [25]</td><td>arXiv&#x27;24</td><td>√</td><td>-</td><td></td><td>0.14</td><td>0.29</td><td>0.54</td><td>0.32</td><td></td><td></td><td></td><td></td></tr><tr><td>ORION [18]</td><td>ICCV’25</td><td>√</td><td>√</td><td></td><td>0.17</td><td>0.31</td><td>0.55</td><td>0.34</td><td>0.05</td><td>0.25</td><td>0.80</td><td>0.37</td></tr><tr><td>OpenDriveVLA [66]</td><td>arXiv&#x27;25</td><td>√</td><td>√</td><td></td><td>0.15</td><td>0.31</td><td>0.55</td><td>0.33</td><td>0.01</td><td>0.08</td><td>0.21</td><td>0.10</td></tr><tr><td>CoT4AD (Ours)</td><td></td><td>√</td><td>√</td><td></td><td>0.12</td><td>0.24</td><td>0.53</td><td>0.29</td><td>0.02</td><td>0.06</td><td>0.22</td><td>0.10</td></tr></table>

Table 2. Results of E2E-AD Methods on Bench2Drive under base set. C/L refers to camera/LiDAR. Avg. L2 is averaged over the predictions in 2 seconds under 2Hz, similar to UniAD. \* denote expert feature distillation. NC: navigation command, TP: target point, DS: Driving Score, SR: Success Rate.
<table><tr><td>Method</td><td>Reference</td><td>*Condition</td><td>Modality</td><td>DS↑</td><td>SR(%)↑</td><td>Efficiency↑</td><td>Comfortness↑</td></tr><tr><td>TCP* [59]</td><td>NeurIPS&#x27;22</td><td>TP</td><td>C</td><td>40.70</td><td>15.00</td><td>54.26</td><td>47.80</td></tr><tr><td>TCP-ctrl* [59]</td><td>NeurIPS&#x27;22</td><td>TP</td><td>C</td><td>30.47</td><td>7.27</td><td>55.97</td><td>51.51</td></tr><tr><td>TCP-traj* [59]</td><td>NeurIPS&#x27;22</td><td>TP</td><td>C</td><td>59.90</td><td>30.00</td><td>76.54</td><td>18.08</td></tr><tr><td>TCP-traj w/o distillation [59]</td><td>NeurIPS’22</td><td>TP</td><td>C</td><td>49.30</td><td>20.45</td><td>78.78</td><td>22.96</td></tr><tr><td>ThinkTwice* [27]</td><td>CVPR&#x27;23</td><td>TP</td><td>C</td><td>62.44</td><td>31.23</td><td>69.33</td><td>16.22</td></tr><tr><td>DriveAdapter* [26]</td><td>ICCV’23</td><td>TP</td><td>C&amp;L</td><td>64.22</td><td>33.08</td><td>70.22</td><td>16.01</td></tr><tr><td>AD-MLP [61]</td><td>arXiv&#x27;23</td><td>NC</td><td>C</td><td>18.05</td><td>0.00</td><td>48.45</td><td>22.63</td></tr><tr><td>UniAD-Tiny [23]</td><td>CVPR&#x27;23</td><td>NC</td><td>C</td><td>40.73</td><td>13.18</td><td>123.92</td><td>47.04</td></tr><tr><td>UniAD-Base [23]</td><td>CVPR&#x27;23</td><td>NC</td><td>C</td><td>45.81</td><td>16.36</td><td>129.21</td><td>43.58</td></tr><tr><td>VAD [31]</td><td>ICCV’23</td><td>NC</td><td>C</td><td>42.35</td><td>15.00</td><td>157.94</td><td>46.01</td></tr><tr><td>GenAD [63]</td><td>ECCV’24</td><td>NC</td><td>C</td><td>44.81</td><td>15.90</td><td></td><td></td></tr><tr><td>MomAD [52]</td><td>CVPR&#x27;25</td><td>NC</td><td>C</td><td>44.54</td><td>16.71</td><td>170.21</td><td>48.63</td></tr><tr><td>DriveTransformer-Large [29]</td><td>ICLR’25</td><td>NC</td><td>C</td><td>63.46</td><td>35.01</td><td>100.64</td><td>20.78</td></tr><tr><td>ORION [18]</td><td>ICCV’25</td><td>NC</td><td>C</td><td>77.74</td><td>54.62</td><td>151.48</td><td>17.38</td></tr><tr><td>Cot4AD (Ours)</td><td>–</td><td>NC</td><td>C</td><td>80.24</td><td>55.22</td><td>153.33</td><td>46.78</td></tr><tr><td>Cot4AD-CoT (Ours)</td><td></td><td>NC</td><td>C</td><td>81.22</td><td>55.78</td><td>149.28</td><td>47.40</td></tr></table>

## 4.4. Comparison with the State-of-Art Methods

NuScenes. Table 1 reports the performance of state-of-theart E2E-AD methods on the NuScenes dataset under UniAD metrics. CoT4AD achieves competitive results with L2 errors of 0.12 m, 0.24 m, and 0.53 m for 1s, 2s, and 3s horizons, respectively (avg. 0.29 m), clearly outperforming recent VLM-based counterparts such as OpenDriveVLA and EMMA. In terms of safety, CoT4AD maintains a notably low collision rate of 0.10%, demonstrating robust and reliable trajectory prediction. Unlike methods that incorporate planner trajectories, CoT4AD relies on ego BEV status and camera images as input, yet consistently achieves lower prediction errors and collision rates than OmniDrive++. This highlights the strong reasoning ability of the proposed chain-of-thought reasoning, which enhances the model’s capability to predict driving trajectories in complex scenes.

Bench2Drive. Table 2 presents the closed-loop results of various E2E-AD methods on the Bench2Drive benchmark. CoT4AD indicates that the model outputs the trajectories end-to-end, while CoT4AD-CoT denotes that the trajectories are produced through step-by-step CoT reasoning. Our proposed CoT4AD and CoT4AD-CoT models achieve the best overall performance. Specifically, CoT4AD-CoT achieves the highest Driving Score with 81.22 and Success Rate with 55.78%, surpassing strong baselines such as ORION and DriveTransformer-Large. In terms of Efficiency and Comfortness, our method achieves a balanced performance—demonstrating smoother and more humanlike control behavior compared with transformer-based approaches that tend to produce abrupt maneuvers. Notably, both versions of CoT4AD rely solely on camera inputs and navigation commands, yet outperform models that incorporate additional LiDAR or expert distillation signals. These results highlight the effectiveness of our chain-of-thought reasoning framework in enhancing decision consistency and improving driving reliability under diverse scenarios. For more detailed experiment results, please see in the Appendix.

![](images/572115047ea1dd7acc8a21a4c21fbcd075f2a9d573fff92c9f014f38013cd46e.jpg)  
Figure 3. Qualitative results of CoT4AD on the Bench2Drive closed-loop evaluation set.

## 4.5. Qualitative Results

To further demonstrate the planning capability of our approach in complex scenarios, we conduct a qualitative comparison between CoT4AD and UniAD. As shown in Figure 3, two representative driving scenes are selected, each containing three consecutive frames to illustrate the models’ decision-making processes. In Scene 1, the model is instructed to change lanes to avoid an obstacle ahead. Although both methods produce reasonable lane-change trajectories, CoT4AD generates a smoother and more continuous trajectory, maintaining a larger safety margin from the obstacle in frame 3. In Scene 2, the model is instructed to perform an overtaking maneuver. UniAD fails to anticipate the overtaking intent early enough, resulting in insufficient acceleration and limited overtaking distance, which prevents it from completing the maneuver safely. In contrast, CoT4AD is capable of recognizing the intent earlier and planning proactively, maintaining a closer following distance while accelerating and changing lanes smoothly to complete the overtaking successfully. This demonstrates that CoT4AD possesses stronger temporal reasoning and high-level semantic understanding, enabling more humanlike and context-aware driving behaviors. Overall, these qualitative results highlight the advantages of the proposed Chain-of-Thought reasoning: it not only improves trajectory smoothness and safety but also enhances robustness and decision interpretability in complex traffic interactions. For additional qualitative visualizations and videos, please refer to the Appendix.

Table 3. Ablation results of tokenizer on Bench2Drive. DS and SR denote Driving Score and Success Rate.
<table><tr><td rowspan="2">ID</td><td rowspan="2"> $T _ { m a p }$ </td><td rowspan="2"> $T _ { o b j }$ </td><td rowspan="2"> $T _ { b e v }$ </td><td colspan="2">Closed-loop</td></tr><tr><td>DS↑</td><td>SR (%) ↑</td></tr><tr><td>1</td><td>√</td><td>X</td><td>X</td><td>44.21</td><td>20.12</td></tr><tr><td>2</td><td>X</td><td>√</td><td>X</td><td>56.28</td><td>38.02</td></tr><tr><td>3</td><td>√</td><td>√</td><td>X</td><td>79.77</td><td>50.88</td></tr><tr><td>4</td><td>X</td><td>X</td><td>√</td><td>69.92</td><td>39.64</td></tr><tr><td>5</td><td></td><td>J</td><td>J</td><td>80.24</td><td>55.22</td></tr></table>

## 4.6. Ablation Studies

Effectiveness of Perception Tokenizers. Table 3 shows the detailed ablations of each tokenizer. We observe that using Tokenizer based on perception labels (ID 1 and ID 2) achieves relatively strong performance. For example, using only $T _ { m a p }$ or $T _ { o b j }$ already significantly improves the success rate (SR), indicating that perception labels provide valuable guidance for planning. Tokenizer based directly on visual features (ID 3 vs. ID 4) also achieves good performance but is less effective than the perception-based tokenizer (50.88 vs. 39.64). Combining both perception and visual features further enhances performance, achieving the best closed-loop metrics. This indicates that although limited perception labels can provide certain environmental information, image features retain more complete semantic information, and combining both can enhance the model’s overall performance.

![](images/0ffac6939f08e08717478f326be4314fe584c4ff5bc935415b7469e73150f195.jpg)  
Figure 4. Ablation on the number of predicted future scenes

Effectiveness of CoT Designs. Table 4 shows the detailed ablations of each step in the introduced CoT pretraing. Removing basic perception (ID 1 vs. ID 2) leads to a significant drop in both DS (66.44 vs. 59.89) and SR (36.86 vs. 27.95), indicating that visual perception features are essential for safe and successful driving. Similarly, removing the VQA module (ID 1 vs. ID 3) reduces a smaller DS (64.38 vs. 59.89) and SR (33.22 vs. 27.95), showing that reasoning about visual questions provides useful contextual information for driving decision-making. However, the future diffusion has a greatest impact on performance. With only the future module enabled (ID 4), both DS and SR increase substantially (DS: 72.38, SR: 45.22), highlighting the importance of anticipating future states in closed-loop control. This phenomenon may be due to the fact that, compared with limited annotated labels, the model learns richer perception representations from future predictions through self-supervised learning. As a result, combining all components (ID 5) achieves the best performance (DS: 80.24, SR: 55.22), demonstrating that perception, VQA reasoning, and future prediction complement each other to enhance driving performance.

Table 4. Ablation results of CoT pre-training. DS and SR denote Driving Score and Success Rate.
<table><tr><td rowspan="2">ID</td><td rowspan="2">Perception</td><td rowspan="2">VQA</td><td rowspan="2">Future</td><td colspan="2">Closed-loop</td></tr><tr><td>DS↑</td><td>SR (%) ↑</td></tr><tr><td>1</td><td>X</td><td>X</td><td>X</td><td>59.89</td><td>27.95</td></tr><tr><td>2</td><td>√</td><td>X</td><td>X</td><td>66.44</td><td>36.86</td></tr><tr><td>3</td><td>X</td><td>√</td><td>X</td><td>64.38</td><td>33.22</td></tr><tr><td>4</td><td>X</td><td>X</td><td>√</td><td>72.38</td><td>45.22</td></tr><tr><td>5</td><td>√</td><td>J</td><td>L</td><td>80.24</td><td>55.22</td></tr></table>

Effectiveness of Future Scenes Prediction. Figure 4 presents a detailed ablation study on the impact of the number of predicted future scenes used in the model. As the number of future scenes increases from 0 to 8, the model’s performance improves, reaching a peak with 4 predicted future scenes, achieving a SR of 55.78%. However, when the number of predicted future scenes exceeds this optimal threshold, the model’s performance begins to degrade. This decline is attributed to the excessive inclusion of future information, which results in overloading the model and introducing confusion, thereby diminishing the SR. These results highlight the importance of balancing the incorporation of future scene predictions.

## 5. Conclusion and Future Work

In this paper, we propose CoT4AD, a model that performs explicit chain-of-thought reasoning in autonomous driving scenarios. By adopting a multi-step reasoning process consisting of perception–VQA–diffusion–planning, the model achieves better alignment across the visual, reasoning, and action spaces, enabling smoother and more accurate planning in driving tasks. Experiments conducted on two datasets demonstrate that CoT4AD outperforms existing state-of-the-art methods, validating the effectiveness of our proposed approach. Although CoT4AD performs well under explicit reasoning, it is constrained by the computational complexity of multi-step CoT reasoning and the training instability of diffusion models. In future work, we plan to explore more efficient CoT reasoning mechanisms to enable real-time autonomous driving.

## References

[1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. arXiv preprint arXiv:2303.08774, 2023. 3

[2] Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katherine Millican, Malcolm Reynolds, et al. Flamingo: a visual language model for few-shot learning. Advances in neural information processing systems, 35:23716–23736, 2022. 3

[3] J Bai, S Bai, S Yang, S Wang, S Tan, P Wang, J Lin, C Zhou, and J Qwen-VL Zhou. A versatile vision-language model for understanding, localization, text reading, and beyond. arXiv preprint arXiv:2308.12966, 6, 2023. 3

[4] Mariusz Bojarski, Davide Del Testa, Daniel Dworakowski, Bernhard Firner, Beat Flepp, Prasoon Goyal, Lawrence D Jackel, Mathew Monfort, Urs Muller, Jiakai Zhang, et al. End to end learning for self-driving cars. arXiv preprint arXiv:1604.07316, 2016. 2

[5] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. arXiv preprint arXiv:2505.06111, 2025. 3

[6] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multimodal dataset for autonomous driving. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 11621–11631, 2020. 2, 5

[7] Loick Chambon, Eloi Zablocki, Mickael Chen, Florent Bar-¨ toccioni, Patrick Perez, and Matthieu Cord. Pointbev: A´ sparse approach for bev predictions. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 15195–15204, 2024. 1

[8] Dian Chen and Philipp Krahenb ¨ uhl. Learning from all vehi-¨ cles. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 17222–17231, 2022. 3

[9] Li Chen, Penghao Wu, Kashyap Chitta, Bernhard Jaeger, Andreas Geiger, and Hongyang Li. End-to-end autonomous driving: Challenges and frontiers. IEEE Transactions on Pattern Analysis and Machine Intelligence, 2024. 1

[10] Kashyap Chitta, Aditya Prakash, Bernhard Jaeger, Zehao Yu, Katrin Renz, and Andreas Geiger. Transfuser: Imitation with transformer-based sensor fusion for autonomous driving. IEEE transactions on pattern analysis and machine intelligence, 45(11):12878–12895, 2022. 3

[11] Felipe Codevilla, Matthias Muller, Antonio L¨ opez, Vladlen´ Koltun, and Alexey Dosovitskiy. End-to-end driving via conditional imitation learning. In 2018 IEEE international conference on robotics and automation (ICRA), pages 4693– 4700. IEEE, 2018. 3

[12] Can Cui, Zichong Yang, Yupeng Zhou, Yunsheng Ma, Juanwu Lu, and Ziran Wang. Large language models for

autonomous driving: Real-world experiments. CoRR, 2023. 3

[13] Timothee Darcet, Maxime Oquab, Julien Mairal, and Pi-´ otr Bojanowski. Vision transformers need registers. In International Conference on Learning Representations (ICLR) 2024. OpenReview, 2024. Also available as arXiv preprint arXiv:2309.16588. 3

[14] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. Carla: An open urban driving simulator. In Conference on robot learning, pages 1–16. PMLR, 2017. 5

[15] Yilun Du, Sherry Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Josh Tenenbaum, Dale Schuurmans, and Pieter Abbeel. Learning universal policies via text-guided video generation. Advances in neural information processing systems, 36:9156–9172, 2023. 1

[16] Yuxin Fang, Quan Sun, Xinggang Wang, Tiejun Huang, Xin long Wang, and Yue Cao. Eva-02: A visual representation for neon genesis. Image and Vision Computing, 149:105171, 2024. 5

[17] Simon Frieder, Luca Pinchetti, Ryan-Rhys Griffiths, Tommaso Salvatori, Thomas Lukasiewicz, Philipp Petersen, and Julius Berner. Mathematical capabilities of chatgpt. Advances in neural information processing systems, 36:27699– 27744, 2023. 1

[18] Haoyu Fu, Diankun Zhang, Zongchuang Zhao, Jianfeng Cui, Dingkang Liang, Chong Zhang, Dingyuan Zhang, Hongwei Xie, Bing Wang, and Xiang Bai. Orion: A holistic end-toend autonomous driving framework by vision-language in structed action generation. arXiv preprint arXiv:2503.19755, 2025. 5, 6

[19] Robert Mansel Gower, Nicolas Loizou, Xun Qian, Alibek Sailanbayev, Egor Shulgin, and Peter Richtarik. Sgd: Gen-´ eral analysis and improved rates. In International conference on machine learning, pages 5200–5209. PMLR, 2019. 5

[20] Mingning Guo, Mengwei Wu, Yuxiang Shen, Haifeng Li, and Chao Tao. Ifship: Interpretable fine-grained ship classification with domain knowledge-enhanced vision-language models. Pattern Recognition, 166:111672, 2025. 1

[21] Kaiming He, Georgia Gkioxari, Piotr Dollar, and Ross Gir-´ shick. Mask r-cnn. In Proceedings ofthe IEEE International Conference on Computer Vision (ICCV), 2017. 3

[22] Shengchao Hu, Li Chen, Penghao Wu, Hongyang Li, Junch Yan, and Dacheng Tao. St-p3: End-to-end vision-based autonomous driving via spatial-temporal feature learning. In European Conference on Computer Vision, pages 533–549. Springer, 2022. 6

[23] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, et al. Planning-oriented autonomous driving. In Pro ceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 17853–17862, 2023. 1, 3, 6

[24] Xin Huang, Eric M Wolff, Paul Vernaza, Tung Phan-Minh, Hongge Chen, David S Hayden, Mark Edmonds, Brian Pierce, Xinxin Chen, Pratik Elias Jacob, et al. Drivegpt: Scaling autoregressive behavior models for driving. arXiv preprint arXiv:2412.14415, 2024. 3

[25] Jyh-Jing Hwang, Runsheng Xu, Hubert Lin, Wei-Chih Hung, Jingwei Ji, Kristy Choi, Di Huang, Tong He, Paul Covington, Benjamin Sapp, et al. Emma: End-to-end multimodal model for autonomous driving. arXiv preprint arXiv:2410.23262, 2024. 6

[26] Xiaosong Jia, Yulu Gao, Li Chen, Junchi Yan, Patrick Langechuan Liu, and Hongyang Li. Driveadapter: Breaking the coupling barrier of perception and planning in end-to-end autonomous driving. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 7953–7963, 2023. 6

[27] Xiaosong Jia, Penghao Wu, Li Chen, Jiangwei Xie, Conghui He, Junchi Yan, and Hongyang Li. Think twice before driving: Towards scalable decoders for end-to-end autonomous driving. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 21983–21994, 2023. 6

[28] Xiaosong Jia, Zhenjie Yang, Qifeng Li, Zhiyuan Zhang, and Junchi Yan. Bench2drive: Towards multi-ability benchmarking of closed-loop end-to-end autonomous driving. Advances in Neural Information Processing Systems, 37:819– 844, 2024. 2, 5

[29] Xiaosong Jia, Junqi You, Zhiyuan Zhang, and Junchi Yan. Drivetransformer: Unified transformer for scalable end-toend autonomous driving. arXiv preprint arXiv:2503.07656, 2025. 6

[30] Anqing Jiang, Yu Gao, Zhigang Sun, Yiru Wang, Jijun Wang, Jinghao Chai, Qian Cao, Yuweng Heng, Hao Jiang, Yunda Dong, et al. Diffvla: Vision-language guided diffusion planning for autonomous driving. arXiv preprint arXiv:2505.19381, 2025. 3

[31] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. Vad: Vectorized scene representation for efficient autonomous driving. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 8340–8350, 2023. 3, 6

[32] Bo Jiang, Shaoyu Chen, Bencheng Liao, Xingyu Zhang, Wei Yin, Qian Zhang, Chang Huang, Wenyu Liu, and Xinggang Wang. Senna: Bridging large vision-language models and end-to-end autonomous driving. arXiv preprint arXiv:2410.22313, 2024. 6

[33] Ming Jin, Chuanxia Sun, and Yinglei Hu. An intelligent traffic detection approach for vehicles on highway using pattern recognition and deep learning. Soft Computing-A Fusion of Foundations, Methodologies & Applications, 27(8), 2023. 1

[34] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. arXiv preprint arXiv:2406.09246, 2024. 1, 3

[35] Wonjae Kim, Bokyung Son, and Ildoo Kim. Vilt: Visionand-language transformer without convolution or region supervision. In International conference on machine learning, pages 5583–5594. PMLR, 2021. 3

[36] Liunian Harold Li, Mark Yatskar, Da Yin, Cho-Jui Hsieh, and Kai-Wei Chang. Visualbert: A simple and perfor-

mant baseline for vision and language. arXiv preprint arXiv:1908.03557, 2019. 3

[37] Zhiqi Li, Wenhai Wang, Hongyang Li, Enze Xie, Chonghao Sima, Tong Lu, Qiao Yu, and Jifeng Dai. Bevformer: learning bird’s-eye-view representation from lidar-camera via spatiotemporal transformers. IEEE Transactions on Pat tern Analysis and Machine Intelligence, 2024. 1

[38] Zhiqi Li, Zhiding Yu, Shiyi Lan, Jiahan Li, Jan Kautz, Tong Lu, and Jose M Alvarez. Is ego status all you need for openloop end-to-end autonomous driving? In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 14864–14873, 2024. 6

[39] Bencheng Liao, Shaoyu Chen, Haoran Yin, Bo Jiang, Cheng Wang, Sixu Yan, Xinbang Zhang, Xiangyu Li, Ying Zhang, Qian Zhang, et al. Diffusiondrive: Truncated diffusion model for end-to-end autonomous driving. In Proceedings of the Computer Vision and Pattern Recognition Conference, pages 12037–12047, 2025. 3

[40] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. Advances in neural information processing systems, 36:34892–34916, 2023. 3

[41] Mingyu Liu, Ekim Yurtsever, Jonathan Fossaert, Xingcheng Zhou, Walter Zimmer, Yuning Cui, Bare Luka Zagar, and Alois C Knoll. A survey on autonomous driving datasets: Statistics, annotation quality, and a future outlook. IEEE Transactions on Intelligent Vehicles, 2024. 1

[42] Liang Ma, Jianru Xue, Kuniaki Kawabata, Jihua Zhu, Chao Ma, and Nanning Zheng. Efficient sampling-based mo tion planning for on-road autonomous driving. IEEE Transactions on Intelligent Transportation Systems, 16(4):1961– 1976, 2015. 1

[43] Yao Mu, Qinglong Zhang, Mengkang Hu, Wenhai Wang, Mingyu Ding, Jun Jin, Bin Wang, Jifeng Dai, Yu Qiao, and Ping Luo. Embodiedgpt: Vision-language pre-training via embodied chain of thought. Advances in Neural Information Processing Systems, 36:25081–25094, 2023. 1

[44] Fei Ni, Jianye Hao, Shiguang Wu, Longxin Kou, Jiashun Liu, Yan Zheng, Bin Wang, and Yuzheng Zhuang. Generate subgoal images before act: Unlocking the chain-of-thought reasoning in diffusion model for robot manipulation with multimodal prompts. In Proceedings ofthe IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 13991–14000, 2024. 1

[45] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In 2024 IEEE International Conference on Robotics and Automation (ICRA), pages 6892–6903. IEEE, 2024. 3

[46] Fred Philippy, Siwen Guo, Shohreh Haddadan, Cedric Lothritz, Jacques Klein, and Tegawende F Bissyand´ e. Soft´ prompt tuning for cross-lingual transfer: When less is more. arXiv preprint arXiv:2402.03782, 2024. 3

[47] Dean A Pomerleau. Alvinn: An autonomous land vehicle in a neural network. Advances in neural information processing systems, 1, 1988. 2

[48] Rui Qian, Xin Lai, and Xirong Li. Badet: Boundary-aware 3d object detection from point clouds. Pattern Recognition, 125:108524, 2022. 1

[49] Tianwen Qian, Jingjing Chen, Linhai Zhuo, Yang Jiao, and Yu-Gang Jiang. Nuscenes-qa: A multi-modal visual question answering benchmark for autonomous driving scenario. In Proceedings of the AAAI Conference on Artificial Intelligence, pages 4542–4550, 2024. 5

[50] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Bjorn Ommer. High-resolution image¨ synthesis with latent diffusion models. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 10684–10695, 2022. 4

[51] Sophia Sirko-Galouchenko, Alexandre Boulch, Spyros Gidaris, Andrei Bursuc, Antonin Vobecky, Patrick Perez, and´ Renaud Marlet. Occfeat: Self-supervised occupancy feature prediction for pretraining bev segmentation networks. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 4493–4503, 2024. 1

[52] Ziying Song, Caiyan Jia, Lin Liu, Hongyu Pan, Yongchang Zhang, Junming Wang, Xingyu Zhang, Shaoqing Xu, Lei Yang, and Yadan Luo. Don’t shake the wheel: Momentumaware planning in end-to-end autonomous driving. In Proceedings of the Computer Vision and Pattern Recognition Conference, pages 22432–22441, 2025. 6

[53] Pei Sun, Henrik Kretzschmar, Xerxes Dotiwalla, Aurelien Chouard, Vijaysai Patnaik, Paul Tsui, James Guo, Yin Zhou, Yuning Chai, Benjamin Caine, et al. Scalability in perception for autonomous driving: Waymo open dataset. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 2446–2454, 2020. 2

[54] Xiaoyu Tian, Junru Gu, Bailin Li, Yicheng Liu, Yang Wang, Zhiyong Zhao, Kun Zhan, Peng Jia, Xianpeng Lang, and Hang Zhao. Drivevlm: The convergence of autonomous driving and large vision-language models. arXiv preprint arXiv:2402.12289, 2024. 6

[55] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. Advances in neural information processing systems, 30, 2017. 3

[56] Fei-Yue Wang. Parallel control and management for intelligent transportation systems: Concepts, architectures, and applications. IEEE transactions on intelligent transportation systems, 11(3):630–638, 2010. 1

[57] Shihao Wang, Zhiding Yu, Xiaohui Jiang, Shiyi Lan, Min Shi, Nadine Chang, Jan Kautz, Ying Li, and Jose M Alvarez. Omnidrive: A holistic llm-agent framework for autonomous driving with 3d perception, reasoning and planning. CoRR, 2024. 6

[58] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. Advances in neural information processing systems, 35:24824–24837, 2022. 1, 3

[59] Penghao Wu, Xiaosong Jia, Li Chen, Junchi Yan, Hongyang Li, and Yu Qiao. Trajectory-guided control prediction for end-to-end autonomous driving: A simple yet strong base-

line. Advances in Neural Information Processing Systems, 35:6119–6132, 2022. 6

[60] Michał Zawalski, William Chen, Karl Pertsch, Oier Mees, Chelsea Finn, and Sergey Levine. Robotic control via embodied chain-of-thought reasoning. arXiv preprint arXiv:2407.08693, 2024. 3

[61] Jiang-Tian Zhai, Ze Feng, Jinhao Du, Yongqiang Mao, Jiang-Jiang Liu, Zichang Tan, Yifu Zhang, Xiaoqing Ye, and Jingdong Wang. Rethinking the open-loop evaluation of end-to-end autonomous driving in nuscenes. arXiv preprint arXiv:2305.10430, 2023. 6

[62] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In Proceedings of the Computer Vision and Pattern Recognition Conference, pages 1702–1713, 2025. 1, 3

[63] Wenzhao Zheng, Ruiqi Song, Xianda Guo, Chenming Zhang, and Long Chen. Genad: Generative end-to-end autonomous driving. In European Conference on Computer Vision, pages 87–104. Springer, 2024. 6

[64] Jiaming Zhou, Ke Ye, Jiayi Liu, Teli Ma, Zifan Wang, Ronghe Qiu, Kun-Yu Lin, Zhilin Zhao, and Junwei Liang. Exploring the limits of vision-language-action manipulations in cross-task generalization. arXiv preprint arXiv:2505.15660, 2025. 1

[65] Xingcheng Zhou and Alois C Knoll. Gpt-4v as traffic assistant: an in-depth look at vision language model on complex traffic events. arXiv preprint arXiv:2402.02205, 2024. 1

[66] Xingcheng Zhou, Xuyuan Han, Feng Yang, Yunpu Ma, and Alois C Knoll. Opendrivevla: Towards end-to-end autonomous driving with large vision language action model. arXiv preprint arXiv:2503.23463, 2025. 6

[67] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In Conference on Robot Learning, pages 2165–2183. PMLR, 2023. 1, 3