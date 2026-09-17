# P0029_GenAD - PDF text extraction

> Source PDF: `papers/pdf/P0029_GenAD.pdf`
> Conversion: Poppler `pdftotext -layout -enc UTF-8`
> Note: layout-preserving text extraction; the PDF remains the source of truth for figures, exact equations, and wording.

---

                                                               GenAD: Generative End-to-End Autonomous Driving

                                               Wenzhao Zheng1, * Ruiqi Song2,3, * Xianda Guo2, *,† Chenming Zhang2                                     Long Chen2,3,†
                                                                   1
                                                                     University of California, Berkeley 2 Waytous
                                                              3
                                                                Institute of Automation, Chinese Academy of Sciences
                                         {wenzhao.zheng, chmzhang}@outlook.com; xianda guo@163.com; {ruiqi.song, long.chen}@ia.ac.cn
arXiv:2402.11502v3 [cs.CV] 7 Apr 2024




                                                                   Abstract                                 Conventional End-to-End Autonomous Driving



                                            Directly producing planning results from raw sensors
                                                                                                                         Perception                Prediction                       Planning
                                        has been a long-desired solution for autonomous driving
                                        and has attracted increasing attention recently. Most ex-
                                        isting end-to-end autonomous driving methods factorize
                                        this problem into perception, motion prediction, and plan-
                                                                                                            Generative End-to-End Autonomous Driving
                                        ning. However, we argue that the conventional progressive                                                               Latent Trajectory
                                                                                                                                                                     Space
                                        pipeline still cannot comprehensively model the entire traf-
                                                                                                                          Scene
                                        fic evolution process, e.g., the future interaction between                     Represneta
                                                                                                                                                     Future                         Prediction
                                                                                                                                                                                    & Planning
                                                                                                                                                   Generation
                                                                                                                           tion                                                      Results
                                        the ego car and other traffic participants and the struc-
                                        tural trajectory prior. In this paper, we explore a new
                                        paradigm for end-to-end autonomous driving, where the              Figure 1. Comparisons of the proposed generative end-to-
                                        key is to predict how the ego car and the surroundings             end autonomous driving framework with the conventional
                                                                                                           pipeline. Most existing methods follow a serial design of percep-
                                        evolve given past scenes. We propose GenAD, a genera-
                                                                                                           tion, prediction, and planning. They usually ignore the high-level
                                        tive framework that casts autonomous driving into a gen-           interactions between the ego car and other agents and the struc-
                                        erative modeling problem. We propose an instance-centric           tural prior of realistic trajectories. We model autonomous driving
                                        scene tokenizer that first transforms the surrounding scenes       as a future generation problem and conduct motion prediction and
                                        into map-aware instance tokens. We then employ a varia-            ego planning simultaneously in a structural latent trajectory space.
                                        tional autoencoder to learn the future trajectory distribu-
                                                                                                           of vision-centric autonomous driving in various tasks in-
                                        tion in a structural latent space for trajectory prior mod-
                                                                                                           cluding 3D object detection [17, 26, 27], map segmenta-
                                        eling. We further adopt a temporal model to capture the
                                                                                                           tion [25, 30, 34, 53], and 3D semantic occupancy predic-
                                        agent and ego movements in the latent space to generate
                                                                                                           tion [18, 19, 46, 47, 50, 51, 57], recent advances in vision-
                                        more effective future trajectories. GenAD finally simultane-
                                                                                                           centric end-to-end autonomous driving [15, 16, 21] have
                                        ously performs motion prediction and planning by sampling
                                                                                                           shed light on a potential and elegant path to directly pro-
                                        distributions in the learned structural latent space condi-
                                                                                                           duce planning results from raw sensors.
                                        tioned on the instance tokens and using the learned tempo-
                                                                                                              Most existing end-to-end autonomous driving models
                                        ral model to generate futures. Extensive experiments on the
                                                                                                           are composed of several modules and follow a pipeline of
                                        widely used nuScenes benchmark show that the proposed
                                                                                                           perception, motion prediction, and planning [5, 15, 16, 21].
                                        GenAD achieves state-of-the-art performance on vision-
                                                                                                           For example, UniAD [16] further progressively performs
                                        centric end-to-end autonomous driving with high efficiency.
                                                                                                           map perception, detection, tracking, motion prediction, oc-
                                        Code: https://github.com/wzzheng/GenAD.
                                                                                                           cupancy prediction, and planning modules to improve the
                                                                                                           robustness of the system. It is also observed that using a
                                                                                                           planning objective improves the performance of intermedi-
                                        1. Introduction                                                    ate tasks [16]. However, the serial design of prediction and
                                        Vision-centric autonomous driving has been extensively ex-         planning of existing pipelines ignores the possible future
                                        plored in recent years due to its economic convenience [17,        interactions between the ego car and the other traffic partic-
                                        26, 27, 41, 44]. While researchers have advanced the limit         ipants. We argue that this type of interaction is important
                                                                                                           for accurate planning. For example, the lane shift of the
                                           ∗ Equal contributions; † Corresponding authors.                 ego car would affect the action of the rear cars, and further


                                                                                                       1
affects the planning of the ego car. This high-order inter-          depths for image features and then projects them into the 3D
action cannot be effectively modeled by the current design           space using camera parameters [17, 26, 29, 35, 41, 44, 53].
of motion prediction before planning. Also, future trajec-           Other methods initialize queries in the 3D space and ex-
tories are highly structured and share a common prior (e.g.,         ploit deformable cross-attention to adaptively aggregate in-
most trajectories are continuous and straight lines). Still,         formation from 2D images [19, 22, 27]. Some works fur-
most existing methods fail to consider this structural prior,        ther design better positional embedding strategies [33], 3D
leading to inaccurate predictions and planning.                      representations [19], or task heads [53] to further improve
   In this paper, we propose a Generative End-to-End                 the perception performance or efficiency. In this paper, we
