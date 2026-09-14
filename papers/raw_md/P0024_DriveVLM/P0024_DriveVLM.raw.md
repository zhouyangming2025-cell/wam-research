# DRIVEVLM: The Convergence of Autonomous Driving and Large Vision-Language Models

Xiaoyu Tian1\* Junru Gu1\* Bailin Li2\* Yicheng Liu1\* Yang Wang2 Zhiyong Zhao2 Kun Zhan2 Peng Jia2 Xianpeng Lang2 Hang Zhao¹† 1IIIS, Tsinghua University 2Li Auto

Abstract: A primary hurdle of autonomous driving in urban environments is understanding complex and long-tail scenarios, such as challenging road conditions and delicate human behaviors. We introduce DriveVLM, an autonomous driving system leveraging Vision-Language Models (VLMs) for enhanced scene understanding and planning capabilities. DriveVLM integrates a unique combination of reasoning modules for scene description, scene analysis, and hierarchical planning. Furthermore, recognizing the limitations of VLMs in spatial reasoning and heavy computational requirements, we propose DriveVLM-Dual, a hybrid system that synergizes the strengths of DriveVLM with the traditional autonomous driving pipeline. Experiments on both the nuScenes dataset and our SUP-AD dataset demonstrate the efficacy of DriveVLM and DriveVLM-Dual in handling complex and unpredictable driving conditions. Finally, we deploy the DriveVLM-Dual on a production vehicle, verifying it is effective in real-world autonomous driving environments.

Keywords: Autonomous Driving, Vision Language Model, Dual System

## 1 Introduction

Autonomous driving, with its great promise to revolutionize transportation, has been an active research area over the past two decades. A primary hurdle to a fully autonomous driving system is scene understanding [1], which involves navigating complex, unpredictable scenarios such as adverse weather, intricate road layouts, and unforeseen human behaviors.

Existing autonomous driving systems, typically comprising 3D perception, motion prediction, and planning, struggle with these scene understanding challenges. Specifically, 3D perception [2, 3, 4, 5] is limited to detecting and tracking familiar objects, omitting rare objects and their unique attributes; motion prediction [6, 7, 8, 9, 10] and planning [11, 12, 13] focus on trajectory-level actions, often neglecting the decision-level interactions between objects and vehicles.

We introduce DriveVLM, a novel autonomous driving system that aims at these scene understanding challenges, capitalizing on the recent Vision-Language Models (VLMs) [14, 15, 16, 17] which have demonstrated exceptional prowess in visual comprehension and reasoning. Specifically, DriveVLM contains a Chain-of-Though (CoT) process with three key modules: scene description, scene analysis, and hierarchical planning. The scene description module linguistically depicts the driving environment and identifies critical objects in the scene; the scene analysis module delves into the characteristics of the critical objects and their influence on the ego vehicle; the hierarchical planning module formulates plans step-by-step, from meta-actions and decision descriptions to waypoints. These modules respectively correspond to the components of the traditional perception-predictionplanning pipeline, but the difference is that these modules tackle object perception, intention-level prediction and task-level planning, which were extremely challenging to cope with in the past.

While VLMs excel in visual understanding, they have limitations in spatial grounding and reasoning, and their computational intensity poses challenges for onboard inference speed. Therefore we further propose DriveVLM-Dual, a hybrid system that combines the strengths of both DriveVLM and traditional systems. DriveVLM-Dual optionally integrates DriveVLM with traditional 3D perception and planning modules, such as 3D object detectors, occupancy networks, and motion planners, enabling the system to achieve 3D grounding and high-frequency planning abilities. This dual system design, akin to the human brain's slow and fast thinking processes, adapts efficiently to varying complexity in driving scenarios.

Meanwhile, we formally define the scene understanding and planning (SUP) task, and propose new evaluation metrics to assess the scene analysis and meta-action planning capabilities of DriveVLM and DriveVLM-Dual. We carry out a comprehensive data mining and annotation pipeline to construct an in-house SUP-AD dataset for the SUP task. Extensive experiments on both the nuScenes dataset and our own dataset demonstrate the superior performance of DriveVLM, particularly in fewshot scenarios. Furthermore, DriveVLM-Dual exceeds state-of-the-art end-to-end motion planning methods. We have also deployed the model on a production vehicle, confirming that DriveVLM-Dual is effective in real-world autonomous driving environments. Additionally, we have included a demo in the supplementary materials.

In summary, the contribution of this paper is three-fold:

1. We introduce DriveVLM, a novel autonomous driving system that leverages VLMs for effective scene understanding and planning. We further introduce DriveVLM-Dual, a hybrid system that incorporates DriveVLM and a traditional autonomous pipeline, which achieves improved spatial reasoning and real-time planning capabilities.

2. We present a comprehensive data mining and annotation pipeline to construct a scene understanding and planning dataset (SUP-AD), together with metrics for evaluation.

3. We have successfully deployed DriveVLM-Dual system in a production vehicle and test various effective strategies for accelerating VLM deployment in real driving scenarios.

## 2 Related Works

Vision-Language Models (VLMs). Recently, there has been a surge in research on large Vision-Language Models (VLMs), exemplified by works such as MiniGPT-4 [16], LLaVA [17], Qwen-VL [18], and others [19, 14, 20, 21]. VLMs can be used in various scenarios, especially robotics [22, 23, 24, 25, 26], where VLMs output corresponding actions that can be high-level instructions [22] or low-level robot actions [24]. DriveVLM focuses on utilizing VLMs to assist in autonomous driving, thereby establishing a novel framework. A Concurrent work [15] shares a similar motivation.

Learning-based Planning. The integration of learning frameworks into motion planning has been an active area of research since Pomerleau [11] pioneering contributions. One promising line of work is Reinforcement learning and imitation learning [27, 28, 29]. These methods can learn an end-to-end planning policy that directly maps raw sensory inputs to control actions [29]. Several works [30, 31, 32, 33] improve interpretability by explicitly building dense cost maps derived from learning-based modules. A recent trend involves training multiple blocks in an end-to-end fashion [32, 33, 34, 35]. These methods enhance overall performance, but rely on backpropagation from future trajectory predictions loss in a less interpretable decision-making process [36].

Driving Caption Datasets. Recent works [37, 15, 38] argue that language captions are an important medium to connect human knowledge with the driving objective, helping to inform decisions and actions. Refer-KITTI [39] annotates objects in the KITTI dataset [40] with language prompts that can reference a collection of objects. Talk2Car [41], NuPrompt [42] and nuScenes-QA [43] introduce free-form captions and QA annotation to the nuScenes dataset [44]. BDD-X [45] and BDD-OIA [46] offer datasets with language explanations for the ego vehicle's actions or traffic scenarios [47] [48]. These datasets offer scenes for natural language use, but lack sufficient data on critical safety scenarios in self-driving systems.

![](images/bf3ac5d9c2ea8377eef32adb9bc0dbdb9f8efc64ed356f5662f3c7a20dbb0775.jpg)  
Figure 1: DriveVLM and DriveVLM-Dual model pipelines. DriveVLM takes images as input and, through a Chain-of-Thought (CoT) mechanism, outputs scene description, scene analysis, and hierarchical planning results. DriveVLM-Dual further incorporates traditional 3D perception and trajectory planning modules to achieve spatial reasoning capability and real-time trajectory planning.

## 3 DriveVLM

## 3.1 Overview

The overall pipeline of DriveVLM is illustrated in Figure 1. A sequence of images is processed by a Vision Language Model (VLM) to perform a special chain-of-thought (CoT) [49] reasoning to derive the driving planning results. The architecture of DriveVLM involves a vision transformer encoder [50] and a Large Language Model (LLM). The vision encoder produces image tokens; then an attention-based extractor aligns these tokens with the LLM. The reasoning process can be divided into three modules: scene description (Section 3.2), scene analysis (Section 3.3), and hierarchical planning (Section 3.4).

For real-world deployment, we propose a hybrid system, DriveVLM-Dual, in Section 3.5, which combines DriveVLM and the traditional autonomous driving pipeline, leveraging the strengths of both approaches.

## 3.2 Scene Description

The scene description module identifies driving environment description and critical objects.

Environment Description. Driving environments, such as weather and road conditions, have a non-negligible impact on driving difficulty. Therefore, the model is first prompted to output a linguistic description E of the driving environment, including several conditions: $E =$ $\{ E _ { \mathrm { w e a t h e r } } , E _ { \mathrm { t i m e } } , E _ { \mathrm { r o a d } } , E _ { \mathrm { l a n e } } \}$ , each representing a crucial aspect of the driving environment. The weather component, $E _ { \mathrm { w e a t h e r } } ,$ spans conditions from sunny to snowy, affecting visibility and traction. The time component, $E _ { \mathrm { t i m e } }$ , distinguishes between daytime and nighttime, impacting driving strategies due to visibility changes. Road types, $E _ { \mathrm { r o a d } } .$ such as urban or highway, introduce different challenges, while lane conditions, $E _ { \mathrm { l a n e } }$ , focus on current lane positioning and possible maneuvers, crucial for safe driving decisions.

Critical Object Identification. In addition to environmental conditions, various objects in driving scenarios significantly influence driving behaviors. Unlike traditional autonomous driving perception modules, which detect all objects within a specific range, we solely focus on identifying critical objects that are most likely to influence the current scenario, inspired by human cognitive processes during driving. Each critical object, denoted as $O _ { c } ,$ contains two attributes: the object category c and its approximate bounding box coordinates $b ( x 1 , y 1 , x 2 , y 2 )$ on the image. The category and coordinates are mapped to their corresponding language token\_id in the language modality, enabling seamless integration into the following modules. Moreover, taking advantage of the pre-trained vision encoder, DriveVLM can identify long-tail critical objects that may elude typical 3D object detectors, such as road debris or unusual animals.

## 3.3 Scene Analysis

In the traditional autonomous driving pipeline, the prediction module typically concentrates on forecasting the future trajectories of objects. The emergence of advanced vision-language models has provided us with the ability to perform a more comprehensive analysis of the current scene. The scene-level analysis summarizes all the critical objects together with the environmental description. This summary gives a comprehensive understanding of the scene, and is fed into the following planning module.

Critical Object Analysis. DriveVLM characterizes critical objects in three aspects: static attributes $C _ { s } ,$ motion states $C _ { m }$ , and particular behaviors $C _ { b } .$ Static attributes $C _ { s }$ describe inherent properties of objects, such as a roadside billboard's visual cues or a truck's oversized cargo, which are critical in preempting and navigating potential hazards. Motion states $C _ { m }$ describe an object's dynamics over a period, including position, direction, and action—characteristics that are vital in predicting the object's future trajectory and potential interactions with the ego vehicle. Particular behaviors $C _ { b }$ refer to special actions or gestures of an object that could directly influence the ego vehicle's next driving decisions. We do not require the model to analyze all three characteristics for all objects. In practice, only one or two characteristics apply to a critical object. Upon analyzing these characteristics, DriveVLM then predicts the potential influence I of each critical object on the ego vehicle.

## 3.4 Hierarchical Planning

The scene-level summary is then combined with the route, ego pose and velocity to form a prompt for planning. Finally, DriveVLM progressively generates driving plans, in three stages: metaactions, decision description, and trajectory waypoints.

Meta-actions A. A meta-action, denoted as $a _ { i } .$ , represents a short-term decision of the driving strategy. These actions fall into 17 categories, including but not limited to acceleration, deceleration, turning left, changing lanes, minor positional adjustments, and waiting. To plan the ego vehicle's future maneuver over a certain period, we generate a sequence of meta-actions.

Decision Description D. Decision description D articulates the more fine-grained driving strategy the ego vehicle should adopt. It contains three elements: Action A, Subject S, and Duration D. Action pertains to meta actions such as turn', wait', or accelerate'. Subject refers to the interacting object, such as a pedestrian, a traffic signal, or a specific lane. Duration indicates the temporal aspect of the action, specifying how long it should be carried out or when it should start.

Trajectory Waypoints W. Upon establishing the decision description $D ,$ our next phase involves the generation of corresponding trajectory waypoints. These waypoints, denoted by $W =$ $\{ w _ { 1 } , w _ { 2 } , . . . , w _ { n } \} , w _ { i } = ( x _ { i } , y _ { i } )$ , depict the vehicle's path over a certain future period with predetermined intervals $\Delta t$ . We map these numerical waypoints into language tokens for auto-regressive generation.

## 3.5 DriveVLM-Dual

To mitigate the challenges of high latency and imprecise spatial and motion understanding in VLMs, we propose DriveVLM-Dual, a collaboration between DriveVLM and the traditional autonomous driving system. This novel approach involves two key strategies: incorporating 3D perception for critical object analysis, and high-frequency trajectory refinement.

