# P0064 Discrete-WAM — Ontology V1 + V1.1 + V1.2 + V1.3 Projection

Last updated: 2026-09-15

Status: **FULL DIMENSION-FIRST PROJECTION — COMPLETE FIRST PASS**

Canonical analysis:

```text
papers/deep_analysis/P0064_DISCRETE_WAM_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_DISCRETE_WAM_AUDIT.md
```

Coordinate system:

```text
WAM_DIMENSION_ONTOLOGY_V1.md
+ WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
+ WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
+ WAM_DIMENSION_ONTOLOGY_V1_3_AMENDMENT.md
```

Method-version scope:

```text
arXiv:2606.05645v2
2026-06-09
official implementation repository not identified as of 2026-09-15
```

Core warning:

```text
shared discrete world-policy framework
!= one shared world/action codebook

joint world-policy generation capability
!= future-world generation required for deployed planning
```

---

# A. Problem and role of world knowledge

| ID | Discrete-WAM value | Evidence / interpretation |
|---|---|---|
| A01 | **unify visual-world prediction and policy generation in one discrete generative backbone; improve compositional action-conditioned reasoning and policy decoding** | Paper motivates direct state→action policies as weak on dynamics and continuous-latent WMs as weakly aligned with policies. |
| A02 | **world/policy multitask pretraining + action-conditioned future generation + shared representation regularization** | World knowledge primarily shapes the shared Transformer before downstream action-only planning. |
| A03 | **hierarchical decision-conditioned direct action-token generator** | Deployed NAVSIM planner predicts a high-level decision then edits action tokens; no explicit online future scorer. |
| A04 | **discrete world-action generative modeling + hierarchical decision prior + token editing** | Scientific family combines WAM joint training with discrete-diffusion policy generation rather than online MPC-style consequence selection. |

---

# B. Observation and current-state representation

| ID | Discrete-WAM value | Evidence / interpretation |
|---|---|---|
| B01 | **camera visual observation + ego/navigation/context information** | Paper centers visual-token input plus structured context; exact view configuration should be source-verified if code appears. |
| B02 | **current/history visual context used as condition for future generation/planning** | World tasks predict future tokens from current/context sequence. |
| B03 | **discrete VQ visual tokens projected into a shared Transformer hidden space** | Current world is represented by quantized visual symbols, not BEV/object state. |
| B04 | **appearance/spatiotemporal scene semantics implicit in VQ tokens** | No explicit object/risk/occupancy meaning per token is guaranteed. |
| B05 | **current visual/context tokens are used online; predicted future visual tokens are optional capability, not required for primary planner** | Deployment planning consumes current context + decision/action policy states. |

---

# C. Representation provenance and imported priors

| ID | Discrete-WAM value | Evidence / interpretation |
|---|---|---|
| C01 | **VQ-style visual tokenizer + learned action-token prototype space + ~1B shared Transformer** | Visual and action representations have different tokenization origins. |
| C02 | **visual VQ indices and action prototype indices are independently produced then embedded into common hidden dimension** | `aligned/shared token space` should not be read as one codebook. |
| C03 | **multi-stage pretraining → LoRA SFT/RL adaptation; exact module freezing SOURCE-UNVERIFIED** | No official implementation identified. |
| C04 | **PARTIALLY ISOLATED** | From-scratch/FT/LoRA-SFT and decision/RL ablations exist, but full joint-world-policy contribution is not cleanly isolated. |

---

# D. Action, intention and candidate space

| ID | Discrete-WAM value | Evidence / interpretation |
|---|---|---|
| D01 | **logged/factual future trajectory during supervised training; generated action sequence at deployment** | World modeling uses teacher-forced future action condition; policy generates action tokens online. |
| D02 | **2D ego acceleration tokens; 60×60 ≈ 3,600 prototypes; trajectory reconstructed/integrated from token sequence** | Strongly physical action-token semantics compared with visual tokens. |
| D03 | **explicit high-level decision token / behavioral skeleton** | Decision precedes dense action editing. |
| D04 | **~400 high-level decision candidates; no WoTE-style online bank of future-world-evaluated full trajectories** | Decision alternatives are structured path×speed candidates. |
| D05 | **decision support controlled by number/top-d of anchors; action sequence has combinatorial token support** | Paper reports decision-count trade-off; more anchors can hurt optimization. |
| D06 | **iterative parallel action-token editing with confidence/JS/freeze schedules; RL explores decision-trajectory combinations** | Refinement is token-space policy optimization, not world-rollout pruning. |

---

# E. Action → world coupling

