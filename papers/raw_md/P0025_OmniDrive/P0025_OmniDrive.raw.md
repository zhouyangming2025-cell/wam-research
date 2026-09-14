# OmniDrive: A Holistic Vision-Language Dataset for Autonomous Driving with Counterfactual Reasoning

Shihao Wang<sup>1,2∗</sup>, Zhiding Yu<sup>1†</sup>, Xiaohui Jiang<sup>3</sup>, Shiyi Lan<sup>1</sup>, Min Shi<sup>1∗</sup>, Nadine Chang<sup>1</sup>, Jan Kautz<sup>1</sup>, Ying Li<sup>3</sup>, Jose M. Alvarez<sup>1</sup>,

<sup>1</sup>NVIDIA <sup>2</sup>The Hong Kong Polytechnic University <sup>3</sup>Beijing Institute of Technology https://github.com/NVlabs/OmniDrive

![](images/2cb510b15f09232cdaa353f6a14d2a67251098407bdfe8f1a459621e23391ea1.jpg)  
Figure 1. OmniDrive is a holistic vision-language dataset for autonomous driving, utilizing counterfactual reasoning to generate high-quality QA data from simulated and actual trajectories. We explore two baseline models: Omni-Q, which designs vision-language models (VLMs) from a 3D perception standpoint, and Omni-L, which builds from VLMs to enhance 3D integration.

## Abstract

The advances in vision-language models (VLMs) have led to a growing interest in autonomous driving to leverage their strong reasoning capabilities. However, extending these capabilities from 2D to full 3D understanding is crucial for real-world applications. To address this challenge, we propose OmniDrive, a holistic vision-language dataset that aligns agent models with 3D driving tasks through counterfactual reasoning. This approach enhances decision-making by evaluating potential scenarios and their outcomes, similar to human drivers considering alternative actions. Our counterfactual-based synthetic data annotation process generates large-scale, high-quality datasets, providing denser supervision signals that bridge planning trajectories and language-based reasoning. Futher, we explore two advanced OmniDrive-Agentframeworks, namely Omni-L and Omni-Q to assess the importance of vision-language alignment versus 3D perception, revealing critical insights into designing effective LLM-agents. Significant improvements on the DriveLM Q&A benchmark and nuScenes open-loop planning demonstrate the effectiveness ofour dataset and methods.

## 1. Introduction

The recent rapid development of 2D Vision-Language Models (VLMs) [1, 20, 25] and their strong reasoning capabilities have led to a stream of applications in end-to-end autonomous driving [4, 34, 41, 48, 53]. However, extending capabilities from 2D to 3D understanding is crucial for unlocking potential in real-world applications. Although previous works [33, 42] have shown successful applications of LLM-agents in autonomous driving (AD), a holistic and principled framework from dataset to LLM-agent is needed to fully extend VLMs’ 2D understanding and reasoning capabilities to 3D geometric and spatial understanding.

Recent drive LLM-agent works feature the importance of datasets [8, 33, 34, 38, 41, 42]. Many are presented as question-answering (Q&A) datasets to train and benchmark the LLM-agent for either reasoning or planning. Noteably, benchmarks that involve planning [8, 41, 42] still resort to using expert trajectories for an open-loop setting on real-world sessions (e.g. nuScenes). However, recent studies [22, 54] reveal several limitations of open-loop evaluation: implicit biases towards ego status, overly simple planning scenarios, and easy overfit to expert trajectories.

OmniDrive: VLM Dataset. Expert driving actions provide only sparse supervision [5, 23], primarily reflecting safe trajectories without delving into the complex decision-making and underlying reasoning processes. Relying solely on this sparse supervision makes it challenging to effectively optimize end-to-end driving models. Counterfactual reasoning involves evaluating potential scenarios and their outcomes, similar to how human drivers consider various possibilities to make safer decisions. Therefore, we combine counterfactual reasoning with the chain-of-thought capabilities of VLMs, as shown in Fig. 1. This approach creates a more effective connection between planning trajectories and language-based reasoning.

Additionally, we found that using simulated trajectories for counterfactual reasoning efficiently identifies key traffic elements in a scene. This process creates a structured and simplified 3D scene representation, making it easier for GPT to understand 3D scenes and generate more effective 3D driving Q&A data. To ensure quality, we utilize a rule-based checklist to assess the consequences of potential trajectories. Based on these results, we design prompts for GPT-4 to generate coherent Q&A, which helps identify which objects require attention and evaluate outcomes based on trajectories. A human-in-the-loop approach is employed in designing the checklist and prompts, ensuring comprehensive coverage of all scenarios. This methodology ensures that data generation is both reliable and interpretable.

Omni-L/Q: LLM-agents. Designing effective Driving Vision-Language Models [8, 41, 48] (VLMs) presents a complex and underexplored challenge. A fundamental question is whether to build upon existing 2D VLMs[25, 26] and align them with 3D space, or to integrate current 3D perception stacks [21, 27, 35, 49] into a vision-language framework. To address this, we explore two promising Large Language Model (LLM) frameworks Omni-L and Omni-Q. The Omni-L utilizes state-of-the-art (SoTA) MLP-projection approach (LLaVA [24, 25]), which enhances the performance of existing VLMs. The Omni-Q is based on the BEV architecture employed by StreamPETR [27, 28, 46], incorporating Q-Former’s [20] design to investigate the synergy between LLMs and traditional autonomous driving perception tasks. By addressing crucial considerations in the design of autonomous driving LLM-Agents, we conduct a comprehensive comparison of these paradigms in tasks such as counterfactual reasoning and open-loop planning. Our findings indicate that migrating 2D VLMs to 3D is a more straightforward approach compared to integrating traditional 3D perception stacks into VLMs.

Contributions. We propose OmniDrive, a holistic framework for end-to-end autonomous driving with counterfactualcentric dataset and LLM-agents. With OmniDrive,

(1) We introduce a counterfactual-based 3D driving Q&A design pipeline that allows for scalable, high-quality data generation.

(2) Models pre-trained on OmniDrive showed significant improvement when tested on DriveLM Q&A benchmark and nuScenes open-loop planning, demonstrating the effectiveness and quality of our dataset.

(3) We explore and compare two advanced frameworks Omni-L and Omni-Q, providing critical insights for designing effective LLM-Agents.

