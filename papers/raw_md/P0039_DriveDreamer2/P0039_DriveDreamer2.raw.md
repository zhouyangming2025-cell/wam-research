# DriveDreamer-2: LLM-Enhanced World Models for Diverse Driving Video Generation

Guosheng Zhao<sup>1∗</sup>, Xiaofeng Wang<sup>1∗</sup>, Zheng Zhu<sup>2∗B</sup>, Xinze Chen<sup>2</sup>, Guan Huang<sup>2</sup>, Xiaoyi Bao<sup>1</sup>, and Xingang Wang<sup>1B</sup>

<sup>1</sup> Institute of Automation, Chinese Academy of Sciences <sup>2</sup> GigaAI Project Page: https://drivedreamer2.github.io

![](images/839a546209cf03da42b017bef110139466bd99a98af797783fd7fbb5761e7aa0.jpg)

(a) User-customized driving video generation.  
![](images/ba3e003d640c1ea654edf67a17fc603963999b8d77277dff425a82a0629ef9f7.jpg)

![](images/ece02d9f94dc4fb7049aba822386ce710d544fe1f392f918efe1e435f1e44e2e.jpg)

![](images/9dbdd83a4e6a36de3f5f7d6ac2057f1f49e5e165156e37f4706787120ffa0d02.jpg)

![](images/8285009d4adccef313ccf0438ac681063b93caf5dfe30c2e2a57ac104a860975.jpg)  
(b) Generated video quality comparison and improvement in the downstream task.  
Fig. 1: DriveDreamer-2 demonstrates powerful capabilities in generating multi-view driving videos. DriveDreamer-2 can produce driving videos based on user descriptions, which improves the diversity of the synthetic data. Besides, the generation quality of DriveDreamer-2 surpasses other state-of-the-art methods and efectively enhances downstream tasks.

Abstract. World models have demonstrated superiority in autonomous driving, particularly in the generation of multi-view driving videos. However, significant challenges still exist in generating customized driving

videos. In this paper, we propose DriveDreamer-2, which builds upon the framework of DriveDreamer and incorporates a Large Language Model (LLM) to generate user-defined driving videos. Specifically, an LLM interface is initially incorporated to convert a user’s query into agent trajectories. Subsequently, a HDMap, adhering to trafic regulations, is generated based on the trajectories. Ultimately, we propose the Unified Multi-View Model to enhance temporal and spatial coherence in the generated driving videos. DriveDreamer-2 is the first world model to generate customized driving videos, it can generate uncommon driving videos (e.g., vehicles abruptly cut in) in a user-friendly manner. Besides, experimental results demonstrate that the generated videos enhance the training of driving perception methods (e.g., 3D detection and tracking). Furthermore, video generation quality of DriveDreamer-2 surpasses other state-of-the-art methods, showcasing FID and FVD scores of 11.2 and 55.7, representing relative improvements of ∼30% and ∼50%.

Keywords: World models · Autonomous driving · Video generation

## 1 Introduction

World models for autonomous driving [23,25,59,62] have drawn extensive attention from both the industry and academia in recent years. Benefiting from their excellent predictive capabilities, autonomous driving world models facilitate the generation of diverse driving videos, encompassing even long-tail scenarios. The generated driving videos can be utilized to enhance the training of various driving perception approaches, proving highly beneficial for practical applications in autonomous driving.

World modeling in autonomous driving presents a formidable challenge due to its inherent complexity and large sampling space. Early approaches [8, 22] mitigate these problems by incorporating world modeling within the Bird’s Eye View (BEV) semantic segmentation space. However, these methods primarily explore world models in simulated autonomous driving environments. In the recent evolution of autonomous driving technologies, there has been a substantial leap forward in the development of world models. This progress has been propelled by the utilization of cutting-edge difusion models [5, 17, 18, 39, 40, 46], exemplified by notable contributions such as DriveDreamer [59], Drive-WM [62], Magic-Drive [7], Panacea [64], and the integration of large language models like GAIA-1 [23], ADriver-I [25]. These sophisticated models have played a pivotal role in pushing the boundaries of world modeling capabilities, enabling researchers and engineers to delve into increasingly intricate and realistic driving scenarios. However, it is important to note that a majority of these methods rely heavily on structured information (e.g., 3D boxes, HDMaps, and optical flow) or real-world image frames as conditions. This dependence not only constrains interactivity but also limits the diversity of generated videos.

To tackle the aforementioned challenges, we propose DriveDreamer-2, which is the first world model to generate diverse driving videos in a user-friendly manner. In contrast to previous methods [7,59,62] that rely on structured conditions either from specific datasets or sophisticated annotations, DriveDreamer-2 emphasizes generating customized driving videos by simulating various trafic conditions with user-friendly text prompts. Specifically, the trafic simulation task has been disentangled into the generation of foreground conditions (trajectories of the ego-car and other agents) and background conditions (HDMaps of lane boundary, lane divider, and pedestrian crossing). For foreground generation, a functional library is constructed to finetune a Large Language Model (LLM), enabling it to generate agent trajectories based on user text input. For background conditions, we propose the HDMap generator that employs a difusion model to simulate road structures. In this process, the previously generated agent trajectories are involved as conditional inputs, which allows the HDMap generator to learn the associations between foreground and background conditions in driving scenes. Building upon the generated trafic structured conditions, we employ the DriveDreamer [59] framework to generate multi-view driving videos. It is noted that we introduce the Unified Multi-view Video Model (UniMVM) within the DriveDreamer framework, which is designed to unify both intra-view and crossview spatial consistency, enhancing the overall temporal and spatial coherence in the generated driving videos.

Extensive experiment results show that DriveDreamer-2 is capable of producing diverse user-customized videos, including uncommon scenarios where vehicles abruptly cut in (depicted in Fig. 1). Besides, DriveDreamer-2 can generate highquality driving videos with an FID of 11.2 and FVD of 55.7, relatively improving previous best-performing methods by ∼30% and ∼50%. Furthermore, experiments are conducted to verify that driving videos generated by DriveDreamer-2 can enhance the training of various autonomous driving perception methods, where the performance of detection and tracking are relatively improved by ∼4% and ∼8%.

The main contributions of this paper can be summarized as follows:

– We present DriveDreamer-2, which is the first world model to generate diverse driving videos in a user-friendly manner.

– We propose a trafic simulation pipeline employing only text prompts as input, which can be utilized to generate diverse trafic conditions for driving video generation.

– UniMVM is presented to seamlessly integrate intra-view and cross-view spatial consistency, elevating the overall temporal and spatial coherence within the generated driving videos.

– Extensive experiments are conducted to show that DriveDreamer-2 can craft diverse customized driving videos. Besides, DriveDreamer-2 enhances the FID and FVD by ∼30% and ∼50% compared to previous best-performing methods. Moreover, the driving videos generated by DriveDreamer-2 enhance the training of various driving perception methods.

## 2 Related Works

## 2.1 World Models

The primary objective of world methods is to establish dynamic environmental models, endowing agents with predictive capabilities for the future. In the early exploration, Variational Autoencoders (VAE) [31] and Long Short-Term Memory (LSTM) [19] are employed to capture transition dynamics and rendering functionality, showcasing remarkable success across diverse applications [9–13,13,29,36,48,65]. Constructing driving world models poses distinctive challenges, primarily arising from the high sample complexity inherent in real-world driving tasks [3]. To address these challenges, ISO-Dream [42] introduces an explicit disentanglement of visual dynamics into controllable and uncontrollable states. MILE [22] strategically incorporates world modeling within the Bird’s Eye View (BEV) semantic segmentation space. Recently, DriveDreamer [59], GAIA-1 [23], ADriver-I [25], and Drive-WM [62] have explored the training of driving world models in the real world, leveraging powerful difusion models or natural language models. However, most of these methods heavily depend on structured information (e.g., 3D boxes, HDMaps, and optical flow) as conditions. This dependency not only constrains interactivity but also limits generation diversity.

