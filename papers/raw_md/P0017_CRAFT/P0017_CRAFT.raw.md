# CRAFT: Counterfactual-to-Interactive Reinforcement Fine-Tuning for Driving Policies

Keyu Chen<sup>1</sup> Nanfei Ye<sup>2</sup> Yida Wang<sup>2</sup> Wenchao Sun<sup>1</sup> Danqi Zhao<sup>1</sup> Hao Cheng<sup>1</sup> Sifa Zheng<sup>1</sup>

<sup>1</sup> School of Vehicle and Mobility, Tsinghua University <sup>2</sup> Li Auto Inc

Abstract: Open-loop imitation learning has advanced modern autonomous driving policy architectures, but closed-loop deployment remains vulnerable to policyinduced distribution shift. Existing post-training paradigms exhibit fundamental trade-offs: closed-loop RL fine-tuning provides grounded feedback from executed actions but is constrained by the sparsity of informative events, whereas counterfactual fine-tuning provides dense supervision over candidate futures but inherits bias from imperfect future estimates. We introduce Counterfactual-to-Interactive Reinforcement Fine-Tuning (CRAFT), an on-policy framework that formulates closed-loop post-training as proxy-residual optimization. CRAFT uses group-normalized counterfactual advantages as a dense proxy for real closed-loop advantages and aligns this proxy with the closed-loop world through grounded residual correction from interaction-critical events. To stabilize adaptation, CRAFT regularizes the online policy toward an EMA teacher via asymmetric KL selfdistillation. Theoretically, CRAFT decomposes the real closed-loop policy gradient into proxy and residual terms under the same visited-state distribution, reducing residual variance with an aligned proxy while mitigating proxy bias through grounded residual approximation. Empirically, CRAFT achieves the strongest closed-loop gains on Bench2Drive across hierarchical planning, vision-languageaction, and vocabulary-scoring architectures. Ablations, scaling behavior, stability analyses, and transfer results further validate the complementary roles of dense counterfactual proxy and grounded residual correction. Project page: https://currychen77.github.io/CRAFT.

## 1 Introduction

Modern autonomous driving policies have rapidly evolved beyond modular perception–planning pipelines. Representative frameworks include unified end-to-end models [1, 2, 3], vision-languageaction models [4, 5], and world action models [6, 7]. While these architectures expand the capability of driving policies, their training remains largely governed by an open-loop imitation learning (IL) paradigm. This paradigm often leads to distribution shift due to the inherent discrepancy between open-loop training and closed-loop deployment. Therefore, further improving the closed-loop performance of pre-trained driving policies remains critical for safe and reliable deployment.

To address the challenges of distribution shift, two distinct post-training paradigms have emerged. As illustrated in Figure 1, closed-loop RL fine-tunes pre-trained driving policies within interactive simulators to obtain grounded feedback from executed actions. However, the inherent sparsity of informative events across diverse scenarios often constrains the training efficiency of pure closed-loop RL. Conversely, counterfactual fine-tuning offers an alternative by evaluating multiple candidate futures from the same visited state, transforming these relative performance differences into dense supervisory signals through group-relative objectives, such as GRPO [8]. Nevertheless, counterfactual estimates of the future remain inherently biased, as the counterfactual world cannot faithfully capture the interaction dynamics of the real closed-loop world.

The complementary strengths of these two paradigms motivate a natural question: can counterfactual supervision serve as a dense proxy, while closed-loop interaction corrects its residual mismatch with the real closed-loop world? CRAFT addresses this question by assigning distinct optimization roles to the two signals. Counterfactual supervision serves as a dense proxy over states visited by the current policy, whereas closed-loop interaction provides grounded residual correction to align this proxy with the real closed-loop world.

![](images/ecea926332f569bd040f6b62c728ebde5ce08b8b0de1999f71cfc542bb6485d7.jpg)  
Figure 1: Two existing post-training paradigms exhibit complementary trade-offs. Closed-loop RL fine-tuning provides grounded but sparse feedback from executed actions, whereas counterfactual fine-tuning provides dense supervision from biased future estimates. CRAFT combines their complementary strengths through a dense counterfactual proxy and grounded residual correction.

Building on this proxy-residual decomposition, we introduce Counterfactual-to-Interactive Reinforcement Fine-Tuning (CRAFT), an on-policy post-training framework for pre-trained driving policies. As illustrated in Figure 1, CRAFT uses the counterfactual world to evaluate groups of candidates from states visited by the online policy and converts their efficiency, safety, and rule-compliance returns into group-normalized counterfactual advantages. These advantages serve as a dense proxy for real closed-loop advantages. CRAFT then derives grounded residual correction from interaction-critical traffic events observed in executed closed-loop rollouts, aligning the proxy with the real closed-loop world through a value-free dual-clipped update [9, 10]. To stabilize adaptation, asymmetric-KL self-distillation regularizes the online policy toward an EMA teacher initialized from the pre-trained policy, preserving reliable behaviors while allowing interaction-driven correction.

Theoretically, CRAFT decomposes the real closed-loop policy gradient into proxy and residual terms under the same state distribution, reducing residual variance with an aligned proxy while mitigating proxy bias through grounded residual approximation. Dual clipping further keeps rare critical events informative without dominating the update. Empirically, CRAFT achieves the largest closed-loop gains on Bench2Drive across policy architectures, including hierarchical planning, vision-languageaction, and vocabulary-scoring. Ablations verify the complementary roles of each component, with the counterfactual proxy providing broad optimization signals, grounded residual correction delivering substantial closed-loop gains on interaction-sensitive metrics, and self-distillation stabilizing adaptation around reliable pre-trained behavior. Scaling and stability analyses further demonstrate that, with increasing fine-tuning data, CRAFT delivers more consistent gains and better training stability than baselines, while transfer results indicate partial robustness beyond the training distribution. Our main contributions are summarized as follows:

• We formulate closed-loop post-training for pre-trained driving policies through a proxy-residual gradient decomposition, revealing the trade-off between dense but biased counterfactual supervision and sparse but grounded closed-loop interaction under the same visited-state distribution.

• We propose CRAFT, an on-policy post-training framework that turns counterfactual supervision into a dense proxy for real closed-loop advantages and uses interaction-critical closed-loop events as grounded residual correction, stabilized by self-distillation from the pre-trained policy.

• We substantiate the proxy-residual design theoretically and empirically. CRAFT reduces residual variance with an aligned proxy while mitigating proxy bias through grounded residual approxima tion, and achieves consistent closed-loop gains on Bench2Drive across diverse policy architectures, including hierarchical planning, vision-language-action, and vocabulary-scoring.

## 2 Related Work

End-to-End Autonomous Driving Policy. Progress in end-to-end driving has been driven largely by advances in model architecture. Diffusion-based models [11, 12, 13, 14], vision-language-action models [15, 16, 17, 18], and trajectory-vocabulary scoring methods [19, 20, 21, 22] all improve policy expressiveness. Yet their training remains largely imitation-based, with policies trained near expert states and then expected to remain reliable after their own actions shift future observations. This assumption is especially fragile in closed-loop deployment, where small planning errors can move the ego vehicle outside the training distribution.

Closed-Loop RL in Autonomous Driving. Closed-loop RL mitigates distribution shift by optimizing policies on executed rollouts, often with policy-gradient methods such as PPO [23] in CARLA [24, 25] or reconstructed simulators [26, 27, 28]. While grounded in real interaction, these methods remain sample-inefficient because informative events are rare, requiring extensive rollouts to obtain useful gradient estimates. Recent approaches improve efficiency through VLM-based reward densification [29] or world-model rollouts [30, 31], but their supervision depends on evaluator or model fidelity. CRAFT instead uses closed-loop interaction only to correct a dense counterfactual proxy, preserving grounded feedback without estimating full advantages from sparse rollouts.

Counterfactual Post-Training in Autonomous Driving. Counterfactual post-training improves learning efficiency through dense local comparisons on real visited states [32], making preferencebased and group-relative objectives attractive [8, 33]. Recent methods combine PDM Score [34, 35, 36, 37, 38, 39] with GRPO in NAVSIM [40] for policy fine-tuning, or use synthetic counterfactual data [41, 42] for offline post-training. A key limitation lies in the rollout condition, since counterfac tual futures generated offline or in a non-reactive simulator do not capture true closed-loop interaction with the environment. CRAFT uses counterfactual futures as a dense proxy on real visited states, while grounded residual correction refines the proxy with feedback from true closed-loop rollouts.

## 3 Methodology

CRAFT is a general paradigm for closed-loop post-training of supervised driving policies. The target is to improve closed-loop performance under the on-policy state distribution. Existing post-training paradigms present a fundamental trade-off: closed-loop RL is physically grounded but relies on sparse, high-variance interaction feedback, whereas counterfactual optimization provides dense supervision but suffers from biased future estimates. CRAFT addresses this trade-off with two complementary components: a dense counterfactual proxy that provides trajectory-level supervision via candidate evaluation, and a grounded residual correction that compensates for proxy bias using executed closed-loop feedback. To preserve pre-trained behavior during fine-tuning, CRAFT further applies on-policy self-distillation with an EMA teacher. The framework is illustrated in Figure 2.

## 3.1 Real Closed-Loop Objective and Proxy–Residual Decomposition

We first formalize the real closed-loop objective that CRAFT aims to improve. We then show that CRAFT optimizes it through two complementary terms defined on the same on-policy state distribution. The key idea is to use dense counterfactual supervision as a proxy for the full closed-loop learning signal, while using grounded interaction feedback to correct the residual mismatch.

Let $\mathcal { M } _ { \mathrm { r e a l } } = ( \mathcal { S } , \mathcal { A } , P _ { \mathrm { r e a l } } , r _ { \mathrm { r e a l } } , \gamma )$ denote the real closed-loop MDP, with state space $s ,$ , low-level action space A, transition function $P _ { \mathrm { r e a l } }$ , reward function $r _ { \mathrm { r e a l } }$ , and discount factor $\gamma \in ( 0 , 1 )$ . The policy scores candidate trajectories $\tau \in \mathcal { T }$ by $\pi _ { \boldsymbol { \theta } } ( \tau \mid s )$ , and the controller κ tracks the selected trajectory $\tau _ { t }$ by executing $a _ { t } = \kappa ( s _ { t } , \tau _ { t } )$ , with rewards evaluated after the induced controller action. Let $d _ { \mathrm { r e a l } } ^ { \pi _ { \theta } }$ be the discounted state-visitation measure. For closed-loop rollout $\xi ,$ , the objective is

$$
J _ { \mathrm { r e a l } } ( \pi _ { \theta } ) = \mathbb { E } _ { \xi \sim ( \pi _ { \theta } , \kappa , P _ { \mathrm { r e a l } } ) } \Big [ \sum _ { t = 0 } ^ { \infty } \gamma ^ { t } r _ { \mathrm { r e a l } } ( s _ { t } , a _ { t } , s _ { t + 1 } ) \Big ] ,\tag{1}
$$

whose policy gradient is

$$
\begin{array} { r } { \nabla _ { \theta } J _ { \mathrm { r e a l } } ( \pi _ { \theta } ) = \mathbb { E } _ { s \sim d _ { \mathrm { r e a l } } ^ { \pi _ { \theta } } , \tau \sim \pi _ { \theta } ( \cdot | s ) } \Big [ \nabla _ { \theta } \log \pi _ { \theta } ( \tau \mid s ) A _ { \pi _ { \theta } } ^ { \mathrm { r e a l } } ( s , \tau ) \Big ] . } \end{array}\tag{2}
$$

![](images/07795ad433f9e2bf60418a1629852e2acfded6ff5dfeee65631c25858dca507e.jpg)  
Figure 2: CRAFT combines dense counterfactual proxy supervision, grounded residual correction from real closed-loop interaction, and on-policy self-distillation toward reliable pre-trained behavior.

Here $A _ { \pi _ { \theta } } ^ { \mathrm { r e a l } } ( s , \tau )$ denotes the real advantage of selecting τ and executing its induced controller action a. Grounded rollouts alone are sample-inefficient because rare critical events provide weak learning signal for most visited states, while the resulting failures dominate return variance. Consequently, value estimation is brittle and value-free optimization suffers from high-variance updates.

CRAFT introduces a dense counterfactual proxy on real visited states. For each $s \sim d _ { \mathrm { r e a l } } ^ { \pi _ { \theta } } $ the counterfactual world assigns each candidate trajectory τ a proxy value $\Phi _ { \pi _ { \theta } } ( s , \tau )$ , such as a shorthorizon rollout score or a group-relative preference. $\operatorname { A s } \Phi _ { \pi _ { \theta } }$ only approximates the real advantage, its residual mismatch is $\Delta _ { \pi _ { \theta } } ( s , \tau ) \triangleq A _ { \pi _ { \theta } } ^ { \mathrm { r e a l } } ( s , \tau ) - \Phi _ { \pi _ { \theta } } ( s , \tau )$

Proposition 3.1 (Exact Counterfactual-Residual Decomposition). For any integrable dense counterfactual proxy $\Phi _ { \pi _ { \theta } } ( s , \tau )$ defined on real visited states, the closed-loop gradient decomposes as

