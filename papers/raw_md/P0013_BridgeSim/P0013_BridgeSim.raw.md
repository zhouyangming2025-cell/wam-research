# BridgeSim: Unveiling the OL-CL Gap in End-to-End Autonomous Driving

Seth Z. Zhao<sup>1∗</sup>, Luobin Wang<sup>2∗</sup>, Hongwei Ruan<sup>2</sup>, Yuxin Bao<sup>1</sup>, Yilan Chen<sup>2</sup>, Ziyang Leng<sup>1</sup>, Abhijit Ravichandran<sup>2</sup>, Honglin He<sup>1</sup>, Zewei Zhou<sup>1</sup>, Xu Han<sup>1</sup>, Abhishek Peri<sup>3</sup>, Zhiyu Huang<sup>1</sup>, Pranav Desai<sup>3</sup>, Henrik Christensen<sup>2</sup>, Jiaqi Ma<sup>1</sup>, Bolei Zhou<sup>1†</sup> <sup>1</sup>UCLA <sup>2</sup>UCSD <sup>3</sup>Qualcomm https://vail-ucla.github.io/BridgeSim/

Abstract: Open-loop (OL) to closed-loop (CL) gap (OL-CL gap) exists when OL-pretrained policies scoring high in OL evaluations fail to transfer effectively in closed-loop (CL) deployment. In this paper, we unveil the root causes of this systemic failure and propose a practical remedy. Specifically, we demonstrate that OL policies suffer from Observational Domain Shift and Objective Mismatch. We show that while the former is largely recoverable with adaptation techniques, the latter creates a structural inability to model complex reactive behaviors, which forms the primary OL-CL gap. We find that a wide range of OL policies learn a biased Q-value estimator that neglects both the reactive nature of CL simulations and the temporal awareness needed to reduce compounding errors. To this end, we propose a Test-Time Adaptation (TTA) framework that calibrates observational shift, reduces state-action biases, and enforces temporal consistency. Extensive experiments show that TTA effectively mitigates planning biases and yields superior scaling dynamics than its baseline counterparts. Furthermore, our analysis highlights the existence of blind spots in standard OL evaluation protocols that fail to capture the realities of closed-loop deployment.

Keywords: Autonomous Driving, Closed-loop Simulation, Test-time Adaptation

## 1 Introduction

A growing number of works in end-to-end (E2E) autonomous driving have directed their efforts toward achieving high scores on open-loop (OL) benchmarks such as nuScenes [1] and NAVSIM [2, 3], with some reporting performance at or near human level [4, 5]. However, the trajectories output from OL policies frequently become infeasible or unsafe when deploying in closed-loop (CL) simulation, which shows strong discrepancy with their claimed behaviors under OL evaluations [6, 7, 8, 9]. We refer to such a discrepancy as the OL-CL gap in E2E driving.

Unveiling the OL-CL gap matters for avoiding hallucinated conclusions from OL benchmarks. We illustrate our motivations in Fig. 1. First, success in OL benchmarks might create a misleading proxy for driving behavior in realistic conditions. Recent works [6, 7, 8] have demonstrated a lack of correspondence between OL and CL performance under similar domain settings. Furthermore, this correlation decays as the simulation horizon increases (see Fig. 3). Second, OL scaling laws fail to predict CL scaling. While recent studies show that OL performance scales predictably with data volume and test-time compute, neither of these relationships transfers reliably to CL deployment [10, 11]. These discrepancies suggest that OL evaluation protocols, while being a practical and scalable proxy for costly CL simulation [1, 12, 3, 2, 13], might be biased and overlook the underlying objectives that real-world driving policies should optimize.

![](images/1a1730f38106b8c20254136a4b75f9e1e0b0ba68f60797e1e7492e796af236b8.jpg)  
Figure 1: Motivation. (a): Open-loop (OL) train-test paradigms do not necessarily align with the objectives and evaluation metrics in closed-loop (CL) deployment; (b): This mismatch results in significant performance discrepancies, characterized by decaying correlation and diverging scaling dynamics; (c): We attribute this OL-CL gap to observational domain shift and objective mismatch. In this paper, our goal is not to criticize OL evaluation protocols or the development of methods drawn from OL evaluations, but rather to clarify where policies might fail and what adaptations are needed to mitigate failures in CL deployment. Our key contributions are summarized as follows:

1. Identify the fundamental failure modes of the OL-CL gap in E2E autonomous driving. We trace the OL-CL gap to two distinct sources. First is Observational Domain Shift, where sensor observations at test time differ from those seen during training. This distributional shift degrades perception before planning even begins (so-called sim-to-sim<sup>3</sup> gap [14]). While our study underscores that domain adaptation can restore much of the lost perceptual fidelity, resolving the domain gap alone does not prevent CL failure. The second and more fundamental source is the Objective Mismatch between OL training and CL testing. More specifically, OL training optimizes against static trajectory-matching objectives that do not correspond to true closed-loop returns, and in doing so produces Q-value estimates that are biased and overfit to the pretrained simulators. Such bias is structural and persists regardless of how well the perceptual inputs are calibrated.

2. Propose a test-time adaptation (TTA) framework that mitigates CL deployment failure. The framework comprises a flow-matching-based observational calibrator that performs cross-domain observational alignment between the training and deployment environments, and a training-free adaptation mechanism that addresses structural misalignment. Specifically, we adapt the OL policy via an truncated Q-value estimator that corrects the scoring bias introduced by OL training objectives, and an adaptive replan mechanism enables reactive replanning as environmental dynamics evolve. Together, these components mitigate the above-mentioned OL-to-CL deployment failures. Across diverse scenarios in CL simulation, our approach improves CL performance by up to 22% on baseline methods and reveals more favorable scaling behavior with adaptation than baseline policies.

3. Introduce BridgeSim, a cross-simulator E2E closed-loop simulation platform. To complement existing E2E benchmarks, we develop a comprehensive platform designed for the rigorous, dynamic evaluations of any E2E driving policy under interactive, closed-loop settings.

## 2 Related Work

Driving Simulators and Benchmarks. Driving simulators and benchmarks have long been recognized as crucial tools for training and evaluating autonomous driving systems, providing safe, efficient, and repeatable environments for developing algorithms [15, 16, 17, 18, 19]. A variety of traditional game-engine-based and high-fidelity simulators, such as GTA V [20], Sim4CV [21], AIRSIM [22], and CARLA [23], offer configurable environments and complex physical condition modeling. Similarly, lightweight platforms like DeepDrive [24] and DriverGym [25] provide simpli fied dynamics for fast experimentation, while simulators like MetaDrive [26] focus on modularity, scalability, and multi-agent interaction-rich scenarios. Despite their utility, these traditional platforms often suffer from domain gaps due to handcrafted assets and limited visual realism. More recent efforts have explored data-driven and generative simulation frameworks to bridge this gap. DriveArena [27] synthesizes realistic traffic scenes to facilitate iterative perception-action loops. HUGSIM [28] and RAD [29] further advance this direction by leveraging 3D Gaussian Splatting for real-time, photorealistic scene reconstruction and closed-loop simulation. Complementing these, ReconDreamer and ReconDreamer-RL [30, 31] demonstrate a world-model-based reconstruction framework to address limitations in representing novel trajectories. However, existing generative simulation frameworks still suffer from simulation artifacts and lack of metric annotations to evalu ate E2E policies (see Appendix E).

End-to-end Autonomous Driving. Traditional autonomous driving systems inherit a modular design comprising perception, prediction, and planning modules, which suffer from error propagation and information loss [32, 33, 34, 35]. Subsequently, recent research has shifted towards an integrated end-to-end (E2E) paradigm, which maps raw sensor inputs directly to control commands. UniAD [36] integrates modules into a unified framework and utilizes rasterized representations for information flow. VAD [37] further optimizes the efficiency by replacing dense grids with instance-centric vectorized representation, while TransFuser [38] extends inputs to multi-modalities. More recently, DiffusionDrive and DiffusionDriveV2 [39, 40] model the multi-modal distribution of actions through diffusion policy. DrivoR [5] utilizes register tokens to avoid complex intermediate representation while maintaining superior performance. Despite the improved performance on planning evaluation metrics, recent works like AD-MLP, PDM-Close, BEV-Planner, LEAD, and RAP [41, 42, 7, 43, 4] point out the limitations of open-loop (OL) benchmarks and reveal the necessity of bridging the OL-CL gap. While closed-loop (CL) training for E2E policies mitigates the gap, it presents greater complexity and computation costs [44]. Instead, this work attributes the OL-CL gap in E2E driving to two distinct factors and formulates closing the gap via test-time adaptation.

Table 1: Comparisons with other E2E open-loop and closed-loop benchmarks. MV-Consistency: multi-view temporal consistency, TF-Consistency: Traffic elements annotations consistency. PG: procedural map and behavior generation. See Appendix B for more details of BridgeSim platform.
<table><tr><td>Name</td><td>Closed-loop</td><td>Long-term Simulation</td><td>MV-Consistency</td><td>TF-Consistency</td><td>Supported Maps</td><td>Supported Traffic Modes</td></tr><tr><td>NAVSIM [3, 2]</td><td>X</td><td>X</td><td>√</td><td>V</td><td>nuPlan</td><td>Log-replay</td></tr><tr><td>Bench2Drive [6]</td><td>V</td><td>√</td><td>√</td><td>√</td><td>CARLA</td><td>IDM</td></tr><tr><td>DriveArena [27]</td><td>√</td><td>V</td><td>×</td><td>X</td><td>nuScenes</td><td>Log-replay</td></tr><tr><td>HUGSIM [28]</td><td>√</td><td>√</td><td>√</td><td>X</td><td>nuScenes, Waymo, KITTI-360, PandaSet</td><td>Log-replay, IDM, Adversarial</td></tr><tr><td>BridgeSim (ours)</td><td>√</td><td>√</td><td>√</td><td>√</td><td>CARLA, Waymo, nuScenes, nuPlan, PG</td><td>Log-replay, IDM, Adversarial</td></tr></table>

## 3 BridgeSim: A Unified Cross-Simulator Closed-loop Simulation Platform for E2E Driving Policies

To empirically investigate the OL-CL gap with quantifiable rigor, we introduce BridgeSim, a crosssimulator platform designed to evaluate OL pretrained policies within high-fidelity CL environments. BridgeSim designs a unified scenario protocol to incorporate diverse map scenarios (e.g., nuPlan [12], WOMD [45], and nuScenes [1]) with heterogeneous traffic modes (e.g., log-replay, IDM [46], and adversarial policies [47]) to stress-test E2E driving policies under a closed-loop simulation environment. Furthermore, BridgeSim offers a flexible deployment setting to simulate open-loop policy with varying execution frequencies and simulation horizons. Consequently, BridgeSim bridges the critical divide between OL benchmarks limited to short-term static prediction and existing CL benchmarks that often lack the comprehensive functionalities and annotations required for complex, reactive stress-testing. A comprehensive functional comparison between BridgeSim and other prominent E2E benchmarks is provided in Table 1.

## 4 Decomposing the Open-Loop to Closed-Loop (OL-CL) Gap

In this section, we revisit the theoretical formulation of the E2E driving task and analyze the failure modes of OL-CL gap, namely observational domain shift and objective mismatch. Through empirical studies, we further illustrate the performance drop caused by those factors, which motivate the design of a test-time adaptation framework that recovers the OL policies from failures.

## 4.1 Preliminaries and Notations

POMDP Formalism. We formalize the end-to-end driving task as a Partially Observable Markov Decision Process (POMDP), defined by the tuple $\langle S , A , \mathcal { O } , \mathcal { T } , \Omega , r , \gamma , \rho _ { 0 } , T \rangle$ . Here, S denotes the true underlying state space of the environment, A is the ego-vehicle’s action space, and O is the high-dimensional observation space. At time step t, the system occupies state $s _ { t } \in S$ . The agent receives an observation $o _ { t } \in \mathcal { O }$ governed by the emission distribution $\Omega ( o _ { t } \mid s _ { t } )$ , executes an action $a _ { t } \in { \mathcal { A } }$ , and the environment evolves via $\mathcal { T } ( s _ { t + 1 } \mid s _ { t } , a _ { t } )$ . The episode proceeds for a finite horizon of T steps, where $\rho _ { 0 } ( s _ { 0 } )$ represents the initial state distribution and $\gamma \in [ 0 , 1 )$ is the discount factor.