## 2.2 Video Generation

Video generation and prediction are pivotal techniques for understanding the visual world. In the early stages of video generation, methods like Variational Autoencoders (VAEs) [4, 21], flow-based model [33], and Generative Adversarial Networks (GANs) [38, 47, 53, 56] are explored. Language models [20, 26, 32, 45, 51, 55, 60, 63] are also employed for intricate visual dynamics modeling. Recent advancements have seen difusion models [5, 17, 18, 39, 40, 46] extending their influence to video generation. Notably, video difusion models [1, 14, 16, 28, 49, 58, 67] exhibit superior capabilities in generating high-quality videos with realistic frames and smooth transitions, ofering enhanced controllability. These models adapt seamlessly to various input conditions, including text, canny, sketch, semantic maps, and depth maps. In the realm of autonomous driving, DriveDreamer-2 leverages powerful difusion models for learning visual dynamics.

## 2.3 Trafic Simulation

Driving simulators stand as a cornerstone in self-driving development, aiming to ofer a controlled environment to mimic real-world conditions. LCTGen [52] utilizes an LLM to encode detailed language descriptions to a vector and subsequently employs a generator to produce corresponding simulated scenarios. This method requires highly detailed language descriptions, including information such as the speed and orientation of agents. TraficGen [6] comprehends the inherent relationships within trafic scenarios, enabling the generation of diverse and legitimate trafic flows within the same map. CTG [70] generates trafic simulations by employing manually designed loss functions that adhere to trafic constraints. CTG++ [69] further extends CTG by utilizing GPT-4 [41] to convert user language descriptions into a loss function, which guides the scene-level conditional difusion model to generate the corresponding scenario. In DriveDreamer-2, we construct a functional library to finetune the LLM to achieve a user-friendly text-to-trafic simulation, which eliminates intricate loss design or complex text prompt inputs.

![](images/0976469f921037d8571c2ff13318df82d1909671933a1182372d3b73f38e1c50.jpg)  
Fig. 2: The overall framework of DriveDreamer-2 involves initially generating agent trajectories according to the user query, followed by producing a realistic HDMap, and finally generating multi-view driving videos.

## 3 DriveDreamer-2

Fig. 2 illustrates the overall framework of DriveDreamer-2. A customized traffic simulation is first proposed to generate foreground agent trajectories and background HDMaps. Specifically, DriveDreamer-2 utilizes a finetuned LLM to translate user prompts into agent trajectories, and the HDMap generator is then introduced to simulate road structures using the generated trajectories as conditions. Leveraging the customized trafic simulation pipeline, DriveDreamer-2 is capable of generating diverse structured conditions for the subsequent video generation. Building upon the architecture of DriveDreamer [59], the UniMVM framework is proposed to unify both intra-view and cross-view spatial consistency, thereby enhancing the overall temporal and spatial coherence in the generated driving videos. In the subsequent sections, we delve into the details of the customized trafic simulation and the UniMVM framework.

## 3.1 Customized Trafic Simulation

In the proposed customized trafic simulation pipeline, a trajectory-generation function library is constructed to finetune the LLM, which facilitates transferring user prompts into diverse agent trajectories, encompassing maneuvers such as cut-ins and U-turns. Additionally, the pipeline incorporates the HDMap generator to simulate the background road structures. During this phase, the previously generated agent trajectories serve as conditional inputs, ensuring that the resulting HDMap adheres to trafic constraints. In the following, we elaborate on the finetuning process of the LLM and the framework of the HDMap generator.

![](images/f46aa59d3745aba1af338344a3ea702c7c9d5acd163b0e313110a15ca72f7f65.jpg)  
Fig. 3: The overview of customized trajectory generation. Initially, we leverage the established function library to assemble Text-to-Python-Script pairs. Subsequently, the constructed dataset is employed to finetune LLM. Finally, the customized trajectories is generated by LLM based on user query.

Finetuning LLM for Trajectory Generation Previous trafic simulation methods [37, 69, 70] necessitate the intricate specification of parameters, involving details such as the agent’s speed, position, acceleration, and mission goal. To simplify this intricate process, we propose to finetune LLM with the constructed trajectory-generation function library, allowing for the eficient transformation of user-friendly language inputs into comprehensive trafic simulation scenarios. As depicted in Fig. 3, the constructed function library encompasses 18 functions, including agent functions (steering, constant speed, acceleration, and braking), pedestrian functions (walking direction and speed), and other utility functions such as saving trajectories. Building upon these functions, Text-to-Python-Scripts pairs are manually curated for finetuning LLM (GPT-3.5). The scripts include a range of fundamental scenarios such as lane-changing, overtaking, following other vehicles, and executing U-turns. Additionally, we encompass more uncommon scenarios like pedestrians abruptly crossing, and vehicles cutting into the lane. Taking the user input a vehicle cuts in as an example, the corresponding script involves the following steps: initially generating a trajectory of cutting in (agent.cut\_in()), followed by generating the corresponding ego car trajectory (agent.forward()), and ultimately utilizing the saving function from utilities to directly output the trajectory of the ego-car and other agents in array format. For additional details, please refer to the supplementary materials. In the inference phase, we follow [37] to expand prompt inputs to a pre-defined template, and the finetuned LLM can directly output the trajectory array.

HDMap Generation A comprehensive trafic simulation not only entails the trajectories of foreground agents but also necessitates the generation of background HDMap elements such as lanes and pedestrian crosswalks. Therefore, the HDMap generator is proposed to ensure the background elements do not conflict with the foreground trajectories. In the HDMap generator, we formulate the background elements generation as a conditional image generation problem, where the conditional input is the BEV trajectory map $\bar { \mathcal { T } _ { b } } \in \mathcal { R } ^ { 3 \times H _ { b } \times } \bar { W } _ { b }$ , and the target is the BEV HDMap $\mathcal { H } _ { b } \in \mathcal { R } ^ { 3 \times H _ { b } \times W _ { b } }$ . Diferent from previous conditional image generation approaches [35, 68] that predominantly rely on outline conditions (edges, depths, boxes, segmentation maps), the proposed HDMap generator explores the correlations between the foreground and background traffic elements. Specifically, the HDMap generator is constructed upon an imagegeneration difusion model. To train the generator, we curate a trajectory-to-HDMap dataset $\mathcal { D } = \{ \mathcal { T } _ { b } , \mathcal { H } _ { b } \}$ . In the trajectory map, distinct colors are assigned to represent diferent agent categories. Meanwhile, the target HDMap comprises three channels, representing lane boundaries, lane dividers, and pedestrian crossings, respectively. Within the HDMap generator, we employ stacks of 2D convolution layers to incorporate the trajectory map condition. The resulting feature maps $C \tau$ are then seamlessly integrated into the difusion model using [68] (see supplement for additional architectural details). In the training stage, the difusion forward process gradually adds noise $\epsilon$ to the latent feature $\mathcal { Z } _ { 0 }$ , resulting in the noisy latent feature $\mathcal { Z } _ { T _ { b } }$ . Then we train $\epsilon _ { \theta }$ to predict the noise we added, and the HDMap generator $\phi$ is optimized via

![](images/6252a46f93ac2561d4c96f4ae711472f0282b8dfaa361f872f3e95b491dfa666.jpg)  
Fig. 4: The proposed HDMap generator can generate diverse BEV HDMaps based on the same BEV trajectory input. The orange and yellow colors represent the motion trajectories of the ego car and other vehicles, respectively. The red color indicates road boundaries, the blue color represents lane dividers, and the green color signifies pedestrian crossings.

$$
\operatorname* { m i n } _ { \boldsymbol { \phi } } \mathcal { L } = \mathbb { E } _ { \mathcal { Z } _ { 0 } , \epsilon \sim \mathcal { N } ( \mathbf { 0 } , \mathbf { I } ) , t , c } \left[ \| \epsilon - \epsilon _ { \theta } ( \mathcal { Z } _ { t } , t , c ) \| _ { 2 } ^ { 2 } \right] ,\tag{1}
$$

