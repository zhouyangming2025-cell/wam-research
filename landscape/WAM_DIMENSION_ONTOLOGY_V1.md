# WAM_DIMENSION_ONTOLOGY_V1

Last updated: 2026-09-15

Status: **V1 STABLE BASELINE — extensible, not frozen forever**

Scope:

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Built from dimension-first deep reads of:

```text
LAW
WoTE
Epona
WorldDrive
World4Drive
```

Primary discovery sources:

```text
papers/deep_analysis/P0048_LAW_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0045_WOTE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0001_EPONA_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0042_WORLDDRIVE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0046_WORLD4DRIVE_DEEP_ANALYSIS_V2.md
landscape/WAM_DIMENSION_DISCOVERY_LOG.md
landscape/WAM_DIMENSION_DISCOVERY_ADDENDUM_EPONA_WORLDDRIVE.md
landscape/WAM_DIMENSION_DISCOVERY_ADDENDUM_WORLD4DRIVE.md
```

---

# 0. Purpose

This ontology is **not a paper-summary template** and is not a taxonomy based on paper marketing labels.

Its purpose is to force every planning-centric WAM paper into the same scientific coordinate system so that:

```text
Paper A discusses dimensions 1/4/6
Paper B discusses dimensions 2/3/9

→ we still inspect A on 2/3/9
→ we still inspect B on 1/4/6
→ ABSENT / NOT REPORTED / NOT EVALUATED are recorded explicitly
→ no paper remains inside its own narrative comfort zone
```

The central rule is:

> **Whenever a paper introduces a module, representation, condition, query, loss, candidate generator, world predictor, scorer, reward, simulator, training stage or evaluation setup, first identify its scientific function; then ask which other papers perform the same function, how they differ, what directly supervises it, what remains at inference, and what evidence isolates its contribution.**

This ontology therefore separates three layers:

```text
L1  implementation fact
L2  mechanism abstraction
L3  cross-paper scientific claim
```

A cross-paper claim is invalid if the underlying L1/L2 evidence is not traceable.

---

# 1. Cell vocabulary and evidence grammar

Every stable dimension must be checked for every anchor. Silent blanks are forbidden.

Allowed absence/status values:

```text
PRESENT
ABSENT
NOT REPORTED
NOT EVALUATED
NOT APPLICABLE
UNCLEAR / NEEDS SOURCE AUDIT
```

Evidence labels:

```text
AUTHOR CLAIM
DIRECT PAPER EVIDENCE
SOURCE/CODE VERIFIED
OUR INFERENCE
```

Recommended comparison-cell structure:

```text
VALUE
Evidence: <paper table/ablation/source fact>
Boundary: <what this does not prove>
```

For decision-critical claims, prefer the strongest matched control immediately before the claimed WAM mechanism is added, not headline SOTA deltas.

---

# 2. Merge/split decisions from the discovery phase

Ontology V1 is **not** a concatenation of the provisional discovery dimensions. The following merges/splits are binding.

## 2.1 `action-conditioned` is permanently split

```text
action provenance
+ action representation
+ intention/command relation
+ candidate multiplicity/support
+ injection mechanism
+ branch parameterization
+ supervision under alternatives
```

LAW, WoTE, WorldDrive and World4Drive are all action-conditioned in some sense, but their scientific mechanisms are different.

## 2.2 `joint world-action modeling` is permanently split

```text
shared representation
shared parameters
shared losses/gradients
online causal action→world coupling
online causal world→action feedback
active-together-at-inference
```

Epona is the anchor showing why these cannot be one yes/no field.

## 2.3 `counterfactual` is represented as a vector

At minimum:

```text
candidate-specific output?
alternative-action future supervision?
reactive other-agent response truth?
external intervention-validity evidence?
```

Candidate branching is not causal identification.

## 2.4 `future → score` is permanently split

Possible scorer meanings include:

```text
utility/value
risk/safety
imitation/expert-likeness
factual-future consistency
mode posterior/likelihood
hybrid
```

WoTE and World4Drive prove these are different scientific objects.

## 2.5 `world-model gain` is permanently decomposed

Attribution may include:

```text
generic foundation prior
WM-specific predictive representation learning
candidate generator/support
candidate refinement
consequence prediction
scorer/value model
future-aware feature
extra supervision / oracle labels
```

WorldDrive's 31.4→84.9→85.8→86.9→87.0→88.1 ladder is the canonical example.

## 2.6 `online vs offline WM` is permanently replaced by a lifecycle

Future/world knowledge may be:

```text
training-only then discarded from selection
used to shape a shared representation
kept online as learned transition model
distilled into a different lightweight model
kept online as compact latent predictor
optional sibling simulation branch
```

## 2.7 `future representation` is permanently split by temporal object

```text
single endpoint
multi-step sequence
recurrent rollout
full generated episode
distilled future summary
training-only target
```

---

# 3. Stable ontology families

