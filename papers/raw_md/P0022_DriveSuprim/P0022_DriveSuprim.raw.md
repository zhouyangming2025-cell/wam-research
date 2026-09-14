# DriveSuprim: Towards Precise Trajectory Selection for End-to-End Planning

Wenhao Yao<sup>1,</sup> <sup>2</sup>, Zhenxin Li<sup>1,</sup> <sup>2</sup>, Shiyi Lan<sup>3</sup>, Zi Wang<sup>3</sup>,

Xinglong Sun<sup>3</sup>, Jose M. Alvarez<sup>3</sup>, Zuxuan Wu<sup>1,</sup> <sup>2</sup>\*

<sup>1</sup>Shanghai Key Lab of Intell. Info. Processing, School of CS, Fudan University

<sup>2</sup>Shanghai Collaborative Innovation Center of Intelligent Visual Computing

<sup>3</sup>NVIDIA

{whyao23, lizx23}@m.fudan.edu.cn, zxwu@fudan.edu.cn

## Abstract

Autonomous vehicles must navigate safely in complex driving environments. Imitating a single expert trajectory, as in regression-based approaches, usually does not explicitly assess the safety of the predicted trajectory. Selection-based methods address this by generating and scoring multiple trajectory candidates and predicting the safety score for each. However, they face optimization challenges in precisely selecting the best option from thousands of candidates and distinguishing subtle but safety-critical differences, especially in rare and challenging scenarios. We propose DriveSuprim to overcome these challenges and advance the selection-based paradigm through a coarse-to-fine paradigm for progressive candidate filtering, a rotation-based augmentation method to improve robustness in out-of-distribution scenarios, and a self-distillation framework to stabilize training. DriveSuprim achieves state-of-theart performance, reaching 93.5% PDMS in NAVSIM v1 and 87.1% EPDMS in NAVSIM v2 without extra data, with 83.02 Driving Score and 60.00 Success Rate on the Bench2Drive benchmark, demonstrating superior planning capabilities in various driving scenarios.

Code — https://github.com/William-Yao-2000/DriveSuprim

## Introduction

End-to-end autonomous driving has traditionally relied on regression-based approaches that predict a single trajectory to mimic expert behavior (Jiang et al. 2023; Hu et al. 2023; Wang et al. 2023) . While regression is a common approach, it fundamentally lacks the ability to evaluate multiple alternatives in safety-critical scenarios where subtle trajectory differences can significantly impact outcomes.

In recent years, selection-based methods (Chen et al. 2024; Li et al. 2024c,a; Wang et al. 2025) have clearly outperformed regression approaches. The key is their capability to generate and evaluate diverse trajectory candidates using comprehensive safety metrics such as collision risk and driving rule compliance (Dauner et al. 2024). This explicit comparison enables the system to select the safest and most appropriate trajectory from multiple alternatives, addressing safetycritical issues that regression-based methods cannot address.

<table><tr><td>Top-K</td><td>NC↑</td><td>DAC↑</td><td>EP↑</td><td>TTC↑</td><td>C↑</td><td>PDMS↑</td></tr><tr><td>1</td><td>99.0</td><td>98.7</td><td>86.5</td><td>96.2</td><td>100</td><td>91.9</td></tr><tr><td>4</td><td>99.4</td><td>99.6</td><td>89.6</td><td>98.0</td><td>100</td><td>94.5</td></tr><tr><td>16</td><td>99.7</td><td>99.8</td><td>92.0</td><td>99.1</td><td>100</td><td>96.1</td></tr><tr><td>256</td><td>100</td><td>100</td><td>97.1</td><td>99.9</td><td>100</td><td>98.7</td></tr><tr><td>Human</td><td>100</td><td>100</td><td>87.5</td><td>100</td><td>99.9</td><td>94.8</td></tr></table>

Table 1: PDM score of the best trajectory in the top-K candidates on ranked predicted scores.

Our oracle study in Tab 1 demonstrates the substantial potential of selection-based methods: when making ideal optimal selection, these approaches can even surpass human demonstrations in NAVSIM (Dauner et al. 2024) safety-critical metrics. This performance ceiling highlights why selection-based planning has become the preferred paradigm for autonomous driving systems requiring robust safety guarantees.

However, selection-based methods still face three critical limitations, which make them difficult to reach the ideal perfect trajectory selection displayed in Tab 1 and limit the model performance. First, selection-based methods struggle to distinguish the optimal trajectory from similar but suboptimal alternatives. During training, the model encounters thousands of trajectory candidates where the vast majority are unsafe or impractical (“easy negatives”, the red trajectory in Fig 1). These easy-to-reject options dominate the training process and gradient, causing the model to focus primarily on avoiding obviously incorrect choices. In contrast, the model receives insufficient supervision to select the most suitable trajectory from reasonable-looking trajectories with subtle but important differences (“hard negatives”, the orange trajectory in Fig 1). The overwhelming number of obvious negative examples hinders the model’s ability to develop fine-grained discrimination capability, which is crucial for selecting optimal trajectories when presented with multiple plausible options, to avoid route deviation or collision.

Second, selection-based methods suffer from directional bias in trajectory distribution. This bias manifests as an imbal ance in training data that, while reflecting real-world driving patterns where straight driving predominates, leads to models that perform relatively poorly in turning scenarios. Training with such imbalanced data naturally results in models that excel at straight-line driving but struggle with turns and complex maneuvers. Even advanced autonomous driving datasets like NAVSIM exhibit this limitation. We find that only 18% of ground-truth trajectories in NAVSIM involve turns exceeding 30 degrees. While this distribution may reflect typical driving patterns, it creates a significant challenge for learning models, which require sufficient examples of all maneuver types to develop robust capabilities. This directional bias significantly impairs the model’s ability to select the most precise largeangle turning trajectories, particularly in navigation-critical scenarios where turns are essential.

![](images/fdb6bc137e597528708e45fcc5e2cccb6efd8f13b33fe360bdad5e6a565fde60.jpg)  
Figure 1: Overall pipeline of our method. Selection-based methods struggle to distinguish suboptimal trajectories, perform poorly in turning, and utilize hard binary labels in training. DriveSuprim introduces coarse-to-fine refinement and a rotation-based data augmentation method with self-distillation to address these weaknesses. The green trajectory is the ground-truth trajectory, and the red and orange trajectories are obviously unsafe and seemingly correct trajectory candidates in the trajectory vocabulary.

Third, selection-based methods typically rely on binary classification for safety-related decisions, labeling trajectories as “safe” or “unsafe” based on specific thresholds for collision risk or rule compliance. This binary approach creates hard decision boundaries where trajectories just above or below a safety threshold could be treated entirely differently. Slight variations in score could suddenly thoroughly flip a trajectory label from being selected to being rejected. As a result, models risk becoming overly sensitive to minor changes in trajectory features, which causes inconsistent behavior.

We present DriveSuprim, a novel method that tackles these three critical challenges in selection-based trajectory prediction and makes more nuanced and precise trajectory selection. Our contributions include:

• We propose a coarse-to-fine refinement method that addresses the challenge of distinguishing between similar trajectories. Our method filters promising candidates and applies fine-grained scoring to the most challenging options, significantly improving discrimination between similar but subtly different trajectories.

• We propose an integrated training pipeline combining rotation-based data augmentation with self-distillation to address directional bias and hard decision boundaries. Our approach synthesizes challenging turning scenarios and leverages teacher-generated soft pseudo-labels, effectively balancing trajectory distributions and realizing better optimization for training a more robust model.

• DriveSuprim achieves state-of-the-art performance on the NAVSIM and Bench2Drive benchmark, demonstrating the effectiveness of our model in handling challenging driving scenarios. DriveSuprim significantly outperforms the previous methods by 3.6% and 1.5% on NAVSIMv1 and NAVSIMv2 without introducing other training data. On the Bench2Drive benchmark, our method achieves 83.02 and 60.00 on driving score and success rate.

## Related Works

## End-to-end planning

Autonomous driving has traditionally relied on modular pipelines that separate perception from planning. However, UniAD (Hu et al. 2023) highlights several limitations of this approach, including information loss and error propagation. To address these challenges, end-to-end driving methods (Chen et al. 2019; Chen, Koltun, and Krahenb¨ uhl 2021; Chitta¨ et al. 2022; Hu et al. 2023; Jiang et al. 2023; Li et al. 2024d,c; Wang et al. 2025) unify the perception-to-planning pipeline within a single optimizable network. They process raw sensor inputs and directly output driving trajectories. While some methods (Chen, Koltun, and Krahenb¨ uhl 2021; Zhang et al.¨ 2021) use reinforcement learning (RL) to learn through interaction with simulated environments, the majority adopt imitation learning (IL), training from expert demonstrations without interaction. Most IL-based approaches (Chitta et al. 2022; Hu et al. 2023; Jiang et al. 2023; Li et al. 2025a; Liao et al. 2025) generate a single trajectory using regression or diffusion-based methods to mimic expert behavior.