End-to-End Driving Policy. We consider end-to-end (E2E) driving policies represented as stochastic mappings $\pi _ { \theta , \phi } ^ { d }$ parameterized by the observation domain d ∈ {source, target}, observation encoder parameters θ and behavior decoder parameters $\phi .$ We consider policies that predict $\mathbf { a } _ { t } \in \mathcal { A } ^ { 4 }$ which is a sequence of actions. Agents receive observations $o _ { t } ~ \in ~ \mathcal { O }$ of underlying environment states $s _ { t } ~ \in ~ S$ through domain-dependent emission distribution $\Omega ^ { d } ( o _ { t } \mid s _ { t } )$ . This setting allows us to isolate observational domain shifts from the behavioral counterpart. Specifically, an encoder $f _ { \theta } : \mathcal { O }  \mathcal { Z }$ maps raw observations to a latent scene representation $z \in { \mathcal { Z } }$ , while the policy head $\pi _ { \phi } ( \mathbf { a } _ { t } \mid z _ { t } )$ generates the ego-vehicle’s future trajectory. The joint distribution of the E2E policy can then be factorized into components over the action sequence, latent representation, and observation $\left( \mathbf { a } _ { t } , z _ { t } , o _ { t } \right)$ conditioned on state $s _ { t } \mathbf { . }$

$$
\pi _ { \theta , \phi } ^ { d } ( \mathbf { a } _ { t } , z _ { t } , o _ { t } \mid s _ { t } ) \triangleq \pi _ { \phi } ( \mathbf { a } _ { t } \mid z _ { t } ) P _ { \theta } ( z _ { t } \mid o _ { t } ) \Omega ^ { d } ( o _ { t } \mid s _ { t } ) ,\tag{1}
$$

where $P _ { \theta } { \left( z _ { t } \mid o _ { t } \right) }$ denotes the encoder-induced conditional distribution. Recent works [39, 40, 4] usually use a deterministic encoder $z _ { t } = f _ { \theta } ( o _ { t } )$ , we may write $P _ { \theta } ( z _ { t } \mid o _ { t } ) = \delta ( z _ { t } - f _ { \theta } ( o _ { t } ) )$ .

Closed-loop Objective. We seek to maximize the performance of a driving policy π via the expected closed-loop cumulative return $J ( \pi ) \triangleq \mathbb { E } _ { s _ { 0 } \sim \rho _ { 0 } , \tau \sim \pi } \left[ \sum _ { t = 0 } ^ { T } \gamma ^ { t } r ( s _ { t } , a _ { t } ) \right]$ , where the reward $r ( s _ { t } , a _ { t } )$ evaluates the executed control $a _ { t } .$ , which typically constitutes only a partial subset of the full sequence $a _ { t : t + H }$ generated by the policy at each time step.

## 4.2 Observational Domain Shift

Failure mode analysis. Observational domain shift occurs when observation encoder fails to extract coherent semantic features (e.g., lane, objects, etc.) in the target environment and impairs the state observability required for planning, as illustrated in Fig. 2(a). To denote the impact of this domain shift on task performance, we define the Observational Domain Gap $\Delta _ { \mathrm { o b s } }$ as:

$$
\Delta _ { \mathrm { o b s } } ( \theta , \phi ) \triangleq J ( \pi _ { \theta , \phi } ^ { \mathrm { s o u r c e } } ) - J ( \pi _ { \theta , \phi } ^ { \mathrm { t a r g e t } } ) ,\tag{2}
$$

where an identical control head $\pi _ { \phi }$ isolates the degradation in expected return attributable solely to domain shift. The discrepancy between source and target domains can be measured by:

$$
\mathrm { D i s t } _ { Z } ( s ; \theta ) \triangleq \mathrm { D i s t } \Big ( P _ { \theta } ( z \mid o ) \Omega ^ { \mathrm { s o u r c e } } ( o \mid s ) , ~ P _ { \theta } ( z \mid o ) \Omega ^ { \mathrm { t a r g e t } } ( o \mid s ) \Big ) ,\tag{3}
$$

where $\operatorname { D i s t } ( \cdot , \cdot )$ is the distance metric over distributions on Z. With this formulation, we hypothesize that observational domain gap is recoverable as long as we calibrate the observation encoder θ to minimize the distributional distance.

![](images/ff5916d86fbea6ea5d388dc56dd77ee16bb6bc4af33fd8edfd0f6d02456efac2.jpg)  
(a) Calibration Process

![](images/eb94588c5235c273f51b3bcb1e38cf07edc9a57636b93cb84eb03451da5ccea1.jpg)

![](images/d181040619b85ccf8cf6775984f6bd1d424de93c9c45445afb3db639ba51eb79.jpg)  
(b) Calibration Efects  
Figure 2: Empirical Study on Observational Domain Shift. (a): Flow-matching procedure for observational calibration; (b): Calibration effects on OL and CL metrics. See Appendix D.2 for experimental details.

Empirical studies. To test this hypothesis, we isolate and quantify $\Delta _ { \mathrm { o b s } }$ to examine policy behavior under observational domain shift, as depicted in Fig. 2(b). To explicitly decouple observational errors from compounding closed-loop dynamics (e.g., control drift), we conduct an open-loop ablation study. By varying only the input observation domain while holding the underlying state transitions constant, we measure the trajectory deviation from the expert ground truth following the protocol in [48]. We find that under observational shift, policy performance degrades dramatically as the perception module fails to extract the semantic information necessary for planning. However, applying our practical calibration method (Section 5.1) successfully recovers these scene features and minimizes the gap. These results unveil that: although observational domain shift degrades perception before planning, it is largely a recoverable failure for driving policy, and targeted calibration could effectively restore its state observability and closes the domain gap.

## 4.3 Objective Mismatch

Failure mode analysis. Objective mismatch occurs when OL policy’s training objective optimizes for a static full-sequence objective that ignores the reactive, receding-horizon reality of CL deployment during test-time, where the agent predicts a trajectory of length H but only executes a short prefix of k steps before receiving a new observation and performing replan. In actual CL simulation, the Unified Closed-loop Objective<sup>5</sup> parameterized by the execution horizon k is defined as:

$$
J _ { k } ( \pi ) = \mathbb { E } _ { s _ { 0 } \sim \rho _ { 0 } , \tau \sim \pi _ { k } } \left[ \sum _ { c = 0 } ^ { T / k - 1 } \gamma ^ { c \cdot k } \sum _ { i = 0 } ^ { k - 1 } \gamma ^ { i } r ( s _ { c \cdot k + i } , a _ { c \cdot k + i } ) \right] ,\tag{4}
$$

where $\pi _ { k }$ denotes the policy perform replan at a frequency of $1 / k$ and c denotes the planning cycles. This formulation enables us to decompose the OL-to-CL degradation brought by objective mismatch in two dimensions, namely biased Q-value estimation and compounding execution error.

![](images/c64401117c9fedc2d1bf5890fc468232411eaf685b3328bab12fc4a14922b2de.jpg)

![](images/3cff225fb22cf16920e1d14bc73a75f580dcb7cda81bffda224928aada495389.jpg)

![](images/19363e0d289898c9c9164159883b50bcbb2053ed978140b4361a60904e561706.jpg)  
Figure 3: Empirical Study on Objective Mismatch. (a): Compounding execution error of $J ( \pi )$ w.r.t. execution horizon k; (b): $J ( \pi )$ under CL and OL objectives, where the divergence between these curves constitutes the objective mismatch gap $( \Delta _ { \mathrm { o b j } } ) ;$ (c): OL-CL Pearson correlation under different traffic modes w.r.t. simulation horizon T. See Appendix D.3 for experimental details.

Biased Q-value estimation is a byproduct of OL training, as E2E planners are typically optimized to minimize errors over the entire predicted sequence H. This is mathematically equivalent to optimizing an OL objective $J _ { \mathrm { O L } } ( \pi ) \approx J _ { H } ( \pi )$ , where the execution horizon k is implicitly forced to equal the planning horizon H. Under $J _ { H } ( \pi )$ , future states are unrolled via open-loop kinematic assumptions, inherently ignoring environmental stochasticity, compounding covariate shift, and the reactive behaviors of other traffic participants. Consequently, these offline proxy distributions remain fundamentally disconnected from the true closed-loop state-visitation distribution $d ^ { \pi _ { \theta , \phi } }$ induced by high-frequency active execution.

Parallel to this, the static nature of OL training fails to instill the temporal robustness required for sequential decision-making, which makes policies susceptible to compounding execution errors. Since the policy is not trained to maintain stability across consecutive, high-frequency executions, the vanilla k-step execution strategy hardly achieves optimal closed-loop return as illustrated in Fig. 3(a). We formalize the cumulative performance degradation resulting from these factors as the Objective Mismatch Gap:

$$
\Delta _ { \mathrm { o b j } } ( \theta ) \triangleq J _ { k ^ { * } } ( \pi _ { \theta , \phi _ { \mathrm { C L } } } ) - J _ { k = H } \big ( \pi _ { \theta , \phi _ { \mathrm { O L } } } \big ) ,\tag{5}
$$

where $\phi _ { \mathrm { C L } }$ represents the decoder parameters optimized under the unified CL objective (via optimal execution $k { * } )$ over the induced distribution $d ^ { \pi _ { \theta , \phi } }$ , whereas $\phi _ { \mathrm { O L } }$ represents the decoder optimized exclusively via the OL proxy $( k = H )$ under the offline expert state distribution. Based on this formalization, we hypothesize that objective mismatch forms the primary structural barrier to CL transfer. Specifically, we expect that relying on the OL proxy will cause diverging optimization targets that would not maximize CL returns.

Empirical studies. To test this hypothesis, we empirically characterize the objective mismatch $( \Delta _ { \mathrm { o b j } } )$ relative to the simulation horizon T across a representative family of E2E policies [39, 40, 38, 4], as illustrated in Fig. 3(b). As illustrated in Fig. 3(b), we track the divergence on the returns under OL and CL objectives. Crucially, the performance gap widens significantly exactly as T exceeds H. This trend confirms our hypothesis, revealing that the biased Q-value estimation is insufficient for evaluating state-action values during long-horizon interaction. Furthermore, Fig. 3(c) shows a drastic decay in the Pearson correlation between OL and CL metrics as $T > H$ , proving that standard OL evaluations might yield misleading conclusions about CL deployment readiness. Our analysis demonstrates that: the main OL-CL gap lies in the objective mismatch, where test-time adaptation is needed to explicitly correct biased Q-value estimations and sequential decisionmaking during CL executions.

## 5 Proposed Method: Test-time Adaptation (TTA) Framework

Motivated by the decomposition analysis in Section 4, we propose a test-time adaptation (TTA) framework that improves closed-loop robustness of OL-pretrained E2E policies without additional end-to-end retraining. The framework consists of an observational calibrator that recovers latent representations via flow-matching (Section 5.1) and a policy adaptation procedure to mitigate biased Q-value estimation and adaptively perform execution to maximize final CL return (Section 5.2).

## 5.1 Observational Calibrator

As illustrated in Section 4.2, we formalize the observational shift at the level of latent representations induced by the observation channel under a fixed vision encoder. Let $f _ { \theta } : \mathcal { O }  \mathcal { Z }$ be a pretrained encoder, and let $\Omega ^ { \mathrm { s o u r c e } } ( \cdot \mid s )$ and $\Omega ^ { \mathrm { t a r g e t } } ( \cdot \mid s )$ denote the observation channels in the source and target domains, respectively. For each domain d ∈ {source, target}, given a domain-specific state distribution $\rho ^ { d }$ , we define the induced representation distribution $\mathcal { D } _ { d }$ as the marginal law of $z = f _ { \theta } ( o )$ under the generative process $s \sim \rho ^ { d }$ and $o \sim \Omega ^ { d } ( \cdot \mid s )$ . Note that $\mathcal { D } _ { \mathrm { s o u r c e } }$ and $\mathcal { D } _ { \mathrm { t a r g e t } }$ are both supported on $\mathcal { Z }$ but generally differ due to the domain-dependent sensing model.

