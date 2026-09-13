# RiskWorld: Object-Centric Latent World Modeling for Autonomous Driving Risk Identification

Jingzheng Li<sup>1</sup>, Yufei Ge<sup>2</sup>, Qianren Mao, <sup>1</sup>, Zhijun Chen<sup>3</sup>, Bing Li<sup>4</sup>, Xingyu Peng<sup>1,5</sup>,

Baochang Zhang<sup>1,5</sup>, Xianglong Liu<sup>1,5</sup>

<sup>1</sup>Zhongguancun Laboratory, Beijing, China

<sup>2</sup>Tianjin University, Beijing, China

<sup>3</sup>Hong Kong Polytechnic University, Hong Kong, China

<sup>4</sup>Nanyang Technological University, Singapore

<sup>5</sup>Beihang University, Beijing, China

## Abstract

Autonomous driving risk identification aims to determine which observed object is likely to become safety-critical to the ego vehicle. Existing approaches typically predict scene-level accidents, infer risk objects indirectly from ego behavior, or apply geometric checks after trajectory forecasting, without directly using predicted ego–object relations for risk-source localization. We propose RiskWorld, an object-centric latent world model that identifies risk from the imagined evolution of each candidate relative to the ego vehicle. RiskWorld combines pretrained predictive video representations with structured ego–object histories, contextualizes observed interactions, and rolls relation-aware object states into the future using RSSM-style latent dynamics. It decodes the rollout into object-level risk scores, supported by auxiliary future-relation and temporal-risk predictions. Inference uses only observations up to the current time, while logged futures provide training supervision. On RiskBench, RiskWorld achieves the best overall F1 of 63.0% and the lowest false-alarm rate of 2.1%. Further analyses show that the learned rollout captures the evolution of object-level risk before critical events, while RiskWorld’s selections preserve planning-critical information under filtered observation.

## Introduction

Safe autonomous driving requires a risk monitor that can answer a question beyond generic scene understanding: among surrounding trafic participants and obstacles, which object is likely to become safety-critical to the ego vehicle? This decision is needed before a collision, near miss, or evasive maneuver becomes visually obvious. For example, a static obstacle may be harmless until the ego path converges with it, whereas a pedestrian that appears safe in the current frame may become critical under future motion. Driving risk is therefore object-specific and temporally evolving, and reliable localization should be grounded in how each candidate’s relation to the ego vehicle is expected to develop.

Existing methods mainly follow three paradigms. Accident anticipation methods estimate scene-level crash likelihood from dashcam videos (Liao et al. 2024; Goldshmidt et al. 2025); recent advances further predict future accident occurrence (Zhao et al. 2025), forecast future latent scene representations (Caselli et al. 2026), or regularize the temporal evolution of risk scores (Zou et al. 2026). Behavior-based methods infer risky objects indirectly from ego reactions such as braking or stopping (Li et al. 2020; Li, Chan, and Chen 2020). Trajectory-geometric methods predict future motion and then apply distance, overlap, or collision rules to select a risk source (Marchetti et al. 2020; Zhou et al. 2023). These paradigms provide complementary signals, but future reasoning remains weakly coupled to object-level risk localization: accident predictors are largely scene-level, behavior-based localization is indirect, and trajectory-based risk is usually decided after forecasting. In particular, objectconditioned future ego–object relations are not directly optimized as predictive evidence for risk-source identification. Figure 1 contrasts these paradigms with our formulation.

![](images/d25a662b4ebd6684610e212a13f6d7ae41a304e54fcbee7f2394d27cec4c55f9.jpg)  
Figure 1: Existing approaches predict scene-level risk, infer risk objects from ego behavior, or apply post-hoc geometric checks. RiskWorld instead predicts object-conditioned future ego–object relations and uses them to identify the risk source.

We take a diferent view: risk is not a static visual attribute but the outcome of an evolving ego–object relation. An object becomes safety-critical when its relative motion, distance, path conflict, or interaction with the ego vehicle trends toward an unsafe state. A risk monitor should therefore predict object-conditioned future relations before assigning object-level risk.

World models and predictive representations provide a natural mechanism for this formulation. Recent driving world models roll compact scene states forward to forecast occupancy, point clouds, videos, or controllable scene evolution (Yang et al. 2025, 2024; Min et al. 2024; Gao et al. 2024; Wang et al. 2024; Zheng et al. 2024b). Their endpoints, however, are typically generation, simulation, occupancy forecasting, representation learning, or planning. Object-level risk identification instead calls for task-oriented latent prediction: rolling compact object states forward under ego–object relation and risk supervision rather than reconstructing an entire future scene.

We propose RiskWorld, a task-oriented latent world model for object-level driving risk identification. RiskWorld adapts pretrained predictive video representations (Bardes et al. 2024; Assran et al. 2025), combines them with structured ego–object histories, and constructs relation-aware object states. RSSM-style latent dynamics (Hafner et al. 2025) roll these states into the future, while relation and risk decoders produce object risk scores together with auxiliary futurerelation and temporal-risk predictions. Inference uses only current and historical observations.

Our contributions are:

• We formulate object-level driving risk identification as future ego–object relation rollout, using predicted relation evolution as evidence for localizing the risk source.

• We propose RiskWorld, an object-centric latent world model that combines pretrained predictive video representations, relation-aware scene encoding, RSSM-style latent dynamics, and risk-oriented supervision.

• On RiskBench, RiskWorld improves overall F1 by 1.2 points over the strongest baseline and achieves the lowest FA of 2.1%; additional analyses examine temporal separation and planning relevance.

## Related Work

## Risk Identification and Accident Anticipation

Accident anticipation predicts impending collisions from observed dashcam video. Early methods estimate scene-level risk with spatiotemporal or agent-centric attention (Chan et al. 2016; Zeng et al. 2017; Liao et al. 2024). BADAS adapts predictive video representations to ego-centric collision prediction, and BADAS-2.0 scales this framework with real-time object-centric explanations (Goldshmidt et al. 2025, 2026). Recent methods make the temporal target more explicit: TOP predicts accident scores at multiple future horizons, FLaRA classifies predicted future latent representations, and RiskProp propagates collision-anchored supervision to learn temporally structured risk scores (Zhao et al. 2025; Caselli et al. 2026; Zou et al. 2026). These works establish futureaware accident anticipation, but their primary prediction remains a scene-level collision score; object attention provides explanatory evidence rather than an object-risk target.