## 2. OmniDrive

We propose OmniDrive, the counterfactual-based synthetic data on nuScenes [3] with high quality Q&A pairs covering perception, reasoning and planning in 3D domain.

OmniDrive features a human-in-the-loop Q&A generation pipeline using rule-based checklist and GPT-4. As shown in Fig. 2, the data generation process can be divided into: planning-oriented key-frame selection, counterfactualbased checklist and prompt design, human-in-the-loop quality assurance, and large-scale data iteration.

## 2.1. Planning-oriented key-frame selection.

Autonomous driving datasets often contain significant redundancy, so we focus on selecting representative key-frames to prototype our data processing strategy. We begin by extracting CLIP [39] embeddings from the front view images of the nuScenes [3] dataset to capture diverse perceptual elements such as landmarks, traffic lights, and lane markings. Using these embeddings, we apply the K-means algorithm to cluster the data, selecting 20% of the cluster centers. This ensures that the most semantically representative data is chosen, covering various static and dynamic traffic elements. Next, we further filter the data based on the vehicle’s future trajectory. We apply K-means clustering again, this time selecting 200 cluster centers. These centers represent different vehicle dynamics, reflecting driving behaviors such as stopping, moving forward, turning left, turning right, U-turns, accelerating, decelerating, and maintaining constant speed.

This approach effectively compresses the dataset, ensuring that our algorithm design can comprehensively cover all these scenarios. By selecting keyframes, we streamline the process, allowing for more effective rule-based checklist design and prompt iteration. Once the checklist and prompts are verified to cover these scenarios, we iterate on the dataset at a larger scale. This targeted approach ensures that the most relevant data is used for further development.

![](images/a82e6c4e9496a554f95082704078b270d126eabb00a940dde08968d47989df73.jpg)  
Figure 2. The proposed counterfactual-based synthetic Q&A data generation pipeline integrates semantic key-frame selection, counterfactualbased checklist and prompt design, and human-in-the-loop quality checks to create high-quality Q&A pairs.

## 2.2. Counterfactual checklist and prompt design.

Although GPT-4 has powerful ablitity in long-context processing, it cannot effectively understand 3D scenes when directly inputting images, 3D objects, lane markings, and scene definitions. It’s difficult to determine the driving status of vehicles or the relationships between traffic elements. This issue becomes more severe as the number of traffic elements in the scene increases.

To address this, we draw inspiration from counterfactual reasoning and represented the entire scene centered around simulated planned trajectories. In this section, we primarily introduce the types of prompts we input into GPT-4 and how we design checklist on counterfactual principles to enhance the quality of Q&A data generation.

Simulated trajectories. We first cluster the driving trajectories from the entire nuScenes dataset. We then classified the cluster centers into categories such as stopping, moving forward, turning left, turning right, making U-turns, accelerating, decelerating, and maintaining a constant speed. In each scene, we simulated these driving behaviors to assess their feasibility. and designed a checklist to determine whether these trajectories violated any traffic rules.

Counterfactual checklist. For fixed categories, such as object collisions, road boundary collisions, and running red lights, we use the 3D object detection, centerline and road element topology annotations from nuScenes [3] and OpenLane-v2 [45] dataset. We design a rule-based checklist to validate these scenarios.

However, relying solely on annotated perception elements cannot cover all traffic rules. Therefore, we convert the simulated driving trajectories into high-level decision-making information (this step also involves rule design, such as object and lane assignment, and determining lane-changing behavior, etc.). We then use GPT-4 to analyze the images and assess whether the driving behavior is safe and complies with traffic regulations. We found that using GPT-4 for counterfactual reasoning based on the high-level decision making still achieves good accuracy and interpretability.

Expert trajectory. We also take the log replay trajectory from nuScenes [3] as input prompt. The expert trajectories are classified into different types for high-level decision making. We also identify an object as “close”, if its minimum distance to the trajectory is smaller than 10 meters in the next 3 seconds. The close objects are then listed below the expert trajectory.

Caption. To improve the quality of Q&A data generation, we utilize counterfactual principles to structure and simplify the 3D perception annotations, avoiding the need to input lengthy and unordered scene information. To provide additional contextual information, we also prompt GPT-4 to generate captions, enhancing OCR capabilities and the recognition of open-world object categories.

When both the image and extensive scene information are fed into GPT-4 simultaneously, it tends to overlook details in the image. Therefore, we first prompt GPT-4 to produce a scene description based on multi-view input only. As shown in the top block of Tab. 1, we stitch the three frontal views and three rear views into two separate images and feed them into GPT-4. We prompt GPT-4 to include the following details: 1) mention weather, time of day, scene type, and other image contents; 2) understand the general direction of each view (e.g. the first frontal view being front-left); and 3) avoid mentioning the contents from each view independently, instead describing positions relative to the ego vehicle.

## 2.3. Q&A generation.

In the bottom block of the Tab. 1, we describe the different types of Q&A responses obtained by using the above context information:

Scene description. We directly take caption (prompt type 1 in Tab. 1) as the answer of scene description.

Attention. Given the simulated and expert trajectories, run simulation to identify close objects. At the same time, we also allowed GPT-4 to use its own common sense to identify threatening traffic elements.

Counterfactual reasoning. Given the simulated trajectories, we simulate to check if the trajectories violate the traffic rules, such as run a red light, collision to other objects or the road boundary.

![](images/509cadef5b417e75142e6bbe9c3e38f9ce5dfdc214ea82a0bd60c74d64eaae79.jpg)  
Table 1. An example to illustrate the counterfactual-based data generation pipeline. The top block shows contexts such as captions and boxes used to prompt GPT-4, and the bottom block shows the four types of responses.

Decision making and planning. We present the high-level decision making as well as the expert trajectory and use GPT-4 to reason why this trajectory is safe, given the previous prompt and response information as context.

General conversation. We also prompt GPT-4 with generating multi-turn dialogues based on caption information and image content, involving the object countings, color, relative position, and OCR-type tasks. We found that this approach helps improve the model’s recognition of long-tail objects.

We design checklists on selected keyframes, followed by prompt design and Q&A generation. We manually verify the quality of the Q&A generated from these data. Once our design meets the generalization requirements, we initiate large-scale data generation. This process involves human-inthe-loop quality assurance and large-scale data iteration.

