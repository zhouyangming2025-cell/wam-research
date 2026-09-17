# P0021_HydraMDP - PDF text extraction

> Source PDF: `papers/pdf/P0021_HydraMDP.pdf`
> Conversion: Poppler `pdftotext -layout -enc UTF-8`
> Note: layout-preserving text extraction; the PDF remains the source of truth for figures, exact equations, and wording.

---

                                                      Hydra-MDP: End-to-end Multimodal Planning with Multi-target
                                                                          Hydra-Distillation

                                                  Zhenxin Li1, 2 Kailin Li3 Shihao Wang1, 4 Shiyi Lan1 Zhiding Yu1 Yishen Ji5
                                                Zhiqi Li5 Ziyue Zhu6 Jan Kautz1 Zuxuan Wu2 Yu-Gang Jiang2 Jose M. Alvarez1
                                                              1
                                                                NVIDIA 2 Fudan University 3 East China Normal University
                                                       4
                                                         Beijing Institute of Technology 5 Nanjing University 6 Nankai University
arXiv:2406.06978v4 [cs.CV] 30 Aug 2024




                                                                   Abstract                                                                                      Limited
                                                                                                                     Planning
                                                                                                                                                              Supervision
                                                                                                                                                                              Log-replay
                                             We propose Hydra-MDP, a novel paradigm employing
                                         multiple teachers in a teacher-student model. This approach                 Perception                        Perception GT
                                         uses knowledge distillation from both human and rule-based
                                                                                                                           (a) Single-modal Planning + Single-target Learning
                                         teachers to train the student model, which features a multi-
                                         head decoder to learn diverse trajectory candidates tailored                                                           Limited
                                                                                                                     Planning
                                                                                                                                                              Supervision
                                         to various evaluation metrics. With the knowledge of rule-                                                                           Log-replay
                                         based teachers, Hydra-MDP learns how the environment                        Perception GT

                                         influences the planning in an end-to-end manner instead of                                   Information Loss
                                                                                                                     Perception                        Post-processing
                                         resorting to non-differentiable post-processing. This method                                Detached from NN.

                                         achieves the 1st place in the Navsim challenge, demonstrat-                       (b) Multimodal Planning + Single-target Learning
                                         ing significant improvements in generalization across diverse
                                                                                                                                                           Knowledge from
                                         driving environments and conditions. More details by visiting               Planning
                                                                                                                                                           Various Teachers
                                                                                                                                                                              Log-replay
                                         https://github.com/NVlabs/Hydra-MDP.
                                                                                                                                  Perception GT

                                                                                                                                                            Fully Utilizes
                                         1. Introduction                                                             Perception               Simulation                      Simulation
                                                                                                                                                           Perception GT

                                         End-to-end autonomous driving, which involves learning a                         (c) Multimodal Planning + Multi -target Learning (Ours)
                                         neural planner with raw sensor inputs, is considered a promis-           Figure 1. Comparison between End-to-end Planning Paradigms.
                                         ing direction to achieve full autonomy. Despite the promising
                                         progress in this field [11, 12], recent studies [4, 8, 14] have          consider closed-loop evaluation via post-processing, which
                                         exposed multiple vulnerabilities and limitations of imitation            is not streamlined and may result in the loss of additional
                                         learning (IL) methods, particularly the inherent issues in               information compared to a fully end-to-end pipeline. Mean-
                                         open-loop evaluation, such as the dysfunctional metrics and              while, rule-based planners [8, 18] struggle with imperfect
                                         implicit biases [8, 14]. This is critical as it fails to guarantee       perception inputs. These imperfect inputs degrade the per-
                                         safety, efficiency, comfort, and compliance with traffic rules.          formance of rule-based planning under both closed-loop
                                         To address this main limitation, several works have proposed             and open-loop metrics, as they rely on predicted perception
                                         incorporating closed-loop metrics, which more effectively                instead of ground truth (GT) labels.
                                         evaluate end-to-end autonomous driving by ensuring that                      To address the issues, we propose a novel end-to-end
                                         the machine-learned planner meets essential criteria beyond              autonomous driving framework called Hydra-MDP (Multi-
                                         merely mimicking human drivers.                                          modal Planning with Multi-target Hydra-distillation). Hydra-
                                            Therefore, end-to-end planning is ideally a multi-target              MDP is based on a novel teacher-student knowledge distil-
                                         and multimodal task, where multi-target planning involves                lation (KD) architecture. The student model learns diverse
                                         meeting various evaluation metrics from either open-loop                 trajectory candidates tailored to various evaluation metrics
                                         and closed-loop settings. In this context, multimodal indi-              through KD from both human and rule-based teachers. We
                                         cates the existence of multiple optimal solutions for each               instantiate the multi-target Hydra-distillation with a multi-
                                         metric.                                                                  head decoder, thus effectively integrating the knowledge
                                            Existing end-to-end approaches [4, 11, 12] often try to               from specialized teachers. Hydra-MDP also features an ex-


                                                                                                              1
                 Perception Network                                Trajectory Decoder                            Multi-target Hydra-Distillation




                                                                                                                 Simulation
   LiDAR BEV      Concatenated Front-view Image                                                                                           Rule-based Teachers
                                                               Planning Vocabulary
    LiDAR                     Image
   Backbone                  Backbone                                                                     MLP        𝒮 𝑁𝐶          𝒮 𝑁𝐶
                                                                                                                                            No at-fault Collisions


                                                                              Q
  LiDAR Tokens               Image Tokens
                 Modality                                   K, V     Transformer
                                                                                                          MLP        𝒮 𝐷𝐴𝐶         𝒮 𝐷𝐴𝐶
                 Fusion                                                Decoder
                                         Env. Tokens                                                                                       Drivable Area Compliance




                                                                                                            …




                                                                                                                              …




                                                                                                                                                     …
                                                                         MLP

    Perception                                                     Imitation Score 𝒮 𝑖𝑚                   MLP         𝒮𝐶            𝒮𝐶
      Heads

                                                                    Human Teacher                  Hydra Prediction Heads                          Comfort
                             Ground truth Perceptions


                                                 Figure 2. The Overall Architecture of Hydra-MDP.