More recently, selection-based methods (Chen et al. 2024; Li et al. 2024c,a; Wang et al. 2025) have emerged. These models evaluate a diverse set of candidate trajectories by scoring them on safety-focused metrics (e.g., PDM scores (Dauner et al. 2024)). A prominent example is Hydra-MDP (Li et al. 2024c), which employs multiple rule-based teachers and distills them into the planner to create diverse trajectory candidates tailored to different evaluation metrics.

Our proposed model also falls under the selection-based paradigm. However, unlike prior methods that perform a single-shot selection from a fixed candidate set—probably leading to suboptimal decisions—we introduce a coarse-tofine selection and refinement strategy. This approach significantly improves selection precision by progressively narrowing down the trajectory set to the most optimal candidates.

## Iterative & Multi-stage Refinement

Iterative refinement has been widely adopted to improve results in optical flow (Ilg et al. 2017; Hui, Tang, and Loy 2018; Teed and Deng 2020; Xu et al. 2022) and motion estimation (Sun, Harley, and Guibas 2024; Zheng et al. 2023). A common strategy in these works is to iteratively propagate features or trajectory estimates through a shared module to progressively refine the predictions. Inspired by this, iterative refinement is also applied in object detection (Zhu et al. 2020; Cai and Vasconcelos 2018) to improve performance. For instance, in Deformable DETR, each decoder layer refines bounding boxes based on predictions from the previous layer.

We similarly adopt a multi-stage refinement strategy to improve trajectory selection accuracy. However, rather than repeatedly updating fixed-dimensional features, we implement selection from a fixed vocabulary of candidate trajectories. After selection, the search space is progressively narrowed to a more precise subset, improving the final prediction quality.

## Augmentation for Enhanced Robustness

Robustness has long been a critical focus in computer vision research (Ganin et al. 2016; Croce et al. 2020; Rebuffi et al. 2021; Sun et al. 2022). Early studies demonstrated that image models are highly sensitive to minor domain shifts (Azulay and Weiss 2019) and adversarial perturbations (Szegedy 2013; Goodfellow, Shlens, and Szegedy 2014). For example, MNIST-C (Mu and Gilmer 2019) introduces 15 distinct corruption types to benchmark model performance against diverse failure modes. Motivated by these insights, several methods (Rusak et al. 2020; Mintun, Kirillov, and Xie 2021; Kar et al. 2022) utilize corruption-based augmentations, such as adding Gaussian and speckle noise, to enhance robustness. Inspired by these methods, our study explores the use of similar corruption-based augmentation techniques specifically for end-to-end driving models. We introduce targeted perturbations tailored to autonomous driving scenarios, addressing critical domain shifts—particularly the overrepresentation of straightforward driving trajectories—which pose challenges for scenarios involving complex maneuvers such as turns.

## Methods

We introduce our method in this section. Firstly, we introduce preliminaries about the end-to-end planning and the selectionbased method. Next, we introduce our proposed coarse-tofine selection paradigm, rotation-based data augmentation method and self-distillation framework.

## Preliminaries

End-to-End planning & Selection-based planning In autonomous driving, the end-to-end planning requires the planning system to output a future trajectory $\overline { { T } }$ based on input sensor data, like RGB image or Lidar point cloud:

$$
T = \mathrm { P l a n n e r } \left( I m g , L i d a r \right) ,\tag{1}
$$

where the trajectory T can be represented as a sequence of vehicle locations $( u _ { 1 } , u _ { 2 } , . . . , u _ { l } )$ or a sequence of controller actions $( a _ { 1 } , a _ { 2 } , . . . , a _ { l } )$ , and l denotes the sequence length.

Among the end-to-end planning methods, the selectionbased paradigm predefines a trajectory vocabulary $\{ \tau _ { i } \} _ { i = 1 } ^ { N }$ covering N planning trajectories. Given a specific driving scenario, the quality of each trajectory is evaluated by several metrics, like the $l _ { 2 }$ distance to the human teacher trajectory, or metrics considering driving safety and traffic rule adherence. The model learns a scorer that generates trajectory scores $\{ s _ { i } \} _ { i = 1 } ^ { N }$ revealing trajectory quality. The trajectory $\tau _ { k }$ with the highest score is chosen as the predicted result in inference.

## Coarse-to-Fine Trajectory selection

DriveSuprim proposes a coarse-to-fine trajectory selection paradigm comprising coarse filtering and fine-grained scoring, improving model capability in distinguishing hard negative trajectories. As shown in Fig 2, in the coarse filtering stage, the model selects several trajectory candidates based on predicted scores, similar to classic selection-based approaches. The fine-grained scoring stage then produces more accurate scores for the filtered trajectories.

Coarse filtering The coarse filtering stage scores all trajectories in the vocabulary and filters a smaller set of candidates for the next stage. Here we apply the same strategy as the previous selection-based method (Li et al. 2024c). The trajectory feature cross-attends with the image feature to extract planning-related information, then several prediction heads are applied on the refined trajectory feature to regress the normalized $l _ { 2 }$ distance to the ground-truth human trajectory and the rule-based metric scores:

$$
{ \mathcal { E } } _ { \mathrm { i m g } } = \operatorname { E n c } _ { \mathrm { i } } ( I ) , f _ { j } = \operatorname { E n c } _ { \mathrm { t } } ( { \tau } _ { j } ) ,\tag{2}
$$

$$
g _ { j } = \mathrm { T r a n s D e c } ( \mathcal { E } _ { \mathrm { i m g } } , f _ { j } )\tag{3}
$$

$$
s _ { j } ^ { ( m ) } = \mathrm { S i g m o i d } \left( \mathrm { h e a d ^ { ( m ) } } ( g _ { j } ) \right) ,\tag{4}
$$

![](images/f75957a9fea55b9002da2c2c76d8774112ce956deefc1e515c538fbce918ac7a.jpg)  
Figure 2: Model architecture. DriveSuprim adopts a coarse-to-fine paradigm to better distinguish hard negatives. According to the scoring distribution, the Trajectory Decoder filters potential candidates, and the Refinement Decoder further outputs fine-grained trajectory scores. The model introduces rotation-based augmented data to ease the directional bias and applies a self-distillation framework for stable training. The teacher outputs serve as soft labels for auxiliary supervision for the student.

where Enc and Enc are image encoder and trajectory encoder, I and $\mathcal { E } _ { \mathrm { i m g } }$ are the input image and image feature, $\tau _ { j }$ and $f _ { j }$ denote the trajectory and the encoded trajectory feature, TransDec denotes the Trajectory Decoder, which is a Transformer decoder (Vaswani et al. $2 0 1 7 ) , g _ { j }$ denotes the refined trajectory feature, head<sup>(m)</sup> denotes the prediction head of evalutation metric m, $s _ { j } ^ { ( m ) }$ denotes the prediction score of trajectory $\tau _ { j }$ on metric m.

At the end of the coarse filtering stage, each trajectory $\tau _ { j }$ corresponds to a score $s _ { j }$ revealing its quality on end-to-end planning. We select the trajectories with top-k scores as the filtered trajectories $T _ { \mathrm { f i l t e r } } \doteq \{ \tau _ { j } \ | \ j \in \mathcal { T } _ { \mathrm { t o p } k } \}$ , where $\mathcal { T } _ { \mathrm { t o p } k } =$ argsor $\mathrm { t } _ { k } ( \{ s _ { j } \} _ { j = 1 } ^ { N } )$ , and the refined features $G _ { \mathrm { { f i l t e r } } } = \{ g _ { j } \ |$ $j \in \mathcal { T } _ { \mathrm { t o p } k } \}$ are utilized for fine-grained fitting.

Fine-grained scoring In this stage, a Transformer decoder similar to the first stage is applied to make fine-grained scoring and further distinguish the trajectories in the first-stage filtered candidates, which contain a large proportion of hard negatives. Specifically, we obtain the refined score from the lth decoder layer output feature, and optimize with the ground truth trajectory score:

$$
\{ h _ { j , l } \} _ { l = 1 } ^ { n _ { \mathrm { r e f } } } = \mathrm { R e f i n e D e c } ( \mathcal { E } _ { \mathrm { i m g } } , g _ { j } )\tag{5}
$$

$$
s _ { j , l } ^ { ( m ) } = \mathrm { S i g m o i d } \left( \mathrm { h e a d } ^ { ( \mathrm { m } ) } \left( h _ { j , l } \right) \right)\tag{6}
$$

where RefineDec is a Transformer decoder with $n _ { \mathrm { r e f } }$ layers, $h _ { j , l }$ is the refined feature of $\tau _ { j }$ from the l-th layer of the Refinement Transformer, $s _ { j , l } ^ { ( m ) }$ denotes the score of $\tau _ { j }$ on metric m output by the l-th decoder layer. The output trajectory $\tau _ { k }$ is selected based on the highest last-layer output score $s _ { k , n _ { \mathrm { r e f } } } ^ { ( m ) } .$

The loss for the coarse-to-fine module on the original dataset is represented as:

$$
L _ { \mathrm { o r i } } = L _ { \mathrm { c o a r s e } } + L _ { \mathrm { r e f i n e } } ,\tag{7}
$$

where $L _ { \mathrm { c o a r s e } }$ and $L _ { \mathrm { r e f i n e } }$ respectively train the coarse filtering stage and the fine-grained scoring stage. $L _ { \mathrm { c o a r s e } }$ consists of an imitation loss $L _ { \mathrm { i m i } }$ (Li et al. 2024c,a) and a binary cross-entropy between the predicted trajectory score and the ground truth metric score:

$$
L _ { \mathrm { c o a r s e } } = L _ { \mathrm { i m i } } + \sum _ { m , i } \mathrm { B C E } ( s _ { i } ^ { ( m ) } , y _ { i } ^ { ( m ) } ) ,\tag{8}
$$

where $y _ { i } ^ { ( m ) }$ and $s _ { i } ^ { ( m ) }$ are the ground-truth metric score and the predicted score of trajectory $\tau _ { i }$ on metric m. $L _ { \mathrm { r e f i n e } }$ is similar to $L _ { \mathrm { c o a r s e } ; }$ , while it only considers the filtered trajectories $T _ { \mathrm { { f i l t e r } } }$ rather than the entire vocabulary, and is applied on each decoder layer output.

## Rotation-based data augmentation

To mitigate the data imbalance, we introduce an end-to-end rotation-based augmentation pipeline, where a 2D horizontal view transformation is applied to the sensor input data to simulate the ego-vehicle rotation in the 3D space. This approach easily synthesizes more challenging scenarios and diversifies the driving scenarios, enabling the model to precisely select trajectories regardless of the vehicle orientation.

As shown in Fig 3, for each scenario, we sample a random angle θ from a uniform distribution $U [ - \Theta , \Theta ]$ , where Θ is the angle boundary. The positive angle indicates the leftward rotation of the ego vehicle. Camera images corresponding to the original field of view (FOV) along with images from two extended views are concatenated to simulate a “pseudo panoramic view”, then the input image is cropped from the concatenated image according to a shifting window based on θ. For example, for a 1-camera FOV input setting, we choose these three cameras as our input: f (front), $l _ { 0 }$ (front-left), and $r _ { 0 }$ (front-right), where f corresponds to the original field of view, and $l _ { 0 }$ and $r _ { 0 }$ correspond to the extended view.

![](images/75c39ff86d5bd4327db907fea841d88d3310bfdcbc4432d722e324c7e648bd3c.jpg)  
Figure 3: Rotation demonstration for input image in a 1-camera FOV setting. Our rotation-based data augmentation method generates the rotated image through horizontal shifting and cropping.

In the synthesized rotated scenario, the ground truth human trajectory $( u _ { 1 } , u _ { 2 } , \ldots , u _ { l } )$ is generated by a trivial rotation approach: under a specific rotation angle θ, each location $u _ { j }$ of the human trajectory $T _ { h }$ applies a 2D-rotation transformation surrounding the initial vehicle position $u _ { 0 } ,$ , and the rotation angle is −θ, ensuring the world coordinate of the trajectory remains unchanged. Given augmented camera views and the prediction of our model, we calculate a loss $L _ { \mathrm { a u g } }$ for training, which has the same formulation as $L _ { \mathrm { o r i } }$

## Self-distillation with Soft-labeling

Instead of training the selection-based model to fit a hard decision boundary of trajectory evaluation, which can impair training stability, we propose a self-distillation framework with teacher-generated soft labels to stabilize model training. The self-distillation framework consists of a teacher and a student model, both sharing the same architecture. The student is updated via standard gradient descent, whereas the teacher is updated using an exponential moving average (EMA) of the student’s parameters.

During training, the student receives noisier input, including both original and augmented data to calculate $L _ { \mathrm { o r i } }$ and $L _ { \mathrm { a u g } }$ , as shown in Fig 2. The teacher only receives original data to generate scores served as soft labels, where a clipping threshold $\delta _ { m }$ is introduced to control the gap between the teacher output and the ground-truth:

$$
\hat { y } _ { i } ^ { ( m ) } = y _ { i } ^ { ( m ) } + \mathrm { c l i p } \left( s _ { i , \mathrm { t e a c h e r } } ^ { ( m ) } - y _ { i } ^ { ( m ) } , - \delta _ { m } , \delta _ { m } \right)\tag{9}
$$

$$
L _ { \mathrm { s o f t } } = L _ { \mathrm { i m i - s o f t } } + \sum _ { m , i } \mathrm { B C E } ( s _ { i } ^ { ( m ) } , \hat { y } _ { i } ^ { ( m ) } ) ,\tag{10}
$$

where $s _ { i , \mathrm { t e a c h e r } } ^ { ( m ) }$ is the score of trajectory i on metric m predicted by the teacher, $y _ { i } ^ { ( m ) }$ is the ground-truth score of trajectory i on metric m, clip $( \cdot , \alpha , \beta )$ denotes clipping the input value to the interval $[ \alpha , \beta ]$ , and $\hat { y } _ { i } ^ { ( m ) }$ is the soft label. $L _ { \mathrm { i m i - s o f t } }$ is a soft version of $L _ { \mathrm { i m i } }$ , where the human trajectory is shifted toward the teacher model’s output trajectory for at most 1 meter, and is adopted to calculate the imitation loss. The overall training loss of the student model is:

$$
{ \cal L } = { \cal L } _ { \mathrm { o r i } } + { \cal L } _ { \mathrm { a u g } } + { \cal L } _ { \mathrm { s o f t } }\tag{11}
$$

During inference, the teacher model is utilized to output the planning trajectories.

## Experiments

In this section, we first introduce our implementation details. Next, we show the superior performance of DriveSuprim on NAVSIM and Bench2Drive, and ablation studies on NAVSIM are listed to validate the effectiveness of the proposed modules. Finally, we produce some visualization results to intuitively show the advantages of our method.

## Implementation Details

Dataset and Metrics We conduct experiments mainly on the NAVSIM (Dauner et al. 2024) and Bench2Drive (Jia et al. 2024a) benchmark. NAVSIM includes two evaluation metrics, leading to NAVSIM v1 and NAVSIM v2. The evaluation metric of NAVSIM v1 is the PDM Score (PDMS). Each predicted trajectory is sent to a simulator to collect different rule-based metrics, which are weighted aggregated to get the final PDMS. NAVSIM v1 includes 5 metrics: no collisions (NC), drivable area compliance (DAC), ego progress (EP), time-to-collision (TTC), and comfort (C). NAVSIM v2 further introduces 4 extended metrics, including driving direction compliance (DDC), traffic light compliance (TLC), lane keeping (LK) and extended comfort (EC). Aggregating all these subscores leads to the EPDMS metric.

Bench2Drive is a closed-loop benchmark evaluating 220 short routes in CARLA v2. The evaluation metrics include Success Rate, Driving Score, Efficiency and Comfortness. More details about datasets and metrics are in Appendix A.

