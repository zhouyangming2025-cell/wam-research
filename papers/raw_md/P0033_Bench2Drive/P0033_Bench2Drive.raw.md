# Bench2Drive: Towards Multi-Ability Benchmarking of Closed-Loop End-To-End Autonomous Driving

Xiaosong Jia\* Zhenjie Yang\* Qifeng Li\* Zhiyuan Zhang\*

Junchi Yan<sup>†</sup> Equal contributions. <sup>†</sup> Correspondence author

Dept. of CSE & School of AI & MoE Key Lab of AI, Shanghai Jiao Tong University

https://thinklab-sjtu.github.io/Bench2Drive/

## Abstract

In an era marked by the rapid scaling of foundation models, autonomous driving technologies are approaching a transformative threshold where end-to-end autonomous driving (E2E-AD) emerges due to its potential of scaling up in the data-driven manner. However, existing E2E-AD methods are mostly evaluated under the open-loop log-replay manner with L2 errors and collision rate as metrics (e.g., in nuScenes), which could not fully reflect the driving performance of algorithms as recently acknowledged in the community. For those E2E-AD methods evaluated under the closed-loop protocol, they are tested in fixed routes (e.g., Town05Long and Longest6 in CARLA) with the driving score as metrics, which is known for high variance due to the unsmoothed metric function and large randomness in the long route. Besides, these methods usually collect their own data for training, which makes algorithm-level fair comparison infeasible.

To fulfill the paramount need of comprehensive, realistic, and fair testing environments for Full Self-Driving (FSD), we present Bench2Drive, the first benchmark for evaluating E2E-AD systems’ multiple abilities in a closed-loop manner. Bench2Drive’s oficial training data consists of 2 million fully annotated frames, collected from 13638 short clips uniformly distributed under 44 interactive scenarios (cut-in, overtaking, detour, etc), 23 weathers (sunny, foggy, rainy, etc), and 12 towns (urban, village, university, etc) in CARLA v2. Its evaluation protocol requires E2E-AD models to pass 44 interactive scenarios under diferent locations and weathers which sums up to 220 routes and thus provides a comprehensive and disentangled assessment about their driving capability under diferent situations. We implement state-of-the-art E2E-AD models and evaluate them in Bench2Drive, providing insights regarding current status and future directions.

## 1 Introduction

In recent years, the field of autonomous driving has witnessed tremendous growth, fueled by the rapid advancement and scaling of foundation models [1–3]. These developments have ushered in a new era of end-to-end autonomous driving (E2E-AD) systems [4–8], which promise a scalable, data-driven approach to vehicle automation, opposed to traditional module-based perception [9–13], prediction [14–17], planning [18–20] pipeline. Such systems are designed to be capable of learning from vast amounts of data, potentially transforming the landscape of vehicle intelligence.

![](images/df153035be501a440842e625f6d77d91a42877aa21d2756cc360558517e78f7c.jpg)  
Figure 1: Overview of Bench2Drive.

Despite these advancements, the evaluation methodologies for E2E-AD systems remain a critical bottleneck. One popular way is to conduct log-replay with the recorded expert trajectories in dataset like nuScenes [21], i.e., open-loop evaluation. These models [4, 22] usually predict the future locations of the ego vehicle with the raw sensor information as inputs. As for metrics, the L2 error relative to the recorded trajectories and the ratio of collision happening are used. However, as widely discussed in the community [23, 24, 19], these open-loop metrics are insuficient for showcasing proficiency in planning, due to issues including distribution shift [25], causal confusion [26, 27], etc. nuScenes is also problematic due to its small and imbalanced validation set (around 75% of the frames only require continuing to drive straight) [24]. As a result, only encoding the ego status (location, speed, etc) [23] could achieve similar L2 errors compared to complex methods with sensor inputs [4], which prompts a call for a closed-loop evaluation benchmark for E2E-AD.

CARLA [28] is one of the most widely used simulator for closed-loop E2E-AD evaluation. Within its framework, benchmarks such as Town05Long and Longest6 have been established, featuring multiple routes that require AD systems to complete safely within specific time constraints. However, these benchmarks only assess basic skills such as lane following, making turns, collision avoidance, and trafic lights obeying [29, 30], failing to examine AD systems’ driving ability under complicated and interactive trafic. The latest CARLA Leaderboard v2 introduces 39 challenging scenarios designed to evaluate the robustness of AD systems in more intricate situations. Nevertheless, the oficial routes for evaluation, ranging from 7 to 10 kilometers and filled with scenarios, present a formidable challenge, often too dificult to complete flawlessly, as shown in Fig. 2 (a). Consequently, with the driving score metric employing an exponential decay function, it becomes challenging to efectively compare diferent AD systems, as they tend to score very low. For instance, in the current Leaderboard v2<sup>1</sup>, participating methods score less than 10 points out of 100. Besides, existing methods usually collect data by themselves which makes algorithm-level fair comparison infeasible.

To address the aforementioned challenges in evaluating autonomous driving (AD) systems, it is essential to develop a new benchmark that fairly assesses their capabilities in a granular manner. To this end, we introduce Bench2Drive, a new benchmark designed to evaluate E2E-AD systems in a comprehensive, realistic, and fair closed-loop environment. Bench2Drive has an oficial training dataset collected by state-of-the-art expert model Think2Drive [31], comprising 2 million fully annotated frames, sourced from 13638 clips. It span a diverse array of 44 interactive scenarios such as cut-ins, overtakings, and detours under diferent weather conditions and towns, ranging from sunny days in bustling city centers to foggy conditions in quaint villages. The evaluation protocol includes 220 short routes, each only around 150 meters in length and containing a single specific scenario. In this way, the assessment of individual skills is isolated and thus allows for a detailed comparison of the AD systems’ proficiency across 44 distinct skill sets. Moreover, the brevity of each route mitigates the impact of the exponential decay function on the driving score, facilitating a more accurate and meaningful comparison of performance across diferent systems. Such a structured and focused benchmark would provide clearer insights into the strengths and weaknesses of each AD system, enabling targeted improvements and more refined technology development.

(a) CARLA Leaderboard V2  
![](images/0b2ef71b5dd90b32eea829ee0f4252a761d1695a8fdeb6b403af6e70e30e3394.jpg)

![](images/10895f5db81ed46b457a5da6e485c21d7566061673af8365179132471df91ab6.jpg)  
(b) Bench2Drive Dataset  
Figure 2: Route length on Town12. We use diferent colors to represent diferent routes. Bench2Drive’s short routes provide more smoothed evaluations.

In summary, the proposed Bench2Drive benchmark features:

• Comprehensive Scenario Coverage: Bench2Drive is designed to test AD systems across 44 interactive scenarios, providing a thorough evaluation about capabilities under complex situations.

• Granular Skill Assessment: By structuring the evaluation across 220 short routes, each focusing on a specific driving scenario, Bench2Drive allows for detailed analysis and comparison of how diferent AD systems perform on individual tasks.

• Closed-Loop Evaluation Protocol: Bench2Drive evaluates AD systems in a closed-loop manner, where the AD system’s actions directly influence the environment. This setup ofers an accurate assessment of an AD system’s driving performance.

• Diverse Large-Scale Oficial Training Data: Bench2Drive consists of a standardized training set of 2 million fully annotated frames from 13638 clips under diverse scenarios, weathers, and towns, ensuring that all AD systems are trained under abundant yet similar conditions, which is crucial for fair algorithm-level comparisons.

These features make Bench2Drive a pioneering benchmark in the field of autonomous driving, providing an essential toolfor researchers to refine and evaluate their E2E-AD systems in a realistic, comprehensive, and fair manner. We implement several classic baselines including TCP [5], ThinkTwice [30], DriveAdapter [27], UniAD [4], VAD [22], and AD-MLP [23] and evaluate them in the Bench2Drive. We confirm the fact that open-loop metrics like L2 error could not reflect the actual driving performance. For the classic closed-loop metric - Drive Score, we find that it lack details and its heavy punishment encourages over-conservative driving strategies while Bench2Drive ofers a comprehensive understanding about capabilities of diferent methods.

## 2 Related Work

## 2.1 Planning Benchmarks

Benchmarking in the field of autonomous driving has evolved from specialized datasets, such as KITTI [32] for perception and NGSIM/highD [33], BARK [34] for behavior prediction, to integrated forms like nuScenes [21], Argoverse [35], and Waymo [36], which facilitate the evaluation of various synergic system components. Recently, the assessment of planning capabilities for learning-based methods has become an area of interest [37–41]. In Table 1, we present a comparison of planning benchmarks. nuScenes [21], while ofering open-loop metrics, has been critiqued for its inability to adequately evaluate planning proficiency due to the lack of closed-loop simulation [23, 24, 19]. Furthermore, it sufers from an imbalanced validation set, with a significant portion (75%) of scenarios only requiring straightforward driving, thus inadequately challenging the decision-making capabilities of AD systems in complex environments [24]. nuPlan [38] and Waymax [37] ofer closed-loop evaluations but are limited to bounding box level assessments, excluding sensor simulation and, consequently, are not suitable for E2E-AD methods. Longest6 [6], a modified version of CARLA

Table 1: Comparison with related planning benchmarks Bench2Drive is the only benchmark to evaluate the E2E-AD methods under closed-loop with multi-ability analysis.
<table><tr><td>Benchmark</td><td>Sensor</td><td>Closed-Loop</td><td>E2E-Sim</td><td>Expert</td><td>Complex</td><td>Multi-Ability-Eval</td></tr><tr><td>nuScenes [21]</td><td>√</td><td>X</td><td>X</td><td>√</td><td>X</td><td>X</td></tr><tr><td>nuPlan [38]</td><td>√</td><td>√</td><td>X</td><td>√</td><td>√</td><td>X</td></tr><tr><td>Waymax [37]</td><td>X</td><td>√</td><td>X</td><td>√</td><td>√</td><td>X</td></tr><tr><td>Longest6 [6]</td><td>√</td><td>√</td><td>√</td><td>√</td><td>X</td><td>X</td></tr><tr><td>CARLA LB V2 [28]</td><td>√</td><td>√</td><td>√</td><td>X</td><td>√</td><td>X</td></tr><tr><td>Bench2Drive (Ours)</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td></tr></table>

Leaderboard V1, only assesses basic skills such as lane following, making turns, collision avoidance, and trafic lights. CARLA Leaderboard V2 [28] lacks expert demonstration data. As widely discussed in the community [42, 43], the lack of an oficial training set makes the comparisons of diferent methods in the system-level instead of the algorithm-level.Bench2Drive deal with these shortcomings by ofering a large-scale, annotation-rich oficial training dataset alongside a multi-ability evaluation set. This enables a more granular and informative assessment of an AD system’s driving capabilities, overcoming the limitations of existing benchmarks that rely on average scoring across all routes as their primary performance metric.