## 3. OmniDrive-agent

Designing effective Driving VLMs is a complex challenge. We consider two primary design approaches:

To explore these approaches, we propose two frameworks: Omni-L and Omni-Q. Omni-L leverages the MLP from LLaVA [25] to align multi-view image features to language embedding. Omni-Q is inspired by the BEV architecture of StreamPETR [46] and incorporates Q-Former’s [20] design to build the interaction between LLMs and traditional autonomous driving tasks.

![](images/6f0499cfa86f9428a3fa1403362c2cd46b8459847e4d230b1b789a42276eebad.jpg)  
Figure 3. Overall pipeline of Omni-L and Omni-Q. The Omni-L. Omni-L follows the 2D VLM design of LLAVA, introducing 3D positional encoding and using MLP layers for vision-language alignment. Omni-Q is based on 3D BEV perception, aligning its architecture with the Q-Former design.

Both Omni-L/Q use a shared visual encoder to extract multi-view image features $F _ { m } \in \mathbb { R } ^ { N \times C \times H \times W }$ The extracted features are combined with the positional encoding $P _ { m }$ and then fed into the projector. The visual features are aligned with the text in the projector and then fed into the large language model for text generation tasks. The main difference between Omni-L and Omni-Q lies in the design of the projector. One prioritizes vision-language alignment, while the other focuses on 3D perception tasks.

## 3.1. Omni-Q

The Transformer decoder in Q-Former [20] and the sparse query-based 3D perception models, represented by Stream-PETR [46], share highly similar architecture designs. To enhance the localization abilities of the VLMs, we consider introducing the design of 3D position encoding $P _ { m }$ and the supervision of the query-based perception models to the training of VLMs. As shown in Fig. 3, in QFormer, we initialize the detection queries and carrier queries and perform self-attention to exchange their information, which can be summarized by the following formula:

$$
\begin{array} { r l r } & { } & { ( Q , K , V ) = ( [ Q _ { c } , Q _ { d } ] , [ Q _ { c } , Q _ { d } ] , [ Q _ { c } , Q _ { d } ] ) , } \\ & { } & { \tilde { Q } = \mathbf { M u l t i - h e a d A t t e n t i o n } ( Q , K , V ) . } \end{array}\tag{1}
$$

[·] is the concatenation operation. For simplicity, we omit the position encoding. Then these queries collect information from multi-view images via:

$$
\begin{array} { r l r } & { } & { ( Q , K , V ) = ( [ Q _ { c } , Q _ { d } ] , P _ { m } + F _ { m } , F _ { m } ) , } \\ & { } & { \tilde { Q } = \mathbf { M } \mathbf { u } \mathbf { l } \mathbf { i } \mathbf { - } \mathbf { h } \mathbf { e a d } \mathbf { A } \mathbf { t t e n t i o n } ( Q , K , V ) . } \end{array}\tag{2}
$$

After that, the perception queries $Q _ { d }$ are used to predict the categories and coordinates of the foreground elements. The carrier queries $Q _ { c }$ are sent to a MLP to align with the dimension of LLM tokens $( e . g .$ . 4096 dimensions in LLaMA2-7B [43]) and further used for text generation following LLaVA [25].

In Omni-Q, the carrier queries play the role of the visuallanguage alignment. Additionally, this design enables carrier queries to leverage the geometric priors provided by the 3D position encoding, while also allowing them to leverage query-based representations acquired through the 3D perception tasks.

## 3.2. Omni-L

Omni-L follows the design of LLaVA [25], utilizing a simple MLP for aligning the visual-language embedding space. We extend LLaVA’s single image input to multiple images, flattening the multi-view image features $F _ { m }$ and feeding them into the large language model. To distinguish different viewpoints, we add 3D position encoding $P _ { m }$ to each image patch. However, for training stability, these position encoding weights are initialized to zero.

## 3.3. Training strategy

The training of Omni-L/Q comprises two stages: 2D-Pretraining and 3D-Finetuning. In the initial stage, we pretrain the VLMs on 2D image tasks to initialize the Q-Former/MLP Projector. Following this, the model is finetuned on 3D-related driving tasks (e.g. motion planning, coutner-factual reasoning, etc.). In both stages, we calculate the text generation loss without considering contrasting learning and matching loss for in BLIP-2 [20].

## 4. Experiment

## 4.1. Implementation details

Our model uses EVA-02-L [12] as the vision encoder. It applies masked image modeling to distill CLIP [39], which can extract language-aligned vision features.

During the 2D pre-training stage, the training data and strategies, including batchsize, learning rate, and optimizer are the same as LLaVA v1.5’s [24]. In the finetuning stage, the model is trained by AdamW [29] optimizer with a batch size of 16. The learning rate for the projector is 4e-4, while the visual encoder and the LLM’s learning rates are 2e-5. The cosine annealing policy is used for training stability.