| ID | Discrete-WAM value | Evidence / interpretation |
|---|---|---|
| E01 | **YES in world/world-policy tasks: future visual prediction conditioned on ego action tokens** | Action-conditioned future generation is explicit. |
| E02 | **action tokens are placed in shared sequence / task-specific attention graph before same-step future visual tokens** | Injection occurs through shared Transformer attention/sequence factorization. |
| E03 | **one shared model conditioned by action sequence; no separately parameterized WMs per candidate** | Alternative action sequences can produce alternative outputs through shared parameters. |
| E04 | **world-policy sequence interleaves action/world states across physical future timesteps** | Branching can persist if different generated action sequences are rolled through joint sequence, but primary planning does not require this online. |
| E05 | **training action support comes from logged/teacher-forced futures plus generated-policy/posttraining distribution; intervention extrapolation not externally validated** | Action-conditioned controllability is not proof of out-of-support causal validity. |

---

# F. Dynamics and future temporal modeling

| ID | Discrete-WAM value | Evidence / interpretation |
|---|---|---|
| F01 | **discrete future visual/world tokens** | Future substrate is quantized visual state, decodable to video/image. |
| F02 | **appearance + scene evolution + implicit motion/interaction** | Physical/interaction semantics are learned implicitly through future visual supervision. |
| F03 | **shared decoder-only Transformer + discrete token editing / discrete-diffusion-style generation** | Dynamics are represented as conditional token distributions rather than continuous latent regression. |
| F04 | **fixed-horizon sequence; world-policy task interleaves A_h then V_h across future physical steps** | Generation order has temporal meaning across h. |
| F05 | **reported short-horizon world generation around 4 s / 8 frames; planner trajectory horizon NAVSIM 4 s** | Intermediate future tokens can be generated, but primary planning does not need them online. |
| F06 | **generative/token-edit stochasticity; alternative action-conditioned generations possible; no calibrated predictive uncertainty** | Diversity/distributional output is not calibrated epistemic uncertainty. |
| F07 | **CURRENT/HISTORY + ACTION → CHRONOLOGICALLY UNSEEN FUTURE VISUAL TOKENS** | Genuine future-directed world prediction, unlike random-mask same-window JEPA completion. |
| F08 | **PHYSICAL FUTURE INDEX in interleaved A_h/V_h sequence + separate INTERNAL TOKEN-EDIT REFINEMENT ROUNDS** | Edit rounds are solver/refinement time, not physical scene time. |

---

# G. Future supervision and truth sources

| ID | Discrete-WAM value | Evidence / interpretation |
|---|---|---|
| G01 | **logged factual future visual tokens** | Future world target is encoded from the realized future observation sequence. |
| G02 | **VQ token target / reconstruction path; no EMA target encoder central to audited formulation** | Different target semantics from Drive-JEPA. |
| G03 | **same-sequence factual future; alternative-action ground-truth futures absent** | Teacher-forced action condition accompanies one realized future. |
| G04 | **EPDMS/PDM-style quality is used in decision target construction/post-training reward, not as world-state truth** | Value truth must be separated from visual consequence truth. |
| G05 | **logged future trajectory/action sequence + downstream policy/RL reward** | Policy has direct action supervision independent of world loss. |
| G06 | **high-level decision winner selected by EPDMS-style evaluation; token editing itself has dense action targets** | Decision branch identity is value/evaluator selected rather than purely latent clustering. |
| G07 | **dense multi-loss supervision across visual tokens, action tokens, trajectory/acceleration geometry, decision/special positions** | Joint training is strongly supervised, but exact task ratios are source-unverified. |
| G08 | **logged factual surrounding-world future; reactive alternative-action response truth NOT ESTABLISHED** | Core counterfactual boundary. |

---

# H. Multimodal branch identity and assignment

| ID | Discrete-WAM value | Evidence / interpretation |
|---|---|---|
| H01 | **high-level decision token / policy branch; action-token stochastic sequence** | Modes are primarily behavioral decisions, not K separately supervised worlds. |
| H02 | **path candidate × speed-profile structure produces decision vocabulary** | Explicit behavior skeleton. |
| H03 | **EPDMS-style winner selection for decision target; RL later explores decision/trajectory combinations** | Branch identity incorporates downstream driving-quality supervision. |
| H04 | **decision-number/top-d trade-off studied; no single clean oracle best-of-N future-world ceiling** | More alternatives can increase reward variance/optimization difficulty. |

---

# I. Counterfactuality and reactivity

| ID | Discrete-WAM value | Evidence / interpretation |
|---|---|---|
| I01 | **YES: action perturbations / alternative action tokens produce different future-world outputs** | Model is action sensitive and controllable. |
| I02 | **NO per-action observed alternative future targets** | Training has one factual future for the executed/logged action. |
| I03 | **NO matched real/simulator truth for all perturbations used in surprise study** | Alternative generations are hypotheses. |
| I04 | **reactive surrounding-agent intervention truth NOT ESTABLISHED** | Generated video can change around ego action, but causal behavioral validity is not directly supervised. |
| I05 | **ABSENT direct external intervention-validity benchmark** | Surprise/PDMS correlation is useful but not causal validation. |

