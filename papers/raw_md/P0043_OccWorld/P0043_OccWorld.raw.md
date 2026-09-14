# OccWorld: Learning a 3D Occupancy World Model for Autonomous Driving

Wenzhao Zheng<sup>1,\*</sup> Weiliang Chen<sup>2,\*</sup> Yuanhui Huang<sup>1</sup> Borui Zhang<sup>1</sup> Yueqi Duan<sup>2</sup> Jiwen Lu<sup>1</sup>

Department of Automation, Tsinghua University, China

Department of Electronic Engineering, Tsinghua University, China

wenzhao.zheng@outlook.com; {chen-wl20,huangyh22,zhang-br21}@mails.tsinghua.edu.cn; {duanyueqi,lujiwen}@tsinghua.edu.cn

![](images/3145ae772c82ac9186b600fe4096931cd08663dbd55a6e1f368454261630dfe1.jpg)

Figure 1. Given past 3D occupancy observations, our self-supervised OccWorld trained can forecast future scene evolutions and ego movements jointly. This task requires a spatial understanding of the 3D scene and temporal modeling of how driving scenarios develop. We observe that OccWorld can successfully forecast the movements of surrounding agents and future map elements such as drivable areas. OccWorld even generates more reasonable drivable areas than the ground truth, demonstrating its ability to understand the scene rathe than memorizing training data. Still, it fails to forecast new vehicles entering the sight, which is difficult given their absence in the inputs.

## Abstract

Understanding how the 3D scene evolves is vital for making decisions in autonomous driving. Most existing methods achieve this by predicting the movements of object boxes, which cannot capture more fine-grained scene information. In this paper, we explore a new framework oflearning a world model, OccWorld, in the 3D Occupancy space to simultaneously predict the movement of the ego car and the evolution ofthe surrounding scenes. We propose to learn a world model based on 3D occupancy rather than 3D bounding boxes and segmentation maps for three reasons: 1) expressiveness. 3D occupancy can describe the more fine-grained 3D structure of the scene; 2) efficiency. 3D occupancy is more economical to obtain (e.g., from sparse LiDAR points). 3) versatility. 3D occupancy can adapt to both vision and LiDAR. To facilitate the modeling of the world evolution, we learn a reconstruction-based scene tokenizer on the 3D occupancy to obtain discrete scene tokens to describe the surrounding scenes. We then adopt a GPT-like spatial-temporal generative transformer to generate subsequent scene and ego tokens to decode the future occupancy and ego trajectory. Extensive experiments on the widely used nuScenes benchmark demonstrate the ability of

OccWorld to effectively model the evolution of the driving scenes. OccWorld also produces competitive planning results without using instance and map supervision. Code: https://github.com/wzzheng/OccWorld.

## 1. Introduction

Autonomous driving has been widely explored in recent years and demonstrated promising results in various scenarios [21, 57, 65, 68]. While LiDAR-based models typically show strong performance and robustness in 3D perception due to its capture of structural information [7, 35, 51, 61, 62], the more hardware-economical vision-centric solutions have dramatically caught up with the increased perception ability of deep networks [19, 32, 33, 42, 44].

Forecasting future scene evolutions is important to the safety of autonomous driving vehicles. Most existing methods follow a conventional pipeline of perception, prediction, and planning [17, 18, 25]. Perception aims to obtain a semantic understanding of the surrounding scene such as 3D object detection [19, 32, 33] and semantic map construction [30, 34, 37, 66]. The subsequent prediction module captures the motion of other traffic participants [11, 14, 24, 66], and the planning module then makes decisions based on previous outputs [17, 18, 25, 45]. However, this serial design usually requires ground-truth labels at each stage of training, yet the instance-level bounding boxes and high-definition maps are difficult to annotate. Furthermore, they usually only predict the motion of object bounding boxes, failing to capture more fine-grained information about the 3D scene.

In this paper, we explore a new paradigm to simultaneously predict the evolution of the surrounding scene and plan the future trajectory of the self-driving vehicle. We propose OccWorld, a world model in the 3D semantic occupancy space, to model the development of the driving scenes. We adopt 3D semantic occupancy as the scene representation over the conventional 3D bounding boxes and segmentation maps, which can describe the more finegrained 3D structure of the scene. Moreover, 3D occupancy can be effectively learned from sparse LiDAR points [21], and thus is a potentially more economical way to describe the surrounding scenes. Given the 3D semantic occupancy representation of the current scene, OccWorld aims to predict how it evolves as the self-driving vehicle advances. To achieve this, we first employ a vector-quantized variational autoencoder (VQVAE) [41] to refine high-level concepts and obtain discrete scene tokens in a self-supervised manner. We then tailor the generative pre-training transformers (GPT) [2] architecture and propose a spatial-temporal generative transformer to predict the subsequent scene tokens and ego tokens to forecast the future occupancy and ego trajectory, respectively. We first perform spatial mixing to aggregate scene tokens and obtain multi-scale tokens to represent scenes at multiple levels. We then apply temporal attention to tokens at different levels to predict tokens for the next frame and use a U-net structure to integrate them. Finally, we use the trained VQVAE decoder to transform scene tokens to the occupancy space and learn a trajectory decoder to obtain ego planning results.

To demonstrate the effectiveness of OccWorld, we formulate a challenging task of 4D occupancy forecasting, which aims to predict the 3D occupancy of the following frames given a few past frames. Our OccWorld can effectively forecast future evolutions including moving agents and static elements as shown in Figure 1, and achieves an average IoU of 26.63 and mIoU of 17.13 for 3s future given 2s history, OccWorld can also produce planning trajectories with an L2 error of 1.16 without using any instance and map annotations. Using self-supervised learned 3D occupancy from camera inputs [20], our method achieves non-trivial 4D occupancy forecasting and planning results, demonstrating the potential for interpretable end-to-end autonomous driving without additional human-annotated labels.

## 2. Related Work

3D Occupancy Prediction: 3D occupancy prediction aims to predict whether each voxel in the 3D space is occupied and its semantic label if occupied [21, 52, 53, 56, 57, 69]. Early methods exploited LiDAR as inputs to complete the 3D occupancy of the entire 3D scene [6, 29, 46, 59]. Recent methods began to explore the more challenging visionbased 3D occupancy prediction [4, 21] or applying vision backbones to efficiently perform LiDAR-based 3D occupancy prediction [69]. 3D occupancy provides more comprehensive descriptions of the surrounding scene and includes both dynamic and static elements [21, 57, 69]. It can also be efficiently learned from sparse accumulated multiple LiDAR scans [57], LiDAR [21], or video sequences [5]. However, existing methods only focus on obtaining the 3D semantic occupancy and ignore its temporal evolution, which is vital to the safety of autonomous driving. In this paper, we explore the task of 4D occupancy forecasting and propose a 3D occupancy world model to achieve this.

World Models for Autonomous Driving: World models have a long history in control engineering and artificial intelligence [49], which are usually defined as producing the next scene observation given action and past observations [12]. The development of deep neural networks [13, 48, 50] promoted the use of deep generative models [10, 28] as world models. Based on large pretrained image generative models like StableDiffusion [47], recent methods [9, 15, 31, 55, 60] can generate realistic driving sequences of diverse scenarios. However, they produce future observations in the 2D image space, lacking understanding of the 3D surrounding scene. Some other methods explore forecasting point clouds using unannotated Li-DAR scans [26, 27, 40, 58], which ignore the semantic information and cannot be applied to vision-based or fusionbased autonomous driving. Considering this, we explore a world model in the 3D occupancy space to more comprehensively model the 3D scene evolution.