<table><tr><td rowspan="2">Method</td><td colspan="2">Ego Status</td><td colspan="4">L2 (m) ↓</td><td colspan="4">Collision (%) ↓</td><td colspan="4">Intersection (%) ↓</td></tr><tr><td>BEV</td><td>Planner</td><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td></tr><tr><td>ST-P3</td><td></td><td></td><td>1.59†</td><td>2.64†</td><td>3.73†</td><td>2.65†</td><td>0.69†</td><td>3.62†</td><td>8.39†</td><td>4.23†</td><td>2.53†</td><td>8.17†</td><td>14.4†</td><td>8.37†</td></tr><tr><td>UniAD</td><td>=</td><td></td><td>0.59</td><td>1.01</td><td>1.48</td><td>1.03</td><td>0.16</td><td>0.51</td><td>1.64</td><td>0.77</td><td>0.35</td><td>1.46</td><td>3.99</td><td>1.93</td></tr><tr><td>UniAD</td><td>√</td><td>√</td><td>0.20</td><td>0.42</td><td>0.75</td><td>0.46</td><td>0.02</td><td>0.25</td><td>0.84</td><td>0.37</td><td>0.20</td><td>1.33</td><td>3.24</td><td>1.59</td></tr><tr><td>VAD-Base</td><td>=</td><td>=</td><td>0.69</td><td>1.22</td><td>1.83</td><td>1.25</td><td>0.06</td><td>0.68</td><td>2.52</td><td>1.09</td><td>1.02</td><td>3.44</td><td>7.00</td><td>3.82</td></tr><tr><td>VAD-Base</td><td>√</td><td>√</td><td>0.17</td><td>0.34</td><td>0.60</td><td>0.37</td><td>0.04</td><td>0.27</td><td>0.67</td><td>0.33</td><td>0.21</td><td>2.13</td><td>5.06</td><td>2.47</td></tr><tr><td>Ego-MLP</td><td>-</td><td>√</td><td>0.15</td><td>0.32</td><td>0.59</td><td>0.35</td><td>0.00</td><td>0.27</td><td>0.85</td><td>0.37</td><td>0.27</td><td>2.52</td><td>6.60</td><td>2.93</td></tr><tr><td>BEV-Planner</td><td></td><td></td><td>0.30</td><td>0.52</td><td>0.83</td><td>0.55</td><td>0.10</td><td>0.37</td><td>1.30</td><td>0.59</td><td>0.78</td><td>3.79</td><td>8.22</td><td>4.26</td></tr><tr><td>BEV-Planner++</td><td>√</td><td>√</td><td>0.16</td><td>0.32</td><td>0.57</td><td>0.35</td><td>0.00</td><td>0.29</td><td>0.73</td><td>0.34</td><td>0.35</td><td>2.62</td><td>6.51</td><td>3.16</td></tr><tr><td>Omni-Q Omni-Q++</td><td>-</td><td>-</td><td>1.15</td><td>1.96</td><td>2.84</td><td>1.98</td><td>0.80</td><td>3.12</td><td>7.46</td><td>3.79</td><td>1.66</td><td>3.86</td><td>8.26</td><td>4.59</td></tr><tr><td></td><td>√</td><td>√</td><td>0.14</td><td>0.29</td><td>0.55</td><td>0.33</td><td>0.00</td><td>0.13</td><td>0.78</td><td>0.30</td><td>0.56</td><td>2.48</td><td>5.96</td><td>3.00</td></tr><tr><td>Omni-L‡</td><td></td><td></td><td>1.47</td><td>2.43</td><td>3.38</td><td>2.43</td><td>0.29</td><td>2.84</td><td>6.54</td><td>3.22</td><td>1.23</td><td>3.27</td><td>7.21</td><td>3.90</td></tr><tr><td>Omni-L++‡</td><td></td><td>✓</td><td>0.31</td><td>0.62</td><td>1.06</td><td>0.66</td><td>0.35</td><td>2.41</td><td>0.92</td><td>0.64</td><td>2.78</td><td>2.48</td><td>5.62</td><td>3.63</td></tr><tr><td>Omni-L</td><td></td><td></td><td>1.43</td><td>2.34</td><td>3.24</td><td>2.34</td><td>0.23</td><td>1.47</td><td>4.00</td><td>1.90</td><td>0.90</td><td>2.82</td><td>6.16</td><td>3.29</td></tr><tr><td>Omni-L++</td><td></td><td>✓</td><td>0.15</td><td>0.36</td><td>0.70</td><td>0.40</td><td>0.06</td><td>0.27</td><td>0.72</td><td>0.35</td><td>0.49</td><td>1.99</td><td>4.86</td><td>2.45</td></tr></table>

Table 2. Comparison on nuScenes Open-loop planning. For a fair comparison, we referred to the reproduced results in BEV-Planner [22]. †: The official implementation of ST-P3 (ID-0) utilized partial erroneous ground truth. ‡: The model was trained using only the trajectory prediction task for open-loop planning, without utilizing our generated OmniDrive Q&A data.

We also explore alternative architectures. The BEV-MLP approach uses LSS method [35, 36] to transform perspective features into a BEV feature map. We implement temporal modeling following SOLOFusion [35]. The BEV features will be consecutively fed into a MLP projector and a LLM. In the following section, both our models – Omni-Q and Omni-L – are trained on OmniDrive unless stated otherwise.

## 4.2. Dataset & metrics

OmniDrive The proposed OmniDrive dataset involves captioning, open-loop planning and counterfactual reasoning tasks. In this section, we elaborate on how we assess the performance of models on our dataset. For caption-related tasks, such as scene description and the selection of attention objects, we utilize the commonly employed language-based metrics to evaluate the sentence similarity CIDEr [44]. Following BEV-Planner [22], Collision Rate and Intersection Rate with the road boundary are adopted to evaluate the performance of Open-loop planning. To evaluate the performance of the counterfactual reasoning, we ask GPT-3.5 to extract keywords based on the predictions. The keywords include ‘safety,’ ‘collision,’, ‘running a red light,’ and ‘out of the drivable area.’ Then we compare extracted keywords with the ground truth to calculate the Precision and Recall for each category of the accident.

DriveLM The DriveLM [41] dataset is designed for end-toend autonomous driving, featuring Graph Visual Question

<table><tr><td>Dataset</td><td>Acc.</td><td>CG.</td><td>Blue</td><td>RL.</td><td>Cl.</td><td>Mat.</td><td>Score</td></tr><tr><td>DriveLM</td><td>0.60</td><td>0.65</td><td>0.50</td><td>0.71</td><td>0.07</td><td>0.36</td><td>0.53</td></tr><tr><td>+OmniDrive</td><td>0.70</td><td>0.65</td><td>0.52</td><td>0.73</td><td>0.13</td><td>0.37</td><td>0.56</td></tr><tr><td>+LLaVA665k</td><td>0.76</td><td>0.63</td><td>0.53</td><td>0.73</td><td>0.15</td><td>0.37</td><td>0.57</td></tr><tr><td>+Both</td><td>0.78</td><td>0.64</td><td>0.54</td><td>0.73</td><td>0.15</td><td>0.37</td><td>0.58</td></tr></table>

Table 3. The performance of Omni-L on the DriveLM benchmark. We added pre-training with OmniDrive and LLaVA665k, which significantly improves performance.

