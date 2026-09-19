# WAM_COMPARISON_MATRIX_V1

Last updated: 2026-09-15

Status: **HISTORICAL PROJECTION SNAPSHOT — not current state or final route authority; retain only as a traceable comparison aid.**

Ontology authority:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
```

Anchors:

```text
LAW
WoTE
Epona
WorldDrive
World4Drive
```

This matrix is grouped by ontology family. It intentionally avoids one unreadable 90+ column table.

Evidence notation used when needed:

```text
[DP]  direct paper evidence
[SV]  source/code verified
[INF] project inference
[NR]  NOT REPORTED
[NE]  NOT EVALUATED
[NA]  NOT APPLICABLE
```

A short cell is not a claim of certainty. Decision-critical boundaries are summarized after each family and in the final evidence section.

---

# A. Problem and role of world knowledge

| ID | LAW | WoTE | Epona | WorldDrive | World4Drive |
|---|---|---|---|---|---|
| A01 Primary bottleneck | weak planner representation under trajectory-only supervision | multi-modal candidate ranking | unify long-horizon world generation and trajectory planning | generation/planning representation misalignment + candidate ranking | annotation-free physical latent + multimodal intention selection |
| A02 Role of world knowledge | auxiliary predictive representation teacher | online consequence model for evaluation | shared-history representation shaping + visual simulator sibling | predictive representation pretraining + future teacher/distilled consequence | online compact future hypothesis for mode selection |
| A03 Host planning paradigm | conventional waypoint planner | candidate bank + learned reward selection | direct diffusion/flow generative trajectory policy | anchor candidate planner + coarse score + FAR rerank | six intention-conditioned candidates + ScoreNet selector |
| A04 Historical position | predictive/self-supervised representation learning | learned trajectory evaluation/model-based candidate scoring | joint world/action generation + generative policy | representation transfer + model-based ranking distillation | multimodal mode selection + latent future consistency |

**Boundary:** these papers solve different immediate bottlenecks. A SOTA number cannot by itself rank the scientific value of representation learning against ranking, direct generative policy, or distilled foresight.

---

# B. Observation and current-state representation

| ID | LAW | WoTE | Epona | WorldDrive | World4Drive |
|---|---|---|---|---|---|
| B01 Sensor/input | camera-based host planner; perspective/BEV variants | camera + LiDAR in NAVSIM implementation | front-view camera + historical ego motion | single-view camera planning setup + ego status; video history for TA-DWM | multi-view camera + trajectory vocabulary |
| B02 Observation history | primarily current visual state; future frame used as target | current compact BEV state from sensor encoder | multiple historical frames/actions; variable-length causal context | historical observation clip/latent | current + previous timestamp temporal aggregation |
| B03 Current-state substrate | planner-facing perspective or BEV latent | compact BEV feature/state, e.g. 8×8 | compact multimodal historical latent `F` | adapted video/VAE visual latent + motion representation | physical latent `L_t` |
| B04 State semantics/granularity | planning visual feature; no explicit physical semantics required | BEV spatial scene feature for online rollout | historical visual+ego-motion dynamics context | visual dynamics + structured motion prior | spatial/depth + semantic + short-temporal context |
| B05 Current vs future separation | current planner latent distinct from predicted future latent | current BEV distinct from recurrent future BEVs | planner consumes `F`; VisDiT future separate | current visual/motion representation distinct from TA-DWM/FAR future feature | current physical latent + predicted candidate future latents both used |

**Boundary:** `latent` is not a sufficient comparison label. LAW, Epona, WorldDrive and World4Drive all use latents, but those latents carry different semantics and enter planning at different stages.

---

# C. Representation provenance and imported priors

| ID | LAW | WoTE | Epona | WorldDrive | World4Drive |
|---|---|---|---|---|---|
| C01 Origin stack | host planner visual encoder; no dedicated foundation prior central to contribution | TransFuser-style encoder; generic backbone prior not isolated as main mechanism | pretrained image compression/tokenizer; world model otherwise trained on driving data | CogVideoX 3D VAE/DiT prior → TA-DWM specialization | image backbone + metric-depth foundation model + Grounded-SAM/VLM semantic prior |
| C02 Prior injection | standard host feature learning | standard sensor encoder | compression latent/tokenizer | pretrained VAE/DiT init + learnable visual adapter | depth→3D positional encoding; semantic pseudo-label supervision |
| C03 Prior trainability | host-dependent; [NR] dedicated prior audit | host encoder training; [NR] dedicated prior audit | DCAE encoder/pretrained components partly fixed/fine-tuned as described; no matched prior ablation | transferred/adapted pieces; planner inherits/freeze policy [SV] | external depth/semantic prior generation; latent encoder learned around them |
| C04 Generic vs WM-specific attribution | not isolated as a foundation-prior ladder | not central | not cleanly isolated | **strong:** 31.4 no pretrain → 84.9 generic VAE → 85.8 TA-DWM vision → 86.9 TA-DWM motion | **partial:** component ablation separates depth/semantic/WM/intentions, but no single generic-pretrain ladder |

**Boundary:** WorldDrive is the canonical warning that the largest performance jump can come from generic pretrained representation rather than WM-specific future modeling.

---

# D. Action, intention and candidate space

| ID | LAW | WoTE | Epona | WorldDrive | World4Drive |
|---|---|---|---|---|---|
| D01 Action provenance | planner's own single predicted waypoints | refined trajectory anchors/candidates | historical ego motion; future visual action can be TrajDiT-predicted or externally provided | Phase1 expert/logged trajectory condition; planning/FAR uses candidate trajectories | intention-conditioned model-generated trajectories |
| D02 Action representation | flattened waypoint sequence | trajectory anchor/refined path embedding | relative ego pose `(Δθ,Δx,Δy)`; future trajectory continuous | trajectory anchor + residual motion embedding | trajectory sequence → MLP action token |
| D03 Command/intention | no explicit multimodal intention bank | anchor modes; no central semantic intention query | history/action context; no explicit scored intention bank | trajectory vocabulary as motion prior; ego driving command also encoded in planner | explicit command-conditioned K=6 intention queries from clustered endpoints |
| D04 Candidate construction | no explicit bank | K-means expert-trajectory anchors | no explicit scored candidate bank; stochastic generative policy | 256 trajectory anchors as planner queries | large trajectory vocabulary (N=8192) → K=6 intention modes per command |
| D05 Breadth/support | one deployed planner output | 256 default; 64/128/256 ablated; 1024 unseen anchors test | distributional samples possible but no explicit scored N-bank in planning evaluation | 256 base anchors → top-K FAR (K=1/3/5/10 ablated) | 6 modes |
| D06 Refinement/support/pruning | [NA] | scene-conditioned residual refinement; unseen-anchor generalization tested | [NA] explicit bank pruning | offset refinement; coarse scores prune 256→top-K before future-aware reasoning | candidate trajectories generated from intention query; no large-bank pruning after six modes |

**Boundary:** candidate support is an independent planning bottleneck. WoTE/WorldDrive/World4Drive gains cannot be assigned only to the WM if their action sets differ.

---

# E. Action → world coupling

| ID | LAW | WoTE | Epona | WorldDrive | World4Drive |
|---|---|---|---|---|---|
| E01 Conditioning presence/scope | yes: predicted waypoints condition future visual latent | yes: each candidate conditions BEV transition | yes: action conditions visual next-frame generation | yes: trajectory conditions TA-DWM/FAR future representation | yes: each trajectory/action token conditions future latent |
| E02 Injection mechanism | waypoint vector concatenated to each visual token + MLP [SV] | action token appended/processed with BEV state in Transformer transition | action modulation/conditioning in VisDiT | motion embedding conditions diffusion; candidate embedding cross-attends in FAR | action+current latent concatenated as cross-attention context |
| E03 Branch multiplicity/parameterization | one branch | shared WM applied in parallel to many candidates | no scored K-branch planner; generative action condition | shared teacher/student models conditioned on top-K candidates | shared predictor + different intention/action conditions for six branches |
| E04 Branch persistence | single endpoint/target, no candidate tree | branch persists recurrently 0→2→4s | visual generation autoregressive through time, but planning branch not K-way scored | teacher candidate futures then distilled endpoint/summary; no long online rollout | endpoint candidate futures; no recurrent branch in core selector |
| E05 Support extrapolation | factual/planner action near logged policy; alternatives absent | refined/unseen candidate anchors tested; reactive truth still absent | external/action-controlled generation can depart from logged path; direct counterfactual validity not established | TA-DWM trained mainly on logged/expert motion then queried with planner alternatives | six modes generated from learned intention support; no matched alternative-action truth |

---

# F. Dynamics and future temporal modeling

| ID | LAW | WoTE | Epona | WorldDrive | World4Drive |
|---|---|---|---|---|---|
| F01 Future object | planner visual latent | compact future BEV states + updated action state | next-frame visual latent/image + future trajectory branch | generative future video latent (teacher); distilled future latent online | compact physical future latent per intention |
| F02 Future semantics | future-aware planner representation target | predicted scene consequence for utility evaluation | visual world evolution / trajectory distribution | motion-conditioned scene dynamics; distilled planning-relevant consequence | future mode/hypothesis consistent with intention and scene |
| F03 Dynamics operator | deterministic Transformer latent predictor | recurrent Transformer state-action transition | causal MST + rectified-flow/diffusion DiTs | diffusion TA-DiT teacher; lightweight query decoder student | multi-layer cross-attention predictor |
| F04 Temporal factorization | selected future endpoint | recurrent intermediate future sequence | visual frame-autoregressive; trajectory multi-step one-shot | generative future sequence teacher; deployed distilled summary | single endpoint `t+n` per mode |
| F05 Interval/horizon/intermediate use | 0.5/1.5/3/10s target ablated; 1.5s best | ~2s and ~4s; intermediate state consumed and recurrent path helps | next-frame AR visual; ~3s trajectory planning | future video/latent horizon per TA-DWM; online FAR consumes summary rather than full rollout | default `n=3` timestamps; endpoint consumed |
| F06 Uncertainty/multimodality/robustness | deterministic single future; no calibrated uncertainty | multimodality from candidate actions, not calibrated world uncertainty; recurrent free-running | stochastic diffusion/flow; Chain-of-Forward targets rollout drift | diffusion teacher can generate varied futures; deployed student uncertainty not calibrated | six action-conditioned modes; ScoreNet probabilities not proven calibrated uncertainty |

**Boundary:** longer horizon, more visual detail or more stochasticity are not automatically planning improvements.

---

# G. Future supervision and truth sources

| ID | LAW | WoTE | Epona | WorldDrive | World4Drive |
|---|---|---|---|---|---|
| G01 Factual future truth | one observed future frame encoded to latent | simulator-generated semantic BEV targets plus logged scenario state semantics | observed future image latent + observed future trajectory | Phase1 observed future video latent | one observed future physical latent |
| G02 Target treatment | same learned visual encoder target; reconstruction path target detached [SV] | explicit semantic BEV labels from simulator; reward labels separate | encoded future visual target under flow loss | frozen TA-DWM acts as FAR teacher; stop-gradient alignment | actual future latent extracted with same physical-latent machinery; nearest-mode comparison |
| G03 Consequence teacher | factual future latent only; no alternative teacher | BEV simulator/semantic target for candidate ego futures | factual next-frame data | **frozen learned TA-DWM** for candidate future latents | one factual future provides nearest-mode proxy; no K-way external consequence teacher |
| G04 Value/utility teacher | [NA] | expert imitation + simulator NC/DAC/TTC/comfort/progress | [NA] explicit evaluator; policy learns data distribution | PDMS/oracle preference for FAR; base imitation+simulation rewards | no external utility teacher; ScoreNet target derived from factual-mode index |
| G05 Policy/trajectory teacher | expert waypoint imitation | WTA expert trajectory + anchor/refinement supervision | observed trajectory under rectified-flow objective | expert trajectory + imitation/simulation targets for base planner | selected mode `T^j` supervised by expert L1 |
| G06 Mode assignment | [NA] | nearest expert/positive anchor in WTA; candidates each get simulator reward targets | no fixed branch identity in direct generative planner | base anchors fixed; FAR ranking by oracle preference among top-K | **nearest predicted future latent to one factual future latent** defines `j` |
| G07 Branch supervision coverage | one factual branch | many ego candidates get reward/semantic targets under simulator semantics | [NA] K-way alternatives | teacher-generated future latent for top-K + pairwise preference ranking | selected branch gets reconstruction/trajectory positive signal; ScoreNet trained on selected index |
| G08 Other-agent response truth | factual log only; no alternatives | cached/interpolated logged GT tracks shared across ego candidates in audited NAVSIM/PDM path [SV] | factual visual future; no intervention-specific alternatives | teacher-generated candidate scenes; no matched real reactive alternatives | one factual future; no intervention-specific other-agent truth |

**Boundary:** `state truth`, `consequence teacher`, `value teacher`, `policy teacher` and `other-agent response truth` must remain separate.

---

# H. Multimodal branch identity and assignment

| ID | LAW | WoTE | Epona | WorldDrive | World4Drive |
|---|---|---|---|---|---|
| H01 Branch meaning | [NA] no explicit multimodal branches | candidate ego action modes | stochastic trajectory distribution; not an explicit scored branch bank | trajectory anchors / top-K candidate actions | intention-conditioned trajectory + future-world modes |
| H02 Mode identity source | [NA] | K-means anchor identity from expert trajectories | emergent continuous generative samples | trajectory vocabulary anchor identity | clustered endpoint intention query + future latent branch |
| H03 Positive branch rule | [NA] | nearest expert anchor for WTA trajectory supervision; reward labels for candidates | generative likelihood/flow, no discrete positive mode | coarse score/top-K then PDMS preference ranking | nearest factual future latent determines positive mode `j` |
| H04 Coverage/oracle ceiling | [NE] | candidate-count + unseen-anchor ablations; no single oracle ceiling emphasized | [NE] scored-bank oracle | best-of-6 oracle 93.6 demonstrates ranking headroom | [NE] explicit best-of-N oracle in audited main analysis |

---

# I. Counterfactuality and reactivity vector

| ID | LAW | WoTE | Epona | WorldDrive | World4Drive |
|---|---|---|---|---|---|
| I01 Candidate-specific output branching | NO multi-candidate branch; one planner-conditioned future | YES | controllable generation can vary with action, but core planning has no scored K-way branch | YES top-K teacher/student futures | YES six candidate futures |
| I02 Candidate-specific consequence supervision | NO alternative branches | YES for candidate ego/simulator targets, but other-agent response fixed | NO matched K-way planning alternatives | teacher-generated candidate future latents, not observed alternatives | NO K real futures; one factual future used for mode assignment |
| I03 Alternative-action ground truth | NO | candidate-specific ego simulation/reward under PDM semantics; not real alternative logs | NO matched intervention set | NO real matched alternatives | NO real matched alternatives |
| I04 Reactive other-agent response truth | NO | NO in audited NAVSIM target path; same logged surrounding tracks | NOT ESTABLISHED | NOT ESTABLISHED / teacher imagination only | NOT ESTABLISHED |
| I05 External intervention-validity evidence | ABSENT | Bench2Drive shows reactive closed-loop policy performance, but does not validate WM counterfactual response accuracy itself | ABSENT | ABSENT | ABSENT |

**Canonical conclusion:** none of the five anchors establishes real intervention-valid counterfactual traffic dynamics. Their architectural branching/supervision levels differ substantially.

---

# J. World → planning interface

| ID | LAW | WoTE | Epona | WorldDrive | World4Drive |
|---|---|---|---|---|---|
| J01 Entry point | training representation | candidate evaluation | shared representation + direct trajectory generation | representation transfer + second-stage re-ranking | candidate future prediction + selector |
| J02 Online future computation | branch may execute, but selection already produced | YES recurrent BEV | visual future optional; NO for planning-only mode | YES lightweight distilled future; heavy diffusion NO | YES compact endpoint future |
| J03 Online future consumption | **NO** [SV] | **YES** | visual future **NO** in planning-only path; shared `F` YES | **YES** distilled future affects argmax | **YES** ScoreNet on future latent chooses trajectory |
| J04 Coupling direction | action→future only for auxiliary loss | action→future→reward→action selection | `F→trajectory`; trajectory/action→visual future; no same-step visual→trajectory rescore | candidate→future surrogate→reward→selection | candidate→future latent→mode score→selection |
| J05 Selection mechanism | direct waypoint head | argmax explicit reward over candidates | direct diffusion/flow policy | base score/refinement then FAR argmax | highest ScoreNet mode |
| J06 Consequence vs decision separation | [NA] online | explicit WM vs Reward Model | no consequence evaluator in planning path | explicit future surrogate vs ranking objective | future predictor + ScoreNet, but ScoreNet is factual-mode classifier rather than utility |
| J07 Task-mode graph | one planner graph; WM output unused for deployed selection | same evaluator graph | planning: MST→TrajDiT; simulation: MST→VisDiT | training teacher graph differs from deployed FAR graph | same compact future predictor/ScoreNet remains online |

---

# K. Scorer and decision semantics

| ID | LAW | WoTE | Epona | WorldDrive | World4Drive |
|---|---|---|---|---|---|
| K01 Scorer presence/placement | no future-based scorer | separate Reward Model after rollout | no explicit planning scorer | base imitation/simulation scorer + FAR second-stage scorer | ScoreNet after future latent prediction |
| K02 Score meaning | [NA] | explicit utility: imitation + safety/compliance/progress | [NA] | preference/ranking aligned to PDMS/oracle with future feature | **factual-future consistency / mode classification** |
| K03 Scorer inputs | [NA] | current+future BEV sequence + action sequence | [NA] | candidate trajectory embedding + distilled future-scene representation | predicted future latent for each mode |
| K04 Decomposition/aggregation | [NA] | imitation + NC/DAC/TTC/comfort/EP, hand-weighted nonlinear aggregation | [NA] | base planner has imitation/simulation heads; FAR produces scalar preference score | softmax classification over modes; no explicit safety/value decomposition |
| K05 Target/ranking source | [NA] | expert distance + simulator rule metrics | [NA] | PDMS/oracle preference pairs (Bradley-Terry) | nearest-factual-future mode index (focal loss) |

**Key scientific split:** WoTE/WorldDrive score candidate utility/preference; World4Drive primarily scores which future hypothesis matches the demonstrated factual future. These are not interchangeable notions of value.

---

# L. Training topology, jointness and gradients

| ID | LAW | WoTE | Epona | WorldDrive | World4Drive |
|---|---|---|---|---|---|
| L01 Stage topology | planner + auxiliary WM objective in shared training | end-to-end combined trajectory/BEV/reward losses after simulator target preparation | joint end-to-end world/trajectory training | Phase1 TA-DWM → Phase2 planner → freeze teacher/planner → FAR training | end-to-end physical latent + future + selector + trajectory losses |
| L02 Representation sharing | planner visual latent shared with WM branch | current BEV shared across candidate planner/WM/evaluator | shared historical `F` for TrajDiT/VisDiT | explicit vision+motion representation inheritance from WM to planner | current physical latent shared by candidate generator and future predictor |
| L03 Parameter sharing | shared upstream planner encoder; WM decoder separate | shared encoder/planner components; WM/reward modules distinct | shared MST, separate TrajDiT/VisDiT | copied/transferred/frozen encoders plus distinct planner/FAR | shared encoder/current latent; future predictor/ScoreNet distinct heads |
| L04 Gradient coupling | WM loss shapes shared upstream; target detached [SV] | total losses jointly optimize relevant model components; simulator labels external | L_traj + L_vis both shape MST | staged/frozen; FAR cannot update heavy teacher [SV] | sem + recon + score + traj jointly train selected mechanism |
| L05 Transfer/freeze/distillation | none as separate lifecycle | no heavy teacher distillation central | no stage transfer central | **central:** frozen representation transfer + TA-DWM→FAR latent distillation | no teacher/student transformation; online predictor trained directly |
| L06 Joint-loss semantics | trajectory imitation + reconstruction/prediction | BEV + sim reward + imitation reward + trajectory | trajectory flow + visual flow | phase-specific; FAR alignment + ranking | semantic + recon + focal score + trajectory L1 |

---

# M. Future-knowledge lifecycle and deployment path

| ID | LAW | WoTE | Epona | WorldDrive | World4Drive |
|---|---|---|---|---|---|
| M01 Lifecycle class | training-only predictive shaping | same compact learned transition remains online | cross-modal future shaping; visual branch optional in planning | heavy generative teacher → distilled lightweight online foresight | direct online compact latent foresight |
| M02 Deployed future object | none consumed by selection | recurrent future BEV sequence | no visual future required; planner uses historical `F` | distilled candidate future latent/summary | one compact endpoint latent per intention |
| M03 Model-class transformation | future branch effectively drops from decision path | same WM class online | sibling visual generator disabled for planning | diffusion teacher → lightweight query-decoder student | same compact predictor remains online |
| M04 Information bottleneck/compression | planner representation only | compact BEV state itself is computational bottleneck | shared `F` compresses history, but no distilled future summary for planning | Future Scene Queries / distilled planning-oriented latent | compact latent endpoint; no explicit teacher distillation |
| M05 Inspectability | latent target, not deployed consequence | BEV sequence relatively structured/decodable | visual simulator explicit when enabled | deployed future opaque latent; explicit TA-DWM video available offline/analysis | opaque physical latent endpoint |
| M06 Optional/sibling branch | WM branch auxiliary | no | VisDiT sibling simulation branch | heavy TA-DWM available but not in deployed planner | no separate optional heavy simulator central |

---

# N. Compute, pruning and latency

| ID | LAW | WoTE | Epona | WorldDrive | World4Drive |
|---|---|---|---|---|---|
| N01 Candidate breadth × future depth | 1 × single target; no online selection rollout | 256 × recurrent future steps | no explicit candidate bank; TrajDiT sampling iterations | 256 base → top-K (best K≈5) × lightweight future | 6 × endpoint future |
| N02 State/dynamics cost | latent predictor not needed for selection | compact 8×8 BEV + Transformer chosen for parallel rollout | 2.5B model; visual DiT expensive, TrajDiT small | heavy diffusion paid offline; online FAR light | compact cross-attention latent predictor |
| N03 Pruning/coarse-to-fine | [NA] | evaluates broad candidate set; no major pre-WM top-K in core | [NA] | **yes:** coarse base scores/refine → top-K → FAR | only six modes; no large-bank prune |
| N04 Parallelization | [NA] | candidates processed in parallel on GPU | diffusion samples/denoising; no bank parallel comparison central | top-K candidate FAR can batch; heavy teacher offline | six mode futures share predictor/batch |
| N05 Latency accounting | no future-selection cost; host-planner runtime separate | ~18.7 ms reported for 256-trajectory setup on L20; not necessarily full sensor-to-action | MST+TrajDiT ~0.05s at 10 steps; ~0.32s at 100 on 4090 module accounting | full pipeline ~53ms on A800; FAR 16.2ms; heavy PWM comparison 570–850ms | [NR/NEEDS CHECK] exact end-to-end latency in current audit |
| N06 Quality–latency scaling | horizon ablation affects quality, not deployment compute curve | K ablation 64/128/256 + latency | 10 vs 100 sampling-step speed; matched planning-quality curve not established | K=1/3/5/10 performance + full latency | model-size/backbone scaling reported; latency scaling not established |

---

# O. Evaluation regime and evidence attribution

| ID | LAW | WoTE | Epona | WorldDrive | World4Drive |
|---|---|---|---|---|---|
| O01 Planning evaluation | nuScenes open-loop; NAVSIM non-reactive; CARLA/reactive evaluation also reported in project record | NAVSIM non-reactive + Bench2Drive/CARLA reactive closed-loop | nuScenes open-loop + NAVSIM non-reactive | NAVSIM; NAVSIM-v2 pseudo/reactive-traffic regime; nuScenes open-loop | nuScenes open-loop + NAVSIM non-reactive |
| O02 World/prediction evaluation | latent prediction/reconstruction + planning ablations; no photorealistic video focus | BEV semantic prediction; planning-centric | FID/FVD + long visual rollout | FID/FVD/motion sensitivity + planning | latent self-supervision; no decoded high-fidelity world benchmark central |
| O03 Training oracle vs eval regime | factual logged future training; later benchmarks do not create alternative-action truth | audited NAVSIM targets non-reactive; Bench2Drive evaluation reactive | factual video/trajectory training; planning eval non-reactive/open-loop | learned teacher + PDM preference; NAVSIM-v2 evaluation more reactive than teacher truth | one factual future supervision; NAVSIM non-reactive eval |
| O04 Strongest matched control | auxiliary/action-condition matched ablations; exact source stronger than headline SOTA | 81.0 baseline → 83.2 evaluator/no future → 85.6 + future | 78.1 trajectory-only training → 86.2 joint visual+trajectory | 84.9→85.8→86.9 representation ladder; 86.9→87.0→88.1 rewarder/future ladder | physical priors+intentions no WM 0.61/0.36 → +WM 0.50/0.16 |
| O05 Attribution ladder | host planner → +predictive latent objective/action condition | candidate generator → scorer → future state | shared policy backbone → +visual predictive supervision | generic VAE → TA-DWM vision → TA-DWM motion → rewarder → future feature | intention → depth/semantic priors → WM predictor+selector |
| O06 Baseline comparability | matched internal ablations strongest; cross-paper inputs differ | SOTA rows vary sensors/candidates | front-camera-only vs many multi-view baselines; headline table heterogeneous | single-view vs multimodal baselines; internal ladder strongest | LAW comparison has backbone/setup differences; component ablation strongest |
| O07 Fidelity→decision evidence | no monotonic proof; 1.5s target best warns longer≠better | future on/off helps, but world accuracy→PDMS monotonic relation not isolated | visual joint task helps planning; better FID/FVD→better planning not shown | generation quality and FAR planning gain both exist, but direct fidelity→decision causality absent | future selector helps; latent prediction accuracy→planning monotonicity not isolated |
| O08 Source verification | official code inference path audited [SV] | official code supervision/reactivity audited [SV] | paper-level deep read; no equivalent source audit in this normalization | official code interface audited [SV] | official code core mechanism audited [SV]; NAVSIM source branch not separately established |
| O09 Oracle/deployed gap | [NE] candidate oracle | candidate-count effects; no headline oracle upper bound central | [NE] | best-of-6 oracle 93.6 > deployed; ranking headroom explicit | [NE] |
| O10 Proves / does-not-prove / alternative | proves auxiliary action-aware future prediction can improve planning representation; does not prove online model-based planning | proves online future features add beyond current-state evaluator; does not prove reactive counterfactual traffic truth | proves visual predictive joint training can improve shared planner; does not prove online visual imagination causes decisions | proves WM-specific transferred reps add modest gains and distilled future feature helps reranking; does not prove teacher dynamics are physically correct counterfactuals | proves WM-selector bundle helps beyond intentions/priors; does not prove six action futures are six true counterfactual outcomes |

---

# P. Safety, uncertainty, interaction and physical validity

| ID | LAW | WoTE | Epona | WorldDrive | World4Drive |
|---|---|---|---|---|---|
| P01 Explicit risk/safety in world state | ABSENT; implicit in latent | BEV state not explicit risk field | ABSENT explicit risk state | distilled/generative latent not explicit risk state | physical latent not explicit risk state |
| P02 Safety/risk in decision value | no explicit future scorer | **explicit:** NC/DAC/TTC/comfort/progress reward heads | no explicit scorer; safety implicit in learned trajectory distribution | base simulation heads + PDMS preference in FAR; future latent itself not risk-labeled | no explicit safety/value head; factual-mode ScoreNet |
| P03 Uncertainty/calibration | deterministic; no calibrated uncertainty | candidate diversity but no calibrated world uncertainty | stochastic diffusion/flow; calibration not established | diffusion teacher stochasticity possible; deployed reward/future confidence not calibrated | softmax over modes; not established as calibrated uncertainty |
| P04 Multi-agent interaction | implicit in visual latent; self-attention among tokens, no behavioral response model | BEV includes agents; audited supervision keeps surrounding-agent logged future fixed | implicit visual dynamics; no evaluated candidate-specific reactive response | generated scene may include agents; no matched reactive alternative truth | implicit multi-view latent; no reactive alternative truth |
| P05 Physical/kinematic/causal constraints | ego trajectory condition; no explicit physics oracle | simulator semantic targets + action-conditioned BEV; fixed-agent semantics | relative-pose action control + learned video dynamics | trajectory-aware generation/motion representation; visual plausibility not causal proof | metric-depth/spatial prior + action-conditioned latent; no intervention ground truth |
| P06 Long-horizon drift/robustness | no deployed long rollout | recurrent compact rollout; intermediate steps help; no explicit Chain-of-Forward-style robustness objective | **Chain-of-Forward** directly trains on self-predicted contexts for visual rollout stability | deployed path avoids heavy long rollout; teacher generation quality evaluated separately | endpoint latent, no long online rollout |
| P07 Rule/legal/corner-case semantics | implicit via data/planning metrics | explicit simulator reward semantics | authors show qualitative traffic knowledge; direct rule encoding absent | base/PDM reward supervision includes compliance/safety; teacher latent semantics implicit | semantics imported via VLM pseudo labels; rule utility not explicit |

---

# Q. Five-anchor synthesis — what survives horizontal comparison

The following field-level statements are supported by the five-anchor projection and should guide later anchors.

## Q1. Substrate is secondary to interface semantics

```text
LAW          latent
WoTE         BEV
Epona        shared latent + visual generator
WorldDrive   video latent teacher + distilled latent
World4Drive  compact physical latent
```

The more explanatory axis is **where/how future information changes planning**, not RGB-vs-BEV-vs-latent.

## Q2. Future information has at least five planning roles

```text
representation teacher          LAW
online consequence model        WoTE
cross-modal representation task Epona
generative teacher→distillation WorldDrive
online factual-mode foresight   World4Drive
```

## Q3. Candidate systems have at least three independent bottlenecks

```text
candidate support / diversity
consequence prediction
selection / value semantics
```

A better WM cannot select an action that is absent from the candidate set; a perfect candidate set is still wasted by a poor scorer.

## Q4. Counterfactuality is not binary

All five anchors reinforce:

```text
candidate-conditioned output
!= alternative-action outcome supervision
!= reactive-agent intervention truth
!= validated causal counterfactual accuracy
```

## Q5. `score` has multiple meanings

```text
WoTE         explicit utility
WorldDrive   oracle preference/value ranking
World4Drive  factual-future/mode consistency
```

Therefore later synthesis must never merge all `future→score` systems into one value-based family without a scorer-semantics field.

## Q6. Predictive knowledge can be useful without full online imagination

```text
LAW          training-only shaping
Epona        shared representation; visual branch off in planning
WorldDrive   heavy imagination offline → distilled future online
```

This falsifies any universal claim that WAM planning value requires full future scene rollout at deployment.

## Q7. Foundation priors are a major confound and sometimes the dominant effect

WorldDrive gives the cleanest evidence; World4Drive reinforces it. Every later foundation-heavy WAM must be audited for:

```text
imported representation gain
vs
WM-specific dynamics gain
```

## Q8. Prediction quality is not yet a universal proxy for decision quality

The five anchors provide evidence that predictive tasks/future features can help planning, but none establishes a general monotonic law:

```text
better future fidelity → better action
```

This remains an empirical question, not an ontology assumption.

---

# R. Quality status of Matrix V1

## Completed

```text
all Ontology V1 stable IDs projected across five anchors
training vs inference separated
counterfactual vector filled
scorer semantics separated
representation-prior attribution recorded
strongest matched controls recorded
source verification status recorded
```

## Known weak cells / future audit candidates

```text
1. exact LAW runtime/latency and some host-specific sensor details;
2. WoTE full sensor-to-action latency vs reported candidate-module latency;
3. Epona source-code verification and exact quality retained at fastest TrajDiT sampling setting;
4. WorldDrive teacher counterfactual behavioral validity beyond motion sensitivity;
5. World4Drive exact end-to-end latency and separate NAVSIM implementation equivalence.
```

These are explicitly unresolved; they are not reasons to delay Ontology V1 use.

---

# S. How to use this matrix for every next paper

For each new anchor:

```text
1. fill A–P before writing a narrative summary;
2. mark ABSENT / NOT REPORTED / NOT EVALUATED explicitly;
3. identify any mechanism residue not expressible by Ontology V1;
4. only then propose an ontology extension;
5. back-project any new dimension onto these five anchors;
6. update the matrix family-by-family;
7. preserve strongest matched control and evidence boundary.
```

Next new-paper target after normalization: **SeerDrive**, unless coverage evidence changes priority.