Object-level risk identification instead asks which participant constitutes the risk source. Behavior-based approaches such as BP, BCP, and DROID infer risky objects from predicted ego behavior, while RiskBench standardizes localization, anticipation, and planning-aware evaluation across scenario types (Li et al. 2020; Li, Chan, and Chen 2020, 2023; Kung et al. 2024). Motion forecasting ofers another route by predicting agent trajectories followed by distance or collision checks (Marchetti et al. 2020; Zhou et al. 2023); MC-Risk extends this route with planner-aligned analytic risk fields on the RiskBench collision subset (Link et al. 2026). Conformal Risk Tube Prediction (CRTP) instead predicts calibrated object-level risk intervals under spatiotemporal uncertainty (Fu and Chen 2026). RiskWorld addresses a complementary gap: it learns object-conditioned latent dynamics supervised by future ego-relative geometry and decodes risk-source scores from the resulting relation rollout.

## World Models and Predictive Representations

World models learn predictive states that can be rolled forward. PlaNet introduced the recurrent state-space model (RSSM), which combines deterministic recurrent and stochastic latent states, and DreamerV3 extends this family to imagination-based control across domains (Hafner et al. 2019, 2025). In parallel, V-JEPA and V-JEPA2 learn predictive video representations by forecasting latent targets rather than reconstructing future pixels (Bardes et al. 2024; Assran et al. 2025). RiskWorld draws on these complementary ideas: frozen predictive visual features encode the observed context, while RSSM-style dynamics roll object states forward.

Driving world models instantiate future prediction through occupancy and flow (Zheng et al. 2024a; Yang et al. 2025), visual point clouds and 4D scene representations (Yang et al. 2024; Min et al. 2024), or controllable video generation (Wang et al. 2024; Gao et al. 2024). Latent models such as LAW and World4Drive predict future representations to support trajectory generation or selection (Li et al. 2025; Zheng et al. 2025), whereas DriveLaW connects video generation and motion planning through a shared latent world (Xia et al. 2026). Their primary endpoints are scene forecasting, generation, simulation, or planning. RiskWorld instead specializes latent rollout for object-level risk-source identification, with future relation and temporal targets providing task-oriented supervision and evidence.

## Method: RiskWorld

## Problem Formulation

At frame $t ,$ RiskWorld observes a K-frame history $\mathcal { H } _ { t }$ comprising front-view RGB, tracked object states, and ego motion. Let $\mathcal { O } _ { t } = \{ o _ { t } ^ { 1 } , . . . , o _ { t } ^ { N } \}$ } be the current candidates and $\nu _ { t } ^ { i } \in \{ 0 , 1 \}$ their validity indicators. For each valid candidate, $y _ { t } ^ { i }$ indicates whether it is the ego-relevant risk object, and RiskWorld estimates

$$
r _ { t } ^ { i } = \mathrm { P r } ( y _ { t } ^ { i } = 1 \mid \mathcal { H } _ { t } , \mathcal { O } _ { t } ) .\tag{1}
$$

Rather than judging risk from frame $t$ alone, the model obtains $r _ { t } ^ { i }$ from an H-step latent rollout of future ego–object

![](images/07283480018466ada8f138896fee2016cb02ad20d855c146336b8940a13239e9.jpg)  
Figure 2: Overview of RiskWorld. Observed RGB frames, object tracks, and ego motion are encoded into relation-aware object states, rolled forward with object-wise RSSM-style latent dynamics, and decoded into risk-source scores with auxiliary futurerelation and temporal-risk predictions. Future annotations supervise training only; inference uses observed history.

relations. Logged future annotations supervise this rollout during training but are never used as inference inputs.

## Overview

Figure 2 summarizes four stages. A frozen V-JEPA2 encoder extracts predictive scene context, while a structured state encoder preserves explicit object and ego motion. Fusion and masked relation attention produce one contextualized token per candidate. An object-wise latent dynamics module, following an RSSM-style deterministic–stochastic design, then rolls each token into a latent future. Finally, step-wise heads decode future relation and risk trajectories, while the pooled future state produces the object risk score; minimum distance and time-to-risk are derived from the decoded trajectories.

## Object-Centric World Representation

Scene encoding. A frozen V-JEPA2 encoder $\Phi _ { \mathrm { w } }$ processes the observed clip $I _ { t - K + 1 : t } ,$ with current boxes $B _ { t }$ guiding object-level feature pooling. Averaging its spatiotemporal tokens gives a global scene feature $s _ { t } ,$ while box pooling over the final temporal grid gives an object-aligned feature $v _ { t } ^ { i . } \mathrm { : }$

$$
( s _ { t } , \{ v _ { t } ^ { i } \} _ { i = 1 } ^ { N } ) = \Phi _ { \mathrm { w } } ( I _ { t - K + 1 : t } , B _ { t } ) .\tag{2}
$$

These frozen features contribute appearance, layout, and motion context learned through predictive pretraining without reconstructing future pixels.

Object-state encoding. A multilayer perceptron (MLP) encodes each candidate’s current ego-relative state, including position, motion, box geometry, and category, while a masked gated recurrent unit (GRU) summarizes its observed track history. Fusing the two gives a structured object feature $e _ { t } ^ { i } ;$ the same encoder produces an ego-motion feature $e _ { t } ^ { \mathrm { e g o } }$

Object-scene relational fusion. A shared fusion MLP projects and combines $( e _ { t } ^ { i } , v _ { t } ^ { i } , s _ { t } )$ into an object token $\boldsymbol { x } _ { t } ^ { i } ,$ while $( e _ { t } ^ { \mathrm { e g o } } , s _ { t } )$ gives an ego token $\boldsymbol x _ { t } ^ { \mathrm { e g o } }$ . Masked multi-head self-attention, denoted Rel $\mathrm { A t t n } .$ then models ego–object and object–object interactions:

$$
\left[ \widetilde { x } _ { t } ^ { 1 } , \dots , \widetilde { x } _ { t } ^ { N } \right] = \mathrm { R e l A t t n } \big ( \left[ x _ { t } ^ { \mathrm { e g o } } , x _ { t } ^ { 1 } , \dots , x _ { t } ^ { N } \right] , \left[ 1 , \nu _ { t } ^ { 1 } , \dots , \nu _ { t } ^ { N } \right] \big ) .\tag{3}
$$

The second argument is the validity mask, and the outputs $\{ \tilde { x } _ { t } ^ { i } \} _ { i = 1 } ^ { N }$ are relation-aware object tokens used to initialize the latent rollout.

## Object-Wise Latent Future Rollout