Answering (GVQA) to handle complex dependencies. It includes 696 scenes from the nuScenes dataset, with 4,072 samples and around 0.3 million image-question pairs. These questions cover perception, prediction, planning, and behavior, helping to fine-tune models and improve performance. DriveLM’s evaluation metrics include language metrics like BLEU, ROUGE L, and CIDEr for text generation, accuracy for multiple-choice questions, and the ChatGPT Score for open-ended Q&A. The Match Score assesses the alignment of predicted 2D boxes with ground truth objects. The final score is the weighted combination of GPT Score (0.4), Language Score (0.2), Match Score (0.2), and Accuracy (0.2).

## 4.3. Discussion on open-loop planning

We compare Omni-L and Omni-Q with previous SoTA vision-based planners on nuScenes open-loop planning in Tab. 2. The VLM-based open-loop planning can also achieve comparable performance to SoTA methods when using ego status. However, as mentioned in BEV-planner [22], encoding the ego status significantly improves the metrics across all methods. We found that large language models tend to overfit more easily to ego status. Omni-Q exhibits weaker

<table><tr><td rowspan="2">Ablation</td><td rowspan="2">Exp.</td><td colspan="2">Safe</td><td colspan="2">Red Light</td><td colspan="2">Collision</td><td colspan="2">Drivable Area</td></tr><tr><td>P</td><td>R</td><td>P</td><td>R</td><td>P R</td><td>P</td><td></td><td>R</td></tr><tr><td rowspan="3">Architecture</td><td>Omni-L</td><td>72.1</td><td>58.0</td><td>59.2</td><td>63.3</td><td>34.3</td><td>71.3</td><td>49.1</td><td>59.2</td></tr><tr><td>Omni-Q</td><td>70.7</td><td>49.0</td><td>57.6</td><td>58.3</td><td>32.3</td><td>72.6</td><td>48.5</td><td>58.6</td></tr><tr><td>BEV-MLP</td><td>70.2</td><td>17.3</td><td>48.7</td><td>53.6</td><td>31.1</td><td>70.4</td><td>32.4</td><td>56.6</td></tr><tr><td>Perception</td><td>No Lane</td><td>67.7</td><td>57.3</td><td>58.1</td><td>59.6</td><td>31.0</td><td>56.7</td><td>47.9</td><td>56.8</td></tr><tr><td>Supervision</td><td>No Object &amp; Lane</td><td>69.0</td><td>57.8</td><td>51.3</td><td>61.2</td><td>30.0</td><td>53.2</td><td>45.3</td><td>57.1</td></tr></table>

Table 4. Analysis on OmniDrive counterfactual reasoning and open-loop planning (without ego status). P and R represent Precision and Recall respectively. “No Object” and “No Lane” indicate no corresponding 3D perception supervision in Omni-Q.

VLM capabilities, making the overfitting more pronounced compared to Omni-L, as evidenced by a lower L2 error but a higher collision rate. Omni-L performs significantly better than Omni-Q without using ego status. Additionally, if the model is trained solely on trajectory prediction tasks, the distribution modeling capability of the language model can degrade, leading to poor open-loop planning results. However, training with our Q&A data without ego status effectively mitigates this issue, reducing the collision rate from 3.22% to 1.90% and the intersection rate from 3.90% to 3.29%. Critically, training Omni-L with both OmniDrive and ego status leads to significant improvements across metrics.

## 4.4. Results on DriveLM dataset

Our dataset, OmniDrive, plays a crucial role in pre-training. Training with only DriveLM dataset leads to an average score of 53%. However, incorporating our pre-training data boosts performance by 3%. Additionally, when combined with LLaVA665K pre-training, our data still provides a significant improvement. Although our annotations are highly automated, the OmniDrive dataset maintains high quality through counterfactual-based checklist and human-in-theloop validation.

## 4.5. Planning with counterfactual reasoning

We evaluated our OmniDrive counterfactual reasoning tasks in Tab. 4. We observe that Omni-L, designed from a VLM perspective, performs better on average (e.g. 72.1% Precision and 58.0% Recall in safety tasks) compared to Omni-Q. However, Omni-Q benefits from 3D perception supervision, showing improvements in tasks like collision detection (32.3% Precision and 72.6% Recall) compared to those without 3D supervision. The combination of BEV features and MLP results in poorer performance due to pre-training gaps (e.g. 17.3% Recall in safety tasks).

## 4.6. Ablation study & analysis

In Tab. 5, we illustrate the performance of different architectures on OmniDrive counterfactual reasoning, language ability, and nuScenes open-loop planning. It shows a positive correlation between language ability and performance in these tasks. Omni-L excels with a counterfactual AP of 53.7%, AR of 63.0%, and a Language CIDEr score of 73.2, alongside better open-loop planning metrics (Col 1.90%, Inter 3.29%). In contrast, Omni-Q, despite benefiting from 3D perception, has lower results with a counterfactual AP of 52.3%, AR of 59.6%, and a CIDEr score of 68.6, due to weaker foundational language skills. This highlights the need for future exploration on aligning traditional 3D perception stacks with language spaces to enhance performance.

## 5. Related works

## 5.1. End-to-end autonomous driving

The objective of end-to-end autonomous driving is to create a fully differentiable system that spans from sensor input to control signals [37, 52, 55]. The current technical road-map is primarily divided into two paths: open-loop autonomous driving and closed-loop autonomous driving.

In the open-loop autonomous driving, the training and evaluation processes are generally conducted on logreplayed real world datasets [38]. Pioneering work UniAD [14] and VAD [17] integrate modularized design of perception tasks such as object detection, tracking, and semantic segmentation into a unified planning framework. However, Ego-MLP [54] and BEV-Planner [22] highlight the limitations of open-loop end-to-end driving benchmarks. In these benchmarks, models may overfit the ego-status information to achieve unreasonably high performance. Researchers are addressing the challenges in open-loop evaluation by introducing closed-loop benchmarks. Recent works, e.g., MILE [13], ThinkTwice [16], VADv2 [5] leverage CARLA [9] as the simulator, which enables the creation of virtual environments with feedback from other agents. Researchers urgently need a reasonable way to evaluate endto-end autonomous driving systems in the real world. VLM models enable us to perform interpretable analysis and conduct counterfactual reasoning based on a specific trajectory, thereby enhancing the safety redundancy of the agent.