Integrating 3D Perception. We represent objects detected by a 3D detector as $O _ { 3 \mathrm { D } } = \{ c _ { 3 \mathrm { D } } ^ { i } , b _ { 3 \mathrm { D } } ^ { i } \}$ where $b _ { 3 \mathrm { D } } ^ { i }$ denotes the i-th bounding box and $c _ { 3 \mathrm { D } } ^ { i }$ denotes its category. These 3D bounding boxes are then back-projected onto 2D images to derive corresponding 2D bounding boxes $b _ { \mathrm { 2 D } } ^ { i }$ . We conduct IoU matching between these 2D bounding boxes $b _ { \mathrm { 2 D } } ^ { i }$ and $b _ { c } ^ { j } . \ b _ { c } ^ { j }$ are the bounding boxes of previously identified critical objects $O _ { \mathrm { c r i t i c a l } } = \{ c _ { c } ^ { j } , b _ { c } ^ { j } \}$ . We classify critical objects that meet a certain approximate IoU threshold and belong to the same category as matched critical objects $O _ { c } ^ { \mathrm { m a t c h e d } }$ , defined as

$$
\begin{array} { r } { O _ { c } ^ { \mathrm { m a t c h e d } } = \{ c _ { c } ^ { j } , b _ { c } ^ { j } \} , \quad \mathrm { i f } \ : c _ { c } ^ { j } = c _ { 2 \mathrm { D } } ^ { i } \mathrm { a n d } \mathrm { a I o U } ( b _ { c } ^ { j } , b _ { 2 \mathrm { D } } ^ { i } ) > \tau , \mathrm { ~ w h e r e ~ a I o U } ( b _ { c } ^ { j } , b _ { 2 \mathrm { D } } ^ { i } ) = \frac { S _ { b _ { c } ^ { j } \cap b _ { 2 \mathrm { D } } ^ { i } } } { S _ { b _ { 2 \mathrm { D } } ^ { i } } } , } \end{array}
$$

Those critical objects without a corresponding match in the 3D data are noted as $O _ { c } ^ { \mathrm { u n m a t c h e d } }$

In the scene analysis module, for $O _ { c } ^ { \mathrm { m a t c h e d } }$ , the center coordinates, orientations, and historical trajectories of the corresponding 3D objects are used as language prompts for the model, assisting in object analysis. Conversely, for $O _ { c } ^ { \mathrm { u n m a t c h e d } }$ , analysis relies solely on the language tokens derived from the image. This design enables DriveVLM-Dual to understand the locations and motions of critical objects more accurately, enhancing the overall performance.

High-frequency Trajectory Refinement. To achieve real-time, high-frequency inference capabilities, we integrate it with a conventional planner to form a slow-fast dual system, combining the advanced capabilities of DriveVLM with the efficiency of traditional planning methods. After obtaining a trajectory from DriveVLM at low frequency, denoted as $W _ { \mathrm { s l o w } }$ , we take it as a reference trajectory for a classical planner for high-frequency trajectory refinement. In the case of an optimization-based planner, $W _ { \mathrm { s l o w } }$ serves as the initial solution for the optimization solver. For a neural network-based planner, $W _ { \mathrm { s l o w } }$ is used as an input query, combined with additional input features $f ,$ and then decoded into a new planning trajectory denoted as $W _ { \mathrm { f a s t } }$ . The formulation of this process can be described as:

$$
W _ { \mathrm { f a s t } } = \mathrm { P l a n n e r } ( [ W _ { \mathrm { s l o w } } , f ] ) .\tag{1}
$$

This refinement step ensures that the trajectory produced by DriveVLM-Dual (1) achieves higher trajectory quality, and (2) meets real-time requirements. In practice, the two branches operate asynchronously in a slow-fast manner, where the planner module in the traditional autonomous driving branch can selectively receive trajectory from the VLM branch as additional input.

## 4 Task and Dataset

To fully exploit the potential of DriveVLM and DriveVLM-Dual in handling complex and long-tail driving scenarios, we formally define a task called Scene Understanding for Planning (Section 4.1), together with a set of evaluation metrics (Section 4.2). Furthermore, we propose a data mining and annotation protocol to curate a scene understanding and planning dataset (Section 4.3).

## 4.1 Task Definition

The Scene Understanding for Planning task is defined as follows. The input comprises multi-view videos V from surrounding cameras and optionally 3D perception results $\mathcal { P }$ from a perception module. The output includes the following components:

1. Scene Description E: Composed of weather condition $E _ { \mathrm { w e a t h e r } } .$ , time $E _ { \mathrm { t i m e } }$ , road condition $E _ { \mathrm { r o a d } } .$ and lane conditions $E _ { \mathrm { l a n e } }$

Scene Summary: The ego vehicle is moving at a constant speed along the current lane, with ongoing road construction work ahead; there are three construction workers working on the left side of the lane at the roadside.

![](images/e7c273afd6cbc1ff3254eb720db9e539bc4fccb975510a7db3860efc7f37f6e0.jpg)  
Figure 2: An annotated sample of the SUP-AD dataset.

2. Scene Analysis S: Including object-level analysis and scene-level summary S.

3. Meta Actions A: A sequence of actions representing task-level maneuvers.

4. Decision Description D: A detailed account of the driving decisions.

5. Trajectory Waypoints W: The waypoints outlining the planned trajectory of the ego vehicle.

## 4.2 Evaluation Metrics

To comprehensively evaluate a model's performance, we care about its interpretation of the driving scene and the decisions made. Therefore, our evaluation has two aspects: scene description/analysis evaluation and meta-action evaluation.

Scene Description/Analysis Evaluation. Given the subjective nature of human evaluation in scene description, we adopt a structured approach using a pre-trained LLM. This method entails comparing the generated scene description with a human-annotated ground truth description. The ground truth description encompasses structured data such as environmental conditions, navigation, lane information, and critical events with specific objects, verbs, and their influences. The LLM assesses and scores the generated descriptions based on their consistency with the ground truth.

Meta-action Evaluation. Meta-actions are a predefined set of decision-making options. A driving decision is formulated as a sequence of meta-actions. Our evaluation method employs a dynamic programming algorithm to compare the model-generated sequences with a manually annotated ground truth sequence. The evaluation should also weigh the relative importance of various meta-actions, designating some as conservative actions' with a lower impact on the sequence's overall context. To increase robustness, we first use the LLM to generate semantically equivalent alternatives to the ground truth sequence to enhance robustness. The sequence with the highest similarity to these alternatives calculates the final driving decision score. More details of the proposed metric are available in the Appendix B.

## 4.3 Dataset Construction

We propose a comprehensive data mining and annotation pipeline, shown in Figure 3, to construct a Scene Understanding for Planning (SUP-AD) Dataset for the proposed task. Specifically, we perform long-tail object mining and challenging scenario mining from a large database to collect samples, then we select a keyframe from each sample and further perform scene annotation. Dataset statistics are available in the Appendix A.

Long-tail Object Mining. According to real-world road object distribution, we first define a list of long-tail object categories, such as weird-shaped vehicles, road debris, and animals crossing the road. Next, we mine these long-tail scenarios using a CLIP-based search engine, capable of mining driving data using language queries from a large collection of logs. Following that, we perform a manual inspection to filter out scenes inconsistent with the specified categories.

![](images/c859748e4f3b77f3488faf1a81caf0d76d404d15fd79d3190765de9839f98ba0.jpg)  
Figure 3: The proposed data mining and annotation pipeline for constructing a scene understanding and planning dataset. Scenario examples randomly sampled from the dataset (below) demonstrate the diversity and complexity of the dataset.

Challenging Scenario Mining. In addition to long-tail objects, we are also interested in challenging driving scenarios, where the driving strategy of the ego vehicle needs to be adapted according to the changing driving conditions. These scenarios are mined according to the variance of the recorded driving maneuvers.

Keyframe Selection. Each scene is a video clip, it is essential to identify the keyframe' to annotate. In most challenging scenarios, a keyframe is the moment before a significant change in speed or direction is required. We select this keyframe 0.5s to 1s earlier than the actual maneuver, based on comprehensive testing, to guarantee an optimal reaction time for decision-making. For scenes that do not involve changes in driving behavior, we select a frame that is relevant to the current driving scenario as the keyframe.

Scene Annotation. We employ a group of annotators to perform the scene annotation, including scene description, scene analysis, and planning, except for waypoints, which can be auto-labeled from the vehicle's IMU recordings. To facilitate scene annotation, we make a video annotation tool with the following features: (1) the annotators can slide the progress bar back and forth to replay any part of a video; (2) while annotating a keyframe, the annotator can draw bounding boxes on the image together with language descriptions; (3) annotators can select from a list of action and decision candidates while annotating driving plans. Each annotation is meticulously verified by 3 annotators for accuracy and consistency, ensuring a reliable dataset for model training. Figure 2 illustrates a sample scenario with detailed annotations.

## 5 Experiments

## 5.1 Settings

We test DriveVLM and DriveVLM-Dual on our proposed SUP-AD dataset and nuScenes dataset [44].

SUP-AD Dataset. The SUP-AD dataset is a dataset built by our proposed data mining and annotation pipeline. It is divided into train, validation, and test splits with a ratio of 7.5 : 1 : 1.5. We train models on the training split and use our proposed scene description and meta-action metrics to evaluate model performance on the test split. We also employ co-tuning with additional datasets to ensure the generalization of the LLM is not compromised.

nuScenes Dataset. The nuScenes dataset is a large-scale driving dataset of urban scenarios with 1000 scenes, where each scene lasts about 20 seconds. Following previous works [34, 51], we adopt Displacement Error (DE) and Collision Rate (CR) as metrics to evaluate models’ performance.

Table 1: Results on the test set of our proposed SUP-AD dataset. †: Using the official API of GPT-4V. For Lynx and CogVLM, we utilize the training split for fine-tuning purposes. In contrast, for GPT-4V, we employ in-context learning.
<table><tr><td>Method</td><td>Scene Description</td><td>Meta-actions</td></tr><tr><td>Fine-tuning w/ Lynx [14]</td><td>0.46</td><td>0.15</td></tr><tr><td>Fine-tuning w/ CogVLM [21]</td><td>0.49</td><td>0.22</td></tr><tr><td>GPT-4V† [52]</td><td>0.38</td><td>0.19</td></tr><tr><td>DriveVLM w/ Qwen</td><td>0.71</td><td>0.37</td></tr></table>

Table 2: Planning results on the nuScenes validation dataset. DriveVLM-Dual achieves the best performance. † denotes cooperating with VAD [51].
<table><tr><td rowspan="2">Method</td><td colspan="4">L2 (m) ↓</td><td colspan="4">Collision (%) ↓</td></tr><tr><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td></tr><tr><td>NMP [30]</td><td>-</td><td>-</td><td>2.31</td><td>–</td><td>-</td><td>-</td><td>1.92</td><td>一</td></tr><tr><td>SA-NMP [30]</td><td></td><td></td><td>2.05</td><td></td><td></td><td></td><td>1.59</td><td></td></tr><tr><td>FF [32]</td><td>0.55</td><td>1.20</td><td>2.54</td><td>1.43</td><td>0.06</td><td>0.17</td><td>1.07</td><td>0.43</td></tr><tr><td>EO [53]</td><td>0.67</td><td>1.36</td><td>2.78</td><td>1.60</td><td>0.04</td><td>0.09</td><td>0.88</td><td>0.33</td></tr><tr><td>ST-P3 [54]</td><td>1.33</td><td>2.11</td><td>2.90</td><td>2.11</td><td>0.23</td><td>0.62</td><td>1.27</td><td>0.71</td></tr><tr><td>UniAD [34]</td><td>0.48</td><td>0.96</td><td>1.65</td><td>1.03</td><td>0.05</td><td>0.17</td><td>0.71</td><td>0.31</td></tr><tr><td>VAD-Base [51]</td><td>0.17</td><td>0.34</td><td>0.60</td><td>0.37</td><td>0.07</td><td>0.10</td><td>0.24</td><td>0.14</td></tr><tr><td>DriveVLM</td><td>0.18</td><td>0.34</td><td>0.68</td><td>0.40</td><td>0.10</td><td>0.22</td><td>0.45</td><td>0.27</td></tr><tr><td>DriveVLM-Dual†</td><td>0.15</td><td>0.29</td><td>0.48</td><td>0.31</td><td>0.05</td><td>0.08</td><td>0.17</td><td>0.10</td></tr></table>

Co-tuning To preserve the LLM's generalization capabilities during the fine-tuning process, we employed co-tuning with several additional datasets. These include the Talk2Car [41], BDDX [45], Drama [48], SUTD [55], and LLAVA [17] datasets. For each dataset, we conducted random sampling in a 1:1 ratio corresponding to the data volume of the SUP-AD and nuScenes datasets. Following this co-tuning approach, we found that the scores on the SUP-AD dataset, under the evaluation metrics of Scene Description and Meta Action, remained virtually unchanged, simultaneously ensuring the preservation of the LLM's original capabilities and its generalization capacity.

Base Model. We use Qwen-VL [18] as our default large vision-language model, which exhibits remarkable performance in tasks like question answering, visual localization, and text recognition. It contains a total of 9.6 billion parameters, including a visual encoder (1.9 billion), a vision-language adapter (0.08 billion), and a large language model (Qwen, 7.7 billion). Images are resized to a resolution of 448 × 448 before being encoded by the vision encoder. During training, we randomly select a sequence of images at the current time Ts, T – 1s, T — 2s, and T — 3s as input. The selected images ensure the inclusion of the current time frame and follow an ascending chronological order.