$$
\nabla _ { \theta } J _ { \mathrm { r e a l } } ( \pi _ { \theta } ) = \mathbb { E } \Bigl [ \nabla _ { \theta } \log \pi _ { \theta } ( \tau \mid s ) \Phi _ { \pi _ { \theta } } ( s , \tau ) \Bigr ] + \mathbb { E } \Bigl [ \nabla _ { \theta } \log \pi _ { \theta } ( \tau \mid s ) \Delta _ { \pi _ { \theta } } ( s , \tau ) \Bigr ] ,\tag{3}
$$

where both expectations are over s ∼ $d _ { \mathrm { r e a l } } ^ { \pi _ { \theta } }$ and $\tau \sim \pi _ { \theta } ( \cdot \mid s )$ . The proof is provided in Appendix A.1.

The proxy term captures the dense component of the real objective, while the residual term accounts for the mismatch between the proxy and real advantage. Since both terms are defined on real visited states, the decomposition introduces no state-distribution mismatch.

The decomposition can reduce variance when the proxy is aligned with the real advantage, since the residual term only needs to estimate the remaining mismatch through grounded rollouts.

Proposition 3.2 (Conditional Variance Reduction). Fix a state s and let $Y ( s , \tau ) = A _ { \pi a } ^ { \mathrm { r e a l } } ( s , \tau )$ and $C ( s , \tau ) = \Phi _ { \pi _ { \theta } } ( s , \tau )$ . For $R _ { \alpha } ( s , \tau ) = Y ( s , \tau ) - \alpha C ( s , \tau )$ with $\tau \sim \pi _ { \theta } ( \cdot \mid s )$ and $\mathrm { V a r } _ { \tau } [ \check { C } ( s , \tau ) ] > 0$ $\mathrm { V a r } _ { \tau } [ R _ { \alpha } ( s , \tau ) ] = \mathrm { V a r } _ { \tau } [ Y ( s , \tau ) ] + \alpha ^ { 2 } \mathrm { V a r } _ { \tau } [ C ( s , \tau ) ] - 2 \alpha \mathrm { C o v } _ { \tau } [ Y ( s , \tau ) , C ( s , \tau ) ] .$ (4) and the minimizin $g \ c o e f f i c i e n t \ i s \ \alpha ^ { \star } ( s ) = \mathrm { C o v } _ { \tau } [ Y ( s , \tau ) , C ( s , \tau ) ] / \mathrm { V a r } _ { \tau } [ C ( s , \tau ) ] . \ I n \ p a r t$ icular, if $\mathrm { C o v } _ { \tau } [ Y ( s , \tau ) , C ( s , \tau ) ] > { \textstyle { \frac { 1 } { 2 } } } \mathrm { V a r } _ { \tau } [ C ( s , \tau ) ]$ , then $\mathrm { V a r } _ { \tau } [ Y ( s , \tau ) - C ( s , \tau ) ] < \mathrm { V a r } _ { \tau } [ Y ( s , \tau ) ]$ . If this condition holds for $d _ { \mathrm { r e a l } } ^ { \pi _ { \theta } }$ -almost every s, the same strict inequality holds after averaging over s.

The proof is in Appendix A.3. Importantly, the proxy need not be unbiased, since residual variance reduction only requires the proxy to be sufficiently aligned with the real advantage.

CRAFT instantiates this decomposition with the surrogate objective:

$$
\begin{array} { r l } { \displaystyle \operatorname* { m a x } _ { \pi _ { \theta } } } & { \underbrace { { \mathbb { E } } _ { s \sim d _ { \mathrm { r e a l } } ^ { \pi _ { \theta } } } \Big [ \mathcal { R } _ { \mathrm { c p } } ( s ; \pi _ { \theta } ) \Big ] } _ { \mathrm { D e n s e ~ C o u n t e r f a c t u a l ~ P r o x y } } + \underbrace { { \mathbb { E } } _ { \xi \sim ( \pi _ { \theta } , \kappa , P _ { \mathrm { r e a l } } ) } \Big [ \sum _ { t } \gamma ^ { t } r _ { t } ^ { \mathrm { g r } } \Big ] } _ { \mathrm { G r o u n d e d ~ R e s i d u a l ~ C o r r e c t i o n } } , } \end{array}\tag{5}
$$

where the two objective components are defined in Sections 3.2 and 3.3.

## 3.2 Dense Counterfactual Proxy

For each on-policy state $s _ { i }$ collected from closed-loop interaction, the counterfactual world evaluates a group of G candidate trajectories $\{ \tau _ { g } \} _ { g = 1 } ^ { G }$ over a finite virtual horizon. Evaluation criteria covering efficiency, safety, and rule compliance yield a scalar return $\tilde { R } _ { i , g }$ for each candidate. Implementation details of the counterfactual world and reward design are provided in Appendices D.3 and D.4. We convert these returns into local relative scores by normalizing within each candidate group:

$$
\tilde { A } _ { i , g } = \frac { \tilde { R } _ { i , g } - \mu _ { i } } { \sigma _ { i } + \varepsilon _ { \mathrm { n o r m } } } , \qquad \mu _ { i } = \frac { 1 } { G } \sum _ { g = 1 } ^ { G } \tilde { R } _ { i , g } ,\tag{6}
$$

where $\sigma _ { i }$ is the empirical standard deviation of $\{ \tilde { R } _ { i , g } \} _ { g = 1 } ^ { G }$ . In CRAFT, this normalized score is the proxy value $\Phi _ { \pi _ { \theta } } ( s _ { i } , \tau _ { g } ) = \tilde { A } _ { i , g }$ . Since fine-tuning is performed in a discrete action space, the counterfactual objective takes the exact expectation over candidate trajectories:

$$
\mathcal { L } _ { \mathrm { c p } } = - \frac { 1 } { B } \sum _ { i = 1 } ^ { B } \sum _ { g = 1 } ^ { G } \pi _ { \theta } ( \tau _ { g } \mid s _ { i } ) \tilde { A } _ { i , g } .\tag{7}
$$

This objective instantiates the dense counterfactual proxy term in Equation (5), where $\mathcal { R } _ { \mathrm { c p } } ( s _ { i } ; \pi _ { \theta } ) =$ $\begin{array} { r } { \sum _ { g = 1 } ^ { G } \pi _ { \theta } ( \tau _ { g } \mid s _ { i } ) \tilde { A } _ { i , g } } \end{array}$ . It provides dense group-wise comparative supervision at each on-policy state by evaluating candidate trajectories in a counterfactual world designed to approximate the real closed-loop world. However, unrealistic traffic interactions and dynamics biases still introduce a discrepancy between the proxy advantage $\tilde { A } _ { i , g }$ and the real advantage $A _ { \pi _ { \theta } } ^ { \mathrm { r e a l } } ( s _ { i } , \tau _ { g } )$ , which motivates the grounded residual correction.

## 3.3 Grounded Residual Correction

Rather than estimating the exact residual in Equation (3), CRAFT approximates the interactioncritical residual component using grounded feedback from traffic events that are not fully captured by the counterfactual proxy, such as collisions and traffic-rule violations. For a selected trajectory $\tau _ { t }$ , the controller executes $a _ { t } = \kappa ( s _ { t } , \tau _ { t } )$ , after which the event-driven corrective reward defined in Appendix D.4 is computed from the closed-loop transition and converted into bounded corrective advantages $\hat { A } _ { t } ^ { \mathrm { g r } }$ , as detailed in Appendix D.5.

Let $\rho _ { t } ( \theta ) = \pi _ { \theta } ( \tau _ { t } \mid s _ { t } ) / \pi _ { \theta _ { \mathrm { o l d } } } ( \tau _ { t } \mid s _ { t } )$ denote the importance sampling ratio. We first form

$$
\ell _ { t } ( \theta ) = \operatorname* { m i n } \Bigl ( \rho _ { t } ( \theta ) \hat { A } _ { t } ^ { \mathrm { g r } } , \ \mathrm { c l i p } ( \rho _ { t } ( \theta ) , 1 - \epsilon _ { \mathrm { c l i p } } , 1 + \epsilon _ { \mathrm { c l i p } } ) \hat { A } _ { t } ^ { \mathrm { g r } } \Bigr ) ,\tag{8}
$$

and then apply the dual-clipping [9, 10] with constant $c > 1$ to form the grounded residual loss

$$
\mathcal { L } _ { \mathrm { g r } } = - \mathbb { E } _ { t \in \mathcal { B } } \Big [ \operatorname* { m a x } \big ( \ell _ { t } ( \theta ) , c \hat { A } _ { t } ^ { \mathrm { g r } } \big ) { \mathbf 1 } _ { \hat { A } _ { t } ^ { \mathrm { g r } } < 0 } + \ell _ { t } ( \theta ) { \mathbf 1 } _ { \hat { A } _ { t } ^ { \mathrm { g r } } \geq 0 } \Big ] .\tag{9}
$$

Proposition A.2 formalizes the stabilization of dual clipping, which preserves informative gradients from rare catastrophic rollouts while preventing extreme negative events from dominating the update.

To characterize the grounded residual correction under the decomposition in Equation (3), let $\widehat { \Delta } _ { \pi _ { \theta } } ( s , \tau )$ be the residual approximation induced by grounded feedback, and define

$$
\boldsymbol { \widehat { g } } ( \theta ) = \mathbb { E } \Big [ \nabla _ { \theta } \log \pi _ { \theta } ( \tau \mid s ) \left( \Phi _ { \pi _ { \theta } } ( s , \tau ) + \widehat { \Delta } _ { \pi _ { \theta } } ( s , \tau ) \right) \Big ] .\tag{10}
$$

Theorem 3.3 (Gradient Bias under Residual Approximation). Let g(θ) denote the real gradient in Equation (3). $I f \mathbb { E } \| \nabla _ { \theta }$ log $\pi _ { \theta } ( \tau \mid s ) \parallel _ { 2 } ^ { 2 } < \infty$ and $\begin{array} { r } { \mathbb { E } | \widehat { \Delta } _ { \pi _ { \theta } } ( s , \tau ) - { \Delta } _ { \pi _ { \theta } } ( s , \tau ) | ^ { 2 } < \infty } \end{array}$ , then

$$
\begin{array} { r } { \| \widehat { g } ( \theta ) - g ( \theta ) \| _ { 2 } \leq \Big ( \mathbb { E } \| \nabla _ { \theta } \log \pi _ { \theta } ( \tau \mid s ) \| _ { 2 } ^ { 2 } \Big ) ^ { 1 / 2 } \Big ( \mathbb { E } | \widehat { \Delta } _ { \pi _ { \theta } } ( s , \tau ) - \Delta _ { \pi _ { \theta } } ( s , \tau ) | ^ { 2 } \Big ) ^ { 1 / 2 } . } \end{array}\tag{11}
$$

$I f \parallel \nabla _ { \theta }$ log $\pi _ { \boldsymbol { \theta } } ( \tau \mid s ) \| _ { 2 } \leq G _ { \nabla }$ almost surely, the first factor reduces to $G _ { \nabla }$ . Proof in Appendix A.5.

Theorem 3.3 establishes the role of grounded residual correction in Equation (5). Grounded feedback captures the dominant mismatch left by the dense counterfactual proxy, focusing correction on the interaction-sensitive part of the real closed-loop objective.

## 3.4 On-Policy Self-Distillation

The proxy-residual objective provides dense and grounded learning signals, but unconstrained policy updates may deviate from reliable pre-trained behavior. CRAFT limits this drift through on-policy self-distillation from an EMA teacher $\pi _ { T }$

$$
\theta _ { T } ^ { ( k + 1 ) }  m \theta _ { T } ^ { ( k ) } + ( 1 - m ) \theta ^ { ( k ) } , \qquad \theta _ { T } ^ { ( 0 ) } = \theta _ { \mathrm { p r e } } , \quad 0 \leq m < 1 .\tag{12}
$$

The teacher is initialized from the pre-trained checkpoint, as a conservative anchor early in training, and subsequently tracks the smoothed online policy through EMA. For a visited state s, let ${ \cal U } ( s , \tau ) =$ $\Phi _ { \pi _ { \theta } } ( s , \tau ) + \widehat { \Delta } _ { \pi _ { \theta } } ( s , \tau )$ denote the proxy-residual advantage estimate. Proposition A.1 indicates that policy improvement constrained by reverse KL induces an exponential reweighting of the teacher distribution according to this advantage estimate. This provides a principled update rule that improves the policy under the proxy-residual objective while remaining close to teacher-supported behavior. CRAFT implements this rule with asymmetric KL penalties,

$$
\mathcal { L } _ { \mathrm { d i s t } } = \mathbb { E } _ { s \sim d _ { \tau _ { \mathrm { c o l l } } ^ { \pi _ { \theta } } , \tau \sim \pi _ { \theta } \left( \cdot \vert s \right) } } \left[ \log \frac { \pi _ { \theta } ( \tau \mid s ) } { \pi _ { T } ( \tau \mid s ) } \right] , \quad \mathcal { L } _ { \mathrm { K L } } = \mathbb { E } _ { s \sim d _ { \tau _ { \mathrm { c o l l } } } ^ { \pi _ { \theta } } , \tau \sim \pi _ { T } \left( \cdot \vert s \right) } \left[ \log \frac { \pi _ { T } ( \tau \mid s ) } { \pi _ { \theta } ( \tau \mid s ) } \right] .\tag{13}
$$