<table><tr><td rowspan="2">Abaltion</td><td rowspan="2">Exp.</td><td colspan="2">Counterfactual</td><td rowspan="2">Language CIDEr ↑</td><td colspan="2">Open-loop</td></tr><tr><td>AP (%) ↑</td><td>AR (%) ↑</td><td>Col(%) ↓</td><td>Inter(%) ↓</td></tr><tr><td rowspan="3">Architecture</td><td>Omni-L</td><td>53.7</td><td>63.0</td><td>73.2</td><td>1.90</td><td>3.29</td></tr><tr><td>Omni-Q</td><td>52.3</td><td>59.6</td><td>68.6</td><td>3.79</td><td>4.59</td></tr><tr><td>BEV-MLP</td><td>45.6</td><td>49.5</td><td>59.5</td><td>4.43</td><td>8.56</td></tr><tr><td>Perception</td><td>No Lane</td><td>51.2</td><td>57.6</td><td>67.8</td><td>4.65</td><td>8.71</td></tr><tr><td>Supervision</td><td>No Object &amp; Lane</td><td>48.9</td><td>57.3</td><td>67.8</td><td>6.77</td><td>8.43</td></tr></table>

Table 5. Analysis on nuScenes open-loop planning and OmniDrive counterfactual reasoning and language ability.

## 5.2. Vision-language models

vision-language models leverage LLMs and various modalities’ encoders to successfully bridge the gap between language and other modalities and perform well on multimodal tasks ranging from visual question answer, captioning, and open-world detection. Some VLMs such as CLIP [39] and ALIGN [15] utilize contrastive learning to create a similar embedding space for both language and vision. More recently, others such as BLIP-2 [20] explicitly targets multimodal tasks and takes multimodal inputs. For these models, there are two common techniques in order to align language and other input modalities: self-attention and cross-attention. LLaVa [25], PaLM-E [10], PaLI [6], and RT2 [56] utilize self-attention for alignment by interleaving or concatenating image and text tokens in fixed sequence lengths. However, self-attention based VLMs are unable to handle high resolution inputs and are unsuitable for autonomous driving with multi-camera high solution images. Conversely, Flamingo [1], Qwen-VL [2], BLIP-2 [20], utilize crossattention and are able to extract a fixed number of visual tokens regardless of image resolution. Because of this, our model utilizes Qformer architecture from BLIP-2 to handle our high resolution images.

## 5.3. Drive LLM-agents and benchmarks

Drive LLM-agents. Given LLM’ high performance and ability to align modalities with language, there is a rush to incorporate VLMs/LLMs with autonomous driving (AD). Most AD VLMs methods attempt to create explainable autonomous driving with end-to-end learning. DriveGPT4 leverages LLMs to generate reasons for car actions while also predicting car’s next control signals [53]. Similarly, Drive Anywhere proposes a patch-aligned feature extraction for VLMs that allow it to provide text query-able driving decisions [47]. Other works leverage VLMs through graphbased VQA (DriveLM) [41] or chain-of-thought (CoT) design [42, 50]. They explicitly solve multiple driving tasks alongside typical VLM tasks, such as generating scene description and analysis, prediction, and planning.

Benchmarks. To evaluate AD perception and planning, there are various datasets that capture perception, planning, steering, motion data (ONCE [32], nuScenes [3], CARLA [9], Waymo [11]). However, datasets with more comprehensive lanugage annotations are required to evaluate Drive LLM methods. Datasets focused on perception and tracking include reasoning, or descriptive like captions range from nuScenes-QA [38], NuPrompt, [51]. HAD and Talk2Car both contain human like advice to best navigate the car [7, 19], while LaMPilot contains labels meant to evaluate transition from human commands to drive action [30]. Beyond scene descriptions, DRAMA [31] and Rank2Tell [40] focus on risk object localization. Contrastly, BDD-X, Reason2Drive focus on car explainability by providing reasons behind ego car’s action and behavior [18, 33, 34]. LingoQA [33] has introduced counterfactual questions into the autonomous driving QA dataset. We believe that the interpretability and safety redundancy of autonomous driving in the open-loop setting can be further enhanced by applying counterfactual reasoning to 3D trajectory analysis.

## 6. Conclusion

We present OmniDrive, a holistic framework designed to advance end-to-end autonomous driving using LLM-agents. By introducing a counterfactual-based 3D driving Q&A pipeline, we enable scalable, high-quality data generation that significantly enhances decision-making capabilities. Pretrained models on OmniDrive exhibit significant improvements on the DriveLM QA benchmark and nuScenes openloop planning, underscoring the effectiveness and quality of our dataset. Furthermore, our exploration of two advanced frameworks, Omni-L and Omni-Q, provides valuable insights into the design of effective LLM-agents, highlighting the advantages of vision-language alignment in 3D spaces. These frameworks demonstrate the potential for improved reasoning and perception by integrating language models with 3D environmental understanding.

Limitations. The simulation of counterfactual outcomes, despite moving beyond single trajectories, does not yet consider reactions from other agents. As research on closed-loop planning simulators progresses, we aim to use closed-loop results to enhance effectiveness.

## 7. Acknowledgments

The team would like to give special thanks to the NVIDIA TSE Team, including Le An, Chengzhe Xu, Yuchao Jin, and Josh Park, for their exceptional work on the TensorRT deployment of OmniDrive.

## References

[1] Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katherine Millican, Malcolm Reynolds, et al. Flamingo: a visual language model for few-shot learning. In NeurIPs, 2022. 1, 8

[2] Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, Sinan Tan, Peng Wang, Junyang Lin, Chang Zhou, and Jingren Zhou. Qwen-VL: A frontier large vision-language model with versatile abilities. arXiv:2308.12966, 2023. 8

[3] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuScenes: A multimodal dataset for autonomous driving. In CVPR, 2020. 2, 3, 8

[4] Long Chen, Oleg Sinavski, Jan Hunermann, Alice Karn-¨ sund, Andrew James Willmott, Danny Birch, Daniel Maund, and Jamie Shotton. Driving with LLMs: Fusing objectlevel vector modality for explainable autonomous driving. arXiv:2310.01957, 2023. 1