Object-wise latent state. Rather than generating future images, RiskWorld adopts an RSSM-style dynamics design to evolve each relation-aware object token in a compact latent space. A learned initializer first maps $\tilde { x } _ { t } ^ { i }$ to a deterministic state:

$$
h _ { \mathrm { i n i t } } ^ { i } = f _ { \mathrm { i n i t } } ( \tilde { x } _ { t } ^ { i } ) .\tag{4}
$$

The latent dynamics combines a deterministic recurrent state h with a stochastic state $z ,$ and the GRU integrates z into h at each step. At the observed boundary, the posterior $q _ { \phi }$ grounds $z _ { 0 } ^ { i }$ in the object token, while the prior p<sub>θ</sub> predicts it from $h _ { \mathrm { i n i t } } ^ { i }$ alone. The initial latent state is

$$
z _ { 0 } ^ { i } \sim q _ { \phi } ( z _ { 0 } ^ { i } \mid h _ { \mathrm { i n i t } } ^ { i } , \tilde { x } _ { t } ^ { i } ) , \ h _ { 0 } ^ { i } = \mathrm { G R U } ( z _ { 0 } ^ { i } , h _ { \mathrm { i n i t } } ^ { i } ) .\tag{5}
$$

Here $\phi$ and $\theta$ parameterize diagonal-Gaussian posterior and prior distributions whose means and scales are predicted from their conditioning states.

Future relation rollout. Starting from the observationgrounded state $h _ { 0 } ^ { i }$ , RiskWorld recursively predicts H future latent states using only the learned prior:

$$
\begin{array} { r l } & { z _ { k } ^ { i } \sim p _ { \theta } ( z _ { k } ^ { i } \mid h _ { k - 1 } ^ { i } ) , } \\ & { h _ { k } ^ { i } = \mathrm { G R U } ( z _ { k } ^ { i } , h _ { k - 1 } ^ { i } ) , \quad k = 1 , \dots , H . } \end{array}\tag{6}
$$

The sequence $\{ h _ { k } ^ { i } \} _ { k = 1 } ^ { H }$ represents the imagined evolution of object i relative to the ego vehicle. No future observation is provided, and dynamics parameters are shared across candidates; observed interaction context is encoded in $\tilde { x } _ { t } ^ { i }$

Latent regularization. We regularize the observationconditioned posterior toward the initial prior using

$$
\mathcal { L } _ { k l } = \mathbb { E } _ { i : \nu _ { t } ^ { i } = 1 } \mathrm { K L } \big [ q _ { \phi } ( z _ { 0 } ^ { i } \mid h _ { \mathrm { i n i t } } ^ { i } , \tilde { x } _ { t } ^ { i } ) \mid \mid p _ { \theta } ( z _ { 0 } ^ { i } \mid h _ { \mathrm { i n i t } } ^ { i } ) \big ] .\tag{7}
$$

This term prevents an unconstrained posterior and stabilizes latent initialization. Since the current object token is observed at inference, we initialize with the posterior mean and subsequently roll forward using prior means; stochastic samples are used during training.

## Risk-Aware Decoding and Learning

Risk and relation decoding. A shared step-wise head $f _ { \mathrm { s t e p } }$ maps every future state to ego-relative position $\hat { \mathbf { p } } _ { t + k } ^ { i }$ , distance $\hat { d } _ { t + k } ^ { i } ,$ , and temporal risk probability $\hat { R } _ { t + k } ^ { i } . \mathrm { ~ A ~ }$ horizonlevel head $f _ { \mathrm { p o o l } }$ predicts the object risk score from the mean future state $\begin{array} { r } { \dot { \bar { h } } _ { t } ^ { i } = H ^ { - 1 } \sum _ { k = 1 } ^ { H } h _ { k } ^ { i } } \end{array}$

$$
\begin{array} { r } { ( \hat { \mathbf { p } } _ { t + k } ^ { i } , \hat { d } _ { t + k } ^ { i } , \hat { R } _ { t + k } ^ { i } ) = f _ { \mathrm { s t e p } } ( h _ { k } ^ { i } ) , } \\ { r _ { t } ^ { i } = f _ { \mathrm { p o o l } } ( \bar { h } _ { t } ^ { i } ) . } \end{array}\tag{8}
$$

The score $r _ { t } ^ { i }$ identifies which object is risky and is supervised by $y _ { t } ^ { i }$ using class-balanced binary cross entropy $\mathcal { L } _ { o b j }$ . The step-wise outputs describe when risk emerges and how the underlying ego–object relation evolves; minimum distance and time-to-risk are derived from these trajectories rather than predicted separately.

Future-relation supervision. Logged ego and object tracks provide future ego-relative position and distance targets $\mathbf { p } _ { t + k } ^ { i , * }$ and $d _ { t + k } ^ { i , * }$ . Over valid future steps, ${ \hat { d } } _ { \operatorname* { m i n } , t } ^ { i } \ =$ min<sub>k</sub> $\mathrm { ~ , ~ } \hat { d } _ { t + k } ^ { i }$ and $d _ { \operatorname* { m i n } , t } ^ { i , * } ~ = ~ \operatorname* { m i n } _ { k } d _ { t + k } ^ { i , * }$ . Smooth- $. L _ { 1 }$ regression on position, distance, and the derived minimum distance gives $\mathcal { L } _ { x y } , \mathcal { L } _ { d i s t }$ , and ${ \mathcal { L } } _ { m i n }$ , respectively. These targets encourage the latent rollout to preserve the geometry most relevant to risk.

Temporal-risk supervision. Let $i ^ { * }$ be the annotated risk object and $[ a , b ]$ its event interval, with $a = b$ for a point event. We define