where time step t is uniformly sampled from $[ 1 , T _ { b } ]$ . As shown in Fig. 4, leveraging the proposed HDMap generator allows us to generate diverse HDMaps based on the same trajectory conditions. It is noteworthy that the generated HDMaps not only adhere to trafic constraints (lane boundaries positioned on either side of lane dividers, and pedestrian crossings at intersections) but also seamlessly integrate with trajectories.

![](images/5dbade9fe3775b8e68d4eec75f141a9486bb44f049488003d5c706bbfc87c7a8.jpg)  
Fig. 5: The comparison of multi-view video generation paradigms. All structural conditions and text prompts are omitted here to emphasize the distinctions between our UniMVM and previous methods. By adjusting the mask, UniMVM can generate videos conditioned on the initial frame, front view video, and without image input.

## 3.2 UniMVM

Utilizing structured information generated by the customized trafic simulation, multi-view driving videos can be generated via the framework of DriveDreamer [59]. However, the view-wise attention introduced in previous methods [59, 66] can not guarantee multi-view consistency. To mitigate this problem, [34, 62, 64] employ image or video conditions to generate multi-view driving videos. While this approach enhances consistency between diferent views, it comes at the expense of reduced generation eficiency and diversity. In DriveDreamer-2, we introduce the UniMVM within the DriveDreamer framework. The UniMVM is designed to unify the generation of multi-view driving videos both with and without adjacent view conditions, which ensures temporal and spatial coherence without compromising generation speed and diversity.

Formulation In multi-view video dataset p , $\mathbf { \bar { x } } \in \mathcal { R } ^ { K \times T \times 3 \times H \times W }$ is a sequence of $T$ images with K views, with height H and width W. Let $\mathrm { x } _ { i }$ denote the sample of i-th view, then the multi-view video joint distribution $p ( \mathrm { x } _ { 1 } , . . . , \mathrm { x } _ { \mathrm { K } } )$ can be obtained by [62]:

$$
p ( \mathrm { x } _ { 1 } , . . . , \mathrm { x } _ { \mathrm { K } } ) = p ( \mathrm { x } _ { 1 } ) p ( \mathrm { x } _ { 2 } | \mathrm { x } _ { 1 } ) . . . p \left( \left. \mathrm { x } _ { K } \right| \mathrm { x } _ { 1 } , \mathrm { x } _ { 2 } . . . , \mathrm { x } _ { K - 1 } \right) .\tag{2}
$$

Eq. 2 indicates that adjacent view videos can be expanded with multiple generation steps, which is ineficient. In the proposed UniMVM, we draw inspiration from the Eq. 2 to expand the view. However, unlike Drive-WM [62] which requires the independent generation of views, UniMVM unifies multiple views as a complete patch. Specifically, we concatenate the multi-view video in the order of {FL, F, FR, BR, B, BL}<sup>1</sup> to obtain the spatially unified image $\mathbf { x } ^ { \prime } \in \mathcal { R } ^ { T \times 3 \times H \times \mathbf { \dot { K } } W }$ Then we can obtain the multi-view driving video distribution $p ( \mathrm { x } ^ { \prime } )$

$$
p ( \mathbf { x } ^ { \prime } ) = p ( \mathbf { x } ^ { \prime } \cdot ( 1 - m ) , \mathbf { x } ^ { \prime } \cdot m ) = p ( \mathbf { x } ^ { \prime } \cdot m ) p ( \mathbf { x } ^ { \prime } \cdot ( 1 - m ) | \mathbf { x } ^ { \prime } \cdot m ) ,\tag{3}
$$

where m represents the mask of one of the all views. As shown in Fig. 5, we compare the paradigm of UniMVM with that of DriveDreamer [59] and Drive-WM [62]. In contrast to these counterparts, UniMVM unifies multiple views into a complete patch for video generation without introducing cross-view parameters. Furthermore, various driving video generation tasks can be accomplished via adjusting the mask m. Specifically, when m is set to mask future $T - 1$ frames, UniMVM enables future video prediction based on the input of the first frame. Configuring m to mask {FL, FR, BR, B, BL} views empowers UniMVM to achieve multi-view video outpainting, leveraging a front-view video input. Furthermore, UniMVM can generate multi-view videos when m is set to mask all video frames, and both quantitative and qualitative experiments verify that UniMVM is capable of generating temporally and spatially coherent videos with enhanced eficiency and diversity.

Video Generation Based on the UniMVM formulation, driving videos can be generated within the framework of DriveDreamer [59]. Specifically, our approach first unify the trafic structured conditions, which results in sequences of HDMaps $\{ \mathcal { H } _ { i } \} _ { i = 0 } ^ { N - \ddot { 1 } } \in \mathcal { R } ^ { N \times 3 \times H \times K W }$ and 3D boxes $\{ B _ { i } \} _ { i = 0 } ^ { N - 1 } \in \mathcal { R } ^ { N \times C \times H \times K W }$ (N is the frame number of video clip, and C is the category number). Note that sequences of 3D boxes can be derived from agent trajectories, and the sizes of 3D boxes are determined based on the respective agent category. Unlike DriveDreamer, the 3D box conditions in DriveDreamer-2 no longer rely on position embedding and category embedding. Instead, the boxes are directly projected onto the image plane, functioning as a control condition. This approach eliminates introducing additional control parameters as in [59]. We adopt three encoders to embed HDMaps, 3D boxes, and image frames into latent space features y , y , and $y _ { \mathcal { T } }$ Then we concatenate the spatially aligned conditions $y _ { \mathcal { H } } , ~ y _ { B }$ with $\mathcal { Z } _ { t }$ to obtain the feature input $\mathcal { Z } _ { i n }$ , where $\mathcal { Z } _ { t }$ is the noisy latent feature generated from y<sub>I</sub> by the forward difusion process. For the training of the video generator, all parameters are optimized via denoising score matching [27] (see supplement for details).

## 4 Experiment

## 4.1 Experiment Details

Dataset. The training dataset is derived from the nuScenes dataset [2], consisting of 700 training videos and 150 validation videos. Each video encompasses approximately 20 seconds of recorded footage, captured by six surround-view cameras. With a frame rate of 12Hz, this accumulates to around 1 million video frames available for training. Following [59,61], we preprocess the nuScenes dataset to calculate 12Hz annotations. Specifically, HDMaps and 3D boxes are transformed to BEV perspective to train HDMap generation, and these annotations are projected to pixel coordinate to train video generation.

Training. For agent trajectory generation, we employ GPT-3.5 as the LLM. Subsequently, we utilize the constructed text-to-script dataset to finetune GPT-3.5 into an LLM with specialized trajectory generation knowledge. The proposed

![](images/861d8b41e6e5ffa634623cccac24b65b991a727a5402e699264c5ff9195ac691.jpg)  
Fig. 6: User-customized driving videos generated by DriveDreamer-2. The top row depicts a scene where the ego car changes lanes, while the bottom row shows an unexpected pedestrian crossing the road at night.

HDMap generator is built upon SD2.1 [46] with the ControlNet parameters [68] being trainable. The HDMap generator undergoes 55K training iterations with a batch size of 24 and a resolution of $5 1 2 \times 5 1 2$ . For the video generator, we harness the powerful video generation capabilities of SVD [1], and all the parameters are finetuned. During the training of the video generator, the mode is trained for 200K iterations with a batch size of 1, a video frame length of N = 8, a view number of $K \ : = \ : 6$ , and a spatial size of 256 × 448. All the experiments are conducted on NVIDIA A800 (80GB) GPUs, and we use the AdamW optimizer [30] with a learning rate $5 \times 1 0 ^ { - 5 }$

