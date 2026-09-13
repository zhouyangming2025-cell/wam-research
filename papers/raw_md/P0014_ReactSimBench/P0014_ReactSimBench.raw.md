# ReactSim-Bench: Benchmarking Reactive Behavior World Model Simulation in Autonomous Driving

Zhiyuan Zhang<sup>1,2∗</sup> Yanlun Peng<sup>2</sup>

Jianing Zhang<sup>3</sup> Xianda Guo<sup>4</sup>

Zehan Huang<sup>1</sup> Haoran Liu<sup>3</sup>

Qifeng Li<sup>3</sup> Shaofeng Zhang<sup>5</sup>

Xiaosong Jia<sup>3</sup>

Junchi Yan<sup>1</sup>

<sup>1</sup> Sch. of Computer Science & Sch. of Artificial Intelligence, Shanghai Jiao Tong University <sup>2</sup> Great Wall Motor

<sup>3</sup> Institute of Trustworthy Embodied AI (TEAI), Fudan University <sup>4</sup> School of Computer Science, Wuhan University <sup>5</sup> University of Science and Technology of China

Correspondence Author https://github.com/Thinklab-SJTU/ReactSim-Bench

## Abstract

Reactive capability is a key property of data-driven behavior world model simulators for autonomous driving simulation systems. With this capability, simulated world agents can respond feasibly to autonomous vehicle (AV) behaviors that differ from the log. However, existing behavior simulation benchmarks do not directly measure reactive capability. They often let the simulator jointly control the AV and surrounding agents and evaluate realism through log similarity or open-loop prediction metrics. In this work, we introduce ReactSim-Bench for evaluating the reactive capability of behavior world model simulation in autonomous driving. We decouple the control of agents and the AV, using AV behaviors that differ from the log and require agents to respond as independent AV inputs. To obtain these AV behaviors, we construct a pipeline that uses an AV planner model to generate candidate behaviors and filters the data using rules and manual verification. Collision metrics, map-based metrics, and kinematic feasibility metrics are used to evaluate the safety and rule compliance of reactive responses. We construct 2,636 test scenarios with three categories and conduct a systematic evaluation of state-of-the-art models across multiple architectures, including Transformer-based, diffusion-based, and next-token-prediction-based models. We further analyze how replan frequency affects performance and provide insights for future studies.

## 1 Introduction

Simulation is a critical component in the development of autonomous driving (AD) algorithms, for both closed-loop evaluation and reinforcement learning. In recent years, AD simulation systems driven by real-world data have attracted increasing attention [1, 2]. Compared with rule-based simulators, they typically offer higher realism and a smaller sim-to-real gap [3]. In such systems, behavior simulation world models control the motion of surrounding vehicles by generating their future behaviors from the environmental context and historical states [4–10].

Reactive capability is a key property of behavior world simulation models, and also one of the main reasons why simulation is needed instead of simple log replay. It answers the question: if the autonomous vehicle (AV) controlled by a model to be tested does not strictly follow the recorded driving log, how will surrounding vehicles respond? As shown in Figure 1 (upper), a behavior simulation model is expected to provide reasonable feedback to the AV, such as following, yielding, and collision avoidance. As simulation rolls forward, the state of the AV increasingly deviates from the logged trajectory, leading to growing distribution shift and posing a major challenge to data-driven behavior world simulation models.

![](images/5a0a952204b626c0d9ca214bf0cf41cd1a59a7adafef888baf04cf33830dfef2.jpg)

![](images/ee22f4e44582f51ff11fe0f27645658baddbdf0b86a9192570760c2b0301dbc0.jpg)  
Figure 1: Motivation of ReactSim-Bench. It evaluates whether simulated surrounding agents can react to an AV that deviates from the recorded log, unlike realism benchmarks that couple all vehicles and evaluate log similarity.

Although several benchmarks and protocols exist for behavior world simulation, the evaluation of reactive capability remains insufficient. Popular benchmarks such as the Waymo Open Sim Agents Challenge (WOSAC) [11] mainly evaluate the realism of world simulation. In their setup, both the AV and surrounding agents are controlled by the behavior simulation model, with the objective of making predictions as close as possible to the recorded data. As a result, they do not evaluate interaction with an AV that is not controlled by the behavior simulation model and may deviate from the logged trajectory. Some other evaluation protocols still follow an open-loop paradigm similar to motion prediction, and therefore cannot assess reactive capability [12].

In this work, we propose ReactSim-Bench, the first benchmark that evaluates the reactive capability of current behavior simulation models, as shown in Figure 1 (lower right). We propose the reactive simulation protocol, which decouples the control of agents and the AV, treating the AV as an independent input to the simulation models. We collect AV behaviors that differ from the log, impose appropriate reactive pressure on agents, and are kinematically feasible as the AV behavior inputs. To obtain such behaviors, we design a data collection pipeline that uses an AV planner model to generate candidate behaviors and filters the data using rules and manual verification. For evaluation, we use collision, map-based, and kinematic metrics to examine the safety and rule compliance of world agents’ responses generated by the simulator.

Our benchmark is built on the nuPlan dataset [13]. We construct 2,636 test scenarios and divide them into three categories. We conduct a comprehensive evaluation of state-of-the-art (SOTA) behavior simulation models across multiple paradigms, including classic Transformer-based models (MTR [14]), diffusion-based models (VBD [15], CTG [16]), and next-token-prediction-based models (SMART [17], CATK [18], TrajTok [19]). Furthermore, we study how replan frequency affects reactive capability. We hope ReactSim-Bench can provide a practical reference point and encourage future studies on reactive behavior simulation.

Our contributions are four-fold:

• We present ReactSim-Bench for evaluating the reactive capability of behavior simulation, which measures how well surrounding-vehicle simulation models handle ego behaviors that deviate from the recorded log in autonomous driving simulators.

• We design a pipeline to collect reasonable AV behaviors that differ from the recorded log as AV inputs in ReactSim-Bench.

• We systematically evaluate the reactive capability of SOTA models across multiple architectures.

• We further analyze the relationship between realism and reactive performance and how replan frequency influences reactive performance.

## 2 Related work

## 2.1 Behavior Simulation World Models

Behavior world simulation in autonomous driving generates future behaviors of traffic participants from historical trajectories and scene context. Early simulators mainly rely on log replay or rulebased methods [20–23]. Data-driven approaches have since been developed for reactive and more realistic simulation [24–37]. Recently, diffusion-based methods and next-token-prediction (NTP) based methods are two representative directions for behavior simulation world models.

Diffusion is used in behavior simulation world models to model the distribution of multimoda behaviors and generate controllable behaviors [1, 12, 38–51]. For example, CTG [16] introduces conditional diffusion with signal temporal logic guidance for controllable traffic generation, and VBD [15] extends this idea to generalized traffic-agent simulation with scene-consistent interactions. The NTP paradigm is adopted for autoregressive generation [2, 52–68]. Trajeglish [69] first models traffic behavior generation as discrete NTP with a data-driven K-disks tokenizer. SMART [17] introduces map and trajectory tokenization and studies architectural scalability, while KiGRAS [70] factorizes driving scenes in action space with kinematic transformations. CATK [18] then addresses the closed-loop OOD problem with supervised fine-tuning, and TrajTok [19] further improves the tokenizer by analyzing coverage, utilization, symmetry, and robustness.

## 2.2 Behavior Simulation Protocols and Benchmarks

Existing behavior-simulation protocols are often defined with individual models and datasets. TrafficSim [71] evaluates generated traffic on the ATG4D dataset [72] using metrics such as scenario collision rate and average displacement error, while BITS [73] reports failure rate and diversity on Lyft [74] and nuScenes [75]. These metrics cover realism, safety, and diversity, but their computation details, validation splits, and rollout settings vary, making unified comparison difficult. The Waymo Open Sim Agents Challenge (WOSAC) [11] is one of the most complete and popular benchmarks for this area. It focuses on realism by computing the negative log-likelihood of multiple features extracted from simulated rollouts against logged driving statistics. It also standardizes protocol details such as the number of rollouts and the replanning frequency.

However, there still lacks benchmark for reactive capability. Most existing benchmarks and protocols predict the AV and surrounding vehicles jointly, which measures whether the simulated scene remains close to the log but does not test the case where the AV trajectory differs from the logged trajectory. Some studies show a few qualitative cases in which some vehicles follow the user-specified behaviors, but they lack a systematic quantitative protocol for reactive ability [15].