$$
R _ { t + k } ^ { i , * } = \left\{ \begin{array} { l l } { \displaystyle \mathrm { e x p } \bigg [ - \frac { ( a - ( t + k ) ) _ { + } } { T } \bigg ] , } & { i = i ^ { * } , a - H \leq t + k \leq b , } \\ { 0 , } & { \mathrm { o t h e r w i s e , } } \end{array} \right.\tag{9}
$$

where $( u ) _ { + } = \operatorname* { m a x } ( u , 0 )$ and $T$ controls temporal decay. The curve rises toward a, remains one over an annotated behavior interval, and is zero for other objects. Class-balanced binary cross entropy between $\hat { R } _ { t + k } ^ { i }$ and $R _ { t + k } ^ { i , * }$ defines $\mathcal { L } _ { c u r v e } .$ Time-to-risk is obtained from the first crossing of the same predicted curve:

$$
\widehat { \mathrm { T T R } } _ { t } ^ { i } = \Delta t \operatorname* { m i n } \{ k : \hat { R } _ { t + k } ^ { i } \geq \gamma _ { \mathrm { t t r } } \} ,\tag{10}
$$

where $\Delta t$ is the duration of one rollout step. No value is returned if the predicted curve does not cross γ<sub>ttr</sub>.

Joint objective and inference. Combining the losses introduced above gives

$$
\begin{array} { r } { \begin{array} { r l } & { \mathcal { L } = \lambda _ { o b j } \mathcal { L } _ { o b j } + \lambda _ { x y } \mathcal { L } _ { x y } + \lambda _ { d i s t } \mathcal { L } _ { d i s t } + \lambda _ { m i n } \mathcal { L } _ { m i n } } \\ & { ~ + ~ \lambda _ { c u r v e } \mathcal { L } _ { c u r v e } + \beta \mathcal { L } _ { k l } , } \end{array} } \end{array}\tag{11}
$$

where validity masks restrict each term to available objects and future steps, the λ coeficients balance the supervised targets, and $\bar { \beta }$ weights latent regularization. At inference, RiskWorld thresholds $r _ { t } ^ { i }$ to identify risky objects; the relation trajectory, risk curve, minimum distance, and curve-derived time-to-risk provide object-specific future evidence.

## Experiments

We organize the evaluation around four research questions. RQ1: How efectively does RiskWorld localize risk sources across diverse driving scenarios compared with existing approaches? RQ2: Does RiskWorld capture how object-level risk evolves over the future horizon and distinguish the risk source before a critical event? RQ3: How do predictive world features, relational reasoning, latent rollout, and future supervision contribute to performance? RQ4: Do the objects selected by RiskWorld preserve planning-critical information when all other objects are masked?

## Experimental Setup

Dataset and protocol. We evaluate on RiskBench (Kung et al. 2024), which contains 6,916 CARLA scenarios spanning interactive conflicts, collisions, static obstacles, and non-interactive driving. We use its map-based train/validation/test split and front-view setting. Each input comprises RGB history, object boxes and tracks, and ego motion. Logged future tracks and event annotations supervise training only; test-time prediction is strictly causal and evaluated at every frame.

Baselines. We compare random and fixed-range rules; trajectory methods using Kalman filtering, Social-GAN, MANTRA, and QCNet (Kalman 1960; Gupta et al. 2018; Marchetti et al. 2020; Zhou et al. 2023); and visual/behavior methods DSA, RRL, BP, and BCP (Chan et al. 2016; Zeng et al. 2017; Li et al. 2020; Li, Chan, and Chen 2020). TOP, BADAS, FLaRA, and RiskProp predict scene-level risk and are not directly comparable under the object-level protocol (Zhao et al. 2025; Goldshmidt et al. 2025; Caselli et al. 2026; Zou et al. 2026). We therefore adapt BADAS and FLaRA: BADAS<sup>∗</sup> adds an object-risk head to predictive video features, whereas FLaRA<sup>∗</sup> pools future latent tokens within each candidate box for object-risk classification. Both are trained and evaluated under the same protocol as RiskWorld.

Metrics. We report precision, recall, and overall micro-F1 for risk-source localization. Progressive Increasing Cost (PIC) assigns increasing weight to frame-level localization errors as the critical frame approaches, while the false-alarm rate (FA) is measured on non-interactive scenes. Future-risk prediction is evaluated using the horizon-wise Brier score, where lower is better. Planning-aware evaluation additionally reports Influenced Ratio (IR), the relative change in the closest ego–risk distance between full and filtered observations, and Collision Rate (CR).

Implementation details. We freeze a V-JEPA2 ViT-L encoder and use a $K = 1 6$ frame observation history and an H = 60 step future horizon (3 s at 20 FPS). RiskWorld considers at most 64 candidates and uses 256-dimensional deterministic states, 64-dimensional stochastic states, and four relation-attention heads. We train for 10 epochs with AdamW, a batch size of 64, and an initial learning rate of $1 0 ^ { - 4 }$ . We set $\lambda _ { o b j } = 1 , \lambda _ { c u r v e } = 0 . 2 , \lambda _ { x y } = \lambda _ { d i s t } = 0 . 0 5 \mathrm { , }$ $\lambda _ { m i n } = 0 . 0 2$ , and $\beta = 1 0 ^ { - 3 } ;$ auxiliary future losses are linearly warmed up over the first two epochs. We select $\eta = 0 . 7 0$ on the validation set to maximize overall micro-F1 and use it for all test categories.

Table 1: Risk localization and anticipation results. P, R, PIC, and FA denote precision, recall, Progressive Increasing Cost, and false-alarm rate. F1 is micro-averaged over all scenario types. <sup>∗</sup> denotes our object-level adaptations of BADAS and FLaRA.
<table><tr><td></td><td colspan="3">Interactive</td><td colspan="3">Collision</td><td colspan="3">Obstacle</td><td>Non-inter.</td><td>All</td></tr><tr><td>Method</td><td>P(%) ↑</td><td>R(%) ↑</td><td>PIC↓</td><td>P(%) ↑</td><td>R(%) ↑</td><td>PIC↓</td><td>P(%) ↑</td><td>R(%) ↑</td><td>PIC↓</td><td>FA(%) ↓</td><td>F1↑</td></tr><tr><td>Random</td><td>9.5</td><td>50.0</td><td>16.7</td><td>19.2</td><td>49.8</td><td>15.7</td><td>7.2</td><td>50.3</td><td>11.4</td><td>80.8</td><td>15.1</td></tr><tr><td>Range (5m)</td><td>38.7</td><td>10.7</td><td>20.3</td><td>85.6</td><td>27.7</td><td>4.1</td><td>45.0</td><td>18.3</td><td>10.2</td><td>3.3</td><td>30.0</td></tr><tr><td>Range (10m)</td><td>43.6</td><td>69.1</td><td>7.1</td><td>69.3</td><td>62.4</td><td>3.8</td><td>33.3</td><td>88.5</td><td>0.8</td><td>15.2</td><td>53.6</td></tr><tr><td>Kalman filter</td><td>37.0</td><td>54.0</td><td>15.4</td><td>59.9</td><td>58.1</td><td>4.2</td><td>35.3</td><td>61.2</td><td>10.2</td><td>18.8</td><td>46.7</td></tr><tr><td>Social-GAN</td><td>39.4</td><td>57.7</td><td>14.1</td><td>60.8</td><td>45.4</td><td>7.8</td><td>36.9</td><td>69.3</td><td>4.0</td><td>16.3</td><td>46.0</td></tr><tr><td>MANTRA</td><td>36.3</td><td>62.1</td><td>13.3</td><td>58.3</td><td>45.4</td><td>7.1</td><td>35.7</td><td>71.8</td><td>2.5</td><td>16.5</td><td>45.4</td></tr><tr><td>QCNet</td><td>40.0</td><td>56.6</td><td>14.1</td><td>60.3</td><td>45.4</td><td>7.3</td><td>38.2</td><td>68.9</td><td>4.4</td><td>14.5</td><td>46.4</td></tr><tr><td>DSA</td><td>54.7</td><td>19.7</td><td>20.9</td><td>79.4</td><td>45.9</td><td>3.7</td><td>54.2</td><td>47.2</td><td>17.5</td><td>3.3</td><td>46.8</td></tr><tr><td>RRL</td><td>49.4</td><td>15.4</td><td>22.4</td><td>87.3</td><td>64.6</td><td>4.6</td><td>47.1</td><td>19.0</td><td>16.0</td><td>5.1</td><td>48.6</td></tr><tr><td>BP</td><td>36.4</td><td>16.3</td><td>25.6</td><td>74.4</td><td>9.8</td><td>25.1</td><td>22.4</td><td>3.0</td><td>27.9</td><td>4.7</td><td>16.6</td></tr><tr><td>BCP</td><td>48.7</td><td>29.2</td><td>22.8</td><td>76.8</td><td>20.7</td><td>20.8</td><td>32.1</td><td>35.2</td><td>20.5</td><td>4.7</td><td>33.4</td></tr><tr><td> ${ \mathrm { B A D A S } } ^ { * }$ </td><td>65.6</td><td>57.1</td><td>13.5</td><td>89.3</td><td>36.0</td><td>9.3</td><td>51.0</td><td>64.5</td><td>28.6</td><td>2.8</td><td>48.8</td></tr><tr><td> $\mathrm { F L a R A ^ { * } }$ </td><td>64.2</td><td>73.6</td><td>12.6</td><td>89.9</td><td>41.5</td><td>6.1</td><td>65.4</td><td>67.8</td><td>15.6</td><td>4.1</td><td>61.8</td></tr><tr><td>RiskWorld</td><td>70.2</td><td>66.5</td><td>10.5</td><td>91.5</td><td>40.4</td><td>8.9</td><td>67.3</td><td>72.0</td><td>15.7</td><td>2.1</td><td>63.0</td></tr></table>

## Risk Localization and Anticipation

To answer RQ1, we compare RiskWorld with representative rule-based, trajectory-based and behavior-based approaches. Table 1 shows that RiskWorld achieves the best overall F1 of 63.0, exceeding Range (10m), BADAS<sup>∗</sup>, and FLaRA<sup>∗</sup> by 9.4, 14.2, and 1.2 points, respectively. FLaRA<sup>∗</sup> is the strongest learned baseline, attaining 73.6% recall on interactive scenes and an overall F1 of 61.8; this confirms that imagined future representations transfer efectively to risk localization. RiskWorld nevertheless achieves higher precision on all three risk-bearing subsets—70.2% on interactive, 91.5% on collision, and 67.3% on obstacle—while attaining the lowest non-interactive FA of 2.1%. Its advantage therefore lies in a stronger precision–recall–FA balance rather than uniformly higher recall. Range (10m) obtains higher recall and lower PIC on several subsets, but its broad proximity trigger increases FA to 15.2% and reduces precision. RiskWorld instead ofers the strongest overall F1 while more reliably distinguishing the risk source from irrelevant objects.

Comparison with fixed-range rules. Because Range (10m) remains competitive in recall and PIC, Figure 3(a–b) examines this comparison across ego–object distance intervals. A range rule selects every object within its radius and therefore incurs a 100% false-positive rate in each active bin. RiskWorld recalls 76.7% and 66.7% of risk objects below 5 m and between 5–10 m while reducing the corresponding false-positive rates to 22.7% and 13.2%. It also retains

Table 2: Ablation of the main RiskWorld components. I, C, and O report F1 on interactive, collision, and obstacle scenarios; N reports the false-alarm rate on non-interactive scenes; All is overall micro-F1. All values are percentages.
<table><tr><td>Variant</td><td>I↑</td><td>C↑</td><td>0↑</td><td>N↓</td><td>All ↑</td></tr><tr><td>w/o world features</td><td>47.6</td><td>60.0</td><td>56.7</td><td>21.3</td><td>50.6</td></tr><tr><td>w/o object visual token</td><td>55.7</td><td>56.6</td><td>51.9</td><td>3.3</td><td>54.6</td></tr><tr><td>w/o relation attention</td><td>63.8</td><td>45.9</td><td>60.7</td><td>1.2</td><td>54.3</td></tr><tr><td>Deterministic GRU</td><td>65.3</td><td>63.9</td><td>68.5</td><td>6.0</td><td>62.0</td></tr><tr><td>w/o future rollout</td><td>62.4</td><td>59.9</td><td>64.4</td><td>5.9</td><td>60.2</td></tr><tr><td>w/o future supervision</td><td>68.5</td><td>57.5</td><td>65.4</td><td>4.4</td><td>61.6</td></tr><tr><td>RiskWorld</td><td>68.3</td><td>56.0</td><td>69.5</td><td>2.1</td><td>63.0</td></tr></table>

25.0% recall at 10–20 m, where both range rules are inactive. RiskWorld is therefore not acting as a learned range rule: it suppresses nearby distractors while retaining risk evidence beyond fixed distance cutofs.

Figure 3(c) further examines sensitivity to the object-score threshold. Overall F1 remains stable over a broad interval around the selected $\eta = 0 . 7 0$ , while non-interactive FA decreases steadily as the threshold increases. This broad plateau shows that the reported performance does not depend on a narrowly tuned operating point and permits the recall–FA trade-of to be adjusted without retraining.

## Future-Risk Prediction Analysis

To answer RQ2, we evaluate future-risk prediction against current-state persistence and examine whether risk sources separate from distractors before critical events.

Figure 4(a) compares RiskWorld with a persistence baseline that repeats the current risk prediction at every future step. On annotated risk-source objects, RiskWorld achieves lower Brier scores across the full 3 s horizon and reduces the error at 3 s by 59.8%, indicating that the rollout tracks future risk evolution more accurately than a static prediction.

![](images/fab91e2050dd8277d9a175baa52d8cb7ac646e167b07c32067aa0769dd86a979.jpg)  
(a) Recall on true risk objects

![](images/9dab407f0f455e27f4b88d8d323368c819c323814abd2f679eb82b94314fb96d.jpg)  
(b) False-positive rate on non-risk objects

![](images/c965203fb3db168bc237d13036a99ea3d8fd7a87f06622124bf4980fd1b2127c.jpg)  
(c) Operating-threshold sensitivity  
Figure 3: Risk-localization behavior and operating point. (a–b) Test-set recall and false-positive rate across ego–object distances for RiskWorld and fixed-range rules. (c) Overall, interactive, and collision F1 together with non-interactive false-alarm rate across validation thresholds; the marker denotes the selected $\eta = 0 . 7 0$ used for all test categories.

![](images/e2f5d5bf28b78ff89bef5ef71dd35cd6f882bf9a547b2d13ec422897029f4221.jpg)

![](images/30673022616122b844807bbc2465219a2f83a095ab6b65226704bf8e22e01a26.jpg)  
(a) Future-rollout accuracy  
(b) Decision-space separation

Figure 4: Future-risk prediction and representation. (a) Horizon-wise Brier score on risk-source objects, comparing the learned rollout with current-state persistence. Lower is better. (b) t-SNE of 1,500 balanced decision representations from risk sources and hard non-risk objects.  
![](images/76572d96476efd23be95567cb9554e80dac700f1e367893581a799b519d24f6e.jpg)  
Figure 5: Temporal risk separation. Mean scores of the annotated risk source and the strongest non-risk object from 3 s before the critical frame; shaded regions denote 95% confidence intervals.

Figure 5 further examines risk-source discrimination during the 3 s preceding the critical frame. The mean source score rises from 0.219 to 0.650 on interactive scenes, from 0.139 to 0.771 on collision scenes, and from 0.191 to 0.625 on obstacle scenes, while the strongest non-risk score remains below 0.08 at the critical frame. At that frame, the annotated source outranks every distractor in 95.9%, 98.0%, and 94.5% of the respective scenarios, showing increasingly clear separation as the event approaches. Finally, Figure 4(b) shows distinct but partially overlapping decision regions; the twodimensional embedding yields a silhouette score of 0.369 over 1,500 balanced samples. Together, these results show that latent rollout improves horizon-wise risk prediction and supports increasingly discriminative object-level decisions as critical events approach.

Table 3: Planning-aware evaluation under the filteredobservation protocol. Lower values indicate that the selected object better preserves planning-critical information.
<table><tr><td rowspan="2">Method</td><td colspan="2">Interactive</td><td colspan="2">Obstacle</td></tr><tr><td>IR↓</td><td>CR(%)↓</td><td>IR↓</td><td>CR(%) ↓</td></tr><tr><td>Auto-pilot</td><td>0.45</td><td>33.6</td><td>0.52</td><td>58.7</td></tr><tr><td>Full observation</td><td>0.00</td><td>0.0</td><td>0.00</td><td>0.0</td></tr><tr><td>Ground-truth risk</td><td>0.02</td><td>0.4</td><td>0.04</td><td>5.3</td></tr><tr><td>Random</td><td>0.11</td><td>7.7</td><td>0.44</td><td>48.1</td></tr><tr><td>Range (10m)</td><td>0.01</td><td>6.2</td><td>0.24</td><td>26.4</td></tr><tr><td>Kalman filter</td><td>0.06</td><td>6.9</td><td>0.33</td><td>41.8</td></tr><tr><td>Social-GAN</td><td>0.16</td><td>10.0</td><td>0.49</td><td>55.3</td></tr><tr><td>MANTRA</td><td>0.15</td><td>9.3</td><td>0.51</td><td>56.7</td></tr><tr><td>QCNet</td><td>0.05</td><td>10.0</td><td>0.52</td><td>57.2</td></tr><tr><td>DSA</td><td>0.01</td><td>0.8</td><td>0.37</td><td>38.5</td></tr><tr><td>RRL</td><td>0.01</td><td>1.2</td><td>0.49</td><td>54.3</td></tr><tr><td>BP</td><td>0.14</td><td>9.3</td><td>0.41</td><td>47.1</td></tr><tr><td>BCP</td><td>0.14</td><td>9.7</td><td>0.34</td><td>39.4</td></tr><tr><td>RiskWorld</td><td>0.09</td><td>1.1</td><td>0.08</td><td>24.2</td></tr></table>

## Ablation Study

To answer RQ3, Table 2 compares six controlled variants in two groups. The representation group examines the contributions of pretrained scene context, object-aligned appearance, and relational reasoning. It removes all V-JEPA2 features (w/o world features), removes bbox-aligned visual tokens while retaining the global scene feature (w/o object visual token), or bypasses relational contextualization (w/o relation attention). The future-modeling group separates the efects of stochastic dynamics, recursive latent rollout, and futureoriented supervision. It replaces the stochastic rollout with a parameter-matched recurrent model and removes $\mathcal { L } _ { k l }$ (Deterministic GRU), replaces recurrent rollout with a multihorizon decoder while retaining future targets (w/o future rollout), or removes $\mathcal { L } _ { x y } , \mathcal { L } _ { d i s t } , \mathbf { \bar { \mathcal { L } } } _ { m i n }$ , and $\bar { \mathcal { L } } _ { c u r v e }$ while retaining $\mathcal { L } _ { o b j }$ and latent rollout (w/o future supervision). All variants use the same experimental settings.

![](images/864d7ed0c318476ac7c0f6adc3e224e180307232ba6207c63c4b863bf19d3837.jpg)

![](images/c4fc11799c3539819da328198b3362bd79a68b7407b6e958ae3415f2e7bfbfae.jpg)

![](images/b9ae83bc9d61fc87e0997590398e3f2c5418866953c6a51c14384fd289b6304d.jpg)  
(a) Interactive scenario

![](images/ee33fe8d6b421b7f2c993fbde64332070915e420064b69f10fdda3caea3495d6.jpg)  
(b) Obstacle scenario

![](images/6a7ae79495999dda1032778a073aa760c480b50d668d82f70aac9ba7c9670aaa.jpg)

![](images/d296988034816d2294994c27919e62d5d570551d4a849105dd80ba60261e2019.jpg)  
(c) Collision scenario  
Figure 6: Risk identification and temporal evolution. The upper panels mark the predicted risk source in red. The lower panels show the annotated source score (orange) and maximum candidate score (cyan) from −3 s to +1 s relative to the critical frame. Black and red vertical lines indicate the displayed and critical frames, respectively.

Object-centric representation. The w/o world features variant produces the largest degradation, reducing overall F1 from 63.0 to 50.6 and increasing FA from 2.1% to 21.3%. Retaining only the global scene feature recovers part of this loss, but w/o object visual token remains 8.4 F1 points below RiskWorld, demonstrating the value of object-aligned visual grounding. The w/o relation attention variant loses 8.7 F1 points; although its FA is lower, collision and obstacle F1 drop sharply. Thus, predictive scene context, object-specific appearance, and relational contextualization provide complementary evidence for localizing the risk source.

Latent future modeling. The Deterministic GRU variant improves collision F1 but lowers overall F1 to 62.0 and raises FA to 6.0%, indicating that stochastic dynamics provide a better aggregate trade-of. The w/o future rollout variant further reduces overall F1 to 60.2 with 5.9% FA, whereas w/ofuture supervision yields 61.6 F1 with 4.4% FA. Both recurrent imagination and future-oriented targets therefore contribute to object-level selectivity. Combining them with the objectcentric representation gives RiskWorld the best overall F1 and a low FA of 2.1%.

## Planning-Aware Evaluation

To answer RQ4, an LBC planner (Chen et al. 2020) observes either all objects, only the ground-truth risk object, or only the objects selected by each method; unselected actors are masked in the last setting. The first two provide fullobservation and privileged-selection references. This comparison measures the planning relevance of the selected objects, not improvements to the planner itself.

As shown in Table 3, RiskWorld performs best among automatic selectors on obstacle scenarios, attaining an IR of 0.08 and a CR of 24.2%. On interactive scenes, it achieves a low CR of 1.1% but an IR of 0.09, indicating that unselected interaction context can still afect the planned trajectory. RiskWorld therefore preserves the most planningrelevant information among automatic selectors for obstacles, whereas interactive planning remains more dependent on broader scene context.

## Qualitative Analysis

Figure 6 visualizes the frame-wise object risk scores produced by RiskWorld. At each observation time, the score of each candidate is decoded from its latent future rollout. In the interactive example, the crossing pedestrian’s score rises sharply before the critical frame and remains near one as the interaction approaches. In the obstacle example, RiskWorld selects the relevant trafic barrel among nearby static objects and maintains high confidence through most of the pre-critical interval. The collision example is less stable at longer lead times, but its score increases rapidly as the collision approaches. Across the three scenarios, the source and maximum-candidate curves overlap over most high-confidence intervals, showing that the annotated source is generally the top-ranked candidate when RiskWorld reports high risk.

## Discussion and Limitations

The results indicate that future ego–object relation rollout provides selective risk evidence beyond proximity, while the filtered-observation evaluation suggests that the selected objects retain planning-relevant information. RiskWorld nevertheless remains a risk monitor rather than a closed-loop planner; the planning-aware protocol evaluates the relevance of selected objects rather than direct improvements to planning. Current evaluation is limited to simulation; complex multi-object interactions, long-tail behaviors, and severe occlusions remain open challenges (Fang et al. 2024). Future work will study real-world generalization and uncertaintyaware, planner-conditioned counterfactual rollouts.

## Conclusion

This paper presents RiskWorld, an object-centric latent world model for autonomous driving risk identification. RiskWorld constructs relation-aware object states from observed visual and motion histories, rolls them forward with RSSM-style latent dynamics, and decodes the imagined ego–object evolution into object-level risk scores and future-relation evidence. On RiskBench, it achieves 63.0% overall F1 with a 2.1% false-alarm rate; temporal and filtered-observation analyses further support early risk-source discrimination and the planning relevance of its selections. These results demonstrate the promise of object-centric latent world modeling for history-only driving risk monitoring.

## References

Assran, M.; Bardes, A.; Fan, D.; Garrido, Q.; Howes, R.; Komeili, M.; Muckley, M.; Rizvi, A.; Roberts, C.; Sinha, K.; Zholus, A.; Arnaud, S.; Gejji, A.; Martin, A.; Hogan, F. R.; Dugas, D.; Bojanowski, P.; Khalidov, V.; Labatut, P.; Massa, F.; Szafraniec, M.; Krishnakumar, K.; Li, Y.; Ma, X.; Chandar, S.; Meier, F.; LeCun, Y.; Rabbat, M.; and Ballas, N. 2025. V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning. arXiv:2506.09985.

Bardes, A.; Garrido, Q.; Ponce, J.; Chen, X.; Rabbat, M.; LeCun, Y.; Assran, M.; and Ballas, N. 2024. Revisiting Feature Prediction for Learning Visual Representations from Video. Transactions on Machine Learning Research.

Caselli, L.; Trinci, T.; Bianconcini, T.; Magistri, S.; Taccari, L.; Sambo, F.; and Bagdanov, A. D. 2026. FLaRA: Predicting Future Latent Representations for Accident Anticipation. arXiv:2606.14380.

Chan, F.-H.; Chen, Y.-T.; Xiang, Y.; and Sun, M. 2016. Anticipating Accidents in Dashcam Videos. In Proceedings of theAsian Conference on Computer Vision (ACCV), 136–153.

Chen, D.; Zhou, B.; Koltun, V.; and Krähenbühl, P. 2020. Learning by Cheating. In Proceedings of the Conference on Robot Learning, 66–75.

Fang, J.; Li, L.-l.; Zhou, J.; Xiao, J.; Yu, H.; Lv, C.; Xue, J.; and Chua, T.-S. 2024. Abductive Ego-View Accident Video Understanding for Safe Driving Perception. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 22030–22040.

Fu, K.-Y.; and Chen, Y.-T. 2026. Uncertainty-Aware Vision-Based Risk Object Identification via Conformal Risk Tube Prediction. In Proceedings of the IEEE International Conference on Robotics and Automation (ICRA).

Gao, S.; Yang, J.; Chen, L.; Chitta, K.; Qiu, Y.; Geiger, A.; Zhang, J.; and Li, H. 2024. Vista: A Generalizable Driving World Model with High Fidelity and Versatile Controllability. In Advances in Neural Information Processing Systems (NeurIPS).

Goldshmidt, R.; Scott, H.; Niccolini, L.; and Matzner, H. 2026. Beyond the Beep: Scalable Collision Anticipation and Real-Time Explainability with BADAS-2.0. arXiv:2604.05767.

Goldshmidt, R.; Scott, H.; Niccolini, L.; Zhu, S.; Moura, D.; and Zvitia, O. 2025. BADAS: Context-Aware Collision Prediction Using Real-World Dashcam Data. arXiv:2510.14876.

Gupta, A.; Johnson, J.; Fei-Fei, L.; Savarese, S.; and Alahi, A. 2018. Social GAN: Socially Acceptable Trajectories with Generative Adversarial Networks. In Proceedings of the

IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2255–2264.

Hafner, D.; Lillicrap, T.; Fischer, I.; Villegas, R.; Ha, D.; Lee, H.; and Davidson, J. 2019. Learning Latent Dynamics for Planning from Pixels. In Proceedings of the International Conference on Machine Learning (ICML), 2555–2565.

Hafner, D.; Pasukonis, J.; Ba, J.; and Lillicrap, T. 2025. Mastering Diverse Control Tasks through World Models. Nature, 640: 647–653.

Kalman, R. E. 1960. A New Approach to Linear Filtering and Prediction Problems. Journal of Basic Engineering, 82(1): 35–45.

Kung, C.-H.; Yang, C.-C.; Pao, P.-Y.; Lu, S.-W.; Chen, P.-L.; Lu, H.-C.; and Chen, Y.-T. 2024. RiskBench: A Scenario-Based Benchmark for Risk Identification. In Proceedings of the IEEE International Conference on Robotics andAutomation (ICRA), 14800–14807.

Li, C.; Chan, S. H.; and Chen, Y.-T. 2020. Who Make Drivers Stop? Towards Driver-Centric Risk Assessment: Risk Object Identification via Causal Inference. In Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 10711–10718.

Li, C.; Chan, S. H.; and Chen, Y.-T. 2023. DROID: Driver-Centric Risk Object Identification. IEEE Transactions on Pattern Analysis and Machine Intelligence, 45(11): 13683– 13698.

Li, C.; Meng, Y.; Chan, S. H.; and Chen, Y.-T. 2020. Learning 3D-Aware Egocentric Spatial-Temporal Interaction via Graph Convolutional Networks. In Proceedings of the IEEE International Conference on Robotics and Automation (ICRA), 8418–8424.

Li, Y.; Fan, L.; He, J.; Wang, Y.; Chen, Y.; Zhang, Z.; and Tan, T. 2025. LAW: Enhancing End-to-End Autonomous Driving with Latent World Model. In Proceedings ofthe International Conference on Learning Representations (ICLR).

Liao, H.; Sun, H.; Shen, H.; Wang, C.; Tam, K.; Tian, C.; Li, L.; Xu, C.; and Li, Z. 2024. CRASH: Crash Recognition and Anticipation System Harnessing with Context-Aware and Temporal Focus Attentions. In Proceedings ofthe ACM International Conference on Multimedia (ACM MM).

Link, M.; Xu, Y.; Hu, Y.; and Liu, Y. 2026. MC-Risk: Multi-Component Risk Fields for Risk Identification and Motion Planning. arXiv:2605.21406.

Marchetti, F.; Becattini, F.; Seidenari, L.; and Del Bimbo, A. 2020. MANTRA: Memory Augmented Networks for Multiple Trajectory Prediction. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 7143–7152.

Min, C.; Zhao, D.; Xiao, L.; Zhao, J.; Xu, X.; Zhu, Z.; Jin, L.; Li, J.; Guo, Y.; Xing, J.; Jing, L.; Nie, Y.; and Dai, B. 2024. DriveWorld: 4D Pre-Trained Scene Understanding via World Models for Autonomous Driving. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR).