## 5.2 Main Results

SUP-AD. We present the performance of our proposed DriveVLM with several large visionlanguage models and compare them with GPT-4V, as shown in Table 1. DriveVLM, utilizing Qwen-VL as its backbone, achieves the best performance due to its strong capabilities in question answering and flexible interaction compared to the other open-source VLMs. Although GPT-4V exhibits robust capabilities in vision and language processing, its inability to undergo fine-tuning, restricting it solely to in-context learning, often results in the generation of extraneous information during scene description tasks. Under our evaluation metric, the additional information is frequently classified as hallucination, consequently leading to lower scores.

nuScenes. As shown in Table 2, DriveVLM-Dual achieves state-of-the-art performance on the nuScenes planning task when cooperating with VAD. It demonstrates that our method, although tailored for understanding complex scenes, also excels in ordinary scenarios.

## 5.3 Ablation Study

Model Design. To better understand the significance of our designed modules in DriveVLM, we conduct ablations on different combinations of modules, as shown in Table 3. The inclusion of critical object analysis enables our model to identify and prioritize important elements in the driving environment, enhancing the decision-making accuracy for safer navigation. Integrating 3D perception data, our model gains a refined understanding of the surroundings and achieves precise predictions.

Table 3: Ablations of design choices on the validation set of nuScenes. “Base" refers to only indicating the hierarchical planning results without our proposed CoT inference. “CO" represents the addition of critical object analysis. “3D" denotes the inclusion of 3D perception results as an auxiliary language prompt.
<table><tr><td rowspan="2">ID</td><td rowspan="2">Base</td><td rowspan="2">CO</td><td rowspan="2">3D</td><td rowspan="2">1s</td><td colspan="4">L2 (m) ↓</td><td colspan="4">Collision (%) ↓</td></tr><tr><td></td><td>2s</td><td>3s</td><td>Avg.</td><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td></tr><tr><td>1</td><td>√</td><td></td><td></td><td>0.19</td><td>0.41</td><td>0.89</td><td>0.49</td><td></td><td>0.16</td><td>0.28</td><td>0.63</td><td>0.36</td></tr><tr><td>2</td><td>√</td><td>√</td><td></td><td>0.20</td><td></td><td>0.38</td><td>0.75</td><td>0.44</td><td>0.15</td><td>0.29</td><td>0.61</td><td>0.35</td></tr><tr><td>3</td><td>√</td><td>√</td><td>√</td><td></td><td>0.18</td><td>0.34</td><td>0.68</td><td>0.40</td><td>0.10</td><td>0.22</td><td>0.45</td><td>0.27</td></tr></table>

Table 4: Ablations of traditional autonomous driving pipeline in DriveVLM-Dual. MLP stands for methods similar to AD-MLP [56].
<table><tr><td rowspan="2">Method</td><td colspan="4">L2 (m) ↓</td><td colspan="4">Collision (%) ↓</td></tr><tr><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td></tr><tr><td>UniAD [34] DriveVLM-Dual (UniAD)</td><td>0.48 0.17</td><td>0.96 0.37</td><td>1.65 0.63</td><td>1.03 0.39</td><td>0.05 0.08</td><td>0.17 0.18</td><td>0.71 0.35</td><td>0.31 0.20</td></tr><tr><td>MLP</td><td>0.25</td><td>0.46</td><td>0.62</td><td>0.44</td><td>0.14</td><td>0.18</td><td>0.28</td><td>0.20</td></tr><tr><td>DriveVLM-Dual (MLP)</td><td>0.14</td><td>0.35</td><td>0.30</td><td>0.31</td><td>0.09</td><td>0.13</td><td>0.18</td><td>0.13</td></tr><tr><td>VAD [51]</td><td>0.17</td><td>0.34</td><td>0.60</td><td>0.37</td><td>0.07</td><td>0.10</td><td>0.24</td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0.14</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>DriveVLM-Dual(VAD)</td><td>0.15</td><td>0.29</td><td>0.48</td><td>0.31</td><td>0.05</td><td>0.08</td><td>0.17</td><td>0.10</td></tr></table>

Traditional AD Pipeline. To demonstrate the generalization of our dual system design, we test DriveVLM-Dual with different traditional autonomous driving pipelines on the validation set of nuScenes. As illustrated in Table 4, our proposed DriveVLM-Dual adapts well to different traditional AD pipelines. While a standalone MLP method shows a notable performance gap compared to VAD, both variants of DriveVLM-Dual achieve nearly identical performance, underscoring the efficacy and robustness of our dual system design.

## 5.4 Qualitative Results

Qualitative results of DriveVLM are shown in Figure 4. In Figure 4a, DriveVLM accurately predicts the current scene conditions and incorporates well-considered planning decisions regarding the cyclist approaching us. In Figure 4b, DriveVLM effectively comprehends the gesture of the traffic police ahead, signaling the ego vehicle to proceed, and also considers the person riding a tricycle on the right side, thereby making sensible driving decisions. These qualitative results demonstrate our model's exceptional ability to understand complex scenarios and make suitable driving plans. More visualization of our model's output is shown in the Appendix C.

![](images/79b2255530c43f488e1443cb44c25c5ca37917650fbca85dea647c13a9f81a08.jpg)  
(a)

![](images/72f65ae081e65df3f4be3ffc5068a568b5f9c2cef1584622d05c26ad30d34da7.jpg)  
(b)  
Figure 4: Qualitative results of DriveVLM. The orange curves represent the model's planned future trajectories for the next 3 seconds.

<table><tr><td>Base LLM</td><td> $\operatorname { A v g } .$ </td><td>MMMU [57] 5%</td><td>SEEDBench [58] 20%</td><td>RefCOCO [59] 15%</td><td>SUP-AD 15%</td><td>Drivelm-QA [60] 7.5%</td><td>Drivelm-Grounding [60] 7.5%</td><td>RealworldQA [61] 15%</td></tr><tr><td>MobileLLaMA1.4B [62]</td><td>0.457</td><td>0.331</td><td>0.590</td><td>0.421</td><td>0.520</td><td>0.686</td><td>0.735</td><td>0.501</td></tr><tr><td>Qwen-1.8B [63]</td><td>0.477</td><td>0.340</td><td>0.622</td><td>0.492</td><td>0.523</td><td>0.680</td><td>0.725</td><td>0.518</td></tr><tr><td>Gemma-2B [64]</td><td>0.439</td><td>0.345</td><td>0.571</td><td>0.330</td><td>0.510</td><td>0.680</td><td>0.721</td><td>0.507</td></tr><tr><td>MiniCPM-2.4B [65]</td><td>0.482</td><td>0.379</td><td>0.640</td><td>0.444</td><td>0.539</td><td>0.676</td><td>0.717</td><td>0.553</td></tr><tr><td>MobileLLaMA2.7B [62]</td><td>0.496</td><td>0.348</td><td>0.635</td><td>0.557</td><td>0.546</td><td>0.683</td><td>0.725</td><td>0.536</td></tr><tr><td>Phi3-3.8B [66]</td><td>0.538</td><td>0.435</td><td>0.688</td><td>0.608</td><td>0.604</td><td>0.697</td><td>0.743</td><td>0.592</td></tr><tr><td>Qwen-4B [63]</td><td>0.511</td><td>0.366</td><td>0.671</td><td>0.603</td><td>0.515</td><td>0.681</td><td>0.735</td><td>0.562</td></tr><tr><td>Qwen-4B*</td><td>0.529</td><td>0.373</td><td>0.684</td><td>0.624</td><td>0.596</td><td>0.699</td><td>0.738</td><td>0.553</td></tr></table>

Table 5: Performance of different LLMs on various datasets using the LLAVA-1.5 [67] architecture with ViT-L-336 [50] as the image encoder. Note that \* indicates using SigLIP-L-384 [68] as the image encoder. Compared to general capabilities, we are more concerned with the performance of VLMs in abilities that are more relevant to autonomous driving. Therefore, we set different score weights for various benchmarks.

<table><tr><td>LLM</td><td>| Promt Length(toks)</td><td>Prefill latency (s)</td><td>Prefill (tok/s)</td><td>Decode (tok/s)</td><td>Output (toks)</td><td>Decode latency (s)</td><td>Model Size (GB)</td><td>Layer Num</td><td>Head Size</td><td>Vocab Size</td></tr><tr><td>Gemma-2B [64]</td><td>1063</td><td>0.95</td><td>1121</td><td>40.9</td><td>59</td><td>1.44</td><td>4.7</td><td>18</td><td>256</td><td>256000</td></tr><tr><td>Phi3-4k [66]</td><td>1045</td><td>1.30</td><td>797.3</td><td>49.0</td><td>59</td><td>1.20</td><td>7.2</td><td>32</td><td>96</td><td>32064</td></tr><tr><td>MobileLLaMa-2.7B [62]</td><td>1047</td><td>0.92</td><td>1134</td><td>61.7</td><td>59</td><td>0.96</td><td>5.0</td><td>32</td><td>80</td><td>32000</td></tr><tr><td>MobileLLaMa-1.4B [62]</td><td>1047</td><td>0.23</td><td>4634</td><td>117.4</td><td>59</td><td>0.50</td><td>2.5</td><td>24</td><td>128</td><td>32000</td></tr><tr><td>Qwen4B [63]</td><td>1078</td><td>0.57</td><td>1882</td><td>44.5</td><td>59</td><td>1.33</td><td>7.5</td><td>40</td><td>128</td><td>151936</td></tr><tr><td>Qwen1.8B [63]</td><td>1078</td><td>0.23</td><td>4709</td><td>79.6</td><td>59</td><td>0.74</td><td>3.7</td><td>24</td><td>128</td><td>151936</td></tr></table>

Table 6: Inference performance of different LLMs after quantization and deployment on an OrinX chip. The Qwen series achieved the best performance.

## 6 Onboard Deployment and Testing

We deploy DriveVLM-Dual on an autonomous vehicle equipped with two OrinX processors, with a high-frequency end-to-end driving system on OrinX-1 and our DriveVLM on OrinX-2. These two systems operate and collaborate asynchronously. Furthermore, we optimize the DriveVLM and achieve an average inference speed of 410 ms on OrinX. The video demonstration of this dualsystem deployment can be found at the following link: https://www.youtube.com/watch?v= MMC00TLMT74.

In this section, we present several comparative experiments, which will provide insights for practical deployment on edge devices. Notice that all the VLMs are pre-trained and fine-tuned on common datasets as well as our proprietary datasets specifically designed for autonomous driving.