End-to-End Autonomous Driving: The ultimate goal of autonomous driving is to obtain controlling signals based on observations of the surrounding scenes. Recent methods follow this concept to output planning results for the ego car given sensor inputs [17, 18, 25, 53, 63]. Most of them follow a conventional pipeline of perception [21, 32, 33, 57, 65], prediction [11, 14, 36, 66], and planning [22, 23, 54, 67]. They usually first perform BEV perception to extract relevant information (e.g., 3D agent boxes, semantic maps, tracklets) and then exploit them to infer future trajectories of agents and the ego vehicle. The following methods incorporated more data [63] or extracted more intermediate features [17, 18, 25] to provide more information for the planner, which achieved remarkable performance. Most methods only model object motions and cannot capture the fine-grained structural and semantic information of the surroundings [11, 14, 24, 25, 66]. Differently, we propose a world model to predict the evolution of both the surrounding dynamic and static elements.

![](images/70a6cb8e558e8b578a913417ecb5e197a60864fc0d220480db65c3f199d9a5fc.jpg)  
Figure 2. Framework of our OccWorld for 3D semantic occupancy forecast and motion planning. We adopt a GPT-like generative architecture to predict the next scene from previous scenes in an autoregressive manner. We adapt GPT [2] to the autonomous driving scenario with two key designs: 1) We train a 3D occupancy scene tokenizer to produce discrete high-level representations of the 3D scene; 2) We perform spatial mixing before and after spatial-wise temporal causal self-attention to efficiently produce globally consistent scene predictions. We use ground-truth and predicted scene tokens as inputs for future generations for training and inference, respectively

## 3. Proposed Approach

## 3.1. World Model for Autonomous Driving

Autonomous driving aims to automatically steer a vehicle to fully prevent or partially reduce actions from human drivers [18]. Formally, the objective of autonomous driving is to obtain the control commands $\mathbf { c } ^ { T }$ (e.g., throttle, steer, break) for the present time stamp $T$ given the sensor inputs $\{ \mathbf { s } ^ { T } , \mathbf { s } ^ { T - 1 } , \cdots , \mathbf { s } ^ { T - t } \}$ from the current and past t frames.

As the mapping from trajectories to control signals is highly dependent on the vehicle specifications and status, the literature usually assumes a given satisfactory controller and thus focuses on trajectory planning for the ego vehicle. An autonomous driving model A then takes input as the sensor inputs and ego trajectory from the past T frames and predicts the ego trajectory of future f frames:

$$
\begin{array} { r l } & { \quad A ( \{ \mathbf { s } ^ { T } , \mathbf { s } ^ { T - 1 } , \cdots , \mathbf { s } ^ { T - t } \} , \{ \mathbf { p } ^ { T } , \mathbf { p } ^ { T - 1 } , \cdots , \mathbf { p } ^ { T - t } \} ) } \\ & { = \{ \mathbf { p } ^ { T + 1 } , \mathbf { p } ^ { T + 2 } , \cdots , \mathbf { p } ^ { T + f } \} , } \end{array}\tag{1}
$$

where $\mathbf { p } ^ { t }$ denotes the 3D ego position at the t-th time.

The conventional pipeline of autonomous driving usually follows a design of perception, prediction, and planning [17, 18, 25]. The perception module $p _ { e r }$ perceives the surrounding scenes and extracts high-level information z from the input sensor data s. The prediction module $p _ { r e }$ then integrates the high-level information z to predict the future trajectory $\mathbf { t } _ { i }$ of each agent in the scene. The planning module $p _ { l a }$ finally processes the perception and prediction results $\left\{ \mathbf { z } , \{ \mathbf { t } _ { i } \} \right\}$ to plan the motion of the ego vehicle. The conventional pipeline can be formulated as:

$$
\begin{array} { r l } & { \quad p _ { l a } ( p _ { e r } ( \{ \mathbf { s } ^ { T } , \cdots , \mathbf { s } ^ { T - t } \} ) , p _ { r e } ( p _ { e r } ( \{ \mathbf { s } ^ { T } , \cdots , \mathbf { \phi } ^ { T - t } \} ) ) ) } \\ & { = \{ \mathbf { p } ^ { T + 1 } , \mathbf { p } ^ { T + 2 } , \cdots , \mathbf { p } ^ { T + f } \} . } \end{array}\tag{2}
$$

Despite the promising performance of this framework [17, 18, 25], it usually requires ground-truth labels for supervision at each stage, which can be laborious to annotate. It only considers object-level movement and fails to model more fine-grained evolutions.

Motivated by this, we explore a new world-model-based autonomous driving paradigm to comprehensively model the evolution of the surrounding scenes and the ego movements. Inspired by the recent success of generative pretraining transformers (GPT) [2] in natural language processing (NLP), we propose an auto-regressive generative modeling framework for autonomous driving scenarios. We define a world model w to act on scene representations y and be able to predict future scenes. Formally, we formulate the function of a world model w as follows:

$$
w ( \{ \mathbf { y } ^ { T } , \cdot \cdot \cdot , \mathbf { y } ^ { T - t } \} , \{ \mathbf { p } ^ { T } , \cdot \cdot \cdot , \mathbf { p } ^ { T - t } \} ) = \mathbf { y } ^ { T + 1 } , \mathbf { p } ^ { T + 1 } .\tag{3}
$$

Having obtained the predicted scene $\mathbf { y } ^ { T + 1 }$ and the ego position $\bar { \mathbf p } ^ { T + 1 }$ , we can add them to the input and further predict the next frame in an auto-regressive manner, as shown in Figure 2. The world model w captures the joint distribution of the evolution of the surrounding scene and the ego vehicle, considering their high-order interactions.

![](images/555abb47bde832a8236f8066c559966247d40f4acf11f07affabcce6222384d3.jpg)  
Figure 3. Illustration of the proposed 3D occupancy scene tokenizer. We use CNNs to encode the 3D occupancy and perform vector quantization to obtain discrete tokens using a learnable codebook [41]. We then employ a decoder to reconstruct the input 3D occupancy using the quantized tokens and use a reconstruction objective to train the autoencoder and codebook simultaneously.

## 3.2. 3D Occupancy Scene Tokenizer

As the world model w operates on the scene representation y, its choice is vital to the performance of the world model. We select y based on three principles: 1) expressiveness. It should be able to comprehensively contain the 3D structural and semantic information of the 3D scene; 2) efficiency. It should be economical to learn (e.g., from weak supervision or self-supervision); 3) versatility. It should be able to adapt to both vision and LiDAR modalities.

Considering all the aforementioned principles, we propose to adopt 3D occupancy as the 3D scene representation $\mathbf { y } \in \mathbb { R } ^ { \hat { H } \times W \times D }$ . 3D occupancy partitions the 3D space surrounding the ego car into $H \times W \times D$ voxels and assigns each voxel with a label l denoting whether it is occupied and which material it is occupied with. 3D occupancy provides a dense representation of the 3D scene and can describe both the 3D structural and semantic information of the scene. It can be effectively learned from sparse Li-DAR annotations [21] or potentially from self-supervision of temporal frames [20]. 3D occupancy is also modalityagnostic and can be obtained from monocular camera [4], surrounding cameras [21, 53, 57], or LiDAR [69].

Despite its comprehensiveness, 3D occupancy only provides a low-level understanding of the scene, making it difficult to directly model its evolution. We therefore propose a self-supervised way to tokenize the scene into high-level tokens from 3D occupancy. We train a vector-quantized autoencoder (VQ-VAE) [41] on y to obtain discrete tokens z to better represent the scene, as shown in Figure 3.