## 2.2 End-to-End Autonomous Driving

The concept of E2E-AD could date back to 1980s [44]. Recently, the arise of neural network, especially Transformer [45], demonstrates the power of scaling laws, which rejuvenates the enthusiasm for E2E-AD [46–50]. However, they are either evaluated only in the open-loop way [51, 4, 22, 52] or in the relatively simple scenes like Town05Long/Longest6 [53, 54, 42, 55–60]. Bench2Drive ofers a challenging and comprehensive arena to compare E2E-AD methods’ ability.

## 3 Bench2Drive

Bench2Drive consists of a large-scale fully annotated dataset collected in CARLA as the oficial training set, an evaluation toolkit for the granular driving skill assessment, and implementations of several state-of-the-art E2E-AD methods tailored for the training dataset and evaluation toolkit. Al data, codes, and checkpoints are in GitHub and Huggingface under Apache License 2.0. We give details in the following section.

## 3.1 Data Collection Agent

The data collection agent (expert) is responsible for collecting the data so that student models could learn from the data. In the real world, this is usually done by human to drive around the city, like the curation of KITTI [32], nuScenes [21], Waymo [36], Argoverse [35]. However, it requires lots of human eforts. In simulation, there is a cheap substitute - teacher model. The teacher model would use information not available in the real world (termed privileged information), for example, ground-truth locations, states, and intentions of surrounding agents and ground-truth states of trafic lights, etc. As a result, people using CARLA either write rules [43, 61] or train a RL model [50, 31] to use the privileged information to drive in the simulation.

In this work, we use the world model based reinforcement learning teacher - Think2Drive [31] to navigate in CARLA and collect data, since it is the only expert model which is able to solve all 44 scenarios during the construction of Bench2Drive. Notably, after the release of Bench2Drive, the rule-based expert PDM-Lite [61]<sup>2</sup> is open sourced and users could use it for customized demand.

## 3.2 Expert Dataset

Existing E2E-AD methods evaluated in the closed-loop manner [5, 6, 56, 57] typically collect their own data using the CARLA simulator. However, as highlighted in [42, 43], the size and distributions of these datasets significantly influence performance, rendering fair algorithm-level comparisons challenging. To address this, we have constructed a large-scale expert dataset with comprehensive annotations including 3D bounding boxes, depth, and semantic segmentation, sampled at 10 Hz, to serve as the oficial training set. As the information from expert could be an important guidance of student models [49, 27, 60], we also provide the expert model - Think2Drive’s [31] value estimation and features. Fig. 3 gives an overview. To facilitate the re-implementation of existing E2E-AD methods of community, we adopt a sensor configuration similar to nuScenes [21]:

![](images/c787323585febabef3efa3a3c00e7c0a84c9001c7a8ec07cd64d891d9ac9ce6d.jpg)  
Figure 3: Sensor setting and annotations of the expert dataset. We follow the sensor settings of nuScenes [21]. The annotations include 3D bounding boxes, depth, semantic/instance segmentation, HD-Map, and RL value estimations and features from Think2Drive [31] Expert.

![](images/1a8f98e64618c9fa65eb8439c6147361ab79f7ded6c854e98c3cfdc513f63aef.jpg)  
Figure 4: Distribution of scenario ’ConstructionObstacle’ in Town12 We use diferent colors to represent diferent routes containing ’ConstructionObstacle’. Bench2Drive has more locations that be able to generate ’ConstructionObstacle’.

• 1x LiDAR: 64 channels, 85-meter range, 600,000 points per second

• 6x Camera: Surround coverage, 900x1600 resolution, JPEG compression (quality-level 20)

• 5x Radar: 100-meter range, 30◦ horizontal and vertical FoV

• 1x IMU & GNSS: Location, yaw, speed, acceleration, and angular velocity

• 1x BEV Camera: Debugging, visualization, remote sensing

• HD-Map: Lanes, centerlines, topology, dynamic light states, trigger areas for lights and stop signs

Moreover, to tackle the challenge posed by the long-tail distribution of data from both perception and behavior perspectives, a significant bottleneck in autonomous driving [62] (approximately 75% of the clips in nuScenes only involve the ego vehicle driving straight), we ensure the distribution of weather conditions, landscapes, and behaviors are as uniform as possible. We add more available locations for scenarios compared to the oficial routes of CARLA Leaderboard V2 as shown in Fig. 4, enhancing the data diversity. Further, we design 5 more scenarios beyond Leaderboard V2 to enhance behavior diversity as detailed in Appendix G. We give the distribution of scenarios and weathers and towns in Appendix B. As illustrated, Bench2Drive dataset is rich in both perception and behavior diversity.

For data partitioning, we segmented the driving process into short clips, each approximately 150 meters in length and containing a single specific scenario. This segmentation allows for the curriculum learning [63] of individual driving skills. To cater to diferent computational capabilities, we designed three data subsets: mini (10 clips for debugging and visualization), base (1,000 clips, comparable to nuScenes, suitable for 8xRTX3090 server), and full (10,000 clips for large-scale studies).

Table 2: Skill Set & Scenarios
<table><tr><td rowspan=1 colspan=1>Skill</td><td rowspan=1 colspan=1>Scenario</td></tr><tr><td rowspan=1 colspan=1>Merging</td><td rowspan=1 colspan=1>CrossingBicycleFlow, EnterActorFlow, HighwayExit, InterurbanActor-Flow, HighwayCutIn, InterurbanAdvancedActorFlow, MergerIntoSlowTraf-ficV2, MergeIntoSlowTraffic, NonSignalizedJunctionLeftTurn, NonSignalized-JunctionRightTurn, NonSignalizedJunctionLeftTurnEnterFlow, ParkingExit,LaneChange, SignalizedJunctionLeftTurn, SignalizedJunctionRightTurn, Sig-nalizedJunctionLeftTurnEnterFlow</td></tr><tr><td rowspan=1 colspan=1>Overtaking</td><td rowspan=1 colspan=1>Accident, AccidentTwoWays, ConstructionObstacle, ConstructionObstacleT-woWays, HazardAtSideLaneTwoWays, HazardAtSideLane, ParkedObstacleT-woWays, ParkedObstacle, VehicleOpenDoorTwoWays</td></tr><tr><td rowspan=1 colspan=1>Emergency Brake</td><td rowspan=1 colspan=1>BlockedIntersection, DynamicObjectCrossing, HardBreakRoute, OppositeVe-hicleTakingPriority, OppositeVehicleRunningRedLight, ParkingCutIn, Pedes-trianCrossing, ParkingCrossingPedestrian, StaticCutIn, VehicleTurningRoute,VehicleTurningRoutePedestrian, ControlLoss</td></tr><tr><td rowspan=1 colspan=1>Give Way</td><td rowspan=1 colspan=1>InvadingTurn, YieldToEmergencyVehicle</td></tr><tr><td rowspan=1 colspan=1>Traffic Sign</td><td rowspan=1 colspan=1>EnterActorFlow, CrossingBicycleFlow, NonSignalizedJunctionLeftTurn,NonSignalizedJunctionRightTurn, NonSignalizedJunctionLeftTurnEnterFlow,OppositeVehicleTakingPriority, OppositeVehicleRunningRedLight, Pedestrian-Crossing, SignalizedJunctionLeftTurn, SignalizedJunctionRightTurn, Signal-izedJunctionLeftTurnEnterFlow, TJunction, VanillaNonSignalizedTurn, Vanil-laSignalizedTurnEncounterGreenLight, VanillaSignalizedTurnEncounterRed-Light, VanillaNonSignalizedTurnEncounterStopsign, VehicleTurningRoute, Ve-hicleTurningRoutePedestrian</td></tr></table>

## 3.3 Multi-Ability Evaluation

Existing planning benchmarks [28, 38, 37] assess the performance of AD systems by averaging scores across all provided routes. This approach ofers a general overview of driving capabilities but fails to pinpoint specific strengths and weaknesses of diferent methods. Even worse, existing benchmarks in CARLA like Longest6 [6] and Leaderboard V2 [28] cover several kilometers, leading to high variance in the driving score metric. This variance arises because the infraction score penalizes errors through cumulative multiplication, which can significantly skew results. For instance, consider three test runs where each achieves 90% route completion, but the number of red lights run difers: 0, 1, and 2. The corresponding driving scores would be 90, $9 0 * 0 . 7 = 6 3$ , and $9 0 * \bar { 0 } . 7 * 0 . 7 = 4 4 . 1$ , which causes a large standard deviation - 18.9 and thus makes comparison between methods unreliable.

To address these issues, we propose a more granular evaluation framework for all 44 scenarios by designing 5 distinct short routes (around 150 meters in length) per scenario, each featuring diferent weathers and towns, which result in a total of 220 routes. This approach allows people to assess AD systems’ capabilities by isolated skills, leading to a more detailed analysis with reduced variance. Further, we summarize 5 advanced skills for urban driving: Merging, Overtaking, Give Way, Trafic Sign, Emergency Brake as in Table 2 and report the score of each skill. The decoupled design provides a clearer insight into which skills are efectively handled by the AD systems and which are not, fostering a more nuanced understanding of system performance.

Formally, the evaluation set consists of 220 routes and each route defines a pair of source location $( x _ { \mathrm { s r c } } , y _ { \mathrm { s r c } } )$ and destination location $( x _ { \mathrm { d s t } } , y _ { \mathrm { d s t } } )$ in one specific town and weather. Given raw sensor inputs (cameras, LiDAR, IMU/GPS, etc) as well as the target waypoints, the ego vehicle should drive from source to the destination location. We design two metrics to evaluate the performance:

• Success Rate (SR): This metric measures the proportion of successfully completed routes within the allotted time and without trafic violations. A route is deemed successful if the ego vehicle reaches its destination without any rule infractions. The success rate is calculated as the ratio of successful routes to the total number of routes, as shown in Equ. 1 (left).

• Driving Score (DS): This metric follows CARLA [28] oficial metric as reference. It considers both route completion and penalty for infractions. Specifically, it averages the route completion percentages and penalizes infractions based on their severity, as depicted in Equation 1 (right). The driving score is normalized by the total number of routes from same type or group as well.