Base LLM Due to the limited memory and bandwidth of the vehicle's hardware, we cannot use overly large LLMs to maintain real-time inference. Therefore, we chose models with fewer than 4 billion parameters. As shown in Table 5 and 6, our experiments revealed that on the Orin architecture, the “wide and shallow"Qwen series (wider and fewer layers) models outperform “narrow and deep"models (narrower and more layers) in inference speed.
<table><tr><td>Backbone</td><td>Token Length</td><td>Method</td><td>Weighted Total</td><td>MMMU [57] 5%</td><td>SEEDBench [58] 20%</td><td>RefCOCO [59] 15%</td><td>SUP-AD 15%</td><td>Drivelm-QA [60] 7.5%</td><td>Drivelm-Grounding [60] 7.5%</td><td>RealworldQA [61] 15%</td><td>PointVQA 15%</td></tr><tr><td>ViT-L-336 [50]</td><td></td><td></td><td>0.421</td><td>0.368</td><td>0.657</td><td>0.502</td><td>0.553</td><td>0.688</td><td>0.742</td><td>0.541</td><td>0.583</td></tr><tr><td>ViT-L-336</td><td></td><td>Fixed 1x2 + CA-256</td><td>0.413</td><td>0.388</td><td>0.62</td><td>0.327</td><td>0.543</td><td>0.699</td><td>0.733</td><td>0.536</td><td>0.563</td></tr><tr><td>ViT-L-336</td><td></td><td>Fixed 2x2 + CA-256</td><td>0.405</td><td>0.376</td><td>0.618</td><td>0.306</td><td>0.518</td><td>0.692</td><td>0.731</td><td>0.523</td><td>0.594</td></tr><tr><td>ViT-L-448</td><td></td><td>Fixed 1x2 + CA-256</td><td>0.383</td><td>0.391</td><td>0.542</td><td>0.184</td><td>0.528</td><td>0.689</td><td>0.718</td><td>0.470</td><td>0.562</td></tr><tr><td>ViT-L-336</td><td></td><td>Fixed 1x2 + S2</td><td></td><td></td><td>0.511</td><td>0.198</td><td>0.469</td><td>0.689</td><td></td><td></td><td></td></tr><tr><td></td><td></td><td>Fixed 1x2 + S2</td><td>0.368</td><td>0.383</td><td></td><td></td><td></td><td></td><td>0.718</td><td>0.469</td><td>0.314</td></tr><tr><td>ViT-L-336</td><td></td><td></td><td>0.368</td><td>0.381</td><td>0.537</td><td>0.207</td><td>0.544</td><td>0.698</td><td>0.729</td><td>0.460</td><td>0.554</td></tr><tr><td>ViT-L-336</td><td></td><td>DM-4 + CA-256</td><td>0.409</td><td>0.377</td><td>0.610</td><td>0.277</td><td>0.544</td><td>0.698</td><td>0.726</td><td>0.525</td><td>0.554</td></tr><tr><td>ViT-L-336</td><td></td><td>DM-6 + CA-256</td><td>0.381</td><td>0.381</td><td>0.500</td><td>0.162</td><td>0.523</td><td>0.700</td><td>0.729</td><td>0.466</td><td>0.584</td></tr><tr><td>ViT-L-336</td><td></td><td>DM-4 + PT</td><td>0.426</td><td>0.376</td><td>0.653</td><td>0.557</td><td>0.585</td><td>0.700</td><td>0.743</td><td>0.540</td><td>0.598</td></tr><tr><td>ViT-L-336</td><td></td><td>DM-4 + SM + LT</td><td>0.413</td><td>0.403</td><td>0.617</td><td>0.293</td><td>0.550</td><td>0.699</td><td>0.737</td><td>0.527</td><td>0.532</td></tr><tr><td>ViT-L-336</td><td></td><td>DM-4 + SM + AAP + LT</td><td>0.406</td><td>0.384</td><td>0.610</td><td>0.273</td><td>0.518</td><td>0.68</td><td>0.726</td><td>0.520</td><td>0.533</td></tr><tr><td>ViT-L-336</td><td></td><td>DM-4 + SM + CD + LT</td><td>0.409</td><td>0.388</td><td>0.630</td><td>0.480</td><td>0.515</td><td>0.700</td><td>0.734</td><td>0.524</td><td>0.577</td></tr><tr><td>SigLIP-L-384 [68]</td><td>576</td><td></td><td>0.432</td><td>0.389</td><td>0.631</td><td>0.615</td><td>0.624</td><td>0.707</td><td>0.749</td><td>0.556</td><td>0.560</td></tr><tr><td>SigLIP-L-768</td><td>576</td><td></td><td>0.438</td><td>0.377</td><td>0.642</td><td>0.580</td><td>0.638</td><td>0.712</td><td>0.764</td><td>0.561</td><td>0.556</td></tr><tr><td>SigLIP-L-1152</td><td>576</td><td></td><td>0.436</td><td>0.377</td><td>0.637</td><td>0.595</td><td>0.628</td><td>0.715</td><td>0.763</td><td>0.571</td><td>0.564</td></tr><tr><td>SigLIP-L-384-768</td><td>576</td><td></td><td>0.434</td><td>0.367</td><td>0.632</td><td>0.581</td><td>0.631</td><td>0.716</td><td>0.762</td><td></td><td></td></tr><tr><td>SigLIP-L-512-960</td><td>480</td><td>PE PE</td><td>0.442</td><td>0.369</td><td>0.640</td><td>0.557</td><td>0.650</td><td>0.719</td><td>0.762</td><td>0.556 0.579</td><td>0.554 0.568</td></tr></table>

Table 7: Performance of different methods for scaling ViT's original input resolution to higher resolution. $\mathbf { \vec { \Delta } C A ^ { \prime } }$ stands for cross-attention, $\mathbf { \hat { \mu } } ^ { 6 6 } \mathbf { D M } ^ { 5 }$ is the abbreviation for Dynamic Max, $\mathrm { \Omega ^ { \ 6 6 } P T ^ { 5 } }$ indicates the use of patch end token, “SM" stands for Spatial Merge, “LT" indicates the use of line end token, $\ " { \bf A } { \bf A } { \bf P } ^ { \prime }$ is the abbreviation for Adaptive Average Pooling, and “CD" stands for Convolutional Downsampling. "PE" represents Position Embedding Interpolation. Among these methods, applying PE interpolation to SigLIP-L-384 and modifying it to take 768-resolution images as input achieves a good trade-off between inference speed and performance.

<table><tr><td>Projector</td><td>| Origin</td><td>Compressed</td><td>Output(ms)</td><td>Prefill(ms)</td><td>Avg.</td><td>MMMU [57]</td><td>SEEDV2 [58]</td><td>BDD [?]</td><td>Drivelm-QA [60]</td><td>Drivelm-grounding [60]</td><td>RealworldQA [61]</td><td>RefCOCO [59]</td><td>SUP-AD</td></tr><tr><td>MLP (Baseline)</td><td>576</td><td>576</td><td>666.60</td><td>707.93</td><td>56.27</td><td>37.90</td><td>64.00</td><td>53.90</td><td>67.60</td><td>71.70</td><td>55.30</td><td>44.40</td><td>53.90</td></tr><tr><td>LDPNetV2 [62]</td><td>576</td><td>576</td><td>661.70</td><td>707.42</td><td>50.53</td><td>37.67</td><td>56.71</td><td>53.36</td><td>68.90</td><td>73.20</td><td>48.30</td><td>21.29</td><td>54.70</td></tr><tr><td>Perceiver Resampler [69]</td><td>576</td><td>576</td><td>637.20</td><td></td><td>49.71</td><td>39.93</td><td>58.84</td><td>52.21</td><td>68.37</td><td>71.90</td><td>49.61</td><td>19.01</td><td>48.70</td></tr><tr><td>Pixel shuffle</td><td>576</td><td>256</td><td>610.70</td><td>666.20 655.92</td><td>52.02</td><td>40.42</td><td>60.20</td><td>55.19</td><td>68.72</td><td>71.52</td><td>51.44</td><td>28.23</td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td>38.93</td><td>62.19</td><td>54.82</td><td>68.57</td><td></td><td></td><td></td><td>48.40</td></tr><tr><td>LDPNetV2</td><td>576</td><td>256</td><td>605.32</td><td>652.79</td><td>54.73</td><td>38.98</td><td>61.63</td><td>56.06</td><td>69.18</td><td>72.78</td><td>50.59</td><td>34.32</td><td>59.30</td></tr><tr><td>Pixel shuffle</td><td>576</td><td>144</td><td>604.98</td><td>645.61</td><td>49.40</td><td></td><td>62.63</td><td></td><td></td><td>73.18</td><td>51.05</td><td>30.67</td><td>58.80</td></tr><tr><td>LDPNetV2</td><td>576</td><td>144</td><td>597.15</td><td>646.77 645.18</td><td>55.56</td><td>38.93</td><td>61.80</td><td>56.23</td><td>68.93</td><td>72.48</td><td>50.59</td><td>33.14</td><td>59.30</td></tr><tr><td>LDPNetV2</td><td>576</td><td>64</td><td>616.20</td><td></td><td>56.24</td><td>39.40</td><td></td><td>54.60</td><td>68.80</td><td>72.60</td><td>51.00</td><td>41.88</td><td>61.20</td></tr></table>

Table 8: Performance of different methods for visual token compression. Using LDPNetV2 to compress the original tokens to 75% of the original token count, achieves the best trade-off between performance and speed.

<table><tr><td></td><td>Base + q4f16_1</td><td>Eagle [72] + q4f16_1</td><td>Medusa [73] + q4f16_ft</td><td>Eagle + q4f16_ft</td><td>Eagle + q4f16_ft + Shrink Vocab Size(1024)</td></tr><tr><td>Quant Type</td><td>q4f16_1</td><td>q4f16_1</td><td>q4f16_ft</td><td>q4f16_ft</td><td>q4f16_ft</td></tr><tr><td>Input Size</td><td>(384, 960)</td><td>(384, 960)</td><td>(384, 960)</td><td>(384, 960)</td><td>(384, 960)</td></tr><tr><td>Prefill Tokens</td><td>604</td><td>604</td><td>613</td><td>604</td><td>613</td></tr><tr><td>Output Tokens</td><td>37</td><td>39</td><td>41</td><td>41</td><td>41</td></tr><tr><td>Prefill Speed (tok/s)</td><td>1818</td><td>1793</td><td>2160.64</td><td>2230</td><td>2175.35</td></tr><tr><td>Decode Speed (tok/s)</td><td>109</td><td>172</td><td>232.34</td><td>295.04</td><td>518.3</td></tr><tr><td>Prefill Latency (s)</td><td>0.332</td><td>0.340</td><td>0.284</td><td>0.276</td><td>0.274</td></tr><tr><td>Decode Latency (s)</td><td>0.328</td><td>0.216</td><td>0.176</td><td>0.130</td><td>0.071</td></tr><tr><td>Acceleration ratio</td><td>1</td><td>1.57</td><td>2.17</td><td>2.7</td><td>4.33</td></tr></table>

Table 9: Performance of different speculative sampling methods. “Shrink Vocab Size" means we reduce the vocabulary to the 1024 most frequently used words. “q4f16\_1"is a 4-bit quantization method using a 16-bit floating-point representation for efficient model compression, while “q4f16\_ft" includes subsequent fine-tuning to enhance performance post-quantization.

Visual Encoder High-resolution images are essential for fine-grained visual understanding in autonomous driving. As shown in Table 7, compared to the basic ViT model used as a visual encoder, we explored several options, including different GridPatch strategies and PE (Position Embedding) interpolation. Ultimately, for real-time inference, we selected the simpler SigLIP-L-384 model with PE interpolation, achieving high-resolution input through original 384-resolution PE interpolation and fine-tuning parameters with additional convolution layers.

Visual Token Compression To address the increased computational load from high-resolution images, we implemented LDPNetv2 [62] to reduce the number of image tokens by 75% without compromising performance, as shown in Table 8. Additionally, we enhanced performance by replacing the average pooling layer with a convolution layer in LDPNetv2.

Video Input In autonomous driving scenarios, more temporal context is needed for accurately assessing object motion changes. We employ a short-term memory-bank [70] strategy, temporarily storing visual features from historical frames in a feature queue. Only the features from the current moment are extracted and fused with multiple historical frames before being projected into the LLM. Besides basic spatiotemporal pooling, we added SE [71] blocks to perform a weighted fusion of multiple temporal frames.

Speculative Sampling Speculative Sampling is used to accelerate inference by preemptively generating likely outputs. This approach reduces the latency of generating predictions, achieving a significant speedup without substantial loss in accuracy. As shown in Table 9, we test two speculative sampling methods: Medusa [73] and Eagle [72] with our inference framework designed specifically for the OrinX chip. Eagle achieved a 2.7 × speedup in decode latency compared to Medusa's 2.17 ×, making real-time vehicle deployment feasible.

## 7 Conclusion

In summary, we introduce DriveVLM and DriveVLM-Dual. DriveVLM leverages VLMs, significantly progressing in interpreting complex driving environments. DriveVLM-Dual further enhances these capabilities by synergizing existing 3D perception and planning approaches, effectively addressing the spatial reasoning and computational challenges inherent in VLMs. Moreover, we define a scene understanding for planning task for autonomous driving, together with evaluation metrics and dataset construction protocol. DriveVLM and DriveVLM-Dual have surpassed the state-of-theart methods on the public and our benchmarks, especially in handling intricate and dynamic scenarios. Finally, we have verified the effectiveness of DriveVLM-Dual through onboard deployment and testing on a production vehicle.

## Acknowledgments

We thank Chenxu Hu at Tsinghua University for the help on paper writing. We thank Xu Bian, Hongkun Chen, Sui Cong, Chengze Guan, Mingyu Guo, Yue Jiang, Qi Jiang, Pengfei Ji, Wei Xiao, Dafeng Wei, Zijian Wang, Zhao Yang, Chenglong Zhao, Simeng Zhao, and Jian Zhou at Li Auto for their efforts in the experiments related to onboard deployment.

## References

[1] I. Barabas, A. Todoruţ, N. Cordoş, and A. Molea. Current challenges in autonomous driving. In IOP conference series: materials science and engineering, volume 252, page 012096. IOP Publishing, 2017.

[2] C. R. Qi, H. Su, K. Mo, and L. J. Guibas. Pointnet: Deep learning on point sets for 3d classification and segmentation. In Proceedings of the IEEE conference on computer vision and pattern recognition, pages 652–660, 2017.

[3] A. H. Lang, S. Vora, H. Caesar, L. Zhou, J. Yang, and O. Beijbom. Pointpillars: Fast encoders for object detection from point clouds. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 12697–12705, 2019.

[4] Y. Wang, V. C. Guizilini, T. Zhang, Y. Wang, H. Zhao, and J. Solomon. Detr3d: 3d object detection from multi-view images via 3d-to-2d queries. In Conference on Robot Learning, pages 180–191. PMLR, 2022.

[5] Z. Li, W. Wang, H. Li, E. Xie, C. Sima, T. Lu, Y. Qiao, and J. Dai. Bevformer: Learning bird's-eye-view representation from multi-camera images via spatiotemporal transformers. In European conference on computer vision, pages 1–18. Springer, 2022.

