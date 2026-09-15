# WAM Dimension Discovery Log

Last updated: 2026-09-15

Status: **ACTIVE — dimensions are provisional; ontology is deliberately NOT frozen**

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
P0045 WoTE         NEXT
P0001 Epona        PENDING dimension-first rebuild
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

# Cross-paper hypotheses to test next — NOT conclusions

These are questions generated by LAW and must be challenged by WoTE/Epona/WorldDrive/World4Drive.

1. **Training teacher → online evaluator may be a major historical transition.** Test whether online future consumption adds value beyond a strong scorer.
2. **Action conditioning is too coarse a label.** Test whether action provenance, branching, injection and alternative-world supervision explain meaningful method differences.
3. **Future representation quality is not the same as decision value.** Test using OccWorld/WorldDrive/WoTE evidence.
4. **Counterfactuality needs levels rather than yes/no.** Test candidate-specific output, candidate-specific supervision, reactive-agent response and intervention validity separately.
5. **World-state substrate may matter less than interface semantics.** Compare BEV/video/latent systems that nevertheless serve the same evaluator or representation-teacher role.
6. **Deployment cost shapes architecture.** Compare LAW training-only future prediction, WoTE online BEV rollout, World4Drive compact latent online foresight and WorldDrive distillation.
7. **Uncertainty/risk are not explicit in LAW.** Do not call this a research gap until other anchors are analyzed under the same dimension.

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