The reverse KL term is the primary constraint, with $\beta _ { r } > \beta _ { f }$ , and suppresses deviations from reliable pre-trained behavior. The weaker forward KL term preserves teacher-supported alternatives and mitigates collapse to a narrow subset of trajectories favored by the proxy-residual objective.

Overall, CRAFT combines the dense counterfactual proxy, grounded residual correction, and asymmetric self-distillation into the final objective, with Algorithm 1 detailing the full training procedure:

$$
{ \mathcal { L } } _ { \mathrm { a l l } } = \lambda _ { \mathrm { c p } } { \mathcal { L } } _ { \mathrm { c p } } + \lambda _ { \mathrm { g r } } { \mathcal { L } } _ { \mathrm { g r } } + \beta _ { r } { \mathcal { L } } _ { \mathrm { d i s t } } + \beta _ { f } { \mathcal { L } } _ { \mathrm { K L } } .\tag{14}
$$

## 4 Experiments

## 4.1 Experimental Setup

Benchmark We conduct experiments on Bench2Drive [43], a CARLA-based benchmark [44] for closed-loop evaluation in autonomous driving. Our setup follows Bench2Drive as the primary protocol, with additional scenario configurations from LEAD [45] and Longest6 V2 [25]. We also apply several protocol-level refinements to the original scenarios and evaluation protocol to improve efficiency and reduce repeated-run variance. Details are provided in Appendix B.

Metrics We adopt the standard Bench2Drive metrics, including Driving Score (DS), Success Rate (SR), and Multi-Ability. DS combines Route Completion (RC) and Infraction Score (IS), where RC measures route progress and IS reflects safety and traffic-rule compliance. SR measures successful scenario completion, while Multi-Ability separately evaluates five advanced urban driving skills.

Driving Policies and Fine-tuning Baselines To demonstrate the generality of CRAFT, we select three representative driving policies from distinct paradigms.

• Hierarchical planning. HiP-AD [46] uses multi-granularity planning queries together with deformable attention to couple perception and planning within a unified decoder.

• Vision-language-action. MindDrive [24] uses a VLA architecture with separate decision and action experts, translating high-level semantic decisions into low-level trajectory generation.

• Vocabulary scoring. SparseDriveV2 [22] uses sparse scene representation for end-to-end driving, and here we use its vocabulary variant to provide a dense candidate-trajectory space for RL. This property also makes it the default driving policy in our subsequent analysis experiments.

We compare CRAFT against the pre-trained policy and three RL fine-tuning baselines under the same setting and evaluation protocol. The baselines differ only in their training objective.

• PPO [23] employs a clipped surrogate objective together with a learned value baseline, making it the standard actor–critic baseline for stable on-policy fine-tuning.

• REINFORCE++ [47] removes the learned critic and uses return-based updates normalized at the batch level, providing a simple critic-free baseline for on-policy fine-tuning.

• GRPO [8] replaces a separate critic with relative rewards computed within output groups, making it the closest baseline to the group-based counterfactual update used in CRAFT.

Table 1: Closed-loop performance on Bench2Drive. † denotes the vocabulary-based variant of SparseDriveV2. Best results are highlighted in bold, and second-best results are underlined.
<table><tr><td rowspan="2">Driving Policy</td><td rowspan="2">Method</td><td colspan="2">Closed-loop Metrics</td><td colspan="6">Multi-Ability (%)</td></tr><tr><td>DS ↑</td><td>SR (%) ↑</td><td>Merging ↑ Overtaking ↑ Emergency Brake ↑ Give Way ↑</td><td></td><td></td><td></td><td>Traffic Sign ↑ Mean ↑</td><td></td></tr><tr><td rowspan="5">HiP-AD [46] (Hierarchical Planning)</td><td>Pre-trained</td><td>73.46</td><td>53.64</td><td>46.30</td><td>53.30</td><td>63.30</td><td>50.00</td><td>46.30</td><td>51.80</td></tr><tr><td>REINFORCE++</td><td>74.82</td><td>55.00</td><td>36.20</td><td>64.40</td><td>71.70</td><td>50.00</td><td>44.20</td><td>53.30</td></tr><tr><td>PPO</td><td>73.58</td><td>53.18</td><td>41.20</td><td>55.60</td><td>68.30</td><td>30.00</td><td>43.20</td><td>47.70</td></tr><tr><td>GRPO</td><td>75.27</td><td>55.91</td><td>42.50</td><td>60.00</td><td>70.00</td><td>40.00</td><td>48.40</td><td>52.20</td></tr><tr><td>CRAFT (Ours)</td><td>75.79</td><td>56.36</td><td>40.00</td><td>64.40</td><td>73.30</td><td>50.00</td><td>48.40</td><td>55.20</td></tr><tr><td rowspan="5">MindDrive [24] (Vision Language Action)</td><td>Pre-trained</td><td>62.60</td><td>40.45</td><td>26.30</td><td>51.10</td><td>50.00</td><td>40.00</td><td>32.60</td><td>40.00</td></tr><tr><td>REINFORCE++</td><td>63.68</td><td>41.36</td><td>32.50</td><td>46.70</td><td>50.00</td><td>50.00</td><td>33.70</td><td>42.60</td></tr><tr><td>PPO</td><td>64.61</td><td>42.73</td><td>30.00</td><td>48.90</td><td>55.00</td><td>50.00</td><td>35.80</td><td>43.90</td></tr><tr><td>GRPO</td><td>65.12</td><td>43.18</td><td>27.50</td><td>57.80</td><td>53.30</td><td>50.00</td><td>34.70</td><td>44.70</td></tr><tr><td>CRAFT (Ours)</td><td>67.45</td><td>46.36</td><td>37.50</td><td>51.10</td><td>56.70</td><td>50.00</td><td>37.90</td><td>46.60</td></tr><tr><td rowspan="5">SparseDriveV2† [22] (Vocabulary Scoring)</td><td>Pre-trained</td><td>66.43</td><td>45.45</td><td>43.80</td><td>40.00</td><td>56.70</td><td>50.00</td><td>32.60</td><td>44.60</td></tr><tr><td>REINFORCE++</td><td>66.60</td><td>46.36</td><td>41.20</td><td>53.30</td><td>55.00</td><td>50.00</td><td>26.30</td><td>45.20</td></tr><tr><td>PPO</td><td>67.44</td><td>49.09</td><td>43.80</td><td>53.30</td><td>61.70</td><td>50.00</td><td>33.70</td><td>48.50</td></tr><tr><td>GRPO</td><td>68.40</td><td>48.18</td><td>41.20</td><td>48.90</td><td>61.70</td><td>50.00</td><td>36.80</td><td>47.70</td></tr><tr><td>CRAFT (Ours)</td><td>71.10</td><td>50.45</td><td>40.00</td><td>53.30</td><td>68.30</td><td>50.00</td><td>37.90</td><td>49.90</td></tr></table>

VI: VRU Interaction OA: Obstacle Avoidance IT: Intersection Turning EH: Emergency Handling HM: Highway Merging  
(a) SparseDriveV2  
![](images/ae726c5ba9c12d511b7972a74bae3651649a495123a2fc387b1748c839eada02.jpg)  
(b) HiP-AD  
(c) MindDrive  
Figure 3: Fine-grained ability profiles. Radar plots compare fine-tuning methods across driving policies. Each axis represents a scenario-specific capability, and higher values indicate better performance.

Implementation Details For all policies, we fine-tune only the planning-related modules while freezing pre-trained visual processing. All fine-tuning methods share a CaRL-style reward formulation based on progress and infractions [25]. Our RL infrastructure is built on RIFT [48] and supports asynchronous rollout collection and policy updates. Details appear in Appendices D.2 to D.5.

## 4.2 Main Closed-Loop Results

The main comparison reveals a consistent pattern across policy architectures. CRAFT improves closed-loop metrics without relying on any specific model architecture. This improvement remains evident even for HiP-AD, where the pre-trained policy is already strong, and is larger for MindDrive and SparseDriveV2, where the initial closed-loop performance indicates greater potential for finetuning. In Table 1, the same ordering holds across hierarchical planning, vision-language-action, and vocabulary-scoring, supporting the claim that CRAFT generalizes across diverse policy architectures.

The comparison also highlights the value of the full CRAFT objective. Even GRPO, the closest proxy-based baseline, underperforms CRAFT across policy architectures. PPO and REINFORCE++ improve specific driving abilities, but their gains are less consistent. This pattern further supports the proxy-residual design of CRAFT, suggesting that dense counterfactual supervision is most effective when refined by grounded residual feedback.

The ability profiles in Figure 3 provide a finer-grained view of the aggregate results. CRAFT leads on most abilities, with the largest gains in safety-critical behaviors such as VRU Interaction, Obstacle Avoidance, and Intersection Turning. These abilities depend more strongly on closed-loop interaction and are therefore less likely to be captured by a dense counterfactual proxy alone. This pattern further supports the proxy-residual design of CRAFT, suggesting that dense counterfactual supervision alone is insufficient for safety-critical events and that grounded residual correction is essential.

Table 2: Ablation study of CRAFT. SD: self-distillation; CP: counterfactual proxy; GR: grounded residual.
<table><tr><td rowspan="2">ID SD</td><td rowspan="2"></td><td rowspan="2">CP</td><td rowspan="2">GR</td><td colspan="2">Closed-loop Metrics</td></tr><tr><td>DS↑ RC↑</td><td>IS↑ SR↑</td></tr><tr><td>1</td><td>X</td><td>X</td><td>X</td><td>66.43 77.53</td><td>0.80 45.45</td></tr><tr><td>2</td><td>√</td><td>x</td><td>x</td><td>66.49 76.65</td><td>0.81 46.36</td></tr><tr><td>3</td><td>√</td><td>√</td><td>x</td><td>68.40 78.28</td><td>0.82 48.18</td></tr><tr><td>4</td><td>√</td><td>√</td><td>1</td><td>71.10 80.01</td><td>0.84 50.45</td></tr></table>

Table 3: Generalization across datasets. Gains over the pre-trained policy under each train-test split. ‡: Town12 subset of LEAD scenarios.
<table><tr><td rowspan="2">Train</td><td rowspan="2">Test</td><td colspan="3">Closed-loop Metrics</td></tr><tr><td>∆ DS ↑</td><td>∆RC↑ ∆IS ↑</td><td>∆ SR ↑</td></tr><tr><td>Bench2Drive</td><td>Bench2Drive</td><td>+4.67</td><td>+2.48 +0.04</td><td>+5.00</td></tr><tr><td></td><td>Bench2Drive Longest6 v2 [25]</td><td>+2.18</td><td>+1.12 +0.06</td><td>+0.00</td></tr><tr><td>LEAD</td><td>LEAD‡ [45]</td><td>+2.14</td><td>+2.60 +0.01</td><td>+1.89</td></tr><tr><td>LEAD$</td><td>Bench2Drive</td><td>+0.58</td><td>-0.34 +0.01</td><td>+0.91</td></tr></table>

![](images/b747bb673e7b3aff29da615ba91816b35356a4f203145102280fa5681090b674.jpg)

![](images/b1bf3fa6cf71872a88412cc8738ba97e3a5d564348efb2ec788da8480dff0b02.jpg)  
(a) Scaling Behavior Across Fine-tuning Methods

![](images/4369232af03bc51138198eedc5cd7096673ce5815e4587a6f0470f5a762aae46.jpg)

![](images/406e225426ab7eab7d09b13dbb8aee4dfa6624de4d417173af8f314f59c16d6f.jpg)  
(b) Training Dynamics and Final Performance

Figure 4: Scaling behavior and reward dynamics. (a) Closed-loop performance as the Bench2Drive scale increases. (b) Reward evolution during RL training on a challenging scenario, with final evaluation performance.  
![](images/e413c804dfa9e7b82daf24f6b318c67909f3ac2ca916dfd408fe3b3b1b5b70af.jpg)  
(a) MindDrive KL Stability

![](images/b21e32cdb91238d26d5830b64654a57e3a0a37737ba582fe33587a20552cf23f.jpg)  
(b) HiP-AD KL Stability

![](images/e61ef53ea69214ca0ecac664cd71fd672a5e05be9f6f784c10dbf83a1926ee9b.jpg)  
(c) SparseDriveV2 KL Stability

![](images/6f75f2d0ccfc395356f87a52886daff6fabae4ec935d565d5e71f50680d42397.jpg)  
(d) Mean KL Stability

![](images/cd1239e2e7209203480030ca10c91c6c1dc8fe1fce2311b0b8e290e8b591bc6f.jpg)  
(e) Expected Advantage Stability  
Figure 5: Training stability. Panels (a)–(d) report the coefficients of variation for KL terms across fine-tuning methods, and panel (e) reports the coefficient of variation for the expected advantage across driving policies.

## 4.3 Ablation and Generalization Analysis