[6] J. Gao, C. Sun, H. Zhao, Y. Shen, D. Anguelov, C. Li, and C. Schmid. Vectornet: Encoding hd maps and agent dynamics from vectorized representation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), June 2020.

[7] H. Zhao, J. Gao, T. Lan, C. Sun, B. Sapp, B. Varadarajan, Y. Shen, Y. Shen, Y. Chai, C. Schmid, C. Li, and D. Anguelov. Tnt: Target-driven trajectory prediction. In J. Kober, F. Ramos, and C. Tomlin, editors, Proceedings of the 2020 Conference on Robot Learning, volume 155 of Proceedings of Machine Learning Research, pages 895–904. PMLR, 16–18 Nov 2021.

[8] Y. Liu, J. Zhang, L. Fang, Q. Jiang, and B. Zhou. Multimodal motion prediction with stacked transformers. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 7577–7586, 2021.

[9] J. Gu, C. Sun, and H. Zhao. Densetnt: End-to-end trajectory prediction from dense goal sets. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 15303– 15312,2021.

[10] N. Nayakanti, R. Al-Rfou, A. Zhou, K. Goel, K. S. Refaat, and B. Sapp. Wayformer: Motion forecasting via simple & efficient attention networks. In 2023 IEEE International Conference on Robotics and Automation (ICRA), pages 2980–2987. IEEE, 2023.

[11] D. A. Pomerleau. Alvinn: An autonomous land vehicle in a neural network. Advances in neural information processing systems, 1, 1988.

[12] M. Bansal, A. Krizhevsky, and A. Ogale. Chauffeurnet: Learning to drive by imitating the best and synthesizing the worst. arXiv preprint arXiv:1812.03079, 2018.

[13] Z. Li, F. Nie, Q. Sun, F. Da, and H. Zhao. Uncertainty-aware decision transformer for stochastic driving environments. arXiv preprint arXiv:2309.16397, 2023.

[14] Y. Zeng, H. Zhang, J. Zheng, J. Xia, G. Wei, Y. Wei, Y. Zhang, and T. Kong. What matters in training a gpt4-style language model with multimodal inputs? arXiv preprint arXiv:2307.02469, 2023.

[15] Z. Xu, Y. Zhang, E. Xie, Z. Zhao, Y. Guo, K. K. Wong, Z. Li, and H. Zhao. Drivegpt4: Interpretable end-to-end autonomous driving via large language model. arXiv preprint arXiv:2310.01412, 2023.

[16] D. Zhu, J. Chen, X. Shen, X. Li, and M. Elhoseiny. Minigpt-4: Enhancing vision-language understanding with advanced large language models. arXiv preprint arXiv:2304.10592, 2023.

[17] H. Liu, C. Li, Q. Wu, and Y. J. Lee. Visual instruction tuning, 2023.

[18] J. Bai, S. Bai, S. Yang, S. Wang, S. Tan, P. Wang, J. Lin, C. Zhou, and J. Zhou. Qwen-vl: A versatile vision-language model for understanding, localization, text reading, and beyond. arXiv preprint arXiv:2308.12966, 2023.

[19] W. Dai, J. Li, D. Li, A. M. H. Tiong, J. Zhao, W. Wang, B. Li, P. Fung, and S. Hoi. Instructblip: Towards general-purpose vision-language models with instruction tuning, 2023.

[20] P. Zhang, X. Dong, B. Wang, Y. Cao, C. Xu, L. Ouyang, Z. Zhao, S. Ding, S. Zhang, H. Duan, W. Zhang, H. Yan, X. Zhang, W. Li, J. Li, K. Chen, C. He, X. Zhang, Y. Qiao, D. Lin, and J. Wang. Internlm-xcomposer: A vision-language large model for advanced text-image comprehension and composition, 2023.

[21] W. Wang, Q. Lv, W. Yu, W. Hong, J. Qi, Y. Wang, J. Ji, Z. Yang, L. Zhao, X. Song, et al. Cogvlm: Visual expert for pretrained language models. arXiv preprint arXiv:2311.03079, 2023.

[22] D. Driess, F. Xia, M. S. M. Sajjadi, C. Lynch, A. Chowdhery, B. Ichter, A. Wahid, J. Tompson, Q. Vuong, T. Yu, W. Huang, Y. Chebotar, P. Sermanet, D. Duckworth, S. Levine, V. Vanhoucke, K. Hausman, M. Toussaint, K. Greff, A. Zeng, I. Mordatch, and P. Florence. Palm-e: An embodied multimodal language model, 2023.

[23] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. arXiv preprint arXiv:2212.06817, 2022.

[24] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, X. Chen, K. Choromanski, T. Ding, D. Driess, A. Dubey, C. Finn, P. Florence, C. Fu, M. G. Arenas, K. Gopalakrishnan, K. Han, K. Hausman, A. Herzog, J. Hsu, B. Ichter, A. Irpan, N. Joshi, R. Julian, D. Kalashnikov, Y. Kuang, I. Leal, L. Lee, T.-W. E. Lee, S. Levine, Y. Lu, H. Michalewski, I. Mordatch, K. Pertsch, K. Rao, K. Reymann, M. Ryoo, G. Salazar, P. Sanketi, P. Sermanet, J. Singh, A. Singh, R. Soricut, H. Tran, V. Vanhoucke, Q. Vuong, A. Wahid, S. Welker, P. Wohlhart, J. Wu, F. Xia, T. Xiao, P. Xu, S. Xu, T. Yu, and B. Zitkovich. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In arXiv preprint arXiv:2307.15818, 2023.

[25] W. Huang, C. Wang, R. Zhang, Y. Li, J. Wu, and L. Fei-Fei. Voxposer: Composable 3d value maps for robotic manipulation with language models. arXiv preprint arXiv:2307.05973, 2023.

[26] A. Padalkar, A. Pooley, A. Jain, A. Bewley, A. Herzog, A. Irpan, A. Khazatsky, A. Rai, A. Singh, A. Brohan, et al. Open x-embodiment: Robotic learning datasets and rt-x models. arXiv preprint arXiv:2310.08864, 2023.

[27] R. Chekroun, M. Toromanoff, S. Hornauer, and F. Moutarde. Gri: General reinforced imitation and its application to vision-based autonomous driving. Robotics, 12(5):127, 2023.

[28] D. Chen, V. Koltun, and P. Krähenbühl. Learning to drive from a world on rails. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 15590–15599, 2021.

[29] M. Toromanoff, E. Wirbel, and F. Moutarde. End-to-end model-free reinforcement learning for urban driving using implicit affordances. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 7153–7162, 2020.

[30] W. Zeng, W. Luo, S. Suo, A. Sadat, B. Yang, S. Casas, and R. Urtasun. End-to-end interpretable neural motion planner. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 8660–8669, 2019.

[31] B. Wei, M. Ren, W. Zeng, M. Liang, B. Yang, and R. Urtasun. Perceive, attend, and drive: Learning spatial attention for safe self-driving. In 2021 IEEE International Conference on Robotics and Automation (ICRA), pages 4875–4881. IEEE, 2021.

[32] P. Hu, A. Huang, J. Dolan, D. Held, and D. Ramanan. Safe local motion planning with selfsupervised freespace forecasting. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 12732–12741, 2021.

[33] S. Casas, A. Sadat, and R. Urtasun. Mp3: A unified model to map, perceive, predict and plan. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition pages 14403–14412, 2021.

[34] Y. Hu, J. Yang, L. Chen, K. Li, C. Sima, X. Zhu, S. Chai, S. Du, T. Lin, W. Wang, et al. Planning-oriented autonomous driving. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 17853–17862, 2023.

[35] K. Renz, K. Chitta, O.-B. Mercea, A. Koepke, Z. Akata, and A. Geiger. Plant: Explainable planning transformers via object-level representations. arXiv preprint arXiv:2210.14222, 2022.

[36] L. Chen, P. Wu, K. Chitta, B. Jaeger, A. Geiger, and H. Li. End-to-end autonomous driving: Challenges and frontiers. arXiv preprint arXiv:2306.16927, 2023.

[37] A. Hu, L. Russell, H. Yeo, Z. Murez, G. Fedoseev, A. Kendall, J. Shotton, and G. Corrado. Gaia-1: A generative world model for autonomous driving. arXiv preprint arXiv:2309.17080, 2023.

[38] Z. Yang, X. Jia, H. Li, and J. Yan. A survey of large language models for autonomous driving. arXiv preprint arXiv:2311.01043, 2023.

[39] D. Wu, W. Han, T. Wang, X. Dong, X. Zhang, and J. Shen. Referring multi-object tracking. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 14633–14642, 2023.

[40] A. Geiger, P. Lenz, C. Stiller, and R. Urtasun. Vision meets robotics: The kitti dataset. The International Journal of Robotics Research, 32(11):1231–1237, 2013.

[41] T. Deruyttere, S. Vandenhende, D. Grujicic, L. Van Gool, and M.-F. Moens. Talk2car: Taking control of your self-driving car. arXiv preprint arXiv:1909.10838, 2019.

[42] D. Wu, W. Han, T. Wang, Y. Liu, X. Zhang, and J. Shen. Language prompt for autonomous driving. arXiv preprint arXiv:2309.04379, 2023.

[43] T. Qian, J. Chen, L. Zhuo, Y. Jiao, and Y.-G. Jiang. Nuscenes-qa: A multi-modal visual question answering benchmark for autonomous driving scenario. arXiv preprint arXiv:2305.14836, 2023.

[44] H. Caesar, V. Bankiti, A. H. Lang, S. Vora, V. E. Liong, Q. Xu, A. Krishnan, Y. Pan, G. Baldan, and O. Beijbom. nuscenes: A multimodal dataset for autonomous driving. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 11621–11631, 2020.

[45] J. Kim, A. Rohrbach, T. Darrell, J. Canny, and Z. Akata. Textual explanations for self-driving vehicles. In Proceedings of the European conference on computer vision (ECCV), pages 563– 578, 2018.

[46] Y. Xu, X. Yang, L. Gong, H.-C. Lin, T.-Y. Wu, Y. Li, and N. Vasconcelos. Explainable objectinduced action decision for autonomous vehicles. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 9523–9532, 2020.

[47] E. Sachdeva, N. Agarwal, S. Chundi, S. Roelofs, J. Li, B. Dariush, C. Choi, and M. Kochenderfer. Rank2tell: A multimodal driving dataset for joint importance ranking and reasoning. arXiv preprint arXiv:2309.06597, 2023.

[48] S. Malla, C. Choi, I. Dwivedi, J. H. Choi, and J. Li. Drama: Joint risk localization and captioning in driving. In Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision, pages 1043–1052, 2023.

[49] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, D. Zhou, et al. Chain-ofthought prompting elicits reasoning in large language models. Advances in Neural Information Processing Systems, 35:24824–24837, 2022.

[50] A. Dosovitskiy, L. Beyer, A. Kolesnikov, D. Weissenborn, X. Zhai, T. Unterthiner, M. Dehghani, M. Minderer, G. Heigold, S. Gelly, et al. An image is worth 16x16 words: Transformers for image recognition at scale. arXiv preprint arXiv:2010.11929, 2020.

[51] B. Jiang, S. Chen, Q. Xu, B. Liao, J. Chen, H. Zhou, Q. Zhang, W. Liu, C. Huang, and X. Wang. Vad: Vectorized scene representation for efficient autonomous driving. arXiv preprint arXiv:2303.12077, 2023.

[52] OpenAI. Gpt-4 technical report, 2023.

[53] T. Khurana, P. Hu, A. Dave, J. Ziglar, D. Held, and D. Ramanan. Differentiable raycasting for self-supervised occupancy forecasting. In European Conference on Computer Vision, pages 353–369. Springer, 2022.

[54] S. Hu, L. Chen, P. Wu, H. Li, J. Yan, and D. Tao. St-p3: End-to-end vision-based autonomous driving via spatial-temporal feature learning. In European Conference on Computer Vision pages 533–549. Springer, 2022.

[55] L. Xu, H. Huang, and J. Liu. Sutd-trafficqa: A question answering benchmark and an efficient network for video reasoning over traffic events. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 9878–9888, 2021.

[56] J.-T. Zhai, Z. Feng, J. Du, Y. Mao, J.-J. Liu, Z. Tan, Y. Zhang, X. Ye, and J. Wang. Rethinking the open-loop evaluation of end-to-end autonomous driving in nuscenes. arXiv preprint arXiv:2305.10430, 2023.

[57] X. Yue, Y. Ni, K. Zhang, T. Zheng, R. Liu, G. Zhang, S. Stevens, D. Jiang, W. Ren, Y. Sun, et al. Mmmu: A massive multi-discipline multimodal understanding and reasoning benchmark for expert agi. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 9556–9567, 2024.

[58] B. Li, R. Wang, G. Wang, Y. Ge, Y. Ge, and Y. Shan. Seed-bench: Benchmarking multimodal 1lms with generative comprehension. arXiv preprint arXiv:2307.16125, 2023.