Autonomous Driving (GenAD) framework (shown in Fig-                  adopt conventional simple designs for 3D perception and
ure 1), which models autonomous driving as a trajectory              focus on motion prediction and planning.
generation problem to unleash the full potential of end-                 Prediction. Accurate motion prediction for traffic par-
to-end methods. We propose a scene tokenizer to obtain               ticipants is the key to the following motion planning of the
instance-centric scene representations, which focus on in-           ego vehicle. Conventional methods utilized ground-truth
stances but also integrate map information. To achieve this,         agent history and HD map information as inputs and fo-
we use a backbone network to extract image features for              cused on the prediction of future agent trajectories [3, 40,
each surrounding camera and then transform them into the             49]. One straightforward way is to draw agent paths and
3D bird’s eye view (BEV) space [17, 26, 27]. We further              HD maps on a BEV image and use convolutional neural
use cross-attention to refine high-level map and agent to-           networks to process them and output motion prediction re-
kens from BEV features. We then add an ego token and                 sults [3, 40]. Further methods employed vectors or tokens to
use ego-agent self-attention to capture their high-order in-         represent separate agents or map elements [28, 32, 39, 49].
teractions. We further inject map information with cross-            They then leverage the reasoning ability of graph neural net-
attention to obtain map-aware instance tokens. To model              works [28] and transformers to infer future motions con-
the structural prior of future trajectories, we learn a varia-       sidering the interaction between agents and map elements.
tional autoencoder to map ground-truth trajectories to Gaus-         The increase of hardware capacity promotes the emergence
sian distributions considering the uncertain nature of motion        of end-to-end motion prediction methods [10, 13, 20, 53],
prediction and driving planning. We then use a simple yet            which jointly perform perception and prediction to get free
effective gated recurrent unit (GRU) [7] to perform auto-            of offline HD maps. Despite being very challenging, recent
regressing to model instance movement in the latent struc-           end-to-end methods have demonstrated promising perfor-
tural space. During inference, we sample from the learned            mance in this more practical setting [10, 13, 20, 53]. They
distributions conditioned on the instance-centric scene rep-         usually adopt the attention mechanism to incorporate agent
resentation and can thus predict different possible futures.         and map information and leverage temporal networks (e.g.,
Our GenAD can simultaneously perform motion predic-                  gated recurrent units [13]) to predict future states. However,
tion and planning using the unified future trajectory gen-           most existing methods directly decode trajectories from la-
eration model. We conduct extensive experiments on the               tent feature and ignores the structural nature of realistic tra-
widely used nuScenes benchmark to evaluate the perfor-               jectories (e.g., most of them are straight lines). Differently,
mance of the proposed GenAD framework. Based on gener-               we learn a variational autoencoder from ground-truth tra-
ative modeling, our GenAD achieves state-of-the-art vision-          jectories to model the trajectory prior in a latent structural
based planning performance with high-efficiency.                     space and sample instances in this space for inference.

2. Related Work                                                         Planning. Planning is the ultimate goal for the first
                                                                     stage of autonomous driving. Despite the mature devel-
Perception. Perception is the basic step in autonomous               opment of rule-based planners [1, 8, 48], learning-based
driving, which aims to extract meaningful information from           planners [6, 42, 45] are receiving increasing attention due
raw sensor inputs. Despite the strong performance of                 to their great potential to benefit from large-scale driving
LiDAR-based methods [4, 9, 38, 55], vision-centric meth-             data and compatibility with end-to-end autonomous driv-
ods [19, 26, 27, 51, 53] have emerged as a competitive alter-        ing methods. Most existing end-to-end planning meth-
native due to the low costs of RGB cameras. Equipped with            ods follow a pipeline of perception, prediction, and plan-
large 2D image backbones, vision-centric methods demon-              ning [5, 15, 16, 21]. For example, ST-P3 [15] progressively
strated great potential in the main perception tasks includ-         employs a map perception, a BEV occupancy prediction,
ing 3D object detection [17, 26, 27, 41, 44, 53], HD map             and a trajectory planning module to obtain future ego move-
reconstruction [25, 30, 34, 53], and 3D semantic occupancy           ments from surrounding cameras. UniAD [16] further ex-
prediction [46, 47, 50, 51, 54, 57]. To accurately complete          tends ST-P3 with additional detection, tracking, and mo-
these 3D tasks, the key procedure is to transform image fea-         tion prediction modules to improve the robustness of the
tures to the 3D space. One line of works predicts explicit           system. VAD [21] simplifies UniAD with vectorized scene

                                                                 2
                              Scene Representation                                                                   Future Generation
                                   Deformable                                                                              Future
                                                      Detection
                                     Cross-            Head
                                                                                                                         Trajectory
                                    Attention                                                                             Encoder                  Future
                                                                                                     Ground-truth
                                                                                                                                                 Trajectory
                                                                                                     Trajectories                                Generator
                                                   Agent Tokens

                      BEV                                 Self-                Cross-                 Instance                      Latent
                    Encoder                             Attention             Attention               Encoder                     Trajectory
                                                                                                                                    Space
                                                   Ego Token
                              BEV Tokens                                                             Reconstructed
                                                                                          Instance    Trajectories
                                                      Map Tokens
                                                                                          -centric
                                                                                                                          Future
                                     Cross-                 Map                            Scene
                                                                                                                        Trajectory
                                    Attention               Head                           Repre.                                              Motion Prediction
Image Backbone                                                                                                          Generator                & Planning


Figure 2. Framework of our generative end-to-end autonomous driving. Given surrounding images as inputs, we employ an image
backbone to extract multi-scale features and then use a BEV encoder to obtain BEV tokens. We then use cross-attention and deformable
cross-attention to transform BEV tokens into map and agent tokens, respectively. With an additional ego token, we use self-attention to
enable ego-agent interactions and cross-attention to further incorporate map information to obtain the instance-centric scene representation.
We map this representation to a structural latent trajectory space which is jointly learned using ground-truth future trajectories. Finally, we
employ a future trajectory generator to produce future trajectories to simultaneously complete motion prediction and planning.

representation and only map, motion, and planning modules                      where T(T, f ) denotes a f -frame trajectory starting from
for end-to-end driving, which achieves state-of-the-art plan-                  the T -th frame, wt denotes the waypoint at the t-th frame,
ning performance with better efficiency. However, the serial                   and st denotes the sensor input at t-th frame.
design of prediction and planning ignores the effect of fu-                       The first step of end-to-end autonomous driving is to per-
ture ego movements on the agent motion prediction. It also                     ceive the sensor inputs to obtain high-level descriptions of
lacks modeling of the uncertain nature of motion prediction                    the surrounding scene. These descriptions usually include
and planning. To address this, GenAD models autonomous                         semantic map [30, 34] and instance bounding box [26, 27].
driving in a generative framework and simultaneously gen-                      To achieve this, we follow a conventional vision-centric
erates the future trajectories for the ego vehicle and other                   perception pipeline to extract bird’s eye view (BEV) B ∈
agents in a learned probabilistic latent space.                                RH×W ×C features first and then build on them to refine
                                                                               map and bounding box features.
3. Proposed Approach                                                              Image to BEV. We basically follow BEVFormer [27] to
                                                                               obtain the BEV features. Specifically, we use a convolu-