The family headings are stable in V1. Individual dimensions may be extended or split only when a new anchor exposes a genuinely new scientific distinction.

---

# A. Problem and role of world knowledge

| ID | Stable dimension | Scientific question / why it matters | Typical values / format | Evidence requirement & common trap | Anchor examples |
|---|---|---|---|---|---|
| A01 | **Primary planning bottleneck targeted** | What failure/bottleneck is the paper actually trying to change? Prevents comparing solutions to different problems as if they compete directly. | representation quality; candidate coverage; candidate ranking; direct policy generation; long-horizon simulation; interaction; data scaling | Reconstruct from method + ablations, not only intro wording. | LAW=representation; WoTE=ranking; Epona=shared generative representation/policy; WorldDrive=representation+ranking; W4D=multimodal future-aware selection |
| A02 | **Scientific role of world knowledge** | What function does “world” information perform? | training target/regularizer; current-state representation; consequence predictor; simulator; teacher; value-support feature; policy hidden state | Do not infer role from RGB/BEV/latent format. | LAW=training teacher; WoTE=consequence; Epona=shared representation + simulator sibling; WD=pretraining + teacher; W4D=online future hypothesis |
| A03 | **Host planning paradigm** | What kind of planner exists before/around the WM? | direct regression; direct generative policy; candidate bank + scorer; search/MPC; RL imagination; hierarchical | Needed to isolate WM contribution from planner architecture. | Epona=direct flow policy; WoTE/WD/W4D=candidate selection variants |
| A04 | **Historical mechanism position** | What older planning/representation concept is this closest to, and what is genuinely new? | predictive pretraining; learned cost/value; conditional prediction; contingency planning; model-based search; multimodal planning | Novel terminology is not historical novelty. Record predecessor/control papers. | WoTE↔learned trajectory evaluation; W4D↔multimodal mode selection; LAW↔predictive representation learning |

---

# B. Observation and current-state representation

| ID | Stable dimension | Scientific question / why it matters | Typical values / format | Evidence requirement & common trap | Anchor examples |
|---|---|---|---|---|---|
| B01 | **Sensor / observation input** | What observations are available to the planner/WM? | single-view RGB; multi-view RGB; LiDAR; ego state; map; language; multimodal | Sensor advantage is a confound in planning comparisons. | WoTE camera+LiDAR; Epona front camera; W4D multi-view camera |
| B02 | **Observation-history context** | How much past context is encoded before future modeling? | current frame only; 2-frame aggregation; fixed history; variable history | Separate historical context from predicted future horizon. | Epona variable causal history; W4D previous-frame aggregation |
| B03 | **Current-state substrate** | What numerical object represents the current world? | RGB/video latent; perspective latent; BEV latent/grid; occupancy; object tokens; scene graph; multimodal hidden state | `latent` alone is insufficient. | LAW planner latent; WoTE 8×8 BEV state; Epona F; W4D physical latent |
| B04 | **Current-state semantics / granularity** | What information is intentionally preserved and at what granularity? | appearance; metric geometry; semantics; objects; motion; interaction; planning relevance | Richer state is not automatically more decision-relevant. | W4D depth+semantic+temporal; WD vision+motion space |
| B05 | **Historical/current state vs predicted future state separation** | Does the planner consume a current/history representation, a predicted future representation, or both? | current only; future only; both; shared latent + sibling future | Prevents calling any “world latent” a future latent. | Epona planner consumes F, not VisDiT future; W4D consumes both current and predicted future |

---

# C. Representation provenance and imported priors

| ID | Stable dimension | Scientific question / why it matters | Typical values / format | Evidence requirement & common trap | Anchor examples |
|---|---|---|---|---|---|
| C01 | **Representation origin stack** | Which pretrained/foundation components create the representation before WM-specific learning? | scratch; ImageNet; video foundation; VLM; depth model; self-supervised encoder | Imported prior gain must not be narrated as WM dynamics gain. | WD CogVideoX VAE; W4D metric depth + Grounded-SAM/VLM priors |
| C02 | **Prior injection / supervision mechanism** | How do imported priors enter? | initialization; frozen feature; pseudo labels; positional encoding; distillation; auxiliary loss | “Uses VLM/depth” hides very different causal roles. | W4D depth→3D positional encoding; semantic pseudo-label loss |
| C03 | **Prior trainability / ownership** | Are prior modules frozen, fine-tuned, jointly trained, or used only offline? | frozen; fine-tuned; adapter; offline teacher | Required for causal attribution and reproducibility. | WD frozen/transferred pieces; W4D external pseudo-label/metric-depth sources |
| C04 | **Generic-prior vs WM-specific representation attribution** | What matched evidence separates generic representation quality from future-model specialization? | explicit incremental ladder preferred | Headline no-pretrain→full is invalid if intermediate generic prior is huge. | WD 31.4→84.9 generic; 84.9→86.9 TA-DWM-specific |

---

# D. Action, intention and candidate space