For efficiency, we first transform the 3D occupancy $\textbf { y } \in$ $\mathbb { R } ^ { H \times W \times D }$ to a BEV representation $\hat { \mathbf { y } } \in \mathbb { R } ^ { H \times \hat { W } \times D ^ { * } C ^ { \prime } }$ by assigning each category with a learnable class embedding $\in \mathbb { R } ^ { \bar { C } ^ { \prime } }$ and concatenating them in the height dimension. We then adopt a lightweight encoder composed of 2D convolution layers to obtain down-sampled features $\hat { \mathbf { z } } \in \mathbb { R } ^ { \frac { H } { d } \times \frac { W } { d } \times C }$ of the scene, where d is the down-sampling factor.

To obtain a more compact representation, we simultaneously learn a codebook $\mathbf { \bar { C } } \in \mathbb { R } ^ { N \times D }$ containing N codes. Each code $\mathbf { c } \in \mathbb { R } ^ { C }$ in the codebook encodes a high-level concept of the scene, $\mathrm { e . g . }$ , whether the corresponding position is occupied by a car. We quantized each spatial feature $\hat { \mathbf { z } } _ { i j }$ in zˆ by classifying it to the nearest code $\mathcal { N } ( \hat { \mathbf { z } } _ { i j } , \mathbf { C } )$

$$
\mathbf { z } _ { i j } = \mathcal { N } ( \hat { \mathbf { z } } _ { i j } , \mathbf { C } ) = \operatorname* { m i n } _ { \mathbf { c } \in \mathbf { C } } | | \hat { \mathbf { z } } _ { i j } - \mathbf { c } | | _ { 2 } ,\tag{4}
$$

where $| | \cdot | | _ { 2 }$ denotes the L2 norm. We then integrate the quantized features $\{ { \bf z } _ { i j } \}$ to obtain the final scene representation $\mathbf { z } \in \mathbb { R } ^ { H \times W \times \mathbf { \dot { C } } }$

To reconstruct $\widetilde { \mathbf { y } }$ from the learned scene representation z, we use a decoder of 2D deconvolution layers to progressively upsample z to its original BEV resolution $\mathbf { \bar { \boldsymbol { H } } } \times \mathbf { \bar { \boldsymbol { W } } } \times \mathbf { \boldsymbol { C } } ^ { \prime \prime }$ . We then perform a split in the channel dimension to reconstruct the height dimension $\begin{array} { r } { H \times W \times D \times \frac { C ^ { \prime \prime } } { D } } \end{array}$ and apply a softmax layer on each spatial feature to classify them into occupied semantics or unoccupied $H \times W \times D$

The scene tokenizer transforms 3D occupancy into a more compact discrete space to encode higher-level concepts. This refined compact space facilitates the modeling of scene evolution for the subsequent world model.

## 3.3. Spatial-Temporal Generative Transformer

The core of autonomous driving lies in the prediction of how the surrounding world evolves and planning the movement of the ego vehicle accordingly. While conventional methods usually perform the two tasks separately [17, 18], we propose to learn a world model w to jointly model the distributions of scene evolution and ego trajectory.

As defined in (3), a world model w takes as inputs the past scenes and ego positions and predicts their outcome after driving a certain time interval. Based on expressiveness, efficiency, and versatility, we adopt 3D occupancy y as the scene representation and use a self-supervised tokenizer to obtain high-level scene tokens ${ \bf T } = \{ { \bf z } _ { i } \}$ . To integrate the ego movement, we further aggregate T with an ego token $\mathbf { z } _ { 0 } \in \mathbb { R } ^ { C }$ to encode the spatial position of the ego vehicle.

The proposed OccWorld w then functions on the world tokens T, which can be formulated as:

$$
w ( \mathbf { T } ^ { T } , \cdot \cdot \cdot , \mathbf { T } ^ { T - t } ) = \mathbf { T } ^ { T + 1 } ,\tag{5}
$$

where $T$ is the current time stamp, and t is the number of history frames available.

Inspired by the remarkable sequential prediction performance of GPT [2], we adopt a GPT-like autoregressive transformer architecture to instantiate (5). However, the migration of GPT from natural language processing to the autonomous driving scenario is not trivial. GPTs predict a single token each time, while the world model w in autonomous driving is required to predict a set of tokens T as

![](images/1851a50bcd677273965c1421e68831a0bf393ba32d336b04fe12ebd478898ddf.jpg)

Figure 4. Illustration of the proposed spatial-temporal generative transformer. As each scene is composed of numerous world tokens, we adopt spatial mixing modules to model their intrinsic dependencies and obtain multi-scale world tokens to capture multi-level information. We then perform spatial-wise temporal causal self-attention at each level to forecast the next scene. We employ a U-net structure to aggregate the multi-scale predictions. the next future. Due to the vast number of world tokens, directly leveraging the GPT architecture to predict each token $\in \mathbf { T } ^ { \overline { { T } } + 1 }$ is both inefficient and ineffective.

Both the spatial relations of world tokens within each time stamp and the temporal relations of tokens across different time stamps should be considered to comprehensively model the world evolution. Therefore, we propose a spatial-temporal generative transformer architecture to effectively process past world tokens and make predictions of the next future, as shown in Figure 4.

We apply spatial aggregation (e.g., self-attention [8]) to world tokens T to enable interactions between scene tokens as well as ego tokens. We then merge the scene tokens in each $2 \times 2$ window with a stride of 2 and thus down-sample the scene tokens by a factor of 4. We repeat this procedure for K times to obtain world tokens of hierarchical scales $\{ \mathbf { T } _ { 0 } , \cdots , \mathbf { T } _ { K } \}$ to describe the 3D scene at different levels.

We use several sub-world models $w = \{ w _ { 0 } , \cdot \cdot \cdot , w _ { K } \}$ to predict the future at different spatial scales. For each sub-world model w , we impose temporal attention on the tokens $\{ \mathbf { z } _ { j , i } ^ { T } , \cdot \cdot \cdot , \mathbf { z } _ { j , i } ^ { \bar { T } - t } \}$ at each position j to obtain the predicted corresponding token $\mathbf { z } _ { j , i } ^ { T + 1 }$ of the next frame:

$$
\begin{array} { r } { \hat { \mathbf { z } } _ { j , i } ^ { T + 1 } = \mathrm { T A } ( \mathbf { z } _ { j , i } ^ { T } , \cdot \cdot \cdot , \mathbf { z } _ { j , i } ^ { T - t } ) , } \end{array}\tag{6}
$$

where TA denotes masked temporal attention which blocks the effect of future tokens to previous tokens. $\mathbf { z } _ { j , i } ^ { t } \in \mathbf { T } _ { i } ^ { t }$ represents the j-th world token of the i-th scale at time stamp t. We finally employ a U-net structure to aggregate predicted tokens at different scales to ensure spatial consistency.

Our spatial-temporal generative transformer can model the world evolution in driving sequences considering the joint distributions of world tokens within each time and across time. The temporal attention predicts the evolution of a fixed position in the surrounding area, while the spatial aggregation makes each token aware of the global scene.

## 3.4. OccWorld: a 3D Occupancy World Model

We present the overall training framework of our OccWorld model for autonomous driving. Having obtained the forecasted world tokens, we reuse the scene decoder d to decode the predicted 3D occupancy $\hat { \mathbf { y } } ^ { T + 1 } = d ( \hat { \mathbf { z } } ^ { T + 1 } )$ and additionally learn an ego decoder $d _ { e g o }$ to produce the ego displacement $\hat { p } ^ { T + 1 } = \bigcup _ { e g o } ( \hat { z } _ { 0 } ^ { T + 1 } )$ w.r.t the current frame.