Model Details and Training Details We conduct our methods on three different backbones as the image encoder Enc , including ResNet34 (He et al. 2016), VoVNet (Lee et al. 2019), and ViT-Large (Dosovitskiy et al. 2021). A 2-layer MLP is leveraged as Enc to encode each trajectory in the vocabulary. The trajectory decoder TransDec and refinement decoder RefineDec are both 3-layer Transformer Decoders with 256 hidden dimensions. The MLP prediction head head<sup>(m)</sup> predicts the normalized $l _ { 2 }$ distance to the human ground-truth trajectory, and each subscore in NAVSIM except for EC. The number of trajectories in the vocabulary and filtered trajectories of the coarse filtering stage are set to 8192 and 256. We adopt a 3-camera FOV setting, with images from $l _ { 0 } , f ,$ , and $r _ { 0 }$ cameras as the input. The rotation angle boundary Θ is set to $\pi / 6$ in the augmentation pipeline. The threshold $\delta _ { m }$ in soft-labeling is set to 0.15.

<table><tr><td>Method</td><td>Backbone</td><td>NC↑</td><td>DAC ↑</td><td>EP↑</td><td>TTC ↑</td><td>C↑</td><td>PDMS ↑</td></tr><tr><td>Human Agent</td><td></td><td>100</td><td>100</td><td>87.5</td><td>100</td><td>99.9</td><td>94.8</td></tr><tr><td>Transfuser (2022)</td><td>ResNet34</td><td>97.7</td><td>92.8</td><td>79.2</td><td>92.8</td><td>100</td><td>84.0</td></tr><tr><td>UniAD (2023)</td><td>ResNet34</td><td>97.8</td><td>91.9</td><td>78.8</td><td>92.9</td><td>100</td><td>83.4</td></tr><tr><td>VADv2 (2024)</td><td>ResNet34</td><td>97.9</td><td>91.7</td><td>77.6</td><td>92.9</td><td>100</td><td>83.0</td></tr><tr><td>LAW (2024b)</td><td>ResNet34</td><td>96.4</td><td>95.4</td><td>81.7</td><td>88.7</td><td>99.9</td><td>84.6</td></tr><tr><td>DRAMA (2024)</td><td>ResNet34</td><td>98.0</td><td>93.1</td><td>80.1</td><td>94.8</td><td>100</td><td>85.5</td></tr><tr><td>Hydra-MDP (2024c)</td><td>ResNet34</td><td>98.3</td><td>96.0</td><td>78.7</td><td>94.6</td><td>100</td><td>86.5</td></tr><tr><td>DiffusionDrive (2025)</td><td>ResNet34</td><td>98.2</td><td>96.2</td><td>82.2</td><td>94.7</td><td>100</td><td>88.1</td></tr><tr><td>DriveSuprim</td><td>ResNet34</td><td>97.8</td><td>97.3</td><td>86.7</td><td>93.6</td><td>100</td><td>89.9 (+1.8)</td></tr><tr><td>Hydra-MDP (2024c)</td><td>V2-99</td><td>98.4</td><td>97.8</td><td>86.5</td><td>93.9</td><td>100</td><td>90.3</td></tr><tr><td>DriveSuprim</td><td>V2-99</td><td>98.0</td><td>98.2</td><td>90.0</td><td>94.2</td><td>100</td><td>92.1 (+1.9)</td></tr><tr><td>Hydra-MDP (2024c)</td><td>ViT-L</td><td>98.4</td><td>97.7</td><td>85.0</td><td>94.5</td><td>100</td><td>89.9</td></tr><tr><td>DriveSuprim</td><td>ViT-L</td><td>98.6</td><td>98.6</td><td>91.3</td><td>95.5</td><td>100</td><td>93.5 (+3.6)</td></tr></table>

Table 2: Evaluation on NAVSIM v1. Results are grouped by backbone types.
<table><tr><td>Method</td><td>Backbone</td><td>NC↑</td><td>DAC ↑</td><td>DDC↑</td><td>TL↑</td><td>EP↑</td><td>TTC↑</td><td>LK↑</td><td>HC↑</td><td>EC↑</td><td>EPDMS ↑</td></tr><tr><td>Human Agent</td><td></td><td>100</td><td>100</td><td>99.8</td><td>100</td><td>87.4</td><td>100</td><td>100</td><td>98.1</td><td>90.1</td><td>90.3</td></tr><tr><td>Ego Status MLP</td><td></td><td>93.1</td><td>77.9</td><td>92.7</td><td>99.6</td><td>86.0</td><td>91.5</td><td>89.4</td><td>98.3</td><td>85.4</td><td>64.0</td></tr><tr><td>Transfuser (2022)</td><td>ResNet34</td><td>96.9</td><td>89.9</td><td>97.8</td><td>99.7</td><td>87.1</td><td>95.4</td><td>92.7</td><td>98.3</td><td>87.2</td><td>76.7</td></tr><tr><td>HydraMDP++ (2024a)</td><td>ResNet34</td><td>97.2</td><td>97.5</td><td>99.4</td><td>99.6</td><td>83.1</td><td>96.5</td><td>94.4</td><td>98.2</td><td>70.9</td><td>81.4</td></tr><tr><td>DriveSuprim</td><td>ResNet34</td><td>97.5</td><td>96.5</td><td>99.4</td><td>99.6</td><td>88.4</td><td>96.6</td><td>95.5</td><td>98.3</td><td>77.0</td><td>83.1 (+1.7)</td></tr><tr><td>HydraMDP++ (2024a)</td><td>V2-99</td><td>98.4</td><td>98.0</td><td>99.4</td><td>99.8</td><td>87.5</td><td>97.7</td><td>95.3</td><td>98.3</td><td>77.4</td><td>85.1</td></tr><tr><td>DriveSuprim</td><td>V2-99</td><td>97.8</td><td>97.9</td><td>99.5</td><td>99.9</td><td>90.6</td><td>97.1</td><td>96.6</td><td>98.3</td><td>77.9</td><td>86.0 (+0.9)</td></tr><tr><td>HydraMDP++ (2024a)</td><td>ViT-L</td><td>98.5</td><td>98.5</td><td>99.5</td><td>99.7</td><td>87.4</td><td>97.9</td><td>95.8</td><td>98.2</td><td>75.7</td><td>85.6</td></tr><tr><td>DriveSuprim</td><td>ViT-L</td><td>98.4</td><td>98.6</td><td>99.6</td><td>99.8</td><td>90.5</td><td>97.8</td><td>97.0</td><td>98.3</td><td>78.6</td><td>87.1 (+1.5)</td></tr></table>

Table 3: Evaluation on NAVSIM v2. Results are grouped by backbone types.

<table><tr><td>Method</td><td>DS↑</td><td>SR↑</td><td>Eff. ↑</td><td>Comf. ↑</td></tr><tr><td>DriveAdapter (2023)</td><td>64.22</td><td>33.08</td><td>70.22</td><td>16.01</td></tr><tr><td>Hydra-NeXt (2025b)</td><td>73.86</td><td>50.00</td><td>197.76</td><td>20.68</td></tr><tr><td>Orion (2025)</td><td>77.74</td><td>54.62</td><td>151.48</td><td>17.38</td></tr><tr><td>AutoVLA (2025)</td><td>78.84</td><td>57.73</td><td>146.93</td><td>39.33</td></tr><tr><td>DriveSuprim</td><td>83.02</td><td>60.00</td><td>238.78</td><td>20.89</td></tr></table>

Table 4: Evaluation on Bench2Drive.

We train our model on 8 NVIDIA A100. We use Adam for model training, the batch size on a GPU is 8, and the learning rate is set to $7 . 5 \times 1 0 ^ { - 5 }$ . More model details and training details are shown in Appendix B.

## Main Results

Result on NAVSIM Tab 2 shows the performance of DriveSuprim on the NAVSIM benchmark. our method reaches 89.9% PDMS with the ResNet34 backbone, surpassing DiffusionDrive by 1.8%. Moreover, DriveSuprim with a stronger Vit-Large backbone can reach 93.5% PDMS. Results in Table 3 show that our model can also reach the SOTA result on the more challenging NAVSIM v2 benchmark. On the EPDMS metric, DriveSuprim surpasses previous SOTA methods by 1.7%, 0.9%, and 1.5%, respectively. DriveSuprim reaches 27.2 FPS and 12.5 FPS with ResNet34 and ViT-Large backbone, achieving real-time planning capability.

Result on Bench2Drive Evaluation on Bench2Drive shows the close loop planning capability of our method. Based on the CARLA-Garage dataset (Jaeger, Chitta, and Geiger 2023; Sima et al. 2024) and the TF++ framework (Jaeger, Chitta, and Geiger 2023), our approach adopts the two-stage trajectory prediction for longitudinal control. Tab 4 shows that DriveSuprim achieves 83.02 and 60.00 scores on Driving Score and Success Rate, with 238.78 Efficiency and 20.89 Comfortness, outperforming the previous SOTA significantly.

