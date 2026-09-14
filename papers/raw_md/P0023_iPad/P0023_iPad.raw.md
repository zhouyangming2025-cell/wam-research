# iPad: Iterative Proposal-centric End-to-End Autonomous Driving

Ke Guo Nanyang Technological University ke.guo@ntu.edu.sg

Xiaojun Wu Desay SV Automotive Xiaojun.Wu@desaysv.com

Haochen Liu Nanyang Technological University haochen002@e.ntu.edu.sg

Jia Pan The University of Hong Kong jpan@cs.hku.hk

Chen Lv Nanyang Technological University lyuchen@ntu.edu.sg

## Abstract

End-to-end (E2E) autonomous driving systems offer a promising alternative to traditional modular pipelines by reducing information loss and error accumulation, with significant potential to enhance both mobility and safety. However, most existing E2E approaches directly generate plans based on dense bird’s-eye view (BEV) grid features, leading to inefficiency and limited planning awareness. To address these limitations, we propose iterative Proposal-centric autonomous driving (iPad), a novel framework that places proposals—a set of candidate future plans—at the center of feature extraction and auxiliary tasks. Central to iPad is ProFormer, a BEV encoder that iteratively refines proposals and their associated features through proposal-anchored attention, effectively fusing multi-view image data. Additionally, we introduce two lightweight, proposal-centric auxiliary tasks—mapping and prediction—that improve planning quality with minimal computational overhead. Extensive experiments on the NAVSIM and CARLA Bench2Drive benchmarks demonstrate that iPad achieves state-of-the-art performance while being significantly more efficient than prior leading methods. Code is available at https://github.com/Kguo-cs/iPad.

## 1 Introduction

Autonomous vehicles have garnered significant research interest due to their potential to revolutionize transportation and enhance traffic safety [41]. Traditional autonomous driving systems are typically composed of modular components—localization, perception, tracking, prediction, planning, and control—to ensure interpretability. However, the decoupled learning and design across these modules often lead to information loss and error accumulation. Recently, end-to-end (E2E) driving paradigms have emerged as a promising alternative [5], leveraging holistic, fully differentiable models that map raw sensor data directly to planning outputs.

Early E2E approaches such as ALVINN [33] and PilotNet [2] aimed to learn a direct mapping from high-dimensional inputs to trajectories or control commands. However, these straightforward models were difficult to optimize and lacked interpretability. To address these shortcomings, more recent work [19, 24, 6, 7, 31] introduces intermediate BEV grid features using a BEV encoder [32, 28]

![](images/5b20f0aa837ad69a322f32201243440743d421a7b60913a3c5aa4ff6b22a4d68.jpg)  
(a) One-shot Grid-Centric Paradigm

![](images/da4e97b3304b50d229eebb7eefae8e35ee6023da90f8ff40f602bbfb36129a11.jpg)  
(b) Iterative Proposal-centric Paradigm

Figure 1: Comparison of end-to-end paradigms. (a) Dense one-shot, grid-centric methods generate BEV features for every cell and directly output the final plan based on the extracted dense BEV grid features. (b) iPad iteratively refines sparse BEV proposals and their queries, concentrating feature extraction on the regions most relevant to planning by using the proposal corner points as anchors. <sub>to</sub> <sub>fuse</sub> <sub>multi-view</sub> <sub>image</sub> <sub>features,</sub> <sub>as</sub> <sub>shown</sub> <sub>in</sub> <sub>fig.</sub> <sub>1,</sub> <sub>which</sub> <sub>are</sub> <sub>then</sub> <sub>used</sub> <sub>to</sub> <sub>directly</sub> <sub>generate</sub> final driving plans. While BEV-based pipelines improve interpretability, their dense grids incur substantial computational cost [23] and often capture spurious correlations with irrelevant scene elements—leading to degraded planning performance and causal confusion [9, 29].

To overcome these limitations, we propose iterative Proposal-centric autonomous driving (iPad), a unified E2E framework that places proposals at the heart of the model. In iPad, each proposal is a candidate future trajectory, and feature extraction, mapping, prediction, and scoring are all centered around these sparse BEV proposals. Unlike prior work that treats planning as a final-stage task built on fixed intermediate features, iPad makes planning the central organizing principle of the entire architecture. Specifically, it formulates planning as an iterative process of proposal refinement. We begin by initializing BEV proposal queries based on the ego vehicle’s current state. We then introduce ProFormer, a proposal-centric BEV encoder that predicts proposals from these queries. Using the corner points of all proposals as anchor points, multi-view image features are aggregated around them to refine the proposal queries. This predict–anchor–refine cycle repeats iteratively, producing increasingly accurate proposals and BEV proposal features. Finally, a lightweight scoring module evaluates the refined proposals and selects the best trajectory for execution.

iPad excels in both efficiency and effectiveness. In terms of efficiency, it scales linearly with the number of proposals, in contrast to the quadratic complexity of dense BEV grid methods. By employing planning-aware image feature extraction, iPad directly captures task-relevant information—avoiding the information bottlenecks inherent to dense grid representations. Furthermore, by modeling multimodal expert planning distributions with a diverse set of learnable proposals, iPad can mitigate the modal collapse common in widely used deterministic planners such as Transfuser [8], ST-P3 [18], and UniAD [19].

In addition, most existing E2E methods incorporate auxiliary tasks—such as object detection [36], occupancy prediction [19], or motion forecasting [24]—to enhance intermediate representations learning. However, these often need dense, computationally expensive features and are poorly aligned with the ultimate planning objective. They also diverge from human driving intuition, which prioritizes context directly relevant to the current decision. In contrast, iPad introduces two lightweight, proposal-centric auxiliary tasks: mapping and prediction, which are tightly coupled with the planning process. For each proposal, the mapping task predicts whether its states lie on-road or on-route, while the prediction task forecasts the future states of both the first object that will collide and the first object that is likely to collide (based on time-to-collision analysis) with the proposal planning trajectory.

## Our main contributions are as follows:

1. Iterative Proposal-Centric Paradigm: We propose iPad, an end-to-end driving paradigm that centers the entire learning pipeline around sparse, learnable BEV proposals. iPad unifies feature extraction, mapping, prediction, and planning in a computationally efficient and interpretable manner.

2. Proposal-Aware Feature Extraction: We design ProFormer, a novel BEV encoder that integrates multi-view image features through proposal-anchored spatial attention. ProFormer jointly refines BEV queries and proposals, enabling high-quality multi-modal plan generation.

3. Planning-Centric Auxiliary Tasks: We introduce two lightweight, proposal-centric auxiliary tasks that enhance the planning process without introducing redundant computation or irrelevant scene modeling, improving both accuracy and efficiency.

4. State-of-the-art performance: iPad achieves state-of-the-art results on both the real-world NAVSIM [12] and CARLA Bench2Drive [22] benchmarks. Notably, experiments show that iPad provides strong scalability and is over 10× more computationally efficient than UniAD [19].

## 2 Related Work

The goal of end-to-end (E2E) autonomous driving is to generate vehicle motion plans or control commands directly from raw sensor input, bypassing the need for task-specific modules such as detection and motion prediction. Early works such as ALVINN [33], PilotNet [2], and CIL [34] leveraged large-scale human driving data to learn policies that directly map sensor observations to control actions. However, these models often suffered from poor interpretability and degraded performance due to issues like causal confusion [9]. To mitigate these limitations, recent research has explored incorporating intermediate representations, auxiliary tasks and proposal-based planning to enhance performance and robustness.

Intermediate representations. Two main categories of intermediate representations have been adopted in E2E autonomous driving: dense BEV grids and sparse query features. BEV representations naturally encode spatial relationships on the ground plane, making them ideal for joint perception and planning, and sensor fusion. ST-P3 [18] was an early example that integrated detection, prediction, and planning into a unified BEV-based framework. Subsequent works—such as UniAD [19], VAD [24], GenAD [44], and GraphAD [43]—follow a similar paradigm: generating dense BEV grid features from images and sequentially performing perception, prediction, and planning. Although effective, these methods are computationally expensive due to the high resolution required for accurate perception. To improve efficiency, a sparse query-centric paradigm has emerged, as seen in SparseDrive [36], DiFSD [35], and DriveTransformer [23]. These methods use a limited number of learned queries to directly aggregate multi-view image features, avoiding costly view transformations. While this approach improves efficiency, it can still suffer from redundant computation and degraded planning performance due to excessive interactions with irrelevant agents—leading to causal confusion. Moreover, these approaches often overlook valuable prior knowledge (e.g., view transformations), resulting in suboptimal performance [29, 42]. However, all previous works typically build intermediate representations without explicit planning awareness, treating planning as a downstream task. In contrast, iPad integrates planning directly into the learning of intermediate representations via iterative proposal refinement. This joint optimization enables iPad to achieve both computational efficiency and high planning performance by focusing on planning-relevant features.

Auxiliary E2E tasks. To support the learning of interpretable intermediate representations, E2E methods often include auxiliary tasks such as object detection [36], BEV semantic segmentation [8], occupancy prediction [19], and motion forecasting [24]. However, these tasks typically require high-resolution inputs and large models [28], increasing computational cost. Furthermore, they often diverge from the core decision-making process of human drivers, who selectively focus on elements relevant to the current driving decision-making. To address these issues, we propose two lightweight, proposal-centric auxiliary tasks—mapping and prediction—that focus explicitly on modeling objects relevant to the ego vehicle’s planning proposals.