The ablation study in Table 2 clarifies each component of CRAFT. Self-distillation reinforces the dominant modes of the pre-trained policy, while the dense counterfactual proxy drives broad closed loop gains. With grounded residual correction, the full CRAFT objective achieves the best overall performance, especially on the interaction-related metrics IS and SR. These results support the proxy-residual view, where the dense counterfactual proxy provides the primary optimization signal and grounded residual correction compensates for counterfactual bias through closed-loop interaction.

As shown in Table 3, CRAFT maintains positive generalization under scenario shift. In-domain fine-tuning on Bench2Drive delivers the largest improvement over the pre-trained policy, while crossscenario transfer still yields consistent gains. The main limitation appears in Route Completion, where the limited improvement under transfer suggests a more conservative policy in unseen scenarios. Overall, CRAFT generalizes beyond the training split, although the magnitude of improvement remains partly dependent on the interaction distribution used for fine-tuning.

## 4.4 Scaling and Training Dynamics

Figure 4 reveals a clear scaling pattern. CRAFT is the only method whose performance improves consistently with more data. PPO and REINFORCE++, which rely only on real interaction, become less stable at larger scales and show saturating gains, suggesting inefficient learning from sparse closedloop feedback. GRPO, which depends only on proxy supervision, delivers limited improvement and even deteriorates at larger scales, indicating that proxy bias may become the main bottleneck in later stages of training. These trends demonstrate that efficient scaling requires dense proxy supervision, while sustained gains depend on grounded residual correction.

![](images/38e9d658fd6ddd7e8427cb2fe60678b03e85d340248be02d599c2fcd9384616b.jpg)  
Figure 6: Policy distribution shift in a pedestrian-crossing scenario. Top: a closed-loop scene snapshot with SparseDriveV2 as the ego vehicle. Bottom: the policy distributions over the trajectory vocabulary for the pre-trained and fine-tuned policies. CRAFT shifts probability mass toward braking-compatible modes.

The results in Figure 5 further confirm the stability of CRAFT. In terms of KL stability, CRAFT shows larger gains for policies with broader action spaces, such as HiP-AD and SparseDriveV2, while the advantage is smaller for MindDrive, which has a more constrained action space. This pattern suggests that a broader action space improves counterfactual proxy stability. The expected-advantage results support the same conclusion from the grounded side. Compared with GRPO, CRAFT reduces expected-advantage variation across policy architectures. Although grounded residual correction is driven by sparse feedback, dual clipping stabilizes training. Together, these results suggest that the stability of CRAFT arises from both components, with broader action spaces improving proxy stability and dual-clipped grounded residual correction further reducing update variance.

## 4.5 Qualitative Scenario Analysis

Figure 6 illustrates how fine-tuning reshapes the policy distribution in a safety-critical state. The pre-trained SparseDriveV2 assigns most probability mass to a left-turn accelerating mode, which remains largely unchanged after PPO and REINFORCE++ fine-tuning. This similarity suggests that sparse closed-loop updates do not efficiently shift the dominant mode away from unsafe behavior. GRPO shifts part of the distribution toward a braking-compatible mode, but this mode remains secondary, indicating that the counterfactual proxy alone gives a biased estimate of the safer closedloop response. CRAFT induces the clearest shift, making the braking-compatible mode dominant while retaining the original peak of the pre-trained policy at lower probability. These results highlight the advantage of proxy-residual fine-tuning for safety-critical events by shifting probability toward interaction-grounded corrective behavior while preserving the pre-trained policy manifold.

## 5 Conclusions

This paper presents CRAFT, a proxy-residual framework for closed-loop post-training of supervised driving policies. CRAFT combines a dense counterfactual proxy on on-policy visited states, grounded residual correction from executed rollouts, and self-distillation to preserve reliable pre-trained behavior during fine-tuning. We support this design with an exact gradient decomposition on the real closed-loop state distribution, together with variance, bias, and stability analyses. On Bench2Drive, CRAFT achieves the strongest closed-loop gains across hierarchical-planning, vision-language-action, and vocabulary-scoring architectures, while ablation and scaling results confirm the complementary roles of counterfactual proxy learning, grounded residual correction, and self-distillation.

## References

[1] Y. Hu, J. Yang, L. Chen, K. Li, C. Sima, X. Zhu, S. Chai, S. Du, T. Lin, W. Wang, L. Lu, X. Jia, Q. Liu, J. Dai, Y. Qiao, and H. Li. Planning-oriented autonomous driving. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2023.

[2] B. Jiang, S. Chen, Q. Xu, B. Liao, J. Chen, H. Zhou, Q. Zhang, W. Liu, C. Huang, and X. Wang. Vad: Vectorized scene representation for efficient autonomous driving. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 8340–8350, 2023.

[3] W. Sun, X. Lin, Y. Shi, C. Zhang, H. Wu, and S. Zheng. Sparsedrive: End-to-end autonomous driving via sparse scene representation. In 2025 IEEE International Conference on Robotics and Automation (ICRA), pages 8795–8801. IEEE, 2025.

[4] Z. Peng, W. Ding, Y. You, Y. Chen, W. Luo, T. Tian, Y. Cao, A. Sharma, D. Xu, B. Ivanovic, et al. Counterfactual vla: Self-reflective vision-language-action model with adaptive reasoning. arXiv preprint arXiv:2512.24426, 2025.

[5] C. Dang, S. Ang, Y. Li, H. Tian, J. Wang, G. Li, H. Ye, J. Ma, L. Chen, and Y. Wang. Drivefine: Refining-augmented masked diffusion vla for precise and robust driving. arXiv preprint arXiv:2602.14577, 2026.

[6] T. Xia, Y. Li, L. Zhou, J. Yao, K. Xiong, H. Sun, B. Wang, K. Ma, G. Chen, H. Ye, et al. Drivelaw: Unifying planning and video generation in a latent driving world. arXiv preprint arXiv:2512.23421, 2025.

[7] Y. Li, S. Shang, W. Liu, B. Zhan, H. Wang, Y. Wang, Y. Chen, X. Wang, Y. An, C. Tang, et al. Drivevla-w0: World models amplify data scaling law in autonomous driving. arXiv preprint arXiv:2510.12796, 2025.

[8] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. Li, Y. Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300, 2024.

[9] D. Ye, Z. Liu, M. Sun, B. Shi, P. Zhao, H. Wu, H. Yu, S. Yang, X. Wu, Q. Guo, et al. Mastering complex control in moba games with deep reinforcement learning. In Proceedings of the AAAI conference on artificial intelligence, volume 34, pages 6672–6679, 2020.

[10] Y. Gao, B. Shi, X. Du, L. Wang, G. Chen, Z. Lian, F. Qiu, G. Han, W. Wang, D. Ye, et al. Learning diverse policies in moba games via macro-goals. Advances in Neural Information Processing Systems, 34: 16171–16182, 2021.

[11] B. Liao, S. Chen, H. Yin, B. Jiang, C. Wang, S. Yan, X. Zhang, X. Li, Y. Zhang, Q. Zhang, et al. Diffusiondrive: Truncated diffusion model for end-to-end autonomous driving. In Proceedings of the Computer Vision and Pattern Recognition Conference, pages 12037–12047, 2025.

[12] L. Liu, C. Jia, G. Yu, Z. Song, J. Li, F. Jia, P. Wu, X. Hao, and Y. Luo. Guideflow: Constraint-guided flow matching for planning in end-to-end autonomous driving. arXiv preprint arXiv:2511.18729, 2025.

[13] Z. Zheng, S. Chen, H. Yin, X. Zhang, J. Zou, X. Wang, Q. Zhang, and L. Zhang. Resad: Normalized residual trajectory modeling for end-to-end autonomous driving. arXiv preprint arXiv:2510.08562, 2025.

[14] Y. Zheng, T. Tan, B. Huang, E. Liu, R. Liang, J. Zhang, J. Cui, G. Chen, K. Ma, H. Ye, et al. Unleashing the potential of diffusion models for end-to-end autonomous driving. arXiv preprint arXiv:2602.22801, 2026.

[15] H. Fu, D. Zhang, Z. Zhao, J. Cui, D. Liang, C. Zhang, D. Zhang, H. Xie, B. Wang, and X. Bai. Orion: A holistic end-to-end autonomous driving framework by vision-language instructed action generation. In Proceedings ofthe IEEE/CVF International Conference on Computer Vision, pages 24823–24834, 2025.

[16] K. Renz, L. Chen, E. Arani, and O. Sinavski. Simlingo: Vision-only closed-loop autonomous driving with language-action alignment. In Proceedings of the Computer Vision and Pattern Recognition Conference, pages 11993–12003, 2025.

[17] Z. Zhou, T. Cai, S. Z. Zhao, Y. Zhang, Z. Huang, B. Zhou, and J. Ma. Autovla: A vision-language-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning. arXiv preprint arXiv:2506.13757, 2025.

[18] X. Wang, Q. Liu, W. Ding, Z. Yang, W. Li, C. Liu, B. Li, K. Zhan, X. Lang, and W. Chen. Unifying language-action understanding and generation for autonomous driving. arXiv preprint arXiv:2603.01441, 2026.

[19] Z. Li, K. Li, S. Wang, S. Lan, Z. Yu, Y. Ji, Z. Li, Z. Zhu, J. Kautz, Z. Wu, et al. Hydra-mdp: End-to-end multimodal planning with multi-target hydra-distillation. arXiv preprint arXiv:2406.06978, 2024.

[20] W. Yao, Z. Li, S. Lan, Z. Wang, X. Sun, J. M. Alvarez, and Z. Wu. Drivesuprim: Towards precise trajectory selection for end-to-end planning. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 40, pages 11910–11918, 2026.

[21] Z. Li, W. Yao, Z. Wang, X. Sun, J. Chen, N. Chang, M. Shen, Z. Wu, S. Lan, and J. M. Alvarez. Generalized trajectory scoring for end-to-end multimodal planning. arXiv preprint arXiv:2506.06664, 2025.

[22] W. Sun, X. Lin, K. Chen, Z. Pei, X. Li, Y. Shi, and S. Zheng. Sparsedrivev2: Scoring is all you need for end-to-end autonomous driving. arXiv preprint arXiv:2603.29163, 2026.

[23] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms. arXiv preprint arXiv:1707.06347, 2017.

[24] H. Fu, D. Zhang, Z. Zhao, J. Cui, H. Xie, B. Wang, G. Chen, D. Liang, and X. Bai. Minddrive: A vision-language-action model for autonomous driving via online reinforcement learning. arXiv preprint arXiv:2512.13636, 2025.

[25] B. Jaeger, D. Dauner, J. Beißwenger, S. Gerstenecker, K. Chitta, and A. Geiger. Carl: Learning scalable planning policies with simple rewards. In 9th Annual Conference on Robot Learning, 2025.

[26] H. Gao, S. Chen, B. Jiang, B. Liao, Y. Shi, X. Guo, Y. Pu, X. Li, W. Liu, Q. Zhang, et al. Rad: Training an end-to-end driving policy via large-scale 3dgs-based reinforcement learning. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, 2025.

[27] H. Gao, S. Chen, Y. Zhu, Y. Song, W. Liu, Q. Zhang, and X. Wang. Rad-2: Scaling reinforcement learning in a generator-discriminator framework. arXiv preprint arXiv:2604.15308, 2026.

[28] C. Ni, G. Zhao, X. Wang, Z. Zhu, W. Qin, X. Chen, G. Jia, G. Huang, and W. Mei. Recondreamer-rl: Enhancing reinforcement learning via diffusion-based scene reconstruction. arXiv preprint arXiv:2508.08170, 2025.

[29] Z. Huang, Z. Sheng, Z. Wan, Y. Qu, J. You, S. Jiang, and S. Chen. Drivevlm-rl: Neuroscience-inspired reinforcement learning with vision-language models for safe and deployable autonomous driving. arXiv preprint arXiv:2603.18315, 2026.

[30] Q. Li, X. Jia, S. Wang, and J. Yan. Think2drive: Efficient reinforcement learning by thinking with latent world model for autonomous driving (in carla-v2). In European conference on computer vision, pages 142–158. Springer, 2024.

[31] Z. Yang, X. Jia, Q. Li, X. Yang, M. Yao, and J. Yan. Raw2drive: Reinforcement learning with aligned world models for end-to-end autonomous driving (in carla v2). In The Thirty-ninth Annual Conference on Neural Information Processing Systems, 2025.

[32] H. Liu, T. Li, H. Yang, L. Chen, C. Wang, K. Guo, H. Tian, H. Li, H. Li, and C. Lv. Reinforced refinement with self-aware expansion for end-to-end autonomous driving. IEEE Transactions on Pattern Analysis and Machine Intelligence, 2026.

[33] R. Rafailov, A. Sharma, E. Mitchell, C. D. Manning, S. Ermon, and C. Finn. Direct preference optimization: Your language model is secretly a reward model. Advances in Neural Information Processing Systems, 36: 53728–53741, 2023.

[34] Y. Li, K. Xiong, X. Guo, F. Li, S. Yan, G. Xu, L. Zhou, L. Chen, H. Sun, B. Wang, et al. Recogdrive: A reinforced cognitive framework for end-to-end autonomous driving. arXiv preprint arXiv:2506.08052, 2025.

