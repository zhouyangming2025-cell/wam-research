# WAM Dimension Discovery Log

Last updated: 2026-09-15

Status: **HISTORICAL DISCOVERY LOG — retained as provenance; the consolidated ontology is a historical comparison baseline, not current route authority.**

## Purpose

This file records comparison dimensions discovered while deeply reading planning-centric WAM anchor papers. It is not a taxonomy to be imposed on papers. Dimensions must emerge from concrete mechanisms, training signals, evaluation designs and evidence boundaries.

The governing rule is:

> **Every time a paper introduces a module, representation, condition, loss, training stage, rollout, scorer, query, decoder, reward, supervision source, evaluation setup or claimed capability, immediately ask: do other papers perform the same scientific function? If yes, how and why differently? If no, is this a genuinely new comparison dimension or only an implementation detail?**

This prevents paper-centric reading from staying inside each author's preferred narrative.

## Reading protocol

Single-paper understanding uses the useful parts of:

- `skills/external/paper-deep-reader-skill/`: mainline map, mechanism map, prerequisite map, claim-evidence table, formula/visual ledger, Before/After/Diff/Trade-off;
- `skills/external/agent-paper-reader/`: claim → evidence → interpretation → what remains unproven; explicit reproduction/falsification thinking.

WAM-specific extension:

```text
paper mechanism
→ identify scientific function
→ search/recall analogues in other anchors
→ compare function, implementation, supervision, deployment and evidence
→ add/split/merge provisional dimension
```

A dimension should survive only if it helps distinguish scientifically meaningful choices across multiple papers. A one-off layer name is not automatically a dimension.

## Anchor sequence for ontology discovery

```text
P0048 LAW          COMPLETE v2 first pass
P0045 WoTE         COMPLETE v2 first pass
P0001 Epona        NEXT — dimension-first rebuild
P0042 WorldDrive   existing strong audit; needs re-projection into discovered dimensions
P0046 World4Drive  existing strong audit; needs re-projection into discovered dimensions
```

After these five anchors, perform the first merge/split pass and create `WAM_DIMENSION_ONTOLOGY_V1.md`. The ontology remains extensible when later anchors reveal genuinely new axes.

---

# LAW-derived provisional dimensions

Source analysis: `papers/deep_analysis/P0048_LAW_DEEP_ANALYSIS_V2.md`

The following IDs are temporary discovery IDs (`LAW-Dxx`), not permanent ontology IDs.

