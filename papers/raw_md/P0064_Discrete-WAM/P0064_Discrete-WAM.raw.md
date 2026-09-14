# Discrete-WAM: Unified Discrete Vision-Action Token Editing for World-Policy Learning

Xiaomi EV

See Contributions and Acknowledgments section for a full author list.

## Abstract

Autonomous driving requires reasoning about how ego actions shape future world evolution, rather than merely mapping observations to actions. However, most end-to-end methods rely on direct state-to-action imitation, while existing world models often remain weakly aligned with downstream policy generation. We introduce Discrete-WAM, a unified discrete vision-action worldpolicy framework that represents visual observations, future states, high-level decisions, and ego actions within a shared token space. Built on this discrete alignment, Discrete-WAM jointly trains world modeling, world-policy modeling, and policy modeling through multi-task and multi-stage pretraining, allowing action-conditioned future prediction to directly support policy generation. For downstream planning, Discrete-WAM further decomposes policy generation into hierarchical decision prediction and parallel action-token editing, where the decision token provides a highlevel planning skeleton and confidence-based scheduling refines dense future actions eficiently. Experiments on large-scale autonomous-driving benchmarks show that Discrete-WAM achieves strong planning performance while supporting controllable future generation, counterfactual evaluation, surprise-based world-model analysis, and eficient parallel policy decoding. These results suggest that discrete representation alignment, unified world-policy training, and hierarchical token editing provide a promising design paradigm for physical AI.

![](images/670305eb047f984c4002cee50e67cce930af9f1199fb0c2305a4b909defaef14.jpg)  
Figure 1 Overview of Discrete-WAM. Discrete-WAM jointly edits visual, decision, and action tokens in a unified discrete space, ofering editable generation of future observations and planning trajectories through unified pretraining and reward-guided post-training.

## 1 Introduction

Autonomous driving is a representative physical AI problem: an agent must reason about how its actions shape future world evolution, rather than merely react to instantaneous observations [12, 37, 39]. Existing end-to-end (E2E) autonomous driving systems [13, 28, 46, 48, 52] often formulate driving as direct visionto-action mapping via behavior cloning [11], capturing statistical correlations without explicitly modeling action-conditioned dynamics. Prediction-augmented planning introduces future reasoning [25], but many methods still rely on predefined intermediate annotations or task-specific representations [15, 31, 78], which limits generalization across diverse scenes and counterfactual futures. Recent vision-language-action (VLA) models [42, 44, 83, 101] incorporate broader semantic priors through language supervision, yet their reasoning capability is still constrained by annotations, providing a low-bandwidth interface for fine-grained spatialtemporal dynamics [33]. These suggest that reliable physical AI requires unified formulation, where world policy prediction and generation are aligned within the same representation and optimization space.

A key bottleneck is representation alignment. Many autonomous driving systems operate in continuous latent spaces [26, 50, 95], where representations provide smooth interpolation but remain highly entangled and lack explicit compositional semantics [55]. As a result, observations, actions, and future states are only weakly aligned, making it dificult to perform reliable action-conditioned reasoning or compare alternative futures. Discrete representations provide compositional semantic units that can serve as shared anchors across vision, action, and future evolution [41, 59, 92]. More importantly, a shared discrete token space enables observations and actions sequences to be optimized with a unified sequence modeling interface, shared framework, and token-level objectives for tighter multi-modal alignment. For action tokens, however, deterministic discretization error are inevitable under hard quantization.

Beyond representation learning, physical AI requires world modeling to directly support policy optimization. Predicting future observations is valuable not for reconstruction itself, but for evaluating the consequences of candidate actions. Recent generative driving models have demonstrated strong capabilities in future generation and action-conditioned world modeling [2, 48, 86, 96], while autoregressive formulations introduce discrete compositional generation for unified world-action prediction [3, 10, 101]. However, future prediction and policy learning are still commonly optimized as separate modules or auxiliary objectives [29, 30, 42, 43, 45, 74], creating a gap between understanding future dynamics and selecting optimal behaviors. Moreover, driving policies are inherently hierarchical: high-level decisions determine the feasible space of low-level trajectories, while route constraints, interactions, and vehicle dynamics induce strong dependencies among future action tokens. As a result, fully parallel action generation can sufer from dependency mismatch, motivating a unified formulation that jointly learns world dynamics and hierarchical policy construction.

Taken together, these observations suggest that physical AI requires a unified world-policy formulation rather than isolated advances in prediction or control. We identify three key properties: (1) representation alignment across observations, actions, and futures; (2) world-policy alignment between future prediction and action generation; (3) and hierarchical policy construction linking high-level decisions with low-level actions. Based on this perspective, we propose Discrete-WAM, a unified discrete vision-action world-policy framework for autonomous driving. Discrete-WAM formulates driving as sequence modeling over a shared discrete token space, where visual observations, ego actions, future states, and decision variables are jointly represented and modeled through a unified generative process. Rather than treating actions merely as conditioning signals for future prediction, Discrete-WAM models observations, actions, decisions, and future evolution as coupled variables, enabling bidirectional interaction between world dynamics and policy learning. To address representation alignment, we introduce a unified discrete representation together with soft-label action interpolation, reducing deterministic discretization error for continuous control. To bridge the gap between future prediction and policy optimization, Discrete-WAM jointly learns world modeling, world-policy modeling, and policy generation within a shared Transformer architecture, allowing future prediction and action generation to mutually benefit from a common training objective. To account for the hierarchical structure of driving behavior, Discrete-WAM further decomposes policy generation into high-level decision prediction and low-level action-token refinement, enabling eficient parallel generation while preserving decision consistency and long-horizon behavioral structure. Training and inference are designed accordingly through progressive world-policy alignment and confidence-guided parallel refinement, providing an eficient framework for both future reasoning and policy generation. Overall, Discrete-WAM provides a unified framework for representation alignment, world-policy learning, and hierarchical decision making, advancing physical AI from reactive imitation toward decision-oriented world modeling

![](images/66589d128f35720bc1479e69b4c6a41e0a6f53a29f5efb2dcade2ac5c19b804b.jpg)  
Figure 2 Model architecture of Discrete-WAM. Discrete-WAM is a unified vision-action world-policy model for autonomous driving. The architecture converts camera observations into discrete visual tokens, represents future ego motion with discrete action tokens, and injects ego-state, navigation, and high-level decision information as conditioning tokens. Built on a shared Transformer backbone, Discrete-WAM supports three complementary training modes: world modeling for action-conditioned vision prediction, world-policy modeling for joint action and future-vision prediction, and policy modeling for decision-conditioned action generation. This unified token interface enables visual observations, driving decisions, and future actions to be modeled and edited within the same discrete sequence space.

Our contributions are summarized as follows:

• We propose a multi-task world-policy framework that jointly models world dynamics, world-policy, and policy generation within a unified training paradigm. The framework is enabled by a shared discrete token space that aligns observations, decisions and actions across temporal horizons.

• We formulate planning as hierarchical decision-conditioned action-token editing and develop post-training strategies with confidence-guided parallel editing, improving the suitability of parallel discrete difusion for autonomous driving.

• Comprehensive evaluations across planning benchmarks, world-model surprise analysis, attention-based grounding, scheduling dynamics, and inference-eficiency studies validates the efectiveness of the proposed physical-AI design paradigm.

## 2 Architecture

## 2.1 Base architecture of Discrete-WAM

The Discrete-WAM architecture consists of four main components: (1) a vision VQ Tokenizer that encodes visual observations into discrete semantic tokens and a projector that align vision feature with transformer hidden dimension; (2) a context encoder that injects ego-state and navigation commands into the latent sequences; (3) a decoder-only Transformer backbone that jointly models observations, actions, and future evolution within a unified token space; and (4) multi-task prediction heads for world modeling, policy generation, and world-action sequence generation.

## 2.2 Vision Tokenization

The vision tokenizer converts continuous camera observations into compact discrete visual tokens, providing a token-level interface between raw images and the Transformer backbone. This discrete representation enables visual observations to be handled in the same sequence format as action tokens, while preserving the scene semantics required for downstream world and policy modeling. To obtain compact visual representations, we follow the previous work [91] and pretrain a VQ-VAE-based tokenizer [71] to encode front-view camera images into discrete visual tokens.

## 2.3 Action Tokenization

For action representation, we convert continuous future motion into a discrete-token-compatible representation over an acceleration vocabulary. Given a future trajectory over H time steps, we first fit the discrete trajectory with a cubic spline to obtain a smooth continuous curve. We then compute the ego-centric 2D acceleration at each future step using second-order finite diferences, denoted as $( a _ { x } , a _ { y } )$ , where $a _ { x }$ and $a _ { y }$ correspond to longitudinal and lateral acceleration, respectively. The spline fitting step improves the continuity of the derived acceleration sequence and ensures that integrating the recovered accelerations can closely match the original discrete trajectory.

We construct a uniformly distributed 2D acceleration vocabulary by independently partitioning the valid ranges of $a _ { x }$ and $a _ { y }$ into $N _ { x }$ and $N _ { y }$ bins. The Cartesian product of these bins forms a grid-structured action vocabulary with size $N _ { x } \times N _ { y }$ . Instead of assigning each continuous acceleration vector to a single nearest bin, which would introduce deterministic hard-quantization error, we represent it with a soft target over its neighboring vocabulary entries. Specifically, for each acceleration component, we find the two adjacent bin centers that bracket the continuous value and assign interpolation weights according to its relative position between them. In the 2D acceleration vocabulary, this produces a soft label over the four neighboring prototypes around $( a _ { x } , a _ { y } )$ . Under this grid interpolation, the continuous acceleration admits an exact interpolation representation within each acceleration grid cell.

During training, the action head is optimized with cross-entropy against this soft target distribution rather than a one-hot label. At inference time, the predicted action distribution can be mapped back to continuous acceleration by taking the weighted sum over the acceleration vocabulary. Under exact recovery of the soft target distribution, the continuous acceleration can be reconstructed exactly as the weighted sum of the neighboring vocabulary prototypes. Therefore, the proposed soft-label representation removes deterministic hard-assignment quantization error, while the remaining reconstruction error is attributed to distribution prediction mismatch. The corresponding derivation and error bound are provided in Appendix.

As a result, a future action sequence is represented as $\mathbf { A } _ { t + 1 : t + H }$ over the discrete acceleration vocabulary, while continuous control values are preserved through soft-label interpolation. This action tokenization enables visual tokens and action tokens to be modeled jointly in the same Transformer token space while avoiding the deterministic error introduced by hard quantization of continuous actions.

## 2.4 Unified World Policy

Discrete-WAM formulates autonomous driving as a unified world-policy modeling problem over discrete visual, decision, and action tokens. At time step $t ,$ we denote the scene context as $\mathbf { C } _ { t } .$ , which contains historical visual observations, ego-state information, and navigation commands. The future visual observations are represented as discrete visual token sequences $\mathbf { V } _ { t + 1 : t + H } ,$ , and the future action policy is represented as discrete action token sequences $\mathbf { A } _ { t + 1 : t + H }$ , where each action token corresponds to a quantized acceleration prototype defined in Sec. 2.3. We further denote the high-level decision condition as $\mathbf { D } _ { t }$ , which captures sparse low-frequency driving structure, such as maneuver intent, target lane, coarse waypoint, speed trend, or interaction priority.

Under this notation, Discrete-WAM integrates three training modes under a shared token-editing interface. These modes difer in which token streams are used as conditioning inputs and which token streams are treated as prediction targets.

The first mode is world modeling, whose objective is vision prediction. Given the scene context $\mathbf { C } _ { t }$ and future action tokens $\mathbf { A } _ { t + 1 : t + H }$ , the model predicts future visual tokens $\mathbf { V } _ { t + 1 : t + H }$ . This task trains the model to understand how the scene evolves under a specified action sequence, and provides action-conditioned world dynamics for downstream policy learning.

The second mode is world-policy modeling, which jointly trains vision prediction and action prediction. In this mode, the model reasons about future actions and their induced visual consequences within the same token sequence. Action tokens represent the future policy, while visual tokens represent the corresponding future world states. This formulation encourages the model to couple policy generation with world evolution, rather than learning them as independent objectives.

The third mode is policy modeling, whose objective is decision prediction followed by action prediction. The model first predicts the high-level decision condition $\mathbf { D } _ { t }$ from the scene context $\mathbf { C } _ { t }$ . Conditioned on this decision, the action-token planner then predicts the future action sequence $\mathbf { A } _ { t + 1 : t + H }$ . This hierarchical decomposition separates policy learning into two levels: the high-level decision task captures multi-modal driving choices, while the low-level action prediction task focuses on generating smooth and temporally consistent trajectories conditioned on the selected decision.

Together, these three modes provide a unified architecture for action-conditioned world prediction, joint world-policy learning, and decision-conditioned action generation. The mathematical task formulations are described in Sec. 3.

## 3 Method

## 3.1 Unified Pretraining

Following the unified world-policy formulation in Sec. 2.4, pretraining instantiates the conditional token-editing objective with multiple task families. Each task uses the same discrete visual and action token interface, but difers in which token streams are treated as conditioning inputs and which corrupted tokens are supervised as editing targets. This design allows world modeling, policy prediction, and joint world-policy modeling to share one training framework while preserving their task-specific conditioning structure.

Training tasks. We instantiate unified pretraining with three task families: world modeling, policy modeling, and joint world-policy modeling.

Tokenization. We tokenize both visual observations and future actions into discrete token sequences so that they can be jointly modeled within a unified Transformer architecture.

For image tokenization, we employ the pretrained tokenizer. Following the previous work [91] whose tokenizer is aligned with [66], the quantizer contains a codebook of size $K _ { V }$ . Each input image is divided into non-overlapping $H _ { V } \times W _ { V }$ patches and encoded into a sequence of discrete visual tokens. This process is applied independently to each of the H input frames, producing the visual token sequence $\mathbf { V } _ { t + 1 : t + H }$

For action tokenization, we discretize the continuous future trajectory using the acceleration-based quantization described above. Specifically, the smoothed trajectory is converted into ego-centric longitudinal and lateral accelerations, which are then quantized into a grid-structured acceleration vocabulary. This yields a discrete action token sequence $\mathbf { A } _ { t + 1 : t + H }$ , where each token corresponds to a 2D acceleration prototype.

To incorporate action tokens into downstream discrete difusion modeling, we associate each action token with a learnable embedding through an action embedding table. During difusion training, corrupted or partially masked action tokens are embedded and fed into the Transformer together with visual tokens, while the model is trained to predict action tokens under the discrete difusion objective. Through joint optimization, the action embeddings learn compact representations of discrete motion prototypes and are implicitly aligned with visual token representations in the shared hidden space. As a result, visual and action tokens can be processed jointly by a unified Transformer, enabling visually conditioned future action generation through discrete difusion. Detailed token design are referred in Appendix 7.2.1.

World modeling. The world modeling task learns action-conditioned future visual prediction. Given the scene context $\mathbf { C } _ { t }$ and a future action sequence $\mathbf { A } _ { t + 1 : t + H }$ , the model predicts the future visual token sequence

$\mathbf { V } _ { t + 1 : t + H }$ . This can be written as

$$
p _ { \theta } ( \mathbf { V } _ { t + 1 : t + H } \mid \mathbf { C } _ { t } , \mathbf { A } _ { t + 1 : t + H } ) .\tag{1}
$$

During training, future action tokens are provided as conditioning inputs through teacher forcing, and the supervision is applied to future visual tokens. This task trains the model to capture how diferent action sequences induce diferent future world evolutions.

Policy modeling. The policy modeling task learns hierarchical decision-conditioned action generation. Following the notation in Sec. 2.4, the model first predicts a high-level decision skeleton $\mathbf { D } _ { t }$ from the scene context $\mathbf { C } _ { t } ,$ , and then predicts the future action sequence $\mathbf { A } _ { t + 1 : t + H }$ conditioned on both the context and the decision tokens:

$$
\begin{array} { r } { p _ { \psi , \theta } ( \mathbf { A } _ { t + 1 : t + H } , \mathbf { D } _ { t } \mid \mathbf { C } _ { t } ) = p _ { \psi } ( \mathbf { D } _ { t } \mid \mathbf { C } _ { t } ) p _ { \theta } ( \mathbf { A } _ { t + 1 : t + H } \mid \mathbf { C } _ { t } , \mathbf { D } _ { t } ) . } \end{array}\tag{2}
$$

Theoretical analysis. This hierarchical decomposition separates policy learning into two levels: the high-level decision task captures multi-modal driving choices, while the low-level action prediction task generates smooth and temporally consistent trajectories under the selected decision condition. Here, $\mathbf { D } _ { t }$ is treated as a sparse latent skeleton that encodes low-frequency planning structure, such as coarse maneuver intent, reference motion trend, or other decision-level constraints.

The motivation for introducing $\mathbf { D } _ { t }$ is that future action tokens are not conditionally independent when only the scene context is given. Let $U \subseteq \{ 1 , \ldots , H \}$ denote a subset of future steps, and let $\mathbf { A } _ { U } = \left\{ \mathbf { A } _ { t + h } : h \in U \right\}$ denote the corresponding action-token group. We use $\mathrm { T C } ( \cdot \mid \cdot )$ to denote conditional total correlation, which measures the residual statistical dependence among a group of tokens under a given condition. As derived in Appendix 7.3.2, conditioning on an upstream decision skeleton changes the residual dependence according to

$$
\mathbb { E } _ { \mathbf { D } _ { t } } \mathrm { T C } ( \mathbf { A } _ { U } \mid \mathbf { C } _ { t } , \mathbf { D } _ { t } ) = \mathrm { T C } ( \mathbf { A } _ { U } \mid \mathbf { C } _ { t } ) - R _ { \mathbf { D } } ( U \mid \mathbf { C } _ { t } ) ,\tag{3}
$$

where $R _ { \mathbf { D } } ( U \mid \mathbf { C } _ { t } )$ is the redundancy gain brought by the decision skeleton. This identity shows that decision conditioning reduces residual action-token dependence only when $R _ { \bf D } ( U \mid { \bf C } _ { t } ) > 0$

Appendix 7.3.3 further gives a suficient condition for positive redundancy gain. Under the residual mixing assumption, the skeleton-conditioned dependence between future action tokens decays with their temporal distance:

$$
I ( \mathbf { A } _ { t + i } ; \mathbf { A } _ { t + j } \mid \mathbf { C } _ { t } , \mathbf { D } _ { t } ) \leq \beta \exp \left( - \frac { d ( i , j ) } { \ell _ { D } } \right) ,\tag{4}
$$

where $\beta$ measures the remaining local coupling strength and $\ell _ { D }$ denotes the residual correlation length after conditioning on the decision skeleton. This assumption means that once the low-frequency driving intent is explained by $\mathbf { D } _ { t } .$ , the remaining fine action tokens mainly encode local residual corrections. If the original action-token group has a dependence lower bound $\mathrm { T C } ( \mathbf { A } _ { U } \mid \mathbf { C } _ { t } ) \geq \kappa ( U )$ , then

$$
\kappa ( U ) > \mathbb { E } _ { \mathbf { D } _ { t } } \left[ \sum _ { \left\{ i , j \right\} \subset U } \beta \exp \left( - \frac { d ( i , j ) } { \ell _ { D } } \right) \right] \implies R _ { \mathbf { D } } ( U \mid \mathbf { C } _ { t } ) > 0 .\tag{5}
$$

Therefore, a valid decision skeleton reduces residual total correlation when it explains stronger group-level low-frequency dependence than the remaining skeleton-conditioned local dependence.

The same analysis also yields a schedule-level KL upper bound when decision prediction error and token-level model error are considered. Let $\pi$ denote the token-editing schedule, $A _ { r }$ the active edit set at round $r ,$ and $S _ { r }$ the editing state before round r. Appendix 7.3.4 shows that

$$
D _ { \mathrm { K L } } \left( q ( \mathbf { A } \mid \mathbf { C } _ { t } ) \| p _ { \psi , \theta , \pi } ( \mathbf { A } \mid \mathbf { C } _ { t } ) \right) \leq \delta _ { D } + \delta _ { \mathrm { i n i t } } + \mathcal { B } _ { \mathrm { m o d e l } } ( \pi ) + \mathcal { U } _ { \mathrm { d e p } } ( \pi ) ,\tag{6}
$$