This section presents our generative framework of vision-                      tional neural network [11] and feature pyramid network [31]
based end-to-end autonomous driving, as shown in Fig-                          to obtain multi-scale image features F from camera inputs
ure 2. We first introduce an instance-centric scene represen-                  s. We then initialize H × W BEV tokens B0 as queries and
tation which incorporates high-order map-ego-agent inter-                      use deformable cross-attention [56] to transfer information
actions to enable comprehensive yet compact scene descrip-                     from the multi-scale image feature F:
tions (Sec. 3.1). We then elaborate on the learning of a la-
tent embedding space to model realistic trajectories as prior                                           B = DA(B0 , F, F),                                   (2)
(Sec. 3.2) and the generation of future motion in this learned
latent space (Sec. 3.3). At last, we detail the training and in-               where DA(Q, K, V) denotes the deformable attention
ference of the Generative end-to-end Autonomous Driving                        block consisting of interleaved self-attention and de-
(GenAD) framework(Sec. 3.4).                                                   formable cross-attention layers using Q, K, and V as
                                                                               queries, keys, and values, respectively. We then align the
3.1. Instance-Centric Scene Representation                                     BEV features from the p past frames into the current coordi-
The goal of end-to-end autonomous driving can be for-                          nate system and concatenate them as the final BEV features
mulated as obtaining a planned f -frame future trajectory                      B.
T(T, f ) = {wT +1 , wT +2 , · · · , wT +f } for the ego vehi-                     BEV to map. As semantic map elements are usu-
cle given the current and past p-frame sensor inputs S =                       ally sparse in the BEV space, we follow a similar con-
{sT , sT −1 , · · · , sT −p } and trajectory T(T − p, p + 1) =                 cept [20, 21] and use map tokens M ∈ RNm ∗C to represent
{wT , wT −1 , · · · , wT −p }.                                                 semantic maps. Each map token m ∈ M can be decoded to
                                                                               a set of points in the BEV space by a map decoder dm rep-
               T(T − p, p + 1), S → T(T, f ),                       (1)        resenting a category of map elements and their correspond-


                                                                          3
ing positions. Following VAD [21], we consider three cat-                Reconstructed
                                                                                                  Future Trajectory Generator
egories of map elements (i.e., lane divider, road boundary,                Trajectoy
and pedestrian crossing). We use the global cross-attention
                                                                                             Decoder                       GRU
mechanism to update learnable initialized queries M0 from
BEV tokens B:                                                                                 Decoder                      GRU

                   M = CA(M0 , B, B),                     (3)                                 Decoder                      GRU

where CA(Q, K, V) denotes the cross-attention block                                           Decoder                      GRU
composed of interleaved self-attention and cross-attention                                    Decoder                      GRU
layers using Q, K, and V as queries, keys, and values, re-
spectively.
   BEV to agent. Similar to the representation of semantic
maps, we adopt a set of agent tokens A to represent the 3D                                       Future
position of each instance in the surroundings. We use de-                                      Trajectory
formable cross-attention to obtain the updated agent tokens                                     Encoder
A from the BEV tokens B:
                   A = DA(A0 , B, B),                     (4)
                                                                      Ground-truth                             Latent Trajectory
where A0 are learnable tokens as initialization.                       Trajectory                                   Space
   Having obtained the agent tokens A, we employ a 3D
                                                                     Figure 3. Illustration of the proposed trajectory prior model-
object detection head da to decode the position, orientation,
                                                                     ing and future generation. We use a future trajectory encoder to
and category information from each agent token a.
                                                                     map ground-truth trajectories to a latent trajectory space, where we
   Instance-centric scene representation. As prediction              use the Gaussian distribution to model the trajectory uncertainty.
and planning mainly focus on the instances of agents and             We then employ a gate recurrent unit (GRU) to progressively pre-
ego vehicles, respectively, we propose an instance-centric           dict the next future in the latent space and use a decoder to obtain
scene representation to comprehensively and efficiently rep-         explicit trajectories.
resent the autonomous driving scenario. We first add an ego
token e to the learned agent tokens A to construct a set of          map and instance information to perform motion prediction
instance tokens I = concat(e, A).                                    and trajectory planning.
   Existing methods [15, 16, 21] usually perform motion
prediction and planning in a serial manner, which ignores
                                                                     3.2. Trajectory Prior Modeling
the effect of future ego movements on the agents. For ex-            We find that the objectives of motion prediction of other
ample, the lane shift of the ego car would possibly affect the       agents and planning of the ego vehicle share the same out-
action of rear cars, rendering the motion prediction results         put space and are essentially the same. They both aim to
inaccurate. Differently, we enable high-order interactions           produce a high-quality realistic trajectory of the concerned
between the ego vehicle and other agents by performing               instance, given semantic maps and interactions with other
self-attention on the instance tokens:                               agents. The goal for the proposed GenAD can be then for-
                                                                     mulated as inferring the future trajectory T given the map-
                      I ← SA(I, I, I),                    (5)
                                                                     aware instance-centric scene representations I.
where SA(Q, K, V) denotes the self-attention block com-                 Different from existing methods which directly output
posed of self-attention layers using Q, K, and V as queries,         the trajectory using a simple decoder, we model it as a tra-
keys, and values, respectively.                                      jectory generation problem T ∼ p(T|I) considering its un-
   Furthermore, to perform accurate prediction and plan-             certain nature.
ning, both the agents and the ego vehicle need to be                    The trajectories of both the ego vehicle and other agents
aware of the semantic map information. We thus employ                are highly structured (e.g., continuous) and follow certain
cross-attention between the updated instance tokens and the          patterns. For example, most of the trajectories are straight
learned map tokens to obtain map-aware instance-centric              lines as the vehicle driving at a constant speed, and some of
scene representations:                                               them are curved lines with a near-constant curvature when
                    I ← CA(I, M, M).                                 the vehicle turning right or left. Only in very rare cases will
                                                          (6)
                                                                     the trajectories be zig-zagging. Considering this, we adopt
    The learned instance tokens I incorporate high-order             a variational autoencoder (VAE) [24] architecture to learn
agent-ego interactions and are aware of the learned seman-           a latent space Z to model this trajectory prior. Specifically,
tic maps, which are compact yet contain all the necessary            we employ a ground-truth trajectory encoder ef to model


                                                                 4