| ID | Provisional dimension | LAW position | Why this dimension matters / immediate horizontal question |
|---|---|---|---|
| LAW-D01 | **World-state semantics** | planner-facing perspective-view or BEV latent | What information does the modeled state preserve: appearance, geometry, semantics, interaction, planning relevance, value? `latent/RGB/BEV` alone is insufficient. |
| LAW-D02 | **Action-condition provenance** | planner's own single predicted waypoint sequence | Is the condition expert/logged action, predicted ego path, anchor, candidate, command, low-level control or imagined policy action? |
| LAW-D03 | **Action multiplicity / branching** | one predicted action | Does the model reason about one factual/planner action or many alternatives simultaneously? |
| LAW-D04 | **Action representation** | full waypoint sequence flattened to `2M` vector | How is action parameterized: trajectory, token, anchor+residual, control, command, policy latent? |
| LAW-D05 | **Action injection mechanism** | trajectory vector concatenated to every visual token then MLP | Where/how does action enter dynamics: concat, cross-attention, token interleaving, diffusion condition, recurrent transition? |
| LAW-D06 | **Action→world causal direction vs world→action feedback** | action conditions WM; predicted future does **not** feed back into deployed action selection | `action-conditioned WM` and `WM-based action selection` are separate properties. This distinction is mandatory. |
| LAW-D07 | **Dynamics operator** | deterministic Transformer blocks with token self-attention | Compare deterministic transition, recurrent/autoregressive rollout, diffusion/flow, JEPA predictor, discrete token dynamics, joint generator. |
| LAW-D08 | **Cross-state interaction capacity** | Transformer self-attention across latent positions beats linear/MLP variants | Does the dynamics model allow interactions among spatial/entity tokens, or mostly per-token transformation? This may reflect interaction modeling capacity, not merely architecture size. |
| LAW-D09 | **Future-target substrate** | encoded future visual/planner latent | Is target raw video, BEV, occupancy, objects, scene graph, latent, trajectory, reward/value, risk? |
| LAW-D10 | **Future-target provenance** | one factual observed future frame encoded to latent | Factual logged future vs simulated target vs teacher-generated target vs directly observed alternative-action consequences. |
| LAW-D11 | **Target-network treatment** | same learned encoder provides target; audited reconstruction path stop-gradients target | Shared online encoder, EMA target, frozen foundation encoder, independent teacher, explicit labels? |
| LAW-D12 | **Supervision economy / annotation dependence** | latent task itself needs no manual future labels; host perception-based variant still has perception losses | Distinguish WM-task annotation cost from full-system annotation cost and pretrained-prior cost. |
| LAW-D13 | **Prediction horizon** | selected single future frame; 0.5/1.5/3/10 s ablated; 1.5 s best in reported setup | Longer horizon is not automatically more useful. Record prediction, supervision, rollout and planner horizons separately. |
| LAW-D14 | **Predictive-task difficulty vs informativeness** | too-near future weak signal; too-far future hard/uncertain; intermediate best | Future target design has an information/difficulty trade-off independent of raw horizon length. |
| LAW-D15 | **WM attachment depth / architectural ownership** | auxiliary predictive branch attached to an existing planner representation | Auxiliary loss, pretraining stage, shared backbone, deployed transition model, central generator, external simulator? |
| LAW-D16 | **Gradient coupling direction** | WM loss shapes shared upstream parameters; target latent detached in audited path | Which modules receive gradients from world prediction? Does planner teach WM, WM teach planner, both, or teacher/student distillation? |
| LAW-D17 | **Inference-path future computation** | branch may execute but output is discarded by planning path | Separate “future is computed” from “future is actually used.” |
| LAW-D18 | **Inference-path future consumption** | no candidate refinement/ranking from predicted future | Does a future representation causally alter the final action at inference? |
| LAW-D19 | **Decision semantics of future information** | representation-shaping teacher/regularizer | Future can function as training target, representation teacher, simulator, evaluator, reward/value, policy hidden state, or generated artifact. |
| LAW-D20 | **Candidate-consequence evaluation** | absent | Is there an explicit action candidate → consequence → score loop? |
| LAW-D21 | **Counterfactual scope** | no alternative-action factual supervision; single planner action conditioned on one factual future | Distinguish action-conditioned prediction, multi-branch imagination, simulated alternatives, and behaviorally validated counterfactuals. |
| LAW-D22 | **Representation portability** | same predictive objective works on perspective-view and BEV planner latents | Is the WM mechanism tied to one state substrate or portable across planner architectures? |
| LAW-D23 | **Host planner dependence** | LAW augments both perception-free and perception-based host planners | Gains may depend on baseline planner capacity/supervision; isolate WM contribution from host architecture. |
| LAW-D24 | **Evaluation feedback regime** | nuScenes open-loop; NAVSIM non-reactive data-driven; CARLA reactive closed-loop | Evaluation regime is part of the claim. Do not merge all “planning scores” into one evidence level. |
| LAW-D25 | **Evidence attribution strength** | matched latent-prediction/action-condition ablations are stronger than headline SOTA | Which experiment isolates the claimed WM mechanism rather than mixing backbone, supervision, candidate set or scorer changes? |
| LAW-D26 | **Deployment imagination cost** | no future representation is consumed for online action selection | Full rollout, compact latent online, distilled future, or training-only predictive cost? |
| LAW-D27 | **State-prediction fidelity vs decision relevance** | latent MSE is optimization target, planning metrics are downstream evidence; no proof of monotonic relation | Does better world prediction actually imply better planning? Must be tested, not assumed. |
| LAW-D28 | **Interaction modeling level** | self-attention permits latent-token interaction, but no explicit agent-response/counterfactual interaction model | Token interaction, object interaction and behavioral reaction are different notions and must not be conflated. |
| LAW-D29 | **Future uncertainty / multimodality** | deterministic single future target/prediction in core setup | Does model represent multiple possible worlds, stochasticity or calibrated uncertainty? |
| LAW-D30 | **Safety/risk semantics** | only implicit through representation and planning metrics; no explicit risk state/value | Where, if anywhere, are collision, TTC, uncertainty or safety encoded inside the learned world rather than only evaluated afterward? |