where $\delta _ { D }$ is the decision prediction error, $\delta _ { \mathrm { i n i t } }$ measures the mismatch of the initial editing proposal, $B _ { \mathrm { m o d e l } } ( \pi )$ accumulates token-level model errors over edit rounds, and $\mathcal { U } _ { \mathrm { d e p } } ( \pi )$ bounds the residual dependence within each active edit set. This bound suggests that hierarchical decision modeling is beneficial when the decision skeleton is predictable and reduces residual action-token dependence enough to ofset its own prediction cost.

![](images/8f0ca40992a5caa64739f17baf937e7cb8956322ccf6eaae0d55f1767ec10bef.jpg)

![](images/f274e5dc6e1401c46588f261268d45c76354972b6779f95a1923d928b348433d.jpg)

![](images/f85b580b9ee0748619f5662e9b8e35f97589d89f0dcbb8156530fbddcca4a3cb.jpg)  
Figure 3 Attention masking strategies for Discrete-WAM pretraining. Discrete-WAM features three diferent types of attention masking that controls respective task families during unified pretraining.

World-policy modeling. The world-policy modeling task jointly learns action prediction and actionconditioned world prediction without using explicit decision tokens. Given the scene context $\mathbf { C } _ { t } ,$ future action tokens and future visual tokens are arranged as an interleaved sequence along the prediction horizon. At each future step, action prediction is conditioned on the available previous action and visual tokens, while visual prediction is conditioned on the available previous action and visual tokens as well as the current action token. This matches the task-specific attention mask, where each prediction block can attend to its permitted historical action-vision context but cannot access its corresponding clean target tokens.

Let $\mathbf { Y } _ { t + 1 : t + H }$ denote the interleaved future token sequence composed of action and visual tokens:

$$
\mathbf { Y } _ { t + 1 : t + H } = [ \mathbf { A } _ { t + 1 } , \mathbf { V } _ { t + 1 } , \ldots , \mathbf { A } _ { t + H } , \mathbf { V } _ { t + H } ] .\tag{7}
$$

Then the world-policy objective can be described as prefix-conditioned token prediction over this interleaved sequence:

$$
p _ { \theta } ( \mathbf { Y } _ { t + 1 : t + H } \mid \mathbf { C } _ { t } ) = \prod _ { h = 1 } ^ { H } p _ { \theta } ( \mathbf { A } _ { t + h } \mid \mathbf { C } _ { t } , \mathbf { Y } _ { t + 1 : t + h - 1 } ) p _ { \theta } ( \mathbf { V } _ { t + h } \mid \mathbf { C } _ { t } , \mathbf { Y } _ { t + 1 : t + h - 1 } , \mathbf { A } _ { t + h } ) .\tag{8}
$$

During training, the corresponding attention mask implements this dependency pattern under the token-editing formulation: noisy action and visual tokens are edited using the permitted historical action-vision context, while clean target tokens are kept isolated from their noisy counterparts.

Meanwhile, the world-policy model always applies token-editing supervision to future visual tokens, encouraging the model to recover future world states from corrupted visual tokens under action-conditioned context. In addition, the action stream can be trained with the same token-editing strategy, where corrupted future action tokens are edited toward the ground-truth action sequence. This joint supervision enables the model to learn not only plausible policy generation from the current context, but also how the generated actions shape subsequent visual evolution. As a result, world-policy modeling provides a unified objective for action generation, world prediction, and action-conditioned counterfactual reasoning.

Task-specific attention masks. We use task-specific attention masks to match the information flow required by each training objective. The general principle is that historical context tokens are visible as teacher-forced conditioning information, while current or future corrupted tokens are predicted through token editing without leaking their corresponding clean targets.

For world modeling, future action tokens are treated as clean conditioning inputs rather than editing targets. Therefore, the action stream does not use dual clean-noisy filling in this task. The future visual stream is constructed with the token-editing format, and the model predicts corrupted future visual tokens conditioned on historical observations, ego-state and navigation tokens, and the provided future action sequence.

For policy modeling, the context tokens follow a causal attention structure, so the model can condition on historical observations and available state information without accessing future context. The future action tokens form the editing target block and are allowed to attend bidirectionally within the action block. This bidirectional action attention allows the model to refine a complete future action sequence jointly, while the causal context mask prevents future information leakage from the observation side.

For world-policy modeling, both future visual tokens and future action tokens can be trained with tokenediting supervision. We adopt a dual-path filling order for each editable stream, where clean tokens and noisy tokens are placed as separate blocks. The attention mask enforces bidirectional isolation between the clean target block and the corresponding noisy prediction block: noisy tokens can use the permitted context and task-specific visible conditions, but cannot directly attend to their clean targets. During training, teacher forcing provides historical ground-truth information as context, while the model learns to edit noisy visual and action tokens into their clean targets.

Training objectives. The unified pretraining objective combines token-level classification losses with continuous motion reconstruction losses. For visual token editing, the model is supervised with a cross-entropy loss over the discrete visual vocabulary. Unlike objectives that only supervise corrupted positions, we apply the token classification loss to all editable visual token positions, including both clean and corrupted tokens. For corrupted positions, the loss trains the model to recover the original clean targets from noisy inputs. For clean positions, the same loss encourages an identity mapping, requiring the model to preserve tokens that are already close to the ground truth rather than unnecessarily editing them. This all-position supervision provides an implicit stopping signal for token editing: the model learns not only how to correct noisy tokens, but also when no edit is needed. When latent visual embeddings are available, we further apply a latent reconstruction loss to preserve fine-grained visual semantics beyond discrete token indices.

For action token editing, the model is supervised with a cross-entropy loss over the discrete action vocabulary. In addition to token classification, we impose motion-level supervision to ensure that the discrete action distribution remains physically consistent with continuous future motion. First, we supervise the decoded acceleration associated with the predicted action distribution, encouraging the discrete action tokens to preserve accurate low-level motion semantics. Second, we convert the predicted action distribution into continuous accelerations and integrate them twice over time to reconstruct the future ego trajectory, on which a trajectory-level regression loss is applied. In addition, we introduce an auxiliary factorized position classification loss, where the ground-truth future x and y positions are discretized into separate position vocabularies and supervised independently. The trajectory obtained by integrating decoded accelerations is used only for the trajectory-level regression loss. The detailed vocabulary configuration and loss formulation are provided in Appendix 7.2.

A naive way to obtain continuous accelerations for motion reconstruction is to multiply the predicted action probabilities with the acceleration vocabulary and use the resulting full-distribution expectation. However, action prediction is often inherently multi-modal: diferent acceleration modes may correspond to diferent plausible driving decisions. Directly taking the expectation over the full predicted distribution can average incompatible modes and produce physically implausible intermediate accelerations. We refer to this issue as decoding-induced mode averaging.

To mitigate this issue, we use a mode-aware decoding strategy only for constructing the continuous acceleration, trajectory reconstruction, and auxiliary position supervision losses. We fit the predicted categorical distribution over the acceleration vocabulary with a multi-modal Gaussian mixture. Specifically, we consider GMMs with one, two, and three components and select the one with the lowest fitting error. We then apply top-p sampling to select one Gaussian mode, re-normalize the action probabilities within the selected mode, and compute the expected acceleration from the re-normalized distribution and the acceleration vocabulary. The resulting mode-aware acceleration is integrated over time for trajectory reconstruction.

This mode-aware decoding is independent of the soft-label interpolation used for action tokenization. The latter removes deterministic hard-assignment quantization error in the construction of the action target, whereas the former is introduced to prevent continuous reconstruction losses from averaging mutually incompatible action modes. The mode-selection step introduces an additional approximation, whose role and error decomposition

are discussed in Appendix 7.2.1.

The final objective is a weighted sum of task-dependent loss terms:

$$
\begin{array} { r } { \mathcal { L } = \lambda _ { \mathrm { v } } \mathcal { L } _ { \mathrm { v } } ^ { \mathrm { c l s } } + \lambda _ { a } \mathcal { L } _ { a } ^ { \mathrm { c l s } } + \lambda _ { \mathrm { a c c } } \mathcal { L } _ { \mathrm { a c c } } + \lambda _ { \mathrm { t r a j } } \mathcal { L } _ { \mathrm { t r a j } } + \lambda _ { \mathrm { p o s } } \mathcal { L } _ { \mathrm { p o s } } ^ { \mathrm { c l s } } + \lambda _ { s } \mathcal { L } _ { s } ^ { \mathrm { c l s } } + \lambda _ { \mathrm { d e c } } \mathcal { L } _ { \mathrm { d e c } } . } \end{array}\tag{9}
$$

Here, $\mathcal { L } _ { v } ^ { \mathrm { c l s } }$ denotes the cross-entropy loss over the visual token vocabulary, and $\mathcal { L } _ { a } ^ { \mathrm { c l s } }$ denotes the cross-entropy loss over the action token vocabulary. $\mathcal { L } _ { \mathrm { a c c } }$ is the acceleration-level regression loss, while $\mathcal { L } _ { \mathrm { t r a j } }$ is the trajectory level regression loss obtained after integrating predicted accelerations into future ego trajectories. $\mathcal { L } _ { \mathrm { p o s } } ^ { \mathrm { c l s } }$ denotes the auxiliary factorized position classification loss over the integrated future positions, with separate classification heads for longitudinal and lateral coordinates. $\mathcal { L } _ { s } ^ { \mathrm { c l s } }$ denotes the classification loss for auxiliary special tokens, such as task or control tokens used to organize diferent training sequences. ${ \mathcal { L } } _ { \mathrm { d e c } }$ terms for decision classification loss. The coeficients $\lambda _ { v } , \lambda _ { a } , \lambda _ { \mathrm { a c c } } , \lambda _ { \mathrm { t r a j } } , \lambda _ { \mathrm { p o s } } , \lambda _ { \mathrm { d e c } }$ , and $\lambda _ { s }$ balance the relative contribution of each loss term. Diferent training tasks activate diferent subsets of these losses according to their prediction targets.

Training schedule. We adopt a multi-stage training schedule to progressively align visual world modeling and action generation. In the first stage, we perform visual pretraining with both world-policy modeling and world modeling tasks. Only the vision prediction loss is applied in this stage, while future action tokens are provided through teacher forcing as conditioning inputs. This stage trains discrete visual representations that are predictive of future scene evolution and aligned with action-conditioned dynamics.

In the second stage, we jointly train visual and action prediction. In addition to world modeling, the world-policy modeling task also activates the action prediction loss, so the model learns to recover both future visual tokens and future action tokens under the shared token-editing framework. This stage strengthens the coupling between policy generation and action-conditioned world evolution.

In the third stage, we perform action finetuning with a LoRA adapter. This stage focuses on the discrete difusion policy model, where the model is finetuned specifically for future action generation and refinement while preserving the visual-world representations learned in the earlier stages.

## 3.2 Post Training

To further capture rare or safety-critical behaviors by limited coverage in the dataset, we apply a post-training fine-tuning stage that leverages model-based trajectory sampling and reinforcement learning to refine the policy on challenging scenarios while preserving previously learned behavior.

Policy sampling. For each driving scene context $\mathbf { C } _ { t }$ , Discrete-WAM generates a group of candidate trajectories $\{ \tau _ { 1 } , \dots , \tau _ { G } \}$ via token-edit planner for eficient exploration. Each trajectory is iteratively edited through r rounds by: $\tau _ { i } \sim p _ { \theta } ( \hat { \mathbf { A } } _ { t + 1 : t + H } ^ { ( r ) } \mid \tilde { \mathbf { A } } _ { t + 1 : t + H } ^ { ( r - 1 ) } , \hat { \mathbf { D } } _ { t } , \mathbf { C } _ { t } ) p _ { \psi } ( \hat { \mathbf { D } } _ { t } \mid \mathbf { C } _ { t } )$ . This produces a diverse set of high-quality rollouts evaluated using online reward function $R ( \tau _ { i } )$ , i.e., (E)/PDMS metrics. The hierarchical modeling for decision of $\mathbf { D } _ { t }$ further embraces two type of sampling strategies. 1) Group sampling under the most probable decision arg max $p _ { \psi } ( \hat { \mathbf { D } } _ { t } \mid \mathbf { C } _ { t } )$ . 2) A parallel line of sampling strategy that Discrete-WAM adopts directly leverage the full distribution of decisions $\hat { \mathbf { D } } _ { t }$ , and conduct group sampling specific for each decision token. This further ofers decision-level post training update for log $p _ { \psi } ( \hat { \mathbf { D } } _ { t } \mid \mathbf { C } _ { t } )$

Training objectives. Following the Grouped Relative Policy Optimization (GRPO) paradigm, we compute per-token log-probabilities under the current policy $\begin{array} { r } { \pi _ { \theta , i } ^ { A } \sim \frac { 1 } { H } \sum _ { h = 1 } ^ { H } \log _ { \mathbf { A } \sim \tau _ { i } } p _ { \theta } ( \hat { \mathbf { A } } _ { t + h } \mid \hat { \mathbf { A } } _ { < t + h } , \hat { \mathbf { D } } _ { t } ^ { i } , \mathbf { C } _ { t } ) } \end{array}$ using a one-step reconstruction estimator following [99]. Decision distribution are directly gathered as $\pi _ { \theta , i } ^ { D } \sim$ $\log p _ { \psi } ( \hat { \mathbf { D } } _ { t } ^ { i } \mid \mathbf { C } _ { t } )$ . The advantage is computed by $\begin{array} { r } { A _ { i } = R ( \tau _ { i } ) - \sum _ { i = 1 } ^ { G } R ( \tau _ { i } ) } \end{array}$ , the overall objective becomes:

$$
\mathbf { E } _ { \tau \sim \pi _ { \theta , \psi } } \sum _ { k \in ( A , D ) } \left[ \frac { 1 } { G } \sum _ { i = 1 } ^ { G } \operatorname* { m i n } \left( \rho _ { i } ^ { k } A _ { i } , \mathrm { c l i p } ( \rho _ { i } ^ { k } , 1 - \epsilon , 1 + \epsilon ) A _ { i } \right) - \mathrm { K L } ( \pi _ { \theta , \psi } ^ { k } | | \pi _ { \mathrm { r e f } } ^ { k } ) \right] ,\tag{10}
$$

where $\rho _ { i } ^ { k } = \pi _ { \theta , \psi , i } ^ { k } / \pi _ { \mathrm { r e f , \ j } } ^ { k }$ terms for the importance sampling ratio.

<table><tr><td>Method</td><td>NC↑</td><td>DAC↑</td><td>DDC↑</td><td>TLC↑</td><td>EP↑</td><td>TTC↑</td><td>LK↑</td><td>HC↑ EC↑</td><td>EPDMS*↑</td><td></td><td>EPDMS↑</td></tr><tr><td>Transfuser [16]</td><td>96.9</td><td>89.9</td><td>97.8</td><td>99.7</td><td>87.1</td><td>95.4</td><td>92.7</td><td>98.3</td><td>87.2</td><td>76.7</td><td></td></tr><tr><td>ReCogDrive [44]</td><td>98.3</td><td>95.2</td><td>99.5</td><td>99.8</td><td>87.1</td><td>97.5</td><td>96.6</td><td>98.3</td><td>86.5</td><td>83.6</td><td>一</td></tr><tr><td>WAM-Flow [82]</td><td>98.5</td><td>94.5</td><td>99.5</td><td>99.8</td><td>86.9</td><td>96.8</td><td>97.4</td><td>97.6</td><td>73.9</td><td>84.7</td><td></td></tr><tr><td>Epona [96]</td><td>97.1</td><td>95.7</td><td>99.3</td><td>99.7</td><td>88.6</td><td>96.3</td><td>97.0</td><td>98.0</td><td>67.8</td><td></td><td>85.1</td></tr><tr><td>DiffusionDriveV2 [103]</td><td>97.7</td><td>96.6</td><td>99.2</td><td>99.8</td><td>88.9</td><td>97.2</td><td>96.0</td><td>97.8</td><td>91.0</td><td>85.5</td><td>87.5</td></tr><tr><td>Hydra-MDP++ [46]</td><td>98.4</td><td>98.0</td><td>99.4</td><td>99.8</td><td>87.5</td><td>97.7</td><td>95.3</td><td>98.3</td><td>77.4</td><td>85.1</td><td></td></tr><tr><td>DriveSuprim [90]</td><td>97.8</td><td>97.9</td><td>99.5</td><td>99.9</td><td>90.6</td><td>97.1</td><td>96.6</td><td>98.3</td><td>77.9</td><td>86.0</td><td></td></tr><tr><td>DriveVLA-W0 [42]</td><td>98.5</td><td>99.1</td><td>98.0</td><td>99.7</td><td>86.4</td><td>98.1</td><td>93.2</td><td>97.9</td><td>58.9</td><td>86.1</td><td></td></tr><tr><td>DreamerAD [89]</td><td>98.0</td><td>97.2</td><td>99.5</td><td>99.8</td><td>87.8</td><td>97.4</td><td>97.5</td><td>98.3</td><td>72.4</td><td></td><td>87.7</td></tr><tr><td>SparseDriveV2 [68]</td><td>98.1</td><td>98.1</td><td>99.6</td><td>99.8</td><td>91.1</td><td>97.3</td><td>96.9</td><td>98.2</td><td>78.4</td><td>86.7</td><td>90.1</td></tr><tr><td>Discrete-WAM</td><td>98.5</td><td>98.2</td><td>99.7</td><td>99.8</td><td>90.5</td><td>97.9</td><td>97.2</td><td>98.3</td><td>78.1</td><td>87.0</td><td>90.4</td></tr></table>

Table 1 Comparison with state-of-the-art methods on the NAVSIM-v2 benchmark. We report no collision (NC), drivable area compliance (DAC), driving direction compliance (DDC), trafic light compliance (TLC), ego progress (EP), time-to-collision (TTC), lane keeping (LK), human comfort (HC), ego comfort (EC), EPDMS<sup>∗</sup> (before benchmark bug fix), and EPDMS. The best results are highlighted in bold, and the second-best result is underlined.

## 4 Evaluation

## 4.1 Setup

Dataset and benchmarks. We manifest the E2E generation and planning capabilities of Discrete-WAM on NAVSIM-v1 and v2 benchmark [8, 17], which ofers large-scale driving scenarios for end-to-end driving. Following the standard protocol, we evaluate Discrete-WAM on the navtest split, containing 12k driving scenes sampled at 2 Hz. NAVSIM evaluates planning quality of 4s horizon trajectories with PDMS and the extended EPDMS, where safety- and rule-critical metrics are incorporated as multiplicative constraints, while progress and comfort-related terms are combined through weighted aggregation. The reported metrics include no at-fault collision (NC), drivable area compliance (DAC), driving direction compliance (DDC), trafic light compliance (TLC), ego progress (EP), time-to-collision (TTC), lane keeping (LK), history comfort (HC), and extended comfort (EC). Detailed metric formulations and baselines are referred in the Appendix 7.2.4.

Implementation details. Discrete-WAM follows a multi-stage training schedule as previously detailed in Sec. 3.1. The unified world-policy pretraining with task families is conducted on the full nuPlan training set [6] for 200k steps with a learning rate of $1 \times 1 0 ^ { - 4 }$ . After pretraining, Discrete-WAM receives supervised finetuning on navtrain dataset for 10 epochs. Finally, Discrete-WAM applies RL post-training for another 2 epochs to further improve planning behavior. Both the SFT and RL post-training stages are performed with LoRA finetuning at a learning rate of $1 \times 1 0 ^ { - 5 }$ . All stages are trained on 32 NVIDIA H20 GPUs using AdamW optimizer with a cosine schedule. Model details are referred in the Appendix 7.2.4.

## 4.2 Quantitative Results