p(z|T(T, f )), which maps the future trajectory T(T, f ) to                 autonomous driving. Given surrounding camera signals s as
a diagonal Gaussian distribution on the latent space Z. The                 inputs, we first employ an image backbone to extract multi-
encoder ef outputs two vectors µf and σf representing the                   scale image features F and then use deformable attention to
mean and variance of the Gaussian distribution:                             transform them into the BEV space. We align the BEV fea-
                                                                            tures from the past p frames to the current ego-coordinate to
                p(z|T(T, f )) ∼ N (µf , σf ),                     (7)
                                                                            obtain the final BEV feature B. We perform global cross-
               2                                                            attention and deformable attention to refine a set of map
where N (µ, σ ) denotes a Gaussian distribution with a
mean of µ and standard deviation of σ.                                      tokens M and agent tokens A, respectively. To model the
   The learned distribution p(z|T(T, f )) contains the prior                high-order interactions between traffic agents and the ego
of the ground-truth trajectories, which can be leveraged to                 vehicle, we combine agent tokens with an ego token and
improve the authenticity of motion prediction and planning                  perform self-attention among them to construct a set of in-
for traffic agents and ego vehicles.                                        stance tokens I. We also use cross-attention to inject seman-
                                                                            tic map information into the instance tokens I to facilitate
3.3. Latent Future Trajectory Generation                                    further prediction and planning.
Having obtained the latent distribution of the future trajec-                   As realistic trajectories are highly structured, we learn a
tories as prior, we need to explicitly decode them from the                 VAE module to model the trajectory prior and adopt a gen-
latent trajectory space Z.                                                  erative framework for both motion prediction and planning.
    While a straightforward way is to directly use an MLP-                  We learn an encoder et to map ground-truth trajectories to
based decoder to output trajectory points in the BEV space                  the structural space Z as Gaussian distributions. We then
to model p(T(T, f )|z), it fails to model the temporal evo-                 employ a GRU-based future trajectory generator g to model
lution of the traffic agents and ego vehicle. To consider the               the temporal evolutions of instances in the latent space Z
temporal relations of instances at different time stamps, we                and use a simple MLP-based decoder dw to decode way-
factorized the joint distribution p(T(T, f )|z) as follows:                 points from latent representations. We can finally recon-
                                                                            struct the trajectories T̂a and T̂e for traffic agents and the
 p(T(T, f )|zT ) = p(wT +1 |zT ) · p(wT +2 |wT +1 , zT )                    ego vehicle by integrating the decoded waypoint of each
                                                                  (8)
                · · · p(wT +f |wT +1 , · · · , wT +f −1 , zT ).             time stamp. For training, we additionally use a class de-
                                                                            coder dc to predict the category for each agent ĉa . To learn
    We sample a vector from the distribution N (µf , σf ) as
                                                                            the future trajectory encoder ef , the future trajectory gen-
the latent state at the current time stamp zT . Instead of
                                                                            erator g, the waypoint decoder dw , and the class decoder
decoding the whole trajectory at once, we adopt a simple
                                                                            dc , we follow VAD [21] to impose trajectory losses on the
MLP-based decoder dw to decode a waypoint w = dw (z)
                                                                            reconstructed and ground-truth trajectories for both traffic
from the latent space Z, i.e., we instantiate p(wT +1 |z) with
                                                                            agents and the ego vehicle:
w = dw (z).
    We then adopt a gated recurrent unit (GRU) [7] as the                                                        1
                                                                                   Jprior = Ltra (T̂e , Te ) +      Ltra (T̂a , Ta )
future trajectory generator to model the temporal evolu-                                                         Na                    (9)
tions of instances. Specifically, the GRU model g takes as                                                  +λc Lf ocal (Ĉa , Ca ),
inputs the current latent representation zt and transforms
it into the next state g(zt ) = zt+1 . We can then de-                      where || · ||1 denotes the L1 norm, Na is the number
code the waypoint wt+1 at the (t + 1)-th time stamp us-                     of agents, and Lf ocal represents the focal loss to con-
ing the waypoint decoder wt+1 = dw (zt+1 ), i.e., we model                  strain the predicted agent class. Ltra denotes the trajectory
p(wt+1 |wT +1 , · · · , wt , z) with dw (g(zt )).                           losses [21] including the L1 discrepancy, ego-agent colli-
    Compared with a single decoder that directly outputs the                sion constraint, ego-boundary overstepping constraint, and
whole trajectory, the waypoint decoder performs a simpler                   the ego-Lane directional constraint. Ĉa and Ca represent
task of only decoding a position in the BEV space and the                   the predicted and ground-truth classes for all the agents, re-
GRU module models the movement of agents in the latent                      spectively.
space Z. The produced trajectory is thus more realistic and                     To infer the future trajectory for traffic agents and the
authentic considering the prior knowledge in this learned                   ego vehicle from the instance tokens I, we use an instance
structured latent space. We illustrate the proposed trajec-                 encoder ei to map each instance token to the latent space
tory prior modeling and latent future trajectory generation                 Z. The encoder ei similarly outputs a mean vector µi and
in Figure 3.                                                                variance vector σi to parameterize a diagonal Gaussian dis-
                                                                            tribution:
3.4. Generative End-to-End Autonomous Driving                                                   p(z|I) ∼ N (µi , σi ).               (10)
In this subsection, we present the overall architecture of the              With the learned latent trajectory space to model realistic
proposed GenAD framework for vision-centric end-to-end                      trajectory prior, the motion prediction and planning can be


                                                                        5
Table 1. Comparisons with state-of-the-art methods in motion planning performance on the nuScenes [2] val dataset. † represents
that the metrics are computed with an average of all the predicted frames. † denotes FPS measured with the same environment on our
machine with a single RTX 3090 GPU.
                                                                                L2 (m) ↓              Collision Rate (%) ↓
 Method               Input                 Aux. Sup.                                                                      FPS
                                                                         1s     2s   3s       Avg.   1s     2s    3s Avg.
 IL [43]             LiDAR                   None                       0.44   1.15    2.47   1.35   0.08   0.27   1.95   0.77    -
 NMP [52]            LiDAR               Box & Motion                   0.53   1.25    2.67   1.48   0.04   0.12   0.87   0.34    -
 FF [14]             LiDAR                 Freespace                    0.55   1.20    2.54   1.43   0.06   0.17   1.07   0.43    -
 EO [23]             LiDAR                 Freespace                    0.67   1.36    2.78   1.60   0.04   0.09   0.88   0.33    -
 ST-P3 [15]         Camera            Map & Box & Depth                 1.33   2.11    2.90   2.11   0.23   0.62   1.27   0.71   1.6
 UniAD [16]         Camera      Map & Box & Motion & Tracklets & Occ    0.48   0.96    1.65   1.03   0.05   0.17   0.71   0.31   1.8
 OccNet [47]        Camera           3D-Occ & Map & Box                 1.29   2.13    2.99   2.14   0.21   0.59   1.37   0.72   2.6
 VAD-Tiny [21]      Camera           Map & Box & Motion                 0.60   1.23    2.06   1.30   0.31   0.53   1.33   0.72   6.9‡
 VAD-Base [21]      Camera           Map & Box & Motion                 0.54   1.15    1.98   1.22   0.04   0.39   1.17   0.53   3.6‡
 GenAD              Camera           Map & Box & Motion                 0.36 0.83 1.55 0.91          0.06 0.23 1.00 0.43         6.7‡
 VAD-Tiny† [21] Camera               Map & Box & Motion                 0.46 0.76 1.12 0.78          0.21 0.35 0.58 0.38         6.9‡
 VAD-Base† [21] Camera               Map & Box & Motion                 0.41 0.70 1.05 0.72          0.07 0.17 0.41 0.22         3.6‡
 GenAD†             Camera           Map & Box & Motion                 0.28 0.49 0.78 0.52          0.08 0.14 0.34 0.19         6.7