---

# LAW evidence that created/sharpened dimensions

## E1 — action condition matters, but does not imply counterfactual planning

LAW reports stronger planning when the latent predictor receives both visual latent and predicted trajectory than when it receives visual latent only. This supports `LAW-D02/04/05`, but not a claim of behaviorally correct alternative-action futures. The source path has one planner trajectory and one factual future.

## E2 — online consumption must be separated from training-time influence

Source audit shows the waypoint is produced before future-latent prediction, and test-time planning discards the future-latent outputs. This directly motivated `LAW-D06`, `LAW-D15–20`.

## E3 — horizon is a task-design variable, not a monotonic capability axis

The 1.5 s target outperforms 0.5, 3 and 10 s settings in LAW. This motivated `LAW-D13–14` and is a warning for later papers that advertise longer rollout horizons.

## E4 — token interaction appears useful

LAW reports Transformer blocks outperform two-layer MLP and linear projection; authors attribute this to interaction across latent feature vectors. This motivates `LAW-D08`, but the ablation does not isolate whether the gain comes specifically from interaction structure versus capacity/optimization differences. Therefore evidence strength is **suggestive, not causal proof of an interaction mechanism**.

## E5 — representation visualization is supportive but weak evidence

The paper visualizes a case where LAW captures scene information missed by VAD and avoids a rear-end trajectory. This is useful qualitative evidence for representation changes, but it cannot establish general causal superiority. Quantitative matched ablations remain the stronger evidence.

---

# WoTE pressure test — dimensions added or split

Source analysis: `papers/deep_analysis/P0045_WOTE_DEEP_ANALYSIS_V2.md`

WoTE confirms that the LAW dimensions are useful but also shows that several are too coarse. The following entries are new discovery axes or required splits.