Planning results. On NAVSIM v2, Discrete-WAM delivers a strong planning result of 90.4 EPDMS, outperforming a series of method jointly built with world modeling, post-training, or generative planers with discretizations. Specifically, Discrete-WAM improves EPDMS of +2.7 over WAM-Flow [82], while both improving safety and comfort. Compared with world-model-based methods [42, 89, 96], Discrete-WAM ofers a 6.2% relative improvement over [96], and 3.1% of [89]. Compared with reinforced cognitive planner, Discrete-WAM performs a 4.1% relative gain. Consistent performance gains are also observed on the NAVSIMv1 benchmark, where Discrete-WAM achieves competitive results with a +2.1 PDMS improvement over WAM-Flow [82] and a +7.0 PDMS improvement over world-model-based planners [96]. These results indicate that both unified world-policy pretraining and the token-editing formulation contribute to the planning performance gains. The former learns aligned vision-action-future representations that support compositional generalization, while the latter provides predictive scenario latents that enhance causal awareness and enable more reliable planning refinement.

<table><tr><td>Method</td><td>NC↑</td><td>DAC↑</td><td>TTC↑</td><td>Comf.↑</td><td>EP↑</td><td>PDMS↑</td></tr><tr><td>VADv2 [13]</td><td>97.2</td><td>89.1</td><td>91.6</td><td>100</td><td>76.0</td><td>80.9</td></tr><tr><td>UniAD [28]</td><td>97.8</td><td>91.9</td><td>92.9</td><td>100</td><td>78.8</td><td>83.4</td></tr><tr><td>Transfuser [16]</td><td>97.7</td><td>92.8</td><td>92.8</td><td>100</td><td>79.2</td><td>84.0</td></tr><tr><td>PARA-Drive [79]</td><td>97.9</td><td>92.4</td><td>93.0</td><td>99.8</td><td>79.3</td><td>84.0</td></tr><tr><td>GoalFlow [81]</td><td>98.3</td><td>93.8</td><td>94.3</td><td>100</td><td>79.8</td><td>85.7</td></tr><tr><td>Epona [96]</td><td>97.9</td><td>95.1</td><td>93.8</td><td>99.9</td><td>80.4</td><td>86.2</td></tr><tr><td>Hydra-MDP++ [46]</td><td>97.6</td><td>96.0</td><td>93.1</td><td>100</td><td>80.4</td><td>86.6</td></tr><tr><td>DiffusionDrive [48]</td><td>98.2</td><td>96.2</td><td>94.7</td><td>100</td><td>82.2</td><td>88.1</td></tr><tr><td>WoTE [43]</td><td>98.5</td><td>96.8</td><td>94.9</td><td>99.9</td><td>81.9</td><td>88.3</td></tr><tr><td>DriveSuprim [90]</td><td>97.8</td><td>97.3</td><td>93.6</td><td>100</td><td>86.7</td><td>89.9</td></tr><tr><td>DriveVLA-W0 [42]</td><td>98.7</td><td>99.1</td><td>95.3</td><td>99.3</td><td>83.3</td><td>90.2</td></tr><tr><td>WAM-Flow [82]</td><td>99.2</td><td>98.3</td><td>97.0</td><td>99.7</td><td>82.3</td><td>90.3</td></tr><tr><td>ReCogDrive [44]</td><td>97.9</td><td>97.3</td><td>94.9</td><td>100</td><td>87.3</td><td>90.8</td></tr><tr><td>ReflectDrive-2 [72]</td><td>97.3</td><td>98.1</td><td>92.5</td><td>100</td><td>89.4</td><td>91.0</td></tr><tr><td>DiffusionDriveV2 [103]</td><td>98.3</td><td>97.9</td><td>94.8</td><td>99.9</td><td>87.5</td><td>91.2</td></tr><tr><td>iPad [24]</td><td>98.6</td><td>98.3</td><td>94.9</td><td>100</td><td>88.0</td><td>91.7</td></tr><tr><td>SparseDrive-V2 [68]</td><td>98.5</td><td>98.4</td><td>95.0</td><td>99.9</td><td>88.6</td><td>92.0</td></tr><tr><td>Discrete-WAM</td><td>98.8</td><td>98.4</td><td>95.3</td><td>100</td><td>88.7</td><td>92.2</td></tr></table>

Table 2 Comparison with state-of-the-art planning methods on NAVSIM-v1. All methods are evaluated using the oficial NAVSIM-v1 metrics: no collision (NC), drivable area compliance (DAC), time-to-collision (TTC), comfort (Comf.), ego progress (EP), and the final planning driving metric score (PDMS). The best result in each column is shown in bold, and the second-best result is underlined.
<table><tr><td>Metric</td><td>DriveDreamer [76] WoVoGen [56] Drive-WM [77] GenAD (OpenDV) [86]</td><td></td><td></td><td></td><td>Vista [21]</td><td>DrivingWorld [27]</td><td>Discrete-WAM</td></tr><tr><td>FID ↓</td><td>52.6</td><td>27.6</td><td>15.8</td><td>15.4</td><td>6.9</td><td>7.4</td><td>6.6</td></tr><tr><td>FVD ↓</td><td>452.0</td><td>417.7</td><td>122.7</td><td>184.0</td><td>89.4</td><td>90.9</td><td>80.0</td></tr><tr><td>Max Duration / Frames*</td><td>4s / 48</td><td>2.5s / 5</td><td>8s / 16</td><td>4s / 8</td><td>15s / 150</td><td>40s /  400</td><td>4s/8</td></tr></table>

Table 3 Comparison of generative driving world models. We report FID, FVD, and maximum generation duration/frames. The best results are highlighted in bold.

World generation results. Tab. 3 quantitatively compares Discrete-WAM with prior generative driving world models in terms of image and video generation quality. While Discrete-WAM is primarily designed for short-horizon unified generation to facilitate downstream planning, it achieves the best overall visual fidelity, obtaining an FID of 6.6 and an FVD of 80.0, outperforming existing approaches including Vista [21] and DrivingWorld [27]. Notably, while some prior methods support substantially longer rollouts, their generation quality degrades as the horizon increases. These results demonstrate that the proposed discrete world-action modeling framework can capture future driving dynamics and scene evolution more efectively while maintaining lower generation cost.

## 4.3 Analysis

Effect of unified pretraining. We compare three policy training strategies to isolate the efect of unified pretraining. “From scratch” trains the policy model directly on the downstream planning data without any unified pretraining. “FT” initializes the model from unified pretraining and then updates all trainable parameters during supervised finetuning. “LoRA-SFT” first performs vision-oriented world-policy pretraining, where future actions are provided as teacher-forced conditions and only vision prediction losses are applied, and then finetunes the policy with LoRA adapters. We study the benefit of unified pretraining with diferent

adaptation strategies under D<sub>t</sub>. As in Tab. 4, training from scratch already gives strong performance, indicating the suficient fitting capacity for Discrete-WAM. However, full finetuning does not further improve the result, likely because the orthogonal of planning objective that may overwrite useful pretrained representations. In contrast, LoRA-SFT achieves the best performance, improving EPDMS to 90.0, suggesting that lightweight adaptation better preserves pretrained world-policy knowledge while adapting to planning.

<table><tr><td>Ablations</td><td>NC↑</td><td>DAC↑</td><td>DDC↑</td><td>TLC↑</td><td>EP↑</td><td>TTC↑</td><td>LK↑</td><td>HC↑</td><td>EC↑</td><td>EPDMS*↑</td><td>EPDMS↑</td></tr><tr><td>From scratch</td><td>98.5</td><td>98.1</td><td>99.6</td><td>99.7</td><td>90.2</td><td>97.8</td><td>97.1</td><td>96.8</td><td>75.6</td><td>86.5</td><td>89.8</td></tr><tr><td>FT</td><td>98.6</td><td>98.0</td><td>99.6</td><td>99.7</td><td>90.3</td><td>97.8</td><td>97.1</td><td>96.4</td><td>75.4</td><td>86.4</td><td>89.7</td></tr><tr><td>LoRA-SFT</td><td>98.6</td><td>98.1</td><td>99.6</td><td>99.8</td><td>90.3</td><td>97.8</td><td>97.1</td><td>97.0</td><td>76.8</td><td>86.7</td><td>90.0</td></tr></table>

Table 4 Effect of policy training strategies on the NAVSIM-v2 benchmark.
<table><tr><td>Ablations</td><td>NC↑</td><td>DAC↑</td><td>DDC↑</td><td>TLC↑</td><td>EP↑</td><td>TTC↑</td><td>LK↑</td><td>HC↑</td><td>EC↑</td><td>EPDMS*↑</td><td>EPDMS↑</td></tr><tr><td>SFT</td><td>98.2</td><td>99.6</td><td>99.5</td><td>98.6</td><td>90.2</td><td>97.6</td><td>97.7</td><td>95.2</td><td>73.6</td><td>86.5</td><td>89.1</td></tr><tr><td>SFT-Dt</td><td>98.6</td><td>98.1</td><td>99.6</td><td>99.8</td><td>90.3</td><td>97.8</td><td>97.1</td><td>97.0</td><td>76.8</td><td>86.7</td><td>90.0</td></tr><tr><td>RL</td><td>98.5</td><td>98.2</td><td>99.7</td><td>99.8</td><td>90.5</td><td>97.9</td><td>97.2</td><td>98.3</td><td>78.1</td><td>87.0</td><td>90.4</td></tr></table>

Table 5 Effect of post-training on the NAVSIM-v2 benchmark.
<table><tr><td>Ablations</td><td>NC↑</td><td>DAC↑</td><td>DDC↑</td><td>TLC↑</td><td>EP↑</td><td>TTC↑</td><td>LK↑</td><td>HC↑</td><td>EC↑</td><td>EPDMS*↑</td><td>EPDMS↑</td></tr><tr><td>Base</td><td>98.2</td><td>92.9</td><td>99.3</td><td>99.8</td><td>86.7</td><td>97.6</td><td>97.7</td><td>98.3</td><td>83.3</td><td>82.9</td><td>84.7</td></tr><tr><td>Base-Dt</td><td>98.8</td><td>94.2</td><td>99.5</td><td>99.8</td><td>87.3</td><td>98.2</td><td>97.4</td><td>98.5</td><td>87.7</td><td>84.0</td><td>87.2</td></tr></table>

Table 6 Effect of decision modeling on the NAVSIM-v2 benchmark.

Effect of post training. As in Tab. 5, compared with based supervised finetuning, leveraging the ground-truth decision condition increases EPDMS from 89.1 to 90.0, confirming that decision-level guidance provides an efective behavioral prior. Nevertheless, this setting still lacks exploration over diferent decisions and the corresponding trajectory refinements. Our RL post-training further improves EPDMS to 90.4 and EPDMS to 87.0, with gains in both comfort and safety. This suggests that the proposed post-training stage jointly benefits high-level decision optimization and low-level token editing, enabling the planner to explore better decision-trajectory combinations rather than only refining trajectories under a fixed decision.

Effect of decision modeling. Tab. 6 reflects the capabilities enabled by decision learning during pretraining. Introducing D improves EPDMS from 84.7 to 87.2 with consistent gains in sub-metrics. This indicates a strong behavioral prior ofered by decision at the pretraining stage that better aligns high-level intent with low-level trajectory generation. The result suggests that the unified world-policy pretraining learns not only scene prediction, but also decision-conditioned planning capability before downstream SFT. Interestingly, performance peaks at k = 16 and gradually degrades as the anchor set expands. As in Fig. 4-a, we attribute this to a trade-of between diversity and optimization dificulty: larger top-d values improve decision coverage but introduce more low-quality anchors, increasing reward variance and weakening the GRPO advantage signal. Consequently, a moderate anchor set provides the most efective policy refinement.

Effect of scheduling strategies. We evaluate four scheduling strategies for iterative policy-token decoding. full\_replace is the baseline scheduler, where all policy tokens are predicted and replaced at every round. replace\_confidence accepts only tokens whose prediction confidence exceeds a predefined threshold, while keeping the remaining tokens unchanged for future refinement. replace\_js\_entropy further considers cross-round uncertainty and distributional change, updating tokens with high entropy, large Jensen–Shannon divergence, or unstable argmax predictions. Finally, replace\_js\_freeze adds a hard-freeze mechanism: tokens that remain stable for consecutive rounds are frozen and no longer updated. For each scheduler, we evaluate diferent scheduling rounds and report the L2 change between the lowest and highest available rounds in Table 8. We report the L2 change between the lowest and highest available rounds for each scheduling strategy, defined as $\Delta \mathrm { L 2 } = \mathrm { L 2 } _ { \mathrm { h i g h \ r o u n d } } - \mathrm { L 2 } _ { \mathrm { l o w \ r o u n d } }$ . The results show that increasing the number of rounds does not always improve performance. For full\_replace, additional rounds consistently increase L2 error, suggesting that repeatedly overwriting all action tokens can perturb already reasonable predictions. This efect is particularly harmful for acceleration-token decoding, where small changes in early acceleration tokens can be amplified through temporal integration into long-horizon position errors. In contrast, the selective schedulers improve or preserve L2 performance with more rounds. By updating only confident, uncertain, distributionally unstable, or non-frozen tokens, these schedulers use additional computation to refine unresolved parts of the action sequence while retaining stable predictions.

![](images/71b5533fb2ac8bdf589a215ae939fed88f926340074ef4e5891cd0ad5203606d.jpg)  
b)

![](images/03dfe01a0fa920538e9658ee8266ecc349e429e2fbf3804b13275f964315f3f0.jpg)

![](images/601a09f7304452eefacb2d1f534c9e71fb5ae0d2eca63e21c3b0fd3df9bff9be.jpg)  
Figure 4 Ablation visualization results of Discrete-WAM. a) Efect of performance trade-of with decision numbers. The orange curve denotes the EPDMS with varied decision numbers. The red curve terms for average L2 planning errors under respective number of decisions. b) Compute performance trade-of of re-edit schedules. The horizontal axis denotes $x = 1 / R _ { \mathrm { { i } } }$ , and the vertical axis denotes $y = 1 0 0 0 ( E _ { \mathrm { F R } , 1 } - E _ { s , R } )$ . c) Inference latency comparison between discrete difusion and autoregressive policy decoding. We compare replace\_confidence discrete difusion decoding with an autoregressive action decoder.

We further analyze the trade-of between scheduling computation and trajectory performance. Since we do not strictly measure wall-clock latency or exact FLOPs, we use the scheduling round number R as a coarse proxy for compute cost and define the inverse-compute coordinate as $x = 1 / R$ . For trajectory performance, we compute the mean L2 error across the four evaluated horizons as $\begin{array} { r } { E _ { s , R } = \frac { 1 } { 4 } \sum _ { t \in \{ 1 , 2 , 3 , 4 \} } \mathrm { L } 2 _ { s , R } @ t } \end{array}$ , where s denotes the scheduling strategy and R denotes the scheduling round. For clearer visualization, we use a baseline-relative coordinate with full\_replace at R = 1 as the baseline: $y _ { s , R } = 1 0 0 0 ( E _ { \mathrm { F R } , 1 } - E _ { s , R } )$ . A positive y indicates lower mean L2 error than the baseline, while a negative value indicates worse performance. The resulting compute-performance coordinates are reported in Table 7 and visualized in Fig. 4-b.

Scheduling dynamics of confidence replacement. We further analyze the detailed editing dynamics of the replace\_confidence scheduler using a representative left-turn scenario. As shown in Fig. 5, the token acceptance ratio gradually decreases as the number of scheduling rounds increases, indicating that more action tokens become stable and no longer require further editing. The accepted and rejected tokens also exhibit clearly separated confidence distributions: accepted tokens consistently have higher confidence, while rejected tokens have lower confidence and are preserved for later refinement. This shows that confidence provides an efective signal for distinguishing tokens that are ready to be updated from tokens that remain uncertain. Meanwhile, the average normalized entropy decreases across scheduling rounds, suggesting that the model prediction becomes progressively sharper during iterative editing.

The token-level visualization further explains this behavior. Tokens with high initial confidence tend to have high final retention, which means that once these positions are confidently predicted, they are less likely to be overwritten in later rounds. In contrast, tokens with low initial confidence usually have higher entropy, indicating ambiguous action distributions. As scheduling proceeds, their confidence gradually increases and entropy decreases, showing a progressive uncertainty reduction process. Across diferent rounds, we also consistently observe an inverse relationship between confidence and entropy: high-confidence tokens usually have low entropy, while high-entropy tokens are more likely to be rejected and refined in subsequent rounds. These observations explain why confidence-based selective replacement can improve multi-round policy editing: additional rounds are mainly allocated to uncertain tokens, while stable tokens are preserved.

Inference latency analysis. We further compare the online inference latency of the discrete difusion policy decoder and an autoregressive action decoder. For the discrete difusion policy, we use the replace\_- confidence scheduling strategy and evaluate diferent editing rounds, including 1, 2, 3, 5, 6, 10, 15, and 30 rounds. For the autoregressive baseline, we implement an AR policy decoder that generates the future action sequence sequentially. To make the comparison focus on the intrinsic decoding pattern, we disable engineering acceleration tricks for both methods: the discrete difusion decoder is evaluated without additional decoding optimizations, and the AR decoder is evaluated without KV-cache acceleration. All latency measurements are conducted for online inference on NVIDIA H20 GPUs.

![](images/455f941d05ae5ceb3c588480a0c5544a92c08419338961b6171bdc0243c44d36.jpg)  
Figure 5 Scheduling dynamics of confidence-based token replacement. We visualize replace\_confidence with four editing rounds in a representative left-turn scenario to inspect the detailed multi-round scheduling behavior. The first round is treated as the initialization round, where all tokens are accepted because no previous prediction is available. The left column reports round-level statistics, including the accept/keep ratio, accepted/rejected token confidence, and mean normalized entropy. The right panel shows token-level details across rounds, where each row corresponds to one round and the horizontal axis denotes action-token time steps, with only even steps 0, 2, 4, . . . , 38 shown for readability. Red bars indicate raw entropy, purple/orange bars indicate accepted/rejected tokens, the red dashed line marks the confidence threshold, and the blue curve shows the cumulative accepted-update ratio for each token. The visualization shows that high-confidence tokens are more likely to be accepted and retained, while high-entropy tokens are refined over multiple rounds, leading to progressive entropy reduction.

As shown in Fig. 4-c, discrete difusion decoding achieves substantially lower latency than the AR decoder under a moderate number of editing rounds. This is because action tokens within each discrete difusion editing round are decoded in parallel, while the AR decoder must generate the action sequence sequentially. Although the latency of discrete difusion increases with the number of editing rounds, it remains more eficient than AR decoding for common low- and medium-round settings. This result highlights the computationa advantage of parallel policy-token editing.

We emphasize that this comparison reflects the theoretical decoding-complexity diference between parallel editing and sequential generation under a controlled non-accelerated setting. In real deployment, AR decoding can benefit from KV-cache acceleration, whereas discrete difusion does not use the same acceleration mechanism. Therefore, the measured latency should not be interpreted as a complete deployment-level speed comparison, but rather as an analysis of the intrinsic eficiency of the two decoding paradigms.

## 4.4 Qualitative Results

Planning results. Fig 6 presents qualitative planning results of Discrete-WAM. The predicted trajectories closely follow the expert demonstrations while remaining geometrically consistent with the underlying road topology. In straight-road cruising scenarios, the planner maintains stable lane centering and accurately captures the intended longitudinal progression. In turning and curved-road scenarios, Discrete-WAM generates smooth trajectories that align well with lane boundaries and preserve appropriate curvature throughout the maneuver. Notably, in more complex urban scenes such as lane-changing or nudging, Discrete-WAM produces feasible future plans without explicit rule-based constraints.

<table><tr><td>Schedule</td><td>Round</td><td> ${ \boldsymbol { x } } = 1 / R$ </td><td> $\mathcal { E } _ { s , R }$ </td><td>y</td></tr><tr><td>Full replace</td><td>R1</td><td>1.000</td><td>0.67325</td><td>0.000</td></tr><tr><td>Full replace</td><td>R3</td><td>0.333</td><td>0.67853</td><td>-5.275</td></tr><tr><td>Confidence replace</td><td>R1</td><td>1.000</td><td>0.66950</td><td>3.747</td></tr><tr><td>Confidence replace</td><td>R2</td><td>0.500</td><td>0.66643</td><td>6.825</td></tr><tr><td>Confidence replace</td><td>R3</td><td>0.333</td><td>0.66488</td><td>8.375</td></tr><tr><td>JS-entropy replace</td><td>R2</td><td>0.500</td><td>0.66710</td><td>6.150</td></tr><tr><td>JS-entropy replace</td><td>R3</td><td>0.333</td><td>0.66690</td><td>6.350</td></tr><tr><td>JS-freeze replace</td><td>R4</td><td>0.250</td><td>0.67695</td><td>-3.700</td></tr><tr><td>JS-freeze replace</td><td>R6</td><td>0.167</td><td>0.66943</td><td>3.825</td></tr></table>