Evaluation. Extensive qualitative and quantitative experiments are conducted to assess DriveDreamer-2. For qualitative experiments, we visualize customized driving video generation to validate that DriveDreamer-2 can produce diverse driving videos in a user-friendly manner. Additionally, visualization comparisons are conducted between UniMVM and other generative paradigms to demonstrate that DriveDreamer-2 excels in generating temporally and spatially coherent videos. For quantitative experiments, the frame-wise Fréchet Inception Distance (FID) [43] and Fréchet Video Distance (FVD) [54] are utilized as metrics. Besides, StreamPETR [57], building upon a ResNet-50 [15] backbone, is trained at the same resolution of 256 × 448 to evaluate the improvements of 3D object detection and multi-object tracking achieved by our generated results. More details can be found in the supplementary material.

## 4.2 User-Customized Driving Video Generation

DriveDreamer-2 ofers a user-friendly interface for generating driving videos. As depicted in Fig. 1a, users are only required to input a text prompt (e.g., on a rainy day, there is a car cut in). Then DriveDreamer-2 produces multiview driving videos aligned with the text input. Fig. 6 illustrates another two customized driving videos. The upper one depicts the process of the ego car changing lanes to the left during the daytime. The lower one showcases an unexpected pedestrian crossing the road at night, prompting the ego car to brake to avoid the collision. Notably, the generated videos demonstrate an exceptional level of realism, where we can even observe the reflection of high beams on the pedestrian.

Table 1: Comparison of the generation quality on nuScenes validation set. † denotes that the corresponding conditions are generated.
<table><tr><td>Method</td><td>Conditions</td><td>FID↓</td><td>FVD↓</td></tr><tr><td>DriveDreamer [59]</td><td>一</td><td>26.8</td><td>353.2</td></tr><tr><td>DriveDreamer-2</td><td></td><td>25.0</td><td>105.1</td></tr><tr><td>Drive-WM [62]</td><td>3-view videos†</td><td>15.8</td><td>122.7</td></tr><tr><td>DriveDreamer-2</td><td>1-view video</td><td>18.4</td><td>74.9</td></tr><tr><td>DriveDreamer [59]</td><td>1st-frame multi-view image</td><td>14.9</td><td>340.8</td></tr><tr><td>Drivingdiffusion [34]</td><td>1st-frame multi-view image†</td><td>15.8</td><td>332.0</td></tr><tr><td>Panacea [64]</td><td>1st-frame multi-view image†</td><td>16.9</td><td>139.0</td></tr><tr><td>DriveDreamer-2</td><td>1st-frame multi-view image</td><td>11.2</td><td>55.7</td></tr></table>

## 4.3 Quality Evaluation of Generated Videos

To verify the video generation quality, we compare DriveDreamer-2 with various driving video generation approaches on the nuScenes validation set. For a fair comparison, we conducted evaluations under three diferent experimental settings—without image condition, with video condition, and with first frame multi-view image condition. Additionally, Drive-WM [62], DrivingDifusion [34] and Panacea [64] adopt a two-stage pipeline, first generating visual conditions and then generating videos. The experimental results, as shown in Tab. 1, indicate that DriveDreamer-2 consistently achieves high-quality evaluation outcomes across all three settings. Specifically, in the absence of the image condition, DriveDreamer-2 attains an FID of 25.0 and an FVD of 105.1, showcasing a significant improvement over DriveDreamer [59]. Moreover, despite being limited to a single-view video condition, DriveDreamer-2 exhibits a 39% relative improvement in FVD compared to DriveWM [62], which utilizes a three-view video condition. Furthermore, when provided with the first-frame multi-view image condition, DriveDreamer-2 achieves an FID of 11.2 and an FVD of 55.7, surpassing all previous methods by a considerable margin.

Table 2: Comparison involving data augmentation using synthetic data on 3D object detection.
<table><tr><td>Image size</td><td>Initial frame</td><td>Real</td><td>Generated</td><td>mAP↑</td><td>mAOE↓</td><td>mAVE↓</td><td>NDS↑</td></tr><tr><td rowspan="3">256×448</td><td></td><td>√</td><td>一</td><td>31.7</td><td>67.9</td><td>33.0</td><td>43.5</td></tr><tr><td>√</td><td>√</td><td>√</td><td>32.6</td><td>61.7</td><td>29.7</td><td>45.2</td></tr><tr><td>1</td><td>√</td><td>√</td><td>32.9</td><td>61.5</td><td>30.4</td><td>45.4</td></tr></table>

Table 3: Comparison involving data augmentation using synthetic data on multiobject tracking.
<table><tr><td>Image size</td><td>Initial frame</td><td>Real</td><td>Generated</td><td></td><td>AMOTA↑</td><td>AMOTP↓</td><td>IDS↓</td></tr><tr><td rowspan="3"> $2 5 6 \times 4 4 8$ </td><td></td><td></td><td></td><td>一</td><td>28.9</td><td>1.419</td><td>687</td></tr><tr><td>√</td><td></td><td>√</td><td>√</td><td>31.2</td><td>1.396</td><td>542</td></tr><tr><td>一</td><td></td><td>√</td><td>√</td><td>31.3</td><td>1.387</td><td>593</td></tr></table>

To further validate the quality of the generated data, we employ the generated driving videos to enhance the training of 3D object detection and multi-object tracking. Specifically, we employ all structured conditions in the nuScenes training set to generate driving videos, which are combined with real videos to train StreamPETR [57] on downstream tasks. The experiment results are in Tab. 2 and Tab. 3. When the initial frame is used as a condition, the generated videos prove to be efective in enhancing the performance of downstream tasks. The 3D detection metrics, mAP and NDS, show a relative improvement of 2.8% and 3.9%, respectively. Besides, the tracking metrics, AMOTA and AMOTP, exhibit a relative enhancement of 8.0% and 1.6%. Furthermore, DriveDreamer-2 is capable of generating high-quality driving videos even in the absence of image conditions. Removing the image condition leads to increased diversity in the generated content, consequently further improving performance metrics for downstream tasks. Specifically, the mAP and NDS for 3D detection show a relative improvement of 3.8% and 4.4%, respectively, while the AMOTA and AMOTP for tracking tasks exhibit enhancements of 8.3% and 2.3%, compared to the baseline.

![](images/582dd2b18bcb8e95a0e1a8da8b1c14965855b2535fc9862a7752c5871a44cbb8.jpg)

![](images/51b2a0c2e2565e7d20780ed4b16d2397acc0eb5ebf5e41df3d6e4b10e9be1b6e.jpg)

![](images/17cc0bdfc7836772069e880b6b4725440435ba46980a6dde683b71146178b312.jpg)

![](images/edf4e95917ef78fbb4b9b12020ec149c4e385db7eaa08924ec9984dd2927ff46.jpg)  
Fig. 7: Visualization comparison between DriveDreamer-2 generation with and without UniMVM. The upper part depicts generation without UniMVM, while the lower part illustrates generation with UniMVM. It is evident that the inclusion of UniMVM results in higher multi-view consistency in the generated content.

![](images/481d0c5910bc31da61e2acdc287d725745eed7624776f7fd3b6af098203ca057.jpg)  
Fig. 8: Visualization comparison with diferent conditions. Under diferent image conditions, DriveDreamer-2 produces videos with a high level of multi-view consistency. Using the 1st frame image (row 1) as a condition, the diversity of the generated second frame (row 3) is constrained, which closely resembles the ground truth second frame (row 2). Employing the front-view video as a condition results in increased generation diversity (row 4), only the front-view image aligns closely with the ground truth (row 2). Strikingly, in the absence of image as a condition, DriveDreamer-2 produces the highest diversity (row 5). The generated colors of the cars and the street backgrounds difer significantly from the ground truth (row 2).

## 4.4 Ablation Study