[59] L. Yu, P. Poirson, S. Yang, A. C. Berg, and T. L. Berg. Modeling context in referring expressions. In Computer Vision-ECCV 2016: 14th European Conference, Amsterdam, The Netherlands, October 11-14, 2016, Proceedings, Part II 14, pages 69–85. Springer, 2016.

[60] C. Sima, K. Renz, K. Chitta, L. Chen, H. Zhang, C. Xie, P. Luo, A. Geiger, and H. Li. Drivelm Driving with graph visual question answering. arXiv preprint arXiv:2312.14150, 2023.

[61] X.ai. Grok-1.5 vision preview. https://x.ai/blog/grok-1.5v, 2024.

[62] X. Chu, L. Qiao, X. Lin, S. Xu, Y. Yang, Y. Hu, F. Wei, X. Zhang, B. Zhang, X. Wei, et al. Mobilevlm: A fast, reproducible and strong vision language assistant for mobile devices. arXiv preprint arXiv:2312.16886, 2023.

[63] Q. Team. Introducing qwen1.5, February 2024. URL https://qwenlm.github.io/blog/ qwen1.5/.

[64] G. Team, T. Mesnard, C. Hardin, R. Dadashi, S. Bhupatiraju, S. Pathak, L. Sifre, M. Rivière, M. S. Kale, J. Love, et al. Gemma: Open models based on gemini research and technology. arXiv preprint arXiv:2403.08295, 2024.

[65] S. Hu, Y. Tu, X. Han, C. He, G. Cui, X. Long, Z. Zheng, Y. Fang, Y. Huang, W. Zhao, et al. Minicpm: Unveiling the potential of small language models with scalable training strategies. arXiv preprint arXiv:2404.06395, 2024.

[66] M. Abdin, S. A. Jacobs, A. A. Awan, J. Aneja, A. Awadallah, H. Awadalla, N. Bach, A. Bahree, A. Bakhtiari, H. Behl, et al. Phi-3 technical report: A highly capable language model locally on your phone. arXiv preprint arXiv:2404.14219, 2024.

[67] H. Liu, C. Li, Y. Li, and Y. J. Lee. Improved baselines with visual instruction tuning. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 26296–26306, 2024.

[68] X. Zhai, B. Mustafa, A. Kolesnikov, and L. Beyer. Sigmoid loss for language image pretraining. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 11975–11986, 2023.

[69] J.-B. Alayrac, J. Donahue, P. Luc, A. Miech, I. Barr, Y. Hasson, K. Lenc, A. Mensch, K. Millican, M. Reynolds, et al. Flamingo: a visual language model for few-shot learning. Advances in neural information processing systems, 35:23716–23736, 2022.

[70] B. He, H. Li, Y. K. Jang, M. Jia, X. Cao, A. Shah, A. Shrivastava, and S.-N. Lim. Malmm: Memory-augmented large multimodal model for long-term video understanding. arXiv preprint arXiv:2404.05726, 2024.

[71] J. Hu, L. Shen, and G. Sun. Squeeze-and-excitation networks. In Proceedings of the IEEE conference on computer vision and pattern recognition, pages 7132–7141, 2018.

[72] Y. Li, F. Wei, C. Zhang, and H. Zhang. Eagle: Speculative sampling requires rethinking feature uncertainty. arXiv preprint arXiv:2401.15077, 2024.

[73] T. Cai, Y. Li, Z. Geng, H. Peng, and T. Dao. Medusa: Simple framework for accelerating llm generation with multiple decoding heads, 2023.

## A SUP-AD Dataset

## A.1 Meta-actions

Meta-action statistics. We use the meta-action sequence to formally represent the driving strategy. Meta actions are classified into 17 categories. We show the distribution of each meta-action being the first/second/third place in the meta-action sequence, as shown in Figure 5. It indicates that the meta-actions are quite diverse in the SUP-AD dataset. We also show the distribution of the length of meta-actions per scene in Figure 6. Most scenes contain two or three meta-actions, and a few scenes with complex driving strategies contain four or more meta-actions.

Annotation of meta-actions. The meta-action sequence for each driving scene is manually annotated based on the actual driving strategy in the future frames. These meta-actions are designed to encompass a complete driving strategy and are structured to be consistent with the future trajectory of the ego vehicle. They can be divided into three primary classes:

1. Speed-control actions. Discerned from acceleration and braking signals within the ego state data, these actions include These actions can be discerned from acceleration and braking signals within the ego state data. They include speed up, slow down, slow down rapidly, go straight slowly, go straight at a constant speed, stop, wait, and reverse.

2. Turning actions. Deduced from steering wheel signals, these actions consist of turn left turn right, and turn around.

3. Lane-control actions. Encompassing lane selection decisions, these actions are derived from a combination of steering wheel signals and either map or perception data. They involve change lane to the left, change lane to the right, shift slightly to the left, and shift slightly to the right.

## A.2 Scenario Categories

The SUP-AD dataset is comprised of 1,000 video clips of driving scenarios. As illustrated in Figure 7, it encompasses a wide range of driving scenarios, spanning over 40 categories. Below are explanations for some of the scenarios:

AEB Data: Automatic Emergency Braking (AEB) data.

Road Construction: A temporary work zone with caution signs, barriers, and construction equipment ahead.

Close-range Cut-ins: A sudden intrusion into the lane of the ego vehicle by another vehicle

Roundabout: A type of traffic intersection where vehicles travel in a continuous loop.

Animals Crossing Road: Animals crossing the road in front of the ego vehicle.

Braking: Brake is pressed by human driver of the ego vehicle.

Traffic Police Officers: Traffic police officers managing and guiding traffic

Blocking Traffic Lights: A massive vehicle obscuring the visibility of the traffic signal.

Cutting into Other Vehicle: Intruding into the lane of another vehicle ahead.

Ramp: A curved roadway that connects the main road to the branch road in highway.

Debris on the Road: Road with different kinds of debris.

Narrow Roads: Narrow roads that require cautious navigation.

Pedestrians Popping Out: Pedestrians popping out in front of the ego vehicle, requiring slowing down or braking.

People on Bus Posters: Buses with posters, which may interfere the perception system.

![](images/103e09812ee8c6ad8e172683f95a2a591fc3f28a4d45a553df35c0c3490a049f.jpg)  
Figure 5: Distribution of each meta action being the first, second, and third place of the meta action sequence, respectively.

![](images/bc9640f76969e346ee22fd98691077db81df138a99a77f557d213a0199c9240d.jpg)  
Figure 6: Distribution of the length of meta actions per scene.

![](images/71e1843ef8245f425e1d0148cabc50729a93286f504c663c47ca05436cab6c5c.jpg)  
Figure 7: Diverse driving scenarios in the SUP-AD dataset.

Merging into High Speed: Driving from a low-speed road into a high-speed road, requiring speeding up.

Barrier Gate: Barrier gate that can be raised obstructing the road.

Fallen Trees: Fallen trees on the road, requiring cautious navigation to avoid potential hazards.

Complex Environments: Complex driving environments that requiring cautious navigation.

Mixed Traffic: A congested scenario where cars, pedestrians, and bicycles appear on the same or adjacent roadway.

Crossing Rivers: Crossing rivers by driving on the bridge.

![](images/7e9e54538fd142b2eed9da00df893dbcb6754003317ed3d919c891a0c0d7ea7d.jpg)  
Figure 8: An example of overturned bicycles and motorcycles in the SUP-AD dataset. A bicycle has fallen in front of the ego vehicle, requiring the ego vehicle to change lanes.

Screen: Roads with screens on one side, which may interfere the perception system.

Herds of Cattle and Sheep: A rural road with herds of cattle and sheep, requiring careful driving to avoid causing distress to these animals.

Vulnerable Road Users: Road users which are more susceptible to injuries while using roads, such as pedestrians, cyclists, and motorcyclists.

Road with Gallet: A dusty road with gallet scattered across the surface.

The remaining scenario categories are: Motorcycles and Trikes, Intersection, People carrying Umbrella, Vehicles Carrying Cars, Vehicles Carrying Branches, Vehicles with Pipes, Strollers, Children, Tunnel, Down Ramp, Sidewalk Stalls, Rainy Day, Crossing Train Tracks, Unprotected U-turns, Snowfall, Large Vehicles Invading, Falling Leaves, Fireworks, Water Sprinklers, Potholes, Overturned Motorcycles, Self-ignition and Fire, Kites, Agricultural Machinery.

## A.3 Annotation Examples

We provide more examples of annotation contents in Figure 8, 9, 10, 11, 12, and 13. The scenario categories of these examples are overturned bicycles and motorcycles, herds of cattle and sheep, collapsed trees, crossing rivers, barrier gate, and snowfall respectively.

![](images/64de93ae260e8ac2e43195379fc446ef8cf2f0816d3339bf75ebd4fc366f13b6.jpg)  
Figure 9: An example of herds of cattle and sheep in the SUP-AD dataset. A group of cattle move slowly in front of the ego vehicle, requiring the ego vehicle to proceed slowly and maintain a safe distance from the cattle.

Scene Summary: The ego vehicle is moving forward on the current road, and a tree suddenly falls towards the ego vehicle from the left front side.  
![](images/be8b1da47ddbef3cbb5b935395fd3ad8f8f2f391238c9072f207f7674a4abbb3.jpg)  
Figure 10: An example of collapsed trees in the SUP-AD dataset. A tree suddenly falls towards the ego vehicle, requiring the ego vehicle to decelerate immediately.

![](images/91564826e1261fe3fc1dfabe8d433993a8ddf748548075d7c1c3366ed25659a7.jpg)  
Figure 11: An example of crossing rivers in the SUP-AD dataset. The ego vehicle is going across a bridge of which width allows only a single vehicle to pass, requiring the ego vehicle to drive without stopping.

Scene Summary: The ego vehicle turns left towards the park entrance, a horizontal bar is blocking the entrance ahead.  
![](images/c965b38420be4f47718a20bcf6b1ec17ac2dfdcdc66de129110c91b219a199d6.jpg)  
Figure 12: An example of barrier gate in the SUP-AD dataset. A horizontal barrier blocks the entrance of a park, requiring the ego vehicle to stop and wait for permission to continue.

Decision Description:"Continue to move forward cautiously at a slow speed."  
![](images/00f4bef8d582df519644b26b6babe893f27daaa922710797f2b3699b7194ed57.jpg)  
Figure 13: An example of snowfall in the SUP-AD dataset. Most of the road is covered by snow, requiring the ego vehicle to move forward cautiously by following the snow-free tire tracks.

## B Evaluation Method

The ability of an autonomous driving system to accurately interpret driving scenes and make logical, suitable decisions is of paramount importance. As presented in this paper, the evaluation of VLMs in autonomous driving concentrates on two primary components: the evaluation of scene description/analysis and the evaluation of meta-actions.

## B.1 Scene Description/Analysis Evaluation

In terms of scene description/analysis evaluation, the process of interpreting and articulating driving scenes is subject to inherent subjectivity, as there are numerous valid ways to express similar descriptions textually, which makes it difficult to effectively evaluate the scene description using a fixed metric. To overcome this challenge, we utilize GPT-4 to evaluate the similarity between the scene descriptions generated by the model and the manually annotated ground truth. Initially, we prompt GPT-4 to extract individual pieces of information from each scene description. Subsequently, we score and aggregate the results based on the matching status of each extracted piece of information.

The ground truth labels for scene descriptions encompass both environment descriptions and event summaries. Environmental condition description includes weather conditions, time conditions, road environment, and lane conditions. Event summaries are the characteristics and influence of critical objects. We employ GPT-4 to extract unique key information from both environment descriptions and event summaries. The extracted information is then compared and quantified. Each matched pair is assigned a score, which is estimated based on the extent of the matching, whether complete, partial, or absent. Instances of hallucinated information incur a penalty, detracting from the overall score. The aggregate of these scores constitutes the scene description score.

$$
\mathrm { S c o r e } = \frac { 1 . 0 \times n _ { \mathrm { m a t c h e d } } + 0 . 5 \times n _ { \mathrm { p a r t i a l } } } { n _ { \mathrm { g t } } }\tag{2}
$$

The prompt for GPT-4 in evaluating scene descriptions is carefully designed, as shown in Table 10. Initially, a role prompt is employed to establish as an intelligent and logical evaluator, possessing a comprehensive understanding of appropriate driving styles. This is followed by specifying the input format, which informs GPT-4 that its task involves comparing an output description with a ground truth description. This comparison is based on the extraction and analysis of key information from both descriptions. Lastly, the prompt outlines the criteria for scoring, as well as the format for the evaluation output, ensuring a structured and systematic approach to the evaluation process.

![](images/84b2917506aef58c031515a0bb9aaecd703881cf0ec6d0afb2d6b2b0a376f687.jpg)  
Table 10: Evaluation process of scene description by GPT-4. Our proposed evaluation method is not only capable of extracting and evaluating information from structured scene descriptions but is also applicable to unstructured descriptions.

## B.2 Meta-action Evaluation

The evaluation process for the meta-action sequence must consider both the quantity and the sequential arrangement of the matched meta-actions. We employ dynamic programming to compare the model's output and the annotated ground truth. Our dynamic programming approach is similar to the method utilized in identifying the longest common subsequence, albeit with two supplementary considerations.