Table 7 Compute performance of different re-edit schedules. The compute coordinate is defined as $x = 1 / R _ { \mathrm { i } }$ , where R is the scheduling round. The performance coordinate is the baseline-relative mean-L2 improvement, $y = 1 0 0 0 ( E _ { \mathrm { F R } , 1 } - E _ { s , R } )$ , where E<sub>FR,1</sub> denotes the mean L2 error of Full replace at R = 1, and $E _ { s , R }$ denotes the mean L2 error of schedule s at round R.

<table><tr><td>Schedule</td><td>Rounds</td><td>∆L2@1s</td><td>∆L2@2s</td><td>∆L2@3s</td><td>∆L2@4s</td></tr><tr><td>Full replace</td><td>R3-R1</td><td>+0.0019</td><td>+0.0040</td><td>+0.0068</td><td>+0.0084</td></tr><tr><td>Confidence replace</td><td>R3-R1</td><td>-0.0001</td><td>-0.0007</td><td>-0.0014</td><td>-0.0040</td></tr><tr><td>JS-entropy replace</td><td>R3-R2</td><td>-0.0001</td><td>-0.0003</td><td>-0.0003</td><td>-0.0001</td></tr><tr><td>JS-freeze replace</td><td>R6-R4</td><td>-0.0022</td><td>-0.0055</td><td>-0.0073</td><td>-0.0151</td></tr></table>

Table 8 Effect of re-edit scheduling rounds on L2 trajectory error. Negative values indicate that additional edit rounds reduce L2 error.
<table><tr><td>Ablations</td><td>ax Err. (m/s²).↓</td><td> $a _ { y }$  Err. (m/s²).↓</td><td>Traj. x Err. (m)↓</td><td>Traj. y Err. (m).↓</td><td>Traj. Err. (m).↓</td></tr><tr><td>Upper-only</td><td>0.477</td><td>0.918</td><td>0.274</td><td>0.652</td><td>0.780</td></tr><tr><td>Upper-masked</td><td>0.476</td><td>0.916</td><td>0.268</td><td>0.647</td><td>0.772</td></tr><tr><td>Full image</td><td>0.475</td><td>0.914</td><td>0.267</td><td>0.646</td><td>0.770</td></tr></table>

Table 9 Effect of vertical image-region ablations on policy prediction. We compare three front-view image settings: Full image keeps the original front-view image unchanged, Upper-only keeps only the upper one-third region, and Upper-masked masks out the upper one-third region. Acceleration errors are reported in $\mathrm { m } / \mathrm { s } ^ { 2 }$ and trajectory position errors are reported in meters. Lower values indicate better performance.

World generation results. Fig 7 visualizes the future world generation results of Discrete-WAM across diverse driving scenarios. Given historical observations and the current frame, Discrete-WAM generates temporally coherent future visual states over multiple prediction steps. The generated sequences preserve scene layout, road geometry, surrounding vehicles, and ego-motion consistency, while capturing realistic forward evolution under diferent urban driving conditions. These results demonstrate that the proposed discrete vision-action token editing framework can efectively model action-conditioned scene dynamics for world generation.

Attention map analysis. We analyze the visual grounding behavior of the policy decoder through attention map visualization. The model contains 18 Transformer layers, 16 attention heads, and 8 key-value heads. All attention maps are computed from the first editing round under the replace\_confidence inference setting. Since each policy prediction contains 40 future action tokens, we average the attention maps over policy queries, attention heads, and layers unless otherwise specified.

Fig. 8 shows the averaged attention maps for the front-view and side-view cameras. The policy decoder attends to driving-relevant semantic regions, including roads, lane markings, surrounding vehicles, trafic signs, and other dynamic or structural cues. This indicates that action-token prediction is grounded in visual scene semantics rather than only low-level image appearance. Meanwhile, we observe consistent high attention in sky regions, especially in the front-view image.

To inspect this behavior across the network depth, we visualize layer-wise attention maps by selecting layers 0, 6, 12, and 17, while averaging over heads and policy queries. As shown in Fig. 9, diferent layers emphasize diferent levels of spatial and semantic abstraction. Early layers show broader attention over the scene, while deeper layers produce more structured responses on lanes, road boundaries, vehicles, and global scene layout. The sky activation remains visible across multiple layers, suggesting that it is a stable attention pattern rather than an artifact of a single layer or head.

We hypothesize that sky patches may act as implicit global anchors in the absence of explicit CLS or register tokens. Sky regions are spatially stable, visually smooth, and low in local texture, making them suitable locations for absorbing attention mass or organizing global scene context. They may also encode weak global cues such as illumination, weather, horizon position, or scene openness. Thus, sky attention may reflect a mixture of attention-sink behavior and implicit-register behavior, rather than direct reliance on sky pixels as causal driving evidence.

![](images/6f12ee25ec47063bf099f05f8fea3630f101d3a29d1320deb64e8c7e6e302a61.jpg)

![](images/8aab08865bdab2055a5080558cf1efc22ded3a9c3fe96e07cc6d84ad70b8ddb4.jpg)  
Figure 6 Planning Performance of Discrete-WAM. Discrete-WAM demonstrate strong planning performance on various driving scenarios, including nudging, lane changing, cruising, or pull-away.

![](images/e463e3d2716f30aacb6064606707c89be4618af7da66673686e9d55fa08afe4c.jpg)  
Figure 7 World generation result of Discrete-WAM. Discrete-WAM delivers coherent generation under a variety of driving scenarios.

To examine this hypothesis, we conduct a sky-region ablation on the front-view image. Since sky regions typically occupy the upper part of the image, we approximate the sky region with the top one-third of the front-view image. We compare three settings: the original image, a top-masked image where the upper one-third region is masked out, and a sky-only image where only the upper one-third region is preserved. This is an approximate intervention because the sky is not guaranteed to always lie exactly in the top one-third region, but it provides a controlled way to study the observed attention pattern.

Fig. 10 shows the ablation results. When the upper region is masked, attention is redistributed toward local driving semantics such as road boundaries, lane markings, vehicles, and trafic signs. This confirms that the sky region absorbs a non-trivial amount of attention in the original input. When only the upper region is preserved, the model can still produce plausible trajectories, but the trajectory quality degrades compared with the full-image baseline. This suggests that sky-region tokens provide useful global context or implicit anchoring, while lower image regions provide the detailed local semantics required for accurate policy prediction. The quantitative results in Table 9 show the same trend: masking the upper region slightly degrades trajectory quality, while using only the upper region gives the worst performance. This indicates that sky-region tokens may provide useful global context, but local driving semantics from the lower image region remain essential for accurate policy prediction. Overall, the attention visualizations show that the policy decoder uses both local driving semantics and global contextual regions. The sky activation should be interpreted as stable attention-sink or implicit-register behavior, not as direct evidence that sky pixels are strong causal cues for driving. Additional attention map examples are provided in Appendix 7.4.

![](images/31089b189a5b64070073aabb488158f28b704d582bec7fbc1242ec37979e4f19.jpg)

Figure 8 Averaged policy attention maps. The three panels show the left-view, front-view, and right-view cameras, respectively. Attention maps are averaged over Transformer layers, attention heads, and policy action queries from the first editing round. The policy decoder attends to driving-relevant regions such as lanes, vehicles, road structures, and trafic signs, while also showing stable activation in upper sky regions.  
![](images/ae269b903e231194c83c92bac8b2c406144033bf8e62fe5a28c303983b178027.jpg)

Figure 9 Layer-wise policy attention maps. All panels show the front-view camera. We visualize layers 0, 6, 12, and 17 by averaging over attention heads and policy queries. Diferent layers emphasize diferent spatial and semantic structures, while the upper-region activation remains visible across multiple layers, suggesting a stable attention pattern rather than an isolated layer-specific artifact  
![](images/b26177482200c74f3c431e3d59a56c1181571b757949e161442255c7b660eb34.jpg)  
Figure 10 Upper-region ablation for policy attention. We compare the original front-view image, an upper-masked image where the top one-third region is masked out, and an upper-only image where only the top one-third region is preserved. Masking the upper region redistributes attention toward local driving semantics, whereas the upper-only setting can still produce plausible but less accurate trajectories, suggesting that upper-region tokens may provide global contextual cues while lower regions remain essential for detailed policy prediction

Counterfactual results. To manifest the causal understandability, we evaluate the surprise value of Discrete-WAM under both factual rollouts and a spectrum of counterfactual world-model generations. Specifically, the world model is injected with both ground-truth action $\mathbf { A } _ { t : t + H }$ condition or counterfactual ones given a sweep of lateral perturbed actions $\tilde { \mathbf { A } } _ { t : t + H }$ . Surprise is quantified by $\begin{array} { r } { \mathbf { S } = \mathrm { K L } \big ( p _ { \theta } \big ( \cdot | \mathbf { A } _ { t : t + H } , \mathbf { V } _ { t } \big ) \big | \big | p _ { \theta } \big ( \cdot | \tilde { \mathbf { A } } _ { t : t + H } , \mathbf { V } _ { t } \big ) \big ) } \end{array}$ [18]. We also report the average pixel L1 distance $\Delta _ { \mathrm { i m g } }$ for reference. A strong negative correlation is observed between surprise and PDMS. As in Fig.11, the surge of S when PDMS drop to zero (collide with static object, drive of the road boundary) indicating that Discrete-WAM captures action-conditioned scene dynamics and safety-critical outcomes. As driving quality deteriorates due to drivable-area violations, or unsafe interactions, the resulting future observations become increasingly dificult for the world model to predict, leading to higher surprise values. While the gradual increase for $\Delta _ { \mathrm { i m g } }$ further indicate the casualty learned under prediction error. Conversely, when no hard safety penalties are incurred (PDMS = 1), surprise remains consistently low across both factual and counterfactual rollouts. This suggests that surprise provides a meaningful proxy for model uncertainty and can potentially be leveraged for risk-aware planning and safety evaluation.

![](images/39378b386be3afef908752ac7e3740f27469bbb6022341b863dfeafde27a42b6.jpg)  
Figure 11 Counterfactual result with surprise metric. We compare surprise value S by both factual and counterfactual world-model generations. A clear correlation is observed between surprise and PDMS, suggesting that Discrete-WAM captures safety-critical scene dynamics such as collisions and drivable-area violations

## 5 Conclusion and Future Directions

In this work, we present Discrete-WAM, a unified discrete vision-action world-policy framework for autonomous driving. Rather than treating world prediction and policy generation as separate modules, Discrete-WAM formulates visual observations, future states, driving decisions, and ego actions within a shared discrete token space. This design enables representation alignment across modalities through shared sequence modeling, shared Transformer computation, and unified token-level objectives. Built on this aligned discrete space, Discrete-WAM further integrates world modeling, world-policy modeling, and policy modeling through multi-task and multi-stage training, allowing future prediction to be optimized toward policy-relevant action generation rather than isolated visual reconstruction. A key component of Discrete-WAM is its structured policy modeling design. By introducing a high-level decision token as a latent planning skeleton, the model separates multi-modal decision selection from low-level trajectory realization. This hierarchical formulation reduces residual dependence among dense future action tokens and makes parallel discrete difusion editing more suitable for planning. Together with confidence-based re-edit scheduling, Discrete-WAM provides an eficient and structured mechanism for generating temporally consistent future actions. Experiments on autonomous-driving benchmarks demonstrate strong planning performance, while additional analyses on world-model surprise, attention grounding, scheduling dynamics, and inference latency show that the learned world-policy representation supports counterfactual evaluation and policy-oriented future reasoning.

More broadly, we view Discrete-WAM as an initial validation of a physical AI design paradigm based on discrete representation alignment, unified world-policy training, and hierarchical policy construction with parallel token editing. Future work will incorporate language-based reasoning, explore adaptive serial-parallel generation schedules, and leverage intrinsic value functions learned from world models for self-supervised reinforcement learning. We will further extend this paradigm to broader autonomous-driving and robotic datasets, including larger-scale in-house driving data, multi-modal reasoning, and interactive field tests. We also plan to release additional evaluation results as these deployments mature, enabling a more comprehensive study of how discrete world-policy alignment can support scalable embodied decision-making.

## References

[1] Jacob Austin, Daniel D Johnson, Jonathan Ho, Daniel Tarlow, and Rianne Van Den Berg. Structured denoising difusion models in discrete state-spaces. Advances in neural information processing systems, 34:17981–17993, 2021.

[2] Alisson Azzolini, Junjie Bai, Hannah Brandon, Jiaxin Cao, Prithvijit Chattopadhyay, Huayu Chen, Jinju Chu, Yin Cui, Jenna Diamond, Yifan Ding, et al. Cosmos-reason1: From physical common sense to embodied reasoning. arXiv preprint arXiv:2503.15558, 2025.

[3] Florent Bartoccioni, Elias Ramzi, Victor Besnier, Shashanka Venkataramanan, Tuan-Hung Vu, Yihong Xu, Loick Chambon, Spyros Gidaris, Serkan Odabas, David Hurych, et al. Vavim and vavam: Autonomous driving through video generative modeling. arXiv preprint arXiv:2502.15672, 2025.

[4] Heli Ben-Hamu, Itai Gat, Daniel Severo, Niklas Nolte, and Brian Karrer. Accelerated sampling from masked difusion models via entropy bounded unmasking. In Advances in Neural Information Processing Systems, 2025.

[5] Hongzhe Bi, Hengkai Tan, Shenghao Xie, Zeyuan Wang, Shuhe Huang, Haitian Liu, Ruowen Zhao, Yao Feng, Chendong Xiang, Yinze Rong, et al. Motus: A unified latent action world model. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 35101–35113, 2026.

[6] Holger Caesar, Juraj Kabzan, Kok Seang Tan, Whye Kit Fong, Eric Wolf, Alex Lang, Luke Fletcher, Oscar Beijbom, and Sammy Omari. nuplan: A closed-loop ml-based planning benchmark for autonomous vehicles. arXiv preprint arXiv:2106.11810, 2021.

[7] Changxiao Cai and Gen Li. Confidence-based decoding is provably eficient for difusion language models. arXiv preprint arXiv:2603.22248, 2026.

[8] Wei Cao, Marcel Hallgarten, Tianyu Li, Daniel Dauner, Xunjiang Gu, Caojun Wang, Yakov Miron, Marco Aiello, Hongyang Li, Igor Gilitschenski, et al. Pseudo-simulation for autonomous driving. arXiv preprint arXiv:2506.04218, 2025.

[9] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, et al. Worldvla: Towards autoregressive action world model. arXiv preprint arXiv:2506.21539, 2025.

[10] Hao Chen, Jiaming Liu, Zhonghao Yan, Nuowei Han, Renrui Zhang, Chenyang Gu, Jialin Gao, Ziyu Guo, Siyuan Qian, Yinxi Wang, et al. Last-r1: Reinforcing action via adaptive physical latent reasoning for vla models. arXiv preprint arXiv:2604.28192, 2026.

[11] Li Chen, Penghao Wu, Kashyap Chitta, Bernhard Jaeger, Andreas Geiger, and Hongyang Li. End-to-end autonomous driving: Challenges and frontiers. IEEE Transactions on Pattern Analysis and Machine Intelligence, 46(12):10164–10183, 2024.

[12] Long Chen, Yuchen Li, Chao Huang, Bai Li, Yang Xing, Daxin Tian, Li Li, Zhongxu Hu, Xiaoxiang Na, Zixuan Li, et al. Milestones in autonomous driving and intelligent vehicles: Survey of surveys. IEEE Transactions on Intelligent Vehicles, 8(2):1046–1056, 2022.

[13] Shaoyu Chen, Bo Jiang, Hao Gao, Bencheng Liao, Qing Xu, Qian Zhang, Chang Huang, Wenyu Liu, and Xinggang Wang. Vadv2: End-to-end vectorized autonomous driving via probabilistic planning. arXiv preprint arXiv:2402.13243, 2024.

[14] Sitan Chen, Kevin Cong, and Jerry Li. Optimal inference schedules for masked difusion models. arXiv preprint arXiv:2511.04647, 2025.

[15] Zhili Chen, Maosheng Ye, Shuangjie Xu, Tongyi Cao, and Qifeng Chen. Ppad: Iterative interactions of prediction and planning for end-to-end autonomous driving. In European Conference on Computer Vision, pages 239–256. Springer, 2024.

[16] Kashyap Chitta, Aditya Prakash, Bernhard Jaeger, Zehao Yu, Katrin Renz, and Andreas Geiger. Transfuser: Imitation with transformer-based sensor fusion for autonomous driving. IEEE transactions on pattern analysis and machine intelligence, 45(11):12878–12895, 2022.

[17] Daniel Dauner, Marcel Hallgarten, Tianyu Li, Xinshuo Weng, Zhiyu Huang, Zetong Yang, Hongyang Li, Igor Gilitschenski, Boris Ivanovic, Marco Pavone, et al. Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking. Advances in Neural Information Processing Systems, 37:28706–28719, 2024.

[18] Carolyn C. Duncan-Johnson and Emanuel Donchin. On quantifying surprise: The variation of event-related potentials with subjective probability. Psychophysiology, 14(5):456–467, 1977.

[19] Guhao Feng, Yihan Geng, Jian Guan, Wei Wu, Liwei Wang, and Di He. Theoretical benefit and limitation of difusion language model. In Advances in Neural Information Processing Systems, 2025.

[20] Hao Gao, Shaoyu Chen, Bo Jiang, Bencheng Liao, Yiang Shi, Xiaoyang Guo, Yuechuan Pu, Xiangyu Li, Wenyu Liu, Qian Zhang, et al. Rad: Training an end-to-end driving policy via large-scale 3dgs-based reinforcement learning. Advances in Neural Information Processing Systems, 38:32551–32576, 2026.

[21] Shenyuan Gao, Jiazhi Yang, Li Chen, Kashyap Chitta, Yihang Qiu, Andreas Geiger, Jun Zhang, and Hongyang Li. Vista: A generalizable driving world model with high fidelity and versatile controllability. Advances in Neural Information Processing Systems, 37:91560–91596, 2024.

[22] Shenyuan Gao, William Liang, Kaiyuan Zheng, Ayaan Malik, Seonghyeon Ye, Sihyun Yu, Wei-Cheng Tseng, Yuzhu Dong, Kaichun Mo, Chen-Hsuan Lin, et al. Dreamdojo: A generalist robot world model from large-scale human videos. arXiv preprint arXiv:2602.06949, 2026.

[23] Yanchen Guan, Haicheng Liao, Zhenning Li, Jia Hu, Runze Yuan, Guohui Zhang, and Chengzhong Xu. World models for autonomous driving: An initial survey. IEEE Transactions on Intelligent Vehicles, 2024.

[24] Ke Guo, Haochen Liu, Xiaojun Wu, Jia Pan, and Chen Lv. ipad: Iterative proposal-centric end-to-end autonomous driving. arXiv preprint arXiv:2505.15111, 2025.

[25] Stefen Hagedorn, Marcel Hallgarten, Martin Stoll, and Alexandru Paul Condurache. The integration of prediction and planning in deep learning automated driving systems: A review. IEEE Transactions on Intelligent Vehicles, 10(5):3626–3643, 2024.

[26] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. Gaia-1: A generative world model for autonomous driving. arXiv preprint arXiv:2309.17080, 2023.

[27] Xiaotao Hu, Wei Yin, Mingkai Jia, Junyuan Deng, Xiaoyang Guo, Qian Zhang, Xiaoxiao Long, and Ping Tan. Drivingworld: Constructing world model for autonomous driving via video gpt. arXiv preprint arXiv:2412.19505, 2024.

[28] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, et al. Planning-oriented autonomous driving. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 17853–17862, 2023.