We then use flow-matching to learn a transport map $g : \mathcal { Z }  \mathcal { Z }$ that aligns these distributions in the push-forward sense, i.e., $g _ { \# } \mathcal { D } _ { \mathrm { s o u r c e } } \approx \mathcal { D } _ { \mathrm { t a r g e t } }$ [49], so that latent features extracted from sourcedomain observations can be mapped into representations that are compatible with the downstream policy $\pi _ { \phi }$ . To improve the alignment performance, we do not rely solely on a vanilla flow-matching objective; instead, we optimize the calibrator using a multi-objective loss inspired by [50]. We show that such calibration effectively mitigates the observational domain shift by demonstrating its latent feature alignment and the resulting recovery of OL and CL metrics in Fig. 2. See Appendix C.1 for the exact formulation of the multi-objective loss and further implementation details about dataset construction and model architecture.

![](images/ce88e7bda701a689664b99a8120225439ec37fc1a74c09b9cfaa653d42364919.jpg)

![](images/eee1533ac93684228295ba191ed7bb79f8436ffa711b6b2a01ba681a767f654a.jpg)  
Figure 4: Test-time Policy Adaptation. (a): Truncated Q-value estimator selects safe planned trajectories during closed-loop execution; (b): Adaptive replan preserves previously verified planned trajectories if the newly proposed trajectory doesn’t obtain higher Q-values; (c): Test-time scaling dynamics between biased (baseline) and truncated Q-value estimators (TTA).

## 5.2 Test-time Policy Adaptation

## 5.2.1 Truncated Q-value Estimation

To address the bias inherent in Q-values estimator learned via open-loop proxy objectives, we propose a dynamic, test-time truncated action-value estimator. At any decision step $t ,$ the stochastic policy $\pi _ { \theta , \phi } ^ { \Omega } ( \cdot \mid s _ { t } )$ outputs a discrete set of N candidate trajectory-actions, denoted as ${ \mathcal { A } } =$ $\{ \mathbf { a } ^ { ( 1 ) } , \ldots , \mathbf { a } ^ { ( \dot { N } ) } \}$ . Each candidate $\mathbf { a } ^ { ( i ) }$ represents a distinct spatial-temporal plan composed of primitive controls over the full planning horizon H.

Evaluating the quality of a chosen prefix trajectory typically relies on the sum of immediate rewards over the k-step execution prefix and the expected future return $\gamma ^ { k } \mathbb { E } [ V ^ { \pi } ( s _ { t + k } ) ]$ . However, this standard expected return implicitly accumulates rewards infinitely into the future. Relying on an open-loop transition model to estimate states far beyond the explicit planning horizon H inherently introduces compounding covariate shifts and unmodeled environmental stochasticity, making the unbiased estimation intractable in practice.

To overcome this, we bound the estimation strictly to the reliable planning horizon H by introducing a truncated action-value estimator:

$$
\hat { Q } ^ { \pi } ( s _ { t } , \mathbf { a } _ { t } ) \triangleq R _ { k } ( s _ { t } , \mathbf { a } _ { t } ) + \boldsymbol { \gamma } ^ { k } \mathbb { E } \left[ V ^ { \pi } ( s _ { t + k } ) \right] - \boldsymbol { \gamma } ^ { H } \mathbb { E } \left[ V ^ { \pi } ( s _ { t + H } ) \right] ,\tag{6}
$$

where $\gamma \in [ 0 , 1 )$ is the discount factor, and $\begin{array} { r } { R _ { k } ( s _ { t } , \mathbf { a } _ { t } ) = \sum _ { i = 0 } ^ { k - 1 } \gamma ^ { i } r ( s _ { t + i } , \mathbf { a } _ { t + i } ) } \end{array}$ captures the immediate geometric and historical penalties strictly over the execution prefix k.

By explicitly subtracting the discounted expected value at the terminal horizon limit $\gamma ^ { \dot { H } } \mathbb { E } [ V ^ { \overline { { \pi } } } ( s _ { t + H } ) ]$ , we mathematically cancel out the intractable infinite tail. This ensures that the value estimation beyond H is safely ignored, restricting the estimator to evaluate only the highconfidence window bounded by the model’s explicit spatial-temporal plan. The implementation of the expected Q-function is detailed in Appendix C.2.

As illustrated in Fig. 4(a), during closed-loop execution, rather than defaulting to the best-scoring sequence from the biased open-loop policies [40, 39], the agent selects the candidate trajectory that maximizes ${ \hat { Q } } ^ { \pi }$ . Operating continuously at each decision step, this mechanism dynamically filters out plans that suffer from the biased estimation defined in Section 4.3.

## 5.2.2 Adaptive Replan

Standard test-time scorers typically operate in a memoryless fashion by selecting exclusively from the current candidate set $\boldsymbol { A } _ { t }$ proposed by the policy, which often leads to high-frequency action chattering and temporal inconsistency across consecutive planning cycles. To overcome compounding execution errors, we preserve the unexecuted waypoints of a previously verified plan and propose an adaptive replan mechanism that adaptively executes replan when needed, as illustrated in Fig. 4(b).

Let $\mathbf { a } _ { \mathrm { p r e v } } ^ { * }$ be the optimal trajectory selected during the previous planning cycle (at step t − k). At the current decision step t, the agent has completed the k-step execution prefix. To rigorously evaluate whether to retain the existing plan, we extract its unexecuted remainder, containing H−k waypoints, and spatially transform it into the ego-centric coordinate frame at $s _ { t }$ . We denote this transformed persistent plan as $\mathbf { a } _ { \mathrm { r e m } }$ . To ensure a fair comparison against the newly generated candidates $\mathbf { a } \in \mathcal { A } _ { t } ,$ we evaluate the truncated action-value of $\mathbf { a } _ { \mathrm { r e m } }$ against the corresponding $( H - k ) { \mathrm { - s t e p } }$ prefix of each new candidate, which we denote as $\mathbf { a } _ { [ : H - k ] }$ . The expected return is estimated using the ${ \hat { Q } } ^ { \pi }$ formulation in Eq. 6 integrated over this shortened horizon.

We retain the persistent plan if its estimated Q-value equals or exceeds that of the corresponding prefix of any new candidate:

$$
\mathbf { a } _ { t } ^ { * } = \left\{ \begin{array} { l l } { \mathbf { a } _ { \mathrm { r e m } } } & { \mathrm { i f } \ \hat { Q } ^ { \pi } ( s _ { t } , \mathbf { a } _ { \mathrm { r e m } } ) \geq \displaystyle \operatorname* { m a x } _ { \mathbf { a } \in \mathcal { A } _ { t } } \hat { Q } ^ { \pi } ( s _ { t } , \mathbf { a } _ { [ : H - k ] } ) , } \\ { \arg \displaystyle \operatorname* { m a x } _ { \mathbf { a } \in \mathcal { A } _ { t } } \hat { Q } ^ { \pi } ( s _ { t } , \mathbf { a } ) } & { \mathrm { o t h e r w i s e } . } \end{array} \right.\tag{7}
$$

The agent abandons the persistent plan only when a newly generated candidate yields a strictly superior expected return over the shared temporal horizon.

## 6 Experiments

## 6.1 Experimental Settings

We utilize the BridgeSim platform as the simulation engine and benchmarks where the scenarios and traffic modes could be loaded via scenario descriptions as referred in Appendix B. Baseline methods include DiffusionDrive [39], DiffuionDriveV2 [40], and RAP [4], which are pretrained in NAVSIM [2]. We evaluate the proposed TTA framework under: 1) In-domain evaluation: the model would be tested in the log-replay scenarios in NavHard test set under different simulation horizons, and 2) Unseen scenes evaluation: the model would be tested in the log-replay scenarios different from pretrained domains, e.g., nuScenes [1], WOMD [45]; 3) Reactive evaluation: the model would be tested in NavHard scenarios where traffic agents would be replaced with IDM [46] or adversarial mode [47]. The closed-loop metrics include a BridgeSim Driving Score (DS), which is a composite score of Extended Predictive Driver Model Score (EPDMS) score and Route Completion (RC). Note that EPDMS is a composite metric based on No At-Fault Collisions (NC), Drivable Area Compliance (DAC), Traffic Light Compliance (TLC), Driving Direction Compliance (DDC), Lane Keeping (LK), Time-to-Collision (TTC), History Comfort (HC), and Extended Comfort (EC). See Appendix B.4 for metric details and Appendix D.1 for more experimental details.

## 6.2 Main Results

In-domain evaluation results. As illustrated in Fig. 5(a), we evaluate the log-replay scenarios under the BridgeSim-NavHard scenarios under different simulation horizons of 4/8/12/16 seconds. The reliability of E2E planners typically degrades as the simulation horizon increases due to compounding covariate shifts. Noticeably, the integration of TTA significantly flattens this decay curve across all baseline agents. By performing test-time adaptation that aligns the CL, the framework mitigates the Objective Mismatch issue. The results demonstrate that TTA allows the agents to maintain higher temporal consistency and safety scores in long-horizon CL simulation.

Unseen scenes evaluation results. As illustrated in Fig. 5(b), the proposed TTA framework yields consistent performance gains when integrated with diverse open-loop baselines [39, 40, 4]. These improvements are sustained across three distinct evaluation environments, namely NavHard [2], nuScenes [1], and WOMD [45], demonstrating the framework’s cross-domain robustness.

![](images/60f7440aff8ec078fe1ec46e1f227d01308cb8e211db16f42c5499f4ce06479a.jpg)

![](images/3b212924cc7d4d6c7556d94098a3c19f036ead601d087d1dc8c2a3203ae9ee32.jpg)

![](images/3f134c037521e45f15e08c7635785782ae1f182148c1a859829d6aabd54f20ed.jpg)  
Figure 5: Improvements of proposed TTA framework. (a): Performance gain under different simulation horizons on BridgeSim-NavHard scenarios; (b): Performance gain under different logreplay domains; (c): Component analysis of TTA framework.

Reactive evaluation results. As illustrated in Table 2, we evaluate the performance gains provided by the proposed TTA framework across diverse traffic modes. Our results indicate that TTA consistently improves key CL metrics, such as progress-related metrics (RC) and safety-related metrics (TTC and NC), across all baseline architectures. These results demonstrate the effectiveness of the TTA framework in achieving efficiency with robust safety constraints in reactive simulations.

Component Analysis. As illustrated in Fig. 5(c), we decouple the contributions of each TTA module to evaluate their individual impact on final performance. Our results indicate that the proposed truncated Q-value estimator significantly outperforms the original biased baseline across all tested execution horizons k. Furthermore, the addition of the adaptive replan mechanism consistently identifies optimal rollout trajectories and effectively mitigates compounding execution errors, leading to more robust and stable driving scores across different backbones.

Table 2: Performance comparisons with different reactive traffic modes. Note that TTA improves key closed-loop metrics such as NC, TTC, and RC, resulting in overall higher DS. See Appendix D.4 for complete sub-metric scores.
<table><tr><td rowspan="2">Model</td><td colspan="7">IDM</td><td colspan="7">Safety-Critical</td></tr><tr><td>DS</td><td>EPDMS</td><td>RC</td><td>NC</td><td>DAC</td><td>TTC</td><td>LK</td><td>DS</td><td>EPDMS</td><td>RC</td><td>NC</td><td>DAC</td><td>TTC</td><td>LK</td></tr><tr><td>DiffusionDrive</td><td>45.30</td><td>72.95</td><td>59.93</td><td>95.41</td><td>85.47</td><td>89.73</td><td>89.83</td><td>38.68</td><td>68.16</td><td>54.77</td><td>93.62</td><td>83.86</td><td>84.97</td><td>90.71</td></tr><tr><td>DiffusionDriveV2</td><td>31.94</td><td>65.43</td><td>45.85</td><td>94.57</td><td>82.09</td><td>89.10</td><td>85.42</td><td>28.17</td><td>61.45</td><td>43.50</td><td>93.15</td><td>80.78</td><td>85.72</td><td>85.81</td></tr><tr><td>RAP</td><td>60.02</td><td>76.85</td><td>77.20</td><td>97.68</td><td>88.84</td><td>93.07</td><td>78.16</td><td>51.83</td><td>70.88</td><td>71.22</td><td>95.03</td><td>88.16</td><td>86.37</td><td>78.26</td></tr><tr><td>TTA (DiffusionDrive)</td><td> $6 2 . 6 8 + 1 7 . 4$ </td><td>84.36</td><td>72.28</td><td>96.85</td><td>95.63</td><td>91.57</td><td>92.43</td><td> $5 5 . 0 2 \substack { + 1 6 . 3 }$ </td><td>78.95</td><td>67.92</td><td>94.73</td><td>95.21</td><td>86.64</td><td>91.30</td></tr><tr><td>TTA (iffusionDriveV2)</td><td> $5 3 . 9 6 \substack { + 2 2 . 0 }$ </td><td>77.47</td><td>67.89</td><td>96.08</td><td>90.53</td><td>89.46</td><td>89.98</td><td> $4 7 . 6 4 + 1 9 . 5 $ </td><td>71.66</td><td>65.91</td><td>93.54</td><td>89.16</td><td>84.23</td><td>90.11</td></tr><tr><td>TTA (RAP)</td><td> $7 9 . 0 7 \substack { + 1 9 . 1 }$ </td><td>90.92</td><td>86.21</td><td>98.28</td><td>98.62</td><td>95.31</td><td>91.52</td><td> $\mathbf { 6 5 . 9 4 \times } \mathbf { \ x } \mathbf { \ x }$ </td><td>82.01</td><td>78.66</td><td>95.30</td><td>96.19</td><td>87.71</td><td>90.26</td></tr></table>

Test-time Scaling Dynamics. We show the benefits of test-time scaling of trajectory proposals in OL metrics following [39, 40, 51, 52]. As illustrated in Fig. 4(c), the comparative experiments across different scoring mechanisms in CL simulation indicate that test-time scaling dynamics is highly dependent on the quality of the scorer. Our proposed scorers consistently benefit from scaling with broader state-visitations, whereas biased Q-value estimators could not reach similar improvements.

## 7 Conclusion