$$
{ \mathrm { S u c c e s s ~ R a t e } } = { \frac { n _ { \mathrm { s u c c e s s } } } { n _ { \mathrm { t o t a l } } } } \qquad { \mathrm { D r i v i n g ~ S c o r e } } = { \frac { 1 } { n _ { \mathrm { t o t a l } } } } \sum _ { i = 1 } ^ { n _ { \mathrm { t o t a l } } } { \mathrm { R o u t e } } - { \mathrm { C o m p l e t i o n } } _ { i } * \prod _ { j = 1 } ^ { n _ { i , \mathrm { p o u t p } } } p _ { i , j }\tag{1}
$$

where $n _ { \mathrm { s u c c e s s } }$ and $n _ { \mathrm { t o t a l } }$ denote the number of successful routes and total samples respectively; Route-Completion<sub>𝑖</sub> representats the percentage of route distance completed for the 𝑖-th route; $p _ { i , j }$ means the 𝑗-th infraction penalty on the 𝑖-th route. Please refer to Appendix F for details about infraction types and penalties scores.

Further, beyond the the goal achieving ability of algorithms, we propose the following two metrics to measure the eficiency and smoothness of driving trajectories:

• Eficiency: The CARLA team has implemented a function to check whether the self-driving car’s speed is too low. This is determined by comparing the vehicle’s speed with nearby vehicle:

$$
{ \mathrm { S p e e d ~ P e r c e n t a g e } } = { \frac { { \mathrm { E g o ~ V e h i c l e } } ^ { \prime } { \mathrm { s ~ S p e e d } } } { \mathrm { A v e r a g e ~ S p e e d ~ o f ~ N e a r b y ~ V e h i c l e s } } }\tag{2}
$$

This function calculates the speed percentage using the vehicle’s speed and the average speed of nearby vehicles at current frame. CARLA Leaderboard sets four checkpoints per route and checks the ego vehicle’s speed when the ego vehicle arrives a checkpoint. Specifically, if the vehicle is faster than nearby vehicles, the driving eficiency would be larger than 100%. The check results are included as a penalty in the final driving score. However, with only four checkpoints, the vehicle must cover 25% of the total route distance before reaching the next checkpoint. This leads to a high variance in the penalty values for low speeds, complicating the reflection of driving capabilities in the driving scores. To alleviate this, we increase the number of checkpoints to 20. Speed check is now performed every 5% of the total route length, and it is excluded from the driving score calculation. The final driving eficiency metric is defined as the average of the speed percentage over all checks.

$$
\mathrm { D r i v i n g ~ E f f i c i e n c y } = \frac { \sum _ { i } \mathrm { S p e e d ~ P e r c e n t a g e } _ { i } } { \mathrm { S p e e d ~ C h e c k ~ T i m e s } }\tag{3}
$$

If the ego vehicle fails to pass the initial 5% checkpoint, this route is not included in the final driving eficiency metric calculation. To account for cases where abnormal speed spikes may occur (e.g., when the vehicle falls of the current map layer), speed percentage values exceeding 1000% are filtered out.

Comfortness: Comfortness is closely related to human experience and thus requires comparing autonomous driving policy with the behavior of numerous human driving experts to measure it. For this, we follow the popular benchmark nuPlan’s [38] smoothness(also called comfort) protocol, which evaluates ego’s minimum and maximum longitudinal accelerations, the maximum absolute values of lateral acceleration, yaw rate, yaw acceleration, the longitudinal component of jerk, and the maximum magnitude of the jerk vector. These variables are compared to thresholds with default values determined empirically from the examination of nuPlan’s human expert trajectories. Comfortness is measured based on whether these values fall within the upper and lower bounds of the expert values.