tendable KD architecture, allowing for easy integration of                         where Lim is usually an L2 loss.
additional teachers.                                                               B. Multimodal Planning + Single-target Learning. This
   The student model uses environmental observations dur-                          approach [1, 4] predicts multiple trajectories {Ti }ki=1 , whose
ing training, while the teacher models use ground truth (GT)                       similarities to the expert trajectory are computed:
data. This setup allows the teacher models to generate better                                                X
planning predictions, helping the student model to learn ef-                                            L=        Lim (Ti , T̂ ),               (2)
fectively. By training the student model with environmental                                                      i
observations, it becomes adept at handling realistic condi-                        where Lim can be KL-Divergence [4] or the max-margin
tions where GT perception is not accessible during testing.                        loss [1]. Perception outputs P are explicitly used to post-
   Our contributions are summarized as follows:                                    process suitable trajectories via a cost function f (Ti , P ). The
1. We propose a universal framework of end-to-end multi-                           trajectory with the lowest cost is selected:
   modal planning via multi-target hydra-distillation, allow-
   ing the model to learn from both rule-based planners and                                            T ∗ = arg minf (Ti , P ),                                     (3)
                                                                                                                     Ti
   human drivers in a scalable manner.
2. Our approach achieves the state-of-the-art performance                          which is a non-differentiable process based on imperfect
   under the simulation-based evaluation metrics on Navsim.                        perception P .
                                                                                   C. Multimodal Planning + Multi-target Learning. We
2. Solution                                                                        propose this paradigm to simultaneously predict various
                                                                                   costs (e.g., collision cost, drivable area compliance cost) via
2.1. Preliminaries                                                                 a neural network f˜. This is performed in a teacher-student
Let O represent sensor observations, P̂ and P denote ground                        distillation manner, where the teacher has access to ground
truth and predicted perceptions (e.g. 3D object detection,                         truth perception P̂ but the student relies only on sensor
lane detection), T̂ be the expert trajectory, and T ∗ be the pre-                  observations O. This paradigm can be formulated as:
dicted trajectory. Lim represents the imitation loss. We first                               X
introduce the two prevailing paradigms and our proposed                                L=         Lim (Ti , T̂ ) + Lkd (f (Ti , P̂ ), f˜(Ti , O)). (4)
                                                                                              i
paradigm (Fig. 1) in this section:
A. Single-modal Planning + Single-target Learning. In                               Here, we only consider one cost function f for clarity. The
this paradigm [11, 12, 14], the planning network directly re-                       trajectory with the lowest predicted cost is selected:
gresses the planned trajectory from the sensor observations.
Ground truth perceptions can be used as auxiliary supervi-                                             T ∗ = arg minf˜(Ti , O).                                      (5)
                                                                                                                     Ti
