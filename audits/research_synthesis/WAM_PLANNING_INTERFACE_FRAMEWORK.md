# Provisional WAM Five-Question Review Interface

Status: **PROVISIONAL REVIEW INTERFACE — not a route taxonomy, ontology authority, or method-design license**

Last updated: **2026-09-19**

## Why this file exists

The canonical-12 audit needs one compact cross-paper review surface. This file replaces the old generic five-dimension framework with the five questions that survived the LAW → Epona → DriveLaW → WoTE → World4Drive → WorldDrive pilot and the canonical-12 pressure test.

It is an interface over existing evidence, not a new per-paper projection layer. The evidence chain remains:

```text
papers/raw_md/<paper>/
        → papers/deep_analysis/<paper>_DEEP_ANALYSIS_V2.md
        → audits/literature/<paper-or-phase>_AUDIT.md (when source/version evidence matters)
        → this compact review surface
```

Do not read a row below as a final route label. Read it together with the linked deep analysis, the source/code boundary, and the paper's core bridge.

## Fixed questions

| Question | Record only | Do not silently infer |
|---|---|---|
| **Q1. Where is future-related computation?** | Module, branch, interface, or process location. | Whether it survives deployment. |
| **Q2. What is the future object/target/intermediate representation?** | Prediction target, future-generation process, or intermediate representation. | A physical future state when the paper only exposes a latent/process target. |
| **Q3. Does the future-related signal enter the forward action chain?** | Whether action generation or candidate selection consumes it. | Deployment use merely because a training branch exists. |
| **Q4. What role does the future mechanism play?** | Training shaping, online single-path conditioning, candidate consequence evaluation/selection, world–planner refinement, or another evidence-backed role. | That all online use is candidate evaluation. |
| **Q5. What remains at deployment?** | Retained, bypassed, or removed modules/modes and future computation. | One paper having one answer when modes or paper/release artifacts differ. |

Every answer must preserve `PAPER FACT`, `CODE FACT`, `OUR INFERENCE`, `UNKNOWN`, `NOT REPORTED`, and `EVIDENCE BOUNDARY` when applicable. In particular, a generated response is not paired real intervention truth, and a future latent is not automatically a world state.

## Canonical-12 compact projection

The table is deliberately compressed. The full mechanism, bridge, provenance, and uncertainty remain in each deep analysis.

| ID / paper | Q1–Q2: location → future object | Q3–Q5: action-chain use → role → deployment remainder |
|---|---|---|
| **P0048 LAW** | Training action-conditioned future-latent branch → waypoint-conditioned future visual latent. | **No** → training-only action-aware representation shaping → waypoint/trajectory path remains; future output is not consumed. |
| **P0001 Epona** | Shared spatiotemporal representation with TrajDiT/VisDiT branches → future ego trajectory and next-frame visual latent/frame. | No evidence that visual rollout feeds planning → joint training plus mode-specific single-path generation → planning can bypass VisDiT; rollout mode retains it. |
| **P0009 DriveLaW** | Video-DiT denoising and video-to-action hidden-state interface → intermediate video hidden representation. | **Yes, single path** → hidden-state conditioning of Action-DiT, not candidate feedback → partial Video-DiT hidden computation plus Action-DiT; full RGB generation is not required. |
| **P0045 WoTE** | Candidate-conditioned recurrent BEV rollout between candidate action and reward model → multi-step candidate BEV states/actions. | **Yes, candidate selection** → online candidate consequence scoring → candidate generator/refiner, recurrent rollout, reward model, resolver. Surrounding-agent future is not established as reactive in the audited path. |
| **P0046 World4Drive** | Candidate future-query/world-model branch and ScoreNet → fixed-time candidate future latent. | **Yes, candidate selection** → factual-future consistency/mode matching → candidate generator, predictor, ScoreNet, resolver; factual future target is unavailable. |
| **P0042 WorldDrive** | Training TA-DWM teacher and deployment FAR surrogate → teacher future latent/scene representation, then candidate-conditioned surrogate. | **Yes, candidate selection** → teacher-to-surrogate distillation and future-aware reward → planner/FAR/surrogate/reward/resolver remain; heavy teacher is off. |
| **P0061 SeerDrive** | Paper: BEV world model ↔ future-aware planner; release: WoTE-like reward path → paper future BEV/future ego feature; release reward-related representation. | Paper: yes, iterative feedback; release: yes, evaluator path → paper world–planner co-refinement; release variant is not the paper loop → preserve artifact/version split; do not conflate them. |
| **P0049 Drive-JEPA** | Masked video-latent pretraining branch → masked spatiotemporal latent target, not confirmed chronological physical future. | **No** → predictive representation pretraining plus simulator-distilled proposal utility → encoder/proposal scorer remains; JEPA predictor is off-line. |
| **P0012 DA-WAM** | Training future-video expert ↔ action expert token interface → action-conditioned future-video latent tokens (logged factual future). | **No direct future read at inference** → asymmetric world-loss-shaped action policy; gradients, not future evaluation, couple them → action expert/denoising remains; future-video path is bypassed. |
| **P0063 DynFlowDrive** | Training candidate-conditioned flow world model and stability criterion → latent endpoint/flow path for a factual next-step target; flow time is not physical time. | **No at deployment** → world-derived candidate-label/selector teacher → candidates + learned score head + argmax remain; world model/future latent are off. |
| **P0064 Discrete-WAM** | Shared Transformer world/world-policy token editing and separate decision/action editing → future visual tokens, future action tokens, decision tokens. | Mandatory planning path does not require future visual generation/scorer → multi-task pretraining plus hierarchical action-token editing → decision/action editing and decoding remain; future visual mode is optional. |
| **P0065 GraphWorld** | ECIG/GRU interaction encoder and flow-refined world-state branch → current structured `W_cur`, future-oriented `W_tgt`, refined latent. | **Yes, state-conditioned planning** → online structured world-state modulation, not candidate-specific resolver → ECIG/history/map state, short refinement, residual/importance modulation, planning heads. |