## Ablation Studies

Ablation on different modules We conduct ablation studies on the modules and approaches we propose, and the result is shown in Tab 5. Compared to baseline, adopting multistage refinement leads to 1.0% performance gain on PDMS, and the improvements further gained by augmented data and the self-distillation framework are 0.3% and 0.4%.

Effectiveness of coarse-to-fine selection We evolve our model from conventional single-stage selection to coarse-tofine selection, to eliminate the effect of parameter number increase and validate the effectiveness of the coarse-to-fine trajectory selection paradigm. Tab 6 reveals that increasing the number of decoder layers from 3 to 6 brings only 0.3% improvement in EPDMS, while introducing layer-wise scoring and trajectory filtering leads to a more substantial 0.7% gain, proving that the performance boost comes from the coarse-to-fine mechanism rather than model size increase.

<table><tr><td>Multi- stage</td><td>Aug Data</td><td>Self- distill</td><td>NC↑</td><td>DAC ↑</td><td>DDC↑</td><td>TL↑</td><td>EP↑</td><td>TTC ↑</td><td>LK↑</td><td>HC↑</td><td>EC↑</td><td>EPDMS↑</td></tr><tr><td>x</td><td>x</td><td>x</td><td>97.2</td><td>97.5</td><td>99.4</td><td>99.6</td><td>83.1</td><td>96.5</td><td>94.4</td><td>98.2</td><td>70.9</td><td>81.4</td></tr><tr><td>V</td><td>x</td><td>x</td><td>97.5</td><td>96.4</td><td>99.1</td><td>99.6</td><td>87.0</td><td>96.4</td><td>95.3</td><td>98.2</td><td>75.0</td><td>82.4</td></tr><tr><td>√</td><td>√</td><td>x</td><td>96.9</td><td>96.9</td><td>99.4</td><td>99.6</td><td>87.9</td><td>96.0</td><td>95.5</td><td>98.3</td><td>76.5</td><td>82.7</td></tr><tr><td>√</td><td>√</td><td>√</td><td>97.5</td><td>96.5</td><td>99.4</td><td>99.6</td><td>88.4</td><td>96.6</td><td>95.5</td><td>98.3</td><td>77.0</td><td>83.1</td></tr></table>

Table 5: Ablation study on different proposed modules. “Multi-stage” denotes using coarse-to-fine selection, “Aug Data” denotes introducing rotation-based augmentation data, and “Self-distill” denotes adopting self-distillation.

<table><tr><td></td><td>EPDMS ↑</td></tr><tr><td>Single-stage</td><td>81.4</td></tr><tr><td>+ 6 layer decoder</td><td>81.7</td></tr><tr><td>+ Layer-wise scoring</td><td>81.9</td></tr><tr><td>+ Trajectory filtering</td><td>82.4</td></tr></table>

Table 6: Ablation study of the evolution from single-stage selection to coarse-to-fine selection.

Ablation on refinement settings and soft label threshold We further conduct comprehensive ablation studies on the refinement approach and soft-labeling. Utilizing a 3-layer refinement Transformer decoder and filtering 256 trajectories for the refinement stage leads to the best result. For the teacher soft label, choosing 0.15 as the threshold leads to the best EPDM score. Results are shown in Appendix C.

## Visualization and Analysis

Visualization Results Fig 4 shows qualitative visualization results on NAVSIM comparing DriveSuprim with the selection-based approach Hydra-MDP++. The images in the first and second columns are the results of Hydra-MDP++ and DriveSuprim. The first row illustrates a challenging overtaking scenario near a crossroad, where DriveSuprim correctly overtakes while Hydra-MDP++ mistakenly turns left and risks collision. In the second row, DriveSuprim outperforms in a sharp turn with smooth and accurate trajectories. These results demonstrate DriveSuprim not only performs well in challenging scenarios by choosing precise trajectories, but also excels in handling sharp turns with high accuracy. More visualization results are shown in Appendix D.

![](images/d398dcde834c427f350dcd6b2c3cec1a19de7ffa2d824f8a2fff6f6081f1ce0d.jpg)  
Figure 4: Visualization results across various challenging scenarios. In each example, the green trajectory represents the ground truth from the human expert, the red trajectory is generated by Hydra-MDP++, and the blue trajectory is produced by DriveSuprim.

<table><tr><td>Method</td><td>|NAVTEST1 NAVTESTf NAVTESTr</td><td></td><td></td></tr><tr><td>Hydra-MDP++</td><td>68.7</td><td>87.2</td><td>77.7</td></tr><tr><td>DriveSuprim</td><td>71.6 (+2.9)</td><td>88.1 (+0.9)</td><td>79.7 (+2.0)</td></tr></table>

Table 7: EPDMS on three dataset splits. NAVTEST<sub>l</sub>, NAVTEST<sub>f</sub>, and NAVTEST<sub>r</sub> involve left-turning scenarios, near-forward scenarios, and right-turning scenarios.

Superior performance on turning scenarios Tab. 7 demonstrates the superior performance of DriveSuprim in turning scenarios. We divide the test dataset into three subsets based on the turning angle of the ground-truth trajectories: NAVTEST<sub>l</sub> (left turns exceeding 30 degrees), NAVTEST<sub>f</sub> (near-forward trajectories), and NAVTEST<sub>r</sub> (right turns exceeding 30 degrees). Performance improvements of DriveSuprim are more pronounced in turning scenarios than in near-straight ones, highlighting enhanced ability to handle turning maneuvers.

Trajectory distribution comparison We illustrate the trajectory frequency distribution in Appendix D. Results show that in the original dataset, trajectories are predominantly concentrated in the forward or near-forward direction, while in the augmented dataset, trajectories across all directions appear with similar frequency.

## Conclusion

We present DriveSuprim, a novel framework for end-to-end planning. By introducing coarse-to-fine selection and an integrated training pipeline with rotation-based data augmentation and soft-label self-distillation, DriveSuprim significantly enhances the model’s ability to distinguish hard negatives and precisely select trajectories, and performs well in scenarios involving sharp turns. Extensive experiments on the NAVSIM and Bench2Drive benchmark demonstrate that our approach outperforms prior methods by a substantial margin.

## Appendix

## A. More information about Datasets and Metrics

NAVSIM NAVSIM (Dauner et al. 2024) is split into navtrain and navtest, containing 103k and 12k samples for model training and testing. There are two different evaluation metrics on NAVSIM, leading to NAVSIM v1 and NAVSIM v2. The evaluation metric of NAVSIM v1 is the PDM Score (PDMS). Each predicted trajectory is sent to a simulator to collect different rule-based subscores, which are multiplied or weighted aggregated to get the final PDMS:

$$
\mathrm { P D M S } = \left( \prod _ { m \in S _ { P } } \mathbf { s } _ { m } \right) \times \left( \frac { \sum _ { w \in S _ { A } } \mathbf { w } _ { w } \times \mathbf { s } _ { w } } { \sum _ { w \in S _ { A } } \mathbf { w } _ { w } } \right) ,\tag{12}
$$

where $S _ { P }$ and $S _ { A }$ denote the multiplier subscore set and the weighted average subscore set, s denotes the subscore, and w is the weight of each subscore. In NAVSIM v1, $S _ { P }$ comprises two subscores: no collisions (NC) and drivable area compliance (DAC), and $S _ { A }$ comprises ego progress (EP), time-to-collision (TTC), and comfort (C). NAVSIM v2 introduces 4 more subscores, including driving direction compliance (DDC) and traffic light compliance (TLC) in $S _ { P }$ and lane keeping (LK) and extended comfort (EC) in $S _ { A }$ The comfort subscore is also revised to become the history comfort (HC). Aggregating all the above subscores leads to the EPDMS metric.

Bench2Drive Bench2Drive (Jia et al. 2024b) is a recently proposed closed-loop evaluation benchmark for end-to-end autonomous driving, which includes 220 short routes spanning 44 interactive driving scenarios. Each route is around 150 meters. This short-distance route design allows for a comprehensive and accurate analysis of the planning model’s capability. The evaluation metrics include the Success Rate (SR), Driving Score (DS), Efficiency, and Comfortness. The Success Rate measures the proportion of routes executed correctly by the planner, the Driving Score considers the planner’s performance from route completion and rule compliance, the Efficiency checks whether the vehicle speed is too slow, and the Comfortness measures the smoothness by comparing the trajectory with human behaviors.

## B. Supplementary Implementation Details