Wang, X.; Zhu, Z.; Huang, G.; Chen, X.; Zhu, J.; and Lu, J. 2024. DriveDreamer: Towards Real-World-Driven World

Models for Autonomous Driving. In Proceedings of the European Conference on Computer Vision (ECCV).

Xia, T.; Li, Y.; Zhou, L.; Yao, J.; Xiong, K.; Sun, H.; Wang, B.; Ma, K.; Chen, G.; Ye, H.; Liu, W.; and Wang, X. 2026. DriveLaW: Unifying Planning and Video Generation in a Latent Driving World. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 39701–39712.

Yang, Y.; Mei, J.; Ma, Y.; Du, S.; Chen, W.; Qian, Y.; Feng, Y.; and Liu, Y. 2025. Driving in the Occupancy World: Vision-Centric 4D Occupancy Forecasting and Planning via World Models for Autonomous Driving. In Proceedings of the AAAI Conference on Artificial Intelligence.

Yang, Z.; Chen, L.; Sun, Y.; and Li, H. 2024. ViDAR: Visual Point Cloud Forecasting Enables Scalable Autonomous Driving. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR).

Zeng, K.-H.; Chou, S.-H.; Chan, F.-H.; Niebles, J. C.; and Sun, M. 2017. Agent-Centric Risk Assessment: Accident Anticipation and Risky Region Localization. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2222–2230.