sion but does not influence the planning output. Perception
losses are not included in the formula for simplicity. The                             We stress that this framework is not restricted by non-
whole processing can be formulated as:                                              differentiable post-processing. It can be easily scaled in an
                                                                                    end-to-end fashion by involving more cost functions or lever-
                            L = Lim (T ∗ , T̂ ),                        (1)         aging imitation similarity in our implementation (Sec. 2.4).


                                                                               2
2.2. Overall Framework                                                  drivable areas [14]. Therefore, to boost the closed-loop per-
                                                                        formance of our end-to-end planner, we propose Multi-target
As shown in Fig. 2, Hydra-MDP consists of two networks: a
                                                                        Hydra-Distillation, a learning strategy that aligns the planner
Perception Network and a Trajectory Decoder.
                                                                        with simulation-based metrics in this challenge.
Perception Network. Our perception network builds upon                      The distillation process expands the learning target
the official challenge baseline Transfuser [5, 6], which con-           through two steps: (1) running offline simulations [8] of
sists of an image backbone, a LiDAR backbone, and per-                  the planning vocabulary Vk for the entire training dataset;
ception heads for 3D object detection and BEV segmenta-                 (2) introducing supervision from simulation scores for each
tion. Multiple transformer layers [19] connect features from            trajectory in Vk during the training process. For a given
stages of both backbones, extracting meaningful information             scenario, step 1 generates ground truth simulation scores
from different modalities. The final output of the percep-                                   |M |
                                                                        {Ŝim |i = 1, ..., k}m=1 for each metric m ∈ M and the i-th
tion network comprises environmental tokens Fenv , which                trajectory, where M represents the set of closed-loop metrics
encode abundant semantic information derived from both                  used in the challenge. For score predictions, latent vectors
images and LiDAR point clouds.                                          Vk′′ are processed with a set of Hydra Prediction Heads, yield-
Trajectory Decoder. Following Vadv2 [4], we construct a                                                           |M |
                                                                        ing predicted scores {Sim |i = 1, ..., k}m=1 . With a binary
fixed planning vocabulary to discretize the continuous ac-              cross-entropy loss, we distill rule-based driving knowledge
tion space. To build the vocabulary, we first sample 700K               into the end-to-end planner:
trajectories randomly from the original nuPlan database [2].
                                                                                             m      m          m            m
                                                                                     P
Each trajectory Ti (i = 1, ..., k) consists of 40 timestamps               Lkd = −     m,i Ŝi log Si + (1 − Ŝi ) log(1 − Si ).      (10)
of (x, y, heading), corresponding to the desired 10Hz fre-              For a trajectory Ti , its distillation loss of each sub-score acts
quency and a 4-second future horizon in the challenge. The              as a learned cost value in Eq. 4, measuring the violation of
planning vocabulary Vk is formed as K-means clustering                  particular traffic rules associated with that metric.
centers of the 700K trajectories, where k denotes the size of
                                                                        2.4. Inference and Post-processing
the vocabulary. Vk is then embedded as k latent queries with
an MLP, sent into layers of transformer encoders [19], and              2.4.1   Inference
added to the ego status E:
                                                                        Given the predicted imitation scores {Siim |i = 1, ..., k} and
                                                                                                              |M |
   Vk′ = T ransf ormer(Q, K, V          = M lp(Vk )) + E.    (6)        metric sub-scores {Sim |i = 1, ..., k}m=1 , we calculate an
To incorporate environmental clues in Fenv , transformer                assembled cost measuring the likelihood of each trajectory
decoders are leveraged:                                                 being selected in the given scenario as follows:
                                                                        f˜(Ti , O) = − (w1 log Siim + w2 log SiN C + w3 log SiDAC
      Vk′′ = T ransf ormer(Q = Vk′ , K, V = Fenv ).          (7)
                                                                                     + w4 log (5SiT T C + 2SiC + 5SiEP )),           (11)
Using the log-replay trajectory T̂ , we implement a distance-
based cross-entropy loss to imitate human drivers:                      where {wi }4i=1 represent confidence weighting parameters
                            k
                                                                        to mitigate the imperfect fitting of different teachers. The
                            X                                           optimal combination of weights is obtained via grid search,
                 Lim = −          yi log(Siim ),             (8)
                                                                        which typically fall within the following ranges: 0.01 ≤
                            i=1
                                                                        w1 ≤ 0.1, 0.1 ≤ w2 , w3 ≤ 1, 1 ≤ w4 ≤ 10, indicating