## What the projection does and does not separate

It reliably separates:

1. training-only future supervision from deployment-time consumption;
2. single-path conditioning, structured-state modulation, candidate selection, and iterative world–planner feedback;
3. factual logged targets, simulator/teacher-derived signals, and unresolved intervention truth;
4. paper/release or mode-dependent deployment boundaries.

It does **not** by itself supply a final technical route. In particular:

```text
World4Drive / WorldDrive / WoTE
  share a candidate → future representation → score/select terminal shape,
  but not the same future semantics or supervision.

LAW / DA-WAM / DynFlowDrive
  can all look training-only at Q3,
  but their indispensable training bridges are different.

DriveLaW / GraphWorld / SeerDrive
  all expose online future-related computation,
  but hidden conditioning, structured-state modulation,
  and world–planner refinement are not interchangeable.
```

The deletion test therefore remains local to each deep analysis: remove the claimed bridge and ask whether the paper is still the same method. A row may be revised only when the underlying raw text or pinned source audit changes.


## Branch-audit guardrails retained without restoring a route layer

A read-only audit of every non-`main` branch found one completed, reusable result: the canonical-12 reconstruction branch separated artifact scope, deployment lifecycle, candidate identity, and evidence boundaries. Its proposed route compression is **not** copied here: that branch labels itself `RECONSTRUCTED-BUT-NOT-NORMATIVE`, and its human-acceptance and held-out tests were still pending. The following guardrails are retained because they prevent the Q1–Q5 interface from collapsing distinct mechanisms:

- **Scope the artifact before comparing it.** Use paper/code version × task mode × planning or generation path. Split when the deployment graph changes (for example, SeerDrive paper versus release, Epona planning versus rollout, or Drive-JEPA PF versus PB); do not force one paper to have one answer.
- **Require candidate identity and a common resolver.** Multiple samples, diffusion steps, or proposal refinements are not a candidate route by themselves. Call it candidate selection only when candidate identity survives to a shared resolver and one output is committed.
- **Separate lifecycle and clocks.** A future branch used only for training is not an online world carrier. Internal denoising, flow transport, or within-decision refinement is not physical-time rollout unless the source establishes that relation.
- **Do not equate the common terminal shape.** World4Drive, WorldDrive, and WoTE can all look like candidate → future representation → score/select, while their future construction, supervision, lifecycle, and deployment role differ.
- **Keep evidence boundaries visible.** Never replace a paper graph with a release graph, and never turn an unresolved deployment or counterfactual claim into verified absence. Preserve `PAPER FACT`, `CODE FACT`, `OUR INFERENCE`, and `UNKNOWN` at the deep-analysis layer.

These are audit controls, not additional questions or a second route/ontology layer. The five-question table remains the only compact cross-paper surface; the raw/deep/source chain remains the dispute resolver.

## External-survey pressure-test boundary

The five questions were not invented from the old driving-only matrices. A separate exploratory audit consulted broad world-model/control lineages (including Dyna, predictive-state/value-prediction methods, latent planning, Dreamer/MuZero and TD-MPC families) and recent world-model surveys. Its useful methodological result is retained here without importing another corpus layer:

```text
artifact/mode/deployment route must be separated;
ontology-free mechanism reconstruction precedes labels;
training-world use must be separated from deployment-world use;
holdout/collision tests are required before promoting a new axis or route.
```

That pass is a pressure test, not a complete primary-source review and not an authorization to add `interaction`, `uncertainty`, a route family, or a research problem. The current interface keeps only the evidence-discipline consequences; the raw/deep/source chain remains authoritative.

## Reading order

```text
state/CURRENT_STATE.md
→ state/NEXT_TASK.md
→ this interface for the five-question cross-paper scan
→ the relevant raw Markdown
→ the relevant deep analysis and source/code audit
```

Five-question status: **PASS-WITH-BOUNDARY**. It is a review interface and a useful embryo for later route reconstruction; it is not the route itself.