Model details We conduct our methods on three different backbones as the image encoder Enc , including ResNet34 (He et al. 2016), VoVNet (Lee et al. 2019), and ViT-Large (Dosovitskiy et al. 2021). The input images are resized to a resolution of 2048×512 for ResNet34 and VoVNet, and 1024 × 256 for Vit-Large. The ViT-Large backbone is pre-trained through Depth Anything (Yang et al. 2024).

Training and inference pipelines We adopt two different training pipelines for different backbones. For the models loading the pre-trained backbones, including VoVNet and Vit-Large, we train our model for 6 epochs. The EMA momentum m is increased linearly from 0.992 to 0.996 in the first 3 epochs, and then fixed to 0.998. The model with the ResNet-34 backbone trained from scratch is trained for 10 epochs. The EMA update is applied after the training for 3 epochs, which means that m is set to 0 in the first 3 epochs, then increased from 0.992 to 0.996 in the subsequent 3 epochs, then fixed to 0.998.

<table><tr><td rowspan="2"></td><td rowspan="2">Imi</td><td colspan="2">Mul</td><td colspan="3">Avg</td></tr><tr><td>NC</td><td>DAC</td><td>EP</td><td>TTC</td><td>C</td></tr><tr><td>coefficient</td><td>0.05</td><td>0.5</td><td>0.5</td><td>5.0</td><td>5.0</td><td>2.0</td></tr></table>

Table 8: The inference coefficients on each metric of NAVSIM v1. “Imi” denotes the imitation metric, “Mul” denotes the multiplied penalties, and $^ { \mathrm { \bullet } } \mathrm { A v g } ^ { \mathrm { \bullet } }$ denotes the weighted averages.
<table><tr><td rowspan="2"></td><td rowspan="2">Imi</td><td colspan="2">Mul</td><td colspan="2">Avg</td></tr><tr><td>NC</td><td>DAC DDC</td><td>TL EP</td><td>TTC LK HC</td></tr><tr><td>coefficient |</td><td>0.02</td><td>0.5 0.5</td><td>0.3 0.1</td><td>5.0 5.0 2.0 1.0</td></tr></table>

Table 9: The inference coefficients on each metric of NAVSIM v2. “Imi” denotes the imitation metric, “Mul” denotes the multiplied penalties, and “Avg” denotes the weighted averages.

During inference, we compute a final score for each trajectory by linearly combining the predicted scores across different metrics, and the filtered and final trajectories are selected based on the final score. Specifically, for the imitation learning metric and the multiplier metrics introduced in NAVSIM (Dauner et al. 2024), we apply a coefficient to the logarithm of the predicted score. For the weighted average metric in NAVSIM, the coefficient is applied to the predicted score, followed by an additional logarithmic process of the sum. The overall inference score can be formulated as:

$$
s _ { i } = \sum _ { m } \lambda ^ { ( m ) } \log s _ { i } ^ { ( m ) } + \lambda _ { \mathrm { a v g } } \log \left( \sum _ { n } \lambda ^ { ( n ) } s _ { i } ^ { ( n ) } \right) ,\tag{13}
$$

where m denotes the imitation metric and the multiplier metric, n denotes the weighted average metric, $\lambda ^ { ( m ) }$ and $\lambda ^ { ( n ) }$ denote the coefficient, and $s _ { i }$ denotes the final combined prediction score. $\lambda _ { \mathrm { a v g } }$ is set to 8.0 and 6.0 in NAVSIM v1 and $\mathbf { v } 2 ,$ respectively. The detailed coefficients used during inference on NAVSIM v1 and v2 are shown in Tab 8 and Tab 9.

## C. Supplementary Experiment Result

Ablation on refinement and soft label settings We further conduct comprehensive ablation studies on the refinement approach and soft-labeling. Tab 10 shows that utilizing a 3-layer refinement Transformer decoder and filtering 256 trajectories for the refinement stage leads to the best result. Tab 11 and Tab 12 show ablations on soft label. For the teacher soft label, choosing 0.15 as the clipping threshold and adopting a 1-meter shift in soft imitation learning lead to the best EPDM score.

Model performance with different FOV settings We show the model performance with different FOV settings in Tab 15. The FOV is revealed by the number of cameras.

<table><tr><td>Stage Layer</td><td>Top-K</td><td>EPDMS ↑</td></tr><tr><td>1</td><td>256</td><td>83.0</td></tr><tr><td>3</td><td>256</td><td>83.1</td></tr><tr><td>6</td><td>256</td><td>82.6</td></tr><tr><td>3</td><td>64</td><td>81.8</td></tr><tr><td>3</td><td>512</td><td>82.9</td></tr><tr><td>3</td><td>1024</td><td>83.0</td></tr></table>

Table 10: Ablation on refinement setting. “Stage Layer” is the layer number of the Refinement Decoder, and “Top-K” denotes the number of trajectories selected by the coarse filtering stage.
<table><tr><td> $\delta _ { m }$ </td><td>EPDMS ↑</td></tr><tr><td>0.00 0.15</td><td>82.6 83.1</td></tr><tr><td>0.30</td><td>83.0</td></tr><tr><td>0.70 1.00</td><td>82.9 82.8</td></tr></table>

Table 11: Results with different soft label thresholds. $\delta _ { m }$ denotes the soft label threshold in the Equation 9.

<table><tr><td> $d _ { i }$ </td><td>EPDMS ↑</td></tr><tr><td>0.0</td><td>82.6</td></tr><tr><td>0.5</td><td>83.0</td></tr><tr><td>1.0</td><td>83.1</td></tr><tr><td>2.0</td><td>82.7</td></tr></table>

Table 12: Results with different soft imitation trajectory shift. $d _ { i }$ denotes the soft imitation trajectory shift in $L _ { \mathrm { i m i - s o f t } }$ in the Equation 10.

As shown in Fig 5, five cameras are involved in these settings: f (front camera), $l _ { 0 }$ (front-left camera), $l _ { 1 }$ (left camera), $r _ { 0 }$ (front-right camera), and $r _ { 1 }$ (right camera). The 1-camera setting uses $f _ { 0 }$ as input, the 3-camera setting uses $l _ { 0 } , f _ { 0 }$ and $r _ { 0 }$ as input, while the 5-camera setting uses $l _ { 1 } , l _ { 0 } , f _ { 0 } , r _ { 0 }$ and $r _ { 1 }$ as input. Experimental results show that the 5-camera setting leads to the best performance.

Superiority of self-distillation DriveSuprim utilizes a selfdistillation framework to mitigate the optimization challenges posed by hard binary ground-truth labels. We compare our self-distillation framework with other smoothing techniques to validate its superiority. We adopt temperature-scaled crossentropy and vallina label smoothing, respectively. The temperature is set to $2 . 0 ,$ and the label smoothing coefficient is set to 0.1. As shown in Tab 13, our proposed self-distillation framework achieves the best performance on EPDMS.

Parameter number and inference time We list the number of parameters and inference time of DriveSuprim in Tab 14. Compared to Hydra-MDP++, our model introduces only a minor increase of approximately 7M parameters. Moreover, the FPS drop due to the parameter increase is acceptable. DriveSuprim maintains the real-time planning capability.

<table><tr><td>Smoothing Method</td><td>EPDMS ↑</td></tr><tr><td>Label Smoothing</td><td>82.5</td></tr><tr><td>Temperature-scaled CE</td><td>82.7</td></tr><tr><td>Šelf-distillation</td><td>83.1</td></tr></table>

Table 13: Comparison of different smoothing methods.
<table><tr><td>Model</td><td>Backbone</td><td>EPDMS↑</td><td>Param. ↓</td><td>FPS ↑</td></tr><tr><td>HydraMDP++</td><td>ResNet34</td><td>81.4</td><td>53M</td><td>32.0</td></tr><tr><td>HydraMDP++</td><td>V2-99</td><td>85.1</td><td>103M</td><td>24.0</td></tr><tr><td>HydraMDP++</td><td>Vit-L</td><td>85.6</td><td>337M</td><td>14.4</td></tr><tr><td>DriveSuprim</td><td>ResNet34</td><td>83.1</td><td>61M</td><td>27.2</td></tr><tr><td>DriveSuprim</td><td>V2-99</td><td>86.0</td><td>110M</td><td>22.1</td></tr><tr><td>DriveSuprim</td><td>Vit-L</td><td>87.1</td><td>345M</td><td>12.5</td></tr></table>

Table 14: Comparison of parameter and inference speed.

## D. Visualization