where Siim is the i-th softmax score of Vk′′ , and yi is the imi-       the necessity to prioritize rule-based costs over imitation.
tation target produced by L2 distances between log-replays              Finally, the trajectory with the lowest overall cost is chosen.
and the vocabulary. Softmax is applied on L2 distances to
produce a probability distribution:                                     2.4.2   Model Ensembling
                                           2                            We present two model ensembling techniques: Mixture of
                             e−(T̂ −Ti )
                   yi = P k                    2
                                                 .           (9)        Encoders and Sub-score Ensembling. The former technique
                                    −(T̂ −Tj )
                            j=1 e                                       uses a linear layer to combine features from different vision
The intuition behind this imitation target is to reward trajec-         encoders, while the latter calculates a weighted sum of sub-
tory proposals that are close to human driving behaviors.               scores from independent models for trajectory selection.

2.3. Multi-target Hydra-Distillation                                    3. Experiments
Though the imitation target provides certain clues for the              3.1. Dataset and metrics
planner, it is insufficient for the model to associate the plan-
ning decision with the driving environment under the closed-            Dataset. The Navsim dataset builds on the existing Open-
loop setting, leading to failures such as collisions and leaving        Scene [7] dataset, a compact version of nuPlan [3] with only


                                                                    3
           Method                                 Inputs               NC              DAC           EP            TTC            C            Score
           PDM-Closed [8]⋄                    Perception GT            94.6            99.8          89.9          86.9          99.9          89.1
           Transfuser [5]                   LiDAR & Camera             96.5            87.9          73.9          90.2          100           78.0
           Vadv2-V4096 [4]*                 LiDAR & Camera             97.1            88.8          74.9          91.4          100           79.7
           Vadv2-V4096 [4]*-PP              LiDAR & Camera             97.0            89.1          75.0          91.2          100           79.9
           Vadv2-V8192 [4]*                 LiDAR & Camera             97.2            89.1          76.0          91.6          100           80.9
           Hydra-MDP-V4096                  LiDAR & Camera             97.7            91.5          77.5          92.7          100           82.6
           Hydra-MDP-V8192                  LiDAR & Camera             97.9            91.7          77.6          92.9          100           83.0
           Hydra-MDP-V8192 -PDM             LiDAR & Camera             97.5            88.9          74.8          92.5          100           80.2
           Hydra-MDP-V8192 -W               LiDAR & Camera             98.1            96.1          77.8          93.9          100           85.7
           Hydra-MDP-V8192 -W-EP            LiDAR & Camera             98.3            96.0          78.7          94.6          100           86.5

Table 1. Performance on the Navtest Split. ⋄ The official Navsim implementation of PDM-Closed is potentially prone to errors due to
inconsistent braking maneuvers and offset formulation compared with the nuPlan implementation [8]. All end-to-end methods use the
official Transfuser [5] as the perception network. * Our distance-based imitation loss is adopted for training. PP: Transfuser perception is
used for post-processing. PDM: The learning target is the overall PDM score. W: Weighted confidence during inference. EP: The model is
trained to fit the continuous EP (Ego Progress) metric.
       Method                   Img. Resolution            Backbone           NC              DAC           EP            TTC            C         Score
       PDM-Closed [8]⋄                 -                      -               94.6            99.8          89.9          86.9          99.9          89.1
       Hydra-MDP-A               256 × 1024                 ViT-L*            98.4            97.7          85.0          94.5          100           89.9
       Hydra-MDP-B               512 × 2048                 V2-99             98.4            97.8          86.5          93.9          100           90.3
                                 256 × 1024                 ViT-L*
       Hydra-MDP-C               256 × 1024                 ViT-L†            98.7            98.2          86.5          95.0          100           91.0
                                 512 × 2048                 V2-99

Table 2. The Impact of Scaling Up on the Navtest Split. ⋄ The official Navsim implementation of PDM-Closed. * ViT-L is initialized from
Depth Anything [20]. †ViT-L is EVA [9] pretrained on Objects365 [17] and COCO [15]. V2-99 [13] is initialized from DD3D [16].