unified and formulated as a distribution matching problem              4. Experiments
between the instance distribution p(z|I) and the ground-
truth distribution p(z|T(T, f )). We impose the Kullback-              4.1. Datasets
Leibler divergence loss to enforce distribution matching:              We conducted extensive experiments on the widely adopted
                                                                       nuScenes [2] dataset to evaluate the proposed GenAD
           Jplan = DKL (p(z|I), p(z|T(T, f ))),           (11)         framework for autonomous driving. The nuScenes dataset
                                                                       is composed of 1000 driving scenes, where each scene pro-
where DKL denotes the Kullback-Leibler divergence.                     vides RGB and LiDAR video of 20 seconds. The ego vehi-
   Additionally, we use two auxiliary tasks to train the pro-          cle is equipped with 6 surrounding cameras with 360◦ hor-
posed GenAD model: map segmentation and 3D object de-                  izontal FOV and a 32-beam LiDAR sensor. nuScenes pro-
tection. We use a map decoder dm on the map tokens M                   vides semantic map and 3D object detection annotations for
and an object decoder do on the agent tokens A to obtain               keyframes at 2Hz. It includes 1.4M 3D bounding boxes of
the predicted maps and 3D object detection results. We fol-            objects from 23 categories. We partitioned the dataset into
low the task decoder design of VAD [21] and employ bi-                 700, 150, and 150 scenes for training, validation, and test-
partite matching for ground truth matching. We then im-                ing, respectively, following the official instructions [2].
pose semantic map loss [53] Jmap and 3D object detection
loss [27] Jdet on them to train the network.                           4.2. Evaluation Metrics
   The overall training objective of our GenAD framework
                                                                       Following existing end-to-end autonomous driving meth-
can be formulated as:
                                                                       ods [15, 16], we use the L2 displacement error and colli-
 JGenAD = Jprior + λplan Jplan + λmap Jmap + λdet Jdet ,               sion rate to measure the quality of planning results. The L2
                                                          (12)         displacement error measures the L2 distance between the
where λplan , λmap , and λdet are balance factors. The pro-            planned trajectory and the ground-truth trajectory. The col-
posed GenAD can be trained efficiently in an end-to-end                lision rate measures how often the self-driving vehicle col-
manner. For inference, we discard the future trajectory en-            lapses with other traffic participants following the planned
coder ef and sample a latent state following the instance              trajectory. By default, we take as inputs 2s history (i.e., 5
distribution p(z|I) as input for the trajectory generator g            frames) and evaluate the planning performance at the 1s, 2s,
and waypoint decoder dw . Our GenAD models end-to-end                  and 3s future.
autonomous driving as a generative problem and performs
                                                                       4.3. Implementation Details
future prediction and planning in a structured latent space,
which considers the prior of realistic trajectories to produce         We adopted ResNet50 [12] as the backbone network to ex-
high-quality trajectory prediction and planning.                       tract image features. We take as input images with a resolu-


                                                                 6
Table 2. Comparisons of perception, prediction, and planning performance. † denotes FPS measured with the same environment on
our machine with a single RTX 3090 GPU card.
              Detection      Map Segmentation         Motion Prediction          Planning
Method                                                                                          FPS
               mAP ↑ mAP@0.5 ↑ mAP@1.0 ↑ mAP@1.5 ↑ EPA (car) ↑ EPA (ped.)↑ Avg. L2 ↓ Avg. CR. ↓
VAD [21]        0.27           0.15            0.44           0.61             0.56          0.29         1.30         0.72       6.9†
GenAD           0.29           0.24            0.56           0.71             0.59          0.34         0.91         0.43       6.7†

Table 3. Effect of the instance-centric scene representation. E          Table 4. Effect of the generative framework for autonomous
→ A represents the proposed ego-to-agent interaction to obtain the       driving. TPM and LFTG denote the trajectory prior modeling and
instance-centric scene representation.                                   latent future trajectory generation, respectively.
                     L2 (m) ↓   Collision Rate (%) ↓                                          L2 (m) ↓   Collision Rate (%) ↓
Setting                                                                  TPM LFTG
                1s   2s 3s Avg. 1s 2s 3s Avg.                                           1s    2s 3s Avg. 1s 2s 3s Avg.
VAD [21] 0.60 1.23 2.06 1.30 0.31 0.53 1.33 0.72                           ×      ×    0.42 1.02 1.89 1.11 0.06 0.43 1.60 0.70
w/ E → A 0.39 0.99 1.91 1.10 0.14 0.39 1.35 0.63                           ✓      ×    0.38 0.92 1.76 1.02 0.23 0.37 1.19 0.60
GenAD     0.36 0.83 1.55 0.91 0.06 0.23 1.00 0.43                          ×      ✓    0.39 0.92 1.74 1.02 0.18 0.45 1.05 0.56
w/o E → A 0.40 0.93 1.74 1.02 0.70 0.98 1.97 1.22                          ✓      ✓    0.36 0.83 1.55 0.91 0.06 0.23 1.00 0.43