| ID | Stable dimension | Scientific question / why it matters | Typical values / format | Evidence requirement & common trap | Anchor examples |
|---|---|---|---|---|---|
| D01 | **Action-condition provenance** | Where does the action/trajectory condition come from? | expert/logged; planner single output; anchor; refined candidate; sampled policy; user/external; command | `action-conditioned=yes` is scientifically insufficient. | LAW planner waypoint; WoTE refined anchors; WD expert in WM pretrain/candidates in FAR; Epona predicted or external action |
| D02 | **Action representation** | How is ego action encoded numerically? | waypoint sequence; relative pose; control; trajectory token; anchor+residual; diffusion latent | Representation changes what dynamics can condition on. | LAW flattened waypoints; Epona Δθ,Δx,Δy; WD anchor+offset; W4D trajectory→MLP token |
| D03 | **High-level command / intention representation** | Is multimodality structured by semantic intention/command? | none; route command; clustered endpoint; learned intent query; discrete mode | High-level intention can improve planning independently of WM. | W4D K=6 intentions per command |
| D04 | **Candidate-set construction** | Is there an explicit action bank and how is it produced? | no bank; K-means anchors; diffusion samples; autoregressive samples; learned proposals; hand rules | Candidate generation is an independent planning bottleneck. | WoTE/WD anchors; W4D intention modes; Epona no scored bank |
| D05 | **Candidate breadth / support / diversity** | How many alternatives exist and what action space do they cover? | count + support description | More candidates can help until ranking difficulty/distractors dominate. | WoTE 256; WD 256→top-K; W4D 6 |
| D06 | **Candidate refinement, train/test support and pruning** | Are candidates scene-refined, evaluated outside training support, or pruned before WM reasoning? | fixed/refined; seen/unseen; prune stage | Must separate candidate quality from world prediction. | WoTE anchor refinement + unseen 1024 test; WD coarse score→top-K before FAR |

---

# E. Action → world coupling

| ID | Stable dimension | Scientific question / why it matters | Typical values / format | Evidence requirement & common trap | Anchor examples |
|---|---|---|---|---|---|
| E01 | **Action conditioning presence and scope** | Does future prediction depend on ego action, and is the intended effect ego-only or whole-world? | none; ego-only transition; world-conditioned; unclear | Conditioning does not establish correct causal response. | LAW/WD/W4D action-conditioned; WoTE state-action transition |
| E02 | **Action injection mechanism / location** | Where/how does action enter dynamics? | concat+MLP; cross-attention; token interleave; modulation; diffusion condition; recurrent transition | Same action variable can have very different expressive influence. | LAW concat to every token; Epona VisDiT modulation; W4D concat action+latent→cross-attention |
| E03 | **Branch multiplicity and parameterization** | Are alternative futures generated by one conditioned model or separate heads/models? | single branch; shared model+differing condition; shared trunk+heads; independent models | K outputs do not imply K independently learned worlds. | W4D shared predictor across 6 modes |
| E04 | **Branch persistence through temporal rollout** | Once alternatives branch, do they persist, merge, or exist only at an endpoint? | endpoint-only; persistent recurrent branch; search tree; no branching | Important for compute and counterfactual semantics. | WoTE persistent recurrent branches; W4D endpoint modes |
| E05 | **Action-support extrapolation** | Is the world model queried on actions outside the support it was directly trained on? | in-support; refined-near-support; unseen anchors; non-expert/counterfactual; unknown | Candidate-conditioned generation can be out-of-distribution even when visually plausible. | WD teacher queried on planner alternatives; WoTE tests unseen anchors |

---

# F. Dynamics and future temporal modeling

| ID | Stable dimension | Scientific question / why it matters | Typical values / format | Evidence requirement & common trap | Anchor examples |
|---|---|---|---|---|---|
| F01 | **Future object substrate** | What object is predicted/generated? | RGB/video; video latent; BEV; occupancy; objects; scene graph; compact latent; trajectory; reward/value | Format alone does not define planning role. | LAW latent; WoTE BEV; Epona image+trajectory; WD generative latent; W4D compact latent |
| F02 | **Future-state semantics** | What is the predicted object intended to encode? | appearance; geometry; semantics; dynamics; interaction; planning-relevant summary; value | Ask what information is constrained by supervision, not what authors hope latent contains. | WD distilled planning future; W4D physical latent |
| F03 | **Dynamics operator / model class** | What transformation models future evolution? | linear/MLP; Transformer; recurrent transition; diffusion/flow; autoregressive token model; JEPA predictor | Architecture size is not mechanism. | LAW Transformer; WoTE recurrent Transformer; Epona AR+DiT; WD diffusion teacher; W4D cross-attention predictor |
| F04 | **Temporal factorization** | How is future time decomposed? | one endpoint; fixed-window joint; frame-autoregressive; recurrent latent steps; full trajectory one-shot | One model may factorize visual and trajectory time differently. | Epona visual frame-AR vs trajectory 3s one-shot |
| F05 | **Prediction interval, horizon and intermediate-state use** | What is transition step, total horizon, and does planner consume intermediate states? | record step/horizon/endpoint-vs-sequence | Longer horizon is not monotonically better. | LAW 1.5s best; WoTE 0→2→4; W4D t+n endpoint |
| F06 | **Rollout uncertainty, multimodality and robustness** | Does dynamics represent uncertainty/multiple futures and train for free-running error? | deterministic; stochastic; multimodal modes; diffusion; self-generated-context training | Multimodal action output ≠ multimodal world uncertainty. | LAW deterministic; Epona diffusion + Chain-of-Forward; W4D mode branches |