[29] Wenhui Huang, Songyan Zhang, Qihang Huang, Zhidong Wang, Zhiqi Mao, Collister Chua, Zhan Chen, Long Chen, and Chen Lv. Automot: A unified vision-language-action model with asynchronous mixture-of-transformers for end-to-end autonomous driving. arXiv preprint arXiv:2603.14851, 2026.

[30] Yuzhou Huang, Benjin Zhu, Hengtong Lu, Victor Shea-Jay Huang, Haiming Zhang, Wei Chen, Jifeng Dai, Yan Xie, and Hongsheng Li. Mindvla-u1: Vla beats va with unified streaming architecture for autonomous driving. arXiv preprint arXiv:2605.12624, 2026.

[31] Zhiyu Huang, Haochen Liu, and Chen Lv. Gameformer: Game-theoretic modeling and learning of transformerbased interactive prediction and planning for autonomous driving. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 3903–3913, 2023.

[32] Anqing Jiang, Yu Gao, Yiru Wang, Zhigang Sun, Shuo Wang, Yuwen Heng, Hao Sun, Shichen Tang, Lijuan Zhu, Jinhao Chai, et al. Irl-vla: Training an vision-language-action policy via reward world model. arXiv preprint arXiv:2508.06571, 2025.

[33] Sicong Jiang, Zilin Huang, Kangan Qian, Ziang Luo, Tianze Zhu, Yang Zhong, Yihong Tang, Menglin Kong, Yunlong Wang, Siwen Jiao, et al. A survey on vision-language-action models for autonomous driving. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 4524–4536, 2025.

[34] Peter Karkus, Maximilian Igl, Yuxiao Chen, Kashyap Chitta, Jef Packer, Bertrand Douillard, Ran Tian, Alexander Naumann, Guillermo Garcia-Cobo, Shuhan Tan, et al. Beyond behavior cloning in autonomous driving: a survey of closed-loop training techniques. Authorea Preprints, 2025.

[35] Jaeyeon Kim, Kulin Shah, Vasilis Kontonis, Sham M. Kakade, and Sitan Chen. Train for the worst, plan for the best: Understanding token ordering in masked difusions. In Proceedings of the 42nd International Conference

on Machine Learning, volume 267 of Proceedings of Machine Learning Research, pages 30749–30768. PMLR, 2025.

[36] Moo Jin Kim, Yihuai Gao, Tsung-Yi Lin, Yen-Chen Lin, Yunhao Ge, Grace Lam, Percy Liang, Shuran Song, Ming-Yu Liu, Chelsea Finn, et al. Cosmos policy: Fine-tuning video models for visuomotor control and planning. arXiv preprint arXiv:2601.16163, 2026.

[37] Lingdong Kong, Wesley Yang, Jianbiao Mei, Youquan Liu, Ao Liang, Dekai Zhu, Dongyue Lu, Wei Yin, Xiaotao Hu, Mingkai Jia, et al. 3d and 4d world modeling: A survey. arXiv preprint arXiv:2509.07996, 2025.

[38] Hugo Lavenant and Giacomo Zanella. Error bounds and optimal schedules for masked difusions with factorized approximations. arXiv preprint arXiv:2510.25544, 2025.

[39] Yann LeCun et al. A path towards autonomous machine intelligence version 0.9. 2, 2022-06-27. Open Review, 62(1):1–62, 2022.

[40] Gen Li and Changxiao Cai. A convergence theory for difusion language models: An information-theoretic perspective. arXiv preprint arXiv:2505.21400, 2025.

[41] Pengxiang Li, Yinan Zheng, Yue Wang, Huimin Wang, Hang Zhao, Jingjing Liu, Xianyuan Zhan, Kun Zhan, and Xianpeng Lang. Discrete difusion for reflective vision-language-action models in autonomous driving. arXiv preprint arXiv:2509.20109, 2025.

[42] Yingyan Li, Shuyao Shang, Weisong Liu, Bing Zhan, Haochen Wang, Yuqi Wang, Yuntao Chen, Xiaoman Wang, Yasong An, Chufeng Tang, et al. Drivevla-w0: World models amplify data scaling law in autonomous driving. arXiv preprint arXiv:2510.12796, 2025.

[43] Yingyan Li, Yuqi Wang, Yang Liu, Jiawei He, Lue Fan, and Zhaoxiang Zhang. End-to-end driving with online trajectory evaluation via bev world model. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 27137–27146, 2025.

[44] Yongkang Li, Kaixin Xiong, Xiangyu Guo, Fang Li, Sixu Yan, Gangwei Xu, Lijun Zhou, Long Chen, Haiyang Sun, Bing Wang, et al. Recogdrive: A reinforced cognitive framework for end-to-end autonomous driving. arXiv preprint arXiv:2506.08052, 2025.

[45] Yongkang Li, Lijun Zhou, Sixu Yan, Bencheng Liao, Tianyi Yan, Kaixin Xiong, Long Chen, Hongwei Xie, Bing Wang, Guang Chen, et al. Unidrivevla: Unifying understanding, perception, and action planning for autonomous driving. arXiv preprint arXiv:2604.02190, 2026.

[46] Zhenxin Li, Kailin Li, Shihao Wang, Shiyi Lan, Zhiding Yu, Yishen Ji, Zhiqi Li, Ziyue Zhu, Jan Kautz, Zuxuan Wu, et al. Hydra-mdp: End-to-end multimodal planning with multi-target hydra-distillation. arXiv preprint arXiv:2406.06978, 2024.

[47] Zhenxin Li, Shihao Wang, Shiyi Lan, Zhiding Yu, Zuxuan Wu, and Jose M Alvarez. Hydra-next: Robust closed-loop driving with open-loop training. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 27305–27314, 2025.

[48] Bencheng Liao, Shaoyu Chen, Haoran Yin, Bo Jiang, Cheng Wang, Sixu Yan, Xinbang Zhang, Xiangyu Li, Ying Zhang, Qian Zhang, et al. Difusiondrive: Truncated difusion model for end-to-end autonomous driving. In Proceedings of the Computer Vision and Pattern Recognition Conference, pages 12037–12047, 2025.

[49] Haohong Lin, Yunzhi Zhang, Wenhao Ding, Jiajun Wu, and Ding Zhao. Model-based policy adaptation for closed-loop end-to-end autonomous driving. In Workshop on Foundation Models Meet Embodied Agents at CVPR 2025, 2025.

[50] Hongbin Lin, Yiming Yang, Yifan Zhang, Chaoda Zheng, Jie Feng, Sheng Wang, Zhennan Wang, Shijia Chen, Boyang Wang, Yu Zhang, et al. Futurex: Enhance end-to-end autonomous driving via latent chain-of-thought world model. arXiv preprint arXiv:2512.11226, 2025.

[51] Haochen Liu, Li Chen, Yu Qiao, Chen Lv, and Hongyang Li. Reasoning multi-agent behavioral topology for interactive autonomous driving. Advances in Neural Information Processing Systems, 37:92605–92637, 2024.

[52] Haochen Liu, Zhiyu Huang, Wenhui Huang, Haohan Yang, Xiaoyu Mo, and Chen Lv. Hybrid-prediction integrated planning for autonomous driving. IEEE Transactions on Pattern Analysis and Machine Intelligence, 47(4):2597–2614, 2025.

[53] Haochen Liu, Tianyu Li, Haohan Yang, Li Chen, Caojun Wang, Ke Guo, Haochen Tian, Hongchen Li, Hongyang Li, and Chen Lv. Reinforced refinement with self-aware expansion for end-to-end autonomous driving. IEEE Transactions on Pattern Analysis and Machine Intelligence, 2026.

[54] Sulin Liu, Juno Nam, Andrew Campbell, Hannes St"ark, Yilun Xu, Tommi Jaakkola, and Rafael G’omez-Bombarelli. Think while you generate: Discrete difusion with planned denoising. arXiv preprint arXiv:2410.06264, 2024.

[55] Francesco Locatello, Dirk Weissenborn, Thomas Unterthiner, Aravindh Mahendran, Georg Heigold, Jakob Uszkoreit, Alexey Dosovitskiy, and Thomas Kipf. Object-centric learning with slot attention. Advances in neural information processing systems, 33:11525–11538, 2020.

[56] Jiachen Lu, Ze Huang, Zeyu Yang, Jiahui Zhang, and Li Zhang. Wovogen: World volume-aware difusion for controllable multi-camera driving scene generation. In European conference on computer vision, pages 329–345. Springer, 2024.

[57] Omer Luxembourg, Haim Permuter, and Eliya Nachmani. Plan for speed: Dilated scheduling for masked difusion language models. arXiv preprint arXiv:2506.19037, 2025.

[58] Teli Ma, Jia Zheng, Zifan Wang, Chunli Jiang, Andy Cui, Junwei Liang, and Shuo Yang. Dit4dit: Jointly modeling video dynamics and actions for generalizable robot control. arXiv preprint arXiv:2603.10448, 2026.

[59] Yingzi Ma, Yulong Cao, Wenhao Ding, Shuibai Zhang, Yan Wang, Boris Ivanovic, Ming Jiang, Marco Pavone, and Chaowei Xiao. dvlm-ad: Enhance difusion vision-language-model for driving via controllable reasoning. arXiv preprint arXiv:2512.04459, 2025.

[60] Yong-Hyun Park, Chieh-Hsin Lai, Satoshi Hayakawa, Yuhta Takida, and Yuki Mitsufuji. Jump your steps: Optimizing sampling schedule of discrete difusion models. In International Conference on Learning Representations, volume 2025, pages 96272–96300, 2025.

[61] Fred Zhangzhi Peng, Zachary Bezemek, Sawan Patel, Jarrid Rector-Brooks, Sherwood Yao, Alexander Tong, and Pranam Chatterjee. Path planning for masked difusion model sampling. arXiv preprint arXiv:2502.03540, 2025.

[62] Yair Schif, Omer Belhasin, Roy Uziel, Guanghan Wang, Marianne Arriola, Gilad Turok, Michael Elad, and Volodymyr Kuleshov. Learn from your mistakes: Self-correcting masked difusion models. arXiv preprint arXiv:2602.11590, 2026.

[63] Shuyao Shang, Yuntao Chen, Yuqi Wang, Yingyan Li, and ZHAO-XIANG ZHANG. Drivedpo: Policy learning via safety dpo for end-to-end autonomous driving. Advances in Neural Information Processing Systems, 38: 81565–81585, 2026.

[64] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300, 2024.

[65] Chen Shi, Jinrui Xu, Shaoshuai Shi, Kehua Sheng, Bo Zhang, and Li Jiang. Drivewam: Video generative priors enable scalable world-action modeling for autonomous driving. arXiv preprint arXiv:2605.28544, 2026.

[66] Oriane Siméoni, Huy V Vo, Maximilian Seitzer, Federico Baldassarre, Maxime Oquab, Cijo Jose, Vasil Khalidov, Marc Szafraniec, Seungeun Yi, Michaël Ramamonjisoa, et al. Dinov3. arXiv preprint arXiv:2508.10104, 2025.

[67] Ziying Song, Lin Liu, Hongyu Pan, Bencheng Liao, Mingzhe Guo, Lei Yang, Yongchang Zhang, Shaoqing Xu, Caiyan Jia, and Yadan Luo. Diver: Reinforced difusion breaks imitation bottlenecks in end-to-end autonomous driving. arXiv preprint arXiv:2507.04049, 2025.

[68] Wenchao Sun, Xuewu Lin, Keyu Chen, Zixiang Pei, Xiang Li, Yining Shi, and Sifa Zheng. Sparsedrivev2: Scoring is all you need for end-to-end autonomous driving. arXiv preprint arXiv:2603.29163, 2026.

[69] Haochen Tian, Tianyu Li, Haochen Liu, Jiazhi Yang, Yihang Qiu, Guang Li, Junli Wang, Yinfeng Gao, Zhang Zhang, Liang Wang, et al. Simscale: Learning to drive via real-world simulation at scale. arXiv preprint arXiv:2511.23369, 2025.

[70] Wenwen Tong, Chonghao Sima, Tai Wang, Li Chen, Silei Wu, Hanming Deng, Yi Gu, Lewei Lu, Ping Luo, Dahua Lin, et al. Scene as occupancy. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 8406–8415, 2023.

[71] Aaron van den Oord, Oriol Vinyals, and Koray Kavukcuoglu. Neural discrete representation learning. In Advances in Neural Information Processing Systems, 2017.

[72] Huimin Wang, Yue Wang, Bihao Cui, Pengxiang Li, Ben Lu, Mingqian Wang, Tong Wang, Chuan Tang, Teng Zhang, and Kun Zhan. Reflectdrive-2: Reinforcement-learning-aligned self-editing for discrete difusion driving. arXiv preprint arXiv:2605.04647, 2026.

[73] Linbo Wang, Yupeng Zheng, Qiang Chen, Shiwei Li, Yichen Zhang, Zebin Xing, Qichao Zhang, Xiang Li, Deheng Qian, Pengxuan Yang, et al. Latent-wam: Latent world action modeling for end-to-end autonomous driving. arXiv preprint arXiv:2603.24581, 2026.

[74] Linhan Wang, Zichong Yang, Chen Bai, Guoxiang Zhang, Xiaotong Liu, Xiaoyin Zheng, Xiao-Xiao Long, Chang-Tien Lu, and Cheng Lu. Drive-jepa: Video jepa meets multimodal trajectory distillation for end-to-end driving. arXiv preprint arXiv:2601.22032, 2026.

[75] Wenshuo Wang, Letian Wang, Chengyuan Zhang, Changliu Liu, and Lijun Sun. Social interactions for autonomous driving: A review and perspectives. Foundations and Trends® in Robotics, 10(3-4):198–377, 2022.

[76] Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, Jiagang Zhu, and Jiwen Lu. Drivedreamer: Towards real-world-drive world models for autonomous driving. In European conference on computer vision, pages 55–72. Springer, 2024.

[77] Yuqi Wang, Jiawei He, Lue Fan, Hongxin Li, Yuntao Chen, and Zhaoxiang Zhang. Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 14749–14759, 2024.

[78] Julong Wei, Shanshuai Yuan, Pengfei Li, Qingda Hu, Zhongxue Gan, and Wenchao Ding. Occllama: An occupancy-language-action generative world model for autonomous driving. arXiv preprint arXiv:2409.03272, 2024.

[79] Xinshuo Weng, Boris Ivanovic, Yan Wang, Yue Wang, and Marco Pavone. Para-drive: Parallelized architecture for real-time autonomous driving. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 15449–15458, 2024.

[80] Tianze Xia, Yongkang Li, Lijun Zhou, Jingfeng Yao, Kaixin Xiong, Haiyang Sun, Bing Wang, Kun Ma, Guang Chen, Hangjun Ye, et al. Drivelaw: Unifying planning and video generation in a latent driving world. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 39701–39712, 2026.

[81] Zebin Xing, Xingyu Zhang, Yang Hu, Bo Jiang, Tong He, Qian Zhang, Xiaoxiao Long, and Wei Yin. Goalflow: Goal-driven flow matching for multimodal trajectories generation in end-to-end autonomous driving. In Proceedings of the Computer Vision and Pattern Recognition Conference, pages 1602–1611, 2025.

[82] Yifang Xu, Jiahao Cui, Feipeng Cai, Zhihao Zhu, Hanlin Shang, Shan Luan, Mingwang Xu, Neng Zhang, Yaoyi Li, Jia Cai, et al. Wam-flow: Parallel coarse-to-fine motion planning via discrete flow matching for autonomous driving. arXiv preprint arXiv:2512.06112, 2025.

[83] Zhenhua Xu, Yujia Zhang, Enze Xie, Zhen Zhao, Yong Guo, Kwan-Yee K Wong, Zhenguo Li, and Hengshuang Zhao. Drivegpt4: Interpretable end-to-end autonomous driving via large language model. IEEE Robotics and Automation Letters, 2024.

[84] Tianyi Yan, Tao Tang, Xingtai Gui, Yongkang Li, Jiasen Zheng, Weiyao Huang, Lingdong Kong, Wencheng Han, Xia Zhou, Xueyang Zhang, et al. Ad-r1: Closed-loop reinforcement learning for end-to-end autonomous driving with impartial world models. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 1085–1095, 2026.

[85] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. arXiv preprint arXiv:2505.09388, 2025.

[86] Jiazhi Yang, Shenyuan Gao, Yihang Qiu, Li Chen, Tianyu Li, Bo Dai, Kashyap Chitta, Penghao Wu, Jia Zeng, Ping Luo, et al. Genad: Generalized predictive model for autonomous driving. arXiv preprint arXiv:2403.09630, 2024.

[87] Jiazhi Yang, Shenyuan Gao, Yihang Qiu, Li Chen, Tianyu Li, Bo Dai, Kashyap Chitta, Penghao Wu, Jia Zeng, Ping Luo, et al. Generalized predictive model for autonomous driving. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 14662–14672, 2024.

[88] Jiazhi Yang, Kunyang Lin, Jinwei Li, Wencong Zhang, Tianwei Lin, Longyan Wu, Zhizhong Su, Hao Zhao, Ya-Qin Zhang, Li Chen, et al. Rise: Self-improving robot policy with compositional world model. arXiv preprint arXiv:2602.11075, 2026.

[89] Pengxuan Yang, Yupeng Zheng, Deheng Qian, Zebin Xing, Qichao Zhang, Linbo Wang, Yichen Zhang, Shaoyu Guo, Zhongpu Xia, Qiang Chen, et al. Dreamerad: Eficient reinforcement learning via latent world model for autonomous driving. arXiv preprint arXiv:2603.24587, 2026.

[90] Wenhao Yao, Zhenxin Li, Shiyi Lan, Zi Wang, Xinglong Sun, Jose M Alvarez, and Zuxuan Wu. Drivesuprim: Towards precise trajectory selection for end-to-end planning. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 40, pages 11910–11918, 2026.

[91] Ziyang Yao, Zeyu Zhu, YunCheng Jiang, Zibin Guo, and Huijing Zhao. Unified driving tokens: Representationand geometry-guided discrete tokenizer for driving world models and planning. arXiv preprint arXiv:2606.01935, 2026.

[92] Bowen Ye, Bin Zhang, and Hang Zhao. Dap: A discrete-token autoregressive planner for autonomous driving. arXiv preprint arXiv:2511.13306, 2025.

[93] Seonghyeon Ye, Yunhao Ge, Kaiyuan Zheng, Shenyuan Gao, Sihyun Yu, George Kurian, Suneel Indupuru, You Liang Tan, Chuning Zhu, Jiannan Xiang, et al. World action models are zero-shot policies. arXiv preprint arXiv:2602.15922, 2026.

[94] Tianyuan Yuan, Zibin Dong, Yicheng Liu, and Hang Zhao. Fast-wam: Do world action models need test-time future imagination? arXiv preprint arXiv:2603.16666, 2026.

[95] Rongxiang Zeng and Yongqi Dong. Latent world models for automated driving: A unified taxonomy, evaluation framework, and open challenges. arXiv preprint arXiv:2603.09086, 2026.

[96] Kaiwen Zhang, Zhenyu Tang, Xiaotao Hu, Xingang Pan, Xiaoyang Guo, Yuan Liu, Jingwei Huang, Li Yuan, Qian Zhang, Xiao-Xiao Long, et al. Epona: Autoregressive difusion world model for autonomous driving. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 27220–27230, 2025.

[97] Kewei Zhang, Jin Wang, Sensen Gao, Chengyue Wu, Yulong Cao, Songyang Han, Boris Ivanovic, Langechuan Liu, Marco Pavone, Song Han, et al. Fast-ddrive: Eficient block-difusion vlm for autonomous driving. arXiv preprint arXiv:2605.23163, 2026.

[98] Leo Zhang and Saifuddin Syed. The cosine schedule is fisher-rao-optimal for masked discrete difusion models. arXiv preprint arXiv:2508.04884, 2025.

[99] Siyan Zhao, Devaansh Gupta, Qinqing Zheng, and Aditya Grover. d1: Scaling reasoning in difusion large language models via reinforcement learning. Advances in Neural Information Processing Systems, 38:56729–56762, 2026.

[100] Yixiu Zhao, Jiaxin Shi, Feng Chen, Shaul Druckmann, Lester Mackey, and Scott Linderman. Informed correctors for discrete difusion models. arXiv preprint arXiv:2407.21243, 2024.