Multi-modal planning. Planning in autonomous driving is inherently multi-modal due to uncertainties in dynamic environments. However, most existing E2E methods [8, 26, 38, 29, 37] generate deterministic plans, which can lead to unrealistic or suboptimal behaviors. Recent works such as VADv2 [6] and Hydra-MDP [27] address this by scoring a large set of fixed anchor trajectories to approximate the planning distribution. In contrast, SparseDrive [36] predicts a small number of planning proposals in the final stage. However, fixed anchor vocabularies and limited proposal sets constrain expressiveness and adaptability. In contrast, iPad iteratively predicts and refines a dynamic set of planning proposals and leverages these proposals to guide feature extraction. This tight integration of planning and representation learning allows iPad to generate diverse, high-quality trajectories while maintaining efficiency.

![](images/d122ffa60e488b7306423a86cb1eef1cfb93e083746c8e2c09e991f1ba8dd95a.jpg)  
Figure 2: Overview of the iPad framework, consisting of four key components: the Scene Encoder (gray) extracts image and ego features; the ProFormer (blue) initializes BEV proposal queries with ego features and iteratively refines them using the image features; Scorer (green) predicts a score for each proposal trajectory; and the Proposal-Centric Mapping and Prediction (red) predict passability maps and agent future states related to potential collisions.

## 3 Method

The overall framework of our iPad method is illustrated in fig. 2. iPad comprises four components: Scene Encoder processes multi-view input images and ego vehicle status to extract both image and ego features; ProFormer iteratively refines trajectory proposals and queries with the extracted image features; Scorer predicts the planning performance of all final proposals and selects the one with the highest score as the output plan; Proposal-Centric Mapping and Prediction module predicts passability and collision risk for all final proposals during training, improving both interpretability and overall performance.

## 3.1 Scene Encoder

Our method takes two types of input: multi-view images and ego status. The multi-view images are processed through an image encoder, comprising a backbone network (e.g., ResNet-34 [16]) and a neck, to extract multi-view image feature maps $\breve { \pmb { I } } \in \mathbb { R } ^ { I \times C \times H \times W }$ , where I is the number of image views, C the feature channel dimension, H the height, and W the width of the feature maps. The ego status, including features such as ego current velocity, acceleration, and future commands, is encoded into the ego feature $\pmb { { \cal E } } \in \mathbb { R } ^ { 1 \times C }$ using a linear layer.

## 3.2 ProFormer

We propose ProFormer, a proposal-centric BEV encoder built upon BEVFormer [28], which iteratively refines BEV proposal queries by leveraging multi-view image features. ProFormer enhances the initial BEV queries by incorporating ego features. Moreover, unlike BEVFormer—which relies on a fixed dense grid of anchors to compute BEV features, leading to high computational overhead and limited planning awareness—ProFormer employs a learnable, proposal-based anchoring strategy that significantly improves both computational efficiency and planning relevance.

At each iteration $k = 0 , \ldots , K - 1$ , we first predict proposals $P _ { k } \in \mathbb { R } ^ { N \times T \times 3 }$ from current BEV proposal queries $Q _ { k } \in \mathbb { R } ^ { N \times T \times C }$ using a MLP, where N is the number of proposals and each proposal is a sequence of $T$ future states $( x , y , h e a d i n g )$ . We initialize proposal queries $Q _ { 0 }$ by adding ego features E to learnable positional embeddings. Then, we apply proposal-anchored deformable self-attention (SA) over the queries to capture temporal dependencies and interactions among proposals, using the predicted proposal positions as anchor points:

$$
\mathrm { S A } ( Q _ { k } ^ { n , t } , Q _ { k } ) = \mathrm { D e f o r m A t t n } ( Q _ { k } ^ { n , t } , P _ { k } ^ { n , t } ( x , y ) , Q _ { k } ) ,\tag{1}
$$

where $Q _ { k } ^ { n , t } \in \mathbb { R } ^ { C }$ denotes the BEV query for the n-th proposal at time step t, and $P _ { k } ^ { n , t } ( x , y ) \in \mathbb { R } ^ { 2 }$ is its predicted 2D position. The deformable attention mechanism [45], described in detail in appendix A, computes attention by sampling a small set of points around each anchor, resulting in high efficiency.

Following self-attention, we apply proposal-anchored deformable spatial cross-attention (SCA) to aggregate multi-view image features I, using the predicted four corner points of each proposal as

anchors to better account for vehicle size and planning heading:

$$
\mathrm { S C A } ( Q _ { k } ^ { n , t } , I ) = \frac { 1 } { | \mathcal { V } _ { \mathrm { h i t } } | } \sum _ { i \in \mathcal { V } _ { \mathrm { h i t } } } \sum _ { j } ^ { 4 } \sum _ { z = 1 } ^ { N _ { \mathrm { r e f } } } \mathrm { D e f o r m A t t n } ( Q _ { k } ^ { n , t } , \mathcal { P } ( P _ { k } ^ { n , t } , i , j , z ) , I _ { i } ) ,\tag{2}
$$

where $\boldsymbol { I } _ { i }$ denotes the features from the i-th camera view. For each BEV query $Q _ { k } ^ { n , t }$ , each proposal’s four corner points are lifted into 3D pillars and sample $N _ { \mathrm { r e f } }$ reference points per pillar. A projection function $\mathcal { P }$ maps the z-th reference point of the j-th corner onto the image plane of the i-th view. Since not all projected points fall within every view, we define the set of camera views that contain valid projections as $\nu _ { \mathrm { h i t } }$ . Finally, a linear layer updates the refined proposal queries, producing $Q _ { k + 1 }$ for the next iteration.

Notably, following previous auto-regressive methods such as GPT [1] and diffusion models [17], we design the ProFormer to share weights across iterations. To supervise proposal prediction at each iteration, we adopt a simple Minimum over N (MoN) loss [15], defined as:

$$
\mathcal { L } _ { p r o p o s a l } = \sum _ { k = 0 } ^ { K - 1 } \lambda ^ { K - 1 - k } \operatorname* { m i n } _ { n = 1 , \dots , N } \left\| \pmb { P } _ { k } ^ { n } - \hat { \pmb { P } } \right\| _ { 1 } ,\tag{3}
$$

where $P _ { k } ^ { n }$ is the n-th proposal generated at iteration k, $\hat { P } \in \mathbb { R } ^ { T \times 3 }$ is the expert trajectory, and $\lambda \in ( 0 , 1 )$ is a discount factor that gradually relaxes the loss constraint for earlier iterations.

## 3.3 Scorer

To select a proposal as the planning, we learn a scorer to evaluate the final proposals $P _ { K }$ . The proposal with the highest predicted score is selected as the final planning trajectory. Specifically, we apply max pooling over the temporal dimension of BEV proposal features (i.e. the final BEV proposal queries $Q _ { K } \in \mathbb { R } ^ { N \times T \times C } )$ , which are then fed into a multi-layer perceptron (MLP) to predict the scores $\pmb { S } \in \mathbb { R } ^ { \tilde { N } \times 1 }$ . The score learning uses the binary cross-entropy (BCE) loss as:

$$
\mathcal { L } _ { s c o r e } = \mathrm { B C E } ( S , \hat { S } ) ,\tag{4}
$$

where $\mathrm { B C E } ( x , y ) = - y \log x + ( 1 - y ) \log ( 1 - x )$ . Considering the safety, efficiency, comfort of each proposal, we compute the ground-truth score following NAVSIM [12]:

$$
\hat { S } = N C \times D A C \times \frac { 5 \times E P + 5 \times T T C + 2 \times C o m f } { 1 2 } ,\tag{5}
$$

No at-fault Collision (NC), Drivable Area Compliance (DAC), Ego Progress (EP), Time-to-Collision (TTC), and Comfort (Comf) are sub-metrics obtained via a log-replay simulator. In this simulator, a controller is applied to recursively track the final proposal while other agents follow their recorded trajectory. For more details on obtaining the ground-truth sub-metrics, please refer to the appendix C.

## 3.4 Proposal-Centric Mapping and Prediction

To enhance planning performance and interpretability, we design two light-weight plan-oriented auxiliary tasks: proposal-centric mapping and prediction. Unlike conventional auxiliary tasks that aim to model all objects in the scene, our approach focuses solely on predicting map and agent information relevant to each proposal. Moreover, since different proposals may lead to different predicted states for the same object, our method can also reflect perception and prediction uncertainty.

For proposal-centric mapping, we predict the on-road and on-route probabilities $M \in \mathbb { R } ^ { N \times T \times 2 }$ for all proposals’ simulated states using the BEV proposal features $Q _ { K }$ as input to a MLP. The mapping task is trained by minimizing the BCE loss between the predicted probabilities and the ground-truth labels $\hat { M } \in \mathbb { R } ^ { N \times T \times 2 }$

$$
\mathcal { L } _ { m a p } = \mathrm { B C E } ( M , \hat { M } ) .\tag{6}
$$

For proposal-centric prediction, we predict the future states of the first at-fault and likely-to-collide (with a time-to-collision below a defined threshold) agents, identified via the log-replay simulation. The agent state predictions are generated using a MLP applied to the max-pooled BEV proposal

features $Q _ { K }$ . The predicted states $\pmb { A } \in \mathbb { R } ^ { N \times T \times 2 \times 9 }$ include the 2D positions of the four corners $\pmb { A } _ { c } \in \mathbb { R } ^ { N \times \tilde { T } \times 2 \times 4 \times 2 }$ , with corresponding validity labels $\pmb { A } _ { v } \in \mathbb { R } ^ { N \times T ^ { \frac { 1 } { \hbar } } \times 2 \times 1 }$ . The prediction task is supervised using an $\mathcal { L } _ { 1 }$ loss on corner positions and a BCE loss on the validity labels:

$$
\mathcal { L } _ { p r e d } = \| A _ { c } - \hat { A } _ { c } \| _ { 1 } + w _ { b c e } \operatorname { B C E } ( A _ { v } , \hat { A } _ { v } ) ,\tag{7}
$$

where $w _ { b c e }$ is the weight for the BCE term, and $\hat { A } _ { c } , \hat { A } _ { v }$ are the ground-truth corner positions and validity labels of the first at-fault and likely-to-collide agents.

## 3.5 Training

iPad can be end-to-end trained and optimized in a fully differentiable manner. The overall loss function can be formulated as follows:

$$
\mathcal { L } = \mathcal { L } _ { p r o p o s a l } + w _ { s c o r e } \mathcal { L } _ { s c o r e } + w _ { m a p } \mathcal { L } _ { m a p } + w _ { p r e d } \mathcal { L } _ { p r e d } ,\tag{8}
$$

where $w _ { s c o r e } , w _ { m a p } ,$ and $w _ { p r e d }$ are the weights for the scoring, mapping, and prediction losses, respectively. For more details on model structure, please refer to the appendix B.

## 4 Experiments

To evaluate the performance of our proposed method, we conducted experiments on both real-world open-loop and simulated closed-loop benchmarks.

## 4.1 Open-Loop NAVSIM Benchmark

For open-loop evaluations, we utilized the NAVSIM [12] benchmark, which is based on real-world driving data. Unlike the popular nuScenes [3] benchmark, which includes approximately 75% of scenarios involving trivial straight driving, NAVSIM focuses on more complex driving situations. This simplicity in nuScenes allows methods like AD-MLP, which bypass perception entirely, to perform exceptionally well [42]. Additionally, nuScenes primarily relies on simple displacement error and collision rate metrics, which fail to adequately capture real-world closed-loop driving performance, such as penalties for off-road driving.

Dataset: The NAVSIM dataset builds on the real-world nuPlan [4] dataset, incorporating only relevant annotations and sensor data sampled at 2 Hz. It emphasizes scenarios involving intention changes where the ego vehicle’s historical data cannot be extrapolated into a future plan. We trained and evaluated our model using the official navtrain and navtest splits, which contain 103k and 12k samples, respectively.

Metrics: The NAVSIM introduces a series of closed-loop metrics designed to evaluate open-loop simulation and reflect real-world closed-loop performance. The sub-metric scores align with our training sub-metric scores, with the addition of a PDM score (PDMS), defined as:

$$
P D M S = N C \times D A C \times \frac { 5 \times E P + 5 \times T T C + 2 \times C } { 1 2 } ,\tag{9}
$$

where sub-metrics are derived from a non-reactive simulation over a 4-second horizon. A kinematic bicycle model, controlled by an LQR controller, tracks the planned trajectory to simulate the ego vehicle’s movement at 10 Hz. These sub-metrics are computed based on the simulated trajectory, recorded trajectories of other agents, and map data.

Results: As shown in table 1, our method significantly outperforms prior works on this benchmark in all metrics without relying on lidar input. The high driving area compliance underscores the effectiveness of our approach in extracting and utilizing planning-relevant map information. Furthermore, the superior ego progress highlights the expressiveness of our multi-modal planning framework.

## 4.2 Closed-Loop Bench2Drive Benchmark

Evaluating closed-loop driving performance in real-world scenarios is challenging, so we used the CARLA [13] simulator, employing the Bench2Drive benchmarks [22].

Table 1: Open-loop Results with Closed-loop Metrics on NAVSIM Benchmark.
<table><tr><td>Method</td><td>Input</td><td>Img. Backbone</td><td>NC↑</td><td>DAC ↑</td><td>TTC ↑</td><td>Comf. ↑</td><td>EP↑</td><td>PDMS ↑</td></tr><tr><td>PDM-Closed [11] (Rule-based)</td><td>Perception GT</td><td></td><td>94.6</td><td>99.8</td><td>86.9</td><td>99.9</td><td>89.9</td><td>89.1</td></tr><tr><td>VADv2-V8192 [6]</td><td>Camera &amp; Lidar</td><td>ResNet-34 [16]</td><td>97.2</td><td>89.1</td><td>91.6</td><td>100</td><td>76.0</td><td>80.9</td></tr><tr><td>Transfuser [8]</td><td>Camera &amp; Lidar</td><td>ResNet-34 [16]</td><td>97.7</td><td>92.8</td><td>92.8</td><td>100</td><td>79.2</td><td>84.0</td></tr><tr><td>DRAMA [40]</td><td>Camera &amp; Lidar</td><td>ResNet-34 [16]</td><td>98.0</td><td>93.1</td><td>94.8</td><td>100</td><td>80.1</td><td>85.5</td></tr><tr><td>Hydra-MDP-V8192-W-EP [27]</td><td>Camera &amp; Lidar</td><td>ResNet-34 [16]</td><td>98.3</td><td>96.0</td><td>94.6</td><td>100</td><td>78.7</td><td>86.5</td></tr><tr><td>DiffusionDrive [30]</td><td>Camera &amp; Lidar</td><td>ResNet-34 [16]</td><td>98.2</td><td>96.2</td><td>94.7</td><td>100</td><td>82.2</td><td>88.1</td></tr><tr><td>UniAD [19]</td><td>Camera</td><td>ResNet-34 [16]</td><td>97.8</td><td>91.9</td><td>92.9</td><td>100</td><td>78.8</td><td>83.4</td></tr><tr><td>LTF [8]</td><td>Camera</td><td>ResNet-34 [16]</td><td>97.4</td><td>92.8</td><td>92.4</td><td>100</td><td>79.0</td><td>83.8</td></tr><tr><td>PARA-Drive [38]</td><td>Camera</td><td>ResNet-34 [16]</td><td>97.9</td><td>92.4</td><td>93.0</td><td>99.8</td><td>79.3</td><td>84.0</td></tr><tr><td>iPad (Ours)</td><td>Camera</td><td>ResNet-34 [16]</td><td>98.6</td><td>98.3</td><td>94.9</td><td>100</td><td>88.0</td><td>91.7</td></tr></table>

Table 2: Open-loop and Closed-loop Results of E2E Methods on Bench2Drive Benchmark.
<table><tr><td rowspan="2">Method</td><td rowspan="2">Latency</td><td>Open-loop</td><td colspan="4">Closed-loop</td></tr><tr><td>Avg. L2 ↓</td><td>Efficiency ↑</td><td>Comfortness ↑</td><td>Success Rate (%) ↑</td><td>Driving Score ↑</td></tr><tr><td>AD-MLP [42]</td><td>4ms</td><td>3.64</td><td>48.45</td><td>22.63</td><td>0.00</td><td>18.05</td></tr><tr><td>UniAD-Tiny [19]</td><td>445 ms</td><td>0.80</td><td>123.92</td><td>47.04</td><td>13.18</td><td>40.73</td></tr><tr><td>UniAD-Base [19]</td><td>558 ms</td><td>0.73</td><td>129.21</td><td>43.58</td><td>16.36</td><td>45.81</td></tr><tr><td>VAD [24]</td><td>359 ms</td><td>0.91</td><td>157.94</td><td>46.01</td><td>15.00</td><td>42.35</td></tr><tr><td>DriveTransformer [23]</td><td>212 ms</td><td>0.62</td><td>100.64</td><td>20.78</td><td>35.01</td><td>63.46</td></tr><tr><td>iPad (Ours)</td><td>43 ms</td><td>0.97</td><td>161.31</td><td>28.21</td><td>35.91</td><td>65.02</td></tr><tr><td>TCP* [39]</td><td>71 ms</td><td>1.70</td><td>54.26</td><td>47.80</td><td>15.00</td><td>40.70</td></tr><tr><td>TCP-ctrl*</td><td>71 ms</td><td></td><td>55.97</td><td>51.51</td><td>7.27</td><td>30.47</td></tr><tr><td>TCP-traj*</td><td>71 ms</td><td>1.70</td><td>76.54</td><td>18.08</td><td>30.00</td><td>59.90</td></tr><tr><td>TCP-traj w/o distillation</td><td>71 ms</td><td>1.96</td><td>78.78</td><td>22.96</td><td>20.45</td><td>49.30</td></tr><tr><td>ThinkTwice* [21]</td><td>762 ms</td><td>0.95</td><td>69.33</td><td>16.22</td><td>31.23</td><td>62.44</td></tr><tr><td>DriveAdapter* [20]</td><td>931 ms</td><td>1.01</td><td>70.22</td><td>16.01</td><td>33.08</td><td>64.22</td></tr></table>

denotes expert feature distillation. All latencies are measured as the average inference time (including input preparation, model inference, and control generation) during CARLA evaluation on NVIDIA RTX 4090 GPU except for DriveTransformer, ThinkTwice and DriveAdapter on A6000 from [23].

Dataset: Bench2Drive provides a training dataset collected by the state-of-the-art expert model Think2Drive [25]. For fair comparisons, we utilized the base subset, which consists of 1,000 clips, with 950 clips allocated for training and 50 clips reserved for open-loop evaluation.