tion of 640 × 360 and use a 200 × 200 BEV representation                 the proposed GenAD model and compared it with VAD-
to perceive the surrounding scene. For fair comparisons, we              tiny [21] with a similar model size, as shown in Table 2. We
basically use the same hyperparameters as VAD-tiny[21].                  use mean average precision (mAP) to measure the 3D ob-
We fixed the number of BEV tokens, map tokens, and agent                 ject detection performance, and mAP@0.5, mAP@1.0, and
tokens to 100 × 100, 100, and 300, respectively. Each map                mAP@1.5 to evaluate the quality of predicted maps. For
token contains 20 point tokens to represent a map point in               motion prediction, we report the end-to-end prediction ac-
the BEV space. We set the hidden dimension of each BEV,                  curacy (EPA) for both cars and pedestrians, which is a more
point, agent, ego, and instance token to 256. We used a la-              fair metric for end-to-end methods to avoid the influence of
tent space with a dimension of 512 to model trajectory prior             falsely detected agents. For motion planning, we report the
and also set the hidden dimension of the GRU to 512. We                  average L2 error and collision rate (CR) over 1s, 2s, and 3s.
employed 3 layers for each attention block.                                  We observe that GenAD outperforms VAD on all the
   For training, we set the loss balance factors to 1 and                tasks with a similar inference speed. Specifically, GenAD
use the AdamW [37] optimizer with a cosine learning rate                 achieves better motion prediction performances by consid-
scheduler [36]. We set the initial learning rate to 2 × 10−4             ering the influence of the ego vehicle on the other agents.
and a weight decay of 0.01. By default, we trained our                   GenAD also demonstrates superior performance in 3D de-
GenAD for 60 epochs with 8 NVIDIA RTX 3090 GPUs                          tection and map segmentation, showing a better consistency
and adopted a total batch size of 8.                                     between perception, prediction, and planning.
                                                                             Effect of the instance-centric scene representation.
4.4. Results and Analysis
                                                                         We conducted an ablation study to analyze the effectiveness
Main results. We compared GenAD with state-of-the-art                    of the instance-centric scene representation, as shown in Ta-
end-to-end autonomous driving methods in Table 1. We                     ble 3. We first added the ego-to-agent interaction with the
use bold and underlined numbers to represent the best and                proposed method to VAD-tiny [21], and observe a large im-
second-best results, respectively. We see that our GenAD                 provement in both the L2 error and the collision rate. We
achieves the best L2 errors among all the methods with an                also removed the ego-to-agent interaction in our GenAD
efficient inference speed. Though UniAD [16] outperforms                 model by masking the self-attention matrix to dissect its
our method with respect to the collision rates, it employs               effect. We see that the collision rate performance drops
additional supervision signals during training such as track-            greatly. We think this is because without considering the
ing and occupancy information, which has been verified to                high-order interactions between the ego car and the other
be vital to avoid collision [16]. However, these labels in               agents, it becomes very difficult to learn the true underlying
the 3D space are difficult to annotate, rendering it not trivial         distributions of trajectories.
to use less labels to achieve competitive performance. Our                   Effect of the generative framework of autonomous
GenAD is also more efficient than UniAD, demonstrating a                 driving. We also analyzed the designs of the proposed fu-
strong performance/speed trade-off.                                      ture trajectory generation model, which is composed of two
    Perception and prediction performance. We further                    modules: trajectory prior modeling (TPM) and latent future
evaluated the perception and prediction performance of                   trajectory generation (LFTG). When using TPM alone, we


                                                                     7
                             GenAD                                                                 VAD




Figure 4. Visualizations of the results of GenAD with comparisons with VAD [21]. We provide perception, motion prediction, and
planning results with surrounding camera inputs.

directly decode the entire trajectory from the latent space.         complex traffic scenes, our GenAD still demonstrates good
With only the LFTG module, we use a gated recurrent unit             results while VAD cannot safely move through.
to gradually produce waypoints given the instance-centric
scene representation. We see that both modules are effec-            5. Conclusion
tive and improve the planning performance. Combining the
two modules further improves the performance by a large              In this paper, we have presented a generative end-to-end au-
margin. This verifies the importance of factorizing the joint        tonomous driving (GenAD) framework for better planning
distribution as in (8) to release the full potential of latent       from vision inputs. We have investigated the conventional
trajectory prior modeling.                                           serial design of perception, prediction, and planning for au-
    Visualizations. We provide a visualization of our                tonomous driving and proposed a generative framework to
GenAD model with comparisons with VAD-tiny [21] with                 enable high-order ego-agent interactions and produce more
a similar model size, as shown in Figure 4. We visualize the         accurate future trajectories with learned structural prior.
map segmentation, detection, motion prediction, and plan-            We have conducted extensive experiments on the widely
ning results on a single image and provide the surrounding           adopted nuScenes dataset and demonstrated the state-of-
camera inputs as references. We see that GenAD produces              the-art planning performance of the proposed GenAD. In
better and safer trajectories than VAD in various scenarios          the future, it is interesting to explore other generative mod-
including going straight, overtaking, and turning. For the           eling methods such as generative adversarial networks or
challenging scenarios when multiple agents are involved in           diffusion models for end-to-end autonomous driving.


                                                                 8