## 3 ReactSim-Bench

## 3.1 Reactive Behavior World Simulation Task

Formulation of behavior world simulation. Autonomous driving simulation starts from an initial scenario that contains an HD map M, the past $T _ { h }$ steps, including the current time step, of the AV states $\{ S _ { - T _ { h } } ^ { \mathrm { A V } } , \ldots , S _ { 0 } ^ { \mathrm { A V } } \}$ , and the world agent states $\{ \mathcal { S } _ { - T _ { h } } ^ { \mathrm { a g e n t s } } , . . . , \mathcal { S } _ { 0 } ^ { \mathrm { a g e n t s } } \}$ . At each step $t > 0$ , the AV policy p controls the next AV state based on the logged history $S _ { - T _ { h } : 0 } = [ S _ { - T _ { h } : 0 } ^ { \mathrm { A V } } , S _ { - T _ { h } : 0 } ^ { \mathrm { a g e n t s } } ]$ and the already executed states $\begin{array} { r } {  { S _ { 0 : t } ^ { \prime } } = [  { S _ { 0 : t } ^ { \prime \mathrm { A V } } } ,  { S _ { 0 : t } ^ { \prime \mathrm { a g e n t s } } } ] } \end{array}$

$$
\begin{array} { r } { S _ { t + 1 } ^ { \prime \mathrm { A V } } = p ( { \mathcal M } , [ S _ { - T _ { h } : 0 } , S _ { 0 : t } ^ { \prime } ] ) . } \end{array}\tag{1}
$$

![](images/8d431c2dfbf6b437c490bbc0b68d9223b8c4e487bf77fb7bdfadd09fd4361c59.jpg)  
Figure 2: Protocol comparison. WOSAC controls all vehicles autoregressively for realism evaluation, motion prediction predicts all timestamps in one pass, and ReactSim-Bench decouples AV and agent behavior in an autoregressive rollout.

The simulator q updates the states of the world agents in the environment using the same historical information:

$$
S _ { t + 1 } ^ { \prime \mathrm { a g e n t s } } = q ( \mathcal { M } , [ S _ { - T _ { h } : 0 } , S _ { 0 : t } ^ { \prime } ] ) .\tag{2}
$$

After the AV policy and the simulator complete their respective updates, the simulation advances to time step t + 1. Repeating this process yields an autoregressive closed-loop rollout.

Importance of reaction in behavior world simulation. Behavior world simulation is usually grounded in a real driving log, which contains both the pre-simulation states $S _ { - T _ { h } : 0 }$ and the future expert states $S _ { 0 : T _ { f } } = [ S _ { 0 : T _ { f } } ^ { \mathrm { A V } } , S _ { 0 : T _ { f } } ^ { \mathrm { a g e n t s } } ]$ over the next $T _ { f }$ steps. We usually expect the AV policy to behave similarly to the expert, i.e., the AV rollout $S _ { 0 : T _ { f } } ^ { \prime \mathrm { A V } }$ remains close to the logged AV trajectory $\mathcal { S } _ { 0 : T _ { f } } ^ { \mathrm { A V } }$ . If the AV exactly reproduces the expert states, a simulator can simply perform log replay and output the logged surrounding agent states $ { S _ { 0 : T _ { f } } } ^ { \mathrm { a g e n t s } }$ , which are closest to real driving behavior. However, AV policies often deviate from the expert. Therefore, a behavior simulator must produce reasonable responses from surrounding agents when the AV trajectory differs from the recorded log.

Reactive task in ReactSim-Bench. The reactive simulation task in ReactSim-Bench is shown in Algorithm 1. We provide AV behaviors that differ from the logged ones $S _ { 0 : T _ { f } } ^ { \mathrm { d e v i a t e d A V } }$ as the AV policy in the behavior world simulation process described above. Notably, the neural network in simulator q is not required to infer the next state at every step. It can infer several states at a time and apply them step by step.

Differences between ReactSim-Bench and previous realism benchmarks. Existing behavior world simulation benchmarks, such as WOSAC, also formulate autonomous driving simulation as stepwise inference and execution by an AV policy and a simulator. However, their evaluation protocols hand both the AV and surrounding agents to the simulator:

$$
S _ { t + 1 } ^ { \prime } = q ( \mathcal { M } , [ S _ { - T _ { h } : 0 } , S _ { 0 : t } ^ { \prime } ] ) .\tag{3}
$$

As summarized in Algorithm 2 and Figure 2, this process in WOSAC is an autoregressive version of motion prediction. The realism metrics evaluate the similarity between the rollouts and the log, and their goal is also similar to motion prediction. Under this protocol, a model can obtain strong scores by fitting the log as closely as possible, making $S _ { t + 1 } ^ { \prime } = [ \bar { S } _ { t + 1 } ^ { \prime \mathrm { A V } } , S _ { t + 1 } ^ { \prime \mathrm { a g e n t s } } ]$ close to $[ S _ { t + 1 } ^ { \mathrm { A V } } , S _ { t + 1 } ^ { \mathrm { a g e n t s } } ]$ while the reactive capability required in practical simulation is ignored. Moreover, when the simulator controls both the AV and surrounding agents, its predicted AV state is guaranteed to be realized in the future rollout, allowing it to coordinate the AV and other agents to avoid potential collisions. In practical simulation, the AV action can differ from the simulator’s prediction, making collisions and other abnormal interactions more likely.