---

# G. Future supervision and truth sources

| ID | Stable dimension | Scientific question / why it matters | Typical values / format | Evidence requirement & common trap | Anchor examples |
|---|---|---|---|---|---|
| G01 | **Factual future truth source** | What directly defines the future target that actually occurred? | logged future frame/latent; simulator state; generated teacher latent; none | Must distinguish factual target from alternatives. | LAW factual latent; Epona factual future image; W4D one factual latent |
| G02 | **Target encoder / target-network treatment** | How is the target representation produced and does gradient flow through it? | same encoder; detached/stop-grad; EMA; frozen teacher; explicit label | Target-network choice changes self-supervision semantics. | LAW detached target branch; WD frozen TA-DWM teacher |
| G03 | **Consequence supervision / teacher** | Who teaches “what happens under this candidate”? | observed data; external simulator; learned WM teacher; self-distillation; none | Consequence teacher and value teacher are different objects. | WoTE simulator BEV; WD TA-DWM teacher; W4D factual mode proxy |
| G04 | **Value / utility supervision / teacher** | Who teaches “how good is this candidate/future”? | expert imitation; rule/PDM score; RL return; human preference; factual consistency; none | Factual consistency is not utility. | WoTE expert+sim rules; WD PDMS preference; W4D no external utility teacher |
| G05 | **Policy / trajectory supervision** | How is ego trajectory itself trained? | expert imitation L1; winner-take-all; generative likelihood/flow; RL; distillation | Planning gains can come from changed policy supervision. | Epona flow on trajectory; WoTE WTA; W4D selected mode L1 |
| G06 | **Mode / branch assignment rule** | If multiple modes exist, how is branch identity/positive branch determined? | fixed semantic mode; nearest expert trajectory; nearest factual future latent; simulator ranking; oracle; learned assignment | This is an independent scientific design choice. | W4D nearest factual latent; WoTE nearest expert anchor for WTA |
| G07 | **Branch supervision coverage** | Do all alternatives get future/score targets, only positive branch, or a subset? | all; positive-only; pairwise; teacher-generated all; unknown | Multi-output architecture may still have one-branch factual supervision. | W4D selected branch reconstruction; WD teacher futures for candidates + ranking |
| G08 | **Other-agent response truth source** | Where do surrounding-agent futures come from under candidate actions? | logged fixed tracks; reactive simulator; learned predictor; observed interaction; absent | Essential for interaction/counterfactual claims. | audited WoTE NAVSIM=PDM cached logged tracks |

---

# H. Multimodal branch identity and assignment

| ID | Stable dimension | Scientific question / why it matters | Typical values / format | Evidence requirement & common trap | Anchor examples |
|---|---|---|---|---|---|
| H01 | **Meaning of a mode/branch** | What does each branch represent? | action mode; intention; future world hypothesis; stochastic policy sample; semantic maneuver | Do not assume modes are counterfactual worlds. | W4D intention+future mode; WoTE action candidates |
| H02 | **Mode identity source** | Is branch identity externally defined or emergent? | command/semantic; clustering; nearest expert; nearest future latent; learned latent | Needed to compare multimodal systems fairly. | W4D endpoint clustering + nearest-factual assignment |
| H03 | **Mode selection during training** | What makes one branch positive? | expert distance; future-latent distance; reward; oracle; likelihood | Positive-branch rule can dominate what scorer learns. | W4D latent-nearest j; WoTE WTA expert-nearest |
| H04 | **Mode coverage / oracle ceiling** | Does candidate bank contain much better actions than deployed selector chooses? | best-of-N/oracle gap; diversity metrics; not evaluated | Separates generation/support bottleneck from ranking bottleneck. | WD best-of-6 oracle 93.6 vs deployed lower |

---

# I. Counterfactuality and reactivity

Counterfactuality is a vector, not one score.