[35] J. Zou, S. Chen, B. Liao, Z. Zheng, Y. Song, L. Zhang, Q. Zhang, W. Liu, and X. Wang. Diffusiondrivev2: Reinforcement learning-constrained truncated diffusion modeling in end-to-end autonomous driving. arXiv preprint arXiv:2512.07745, 2025.

[36] R. Yasarla, D. Hegde, S. Han, H.-P. Cheng, Y. Shi, M. Sadeghigooghari, S. Mahajan, A. Bhattacharyya, L. Liu, R. Garrepalli, et al. Generative scenario rollouts for end-to-end autonomous driving. arXiv preprint arXiv:2601.11475, 2026.

[37] S. Shang, B. Zhan, Y. Yan, Y. Wang, Y. Li, Y. An, X. Wang, J. Liu, L. Hou, L. Fan, et al. Dynvla: Learning world dynamics for action reasoning in autonomous driving. arXiv preprint arXiv:2603.11041, 2026.

[38] R. Liang, Y. Zheng, K. Zheng, T. Tan, J. Li, L. Mao, Z. Wang, G. Chen, H. Ye, J. Liu, et al. Dichotomous diffusion policy optimization. arXiv preprint arXiv:2601.00898, 2025.

[39] C. Chen, Y. Yang, Z. Tan, Y. Wang, R. Zhan, H. Liu, X. Mao, J. Bao, X. Tang, L. Yang, et al. Devil is in narrow policy: Unleashing exploration in driving vla models. arXiv preprint arXiv:2603.06049, 2026.

[40] D. Dauner, M. Hallgarten, T. Li, X. Weng, Z. Huang, Z. Yang, H. Li, I. Gilitschenski, B. Ivanovic, M. Pavone, et al. Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking. Advances in Neural Information Processing Systems, 37:28706–28719, 2024.

[41] H. Lin, Y. Zhang, W. Ding, J. Wu, and D. Zhao. Model-based policy adaptation for closed-loop end-to-end autonomous driving. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, 2025. URL https://openreview.net/forum?id=4OLbpaTKJe.

[42] T. Yan, T. Tang, X. Gui, Y. Li, J. Zhesng, W. Huang, L. Kong, W. Han, X. Zhou, X. Zhang, et al. Ad-r1: Closed-loop reinforcement learning for end-to-end autonomous driving with impartial world models. arXiv preprint arXiv:2511.20325, 2025.

[43] X. Jia, Z. Yang, Q. Li, Z. Zhang, and J. Yan. Bench2drive: Towards multi-ability benchmarking of closed-loop end-to-end autonomous driving. arXiv preprint arXiv:2406.03877, 2024.

[44] A. Dosovitskiy, G. Ros, F. Codevilla, A. Lopez, and V. Koltun. Carla: An open urban driving simulator. In Conference on robot learning, pages 1–16. PMLR, 2017.

[45] L. Nguyen, M. Fauth, B. Jaeger, D. Dauner, M. Igl, A. Geiger, and K. Chitta. Lead: Minimizing learnerexpert asymmetry in end-to-end driving. In Conference on Computer Vision and Pattern Recognition (CVPR), 2026.

[46] Y. Tang, Z. Xu, Z. Meng, and E. Cheng. Hip-ad: Hierarchical and multi-granularity planning with deformable attention for autonomous driving in a single decoder. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 25605–25615, 2025.

[47] J. Hu, J. K. Liu, H. Xu, and W. Shen. Reinforce++: Stabilizing critic-free policy optimization with global advantage normalization. arXiv preprint arXiv:2501.03262, 2025.

[48] K. Chen, W. Sun, H. Cheng, and S. Zheng. Rift: Group-relative rl fine-tuning for realistic and controllable traffic simulation. arXiv preprint arXiv:2505.03344, 2025.

[49] C. Sima, K. Renz, K. Chitta, L. Chen, H. Zhang, C. Xie, J. Beißwenger, P. Luo, A. Geiger, and H. Li. Drivelm: Driving with graph visual question answering. In European conference on computer vision, pages 256–274. Springer, 2024.

[50] S. Gerstenecker, A. Geiger, and K. Renz. Plant 2.0: Exposing biases and structural flaws in closed-loop driving. arXiv preprint arXiv:2511.07292, 2025.

## Appendix

## A Proofs

This appendix provides the proofs for the formal statements in Section 3. Unless noted otherwise, expectations are taken over $s \sim d _ { \mathrm { r e a l } } ^ { \pi _ { \theta } }$ and candidate trajectory $\tau \sim \pi _ { \theta } ( \cdot \mid s )$

## A.1 Exact Decomposition

Proof. By definition of the residual mismatch,

$$
A _ { \pi _ { \theta } } ^ { \mathrm { r e a l } } ( s , \tau ) = \Phi _ { \pi _ { \theta } } ( s , \tau ) + \Delta _ { \pi _ { \theta } } ( s , \tau ) .\tag{15}
$$

Substituting this identity into the real policy gradient in Equation (2) gives

$$
\nabla _ { \theta } J _ { \mathrm { r e a l } } ( \pi _ { \theta } ) = \mathbb { E } \Big [ \nabla _ { \theta } \log \pi _ { \theta } ( \tau \mid s ) \left( \Phi _ { \pi _ { \theta } } ( s , \tau ) + \Delta _ { \pi _ { \theta } } ( s , \tau ) \right) \Big ]\tag{16}
$$

$$
\begin{array} { r } { = \mathbb { E } \Big [ \nabla _ { \theta } \log { \pi _ { \theta } ( \tau \mid s ) } \Phi _ { \pi _ { \theta } } ( s , \tau ) \Big ] + \mathbb { E } \Big [ \nabla _ { \theta } \log { \pi _ { \theta } ( \tau \mid s ) } \Delta _ { \pi _ { \theta } } ( s , \tau ) \Big ] , } \end{array}\tag{17}
$$

which proves the claim.

## A.2 KL-Proximal Policy Improvement

Proposition A.1 (KL-Proximal Policy Improvement). For afinite or countable discrete trajectory space, fix state s and a strictly positive teacher distribution $q ( \tau ) = \pi _ { T } ( \tau \mid s )$ . For anyfixed bounded score $U ( s , \tau )$ and temperature $\eta > 0 ,$ , the non-parametric solution to

$$
\operatorname* { m a x } _ { p \in \Delta ( \mathcal { T } ) } \mathbb { E } _ { \tau \sim p } [ U ( s , \tau ) ] - \eta D _ { \mathrm { K L } } ( p \Vert q )\tag{18}
$$

is

$$
p _ { \eta } ^ { \star } ( \tau \mid s ) = \frac { q ( \tau ) \exp ( U ( s , \tau ) / \eta ) } { \sum _ { \tau ^ { \prime } \in \mathcal { T } } q ( \tau ^ { \prime } ) \exp ( U ( s , \tau ^ { \prime } ) / \eta ) } .\tag{19}
$$

Proof. Fix s and write $U ( \tau ) = U ( s , \tau )$ . The Lagrangian for the optimization problem in Proposition A.1, with multiplier λ for the normalization constraint $\begin{array} { r } { \sum _ { \tau } p ( \tau ) = 1 } \end{array}$ , is

$$
\mathcal { L } ( p , \lambda ) = \sum _ { \tau } p ( \tau ) U ( \tau ) - \eta \sum _ { \tau } p ( \tau ) \log \frac { p ( \tau ) } { q ( \tau ) } + \lambda \Big ( \sum _ { \tau } p ( \tau ) - 1 \Big ) .\tag{20}
$$

For any candidate trajectory with $p ( \tau ) > 0$ , stationarity gives

$$
U ( \tau ) - \eta \Big ( \log \frac { p ( \tau ) } { q ( \tau ) } + 1 \Big ) + \lambda = 0 ,\tag{21}
$$

and therefore

$$
p ( \tau ) = q ( \tau ) \exp \biggl ( \frac { U ( \tau ) + \lambda - \eta } { \eta } \biggr ) .\tag{22}
$$

The normalizing constraint determines the common factor,

$$
\exp \biggl ( \frac { \lambda - \eta } { \eta } \biggr ) = \left( \sum _ { \tau ^ { \prime } } q ( \tau ^ { \prime } ) \exp ( U ( \tau ^ { \prime } ) / \eta ) \right) ^ { - 1 } .\tag{23}
$$

Substituting this factor yields Equation (19). Since the objective is strictly concave in p when $\eta > 0$ and q has full support, this stationary point is the unique maximizer. □

## A.3 Variance Reduction

Proof. Fix s and suppress the dependence on $( s , \tau )$ for readability. Since $R _ { \alpha } = Y - \alpha C ,$

$$
\operatorname { V a r } [ R _ { \alpha } ] = \operatorname { V a r } [ Y - \alpha C ]\tag{24}
$$

$$
= \operatorname { V a r } [ Y ] + \operatorname { V a r } [ \alpha C ] - 2 \operatorname { C o v } [ Y , \alpha C ]\tag{25}
$$

$$
= \mathrm { V a r } [ Y ] + \alpha ^ { 2 } \mathrm { V a r } [ C ] - 2 \alpha \mathrm { C o v } [ Y , C ] ,\tag{26}
$$

which proves the variance identity. Differentiating with respect to α gives

$$
{ \frac { \partial } { \partial \alpha } } \mathrm { V a r } [ R _ { \alpha } ] = 2 \alpha \mathrm { V a r } [ C ] - 2 \mathrm { C o v } [ Y , C ] .\tag{27}
$$

Because $\mathrm { V a r } [ C ] > 0$ , the unique stationary point is $\alpha ^ { \star } = \mathrm { C o v } [ Y , C ] / \mathrm { V a r } [ C ]$ , and the second derivative is $2 \mathrm { V a r } [ C ] > 0 .$ , so $\alpha ^ { \star }$ is the global minimizer.

For $\alpha = 1$

$$
\operatorname { V a r } [ Y - C ] - \operatorname { V a r } [ Y ] = \operatorname { V a r } [ C ] - 2 \operatorname { C o v } [ Y , C ] .\tag{28}
$$

Thus $\mathrm { C o v } [ Y , C ] > { \frac { 1 } { 2 } } \mathrm { V a r } [ C ]$ implies $\mathrm { V a r } [ Y - C ] < \mathrm { V a r } [ Y ]$ . If the condition holds for $d _ { \mathrm { r e a l } } ^ { \pi _ { \theta } } .$ almost every s, taking expectation over s preserves the strict inequality for the expected conditional variances. □

## A.4 Dual Clipping

Proposition A.2 (Bounded Dual-Clipped Surrogate). Suppose $| \hat { A } _ { t } ^ { \mathrm { g r } } | \leq A _ { \operatorname* { m a x } }$ for all t after clipping, $0 < \epsilon _ { \mathrm { c l i p } } < 1 , c > 1$ , and $\rho _ { t } ( \theta ) > 0$ . With $\ell _ { t } ( \theta )$ defined in Equation (8), define

$$
u _ { t } ( \theta ) = \mathrm { m a x } ( \ell _ { t } ( \theta ) , c \hat { A } _ { t } ^ { \mathrm { g r } } ) \mathbf { 1 } _ { \hat { A } _ { t } ^ { \mathrm { g r } } < 0 } + \ell _ { t } ( \theta ) \mathbf { 1 } _ { \hat { A } _ { t } ^ { \mathrm { g r } } \geq 0 } .\tag{29}
$$

Then, for every t,

$$
- c A _ { \mathrm { m a x } } \leq u _ { t } ( \theta ) \leq ( 1 + \epsilon _ { \mathrm { c l i p } } ) A _ { \mathrm { m a x } } .\tag{30}
$$

Proof. If $\hat { A } _ { t } ^ { \mathrm { g r } } \geq 0$ , then $u _ { t } ( \theta ) = \ell _ { t } ( \theta )$ . Since c $\begin{array} { r } { \mathrm { l i p } ( \rho _ { t } ( \theta ) , 1 - \epsilon _ { \mathrm { c l i p } } , 1 + \epsilon _ { \mathrm { c l i p } } ) \leq 1 + \epsilon _ { \mathrm { c l i p } } } \end{array}$ , the clipped surrogate satisfies

$$
\ell _ { t } ( \theta ) \leq ( 1 + \epsilon _ { \mathrm { c l i p } } ) \hat { A } _ { t } ^ { \mathrm { g r } } \leq ( 1 + \epsilon _ { \mathrm { c l i p } } ) A _ { \mathrm { m a x } } .\tag{31}
$$

Moreover $\ell _ { t } ( \theta ) \geq 0$ in this case, and therefore $- c A _ { \mathrm { m a x } } \leq u _ { t } ( \theta ) \leq ( 1 + \epsilon _ { \mathrm { c l i p } } ) A _ { \mathrm { m a x } } .$

If $\hat { A } _ { t } ^ { \mathrm { g r } } < 0$ , then $u _ { t } ( \theta ) = \mathrm { m a x } ( \ell _ { t } ( \theta ) , c \hat { A } _ { t } ^ { \mathrm { g r } } )$ . Since $c > 1$ and $\hat { A } _ { t } ^ { \mathrm { g r } } \geq - A _ { \operatorname* { m a x } }$ , we have $c \hat { A } _ { t } ^ { \mathrm { g r } } \geq$ $- c A _ { \mathrm { m a x } } , \mathrm { s o }$