In this work, we provide an in-depth analysis of the OL-CL gap in E2E autonomous driving and show that OL optimization does not guarantee safe or stable behavior on long-horizon CL simulation. Consequently, our analysis reveals that simply scaling OL training is insufficient for realistic deployment. Instead, targeted test-time adaptation, such as our proposed TTA framework, needs to be applied to both the observation and policy modules to obtain safe and robust driving behaviors in CL deployment. Our findings also suggest that E2E driving has reached the saturation point in OL benchmarks. At this plateau, the reliability of the predictive power of OL metrics for real-world, closed-loop capabilities remains in question. For future directions, we believe that E2E driving research should shift its focus towards more realistic CL evaluation and objective-aligned learning that directly improves driving models in a CL setting.

## References

[1] H. Caesar, V. Bankiti, A. H. Lang, S. Vora, V. E. Liong, Q. Xu, A. Krishnan, Y. Pan, G. Baldan, and O. Beijbom. nuscenes: A multimodal dataset for autonomous driving. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 11621–11631, 2020.

[2] W. Cao, M. Hallgarten, T. Li, D. Dauner, X. Gu, C. Wang, Y. Miron, M. Aiello, H. Li, I. Gilitschenski, B. Ivanovic, M. Pavone, A. Geiger, and K. Chitta. Pseudo-simulation for autonomous driving. In Conference on Robot Learning (CoRL), 2025.

[3] D. Dauner, M. Hallgarten, T. Li, X. Weng, Z. Huang, Z. Yang, H. Li, I. Gilitschenski, B. Ivanovic, M. Pavone, A. Geiger, and K. Chitta. Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking. In Advances in Neural Information Processing Systems (NeurIPS), 2024.

[4] L. Feng, Y. Gao, E. Zablocki, Q. Li, W. Li, S. Liu, M. Cord, and A. Alahi. Rap: 3d rasterization augmented end-to-end planning, 2025. URL https://arxiv.org/abs/2510.04333.

[5] E. Kirby, A. Boulch, Y. Xu, Y. Yin, G. Puy, E. Zablocki, A. Bursuc, S. Gidaris, R. Marlet, F. Bartoccioni, A.-Q. Cao, N. Samet, T.-H. Vu, and M. Cord. Driving on registers. preprint, 2026.

[6] X. Jia, Z. Yang, Q. Li, Z. Zhang, and J. Yan. Bench2drive: Towards multi-ability benchmarking of closed-loop end-to-end autonomous driving. In NeurIPS 2024 Datasets and Benchmarks Track, 2024.

[7] Z. Li, Z. Yu, S. Lan, J. Li, J. Kautz, T. Lu, and J. M. Alvarez. Is ego status all you need for open-loop end-to-end autonomous driving? In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 14864–14873, 2024.

[8] P. Karkus, M. Igl, Y. Chen, K. Chitta, J. Packer, B. Douillard, R. Tian, A. Naumann, G. Garcia-Cobo, S. Tan, et al. Beyond behavior cloning in autonomous driving: a survey of closed-loop training techniques. Authorea Preprints.

[9] S. Z. Zhao, H. Zhang, Z. Li, J. Peng, A. Chui, Z. Zhou, Z. Meng, H. Xiang, Z. Huang, F. Wang, et al. Quantv2x: A fully quantized multi-agent system for cooperative perception. arXiv preprint arXiv:2509.03704, 2025.

[10] Y. Zheng, P. Yang, Z. Xia, Q. Zhang, Y. Zheng, S. Gu, B. Jin, T. Zhang, B. Lu, C. Han, et al. Data scaling laws for imitation learning-based end-to-end autonomous driving. arXiv preprint arXiv:2412.02689, 2024.

[11] A. Naumann, X. Gu, T. Dimlioglu, M. Bojarski, A. Degirmenci, A. Popov, D. Bisla, M. Pavone, U. Muller, and B. Ivanovic. Data scaling laws for end-to-end autonomous driving. In Proceedings of the Computer Vision and Pattern Recognition Conference, pages 2571–2582, 2025.

[12] H. Caesar, J. Kabzan, K. S. Tan, W. K. Fong, E. Wolff, A. Lang, L. Fletcher, O. Beijbom, and S. Omari. nuplan: A closed-loop ml-based planning benchmark for autonomous vehicles. arXiv preprint arXiv:2106.11810, 2021.

[13] Y. Li, S. Z. Zhao, C. Xu, C. Tang, C. Li, M. Ding, M. Tomizuka, and W. Zhan. Pre-training on synthetic driving data for trajectory prediction. In 2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 5910–5917, 2024. doi:10.1109/IROS58592. 2024.10802492.

[14] G. Garcia-Cobo, M. Igl, P. Karkus, Z. Zhang, M. Watson, Y. Chen, B. Ivanovic, and M. Pavone. Road: Rollouts as demonstrations for closed-loop supervised fine-tuning of autonomous driving policies. arXiv preprint arXiv:2512.01993, 2025.

[15] H. Alghodhaifi and S. Lakshmanan. Autonomous vehicle evaluation: A comprehensive survey on modeling and simulation approaches. Ieee Access, 9:151531–151566, 2021.

[16] F. Rosique, P. J. Navarro, C. Fernandez, and A. Padilla. A systematic review of perception´ system and simulators for autonomous vehicles research. Sensors, 19(3):648, 2019.

[17] Y. Ye, X. Zhang, and J. Sun. Automated vehicle’s behavior decision making using deep reinforcement learning and high-fidelity simulation environment. Transportation Research Part C: Emerging Technologies, 107:155–170, 2019.

[18] B. Osinski, A. Jakubowski, P. Ziecina, P. Miło´ s, C. Galias, S. Homoceanu, and H. Michalewski.´ Simulation-based reinforcement learning for real-world autonomous driving. In 2020 IEEE international conference on robotics and automation (ICRA), pages 6411–6418. IEEE, 2020.

[19] J. Wu, C. Huang, H. Huang, C. Lv, Y. Wang, and F.-Y. Wang. Recent advances in reinforcement learning-based autonomous driving behavior planning: A survey. Transportation Research Part C: Emerging Technologies, 164:104654, 2024.

[20] M. Martinez, C. Sitawarin, K. Finch, L. Meincke, A. Yablonski, and A. Kornhauser. Beyond grand theft auto v for training, testing and enhancing deep learning in self driving cars, 2017. URL https://arxiv.org/abs/1712.01397.

[21] M. Muller, V. Casser, J. Lahoud, N. Smith, and B. Ghanem. Sim4cv: A photo-realistic simu-¨ lator for computer vision applications. IJCV, 2018.

[22] S. Shah, D. Dey, C. Lovett, and A. Kapoor. Airsim: High-fidelity visual and physical simulation for autonomous vehicles. In FSR, 2018.

[23] A. Dosovitskiy, G. Ros, F. Codevilla, A. Lopez, and V. Koltun. Carla: An open urban driving simulator. In Conference on robot learning, pages 1–16. PMLR, 2017.

[24] D. Team. Deepdrive: a simulator that allows anyone with a pc to push the state-of-the-art in self-driving. https://github.com/deepdrive/deepdrive.

[25] P. Kothari, C. Perone, L. Bergamini, A. Alahi, and P. Ondruska. Drivergym: Democratising reinforcement learning for autonomous driving. arXiv preprint arXiv:2111.06889, 2021.

[26] Q. Li, Z. Peng, L. Feng, Q. Zhang, Z. Xue, and B. Zhou. Metadrive: Composing diverse driving scenarios for generalizable reinforcement learning. TPAMI, 2022.

[27] X. Yang, L. Wen, Y. Ma, J. Mei, X. Li, T. Wei, W. Lei, D. Fu, P. Cai, M. Dou, B. Shi, L. He, Y. Liu, and Y. Qiao. Drivearena: A closed-loop generative simulation platform for autonomous driving. arXiv preprint arXiv:2408.00415, 2024.

[28] H. Zhou, L. Lin, J. Wang, Y. Lu, D. Bai, B. Liu, Y. Wang, A. Geiger, and Y. Liao. Hugsim: A real-time, photo-realistic and closed-loop simulator for autonomous driving. arXiv preprint arXiv:2412.01718, 2024.

[29] H. Gao, S. Chen, B. Jiang, B. Liao, Y. Shi, X. Guo, Y. Pu, H. Yin, X. Li, X. Zhang, et al. Rad: Training an end-to-end driving policy via large-scale 3dgs-based reinforcement learning. arXiv preprint arXiv:2502.13144, 2025.

[30] C. Ni, G. Zhao, X. Wang, Z. Zhu, W. Qin, G. Huang, C. Liu, Y. Chen, Y. Wang, X. Zhang, et al. Recondreamer: Crafting world models for driving scene reconstruction via online restoration. In Proceedings ofthe Computer Vision and Pattern Recognition Conference, pages 1559–1569, 2025.

[31] C. Ni, G. Zhao, X. Wang, Z. Zhu, W. Qin, X. Chen, G. Jia, G. Huang, and W. Mei. Recondreamer-rl: Enhancing reinforcement learning via diffusion-based scene reconstruction. arXiv preprint arXiv:2508.08170, 2025.

[32] W. Luo, B. Yang, and R. Urtasun. Fast and furious: Real time end-to-end 3d detection, tracking and motion forecasting with a single convolutional net. In Proceedings ofthe IEEE conference on Computer Vision and Pattern Recognition, pages 3569–3577, 2018.

[33] M. Liang, B. Yang, W. Zeng, Y. Chen, R. Hu, S. Casas, and R. Urtasun. Pnpnet: End-toend perception and prediction with tracking in the loop. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 11553–11562, 2020.

[34] A. Sadat, S. Casas, M. Ren, X. Wu, P. Dhawan, and R. Urtasun. Perceive, predict, and plan: Safe motion planning through interpretable semantic representations. In European Conference on Computer Vision, pages 414–430. Springer, 2020.

[35] Y. Li, C. Fan, C. Ge, Z. Zhao, C. Li, C. Xu, H. Yao, M. Tomizuka, B. Zhou, C. Tang, et al. Womd-reasoning: A large-scale dataset for interaction reasoning in driving. arXiv preprint arXiv:2407.04281, 2024.

[36] Y. Hu, J. Yang, L. Chen, K. Li, C. Sima, X. Zhu, S. Chai, S. Du, T. Lin, W. Wang, L. Lu, X. Jia, Q. Liu, J. Dai, Y. Qiao, and H. Li. Planning-oriented autonomous driving. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2023.

[37] B. Jiang, S. Chen, Q. Xu, B. Liao, J. Chen, H. Zhou, Q. Zhang, W. Liu, C. Huang, and X. Wang. Vad: Vectorized scene representation for efficient autonomous driving. ICCV, 2023.

[38] K. Chitta, A. Prakash, B. Jaeger, Z. Yu, K. Renz, and A. Geiger. Transfuser: Imitation with transformer-based sensor fusion for autonomous driving. Pattern Analysis and Machine Intelligence (PAMI), 2023.

[39] B. Liao, S. Chen, H. Yin, B. Jiang, C. Wang, S. Yan, X. Zhang, X. Li, Y. Zhang, Q. Zhang, and X. Wang. Diffusiondrive: Truncated diffusion model for end-to-end autonomous driving. pages 12037–12047, 2025. doi:10.1109/CVPR52734.2025.01124. URL https: //openaccess.thecvf.com/content/CVPR2025/html/Liao\_DiffusionDrive\_ Truncated\_Diffusion\_Model\_for\_End-to-End\_Autonomous\_Driving\_CVPR\_2025\_ paper.html.

[40] J. Zou, S. Chen, B. Liao, Z. Zheng, Y. Song, L. Zhang, Q. Zhang, W. Liu, and X. Wang. Diffusiondrivev2: Reinforcement learning-constrained truncated diffusion modeling in endto-end autonomous driving. arXiv preprint arXiv:2512.07745, 2025.

[41] J.-T. Zhai, Z. Feng, J. Du, Y. Mao, J.-J. Liu, Z. Tan, Y. Zhang, X. Ye, and J. Wang. Rethinking the open-loop evaluation of end-to-end autonomous driving in nuscenes. arXiv preprint arXiv:2305.10430, 2023.

[42] D. Dauner, M. Hallgarten, A. Geiger, and K. Chitta. Parting with misconceptions about learning-based vehicle motion planning. In Conference on Robot Learning, pages 1268–1281. PMLR, 2023.

[43] L. Nguyen, M. Fauth, B. Jaeger, D. Dauner, M. Igl, A. Geiger, and K. Chitta. Lead: Minimizing learner-expert asymmetry in end-to-end driving. arXiv preprint arXiv:2512.20563, 2025.

[44] P. Karkus, M. Igl, Y. Chen, K. Chitta, J. Packer, B. Douillard, R. Tian, A. Naumann, G. Garcia-Cobo, S. Tan, A. Degirmenci, A. Popov, N. Smolyanskiy, U. Muller, B. Ivanovic, and˘ M. Pavone. Beyond behavior cloning in autonomous driving: a survey of closed-loop training techniques. URL https://api.semanticscholar.org/CorpusID:283728300.