We conduct an ablation study to investigate the efect of difusion backbone and the proposed UniMVM, and the results are in Tab. 4. Compared to SD1.4 [46] used in DriveDreamer, SVD [1] provides richer prior knowledge of videos, resulting in 17.2 FID and 94.6 FVD. The introduction of SVD results in an almost 70% improvement in FVD. Additionally, we also note that a slight decrease in FID, which we hypothesize is attributed to the introduction of the cross-view module, disrupting the SVD’s ability to learn spatial features. To fully unleash the potential of SVD in multi-view video generation, we propose UniMVM, which unifies constraints on intra- and cross-view, achieving remarkable FID and FVD scores of 11.2 and 55.7, respectively. These represent relative improvements of ∼30% and ∼80% compared to DriveDreamer. As depicted in Fig. 7, the upper row in each compared pair is generated by DriveDreamer-2 without UniMVM, while the lower row is generated by DriveDreamer-2 with UniMVM. In the absence of UniMVM, DriveDreamer-2 generates inconsistent results between views, including foreground vehicles and background structures. The introduction of UniMVM leads to significant improvements in generating multi-view videos, both in foreground and background aspects. The qualitative results demonstrate the impressive capability of our UniMVM in achieving multi-view consistency.

Table 4: The ablation study on the backbone and UniMVM. Cross-view module denotes the cross-view attention used in previous methods [34, 59, 62, 64].
<table><tr><td>Method</td><td>Backbone</td><td>Cross-view module</td><td>UniMVM</td><td>FID↓</td><td>FVD↓</td></tr><tr><td>DriveDreamer [59]</td><td>SD1.4</td><td>√</td><td>一</td><td>14.9</td><td>340.8</td></tr><tr><td>DriveDreamer-2</td><td>SVD</td><td>√</td><td>- √</td><td>17.2 11.2</td><td>94.6 55.7</td></tr></table>

Table 5: The ablation study on diferent conditions.
<table><tr><td>Method</td><td>Conditions</td><td>FID↓</td><td>FVD↓</td></tr><tr><td rowspan="2">DriveDreamer [59]</td><td>-</td><td>26.8</td><td>353.2</td></tr><tr><td>1st-frame multi-view image</td><td>14.9</td><td>340.8</td></tr><tr><td rowspan="3">DriveDreamer-2</td><td></td><td>25.0</td><td>105.1</td></tr><tr><td>1-view video</td><td>18.4</td><td>74.9</td></tr><tr><td>1-st frame multi-view image</td><td>11.2</td><td>55.7</td></tr></table>

Moreover, we explore the influence of various conditions on driving video generation, as shown in Tab. 5 and Fig. 8. The first row in Fig. 8 illustrates the ground truth (GT) of the first frame, representing the style of the GT video. Meanwhile, the second row displays the GT of the second frame, representing the GT of the generated multi-view frame. DriveDreamer-2 with the initial frame can generate results that are highly similar to the GT video, achieving optimal results in terms of FID and FVD, with scores of 11.2 and 55.7, respectively. The video generated by DriveDreamer-2 with the front-view video retains some aspects of the GT scene while also introducing some diversity, resulting in 17.2 FID and 94.6 FVD. DriveDreamer-2 can also generate extremely competitive results even without any image conditioning, achieving FID and FVD scores of 25.0 and 105.1, respectively. Notably, DriveDreamer-2 exhibits the highest diversity in this setting, where the generated appearance of cars and the street backgrounds difer significantly from the ground truth.

## 5 Discussion and Conclusion

This paper introduces DriveDreamer-2, an innovative extension of the Drive-Dreamer framework that pioneers the generation of user-customized driving videos. Leveraging a Large Language Model, DriveDreamer-2 first transfers user queries into foreground agent trajectories. Then the background trafic conditions can be generated using the proposed HDMap generator, with agent trajectories as conditions. The generated structured conditions can be utilized for video generation, and we propose UniMVM to enhance temporal and spatial coherence. We conduct extensive experiments to verify that DriveDreamer-2 can generate uncommon driving videos, such as abrupt vehicle maneuvers. Importantly, experimental results showcase the utility of the generated videos in enhancing the training of driving perception methods. Furthermore, DriveDreamer-2 demonstrates superior video generation quality compared to state-of-the-art methods, achieving FID and FVD scores of 11.2 and 55.7, respectively. These scores represent remarkable relative improvements of approximately 30% and 50%, afirming the eficacy and advancement of DriveDreamer-2 in multi-view driving video generation.

## References

1. Blattmann, A., Dockhorn, T., Kulal, S., Mendelevitch, D., Kilian, M., Lorenz, D., Levi, Y., English, Z., Voleti, V., Letts, A., et al.: Stable video difusion: Scaling latent video difusion models to large datasets. arXiv preprint arXiv:2311.15127 (2023) 4, 10, 13

2. Caesar, H., Bankiti, V., Lang, A.H., Vora, S., Liong, V.E., Xu, Q., Krishnan, A., Pan, Y., Baldan, G., Beijbom, O.: nuscenes: A multimodal dataset for autonomous driving. CVPR (2019) 9, 23

3. Chen, L., Wu, P., Chitta, K., Jaeger, B., Geiger, A., Li, H.: End-to-end autonomous driving: Challenges and frontiers. arXiv preprint arXiv:2306.16927 (2023) 4

4. Denton, E., Fergus, R.: Stochastic video generation with a learned prior. In: ICML (2018) 4

5. Dhariwal, P., Nichol, A.: Difusion models beat gans on image synthesis. NeurIPS (2021) 2, 4, 21

6. Feng, L., Li, Q., Peng, Z., Tan, S., Zhou, B.: Traficgen: Learning to generate diverse and realistic trafic scenarios. In: ICRA (2023) 4

7. Gao, R., Chen, K., Xie, E., Hong, L., Li, Z., Yeung, D.Y., Xu, Q.: Magicdrive: Street view generation with diverse 3d geometry control. arXiv preprint arXiv:2310.02601 (2023) 2

8. Gao, Z., Mu, Y., Shen, R., Chen, C., Ren, Y., Chen, J., Li, S.E., Luo, P., Lu, Y.: Enhance sample eficiency and robustness of end-to-end urban autonomous driving via semantic masked world model. arXiv preprint arXiv:2210.04017 (2022) 2

9. Ha, D., Schmidhuber, J.: Recurrent world models facilitate policy evolution. NeurIPS (2018) 4

10. Hafner, D., Lee, K.H., Fischer, I., Abbeel, P.: Deep hierarchical planning from pixels. NeurIPS (2022) 4

11. Hafner, D., Lillicrap, T., Ba, J., Norouzi, M.: Dream to control: Learning behaviors by latent imagination. arXiv preprint arXiv:1912.01603 (2019) 4

12. Hafner, D., Lillicrap, T., Norouzi, M., Ba, J.: Mastering atari with discrete world models. arXiv preprint arXiv:2010.02193 (2020) 4

13. Hafner, D., Pasukonis, J., Ba, J., Lillicrap, T.: Mastering diverse domains through world models. arXiv preprint arXiv:2301.04104 (2023) 4

14. Harvey, W., Naderiparizi, S., Masrani, V., Weilbach, C., Wood, F.: Flexible difusion modeling of long videos. NeurIPS (2022) 4

15. He, K., Zhang, X., Ren, S., Sun, J.: Deep residual learning for image recognition. In: CVPR (2016) 10

16. Ho, J., Chan, W., Saharia, C., Whang, J., Gao, R., Gritsenko, A., Kingma, D.P., Poole, B., Norouzi, M., Fleet, D.J., et al.: Imagen video: High definition video generation with difusion models. arXiv preprint arXiv:2210.02303 (2022) 4

17. Ho, J., Jain, A., Abbeel, P.: Denoising difusion probabilistic models. NeurIPS (2020) 2, 4, 21