$$
u _ { t } ( \theta ) \geq c \hat { A } _ { t } ^ { \mathrm { g r } } \geq - c A _ { \operatorname* { m a x } } .\tag{32}
$$

Both $\ell _ { t } ( \theta )$ and $c \hat { A } _ { t } ^ { \mathrm { g r } }$ are non-positive when $\hat { A } _ { t } ^ { \mathrm { g r } } < 0$ , hence $u _ { t } ( \theta ) \leq 0 \leq ( 1 + \epsilon _ { \mathrm { c l i p } } ) A _ { \mathrm { m a x } }$ . Combining the two cases proves the bound. □

## A.5 Residual Approximation Bias

Proof. From Equation (3), the real gradient can be written as

$$
g ( \theta ) = \mathbb { E } \Big [ \nabla _ { \theta } \log \pi _ { \theta } ( \tau \mid s ) \left( \Phi _ { \pi _ { \theta } } ( s , \tau ) + \Delta _ { \pi _ { \theta } } ( s , \tau ) \right) \Big ] .\tag{33}
$$

Subtracting this expression from the surrogate gradient in Equation (10) yields

$$
\begin{array} { r } { \widehat { g } ( \theta ) - g ( \theta ) = \mathbb { E } \Big [ \nabla _ { \theta } \log \pi _ { \theta } ( \tau \mid s ) \left( \widehat { \Delta } _ { \pi _ { \theta } } ( s , \tau ) - \Delta _ { \pi _ { \theta } } ( s , \tau ) \right) \Big ] . } \end{array}\tag{34}
$$

Let $X = \nabla _ { \theta }$ log $\pi _ { \boldsymbol { \theta } } ( \tau \mid s )$ and $e = \widehat { \Delta } _ { \pi _ { \theta } } ( s , \tau ) - { \Delta } _ { \pi _ { \theta } } ( s , \tau )$ . Jensen’s inequality gives

$$
\| \widehat { g } ( \theta ) - g ( \theta ) \| _ { 2 } = \| \mathbb { E } [ X e ] \| _ { 2 } \leq \mathbb { E } [ \| X \| _ { 2 } | e | ] .\tag{35}
$$

Applying Cauchy–Schwarz to the scalar random variables $\| X \| _ { 2 }$ and |e| gives

$$
\begin{array} { r } { \mathbb { E } [ \| X \| _ { 2 } | e | ] \le \big ( \mathbb { E } \| X \| _ { 2 } ^ { 2 } \big ) ^ { 1 / 2 } \big ( \mathbb { E } | e | ^ { 2 } \big ) ^ { 1 / 2 } , } \end{array}\tag{36}
$$

which proves Equation (11). $\operatorname { I f } \| X \| _ { 2 } \leq G _ { \nabla }$ almost surely, then $\left( \mathbb { E } \| X \| _ { 2 } ^ { 2 } \right) ^ { 1 / 2 } \leq G _ { \nabla }$ , yielding the bounded-gradient version. □

## B Bench2Drive Protocol

## B.1 Motivation for Adjustments

Closed-loop training imposes fundamentally different requirements on a benchmark than closed-loop evaluation. Beyond accurate assessment, training requires clear and informative failure signals, as well as visually and physically consistent environment dynamics across policy updates to avoid nonstationarity, together with high rollout efficiency. In particular, rollouts should terminate immediately upon meaningful failure events to provide concise supervision, and unnecessary criteria overhead should be minimized, as rollout time directly dictates training efficiency.

We therefore adopt a patched protocol, Bench2Drive<sup>∗</sup>, which preserves the route set, ego-policy interface, and core metrics, while mitigating scenario artifacts that introduce non-policy noise into both training and evaluation.

## B.2 Protocol-Level Adjustments

We apply six local adjustments to the official protocol.

• Actor cleanup. The official scenario manager can remove background or scenario-related actors at runtime, causing vehicles to disappear from the visual scene. We now clean up only background vehicles that block normal ego progress. Other nonblocking vehicles are kept in autopilot mode, and actors that would be removed immediately after spawning are skipped before they are spawned.

• Timeout handling. During both data collection and evaluation, we lower the upper bounds for scenario and route timeouts. This prevents a deadlocked route from consuming long simulator time after the policy has already produced the relevant failure signal.

• BicycleFlow spawning. We fix the BicycleFlow scenario so that cyclists are spawned only within the range specified by the scenario definition. The resulting flow follows normal behavior and avoids abnormal cyclist motion or collisions that are unrelated to the ego policy.

• Route 3749 actor flow. For route id 3749, we set the actor-flow speed to 12 m/s. This avoids an overly aggressive flow for the turning geometry, where the original setting could produce an invalid scene before the ego policy makes a meaningful decision.

• Collision termination. In both data collection and evaluation, a collision terminates the scene immediately. The original protocol may continue simulation after a collision; in BicycleFlow, for example, a cyclist can keep moving and generate repeated contacts from the same physical event. Early termination makes the failure state unambiguous and reduces noise in Driving Score. It may slightly lower Driving Score by removing post-collision driving segments, but it does not change Success Rate. We also ignore collision events with relative speed below 0.1 m/s to avoid duplicate contact records.

• Town07 stop sign. We ignore the invisible stop sign located at (0, 0, 0) in Town07. This removes spurious stop-sign violations caused by a map artifact rather than by policy behavior.

## B.3 Sanity Check Against Official Bench2Drive

The protocol adjustments aim to produce cleaner RL rollouts without altering the benchmark’s qualitative semantics. We therefore compare the official protocol with Bench2Drive<sup>∗</sup> across five representative policies.

• PDM-Lite [49] is a rule-based CARLA planner. It provides a nonlearned reference point whose behavior is driven by hand-designed planning logic rather than end-to-end perception and control.

• PlanT v2 [50] is a privileged planner with access to structured scene information. We include it to test whether the patched protocol remains consistent for high-performing planners that operate outside the sensor-only setting.

Table 4: Evaluation comparison between official Bench2Drive and Bench2Drive<sup>∗</sup>. Bench2Drive<sup>∗</sup> denotes the patched protocol used for cleaner and more efficient closed-loop training and evaluation. For Bench2Drive<sup>∗</sup>, results are reported as mean ± standard deviation over three random seeds.
<table><tr><td rowspan="2">Driving Policy</td><td rowspan="2">Benchmark</td><td colspan="2">Closed-loop Metrics</td><td colspan="6">Multi-Ability (%)</td></tr><tr><td>DS↑</td><td>SR (%) ↑</td><td>Merging ↑ Overtaking ↑ Emergency Brake ↑ Give Way ↑ Traffic Sign ↑</td><td></td><td></td><td></td><td></td><td>Mean ↑</td></tr><tr><td colspan="12">Rule-based Planner</td></tr><tr><td rowspan="3">PDM-Lite [49]</td><td>Bench2Drive</td><td>97.02</td><td>92.27</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Bench2Drive*</td><td></td><td></td><td>94.62 ± 0.59 88.48 ± 0.6986.30 ± 0.00 86.67 ± 2.25</td><td></td><td>98.87 ±0.98</td><td>73.33 ± 5.77</td><td>84.20 ± 2.10</td><td>85.83±1.25</td></tr><tr><td></td><td></td><td></td><td></td><td>Privileged Planner</td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="2">PlanTv2 [50]</td><td>Bench2Drive</td><td>92.40 ± 1.7083.80 ± 3.30|</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Bench2Drive*</td><td>84.61 ± 0.74 76.06± 0.6984.20 ± 0.69 56.30 ± 2.60</td><td></td><td></td><td></td><td>88.87 ± 0.98</td><td>16.67 ± 5.77</td><td>81.80 ± 1.21</td><td>65.53 ±1.35</td></tr><tr><td colspan="10"></td></tr><tr><td rowspan="2">UniAD [1]</td><td>Bench2Drive</td><td>45.81</td><td></td><td></td><td>End-to-End method</td><td></td><td></td><td></td><td></td></tr><tr><td>Bench2Drive*</td><td>45.74± 0.6020.00± 0.7922.90± 0.69</td><td>16.36</td><td></td><td>26.67 ± 6.65</td><td>15.00 ± 0.00</td><td>30.00 ± 10.00</td><td>4.90 ± 1.21</td><td>19.90 ± 1.01</td></tr><tr><td rowspan="2">VAD [2]</td><td>Bench2Drive</td><td>42.35</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Bench2Drive*</td><td>44.25 ± 0.67 16.06 ± 0.9512.13 ± 1.44</td><td>15.00</td><td></td><td>5.93 ± 3.42</td><td>30.53 ±2.54</td><td>30.00 ± 10.00</td><td>2.47 ± 0.64</td><td>16.23 ± 1.38</td></tr><tr><td rowspan="2">SparseDrive [3]</td><td>Bench2Drive</td><td>44.54</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Bench2Drive*</td><td></td><td>16.71</td><td>44.21 ±0.43 19.55 ±0.4514.63 ± 1.44 19.30±6.41</td><td></td><td>28.33 ±2.89</td><td>36.67±5.77</td><td>3.53 ± 1.63</td><td>20.47 ± 0.95</td></tr></table>

• UniAD [1] is a planning-oriented end-to-end driving system. We use it as a representative learned policy with integrated perception, prediction, and planning modules.

• VAD [2] is an end-to-end method based on vectorized scene representations. It offers a learned baseline with a different intermediate representation from UniAD while staying in the same sensor-driven evaluation regime.

• SparseDrive [3] is an end-to-end method built around sparse scene representations. It is included because its closed-loop scores are close to the regime studied in this paper and because CRAFT is evaluated on SparseDrive-style policies.

Together, these policies cover rule-based, privileged, and end-to-end settings, allowing us to check whether the patched protocol changes efficiency and rollout cleanliness without altering the broad ordering of representative methods.

Table 4 shows the expected pattern. The adjusted protocol is slightly stricter for strong planners, mainly because terminal events are handled more directly and avoidable post-failure rollout time is removed. For end-to-end methods, the ranking remains broadly stable. UniAD remains ahead of VAD and SparseDrive. Moreover, Bench2Drive<sup>∗</sup> produces substantially lower standard deviations than the official protocol, suggesting a more stable evaluation of closed-loop performance. This lower variance supports single-seed evaluation in the main experiments as a practical and cost-effective protocol for comparing relative method improvements under identical evaluation conditions. In practice, the shorter timeout and cleaner termination rules yield over 2× higher closed-loop training throughput and over 3× higher evaluation throughput. These efficiency gains are critical for reinforcement fine-tuning, where closed-loop rollout time is the primary bottleneck.

## C Algorithm Framework

Algorithm 1 gives the training procedure that instantiates the objective in Equation (14). The loop follows the separation used throughout the method section. At each closed-loop state, the policy scores a finite set of candidate trajectories, and only the selected trajectory is passed to the controller to produce the action executed in the real environment. The counterfactual world later evaluates the stored candidate set from the same visited state, where counterfactual returns provide groupnormalized counterfactual advantages without executing alternative candidates in CARLA. In parallel, the corrective reward is computed from the executed controller action and the resulting next state, then discounted, scaled, and clipped into the corrective advantage. The update combines the counterfactual advantage and corrective advantage with EMA teacher regularization, aligning the algorithm with the proxy-residual formulation in Section 3 and the implementation details reported below.