[45] J. Mei, A. Z. Zhu, X. Yan, H. Yan, S. Qiao, L.-C. Chen, and H. Kretzschmar. Waymo open dataset: Panoramic video panoptic segmentation. In European Conference on Computer Vision, pages 53–72. Springer, 2022.

[46] M. Treiber, A. Hennecke, and D. Helbing. Congested traffic states in empirical observations and microscopic simulations. Physical review E, 62(2):1805, 2000.

[47] Y. Liu, Z. Peng, X. Cui, and B. Zhou. Adv-bmt: Bidirectional motion transformer for safetycritical traffic scenario generation, 2025. URL https://arxiv.org/abs/2506.09485.

[48] H. Lin, Y. Zhang, W. Ding, J. Wu, and D. Zhao. Model-based policy adaptation for closed-loop end-to-end autonomous driving. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, 2025. URL https://openreview.net/forum?id=4OLbpaTKJe.

[49] Y. Lipman, R. T. Chen, H. Ben-Hamu, M. Nickel, and M. Le. Flow matching for generative modeling. arXiv preprint arXiv:2210.02747, 2022.

[50] Q. Liu, X. Yin, A. Yuille, A. Brown, and M. Singh. Flowing from words to pixels: A noise-free framework for cross-modality evolution. In Proceedings of the Computer Vision and Pattern Recognition Conference, pages 2755–2765, 2025.

[51] Z. Li, W. Yao, Z. Wang, X. Sun, J. Chen, N. Chang, M. Shen, J. Song, Z. Wu, S. Lan, et al. Ztrs: Zero-imitation end-to-end autonomous driving with trajectory scoring. arXiv preprint arXiv:2510.24108, 2025.

[52] W. Yao, Z. Li, S. Lan, Z. Wang, X. Sun, J. M. Alvarez, and Z. Wu. Drivesuprim: Towards precise trajectory selection for end-to-end planning. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 40, pages 11910–11918, 2026.

[53] S. Ross, G. Gordon, and J. A. Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In AISTATS, 2011.

[54] S. Ross and J. A. Bagnell. Reinforcement and imitation learning via interactive no-regret learning. arXiv preprint arXiv:1406.5979, 2014.

[55] F. Codevilla et al. Exploring the limitations of behavior cloning for autonomous driving. In ICCV, 2019.

[56] Q. Li, Z. Peng, L. Feng, Z. Liu, C. Duan, W. Mo, and B. Zhou. Scenarionet: Open-source platform for large-scale traffic scenario simulation and modeling. Advances in Neural Information Processing Systems, 2023.

[57] H. Christensen, D. Paz, H. Zhang, D. Meyer, H. Xiang, Y. Han, Y. Liu, A. Liang, Z. Zhong, and S. Tang. Autonomous vehicles for micro-mobility. Autonomous Intelligent Systems, 1(1): 11, 2021.

[58] R. C. Coulter. Implementation of the pure pursuit path tracking algorithm. Technical report, 1992.

[59] K. Li, Z. Li, S. Lan, Y. Xie, Z. Zhang, J. Liu, Z. Wu, Z. Yu, and J. M. Alvarez. Hydramdp++: Advancing end-to-end driving via expert-guided hydra-distillation. arXiv preprint arXiv:2503.12820, 2025.

[60] Y. Wang, W. Luo, J. Bai, Y. Cao, T. Che, K. Chen, Y. Chen, J. Diamond, Y. Ding, W. Ding, et al. Alpamayo-r1: Bridging reasoning and action prediction for generalizable autonomous driving in the long tail. arXiv preprint arXiv:2511.00088, 2025.

[61] comma.ai. openpilot. https://github.com/commaai/openpilot, 2026.

[62] W. Peebles and S. Xie. Scalable diffusion models with transformers. arXiv preprint arXiv:2212.09748, 2022.

[63] D. P. Kingma and J. Ba. Adam: A method for stochastic optimization. arXiv preprint arXiv:1412.6980, 2014.

[64] A. P. Tarko. Surrogate measures of safety. 2018.

[65] H. Guo, K. Xie, and M. Keyvan-Ekbatani. Modeling driver’s evasive behavior during safety– critical lane changes: Two-dimensional time-to-collision and deep reinforcement learning. Accident Analysis & Prevention, 186:107063, 2023.

[66] A. Laureshyn, A. Svensson, and C. Hyd<sup>˚</sup> en. Evaluation of traffic safety, based on micro-level´ behavioural data: Theoretical framework and first implementation. Accident Analysis & Prevention, 42(6):1637–1646, 2010.

[67] K. Ozbay, H. Yang, B. Bartin, and S. Mudigonda. Derivation and validation of new simulationbased surrogate safety measure. Transportation research record, 2083(1):105–113, 2008.

[68] S. Ettinger, S. Cheng, B. Caine, C. Liu, H. Zhao, S. Pradhan, Y. Chai, B. Sapp, C. R. Qi, Y. Zhou, Z. Zoeggeler, A. Chouard, P. Sun, J. Ngiam, V. Vasudevan, A. McCauley, J. Pang, and D. Anguelov. Large scale interactive motion forecasting for autonomous driving: The waymo open motion dataset. In Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), pages 9710–9719, 2021.

[69] Z. Zhou, T. Cai, Y. Zhao, Seth Z.and Zhang, Z. Huang, B. Zhou, and J. Ma. Autovla: A vision-language-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning. Advances in Neural Information Processing Systems (NeurIPS), 2025.

## Appendix

## A More Related Works

E2E Driving Policy Adaptation. Adaptation of end-to-end (E2E) driving policies has long been studied under the broader problem of covariate shift in imitation learning. Behavior cloning suf fers from compounding errors when policies encounter off-distribution states, motivating interactive learning methods such as DAgger that address behavioral distribution shift through on-policy data aggregation [53, 54]. In driving-specific settings, prior studies confirm that large-scale OL imitation learning often overfits to static expert trajectories and fails under long-horizon or reactive interactions [55, 10]. Orthogonal to behavioral shift, sim-to-real transfer research highlights observational distribution shift as a critical failure mode for E2E policies [23]. While domain randomization and representation learning improve robustness, they do not explicitly guarantee planning-oriented fi delity across heterogeneous simulators. Recent OL benchmarks enable scalable evaluation but have been shown to correlate weakly with CL reliability, underscoring the limitations of static evaluation protocols [3, 2]. In contrast to prior work that addresses perception or policy shift in isolation, our work provides in-depth decomposition of the OL–CL gap and studies their interaction under controlled simulator-induced transition changes.

## B More Details on BridgeSim Platform

## B.1 Motivation

BridgeSim platform is a unified cross-simulator closed-loop simulation platform to enable E2E policies to be evaluated across simulators, as illustrated in Fig. 6. We argue that existing benchmarking testbeds are insufficient for a rigorous and unified analysis of the OL-CL gap in E2E autonomous driving. The limitations of current E2E driving benchmarks can be categorized into three primary deficiencies: 1) open-loop evaluations in existing benchmarks [3, 2] often exhibit only a superficial correlation with short-term closed-loop performance and fail to serve as reliable indicators of longhorizon closed-loop capabilities; 2) current closed-loop benchmarks frequently suffer from a lack of multi-view temporal consistency [27], inaccurate annotations for observationally consistent traffic elements [28], or a lack of environmental diversity and agent behaviors necessary to stress-test generalizability [6] (see Appendix E for more details); and 3) policies transferred between simulators often encounter inconsistent vehicle dynamics and controller configurations, inducing artificial performance drops that obscure the true OL-CL gap.

These systematic deficiencies necessitate the design of the BridgeSim platform, which is engineered to be controllable for identifying modular changes and consistent across evaluation modes and metrics. To this end, BridgeSim leverages the MetaDrive [26, 56] simulation engine to resolve the controllability and inconsistency issues prevalent in previous benchmarks. As illustrated in Fig. 6, BridgeSim ensures high-fidelity closed-loop simulation through a modularized architecture imple menting: 1) a unified structural framework for policy transfer to maintain state-action compatibility across domains; 2) unified scenario protocols that enable precise, repeatable environment replay and controllable agent interactions; and 3) unified evaluation modes and metrics to ensure fair and accurate comparisons.

## B.2 Unified Structural Invariance in Policy Transfer

To quantify the OL-CL gap, it is imperative to decouple the policy’s decision-making logic from confounding systemic variables. To establish an equitable diagnostic framework, BridgeSim enforces two levels of structural invariance:

1) Observational Alignment: We standardize sensor configurations, including camera extrinsics and intrinsics, across all evaluated benchmarks. This standardization ensures that performance failures are strictly attributable to the policy’s representational robustness rather than superficial geometric mismatches in the input space Ω. Since the simulator maintains rigorous physical properties, we further enforce multi-view temporal consistency, addressing a common deficiency in existing benchmarks. Sensor observations $o _ { t }$ are synthesized via geometric projection, ensuring that $o _ { t }$ remains spatially and temporally consistent with the underlying state $s _ { t }$ across all camera frames and timesteps. This approach eliminates spurious distribution shifts, thereby ensuring that policy failures are rooted in decision-making errors rather than simulation artifacts. Representative failure cases of existing generative and Gaussian Splatting-based simulation paradigms are detailed in the Appendix E.

![](images/7dc3e822c83e5c1d134d5538c3133933cfd5e063bbaa3a19df9a7d6d48218184.jpg)  
Figure 6: Illustration of BridgeSim Platform. BridgeSim supports unified closed-loop simulation of policies pretrained from any other simulators, enabling us to perform rigorous decomposition analysis.

2) Kinematic and Control Alignment: We enforce consistency across vehicle dynamics and control execution layers to isolate the sources of performance degradation. By standardizing the transition dynamics P during the execution of predicted waypoints, we ensure that the measured OL-CL gap reflects fundamental planning-level failures rather than downstream actuation discrepancies. To ensure our evaluation reflects standard practice, we adopt controllers that are ubiquitous across diverse real-world autonomous driving platforms [57]; specifically, we utilize a standard PID formulation for longitudinal control and a Pure Pursuit [58] controller for lateral tracking. Furthermore, BridgeSim maintains strict structural invariance by explicitly decoupling these vehicle dynamics from the rendering pipeline.

## B.3 Unified Scenario Protocols

Scenario Descriptions. We define a unified, serialized data schema designed to encapsulate all static and dynamic elements necessary to reconstruct any driving episode. To ensure cross-platform compatibility, the converters map diverse source data from real-world logs (e.g., Waymo [45], nuScenes [1]) to synthetic environments (e.g., CARLA [6]) into a standardized ScenarioDescription format.

## This centralized data structure contains three primary components:

1) Map features. BridgeSim ingests diverse real-world datasets, including Waymo [45], nuPlan [12], nuScenes [1], via a standardized protocol to extract map geometry. This geometry is discretized and stored as dense point sequences, each assigned specific type attributes. We subsequently vectorize HD map elements, such as lanes, boundaries, crosswalks, and stop lines, into a unified polyline representation. By ensuring the precise spatial alignment of these layouts within the simulation environment, we eliminate rendering artifacts that might otherwise distort lane properties, maintaining higher fidelity and consistency than existing benchmarks.

2) Object tracks. Dynamic agents are stored as temporal tracks containing state sequences, including position, heading, velocity, and dimensions alongside validity masks. To address the varying sampling rates across different datasets, we implement an interpolation pipeline that up-samples trajectories. This process utilizes linear interpolation for position and velocity, while applying angular interpolation for heading to ensure smooth kinematic playback during simulation.

3) Dynamic map states. Traffic light states are decoupled from the static map geometry. We map individual traffic signals to specific lane IDs and store their state sequences (e.g., STOP, WAIT, GO). This mapping enables the simulator to dynamically update the lane signaling during replay, ensuring that the behavioral constraints of the agents remain in sync with the visual environment.

Traffic Modes. BridgeSim provides an API for the dynamic configuration of agent behaviors to stress-test policies under varying levels of interactivity. We allow for the following agent behavior modes:

1) Log-replay mode. In this mode, background agents strictly adhere to their recorded trajectories from the source dataset. The simulator essentially replays the preset vehicle tracks. While this preserves the exact real-world context, these agents remain non-reactive to the ego-vehicle’s deviations.

2) IDM mode [46]. To bridge the gap between static datasets and closed-loop interaction, we replace log-replay policies with an Intelligent Driver Model (IDM). While background vehicles are initialized at their ground-truth poses, their subsequent behaviors are governed by heuristic policies. These agents adhere to lane geometry, maintain safety gaps, and actively respond to the ego-vehicle’s presence.

3) Adversarial mode. We provide an interface for injecting adversarial agents [47] into log-replay scenarios. This enables the generation of safety-critical edge cases, challenging ego-policies to react instantaneously to avoid imminent collisions.

Coordinate Systems. A critical challenge in evaluating policies across different simulators is the misalignment of coordinate systems (e.g., global vs. local, left-handed vs. right-handed). BridgeSim enforces a unified right-handed coordinate system (RHS) centered on a local scenario anchor. We employ the following techniques to ensure coordinate system alignment:

1) Chirality normalization. For datasets using left-handed systems (e.g., CARLA, Bench2Drive), we apply a basis transformation during conversion. Orientation angles (yaw, roll) are inverted accordingly to maintain kinematic consistency.

2) Spatial anchoring. To mitigate floating-point errors inherent in large-scale global coordinates (common in nuScenes and nuPlan), we normalize all spatial data relative to a scenario anchor, de fined as the ego-vehicle’s position at t = 0. All map features and trajectories are translated so that the map origin aligns with this anchor, ensuring numerical stability for the planner and simulator physics engine.

Time Lengths. BridgeSim decouples the simulation horizon from the source simulators by supporting long-term simulation durations determined by the full extent of the source log. The scenario duration can also be manually configured to a variable length comprising a sub-duration of the full source scenario. To accommodate the heterogeneous sampling rates of these diverse datasets, we implement a standardized trajectory interpolation protocol. This pipeline resamples source signals to the simulator’s native 10Hz control frequency using linear and angular interpolation. This ensures consistent kinematic evaluation across varying time steps without artificially truncating the scenario.

## B.4 Unified Evaluation Modes and Metrics

Evaluation modes. To rigorously assess the capability of driving agents to generalize from offline datasets to online deployment, BridgeSim implements a unified evaluation pipeline. This pipeline supports both non-reactive open-loop evaluation and reactive closed-loop evaluation, within a shared environment $\mathcal { E } .$ Let $s$ denote the state space and A the action space. At time t, the agent observes state $s _ { t } \in S$ and generates a planned trajectory $\tau _ { t } = \pi ( s _ { t } )$

1) Non-reactive open-loop simulation. In open-loop mode, the simulation decouples the egoagent’s trajectory planning from the environment’s state transitions. The environment dynamics are strictly governed by the ground-truth trajectories from the source dataset. In this mode, the egovehicle’s state transition is forced to match the logged trajectory $\mathcal { T } _ { l o g }$ independent of the policy output. Specifically, the state transition is defined as $s _ { t + 1 } = f ( s _ { t } , a _ { t } ^ { * } )$ , where $a _ { t } ^ { * }$ denotes the expert action recorded in the log. The model predicts a trajectory $\hat { \tau } _ { t }$ at every timestep, which is transformed from the ego-frame to the global simulation frame for evaluation against the static map and dynamic agents (replayed from logs). This mode isolates the planner’s reasoning ability without the confounding factor of cumulative control error.

2) Reactive closed-loop simulation. In closed-loop mode, the evaluation focuses on the agent’s ability to robustly control the vehicle over long horizons. The simulation environment is configurable to support either a $f u l l y$ reactive paradigm, where background traffic behavior is governed by Intelligent Driver Models (IDM) that dynamically respond to the ego-agent’s movements, or a semi-reactive paradigm, where background traffic strictly adheres to the original logged trajectories while the ego-vehicle remains physically controlled by the policy.

Evaluation metrics. To quantify driving performance within the BridgeSim environment, we implement a set of open-loop and closed-loop metrics following previous protocols [3, 2, 28, 27, 59]. For non-reactive open-loop simulations, we adopt the EPDMS framework [3, 2, 59]. For reactive closed-loop simulations, we incorporate a composite metric inspired by the HUGSIM [28] and DriveArena [27] Driving Score.

1) Open-loop Metric: Extended Predictive Driver Model Score (EPDMS). The EPDMS score is implemented as a weighted combination of safety-critical constraints and driving quality features, as shown in Table 3. Unlike L2 displacement errors, EPDMS penalizes physically infeasible or unsafe plans even if they mimic the log. At every frame, we transform the model’s predicted trajectory into the simulation frame and score it against the static and dynamic map features. The final score $S _ { E P D M S } \in [ 0 , 1 ]$ for a given frame is defined as the product of critical boolean constraints C and a weighted sum of soft metrics ${ \mathcal { F } } \mathrm { : }$

$$
S _ { E P D M S } = \left( \prod _ { c \in \mathcal { C } } \mathbb { I } _ { c } \right) \cdot \left( \frac { \sum _ { f \in \mathcal { F } } w _ { f } \cdot v _ { f } } { \sum _ { f \in \mathcal { F } } w _ { f } } \right) ,\tag{8}
$$

where $\mathbb { I } _ { c } \in \{ 0 , 1 \}$ is the indicator function for constraint compliance, $v _ { f } \in [ 0 , 1 ]$ is the normalized feature score, and $w _ { f }$ is the corresponding weight.

2) Closed-loop Metric: BridgeSim Driving Score. For reactive closed-loop simulation, we define the final driving score $S _ { C L S }$ as the product of the agent’s global Route Completion (RC) and the temporal average of the frame-level scores $( S _ { E P D M S } ^ { ( t ) } ) \mathrm { : }$

$$
S _ { C L S } = R _ { c } \times \frac { 1 } { T } \sum _ { t = 1 } ^ { T } S _ { E P D M S } ^ { ( t ) } ,\tag{9}
$$

where $R _ { c } \in [ 0 , 1 ]$ represents the percentage of the route completed by the agent relative to the expert driver’s path or the goal destination, $T$ is the total number of frames in the simulation episode, and $S _ { E P D M S } ^ { ( t ) }$ is the EPDM score at time step t. Note that the frame-level ego progress score (EP) from open-loop EPDM scoring is removed, as progress is now explicitly measured by the distance traveled to the goal in the simulator [28]. Crucially, for the closed-loop setting, the set of soft features $\mathcal { F }$ is modified to exclude displacement error or progress-based terms, focusing solely on driving quality and safety constraints. This formulation ensures that an agent achieves a high score only if it completes the route while consistently maintaining safe and comfortable driving behavior throughout the episode.

Table 3: Descriptions of subscores of EPDMS.
<table><tr><td>Metric</td><td>Description</td></tr><tr><td>Critical Constraints (C)</td><td></td></tr><tr><td>No At-Fault Collisions (NC)</td><td>Ego polygon  $\mathcal { P } _ { e g o }$  must not intersect any replayed object polygons  $\mathcal { P } _ { o b j }$ </td></tr><tr><td>Drivable Area Compliance (DAC) Traffic Light Compliance (TLC)</td><td>Entire horizon must satisfy  $\mathcal { P } _ { e g o } \subset \mathcal { M } _ { d r i v a b l e }$  within the HD map.</td></tr><tr><td>Driving Direction Compliance (DDC)</td><td>Agent cannot cross stop lines associated with red light states. Heading deviation  $| \theta _ { e g o } - \theta _ { l a n e } |$  must remain within  $\pm \pi / 2 .$ </td></tr><tr><td>Quality Features (F)</td><td></td></tr><tr><td>Ego Progress (EP)</td><td>Represents the agent progress as a ratio to an approximated safe</td></tr><tr><td>Lane Keeping (LK)</td><td>upper bound. Checks the ego-vehicle follows the centerline of its current lane and</td></tr><tr><td>Time-to-Collision (TTC)</td><td>avoids lingering between adjacent lanes. Penalizes trajectory î if the projected time-to-collision is too low.</td></tr><tr><td>History Comfort (HC)</td><td>Evaluates the planner&#x27;s predicted trajectory with a short segment of</td></tr><tr><td>Extended Comfort (EC)</td><td>historical motion from the human driver. Limits kinematic derivatives for passenger comfort: acceleration  $a \leq 4 . 8 9 .$  jerk  $j \le 8 . 3 7 ,$  and yaw rate  $\dot { \theta } \leq 0 . 9 5$ </td></tr></table>

## B.5 Sim-to-Sim Evaluation Results across Simulators

## B.5.1 Supported Model Zoo

We include a diverse set of publicly available end-to-end driving models for zero-shot crosssimulator evaluation. Unless otherwise specified, we use the official checkpoints released by the original authors or benchmark maintainers. Note that new models could be easily incorporated into BridgeSim following the instructions in Appendix B.6.

UniAD [36] is a unified end-to-end autonomous driving framework that jointly models perception, prediction, and planning through a query-based transformer architecture. We use its official Bench2Drive checkpoint in our evaluation.

Vectorised Autonomous Driving (VAD) [37] is a vectorized end-to-end driving method that represents map elements and traffic agents with structured queries rather than dense raster features. We use its official Bench2Drive checkpoint.

TransFuser [38] is a multi-modal end-to-end driving model that fuses RGB camera and LiDAR observations for waypoint prediction. We use the released NAVSIM-trained checkpoint in our evaluation.

DiffusionDrive [39] formulates autonomous driving as a generative planning problem using a truncated diffusion process with anchor trajectories. The released checkpoint used in our evaluation is trained on NAVSIM.

DiffusionDriveV2 [40] extends DiffusionDrive by incorporating reinforcement learning into the trajectory denoising process. We use the released NAVSIM-trained checkpoint.

LEAD [43] studies learner–expert asymmetry in imitation learning and builds on a TransFuser-v6 driving architecture. The released checkpoints include CARLA-based models for Leaderboard 2.0 / Bench2Drive-style evaluation as well as a NAVSIM checkpoint under the LTFv6 variant.

DrivoR [5] is a transformer-based end-to-end planner built on a pretrained DINOv2 visual encoder with token compression and trajectory scoring modules. The released model used in our evaluation is trained on NAVSIM.

Rasterization Augmented Planning (RAP) [4] is a rasterisation-based augmentation framework for end-to-end driving that improves training with counterfactual rasterised views and raster-to-real feature alignment. The official checkpoint used in our comparison is trained on NAVSIM.

Alpamayo-R1 [60] is a vision-language-action (VLA) model for end-to-end driving model that emphasizes robust temporal reasoning to handle complex urban maneuvers. We utilize the official released checkpoint in our evaluation.

OpenPilot [61] is a vision-based driving system that utilizes a multi-task convolutional neural network to predict the path, lead vehicle properties, and lane boundaries. We use the released v0.11.0 version checkpoint provided by comma.ai.