Metrics: Bench2Drive evaluates open-loop performance using the average $\mathcal { L } _ { 2 }$ distance between the planned and expert trajectories over 2 seconds at 2 Hz. Closed-loop evaluations are conducted on 220 routes (approximately 150 meters each) across all CARLA towns, with each route featuring a safety-critical scenario. A PID controller tracks the planned trajectory at 20 Hz. Bench2Drive defines four closed-loop metrics:

• Success Rate: The proportion of successfully completed routes within the allowed time and without traffic violations.

• Driving Score: The product of the route completion ratio and penalties for infractions, averaged across all routes.

• Efficiency: The ego vehicle’s average speed as a percentage of the average speed of nearby vehicles over 20 checkpoints along a route.

• Comfortness: The ratio of smooth trajectory segments to total segments. A trajectory segment is considered smooth if its lateral acceleration, yaw rate, yaw acceleration, and jerk remain within predefined thresholds.

Additionally, Bench2Drive evaluates five driving skills: merging, overtaking, emergency braking, yielding, and traffic sign adherence. The ability score for each skill is defined as the average success rate across all corresponding scenarios.

Results: As shown in table 2, our method achieves state-of-the-art performance in success rate and driving score without relying on an expert model. Furthermore, our lightweight network design result in significantly reduced latency, making it highly efficient for real-time applications. As demonstrated in table 3, our method also achieve best average performance over five driving abilities, showcasing its versatility and robustness in handling diverse and challenging scenarios.

Table 3: Multi-Ability Results of E2E Methods on Bench2Drive Benchmark.
<table><tr><td rowspan="2">Method</td><td colspan="6">Ability (%) ↑</td></tr><tr><td>Merging</td><td>Overtaking</td><td>Emergency Brake</td><td>Give Way</td><td>Traffic Sign</td><td>Mean</td></tr><tr><td>AD-MLP [42]</td><td>0.00</td><td>0.00</td><td>0.00</td><td>0.00</td><td>4.35</td><td>0.87</td></tr><tr><td>UniAD-Tiny [19]</td><td>8.89</td><td>9.33</td><td>20.00</td><td>20.00</td><td>15.43</td><td>14.73</td></tr><tr><td>UniAD-Base [19]</td><td>14.10</td><td>17.78</td><td>21.67</td><td>10.00</td><td>14.21</td><td>15.55</td></tr><tr><td>VAD [24]</td><td>8.11</td><td>24.44</td><td>18.64</td><td>20.00</td><td>19.15</td><td>18.07</td></tr><tr><td>DriveTransformer [23]</td><td>17.57</td><td>35.00</td><td>48.36</td><td>40.00</td><td>52.10</td><td>38.60</td></tr><tr><td>iPad (Ours)</td><td>30.00</td><td>20.00</td><td>53.33</td><td>60.00</td><td>49.47</td><td>42.56</td></tr><tr><td>TCP* [39]</td><td>16.18</td><td>20.00</td><td>20.00</td><td>10.00</td><td>6.99</td><td>14.63</td></tr><tr><td>TCP-ctrl*</td><td>10.29</td><td>4.44</td><td>10.00</td><td>10.00</td><td>6.45</td><td>8.23</td></tr><tr><td>TCP-traj*</td><td>8.89</td><td>24.29</td><td>51.67</td><td>40.00</td><td>46.28</td><td>34.22</td></tr><tr><td>TCP-traj w/o distillation</td><td>17.14</td><td>6.67</td><td>40.00</td><td>50.00</td><td>28.72</td><td>28.51</td></tr><tr><td>ThinkTwice* [21]</td><td>27.38</td><td>18.42</td><td>35.82</td><td>50.00</td><td>54.23</td><td>37.17</td></tr><tr><td>DriveAdapter* [20]</td><td>28.82</td><td>26.38</td><td>48.76</td><td>50.00</td><td>56.43</td><td>42.08</td></tr></table>

Table 4: Ablation Studies on the NAVSIM Benchmark.
<table><tr><td>Proposal Refinement</td><td>BEV Encoder</td><td>Mapping Module</td><td>Prediction Module</td><td>NC↑</td><td>DAC ↑</td><td>TTC ↑</td><td>EP↑</td><td>PDMS ↑</td></tr><tr><td>No</td><td>BEVFormer</td><td>General [8]</td><td>General [8]</td><td>97.6</td><td>93.0</td><td>92.9</td><td>68.9</td><td>78.5</td></tr><tr><td>Yes</td><td>BEVFormer</td><td>General [8]</td><td>General [8]</td><td>96.9</td><td>93.2</td><td>90.8</td><td>71.5</td><td>79.4</td></tr><tr><td>Yes</td><td>ProFormer</td><td>General [8]</td><td>General [8]</td><td>98.1</td><td>96.5</td><td>94.3</td><td>84.2</td><td>89.8</td></tr><tr><td>Yes</td><td>ProFormer</td><td>Proposal-centric</td><td>General [8]</td><td>98.3</td><td>97.9</td><td>94.4</td><td>85.9</td><td>90.5</td></tr><tr><td>Yes</td><td>ProFormer</td><td>Proposal-centric</td><td>Proposal-centric</td><td>98.6</td><td>98.3</td><td>94.9</td><td>88.0</td><td>91.7</td></tr></table>

## 4.3 Ablation Studies

To evaluate the contributions of individual components, we conducted ablation studies using the NAVSIM benchmark. Comfort metrics were omitted, as all ablated models consistently achieved a perfect score of 100.

Effectiveness of proposal-centric BEV encoder: We evaluate the effectiveness of our proposalcentric BEV encoder by replacing ProFormer with the baseline BEVFormer. First, to exclude the impact of the intermediate proposal learning, we conduct an experiment using BEVFormer to also predict proposals at each iteration. As shown in table 4, this naive approach to proposal learning yields limited gains, as the image feature extraction process in BEVFormer does not incorporate the predicted proposals. We then replace BEVFormer with our ProFormer, which leads to a significant improvement in all planning metrics—highlighting the benefit of our proposal-aware spatial crossattention mechanism.

Advantages of proposal-centric auxiliary tasks: To evaluate the impact of our auxiliary task design, we substitute the standard mapping and prediction tasks from Transfuser [8] with our proposal-centric variants. As shown in table 4, replacing the proposal-centric mapping task results in a drop in driving area compliance. Similarly, replacing the proposal-centric prediction task degrades performance in terms of no at-fault collisions and time-to-collision. These results demonstrate the value of our planning-oriented auxiliary tasks in enhancing driving performance.

## 4.4 Scalability

We investigate the trend in iPad’s planning performance as the proposal number, iteration number, and training data size increase. The final PDM score on the test set of the NAVSIM Benchmark is evaluated, and the results are presented in fig. 3. A clear power-law scaling trend is observed for the PDM score with respect to the proposal number, iteration count, and training data size. Specifically, a higher number of proposals enhances the flexibility of the planning distribution and effectively expands the model’s representation capacity. More refinement iterations improve the accuracy of the proposals by leveraging a greater number of image features, while larger training data volumes contribute to better generalization of the model.

## 4.5 Qualitative Analysis

We visualized the planning and prediction results of our method in NAVSIM and Bench2Drive scenarios. As illustrated in fig. 4, in a NAVSIM turning scenario, our method generates diverse, human-like

![](images/468a4ab2537d32e7e52167495ebb55c0bcaf4ba29f742f42f2c0de8524b64a66.jpg)

![](images/642ff5eff65d3aa4bf60b5428c1000093381f0cc40e2e73dbc3c11edfc8941f4.jpg)

![](images/ab51b01e028d35ce10276b790afdb83782e871b92eb46329b33961781d66ad8c.jpg)

Figure 3: Scaling law in iPad. The PDM score performance on the NAVSIM Benchmark increases logarithmically with the proposal number, iteration number and training data size,  
![](images/7acb48e200f5b7b9e2fb3015342b80c6aa7f7bee865022f9904888e090f35a99.jpg)  
(a) NAVSIM Turning Scenario

![](images/454a0651ae3b3dc17f0fce9f707266c707a2cfbb46f987e64a5913e318a57dcc.jpg)  
(b) Bench2Drive Merging Scenario

Figure 4: Qualitative planning and collision prediction results on NAVSIM and Bench2Drive. Proposal lines are shaded with brightness proportional to their predicted scores, while the brightness of predicted agent boxes reflects their associated proposals.

planning proposals closely aligned with actual human trajectories. The prediction results accurately reflect collision risks, prioritizing central proposals with higher scores. In a Bench2Drive merging scenario, our method produced a collision-free planning, with predictions effectively highlighting collision risks and prioritizing conservative merging proposals. More qualitative examples can be found in appendix D.

## 5 Limitations

Our work has two primary limitations. First, we do not incorporate historical image and status information to maintain efficiency. However, utilizing historical data could help address occlusion issues and enhance the accuracy of trajectory predictions for other agents. Second, we lack realworld closed-loop evaluations. While our open-loop evaluations use real-world data, closed-loop performance remains uncertain due to the distribution shift. Simulated closed-loop evaluations face challenges from the sim-to-real gap, as simulations cannot fully capture the complexity and unpredictability of real-world driving. Factors such as corner cases, unexpected human behavior, and diverse environmental conditions are often inadequately modeled.

## 6 Conclusion