References                                                              [15] Shengchao Hu, Li Chen, Penghao Wu, Hongyang Li, Junchi
                                                                             Yan, and Dacheng Tao. St-p3: End-to-end vision-based au-
 [1] Frédéric Bouchard, Sean Sedwards, and Krzysztof Czar-                 tonomous driving via spatial-temporal feature learning. In
     necki. A rule-based behaviour planner for autonomous driv-              ECCV, 2022. 1, 2, 4, 6
     ing. In IJCRR, pages 263–279, 2022. 2                              [16] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima,
 [2] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora,                Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai
     Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan,                    Wang, et al. Planning-oriented autonomous driving. In
     Giancarlo Baldan, and Oscar Beijbom. nuscenes: A mul-                   CVPR, pages 17853–17862, 2023. 1, 2, 4, 6, 7
     timodal dataset for autonomous driving. In CVPR, pages             [17] Junjie Huang, Guan Huang, Zheng Zhu, and Dalong Du.
     11621–11631, 2020. 6                                                    Bevdet: High-performance multi-camera 3d object detection
 [3] Yuning Chai, Benjamin Sapp, Mayank Bansal, and Dragomir                 in bird-eye-view. arXiv preprint arXiv:2112.11790, 2021. 1,
     Anguelov. Multipath: Multiple probabilistic anchor tra-                 2
     jectory hypotheses for behavior prediction. arXiv preprint         [18] Yuanhui Huang, Wenzhao Zheng, Borui Zhang, Jie Zhou,
     arXiv:1910.05449, 2019. 2                                               and Jiwen Lu. Selfocc: Self-supervised vision-based 3d oc-
 [4] Yukang Chen, Jianhui Liu, Xiangyu Zhang, Xiaojuan Qi, and               cupancy prediction. In CVPR, 2023. 1
     Jiaya Jia. Voxelnext: Fully sparse voxelnet for 3d object          [19] Yuanhui Huang, Wenzhao Zheng, Yunpeng Zhang, Jie Zhou,
     detection and tracking. arXiv preprint arXiv:2303.11301,                and Jiwen Lu. Tri-perspective view for vision-based 3d se-
     2023. 2                                                                 mantic occupancy prediction. In CVPR, pages 9223–9232,
 [5] Zhili Chen, Maosheng Ye, Shuangjie Xu, Tongyi Cao, and                  2023. 1, 2
     Qifeng Chen. Ppad: Iterative interactions of prediction and        [20] Bo Jiang, Shaoyu Chen, Xinggang Wang, Bencheng Liao,
     planning for end-to-end autonomous driving. arXiv preprint              Tianheng Cheng, Jiajie Chen, Helong Zhou, Qian Zhang,
     arXiv:2311.08100, 2023. 1, 2                                            Wenyu Liu, and Chang Huang. Perceive, interact, predict:
 [6] Jie Cheng, Ren Xin, Sheng Wang, and Ming Liu. Mpnp:                     Learning dynamic and static clues for end-to-end motion pre-
     Multi-policy neural planner for urban driving. In IROS,                 diction. arXiv preprint arXiv:2212.02181, 2022. 2, 3
     pages 10549–10554, 2022. 2                                         [21] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jia-
 [7] Kyunghyun Cho, Bart van Merrienboer, Caglar Gulcehre,                   jie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang
     Dzmitry Bahdanau, Fethi Bougares, Holger Schwenk, and                   Huang, and Xinggang Wang. Vad: Vectorized scene rep-
     Yoshua Bengio. Learning phrase representations using                    resentation for efficient autonomous driving. arXiv preprint
     rnn encoder–decoder for statistical machine translation. In             arXiv:2303.12077, 2023. 1, 2, 3, 4, 5, 6, 7, 8
     EMNLP, page 1724, 2014. 2, 5                                       [22] Yanqin Jiang, Li Zhang, Zhenwei Miao, Xiatian Zhu, Jin
 [8] Daniel Dauner, Marcel Hallgarten, Andreas Geiger, and                   Gao, Weiming Hu, and Yu-Gang Jiang. Polarformer: Multi-
     Kashyap Chitta. Parting with misconceptions about learning-             camera 3d object detection with polar transformers. arXiv
     based vehicle motion planning. In Conference on Robot                   preprint arXiv:2206.15398, 2022. 2
     Learning (CoRL), 2023. 2                                           [23] Tarasha Khurana, Peiyun Hu, Achal Dave, Jason Ziglar,
                                                                             David Held, and Deva Ramanan. Differentiable raycasting
 [9] Benjamin Graham, Martin Engelcke, and Laurens Van
                                                                             for self-supervised occupancy forecasting. In ECCV, 2022.
     Der Maaten. 3d semantic segmentation with submanifold
                                                                             6
     sparse convolutional networks. In CVPR, pages 9224–9232,
                                                                        [24] Diederik P Kingma and Max Welling. Auto-encoding varia-
     2018. 2
                                                                             tional bayes. arXiv preprint arXiv:1312.6114, 2013. 4
[10] Junru Gu, Chenxu Hu, Tianyuan Zhang, Xuanyao Chen,
                                                                        [25] Qi Li, Yue Wang, Yilun Wang, and Hang Zhao. Hdmapnet:
     Yilun Wang, Yue Wang, and Hang Zhao. Vip3d: End-to-
                                                                             An online hd map construction and evaluation framework. In
     end visual trajectory prediction via 3d agent queries. arXiv
                                                                             ICRA, 2022. 1, 2
     preprint arXiv:2208.01582, 2022. 2
                                                                        [26] Yinhao Li, Zheng Ge, Guanyi Yu, Jinrong Yang, Zengran
[11] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun.                  Wang, Yukang Shi, Jianjian Sun, and Zeming Li. Bevdepth:
     Deep residual learning for image recognition. In CVPR,                  Acquisition of reliable depth for multi-view 3d object detec-
     pages 770–778, 2016. 3                                                  tion. arXiv preprint arXiv:2206.10092, 2022. 1, 2, 3
[12] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun.             [27] Zhiqi Li, Wenhai Wang, Hongyang Li, Enze Xie, Chong-
     Deep residual learning for image recognition. In Proceed-               hao Sima, Tong Lu, Qiao Yu, and Jifeng Dai. Bevformer:
     ings of the IEEE conference on computer vision and pattern              Learning bird’s-eye-view representation from multi-camera
     recognition, 2016. 6                                                    images via spatiotemporal transformers. In ECCV, 2022. 1,
[13] Anthony Hu, Zak Murez, Nikhil Mohan, Sofı́a Dudas, Jef-                 2, 3, 6
     frey Hawke, Vijay Badrinarayanan, Roberto Cipolla, and             [28] Ming Liang, Bin Yang, Rui Hu, Yun Chen, Renjie Liao, Song
     Alex Kendall. Fiery: Future instance prediction in bird’s-              Feng, and Raquel Urtasun. Learning lane graph representa-
     eye view from surround monocular cameras. In ICCV, 2021.                tions for motion forecasting. In ECCV, 2020. 2
     2                                                                  [29] Tingting Liang, Hongwei Xie, Kaicheng Yu, Zhongyu Xia,
[14] Peiyun Hu, Aaron Huang, John Dolan, David Held, and                     Zhiwei Lin, Yongtao Wang, Tao Tang, Bing Wang, and Zhi
     Deva Ramanan. Safe local motion planning with self-                     Tang. Bevfusion: A simple and robust lidar-camera fusion
     supervised freespace forecasting. In CVPR, 2021. 6                      framework. arXiv preprint arXiv:2205.13790, 2022. 2


                                                                    9
[30] Bencheng Liao, Shaoyu Chen, Xinggang Wang, Tianheng                       In Conference on Robot Learning, pages 718–728. PMLR,
     Cheng, Qian Zhang, Wenyu Liu, and Chang Huang. Maptr:                     2022. 2
     Structured modeling and learning for online vectorized hd            [46] Xiaoyu Tian, Tao Jiang, Longfei Yun, Yue Wang, Yilun
     map construction. arXiv preprint arXiv:2208.14437, 2022.                  Wang, and Hang Zhao. Occ3d: A large-scale 3d occu-
     1, 2, 3                                                                   pancy prediction benchmark for autonomous driving. arXiv