$$
\begin{array} { r l } { \mathrm { F r a m e ~ V a r i a b l e ~ S m o o t h n e s s ~ ( F V S ) } = \displaystyle { \left\{ \begin{array} { l l } { \mathrm { T r u e } } & { \mathrm { ~ i f ~ l o w e r ~ b o u n d ~ } \le p _ { i } \le \mathrm { ~ u p p e r ~ b o u n d , } } \\ { \mathrm { F a l s e } } & { \mathrm { o t h e r w i s e } } \end{array} \right. } } \\ { p \in \mathrm { s m o o t h n e s s ~ v a r s , } \ 0 \le i \le t \mathrm { o t a l ~ f r a m e s } } & { } \end{array}\tag{4}
$$

where smoothness variables(vars) include: longitudinal acceleration - expert bound: [-4.05, 2.40], maximum absolute lateral acceleration - expert bound: [-4.89, 4.89], yaw rate - expert bound: [-0.95, 0.95], yaw acceleration - expert bound: [-1.93, 1.93], longitudinal component of jerk - expert bound: [-4.13, 4.13], maximum magnitude of jerk vector - expert bound:[-8.37, 8.37]. A trajectory is deemed Smooth only if all smoothness variables meet the smoothness criteria.

$$
\mathrm { T r a j e c t o r y ~ S m o o t h n e s s } = \bigwedge _ { i = 0 } ^ { \mathrm { t o t a l ~ f r a m e s } } \mathrm { F V S }
$$

In nuPlan, smoothness is determined by frame-by-frame evaluation of these variables over the entire trajectory, which makes it susceptible to local driving behaviors. For example, if a vehicle ahead suddenly brakes, the ego vehicle must also brake abruptly to avoid a collision. Even if the ego’s hard brake behavior is appropriate in this case and its driving is smooth at other times, the entire trajectory could still be judged as unsmooth, leading to unreasonable evaluation results. To mitigate this issue, we segment the entire trajectory at a timestep interval 𝑛 = 20 for evaluation.

$$
{ \mathrm { S e g m e n t ~ S m o o t h n e s s } } = \bigwedge _ { i = \mathrm { s t a r t } \mathrm { f r a m e } } ^ { \mathrm { e n d f r a m e } } { \mathrm { F V S } }
$$

The final smoothness metric is defined as the ratio of smooth trajectory segments to the total number of segments.

$$
\mathrm { S m o o t h n e s s } = \frac { \mathrm { N u m b e r ~ o f ~ S m o o t h n e s s ~ S e g m e n t s } } { \mathrm { T o t a l ~ S e g m e n t s } }
$$

Specifically, if the ego vehicle is blocked (speed remains below 0.1 for more than 60 seconds.), resulting in a failure case, this segment is still be considered as smooth because its speed is safe for human. Note that if the total frames of a trajectory are less than 20, the respective route is excluded from the smoothness assessment.

## 4 Experiments

## 4.1 Baselines & Datasets

To establish a starting point for the community, we have implemented several classic E2E-AD methods in Bench2Drive including:

• UniAD [4] explicitly conducts perception and prediction and uses Transformer Query to transport information. Together with it, we also implement the commonly used BEVFormer [10] in Bench2Drive,

• VAD [22] also adopts Transformer Query yet with vectorized scene representation and thus improves eficiency.

• AD-MLP [23] simply feeds the ego vehicle’s history states into an MLP to predict future trajectories, which is a simple baseline for history state interpolation planner.

• TCP [64] only uses the front cameras and the ego state as inputs to predict both trajectories and control signals. It is a simple yet efective baseline in CARLA v1.

• ThinkTwice [30] promotes the idea of coarse-to-fine by refining the planning routes in a layer-bylayer manner and distilling the expert features.

• DriveAdapter [27] proposes a new paradigm to fully unleash the power of expert model by decoupling the learning of perception and planning and connecting the two parts by adapter modules.

Recognizing the varied computational resources available within the community, we have trained these baseline models on the base subset (1,000 clips). We use 950 clips for training while leaving 50 clips for open-loop evaluation. We ensure that the validation set contains at least one clip for each of 44 scenarios and the weather distribution is balanced. AD-MLP and TCP are trained with 1 \* A6000 while ThinkTwice, DriveAdapter, UniAD, and VAD are trained with 8 \* A100. For the closed-loop evaluation, we run all models in CARLA with the 220 test routes mentioned in Sec. 3.3 and calculate the metric accordingly. Note that some models’ might have wrong behaviors in some certain routes (e.g., driving to some buggy location) and cause CARLA to crash without scoring. We treat these routes as 0 score. Please refer to Appendix C for more implementation details.

## 4.2 Results

In Table 3 and Table 4, we compare baselines E2E-AD methods with both open-loop and closed-loop evaluation, which lead to the following findings:

Open-loop metric could indicate model convergence but it fails for advanced comparison.. AD-MLP has a high L2 error and performs extremely bad in closed-loop evaluation while VAD has a low L2 error and a decent closed-loop performance. It shows that we could use L2 error to verify the convergence andfitting status ofneural networks, i.e., when the L2 error is very high, there should be something wrong within the system. In this case, AD-MLP does not use raw sensors, which is similar to drive blindly and thus infeasible to fit the dataset. Notably, diferent from findings in nuScenes [21], AD-MLP fails to achieve decent L2 error in Bench2Drive, due to the better behavior diversity as shown in Fig. 5. On the other hand, UniAD-base has a lower L2 error compared to VAD yet with worse closed-loop performance, aligning with findings in [19, 24]. Open-loop evaluation ignore the issues including distribution shift [25] and causal confusion [26, 27] and thus fails to give meaningful comparsion for models with good fitting of dataset, demonstrating the importance of closed-loop evaluation. For eficiency and smoothness, we could observe that AD-MLP has the lowest eficiency due to its quick failure and stuck. UniAD has higher eficiency and smoother trajectories compared to TCP-traj, demonstrating the efectivenes of the UniAD’s post optimization for the planning head.

Table 3: Open-loop and Closed-loop Results of E2E-AD Methods in Bench2Drive under base training set. Avg. L2 is averaged over the predictions in 2 seconds under 2Hz, similar to UniAD. \* denotes expert feature distillation.
<table><tr><td rowspan="2">Method</td><td>Open-loop Metric</td><td colspan="4">Closed-loop Metric</td></tr><tr><td>Avg. L2 ↓</td><td>Driving Score ↑</td><td>Success Rate(%) ↑</td><td>Efficiency ↑</td><td>Comfortness ↑</td></tr><tr><td>AD-MLP [23]</td><td>3.64</td><td>18.05</td><td>0.00</td><td>48.45</td><td>22.63</td></tr><tr><td>UniAD-Tiny [4]</td><td>0.80</td><td>40.73</td><td>13.18</td><td>123.92</td><td>47.04</td></tr><tr><td>UniAD-Base [4]</td><td>0.73</td><td>45.81</td><td>16.36</td><td>129.21</td><td>43.58</td></tr><tr><td>VAD [22]</td><td>0.91</td><td>42.35</td><td>15.00</td><td>157.94</td><td>46.01</td></tr><tr><td>TCP* [5]</td><td>1.70</td><td>40.70</td><td>15.00</td><td>54.26</td><td>47.80</td></tr><tr><td>TCP-ctrl*</td><td></td><td>30.47</td><td>7.27</td><td>55.97</td><td>51.51</td></tr><tr><td>TCP-traj*</td><td>1.70</td><td>59.90</td><td>30.00</td><td>76.54</td><td>18.08</td></tr><tr><td>TCP-traj w/o distillation</td><td>1.96</td><td>49.30</td><td>20.45</td><td>78.78</td><td>22.96</td></tr><tr><td>ThinkTwice* [30]</td><td>0.95</td><td>62.44</td><td>31.23</td><td>69.33</td><td>16.22</td></tr><tr><td>DriveAdapter* [27]</td><td>1.01</td><td>64.22</td><td>33.08</td><td>70.22</td><td>16.01</td></tr></table>

Table 4: Multi-Ability Results of E2E-AD Methods under base training set. \* denotes expert feature distillation.
<table><tr><td rowspan="2">Method</td><td colspan="6">Ability (%) ↑</td></tr><tr><td>Merging</td><td>Overtaking</td><td>Emergency Brake</td><td>Give Way</td><td>Traffic Sign</td><td>Mean</td></tr><tr><td>AD-MLP [23]</td><td>0.00</td><td>0.00</td><td>0.00</td><td>0.00</td><td>4.35</td><td>0.87</td></tr><tr><td>UniAD-Tiny [4]</td><td>8.89</td><td>9.33</td><td>20.00</td><td>20.00</td><td>15.43</td><td>14.73</td></tr><tr><td>UniAD-Base [4]</td><td>14.10</td><td>17.78</td><td>21.67</td><td>10.00</td><td>14.21</td><td>15.55</td></tr><tr><td>VAD [22]</td><td>8.11</td><td>24.44</td><td>18.64</td><td>20.00</td><td>19.15</td><td>18.07</td></tr><tr><td>TCP* [5]</td><td>16.18</td><td>20.00</td><td>20.00</td><td>10.00</td><td>6.99</td><td>14.63</td></tr><tr><td>TCP-ctrl*</td><td>10.29</td><td>4.44</td><td>10.00</td><td>10.00</td><td>6.45</td><td>8.23</td></tr><tr><td>TCP-traj*</td><td>8.89</td><td>24.29</td><td>51.67</td><td>40.00</td><td>46.28</td><td>34.22</td></tr><tr><td>TCP-traj w/o distillation</td><td>17.14</td><td>6.67</td><td>40.00</td><td>50.00</td><td>28.72</td><td>28.51</td></tr><tr><td>ThinkTwice* [30]</td><td>27.38</td><td>18.42</td><td>35.82</td><td>50.00</td><td>54.23</td><td>37.17</td></tr><tr><td>DriveAdapter* [27]</td><td>28.82</td><td>26.38</td><td>48.76</td><td>50.00</td><td>56.43</td><td>42.08</td></tr></table>

Expert feature distillation ofers important guidance. As pointed out in [49, 50], due to the high-dimensional input space of AD, i.e., multiple images and point clouds, E2E-AD methods tend to overfit. The features from expert, which already possesses strong driving knowledge, could be helpful to mitigate the issue by distillation. As a result, methods (TCP/ThinkTwice/DriveAdapter) with expert feature distillation outperforms those without (VAD/UniAD) by a large margin. From the comparison between TCP-traj with and without distillation, we could observe similar trend. However, in the real world setting, it could be dificult to obtain expert features, which worths further study.

Interactive behaviors are dificult to learn. All models’ scores of skills regarding strong interaction (Merging, Overtaking, and Emergency Brake) are unsatisfying. It might come from two perspectives: (I) Long-tail issue. Even though we ensure that the number of clips for diferent scenarios are similar, there are only a few frames within one clip are about interactive behaviors. As a result, it might be challenging for the learning. (II) Imitation learning paradigm. Direct supervised training of control signals or trajectories might fail to give guidance regarding the gaming, thinking, and reasoning process of interaction. More advanced training paradigms could be a promising direction.

![](images/6d1d85a86bd7880a89562dcd934dfe820bbfeec5e07e613651f9b01ea5cb772c.jpg)  
(a) nuScenes [21] dataset drawn by [24].

![](images/3ea0a494a5df2e7d385311076796c4585d468d8067395044f8058646c07bd958.jpg)  
(b) Bench2Drive Dataset  
Figure 5: Distribution of ego vehicle’s future location. Bench2Drive possesses more turning trajectories, indicating better action diversity and thus providing better training data and having less gap between open-loop and closed-loop evaluation.

## 4.3 Case Analysis

We conduct visualizations and upload the results to https://github.com/Thinklab-SJTU/ Bench2DriveZoo/blob/uniad/vad/analysis/analysis.md. For all five abilities, we choose some representative scenarios to visualize, where some baselines success and some baselines fail for the ease of comparison and analysis. We give the corresponding failure analysis so that the users and practioners could have a sense about the pros, cons, and future works of existing E2E-AD methods.

## 5 Conclusion

In this work, we present Bench2Drive, a new benchmark tailed for closed-loop evaluation of endto-end autonomous driving methods. We open source a fully-annotated large-scale dataset as the oficial training set and a multi-ability evaluation toolkit for the granular driving skill assessment. State-of-the-art E2E-AD methods are tested in Bench2Drive with their pros and cons evaluated, which provides insights for the future direction.

Limitations: Since the rendering of simulation in CARLA has gaps compared to real world, utilizing real world datasets could be complementary as done in the concurrent work - NAVSIM [65]. Actually, there is a dilemma in the field for the evaluation of end-to-end autonomous driving algorithms:

<table><tr><td>Source of Images</td><td>Pros</td><td>Cons</td></tr><tr><td>Real World Datasets Simulation Rendering</td><td>Realistic Reactive</td><td>Non-Reactive Cartoon Style</td></tr></table>

Generative models like difusion models [66] might have the potential to provide realistic and reactive rendering, with some pioneering works in the field [67–69]. However, the illusion and artifact issue of difusion requires further exploration.

Social Impact: The deployment ofAD systems holds immense potential to revolutionize transportation, but it also brings significant ethical and safety concerns. Bench2Drive could serve as a platform for rigorously validating the capabilities of AD systems in a controlled and simulated environment, helping to identify potential flaws before real-world deployment. One of the primary risks is the simulation-reality gap—the diference between how an AD system performs in simulation versus in the real world. Simulations have the dificulties to fully replicate the complexities and unpredictability of real-world driving conditions. There is a risk that an AD system might perform well in simulation but fail in real-world scenarios due to unmodeled factors like rare edge cases, unexpected human behaviors, or varying environmental conditions. Bench2Drive is intended to complement, not replace, real-world testing, and it is crucial to emphasize that simulation is one part of a broader validation process that must include extensive on-road testing.

## References

[1] Rishi Bommasani, Drew A Hudson, Ehsan Adeli, Russ Altman, Simran Arora, Sydney von Arx, Michael S Bernstein, Jeannette Bohg, Antoine Bosselut, Emma Brunskill, et al. On the opportunities and risks of foundation models. arXiv preprint arXiv:2108.07258, 2021. 1

[2] Team OpenAI. Gpt-4 technical report. 2023.

[3] Zhenjie Yang, Xiaosong Jia, Hongyang Li, and Junchi Yan. Llm4drive: A survey of large language models for autonomous driving. ArXiv, abs/2311.01043, 2023. 1

[4] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, et al. Planning-oriented autonomous driving. In CVPR, pages 17853–17862, 2023. 1, 2, 3, 4, 8, 9

[5] Penghao Wu, Xiaosong Jia, Li Chen, Junchi Yan, Hongyang Li, and Yu Qiao. Trajectory-guided control prediction for end-to-end autonomous driving: A simple yet strong baseline. NeurIPS, 35:6119–6132, 2022. 3, 4, 9

[6] Kashyap Chitta, Aditya Prakash, Bernhard Jaeger, Zehao Yu, Katrin Renz, and Andreas Geiger. Transfuser: Imitation with transformer-based sensor fusion for autonomous driving. TPAMI, 2023. 3, 4, 6

[7] Yinda Xu, Zeyu Wang, Zuoxin Li, Ye Yuan, and Gang Yu. Siamfc++: Towards robust and accurate visual tracking with target estimation guidelines. In AAAI, pages 12549–12556, 2020.

[8] Yinda Xu and Lidong Yu. Drl-based trajectory tracking for motion-related modules in autonomous driving. arXiv preprint arXiv:2308.15991, 2023. 1

[9] Hongyang Li, Chonghao Sima, Jifeng Dai, Wenhai Wang, Lewei Lu, Huĳie Wang, Jia Zeng, Zhiqi Li, Jiazhi Yang, Hanming Deng, Hao Tian, Enze Xie, Jiangwei Xie, Li Chen, Tianyu Li, Yang Li, Yulu Gao, Xiaosong Jia, Si Liu, Jianping Shi, Dahua Lin, and Yu Qiao. Delving into the devils of bird’s-eye-view perception: A review, evaluation and recipe. TPAMI, pages 1–20, 2023. 1

[10] Zhiqi Li, Wenhai Wang, Hongyang Li, Enze Xie, Chonghao Sima, Tong Lu, Yu Qiao, and Jifeng Dai. Bevformer: Learning bird’s-eye-view representation from multi-camera images via spatiotemporal transformers. ECCV, 2022. 8

[11] Zhĳian Liu, Haotian Tang, Alexander Amini, Xingyu Yang, Huizi Mao, Daniela Rus, and Song Han. Bevfusion: Multi-task multi-sensor fusion with unified bird’s-eye view representation. In ICRA, 2023.

[12] Xianliang Huang, Jiajie Gou, Shuhang Chen, Zhizhou Zhong, Jihong Guan, and Shuigeng Zhou. Iddr-ngp: Incorporating detectors for distractors removal with instant neural radiance field. In Proceedings ofthe 31st ACM International Conference on Multimedia, pages 1343–1351, 2023.

[13] Yutao Zhu, Xiaosong Jia, Xinyu Yang, and Junchi Yan. Flatfusion: Delving into details of sparse transformer-based camera-lidar fusion for autonomous driving, 2024. 1

[14] Xiaosong Jia, Liting Sun, Hang Zhao, Masayoshi Tomizuka, and Wei Zhan. Multi-agent trajectory prediction by combining egocentric and allocentric views. In CoRL, pages 1434–1443. PMLR, 2022. 2

[15] Xiaosong Jia, Li Chen, Penghao Wu, Jia Zeng, Junchi Yan, Hongyang Li, and Yu Qiao. Towards capturing the temporal dynamics for trajectory prediction: a coarse-to-fine approach. In CoRL, pages 910–920. PMLR, 2023.

[16] Xiaosong Jia, Penghao Wu, Li Chen, Yu Liu, Hongyang Li, and Junchi Yan. Hdgt: Heterogeneous driving graph transformer for multi-agent trajectory prediction via scene encoding. TPAMI, 2023.

[17] Xiaosong Jia, Shaoshuai Shi, Zĳun Chen, Li Jiang, Wenlong Liao, Tao He, and Junchi Yan. Amp: Autoregressive motion prediction revisited with next token prediction for autonomous driving. arXiv preprint arXiv:2403.13331, 2024. 2

[18] Xiaosong Jia, Liting Sun, Masayoshi Tomizuka, and Wei Zhan. Ide-net: Interactive driving event and pattern extraction from human data. IEEE RA-L, 6(2):3065–3072, 2021. 2

[19] Daniel Dauner, Marcel Hallgarten, Andreas Geiger, and Kashyap Chitta. Parting with misconceptions about learning-based vehicle motion planning. In CoRL, 2023. 2, 3, 9

[20] Yazhe Niu, Yuan Pu, Zhenjie Yang, Xueyan Li, Tong Zhou, Jiyuan Ren, Shuai Hu, Hongsheng Li, and Yu Liu. Lightzero: A unified benchmark for monte carlo tree search in general sequential decision scenarios. Advances in Neural Information Processing Systems, 36, 2024. 2

[21] Holger Caesar, Varun Bankiti, Alex H. Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beĳbom. nuscenes: A multimodal dataset for autonomous driving. In CVPR, 2020. 2, 3, 4, 5, 9, 10

[22] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. Vad: Vectorized scene representation for eficient autonomous driving. ICCV, 2023. 2, 3, 4, 8, 9

[23] Jiang-Tian Zhai, Ze Feng, Jihao Du, Yongqiang Mao, Jiang-Jiang Liu, Zichang Tan, Yifu Zhang, Xiaoqing Ye, and Jingdong Wang. Rethinking the open-loop evaluation of end-to-end autonomous driving in nuscenes. arXiv preprint arXiv:2305.10430, 2023. 2, 3, 8, 9

[24] Zhiqi Li, Zhiding Yu, Shiyi Lan, Jiahan Li, Jan Kautz, Tong Lu, and José M. Álvarez. Is ego status all you need for open-loop end-to-end autonomous driving? ArXiv, abs/2312.03031, 2023. 2, 3, 9, 10

[25] Stéphane Ross, Geofrey Gordon, and Drew Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In Proceedings of the fourteenth international conference on artificial intelligence and statistics, pages 627–635. JMLR Workshop and Conference Proceedings, 2011. 2, 9

[26] Pim De Haan, Dinesh Jayaraman, and Sergey Levine. Causal confusion in imitation learning. NeurIPS, 32, 2019. 2, 9

[27] Xiaosong Jia, Yulu Gao, Li Chen, Junchi Yan, Patrick Langechuan Liu, and Hongyang Li. Driveadapter: Breaking the coupling barrier of perception and planning in end-to-end autonomous driving. In ICCV, 2023. 2, 3, 5, 8, 9

[28] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. Carla: An open urban driving simulator. In CoRL, pages 1–16. PMLR, 2017. 2, 4, 6

[29] Dian Chen and Philipp Krähenbühl. Learning from all vehicles. In CVPR, pages 17222–17231, 2022. 2

[30] Xiaosong Jia, Penghao Wu, Li Chen, Jiangwei Xie, Conghui He, Junchi Yan, and Hongyang Li. Think twice before driving: Towards scalable decoders for end-to-end autonomous driving. In CVPR, 2023. 2, 3, 8, 9

[31] Qifeng Li, Xiaosong Jia, Shaobo Wang, and Junchi Yan. Think2drive: Eficient reinforcement learning by thinking in latent world model for quasi-realistic autonomous driving (in carla-v2). arXiv preprint arXiv:2402.16720, 2024. 2, 4, 5

[32] Andreas Geiger, Philip Lenz, and Raquel Urtasun. Are we ready for autonomous driving? the kitti vision benchmark suite. In CVPR, 2012. 3, 4

[33] Robert Krajewski, Julian Bock, Laurent Kloeker, and Lutz Eckstein. The highd dataset: A drone dataset of naturalistic vehicle trajectories on german highways for validation of highly automated driving systems. In ITSC, pages 2118–2125. IEEE, 2018. 3

[34] Julian Bernhard, Klemens Esterle, Patrick Hart, and Tobias Kessler. Bark: Open behavior benchmarking in multi-agent environments. In 2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 6201–6208. IEEE, 2020. 3

[35] Benjamin Wilson, William Qi, Tanmay Agarwal, John Lambert, Jagjeet Singh, Siddhesh Khandelwal, Bowen Pan, Ratnesh Kumar, Andrew Hartnett, Jhony Kaesemodel Pontes, Deva Ramanan, Peter Carr, and James Hays. Argoverse 2: Next generation datasets for self-driving perception and forecasting. In NeurIPS Datasets and Benchmarks, 2021. 3, 4

[36] Pei Sun, Henrik Kretzschmar, Xerxes Dotiwalla, Aurelien Chouard, Vĳaysai Patnaik, Paul Tsui, James Guo, Yin Zhou, Yuning Chai, Benjamin Caine, et al. Scalability in perception for autonomous driving: Waymo open dataset. In CVPR, pages 2446–2454, 2020. 3, 4

[37] Cole Gulino, Justin Fu, Wenjie Luo, George Tucker, Eli Bronstein, Yiren Lu, Jean Harb, Xinlei Pan, Yan Wang, Xiangyu Chen, et al. Waymax: An accelerated, data-driven simulator for large-scale autonomous driving research. NeurIPS, 36, 2024. 3, 4, 6

[38] Napat Karnchanachari, Dimitris Geromichalos, Kok Seang Tan, Nanxiang Li, Christopher Eriksen, Shakiba Yaghoubi, Noushin Mehdipour, Gianmarco Bernasconi, Whye Kit Fong, Yiluan Guo, et al. Towards learning-based planning: The nuplan benchmark for real-world autonomous driving. arXiv preprint arXiv:2403.04133, 2024. 3, 4, 6, 7

[39] Runze Liu, Fengshuo Bai, Yali Du, and Yaodong Yang. Meta-reward-net: Implicitly diferentiable reward learning for preference-based reinforcement learning. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh, editors, Advances in Neural Information Processing Systems, volume 35, pages 22270–22284. Curran Associates, Inc., 2022.

[40] Fengshuo Bai, Hongming Zhang, Tianyang Tao, Zhiheng Wu, Yanna Wang, and Bo Xu. Picor: Multi-task deep reinforcement learning with policy correction. Proceedings of the AAAI Conference on Artificial Intelligence, 37(6):6728–6736, Jun. 2023.

[41] Fengshuo Bai, Rui Zhao, Hongming Zhang, Sĳia Cui, Ying Wen, Yaodong Yang, Bo Xu, and Lei Han. Eficient preference-based reinforcement learning via aligned experience estimation. arXiv preprint arXiv:2405.18688, 2024. 3

[42] Katrin Renz, Kashyap Chitta, Otniel-Bogdan Mercea, A. Sophia Koepke, Zeynep Akata, and Andreas Geiger. Plant: explainable planning transformers via object-level representations. In CoRL, 2022. 4

[43] Bernhard Jaeger, Kashyap Chitta, and Andreas Geiger. Hidden biases of end-to-end driving models. In ICCV, 2023. 4, 16

[44] Dean A Pomerleau. Alvinn: An autonomous land vehicle in a neural network. NeurIPS, 1, 1988. 4

[45] Ashish Vaswani, Noam M. Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukas Kaiser, and Illia Polosukhin. Attention is all you need. In NeurIPS, 2017. 4

[46] Felipe Codevilla, Matthias Müller, Antonio López, Vladlen Koltun, and Alexey Dosovitskiy. End-to-end driving via conditional imitation learning. In ICRA, pages 4693–4700, 2018. 4

[47] Felipe Codevilla, Eder Santana, Antonio M López, and Adrien Gaidon. Exploring the limitations of behavior cloning for autonomous driving. In CVPR, pages 9329–9338, 2019.

[48] Marin Toromanof, Emilie Wirbel, and Fabien Moutarde. End-to-end model-free reinforcement learning for urban driving using implicit afordances. In CVPR, pages 7153–7162, 2020.

[49] Dian Chen, Brady Zhou, Vladlen Koltun, and Philipp Krähenbühl. Learning by cheating. In CoRL, pages 66–75. PMLR, 2020. 5, 9

[50] Zhejun Zhang, Alexander Liniger, Dengxin Dai, Fisher Yu, and Luc Van Gool. End-to-end urban driving by imitating a reinforcement learning coach. In ICCV, 2021. 4, 9

[51] Shengchao Hu, Li Chen, Penghao Wu, Hongyang Li, Junchi Yan, and Dacheng Tao. St-p3: End-to-end vision-based autonomous driving via spatial-temporal feature learning. In ECCV, 2022. 4

[52] Han Lu, Xiaosong Jia, Yichen Xie, Wenlong Liao, Xiaokang Yang, and Junchi Yan. Activead: Planningoriented active learning for end-to-end autonomous driving, 2024. 4

[53] Kashyap Chitta, Aditya Prakash, and Andreas Geiger. Neat: Neural attention fields for end-to-end autonomous driving. In ICCV, pages 15793–15803, 2021. 4

[54] Aditya Prakash, Kashyap Chitta, and Andreas Geiger. Multi-modal fusion transformer for end-to-end autonomous driving. In CVPR, 2021. 4

[55] Penghao Wu, Li Chen, Hongyang Li, Xiaosong Jia, Junchi Yan, and Yu Qiao. Policy pre-training for autonomous driving via self-supervised geometric modeling. In ICLR, 2023. 4

[56] Dian Chen and Philipp Krähenbühl. Learning from all vehicles. In CVPR, 2022. 4

[57] Hao Shao, Letian Wang, RuoBing Chen, Hongsheng Li, and Yu Liu. Safety-enhanced autonomous driving using interpretable sensor fusion transformer. CoRL, 2022. 4

[58] Anthony Hu, Gianluca Corrado, Nicolas Grifiths, Zak Murez, Corina Gurau, Hudson Yeo, Alex Kendall, Roberto Cipolla, and Jamie Shotton. Model-based imitation learning for urban driving. NeurIPS, 2022.

[59] Qingwen Zhang, Mingkai Tang, Ruoyu Geng, Feiyi Chen, Ren Xin, and Lujia Wang. Mmfn: multi-modalfusion-net for end-to-end driving. IROS, 2022.

[60] Jimuyang Zhang, Zanming Huang, and Eshed Ohn-Bar. Coaching a teachable student. In CVPR, 2023. 4, 5

[61] Jens Beißwenger. PDM-Lite: A rule-based planner for carla leaderboard 2.0. https://github.com/ OpenDriveLab/DriveLM/blob/DriveLM-CARLA/docs/report.pdf, 2024. 4

[62] Ashesh Jain, Luca Del Pero, Hugo Grimmett, and Peter Ondruska. Autonomy 2.0: Why is self-driving always 5 years away? arXiv preprint arXiv:2107.08142, 2021. 5

[63] Petru Soviany, Radu Tudor Ionescu, Paolo Rota, and Nicu Sebe. Curriculum learning: A survey, 2022. 5

[64] Penghao Wu, Xiaosong Jia, Li Chen, Junchi Yan, Hongyang Li, and Yu Qiao. Trajectory-guided control prediction for end-to-end autonomous driving: A simple yet strong baseline. In NeurIPS, 2022. 8

[65] Daniel Dauner, Marcel Hallgarten, Tianyu Li, Xinshuo Weng, Zhiyu Huang, Zetong Yang, Hongyang Li, Igor Gilitschenski, Boris Ivanovic, Marco Pavone, Andreas Geiger, and Kashyap Chitta. Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking. arXiv, 2406.15349, 2024. 10

[66] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising difusion probabilistic models. Advances in neural information processing systems, 33:6840–6851, 2020. 10

[67] Jiazhi Yang, Shenyuan Gao, Yihang Qiu, Li Chen, Tianyu Li, Bo Dai, Kashyap Chitta, Penghao Wu, Jia Zeng, Ping Luo, Jun Zhang, Andreas Geiger, Yu Qiao, and Hongyang Li. Generalized predictive model for autonomous driving. In Proceedings ofthe IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2024. 10

[68] Shenyuan Gao, Jiazhi Yang, Li Chen, Kashyap Chitta, Yihang Qiu, Andreas Geiger, Jun Zhang, and Hongyang Li. Vista: A generalizable driving world model with high fidelity and versatile controllability. In Advances in Neural Information Processing Systems (NeurIPS), 2024.

[69] Yunsong Zhou, Michael Simon, Zhenghao Peng, Sicheng Mo, Hongzi Zhu, Minyi Guo, and Bolei Zhou. Simgen: Simulator-conditioned driving scene generation. arXiv preprint arXiv:2406.09386, 2024. 10

## Checklist

The checklist follows the references. Please read the checklist guidelines carefully for information on how to answer these questions. For each question, change the default [TODO] to [Yes] , [No] , or [N/A] . You are strongly encouraged to include a justification to your answer, either by referencing the appropriate section of your paper or providing a brief inline description. For example:

## • Did you include the license to the code and datasets? [Yes] See Section 3.

Please do not modify the questions and only use the provided macros for your answers. Note that the Checklist section does not count towards the page limit. In your paper, please delete this instructions block and only keep the Checklist section heading above along with the questions/answers below.

1. For all authors...

(a) Do the main claims made in the abstract and introduction accurately reflect the paper’s contributions and scope? [Yes]

(b) Did you describe the limitations of your work? [Yes]

(c) Did you discuss any potential negative societal impacts of your work? [Yes]

(d) Have you read the ethics review guidelines and ensured that your paper conforms to them? [Yes]

2. If you are including theoretical results...

(a) Did you state the full set of assumptions of all theoretical results? [N/A]

(b) Did you include complete proofs of all theoretical results? [N/A]

3. If you ran experiments (e.g. for benchmarks)...

(a) Did you include the code, data, and instructions needed to reproduce the main experimental results (either in the supplemental material or as a URL)? [Yes]

(b) Did you specify all the training details (e.g., data splits, hyperparameters, how they were chosen)? [Yes]

(c) Did you report error bars (e.g., with respect to the random seed after running experiments multiple times)? [No]

(d) Did you include the total amount of compute and the type of resources used (e.g., type of GPUs, internal cluster, or cloud provider)? [Yes]

4. If you are using existing assets (e.g., code, data, models) or curating/releasing new assets...

(a) If your work uses existing assets, did you cite the creators? [Yes]

(b) Did you mention the license of the assets? [Yes]

(c) Did you include any new assets either in the supplemental material or as a URL? [Yes]

(d) Did you discuss whether and how consent was obtained from people whose data you’re using/curating? [N/A]

(e) Did you discuss whether the data you are using/curating contains personally identifiable information or ofensive content? [N/A]

5. If you used crowdsourcing or conducted research with human subjects...

(a) Did you include the full text of instructions given to participants and screenshots, if applicable? [N/A]

(b) Did you describe any potential participant risks, with links to Institutional Review Board (IRB) approvals, if applicable? [N/A]

(c) Did you include the estimated hourly wage paid to participants and the total amount spent on participant compensation? [N/A]

## A Details of Data Collecting

The collection of data is a mix of automatic pipelines and manual checking. We give details below:

Route: We use the expert model Think2Drive to run on the predefined route files and only keep those without infractions. We design a traversal algorithm over all maps to determine whether a scenario could be triggered, aiming to cover towns as much as possible. The balance of weather, towns, and scenarios are ensured by manually checking. The behaviors and rendering of CARLA sometimes could be buggy as shown in Fig. 7 and we manually filter those bad clips.

Annotations: We utilize CARLA’s oficial APIs to collect annotations. Notably, there are several bugs within the APIs: (I) All pedestrians’ speed value are 0 from the API. We manually calculate their speed by diferentiating during training of baseline methods. (II) The returned value of Speedometer and IMU could be None. We pad these values with 0 during training. (III) Some stop signs in CARLA are on the ground and thus there is no bounding box. To compensate this, We record all stop signs with rectangles to denote their trigger volume. (IV) Some static vehicles’ rotation and location are wrong by API. Thus, we use the correct center and extent to obtain their 3D bounding boxes.

Object Class: Considering diferent attributes of diferent objects, we categorize all objects into four main types and store them group by group: Vehicle, Trafic Sign, Trafic Light, and Pedestrian. Vehicles are further subdivided into static and dynamic vehicles. Static vehicles remain stationary throughout the entire scenario and are distinguished by a unique actor identifier obtained from "static.prop.mesh". For Trafic Signs, they consist of speed\_limit\_sign, stop\_sign, yield\_sign, warning\_sign (including warning construction, trafic warning, and warning accident), dirt\_debris, and cone. Notably, signs involving trigger\_volume, such as speed\_limit\_sign, stop\_sign, and yield\_sign, has trigger volume where we store the rectangle as well. The coordinates for warning signs and cones are obtained from the center and extent of their actor class, while dirt\_debris requires additional conversion due to inaccurate coordinates. For Trafic Lights, the trigger volume coordinates for trafic signs and lights are relative to the actor, which requires extra transformation. Each trafic sign/light consists of two parts: the pole and the light/sign itself while the bounding boxes from API is only the lights/signs.

Coordinate System: Unlike the Y-down right-hand system used by Nuscenes, CARLA employs the Unreal Engine coordinate system, which is a Z-up left-hand coordinate system. In Compass, orientation with regard to the North ([0.0, -1.0, 0.0] in Unreal Engine) means the standard yaw angle in the left-hand system is theta in the compass minus 1/2 pi. In rare cases, this may result in NaN values, which need to be manually filtered.

Map Information: The HD-Map is organized into road\_ids with lane\_index. Each lane includes the world coordinates and orientations of points, lane type, color identifiers and adjacent road\_ids-lane\_ids (left, right and connected road ids and lane ids), as well as topological structures (e.g., ’Junction’, ’Normal’, ’EnterNormal’, ’EnterJunction’, ’PassNormal’, ’PassJunction’, ’StartJunctionMultiChange’, or ’StartNormalMultiChange’). The Trigger\_Volumes represent the trigger areas for signs, where ’Points’ specify the vertices’ locations of the trigger volume, ’Type’ can be ’StopSign’ or ’TraficLight’, and ’ParentActor\_Location’ provides details on the location of the parent actor associated with the trigger volume.

![](images/58de691b3319ef58b3872ef2ab223a0a43abb97c1ad5f7f09aef8062248386b9.jpg)  
Figure 6: Scenario Distribution of Bench2Drive Dataset

Data Compression To reduce file size, following [43], we adopted compressed data format. Images are compressed using JPG with the quality= 20. To avoid train-val gap during closed-loop evaluation, we also use in-memory JPG compression and decompression during inference. Semantic segmentation and depth data are stored as PNG files. We use a specialized algorithm called laszip to compress our LiDAR point clouds. JSON files are compressed using GZIP.

## B Distribution of Scenarios, Towns and Weathers

As shown in Fig. 8, the distribution of weathers are nearly uniform while the distribution of town is dominated by Town12 and Town13. The imbalance comes from two perspectives: (I) New towns, like Town12 and Town13, are designed on purpose by CARLA team to be much larger than old towns so that the community could explore applications in city-level scene. Thus, we collect more data in larger towns for more diverse landscapes. (II) Lots of new scenarios in Leaderboard v2 are designed recently and thus old towns do not support the layouts required by new scenarios. For example, parting exit requires the existence of other parked vehicles. As a result, we have to collect more data in new towns to ensure the balance of scenario types.

![](images/3c17281772ead66b330a0e41db5227439d61c0533df06128d77a0bbc3b1e4cf5.jpg)  
Figure 7: Bugged Rendering of CARLA.

![](images/079675c29c4fd63f4589a1e5123d93055ced451af1e4ac1f7755ddc87f10bf45.jpg)  
Figure 8: Town and Weather Distribution of Bench2Drive Dataset

## C Implementation Details of Baselines

For all baseline E2E-AD methods, we strictly follow their oficial open-sourced code, environments, and configs. There are a few modifications: (I) For methods with object detection module, we change the detection classes according to CARLA<sup>3</sup>. (II) Data collection of Bench2Drive is in 10Hz while nuScenes with bounding boxes is in 2Hz. Due to Bench2Drive’s longer clips, Bench2Drive-base has approximately 10x frames compared to nuScenes yet with higher redundancy. For computationally demanding methods like UniAD/VAD/ThinkTwice/DriveAdapter, we train <sup>1</sup> epochs compared to the original version. We observe similar level of loss due to similar number of training steps. (III) Since ThinkTwice and DriveAdapter require expert’s BEV features, we use Think2Drive expert to regenerate those expert feature. Additionally, for fair comparison with other methods, we modify both of them into 6 cameras without LiDAR.

## D Training and Evaluation Resource Requirements

We report resource requirements of training and evaluating baselines. Note that the evaluation time could be linearly speed up with more GPUs to parallely evaluate on more routes.

Table 5: Resource requirements for training on base set and evaluation on 220 routes. The training of UniAD consists of BEVFormer, stage1, and stage2.
<table><tr><td></td><td>Training</td><td>Evaluation</td></tr><tr><td>AD-MLP</td><td>1 A600 * 1 day</td><td>4 A6000 * 6 hours</td></tr><tr><td>TCP</td><td> $1 \mathrm { A 6 0 0 } * 1 \mathrm { d a y }$ </td><td>4 A6000 * 6 hours</td></tr><tr><td>VAD</td><td>8H800 *5 days</td><td>8 H800 * 2 days</td></tr><tr><td>UniAD-base</td><td>8 H800 * (3+3+3)=9 days</td><td>8 H800 * 2 days</td></tr></table>

## E Behavior Model of NPC Agents

In CARLA, three behavior types are preset in CARLA Agent: cautious, normal and aggressive. These behavior types govern the driving actions of NPCs, influencing factors such as speed, responses to other vehicles, and safety protocols. The key parameters for each behavior mode include:

• max\_speed: Sets the maximum speed(km/h) that an NPC vehicle can reach.

• speed\_lim\_dist: Value in km/h that defines how far your vehicle’s target speed will be from the current speed limit

• speed\_decrease: Controls the deceleration of the NPC when approaching a slower vehicle ahead.

• safety\_time: Estimates the time to a collision if the vehicle in front suddenly brakes.

• min\_proximity\_threshold: Defines the minimum distance before the NPC takes actions such as evasive maneuvers or tailgating.

• braking\_distance: The distance at which the NPC performs an emergency stop to avoid a collision.

• tailgate\_counter: A counter that prevents the NPC from initiating a new tailgating action too soon after the last one.

These behavior designs interact with the ego (self-driving) vehicle, ensuring that NPCs respond to the presence and actions of the ego vehicle in the simulation. The parameters for diferent behavior styles are as follows,

Table 6: Comparison of Cautious, Normal, and Aggressive behavior parameters.
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Cautious</td><td rowspan=1 colspan=1>Normal</td><td rowspan=1 colspan=1>Aggressive</td></tr><tr><td rowspan=1 colspan=1>max_speed (km/h)</td><td rowspan=1 colspan=1>40</td><td rowspan=1 colspan=1>50</td><td rowspan=1 colspan=1>70</td></tr><tr><td rowspan=1 colspan=1>speed_lim_dist (km/h)</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>speed_decrease (km/h)</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>8</td></tr><tr><td rowspan=1 colspan=1>safety_time (seconds)</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>min_proximity_threshold (meters)</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>8</td></tr><tr><td rowspan=1 colspan=1>braking_distance (meters)</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=1>tailgate_counter (times)</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>-1</td></tr></table>

The rule-based behavior decision algorithm in behavior\_agent.py for non-player character (NPC) vehicles is shown below:

The behavior of walkers/pedestrians is characterized by their consistent adherence to the route line at a constant speed, with the inability to walk backward. In autonomous driving scenarios, pedestrian safety is of utmost importance. Pedestrians have the highest priority when autonomous vehicles interact with humans, and autonomous vehicles should learn to give way to pedestrians regardless of trafic conditions.

## F Details about Infraction Score

In Table 7, we gives the penalty score of each infraction designed by Leaderboard v2.

Algorithm 1 Non-Player Character (NPC) Vehicles Behavior Decision   
1: Update vehicle’s surrounding information   
2: if red light or stop sign detected then   
3: return emergency\_stop()   
4: end if   
5: if pedestrian detected and within braking distance then   
6: return emergency\_stop()   
7: end if   
8: if other vehicle nearby then   
9: if within braking distance then   
10: return emergency\_stop()   
11: else   
12: return car\_following()   
13: end if   
14: else if ego vehicle at intersection and (turn left or turn right) then   
15: adjust\_speed\_limit()   
16: return PID\_Control   
17: else if in normal driving conditions then   
18: maintain\_speed\_limit()   
19: return PID\_Control   
20: end if

Table 7: Infraction Types & Penalty. Following https://leaderboard.carla.org/.
<table><tr><td>Infraction</td><td>Penalty Note</td><td></td></tr><tr><td>Pedestrian Collision</td><td>0.50</td><td>Punished every infraction.</td></tr><tr><td>Vehicles Collision</td><td>0.60</td><td>Punished every infraction.</td></tr><tr><td>Other Collision</td><td>0.65</td><td>Punished every infraction.</td></tr><tr><td>Running Red Light</td><td>0.70</td><td>Punished every infraction.</td></tr><tr><td>Scenario Timeout</td><td>0.70</td><td>Fail to pass certain scenarios in 4 minutes.</td></tr><tr><td>Too Slow</td><td>0.70</td><td>Fail to maintain a suitable speed with surrounding vehicle.</td></tr><tr><td>No Give Way</td><td>0.70</td><td>Failure to yield to emergency vehicle.</td></tr><tr><td>Off-road</td><td></td><td>Not considered in route completion.</td></tr><tr><td>Route Deviation</td><td></td><td>Deviates more than 30 meters. Shutdown immediately.</td></tr><tr><td>Agent Blocked</td><td></td><td>No action for 180 seconds. Shutdown immediately.</td></tr><tr><td>Route Timeout</td><td></td><td>Exceed the maximum time limit. Shutdown immediately.</td></tr></table>

## G Description of Scenarios

Bench2Drive provides 44 corner scenarios, extended from CARLA Leaderboard V2. We give details about them below:

## 1. ControlLoss

![](images/437fa18b8fc20a9b72c802b0624f036e51a485240f52f5de42508dbde24d97f0.jpg)

The ego vehicle loses control due to bad conditions on the road and it must recover, coming back to its original lane.

## 2. ParkingExit

![](images/60832b384b31f727c501467a552e327c49c55008f39255d8fd9c38b818251df9.jpg)

The ego vehicle must exit a parallel parking bay into a flow of trafic.

## 3. ParkingCutIn

![](images/712ffb813c67e8f433a5113d9abd30a19c98967c93d5512a72c5d1af27eee852.jpg)

## 4. StaticCutIn

![](images/9652900c1149f3f7d906071694d1f1175982adccfd7729945e55f6a9417d1d94.jpg)

## 5. ParkedObstacle

The ego vehicle must slow down or brake to allow a parked vehicle exiting a parallel parking bay to cut in front.

![](images/1e34c684a59b5e04a2c02ea38738327ebde20cc4f9f2beb6bea9c9eb8d333fe9.jpg)

## 6. ParkedObstacleTwoWays

The ego vehicle must slow down or brake to allow a vehicle of the slow trafic flow in the adjacent lane to cut in front. Compared to ParkingCutIn, there are more cars in the adjacent lane and any one of them may cut in.

![](images/f6da67a1822c9a9a469fa8a1dc89cbe5e1c94449b126ba0774c30b40d752fb25.jpg)

The ego vehicle encounters a parked vehicle blocking part of the lane and must perform a lane change into trafic moving in the same direction to avoid it.

## 7. Construction

![](images/ee473e2db7d9137d5be5ce06d7eff05a9aa2574ba4b41056cd52780c2c0056c1.jpg)

## 9. Accident

![](images/c708d952da86da0e9272b93437950a948049d654d619af223283f739be26853f.jpg)

10. AccidentTwoWays

## 8. ConstructionTwoWays

The ’TwoWays’ version of ParkedObstacle. The ego vehicle encounters a parked vehicle blocking the lane and must perform a lane change into trafic moving in the opposite direction to avoid it.

![](images/4972f12f220b7a657e2942b9c29b7d7b46a0272e3e6c1c371b52ca3ac4c7dd8b.jpg)

![](images/b7d273f47d59bcd8823ec1b55acf3c41e1aabf0ba75c131264dec0b2da9b6a3c.jpg)

The ego vehicle encounters a construction site blocking and must perform a lane change into trafic moving in the same direction to avoid it. Compared to ParkedObstacle, the construction occupies more width of the lane. The ego vehicle has to completely deviate from its task route temporarily to bypass the construction zone.

The ’TwoWays’ version of Construction.

The ego vehicle encounters multiple accident cars blocking part of the lane and must perform a lane change into trafic moving in the same direction to avoid it. Compared to ParkedObstacle and Construction, these accident cars occupy more length along the lane. The ego vehicle has to completely deviate from its task route for a longer time to bypass the accident zone.

The ’TwoWays’ version of Accident. Compared to ParkedObstacleTwoWays and ConstructionTwoWays, there is a much shorter time window for the ego vehicle to bypass the route obstacles (i.g. accident cars).

## 11. HazardAtSideLane

![](images/ffd6103bbcb4c44be0a4240d8f7a1a89233284a85e535b30771663c1f6191989.jpg)

The ego vehicle encounters a slow-moving hazard blocking part of the lane. The ego vehicle must brake or maneuver next to a lane of trafic moving in the same direction to avoid it.

## 12. HazardAtSideLaneTwoWays

![](images/5a19373663e1597ed9d490151fc72620245393438c8b103b507f5db41c7a85a6.jpg)

The ego vehicle encounters a slow-moving hazard blocking part of the lane. The ego vehicle must brake or maneuver to avoid it next to a lane of trafic moving in the opposite direction.

## 13. VehiclesDooropenTwoWays

![](images/826d7e74e68380d3fa767d04fdc87be26fabc27955b34c49198711d8370988a6.jpg)

The ego vehicle encounters a parked vehicle opening a door into its lane and must maneuver to avoid it.

## 14. DynamicObjectCrossing

![](images/b41dd933ed55ac390045fb476b1c0bf57825ad3cc85a769ba69bdad9f8e3e097.jpg)

A walker or bicycle behind a static prop crosses the road suddenly when the ego vehicle is close to the prop. The ego vehicle must make a hard brake promptly.

## 15. ParkingCrossingPedestrian

![](images/307e5ec954a2dfda8e58d21e5326f55c7ceba3bb5471422b9a419ea7725ff8a6.jpg)

The ego vehicle encounters a pedestrian emerging from behind a parked vehicle and advancing into the lane. The ego vehicle must brake or maneuver to avoid it. Compared to DynamicObjectCrossing, the pedestrian is closer to the road and the ego vehicle has to act more timely.

## 16. HardBrake

![](images/a292e510105438689363bb35cb065a9db2921693a2e8ae9bdb839b11941a7baf.jpg)

The leading vehicle decelerates suddenly and the ego vehicle must perform an emergency brake or an avoidance maneuver.

## 17. YieldToEmergencyVehicle

![](images/28ba80029206d0801ba06927fbb59912a154b57af84625fb3e7ae62a8918a4ad.jpg)

## 18. InvadingTurn

The ego vehicle is approached by an emergency vehicle coming from behind. The ego vehicle must maneuver to allow the emergency vehicle to pass.

![](images/82f9361ff13ed460c8c158472165232db34b0d84e8ec36b4a4dd045f115bff04.jpg)

When the ego vehicle is about to turn right, a vehicle coming from the opposite lane invades the ego’s lane, forcing the ego to move right to avoid a possible collision.

## 19. PedestrainCrossing

![](images/9da399474e5ce4c4018a80138b7cb82fd6e98ed8b874fd960cabdb5c393f7f9f.jpg)

While the ego vehicle is entering a junction, a group of natural pedestrians suddenly cross the road and ignore the trafic light. The ego vehicle must stop and wait for all pedestrians to pass even though there is a green trafic light or a clear junction.

## 20. VehicleTurningRoutePedestrian

![](images/ae23f9d9319ae2aeb26aeb7cbfb88b11fc2d3d137a3183e47d0a3b1228d651f8.jpg)

While performing a maneuver, the ego vehicle encounters a pedestrian crossing the road and must perform an emergency brake or an avoidance maneuver.

21. VehicleTurningRoute While performing a maneuver, the ego vehicle encounters a bicycle crossing the road and must perform an emergency brake or an avoidance maneuver. Compared to VehicleTurningRoutePedestrian, the bicycle moves faster and the ego has to brake earlier.

## 22. BlockedIntersection

![](images/f27379878d82bf7385bea3b34480139c72b14cf3ef3524c3559e432f615bc4f3.jpg)

While performing a maneuver, the ego vehicle encounters a stopped vehicle on the road and must perform an emergency brake or an avoidance maneuver.

## 23. SignalizedJunctionLeftTurn

![](images/5ff0cedfa78cceda437b9a04f3a1368a95ea850dbd817f0c34f875ee4baca7f4.jpg)

The ego vehicle is performing an unprotected left turn at an intersection, yielding to oncoming trafic.

## 24. SignalizedJunctionLeftTurnEnterFlow

The ego vehicle is performing an unprotected left turn at an intersection, merging into opposite trafic.

25. NonSignalizedJunctionLeftTurn

![](images/5287475369644963506c257790ac59f3ceae0e33764f8407c05502df23a25b44.jpg)

Non-signalized version of SignalizedJunctionLeftTurn. The ego has to negotiate with the opposite vehicles without trafic lights.

26. NonSignalizedJunctionLeftTurnEnterFlow

Non-signalized version of SignalizedJunctionLeftTurnEnterFlow.

27. SignalizedJunctionRightTurn

![](images/dd9c9ecda69275efaf2d88b5d07d7d23f339bd1d608b9e6c832be37980a954de.jpg)

The ego vehicle is turning right at an intersection and has to safely merge into the trafic flow coming from its left.

## 28. NonSignalizedJunctionRightTurn

Non-signalized version of SignalizedJunctionRightTurn. The ego has to negotiate with the trafic flow without trafic lights.

## 29. EnterActorFlows

![](images/aded4e6dd93d555c355af88ae1ef6927974bc0217093ffc9c680e69cd3da1dce.jpg)

30. HighwayExit

A flow of cars runs a red light in front of the ego when it enters the junction, forcing it to react (interrupting the flow or merging into the flow). These vehicles are ’special’ ones such as police cars, ambulances, or firetrucks.

![](images/c9a91a4ab6c012f9bfa2e3b934500a8d6623f150554c780459cdd88d3c603c9b.jpg)

The ego vehicle must cross a lane of moving trafic to exit the highway at an of-ramp.

31. MergerIntoSlowTrafic

![](images/fe7dd3a91214a605b8b5a4b455e8467a4f485cc59223e843918fa3db4e10fb76.jpg)

The ego vehicle must merge into a slow trafic flow on the of-ramp when exiting the highway.

32. MergerIntoSlowTraficV2

![](images/f9a773187a2770c9fe65b9b28ee96ee421bb0ea33ce988f203cd395db63cb2dd.jpg)

The ego vehicle must merge into a slow trafic flow coming from the on-ramp when driving on highway roads.

33. InterurbanActorFlow

![](images/366089169c04d5f12031b77739bd949b7c310d947e226a372cedfb9beaa5745d.jpg)

The ego vehicle leaves the interurban road by turning left, crossing a fast trafic flow.

## 34. InterurbanAdvancedActorFlow

![](images/d980fa455e71a99341a8e0a157163e9fe86ac10b0945ff9deac23ef7aab46769.jpg)

The ego vehicle incorporates into the interurban road by turning left, first crossing a fast trafic flow, and then merging into another one.

## 35. HighwayCutIn

![](images/1ac432bb25113cf7f0ed29039b5e2890e88b26e4836879aec4e6a66f0f0a012a.jpg)

36. CrossingBicycleFlow

![](images/d81aa4f4963bf63a304541e219dc631d545b1fca03ab6cd1f2530460538d8579.jpg)

37. OppositeVehicleRunningRedLight

![](images/e2a6bdaa80bc0e12966de101c103ff9e13433ede8342bf0949e152415a0c571c.jpg)

38. OppositeVehicleTakingPriority

![](images/dc110101fddaacf2828b7662ba0141aca266a334bfa392e30a737c85d1d3f363.jpg)

39. VinillaNonSignalizedTurn

![](images/a4743c735b72f4fa74ca142c778eb91d59e8ab64cfcab695acdbdbb1b223c7c5.jpg)

The ego vehicle needs to perform a turn at an intersection yielding to bicycles crossing from either the left.

The ego vehicle is going straight at an intersection but a crossing vehicle runs a red light, forcing the ego vehicle to avoid the collision.

![](images/20d14556fb6ec34841046771012fd9bf92d1a1210ae649316d4f33fa0e11b218.jpg)

40. VinillaNonSignalizedTurnEncounterStopsign

Non-signalized version of OppositeVehicleTakingPriority.

A basic scenario for the ego vehicle to learn to pass through a non-signalized junction (without trafic signs and trafic lights).

![](images/152684395bf1ed04296b9f61dd2be2958dcbd72e44a72b79d94c0f83a1b1ca5d.jpg)  
43. LaneChange

The ego vehicle encounters a vehicle merging into its lane from a highway on-ramp. The ego vehicle must decelerate, brake, or change lanes to avoid a collision.

![](images/f659d0ae74c4f83052629adb76fb1dc47b90ae2de10f5b43d704fc043af89502.jpg)

41. VinillaSignalizedTurnEncounterGreenLight

A basic scenario for the ego vehicle to learn to stop and start at stop signs.

42. VinillaSignalizedTurnEncounterRedLight

A basic scenario for the ego vehicle to learn to pass through the signalized junction.

A basic scenario for the ego vehicle to learn to pass through the signalized junction when the trafic light changes from red to green.

![](images/b6e9d4ec6632a20b094b324a98976db106d5db68dab541216d99e6271923bd3e.jpg)

A basic scenario for the ego vehicle to learn to change lanes and avoid collision.

44. TJunction  
![](images/42bc5f597939a8d6169c1135527dc52fc098c9c7f4b8ee8dd524587178649fd4.jpg)

A basic scenario for the ego vehicle to learn to pass through a T-junction.

## H Author Statement

We bear all responsibility in case of violation of rights, etc., and confirm the license of data, codes, and checkpoints as in Sec. 3.

## I License

All data, codes, and checkpoints are in GitHub and Huggingface under Apache License 2.0.

## J Datasheet

## J.1 Motivation

For what purpose was the dataset created? Was there a specific task in mind? Was there a specific gap that needed to be filled? Please provide a description. We build the benchmark to fulfill the need of comprehensive and realistic testing environments for Full Self-Driving (FSD). The primary task is end-to-end autonomous driving. Existing benchmarks failed to provide a closed-loop granular assessment of driving skills for E2E-AD methods.

Who created the dataset (e.g., which team, research group) and on behalf of which entity (e.g., company, institution, organization)? This dataset is curated by Xiaosong Jia, Zhenjie Yang, Qifeng Li, Zhiyuan Zhang, Junchi Yan from ReThinkLab with School of AI and Department of CSE, Shanghai Jiao Tong University.

## J.2 Distribution

Will the dataset be distributed to third parties outside of the entity (e.g., company, institution, organization) on behalf of which the dataset was created? Yes.

How will the dataset be distributed (e.g., tarball on website, API, GitHub)? All data, codes, and checkpoints are in GitHub (https://github.com/Thinklab-SJTU/Bench2Drive) and Huggingface (https://huggingface.co/datasets/rethinlab/Bench2Drive).

## J.3 Maintenance

Who will be supporting/hosting/maintaining the dataset? All authors and potentially new members of ReThinLab in Shanghai Jiao Tong University led by Prof. Junchi Yan.

How can the owner/curator/manager of the dataset be contacted (e.g., email address)? Please contact Xiasong Jia (jiaxiaosong@sjtu.edu.cn) and Junchi Yan (yanjunchi@sjtu.edu.cn).

Is there an erratum? No erratum as of submission.

Will the dataset be updated (e.g., to correct labeling errors, add new instances, delete instances)? Yes, we will maintain the dataset.

Will older versions of the dataset continue to be supported/hosted/maintained? Yes.

If others want to extend/augment/build on/contribute to the dataset, is there a mechanism for them to do so? Yes, they could follow the guide in https://github.com/Thinklab-SJTU/ Bench2Drive.

## J.4 Composition

What do the instances that comprise the dataset represent? One basic instance is one clip. Each clip contains hundreds or thousands of frames in 10 Hz with raw sensor information and annotations..

How many instances are there in total (of each type, if appropriate)? There are 13638 clips in Bench2Drive.

Are relationships between individual instances made explicit? Yes. Each clip is annotated with scenario types and locations. Clips could have the same scenario type or nearby location.

Are there recommended data splits (e.g., training, development/validation, testing)? Yes. In the github repo.

Is the dataset self-contained, or does it link to or otherwise rely on external resources? Self-contained.

## J.5 Collection Process

Who was involved in the data collection process (e.g., students, crowdworkers, contractors) and how were they compensated (e.g., how much were crowdworkers paid)? All data is collected in CARLA automatically The collection code is written by authors

## J.6 Use

What (other) tasks could the dataset be used for? With existing annotations, the dataset could also be used to conduct 3D object detection, semantic segmentation, instance segmentation, point cloud segmentation, depth estimation, tracking, motion prediction.