We presented iPad, a novel end-to-end autonomous driving framework that rethinks the role of planning in the E2E learning paradigm. By placing sparse, learnable proposals at the center of perception, prediction, and planning, iPad offers a unified, interpretable, and computationally efficient alternative to dense BEV grid-based methods. Our proposed ProFormer encoder and lightweight proposal-centric auxiliary tasks enable the model to focus on planning-relevant information while avoiding unnecessary computation and spurious correlations. Extensive experiments on challenging real-world and simulation benchmarks demonstrate that iPad achieves state-of-the-art performance while being significantly more efficient than prior work.

## References

[1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. arXiv preprint arXiv:2303.08774, 2023.

[2] Mariusz Bojarski, Davide Del Testa, Daniel Dworakowski, Bernhard Firner, Beat Flepp, Prasoon Goyal, Lawrence D Jackel, Mathew Monfort, Urs Muller, Jiakai Zhang, et al. End to end learning for self-driving cars. arXiv preprint arXiv:1604.07316, 2016.

[3] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multimodal dataset for autonomous driving. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 11621–11631, 2020.

[4] Holger Caesar, Juraj Kabzan, Kok Seang Tan, Whye Kit Fong, Eric Wolff, Alex Lang, Luke Fletcher, Oscar Beijbom, and Sammy Omari. Nuplan: A closed-loop ml-based planning benchmark for autonomous vehicles. In CVPR ADP3 workshop, 2021.

[5] Li Chen, Penghao Wu, Kashyap Chitta, Bernhard Jaeger, Andreas Geiger, and Hongyang Li. End-to-end autonomous driving: Challenges and frontiers. IEEE Transactions on Pattern Analysis and Machine Intelligence, 2024.

[6] Shaoyu Chen, Bo Jiang, Hao Gao, Bencheng Liao, Qing Xu, Qian Zhang, Chang Huang, Wenyu Liu, and Xinggang Wang. Vadv2: End-to-end vectorized autonomous driving via probabilistic planning. arXiv preprint arXiv:2402.13243, 2024.

[7] Zhili Chen, Maosheng Ye, Shuangjie Xu, Tongyi Cao, and Qifeng Chen. Ppad: Iterative interactions of prediction and planning for end-to-end autonomous driving. In ECCV, pages 239–256, 2025.

[8] Kashyap Chitta, Aditya Prakash, Bernhard Jaeger, Zehao Yu, Katrin Renz, and Andreas Geiger. Transfuser: Imitation with transformer-based sensor fusion for autonomous driving. IEEE Transactions on Pattern Analysis and Machine Intelligence, 45(11):12878–12895, 2022.

[9] Felipe Codevilla, Eder Santana, Antonio M López, and Adrien Gaidon. Exploring the limitations of behavior cloning for autonomous driving. In CVPR, pages 9329–9338, 2019.

[10] Jifeng Dai, Haozhi Qi, Yuwen Xiong, Yi Li, Guodong Zhang, Han Hu, and Yichen Wei. Deformable convolutional networks. In Proceedings ofthe IEEE international conference on computer vision, pages 764–773, 2017.

[11] Daniel Dauner, Marcel Hallgarten, Andreas Geiger, and Kashyap Chitta. Parting with misconceptions about learning-based vehicle motion planning. In Conference on Robot Learning, pages 1268–1281. PMLR, 2023.

[12] Daniel Dauner, Marcel Hallgarten, Tianyu Li, Xinshuo Weng, Zhiyu Huang, Zetong Yang, Hongyang Li, Igor Gilitschenski, Boris Ivanovic, Marco Pavone, et al. Navsim: Data-driven nonreactive autonomous vehicle simulation and benchmarking. arXiv preprint arXiv:2406.15349, 2024.

[13] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. Carla: An open urban driving simulator. In CoRL, pages 1–16. PMLR, 2017.

[14] Ke Guo, Wei Jing, Junbo Chen, and Jia Pan. CCIL: Context-conditioned imitation learning for urban driving. In Robotics: Science and Systems, 2023.

[15] Agrim Gupta, Justin Johnson, Li Fei-Fei, Silvio Savarese, and Alexandre Alahi. Social gan: Socially acceptable trajectories with generative adversarial networks. In CVPR, pages 2255– 2264, 2018.

[16] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In CVPR, pages 770–778, 2016.

[17] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. Advances in neural information processing systems, 33:6840–6851, 2020.

[18] Shengchao Hu, Li Chen, Penghao Wu, Hongyang Li, Junchi Yan, and Dacheng Tao. St-p3: End-to-end vision-based autonomous driving via spatial-temporal feature learning. In ECCV, pages 533–549, 2022.

[19] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, et al. Planning-oriented autonomous driving. In CVPR, pages 17853–17862, 2023.

[20] Xiaosong Jia, Yulu Gao, Li Chen, Junchi Yan, Patrick Langechuan Liu, and Hongyang Li. Driveadapter: Breaking the coupling barrier of perception and planning in end-to-end autonomous driving. In ICCV, 2023.

[21] Xiaosong Jia, Penghao Wu, Li Chen, Jiangwei Xie, Conghui He, Junchi Yan, and Hongyang Li. Think twice before driving: Towards scalable decoders for end-to-end autonomous driving. In CVPR, 2023.

[22] Xiaosong Jia, Zhenjie Yang, Qifeng Li, Zhiyuan Zhang, and Junchi Yan. Bench2drive: Towards multi-ability benchmarking of closed-loop end-to-end autonomous driving. arXiv preprint arXiv:2406.03877, 2024.

[23] Xiaosong Jia, Junqi You, Zhiyuan Zhang, and Junchi Yan. Drivetransformer: Unified transformer for scalable end-to-end autonomous driving. In ICLR, 2025.

[24] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. Vad: Vectorized scene representation for efficient autonomous driving. ICCV, pages 8340–8350, 2023.

[25] Qifeng Li, Xiaosong Jia, Shaobo Wang, and Junchi Yan. Think2drive: Efficient reinforcement learning by thinking in latent world model for quasi-realistic autonomous driving (in carla-v2). arXiv preprint arXiv:2402.16720, 2024.

[26] Yingyan Li, Lue Fan, Jiawei He, Yuqi Wang, Yuntao Chen, Zhaoxiang Zhang, and Tieniu Tan. Enhancing end-to-end autonomous driving with latent world model. arXiv preprint arXiv:2406.08481, 2024.

[27] Zhenxin Li, Kailin Li, Shihao Wang, Shiyi Lan, Zhiding Yu, Yishen Ji, Zhiqi Li, Ziyue Zhu, Jan Kautz, Zuxuan Wu, et al. Hydra-mdp: End-to-end multimodal planning with multi-target hydra-distillation. arXiv preprint arXiv:2406.06978, 2024.

[28] Zhiqi Li, Wenhai Wang, Hongyang Li, Enze Xie, Chonghao Sima, Tong Lu, Yu Qiao, and Jifeng Dai. Bevformer: Learning bird’s-eye-view representation from multi-camera images via spatiotemporal transformers. In ECCV, pages 1–18, 2022.

[29] Zhiqi Li, Zhiding Yu, Shiyi Lan, Jiahan Li, Jan Kautz, Tong Lu, and Jose M Alvarez. Is ego status all you need for open-loop end-to-end autonomous driving? In CVPR, pages 14864–14873, 2024.

[30] Bencheng Liao, Shaoyu Chen, Haoran Yin, Bo Jiang, Cheng Wang, Sixu Yan, Xinbang Zhang, Xiangyu Li, Ying Zhang, Qian Zhang, et al. Diffusiondrive: Truncated diffusion model for end-to-end autonomous driving. In CVPR, 2025.

[31] Haochen Liu, Zhiyu Huang, Wenhui Huang, Haohan Yang, Xiaoyu Mo, and Chen Lv. Hybridprediction integrated planning for autonomous driving. IEEE Transactions on Pattern Analysis and Machine Intelligence, 2025.

[32] Jonah Philion and Sanja Fidler. Lift, splat, shoot: Encoding images from arbitrary camera rigs by implicitly unprojecting to 3d. In Computer Vision–ECCV 2020: 16th European Conference, Glasgow, UK, August 23–28, 2020, Proceedings, Part XIV 16, pages 194–210. Springer, 2020.

[33] Dean A Pomerleau. Alvinn: An autonomous land vehicle in a neural network. NeurIPS, 1, 1988.

[34] Axel Sauer, Nikolay Savinov, and Andreas Geiger. Conditional affordance learning for driving in urban environments. In CoRL, pages 237–252, 2018.

[35] Haisheng Su, Wei Wu, and Junchi Yan. Difsd: Ego-centric fully sparse paradigm with uncertainty denoising and iterative refinement for efficient end-to-end autonomous driving. arXiv preprint arXiv:2409.09777, 2024.

[36] Wenchao Sun, Xuewu Lin, Yining Shi, Chuang Zhang, Haoran Wu, and Sifa Zheng. Sparsedrive: End-to-end autonomous driving via sparse scene representation. arXiv preprint arXiv:2405.19620, 2024.

[37] Yuqi Wang, Jiawei He, Lue Fan, Hongxin Li, Yuntao Chen, and Zhaoxiang Zhang. Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving. In CVPR, pages 14749–14759, 2024.

[38] Xinshuo Weng, Boris Ivanovic, Yan Wang, Yue Wang, and Marco Pavone. Para-drive: Parallelized architecture for real-time autonomous driving. In CVPR, pages 15449–15458, 2024.

[39] Penghao Wu, Xiaosong Jia, Li Chen, Junchi Yan, Hongyang Li, and Yu Qiao. Trajectory-guided control prediction for end-to-end autonomous driving: A simple yet strong baseline. NeurIPS, 35:6119–6132, 2022.

[40] Chengran Yuan, Zhanqi Zhang, Jiawei Sun, Shuo Sun, Zefan Huang, Christina Dao Wen Lee, Dongen Li, Yuhang Han, Anthony Wong, Keng Peng Tee, et al. Drama: An efficient end-to-end motion planner for autonomous driving with mamba. arXiv preprint arXiv:2408.03601, 2024.

[41] Ekim Yurtsever, Jacob Lambert, Alexander Carballo, and Kazuya Takeda. A survey of autonomous driving: Common practices and emerging technologies. IEEE access, 8:58443–58469, 2020.

[42] Jiang-Tian Zhai, Ze Feng, Jinhao Du, Yongqiang Mao, Jiang-Jiang Liu, Zichang Tan, Yifu Zhang, Xiaoqing Ye, and Jingdong Wang. Rethinking the open-loop evaluation of end-to-end autonomous driving in nuscenes. arXiv preprint arXiv:2305.10430, 2023.

[43] Yunpeng Zhang, Deheng Qian, Ding Li, Yifeng Pan, Yong Chen, Zhenbao Liang, Zhiyao Zhang, Shurui Zhang, Hongxu Li, Maolei Fu, et al. Graphad: Interaction scene graph for end-to-end autonomous driving. arXiv preprint arXiv:2403.19098, 2024.

[44] Wenzhao Zheng, Ruiqi Song, Xianda Guo, Chenming Zhang, and Long Chen. Genad: Generative end-to-end autonomous driving. In ECCV, pages 87–104, 2024.

[45] Xizhou Zhu, Weijie Su, Lewei Lu, Bin Li, Xiaogang Wang, and Jifeng Dai. Deformable detr: Deformable transformers for end-to-end object detection. arXiv preprint arXiv:2010.04159, 2020.

## Appendix

## A Detailed Mechanism in ProFormer

Deformable attention defintion: The deformable attention is defined as:

$$
\mathrm { D e f o r m A t t n } ( q , p , x ) = \sum _ { i = 1 } ^ { N _ { \mathrm { h e a d } } } \mathcal { W } _ { i } \sum _ { j = 1 } ^ { N _ { \mathrm { k e y } } } A _ { i j } \cdot \mathcal { W } _ { i } ^ { \prime } x ( p + \Delta p _ { i j } ) ,\tag{10}
$$

where $q , p ,$ x represent the query, reference point and input features, respectively. i indexes the attention head, and $N _ { \mathrm { h e a d } }$ denotes the total number of attention heads. $j$ indexes the sampled keys, and $N _ { \mathrm { k e y } }$ is the total sampled key number for each head. $W _ { i } \in \mathbb { R } ^ { C \times ( C / H _ { \mathrm { h e a d } } ) }$ and $W _ { i } ^ { \prime } { \in } \mathbb { R } ^ { ( C ^ { \prime } H _ { \mathrm { h e a d } } ) ^ { * } \times C }$ are the learnable weights, where C is the feature dimension. $A _ { i j } \in [ 0 , 1 ]$ is the predicted attention weight, and is normalized by $\begin{array} { r } { \sum _ { j = 1 } ^ { N _ { \mathrm { k e y } } } A _ { i j } = 1 . ~ \Delta p _ { i j } \in \mathbb { R } ^ { 2 } } \end{array}$ are the predicted offsets to the reference point p. $x ( p + \Delta p _ { i j } )$ represents the feature at location $p + \Delta p _ { i j }$ , which is extracted by bilinear interpolation as in Dai et al. [10].

Spatial cross attention details: Spatial cross-attention, shown in fig. 5, computes the attention between proposal queries and the image features I using the predicted proposal. For each proposal pose, the vehicle’s four corner points are calculated as BEV anchor points, incorporating vehicle size and planned heading information. Reference points sampled from pillars lifted from these anchors are projected onto 2D image views, and image features around these projected points are aggregated using deformable attention. For one BEV query, the projected 2D points can only fall on some views, and other views are not hit. Here, we term them the hit views.

![](images/2760416016f5591530de630079db16a66d549e7f245f3b55d9c817e96d572455.jpg)  
Figure 5: Detailed architecture of ProFormer. The proposals are used to query deformable proposalcentric image features I (yellow) to update the proposal features.

## B Model Details

For both datasets, the same model architecture is used, whose hyper-parameters are listed in table 5. All models are trained on a single NVIDIA H800 GPU with a batch size of 64 for 20 epochs, using the Adam optimizer with a learning rate of $1 \times 1 0 ^ { - 4 }$ . For efficiency, we only use downsampled images from the front, front-left, front-right, and back views as input.

Table 5: Hyper-parameters
<table><tr><td>Hyper-parameter</td><td>Value 64</td></tr><tr><td>Proposal number N Iteration number K Planning time step interval Channel dimension C Hidden size Feed-forward size Pillar reference point number  $N _ { r e f }$  Proposal loss discount λ Score loss weight  $w _ { s c o r e }$  Map loss weight  $w _ { m a p }$  Prediction loss weight</td><td>4 0.5s 256 256 1024 4 0.1 1 2</td></tr><tr><td> $w _ { p r e d }$  Prediction BCE loss weight  $w _ { b c e }$  NAVSIM future planning horizon T</td><td>1 0.1 8</td></tr><tr><td>NAVSIM image input down-sample rate Bench2Drive future planning horizon T Bench2Drive image input down-sample rate</td><td>0.4 6 0.64</td></tr></table>

## C Training Scoring

To efficiently obtain ground-truth scores for the final proposals during training, we employ parallelized computation using Ray for multi-processing.

## C.1 NAVSIM Scoring

For NAVSIM, we use the official log-replay simulator with an LQR controller operating at 10 Hz over a 4-second horizon. Final scores are derived based on the following official sub-metrics:

• No At-Fault Collision (NC): Set to 0 if, at any simulation step, the proposal’s bounding box intersects with other road users (vehicles, pedestrians, or bicycles). Collisions that are not considered “at-fault” in the non-reactive environment (e.g., when the ego vehicle is stationary) are ignored. For collisions with static objects, a softer penalty of 0.5 is applied.

• Drivable Area Compliance: Set to 0 if, at any simulation step, any corner of the proposal state lies outside the drivable area polygons.

• Time-to-Collision (TTC): Initialized to 1. Set to 0 if, at any point during the 4-second horizon, the ego vehicle’s projected time-to-collision—assuming constant velocity and heading—is less than 1 second.

• Comfort: Set to 0 if, at any simulation step, motion exceeds any of the following thresholds:

– Lateral acceleration $\mathrm { > 4 . 8 9 \ m / s ^ { 2 } }$

– Longitudinal acceleration $> 2 . 4 0 \mathrm { m / s ^ { 2 } }$

– Longitudinal deceleration $> 4 . 0 5 \mathrm { m / s ^ { 2 } }$

– Absolute jerk $> 8 . 3 7 \mathrm { m } / \mathrm { s } ^ { 3 }$

– Longitudinal $\mathrm { j e r k } > 4 . 1 3 \mathrm { m } / \mathrm { s } ^ { 3 }$

– Yaw rate > 0.95 rad/s

– Yaw acceleration $> 1 . 9 3 ~ \mathrm { r a d / s ^ { 2 } }$

• Ego Progress: Measures the agent’s progress along the route center, normalized by a safe upper bound estimated by the PDM-Closed planner. The final ratio is clipped to [0, 1], and scores are discarded if the upper bound is below 5 meters or the progress is negative.

## C.2 Bench2Drive Scoring

For Bench2Drive, we utilize a log-replay simulator with a perfect controller operating at 2 Hz over a 3-second horizon. Evaluation is based on the following sub-metrics:

• No Collision (NC): Set to 0 if, at any simulation step, the proposal’s bounding box intersects with any object (vehicles, bicycles, pedestrians, traffic signs, traffic cones, or traffic lights).

• Drivable Area Compliance (DAC): Set to 0 if, at any simulation step, any corner of the proposal state lies off-road or all centers off-route.

• Time-to-Collision (TTC): Set to 0 if, at any point during the 3-second horizon, the ego vehicle’s projected time-to-collision is less than 1 second.

• Comfort: Set to 0 if the proposal’s acceleration or turning rate exceeds the expert trajectory’s maximum values.

• Ego Progress: Defined as the ratio of the ego progress along the expert trajectory, conditioned on being collision-free and on-road. If the ratio exceeds 1, its reciprocal is taken.

## C.3 Relations between Open-loop and Closed-loop Scores

To evaluate the effectiveness of our scoring method, we analyze the relationship between open-loop validation metrics (L2, Score, NC, DAC, TTC, Progress, Comfort), closed-loop metrics (driving score, success rate), and training epoch. Specifically, we test 20 checkpoints—randomly sampled after the 10th training epoch, when the model has stabilized—for both the shared and non-shared versions of iPad. We compute the correlation coefficients between all metrics, as shown in fig. 6.

Our results show that both the Score and Progress metrics are positively correlated with the final closed-loop driving performance. In contrast, the collision-related metrics (NC and TTC) exhibit a negative correlation with the closed-loop metrics, which may be attributed to a mismatch between agent behaviors: the real-world agents are reactive, while our log-sim assumes them to be non-reactive. Additionally, we observe a negative correlation between the open-loop L2 metric and closed-loop performance, consistent with findings in prior work [14]. Finally, the Comfort metric also shows a negative correlation with closed-loop driving scores, likely due to the high frequency of hazardous scenarios in the Bench2Drive benchmark that require abrupt braking.

![](images/a398cce3d991d47c377b13ecb9247ed67bbf0268a90a818bcebbcf844b9c8b83.jpg)  
Figure 6: Correlation Matrix of Open-loop and Closed-loop Driving Metrics

## D More Qualitative Results

We show more qualitative results in both NAVSIM and Bench2Drive closed-loop testing scenarios.

## D.1 Proposal Refinement

The fig. 7 demonstrate that iPad can gradually refine the proposals, making it more similar to human trajectory.

![](images/0e7a7b18c3fae0be5047d3d774a0768941acf4151ee3717064b4815b800c61a4.jpg)  
Figure 7: Proposal prediction results at all iterations in a NAVSIM scenario.

The fig. 8 demonstrate that iPad can gradually refine the proposals, while keeping the multi-modality in the intersection scenarios.  
![](images/cf204c6196eaa3c946cdf729a9fb2e2695a2dd5f45ad0e259e4548c5ecd24db9.jpg)  
Figure 8: Proposal prediction results at all iterations in a Bench2Drive scenario.

## D.2 Mapping

The fig. 9 demonstrate that iPad can generate accurate on-road and on-route probability predictions in NAVSIM scenarios, being aware of the proposal heading and vehicle size. Therefore, a on-road and on-route proposal is chosen as the planning.

![](images/9a20908f2ada88cc45b26df6805901cf2f4b99a95fd0337f09e03324f1f7e191.jpg)  
Figure 9: Passability prediction results in a NAVSIM scenario. The lightness of the proposal lines or points decreases with their scores or predicted on-road or on-route probabilities. The proposal state is off-road if any corner point is off-road.

As shown in fig. 10, iPad accurately predicts on-road and on-route probabilities in Bench2Drive scenarios, demonstrating awareness of both proposal heading and vehicle size. Therefore, a on-road and on-route proposal is chosen as the planning.

![](images/25c9282135db240e862eca37bdfb1d1a582d702dfce72a277baf74a78ea32c86.jpg)  
Figure 10: Passability prediction results in a Bench2Drive scenario. The lightness of the proposal lines or points decreases with their scores or predicted on-road or on-route probabilities. The proposal state is off-road if any corner point is off-road.

## D.3 Collision Prediction

The fig. 11 demonstrates that iPad can identify potential collision risks in NAVSIM scenarios by accurately predicting the future bounding boxes of at-fault and likely collided agents for outlier proposals. Consequently, the planner selects a safe centering proposal.

![](images/dd3369b8515f89a1a5668b994504ac4f2083d175bf2f206dbd3158bcd54387b0.jpg)  
Figure 11: Collision prediction results in a NAVSIM turning scenario. The lightness of the proposal lines decreases with their scores. The lightness of the predicted agent boxes corresponds to their associated proposals.

The fig. 12 demonstrates that iPad can effectively recognize potential collision risks in parking cut-in scenarios by accurately predicting the future bounding boxes of the at-fault and likely collided vehicle for dangerous proposals, when the taillights of the red car are illuminated. Therefore, a deceleration proposal is chosen as the planning.

![](images/e29e3a6cfd29da35c88de9535c0a98ceddf890551b7b7e29905cfcb9f24c7e76.jpg)  
Figure 12: Collision prediction results in a Bench2Drive parking cutin scenario. The lightness of the proposal lines decreases with their scores. The lightness of the predicted agent boxes corresponds to their associated proposals.

## NeurIPS Paper Checklist

## 1. Claims

Question: Do the main claims made in the abstract and introduction accurately reflect the paper’s contributions and scope?

Answer: [Yes]

Justification: We have clearly state the motivations and contributions for iPad in abstract and section 1.

Guidelines: The abstract and introduction in this paper accurately reflect the paper’s contributions and scope.

• The answer NA means that the abstract and introduction do not include the claims made in the paper.

• The abstract and/or introduction should clearly state the claims made, including the contributions made in the paper and important assumptions and limitations. A No or NA answer to this question will not be perceived well by the reviewers.

• The claims made should match theoretical and experimental results, and reflect how much the results can be expected to generalize to other settings.

• It is fine to include aspirational goals as motivation as long as it is clear that these goals are not attained by the paper.

## 2. Limitations

Question: Does the paper discuss the limitations of the work performed by the authors?

Answer: [Yes]

Justification: We discuss the limitations of the work in section 5.

Guidelines:

• The answer NA means that the paper has no limitation while the answer No means that the paper has limitations, but those are not discussed in the paper.

• The authors are encouraged to create a separate "Limitations" section in their paper.

• The paper should point out any strong assumptions and how robust the results are to violations of these assumptions (e.g., independence assumptions, noiseless settings, model well-specification, asymptotic approximations only holding locally). The authors should reflect on how these assumptions might be violated in practice and what the implications would be.

• The authors should reflect on the scope of the claims made, e.g., if the approach was only tested on a few datasets or with a few runs. In general, empirical results often depend on implicit assumptions, which should be articulated.

• The authors should reflect on the factors that influence the performance of the approach. For example, a facial recognition algorithm may perform poorly when image resolution is low or images are taken in low lighting. Or a speech-to-text system might not be used reliably to provide closed captions for online lectures because it fails to handle technical jargon.

• The authors should discuss the computational efficiency of the proposed algorithms and how they scale with dataset size.

• If applicable, the authors should discuss possible limitations of their approach to address problems of privacy and fairness.

• While the authors might fear that complete honesty about limitations might be used by reviewers as grounds for rejection, a worse outcome might be that reviewers discover limitations that aren’t acknowledged in the paper. The authors should use their best judgment and recognize that individual actions in favor of transparency play an important role in developing norms that preserve the integrity of the community. Reviewers will be specifically instructed to not penalize honesty concerning limitations.

## 3. Theory assumptions and proofs

Question: For each theoretical result, does the paper provide the full set of assumptions and a complete (and correct) proof?

Answer: [NA]

Justification: The paper does not include theoretical results.

## Guidelines:

• The answer NA means that the paper does not include theoretical results.

• All the theorems, formulas, and proofs in the paper should be numbered and crossreferenced.

• All assumptions should be clearly stated or referenced in the statement of any theorems.

• The proofs can either appear in the main paper or the supplemental material, but if they appear in the supplemental material, the authors are encouraged to provide a short proof sketch to provide intuition.

• Inversely, any informal proof provided in the core of the paper should be complemented by formal proofs provided in appendix or supplemental material.

• Theorems and Lemmas that the proof relies upon should be properly referenced.

## 4. Experimental result reproducibility

Question: Does the paper fully disclose all the information needed to reproduce the main experimental results of the paper to the extent that it affects the main claims and/or conclusions of the paper (regardless of whether the code and data are provided or not)?

Answer: [Yes]

Justification: All the results in this paper can be reproduced.

Guidelines:

• The answer NA means that the paper does not include experiments.

• If the paper includes experiments, a No answer to this question will not be perceived well by the reviewers: Making the paper reproducible is important, regardless of whether the code and data are provided or not.

• If the contribution is a dataset and/or model, the authors should describe the steps taken to make their results reproducible or verifiable.

• Depending on the contribution, reproducibility can be accomplished in various ways. For example, if the contribution is a novel architecture, describing the architecture fully might suffice, or if the contribution is a specific model and empirical evaluation, it may be necessary to either make it possible for others to replicate the model with the same dataset, or provide access to the model. In general. releasing code and data is often one good way to accomplish this, but reproducibility can also be provided via detailed instructions for how to replicate the results, access to a hosted model (e.g., in the case of a large language model), releasing of a model checkpoint, or other means that are appropriate to the research performed.

• While NeurIPS does not require releasing code, the conference does require all submissions to provide some reasonable avenue for reproducibility, which may depend on the nature of the contribution. For example

(a) If the contribution is primarily a new algorithm, the paper should make it clear how to reproduce that algorithm.

(b) If the contribution is primarily a new model architecture, the paper should describe the architecture clearly and fully.

(c) If the contribution is a new model (e.g., a large language model), then there should either be a way to access this model for reproducing the results or a way to reproduce the model (e.g., with an open-source dataset or instructions for how to construct the dataset).

(d) We recognize that reproducibility may be tricky in some cases, in which case authors are welcome to describe the particular way they provide for reproducibility. In the case of closed-source models, it may be that access to the model is limited in some way (e.g., to registered users), but it should be possible for other researchers to have some path to reproducing or verifying the results.

## 5. Open access to data and code

Question: Does the paper provide open access to the data and code, with sufficient instructions to faithfully reproduce the main experimental results, as described in supplemental material?

Answer: [Yes]

Justification: We provide open access to the data and code, with sufficient instructions to faithfully reproduce the main experimental results.

Guidelines:

• The answer NA means that paper does not include experiments requiring code.

• Please see the NeurIPS code and data submission guidelines (https://nips.cc/ public/guides/CodeSubmissionPolicy) for more details.

• While we encourage the release of code and data, we understand that this might not be possible, so “No” is an acceptable answer. Papers cannot be rejected simply for not including code, unless this is central to the contribution (e.g., for a new open-source benchmark).

• The instructions should contain the exact command and environment needed to run to reproduce the results. See the NeurIPS code and data submission guidelines (https: //nips.cc/public/guides/CodeSubmissionPolicy) for more details.

• The authors should provide instructions on data access and preparation, including how to access the raw data, preprocessed data, intermediate data, and generated data, etc.

• The authors should provide scripts to reproduce all experimental results for the new proposed method and baselines. If only a subset of experiments are reproducible, they should state which ones are omitted from the script and why.

• At submission time, to preserve anonymity, the authors should release anonymized versions (if applicable).

• Providing as much information as possible in supplemental material (appended to the paper) is recommended, but including URLs to data and code is permitted.

## 6. Experimental setting/details

Question: Does the paper specify all the training and test details (e.g., data splits, hyperparameters, how they were chosen, type of optimizer, etc.) necessary to understand the results?

Answer: [Yes]

Justification: The paper specify all the training and test details necessary to understand the results.

Guidelines:

• The answer NA means that the paper does not include experiments.

• The experimental setting should be presented in the core of the paper to a level of detail that is necessary to appreciate the results and make sense of them.

• The full details can be provided either with the code, in appendix, or as supplemental material.

## 7. Experiment statistical significance

Question: Does the paper report error bars suitably and correctly defined or other appropriate information about the statistical significance of the experiments?

Answer: [No]

Justification: While not conducting significance tests over results, our experiments are conducted on the NAVSIM and Bench2Drive Dataset, which has a large data scale. Thus, the experimental results are stable across multiple trials, and the reported results can be accurately reproduced using the provided open-source code.

Guidelines:

• The answer NA means that the paper does not include experiments.

• The authors should answer "Yes" if the results are accompanied by error bars, confidence intervals, or statistical significance tests, at least for the experiments that support the main claims of the paper.

• The factors of variability that the error bars are capturing should be clearly stated (for example, train/test split, initialization, random drawing of some parameter, or overall run with given experimental conditions).

• The method for calculating the error bars should be explained (closed form formula, call to a library function, bootstrap, etc.)

• The assumptions made should be given (e.g., Normally distributed errors).

• It should be clear whether the error bar is the standard deviation or the standard error of the mean.

• It is OK to report 1-sigma error bars, but one should state it. The authors should preferably report a 2-sigma error bar than state that they have a 96% CI, if the hypothesis of Normality of errors is not verified.

• For asymmetric distributions, the authors should be careful not to show in tables or figures symmetric error bars that would yield results that are out of range (e.g. negative error rates).

• If error bars are reported in tables or plots, The authors should explain in the text how they were calculated and reference the corresponding figures or tables in the text.

## 8. Experiments compute resources

Question: For each experiment, does the paper provide sufficient information on the computer resources (type of compute workers, memory, time of execution) needed to reproduce the experiments?

Answer: [Yes]

Justification: The resources used for model training have been introduced clearly in the training section.

Guidelines:

• The answer NA means that the paper does not include experiments.

• The paper should indicate the type of compute workers CPU or GPU, internal cluster, or cloud provider, including relevant memory and storage.

• The paper should provide the amount of compute required for each of the individual experimental runs as well as estimate the total compute.

• The paper should disclose whether the full research project required more compute than the experiments reported in the paper (e.g., preliminary or failed experiments that didn’t make it into the paper).

## 9. Code of ethics

Question: Does the research conducted in the paper conform, in every respect, with the NeurIPS Code of Ethics https://neurips.cc/public/EthicsGuidelines?

Answer: [Yes]

Justification: We have all reviewed the NeurIPS Code of Ethics and striven to maintain and preserve anonymity.

Guidelines:

• The answer NA means that the authors have not reviewed the NeurIPS Code of Ethics.

• If the authors answer No, they should explain the special circumstances that require a deviation from the Code of Ethics.

• The authors should make sure to preserve anonymity (e.g., if there is a special consideration due to laws or regulations in their jurisdiction).

## 10. Broader impacts

Question: Does the paper discuss both potential positive societal impacts and negative societal impacts of the work performed?

Answer: [Yes]

Justification: In the introduction, we summarize this paper’s application to autonomous driving and traffic safety.

Guidelines:

• The answer NA means that there is no societal impact of the work performed.

• If the authors answer NA or No, they should explain why their work has no societal impact or why the paper does not address societal impact.

• Examples of negative societal impacts include potential malicious or unintended uses (e.g., disinformation, generating fake profiles, surveillance), fairness considerations (e.g., deployment of technologies that could make decisions that unfairly impact specific groups), privacy considerations, and security considerations.

• The conference expects that many papers will be foundational research and not tied to particular applications, let alone deployments. However, if there is a direct path to any negative applications, the authors should point it out. For example, it is legitimate to point out that an improvement in the quality of generative models could be used to generate deepfakes for disinformation. On the other hand, it is not needed to point out that a generic algorithm for optimizing neural networks could enable people to train models that generate Deepfakes faster.

• The authors should consider possible harms that could arise when the technology is being used as intended and functioning correctly, harms that could arise when the technology is being used as intended but gives incorrect results, and harms following from (intentional or unintentional) misuse of the technology.

• If there are negative societal impacts, the authors could also discuss possible mitigation strategies (e.g., gated release of models, providing defenses in addition to attacks, mechanisms for monitoring misuse, mechanisms to monitor how a system learns from feedback over time, improving the efficiency and accessibility of ML).

## 11. Safeguards

Question: Does the paper describe safeguards that have been put in place for responsible release of data or models that have a high risk for misuse (e.g., pretrained language models, image generators, or scraped datasets)?

Answer: [NA]

Justification: The paper poses no such risks

Guidelines:

• The answer NA means that the paper poses no such risks.

• Released models that have a high risk for misuse or dual-use should be released with necessary safeguards to allow for controlled use of the model, for example by requiring that users adhere to usage guidelines or restrictions to access the model or implementing safety filters.

• Datasets that have been scraped from the Internet could pose safety risks. The authors should describe how they avoided releasing unsafe images.

• We recognize that providing effective safeguards is challenging, and many papers do not require this, but we encourage authors to take this into account and make a best faith effort.

## 12. Licenses for existing assets

Question: Are the creators or original owners of assets (e.g., code, data, models), used in the paper, properly credited and are the license and terms of use explicitly mentioned and properly respected?

Answer: [Yes]

Justification: The training and evaluation datasets used in this study are cited within this paper.

Guidelines:

• The answer NA means that the paper does not use existing assets.

• The authors should cite the original paper that produced the code package or dataset.

• The authors should state which version of the asset is used and, if possible, include a URL.

• The name of the license (e.g., CC-BY 4.0) should be included for each asset.

• For scraped data from a particular source (e.g., website), the copyright and terms of service of that source should be provided.

• If assets are released, the license, copyright information, and terms of use in the package should be provided. For popular datasets, paperswithcode.com/datasets has curated licenses for some datasets. Their licensing guide can help determine the license of a dataset.

• For existing datasets that are re-packaged, both the original license and the license of the derived asset (if it has changed) should be provided.

• If this information is not available online, the authors are encouraged to reach out to the asset’s creators.

## 13. New assets

Question: Are new assets introduced in the paper well documented and is the documentation provided alongside the assets?

Answer: [No]

Justification: The paper does not release new assets.

Guidelines:

• The answer NA means that the paper does not release new assets.

• Researchers should communicate the details of the dataset/code/model as part of their submissions via structured templates. This includes details about training, license, limitations, etc.

• The paper should discuss whether and how consent was obtained from people whose asset is used.

• At submission time, remember to anonymize your assets (if applicable). You can either create an anonymized URL or include an anonymized zip file.

## 14. Crowdsourcing and research with human subjects

Question: For crowdsourcing experiments and research with human subjects, does the paper include the full text of instructions given to participants and screenshots, if applicable, as well as details about compensation (if any)?

Answer: [No]

Justification: The paper does not involve crowdsourcing nor research with human subjects. Guidelines:

• The answer NA means that the paper does not involve crowdsourcing nor research with human subjects.

• Including this information in the supplemental material is fine, but if the main contribution of the paper involves human subjects, then as much detail as possible should be included in the main paper.

• According to the NeurIPS Code of Ethics, workers involved in data collection, curation, or other labor should be paid at least the minimum wage in the country of the data collector.

## 15. Institutional review board (IRB) approvals or equivalent for research with human subjects

Question: Does the paper describe potential risks incurred by study participants, whether such risks were disclosed to the subjects, and whether Institutional Review Board (IRB) approvals (or an equivalent approval/review based on the requirements of your country or institution) were obtained?

Answer: [NA]

Justification: The paper does not involve crowdsourcing nor research with human subjects Guidelines:

• The answer NA means that the paper does not involve crowdsourcing nor research with human subjects.

• Depending on the country in which research is conducted, IRB approval (or equivalent) may be required for any human subjects research. If you obtained IRB approval, you should clearly state this in the paper.

• We recognize that the procedures for this may vary significantly between institutions and locations, and we expect authors to adhere to the NeurIPS Code of Ethics and the guidelines for their institution.

• For initial submissions, do not include any information that would break anonymity (if applicable), such as the institution conducting the review.

## 16. Declaration of LLM usage

Question: Does the paper describe the usage of LLMs if it is an important, original, or non-standard component of the core methods in this research? Note that if the LLM is used only for writing, editing, or formatting purposes and does not impact the core methodology, scientific rigorousness, or originality of the research, declaration is not required.

Answer: [NA]

Justification: The core method development in this research does not involve LLMs as any important, original, or non-standard components

Guidelines:

• The answer NA means that the core method development in this research does not involve LLMs as any important, original, or non-standard components.

• Please refer to our LLM policy (https://neurips.cc/Conferences/2025/LLM) for what should or should not be described.