Algorithm 1 Counterfactual-to-Interactive Reinforcement Fine-Tuning (CRAFT)   
Require: Pre-trained driving policy $\pi _ { \theta _ { \mathrm { p r e } } } ,$ controller $\kappa ,$ closed-loop environment $\mathcal { M } _ { \mathrm { r e a l } } .$ , counter  
factual world $\mathcal E _ { \mathrm { c p } } .$ , rollout buffer size B, candidate group size G, weights $\lambda _ { \mathrm { c p } } , \lambda _ { \mathrm { g r } } , \beta _ { r } , \beta _ { f }$ , EMA   
momentum m   
Ensure: Fine-tuned policy $\pi _ { \theta }$   
1: Initialize $\theta  \theta _ { \mathrm { p r e } }$ and $\theta _ { T }  \theta _ { \mathrm { p r e } }$   
2: for training iteration $k = 1 , 2 , \ldots$ do   
3: Set $\bar { \theta _ { \mathrm { o l d } } }  \theta$ and clear $\boldsymbol { B }$   
4: while $| B | < B$ do   
5: Observe $s _ { t }$ and candidates $\{ \tau _ { t , g } \} _ { g = 1 } ^ { G }$   
6: Sample $\tau _ { t } \sim \pi _ { \theta _ { \mathrm { o l d } } } ( \cdot \perp s _ { t } )$ and execute $a _ { t } = \kappa ( s _ { t } , \tau _ { t } )$ ▷ closed-loop execution   
7: Observe $s _ { t + 1 } \tilde { \mathrm { \ a n d } } r _ { t } ^ { \mathrm { g r } } = r ^ { \mathrm { g r } } ( s _ { t } , a _ { t } , s _ { t + 1 } )$   
8: Store $( s _ { t } , \dot { \{ \tau _ { t , g } \} } _ { g = 1 } ^ { G } , \tau _ { t }$ , log $\dot { \pi } _ { \boldsymbol { \theta } _ { \mathrm { o l d } } } ( \tau _ { t } \mid \dot { s } _ { t } ) , r _ { t } ^ { \mathrm { g r } } )$ in B   
9: end while   
10: for each visited state $s _ { i }$ in B do   
11: Run $\mathcal E _ { \mathrm { c p } }$ on $\{ \tau _ { i , g } \} _ { g = 1 } ^ { \bar { G } }$ to obtain counterfactual returns $\tilde { R } _ { i , g }$ ▷ counterfactual reward   
12: Mask invalid candidates and normalize valid returns to $\tilde { A } _ { i , g }$ as in Equation (6)   
13: end for   
14: Compute $\mathcal { L } _ { \mathrm { c p } }$ using Equation (7)   
15: Discount corrective rewards with $\gamma _ { c } ,$ then scale and clip to $\hat { A } _ { t } ^ { \mathrm { g r } }$ ▷ corrective advantage   
16: Form $\rho _ { t } ( \theta ) = \pi _ { \theta } ( \tau _ { t } \mid s _ { t } ) / \pi _ { \theta _ { \mathrm { o l d } } } ( \tau _ { t } \mid s _ { t } )$ and compute $\hat { \mathcal { L } } _ { \mathrm { g r } }$ using Equations (8) and (9)   
17: Compute ${ \mathcal { L } } _ { \mathrm { d i s t } }$ and ${ \mathcal { L } } _ { \mathrm { K L } }$ using Equation (13) ▷ on-policy self-distillation   
18: Update trainable policy parameters by minimizing $\mathcal { L } _ { \mathrm { a l l } }$ in Equation (14)   
19: Update $\theta _ { T }  m \bar { \theta } _ { T } + \mathbf { \bar { ( 1 -  { m ) } } } \theta$   
20: end for   
21: return π

## D Implementation Details

This section records the implementation choices used in the experiments in Section 4. The main paper keeps the method description abstract; here we specify which policy parameters are updated, how candidate futures are simulated, and how the reward and optimization terms are instantiated.

## D.1 Compute Resources

Our experiments are conducted on a single server equipped with eight NVIDIA RTX 4090D GPUs. CRAFT uses an asynchronous collect-and-train pipeline, where rollout workers interact with CARLA and write synchronized rollout snapshots to a shared buffer. The trainer then waits until enough rollout files are ready and aggregates them into a rollout batch, preprocesses the counterfactual and corrective signals, and performs one Lightning<sup>1</sup> training iteration before releasing the collectors to continue with the updated policy version. Each driving policy uses four GPUs for closed-loop rollout collection and four GPUs for policy training; under this configuration, one complete fine-tuning run takes 6–10 hours, depending on the policy’s inference efficiency and the trainable modules. This design overlaps closed-loop data collection with policy optimization, which reduces idle time in the main training loop.

## D.2 Trainable Modules of Driving Policies

We fine-tune only the modules that score candidate trajectories. All perception, map construction, detection, motion prediction, and trajectory-generation modules remain frozen. This restriction keeps sparse online rewards close to the policy decision boundary. The update can change which trajectory candidate is preferred, but it does not rewrite the visual or geometric driving stack. Figure 7 illustrates the operational paradigms of these driving policies.

![](images/df7568f43e298e8f2a2bef9de1c18b522791838470867725e78159416ec99594.jpg)  
Figure 7: Operational paradigms of driving policies.

• HiP-AD [46]. The ego decision is represented as joint path-speed candidates with 48 ego modes. CRAFT and the non-PPO baselines update only the final classification branch in the last planrefinement layer. When PPO is used, a lightweight critic is trained in addition to this branch.

• MindDrive [24]. The high-level speed decision is chosen by a VLM decision expert before the policy generates the low-level path. Fine-tuning updates only the LoRA decision expert used for this high-level decision. The visual encoder, map and detection heads, language backbone, and action expert stay fixed. Under PPO, the critic is the only additional trainable component.

• SparseDriveV2<sup>†</sup> [22]. The policy scores a 512-mode trajectory vocabulary. Fine-tuning updates only the final trajectory classification branch that assigns probabilities to vocabulary candidates. The trajectory vocabulary, temporal queue, perception backbone, map head, detection head, and trajectory decoder remain frozen. PPO adds the critic, while all other fine-tuning methods update only the classification branch.

## D.3 Counterfactual World

The counterfactual world evaluates the policy candidate set at states visited by real closed-loop rollouts. For each observation, the Bench2Drive agent stores an auxiliary record containing candidate trajectories $\tau _ { 1 : G }$ in the local ego frame, candidate logits, the current ego state, nearby-agent states and actions, route geometry, scenario flags, and nearby map polygons. Ragged candidate counts, route lengths, and agent counts are padded into dense tensors with validity masks before simulation.

By default, each candidate is simulated with a batched trajectory tracker. The tracker prepends the current ego pose to each candidate trajectory, transforms the local trajectory into the global CARLA frame, and flattens the batch and candidate dimensions into independent tracking problems. At each virtual step, a PID controller tracks a short reference segment, and a kinematic bicycle model advances the ego state. Nearby agents use a decay rollout model in which their current actions are held for a short decision window. The model then reduces throttle and ramps up braking, with a shorter ramp when an agent is on a lane connector. Collision checks use rectangular vehicle footprint and batched separating-axis tests.

Table 5: Main implementation hyperparameters. The settings are shared across policies unless the table states otherwise. CRAFT uses the counterfactual reward for candidate scoring and the corrective reward for residual correction.
<table><tr><td>Component</td><td>Setting</td><td>Value</td></tr><tr><td>Trainer</td><td>Epochs per update round Optimizer Initial / minimum learning rate Weight decay Gradient clipping Precision / training devices Data decode workers Shared rollout discount GAE trace parameter</td><td>AdamW  $1 0 ^ { - 4 } / 5 { \times } 1 0 ^ { - 6 }$   $1 0 ^ { - 5 }$  Global norm 0.5  $3 2 { \mathrm { - b i t } } / 4 \mathrm { G P U s }$   $\gamma = 0 . 9 8$ </td></tr><tr><td>counterfactual world</td><td>EMA teacher momentum Rollout buffer size Tracker Virtual time step Rollout horizon Inference interval Chunk size Other-agent model Group normalization Std floor for group advantages</td><td> $\varepsilon _ { \mathrm { n o r m } } = 1 0 ^ { - 8 }$   $m = 0 . 9 9$   $B = 2 0 4 8$  transitions Batched PID trajectory tracker  $\Delta t = 0 . 1 \mathrm { s }$  H = 20 steps, 21 states including the current state 5 simulator frames 500 candidate rollouts Decay rollout with kinematic bicycle dynamics Mean/std within valid candidates  $\sigma _ { \mathrm { m i n } } = 5 . 0$ </td></tr><tr><td>Fine-tuning objectives PPO clip range</td><td>Grounded residual loss weight  $\lambda _ { \mathrm { g r } }$  Distillation weight  $\beta _ { r }$  Forward-KL weight  $\beta _ { f }$   $\epsilon _ { \mathrm { c l i p } }$  Dual-clip constant c Corrective discount  $\gamma _ { c }$  Corrective return scale</td><td>1.0 0.5 0.5 0.1 0.2 2.0 0.8  $S _ { \mathrm { g r } } = 8 . 0$ </td></tr></table>

The counterfactual return for candidate $g$ at real state $s _ { i }$ is

$$
\tilde { R } _ { i , g } = \sum _ { t = 0 } ^ { H - 1 } \gamma ^ { t } r _ { i , g , t } ^ { \mathrm { c p } } - \lambda _ { \mathrm { r e d } } ^ { \mathrm { c p } } I _ { i , g } ^ { \mathrm { r e d } } - \lambda _ { \mathrm { s t o p } } ^ { \mathrm { c p } } I _ { i , g } ^ { \mathrm { s t o p } } .\tag{37}
$$

The rollout horizon $H _ { \cdot }$ , simulator step $\Delta t ,$ and discount $\gamma$ are listed in Table 5; in this setting, the simulated rollout contains the current state plus H future states. Candidate returns are normalized within each valid group as follows:

$$
\mu _ { i } = \frac { 1 } { \left| G _ { i } \right| } \sum _ { g \in G _ { i } } \tilde { R } _ { i , g } , \qquad \sigma _ { i } = \operatorname* { m a x } \left( \sqrt { \frac { 1 } { \left| G _ { i } \right| } \sum _ { g \in G _ { i } } ( \tilde { R } _ { i , g } - \mu _ { i } ) ^ { 2 } } , \sigma _ { \operatorname* { m i n } } \right) ,\tag{38}
$$

$$
\tilde { A } _ { i , g } = \frac { \tilde { R } _ { i , g } - \mu _ { i } } { \sigma _ { i } } .\tag{39}
$$

Padded candidates are masked out and receive zero advantage. This is the group advantage used by GRPO and by the counterfactual proxy of CRAFT.

## D.4 Reward Design

The implementation uses two rewards. The counterfactual reward is a dense progress-and-infraction signal used to score candidate futures in the counterfactual world; PPO and REINFORCE++ use the closed-loop instance of the same dense design as their rollout reward. The corrective reward is a sparse safety signal used to instantiate grounded residual correction in CRAFT. The two rewards implement the counterfactual proxy and grounded residual correction, respectively. Both designs are inspired by the progress, route-adherence, and safety terms of CaRL [25].

Table 6: Reward hyperparameters. Superscripts distinguish the counterfactual proxy reward from the grounded residual corrective reward; these instantiate the dense counterfactual proxy and grounded residual correction, respectively.
<table><tr><td>Reward</td><td>Symbol</td><td>Value</td><td>Role</td></tr><tr><td rowspan="10">Counterfactual reward</td><td> $p _ { \operatorname* { m i n } } \mathrm { ~ / ~ } p _ { \operatorname* { m a x } }$   $w _ { \mathrm { p r o g } }$ </td><td>0.0 / 1.2</td><td>Progress clipping bounds</td></tr><tr><td></td><td>8.0</td><td>Progress weight</td></tr><tr><td> $w _ { g } \mathrm { ~ / ~ } w _ { c } \mathrm { ~ / ~ } w _ { h }$ </td><td>3.0 / 0.8 / 2.0</td><td>Route, centerline, and heading efficiency weights</td></tr><tr><td> $\eta _ { \mathrm { m i n } }$ </td><td>0.0</td><td>Minimum route-efficiency multiplier</td></tr><tr><td> $d _ { \mathrm { c l i p } }$ </td><td>0.10</td><td>Deviation-delta clipping bound</td></tr><tr><td> $\delta _ { g } ^ { \mathrm { r e c } } / \delta _ { c } ^ { \mathrm { r e c } }$ </td><td>0.08 / 0.08</td><td>Recovery activation thresholds</td></tr><tr><td> $\bar { k _ { g } } / k _ { c } / k _ { h }$ </td><td>0.4 / 0.2 / 0.4</td><td>Recovery weights</td></tr><tr><td> $c _ { \mathrm { c l i p } }$ </td><td>0.5</td><td>Recovery reward clipping bound</td></tr><tr><td> $a _ { \mathrm { { r e c } } } / b _ { \mathrm { { r e c } } }$  cp</td><td>0.5 / 0.5</td><td>Progress-dependent recovery scaling</td></tr><tr><td> $\lambda _ { \mathrm { o f f r o a d } }$ </td><td>1.5</td><td>Off-road step cost</td></tr><tr><td rowspan="10"></td><td> $\lambda _ { \mathrm { - } \mathrm { - } \mathrm { - } } ^ { \mathrm { c p } }$   $\boldsymbol { \mathscr { n } } _ { \mathrm { o p p } }$ </td><td>0.1</td><td>Opposite-lane step cost</td></tr><tr><td> $\lambda ^ { \mathrm { { c } \tilde { P } ^ { * } } }$   $\lambda _ { \mathrm { o f f r o u t e } }$ </td><td>1.5</td><td>Off-route step cost</td></tr><tr><td> $\lambda _ { \mathrm { - } \mathrm { ~ } \mathrm { ~ } \mathrm { ~ } } ^ { \mathrm { { c p } } }$   $\lambda _ { \mathrm { e m g } } ^ { - \mathrm { r } }$ </td><td>1.0</td><td>Emergency-lane step cost</td></tr><tr><td> $\lambda ^ { \bar { \mathbf { c } } \bar { \mathbf { p } } ^ { - } \bar { \mathbf { \Lambda } } ^ { \mathrm { e } } }$   $\hat { \mathbf { \xi } } _ { \mathrm { w } } \hat { \mathbf { \xi } } _ { \mathrm { c o l l } }$ </td><td>40.0</td><td>First-collision penalty</td></tr><tr><td> $\lambda _ { \infty , 1 } ^ { \mathrm { c p } }$ </td><td>40.0</td><td>Red-light trajectory penalty</td></tr><tr><td> $\therefore \mathrm { { \frac { r e d } { c p } } }$   $\lambda _ { \mathrm { s t o p } }$ </td><td>40.0</td><td>Stop-sign trajectory penalty</td></tr><tr><td></td><td></td><td></td></tr><tr><td> $\lambda _ { \mathrm { o f f r o a d } } ^ { \mathrm { g r } }$ </td><td>0.5 0.2</td><td>Off-road penalty Emergency-lane penalty</td></tr><tr><td> $\lambda _ { \mathrm { e m g } } ^ { \mathrm { g } \mathrm { \scriptscriptstyle { 1 } } }$  λgr</td><td></td><td></td></tr><tr><td> $\binom { \sim } { \textrm { o f f r o u t e } }$ </td><td>0.5</td><td>Off-route penalty</td></tr><tr><td rowspan="5">Corrective reward</td><td> $\lambda _ { \mathrm { r e d } } ^ { \mathrm { { s } ^ { \circ } } }$ </td><td>2.0</td><td>Red-light violation penalty</td></tr><tr><td> $\lambda _ { \mathrm { s t o p } } ^ { \mathrm { g r } }$ </td><td>2.0</td><td>Stop-sign violation penalty</td></tr><tr><td> $\lambda _ { \mathrm { c o l l } } ^ { \mathrm { g r } }$ </td><td>5.0</td><td>Collision penalty</td></tr><tr><td> $v _ { \mathrm { s t o p } }$ </td><td>0.1 m/s</td><td>Stop-required motion threshold</td></tr><tr><td> $v _ { \mathrm { g o } }$ </td><td>2.0 m/s</td><td>Go-required slow-motion threshold</td></tr></table>