relevant annotations and sensor data sampled at 2 Hz. The                            applied for feature extraction unless otherwise specified. No
dataset primarily focuses on scenarios involving changes in                          data or test-time augmentations are used.
intention, where the ego vehicle’s historical data cannot be
extrapolated into a future plan. The dataset provides anno-                          3.3. Main Results
tated 2D high-definition maps with semantic categories and
3D bounding boxes for objects. The dataset is split into two                         Our results, presented in Tab. 1, highlight the absolute ad-
parts: Navtrain and Navtest, which respectively contain 1192                         vantage of Hydra-MDP over the baseline. In our exploration
and 136 scenarios for training/validation and testing.                               of different planning vocabularies [4], utilizing a larger vo-
Metrics. For this challenge, we evaluate our models based                            cabulary V8192 demonstrates improvements across different
on the PDM score, which can be formulated as follows:                                methods. Furthermore, non-differentiable post-processing
                                                                                     yields fewer performance gains than our framework, while
  P DMscore = N C × DAC × DDC × (5×T T C+2×C+5×EP
                                         12
                                                  )
                                                    ,                 (12)           weighted confidence enhances the performance comprehen-
                                                                                     sively. To ablate the effect of different learning targets, the
where sub-metrics N C, DAC, T T C, C, EP correspond to
                                                                                     continuous metric EP (Ego Progress) is not considered in
the No at-fault Collisions, Drivable Area Compliance, Time
                                                                                     early experiments and we attempt the distillation of the over-
to Collision, Comfort, and Ego Progress. For the distillation
                                                                                     all PDM score. Nonetheless, the irregular distribution of the
process and subsequent results, DDC is neglected due to an
                                                                                     PDM score incurs performance degradation, which suggests
implementation problem.1 .
                                                                                     the necessity of our multi-target learning paradigm. In the
3.2. Implementation Details                                                          final version of Hydra-MDP-V8192 -W-EP, the distillation of
                                                                                     EP can improve the corresponding metric.
We train our models on the Navtrain split using 8 NVIDIA
A100 GPUs, with a total batch size of 256 across 20 epochs.
The learning rate and weight decay are set to 1×10−4 and 0.0                         3.4. Scaling Up and Model Ensembling
following the official baseline. LiDAR points from 4 frames
                                                                                     Previous literature [11] suggests larger backbones only lead
are splatted onto the BEV plane to form a density BEV fea-
                                                                                     to minor improvements in planning performance. Neverthe-
ture, which is encoded using ResNet34 [10]. For images, the
                                                                                     less, we further demonstrate the scalability of our model
front-view image is concatenated with the center-cropped
                                                                                     with larger backbones. Tab. 2 shows three best-performing
front-left-view and front-right-view images, yielding an in-
                                                                                     versions of Hydra-MDP with ViT-L [9, 20] and V2-99 [13]
put resolution of 256 × 1024 by default. ResNet34 is also
                                                                                     as the image backbone. For the final submission, we use the
1 https://github.com/autonomousvision/navsim/issues/14                               ensembled sub-scores of these three models for inference.


                                                                               4