Table 4: Quantitative comparison of E2E driving policies evaluated on BridgeSim-NavHard. All results are reported with a replan rate of 5 and a simulation horizon of 8 seconds. We use rr = 5 to align with the temporal discretization commonly used for training on NAVSIM/OpenScene, where the dataset is provided at 2 Hz (i.e., ∆t = 0.5 s).
<table><tr><td>Model</td><td>Pretrained Sim</td><td>DS</td><td>EPDMS</td><td>RC</td><td>NC</td><td>DAC</td><td>DDC</td><td>TLC</td><td>TTC</td><td>LK</td><td>HC</td><td>EC</td></tr><tr><td>Human Expert</td><td>N/A</td><td>91.14</td><td>91.96</td><td>98.86</td><td>98.18</td><td>99.23</td><td>99.76</td><td>98.62</td><td>94.55</td><td>90.22</td><td>99.10</td><td>71.44</td></tr><tr><td>UniAD (CVPR&#x27;23)</td><td>Bench2Drive</td><td>31.00</td><td>57.55</td><td>55.25</td><td>93.15</td><td>71.75</td><td>99.76</td><td>99.61</td><td>81.13</td><td>97.70</td><td>74.25</td><td>30.04</td></tr><tr><td>VAD (ICCV&#x27;23)</td><td>Bench2Drive</td><td>26.25</td><td>57.60</td><td>46.76</td><td>93.29</td><td>71.22</td><td>99.76</td><td>99.68</td><td>82.31</td><td>98.67</td><td>71.13</td><td>27.67</td></tr><tr><td>DiffusionDrive (CVPR&#x27;25)</td><td>NAVSIM</td><td>43.29</td><td>69.70</td><td>61.30</td><td>95.38</td><td>81.48</td><td>99.76</td><td>98.81</td><td>87.47</td><td>91.57</td><td>91.64</td><td>39.02</td></tr><tr><td>DiffusionDriveV2 (arXiv)</td><td>NAVSIM</td><td>29.81</td><td>62.01</td><td>45.85</td><td>93.48</td><td>79.75</td><td>99.76</td><td>98.83</td><td>86.93</td><td>84.11</td><td>71.38</td><td>20.62</td></tr><tr><td>RAP (ICLR&#x27;26)</td><td>NAVSIM</td><td>52.08</td><td>72.41</td><td>70.74</td><td>95.63</td><td>85.24</td><td>99.76</td><td>99.18</td><td>88.14</td><td>84.69</td><td>92.84</td><td>48.91</td></tr><tr><td>LEAD (CVPR&#x27;26)</td><td>NAVSIM</td><td>26.34</td><td>54.02</td><td>47.42</td><td>93.29</td><td>68.44</td><td>99.53</td><td>99.89</td><td>84.70</td><td>96.38</td><td>91.62</td><td>36.59</td></tr><tr><td>TransFuser (PAMI&#x27;23)</td><td>NAVSIM</td><td>41.46</td><td>68.17</td><td>61.28</td><td>95.73</td><td>78.99</td><td>99.76</td><td>98.63</td><td>88.79</td><td>89.25</td><td>95.06</td><td>49.25</td></tr><tr><td>LTF (NeurIPS&#x27;24)</td><td>NAVSIM</td><td>50.10</td><td>69.29</td><td>70.64</td><td>95.49</td><td>78.80</td><td>99.53</td><td>98.51</td><td>88.61</td><td>90.28</td><td>95.02</td><td>58.27</td></tr><tr><td>DrivoR (CVPR&#x27;26)</td><td>NAVSIM</td><td>42.79</td><td>66.54</td><td>64.66</td><td>95.41</td><td>76.34</td><td>100.00</td><td>99.46</td><td>95.41</td><td>94.37</td><td>96.99</td><td>66.69</td></tr><tr><td>OpenPilot</td><td>Comma.ai</td><td>64.75</td><td>79.50</td><td>82.21</td><td>97.55</td><td>94.29</td><td>100.00</td><td>98.89</td><td>92.58</td><td>84.43</td><td>92.12</td><td>62.06</td></tr><tr><td>Alpamayo-R1</td><td>Nvidia</td><td>37.78</td><td>64.69</td><td>59.65</td><td>94.98</td><td>76.54</td><td>100.00</td><td>99.73</td><td>87.39</td><td>93.63</td><td>94.82</td><td>68.24</td></tr><tr><td>TTA (DiffusionDrive)</td><td>NAVSIM</td><td>67.84</td><td>79.77</td><td>82.54</td><td>96.48</td><td>87.03</td><td>100.00</td><td>99.01</td><td>96.07</td><td>91.85</td><td>36.18</td><td>33.72</td></tr><tr><td>TTA (DiffusionDriveV2)</td><td>NAVSIM</td><td>61.46</td><td>76.86</td><td>77.86</td><td>95.83</td><td>86.80</td><td>100.00</td><td>99.17</td><td>92.93</td><td>91.51</td><td>26.22</td><td>24.32</td></tr><tr><td>TTA (RAP)</td><td>NAVSIM</td><td>80.92</td><td>91.68</td><td>87.06</td><td>96.95</td><td>90.14</td><td>100.00</td><td>98.90</td><td>98.07</td><td>94.72</td><td>46.18</td><td>54.60</td></tr></table>

## B.5.2 Sim-to-Sim Evaluation Results

Our evaluation in Table 4 reveals that most open-source models suffer from the OL-to-CL deployment gap when integrated into the BridgeSim platform. We observe that models pretrained on synthetic simulation domains frequently encounter simulation overfitting across both visual and behavioral aspects. Specifically, models trained on Bench2Drive exhibit a substantial performance degradation. This disparity underscores a significant sim-to-sim gap between CARLA’s synthetic rendering and BridgeSim’s real-world replayed scenarios. On the other hand, NAVSIM-pretrained models demonstrate better performance, as their training environment relies on real-world traffic behaviors. These findings emphasize that, besides visual fidelity, behavioral realism is also critical when training autonomous agents for robust simulation performance. The results show that strong in-domain performance doesn’t always translate to broader generalizability.

## B.6 Extensible Design for Incorporating New Maps, Models, and Traffic Modes

BridgeSim possesses high backward-compatibility and extensibility to incorporate new maps, models, and traffic modes, encouraging open-source contributors to independently augment the benchmark with novel driving environments, state-of-the-art planning models, and alternative traffic behaviors without modifying any shared evaluation logic.

Incorporating New Maps. To integrate a new map, contributors only need to implement the converter module and integrate the new maps into the scenario description protocol. This module provides dedicated, dataset-specific pipelines for each supported source. Each pipeline implements a conversion function that transforms raw, dataset-native records into a standardized scenario description dictionary. By invoking the shared serialization utility within this function, the resulting scenario directory becomes automatically discoverable by the environment manager during evaluation, requiring no modifications to downstream evaluation logic.

Incorporating New Models. Contributor could use the adapter module to incorporate new planners for evaluations. We provide an interface through the abstract base class BaseModelAdapter, which has four core functions to enable simulation on BridgeSim: load model() for checkpoint initialization and device mapping; prepare input() for transforming raw multi-camera images and ego-state vectors into the model’s native input format; run inference() for executing the forward pass; and parse output() for extracting a predicted waypoint trajectory of shape $N \times 2$ in the ego-vehicle coordinate frame. Once the model adapter is implemented, it is registered by adding a single entry to the create model adapter() factory, after which the new model is immediately ready for evaluations across all loaded maps and traffic modes.

Incorporating New Traffic Modes. Traffic behavior is governed by the EnvironmentManager component, which maps symbolic traffic-mode identifiers to their corresponding MetaDrive simulation configurations. To introduce a new traffic mode, such as a learning-based traffic generation model or an adversarial agent policy, contributors simply define a new mode identifier, extend the internal configuration resolver to emit the necessary MetaDrive flags, and optionally provide a custom agent policy class.

## C Implementation Details on TTA Framework

## C.1 Implementation Details on Observational Calibrator

The observational calibrator is designed to align latent representation distributions $\mathcal { D } _ { \mathrm { s o u r c e } }$ and $\mathcal { D } _ { \mathrm { t a r g e t } }$ via a flow-matching framework. To construct the necessary feature pairs for training, we utilize the NAVSIM dataset [3, 2], replaying and rendering all annotated frames to generate paired image observations between the source and target domains, as shown in Fig. 7. To process these input observations, we first employ a small encoder that transforms raw scene features into a regularized latent space Z. We then parameterize the vector field $v _ { \theta } ( z , t )$ operating on this space using a Diffusion Transformer (DiT) [62] architecture. Specifically, we employ the DiT-L configuration with a patch size of 2 to process the latent features, ensuring high-resolution alignment across the domain shift.

![](images/51b950a678ec05b52ccba295791d35cbdbf4cd9ab1bf03c8dadf830abb3d4c2c.jpg)  
Figure 7: Visualization of observation pairs in source and target domains.

Following [50], we optimize the calibrator using a multi-objective loss function. In addition to the standard flow-matching objective, the intermediate latent space Z is explicitly regularized via an encoder loss and a KL divergence loss to preserve semantic consistency and maintain a wellbehaved manifold. The total training objective is:

$$
\mathcal { L } _ { \mathrm { t o t a l } } = \mathcal { L } _ { \mathrm { F M } } + \lambda _ { \mathrm { e n c } } \mathcal { L } _ { \mathrm { e n c } } + \lambda _ { \mathrm { K L } } \mathcal { L } _ { \mathrm { K L } } ,\tag{10}
$$

where each component is defined as follows:

• Flow-Matching Loss $( \mathcal { L } _ { \mathrm { F M } } ) { : }$ We adopt a linear probability path to learn the transport map between source and target distributions. The loss is defined as:

$$
\mathcal { L } _ { \mathrm { F M } } ( \theta ) = \mathbb { E } _ { t , q ( z _ { t } | z _ { 0 } , z _ { 1 } ) } \left[ | | v _ { \theta } ( z _ { t } , t ) - ( z _ { 1 } - z _ { 0 } ) | | ^ { 2 } \right] ,\tag{11}
$$

where $z _ { 0 } \sim \mathcal { D } _ { \mathrm { s o u r c e } }$ and $z _ { 1 } \sim \mathcal { D } _ { \mathrm { t a r g e t } }$

• Encoder Loss $( { \mathcal { L } } _ { \mathrm { e n c } } ) { : }$ We employ a categorical contrastive loss between source and target feature pairs to regularize the small encoder. This term ensures that latent features corresponding to similar underlying states are clustered together while pushing dissimilar states apart. This prevents mode collapse during the transport process and preserves the discriminative structure of the latent space necessary for the downstream policy $\pi _ { \phi }$

• KL Loss $( \mathcal { L } _ { \mathrm { K L } } ) \colon$ To maintain a structured and smooth latent manifold, we apply a Kullback-Leibler divergence penalty against a standard normal prior $\mathcal { P } ( z ) = \mathcal { N } ( 0 , \mathbf { I } )$

$$
{ \mathcal { L } } _ { \mathrm { K L } } = D _ { \mathrm { K L } } ( q ( z | o ) \| { \mathcal { P } } ( z ) ) .\tag{12}
$$

This variational regularization ensures that the flow-matching trajectory remains within a well-behaved region of the latent space Z.

During training, we use the AdamW [63] optimizer with a learning rate of $1 \times 1 0 ^ { - 4 }$ and weight decay of 0.01. At test time, the calibrated representations are obtained by integrating the learned ODE from $t = 0 \mathrm { t o } t = 1$ using a first-order Euler solver.

## C.2 More Implementation Details on Test-time Policy Adaptation

To operationalize the truncated action-value estimator defined in Section 5.2.1, we employ Monte Carlo sampling to generate and evaluate future candidate rollouts over the horizon H. The empirical reward function $R _ { k } ( s _ { t } , \mathbf { a } _ { t } )$ evaluates each candidate prefix by computing EPDMS. Assuming the subscore definitions established in Appendix B.4, we detail the computational mechanisms enabling their exact and estimated evaluation during real-time closed-loop execution.

The prefix reward is mathematically formulated as a gated sum of the continuous Quality Features (F), strictly conditioned on the satisfaction of the Critical Constraints (C):

$$
R _ { k } ( s _ { t } , \mathbf { a } _ { t } ) = \mathbb { I } _ { \mathcal { C } } \cdot \sum _ { f \in \mathcal { F } } w _ { f } f \big ( s _ { t : t + k } , \mathbf { a } _ { t : t + k } \big )\tag{13}
$$

where $\mathbb { I } _ { \mathcal { C } } \in \{ 0 , 1 \}$ acts as a hard safety filter. If a candidate trajectory violates any critical constraint, $\mathbb { I } _ { C } = 0$ , immediately zeroing out the trajectory’s expected value.

Kinematic Comfort. Because the test-time adaptation mechanism operates directly on spatialtemporal plans, we have explicit access to both the historical states and the predicted future waypoints of the ego vehicle. Consequently, we do not need to rely on transition approximations; the exact comfort score is computed deterministically by extracting the high-frequency kinematic derivatives (acceleration, jerk, and yaw rate) directly from the sequence of waypoints.

Semantic and Map Awareness. Evaluating map-dependent metrics, such as Drivable Area Compliance (DAC), Driving Direction Compliance (DDC), Traffic Light Compliance (TLC), and Lane Keeping (LK), requires grounding the generated waypoints in the environment’s topology. To achieve this, we assume access to an accurate localization model and a robust mapping model, such as High-Definition (HD) Map or other online map generative models. The candidate ego-polygon $\mathcal { P } _ { e g o }$ is projected at each timestep and geometrically queried against the generated real-time semantic layouts to compute both constraint satisfaction and routing efficiency.

Dynamic Safety Estimation. Evaluating interaction safety, specifically No At-Fault Collisions (NC) and Time-to-Collision (TTC), requires predicting the stochastic futures of other actors. We assume access to the current estimated velocity and acceleration profiles of surrounding agents. Using these profiles, we kinematically propagate their bounding boxes $\mathcal { P } _ { o b j }$ over the planning horizon to check for intersections with the ego trajectory and to compute the time-to-collision margins.

Two-Dimensional Surrogate Safety Measures. To rigorously evaluate the spatial-temporal proximity to potential collisions across complex driving environments, we utilize a two-dimensional Surrogate Safety Measure (SSM) framework. The foundational metric in this domain is the Timeto-Collision (TTC), which evaluates the temporal proximity to a conflict based on the projected Distance-to-Collision (DTC). Operating under a classical assumption of constant velocity at the instantaneous moment of evaluation [64], the base 2D-TTC is defined using the relative velocity vector ${ \pmb v } _ { i j }$ between the host vehicle i and an interacting agent $j \colon$

$$
T T C = \frac { D T C } { \Vert \pmb { v } _ { i j } \Vert }\tag{14}
$$

While computationally straightforward, the standard constant-velocity assumption exhibits significant drawbacks in dynamic, real-world driving scenarios. Specifically, it fails to capture slow, conscious interactive behaviors, such as yielding, braking, or evasive maneuvering, often leading to inaccurate risk assessments during higher-order kinematic interactions [65, 66].

To address these limitations, we adopt the Modified Time-To-Collision (MTTC) as our primary safety evaluation metric. The MTTC relaxes the constant-velocity constraint by incorporating the relative acceleration vector, $( { \pmb a } _ { i } - { \pmb a } _ { j } )$ , thereby yielding a higher-fidelity, second-order temporal projection. By solving the kinematic displacement equation, the MTTC is formulated as:

$$
M T T C = \frac { - \| \pmb { v _ { i j } } \| \pm \sqrt { \| \pmb { v _ { i j } } \| ^ { 2 } + 2 ( \pmb { a _ { i } } - \pmb { a _ { j } } ) D T C } } { \pmb { a _ { i } } - \pmb { a _ { j } } }\tag{15}
$$

Consistent with established collision warning logic, the final MTTC is determined by extracting the minimum positive real root from this quadratic formulation. Furthermore, by structuring the vehicle states into matrices, we enable the parallel computation of the MTTC across all $i , j$ pairs simultaneously. The resulting indicator sets are subsequently filtered according to the behavioral thresholds established by Ozbay et al. [67], ensuring both high-fidelity risk assessment and computational effi ciency for large-scale, multi-agent evaluation.

## D More Experimental Details

## D.1 Closed-loop Evaluation Setting

Scenario Descriptions. We convert three real-world datasets into BridgeSim platform. BridgeSim NavHard is derived from the NAVSIM benchmark [3], whose logs originate from the nuPlan dataset [12] at 2 Hz. Agent trajectories are up-sampled to 10 Hz via linear interpolation, and HD maps are extracted from the nuPlan map API with a large spatial buffer to cover the full ego trajectory. The converted scenes contain 421 scenarios. BridgeSim-WOMD is converted from the Waymo Open Motion Dataset [68], which provides 9-second scenarios at 10 Hz in a world-frame coordinate system. All agent and map positions are re-centered at the ego vehicle’s initial position, and ego velocity is rotated into the vehicle’s local frame. The converted scenes contain 400 scenarios. BridgeSim-nuScenes is built on the nuScenes dataset [1], which runs at 2 Hz. The converted scenes contain 143 scenarios. Camera images are re-rendered in MetaDrive at 10 Hz, sampled at every fifth step to match the original keyframe rate.

Simulation Settings. All models are evaluated under simulation operating at a default timestep (sim dt=0.1s). Inference is executed at a specified replan rate, with cached waypoints consumed between replan intervals. An initial replay phase is performed before evaluation begins to provide historical temporal buffer for agents. For multi-proposal models, a trajectory scorer selects the final plan within a set of trajectory candidates. For running TTA module, an observational cali bration module is applied to reduce the domain gap between simulation and real-world training data via a flow matching network with a fixed number of sampling steps.

## D.2 Details on Empirical Study in Section 4.2

In Fig. 2 from Section 4.2, the Average Displacement Error (ADE) comparisons are obtained by evaluating the policy’s predicted trajectories over a 4-second horizon against the ground-truth expert demonstrations. To quantify the prediction accuracy accounting for multi-modal outputs, we compute the Minimum Average Displacement Error (minADE) by evaluating the closest predicted trajectory candidate to the ground truth. Let T denote the prediction horizon, $K$ the number of predicted trajectory candidates, $\mathbf { p } _ { t }$ the ground truth spatial coordinates at time step $t ,$ and $\hat { \mathbf { p } } _ { t } ^ { ( k ) }$ the predicted coordinates for the k-th candidate. The metric is formulated as:

$$
\mathrm { m i n A D E } = \operatorname* { m i n } _ { k \in \left\{ 1 , \ldots , K \right\} } \frac { 1 } { T } \sum _ { t = 1 } ^ { T } \left\| \hat { { \mathbf p } } _ { t } ^ { ( k ) } - { \mathbf p } _ { t } \right\| _ { 2 } ,\tag{16}
$$

where $\| \cdot \| _ { 2 }$ denotes the Euclidean $\left( L _ { 2 } \right)$ norm. Furthermore, the closed-loop performance metrics are evaluated using the BridgeSim Driving Score across the BridgeSim-NavHard scenarios.

## D.3 Details on Empirical Study in Section 4.3

In the analysis presented in Fig. 3, we employ the BridgeSim Driving Score as the empirical realization of the return objective J(π). To ensure a rigorous assessment, we evaluate a representative family of state-of-the-art E2E policies [38, 39, 40, 4, 5], reporting the upper and lower performance bounds to characterize the variance across different architectural paradigms. The experimental protocols are defined as follows:

• Fig. 3(a): we evaluate policies over a fixed simulation horizon of T = 80 in BridgeSim-NavHard. To isolate the impact of the execution horizon k, we compare a baseline of fixed k-step prefixes against an “optimal execution” baseline derived via exhaustive search over the policy’s predicted trajectory set.

• Fig. 3(b): we contrast the performance of policies operating under two distinct selection criteria in BridgeSim-Navhard: 1) the OL Objective, which relies on the agent’s learned Q-value estimator, and 2) the CL Objective, where actions are selected via the groundtruth EPDMS metric to simulate an unbiased value function. The evaluation is done across (T ∈ {40, 80, 120, 160}).