More visualization result Fig 6 shows qualitative visualization results comparing our method with the selectionbased approach Hydra-MDP++ (Li et al. 2024a). In each example, the image with a grey border shows the BEV visualization, the image with a red border is the result of Hydra-MDP++, and the image with a blue border is our result.

The first three columns on the left show challenging driving scenarios with complex vehicle interaction. In the first row, the ego vehicle attempts to overtake a leading vehicle just before a crossroad. DriveSuprim successfully completes the overtaking maneuver, whereas the classic selectionbased method incorrectly does a left turn, potentially leading to a collision. The second and third rows further highlight DriveSuprim’s ability to distinguish between trajectories that appear right at first glance, i.e., the “hard negatives”. Although both models generate similar trajectories, the trajectories produced by Hydra-MDP++ deviate from the road centerline at the endpoint, whereas our method generates near-perfect trajectories that closely align with the human expert’s ground truths. The last three columns highlight the superior performance of our model in sharp-turning scenarios. DriveSuprim consistently produces smooth and accurate turning trajectories even under large turning angles.

These qualitative results demonstrate that DriveSuprim not only performs well in complex and challenging scenarios by generating precise trajectories, but also excels in handling sharp turns with high accuracy.

Trajectory distribution comparison Fig. 7 illustrates the trajectory frequency distribution in both the original dataset and the dataset enhanced with our rotation-based augmentation method. Using the ground-truth PDM score, we count the trajectory that either scores above 0.99 or ranks among the top-three-highest scores in each scenario. We then normalize the frequency by setting the most frequent trajectory to 1. Results show that in the original dataset, the high-score trajectories are predominantly concentrated in the forward or near-forward direction, whereas in the augmented dataset, trajectories across all directions appear with similar frequency.

<table><tr><td>Camera Number</td><td>NC↑</td><td>DAC ↑</td><td>DDC↑</td><td>TL↑</td><td>EP↑</td><td>TTC ↑</td><td>LK↑</td><td>HC↑</td><td>EC↑</td><td>EPDMS ↑</td></tr><tr><td>1 Camera</td><td>97.1</td><td>96.4</td><td>99.4</td><td>99.5</td><td>88.6</td><td>96.2</td><td>96.0</td><td>98.3</td><td>76.2</td><td>82.9</td></tr><tr><td>3 Cameras</td><td>97.5</td><td>96.5</td><td>99.4</td><td>99.6</td><td>88.4</td><td>96.6</td><td>95.5</td><td>98.3</td><td>77.0</td><td>83.1</td></tr><tr><td>5 Cameras</td><td>97.3</td><td>96.8</td><td>99.4</td><td>99.5</td><td>88.3</td><td>96.4</td><td>96.0</td><td>98.3</td><td>76.6</td><td>83.2</td></tr></table>

Table 15: Results with different FOVs (number of cameras).

![](images/b8f4e87e86b0724a9328b77d73c03a9decc564cb62dc8d9c7de2e83bd217529d.jpg)  
Figure 6: Visualization results across various challenging or sharp turning scenarios. In each example, the green trajectory represents the ground truth from the human expert, the red trajectory is generated by the classic selection-based method, and the blue trajectory is produced by DriveSuprim. Zoom in for a better view.

## E. Limitations and Future Work

In this paper, we evaluate the performance of DriveSuprim on the NAVSIM and Bench2Drive benchmark. Our two-stage coarse-to-fine trajectory filtering approach proves effective in enhancing model performance. However, extending this filtering strategy to a multi-stage setting does not yield additional improvements, and the model still has potential to improve performance under challenging or corner cases. In the future, we will further investigate multi-stage refinement techniques and explore reinforcement learning for a more robust planning system.

![](images/563ae53d946cc36ca89ff89bfa84c7763c830225cb81166da1c07473d4f9dee8.jpg)  
Figure 7: Comparison of dataset high-score trajectory distribution. Our augmentation mitigates directional bias, significantly increasing the frequency of previously underrepresented turning trajectories. The color bar represents the normalized frequency of different trajectories in the dataset.

## Acknowledgments

This work was supported by National Natural Science Foundation of China (No. 62427819) and the Science and Technology Commission of Shanghai Municipality (No. 24511103100).

## References

Azulay, A.; and Weiss, Y. 2019. Why do deep convolutional networks generalize so poorly to small image transformations? Journal ofMachine Learning Research, 20(184): 1– 25.

Cai, Z.; and Vasconcelos, N. 2018. Cascade R-CNN: Delving Into High Quality Object Detection. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR).

Chen, D.; Koltun, V.; and Krahenb¨ uhl, P. 2021. Learning to¨ drive from a world on rails. In ICCV, 15590–15599.

Chen, D.; Zhou, B.; Koltun, V.; and Krahenb¨ uhl, P. 2019.¨ Learning by Cheating. In Conference on Robot Learning (CoRL).

Chen, S.; Jiang, B.; Gao, H.; Liao, B.; Xu, Q.; Zhang, Q.; Huang, C.; Liu, W.; and Wang, X. 2024. Vadv2: End-to-end vectorized autonomous driving via probabilistic planning. arXiv preprint arXiv:2402.13243.

Chitta, K.; Prakash, A.; Jaeger, B.; Yu, Z.; Renz, K.; and Geiger, A. 2022. Transfuser: Imitation with transformerbased sensor fusion for autonomous driving. TPAMI, 45(11): 12878–12895.

Croce, F.; Andriushchenko, M.; Sehwag, V.; Debenedetti, E.; Flammarion, N.; Chiang, M.; Mittal, P.; and Hein, M. 2020. Robustbench: a standardized adversarial robustness benchmark. arXiv preprint arXiv:2010.09670.

Dauner, D.; Hallgarten, M.; Li, T.; Weng, X.; Huang, Z.; Yang, Z.; Li, H.; Gilitschenski, I.; Ivanovic, B.; Pavone, M.; Geiger, A.; and Chitta, K. 2024. NAVSIM: Data-Driven Non-Reactive Autonomous Vehicle Simulation and Benchmarking. In NeurIPS, volume 37, 28706–28719.

Dosovitskiy, A.; Beyer, L.; Kolesnikov, A.; Weissenborn, D.; Zhai, X.; Unterthiner, T.; Dehghani, M.; Minderer, M.; Heigold, G.; Gelly, S.; Uszkoreit, J.; and Houlsby, N. 2021. An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale. In ICLR.

Fu, H.; Zhang, D.; Zhao, Z.; Cui, J.; Liang, D.; Zhang, C.; Zhang, D.; Xie, H.; Wang, B.; and Bai, X. 2025. Orion: A holistic end-to-end autonomous driving framework by vision-language instructed action generation. arXiv preprint arXiv:2503.19755.

Ganin, Y.; Ustinova, E.; Ajakan, H.; Germain, P.; Larochelle, H.; Laviolette, F.; March, M.; and Lempitsky, V. 2016. Domain-adversarial training of neural networks. Journal ofMachine Learning Research, 17(59): 1–35.

Goodfellow, I. J.; Shlens, J.; and Szegedy, C. 2014. Explaining and harnessing adversarial examples. arXiv preprint arXiv:1412.6572.

He, K.; Zhang, X.; Ren, S.; and Sun, J. 2016. Deep Residua Learning for Image Recognition. In CVPR.

Hu, Y.; Yang, J.; Chen, L.; Li, K.; Sima, C.; Zhu, X.; Chai, S.; Du, S.; Lin, T.; Wang, W.; et al. 2023. Planning-oriented autonomous driving. In Proceedings ofthe IEEE/CVF Conference on Computer Vision and Pattern Recognition, 17853– 17862.

Hui, T.-W.; Tang, X.; and Loy, C. C. 2018. Liteflownet: A lightweight convolutional neural network for optical flow estimation. In Proceedings of the IEEE conference on computer vision and pattern recognition, 8981–8989.

Ilg, E.; Mayer, N.; Saikia, T.; Keuper, M.; Dosovitskiy, A.; and Brox, T. 2017. Flownet 2.0: Evolution of optical flow estimation with deep networks. In Proceedings ofthe IEEE conference on computer vision andpattern recognition, 2462– 2470.

Jaeger, B.; Chitta, K.; and Geiger, A. 2023. Hidden biases of end-to-end driving models. In Proceedings ofthe IEEE/CVF International Conference on Computer Vision, 8240–8249.