18. Ho, J., Saharia, C., Chan, W., Fleet, D.J., Norouzi, M., Salimans, T.: Cascaded difusion models for high fidelity image generation. JMLR (2022) 2, 4, 21

19. Hochreiter, S., Schmidhuber, J.: Long short-term memory. Neural computation (1997) 4

20. Hong, W., Ding, M., Zheng, W., Liu, X., Tang, J.: Cogvideo: Large-scale pretraining for text-to-video generation via transformers. arXiv preprint arXiv:2205.15868 (2022) 4

21. Hsieh, J.T., Liu, B., Huang, D.A., Fei-Fei, L.F., Niebles, J.C.: Learning to decompose and disentangle representations for video prediction. NeurIPS (2018) 4

22. Hu, A., Corrado, G., Grifiths, N., Murez, Z., Gurau, C., Yeo, H., Kendall, A., Cipolla, R., Shotton, J.: Model-based imitation learning for urban driving. NeurIPS (2022) 2, 4

23. Hu, A., Russell, L., Yeo, H., Murez, Z., Fedoseev, G., Kendall, A., Shotton, J., Corrado, G.: Gaia-1: A generative world model for autonomous driving. arXiv preprint arXiv:2309.17080 (2023) 2, 4

24. Hyvärinen, A., Dayan, P.: Estimation of non-normalized statistical models by score matching. JMLR (2005) 22

25. Jia, F., Mao, W., Liu, Y., Zhao, Y., Wen, Y., Zhang, C., Zhang, X., Wang, T.: Adriver-i: A general world model for autonomous driving. arXiv preprint arXiv:2311.13549 (2023) 2, 4

26. Kalchbrenner, N., Oord, A., Simonyan, K., Danihelka, I., Vinyals, O., Graves, A., Kavukcuoglu, K.: Video pixel networks. In: ICML (2017) 4

27. Karras, T., Aittala, M., Aila, T., Laine, S.: Elucidating the design space of difusionbased generative models. NeurIPS (2022) 9, 22

28. Khachatryan, L., Movsisyan, A., Tadevosyan, V., Henschel, R., Wang, Z., Navasardyan, S., Shi, H.: Text2video-zero: Text-to-image difusion models are zeroshot video generators. arXiv preprint arXiv:2303.13439 (2023) 4

29. Kim, S.W., Zhou, Y., Philion, J., Torralba, A., Fidler, S.: Learning to simulate dynamic environments with gamegan. In: CVPR (2020) 4

30. Kingma, D.P., Ba, J.: Adam: A method for stochastic optimization. arXiv preprint arXiv:1412.6980 (2014) 10

31. Kingma, D.P., Welling, M.: Auto-encoding variational bayes. arXiv preprint arXiv:1312.6114 (2013) 4

32. Kondratyuk, D., Yu, L., Gu, X., Lezama, J., Huang, J., Hornung, R., Adam, H., Akbari, H., Alon, Y., Birodkar, V., et al.: Videopoet: A large language model for zero-shot video generation. arXiv preprint arXiv:2312.14125 (2023) 4

33. Kumar, M., Babaeizadeh, M., Erhan, D., Finn, C., Levine, S., Dinh, L., Kingma, D.: Videoflow: A flow-based generative model for video. arXiv preprint arXiv:1903.01434 (2019) 4

34. Li, X., Zhang, Y., Ye, X.: Drivingdifusion: Layout-guided multi-view driving scene video generation with latent difusion model. arXiv preprint arXiv:2310.07771 (2023) 8, 11, 14

35. Li, Y., Liu, H., Wu, Q., Mu, F., Yang, J., Gao, J., Li, C., Lee, Y.J.: Gligen: Open-set grounded text-to-image generation. In: CVPR (2023) 7

36. Lin, J., Du, Y., Watkins, O., Hafner, D., Abbeel, P., Klein, D., Dragan, A.: Learning to model the world with language. arXiv preprint arXiv:2308.01399 (2023) 4

37. Mao, J., Qian, Y., Zhao, H., Wang, Y.: Gpt-driver: Learning to drive with gpt. arXiv preprint arXiv:2310.01415 (2023) 6

38. Mathieu, M., Couprie, C., LeCun, Y.: Deep multi-scale video prediction beyond mean square error. arXiv preprint arXiv:1511.05440 (2015) 4

39. Nichol, A., Dhariwal, P., Ramesh, A., Shyam, P., Mishkin, P., McGrew, B., Sutskever, I., Chen, M.: Glide: Towards photorealistic image generation and edit-

ing with text-guided difusion models. arXiv preprint arXiv:2112.10741 (2021) 2, 4

40. Nichol, A.Q., Dhariwal, P.: Improved denoising difusion probabilistic models. In: ICML (2021) 2, 4

41. OpenAI, R.: Gpt-4 technical report. arxiv 2303.08774. View in Article (2023) 5

42. Pan, M., Zhu, X., Wang, Y., Yang, X.: Iso-dream: Isolating and leveraging noncontrollable visual dynamics in world models. NeurIPS (2022) 4

43. Parmar, G., Zhang, R., Zhu, J.Y.: On aliased resizing and surprising subtleties in gan evaluation. In: CVPR (2022) 10

44. Poole, B., Jain, A., Barron, J.T., Mildenhall, B.: Dreamfusion: Text-to-3d using 2d difusion. arXiv preprint arXiv:2209.14988 (2022) 21

45. Ranzato, M., Szlam, A., Bruna, J., Mathieu, M., Collobert, R., Chopra, S.: Video (language) modeling: a baseline for generative models of natural videos. arXiv preprint arXiv:1412.6604 (2014) 4

46. Rombach, R., Blattmann, A., Lorenz, D., Esser, P., Ommer, B.: High-resolution image synthesis with latent difusion models. In: CVPR (2022) 2, 4, 10, 13

47. Saito, M., Matsumoto, E., Saito, S.: Temporal generative adversarial nets with singular value clipping. In: ICCV (2017) 4

48. Seo, Y., Hafner, D., Liu, H., Liu, F., James, S., Lee, K., Abbeel, P.: Masked world models for visual control. In: CoRL (2023) 4

49. Singer, U., Polyak, A., Hayes, T., Yin, X., An, J., Zhang, S., Hu, Q., Yang, H., Ashual, O., Gafni, O., et al.: Make-a-video: Text-to-video generation without textvideo data. arXiv preprint arXiv:2209.14792 (2022) 4

50. Song, Y., Sohl-Dickstein, J., Kingma, D.P., Kumar, A., Ermon, S., Poole, B.: Scorebased generative modeling through stochastic diferential equations. arXiv preprint arXiv:2011.13456 (2020) 21

51. Srivastava, N., Mansimov, E., Salakhudinov, R.: Unsupervised learning of video representations using lstms. In: ICML (2015) 4

52. Tan, S., Ivanovic, B., Weng, X., Pavone, M., Kraehenbuehl, P.: Language conditioned trafic generation. arXiv preprint arXiv:2307.07947 (2023) 4

53. Tulyakov, S., Liu, M.Y., Yang, X., Kautz, J.: Mocogan: Decomposing motion and content for video generation. In: CVPR (2018) 4

54. Unterthiner, T., Van Steenkiste, S., Kurach, K., Marinier, R., Michalski, M., Gelly, S.: Towards accurate generative models of video: A new metric & challenges. arXiv preprint arXiv:1812.01717 (2018) 10

55. Villegas, R., Babaeizadeh, M., Kindermans, P.J., Moraldo, H., Zhang, H., Safar, M.T., Castro, S., Kunze, J., Erhan, D.: Phenaki: Variable length video generation from open domain textual description. ICLR (2023) 4

56. Vondrick, C., Pirsiavash, H., Torralba, A.: Generating videos with scene dynamics. NeurIPS (2016) 4

57. Wang, S., Liu, Y., Wang, T., Li, Y., Zhang, X.: Exploring object-centric temporal modeling for eficient multi-view 3d object detection. arXiv preprint arXiv:2303.11926 (2023) 10, 12, 22