[31] Tsung-Yi Lin, Piotr Dollár, Ross Girshick, Kaiming He,                   preprint arXiv:2304.14365, 2023. 1, 2
     Bharath Hariharan, and Serge Belongie. Feature pyramid               [47] Wenwen Tong, Chonghao Sima, Tai Wang, Li Chen, Silei
     networks for object detection. In CVPR, pages 2117–2125,                  Wu, Hanming Deng, Yi Gu, Lewei Lu, Ping Luo, Dahua Lin,
     2017. 3                                                                   et al. Scene as occupancy. In ICCV, pages 8406–8415, 2023.
[32] Yicheng Liu, Jinghuai Zhang, Liangji Fang, Qinhong Jiang,                 1, 2, 6
     and Bolei Zhou. Multimodal motion prediction with stacked            [48] Martin Treiber, Ansgar Hennecke, and Dirk Helbing. Con-
     transformers. In CVPR, 2021. 2                                            gested traffic states in empirical observations and micro-
[33] Yingfei Liu, Tiancai Wang, Xiangyu Zhang, and Jian Sun.                   scopic simulations. Physical review E, 62(2):1805, 2000.
     Petr: Position embedding transformation for multi-view 3d                 2
     object detection. arXiv preprint arXiv:2203.05625, 2022. 2           [49] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszko-
[34] Yicheng Liu, Yue Wang, Yilun Wang, and Hang Zhao. Vec-                    reit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia
     tormapnet: End-to-end vectorized hd map learning. arXiv                   Polosukhin. Attention is all you need. NeurIPS, 2017. 2
     preprint arXiv:2206.08920, 2022. 1, 2, 3                             [50] Xiaofeng Wang, Zheng Zhu, Wenbo Xu, Yunpeng Zhang,
[35] Zhijian Liu, Haotian Tang, Alexander Amini, Xinyu Yang,                   Yi Wei, Xu Chi, Yun Ye, Dalong Du, Jiwen Lu, and Xin-
     Huizi Mao, Daniela Rus, and Song Han. Bevfusion: Multi-                   gang Wang. Openoccupancy: A large scale benchmark for
     task multi-sensor fusion with unified bird’s-eye view repre-              surrounding semantic occupancy perception. arXiv preprint
     sentation. arXiv preprint arXiv:2205.13542, 2022. 2                       arXiv:2303.03991, 2023. 1, 2
[36] Ilya Loshchilov and Frank Hutter.            Sgdr: Stochas-          [51] Yi Wei, Linqing Zhao, Wenzhao Zheng, Zheng Zhu, Jie
     tic gradient descent with warm restarts. arXiv preprint                   Zhou, and Jiwen Lu. Surroundocc: Multi-camera 3d occu-
     arXiv:1608.03983, 2016. 7                                                 pancy prediction for autonomous driving. In ICCV, pages
[37] Ilya Loshchilov and Frank Hutter. Decoupled weight decay                  21729–21740, 2023. 1, 2
     regularization. arXiv preprint arXiv:1711.05101, 2017. 7             [52] Wenyuan Zeng, Wenjie Luo, Simon Suo, Abbas Sadat, Bin
[38] Jiageng Mao, Yujing Xue, Minzhe Niu, Haoyue Bai, Jiashi                   Yang, Sergio Casas, and Raquel Urtasun. End-to-end inter-
     Feng, Xiaodan Liang, Hang Xu, and Chunjing Xu. Voxel                      pretable neural motion planner. In CVPR, 2019. 6
     transformer for 3d object detection. In ICCV, pages 3164–            [53] Yunpeng Zhang, Zheng Zhu, Wenzhao Zheng, Junjie Huang,
     3173, 2021. 2                                                             Guan Huang, Jie Zhou, and Jiwen Lu. Beverse: Unified per-
[39] Jiquan Ngiam, Benjamin Caine, Vijay Vasudevan, Zheng-                     ception and prediction in birds-eye-view for vision-centric
     dong Zhang, Hao-Tien Lewis Chiang, Jeffrey Ling, Rebecca                  autonomous driving. arXiv preprint arXiv:2205.09743,
     Roelofs, Alex Bewley, Chenxi Liu, Ashish Venugopal, et al.                2022. 1, 2, 6
     Scene transformer: A unified architecture for predicting mul-        [54] Wenzhao Zheng, Weiliang Chen, Yuanhui Huang, Borui
     tiple agent trajectories. arXiv preprint arXiv:2106.08417,                Zhang, Yueqi Duan, and Jiwen Lu. Occworld: Learning a
     2021. 2                                                                   3d occupancy world model for autonomous driving. arXiv
[40] Tung Phan-Minh, Elena Corina Grigore, Freddy A Boulton,                   preprint arXiv:2311.16038, 2023. 2
     Oscar Beijbom, and Eric M Wolff. Covernet: Multimodal                [55] Yin Zhou and Oncel Tuzel. Voxelnet: End-to-end learning
     behavior prediction using trajectory sets. In CVPR, 2020. 2               for point cloud based 3d object detection. In CVPR, pages
[41] Jonah Philion and Sanja Fidler. Lift, splat, shoot: Encoding              4490–4499, 2018. 2
     images from arbitrary camera rigs by implicitly unprojecting         [56] Xizhou Zhu, Weijie Su, Lewei Lu, Bin Li, Xiaogang Wang,
     to 3d. In ECCV, pages 194–210, 2020. 1, 2                                 and Jifeng Dai. Deformable detr: Deformable transformers
[42] Stefano Pini, Christian S Perone, Aayush Ahuja, Ana                       for end-to-end object detection. In ICLR, 2020. 3
     Sofia Rufino Ferreira, Moritz Niendorf, and Sergey                   [57] Sicheng Zuo, Wenzhao Zheng, Yuanhui Huang, Jie Zhou,
     Zagoruyko. Safe real-world autonomous driving by learn-                   and Jiwen Lu. Pointocc: Cylindrical tri-perspective view
     ing to predict and plan with a mixture of experts. In ICRA,               for point-based 3d semantic occupancy prediction. arXiv
     pages 10069–10075, 2023. 2                                                preprint arXiv:2308.16896, 2023. 1, 2
[43] Nathan D Ratliff, J Andrew Bagnell, and Martin A Zinke-
     vich. Maximum margin planning. In ICML, pages 729–736,
     2006. 6
[44] Cody Reading, Ali Harakeh, Julia Chae, and Steven L
     Waslander. Categorical depth distribution network for
     monocular 3d object detection. In CVPR, 2021. 1, 2
[45] Oliver Scheel, Luca Bergamini, Maciej Wolczyk, Błażej
     Osiński, and Peter Ondruska. Urban driver: Learning to
     drive from real-world demonstrations using policy gradients.


                                                                     10