Jia, X.; Gao, Y.; Chen, L.; Yan, J.; Liu, P. L.; and Li, H. 2023. Driveadapter: Breaking the coupling barrier of perception and planning in end-to-end autonomous driving. In Proceedings of the IEEE/CVF International Conference on Computer Vision, 7953–7963.

Jia, X.; Yang, Z.; Li, Q.; Zhang, Z.; and Yan, J. 2024a. Bench2Drive: Towards Multi-Ability Benchmarking of Closed-Loop End-To-End Autonomous Driving. In NeurIPS 2024 Datasets and Benchmarks Track.

Jia, X.; Yang, Z.; Li, Q.; Zhang, Z.; and Yan, J. 2024b. Bench2drive: Towards multi-ability benchmarking of closedloop end-to-end autonomous driving. NeurIPS, 37: 819–844.

Jiang, B.; Chen, S.; Xu, Q.; Liao, B.; Chen, J.; Zhou, H.; Zhang, Q.; Liu, W.; Huang, C.; and Wang, X. 2023. Vad: Vectorized scene representation for efficient autonomous driving. In Proceedings of the IEEE/CVF International Conference on Computer Vision, 8340–8350.

Kar, O. F.; Yeo, T.; Atanov, A.; and Zamir, A. 2022. 3d common corruptions and data augmentation. In Proceedings ofthe IEEE/CVF Conference on Computer Vision and Pattern Recognition, 18963–18974.

Lee, Y.; Hwang, J.-w.; Lee, S.; Bae, Y.; and Park, J. 2019. An Energy and GPU-Computation Efficient Backbone Network for Real-Time Object Detection. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) Workshops.

Li, D.; Ren, J.; Wang, Y.; Wen, X.; Li, P.; Xu, L.; Zhan, K.; Xia, Z.; Jia, P.; Lang, X.; et al. 2025a. Finetuning Generative Trajectory Model with Reinforcement Learning from Human Feedback. arXiv preprint arXiv:2503.10434.

Li, K.; Li, Z.; Lan, S.; Liu, J.; Xie, Y.; zhizhong zhang; Wu, Z.; Yu, Z.; and Alvarez, J. M. 2024a. Hydra-MDP++: Advancing End-to-End Driving via Hydra-Distillation with Expert-Guided Decision Analysis.

Li, Y.; Fan, L.; He, J.; Wang, Y.; Chen, Y.; Zhang, Z.; and Tan, T. 2024b. Enhancing end-to-end autonomous driving with latent world model. arXiv preprint arXiv:2406.08481.

Li, Z.; Li, K.; Wang, S.; Lan, S.; Yu, Z.; Ji, Y.; Li, Z.; Zhu, Z.; Kautz, J.; Wu, Z.; et al. 2024c. Hydra-MDP: End-to-end Multimodal Planning with Multi-target Hydra-Distillation. arXiv preprint arXiv:2406.06978.

Li, Z.; Wang, S.; Lan, S.; Yu, Z.; Wu, Z.; and Alvarez, J. M. 2025b. Hydra-next: Robust closed-loop driving with openloop training. arXiv preprint arXiv:2503.12030.

Li, Z.; Yu, Z.; Lan, S.; Li, J.; Kautz, J.; Lu, T.; and Alvarez, J. M. 2024d. Is ego status all you need for open-loop end-toend autonomous driving? In Proceedings ofthe IEEE/CVF Conference on Computer Vision and Pattern Recognition, 14864–14873.

Liao, B.; Chen, S.; Yin, H.; Jiang, B.; Wang, C.; Yan, S.; Zhang, X.; Li, X.; Zhang, Y.; Zhang, Q.; and Wang, X. 2025. DiffusionDrive: Truncated Diffusion Model for End-to-End Autonomous Driving. In Proceedings ofthe IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR).

Mintun, E.; Kirillov, A.; and Xie, S. 2021. On interaction between augmentations and corruptions in natural corruption robustness. Advances in Neural Information Processing Systems, 34: 3571–3583.

Mu, N.; and Gilmer, J. 2019. Mnist-c: A robustness benchmark for computer vision. arXiv preprint arXiv:1906.02337.

Rebuffi, S.-A.; Gowal, S.; Calian, D. A.; Stimberg, F.; Wiles, O.; and Mann, T. A. 2021. Data augmentation can improve robustness. Advances in Neural Information Processing Systems, 34: 29935–29948.

Rusak, E.; Schott, L.; Zimmermann, R. S.; Bitterwolf, J.; Bringmann, O.; Bethge, M.; and Brendel, W. 2020. A simple way to make neural networks robust against diverse image corruptions. In Computer Vision–ECCV2020: 16th European Conference, Glasgow, UK, August 23–28, 2020, Proceedings, Part III 16, 53–69. Springer.

Sima, C.; Renz, K.; Chitta, K.; Chen, L.; Zhang, H.; Xie, C.; Beißwenger, J.; Luo, P.; Geiger, A.; and Li, H. 2024. Drivelm: Driving with graph visual question answering. In European conference on computer vision, 256–274. Springer.

Sun, J.; Zhang, Q.; Kailkhura, B.; Yu, Z.; Xiao, C.; and Mao, Z. M. 2022. Benchmarking robustness of 3d point cloud recognition against common corruptions. arXiv preprint arXiv:2201.12296.

Sun, X.; Harley, A. W.; and Guibas, L. J. 2024. Refining pre-trained motion models. In 2024 IEEE International Conference on Robotics and Automation (ICRA), 4932–4938. IEEE.

Szegedy, C. 2013. Intriguing properties of neural networks. arXiv preprint arXiv:1312.6199.

Teed, Z.; and Deng, J. 2020. Raft: Recurrent all-pairs field transforms for optical flow. In Computer Vision–ECCV 2020: 16th European Conference, Glasgow, UK, August 23–28, 2020, Proceedings, Part II 16, 402–419. Springer.

Vaswani, A.; Shazeer, N.; Parmar, N.; Uszkoreit, J.; Jones, L.; Gomez, A. N.; Kaiser, L. u.; and Polosukhin, I. 2017. Attention is All you Need. In Guyon, I.; Luxburg, U. V.; Bengio, S.; Wallach, H.; Fergus, R.; Vishwanathan, S.; and Garnett, R., eds., Advances in Neural Information Processing Systems.

Wang, X.; Zhu, Z.; Huang, G.; Chen, X.; Zhu, J.; and Lu, J. 2023. Drivedreamer: Towards real-world-driven world models for autonomous driving. arXiv preprint arXiv:2309.09777.

Wang, Z.; Lan, S.; Sun, X.; Chang, N.; Li, Z.; Yu, Z.; and Alvarez, J. M. 2025. Enhancing Autonomous Driving

Safety with Collision Scenario Integration. arXiv preprint arXiv:2503.03957.

Xu, H.; Zhang, J.; Cai, J.; Rezatofighi, H.; and Tao, D. 2022. Gmflow: Learning optical flow via global matching. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 8121–8130.

Yang, L.; Kang, B.; Huang, Z.; Xu, X.; Feng, J.; and Zhao, H. 2024. Depth Anything: Unleashing the Power of Large-Scale Unlabeled Data. In CVPR.

Yuan, C.; Zhang, Z.; Sun, J.; Sun, S.; Huang, Z.; Lee, C. D. W.; Li, D.; Han, Y.; Wong, A.; Tee, K. P.; et al. 2024. Drama: An efficient end-to-end motion planner for autonomous driving with mamba. arXiv preprint arXiv:2408.03601.

Zhang, Z.; Liniger, A.; Dai, D.; Yu, F.; and Van Gool, L. 2021. End-to-end urban driving by imitating a reinforcement learning coach. In Proceedings of the IEEE/CVF international conference on computer vision, 15222–15232.

Zheng, Y.; Harley, A. W.; Shen, B.; Wetzstein, G.; and Guibas, L. J. 2023. Pointodyssey: A large-scale synthetic dataset for long-term point tracking. In Proceedings ofthe IEEE/CVF International Conference on Computer Vision, 19855–19865.

Zhou, Z.; Cai, T.; Zhao, S. Z.; Zhang, Y.; Huang, Z.; Zhou, B.; and Ma, J. 2025. AutoVLA: A Vision-Language-Action Model for End-to-End Autonomous Driving with Adaptive Reasoning and Reinforcement Fine-Tuning. arXiv preprint arXiv:2506.13757.

Zhu, X.; Su, W.; Lu, L.; Li, B.; Wang, X.; and Dai, J. 2020. Deformable detr: Deformable transformers for end-to-end object detection. arXiv preprint arXiv:2010.04159.