58. Wang, X., Yuan, H., Zhang, S., Chen, D., Wang, J., Zhang, Y., Shen, Y., Zhao, D., Zhou, J.: Videocomposer: Compositional video synthesis with motion controllability. arXiv preprint arXiv:2306.02018 (2023) 4

59. Wang, X., Zhu, Z., Huang, G., Chen, X., Lu, J.: Drivedreamer: Towards real-worlddriven world models for autonomous driving. arXiv preprint arXiv:2309.09777 (2023) 2, 3, 4, 5, 8, 9, 11, 14

60. Wang, X., Zhu, Z., Huang, G., Wang, B., Chen, X., Lu, J.: Worlddreamer: Towards general world models for video generation via predicting masked tokens. arXiv preprint arXiv:2401.09985 (2024) 4

61. Wang, X., Zhu, Z., Zhang, Y., Huang, G., Ye, Y., Xu, W., Chen, Z., Wang, X.: Are we ready for vision-centric driving streaming perception? the asap benchmark. In: CVPR (2023) 9

62. Wang, Y., He, J., Fan, L., Li, H., Chen, Y., Zhang, Z.: Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving. arXiv preprint arXiv:2311.17918 (2023) 2, 4, 8, 9, 11, 14

63. Weissenborn, D., Täckström, O., Uszkoreit, J.: Scaling autoregressive video models. arXiv preprint arXiv:1906.02634 (2019) 4

64. Wen, Y., Zhao, Y., Liu, Y., Jia, F., Wang, Y., Luo, C., Zhang, C., Wang, T., Sun, X., Zhang, X.: Panacea: Panoramic and controllable video generation for autonomous driving. arXiv preprint arXiv:2311.16813 (2023) 2, 8, 11, 14

65. Wu, P., Escontrela, A., Hafner, D., Abbeel, P., Goldberg, K.: Daydreamer: World models for physical robot learning. In: CoRL (2023) 4

66. Yang, K., Ma, E., Peng, J., Guo, Q., Lin, D., Yu, K.: Bevcontrol: Accurately controlling street-view elements with multi-perspective consistency via bev sketch layout. arXiv preprint arXiv:2308.01661 (2023) 8

67. Yang, R., Srivastava, P., Mandt, S.: Difusion probabilistic modeling for video generation. arXiv preprint arXiv:2203.09481 (2022) 4

68. Zhang, L., Rao, A., Agrawala, M.: Adding conditional control to text-to-image difusion models. In: ICCV (2023) 7, 10

69. Zhong, Z., Rempe, D., Chen, Y., Ivanovic, B., Cao, Y., Xu, D., Pavone, M., Ray, B.: Language-guided trafic simulation via scene-level difusion. arXiv preprint arXiv:2306.06344 (2023) 5, 6

70. Zhong, Z., Rempe, D., Xu, D., Chen, Y., Veer, S., Che, T., Ray, B., Pavone, M.: Guided conditional difusion for controllable trafic simulation. In: ICRA (2023) 5, 6

In the supplementary material, we begin by detailing the implementation of customized trafic simulation and the Unified Mulit-view Video Model (UniMVM). This is followed by an overview of the training specifics for downstream tasks and evaluation details. Additionally, a collection of visualization results is provided for further analysis.

## 6 Implement Details

Function Library Below is an example of a cut in trajectory generation function. Firstly, we initialize a starting point coordinate, and then during the generation of the cut in trajectory, we check the distance between the agent and other agents to control direction and avoid collisions. To enhance the diversity of generated trajectories, we introduce random disturbances to the agent’s speed and orientation, aiming to approximate real-world scenarios as closely as possible. Moreover, this function library can be further expanded to meet users’ demands for generating scenes. More details about the function library can be found in the code that we will release later.

```python
def cut_in ( obj_trajs =None , obj_vels =None ,
safe_dis =10 , is_ego = False ):
Generate a trajectory for a agent cutting in.
Parameters :
Returns :
obj_trajs : the cutting in trajectory of the agent .
obj_vels : the velocities of the agent .
agent_trajs = np. zeros ((1, NUM_POINT ,3))
agent_vels = np. zeros ((1, NUM_POINT ,1))
#initialize the start point
if not is_ego :
xy0 = np. random . rand (2)
xy0 [0] = utils . get_random_value (xy0 [0],[0,10])
multi_factor = 1 if random . random ()>0.5 else -1
xy0 [1] = utils . get_random_value (xy0 [1],Y_RANGE )\
*multi_factor
y_margin = xy0[1]* multi_factor
agent_trajs [0,0,:2] = xy0
target_y = 0
else:
y_margin = abs( obj_trajs [0,0,1])
target_y = obj_trajs [0,0,1]
vel = utils . get_random_value (np. random . rand () ,V_RANGE )
agent_vels [0,0] = vel
yaw = utils . get_random_value (np. random . rand () ,
FORWARD RANGE)
vel_x = vel*np.cos(yaw )
```

vel\_y = vel\*np.sin(yaw )   
flag = True   
# generate the cut in trajectory   
for t in range (1, NUM\_POINT ):   
agent\_trajs [0,t,0] = agent\_trajs [0,t-1,0]\   
+ vel\_x \* T\_INTER   
agent\_trajs [0,t,1] = agent\_trajs [0,t-1,1]\   
+ vel\_y \* T\_INTER   
#check whether the agent reaches the front of the   
#target vehicle   
if ( agent\_trajs [0,t-1,1]- y\_margin )\*\   
( agent\_trajs [0,t,1]- y\_margin )<=0:   
flag = False   
# approach the target vehicle   
if abs( agent\_trajs [0,t,1]- target\_y )\   
> y\_margin /2 and flag :   
aw\_ran e = [-0.1,0] if multi\_factor ==1 \   
else [0,0.1]   
yaw\_max = 0 if multi\_factor ==1 else 20\*np.pi/180   
yaw\_min = -20\*np.pi/180 if multi\_factor ==1 else 0   
# gradually return to the forward direction .   
elif abs ( agent\_trajs [0 ,t , 1]- target\_y ) \   
>0.5 and flag :   
yaw\_range = [0,0.1] if multi\_factor ==1\   
else [-0.1,0]   
yaw\_max = -10\*np.pi/180 if multi\_factor ==1\   
else 20\*np.pi/180   
yaw\_min = -20\*np.pi/180 if multi\_factor ==1\   
else 10\*np.pi/180   
# move forward   
else :   
yaw\_range = [-0.3\*np.pi/180 ,0] if yaw>=0 \   
else [0,0.3\*np.pi/180]   
yaw\_max = 1\*np.pi/180   
yaw\_min = -1\*np.pi/180   
# finetune the direction to avoid collision   
if ob \_tra s is not None :   
yaw\_range = utils . update\_yaw (yaw , safe\_dis ,   
agent\_trajs ,   
obj\_trajs )   
yaw += utils . get\_random\_value (np. random . rand () ,   
yaw\_range )   
yaw = np. clip (yaw , yaw\_min , yaw\_max )   
vel += utils . get\_random\_value (np. random . rand () ,[-2,2]   
)   
# guarentee the generated velocity surpasses the   
# other vehicle to relize cutting in   
if obj\_vels is not None :   
v\_range = [ obj\_vels [0,t,0]+0.5, V\_RANGE [1]+0.5]   
else :

```python
v_range = V_RANGE
vel = np. clip (vel , v_range [0],v_range [1])
agent_vels [0,t] = vel
vel_x = vel*np.cos(yaw )
vel_y = vel*np.sin(yaw )
return agent_trajs , agent_vels
```

Prompt Template Fig. 9 depicts the general prompt template designed for finetuning LLM. It includes encapsulated trajectory generation functions, and instruction. During usage, the user prompt integrates into the instruction, directly guiding the finetuned LLM to generate the corresponding Python script.