| ID | Stable dimension | Scientific question / why it matters | Typical values / format | Evidence requirement & common trap | Anchor examples |
|---|---|---|---|---|---|
| I01 | **Candidate-specific output branching** | Does architecture emit different future outputs for different candidate actions? | yes/no/partial | Architectural branching only. | WoTE/WD/W4D=yes; LAW=no multi-candidate branch |
| I02 | **Candidate-specific consequence supervision** | Does each alternative action receive its own consequence target? | observed; simulator; learned-teacher; positive-only; none | Teacher-generated alternatives are not observed alternatives. | WD teacher-generated; W4D no K real targets |
| I03 | **Observed/simulated alternative-action ground truth** | Are alternative ego actions paired with outcome truth under those interventions? | none; fixed-agent simulator; reactive simulator; real intervention data | Logs normally provide one factual future. | WoTE candidate ego simulation exists, but not reactive agent alternatives |
| I04 | **Reactive other-agent response under intervention** | Do other agents change behavior as a function of each ego candidate in the supervision/evaluation source? | no/fixed tracks; learned response; reactive simulator; real world | Reactive feasibility ≠ correct causal response. | audited WoTE target path=no |
| I05 | **External intervention-validity evidence** | Is predicted response accuracy under interventions directly validated? | none; simulator consistency; held-out interventions; real closed-loop | Without this, “counterfactual world” remains an architectural claim. | none of five anchors establishes CF5-level real counterfactual truth |

Shorthand CF ladder may still be used, but the five fields above are canonical.

---

# J. World → planning interface

| ID | Stable dimension | Scientific question / why it matters | Typical values / format | Evidence requirement & common trap | Anchor examples |
|---|---|---|---|---|---|
| J01 | **Where world information enters planning** | Which decision stage is changed? | representation learning; candidate generation; refinement; consequence prediction; scoring; final selection; policy training | This is more informative than WM substrate. | LAW representation; WoTE scoring loop; WD transfer+rerank; W4D selector |
| J02 | **Online future computation** | Is a future representation actually computed at deployment? | no; optional; yes-heavy; yes-compact; distilled surrogate | Branch may execute but still be ignored. | LAW may compute but discard; W4D yes; WD lightweight surrogate |
| J03 | **Online future consumption** | Does predicted future causally alter the selected action at inference? | yes/no/optional | This separates LAW/Epona from WoTE/WD/W4D. | direct source/code path required when ambiguous |
| J04 | **Causal coupling direction** | What arrows exist online? | action→world; world→action; bidirectional iterative; shared-state only | `joint` does not imply bidirectional. | Epona action→visual but no same-step visual→trajectory; WoTE future→reward→action |
| J05 | **Action-selection mechanism** | How is final action chosen? | direct regression; direct generative policy; candidate scorer; future scorer; search/MPC; RL policy | Direct policy generation ≠ candidate evaluation. | Epona direct flow policy; W4D future-mode selector |
| J06 | **Consequence model vs decision model separation** | Are “what happens” and “how good” represented by separate modules/objectives? | fused; separate; partially separate; N/A | Critical bottleneck split. | WoTE explicit; WD teacher/surrogate + ranking; W4D consequence + factual-mode classifier |
| J07 | **Task-mode-dependent inference graph** | Does planning, simulation and controllable generation activate different modules? | single graph; modular graphs | Avoid calling optional simulation cost a planning cost. | Epona planning disables VisDiT |

---

# K. Scorer and decision semantics

| ID | Stable dimension | Scientific question / why it matters | Typical values / format | Evidence requirement & common trap | Anchor examples |
|---|---|---|---|---|---|
| K01 | **Scorer presence and placement** | Is there an explicit scorer, and before/after future modeling? | none; coarse scorer; future scorer; multi-stage scorer | Extra scorer can explain gain independently of WM. | WD coarse planner score + FAR; WoTE reward model |
| K02 | **Scorer semantics** | What does a high score mean scientifically? | utility/value; safety/risk; imitation; factual consistency; mode posterior; preference; hybrid | Never call every score “value.” | WoTE utility; WD PDMS preference; W4D factual-mode consistency |
| K03 | **Scorer input scope** | What information can scorer see? | current state; trajectory only; endpoint future; full future sequence; distilled future; action history | More input can improve scorer independent of world accuracy. | WoTE current+future BEV+actions; WD future latent summary |
| K04 | **Reward/value decomposition and aggregation** | Are safety/progress/comfort/etc separate and how combined? | scalar direct; multi-head; hand weights; learned aggregation; pairwise ranking | Utility composition is itself a planning design. | WoTE imitation + NC/DAC/TTC/comfort/progress |
| K05 | **Scorer target / ranking source** | What directly supervises score ordering/class? | simulator metrics; expert distance; PDMS; factual-mode ID; RL return; preference | Target semantics determine what planner optimizes. | WD Bradley-Terry PDMS; W4D focal loss on j |

---

# L. Training topology, jointness and gradient coupling