Algorithm 1 ReactSim-Bench: Closed-Loop, Agent-AV Decoupled Inference, Reactive Task   
Input: HD map M; logged history $S _ { - T _ { h } : 0 } ;$ fixed deviated AV trajectory $S _ { 0 : T _ { f } } ^ { \mathrm { d e v i a t e d . A V } }$ ; behavior   
simulator q; horizon $T _ { f }$   
1: Initialize $S _ { 0 } ^ { \prime \mathrm { A V } }  S _ { 0 } ^ { \mathrm { d } }$ <sup>eviated</sup> <sup>AV</sup> and $S _ { 0 } ^ { \mathrm { \prime a g e n t s } }  S _ { 0 } ^ { \mathrm { a g e n t s } }$   
2: for $t = 0 , \ldots , T _ { f } - 1$ do   
3: $S _ { t + 1 } ^ { \prime \mathrm { A V } }  S _ { t + 1 } ^ { \mathrm { d e v i } }$ ated AV ▷ The AV is an external input, not controlled by q.   
4: $S _ { t + 1 } ^ { ' \mathrm { a g e n t s } }  \dot { q } ( \mathcal { M } , [ S _ { - T _ { h } : 0 } , S _ { 0 : t + 1 } ^ { \prime \mathrm { A V } } , S _ { 0 : t } ^ { \prime \mathrm { a g e n t s } } ] )$ ▷ Agents react to the realized AV state.   
5: end for   
6: return $[ S _ { 0 : T _ { f } } ^ { \prime \mathrm { A V } } , S _ { 0 : T _ { f } } ^ { \prime \mathrm { a g e n t s } } ] .$

Algorithm 2 WOSAC: Closed-Loop, Agent-AV Coupled Inference, Realism Task   
Input: HD map M; logged history $S _ { - T _ { h } }$ <sub>:0</sub>; logged future $\mathcal { S } _ { 1 : T _ { f } }$ ; behavior simulator q; horizon   
$\mathop { T _ { f } } ^ { - } .$   
1: Initialize $\begin{array} { r } { S _ { 0 } ^ { \prime } \gets [ S _ { 0 } ^ { \mathrm { A V } } , S _ { 0 } ^ { \mathrm { a g e n t s } } ] . } \end{array}$   
2: for $t = 0 , \ldots , \dot { T _ { f } } - 1 \dot { \mathbf { d o } }$   
3: $S _ { t + 1 } ^ { \prime }  q ( \dot { \mathcal { M } } , [ S _ { - T _ { h } : 0 } , S _ { 0 : t } ^ { \prime } ] )$ ▷ q controls both the AV and surrounding agents.   
4: end for   
5: return $ { S _ { 1 : T _ { f } } ^ { \prime } }$

## 3.2 Deviated AV Data for ReactSim-Bench

## 3.2.1 Data Requirements

The AV trajectories used to test reactive capability are expected to satisfy three criteria:

• Behavioral deviation from the log. The AV behavior should differ sufficiently from the recorded trajectory to evaluate agent reactivity beyond log replay.

• Reactive pressure. The deviated AV trajectory should affect the logged motion of surrounding agents, for example by inducing a collision or a small time-to-collision (TTC) under log replay. This makes log replay infeasible and requires surrounding agents to react to avoid potential collisions. Meanwhile, the induced conflict should be avoidable through reasonable agent behavior.

• Feasibility. The deviated AV behavior should be kinematically feasible and satisfy map-related constraints, such as staying within the drivable area.

## 3.2.2 Data Collection Pipeline

The most direct way to get such data is to manually select scenarios and draw all future AV states that meet the above requirements, but it requires a lot of human effort. Thus, we design a data collection pipeline with model-based candidate generation and rule-based filtering, as shown in Figure 3. The pipeline has four steps:

• Step 1: Scenario pre-selection. We first prescreen scenarios in the dataset. Based on the number, distance, and TTC of surrounding vehicles around the AV, we select scenarios with potential AV-agent interactions.

• Step 2: Candidate generation. We use a pretrained planner [76] with strong multimodal capability as the AV policy and run inference in the pre-selected scenarios. Specifically, we use Diffusion Planner for this step. The resulting trajectories are treated as candidates. This converts the labor-intensive trajectory drawing process into a trajectory selection process.

• Step 3: Filtering. We filter invalid trajectories with a set of rules to reduce the workload of subsequent manual selection. Specifically, we remove trajectories that are too close to the log according to average displacement error (ADE), leave the drivable area, violate kinematic constraints, lack sufficient interaction with other vehicles according to TTC, or actively collide with stationary or slow-moving vehicles.

![](images/371563fd03d0d555921a36d7561fbbf395e764f29b167e113128b0c031e55f62.jpg)  
Figure 3: Data collection pipeline. We pre-select interactive scenarios, generate candidate AV trajectories with a multimodal planner, filter invalid candidates, and manually verify the final deviated AV behaviors.

![](images/dd157c6b4812f217e0914f1ab7e9aa3e2baf2e9561741619d178962b02f82494.jpg)  
Figure 4: Typical cases in each deviation taxonomy. We group collected AV behaviors into lateral, directional, and longitudinal deviations.

• Step 4: Manual verification. We further verify the filtered trajectories manually to ensure that they satisfy the requirements above. If multiple candidate trajectories in a scenario meet the requirements, we select one of them. If all the candidates are invalid, the scenario is discarded.

## 3.2.3 Deviation Taxonomy

We categorize collected AV behaviors according to the dominant source of deviation from the log, which reflects the different forms of reactive pressure shown in Figure 4.

• Directional deviation. In this category, the AV drives in a different direction from the log, such as taking a different turning direction or entering a different lane connector.

• Lateral deviation. In this category, the AV keeps a similar overall driving direction to the log but drives a shifted lateral position, such as a lane change, a different merge position, or a slightly displaced path through an interaction region.

• Longitudinal deviation. In this category, the AV follows a spatial path similar to the logged trajectory, but its temporal profile differs, such as moving faster, slowing down, or stopping.

When a trajectory exhibits multiple deviation cues, we assign it to the category that best explains the interaction conflict induced by the deviated AV trajectory.

## 3.2.4 Data Analysis

Data distribution. We construct the test set of ReactSim-Bench on the nuPlan [13] dataset. The test set contains 2,636 scenarios with deviated AV behaviors, including 937 longitudinal deviations, 799 directional deviations, and 900 lateral deviations. Figure 5(a) visualizes the endpoint offset of each collected AV trajectory relative to the logged AV trajectory. The endpoint distribution is consistent with the taxonomy above: longitudinal deviations concentrate near zero lateral offset, lateral deviations show clear lateral displacement, and directional deviations spread over a wider spatial range. Figures 5(b) and 5(c) further show that the collected AV behaviors differ substantially from the recorded log. The ADE distributions are separated from zero and extend over a wide range, while the mean speed-difference distributions show non-negligible temporal deviations from the logged AV motion. Different categories emphasize different deviation sources, with directional cases tending to have larger spatial differences and longitudinal cases more directly affecting speed profiles.

Reactive pressure. To analyze the reactive pressure, we replay the logged surrounding agent behaviors while replacing the AV future behavior with the collected data, and calculate the AV-agent collision count and TTC. Log replay produces at least one AV-agent collision in 83.46% of scenarios and risky interactions with a minimum TTC below $\tau _ { \mathrm { T T C } } = 0 . 5$ s in 98.14% of scenarios. This means the world agents in our test scenarios should react to the AV to avoid unsafe interactions, rather than just replay the log.

## 3.3 Metrics

We aim to evaluate whether surrounding agents can respond reasonably to a deviated AV input in the reactive setting. To this end, we select several evaluation dimensions that are commonly used in autonomous-driving evaluation [13, 77] for measuring driving safety and feasibility, and adapt their computation to our protocol. The resulting metrics cover AV-agent safety, agent-agent safety, map and driving-direction compliance, and kinematic feasibility:

• Agent-AV collision count reports the average number of surrounding agents that collide with the AV, reflecting whether agents can respond to AV behavior to avoid potential collisions. For each scenario, we first identify all agents that collide with the AV at any time step. For each such agent, at its first collision time with the AV, we determine whether the agent is at fault by their position and heading. The agent is counted only if it is at fault.

• Agent-AV risky TTC count is a stricter counterpart to the average Agent-AV collision count. We compute the TTC between each surrounding agent and the AV. If the TTC falls below a threshold at any time step, the agent is marked as risky. The final metric is the average risky-agent count over all scenarios.

• Agent-agent collision rate computes the fraction of world agents involved in collisions with other world agents at each step.

• Off-road rate computes the fraction of timestamps at which a vehicle leaves the drivable area. We only evaluate vehicles that are initially in the drivable area.

• Driving-direction violation rate computes the fraction of vehicles that violate the driving direction of their current road segment, such as driving against traffic.

• Kinematic infeasibility rate estimates each vehicle’s acceleration and steering curvature from consecutive states using an inverse kinematic model and checks whether they remain within predefined thresholds. We report acceleration and steering-curvature infeasibility rates separately.

Detailed metric computation rules are provided in Appendix C.2.

![](images/b0c7a3d376e5999c11678ef7b2a3999ba0dffbb002487cdf6e6aef4ab6ba5f3f.jpg)  
(a) AV Endpoint Offset

![](images/cd07968bec7a6e4a6ca2f4ac2788dde8677739e674ce8570a6eede40c0336488.jpg)  
(b) ADE Distribution

![](images/c784cac774daa43a919b5565c3166323134179c82734d6347da585c6b9cddad3.jpg)  
(c) Mean Speed Difference Distribution  
Figure 5: Distribution of collected AV deviations. (a) Endpoint offsets by deviation type. (b) ADE and (c) mean speed difference between deviated and logged AV trajectories.

## 4 Experiments

## 4.1 Datasets & Baselines

Our benchmark is built on the nuPlan [13] dataset, which contains more than 1,000 hours of driving data. We repartition the data into a training set with 642,640 scenarios and a test set with 2,636 scenarios. Each scenario lasts 9 seconds, consisting of 1 second of history and 8 seconds of future rollout. The sampling frequency is 10 Hz, resulting in 91 frames per scenario. We select the 64 agents closest to the AV at the current time step, i.e., the 10th frame, as prediction targets. For map inputs, we use four types of map elements, with the input range following the original setting of each baseline. Our baselines include:

• MTR [14] is a classic Transformer-based motion prediction model. It uses global intention localization and local movement refinement, and achieves strong performance in open-loop trajectory prediction for surrounding agents. We use it as a baseline that directly applies a motion prediction model to behavior simulation.

• CTG [16] is one of the earliest works that applies diffusion models to behavior simulation. It takes rasterized environmental and historical information as input and uses signal temporal logic (STL) as guidance to generate realistic and controllable behaviors.

• VBD [15] uses a behavior prior predictor to predict a goal point for each agent, and then uses the predicted goals as guidance for a diffusion decoder to generate diverse surrounding-agent behaviors.

• SMART [17] follows the next-token prediction paradigm. It discretizes agent trajectories into a vocabulary and generates trajectories autoregressively, winning WOSAC 2024.

• CATK [18] builds on the NTP paradigm and proposes Closed-Loop Supervised Fine-Tuning, which further improves performance through post-training.

• TrajTok [19] studies vocabulary design under the NTP paradigm and proposes a trajectory vocabulary with strong coverage, utilization, symmetry, and robustness, winning WOSAC 2025.

The above methods were originally implemented on Waymo or nuScenes. We implement them on the nuPlan dataset for evaluation under our benchmark.

## 4.2 Main Results

Table 1 reports all metrics on ReactSim-Bench, and Table 2 compares these methods under our Reactive Protocol and the prior Realism Protocol. We make the following findings:

Behavior world simulation models have a certain level of reactive capability. When the AV behavior differs from the log, log replay produces many collisions and unsafe interactions, while all learned models substantially reduce the A-AV collision count and risky TTC count. This indicates that our test scenarios impose reactive pressure while still remaining solvable.

Better realism does not necessarily lead to better reactive performance. For example, MTR has worse ADE and kinematic likelihood than CTG under the realism protocol, but achieves lower A-AV collision and risky TTC counts under the reactive protocol. Similarly, CATK improves the realism metrics over SMART but has slightly worse reactive metrics. Realism is an important criterion for evaluating behavior world simulation models, but it cannot represent every aspect of model performance.

Table 1: Main results on ReactSim-Bench. All methods are evaluated with a replan rate of 2 Hz. A-AV Coll. Count denotes Agent-AV collision count, A-AV risky Count denotes Agent-AV risky TTC count, A-A Coll. denotes Agent-Agent collision rate, Dir. denotes driving-direction violation rate, Acc. denotes acceleration infeasibility rate, and Steer. denotes steering-curvature infeasibility rate.
<table><tr><td>Method</td><td></td><td>A-AV Coll. Count ↓ A-AV risky Count ↓ A-A Coll. ↓ (%)</td><td></td><td>Offroad ↓(%)</td><td></td><td>Dir. (%) ↓ Acc. (%) ↓ Steer. (%) ↓</td><td></td></tr><tr><td>Log Replay</td><td>0.9829</td><td>1.5380</td><td>2.25</td><td>0.18</td><td>0.80</td><td>0.16</td><td>2.51</td></tr><tr><td>MTR</td><td>0.1457</td><td>0.5819</td><td>3.29</td><td>2.67</td><td>2.83</td><td>0.64</td><td>14.29</td></tr><tr><td>CTG</td><td>0.6195</td><td>0.9476</td><td>4.88</td><td>2.95</td><td>2.10</td><td>10.87</td><td>7.08</td></tr><tr><td>VBD</td><td>0.2276</td><td>0.4711</td><td>3.19</td><td>1.03</td><td>2.35</td><td>0.01</td><td>0.18</td></tr><tr><td>SMART</td><td>0.1419</td><td>0.3976</td><td>2.23</td><td>0.68</td><td>1.09</td><td>9.74</td><td>4.83</td></tr><tr><td>CATK</td><td>0.1426</td><td>0.4029</td><td>2.22</td><td>0.69</td><td>1.13</td><td>10.25</td><td>5.02</td></tr><tr><td>TrajTok</td><td>0.1407</td><td>0.4173</td><td>2.23</td><td>0.61</td><td>1.03</td><td>3.23</td><td>3.93</td></tr></table>

Table 2: Results in realism and reactive evaluation protocols. Kin. Lik. denotes kinematic likelihood in WOSAC.
<table><tr><td rowspan="2">Method</td><td colspan="2">Reactive Protocol</td><td colspan="4">Realism Protocol</td></tr><tr><td>A-AV Coll. Count ↓</td><td>A-AV risky Count ↓</td><td>A-AV Coll. Count ↓</td><td>A-AV risky Count ↓</td><td>ADE (m) ↓</td><td>Kin. Lik. ↑</td></tr><tr><td>MTR</td><td>0.1457</td><td>0.5819</td><td>0.0781</td><td>0.5353</td><td>2.5498</td><td>0.2379</td></tr><tr><td>CTG</td><td>0.6195</td><td>0.9476</td><td>0.2527</td><td>0.4586</td><td>1.9405</td><td>0.2721</td></tr><tr><td>VBD</td><td>0.2276</td><td>0.4711</td><td>0.0819</td><td>0.2041</td><td>1.1579</td><td>0.2975</td></tr><tr><td>SMART</td><td>0.1419</td><td>0.3976</td><td>0.0125</td><td>0.0617</td><td>0.8021</td><td>0.3510</td></tr><tr><td>CATK</td><td>0.1426</td><td>0.4029</td><td>0.0095</td><td>0.0501</td><td>0.7988</td><td>0.3645</td></tr><tr><td>TrajTok</td><td>0.1407</td><td>0.4173</td><td>0.0099</td><td>0.0524</td><td>0.8266</td><td>0.3652</td></tr></table>

![](images/05be0c73a153cf1ee70acb0760d29d029bf66b3788f8a94640a30c3c4c74bd2f.jpg)  
Figure 6: Effect of replanning interval. We ablate the replanning interval in ReactSim-Bench and report A-AV collision count and risky TTC count. More frequent replanning generally improves reactive capability by letting the simulator observe the realized AV behavior more often, but the effect remains model-dependent.

Learning strong reactive capability from fitting the log is difficult. SMART, CATK, and TrajTok fit the logged trajectories well under the realism protocol, as reflected by their low ADE and very low A-AV collision counts. However, their A-AV collision counts increase markedly under the Reactive Protocol. Imitation-learning paradigms rely on fitting the log and therefore face an out-ofdistribution problem when responding to AV trajectories that differ from the log. Although diffusion and next-token-prediction paradigms provide stronger probabilistic modeling than direct regression, understanding and responding to the behavior of other vehicles remains challenging.

## 4.3 Analysis on Replan Rate

Figure 6 ablates the replanning interval in ReactSim-Bench. As mentioned in Section 3.1, a model can predict multiple steps at once and then execute them alternately with the AV policy. The results show that higher replanning rates (above 1 Hz) generally bring better reactive capability. This is because the simulator does not know the future AV behavior in ReactSim-Bench, and more frequent replanning allows it to observe the current scene state, especially the realized AV behavior, more often and respond more effectively. However, frequent replanning can also introduce larger accumulated errors, so smaller replanning intervals are not always better for every model. Therefore, the replanning strategy can strongly affect reactive performance.

This differs from realism benchmarks such as WOSAC. In prior studies [30], smaller replanning rates on WOSAC (below 0.5 Hz) have better realism. This is because WOSAC lets the model control all vehicles, including the AV, and does not consider interactions with vehicles outside model control. Therefore, accumulated error becomes the main negative effect of high-frequency replanning. To maintain the autoregressive requirement of simulation, WOSAC restricts the replanning rate to be greater than 1 Hz. ReactSim-Bench does not need this type of restriction. Its demand for high-frequency replanning is natural and closer to practical simulation.

## 5 Conclusion

In this work, we introduce ReactSim-Bench for evaluating the reactive capability of behavior world model simulation in autonomous driving. We decouple AV control from surrounding-agent simulation and collect deviated AV behaviors as benchmark inputs, allowing the simulator to be tested under situations where the AV does not simply follow the recorded log. We evaluate multiple state-of-the-art behavior world models under this protocol and provide a foundation and insights for developing future reactive behavior world models.

## References

[1] Xuemeng Yang, Licheng Wen, Tiantian Wei, Yukai Ma, Jianbiao Mei, Xin Li, Wenjie Lei, Daocheng Fu, Pinlong Cai, Min Dou, et al. Drivearena: A closed-loop generative simulation platform for autonomous driving. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 26933– 26943, 2025.

[2] Jiazhi Yang, Kashyap Chitta, Shenyuan Gao, Long Chen, Yuqian Shao, Xiaosong Jia, Hongyang Li, Andreas Geiger, Xiangyu Yue, and Li Chen. Resim: Reliable world simulation for autonomous driving. arXiv preprint arXiv:2506.09981, 2025.

[3] Di Chen, Meixin Zhu, Hao Yang, Xuesong Wang, and Yinhai Wang. Data-driven traffic simulation: A comprehensive review. IEEE Transactions on Intelligent Vehicles, 9(4):4730–4748, 2024.

[4] Raunak P Bhattacharyya, Derek J Phillips, Changliu Liu, Jayesh K Gupta, Katherine Driggs-Campbell, and Mykel J Kochenderfer. Simulating emergent properties of human driving behavior using multi-agent reward augmented imitation learning. In 2019 International Conference on Robotics and Automation (ICRA), pages 789–795. IEEE, 2019.

[5] Raunak P Bhattacharyya, Derek J Phillips, Blake Wulfe, Jeremy Morton, Alex Kuefler, and Mykel J Kochenderfer. Multi-agent imitation learning for driving simulation. In 2018 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 1534–1539. IEEE, 2018.

[6] MyungJae Shin and Joongheon Kim. Randomized adversarial imitation learning for autonomous driving. arXiv preprint arXiv:1905.05637, 2019.

[7] Seongjin Choi, Jiwon Kim, and Hwasoo Yeo. Trajgail: Generating urban vehicle trajectories using generative adversarial imitation learning. Transportation Research Part C: Emerging Technologies, 128: 103091, 2021.

[8] Jie Sun and Jiwon Kim. Modelling two-dimensional driving behaviours at unsignalised intersection using multi-agent imitation learning. Transportation Research Part C: Emerging Technologies, 165:104702, 2024.

[9] Jie Sun and Hai Yang. Learning two-dimensional merging behaviour from vehicle trajectories with imitation learning. Transportation research part C: emerging technologies, 160:104530, 2024.

[10] Shuqiao Wei, Ying Ni, and Jian Sun. Transformer-based multi-agent traffic simulation for autonomous vehicle testing in shared urban road segments. Accident Analysis & Prevention, 232:108550, 2026.

[11] Nico Montali, John Lambert, Paul Mougin, Alex Kuefler, Nicholas Rhinehart, Michelle Li, Cole Gulino, Tristan Emrich, Zoey Yang, Shimon Whiteson, et al. The waymo open sim agents challenge. Advances in Neural Information Processing Systems, 36:59151–59171, 2023.

[12] Ethan Pronovost, Meghana Reddy Ganesina, Noureldin Hendy, Zeyu Wang, Andres Morales, Kai Wang, and Nick Roy. Scenario diffusion: Controllable driving scenario generation with diffusion. Advances in Neural Information Processing Systems, 36:68873–68894, 2023.

[13] Holger Caesar, Juraj Kabzan, Kok Seang Tan, Whye Kit Fong, Eric Wolff, Alex Lang, Luke Fletcher, Oscar Beijbom, and Sammy Omari. nuplan: A closed-loop ml-based planning benchmark for autonomous vehicles. arXiv preprint arXiv:2106.11810, 2021.

[14] Shaoshuai Shi, Li Jiang, Dengxin Dai, and Bernt Schiele. Motion transformer with global intention localization and local movement refinement. Advances in Neural Information Processing Systems, 35: 6531–6543, 2022.

[15] Zhiyu Huang, Zixu Zhang, Ameya Vaidya, Yuxiao Chen, Jaime Fernández Fisac, and Chen Lv. Versatile behavior diffusion for generalized traffic agent simulation. IEEE Transactions on Intelligent Transportation Systems, 2026.

[16] Ziyuan Zhong, Davis Rempe, Danfei Xu, Yuxiao Chen, Sushant Veer, Tong Che, Baishakhi Ray, and Marco Pavone. Guided conditional diffusion for controllable traffic simulation. In 2023 IEEE international conference on robotics and automation (ICRA), pages 3560–3566. IEEE, 2023.

[17] Wei Wu, Xiaoxin Feng, Ziyan Gao, and Yuheng Kan. Smart: Scalable multi-agent real-time motion generation via next-token prediction. Advances in Neural Information Processing Systems, 37:114048– 114071, 2024.

[18] Zhejun Zhang, Peter Karkus, Maximilian Igl, Wenhao Ding, Yuxiao Chen, Boris Ivanovic, and Marco Pavone. Closed-loop supervised fine-tuning of tokenized traffic models. In Proceedings of the Computer Vision and Pattern Recognition Conference, pages 5422–5432, 2025.

[19] Zhiyuan Zhang, Xiaosong Jia, Guanyu Chen, Qifeng Li, Zuxuan Wu, Yu-Gang Jiang, and Junchi Yan. Trajtok: What makes for a good trajectory tokenizer in behavior generation? In International Conference on Learning Representations (ICLR), 2026.

[20] Michael Behrisch, Laura Bieker, Jakob Erdmann, and Daniel Krajzewicz. Sumo–simulation of urban mobility: an overview. In Proceedings ofSIMUL 2011, the third international conference on advances in system simulation. ThinkMind, 2011.

[21] Martin Treiber and Arne Kesting. The intelligent driver model with stochasticity-new insights into traffic flow oscillations. Transportation research procedia, 23:174–187, 2017.

[22] Arne Kesting, Martin Treiber, and Dirk Helbing. General lane-changing model mobil for car-following models. Transportation Research Record, 1999(1):86–94, 2007.

[23] Arne Kesting, Martin Treiber, and Dirk Helbing. Enhanced intelligent driver model to access the impact of driving strategies on traffic capacity. Philosophical Transactions ofthe Royal Society A: Mathematical, Physical and Engineering Sciences, 368(1928):4585–4605, 2010.

[24] Guanjie Zheng, Hanyang Liu, Kai Xu, and Zhenhui Li. Learning to simulate vehicle trajectories from demonstrations. In 2020 IEEE 36th International Conference on Data Engineering (ICDE), pages 1822– 1825. IEEE, 2020.

[25] Laura Zheng, Sanghyun Son, and Ming C Lin. Traffic-aware autonomous driving with differentiable traffic simulation. arXiv preprint arXiv:2210.03772, 2022.

[26] Lan Feng, Quanyi Li, Zhenghao Peng, Shuhan Tan, and Bolei Zhou. Trafficgen: Learning to generate diverse and realistic traffic scenarios. arXiv preprint arXiv:2210.06609, 2022.

[27] Chris Zhang, James Tu, Lunjun Zhang, Kelvin Wong, Simon Suo, and Raquel Urtasun. Learning realistic traffic agents in closed-loop. arXiv preprint arXiv:2311.01394, 2023.

[28] Zhejun Zhang, Alexander Liniger, Dengxin Dai, Fisher Yu, and Luc Van Gool. Trafficbots: Towards world models for autonomous driving simulation and motion prediction. arXiv preprint arXiv:2303.04116, 2023.

[29] Zhejun Zhang, Christos Sakaridis, and Luc Van Gool. Trafficbots v1. 5: Traffic simulation via conditional vaes and transformers with relative pose encoding. arXiv preprint arXiv:2406.10898, 2024.

[30] Longzhong Lin, Xuewu Lin, Kechun Xu, Haojian Lu, Lichao Huang, Rong Xiong, and Yue Wang. Revisit mixture models for multi-agent simulation: Experimental study within a unified framework. arXiv preprint arXiv:2501.17015, 2025.

[31] Quanyi Li, Zhenghao Mark Peng, Lan Feng, Zhizheng Liu, Chenda Duan, Wenjie Mo, and Bolei Zhou. Scenarionet: Open-source platform for large-scale traffic scenario simulation and modeling. Advances in neural information processing systems, 36:3894–3920, 2023.

[32] Shuhan Tan, Kelvin Wong, Shenlong Wang, Sivabalan Manivasagam, Mengye Ren, and Raquel Urtasun. Scenegen: Learning to generate realistic traffic scenes. In Proceedings ofthe IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 892–901, 2021.

[33] Tsun-Hsuan Wang, Alexander Amini, Wilko Schwarting, Igor Gilitschenski, Sertac Karaman, and Daniela Rus. Learning interactive driving policies via data-driven simulation. In 2022 International Conference on Robotics and Automation (ICRA), pages 7745–7752. IEEE, 2022.

[34] Luke Rowe, Roger Girgis, Anthony Gosselin, Liam Paull, Christopher Pal, and Felix Heide. Scenario dreamer: Vectorized latent diffusion for generating driving simulation environments. In Proceedings ofthe IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 17207–17218, 2025.

[35] Mozhgan Pourkeshavatz, Tianran Liu, and Nicholas Rhinehart. Autoworld: Scaling multi-agent traffic simulation with self-supervised world models. arXiv preprint arXiv:2603.28963, 2026.

[36] Kashyap Chitta, Daniel Dauner, and Andreas Geiger. Sledge: Synthesizing driving environments with generative models and rule-based traffic. In European Conference on Computer Vision, pages 57–74. Springer, 2024.

[37] Yuanfu Luo, Panpan Cai, Yiyuan Lee, and David Hsu. Gamma: A general agent motion model for autonomous driving. IEEE Robotics and Automation Letters, 7(2):3499–3506, 2022.

[38] Wei-Jer Chang, Francesco Pittaluga, Masayoshi Tomizuka, Wei Zhan, and Manmohan Chandraker. Safesim: Safety-critical closed-loop traffic simulation with diffusion-controllable adversaries. In European conference on computer vision, pages 242–258. Springer, 2024.

[39] Yunpeng Liu, Matthew Niedoba, William Harvey, Adam Scibior, Berend Zwartsenberg, and Frank Wood. Rolling ahead diffusion for traffic scene simulation. arXiv preprint arXiv:2502.09587, 2025.

[40] Yue Yao, Mohamed-Khalil Bouzidi, Daniel Goehring, and Joerg Reichardt. Ep-diffuser: An efficient diffusion model for traffic scene generation and prediction via polynomial representations. IEEE Robotics and Automation Letters, 2025.

[41] Jinxiong Lu, Shoaib Azam, Gokhan Alcan, and Ville Kyrki. Data-driven diffusion models for enhancing safety in autonomous vehicle traffic simulations. arXiv preprint arXiv:2410.04809, 2024.

[42] Kargi Chauhan and Leilani H Gilpin. Vfsi: Validity first spatial intelligence for constraint-guided traffic diffusion. arXiv preprint arXiv:2509.23971, 2025.

[43] Chiyu M Jiang, Yijing Bai, Andre Cornman, Christopher Davis, Xiukun Huang, Hong Jeon, Sakshum Kulshrestha, John Lambert, Shuangyu Li, Xuanyu Zhou, et al. Scenediffuser: Efficient and controllable driving simulation initialization and rollout. Advances in Neural Information Processing Systems, 37: 55729–55760, 2024.

[44] Chiyu Jiang, Andre Cornman, Cheolho Park, Benjamin Sapp, Yin Zhou, Dragomir Anguelov, et al. Motiondiffuser: Controllable multi-agent motion prediction using diffusion. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 9644–9653, 2023.

[45] Shuhan Tan, John Lambert, Hong Jeon, Sakshum Kulshrestha, Yijing Bai, Jing Luo, Dragomir Anguelov, Mingxing Tan, and Chiyu Max Jiang. Scenediffuser++: City-scale traffic simulation via a generative world model. In Proceedings ofthe Computer Vision and Pattern Recognition Conference, pages 1570–1580, 2025.

[46] Theodor Westny, Björn Olofsson, and Erik Frisk. Diffusion-based environment-aware trajectory prediction. arXiv preprint arXiv:2403.11643, 2024.

[47] Yuheng Zhang, Tianjian Ouyang, Fudan Yu, Lei Qiao, Wei Wu, Jingtao Ding, Jian Yuan, and Yong Li. Lcsim: A large-scale controllable traffic simulator. arXiv preprint arXiv:2406.19781, 2024.

[48] Yuxin Liu, Zhenghao Peng, Xuanhao Cui, and Bolei Zhou. Adv-bmt: Bidirectional motion transformer for safety-critical traffic scenario generation. arXiv preprint arXiv:2506.09485, 2025.

[49] Yu Yang, Alan Liang, Jianbiao Mei, Yukai Ma, Yong Liu, and Gim Hee Lee. X-scene: Large-scale driving scene generation with high fidelity and flexible controllability. arXiv preprint arXiv:2506.13558, 2025.

[50] Xiangyu Guo, Zhanqian Wu, Kaixin Xiong, Ziyang Xu, Lijun Zhou, Gangwei Xu, Shaoqing Xu, Haiyang Sun, Bing Wang, Guang Chen, et al. Genesis: Multimodal driving scene generation with spatio-temporal and cross-modal consistency. arXiv preprint arXiv:2506.07497, 2025.

[51] Wei Cao, Marcel Hallgarten, Tianyu Li, Daniel Dauner, Xunjiang Gu, Caojun Wang, Yakov Miron, Marco Aiello, Hongyang Li, Igor Gilitschenski, et al. Pseudo-simulation for autonomous driving. arXiv preprint arXiv:2506.04218, 2025.

[52] Yu Wang, Tiebiao Zhao, and Fan Yi. Multiverse transformer: 1st place solution for waymo open sim agents challenge 2023. arXiv preprint arXiv:2306.11868, 2023.

[53] Cheng Qian, Di Xiu, and Minghao Tian. The 2nd place solution for 2023 waymo open sim agents challenge. arXiv preprint arXiv:2306.15914, 2023.

[54] Zikang Zhou, Haibo Hu, Xinhong Chen, Jianping Wang, Nan Guan, Kui Wu, Yung-Hui Li, Yu-Kai Huang, and Chun J Xue. Behaviorgpt: Smart agent simulation for autonomous driving with next-patch prediction. Advances in Neural Information Processing Systems, 37:79597–79617, 2024.

[55] Muleilan Pei, Shaoshuai Shi, and Shaojie Shen. Advancing multi-agent traffic simulation via r1-style reinforcement fine-tuning. arXiv preprint arXiv:2509.23993, 2025.

[56] Zhenghao Peng, Yuxin Liu, and Bolei Zhou. Infgen: Scenario generation as next token group prediction. arXiv preprint arXiv:2506.23316, 2025.

[57] Zhenghao Peng, Wenjie Luo, Yiren Lu, Tianyi Shen, Cole Gulino, Ari Seff, and Justin Fu. Improving agent behaviors with rl fine-tuning for autonomous driving. In European Conference on Computer Vision, pages 165–181. Springer, 2024.

[58] Wei-Jer Chang, Akshay Rangesh, Kevin Joseph, Matthew Strong, Masayoshi Tomizuka, Yihan Hu, and Wei Zhan. Spacer: Self-play anchoring with centralized reference models. arXiv preprint arXiv:2510.18060, 2025.

[59] Daphne Cornelisse, Aarav Pandya, Kevin Joseph, Joseph Suárez, and Eugene Vinitsky. Building reliabl sim driving agents by scaling self-play. arXiv preprint arXiv:2502.14706, 2025.

[60] Zhenghao Peng, Yuxin Liu, and Bolei Zhou. Scenestreamer: Continuous scenario generation as next token group prediction. In The Fourteenth International Conference on Learning Representations, 2026. URL https://openreview.net/forum?id=IWt4ERrdYp.

[61] Shuhan Tan, Boris Ivanovic, Yuxiao Chen, Boyi Li, Xinshuo Weng, Yulong Cao, Philipp Krähenbühl, and Marco Pavone. Promptable closed-loop traffic simulation. arXiv preprint arXiv:2409.05863, 2024.

[62] Keyu Chen, Wenchao Sun, Hao Cheng, and Sifa Zheng. Rift: Group-relative rl fine-tuning for realistic and controllable traffic simulation. arXiv preprint arXiv:2505.03344, 2025.

[63] Hao Gao, Jingyue Wang, Wenyang Fang, Jingwei Xu, Yunpeng Huang, Taolue Chen, and Xiaoxing Ma. Laser: Script execution by autonomous agents for on-demand traffic simulation. In Proceedings of the 16th International Conference on Internetware, pages 84–95, 2025.

[64] Mingyi Wang, Jingke Wang, Tengju Ye, Junbo Chen, and Kaicheng Yu. Do llm modules generalize? a study on motion generation for autonomous driving. arXiv preprint arXiv:2509.02754, 2025.

[65] Junqi You, Xiaosong Jia, Zhiyuan Zhang, Yutao Zhu, and Junchi Yan. Bench2drive-r: Turning real world data into reactive closed-loop autonomous driving benchmark by generative model. arXiv preprint arXiv:2412.09647, 2024.

[66] Ehsan Ahmadi and Hunter Schofield. Rlftsim: Multi-agent traffic simulation via reinforcement learning fine-tuning. In CVPR Workshop on Autonomous Driving (WAD), 2025.

[67] Ziyan Wang, Peng Chen, Ding Li, Chiwei Li, Qichao Zhang, Zhongpu Xia, and Guizhen Yu. Learning rollout from sampling: An r1-style tokenized traffic simulation model. IEEE Robotics and Automation Letters, 11(5):6336–6343, 2026.

[68] Ziyi Song, Chen Xia, Chenbing Wang, Haibao Yu, Sheng Zhou, and Zhisheng Niu. Unimm-v2x: Moeenhanced multi-level fusion for end-to-end cooperative autonomous driving. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 40, pages 9135–9143, 2026.

[69] Jonah Philion, Xue Bin Peng, and Sanja Fidler. Trajeglish: Traffic modeling as next-token prediction. arXiv preprint arXiv:2312.04535, 2023.

[70] Jianbo Zhao, Jiaheng Zhuang, Qibin Zhou, Taiyu Ban, Ziyao Xu, Hangning Zhou, Junhe Wang, Guoan Wang, Zhiheng Li, and Bin Li. Kigras: Kinematic-driven generative model for realistic agent simulation. IEEE Robotics and Automation Letters, 10(2):1082–1089, 2024.

[71] Simon Suo, Sebastian Regalado, Sergio Casas, and Raquel Urtasun. Trafficsim: Learning to simulate realistic multi-agent behaviors. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 10400–10409, 2021.

[72] Wenjie Luo, Bin Yang, and Raquel Urtasun. Fast and furious: Real time end-to-end 3d detection, tracking and motion forecasting with a single convolutional net. In Proceedings ofthe IEEE conference on Computer Vision and Pattern Recognition, pages 3569–3577, 2018.

[73] Danfei Xu, Yuxiao Chen, Boris Ivanovic, and Marco Pavone. Bits: Bi-level imitation for traffic simulation. arXiv preprint arXiv:2208.12403, 2022.

[74] Guopeng Li, Yiru Jiao, Victor L Knoop, Simeon C Calvert, and JWC Van Lint. Large car-following data based on lyft level-5 open dataset: Following autonomous vehicles vs. human-driven vehicles. In 2023 IEEE 26th International Conference on Intelligent Transportation Systems (ITSC), pages 5818–5823. IEEE, 2023.

[75] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multimodal dataset for autonomous driving. In Proceedings ofthe IEEE/CVF conference on computer vision and pattern recognition, pages 11621–11631, 2020.

[76] Yinan Zheng, Ruiming Liang, Kexin Zheng, Jinliang Zheng, Liyuan Mao, Jianxiong Li, Weihao Gu, Rui Ai, Shengbo Eben Li, Xianyuan Zhan, et al. Diffusion-based planning for autonomous driving with flexible guidance. arXiv preprint arXiv:2501.15564, 2025.

[77] Cole Gulino, Justin Fu, Wenjie Luo, George Tucker, Eli Bronstein, Yiren Lu, Jean Harb, Xinlei Pan, Yan Wang, Xiangyu Chen, et al. Waymax: An accelerated, data-driven simulator for large-scale autonomous driving research. Advances in Neural Information Processing Systems, 36:7730–7742, 2023.

![](images/dd400ba3171b2795419c99a9bda9d611ef666bedb673196ab141a772ee3c1c71.jpg)  
Figure 7: Qualitative case study. In a ramp-merging scenario, the deviated AV enters the main road earlier than in the log. CATK slows down but still collides, CTG remains close to log replay and collides, while TrajTok decelerates in time and avoids the collision.

## A Case Study

Figure 7 shows a merging scenario where the AV on the ramp starts earlier than in the log and merges onto the main road, requiring the rear vehicle to yield. CATK produces a deceleration response, but the deceleration is insufficient. CTG largely ignores the change in AV behavior, keeping the rear vehicle close to the logged trajectory and directly colliding with the AV. In contrast, TrajTok decelerates in time and avoids the potential collision. The two failure cases suggest that when the AV behavior differs from the log, simulators may still tend to make surrounding agents follow the recorded trajectories.

Figure 8 shows another case with a directional deviation. In the logged behavior, the AV follows the original traffic flow, while the collected AV input drives toward a different direction and creates a new interaction with nearby vehicles. VBD does not sufficiently adapt the surrounding-agent behavior to the deviated AV motion. The interacting vehicle remains close to its logged trajectory and collides with the AV, as highlighted in the red box. SMART produces a more compatible response and avoid the collision.

## B Limitations

We mainly focus on evaluating the reactive capability of behavior world model simulation. In addition to reactivity and realism, some methods also target other objectives, such as controllability and diversity. A systematic benchmark for these objectives is outside the scope of this paper, but may serve as a direction for future research.

![](images/f8be3dfe012670b422d112e0cfd190925aafada27bbb12dc29f123c5368b35d0.jpg)  
Figure 8: Directional-deviation case study. The collected AV input drives toward a direction different from the log. VBD keeps the interacting vehicle close to the logged behavior and collides with the AV, while SMART produces a safer response.

## C Implementation Details

## C.1 Baseline Implementation on nuPlan

Scenario Data. All models are trained on the same unified per-scenario nuPlan data cache. Our current cache contains 642,639 training scenarios and 2,636 validation scenarios. Each scenario is represented by 91 frames sampled at 10 Hz, with the current frame fixed at index 10, yielding 11 history frames and 80 future frames. We keep the ego vehicle plus up to 63 nearby agents in each scene, using the same current-time index and the same train/validation split for all methods. Agent state tensors contain position, heading, velocity, and object size, and are padded to the same history and future lengths before model-specific preprocessing.

We first map raw nuPlan tracked-object types into a canonical agent taxonomy. Specifically, VEHICLE and EGO are mapped to the vehicle class, PEDESTRIAN to the pedestrian class, and BICYCLE to the cyclist class, while TRAFFIC\_CONE, BARRIER, CZONE\_SIGN, and GENERIC\_OBJECT are merged into an auxiliary “other” category in the cache. For training the world models, we use the three shared dynamic classes vehicle / pedestrian / cyclist, and ego is always preserved as slot 0. The remaining slots are filled by selecting the nearest valid agents around ego at the current frame, up to the shared limit of 64 total agents. This gives all methods the same scene-centric agent budget and the same temporal alignment before their own feature builders are applied.

The unified cache is built from original nuPlan map API queries around the scenario region. During preprocessing, we collect lane, lane connector, crosswalk, and stop-line map objects, and derive road-edge geometry from lane and lane-connector boundaries. In the common representation used across methods, map elements are organized into four semantic categories: lane, road edge, stop line, and crosswalk. Each element is represented as a sampled polyline together with a validity mask. Lane connectors are merged into the lane class in the shared vector representation, but connector-specific identity is retained in the cache when downstream modules need exact traffic-light alignment. Traffic lights are stored through stop-point coordinates, future state sequences, and lane-polyline indices, with raw nuPlan states normalized into a canonical state space before model-specific remapping. This common cache is then adapted into each model’s native input format, so that differences across methods mainly come from the model architecture rather than scene parsing or map extraction.

Model Settings. All models are trained on 8 NVIDIA H200 GPUs. We preserve the original optimizer family and the original model architecture of each baseline whenever possible, and only replace the dataset interface and nuPlan alignment layer required to consume the unified data cache. The model-specific settings are summarized in Table 3.

Table 3: Model-specific training and map settings under the unified nuPlan data cache.
<table><tr><td>Model</td><td>Architecture</td><td>Map setting</td><td>Batch Size</td><td>Training</td><td>LR</td></tr><tr><td>VBD</td><td>6-layer encoder; 50 diffusion steps; 2-step actions</td><td>300 m crop; 256 polylines; 30 pts / polyline</td><td>32 scenar- ios</td><td>16 epochs</td><td> $2 \times 1 0 ^ { - 4 }$ </td></tr><tr><td>MTR</td><td>6-layer encoder; 6-layer decoder; 6 modes; hidden 256 / 512</td><td>120 m radius; 768 source poly- lines; 20 pts / polyline</td><td>8 scenarios</td><td>12 epochs</td><td> $1 0 ^ { - 4 }$ </td></tr><tr><td>CTG</td><td>ResNet-18 BC policy</td><td>224 × 224 raster; 0.5 m / px; 112 × 112 m</td><td>1,600 agents</td><td>1M iters</td><td>10-3</td></tr><tr><td>SMART</td><td>hidden dim 128; 6 agent layers</td><td>300 m crop; tokenized vector map</td><td>10 scenar- ios</td><td>32 epochs</td><td> $5 \times 1 0 ^ { - 4 }$ </td></tr><tr><td>TrajTok</td><td>hidden dim 128; 6 agent layers; new traj. vocab; LS + SAS</td><td>300 m crop; tokenized vector map</td><td>10 scenar- ios</td><td>32 epochs</td><td> $5 \times 1 0 ^ { - 4 }$ </td></tr><tr><td>CLSFT</td><td>SMART init.; closed-loop SFT</td><td>300 m crop; tokenized vector map</td><td>10 scenar- ios</td><td>fine-tuning 32 epochs on SMART</td><td> $5 \times 1 0 ^ { - 5 }$ </td></tr></table>

## C.2 Metric Computation Details

This section provides the implementation details of the seven metrics used in ReactSim-Bench. Let V denote the set of evaluated non-ego vehicles, A denote the set of evaluated non-ego objects, and T denote the number of future simulation steps. All scenarios are sampled at $\Delta t = 0 . 1 \mathrm { s }$ . For metrics reported as rates, we first compute a scenario-level rate and then average it over all valid scenarios. For metrics reported as counts, the reported value is the mean scenario-level count. Collision-related metrics use oriented bounding boxes in bird’s-eye view. A pair of boxes is treated as colliding when their rounded-box signed distance is below 0.

Agent-AV collision count. This metric counts at-fault collision events between evaluated non-ego vehicles and the AV. For each scenario, we first identify new collision events between a vehicle $i \in \mathcal V$ and the AV, where a repeated overlap between the same pair is counted only at its first collision step. A new collision event is counted only if the non-ego vehicle is judged to be at fault. Specifically, the event is ignored if the non-ego vehicle is stopped or if the AV is behind the non-ego vehicle. It is counted as at-fault if the AV is stopped, if the front bumper segment of the non-ego vehicle intersects the AV box, or if the non-ego vehicle is already off-road at the collision step. The scene-level metric is

$$
\operatorname { A A V C o l l } = \sum _ { i \in \mathcal { V } } \mathbb { 1 } \{ \exists t : \operatorname { N e w C o l l } _ { i , \operatorname { A V } } ( t ) \land \operatorname { A t F a u l t } _ { i , \operatorname { A V } } ( t ) \} .\tag{4}
$$

In the implementation, the stopped-speed threshold is 0.05 m/s, and the rear-collision test uses a $1 5 0 ^ { \circ }$ angular threshold.

Agent-AV risky TTC count. This metric counts how many evaluated non-ego vehicles produce a risky time-to-collision (TTC) with the AV. For each vehicle, the AV is considered a possible front object only when it lies ahead of the vehicle, has sufficient lateral overlap, and has a heading difference within the front-object filtering threshold. The relative closing speed is computed as $v _ { i } - v _ { \mathrm { A V } }$ . If the pair is valid and the closing speed is positive, we compute

$$
\mathrm { T T C } _ { i , \mathrm { A V } } ( t ) = \operatorname* { m i n } \left( \frac { d _ { i , \mathrm { A V } } ^ { \mathrm { l o n g } } ( t ) } { v _ { i } ( t ) - v _ { \mathrm { A V } } ( t ) } , 5 . 0 \right) ,\tag{5}
$$

where $d _ { i , \mathrm { A V } } ^ { \mathrm { l o n g } }$ is the longitudinal gap from vehicle i to the AV after accounting for vehicle extents. If the boxes already overlap, the TTC is set to 0. The scene-level metric is

$$
\mathrm { A A V T T C } = \sum _ { i \in \mathcal { V } } \mathbb { 1 } \{ \operatorname* { m i n } _ { t } \mathrm { T T C } _ { i , \mathrm { A V } } ( t ) < 0 . 5 \mathrm { s } \} .\tag{6}
$$

Agent-agent collision rate. This metric measures how often evaluated non-ego objects collide with other objects. At each future step, we compute the minimum signed distance between each evaluated object $i \in \mathcal { A }$ and all other valid objects. Self-pairs and invalid pairs are masked out. The implementation also excludes pedestrian–pedestrian, pedestrian–cyclist, and cyclist–pedestrian pairs from this metric. Let $C _ { i } ( t )$ indicate whether object i overlaps with any remaining valid object at step t. The scene-level metric is

$$
\mathrm { A A C o l l R a t e } = \frac { 1 } { | \Omega _ { \mathrm { c o l l } } | } \sum _ { ( i , t ) \in \Omega _ { \mathrm { c o l l } } } C _ { i } ( t ) ,\tag{7}
$$

where $\Omega _ { \mathrm { c o l l } }$ is the set of valid evaluated object-step pairs.

Off-road rate. This metric measures whether non-ego vehicles leave the drivable area. For each vehicle and future step, we query the nuPlan map and mark the step as off-road if the vehicle center point $( x _ { i } ( t ) , y _ { i } ( t ) )$ is not inside the DRIVABLE\_AREA layer. Vehicles whose center point is already off-road at the current frame are excluded from the denominator. The scene-level metric is

$$
\mathrm { O f f r o a d R a t e } = \frac { 1 } { | \Omega _ { \mathrm { o f f } } | } \sum _ { ( i , t ) \in \Omega _ { \mathrm { o f f } } } \mathbb { 1 } \{ ( x _ { i } ( t ) , y _ { i } ( t ) ) \not \in \mathrm { D R I V A B L E \_ A R E A } \} .\tag{8}
$$

This implementation checks the vehicle center point rather than all corners of the bounding box.

Driving-direction violation rate. This metric is an agent-level rate over non-ego vehicles. For each vehicle, we first project valid poses onto the corresponding nuPlan route baseline and compute progress along the lane centerline. A raw wrong-way violation at time t requires the vehicle to move faster than 1.0 m/s, have a heading error larger than $\dot { 7 } 5 ^ { \circ }$ relative to the lane direction, and accumulate more than 2.0 m of negative progress over a 1.0 s window. A raw violation becomes a final violation only if it persists for at least 0.5 s. The scene-level metric is

$$
\mathrm { D i r R a t e } = \frac { 1 } { \vert \mathcal { V } _ { \mathrm { d i r } } \vert } \sum _ { i \in \mathcal { V } _ { \mathrm { d i r } } } \mathbb { 1 } \{ \exists t : \mathrm { P e r s i s t W r o n g W a y } _ { i } ( t ) \} ,\tag{9}
$$

where $\nu _ { \mathrm { d i r } }$ contains vehicles with at least one valid candidate step.

Acceleration infeasibility rate. Following the Waymax kinematic infeasibility metric [77], our two kinematic metrics estimate acceleration and steering curvature from consecutive vehicle states and use the same bounds, i.e., acceleration magnitude below $6 . 0 \mathrm { m } / \mathrm { s } ^ { 2 }$ and steering-curvature magnitude below $0 . 3 \mathrm { m } ^ { - 1 }$ . We report the two violations separately as step-level rates rather than as a single kinematic-infeasibility flag. This metric measures the fraction of valid non-ego vehicle transitions that violate the acceleration bound. Velocities are taken from the trajectory state when available; otherwise they are computed from position differences. We concatenate the last history frame with the future rollout so that the first transition from history to prediction is also checked. For vehicle i and transition t,

$$
a _ { i } ( t ) = \frac { \| v _ { i } ( t + 1 ) \| _ { 2 } - \| v _ { i } ( t ) \| _ { 2 } } { \Delta t } .\tag{10}
$$

The violation indicator is $1 \{ | a _ { i } ( t ) | > 6 . 0 + 1 0 ^ { - 3 } \}$ , and the scene-level metric is the mean of this indicator over valid non-ego vehicle transitions.

Steering-curvature infeasibility rate. This metric measures the fraction of valid non-ego vehicle transitions that violate the steering-curvature bound. Let $\Delta \psi _ { i } ( t )$ be the wrapped heading change and let

$$
d _ { i } ( t ) = \| v _ { i } ( t ) \| _ { 2 } \Delta t + \frac { 1 } { 2 } a _ { i } ( t ) \Delta t ^ { 2 }\tag{11}
$$

be the approximate traveled distance over the transition. The steering curvature is computed as

$$
\kappa _ { i } ( t ) = \frac { \Delta \psi _ { i } ( t ) } { d _ { i } ( t ) } .\tag{12}
$$

When the current or next speed is below 0.6 m/s, the curvature is set to 0 to avoid unstable low-speed estimates. The violation indicator is 1 $\{ | \kappa _ { i } ( t ) | > 0 . 3 + 1 0 ^ { - 3 } \}$ , and the scene-level metric is the mean of this indicator over valid non-ego vehicle transitions.

## C.3 Details about data collection

We use Diffusion Planner as the AV planner to collect data that differ from the log. We use the official open-source model weights to perform inference on nuPlan scenarios. Following the original paper, we remove navigation information and increase the temperature to improve its multimodal capability. Diffusion Planner generates only one trajectory per inference. For each scenario, we independently repeat inference 16 times and obtain diverse trajectories through stochastic sampling in diffusion.

We build an interactive data verification tool that visualizes the scenario and candidate AV behaviors and displays information such as speed and TTC, making it easier for annotators to select candidates and verify whether the filtered AV behaviors satisfy our requirements.