[101] Zewei Zhou, Tianhui Cai, Seth Z Zhao, Yun Zhang, Zhiyu Huang, Bolei Zhou, and Jiaqi Ma. Autovla: A vision-language-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning. arXiv preprint arXiv:2506.13757, 2025.

[102] Chuning Zhu, Raymond Yu, Siyuan Feng, Benjamin Burchfiel, Paarth Shah, and Abhishek Gupta. Unified world models: Coupling video and action difusion for pretraining on large robotic datasets. arXiv preprint arXiv:2504.02792, 2025.

[103] Jialv Zou, Shaoyu Chen, Bencheng Liao, Zhiyu Zheng, Yuehao Song, Lefei Zhang, Qian Zhang, Wenyu Liu, and Xinggang Wang. Difusiondrivev2: Reinforcement learning-constrained truncated difusion modeling in end-to-end autonomous driving. arXiv preprint arXiv:2512.07745, 2025.

## 6 Contributions and Acknowledgments

## Core Contributors

• Ziyang Yao<sup>∗</sup>

• Haochen Liu<sup>∗†</sup>

• Yuncheng Jiang<sup>∗†§</sup>

• Zeyu Zhu<sup>‡</sup>

• Zibin Guo

• Jingwei Zhao

• Guang Chen

• Hangjun Ye

## Contributors

• Jingru Wang

• Tianle Liu

• Jianwei Cui

• Kuiyuan Yang

• Hongwei Xie

## 7 Appendix

## 7.1 Related Work

## 7.1.1 World Policy Modeling

World models (WMs) have emerged as a central paradigm for physical intelligence, aiming to model how the external world evolves under agent actions [23]. In autonomous driving, early world-model-inspired approaches were often coupled with planning through intermediate representations, such as occupancy forecasting [52, 70, 78] or joint motion prediction [15, 25, 31, 51], where future dynamics were learned primarily to support downstream decision making. With the emergence of large-scale vision foundation models [37], recent research has increasingly shifted toward future visual supervision [21, 56, 76, 87], leveraging image and video generation as rich supervisory signals for representation learning [74], planning-oriented reasoning [89], and even explicit or implicit reward modeling [43, 77]. In parallel, another line of research focuses on simulation and data generation engines. These approaches construct interactive or long-tail scenarios through structured world modeling [88], such as behavior simulation [49], 3D scene reconstruction [20, 69], or generative video models [76, 86]. By synthesizing diverse future outcomes and counterfactual interactions, they provide scalable environments for policy evaluation, closed-loop training, and safety validation. Despite their success, most existing approaches still treat world modeling and planning as loosely coupled components, where the world model primarily serves as an auxiliary predictor or simulator rather than being jointly optimized with decision making under a unified causal formulation.

This limitation has motivated the recent development of world-action modeling (WAM) [102], which jointly formulates future observation and policy generation as a unified learning problem [9, 42]. Some works model future worlds and agent actions as a single generative process [58, 80, 93], while others emphasize unified pretraining [94] of shared world-policy representations [5], latent action modeling [22], and value-aware world models [36] to reduce the redundancy of explicit observation generation and strengthen the coupling between environment dynamics and control. However, existing formulations are predominantly built upon continuous latent spaces, which often sufer from representation ambiguity [65, 96]. These limitations have recently inspired the adoption of parallel generative paradigms based on discrete token spaces, including mask modeling and discrete difusion [72, 82, 97]. While such methods improve generation eficiency and enable iterative refinement, most of them still formulate decision making as a direct observation-to-action mapping without explicitly learning a unified generative prior over both future worlds and policies. In contrast, Discrete-WAM formulates observations and actions within a shared discrete representation space. Unified generative pretraining establishes a common prior over world evolution and policy generation, while the joint discrete difusion formulation provides a unified framework for world modeling and decision making.

## 7.1.2 Discrete Diffusion Scheduling

Sampling schedules play a central role in discrete and masked difusion models because they determine not only the number of reverse steps, but also which tokens are decoded jointly at each step. In discrete difusion models, early work such as D3PM formalizes discrete corruption kernels, including absorbing-state processes, which provide the basis for mask-based reverse generation [1]. Subsequent work studies scheduling from several complementary perspectives.

One line of work focuses on time-grid or noise-level scheduling. JYS optimizes the sampling time grid by minimizing a path-space KL upper bound, showing that non-uniform schedules can reduce discretization error in discrete difusion sampling [60]. Related information-geometric analysis further argues that the commonly used cosine schedule can be interpreted as Fisher–Rao optimal for masked discrete difusion under specific geometric assumptions [98].

A second line studies how many tokens should be decoded per iteration. [40] derive an information-theoretic convergence bound for difusion language models and show that balanced block schedules yield an O(1/T)-type reduction of KL error under general assumptions . [14] further characterize the optimal inference schedule as the best step-function approximation to an information curve, making explicit that the optimal block sizes depend on the dependency structure of the data distribution . [38] also analyze the error induced by factorized approximations and derive asymptotically optimal schedules from an information-profile viewpoint .

A third line uses confidence or entropy to adapt the unmasking budget. EB-Sampler decomposes sampling error into denoiser model error and joint-dependence error, and uses entropy-bounded unmasking to accelerate masked difusion sampling while controlling the risk of decoding too many uncertain tokens simultaneously [4]. [7] provide a provable analysis of confidence-based decoding and show that entropy-sum stopping rules can achieve KL-accurate sampling with an expected number of steps depending on the intrinsic entropy of the data distribution .

A fourth line studies which positions should be decoded together. DUS proposes a dilated unmasking schedule that selects separated positions in early iterations to reduce the entropy gap among jointly decoded tokens, followed by finer local decoding in later iterations [57]. This is particularly suitable when dependencies are local or fast-mixing, but it may be less reliable for tasks dominated by global consistency constraints.

Finally, several works extend scheduling with learned planners or correction mechanisms. DDPD and P2 decouple position planning from token denoising, allowing the model to learn nontrivial unmasking paths [54, 61]. Informed correctors and self-correcting masked difusion further introduce correction or remasking mechanisms to revise earlier decoding errors [62, 100]. These methods are practically useful, but their theoretical guarantees are generally weaker than the information-theoretic schedule analyses above. Recent theory also shows that although masked difusion can be eficient for token-level quality, sequence-level correctness may still require a number of steps scaling with sequence length in worst-case settings [19, 35]. Therefore, scheduling should be understood as a mechanism for reducing discretization error and paralleldependence error, rather than as a universal solution to all long-range dependency constraints.

## 7.1.3 Policy Post-training

While large-scale pretraining has significantly improved the generalization capability of E2E autonomous driving systems [11], it is fundamentally optimized under an open-loop objective and therefore cannot fully address distribution shifts induced by closed-loop interactions [75]. In particular, behavior cloning learns to match demonstrated actions but does not directly optimize the sequential objectives used in closed-loop evaluation, resulting in a persistent objective gap [34]. To mitigate this discrepancy, studies have explored ofline reinforcement learning and post-training strategies for policy alignment [47, 67]. Early approaches construct positive and negative trajectory pairs and apply preference optimization, such as DPO-style ranking [63] or inverse reinforcement learning [32], to encourage preferred behaviors. However, these methods remain optimizing relative preferences rather than long-horizon driving objective. More recently, policy-gradientbased approaches such as GRPO [64] have been introduced to directly optimize trajectory-level rewards and closed-loop metrics [43, 44, 53]. Nevertheless, existing methods typically operate on complete trajectories and therefore only improve trajectory generation conditioned on a fixed decision, without explicitly optimizing the high-level decision-making process itself. A parallel research direction leverages 3DGS-based simulators or learned world models to enable online RL through interaction [20, 49, 69, 84]. Although these methods provide a mechanism for closed-loop optimization, their performance is inherently limited by accumulated simulation and model errors, which introduce additional bias into policy learning. Recent approaches attempt to alleviate this issue by performing reinforcement learning directly in latent transition spaces [10, 72, 73, 89], avoiding explicit simulator rollouts while still improving long-horizon reasoning capabilities. In contrast, our framework jointly optimizes both decision selection and trajectory planning through a unified GRPO objective. By performing policy optimization over a structured decision-planning hierarchy, our method not only improves planning quality under closed-loop metrics but also explicitly refines the decision space itself, enabling more efective optimization of long-horizon driving behavior.

## 7.2 Additional Implementation Details

## 7.2.1 Token Design

Vision token configuration. We employ the codebook size of $K _ { V } = 1 6 3 8 4$ for quantizer, and $H _ { V } , W _ { V } = 1 6$ for image patch. The rest of the pipeline are aligned with our previous setup.

Decision token configuration. We parameterize high-level driving decisions with a discrete decision vocabulary constructed from lateral path candidates and longitudinal speed profiles. Specifically, let $\mathcal { P } = \{ p _ { i } \} _ { i = 1 } ^ { N _ { \mathrm { l a t } } }$ denote the set of lateral path primitives and $\mathcal { S } = \{ s _ { j } \} _ { j = 1 } ^ { N _ { \mathrm { l o r } } }$ denote the set of longitudinal speed profiles. Their Cartesian product defines a decision token space: $\mathcal { D } \stackrel { } { = } \tilde { \mathcal { P } } \times \mathcal { S } , | \mathcal { D } | = N _ { \mathrm { l a t } } N _ { \mathrm { l o n } } = 4 0 0$ , where each decision token $d _ { i , j } \in \mathcal { D }$ specifies a coarse behavior prior combining path topology and speed evolution. During pretraining, we assign supervision by evaluating all candidate decisions with a winner-take-all criterion based on the EPDMS sub-scores. The selected decision is $d ^ { \star } = \arg \operatorname* { m a x } _ { d \in \mathcal { D } } R _ { \mathrm { E P D M S } } ( d )$ , where $R _ { \mathrm { E P D M S } }$ aggregates safety, progress, comfort, and rule-compliance sub-scores. The model is then trained to predict $d ^ { \star }$ from the current observation and context using a cross-entropy objective: $\mathcal { L } _ { \mathrm { d e c } } = - \log p _ { \theta } ( d ^ { \star } \mid \mathbf { o } , \mathbf { c } ) + \mathcal { L } _ { \mathrm { s c o r e } }$

For SFT and post-training, we further restrict the decision space to the top-D candidates ranking, forming a compact decision set $\mathcal { D } _ { \mathrm { t o p } } \subset \mathcal { D }$ . Subsequent supervised fine-tuning and RL optimization are performed within $\mathcal { D } _ { \mathrm { t o p } } ,$ which preserves high-quality behavioral diversity while avoiding exploration over suboptimal decisions.

Vocabulary configuration for action and auxiliary position supervision. For the acceleration-token vocabulary, we use a two-dimensional grid over ego-centric longitudinal and lateral accelerations. Both acceleration components are clipped to the valid range $[ - 4 , 4 ] \mathrm { m } / \mathrm { { s } ^ { 2 } }$ . The longitudinal and lateral acceleration dimensions are uniformly partitioned into $N _ { x } = N _ { y } = 6 0$ bins, forming a grid-structured acceleration vocabulary with $6 0 \times 6 0 = 3 6 0 0$ prototypes. Each vocabulary entry corresponds to a 2D acceleration prototype

$$
\begin{array} { r } { \mathbf v _ { i j } = ( c _ { i } ^ { x } , c _ { j } ^ { y } ) , \qquad i , j \in \{ 1 , \dots , 6 0 \} , } \end{array}
$$

where $c _ { i } ^ { x }$ and $c _ { j } ^ { y }$ denote the uniformly spaced bin centers along the longitudinal and lateral acceleration dimensions. Continuous accelerations are represented by soft labels over the four neighboring prototypes through bilinear interpolation, as described in Sec. 2.3.

In addition to acceleration-token classification, we introduce an auxiliary position classification task to supervise the trajectory obtained after integrating the predicted accelerations. To avoid the prohibitive vocabulary size induced by a Cartesian-product 2D position grid, we factorize position supervision into two independent one-dimensional classification tasks over ego-centric longitudinal and lateral positions. The longitudinal position range is [−2, 65] m, and the lateral position range is [−25, 25] m. Both dimensions use a grid-cell resolution of 0.02 m, resulting in

$$
N _ { x } ^ { p } = { \frac { 6 5 - ( - 2 ) } { 0 . 0 2 } } = 3 3 5 0 , \qquad N _ { y } ^ { p } = { \frac { 2 5 - ( - 2 5 ) } { 0 . 0 2 } } = 2 5 0 0 .
$$

The auxiliary position heads therefore predict two categorical distributions, one over 3350 longitudinal bins and the other over 2500 lateral bins, rather than a single 3350 × 2500 joint vocabulary. This factorized position supervision provides fine-grained trajectory-level spatial constraints while keeping the classification space computationally tractable.

Auxiliary factorized position classification loss. Let ${ \bf p } _ { h } = ( x _ { h } , y _ { h } )$ denote the ground-truth future ego position at horizon step h. The auxiliary position classification loss is defined as the sum of the longitudinal and lateral cross-entropy losses:

$$
\mathcal { L } _ { \mathrm { p o s } } = \sum _ { h = 1 } ^ { H } \left[ \mathrm { C E } \left( \boldsymbol { p } _ { h } ^ { x , * } , \boldsymbol { q } _ { \theta , h } ^ { x } \right) + \mathrm { C E } \left( \boldsymbol { p } _ { h } ^ { y , * } , \boldsymbol { q } _ { \theta , h } ^ { y } \right) \right] ,
$$

where $p _ { h } ^ { x , * }$ and $p _ { h } ^ { y , * }$ denote the target distributions over the discretized x and y position bins, and $q _ { \theta , h } ^ { x }$ and $q _ { \theta , h } ^ { y }$ are the corresponding predicted distributions. This factorized formulation avoids the cost of a joint 2D position vocabulary while still providing direct supervision on the integrated trajectory.

## 7.2.2 Detailed Token-Editing Objective

We provide the detailed mathematical formulation of the token-editing objective used in unified pretraining. At time step $t ,$ the scene context is denoted as $\mathbf { C } _ { t } ,$ which contains historical visual tokens, ego-state tokens, and navigation tokens. The model may also condition on a high-level decision token sequence $\mathbf { D } _ { t } \subset \mathcal { D } _ { \mathrm { t o p } }$

Let $\mathbf { X } = \{ x _ { j } \} _ { j = \cdot } ^ { N }$ denote a clean target token sequence. Depending on the task, X can be a future visual token sequence $\mathbf { V } _ { t + \bar { 1 } : t + H }$ or a future action token sequence $\mathbf { A } _ { t + 1 : t + H }$ . The corrupted version of the target sequence is denoted as $\tilde { \mathbf { X } } = \{ \tilde { x } _ { j } \} _ { j = 1 } ^ { N }$ . The efective model input is the concatenation of the scene context, optional decision tokens, and corrupted target tokens: $[ \mathbf { C } _ { t } , \mathbf { D } _ { t } , \tilde { \mathbf { X } } ]$ . Unlike masked difusion methods that introduce a special mask token, our formulation corrupts tokens within the original discrete vocabulary. Let $\mathcal { M } _ { \gamma } ^ { X }$ denote the corrupted token positions under corruption ratio $\gamma \in [ 0 , 1 ]$ . The vocabulary associated with X is