• Fig. 3(c): we compute the Pearson correlation between open-loop and closed-loop metrics across the policies. The OL metric is obtained through non-reactive simulation (T = 40) following the NAVSIMV2 protocol [2] in BridgeSim-NavHard. In contrast, the CL metric is derived from the BridgeSim Driving Score across expanding simulation horizons (T ∈ {40, 80, 120, 160}) to observe the decay of predictive validity over time in BridgeSim-NavHard.

![](images/a2e68cc88b8bcdc66929866ef5b00aa5ee7a41213bf7c725ca7861bef1b9371c.jpg)  
Figure 8: Qualitative analysis of simulation artifacts in DriveArena: multi-view incoherence (left) and temporal instability (right). Red boxes highlight inconsistencies that lead to policy failures or metric distortion.

## D.4 Details on Experimental Results in Reactive Evaluation

We show the complete sub-metric scores in reactive evaluations results (see Table 2) in Table 5.

![](images/2d0e28e9a5f959b7b85c1bbfa30935244f2cb6933ef9bbac47be2e45981a09a4.jpg)

![](images/3db97a7c3b2c2a180cabdf53e68714b428f6226362b4027330bd0a81951bd7c7.jpg)  
Figure 9: Qualitative analysis of reconstruction artifacts and ghosting effects in HUGSIM. Red boxes highlight inconsistencies.

Table 5: Performance comparisons with different reactive traffic modes with complete sub-metric scores.
<table><tr><td rowspan="2">Model</td><td colspan="10">IDM</td><td colspan="10">Safety-Critical</td></tr><tr><td>DS</td><td>EPDMS</td><td>RC</td><td>NC DAC</td><td>DDC</td><td></td><td>TL</td><td>TTC</td><td>LK</td><td>HC</td><td>EC</td><td>DS</td><td>EPDM</td><td>RC</td><td>NC DAC</td><td>DDC</td><td>TL</td><td>TTC</td><td>LK</td><td>HC</td><td>EC</td></tr><tr><td>DiffusionDrive</td><td>45.30</td><td>72.95</td><td>59.93</td><td>95.41 85.47</td><td>100.00</td><td>98.36</td><td>89.73</td><td>89.83</td><td>92.31</td><td>40.82</td><td>38.68</td><td>68.16</td><td>54.77</td><td>93.62</td><td>83.86</td><td>100.00</td><td>98.36</td><td>84.97</td><td>90.71</td><td>89.56</td><td>39.13</td></tr><tr><td>DiffusionDriveV2</td><td>31.94</td><td>65.43</td><td>45.85</td><td>94.57 82.09</td><td>100.00</td><td></td><td>98.23</td><td>89.10</td><td>85.42</td><td>74.52 22.99</td><td></td><td>28.17</td><td>61.45 43.50</td><td>93.15</td><td>80.78</td><td>100.00</td><td>98.30</td><td>85.72</td><td>85.81</td><td>70.99</td><td>21.68</td></tr><tr><td>RAP</td><td>60.02</td><td>76.85</td><td>77.20</td><td>97.68</td><td>88.84</td><td>100.00</td><td>98.49</td><td>93.07</td><td>78.16</td><td>94.49 53.84</td><td>51.83</td><td>70.88</td><td>71.22</td><td>95.03</td><td>88.16</td><td>100.00</td><td>98.58</td><td>86.37</td><td>78.26</td><td>90.22</td><td>50.53</td></tr><tr><td>TTA (DiffusionDrive)</td><td>62.68 +17.4</td><td>84.36</td><td>72.28</td><td>96.85 95.63</td><td>100.00</td><td>98.98</td><td>91.57</td><td>92.43</td><td>87.95</td><td>40.13</td><td>55.02 +16.3</td><td>78.95</td><td>67.92</td><td>94.73</td><td>95.21</td><td>100.00</td><td>98.76</td><td>86.64</td><td>91.30</td><td>83.65</td><td>37.11</td></tr><tr><td>TTA (DiffusionDriveV2)</td><td>53.96 +22.0</td><td>77.47</td><td>67.89</td><td>96.08 90.53</td><td></td><td>100.00</td><td>99.43</td><td>89.46</td><td>89.98 85.46</td><td>29.90</td><td>47.64 +19.5</td><td>71.66</td><td>65.91</td><td>93.54</td><td>89.16</td><td>100.00</td><td>99.07</td><td>84.23</td><td>90.11</td><td>81.73</td><td>27.49</td></tr><tr><td>TTA (RAP)</td><td>79.07 +19.1</td><td>90.92</td><td>86.21</td><td>98.28</td><td>98.62</td><td>100.00</td><td>99.02</td><td>95.31</td><td>91.52 92.60</td><td>51.38</td><td>65.94 +14.1</td><td>82.01</td><td>78.66</td><td>95.30</td><td>96.19</td><td>100.00</td><td>99.14</td><td>87.71</td><td>90.26</td><td>88.18</td><td>48.07</td></tr></table>

## D.5 More Discussions of OL Training and Evaluations

Will RL finetuning on OL proxy reward benefit CL performance? Recent papers [40, 69] ad vocate for RL finetuning to enhance planning performance, primarily utilizing open-loop proxy rewards as the training objective. However, as shown in Table 2, our comparison between Diffusion-Drive and DiffusionDriveV2 reveals a significant discrepancy between open-loop and closed-loop outcomes. Specifically, DiffusionDriveV2 exhibits a pronounced performance degradation in CL simulations while it obtains higher OL metrics in NAVSIM. This suggests that optimizing the OL objective doesn’t guarantee the optimization of the CL objective.

To what extent can we rely on OL metrics to predict CL performance? Fig. 3(c) indicates that while OL metrics maintain predictive validity for short horizons (T = H), this correlation decays rapidly as T exceeds H. This decaying trend indicates that while high OL scores signify that a policy possesses sufficient local planning proficiency and safety for in-distribution scenarios, they do not serve as a reliable predictor of CL performance in reactive or out-of-distribution environments. These findings suggest two critical takeaways: 1) scaling open-loop training data doesn’t statistically guarantee improvements for closed-loop performance, and 2) effective policies must prioritize objectives that approximate gold Q-value estimations to ensure long-horizon stability.

## E Limitations of Existing E2E Closed-loop Benchmarks

Existing end-to-end closed-loop benchmarks, such as DriveArena [27] and HUGSIM [28], exhibit limitations stemming from temporal and semantic inconsistencies during simulation.

Generative Artifacts in DriveArena. As illustrated in Fig. 8, DriveArena displays notable simulation discrepancies. 1) Multi-view Incoherence: in the multi-view comparison, discrepancies in the color, length, and placement of lane markings between front and rear camera views (red boxes) can lead to oscillatory policy behavior due to contradictory observations. 2) Temporal Instability: as shown in the temporal sequences, road features such as intersections are inconsistently rendered or spontaneously modified across sequential timestamps (e.g., t = 2s in Singapore and t = 19s in Boston, marked by red boxes), resulting in unstable scene geometry.

Semantic Mismatch in HUGSIM. As shown in Fig. 9, 3D Gaussian Splatting-based methods like HUGSIM encounter challenges with dynamic actor integration. The Sample A & B highlight simulation artifacts and blurring around moving vehicles (red boxes), which are frequently misinterpreted as obstacles. Furthermore, the misalignment between visual rendering and the underlying HD map creates semantic inconsistency.

Structural Invariance in BridgeSim. In contrast, BridgeSim maintains strict structural invariance by decoupling vehicle dynamics from visual rendering. By leveraging the MetaDrive physics engine, the kinematic state $s _ { t }$ serves as the deterministic reference for the environment. Sensor observations $o _ { t }$ are generated via geometric projection rather than generative synthesis, ensuring spatial and temporal consistency across all camera frames and timestamps.

## F Future Work

We expect that future research will focus on building more realistic evaluations and developing methods that enhance driving agents’ safety and robustness under real-world constraints:

1. E2E Closed-loop Benchmarks. Existing CL benchmarks remain limited by observational fidelity, temporal inconsistencies, and evaluation efficiency (see Appendix E). Future benchmarks should move toward unified, hybrid-engine frameworks that combine the controllability of gameengine simulation with the diversity of data-driven world models, enabling scalable yet realistic stress testing of long-horizon CL simulation.

2. E2E Closed-loop Training. Current OL pretraining methods lack error-recovery samples and feedback-driven learning objectives to teach a policy to safely navigate dynamic and reactive environments. Advancing CL training methods, such as scalable variants of RoAD [14], learning with world modeling, and reinforcement learning with reliable reward formulation, remains critical. In particular, defining and learning unbiased value functions that reflect true CL returns in real-world driving is a key open challenge.