The first consideration acknowledges the unequal weighting of different meta-actions. For instance, certain meta actions such as “Slow Down", “Wait", and “Go Straight Slowly" exhibit a greater emphasis on attitude rather than action. The presence or absence of these actions from a meta-action sequence does not alter the basic semantic essence of driving decisions but rather modifies the driv-

![](images/1f01ae922bc8d6b7c820fb2d0f0e067211101b4567a79b9fc0d21de7de43b9a8.jpg)  
Table 11: Example of generating alternative action sequences by GPT-4.

The state of dynamic programming is saved in a 2D matrix, wherein each row corresponds to a meta action in the ground truth action sequence, and each column corresponds to a meta action in the model output action sequence, noted as $S ^ { r , c }$ . The dynamic programming initiates recursive calculations beginning from the first meta action of both sequences. Each element of the 2D matrix encompasses the optimal total score at the current matching position, as well as the preceding matching condition that yielded the optimal matching. In our dynamic programming algorithm, three transition equations govern distinct cases: $S _ { \mathrm { m i s s i n g } }$ for missing matching, $S _ { \mathrm { r e d u n d a n t } }$ for redundant matching, and $S _ { \mathrm { { m a t c h i n g } } }$ for successful matching. Successful matching occurs when the meta action is identical at the $r ^ { t h }$ position in the reference sequence and the $c ^ { t h }$ position in the model-generated sequence. In the case of missing matching, the meta action at the $r ^ { t h }$ position in the reference sequence is unmatched, prompting a comparison with the $r - 1 ^ { t h }$ position in the reference sequence and the $c ^ { t h }$ position in the model-generated sequence. Conversely, redundant matching implies that the meta action at the $c ^ { t h }$ position in the model-generated sequence is unmatched, leading to further examination of the $r ^ { t h }$ position in the reference and the $c - 1 ^ { t h }$ position in the model-generated sequence. The transformation equations for these cases are as follows:

$$
\begin{array} { r l } & { \quad S _ { \mathrm { m i s s i n g } } ^ { r , c } = S ^ { r - 1 , c } - p _ { \mathrm { m i s s i n g } } , } \\ & { \quad S _ { \mathrm { r e d u n d a n t } } ^ { r , c } = S ^ { r , c - 1 } - p _ { \mathrm { r e d u n d a n t } } , } \\ & { \quad S _ { \mathrm { m a t c h i n g } } ^ { r , c } = S ^ { r - 1 , c - 1 } + s _ { \mathrm { m a t c h i n g } } , } \\ & { \quad S ^ { r , c } = \operatorname* { m a x } ( S _ { \mathrm { m i s s i n g } } ^ { r , c } , S _ { \mathrm { r e d u n d a n t } } ^ { r , c } , S _ { \mathrm { m a t c h i n g } } ^ { r , c } ) , } \end{array}\tag{3}
$$

where $s _ { \mathrm { m a t c h i n g } } = 1 . 0$ represents the reward score after a successful matching. If an action considered missing or redundant is classified as a conservative action, the penalties $p _ { \mathrm { m i s s i n g } }$ and $p _ { \mathrm { r e d u n d a n t } }$ are quantified as half of $s _ { \mathrm { m a t c h i n g } } ,$ i.e., 0.5. Conversely, if an action is not conservative, both penalties are assigned the same magnitude as $s _ { \mathrm { m a t c h i n g } } ,$ i.e., 1.0. This approach is based on the premise that omitting a crucial meta action or inaccurately introducing a non-existent one equally hampers the effectiveness of the action sequence. The final score $S c o r e _ { \mathrm { a c t i o n } }$ should be divided by the length of the selected reference meta-action sequence, formulated as follow:

$$
S c o r e _ { \mathrm { a c t i o n } } = { \frac { S ^ { r , c } } { N _ { r } } }\tag{4}
$$

## C Qualitative Results

To further demonstrate the effectiveness and robustness of our DriveVLM, we provide additional visualization results in Figure 14, 15, 16, 17, and 18. In Figure 14, DriveVLM recognizes the slowly moving vehicle ahead and provides a driving decision to change lanes for overtaking. In Figures 15 and 16, DriveVLM accurately identifies the type of unconventional vehicles and a fallen tree, demonstrating its capability in recognizing long-tail objects. In Figure 17, the traffic police signaling to proceed with hand gestures has been accurately captured by DriveVLM. In Figure 18, DriveVLM successfully recognizes the road environment of a roundabout and generates a planned trajectory with a curved path.

![](images/b7d728514b6fc2207f20630c4f4e2d8d9aa30e4c3f7e1dd7fc7add3f73a3c5a1.jpg)

![](images/4e8164281a3219b4661c4147cd29cf2818f59a93a0a27c6fc2a7cdadeaaf0e3e.jpg)

These are a few frames taken at regular intervals from a driving video:<img></img>...<img></img>. Suppose you are driving in this scenario, please describe the scene condition.

![](images/96e9388343e0fadf5dd10f888a555a3a7289bf456ef9b09d8f33387fc4b54283.jpg)

Scene Condition:

Weather:Sunny.

![](images/920ea56fb189f33fe9b148f3b2af495c97e9d6fabb00aa916e2324742973e609.jpg)

Time:Night.

Road Environment:Urban.

Lane Options:Own Lane, Right Lane.

Ego Lane Position: Leftmost Lane.

Please list the critical objects in the front view that affect ego vehicle's next driving decisions, and box them step by step.

![](images/7267f5710bce0f2e9522f3434e5e8d65a31c57d1af937d316b0728ababccb29a.jpg)

![](images/9abcd76863b4614052c114043d50589051c82fcb26e188c7254ac02da3395510.jpg)

There are 1 critical object in the front view. The objects include ['Sedan'].   
Object 1:<ref>Sedan</ref><box>(404,519),(488,633)</box>.

Matching 2D Objects: - Sedan at img region [404, 519, 488, 633].

Matching Information: Object in the BEV view [18.86, 1.77], history trajectory: [(13.9,1.3), (9.2,0.8), (4.3,0.4), (-0.1,0.2)]. Describe the characteristics of the object and indicte its influence based on the matching information

![](images/52e1e7ded780aa1ee777be3735113611e5f84c9f8b1aa6ac5ff1c52579f8e9df.jpg)

![](images/9620055086d30840b06317b146303fb8de61e9fdd87acbafb0fddf5ee24573ed.jpg)

Characteristics: Driving slowly ahead in the ego lane. | Influence: Blocking the future path of the ego vehicle.

Ego-States:

Historical Trajectory (last 2 seconds): [(-5.30,0.04), (-10.47,0.16), (-15.38,0.36), (-20.47,0.65)] Navigation: MAINTAIN.

![](images/40be5716920af2c8bb8e4c4d2006aeadc29881e58c5fe6dafe8bc24f4661b1ad.jpg)

Please make a summary of the current scene based on the information provided and your previous analysis.

![](images/a691170337d18d66cfecba7a8bc99129e9ac07014bb8a358323fdd13acc6a846.jpg)

Scene Condition:

Weather:Sunny.

Time:Day.

Road Environment:Urban.

Lane Options:Own Lane, Left Lane.

Ego Lane Position:Rightmost Lane.

Critical Events: The ego vehicle maintains a constant speed along the current lane, with a slow-moving sedan ahead and no oncoming vehicles in the right rear lane.

Based on the above analysis and the current scenario, please determine the driving meta actions and decisions you will take next.

![](images/dfee0bedcc3d3463be4052be6b4ae3b6a96d1dd32acaf7eca957aec090c2018d.jpg)

![](images/aadd94765eb232972b651b46b8e5dceca550a500ccf8dca419e66fd2faf3e994.jpg)

Meta Actions: ['Change lane to the right', 'Go straight at a constant speed'].   
Decisions: Maintain a safe distance from the vehicle ahead, change lanes to the right, and continue driving.

Based on the above decisions and analysis, please plan the 3s future trajectory of the ego vehicle.

![](images/9d9d0cd614e87390d9354aea732c155dc7480c157ebbee1e261fccdd59a7fc76.jpg)

![](images/5717903411f4cecec9834290861207d2c35db51e0db896efcc09a84c5ff9cb09.jpg)

[(5.3,0.0),(10.5,0.1),(15.6,0.2),(20.7,0.3),(25.8,0.4),(30.9,0.5)]

![](images/9e13f9c4043aaa329938a63dbaf490a517f2ed07e9a31b66f484ab216fa88d36.jpg)

![](images/1249d1ecc8a5e71ed9fa3a2c09746e34384606b29a5396d8b006664a2556cc92.jpg)  
System Prompt

![](images/e32dc8c0cda1691a4135320d63a545b0d20b8ae523967d26ecbf871bea65c571.jpg)  
Planned Trajectory  
Figure 14: Visualization of DriveVLM's output. DriveVLM recognizes the slowly moving vehicle ahead and provides a driving decision for changing lanes to overtake.

![](images/e99ac2ce3b3c819f81048dd9b8a7a91e2ae21ad8bf495efde529f07dd23ebb3f.jpg)

![](images/07d7bca6b0e6a3d300bd2fe376c1ef88a1689e58fe7bf004adccfb78f50eb0c4.jpg)

These are a few frames taken at regular intervals from a driving video:<img></img>...<img></img>. Suppose you are driving in this scenario, please describe the scene condition.

![](images/fd61fb3eaa34f080efafc22afd088a6a653cbbfd7198b45056967c53d6a4c737.jpg)

Scene Condition:

Weather:Sunny.

![](images/b88654aea3f159492708b93ce155ea2f1cefa018b78d09a6e2613215cf292061.jpg)

Time:Day.

Road Environment:Urban.

Lane Options:Own Lane, Left Lane.

Ego Lane Position:Rightmost Lane.

Please list the critical objects in the front view that affect ego vehicle's next driving decisions, and box them step by step.

![](images/b2caef62651d99dbe634be55f1fe47153e8118a4bcfcf0f9b6806663f9bc4bd1.jpg)

![](images/ad2c6948ea858cc8f4d56f01607ddda568a39b1fb78f8a2525283520492aa105.jpg)

There are 1 critical object in the front view. The objects include ['Water-spraying vehicle'].   
Object 1:<ref>Water-spraying vehicle</ref><box>(374,446),(456,596)</box>.

Matching 2D Objects: - Water-spraying vehicle at img region [374, 446, 456, 596]. Matching Information: Object in the BEV view [26.03, 4.09], history trajectory: [(26.3,4.1), (27.0,4.0), (28.2,4.1), (29.6,4.2)]. Describe the characteristics of the object and indicte its influence based on the matching information

![](images/3f7b0c673d77c415393e04cf22564e95bcde0cada83c1ea6b7c60c86f11c70d3.jpg)

![](images/811715b9607bd4c6e9d6c6ba91aff75216e399aa3d1ac15deb7b93217f5328d1.jpg)

Characteristics: Water-spraying vehicle ahead on the current road. | Influence: No influence.

Ego-States:

Historical Trajectory (last 2 seconds):[(-4.17,-0.00),(-8.51,-0.02),(-12.97,-0.06),(-17.60,-0.10)] Navigation: MAINTAIN.

![](images/aa9e627f469760a25d1a84bd04fd3a398dab9d29988789cf4895f97a29994618.jpg)

Please make a summary of the current scene based on the information provided and your previous analysis.

![](images/471c79453ba183f289902a8536beecb278e9786b49ec31b9df202ffa3839e7a3.jpg)

Scene Condition :

Weather:Sunny.

Time:Day.

Road Environment:Urban.

Lane Options:Own Lane, Left Lane.

Ego Lane Position:Rightmost Lane.

Critical Events: The ego vehicle is driving straight on the current road, and there is a water-spraying vehicle ahead on the road, which has no impact on the ego vehicle.

Based on the above analysis and the current scenario, please determine the driving meta actions and decisions you will take next.

![](images/bbc65cc896dce83343b9f206ce26a320ea921159e667c5c98789e7bde087d291.jpg)

![](images/1486d3c9f3e5bd3103907234e16de02eff0a202f45b7211005d457574888ca4e.jpg)

Meta Actions: ['Go straight at a constant speed'].

Decisions: Maintain a safe distance from the vehicle ahead and continue driving.

Based on the above decisions and analysis, please plan the 3s future trajectory of the ego vehicle.

![](images/63f8261e4d483b248fe5ca3dd4474c53c8af1c504b86184359c90bddecfb258c.jpg)

![](images/554e9ace61d37de45874ba9ac2846a7af81f9eed4b70ae64d9cc2c10943006f6.jpg)  
[(4.1,-0.0),(8.2,-0.0),(12.2,-0.0),(16.2,-0.1),(20.1,-0.1),(24.0,-0.1)]

![](images/ddaf635203166b7e8552ff8f1cfae25933c7ee1dd8a3db3ea4b75235b3fc6f45.jpg)