| ID | New/refined dimension | WoTE position | Why LAW alone could not expose it |
|---|---|---|---|
| WOTE-D01 | **Candidate source** | K-means trajectory anchors from expert logs | LAW has no action-set construction problem. |
| WOTE-D02 | **Candidate count / branching breadth** | 256 default; 64/128/256 ablated | Online evaluator quality depends on how many alternatives exist. |
| WOTE-D03 | **Candidate refinement** | anchor query cross-attends current BEV and predicts residual | Separate fixed motion vocabulary from scene-conditioned candidate adaptation. |
| WOTE-D04 | **Candidate diversity / support coverage** | anchor vocabulary covers multiple driving modes | A perfect evaluator cannot select an absent action. |
| WOTE-D05 | **Train/test candidate distribution** | training uses precomputed labels on anchors; inference evaluates refined trajectories | Evaluator can face action distributions not exactly matching supervision set. |
| WOTE-D06 | **Action-space generalization** | trained with 256 anchors, tested with 1024 unseen anchors; paper reports improvement | Need distinguish memorized vocabulary score from a function generalizing over actions. |
| WOTE-D07 | **Branch persistence through rollout** | each candidate keeps a separate recurrent world branch | Multi-action branching can terminate early, merge, or persist across horizon. |
| WOTE-D08 | **Environment-state vs action-state transition** | WM predicts both future BEV state and updated action embedding | Dynamics may evolve world only, ego only, or coupled state/action. |
| WOTE-D09 | **Transition interval** | intermediate future around 2 s in reported NAVSIM configuration | Total horizon alone hides temporal discretization. |
| WOTE-D10 | **Rollout depth / recurrence count** | recurrent 0→2→4 s outperforms direct 0→4 s | Multi-step imagination creates both richer temporal signal and error-compounding risk. |
| WOTE-D11 | **Intermediate-state consumption** | reward model consumes concatenated current + future states | Some systems use endpoint only; others evaluate full imagined sequence. |
| WOTE-D12 | **Free-running rollout exposure** | predicted state/action fed back recurrently | Teacher-forcing vs free-running affects deployment error accumulation. |
| WOTE-D13 | **Consequence model vs value model separation** | BEV WM predicts consequence; Reward Model values it | Future prediction and decision scoring are independent bottlenecks. |
| WOTE-D14 | **Evaluator input scope** | current BEV + future BEVs + action sequence | Scorer may see only current state, endpoint future, full rollout, or trajectory embeddings. |
| WOTE-D15 | **Value/reward semantics** | imitation + NC/DAC/TTC/comfort/progress | “Good future” is a design choice, not inherent in the world state. |
| WOTE-D16 | **Reward decomposition** | separate imitation and five simulation reward heads | Safety, legality, comfort and progress can conflict and should not be collapsed. |
| WOTE-D17 | **Reward aggregation rule** | hand-weighted nonlinear/log combination | World-model planner includes a utility-composition design beyond dynamics. |
| WOTE-D18 | **State-truth source** | simulator/BEV semantic maps | Split from generic `future-target provenance`. |
| WOTE-D19 | **Value-truth source** | simulator rules + expert imitation | State supervision and value supervision may come from different oracles. |
| WOTE-D20 | **Simulator role** | training-time target/teacher, not deployed simulator | Distinguish external simulator used for labels from learned world model deployed online. |
| WOTE-D21 | **Other-agent response source** | cached/interpolated logged GT tracks in audited NAVSIM/PDM path | Candidate-specific ego simulation does not mean candidate-specific surrounding response. |
| WOTE-D22 | **Supervision reactivity** | non-reactive surrounding-agent target semantics in audited path | Counterfactuality needs explicit reactivity dimension. |
| WOTE-D23 | **Counterfactual evidence level** | multiple candidate branches + ego-specific simulated scores, but no reactive alternative-agent oracle | Binary counterfactual yes/no is inadequate. |
| WOTE-D24 | **World-model vs evaluator attribution** | scorer without future already improves 81.0→83.2; future adds 83.2→85.6 | Planning gain must be decomposed between generator, evaluator and future state. |
| WOTE-D25 | **Utility-signal complementarity** | imitation-only 83.5, simulation-only 83.6, combined 85.6 PDMS | Multiple objectives can contribute differently to planning metrics. |
| WOTE-D26 | **Candidate breadth × rollout depth compute frontier** | 256 parallel branches, recurrent rollout, compact 8×8 BEV state | Online WM design is constrained by product of action breadth, state richness and temporal depth. |
| WOTE-D27 | **Parallelization strategy** | candidate state-action pairs processed in parallel on GPU | Same theoretical planner can differ materially in deployment feasibility. |
| WOTE-D28 | **End-to-end latency accounting** | paper reports ~18.7 ms for 256-trajectory setup on L20 | Need distinguish module latency from complete sensor-to-action system latency. |
| WOTE-D29 | **Semantic-state decoding supervision** | predicted BEV latent decoded to semantic map for focal-loss supervision | A latent may be constrained through an explicit semantic decoder even if reward uses latent features. |
| WOTE-D30 | **Closed-loop claim regime vs training oracle regime** | NAVSIM training supervision non-reactive; Bench2Drive used for reactive closed-loop evaluation | Training-world semantics and evaluation-world semantics are separate dimensions. |

## WoTE forces four major splits of LAW dimensions

### Split A — `action multiplicity` → action-set system

```text
candidate source
candidate count
candidate refinement
candidate diversity/support
train/test action support
branch persistence
```

### Split B — `future target provenance` → three truth sources

```text
world/state truth source
value/reward truth source
other-agent response truth source
```

A system can have rich candidate-specific state/reward labels while still lacking candidate-specific reactive agent behavior.

### Split C — `decision semantics` → consequence / valuation / utility composition

```text
world/consequence predictor
→ evaluator/value model
→ final utility aggregation
```

The three are separately learnable and separately fallible.

### Split D — `deployment imagination cost` → planning compute frontier

```text
candidate breadth
× transition steps
× state size/richness
× dynamics cost
× evaluator cost
```

This will be essential when comparing WoTE, World4Drive and WorldDrive.

---

# Counterfactual ladder — provisional v0