We adopt a two-stage training strategy to effectively train our OccWorld. For the first stage, we train the scene tokenizer e and decoder d using 3D occupancy loss [21]:

$$
J _ { e , d } = L _ { s o f t } ( d ( e ( \mathbf { y } ) ) , \mathbf { y } ) + \lambda _ { 1 } L _ { l o v a s z } ( d ( e ( \mathbf { y } ) ) , \mathbf { y } ) ,\tag{7}
$$

where $\scriptstyle L _ { s o f t }$ and $L _ { l o v a s z }$ is the softmax and lovasz-softmax loss [1], respectively, and $\lambda _ { 1 }$ is a balance factor.

For the second stage, we adopt the learned scene tokenizer e to obtain scene tokens z for all the frames and constrain the discrepancy between predicted tokens zˆ and z. We then apply the softmax loss to enforce the correct classification of zˆ to the correct codes in the codebook C as z. For the ego token, we simultaneously learn the ego decoder $d _ { e g o }$ and apply L2 loss on the predicted displacement $\hat { p } = d _ { e g o } ( \hat { \mathbf { z } } _ { 0 } )$ and the ground-truth one p. The overall objective for the second stage can be formulated as follows:

$$
\begin{array} { r } { J _ { w , d _ { e g o } } = \displaystyle \sum _ { t = 1 } ^ { T } ( \sum _ { j = 1 } ^ { M _ { 0 } } L _ { s o f t } ( \hat { \mathbf { z } } _ { j , 0 } ^ { t } , \mathbf { C } ( \mathbf { z } _ { j , 0 } ^ { t } ) } \\ { + \lambda _ { 2 } L _ { L 2 } ( d _ { e g o } ( \hat { \mathbf { z } } _ { 0 } ^ { t } ) , \mathbf { p } ^ { t } ) ) , } \end{array}\tag{8}
$$

where T and $M _ { 0 }$ are the numbers of frames and spatial tokens of the original scale, respectively. $\mathbf { C } ( \cdot )$ denotes the index of the corresponding code in the codebook C. $L _ { L 2 }$ measures the L2 discrepancy between two trajectories.

For efficient training, we use tokens obtained by the scene tokenizer e as inputs but apply masked temporal attention [2] to block the effect of future tokens. During inference, we progressively predict world tokens of the next frame using predicted tokens of past frames.

Our OccWorld can be applied to various types of 3D occupancy to adapt to different settings (e.g., end-to-end autonomous driving). The scene representation model r can be an oracle providing ground-truth occupancy, or a perception model taking images or LiDAR as inputs. Different from the conventional perception, predicting, and planning pipeline, OccWorld models the joint evolution of the surrounding scene and the ego movement to capture highorder interactions between the ego vehicle and the environment. Combined with machine-annotated [57], LiDARcollected [21], or self-supervised [20] 3D occupancy, Occ-World has the potential to scale up to large-scale training, paving the way for large driving models.

Table 1. 4D occupancy forecasting performance. Aux. Sup. denotes auxiliary supervision apart from the ego trajectory. Avg. denotes the average performance of that in 1s, 2s, and 3s. We use bold numbers to denote the best results.
<table><tr><td rowspan="2">Method</td><td rowspan="2">Input</td><td rowspan="2">Aux. Sup.</td><td colspan="4">mIoU (%) ↑</td><td rowspan="2">IoU (%) ↑</td><td colspan="5"></td><td rowspan="2">FPS</td></tr><tr><td>0s</td><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td><td>0s 1s</td><td>2s</td><td>3s</td><td>Avg.</td></tr><tr><td>Copy&amp;Paste</td><td>3D-Occ</td><td>None</td><td>66.38</td><td>14.91</td><td>10.54</td><td>8.52</td><td>11.33</td><td>62.29</td><td>24.47</td><td>19.77</td><td>17.31</td><td>20.52</td><td></td></tr><tr><td>OccWorld-O</td><td>3D-Occ</td><td>None</td><td>66.38</td><td>25.78</td><td>15.14</td><td>10.51</td><td>17.14</td><td>62.29</td><td>34.63</td><td>25.07</td><td>20.18</td><td>26.63</td><td>18.0</td></tr><tr><td>OccWorld-D</td><td>Camera</td><td>3D-Occ</td><td>18.63</td><td>11.55</td><td>8.10</td><td>6.22</td><td>8.62</td><td>22.88</td><td>18.90</td><td>16.26</td><td>14.43</td><td>16.53</td><td>2.8</td></tr><tr><td>OccWorld-T</td><td>Camera</td><td>Semantic LiDAR</td><td>7.21</td><td>4.68</td><td>3.36</td><td>2.63</td><td>3.56</td><td>10.66</td><td>9.32</td><td>8.23</td><td>7.47</td><td>8.34</td><td>2.8</td></tr><tr><td>OccWorld-S</td><td>Camera</td><td>None</td><td>0.27</td><td>0.28</td><td>0.26</td><td>0.24</td><td>0.26</td><td>4.32</td><td>5.05</td><td>5.01</td><td>4.95</td><td>5.00</td><td>2.8</td></tr></table>

![](images/0af4709011cd8367a1799aab566ab6ba872caba7e582d85066692f0dd3f374a7.jpg)  
Figure 5. Visualizations of the forecasting and planning results of OccWorld-O, OccWorld-D, and OccWorld-T.

## 4. Experiments

## 4.1. Task Descriptions

In this paper, we explore a world-model-based framework for autonomous driving and propose OccWorld to model the joint evolutions of ego trajectory and scene evolutions. We conduct two tasks to evaluate our OccWorld: 4D occupancy forecasting on the Occ3D dataset [52] and motion planning on the nuScenes dataset [3]. We present the dataset and evaluation metric details in the supplementary material.

4D occupancy forecasting. 3D occupancy prediction aims to reconstruct the semantic occupancy for each voxel in the surrounding space, which cannot capture the temporal evolution of the 3D occupancy. In this paper, we explore the task of 4D occupancy forecasting, which aims to forecast the future 3D occupancy given a few historical occupancy inputs. We use mIoU and IoU as the evaluation metric.

Motion planning. The objective of motion planning is to produce safe future trajectories for the self-driving vehicle given ground-truth surrounding information or perception results. The planned trajectory is represented by a series of 2D waypoints in the BEV plane (ground plane). We use L2 error and collision rate as the evaluation metric.

## 4.2. Implementation Details

We followed existing works [18, 25] and used a 2-second historical context to forecast the subsequent 3 seconds. The scene tokenizer employs a down-sampling factor of 4, featuring a codebook comprising 512 nodes and a 128- dimensional feature representation. The spatial-temporal generative transformer comprises 3 scales, each incorporating 6 layers of spatial-wise temporal attention for scene tokens with 2 layers of spatial cross-attention and temporal cross-attention for ego planning tokens.

Table 2. Motion planning performance. Aux. Sup. denotes auxiliary supervision apart from the ego trajectory. We use bold and underlined numbers to denote the best and second-best results, respectively. <sup>†</sup> denotes using the metric computation adopted in VAD [25].
<table><tr><td rowspan="2">Method</td><td rowspan="2">Input</td><td rowspan="2">Aux. Sup.</td><td colspan="4">L2 (m) ↓</td><td colspan="4">Collision Rate (%) ↓</td><td rowspan="2">FPS</td></tr><tr><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td></tr><tr><td>IL [43]</td><td>LiDAR</td><td>None</td><td>0.44</td><td>1.15</td><td>2.47</td><td>1.35</td><td>0.08</td><td>0.27</td><td>1.95</td><td>0.77</td><td>–</td></tr><tr><td>NMP [64]</td><td>LiDAR</td><td>Box &amp; Motion</td><td>0.53</td><td>1.25</td><td>2.67</td><td>1.48</td><td>0.04</td><td>0.12</td><td>0.87</td><td>0.34</td><td></td></tr><tr><td>FF [16]</td><td>LiDAR</td><td>Freespace</td><td>0.55</td><td>1.20</td><td>2.54</td><td>1.43</td><td>0.06</td><td>0.17</td><td>1.07</td><td>0.43</td><td>-</td></tr><tr><td>EO [26]</td><td>LiDAR</td><td>Freespace</td><td>0.67</td><td>1.36</td><td>2.78</td><td>1.60</td><td>0.04</td><td>0.09</td><td>0.88</td><td>0.33</td><td>–</td></tr><tr><td>ST-P3 [17]</td><td>Camera</td><td>Map &amp; Box &amp; Depth</td><td>1.33</td><td>2.11</td><td>2.90</td><td>2.11</td><td>0.23</td><td>0.62</td><td>1.27</td><td>0.71</td><td>1.6</td></tr><tr><td>UniAD [18]</td><td>Camera</td><td>Map &amp; Box &amp; Motion &amp; Tracklets &amp; Occ</td><td>0.48</td><td>0.96</td><td>1.65</td><td>1.03</td><td>0.05</td><td>0.17</td><td>0.71</td><td>0.31</td><td>1.8</td></tr><tr><td>VAD-Tiny [25]</td><td>Camera</td><td>Map &amp; Box &amp; Motion</td><td>0.60</td><td>1.23</td><td>2.06</td><td>1.30</td><td>0.31</td><td>0.53</td><td>1.33</td><td>0.72</td><td>16.8</td></tr><tr><td>VAD-Base [25]</td><td>Camera</td><td>Map &amp; Box &amp; Motion</td><td>0.54</td><td>1.15</td><td>1.98</td><td>1.22</td><td>0.04</td><td>0.39</td><td>1.17</td><td>0.53</td><td>4.5</td></tr><tr><td>OccNet [53]</td><td>Camera</td><td>3D-Occ &amp; Map &amp; Box</td><td>1.29</td><td>2.13</td><td>2.99</td><td>2.14</td><td>0.21</td><td>0.59</td><td>1.37</td><td>0.72</td><td>2.6</td></tr><tr><td>OccNet [53]</td><td>3D-Occ</td><td>Map &amp; Box</td><td>1.29</td><td>2.31</td><td>2.98</td><td>2.25</td><td>0.20</td><td>0.56</td><td>1.30</td><td>0.69</td><td>-</td></tr><tr><td>OccWorld-O</td><td>3D-Occ</td><td>None</td><td>0.43</td><td>1.08</td><td>1.99</td><td>1.17</td><td>0.07</td><td>0.38</td><td>1.35</td><td>0.60</td><td>18.0</td></tr><tr><td>OccWorld-D</td><td>Camera</td><td>3D-Occ</td><td>0.52</td><td>1.27</td><td>2.41</td><td>1.40</td><td>0.12</td><td>0.40</td><td>2.08</td><td>0.87</td><td>2.8</td></tr><tr><td>OccWorld-T</td><td>Camera</td><td>Semantic LiDAR</td><td>0.54</td><td>1.36</td><td>2.66</td><td>1.52</td><td>0.12</td><td>0.40</td><td>1.59</td><td>0.70</td><td>2.8</td></tr><tr><td>OccWorld-S</td><td>Camera</td><td>None</td><td>0.67</td><td>1.69</td><td>3.13</td><td>1.83</td><td>0.19</td><td>1.28</td><td>4.59</td><td>2.02</td><td>2.8</td></tr><tr><td>VAD-Tiny† [25]</td><td>Camera</td><td>Map &amp; Box &amp; Motion</td><td>0.46</td><td>0.76</td><td>1.12</td><td>0.78</td><td>0.21</td><td>0.35</td><td>0.58</td><td>0.38</td><td>16.8</td></tr><tr><td>VAD-Base† [25]</td><td>Camera</td><td>Map &amp; Box &amp; Motion</td><td>0.41</td><td>0.70</td><td>1.05</td><td>0.72</td><td>0.07</td><td>0.17</td><td>0.41</td><td>0.22</td><td>4.5</td></tr><tr><td>OccWorld-O†</td><td>3D-0cc</td><td>None</td><td>0.32</td><td>0.61</td><td>0.98</td><td>0.64</td><td>0.06</td><td>0.21</td><td>0.47</td><td>0.24</td><td>18.0</td></tr><tr><td>OccWorld-D†</td><td>Camera</td><td>3D-Occ</td><td>0.39</td><td>0.73</td><td>1.18</td><td>0.77</td><td>0.11</td><td>0.19</td><td>0.67</td><td>0.32</td><td>2.8</td></tr><tr><td>OccWorld-T†</td><td>Camera</td><td>Semantic LiDAR</td><td>0.40</td><td>0.77</td><td>1.28</td><td>0.82</td><td>0.12</td><td>0.22</td><td>0.56</td><td>0.30</td><td>2.8</td></tr><tr><td>OccWorld-S†</td><td>Camera</td><td>None</td><td>0.49</td><td>0.95</td><td>1.55</td><td>0.99</td><td>0.19</td><td>0.56</td><td>1.54</td><td>0.76</td><td>2.8</td></tr></table>

During training, we applied mask operations to all temporal attention mechanisms to prevent the influence of future information on forecasting. For inference, we employ autoregressive prediction to foresee 3 seconds into the future based on a 2-second historical context. We adopted the AdamW optimizer [39] and a Cosine Annealing scheduler [38] for training. We set an initial learning rate of 1 × 10<sup>−3</sup> and the weight decay at 0.01 and. We use a batch size of 1 per GPU on 8 NVIDIA GeForce RTX 4090 GPUs.

## 4.3. Results and Analysis

4D occupancy forecasting. We evaluated the 4D occupancy forecasting performance of our OccWorld in several settings: OccWorld-O (using ground-truth 3D occupancy), OccWorld-D (using predicted results of TPVFormer [21] trained with dense ground-truth 3D occupancy), OccWorld-T (using predicted results of TPVFormer [21] trained with sparse semantic LiDAR<sup>1</sup>), and OccWorld-S (using predicted results of TPVFormer [20] trained in a selfsupervised manner<sup>2</sup>). Copy&Paste denotes copying the current ground-truth occupancy as future observations. The 0s results represent the reconstruction accuracy.

We compare the performance of the aforementioned settings in Table 1. We observe that OccWorld-O can generate non-trivial future 3D occupancy with much better results than Copy&Paste, showing that our model learns the underlying scene evolution. OccWorld-D, OccWorld-T, and OccWorld-S can be seen as end-to-end vision-based 4D occupancy forecasting methods as they take surrounding images as input. This task is very challenging since it requires both 3D structure reconstruction and forecasting. It is especially difficult for the self-supervised OccWorld-S, which exploits no 3D occupancy information even during training. Still, our OccWorld generates future 3D occupancy with non-trivial mIoU and IoU on the end-to-end setting.

Visualizations. We visualize the output results of the proposed OccWorld in Figure 5. We see that our models can successfully forecast the movements of cars and can complete unseen map elements in the inputs such as drivable areas. The planning trajectory is also more accurate with better 4D occupancy forecasting.

Motion planning. We compare the motion planning performance of the proposed OccWorld with state-of-the-art end-to-end autonomous driving methods, as shown in Table 2. We also evaluate our model under different settings as those in the 4D occupancy forecasting task.

We see that UniAD achieves the best overall performance, which exploits various types of auxiliary supervision to improve its planning quality. Despite the strong performance, the additional annotations in the 3D space are very difficult to obtain, making it difficult to scale to largescale driving data. As an alternative, OccWorld demonstrates competitive performance by employing 3D occupancy as the scene representation which can be efficiently obtained by accumulating LiDAR scans [57].

Table 3. Effect of different hyperparameters for the scene tokenizer. We use bold numbers to denote the best results.
<table><tr><td rowspan="2">Setting</td><td colspan="2">Reconstruction</td><td colspan="4">Forecasting mIoU (%) ↑</td><td colspan="4">Planning L2 (m) ↓</td><td rowspan="2">FPS</td></tr><tr><td>mIoU ↑</td><td>IoU↑</td><td>1s</td><td> $2 \mathrm { s }$ </td><td> $3 s$ </td><td>Avg.</td><td>1s</td><td>2s</td><td>3s</td><td>Avg.</td></tr><tr><td>(502, 128, 512)</td><td>66.38</td><td>62.29</td><td>25.78</td><td>15.14</td><td>10.51</td><td>17.14</td><td>0.43</td><td>1.08</td><td>1.99</td><td>1.17</td><td>18.0</td></tr><tr><td>(502, 128, 256)</td><td>63.40</td><td>60.33</td><td>24.25</td><td>14.34</td><td>10.13</td><td>16.24</td><td>0.42</td><td>1.08</td><td>1.95</td><td>1.15</td><td>17.8</td></tr><tr><td>(502, 128, 1024)</td><td>60.50</td><td>59.07</td><td>23.55</td><td>14.66</td><td>10.68</td><td>16.30</td><td>0.47</td><td>1.18</td><td>2.19</td><td>1.28</td><td>17.8</td></tr><tr><td>(252, 256, 512)</td><td>36.28</td><td>44.02</td><td>12.10</td><td>8.13</td><td>6.20</td><td>8.81</td><td>3.27</td><td>6.54</td><td>9.78</td><td>6.53</td><td>28.1</td></tr><tr><td>(1002, 128, 512)</td><td>78.12</td><td>71.63</td><td>18.71</td><td>10.75</td><td>7.68</td><td>12.38</td><td>0.50</td><td>1.25</td><td>2.33</td><td>1.36</td><td>6.7</td></tr><tr><td>(502, 64, 512)</td><td>64.98</td><td>61.50</td><td>21.83</td><td>12.90</td><td>9.28</td><td>14.67</td><td>0.49</td><td>1.24</td><td>2.26</td><td>1.33</td><td>20.1</td></tr></table>

Table 4. Ablation study of the spatial-temporal generative transformer. We report average results over the 1s, 2s, and 3s.
<table><tr><td>Method</td><td colspan="2">Forecast mIoU↑ IoU↑</td><td colspan="2">Planning L2↓ Col.↓</td><td rowspan="2">FPS</td></tr><tr><td>OccWorld-O</td><td>17.14</td><td>26.63</td><td>1.17</td><td>0.60</td></tr><tr><td>w/o spatial attn</td><td>10.07</td><td>21.44</td><td>1.42</td><td>1.21</td><td>18.0 28.6</td></tr><tr><td>w/o temporal attn</td><td>8.98</td><td>20.10</td><td>2.06</td><td>2.56</td><td>26.5</td></tr><tr><td>w/o ego w/o ego temporal</td><td>15.13 12.07</td><td>24.66 23.09</td><td>5.89</td><td>6.23</td><td>18.8 18.5</td></tr></table>

We observe that using ground-truth 3D occupancy as inputs, our OccWorld-O outperforms the previous perceptionprediction-planning-based method OccNet [53] by a large margin without using maps and bounding boxes as supervision, demonstrating the superiority of the world-model paradigm for autonomous driving. Our end-to-end models OccWorld-D and OccWorld-T also demonstrate competitive performance using only 3D occupancy as supervision and OccWorld-S delivers non-trivial results with no supervision other than the future trajectory, showing the potential for interpretable end-to-end autonomous driving.

Though our model demonstrates very competitive L2 error, it slightly falls behind on the collision rate. This is because it is more difficult to learn safe trajectories without the guidance of freespace or bounding box. Still, OccWorld-O demonstrates comparable collision rates with OccNet which exploits map and box supervision, showing that OccWorld can learn the concept of freespace with 3D occupancy.

We also observe that OccWorld shows excellent shortterm planning performance (1s), but worsens quickly when planning longer futures. For example, OccWorld-O achieves the best L2 error at 1s among all the methods but reaches 1.99 at 3s compared to 1.65 of UniAD. This might result from the diverse future generations of world models, which might deviate from the ground-truth trajectory.

Analysis of the scene tokenizer. We analyze the effect of different hyperparameters for the scene tokenizer in Table 3. The setting denotes latent spatial resolution, latent channel dimension, and the codebook size. We see that using a larger codebook than 512 leads to overfitting and using a smaller codebook, spatial resolution, or channel dimen sion might not be enough to capture the scene distribution. The reconstruction accuracy greatly improves with a larger spatial resolution, yet leads to poor forecasting and planning performance. This is because the tokens cannot learn high-level concepts and are difficult to forecast the future.

Analysis of the spatial-temporal generative transformer. We conducted an ablation study on both 4D occupancy forecasting and motion planning to analyze the design of the proposed spatial-temporal generative transformer, as shown in Table 4. w/o spatial attn denotes discarding spatial aggregation and directly applying temporal attention to the input tokens. w/o temporal attn represents that we replace the temporal attention with a simple convolution to output the next scene using the current world tokens. w/o ego represents that we discard the ego token. w/o ego temporal represents that we replace the temporal attention of the ego token with a simple MLP. We observe that using spatial aggregation to model spatial dependencies and using temporal attention to integrate history information is vital to the performance of both 4D occupancy forecasting and motion planning tasks. Also, only performing the 4D occupancy forecasting task without predicting motion reduces the performance. This verifies the effectiveness of joint modeling of scene evolutions and ego trajectories. Finally, discarding the ego temporal attention leads to poor planning and surprisingly worse 3D forecast occupancy performance. We think this is because integrating a wrongly predicted ego trajectory will mislead the forecasting.

## 5. Conclusion

In this paper, we have presented a 3D occupancy world model (OccWorld) to model the joint evolutions of ego movements and surrounding scenes. We have employed a 3D occupancy scene tokenizer to extract high-level concepts and used a spatial-temporal generative transformer for future prediction in an auto-regressive manner. Both quan titive and visualization results have shown that OccWorld can effectively predict future scene evolutions in the comprehensive 3D semantic occupancy space. We believe that OccWorld has paved the way for interpretable end-to-end autonomous driving without additional supervision signals.

## References

[1] Maxim Berman, Amal Rannen Triki, and Matthew B Blaschko. The lovasz-softmax loss: A tractable surrogate´ for the optimization of the intersection-over-union measure in neural networks. In CVPR, pages 4413–4421, 2018. 5

[2] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. NeurIPS, 33:1877– 1901, 2020. 2, 3, 4, 5

[3] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multimodal dataset for autonomous driving. In CVPR, 2020. 6

[4] Anh-Quan Cao and Raoul de Charette. Monoscene: Monocular 3d semantic scene completion. In CVPR, pages 3991– 4001, 2022. 2, 4

[5] Anh-Quan Cao and Raoul de Charette. Scenerf: Selfsupervised monocular 3d scene reconstruction with radiance fields. In ICCV, pages 9387–9398, 2023. 2

[6] Xiaokang Chen, Kwan-Yee Lin, Chen Qian, Gang Zeng, and Hongsheng Li. 3d sketch-aware semantic scene completion via semi-supervised structure prior. In CVPR, pages 4193– 4202, 2020. 2

[7] Ran Cheng, Ryan Razani, Ehsan Taghavi, Enxu Li, and Bingbing Liu. 2-s3net: Attentive feature fusion with adaptive feature selection for sparse semantic segmentation network. In CVPR, pages 12547–12556, 2021. 1

[8] Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, et al. An image is worth 16x16 words: Transformers for image recognition at scale. In ICLR, 2020. 5

[9] Ruiyuan Gao, Kai Chen, Enze Xie, Lanqing Hong, Zhenguo Li, Dit-Yan Yeung, and Qiang Xu. Magicdrive: Street view generation with diverse 3d geometry control. arXiv preprint arXiv:2310.02601, 2023. 2

[10] Ian Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, and Yoshua Bengio. Generative adversarial nets. NeurIPS, 27, 2014. 2

[11] Junru Gu, Chenxu Hu, Tianyuan Zhang, Xuanyao Chen, Yilun Wang, Yue Wang, and Hang Zhao. Vip3d: End-toend visual trajectory prediction via 3d agent queries. arXiv preprint arXiv:2208.01582, 2022. 1, 2

[12] David Ha and Jurgen Schmidhuber. World models.¨ arXiv preprint arXiv:1803.10122, 2018. 2

[13] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In CVPR, pages 770–778, 2016. 2

[14] Anthony Hu, Zak Murez, Nikhil Mohan, Sof´ıa Dudas, Jeffrey Hawke, Vijay Badrinarayanan, Roberto Cipolla, and Alex Kendall. Fiery: Future instance prediction in bird’seye view from surround monocular cameras. In ICCV, 2021. 1, 2

[15] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gian-

luca Corrado. Gaia-1: A generative world model for autonomous driving. arXiv preprint arXiv:2309.17080, 2023. 2

[16] Peiyun Hu, Aaron Huang, John Dolan, David Held, and Deva Ramanan. Safe local motion planning with selfsupervised freespace forecasting. In CVPR, 2021. 7

[17] Shengchao Hu, Li Chen, Penghao Wu, Hongyang Li, Junchi Yan, and Dacheng Tao. St-p3: End-to-end vision-based autonomous driving via spatial-temporal feature learning. In ECCV, 2022. 1, 2, 3, 4, 7

[18] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, et al. Planning-oriented autonomous driving. In CVPR, pages 17853–17862, 2023. 1, 2, 3, 4, 6, 7

[19] Junjie Huang, Guan Huang, Zheng Zhu, and Dalong Du. Bevdet: High-performance multi-camera 3d object detection in bird-eye-view. arXiv preprint arXiv:2112.11790, 2021. 1

[20] Yuanhui Huang, Wenzhao Zheng, Borui Zhang, Jie Zhou, and Jiwen Lu. Selfocc: Self-supervised vision-based 3d occupancy prediction. arXiv preprint arXiv:2311.12754, 2023. 2, 4, 5, 7

[21] Yuanhui Huang, Wenzhao Zheng, Yunpeng Zhang, Jie Zhou, and Jiwen Lu. Tri-perspective view for vision-based 3d semantic occupancy prediction. In CVPR, pages 9223–9232, 2023. 1, 2, 4, 5, 7

[22] Zhiyu Huang, Haochen Liu, and Chen Lv. Gameformer: Game-theoretic modeling and learning of transformer-based interactive prediction and planning for autonomous driving. arXiv preprint arXiv:2303.05760, 2023. 2

[23] Zhiyu Huang, Haochen Liu, Jingda Wu, and Chen Lv. Differentiable integrated motion prediction and planning with learnable cost function for autonomous driving. IEEE transactions on neural networks and learning systems, 2023. 2

[24] Bo Jiang, Shaoyu Chen, Xinggang Wang, Bencheng Liao, Tianheng Cheng, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, and Chang Huang. Perceive, interact, predict: Learning dynamic and static clues for end-to-end motion prediction. arXiv preprint arXiv:2212.02181, 2022. 1, 2

[25] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. Vad: Vectorized scene representation for efficient autonomous driving. arXiv preprint arXiv:2303.12077, 2023. 1, 2, 3, 6, 7

[26] Tarasha Khurana, Peiyun Hu, Achal Dave, Jason Ziglar, David Held, and Deva Ramanan. Differentiable raycasting for self-supervised occupancy forecasting. In ECCV, 2022. 2, 7

[27] Tarasha Khurana, Peiyun Hu, David Held, and Deva Ramanan. Point cloud forecasting as a proxy for 4d occupancy forecasting. In CVPR, pages 1116–1124, 2023. 2

[28] Diederik P Kingma and Max Welling. Auto-encoding variational bayes. arXiv preprint arXiv:1312.6114, 2013. 2

[29] Jie Li, Kai Han, Peng Wang, Yu Liu, and Xia Yuan. Anisotropic convolutional networks for 3d semantic scene completion. In CVPR, pages 3351–3359, 2020. 2

[30] Qi Li, Yue Wang, Yilun Wang, and Hang Zhao. Hdmapnet: An online hd map construction and evaluation framework. In ICRA, 2022. 1

[31] Xiaofan Li, Yifu Zhang, and Xiaoqing Ye. Drivingdiffusion: Layout-guided multi-view driving scene video generation with latent diffusion model. arXiv preprint arXiv:2310.07771, 2023. 2

[32] Yinhao Li, Zheng Ge, Guanyi Yu, Jinrong Yang, Zengran Wang, Yukang Shi, Jianjian Sun, and Zeming Li. Bevdepth: Acquisition of reliable depth for multi-view 3d object detection. arXiv preprint arXiv:2206.10092, 2022. 1, 2

[33] Zhiqi Li, Wenhai Wang, Hongyang Li, Enze Xie, Chonghao Sima, Tong Lu, Qiao Yu, and Jifeng Dai. Bevformer: Learning bird’s-eye-view representation from multi-camera images via spatiotemporal transformers. In ECCV, 2022. 1, 2

[34] Bencheng Liao, Shaoyu Chen, Xinggang Wang, Tianheng Cheng, Qian Zhang, Wenyu Liu, and Chang Huang. Maptr: Structured modeling and learning for online vectorized hd map construction. arXiv preprint arXiv:2208.14437, 2022. 1

[35] Venice Erin Liong, Thi Ngoc Tho Nguyen, Sergi Widjaja, Dhananjai Sharma, and Zhuang Jie Chong. Amvnet: Assertion-based multi-view fusion network for lidar semantic segmentation. arXiv preprint arXiv:2012.04934, 2020. 1

[36] Yicheng Liu, Jinghuai Zhang, Liangji Fang, Qinhong Jiang, and Bolei Zhou. Multimodal motion prediction with stacked transformers. In CVPR, 2021. 2

[37] Yicheng Liu, Yue Wang, Yilun Wang, and Hang Zhao. Vectormapnet: End-to-end vectorized hd map learning. arXiv preprint arXiv:2206.08920, 2022. 1

[38] Ilya Loshchilov and Frank Hutter. Sgdr: Stochastic gradient descent with warm restarts. arXiv preprint arXiv:1608.03983, 2016. 7

[39] Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. arXiv preprint arXiv:1711.05101, 2017. 7

[40] Benedikt Mersch, Xieyuanli Chen, Jens Behley, and Cyrill Stachniss. Self-supervised point cloud prediction using 3d spatio-temporal convolutional networks. In CoRL, pages 1444–1454. PMLR, 2022. 2

[41] Aaron van den Oord, Oriol Vinyals, and Koray Kavukcuoglu. Neural discrete representation learning. arXiv preprint arXiv:1711.00937, 2017. 2, 4

[42] Jonah Philion and Sanja Fidler. Lift, splat, shoot: Encoding images from arbitrary camera rigs by implicitly unprojecting to 3d. In ECCV, pages 194–210, 2020. 1

[43] Nathan D Ratliff, J Andrew Bagnell, and Martin A Zinkevich. Maximum margin planning. In Proceedings of the 23rd international conference on Machine learning, pages 729–736, 2006. 7

[44] Cody Reading, Ali Harakeh, Julia Chae, and Steven L Waslander. Categorical depth distribution network for monocular 3d object detection. In CVPR, 2021. 1

[45] Katrin Renz, Kashyap Chitta, Otniel-Bogdan Mercea, A Koepke, Zeynep Akata, and Andreas Geiger. Plant: Explainable planning transformers via object-level representations. arXiv preprint arXiv:2210.14222, 2022. 1

[46] Luis Roldao, Raoul de Charette, and Anne Verroust-Blondet. Lmscnet: Lightweight multiscale 3d semantic completion.

In 2020 International Conference on 3D Vision (3DV), pages 111–119, 2020. 2

[47] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Bjorn Ommer. High-resolution image syn-¨ thesis with latent diffusion models. In CVPR, pages 10684– 10695, 2022. 2

[48] Karen Simonyan and Andrew Zisserman. Very deep convolutional networks for large-scale image recognition. arXiv, abs/1409.1556, 2014. 2

[49] Richard S Sutton. Dyna, an integrated architecture for learning, planning, and reacting. ACM Sigart Bulletin, 2(4):160– 163, 1991. 2

[50] Christian Szegedy, Wei Liu, Yangqing Jia, Pierre Sermanet, Scott E Reed, Dragomir Anguelov, Dumitru Erhan, Vincent Vanhoucke, and Andrew Rabinovich. Going deeper with convolutions. In CVPR, pages 1–9, 2015. 2

[51] Haotian Tang, Zhijian Liu, Shengyu Zhao, Yujun Lin, Ji Lin, Hanrui Wang, and Song Han. Searching efficient 3d architectures with sparse point-voxel convolution. In ECCV, pages 685–702, 2020. 1

[52] Xiaoyu Tian, Tao Jiang, Longfei Yun, Yue Wang, Yilun Wang, and Hang Zhao. Occ3d: A large-scale 3d occupancy prediction benchmark for autonomous driving. arXiv preprint arXiv:2304.14365, 2023. 2, 6

[53] Wenwen Tong, Chonghao Sima, Tai Wang, Li Chen, Silei Wu, Hanming Deng, Yi Gu, Lewei Lu, Ping Luo, Dahua Lin, et al. Scene as occupancy. In ICCV, pages 8406–8415, 2023. 2, 4, 7, 8

[54] Matt Vitelli, Yan Chang, Yawei Ye, Ana Ferreira, Maciej Wołczyk, Błazej Osi˙ nski, Moritz Niendorf, Hugo Grimmett,´ Qiangui Huang, Ashesh Jain, et al. Safetynet: Safe planning for real-world self-driving vehicles using machine-learned policies. In 2022 International Conference on Robotics and Automation (ICRA), pages 897–904, 2022. 2

[55] Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, and Jiwen Lu. Drivedreamer: Towards real-world-driven world models for autonomous driving. arXiv preprint arXiv:2309.09777, 2023. 2

[56] Xiaofeng Wang, Zheng Zhu, Wenbo Xu, Yunpeng Zhang, Yi Wei, Xu Chi, Yun Ye, Dalong Du, Jiwen Lu, and Xingang Wang. Openoccupancy: A large scale benchmark for surrounding semantic occupancy perception. arXiv preprint arXiv:2303.03991, 2023. 2

[57] Yi Wei, Linqing Zhao, Wenzhao Zheng, Zheng Zhu, Jie Zhou, and Jiwen Lu. Surroundocc: Multi-camera 3d occupancy prediction for autonomous driving. In ICCV, pages 21729–21740, 2023. 1, 2, 4, 5, 8

[58] Xinshuo Weng, Jianren Wang, Sergey Levine, Kris Kitani, and Nicholas Rhinehart. Inverting the pose forecasting pipeline with spf2: Sequential pointcloud forecasting for sequential pose forecasting. In Conference on robot learning, pages 11–20, 2021. 2

[59] Xu Yan, Jiantao Gao, Jie Li, Ruimao Zhang, Zhen Li, Rui Huang, and Shuguang Cui. Sparse single sweep lidar point cloud segmentation via learning contextual shape priors from scene completion. In AAAI, pages 3101–3109, 2021. 2

[60] Kairui Yang, Enhui Ma, Jibin Peng, Qing Guo, Di Lin, and Kaicheng Yu. Bevcontrol: Accurately controlling streetview elements with multi-perspective consistency via bev sketch layout. arXiv preprint arXiv:2308.01661, 2023. 2

[61] Dongqiangzi Ye, Zixiang Zhou, Weijia Chen, Yufei Xie, Yu Wang, Panqu Wang, and Hassan Foroosh. Lidarmultinet: Towards a unified multi-task network for lidar perception. arXiv preprint arXiv:2209.09385, 2022. 1

[62] Maosheng Ye, Rui Wan, Shuangjie Xu, Tongyi Cao, and Qifeng Chen. Drinet++: Efficient voxel-as-point point cloud segmentation. arXiv preprint arXiv: 2111.08318, 2021. 1

[63] Tengju Ye, Wei Jing, Chunyong Hu, Shikun Huang, Lingping Gao, Fangzhen Li, Jingke Wang, Ke Guo, Wencong Xiao, Weibo Mao, et al. Fusionad: Multi-modality fusion for prediction and planning tasks of autonomous driving. arXiv preprint arXiv:2308.01006, 2023. 2

[64] Wenyuan Zeng, Wenjie Luo, Simon Suo, Abbas Sadat, Bin Yang, Sergio Casas, and Raquel Urtasun. End-to-end interpretable neural motion planner. In CVPR, 2019. 7

[65] Yunpeng Zhang, Zheng Zhu, Wenzhao Zheng, Junjie Huang, Guan Huang, Jie Zhou, and Jiwen Lu. Beverse: Unified perception and prediction in birds-eye-view for vision-centric autonomous driving. arXiv preprint arXiv:2205.09743, 2022. 1, 2

[66] Yunpeng Zhang, Zheng Zhu, Wenzhao Zheng, Junjie Huang, Guan Huang, Jie Zhou, and Jiwen Lu. Beverse: Unified perception and prediction in birds-eye-view for vision-centric autonomous driving. arXiv preprint arXiv:2205.09743, 2022. 1, 2

[67] Jinyun Zhou, Rui Wang, Xu Liu, Yifei Jiang, Shu Jiang, Jiaming Tao, Jinghao Miao, and Shiyu Song. Exploring imitation learning for autonomous driving with feedback synthesizer and differentiable rasterization. In IROS, pages 1450– 1457, 2021. 2

[68] Xinge Zhu, Hui Zhou, Tai Wang, Fangzhou Hong, Yuexin Ma, Wei Li, Hongsheng Li, and Dahua Lin. Cylindrical and asymmetrical 3d convolution networks for lidar segmentation. In CVPR, pages 9939–9948, 2021. 1

[69] Sicheng Zuo, Wenzhao Zheng, Yuanhui Huang, Jie Zhou, and Jiwen Lu. Pointocc: Cylindrical tri-perspective view for point-based 3d semantic occupancy prediction. arXiv preprint arXiv:2308.16896, 2023. 2, 4