![](images/ed1ec86ff7e0b58fcbad6c7409e83f4c8ce02bec905e91bc46f2a4709e6c966d.jpg)  
System Prompt  
Planned Trajectory  
Figure 15: Visualization of DriveVLM's output. DriveVLM has identified the type of the unconventional vehicle ahead.

![](images/fc948112385a4c7bb32745042b32ae0d623fc21b47e652f97c2877dfd972345a.jpg)

These are a few frames taken at regular intervals from a driving video:<img></img>...<img></img>. Suppose you are driving in this scenario, please describe the scene condition.

![](images/138c9d4bace0ed6dc4c591277fd63a644de47bd4c9db591248fcbfe54700de50.jpg)

Scene Condition:

Weather:Sunny.

![](images/c9c9e4d90a8a7130661e304767a0b28d173932852b0ff4b35bc54ef128b66ac9.jpg)

Time:Day.

Road Environment:Urban.

Lane Options:Own Lane, Left Lane.

Ego Lane Position:Rightmost Lane.

Please list the critical objects in the front view that affect ego vehicle's next driving decisions, and box them step by step.

![](images/746782e4c299dd6dcb558380452a1c92c54d8b920cd5f83272f9de7d8da432f9.jpg)

![](images/3f8bf00c563241a8a6a9582ef5b739caadf5d8a3c1c6d46239cabfd751851a2b.jpg)

There are 1 critical object in the front view. The objects include ['Fallen tree'].   
Object 1:<ref>Fallen tree</ref><box>(353,413),(483,566)</box>.

Unmatching 2D Objects: - Fallen tree at img region [353, 413, 483, 566]. Describe the characteristics of the object and indicte its influence based on the matching information

![](images/4573d161acfc2f6508560f806dd342a30094148756350a919f8206a406cba80f.jpg)

![](images/da7d888c9bd15b51d00bc3cda8f10216258cbb29d94b78d97db26a2387e7a122.jpg)

Characteristics: In the lane on the left front side of the ego vehicle. | Influence: Blocking the future path of the ego vehicle.

Ego-States:

Historical Trajectory (last 2 seconds):[(-6.21,-0.05),(-12.39,-0.20),(-18.43,-0.43),(-24.44,-0.67)] Navigation: MAINTAIN.

![](images/8d216dc497424d59da493ba303aaffa9ac16cf73c5c86c95a6a5995179cb4e4a.jpg)

Please make a summary of the current scene based on the information provided and your previous analysis.

![](images/9e1c7e87a601b389ee163bc42dc35fd67afe11f9d6388ab3adad282d07faabbb.jpg)

Scene Condition:

Weather:Sunny.

Time:Day.

Road Environment:Urban.

Lane Options:Own Lane, Left Lane.

Ego Lane Position:Rightmost Lane.

Critical Events: The ego vehicle is driving straight ahead at a constant speed in the current lane, with a fallen tree blocking the left lane ahead.

Based on the above analysis and the current scenario, please determine the driving meta actions and decisions you will take next.

![](images/da1b8af82c852e014e082578bd40c47c6c6ba890b7312728533166ac46ff9255.jpg)

![](images/6b725714f8a371f6390b06fe81f16e67ddc42d7f006cbf43458dbe38f0a6e4db.jpg)

Meta Actions: ['Slow down', 'Shift slightly to the right', 'Go straight slowly'].   
Decisions: Slow down, shift to the right to avoid the fallen tree, and continue driving.

Based on the above decisions and analysis, please plan the 3s future trajectory of the ego vehicle.

![](images/f512e91af04aed8075b73755fd846db46ea2451f56bd66df7b245b2f94d56d9c.jpg)

![](images/40e574b43c6b73c4173a19a32519306e4fd48860a1cfc55bf5e8dfc053deec49.jpg)

[(6.1,-0.0),(12.1,-0.1),(18.1,-0.2),(24.1,-0.3),(30.1,-0.4),(36.1,-0.5)]

![](images/eb9424433c1c44f3e1e987326c3dcfc3024b323b3540453eaa0c5320cf57ad35.jpg)

![](images/68e3e9add13b798e2b4e3ff18833c0ffccbe9317a83a91ccd3f774a320311c31.jpg)  
DriveVLM  
System Prompt  
Planned Trajectory  
Figure 16: Visualization of DriveVLM's output. DriveVLM precisely detect the fallen tree and its position, subsequently planning an appropriate detour trajectory.

![](images/7c25f9bfbfe6ec7adafc52ce14a4757910d0c7d60dc011bbac4b06cc8035d483.jpg)

These are a few frames taken at regular intervals from a driving video:<img></img>..<img></img>. Suppose you are driving in this scenario, please describe the scene condition.

![](images/d150b2f838b515babcd86da8b7eb3bfe659ee48b143dc323757c41087e18a44a.jpg)

Scene Condition:

Weather:Cloudy.

![](images/a5592d98bc3c88111490c0c7d6ae82e790cd7452c1ae28fddee60c7faa0f9f44.jpg)

Time:Day.

Road Environment:Urban.

Lane Options:Own Lane.

Ego Lane Position:DNA.

Please list the critical objects in the front view that affect ego vehicle's next driving decisions, and box them step by step.

![](images/3f88ed7ba939eda8ff93108ad1a41751b457d1d549aa457ecc1ebecc140f1c5e.jpg)

![](images/34e14259bb90986b7c41bf5e21a6c6c3caf76eaf866f2ee2872ce053715b6876.jpg)

There are 2 critical objects in the front view. The objects include ['Traffic police', 'Traffic police'] Object 1:<ref>Traffic police</ref><box>(134,523),(350,741)</box>. Object 2:<ref>Traffic police</ref><box>(694,525),(805,795)</box>.

Unmatching 2D Objects: - Traffic police at img region [134, 523, 350, 741]. Describe the characteristics of the object and indicte its influence based on the matching information

![](images/212640f74b0ae7a954f0f384bf0473a87215a0b645ccd799691e0fe1049df413.jpg)

![](images/1713c511edbaa9ffd91e360a18fe4f4598c629d59a7961c1ee07e3f0e3ef9c04.jpg)

Characteristics: Traffic police on the left side of the road ahead | Influence: Signaling that the ego vehicle can proceed.

- Traffic police at img region [694, 525, 805, 795].   
Describe the characteristics of the object and indicte its influence based on the matching information.

![](images/a28f43420281f4a0d36917e99a7a803f8b41d17348ace5fd0047f26705404ba0.jpg)

![](images/32b6ac16e4445e515212ad5cf0d527fddc2002873bc3bcec99050aa2eaa8893a.jpg)

Characteristics: Traffic police on the right side of the road ahead | Influence: Signaling that the ego vehicle can proceed.

Ego-States:

Historical Trajectory (last 2 seconds):[(-1.77,0.00),(-3.65,0.01),(-5.61,0.03),(-7.66,0.04)] Navigation: MAINTAIN.

![](images/569bfc63eed41b18f9203db0588bed7e73396a2a06062d74081a908b13cd5a19.jpg)

Please make a summary of the current scene based on the information provided and your previous analysis.

![](images/fff4dc8dcc67ecb60621310a4bdae40fef022a743acf6501a7504f6acde50f04.jpg)

Scene Condition:

Weather:Cloudy.

Time:Day.

Road Environment:Urban.

Lane Options:Own Lane.

Ego Lane Position:DNA.

Critical Events: The ego vehicle is driving straight, with traffic police on both sides of the road ahead signaling that it can proceed.

Based on the above analysis and the current scenario, please determine the driving meta actions and decisions you will take next.

![](images/77e63f960cbe32d451fc0acaf0290a82b28e15865366553732f6975b7f0bb152.jpg)

![](images/08512255b4477f78ec61f4ef3c5909d37f90fbca59717f41807d58ad3ea2e7ea.jpg)

Meta Actions: ['Go straight at a constant speed'].   
Decisions: Maintain a constant speed and continue driving straight.

Based on the above decisions and analysis, please plan the 3s future trajectory of the ego vehicle.

![](images/b6debc699becc2cc1cf596640f4b67568dc7b133b1bae3e2069dea9e724c99a7.jpg)

![](images/104d36e577bbb7e43dbfb399439ae74a898633eec329eaedc54a535fbc79696d.jpg)

[(1.8,0.0),(3.6,0.0),(5.5,0.0),(7.4,0.0),(9.4,0.0),(11.5,0.1)]

![](images/bd220e955117982c0b4cdc19ecd6eb2b63b55d708bb5755d8d29fe39f4044aa4.jpg)  
DriveVLM

![](images/85cbe12d33b7e00acaead9961ab012d4474a03ba30b3796ec3e47b73a19d5719.jpg)  
System Prompt  
Planned Trajectory

![](images/ffd5e2cb4788307bfb2b36535ee3ee8d353fd2a270ac08e26859f43449e6fe4e.jpg)  
Figure 17: Visualization of DriveVLM's output. The traffic police signaling to proceed with hand gestures has been accurately captured by DriveVLM.

![](images/03c83ae819ea4e670af1774180770cc214ebf1ce5583c204112109cfe90dd6b2.jpg)

![](images/6830b91ce9b38ade63eaaf8f7444ce1d2ed4ccbb0b6ce46e308af912feba0b80.jpg)  
Figure 18: Visualization of DriveVLM's output. DriveVLM successfully recognizes the road environment of a roundabout and generates a planned trajectory with a curved path.

![](images/722a919a9a675647fa44bcf470a31664953d7609b233fa0dfe76198a68aeea8a.jpg)

These are a few frames taken at regular intervals from a driving video:<img></img>...<img></img>. Suppose you are driving in this scenario, please describe the scene condition.

![](images/09bb45c9c433f7cac5953e32707a79f31835f05c6b58322ae511c1efa012487c.jpg)

Scene Condition:

Weather:Sunny.

![](images/4f2912fc9d5ef1422b55e81791fb03ca7f42d507ab42837bce924268a5d846d7.jpg)

Time:Night.

Road Environment:Roundabout.

Lane Options:Intersection.

Ego Lane Position:Do not apply.

Please list the critical objects in the front view that affect ego vehicle's next driving decisions, and box them step by step.

![](images/d970b73b02f69fa19036f52a60aa565fafa70e924739568581aaa65dfa891353.jpg)

![](images/4b45dbecf25154f6714b42e581f9cabf2a5cbfb38cecb8c66d7248f60351bff2.jpg)

There are 1 critical object in the front view. The objects include [SUV'].   
Object 1:<ref>Water-spraying vehicle</ref><box>(590,545),(955,676)</box>.

Matching 2D Objects: - SUV at img region [590, 545, 955, 676].

Matching Information: Object in the BEV view [16.23, 2.84], history trajectory: [(14.7,5.3), (13.7,7.7), (13.0,9.9), (12.8,12.4)]. Describe the characteristics of the object and indicte its influence based on the matching information

![](images/9f0e4108e1eb26f1ff932b6fddefd00a2bd0988ee55681435682979f351332d8.jpg)

![](images/c138040d3004365a488bff138ca0d5c6a9d57c1ae401664911475330213c51cf.jpg)

Characteristics: Driving around the roundabout in front of the ego vehicle. | Influence: No influence.

Ego-States:

Historical Trajectory (last 2 seconds):[(-3.04,-0.11),(-5.84,-0.42),(-8.22,-0.83),(-10.29,-1.28)] Navigation: MAINTAIN. Please make a summary of the current scene based on the information provided and your previous analysis.

![](images/e3c3f9ca9dfe8681b917caa1a5e7615446211d48138dee21ab8f5f12be1d7b9d.jpg)

Scene Condition:

![](images/14017e10c282508657144d4f09b37d372849e46345165455e572c3b006ed3212.jpg)

Weather:Sunny.

Time:Night.

Road Environment:Roundabout.

Lane Options:Intersection.

Ego Lane Position:Do not apply.

Critical Events: The ego vehicle is driving on the roundabout road, and SUV is driving around the roundabout ahead, with no impact on the ego vehicle

Based on the above analysis and the current scenario, please determine the driving meta actions and decisions you will take next.

![](images/82e5373152fe7f0e60902f529c3f329249ab66e0037ccc0ecf5306f6f4060e05.jpg)

![](images/7a41e1f401c57bafefc945aafe33ffa97094b46491500dfd5c5a2ceffa7a0b0a.jpg)

Meta Actions: ['Go straight at a constant speed', 'Turn right'].   
Decisions: Maintain a safe distance and continue driving.

Based on the above decisions and analysis, please plan the 3s future trajectory of the ego vehicle.

![](images/d6d303da5b2c61df8df612319c1e4cb2d105945c313f9ebc307130fed8c8b622.jpg)

![](images/f6054dce4ea784bc5f194af9e5463b2589c75d3d1dfcc801f5a9d13748f99064.jpg)

[(3.0,-0.1),(5.9,-0.4),(8.7,-0.9),(11.3,-1.6),(13.7,-2.7),(16.0,-4.2)]

![](images/3ecce8977c7c85093e883cd2b192614b3fc1909b89dcef2971af0c8d65a532c3.jpg)  
DriveVLM  
System Prompt  
Planned Trajectory