---

# J. World → planning interface

| ID | Discrete-WAM value | Evidence / interpretation |
|---|---|---|
| J01 | **shared representation / pretraining and optional joint world-policy generation; primary planning uses decision-conditioned action generation** | World knowledge enters policy primarily through shared weights/representations, not online evaluator. |
| J02 | **NO mandatory online future-world computation for primary NAVSIM planning; YES as optional generation capability** | Must distinguish model capability from planner execution graph. |
| J03 | **NO mandatory online future-world consumption for reported action selection** | Policy can produce D→A directly. |
| J04 | **training/world-policy: action→same-step world and prior world→later action through interleaved sequence; planning inference: current context→decision→action** | Strong joint sequence coupling exists in capability mode but not mandatory deployment loop. |
| J05 | **direct hierarchical generative policy** | Final action does not require a consequence scorer/argmax over generated worlds. |
| J06 | **NO dedicated deployed consequence→utility model** | EPDMS appears in decision-label/reward construction, not as online world scorer. |
| J07 | **task-mode-dependent graph: world generation / joint world-policy generation / planning-only policy decoding** | Same backbone supports multiple execution graphs. |
| J08 | **GENERATIVE TOKEN-EDIT / DISCRETE-DIFFUSION REFINEMENT** | One edit round updates policy tokens; does not advance environment time. |
| J09 | **world-generation mode: ACTION TOKEN SEQUENCE; primary planning mode: NOT APPLICABLE as no planner→world feedback is required** | Action is the control carrier to visual generation when that task is run. |

---

# K. Scorer and decision semantics

| ID | Discrete-WAM value | Evidence / interpretation |
|---|---|---|
| K01 | **NO deployed candidate-consequence scorer in primary policy path; high-level decision classifier + RL reward instead** | Important difference from WoTE/WorldDrive/World4Drive. |
| K02 | **decision token semantics = high-level behavior selected/trained with EPDMS-style quality; action policy refined by reward** | This is behavioral value guidance, not world-future likelihood score. |
| K03 | **decision head sees current/shared context; not generated future visual consequence in primary planner** | Future world is not an online scorer input. |
| K04 | **EPDMS/PDM-style reward decomposes safety/progress/comfort/rules during target/reward construction** | Explicit safety exists on decision/value side, not visual state representation. |
| K05 | **decision CE target from evaluator-selected candidate; GRPO reward for decision/action combinations** | Value supervision is separate from world visual-token target. |

---

# L. Training topology, jointness and gradient coupling

| ID | Discrete-WAM value | Evidence / interpretation |
|---|---|---|
| L01 | **multi-stage: world-oriented visual pretraining → joint vision/action stage → LoRA policy/RL adaptation** | Do not collapse stages into one joint objective. |
| L02 | **YES shared Transformer hidden representation; modality-specific embeddings/vocabularies** | Representation unification is hidden-space/sequence-level, not one codebook. |
| L03 | **YES substantial shared backbone parameters** | Stronger parameter sharing than Metis/Epona branch-specific experts. |
| L04 | **YES visual/action losses can shape shared backbone during joint stage; exact detach/task-routing SOURCE-UNVERIFIED** | Code unavailable. |
| L05 | **pretraining knowledge retained via shared weights; LoRA used to preserve/adapt policy** | No teacher→student future-latent distillation. |
| L06 | **multi-loss visual + action + acceleration + trajectory + position + special-token + decision objective** | Final performance is a bundle. |
| L07 | **NOT APPLICABLE to world↔planner recurrent state; token-edit rounds receive token prediction objectives under corruption schedule** | Editing supervision is solver/policy refinement, not intermediate physical-state supervision. |

---

# M. Future-knowledge lifecycle and deployment path

| ID | Discrete-WAM value | Evidence / interpretation |
|---|---|---|
| M01 | **joint/multitask world-policy pretraining → shared policy/backbone knowledge → action-only planning graph** | Canonical lifecycle. |
| M02 | **NONE mandatory in primary planning; optional future visual generation capability exists** | Contrast with online future evaluators. |
| M03 | **explicit future-world computation used in training/capability mode; skipped in primary planning forward graph** | Model class stays shared Transformer but task/execution path changes. |
| M04 | **implicit compression into shared weights/hidden representation rather than explicit distilled future latent** | Closest to training-time knowledge shaping. |
| M05 | **optional inspectable visual future if generation mode is run; no inspectable future on ordinary planning path** | Interpretability depends on task mode. |
| M06 | **YES — future visual generation is an optional sibling/capability mode relative to planning** | Similar lifecycle-level optionality to Epona/Metis, with stronger parameter sharing. |

---

# N. Compute, pruning and latency