Counterfactual reward. The counterfactual reward scores efficiency, route adherence, traffic-rule compliance, and collision safety for each simulated candidate. Progress is clipped and normalized as

$$
\bar { \Delta p } _ { t } = \mathrm { c l i p } ( \Delta p _ { t } , p _ { \operatorname* { m i n } } , p _ { \operatorname* { m a x } } ) , \qquad \Delta \hat { p } _ { t } = \frac { \bar { \Delta p } _ { t } } { p _ { \operatorname* { m a x } } } .\tag{40}
$$

The route-efficiency multiplier penalizes route, lane-center, and heading deviations as

$$
\eta _ { t } = \operatorname* { m a x } \bigl ( \exp ( - w _ { g } d _ { t } ^ { g } ) \exp ( - w _ { c } d _ { t } ^ { c } ) \exp ( - w _ { h } d _ { t } ^ { h } ) , \eta _ { \operatorname* { m i n } } \bigr ) .\tag{41}
$$

The recovery term rewards reductions in existing deviations through

$$
c _ { t } = { \bf 1 } [ d _ { t } ^ { g } > \delta _ { g } ^ { \mathrm { r e c } } ] k _ { g } ( - \bar { \Delta } d _ { t } ^ { g } ) + { \bf 1 } [ d _ { t } ^ { c } > \delta _ { c } ^ { \mathrm { r e c } } ] k _ { c } ( - \bar { \Delta } \bar { d } _ { t } ^ { c } ) + { \bf 1 } [ d _ { t } ^ { h } > \delta _ { c } ^ { \mathrm { r e c } } ] k _ { h } ( - \bar { \Delta } \bar { d } _ { t } ^ { h } ) ,\tag{42}
$$

$$
r _ { t } ^ { \mathrm { r e c } } = \mathrm { c l i p } \left( c _ { t } , - c _ { \mathrm { c l i p } } , c _ { \mathrm { c l i p } } \right) \left( a _ { \mathrm { r e c } } + b _ { \mathrm { r e c } } \Delta \hat { p } _ { t } \right) ,\tag{43}
$$

where each deviation delta is clipped to $[ - d _ { \mathrm { c l i p } } , d _ { \mathrm { c l i p } } ]$ . Table 6 reports separate route and centerline recovery thresholds; the heading recovery term intentionally reuses the centerline threshold because both deviations are activated at the same local-lane recovery boundary. The collision penalty is scaled by

$$
m _ { t } ^ { \mathrm { c o l l } } = 1 + \alpha _ { v } \mathrm { c l i p } \bigg ( \frac { v _ { t } } { v _ { \mathrm { r e f } } } , \nu _ { \mathrm { m i n } } , \nu _ { \mathrm { m a x } } \bigg ) .\tag{44}
$$

The counterfactual reward parameters are summarized in Table 6. The per-step counterfactual reward is

$$
\begin{array} { r l } & { r _ { t } ^ { \mathrm { { c p } } } = w _ { \mathrm { p r o g } } \Delta \hat { p } _ { t } \eta _ { t } + r _ { t } ^ { \mathrm { { r e c } } } - \lambda _ { \mathrm { o f f r o a d } } ^ { \mathrm { c p } } I _ { \mathrm { o f f r o a d } } - \lambda _ { \mathrm { o p p } } ^ { \mathrm { c p } } I _ { \mathrm { o p p o s i t e } } - \lambda _ { \mathrm { o f f r o u t e } } ^ { \mathrm { c p } } I _ { \mathrm { o f f r o u t e } } } \\ & { \phantom { x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x } } \\ & { \phantom { x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x } - \lambda _ { \mathrm { e m g } } ^ { \mathrm { c p } } I _ { \mathrm { e m e r g e n c y e n c t r o u t e } } } \end{array}\tag{45}
$$

In the counterfactual world, red-light and stop-sign violations are trajectory-level flags, giving the return-level penalties in Equation (37). The implementation applies these penalties at the first reward index of the simulated rollout. Collision cost is applied only at the first collision event for each candidate, so high-speed first impacts receive larger penalties.

Corrective reward. The corrective reward is intentionally sparse and safety centered. It is computed after the selected trajectory is converted by the controller into the action actually executed in CARLA, not from alternative virtual candidates:

$$
\begin{array} { r } { r _ { t } ^ { \mathrm { g r } } = - \lambda _ { \mathrm { o f f r o a d } } ^ { \mathrm { g r } } I _ { \mathrm { o f f r o a d } } - \lambda _ { \mathrm { e m g } } ^ { \mathrm { g r } } I _ { \mathrm { e m e r g e n c y } } - \lambda _ { \mathrm { o f f r o u t e } } ^ { \mathrm { g r } } I _ { \mathrm { o f f r o u t e } } - \lambda _ { \mathrm { r e d } } ^ { \mathrm { g r } } I _ { \mathrm { r e d } } } \\ { - \lambda _ { \mathrm { s t o p } } ^ { \mathrm { g r } } I _ { \mathrm { s t o p } } - \lambda _ { \mathrm { c o l l } } ^ { \mathrm { g r } } I _ { \mathrm { c o l l i s i o n } } . \qquad } \end{array}\tag{46}
$$

The traffic-light and stop-sign terms distinguish uncontrolled zones, stop-required zones, and gorequired zones. In a stop-required zone, moving faster than $v _ { \mathrm { s t o p } }$ is penalized; in a go-required zone, the wrapper checks whether the path ahead is clear before penalizing motion below $v _ { \mathrm { g o } }$

## D.5 Fine-tuning Baselines

The fine-tuners differ in how they consume closed-loop and counterfactual signals. PPO and RE-INFORCE++ use the dense progress-and-infraction reward on executed rollouts, GRPO uses only counterfactual advantages, and CRAFT combines the counterfactual proxy with the corrective reward.

PPO baseline. PPO is the only compared fine-tuner that trains a critic. The datamodule computes generalized advantage estimates with discount $\gamma$ and trace parameter $\lambda _ { \mathrm { G A E } }$

$$
\delta _ { t } = r _ { t } + \gamma u _ { t } ^ { \mathrm { t e r m } } V ( s _ { t + 1 } ) - V ( s _ { t } ) , \qquad A _ { t } = \delta _ { t } + \gamma \lambda _ { \mathrm { G A E } } u _ { t } ^ { \mathrm { d o n e } } A _ { t + 1 } .\tag{47}
$$

Here $u _ { t } ^ { \mathrm { t e r m } }$ is the continuation mask for value bootstrapping after terminal states, and $u _ { t } ^ { \mathrm { d o n e } }$ is the continuation mask for recursive return or advantage computation after episode boundaries. The policy loss uses the standard clipped ratio with range $\epsilon _ { \mathrm { c l i p } }$ , and the value loss uses a clipped SmoothL1 target with value-clip range $\epsilon _ { v }$ . The critic parameter group uses the actor learning rate multiplied by $\kappa _ { v }$

REINFORCE++ baseline. This value-free baseline removes the critic and uses normalized Monte Carlo returns from the executed rollout,

$$
G _ { t } = r _ { t } + \gamma u _ { t } ^ { \mathrm { d o n e } } G _ { t + 1 } , \qquad A _ { t } = \frac { G _ { t } - \mu _ { G } } { \sigma _ { G } + \varepsilon _ { \mathrm { n o r m } } } .\tag{48}
$$

It then uses the same selected-trajectory clipped ratio as PPO, with the shared clip range $\epsilon _ { \mathrm { c l i p } }$

GRPO baseline. This group-relative baseline discards the closed-loop rollout reward and optimizes the normalized counterfactual advantages in Equation (39). For valid candidates, its objective is

$$
\mathcal { L } _ { \mathrm { G R P O } } = - \mathbb { E } _ { i } \left[ \sum _ { g \in G _ { i } } \pi _ { \theta } ( \tau _ { g } \mid s _ { i } ) \tilde { A } _ { i , g } \right] + \beta _ { r } \mathcal { L } _ { \mathrm { d i s t } } + \beta _ { f } \mathcal { L } _ { \mathrm { K L } } ,\tag{49}
$$

where $\beta _ { r }$ and $\beta _ { f }$ are the regularization weights in Table 5.

CRAFT. The full method keeps the same counterfactual proxy as GRPO, but adds a selectedtrajectory update weighted by the corrective reward observed after closed-loop execution. The corrective return is

$$
G _ { t } ^ { \mathrm { g r } } = { r _ { t } ^ { \mathrm { g r } } } + \gamma _ { c } u _ { t } ^ { \mathrm { d o n e } } G _ { t + 1 } ^ { \mathrm { g r } } ,\tag{50}
$$

and the implementation scales and clips it as

$$
\hat { A } _ { t } ^ { \mathrm { g r } } = \mathrm { c l i p } \left( \frac { G _ { t } ^ { \mathrm { g r } } } { S _ { \mathrm { g r } } } , A _ { \mathrm { m i n } } , A _ { \mathrm { m a x } } \right) .\tag{51}
$$

Let $\tau _ { t }$ be the selected trajectory at $s _ { t }$ and $a _ { t } = \kappa ( s _ { t } , \tau _ { t } )$ be the executed controller action. The likelihood ratio is $\rho _ { t } = \exp ( \log \pi _ { \boldsymbol { \theta } } ( \tau _ { t } \mid s _ { t } ) - \log \pi _ { \mathrm { o l d } } ( \tau _ { t } \mid s _ { t } ) )$ ). The grounded residual correction objective uses PPO clipping followed by dual clipping:

$$
o _ { t } ^ { \operatorname* { m i n } } = \operatorname* { m i n } \Bigl ( \rho _ { t } \hat { A } _ { t } ^ { \mathrm { g r } } , \mathrm { c l i p } ( \rho _ { t } , 1 - \epsilon _ { \mathrm { c l i p } } , 1 + \epsilon _ { \mathrm { c l i p } } ) \hat { A } _ { t } ^ { \mathrm { g r } } \Bigr ) ,\tag{52}
$$

$$
o _ { t } = \left\{ \begin{array} { l l } { \operatorname* { m a x } ( o _ { t } ^ { \mathrm { m i n } } , c \hat { A } _ { t } ^ { \mathrm { g r } } ) , } & { \hat { A } _ { t } ^ { \mathrm { g r } } < 0 , } \\ { o _ { t } ^ { \mathrm { m i n } } , } & { \hat { A } _ { t } ^ { \mathrm { g r } } \geq 0 , } \end{array} \right.\tag{53}
$$

The implemented CRAFT loss is

$$
\begin{array} { r } { \mathcal { L } _ { \mathrm { C R A F T } } = \lambda _ { \mathrm { c p } } \mathcal { L } _ { \mathrm { c p } } + \lambda _ { \mathrm { g r } } \mathcal { L } _ { \mathrm { g r } } + \beta _ { r } \mathcal { L } _ { \mathrm { d i s t } } + \beta _ { f } \mathcal { L } _ { \mathrm { K L } } , } \end{array}\tag{54}
$$

where $\lambda _ { \mathrm { c p } } , \lambda _ { \mathrm { g r } } , \beta _ { r }$ , and $\beta _ { f }$ are set as in Table 5.

Teacher regularization. All reported fine-tuners keep a teacher initialized from the pre-trained actor. For the trainable actor subset, the teacher is updated by EMA,

$$
\theta _ { T } \gets m \theta _ { T } + ( 1 - m ) \theta .\tag{55}
$$

The distillation term is $D _ { \mathrm { K L } } ( \pi _ { \boldsymbol { \theta } } \Vert \pi _ { T } )$ , and the optional forward-KL term is $D _ { \mathrm { K L } } ( \pi _ { T } \Vert \pi _ { \theta } )$ . The ego configurations enable the forward-KL term for all reported fine-tuners.