[5] Shaoyu Chen, Bo Jiang, Hao Gao, Bencheng Liao, Qing Xu, Qian Zhang, Chang Huang, Wenyu Liu, and Xinggang Wang. VADv2: End-to-end vectorized autonomous driving via probabilistic planning. arXiv:2402.13243, 2024. 2, 7

[6] Xi Chen, Xiao Wang, Soravit Changpinyo, AJ Piergiovanni, Piotr Padlewski, Daniel Salz, Sebastian Goodman, Adam Grycner, Basil Mustafa, Lucas Beyer, et al. PaLI: A jointly-scaled multilingual language-image model. arXiv:2209.06794, 2022. 8

[7] Thierry Deruyttere, Simon Vandenhende, Dusan Grujicic, Luc Van Gool, and Marie Francine Moens. Talk2Car: Taking control of your self-driving car. In EMNLP-IJCNLP, 2019. 8

[8] Xinpeng Ding, Jinahua Han, Hang Xu, Xiaodan Liang, Wei Zhang, and Xiaomeng Li. Holistic autonomous driving understanding by bird’s-eye-view injected multi-modal large models. arXiv:2401.00988, 2024. 1, 2

[9] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. Carla: An open urban driving simulator. In CoRL, 2017. 7, 8

[10] Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, et al. Palm-e: An embodied multimodal language model. arXiv:2303.03378, 2023. 8

[11] Scott Ettinger, Shuyang Cheng, Benjamin Caine, Chenxi Liu, Hang Zhao, Sabeek Pradhan, Yuning Chai, Ben Sapp, Charles R. Qi, Yin Zhou, Zoey Yang, Aur’elien Chouard, Pei Sun, Jiquan Ngiam, Vijay Vasudevan, Alexander McCauley, Jonathon Shlens, and Dragomir Anguelov. Large scale interactive motion forecasting for autonomous driving: The waymo open motion dataset. In ICCV, 2021. 8

[12] Yuxin Fang, Quan Sun, Xinggang Wang, Tiejun Huang, Xinlong Wang, and Yue Cao. EVA-02: A visual representation for neon genesis. arXiv:2303.11331, 2023. 5

[13] Anthony Hu, Gianluca Corrado, Nicolas Griffiths, Zak Murez, Corina Gurau, Hudson Yeo, Alex Kendall, Roberto Cipolla, and Jamie Shotton. Model-based imitation learning for urban driving. In NeurIPS, 2022. 7

[14] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, et al. Planning-oriented autonomous driving. In CVPR, 2023. 7

[15] Chao Jia, Yinfei Yang, Ye Xia, Yi-Ting Chen, Zarana Parekh, Hieu Pham, Quoc Le, Yun-Hsuan Sung, Zhen Li, and Tom Duerig. Scaling up visual and vision-language representation learning with noisy text supervision. In ICML, 2021. 8

[16] Xiaosong Jia, Penghao Wu, Li Chen, Jiangwei Xie, Conghui He, Junchi Yan, and Hongyang Li. Think Twice before Driving: Towards scalable decoders for end-to-end autonomous driving. In CVPR, 2023. 7

[17] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. VAD: Vectorized scene representation for efficient autonomous driving. arXiv:2303.12077, 2023. 7

[18] Jinkyu Kim, Anna Rohrbach, Trevor Darrell, John Canny, and Zeynep Akata. Textual explanations for self-driving vehicles. ECCV, 2018. 8

[19] Jinkyu Kim, Teruhisa Misu, Yi-Ting Chen, Ashish Tawari, and John Canny. Grounding human-to-vehicle advice for self-driving vehicles. In CVPR, 2019. 8

[20] Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. BLIP-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. In ICML, 2023. 1, 2, 5, 8

[21] Zhiqi Li, Hanming Deng, Tianyu Li, Yangyi Huang, Chonghao Sima, Xiangwei Geng, Yulu Gao, Wenhai Wang, Yang Li, and Lewei Lu. BEVFormer++ : Improving bevformer for 3d camera-only object detection: 1st place solution for waymo open dataset challenge 2022. 2023. 2

[22] Zhiqi Li, Zhiding Yu, Shiyi Lan, Jiahan Li, Jan Kautz, Tong Lu, and Jose M Alvarez. Is ego status all you need for openloop end-to-end autonomous driving? arXiv:2312.03031, 2023. 1, 6, 7

[23] Zhenxin Li, Kailin Li, Shihao Wang, Shiyi Lan, Zhiding Yu, Yishen Ji, Zhiqi Li, Ziyue Zhu, Jan Kautz, Zuxuan Wu, Yu-Gang Jiang, and Jose M. Alvarez. Hydra-mdp: End-toend multimodal planning with multi-target hydra-distillation, 2024. 2

[24] Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. Improved baselines with visual instruction tuning. arXiv:2310.03744, 2023. 2, 6

[25] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. NeurIPS, 2023. 1, 2, 4, 5, 8

[26] Haotian Liu, Chunyuan Li, Yuheng Li, Bo Li, Yuanhan Zhang, Sheng Shen, and Yong Jae Lee. LLaVA-NeXT: Improved reasoning, ocr, and world knowledge, 2024. 2

[27] Yingfei Liu, Tiancai Wang, Xiangyu Zhang, and Jian Sun. PETR: Position embedding transformation for multi-view 3d object detection. arXiv:2203.05625, 2022. 2

[28] Yingfei Liu, Junjie Yan, Fan Jia, Shuailin Li, Qi Gao, Tiancai Wang, Xiangyu Zhang, and Jian Sun. PETRv2: A unified framework for 3d perception from multi-camera images. arXiv:2206.01256, 2022. 2

[29] Ilya Loshchilov and Frank Hutter. SGDR: Stochastic gradient descent with warm restarts. arXiv:1608.03983, 2016. 6

[30] Yunsheng Ma, Can Cui, Xu Cao, Wenqian Ye, Peiran Liu, Juanwu Lu, Amr Abdelraouf, Rohit Gupta, Kyungtae Han, Aniket Bera, et al. LaMPilot: An open benchmark dataset for autonomous driving with language model programs. arXiv:2312.04372, 2023. 8

[31] Srikanth Malla, Chiho Choi, Isht Dwivedi, Joon Hee Choi, and Jiachen Li. DRAMA: Joint risk localization and captioning in driving. In WACV, 2023. 8