| ID | Discrete-WAM value | Evidence / interpretation |
|---|---|---|
| N01 | **decision candidates ~400 at target construction; online token-edit rounds configurable; deployed future-world depth 0 for primary planner** | Candidate/solver axes should not be conflated. |
| N02 | **~1B shared Transformer + VQ token interface** | Exact active-parameter count per task awaits code. |
| N03 | **future visual-token decoding/generation can be skipped for primary planning** | Major deployment branch pruning by task mode. |
| N04 | **parallel action-token editing rather than strict action AR decoding** | Main efficiency claim. |
| N05 | **paper reports discrete diffusion policy decoder latency advantage relative to AR action decoding** | Exact code-level benchmark scope/source unavailable. |
| N06 | **strong scheduler/round quality–compute trade-off; more rounds not monotonic** | Token editing round is policy refinement compute, not physical horizon. |

---

# O. Evaluation regime and evidence attribution

| ID | Discrete-WAM value | Evidence / interpretation |
|---|---|---|
| O01 | **NAVSIM v1/v2 non-reactive data-driven/pseudo-simulation planning + offline future-video generation evaluation** | Not reactive closed-loop proof. |
| O02 | **YES: FID/FVD short-horizon world-generation metrics** | Dedicated generation fidelity exists. |
| O03 | **logged factual world/action training; NAVSIM planning evaluation; perturbation surprise analysis** | Evaluation does not create alternative-action truth. |
| O04 | **world-pretraining control weak/modest: from scratch 89.8, FT 89.7, vision-oriented pretrain+LoRA 90.0** | Does not cleanly isolate full joint world-policy training. |
| O05 | **decision modeling + token editing + RL + world-oriented pretraining all independently vary** | Mandatory attribution decomposition. |
| O06 | **headline SOTA comparisons heterogeneous in architecture/data/training** | Within-paper controls are stronger. |
| O07 | **NO clean fidelity→planning causal link** | FID/FVD are not connected by matched monotonic ablation to EPDMS. |
| O08 | **paper/appendix verified; implementation source unavailable/not identified** | Code-level mechanism remains pending. |
| O09 | **decision support / policy sampling headroom studied; not a future-world oracle ranking ceiling** | Candidate count and post-training affect performance. |
| O10 | **see normalized evidence boundary below** | Strong claims must remain symmetric. |

O10 normalized boundary:

```text
PROVES:
strong shared-backbone discrete world/policy capability;
action-conditioned world generation;
strong hierarchical token-edit planner;
planning and generation competence in reported benchmarks.

DOES NOT PROVE:
one shared codebook;
online world imagination required for planning;
full joint pretraining is the dominant planning-gain source;
intervention-correct counterfactual world dynamics.
```

---

# P. Safety, uncertainty and interaction semantics

| ID | Discrete-WAM value | Evidence / interpretation |
|---|---|---|
| P01 | **NO explicit risk field/state; risk implicit in visual tokens/world distribution** | Surprise can act as a diagnostic but is not an explicit risk-state channel. |
| P02 | **YES on decision/reward side via EPDMS/PDM-style safety/rule/comfort terms; no deployed explicit future utility scorer** | Risk/value lives more clearly in supervision/posttraining than world state. |
| P03 | **token probabilities/entropy/surprise exist; calibration NOT ESTABLISHED** | Confidence is used for editing schedules but should not be called calibrated uncertainty. |
| P04 | **other-agent interaction implicit in visual world tokens/video generation** | No explicit game/agent-response model. |
| P05 | **action-conditioned future generation + trajectory/acceleration geometry losses; no explicit physical simulator constraint** | Visual plausibility/action sensitivity is not physical correctness proof. |
| P06 | **short-horizon future generation; no deployed recursive world rollout in primary planning, so online WM drift is not the planner bottleneck** | Token-edit policy refinement has its own accumulation/schedule effects. |
| P07 | **traffic/rule semantics enter NAVSIM/EPDMS target/reward evaluation; not proven as explicit visual-token rule representation** | Benchmark compliance ≠ interpretable latent rule state. |

---

# Residue / ontology decision

Discrete-WAM exposes one real representational distinction:

```text
shared codebook
vs
separate modality vocabularies embedded into one hidden/sequence space
```

But current prior anchors are overwhelmingly continuous-latent, so back-projection would mostly produce `NOT APPLICABLE` and would not yet improve cross-paper discrimination.

Decision:

```text
NO ONTOLOGY V1.4 YET

RESIDUE WATCHLIST:
Discrete representation alignment topology
(shared codebook / disjoint vocabularies / common hidden interface)
```

Re-test when another discrete-token WAM anchor is normalized.

The apparent second residue — world/action token generation order — is already represented by:

```text
F04 + E02 + J04 + F08
```

and is therefore merged rather than added.