![](images/90ef865e4fcd514a6628ae35c8a62714f5d0da88d4181bc59fee2a4117284271.jpg)  
Fig. 9: Our prompt template designed for finetuning LLM. It contains information about functions, and instruction. The user query is inserted into the placeholder {USER QUERY}.

BEV HDMap Post-Process Since the generated HDMap is in the BEV perspective, it cannot be directly applied to UniMVM for video generation. Hence, we need post-processing to project the BEV HDMap onto the image coordinate system. Firstly, binarization and skeleton extraction algorithms are employed to extract diferent types of lane markings (as depicted in Fig. 4 (in the main text), red for lane boundaries, blue for lane dividers, and green for pedestrian crossings). Then, the extracted lane markings are transformed into pixel coordinates to serve as the condition for UniMVM.

Training UniMVM We assume the data distribution is $p _ { d a t a } ( y _ { \mathbb { Z } } )$ , where y<sub>I</sub> denotes the image latents, and let $p ( y ; \sigma )$ be the distribution obtained by adding i.i.d. $\sigma ^ { 2 } .$ -variance Gaussian noise to the data. Note that or suficiently large $\sigma _ { m a x } ,$ $p ( y ; \sigma _ { m a x ^ { 2 } } ) \approx \mathcal { N } ( 0 , \sigma _ { m a x ^ { 2 } } )$ . Difusion models (DM) [5, 17, 18, 44] use this fact and, starting from high variance Gaussian noise $y _ { M } \sim \mathcal { N } ( 0 , \sigma _ { m a x ^ { 2 } } )$ , sequentially denoise towards $\sigma _ { 0 } = 0$ . In practice, this iterative refinement process can be implemented through the numerical simulation of the Probability Flow ordinary diferential equation (ODE) [50]

$$
d x = - \dot { \sigma } ( t ) \sigma ( t ) \nabla _ { y } \log p ( y ; \sigma ( t ) ) d t ,\tag{4}
$$

![](images/df58e87c8b8eff3245a84464fecd4afa917389a6bf810a306e30e1166a407982.jpg)

Fig. 10: Visualization of the generated multi-view video. Regions highlighted by yellow <sub>rectangles indicate that DriveDreamer-2 exhibits strong temporal consistency.</sub>Frame  
![](images/6095914fabc1d0c06f46e2500d3202e603ecb29733fa085508622acdb8cd9658.jpg)  
Fig. 11: A generated video of a rainy day scene. The movement of the windshield wipers (highlighted by yellow rectangles) demonstrates that as DriveDreamer-2 possesses a high level of scene understanding.

where $\nabla _ { y }$ log $p ( y ; \sigma )$ is the score function [24]. DM training reduces to learning a model $s _ { \theta } ( x ; \sigma )$ for the score function $\nabla _ { x } \log p ( y ; \sigma )$ . The model can, for example, be parameterized as $\nabla _ { x } \log p ( y ; \sigma ) \approx s _ { \theta } ( y ; \sigma ) = ( D _ { \theta } ( y ; \sigma ) - y ) / \sigma ^ { 2 } ~ [ 2 7 ]$ , where $D _ { \theta }$ is a learnable denoiser that tries to predict the clean $y _ { \mathcal { T } }$ . The denoiser $D _ { \theta }$ is trained via denoising score matching (DSM)

$$
\mathbb { E } _ { ( y _ { \mathcal { T } } , c ) \sim p _ { d a t a } ( y _ { \mathcal { T } } , c ) , ( \sigma , n ) \sim p ( \sigma , n ) } \left[ \lambda _ { \sigma } \| D _ { \theta } ( y _ { \mathcal { T } } + n ; \sigma , c ) - y _ { \mathcal { T } } \| _ { 2 } ^ { 2 } \right] ,\tag{5}
$$

where $p ( \sigma , n ) = p ( \sigma ) \mathcal { N } ( n ; 0 , \sigma ^ { 2 } ) , p ( \sigma )$ can be a probability distribution or density over noise levels σ. $\lambda _ { \sigma } = ( 1 + \sigma ^ { 2 } ) \sigma ^ { - 2 } $ is a weighting function, and c is the conditional signal, which including the HDMap features $y _ { \mathcal { H } }$ , box conditions y<sub>B</sub> and text prompt embeddings $c _ { p }$ . In this work, we follow the EDM preconditioning framework [27], parameterizing the learnable denoiser $D _ { \theta }$ as

$$
D _ { \theta } ( y ; \sigma ) = c _ { s k i p } ( \sigma ) y + c _ { o u t } ( \sigma ) F _ { \theta } ( c _ { i n } ( \sigma ) y ; c _ { n o i s e } ( \sigma ) ) ,\tag{6}
$$

where $F _ { \theta }$ is the network to be trained, and $c _ { s k i p } ( \sigma ) = 1 / ( \sigma ^ { 2 } + 1 ) , c _ { o u t } ( \sigma ) =$ $- \sigma / \sqrt { \sigma ^ { 2 } + 1 } , c _ { i n } ( \sigma ) = 1 / \sqrt { \sigma ^ { 2 } + 1 } , c _ { n o i s e } ( \sigma ) = 0 . 2 5 \log \sigma$

Training Downstream Tasks StreamPETR is retrained at a resolution of $5 1 2 \times 2 5 6$ instead of the $7 0 4 \times 2 5 6$ in original baseline [57]. The augmented training data is generated by utilizing the structured information from the training set.

![](images/9a45ef1b50ed089ec0ed93671924cd755093e329072d425f87ec2a262b28be8a.jpg)  
Fig. 12: A long video generated by the prompt a person crosses the road on a rainy day. Regions highlighted by yellow rectangles indicate the movement of the pedestrian.

Evaluation Details The FID and FVD calculations are performed on 150 validation videos from the nuScenes dataset [2]. A setting with a frame rate of 4Hz and 8 frames per clip is employed to generate data for evaluating FID and FVD. And we use the oficial UCF FVD evaluation code<sup>2</sup>.

## 7 Visualization

![](images/92d5e8b49315421c43a55518a591f9e23e0d33ae4ffd686f48bd18b210195da0.jpg)  
Fig. 13: A long video generated by the prompt the ego car changes lane during the daytime.

As shown in Fig. 10, DriveDreamer-2 demonstrates strong consistency across views and frames, allowing even the completely occluded car to reappear in subsequent frames (as highlighted by yellow rectangles). The more details can be seen in videos/occluded\_car.mp4. Fig. 11 depicts a rainy scene video generated by DriveDreamer-2 (see videos/windshield\_wiper.mp4 for more details). As illustrated in Fig. 11, the windshield wipers of the truck are continuously clearing the windshield. This showcases the powerful scene understanding capabilities of our DriveDreamer-2. It can not only manipulate macroscopic weather conditions but also adjust the behaviors of generated agents within the scene according to the weather.

![](images/b1007b3db736ba85241405f3118877dab217af7ebdd4b55cbe6810218c5c930a.jpg)  
Fig. 14: A long video generated by the prompt on a rainy day, a car cuts in.

Regarding the generation of long videos, we can utilize DriveDreamer-2 without any image conditioning to first generate a clip. Subsequently, the last frame of this clip is employed as the initial image condition to generate subsequent clips. Below, we showcase the results of directly using text prompts to generate a 29-frame multi-view video. Fig. 12 is a long video generated by the prompt a person crosses the road on a rainy day. (see videos/cross\_road.mp4 for more details). It depicts a pedestrian crosses the road in front of the ego vehicle on a rainy day. Fig. 13 is generated by a prompt the ego car changes lane during the daytime. (see videos/change\_lane.mp4 for more details). It showcases the ego car changes lanes to the right side during the daytime. As shown in Fig. 14, a vehicle cuts in from the left to the front of the ego car (prompted by on a rainy day, a car cuts in and see more details in videos/cut\_in.mp4).