Zhao, T.; Zou, Y.; Mao, Z.; Xiao, P.; Huang, Y.; Yang, H.; Li, Y.; Li, T.; Wu, G.; and Lin, Y. 2025. Accident Anticipation via Temporal Occurrence Prediction. In Advances in Neural Information Processing Systems (NeurIPS).

Zheng, W.; Chen, W.; Huang, Y.; Zhang, B.; Duan, Y.; and Lu, J. 2024a. OccWorld: Learning a 3D Occupancy World Model for Autonomous Driving. In Proceedings of the European Conference on Computer Vision (ECCV).

Zheng, W.; Song, R.; Guo, X.; Zhang, C.; and Chen, L. 2024b. GenAD: Generative End-to-End Autonomous Driving. In Proceedings of the European Conference on Computer Vision (ECCV).

Zheng, Y.; Yang, P.; Xing, Z.; Zhang, Q.; Zheng, Y.; Gao, Y.; Li, P.; Zhang, T.; Xia, Z.; Jia, P.; Lang, X.; and Zhao, D. 2025. World4Drive: End-to-End Autonomous Driving via Intention-aware Physical Latent World Model. In Proceedings ofthe IEEE/CVFInternational Conference on Computer Vision (ICCV), 28632–28642.

Zhou, Z.; Wang, J.; Li, Y.-H.; and Huang, Y.-K. 2023. Query-Centric Trajectory Prediction. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 17863–17873.

Zou, Y.; Zhao, T.; Xiao, P.; Jin, H.; Qi, L.; Li, Y.; Liang, L.; Qian, Y.; Lai, C.; Lin, Y.; Li, Z.; and Wu, Y. 2026. RiskProp: Collision-Anchored Self-Supervised Risk Propagation for Early Accident Anticipation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2768–2777.