$$
B _ { X } = \left\{ { \begin{array} { l l } { V , } & { \mathbf { X } = \mathbf { V } _ { t + 1 : t + H } , } \\ { A , } & { \mathbf { X } = \mathbf { A } _ { t + 1 : t + H } , } \end{array} } \right.\tag{11}
$$

where V and A denote the visual and action vocabularies, respectively. The corrupted sequence is constructed as

$$
\tilde { x } _ { j } = \left\{ \begin{array} { l l } { \eta _ { j } , } & { j \in { \mathcal { M } } _ { \gamma } ^ { X } , } \\ { x _ { j } , } & { j \notin { \mathcal { M } } _ { \gamma } ^ { X } , } \end{array} \right. \ \eta _ { j } \sim \mathrm { U n i f } ( { \mathcal { B } _ { X } } ) ,\tag{12}
$$

where $\operatorname { U n i f } ( B _ { X } )$ denotes the uniform distribution over valid tokens in $\boldsymbol { { B } } _ { X }$

The token-editing loss is applied to all editable positions, including both corrupted and clean tokens:

$$
\mathcal { L } _ { \mathrm { e d i t } } ( \mathbf { X } ) = - \frac { 1 } { N } \sum _ { j = 1 } ^ { N } \log p _ { \theta } ( x _ { j } \mid \mathbf { C } _ { t } , \mathbf { D } _ { t } , \tilde { \mathbf { X } } , \gamma ) .\tag{13}
$$

For corrupted positions, this loss trains the model to recover the clean target tokens. For clean positions, it encourages an identity mapping, teaching the model to preserve tokens that are already correct and providing an implicit stopping signal for token editing.

The corruption pattern difers across modalities. For visual prediction, corrupted image-token positions are sampled uniformly from all subsets with cardinality $\lfloor \gamma N _ { v } \rfloor$

$$
\mathcal { M } _ { \gamma } ^ { v } \sim \mathrm { U n i f } \left( \left\{ \mathcal { M } \subseteq \left\{ 1 , \dots , N _ { v } \right\} : \left| \mathcal { M } \right| = \left\lfloor \gamma N _ { v } \right\rfloor \right\} \right) .\tag{14}
$$

For action prediction, corruption follows a causal sufix pattern:

$$
h _ { \gamma } = \lfloor ( 1 - \gamma ) H \rfloor , \quad \mathcal { M } _ { \gamma } ^ { a } = \{ h _ { \gamma } + 1 , \ldots , H \} .\tag{15}
$$

Thus, the first $h _ { \gamma }$ action tokens remain clean, while the remaining sufix is corrupted. This design respects the temporal dependency of acceleration-based action tokens.

The final training objective combines token classification losses and continuous motion regression losses:

$$
\begin{array} { r } { \mathscr { L } = \lambda _ { v } \mathscr { L } _ { v } ^ { \mathrm { c l s } } + \lambda _ { a } \mathscr { L } _ { a } ^ { \mathrm { c l s } } + \lambda _ { \mathrm { a c c } } \mathscr { L } _ { \mathrm { a c c } } + \lambda _ { \mathrm { t r a j } } \mathscr { L } _ { \mathrm { t r a j } } + \lambda _ { s } \mathscr { L } _ { s } ^ { \mathrm { c l s } } + \lambda _ { \mathrm { d e c } } \mathscr { L } _ { \mathrm { d e c } } . } \end{array}\tag{16}
$$

Here, $\mathcal { L } _ { v } ^ { \mathrm { c l s } }$ and $\mathcal { L } _ { a } ^ { \mathrm { c l s } }$ are cross-entropy losses over the visual and action vocabularies. $\mathcal { L } _ { \mathrm { a c c } }$ is the acceleration-level regression loss, and $\mathcal { L } _ { \mathrm { t r a j } }$ is the trajectory-level regression loss obtained after integrating predicted accelerations into future ego trajectories. $\mathcal { L } _ { s } ^ { \mathrm { c l s } }$ denotes the classification loss for auxiliary special tokens. Diferent tasks activate diferent subsets of these losses according to their prediction targets.

## 7.2.3 Model Structure Design

Our model is built upon a decoder-only Transformer [85] with hidden dimension $d = 2 0 4 8$ , 18 Transformer layers, 16 attention heads, and 8 key-value heads of grouped-query attention. Rotary positional embeddings follow the Qwen3-MRoPE scheme with $\theta = 1 0 ^ { 6 }$ and multi-axis section splits [24, 20, 20]. The total parameter count is approximately 1B. Parameters for LoRA finetuning is about 30M.

## 7.2.4 Benchmark Details

Evaluation metrics. We evaluate planning performance using the Predictive Driver Model Score (PDMS) and its extended version EPDMS used in NAVSIM. PDMS was introduced in NAVSIM v1 [17] as a simulation-based open-loop metric, where the predicted 4-second trajectory is unrolled in a BEV simulator and scored by combining multiplicative safety constraints with weighted planning-quality subscores. It is defined as

$$
\mathrm { P D M S } = \left( \prod _ { m \in \{ \mathrm { N C , D A C } \} } m ( \mathrm { a g e n t } ) \right) \cdot \frac { \sum _ { m \in \{ \mathrm { T T C , E P , C \} } } w _ { m } m ( \mathrm { a g e n t } ) } { \sum _ { m \in \{ \mathrm { T T C , E P , C \} } } w _ { m } } ,\tag{17}
$$

where NC denotes no at-fault collision, DAC denotes drivable-area compliance, TTC denotes time-to-collision, EP denotes ego progress, and C denotes comfort. NAVSIM v2 [8] further adopts the Extended Predictive Driver Model Score (EPDMS), which adds driving-direction compliance (DDC), trafic-light compliance (TLC) for multiplicative scoring, and adding lane keeping (LK), history comfort (HC), and extended comfort (EC) in weighted scores. EPDMS further adds filter with

$$
\mathrm { f l l t e r } _ { m } ( \mathrm { a g e n t , h u m a n } ) = \left\{ \begin{array} { l l } { 1 . 0 , } & { \mathrm { i f ~ } m ( \mathrm { h u m a n } ) = 0 , } \\ { m ( \mathrm { a g e n t } ) , } & { \mathrm { o t h e r w i s e } . } \end{array} \right.\tag{18}
$$

This filtering avoids penalizing the planner when the same violation is also present in the human demonstration, which can occur due to annotation noise or contextually valid maneuvers. The weighted EPDMS terms use $w _ { \mathrm { E P } } = 5 , w _ { \mathrm { T T C } } = 5 , w _ { \mathrm { L K } } = 2 , w _ { \mathrm { H C } } = 2 ,$ and $w _ { \mathrm { E C } } = 2$

Baselines. We compare Discrete-WAM with a diverse set of state-of-the-art autonomous driving systems, including modular end-to-end plannersr [13, 16, 28], generative planners [24, 44, 46, 48, 68, 103], world-model based methods [42, 96], world-action policies [73, 82, 89], and vision-language-action (VLA) approaches [32, 42].

## 7.3 Analytical Results

This section provides the theoretical analysis used in Sec. 3.1. We use a generic notation where C denotes the context, Z denotes a latent skeleton, and $\mathbf { Y } _ { U } = \{ Y _ { i } : i \in U \}$ denotes a group of future tokens. For policy modeling, Z corresponds to the decision skeleton $\mathbf { D } _ { t } ,$ , and $\mathbf { Y } _ { U }$ corresponds to a subset of future action tokens.

## 7.3.1 One-step KL Decomposition

For a token group $\mathbf { Y } _ { U } .$ , the conditional total correlation is defined as

$$
\operatorname { T C } ( \mathbf { Y } _ { U } \mid C ) = D _ { \mathrm { K L } } \left( q ( \mathbf { Y } _ { U } \mid C ) \parallel \prod _ { i \in U } q ( Y _ { i } \mid C ) \right) .\tag{19}
$$

Equivalently,

$$
\operatorname { T C } ( \mathbf { Y } _ { U } \mid C ) = \sum _ { i \in U } H ( Y _ { i } \mid C ) - H ( \mathbf { Y } _ { U } \mid C ) .\tag{20}
$$

Assume a parallel token predictor factorizes the token group as

$$
p _ { \theta } ( \mathbf { Y } _ { U } \mid C ) = \prod _ { i \in U } p _ { \theta } ( Y _ { i } \mid C ) .\tag{21}
$$

Then the one-step KL error decomposes as

$$
\begin{array} { r l } {  { D _ { \mathrm { K L } } ( q ( \mathbf { Y } _ { U } \mid C ) \| \prod _ { i \in U } p _ { \theta } ( Y _ { i } \mid C ) ) } } \\ & { = \mathrm { T C } ( \mathbf { Y } _ { U } \mid C ) + \displaystyle \sum _ { i \in U } D _ { \mathrm { K L } } ( q ( Y _ { i } \mid C ) \| p _ { \theta } ( Y _ { i } \mid C ) ) . } \end{array}\tag{22}
$$

Proof. By expanding the KL divergence,

$$
\begin{array} { r l } & { D _ { \mathrm { K L } } \left( q ( \mathbf { Y } _ { U } \mid C ) \| \displaystyle \prod _ { i \in U } p _ { \theta } ( Y _ { i } \mid C ) \right) } \\ & { = \mathbb { E } _ { q } \left[ \log q ( \mathbf { Y } _ { U } \mid C ) - \displaystyle \sum _ { i \in U } \log p _ { \theta } ( Y _ { i } \mid C ) \right] . } \end{array}\tag{23}
$$

Adding and subtracting $\textstyle \sum _ { i \in U }$ log $q ( Y _ { i } \mid C )$ gives

$$
\mathbb { E } _ { q } \left[ \log \frac { q ( \mathbf { Y } _ { U } \mid C ) } { \prod _ { i \in U } q ( Y _ { i } \mid C ) } \right] + \sum _ { i \in U } \mathbb { E } _ { q } \left[ \log \frac { q ( Y _ { i } \mid C ) } { p _ { \theta } ( Y _ { i } \mid C ) } \right] ,\tag{24}
$$

which is exactly the sum of conditional total correlation and token-level model errors.

## 7.3.2 Latent Skeleton Decomposition

We define the redundancy gain of a latent skeleton $Z$ as

$$
R _ { Z } ( U \mid C ) = \sum _ { i \in U } I ( Y _ { i } ; Z \mid C ) - I ( \mathbf { Y } _ { U } ; Z \mid C ) .\tag{25}
$$

Then the skeleton-conditioned residual total correlation satisfies

$$
\operatorname { \mathbb { E } } _ { Z } \mathrm { T C } ( \mathbf { Y } _ { U } \mid C , Z ) = \mathrm { T C } ( \mathbf { Y } _ { U } \mid C ) - R _ { Z } ( U \mid C ) .\tag{26}
$$

Proof. Using the entropy form of total correlation,

$$
\operatorname { \mathbb { E } } _ { Z } \mathrm { T C } ( \mathbf { Y } _ { U } \mid C , Z ) = \sum _ { i \in U } H ( Y _ { i } \mid C , Z ) - H ( \mathbf { Y } _ { U } \mid C , Z ) .\tag{27}
$$

Since

$$
H ( Y _ { i } \mid C , Z ) = H ( Y _ { i } \mid C ) - I ( Y _ { i } ; Z \mid C )\tag{28}
$$

and

$$
H ( \mathbf { Y } _ { U } \mid C , Z ) = H ( \mathbf { Y } _ { U } \mid C ) - I ( \mathbf { Y } _ { U } ; Z \mid C ) ,\tag{29}
$$

we obtain

$$
\begin{array} { l } { \displaystyle \mathbb { E } _ { Z } \mathrm { T C } ( \mathbf { Y } _ { U } \mid C , Z ) = \sum _ { i \in U } H ( Y _ { i } \mid C ) - H ( \mathbf { Y } _ { U } \mid C ) } \\ { \displaystyle \qquad - \left[ \sum _ { i \in U } I ( Y _ { i } ; Z \mid C ) - I ( \mathbf { Y } _ { U } ; Z \mid C ) \right] } \\ { \displaystyle = \mathrm { T C } ( \mathbf { Y } _ { U } \mid C ) - R _ { Z } ( U \mid C ) . } \end{array}\tag{30}
$$

This identity shows that introducing a latent skeleton does not automatically reduce token dependence. The residual total correlation decreases only when $R _ { Z } ( U \mid C ) > 0$ . This is expected when Z is an upstream common-cause skeleton of the fine tokens, but may fail when $Z$ is a downstream collider or a synergistic summary of the token group.

## 7.3.3 Positive Redundancy Gain under Residual Mixing

We now state suficient conditions under which a latent skeleton yields positive redundancy gain.

Assumption 1: Upstream common-cause skeleton. Given context $C ,$ the latent skeleton $Z$ is an upstream low-frequency variable that conditions the generation of the fine token group $\mathbf { Y } _ { U } { \mathrm { : } }$

$$
C \to Z \to \mathbf { Y } _ { U } .\tag{31}
$$

This excludes downstream trajectory summaries, evaluation labels, or selection variables that are computed after observing the full token group.

Assumption 2: Pre-skeleton dependence lower bound. There exists $\kappa ( U ) > 0$ such that

$$
\operatorname { T C } ( \mathbf { Y } _ { U } \mid C ) \geq \kappa ( U ) .\tag{32}
$$

This means that the token group contains non-trivial group-level dependence before conditioning on the skeleton.

Assumption 3: Residual mixing after skeleton conditioning. After conditioning on $( C , Z )$ , the residual dependence between fine tokens decays with their distance:

$$
I ( Y _ { i } ; Y _ { j } \mid C , Z ) \leq \beta \exp \left( - \frac { d ( i , j ) } { \ell _ { z } } \right) ,\tag{33}
$$

where $\beta$ measures residual local coupling strength, $d ( i , j )$ is the distance between tokens i and $j ,$ and $\ell _ { z }$ is the residual correlation length. Under this assumption, the skeleton-conditioned residual total correlation is upper bounded by

$$
\begin{array} { r } { \operatorname { \mathbb { E } } _ { Z } \mathrm { T C } ( \mathbf { Y } _ { U } \mid C , Z ) \leq \varepsilon _ { z } ( U ) , } \end{array}\tag{34}
$$

where

$$
\varepsilon _ { z } ( U ) = \mathbb { E } _ { Z } \left[ \sum _ { \{ i , j \} \subset U } \beta \exp \left( - \frac { d ( i , j ) } { \ell _ { z } } \right) \right] .\tag{35}
$$

Combining the latent skeleton decomposition with the above assumptions gives

$$
\begin{array} { r l } & { { \cal R } _ { Z } ( { \cal U } \mid { \cal C } ) = \mathrm { T C } ( { \bf Y } _ { \cal U } \mid { \cal C } ) - \mathbb { E } _ { Z } \mathrm { T C } ( { \bf Y } _ { \cal U } \mid { \cal C } , Z ) } \\ & { \quad \quad \quad \ge \kappa ( { \cal U } ) - \varepsilon _ { z } ( { \cal U } ) . } \end{array}\tag{36}
$$

Therefore, if

$$
\begin{array} { r } { \kappa ( U ) > \varepsilon _ { z } ( U ) , } \end{array}\tag{37}
$$

then

$$
R _ { Z } ( U \mid C ) > 0 .\tag{38}
$$

Equivalently, under the residual mixing bound, a verifiable suficient condition is

$$
\kappa ( U ) > \mathbb { E } _ { Z } \left[ \sum _ { \left\{ i , j \right\} \subset U } \beta \exp \left( - \frac { d ( i , j ) } { \ell _ { z } } \right) \right] \Longrightarrow R _ { Z } ( U \mid C ) > 0 .\tag{39}
$$

This condition has a direct interpretation for trajectory planning. The skeleton $Z$ is useful when it explains the strong low-frequency dependence shared by multiple future action tokens, leaving only weak local residual dependence after conditioning. If Z is hard to predict, acts as a downstream collider, or fails to reduce residual dependence, the positive-gain condition may not hold.

## 7.3.4 KL Upper Bound with Model Error and Re-edit Schedule

We finally incorporate token-level model error, initial proposal mismatch, skeleton prediction error, and re-edit scheduling. Let π denote an iterative token-editing schedule with R rounds. At round $r ,$ let A be the active edit set and let $S _ { r }$ denote the editing state before updating the active tokens. The token-level model error is defined as

$$
\delta _ { i , r } ( S _ { r } , Z ) = D _ { \mathrm { K L } } \left( q ( Y _ { i } ^ { ( r ) } \mid S _ { r } ) \parallel p _ { \theta } ( Y _ { i } ^ { ( r ) } \mid S _ { r } ) \right) .\tag{40}
$$

We also define the initial proposal mismatch as

$$
\delta _ { \mathrm { i n i t } } = \mathbb { E } _ { q ( C , Z ) } D _ { \mathrm { K L } } \left( q _ { 0 } ( \mathbf { Y } ^ { ( 0 ) } \mid C , Z ) \| p _ { 0 } ( \mathbf { Y } ^ { ( 0 ) } \mid C , Z ) \right) ,\tag{41}
$$

where $q _ { 0 }$ is the reference initial proposal distribution and $p _ { 0 }$ is the initial proposal distribution used by the model. If both processes start from the same proposal distribution, then $\delta _ { \mathrm { i n i t } } = 0$

For a given skeleton $Z ,$ applying the one-step KL decomposition at each edit round gives

$$
\begin{array} { r l } & { D _ { \mathrm { K L } } \left( q ( \mathbf { Y } ^ { ( R ) } \mid \boldsymbol { C } , \boldsymbol { Z } ) \| p _ { \theta , \pi } ( \mathbf { Y } ^ { ( R ) } \mid \boldsymbol { C } , \boldsymbol { Z } ) \right) } \\ & { \leq \delta _ { \mathrm { i n i t } } + \displaystyle \sum _ { r = 1 } ^ { R } \mathbb { E } \left[ \sum _ { i \in A _ { r } } \delta _ { i , r } ( S _ { r } , \boldsymbol { Z } ) + \mathrm { T C } ( \mathbf { Y } _ { A _ { r } } ^ { ( r ) } \mid S _ { r } , \boldsymbol { Z } ) \right] . } \end{array}\tag{42}
$$

Using the residual mixing bound on each active edit set,

$$
\mathrm { T C } ( \mathbf { Y } _ { A _ { r } } ^ { ( r ) } \mid S _ { r } , Z ) \leq \sum _ { \{ i , j \} \subset A _ { r } } \beta _ { r } \exp \left( - \frac { d _ { r } ( i , j ) } { \ell _ { r } } \right) ,\tag{43}
$$

we obtain

$$
\begin{array} { r l } & { D _ { \mathrm { K L } } \left( q ( \mathbf { Y } ^ { ( R ) } \mid C , Z ) \| p _ { \theta , \pi } ( \mathbf { Y } ^ { ( R ) } \mid C , Z ) \right) } \\ & { \leq \delta _ { \mathrm { i n i t } } + \displaystyle \sum _ { r = 1 } ^ { R } \mathbb { E } \left[ \sum _ { i \in A _ { r } } \delta _ { i , r } ( S _ { r } , Z ) + \sum _ { \{ i , j \} \subset A _ { r } } \beta _ { r } \exp \left( - \frac { d _ { r } ( i , j ) } { \ell _ { r } } \right) \right] . } \end{array}\tag{44}
$$

In our hierarchical policy model, the latent skeleton $Z$ is instantiated as the decision token $\mathbf { D } _ { t }$ and is predicted from the scene context. Therefore, we introduce a skeleton prediction error to measure the mismatch between the target skeleton distribution and the model-predicted skeleton distribution:

$$
\delta _ { Z } = D _ { \mathrm { K L } } \left( q ( Z \mid C ) \| p _ { \psi } ( Z \mid C ) \right) .\tag{45}
$$

The full KL upper bound is then

$$
D _ { \mathrm { K L } } \left( q ( \mathbf { Y } \mid C ) \lVert p _ { \psi , \theta , \pi } ( \mathbf { Y } \mid C ) \right) \leq \delta _ { Z } + \Lambda _ { z } ( \pi ) ,\tag{46}
$$

where

$$
\Lambda _ { z } ( \pi ) = \delta _ { \mathrm { i n i t } } + \sum _ { r = 1 } ^ { R } \mathbb { E } \left[ \sum _ { i \in A _ { r } } \delta _ { i , r } ( S _ { r } , Z ) + \sum _ { \lbrace i , j \rbrace \subset A _ { r } } \beta _ { r } \exp \left( - \frac { d _ { r } ( i , j ) } { \ell _ { r } } \right) \right] .\tag{47}
$$

Equivalently, define

$$
\mathcal { B } _ { \mathrm { m o d e l } } ( \pi ) = \sum _ { r = 1 } ^ { R } \mathbb { E } \left[ \sum _ { i \in A _ { r } } \delta _ { i , r } ( S _ { r } , Z ) \right] ,\tag{48}
$$

and

$$
\mathcal { U } _ { \mathrm { d e p } } ( \pi ) = \sum _ { r = 1 } ^ { R } \mathbb { E } \left[ \sum _ { \substack { \{ i , j \} \subset A _ { r } } } \beta _ { r } \exp \left( - \frac { d _ { r } ( i , j ) } { \ell _ { r } } \right) \right] .\tag{49}
$$

Then

$$
D _ { \mathrm { K L } } \left( q ( { \mathbf { Y } } \mid C ) \| p _ { \psi , \theta , \pi } ( { \mathbf { Y } } \mid C ) \right) \leq \delta _ { Z } + \delta _ { \mathrm { i n i t } } + B _ { \mathrm { m o d e l } } ( \pi ) + \mathcal { U } _ { \mathrm { d e p } } ( \pi ) .\tag{50}
$$

This bound shows that the latent skeleton improves the overall generation risk only when its prediction cost is small and the reduction in residual dependence outweighs the additional skeleton prediction error.

Implication for policy modeling. In our policy modeling task, the decision token $\mathbf { D } _ { t }$ plays the role of the latent skeleton Z. A valid decision token should represent upstream low-frequency planning structure, such as maneuver intent, coarse reference motion, target lane, or speed trend, rather than a downstream trajectory-quality label computed from the final action sequence. Under this interpretation, $\mathbf { D } _ { t }$ explains global multi-modal driving choices before fine action-token editing, while the remaining action tokens mainly model local residual corrections. Therefore, the hierarchical factorization

$$
\begin{array} { r } { p _ { \psi , \theta } ( \mathbf { A } _ { t + 1 : t + H } , \mathbf { D } _ { t } \mid \mathbf { C } _ { t } ) = p _ { \psi } ( \mathbf { D } _ { t } \mid \mathbf { C } _ { t } ) p _ { \theta } ( \mathbf { A } _ { t + 1 : t + H } \mid \mathbf { C } _ { t } , \mathbf { D } _ { t } ) } \end{array}
$$

is theoretically justified when $\mathbf { D } _ { t }$ reduces residual action-token dependence enough to ofset its own prediction error.

## 7.3.5 Exact Reconstruction under Soft-label Interpolation

We show that the proposed soft-label action representation removes the deterministic hard-quantization error within each acceleration grid cell. Let the acceleration vocabulary be defined by the Cartesian product of the bin centers along the longitudinal and lateral acceleration dimensions. Denote the bin centers of $a _ { x }$ by $\{ c _ { i } ^ { x } \} _ { i = 1 } ^ { N _ { x } }$ and the bin centers of $a _ { y }$ by $\{ c _ { j } ^ { y } \} _ { j = 1 } ^ { N _ { y } }$ . Consider a continuous acceleration vector $\mathbf { a } = ( a _ { x } , a _ { y } )$ that lies in the grid cell spanned by four neighboring prototypes:

$$
\begin{array} { r l r } & { } & { \mathbf { v } _ { i j } = ( c _ { i } ^ { x } , c _ { j } ^ { y } ) , \quad \quad \mathbf { v } _ { i + 1 , j } = ( c _ { i + 1 } ^ { x } , c _ { j } ^ { y } ) , } \\ & { } & { \mathbf { v } _ { i , j + 1 } = ( c _ { i } ^ { x } , c _ { j + 1 } ^ { y } ) , \mathbf { v } _ { i + 1 , j + 1 } = ( c _ { i + 1 } ^ { x } , c _ { j + 1 } ^ { y } ) . } \end{array}\tag{51}
$$

That is,

$$
a _ { x } \in [ c _ { i } ^ { x } , c _ { i + 1 } ^ { x } ] , \qquad a _ { y } \in [ c _ { j } ^ { y } , c _ { j + 1 } ^ { y } ] .\tag{52}
$$

We define the interpolation coeficients

$$
\lambda _ { x } = { \frac { a _ { x } - c _ { i } ^ { x } } { c _ { i + 1 } ^ { x } - c _ { i } ^ { x } } } , \qquad \lambda _ { y } = { \frac { a _ { y } - c _ { j } ^ { y } } { c _ { j + 1 } ^ { y } - c _ { j } ^ { y } } } .\tag{53}
$$

The soft target distribution $p ^ { * } ( \cdot \mid \mathbf { a } )$ is nonzero only on the four neighboring prototypes, with weights

$$
\begin{array} { c } { p _ { i j } ^ { * } = ( 1 - \lambda _ { x } ) ( 1 - \lambda _ { y } ) , } \\ { p _ { i + 1 , j } ^ { * } = \lambda _ { x } ( 1 - \lambda _ { y } ) , } \\ { p _ { i , j + 1 } ^ { * } = ( 1 - \lambda _ { x } ) \lambda _ { y } , } \\ { p _ { i + 1 , j + 1 } ^ { * } = \lambda _ { x } \lambda _ { y } . } \end{array}\tag{54}
$$

These weights are non-negative and sum to one. The acceleration reconstructed from the soft target is

$$
\bar { \mathbf { a } } = \sum _ { m \in \{ i , i + 1 \} } \sum _ { n \in \{ j , j + 1 \} } p _ { m n } ^ { * } \mathbf { v } _ { m n } .\tag{55}
$$

For the longitudinal component, we have

$$
\bar { a } _ { x } = p _ { i j } ^ { * } c _ { i } ^ { x } + p _ { i + 1 , j } ^ { * } c _ { i + 1 } ^ { x } + p _ { i , j + 1 } ^ { * } c _ { i } ^ { x } + p _ { i + 1 , j + 1 } ^ { * } c _ { i + 1 } ^ { x } .\tag{56}
$$

Substituting the interpolation weights gives

$$
\begin{array} { r } { \bar { a } _ { x } = ( 1 - \lambda _ { x } ) c _ { i } ^ { x } + \lambda _ { x } c _ { i + 1 } ^ { x } = a _ { x } . } \end{array}\tag{57}
$$

Similarly, for the lateral component,

$$
\begin{array} { r } { \bar { a } _ { y } = ( 1 - \lambda _ { y } ) c _ { j } ^ { y } + \lambda _ { y } c _ { j + 1 } ^ { y } = a _ { y } . } \end{array}\tag{58}
$$

Therefore,

$$
{ \bar { \mathbf { a } } } = \mathbf { a } .\tag{59}
$$

During training, the action head predicts a distribution $q _ { \theta } ( \cdot \mid C _ { t } )$ over the acceleration vocabulary and is optimized using soft-label cross-entropy:

$$
\mathcal { L } _ { a } ^ { \mathrm { c l s } } = - \sum _ { k = 1 } ^ { N _ { x } N _ { y } } p _ { k } ^ { * } ( \mathbf { a } ) \log q _ { \theta , k } ( C _ { t } ) .\tag{60}
$$

Since

$$
\begin{array} { r } { \mathcal { L } _ { a } ^ { \mathrm { c l s } } = H ( p ^ { * } ) + \mathrm { K L } ( p ^ { * } \| q _ { \theta } ) , } \end{array}\tag{61}
$$

the ideal optimum under suficient model capacity and optimization satisfies

$$
q _ { \theta } ( \cdot \mid C _ { t } ) = p ^ { * } ( \cdot \mid \mathbf { a } ) .\tag{62}
$$

At inference time, if the continuous acceleration is decoded by the vocabulary expectation

$$
\hat { \mathbf { a } } = \sum _ { k = 1 } ^ { N _ { x } N _ { y } } q _ { \theta , k } ( C _ { t } ) \mathbf { v } _ { k } ,\tag{63}
$$

then under the ideal prediction condition $q _ { \theta } = p ^ { * }$ , we obtain

$$
\hat { \mathbf { a } } = \sum _ { k = 1 } ^ { N _ { x } N _ { y } } p _ { k } ^ { * } ( \mathbf { a } ) \mathbf { v } _ { k } = \mathbf { a } .\tag{64}
$$

Thus, under exact recovery of the soft target distribution, the proposed soft-label interpolation yields zero deterministic quantization error within the acceleration grid cell.

## 7.3.6 Consistency Bound for Continuous Motion Supervision

Acceleration error under distribution prediction mismatch. We next characterize the remaining reconstruction error when the predicted action distribution does not exactly match the soft target distribution. Let $p ^ { * } ( \cdot \mid \mathbf { a } )$ denote the interpolation target distribution for the continuous acceleration a, and let $q _ { \theta } ( \cdot \mid C _ { t } )$ denote the predicted action distribution. The decoded continuous acceleration is

$$
\hat { \mathbf { a } } = \sum _ { k = 1 } ^ { N _ { x } N _ { y } } q _ { \theta , k } ( C _ { t } ) \mathbf { v } _ { k } .\tag{65}
$$

Since the soft target distribution exactly reconstructs a under grid interpolation,

$$
\mathbf { a } = \sum _ { k = 1 } ^ { N _ { x } N _ { y } } p _ { k } ^ { * } ( \mathbf { a } ) \mathbf { v } _ { k } .\tag{66}
$$

Therefore, the acceleration reconstruction error can be written as

$$
\hat { \mathbf { a } } - \mathbf { a } = \sum _ { k = 1 } ^ { N _ { x } N _ { y } } \left( q _ { \theta , k } ( C _ { t } ) - p _ { k } ^ { * } ( \mathbf { a } ) \right) \mathbf { v } _ { k } .\tag{67}
$$

Assume the acceleration vocabulary is bounded by

$$
\begin{array} { r } { \| \mathbf { v } _ { k } \| _ { 2 } \leq V _ { \operatorname* { m a x } } , \qquad \forall k \in \{ 1 , \dots , N _ { x } N _ { y } \} . } \end{array}\tag{68}
$$

Then, by the triangle inequality,

$$
\| \widehat { \mathbf { a } } - \mathbf { a } \| _ { 2 } \leq \sum _ { k = 1 } ^ { N _ { x } N _ { y } } \vert q _ { \theta , k } ( C _ { t } ) - p _ { k } ^ { * } ( \mathbf { a } ) \vert \| \mathbf { v } _ { k } \| _ { 2 } .\tag{69}
$$

Using the boundedness of the vocabulary prototypes, we obtain

$$
\| \widehat { \mathbf { a } } - \mathbf { a } \| _ { 2 } \leq V _ { \operatorname* { m a x } } \| q _ { \theta } ( \cdot  { | } \mathbf {  { C } } _ { t } ) - p ^ { * } ( \cdot  { | } \mathbf {  { a } } ) \| _ { 1 } .\tag{70}
$$

By Pinsker’s inequality,

$$
\| q _ { \theta } ( \cdot  { | } C _ { t } ) - p ^ { * } ( \cdot  { | } \mathbf { \delta } \mathbf { a } ) \| _ { 1 } \le \sqrt { 2 \mathrm { K L } \left( p ^ { * } ( \cdot  { | } \mathbf { \delta } \mathbf { a } ) \| q _ { \theta } ( \cdot  { | } C _ { t } ) \right) } .\tag{71}
$$

Therefore,

$$
\| \hat { \mathbf { a } } - \mathbf { a } \| _ { 2 } \leq V _ { \operatorname* { m a x } } \sqrt { 2 \mathrm { K L } \left( p ^ { * } ( \cdot \mid \mathbf { a } ) \| q _ { \theta } ( \cdot \mid C _ { t } ) \right) } .\tag{72}
$$

Since the soft-label cross-entropy satisfies

$$
\mathcal { L } _ { a } ^ { \mathrm { c l s } } = H ( p ^ { * } ) + \mathrm { K L } \left( p ^ { * } ( \cdot \mid \mathbf { a } ) \Vert q _ { \theta } ( \cdot \mid C _ { t } ) \right) ,\tag{73}
$$

we further have

$$
\| \hat { \mathbf { a } } - \mathbf { a } \| _ { 2 } \leq V _ { \operatorname* { m a x } } \sqrt { 2 \left( \mathcal { L } _ { a } ^ { \mathrm { c l s } } - H ( p ^ { * } ) \right) } .\tag{74}
$$

This shows that, after replacing hard one-hot quantization with soft-label interpolation, the remaining acceleration reconstruction error is controlled by the distribution prediction error rather than by deterministic nearest-bin quantization error.

Mode-aware decoding for continuous motion supervision. The soft-label interpolation analysis above concerns the construction of the action-token target distribution and the deterministic error introduced by hard quantization. In contrast, the mode-aware decoding strategy is used for a diferent purpose: it converts the predicted categorical action distribution into a continuous acceleration for the auxiliary continuous motion losses. Its goal is not to preserve the full-distribution expectation, but to avoid averaging incompatible action modes.

Let $q _ { \theta } ( \cdot \mid C _ { t } )$ denote the predicted categorical distribution over the acceleration vocabulary $\{ \mathbf { v } _ { k } \} _ { k = 1 } ^ { K }$ . Fulldistribution expectation decoding gives

$$
\bar { \mathbf { a } } = \sum _ { k = 1 } ^ { K } q _ { \theta , k } ( C _ { t } ) \mathbf { v } _ { k } .\tag{75}
$$

When $q _ { \theta }$ is multi-modal, a¯ can lie between several plausible modes and may not correspond to any physically meaningful driving behavior. To avoid this decoding-induced mode averaging, we fit $q _ { \theta }$ with a Gaussian mixture over the acceleration vocabulary, select one mode support $S _ { m ^ { \star } }$ , and form the normalized local distribution

$$
\tilde { q } _ { \theta , k } ( C _ { t } ) = \frac { q _ { \theta , k } ( C _ { t } ) \mathbf { 1 } [ k \in \cal S _ { m ^ { \star } } ] } { \sum _ { \ell \in \cal S _ { m ^ { \star } } } q _ { \theta , \ell } ( C _ { t } ) } .\tag{76}
$$

The mode-aware decoded acceleration is then

$$
\widehat { \mathbf { a } } _ { \mathrm { m o d e } } = \sum _ { k = 1 } ^ { K } \widetilde { q } _ { \theta , k } ( C _ { t } ) \mathbf { v } _ { k } .\tag{77}
$$

This operation intentionally replaces the full predicted distribution $q _ { \theta }$ with a mode-conditioned local distribution $\tilde { q } _ { \theta }$ . Therefore, it introduces a mode-selection approximation while avoiding the mode-averaging efect of full-distribution expectation decoding. Let $p ^ { * } ( \cdot \mid \mathbf { a } )$ denote the soft interpolation target of the ground-truth acceleration. The reconstruction error of mode-aware decoding can be decomposed as

$$
\begin{array} { l } { { \displaystyle \hat { \bf a } _ { \mathrm { m o d e } } - { \bf a } = \sum _ { k = 1 } ^ { K } \left( \tilde { q } _ { \boldsymbol { \theta } , \boldsymbol { k } } ( C _ { t } ) - p _ { k } ^ { * } ( { \bf a } ) \right) { \bf v } _ { k } } \ ~ } \\ { { \displaystyle ~ = \sum _ { k = 1 } ^ { K } \left( q _ { \boldsymbol { \theta } , k } ( C _ { t } ) - p _ { k } ^ { * } ( { \bf a } ) \right) { \bf v } _ { k } + \sum _ { k = 1 } ^ { K } \left( \tilde { q } _ { \boldsymbol { \theta } , k } ( C _ { t } ) - q _ { \boldsymbol { \theta } , k } ( C _ { t } ) \right) { \bf v } _ { k } } . } \end{array}\tag{78}
$$

The first term corresponds to the distribution prediction error with respect to the soft-label target, while the second term corresponds to the additional mode-selection error introduced by replacing $q _ { \theta }$ with $\tilde { q } _ { \theta }$ . Assuming $\| \mathbf { v } _ { k } \| _ { 2 } \leq V _ { \operatorname* { m a x } }$ for all vocabulary prototypes, we obtain

$$
\begin{array} { r l } & { \| \widehat { \mathbf { a } } _ { \mathrm { m o d e } } - \mathbf { a } \| _ { 2 } \leq V _ { \operatorname* { m a x } } \| q _ { \theta } ( \cdot  { | } \mathbf {  { C } } _ { t } ) - p ^ { * } ( \cdot  { | } \mathbf {  { a } } ) \| _ { 1 } } \\ & { \phantom { \quad \quad \quad } + V _ { \operatorname* { m a x } } \| \widetilde { q } _ { \theta } ( \cdot  { | } \mathbf {  { C } } _ { t } ) - q _ { \theta } ( \cdot  { | } \mathbf {  { C } } _ { t } ) \| _ { 1 } . } \end{array}\tag{79}
$$

Using Pinsker’s inequality for the first term gives

$$
\begin{array} { r } { \| \widehat { \mathbf { a } } _ { \mathrm { m o d e } } - \mathbf { a } \| _ { 2 } \leq V _ { \operatorname* { m a x } } \sqrt { 2 \mathrm { K L } \big ( p ^ { * } ( \cdot \mid \mathbf { a } ) \| q _ { \theta } ( \cdot \mid C _ { t } ) \big ) } } \\ { + V _ { \operatorname* { m a x } } \| \widetilde { q } _ { \theta } ( \cdot \mid C _ { t } ) - q _ { \theta } ( \cdot \mid C _ { t } ) \| _ { 1 } . } \end{array}\tag{80}
$$

This bound separates the error caused by imperfect distribution prediction from the error introduced by mode selection. In practice, the mode-aware decoding is used only for continuous acceleration and trajectory regression losses. It prevents the regression loss from forcing a multi-modal categorical prediction into its global mean, thereby reducing mode collapse while preserving the discrete action distribution for token-level policy prediction.

The first term is the prediction mismatch of the original categorical action distribution, while the second term is the approximation introduced by mode selection and re-normalization. If the acceleration vocabulary is bounded by $\| \mathbf { v } _ { k } \| _ { 2 } \leq V _ { \operatorname* { m a x } }$ , then

$$
\lVert \widehat { \mathbf { a } } _ { \mathrm { m o d e } } - \mathbf { a } \rVert _ { 2 } \leq V _ { \mathrm { m a x } } \lVert q _ { \theta } ( \cdot \mid C _ { t } ) - p ^ { * } ( \cdot \mid \mathbf { a } ) \rVert _ { 1 } + V _ { \mathrm { m a x } } \lVert \widetilde { q } _ { \theta } ( \cdot \mid C _ { t } ) - q _ { \theta } ( \cdot \mid C _ { t } ) \rVert _ { 1 } .
$$

Using Pinsker’s inequality for the first term gives

$$
\lVert \widehat { \mathbf { a } } _ { \mathrm { m o d e } } - \mathbf { a } \rVert _ { 2 } \leq V _ { \mathrm { m a x } } \sqrt { 2 \mathrm { K L } ( p ^ { * } ( \cdot  { | \mathbf { \Delta } | } \Vert q _ { \theta } ( \cdot  { | \mathbf { \Delta } C _ { t } ) } ) + V _ { \mathrm { m a x } } \Vert \widetilde { q } _ { \theta } ( \cdot  { | \mathbf { \Delta } C _ { t } ) } - q _ { \theta } ( \cdot  { | \mathbf { \Delta } C _ { t } ) } \Vert _ { 1 } .  }
$$

Implication for proposed supervision. This bound separates the original distribution prediction error from the additional mode-selection approximation. Unlike the soft-label interpolation result, mode-aware decoding is not claimed to be error-free. Instead, it trades the unbiased full-distribution expectation for a mode-conditioned acceleration that is more physically consistent for multi-modal action prediction.

## 7.4 Additional Qualitative Results

Planning. We further visualize the iterative scheduling process of policy-token decoding. Specifically, Discrete-WAM is further evaluated on navhard, a curated subset of navtest consisting of challenging and safety-critical driving scenarios, as shown in Fig. 12. The qualitative results show that selective re-editing gradually reduces the uncertainty of the predicted action distribution across scheduling rounds. At early rounds, high-entropy tokens often appear around decision-sensitive or dynamically constrained segments, where multiple future actions may still be plausible. As scheduling proceeds, the entropy of these tokens decreases, indicating that the model progressively resolves ambiguous action choices and converges to a more stable policy.

Importantly, the entropy reduction is not achieved by blindly overwriting the entire action sequence. Instead, the scheduler selectively updates tokens that remain uncertain or distributionally unstable, while preserving tokens that have already become confident. This behavior is consistent with the quantitative results in Sec. 4.3: selective replacement improves with additional rounds, whereas full replacement may perturb stable tokens and degrade long-horizon trajectory accuracy. The visualization therefore provides qualitative evidence that the proposed scheduling strategy performs uncertainty-aware iterative refinement rather than repeated full-sequence resampling.

World modeling. Figure 13 presents additional qualitative world-generation examples across a diverse set of urban driving scenarios. Given two historical frames and the current observation, Discrete-WAM generates future visual observations over multiple prediction horizons. Across intersections, urban roads, highway ramps, underpasses, and open-road environments, the generated futures remain temporally coherent and geometrically consistent with the underlying scene structure. In particular, Discrete-WAM accurately preserves static elements such as road boundaries, lane layouts, buildings, and trafic infrastructure, while simultaneously modeling the motion of surrounding vehicles and the ego-induced viewpoint changes.

![](images/cf465c1d1cba2a1aa1500a9fbafd5b84082a9f86e3ccf3b5f531dbaf97f80084.jpg)  
Figure 12 Additional planning results in navhard subset. Discrete-WAM consistently handles complex interactions, road geometries, and hazard situations, producing safe and goal-directed behaviors across diverse environments.

Counterfactual inference. Fig. 14 presents additional counterfactual evaluations under diverse hazard scenarios by progressively increasing the magnitude of lateral action perturbations. Across all examples, the surprise metric exhibits a clear monotonic relationship with the severity of counterfactual interventions. When the perturbation remains small and the generated future is still physically plausible, the surprise value stays low and the planning score remains largely unafected. As the counterfactual action increasingly deviates from the factual behavior, the generated future begins to violate scene constraints, leading to of-road behaviors, unsafe interactions, or imminent collisions. Correspondingly, the surprise value rises substantially while the PDM score drops sharply. We further observe that the pixel-level reconstruction error (L1) increases much more gradually than surprise, suggesting that surprise captures semantically meaningful deviations beyond low-level appearance diferences. This consistent trend across multiple scenes indicates that the world model has learned action-conditioned causal dynamics rather than merely modeling visual statistics. The strong negative correlation between surprise and planning quality demonstrates that surprise can serve as an efective indicator of causal inconsistency and unsafe future outcomes in generated driving scenarios. Further generation results are provided in Fig. 15.

![](images/8ded238c4a89c70a86230f319cc215167532415fc1931a25264894737f5eb196.jpg)  
Figure 13 Additional world model generation results.

Attention map visualization. We provide additional attention map visualizations to complement the analysis in the main text. These examples include averaged policy attention maps across camera views, layer-wise front-view attention maps, and upper-region ablation results. They are intended to show that the observed attention patterns, including attention to driving-relevant semantics and stable activation in upper image regions, are not limited to a single example.

![](images/4de3f3ad3ff06681544cf387e8f6789593f28693fe467415b5b5c950eef1fe48.jpg)  
Figure 14 Additional counterfactual result with surprise metric. We compare surprise value S by both factual and counterfactual world-model generations by larger sweep of lateral counterfactual actions under havhard subset. A clear correlation persists of Discrete-WAM with causal understanding.

![](images/8b8ff899435313e9758d36052a483813812e176c433103d244241e46610d45ed.jpg)  
Figure 15 Additional world model counterfactual prediction results.

![](images/a3c527c1e671aec17f5b47061aadf89efc8af375020ce7cf280dd06ac08e939a.jpg)  
Figure 16 Additional averaged policy attention maps. Supplementary examples of policy attention averaged over Transformer layers, attention heads, and policy action queries from the first editing round. The three panels in each example correspond to the left-view, front-view, and right-view cameras.

![](images/df61e2b861552713b7e53a93b67edca7bf63c57e333a05134f8a12cc980e6688.jpg)  
Figure 17 Additional layer-wise policy attention maps. Supplementary front-view examples of layer-wise policy attention. Layers 0, 6, 12, and 17 are visualized by averaging over attention heads and policy queries.

![](images/6cf9745a53c857ccd01e43f56046bc2641b4a52b018289e85484944fa3847e5b.jpg)  
Figure 18 Additional upper-region ablation examples. Supplementary front-view examples comparing the original image, the upper-masked setting, and the upper-only setting. These examples provide additional qualitative evidence for the attention redistribution behavior discussed in the main text.