| ID | Stable dimension | Scientific question / why it matters | Typical values / format | Evidence requirement & common trap | Anchor examples |
|---|---|---|---|---|---|
| L01 | **Training-stage topology** | Is system trained jointly, sequentially, or in teacher/student phases? | joint; pretrain→finetune; freeze→planner; teacher→distill; multi-stage | Deployed end-to-end interface does not imply end-to-end joint optimization. | WD Phase1 WM→planner→FAR; Epona joint |
| L02 | **Representation sharing** | Do world and planning tasks consume the same representation object? | none; shared upstream; transferred identity; partially shared | Distinguish shared representation from shared parameters. | Epona shared F; WD transferred vision/motion representation |
| L03 | **Parameter sharing** | Which modules/weights are actually shared? | shared backbone; separate heads; copied then frozen; independent | Marketing `unified` is insufficient. | Epona shared MST + separate DiTs |
| L04 | **Gradient coupling direction** | Which losses update which modules? | WM→shared encoder; planner→shared encoder; bidirectional joint; stop-grad; teacher/student | This determines causal training influence. | LAW WM loss shapes upstream; W4D selected branch losses interact |
| L05 | **Transfer / freeze / distillation policy** | What knowledge crosses stages and in what form? | initialize+finetune; frozen transfer; latent distill; policy distill; none | Needed for lifecycle and attribution. | WD frozen inherited encoders + FAR distillation |
| L06 | **Joint-loss semantics** | What objectives coexist and can they conflict? | trajectory + future; future + reward; reconstruction + classification + imitation | Joint gain does not reveal which component mattered unless ablated. | Epona L_traj+L_vis; W4D sem+recon+score+traj |

---

# M. Future-knowledge lifecycle and deployment path

This family is one of the main products of the five-anchor synthesis.

| ID | Stable dimension | Scientific question / why it matters | Typical values / format | Evidence requirement & common trap | Anchor examples |
|---|---|---|---|---|---|
| M01 | **Future-knowledge lifecycle class** | What happens to learned predictive knowledge from training to deployment? | training-only shaping; shared-latent shaping; direct online transition; teacher→student distillation; online compact predictor; policy imagination | Replaces coarse online/offline labels. | LAW / Epona / WoTE / WD / W4D each occupy different pattern |
| M02 | **Deployed future object** | What future-related object exists on the actual planning inference path? | none; recurrent BEV; endpoint latent; distilled summary; generated video; hidden policy state | Distinguish training target from deployment object. | WD distilled latent; W4D endpoint latent |
| M03 | **Model-class transformation across lifecycle** | Does future knowledge change model form? | same predictor; decoder removed; heavy→light student; shared representation only | Important for efficiency and semantic fidelity. | WD diffusion teacher→query-decoder student |
| M04 | **Future information bottleneck / compression** | Is only planning-relevant future information intentionally retained? | no compression; learned queries; pooled latent; distilled summary | Compression can improve deployment but hide physical detail. | WD Future Scene Queries |
| M05 | **Future consequence explicitness / inspectability** | Can the deployed consequence be decoded/verified, or is it opaque? | explicit RGB/BEV/occupancy; semantic latent; opaque latent; none | Interpretability is not automatically accuracy, but affects auditability. | WoTE BEV more structured; WD/W4D compact latent |
| M06 | **Optional / sibling future branch** | Is world generation present in model but unnecessary for planning mode? | yes/no/conditional | Prevents overclaiming online imagination. | Epona VisDiT sibling branch |

---

# N. Compute, pruning and latency

| ID | Stable dimension | Scientific question / why it matters | Typical values / format | Evidence requirement & common trap | Anchor examples |
|---|---|---|---|---|---|
| N01 | **Online candidate breadth × future depth** | How many branches are imagined and how many temporal steps per branch? | K × rollout depth | Core deployment frontier. | WoTE 256×recurrent; W4D 6×endpoint; WD top-K×surrogate |
| N02 | **State richness / dynamics cost** | How expensive is each branch's world object/model? | compact latent; BEV; diffusion latent/video | Representation choice must be read with interface demand. | WoTE compact 8×8 BEV supports many branches |
| N03 | **Pruning location / coarse-to-fine compute** | When are candidates reduced before expensive reasoning? | before WM; after WM; multi-stage; none | Changes both compute and candidate quality. | WD 256→top-K before FAR |
| N04 | **Parallelization strategy** | Are candidate branches processed sequentially or batched/parallel? | parallel GPU; recurrent per branch; search tree | The same conceptual method may differ dramatically in real-time feasibility. | WoTE parallel state-action pairs |
| N05 | **Latency accounting scope and hardware** | What does reported latency include and on what hardware? | module-only; planner-only; sensor-to-action; hardware; batch | Never compare 18.7ms module to 53ms full pipeline blindly. | WD full pipeline 53ms A800; WoTE reported candidate setup L20 |
| N06 | **Quality–latency / scale operating curve** | How does performance change with sampling steps, K, horizon or model size? | matched curve preferred | A fastest-speed claim without quality at that operating point is incomplete. | Epona 10 vs 100 steps lacks fully matched planning-quality curve; WD K ablation |

---

# O. Evaluation regime and evidence attribution