[32] Jiageng Mao, Minzhe Niu, Chenhan Jiang, Xiaodan Liang, Yamin Li, Chaoqiang Ye, Wei Zhang, Zhenguo Li, Jie Yu, Chunjing Xu, et al. One million scenes for autonomous driving: Once dataset. 2021. 8

[33] Ana-Maria Marcu, Long Chen, Jan Hunermann, Alice Karn-¨ sund, Benoit Hanotte, Prajwal Chidananda, Saurabh Nair, Vijay Badrinarayanan, Alex Kendall, Jamie Shotton, et al. LingoQA: Video question answering for autonomous driving. arXiv:2312.14115, 2023. 1, 8

[34] Ming Nie, Renyuan Peng, Chunwei Wang, Xinyue Cai, Jianhua Han, Hang Xu, and Li Zhang. Reason2Drive: Towards interpretable and chain-based reasoning for autonomous driving. arXiv:2312.03661, 2023. 1, 8

[35] Jinhyung Park, Chenfeng Xu, Shijia Yang, Kurt Keutzer, Kris Kitani, Masayoshi Tomizuka, and Wei Zhan. Time will tell: New outlooks and a baseline for temporal multi-view 3d object detection. arXiv:2210.02443, 2022. 2, 6

[36] Jonah Philion and Sanja Fidler. Lift, splat, shoot: Encoding images from arbitrary camera rigs by implicitly unprojecting to 3d. In ECCV, 2020. 6

[37] Aditya Prakash, Kashyap Chitta, and Andreas Geiger. Multimodal fusion transformer for end-to-end autonomous driving. In CVPR, 2021. 7

[38] Tianwen Qian, Jingjing Chen, Linhai Zhuo, Yang Jiao, and Yu-Gang Jiang. NuScenes-QA: A multi-modal visual question answering benchmark for autonomous driving scenario. arXiv:2305.14836, 2023. 1, 7, 8

[39] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In ICML, 2021. 2, 5, 8

[40] Enna Sachdeva, Nakul Agarwal, Suhas Chundi, Sean Roelofs, Jiachen Li, Mykel Kochenderfer, Chiho Choi, and Behzad Dariush. Rank2Tell: A multimodal driving dataset for joint importance ranking and reasoning. In WACV, 2024. 8

[41] Chonghao Sima, Katrin Renz, Kashyap Chitta, Li Chen, Hanxue Zhang, Chengen Xie, Ping Luo, Andreas Geiger, and Hongyang Li. DriveLM: Driving with graph visual question answering. arXiv:2312.14150, 2023. 1, 2, 6, 8

[42] Xiaoyu Tian, Junru Gu, Bailin Li, Yicheng Liu, Chenxu Hu, Yang Wang, Kun Zhan, Peng Jia, Xianpeng Lang, and Hang Zhao. DriveVLM: The convergence of autonomous driving

and large vision-language models. arXiv:2402.12289, 2024. 1, 8

[43] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. arXiv:2307.09288, 2023. 5

[44] Ramakrishna Vedantam, C Lawrence Zitnick, and Devi Parikh. CIDEr: Consensus-based image description evaluation. In CVPR, 2015. 6

[45] Huijie Wang, Tianyu Li, Yang Li, Li Chen, Chonghao Sima, Zhenbo Liu, Bangjun Wang, Peijin Jia, Yuting Wang, Shengyin Jiang, et al. OpenLane-V2: A topology reasoning benchmark for unified 3d hd mapping. NeurIPs, 2024. 3

[46] Shihao Wang, Yingfei Liu, Tiancai Wang, Ying Li, and Xiangyu Zhang. Exploring object-centric temporal modeling for efficient multi-view 3d object detection. arXiv:2303.11926, 2023. 2, 5

[47] Tsun-Hsuan Wang, Alaa Maalouf, Wei Xiao, Yutong Ban, Alexander Amini, Guy Rosman, Sertac Karaman, and Daniela Rus. Drive Anywhere: Generalizable end-to-end autonomous driving with multi-modal foundation models. arXiv:2310.17642, 2023. 8

[48] Wenhai Wang, Jiangwei Xie, ChuanYang Hu, Haoming Zou, Jianan Fan, Wenwen Tong, Yang Wen, Silei Wu, Hanming Deng, Zhiqi Li, et al. DriveMLM: Aligning multi-modal large language models with behavioral planning states for autonomous driving. arXiv:2312.09245, 2023. 1, 2

[49] Yue Wang, Guizilini Vitor Campagnolo, Tianyuan Zhang, Hang Zhao, and Justin Solomon. DETR3D: 3d object detection from multi-view images via 3d-to-2d queries. In CoRL, 2022. 2

[50] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. Chain-ofthought prompting elicits reasoning in large language models. NeurIPS, 2022. 8

[51] Dongming Wu, Wencheng Han, Tiancai Wang, Yingfei Liu, Xiangyu Zhang, and Jianbing Shen. Language prompt for autonomous driving. arXiv:2309.04379, 2023. 8

[52] Penghao Wu, Xiaosong Jia, Li Chen, Junchi Yan, Hongyang Li, and Yu Qiao. Trajectory-guided control prediction for end-to-end autonomous driving: A simple yet strong baseline. In NeurIPS, 2022. 7

[53] Zhenhua Xu, Yujia Zhang, Enze Xie, Zhen Zhao, Yong Guo, Kenneth KY Wong, Zhenguo Li, and Hengshuang Zhao. DriveGPT4: Interpretable end-to-end autonomous driving via large language model. arXiv:2310.01412, 2023. 1, 8

[54] Jiang-Tian Zhai, Ze Feng, Jinhao Du, Yongqiang Mao, Jiang-Jiang Liu, Zichang Tan, Yifu Zhang, Xiaoqing Ye, and Jingdong Wang. Rethinking the open-loop evaluation of endto-end autonomous driving in nuscenes. arXiv:2305.10430, 2023. 1, 7

[55] Zhejun Zhang, Alexander Liniger, Dengxin Dai, Fisher Yu, and Luc Van Gool. End-to-end urban driving by imitating a reinforcement learning coach. In ICCV, 2021. 7

[56] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan

Wahid, et al. RT-2: Vision-language-action models transfer web knowledge to robotic control. In CoRL, 2023. 8