LAW + WoTE show that `counterfactual = yes/no` is unusably coarse. Use this provisional ladder until further anchors challenge it:

```text
CF0  no action-conditioned future
CF1  single action-conditioned factual future prediction
CF2  multiple candidate-conditioned model future outputs
CF3  candidate-specific ego simulation/reward under fixed/logged other-agent futures
CF4  candidate-specific reactive simulator targets where other agents respond to ego intervention
CF5  externally validated behavioral intervention accuracy / real counterfactual evidence
```

Current provisional placement:

```text
LAW                         ≈ CF1
WoTE model outputs          ≈ CF2
WoTE audited NAVSIM targets ≈ CF3
```

Important: a paper can occupy different levels for **model output form**, **training supervision**, and **evaluation evidence**. These must be recorded separately.

---

# Strongest LAW ↔ WoTE contrast discovered so far

| Axis | LAW | WoTE |
|---|---|---|
| primary bottleneck | representation quality | candidate ranking quality |
| future role | training teacher/regularizer | deployed decision variable |
| action branches | one planner output | many candidate trajectories |
| future dynamics | one target latent | recurrent candidate-specific BEV sequence |
| online consequence valuation | absent | explicit Reward Model |
| value truth | not applicable | expert imitation + simulator metrics |
| state truth | one factual future latent | simulator/semantic BEV supervision for ego candidates |
| other-agent alternative response | no | fixed/logged in audited NAVSIM/PDM target path |
| strongest evidence | auxiliary/action-condition matched ablation | scorer ± future matched ablation |
| compute design | no online future consumption | many parallel branches under latency budget |

This comparison supports a larger historical hypothesis to test later:

> The important evolution is not simply `latent → BEV` or `small WM → large WM`; it is the migration of future information from **representation learning** into an explicit **consequence → value → action-selection loop**.

This remains a hypothesis until Epona, WorldDrive and World4Drive are projected under the same axes.

---

# Cross-paper hypotheses to test next — NOT conclusions

1. **Training teacher → online evaluator may be a major historical transition.** LAW and WoTE now support opposite ends; WorldDrive/World4Drive may reveal intermediate/hybrid forms.
2. **Action conditioning is too coarse a label.** Action provenance, branching, injection, support and supervision explain much more.
3. **Future representation quality is not the same as decision value.** WoTE's separate Reward Model makes this explicit; OccWorld/WorldDrive provide counterexamples/controls.
4. **Counterfactuality needs levels and separate output/supervision/evaluation columns.** WoTE proves why.
5. **World-state substrate may matter less than interface semantics, but operational cost constrains substrate choice.** WoTE chooses compact BEV partly because it must branch online.
6. **Deployment cost shapes architecture.** Compare LAW training-only future prediction, WoTE online BEV rollout, World4Drive compact latent foresight and WorldDrive distillation.
7. **Risk/safety may reside in valuation rather than world state.** WoTE explicitly predicts NC/TTC/etc. in reward heads while its world state is BEV. This warns against assuming risk must be encoded as an explicit world-state channel.
8. **Candidate generation may be as important as world prediction.** WorldDrive/World4Drive must be checked for candidate-vocabulary dependence.
9. **Simulator supervision can fill offline counterfactual gaps but imports simulator semantics/bias.** Later papers must be checked for teacher-source assumptions.

---

# Update rules

When reading each next anchor:

1. Fill every existing dimension even if the paper does not discuss it. Use `ABSENT`, `NOT EVALUATED`, `NOT REPORTED`, or `NOT APPLICABLE` rather than leaving silent blanks.
2. If a paper introduces a mechanism not expressible by existing dimensions, add a new provisional dimension with evidence.
3. If one dimension hides multiple scientific questions, split it.
4. If two dimensions always collapse to the same scientific choice across anchors, merge them later.
5. Record **author claim**, **direct evidence**, **our inference**, and **what remains unproven** separately.
6. Never infer novelty from an empty cell. A missing mechanism must be checked against prior art before it becomes a research-gap candidate.
7. Do not freeze stable ontology IDs until at least LAW + WoTE + Epona + WorldDrive + World4Drive have been re-projected under this protocol.