| ID | Stable dimension | Scientific question / why it matters | Typical values / format | Evidence requirement & common trap | Anchor examples |
|---|---|---|---|---|---|
| O01 | **Planning evaluation regime** | In what feedback setting is planning evaluated? | open-loop trajectory; NAVSIM non-reactive data-driven; non-reactive sim; reactive closed-loop; CARLA/Bench2Drive; real vehicle | Evaluation regime is part of the claim. | LAW/W4D nuScenes open-loop; WoTE Bench2Drive reactive sim |
| O02 | **World-generation / prediction evaluation regime** | How is world quality evaluated separately from planning? | MSE; semantic accuracy; FID/FVD; occupancy; rollout stability; none | Generation evidence cannot stand in for planning evidence. | Epona FVD; WD FID/FVD |
| O03 | **Training-oracle regime vs evaluation regime** | Are training labels non-reactive while evaluation is reactive, or vice versa? | same/different/unknown | Prevents upgrading training semantics based on evaluation benchmark. | WoTE NAVSIM target path non-reactive + Bench2Drive reactive evaluation |
| O04 | **Strongest matched control immediately before WAM mechanism** | What comparison most directly isolates the claimed world-related component? | exact row-to-row ablation | Mandatory field for every anchor. | WoTE 83.2→85.6 future; WD 87.0→88.1 future; W4D 0.61/0.36→0.50/0.16 |
| O05 | **Attribution ladder** | What other gains appear earlier in the causal stack? | baseline→prior→candidate→WM→scorer→future | Prevent monolithic `WM gain`. | WD canonical ladder |
| O06 | **Baseline comparability / confounds** | Do inputs, backbones, supervision, candidate sets or data differ? | matched / partial / heterogeneous | Headline SOTA tables are often weak causal evidence. | W4D vs LAW backbone differs; WD single-view vs multimodal baselines |
| O07 | **Prediction fidelity → planning relevance evidence** | Is there direct evidence that better world prediction yields better planning? | matched correlation/ablation; suggestive; absent | Never assume monotonic link. | OccWorld/LAW horizon evidence warns against monotonic assumptions |
| O08 | **Source / code verification status** | Are decision-critical inference/supervision claims paper-only or source-verified? | paper; official code; exact commit; unresolved | Required when inference path is ambiguous. | LAW/WoTE/WD/W4D source-audited |
| O09 | **Oracle / deployed gap and candidate ceiling** | How much better could planning be with oracle selection of existing candidates? | best-of-N gap / not evaluated | Separates candidate support from ranking. | WD oracle best-of-6 |
| O10 | **Proves / does-not-prove / strongest alternative explanation** | What scientific conclusion is justified and what remains unresolved? | compact three-part statement | Mandatory symmetric evidence boundary for every anchor. | W4D proves WM-selector bundle helps; not true K-way counterfactual truth |

---

# P. Safety, uncertainty, interaction and physical validity

| ID | Stable dimension | Scientific question / why it matters | Typical values / format | Evidence requirement & common trap | Anchor examples |
|---|---|---|---|---|---|
| P01 | **Explicit safety/risk in world state** | Is risk/safety represented as part of predicted world state? | explicit field/channel/object; implicit latent; absent | Absence is not automatically a research gap. | five anchors mostly implicit in world state |
| P02 | **Explicit safety/risk in decision value** | Is safety encoded in reward/scorer rather than state? | collision/TTC/rule heads; learned risk; implicit; none | Risk can live in valuation rather than world representation. | WoTE explicit NC/TTC/etc heads |
| P03 | **Uncertainty representation / calibration** | Does model quantify epistemic/aleatoric uncertainty or confidence? | stochastic samples; probabilities; calibrated scores; none | Multimodality alone is not calibrated uncertainty. | W4D softmax mode score is not proven calibrated uncertainty |
| P04 | **Multi-agent interaction modeling level** | How are other agents represented and coupled? | implicit pixels/latent; explicit objects; BEV occupancy; learned response; game interaction | Token interaction ≠ behavioral reaction. | LAW token self-attention; WoTE BEV agents but fixed logged responses in audited targets |
| P05 | **Physical / kinematic / causal consistency constraints** | What constrains imagined futures to obey geometry/ego motion/physics? | action condition; kinematic model; simulator; semantic/occupancy constraints; none | Plausible video is not physical correctness. | WD trajectory conditioning; WoTE simulator targets |
| P06 | **Long-horizon error accumulation and robustness** | Does deployment recursively consume self-predictions, and how is drift handled? | no rollout; recurrent compact rollout; noise/self-generated-context training | Long visual stability and planning robustness are different capabilities. | Epona Chain-of-Forward; WoTE recurrent BEV |
| P07 | **Rule/legal/corner-case semantics** | Where are traffic rules, rare events and compliance represented/tested? | explicit reward; simulator metric; learned latent; benchmark only | Benchmark score is not proof latent encodes rules. | WoTE explicit reward; Epona claimed implicit red-light knowledge requires evidence boundary |

---