References                                                                    Proceedings of the IEEE/CVF conference on computer vision
                                                                              and pattern recognition workshops, pages 0–0, 2019. 4
 [1] Sourav Biswas, Sergio Casas, Quinlan Sykora, Ben Agro,
                                                                         [14] Zhiqi Li, Zhiding Yu, Shiyi Lan, Jiahan Li, Jan Kautz, Tong
     Abbas Sadat, and Raquel Urtasun. Quad: Query-based in-
                                                                              Lu, and Jose M Alvarez. Is ego status all you need for
     terpretable neural motion planning for autonomous driving.
                                                                              open-loop end-to-end autonomous driving? arXiv preprint
     arXiv preprint arXiv:2404.01486, 2024. 2
                                                                              arXiv:2312.03031, 2023. 1, 2, 3
 [2] Holger Caesar, Juraj Kabzan, Kok Seang Tan, Whye Kit
                                                                         [15] Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays,
     Fong, Eric Wolff, Alex Lang, Luke Fletcher, Oscar Beijbom,
                                                                              Pietro Perona, Deva Ramanan, Piotr Dollár, and C Lawrence
     and Sammy Omari. nuplan: A closed-loop ml-based plan-
                                                                              Zitnick. Microsoft coco: Common objects in context. In
     ning benchmark for autonomous vehicles. arXiv preprint
                                                                              Computer Vision–ECCV 2014: 13th European Conference,
     arXiv:2106.11810, 2021. 3
                                                                              Zurich, Switzerland, September 6-12, 2014, Proceedings, Part
 [3] Holger Caesar, Juraj Kabzan, Kok Seang Tan, Whye Kit
                                                                              V 13, pages 740–755. Springer, 2014. 4
     Fong, Eric Wolff, Alex Lang, Luke Fletcher, Oscar Beijbom,
                                                                         [16] Dennis Park, Rares Ambrus, Vitor Guizilini, Jie Li, and
     and Sammy Omari. nuplan: A closed-loop ml-based plan-
                                                                              Adrien Gaidon. Is pseudo-lidar needed for monocular 3d
     ning benchmark for autonomous vehicles. arXiv preprint
                                                                              object detection? In Proceedings of the IEEE/CVF Interna-
     arXiv:2106.11810, 2021. 3
                                                                              tional Conference on Computer Vision, pages 3142–3152,
 [4] Shaoyu Chen, Bo Jiang, Hao Gao, Bencheng Liao, Qing
                                                                              2021. 4
     Xu, Qian Zhang, Chang Huang, Wenyu Liu, and Xinggang
                                                                         [17] Shuai Shao, Zeming Li, Tianyuan Zhang, Chao Peng, Gang
     Wang. Vadv2: End-to-end vectorized autonomous driving
                                                                              Yu, Xiangyu Zhang, Jing Li, and Jian Sun. Objects365: A
     via probabilistic planning. arXiv preprint arXiv:2402.13243,
                                                                              large-scale, high-quality dataset for object detection. In Pro-
     2024. 1, 2, 3, 4
                                                                              ceedings of the IEEE/CVF international conference on com-
 [5] Kashyap Chitta, Aditya Prakash, Bernhard Jaeger, Zehao
                                                                              puter vision, pages 8430–8439, 2019. 4
     Yu, Katrin Renz, and Andreas Geiger. Transfuser: Imita-
                                                                         [18] Martin Treiber, Ansgar Hennecke, and Dirk Helbing. Con-
     tion with transformer-based sensor fusion for autonomous
                                                                              gested traffic states in empirical observations and microscopic
     driving. IEEE Transactions on Pattern Analysis and Machine
                                                                              simulations. Physical review E, 62(2):1805, 2000. 1
     Intelligence, 2022. 3, 4
 [6] NAVSIM Contributors. Navsim: Data-driven non-reactive               [19] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszko-
     autonomous vehicle simulation. https://github.com/                       reit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia
     autonomousvision/navsim, 2024. 3                                         Polosukhin. Attention is all you need. Advances in neural
                                                                              information processing systems, 30, 2017. 3
 [7] OpenScene Contributors. Openscene: The largest up-to-
     date 3d occupancy prediction benchmark in autonomous                [20] Lihe Yang, Bingyi Kang, Zilong Huang, Xiaogang Xu, Ji-
     driving. https://github.com/OpenDriveLab/                                ashi Feng, and Hengshuang Zhao. Depth anything: Unleash-
     OpenScene, 2023. 3                                                       ing the power of large-scale unlabeled data. arXiv preprint
                                                                              arXiv:2401.10891, 2024. 4
 [8] Daniel Dauner, Marcel Hallgarten, Andreas Geiger, and
     Kashyap Chitta. Parting with misconceptions about learning-
     based vehicle motion planning. In Conference on Robot
     Learning, pages 1268–1281. PMLR, 2023. 1, 3, 4
 [9] Yuxin Fang, Quan Sun, Xinggang Wang, Tiejun Huang, Xin-
     long Wang, and Yue Cao. Eva-02: A visual representation for
     neon genesis. arXiv preprint arXiv:2303.11331, 2023. 4
[10] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun.
     Deep residual learning for image recognition. In Proceed-
     ings of the IEEE conference on computer vision and pattern
     recognition, pages 770–778, 2016. 4
[11] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima,
     Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai
     Wang, et al. Planning-oriented autonomous driving. In Pro-
     ceedings of the IEEE/CVF Conference on Computer Vision
     and Pattern Recognition, pages 17853–17862, 2023. 1, 2, 4
[12] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen,
     Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and
     Xinggang Wang. Vad: Vectorized scene representation for ef-
     ficient autonomous driving. In Proceedings of the IEEE/CVF
     International Conference on Computer Vision, pages 8340–
     8350, 2023. 1, 2
[13] Youngwan Lee, Joong-won Hwang, Sangrok Lee, Yuseok
     Bae, and Jongyoul Park. An energy and gpu-computation
     efficient backbone network for real-time object detection. In


                                                                     5