# 4. Canonical five-anchor mechanism profiles

These are not substitutes for the detailed matrix; they provide a sanity check for the ontology.

## LAW

```text
single planner action
→ action-aware latent predictor
→ factual future latent target
→ auxiliary predictive loss
→ shared representation improves
→ predicted future does not choose deployed action
```

Primary ontology identity:

```text
A02 training representation shaping
J03 online future consumption = NO
M01 training-only predictive knowledge
```

## WoTE

```text
256 candidates
→ recurrent compact BEV consequences
→ explicit imitation + simulator utility heads
→ weighted reward
→ argmax
```

Primary ontology identity:

```text
J05 candidate evaluator
K02 explicit utility/value
I04 reactive alternative-agent truth = NO in audited NAVSIM target path
M01 same learned compact transition remains online
```

## Epona

```text
history → shared latent F
F → TrajDiT → direct generative trajectory
F + action → VisDiT → visual future
joint L_traj + L_vis shapes F
planning can disable VisDiT
```

Primary ontology identity:

```text
L02/L04 shared representation+gradient jointness
J05 direct generative policy
M06 optional sibling future branch
```

## WorldDrive

```text
TA-DWM generative pretraining
→ transfer/freeze vision+motion representation
→ base candidate planner
→ heavy TA-DWM future teacher during FAR training
→ lightweight distilled future summary online
→ preference ranking
```

Primary ontology identity:

```text
C04 generic-vs-WM attribution mandatory
G03 consequence teacher = TA-DWM
G04 value teacher = PDMS/oracle
M01 teacher→student distilled foresight
```

## World4Drive

```text
current physical latent + 6 intentions
→ 6 trajectories
→ 6 action-conditioned future latents
→ nearest-to-one-factual-future branch defines target mode
→ ScoreNet predicts that mode
→ online highest-score mode selected
```

Primary ontology identity:

```text
K02 factual-future consistency / mode selection
I01 branching = YES
I03 K-way alternative factual ground truth = NO
M01 direct online compact latent foresight
```

---

# 5. Minimum paper quality gate under Ontology V1

A core/anchor paper is **not normalized** until all of the following are satisfied:

```text
1. architecture/dataflow reconstructed end to end;
2. training and inference graphs separated;
3. current-state and future-state objects distinguished;
4. action provenance/representation/candidate support explicit;
5. future target and truth lineage explicit;
6. mode/branch assignment explicit when multimodal;
7. counterfactual vector I01–I05 filled;
8. world→planning interface J01–J07 filled;
9. scorer semantics K01–K05 filled;
10. training/jointness L01–L06 filled;
11. future-knowledge lifecycle M01–M06 filled;
12. online compute/latency boundary N01–N06 filled;
13. evaluation regime O01–O03 labeled correctly;
14. strongest matched control O04 identified;
15. generic-prior / planner / scorer / future attribution separated where possible;
16. strongest evidence, strongest alternative explanation, proves / does-not-prove recorded;
17. source verification status recorded for decision-critical ambiguities.
```

A paper may legitimately have many `ABSENT` or `NOT EVALUATED` cells. Completeness means the questions were asked, not that every mechanism exists.

---

# 6. Ontology extension rule

Ontology V1 is a stable baseline, not a closed universe.

A new paper may add/split a dimension only if:

```text
1. an important mechanism/evidence property cannot be expressed by existing dimensions;
2. the distinction changes scientific comparison, supervision interpretation, deployment behavior, or evidence strength;
3. it is not merely a paper-specific layer/module name;
4. at least one existing anchor can be meaningfully re-examined under the new dimension;
5. the new dimension receives a definition, allowed values, evidence rule and misclassification warning.
```

When extending:

```text
new paper
→ fill all existing ontology dimensions first
→ identify residue not representable
→ propose new/split dimension
→ back-project onto prior anchors
→ update ontology version
```

Do not silently change the meaning of an existing ID.

---

# 7. What Ontology V1 is designed to prevent

```text
“latent WM is better than video WM”
→ substrate-only comparison

“action-conditioned = counterfactual”
→ conditioning confused with intervention truth

“joint world-action model”
→ shared loss confused with online causal feedback

“future score = value”
→ factual-mode classification confused with utility

“WM improves 50 points”
→ foundation prior / candidate / scorer gains collapsed together

“closed-loop result proves counterfactual dynamics”
→ evaluation feedback confused with supervision causality

“better FID/FVD means better planner”
→ world fidelity confused with decision relevance

“risk is absent, therefore risk module is the gap”
→ missing component confused with research problem
```

---

# 8. Immediate use

Next artifact:

```text
landscape/WAM_COMPARISON_MATRIX_V1.md
```

The matrix must project LAW / WoTE / Epona / WorldDrive / World4Drive across the stable IDs above, grouped by family rather than as one unreadable 80-column table.

After that, resume new core-WAM anchors. Every new anchor must be projected into Ontology V1 and may only extend it through the extension rule above.
