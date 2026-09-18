# P0049 Drive-JEPA — Source-First Record

Status: `READY-FOR-REVIEW`

Primary source: `papers/raw_md/P0049_DriveJEPA/P0049_DriveJEPA.raw.md`

Pinned source audit: `audits/literature/PHASE_C5_DRIVEJEPA_AUDIT.md`

Audited official repository commit: `linhanwang/Drive-JEPA@e21f47410b4d26b61f05f9bd23e169c0390cae2a`

Historical route labels are intentionally absent.

## A. Author problem / gap ledger

| ID | Author-stated problem or gap | Evidence location | Status |
|---|---|---|---|
| DJ-P1 | Pixel-level video pretraining is computationally expensive and may over-emphasize visual details unrelated to planning; prior latent approaches are presented as difficult to scale or vulnerable to representation collapse. | Abstract; Introduction; Sec. 2.2 | `AUTHOR CLAIM` |
| DJ-P2 | Each driving scene usually supplies one human trajectory although driving is multimodal, limiting behavior diversity under direct supervision. | Introduction; Sec. 2.3 | `AUTHOR CLAIM` |
| DJ-P3 | Fixed trajectory vocabularies have limited coverage, diffusion planners are costly, and proposal methods remain tied to one human trajectory per scene. | Introduction; Sec. 2.3 | `AUTHOR CLAIM` |
| DJ-G1 | The paper proposes scalable predictive video representation pretraining plus simulator-distilled multimodal proposal supervision. | Abstract; Introduction; Contributions | `AUTHOR CLAIM` |

These entries preserve the authors' framing and do not validate the claims as field-wide facts.

## B. Neutral mechanism record

### B1. Predictive pretraining

V-JEPA predicts latent representations at randomly masked spatiotemporal positions:

```text
masked video view
→ online encoder + predictor
→ masked-position latent prediction
full target view
→ EMA target encoder / stop-gradient target latent
```

The audited objective is action-agnostic random masked completion. It is not evidence of a history-only-to-future causal transition model.

### B2. Deployment paths

Two planner settings must remain visible:

1. Perception-free: the pretrained encoder supplies features to a direct waypoint decoder.
2. Perception-based: multiple waypoint proposals are iteratively refined with WADA, then a learned scorer and momentum/comfort calibration select one proposal.

The JEPA predictor, EMA target encoder, masked-target loss, and world rollout are absent from downstream inference. WADA's waypoint-anchored BEV sampling is planner-side proposal refinement, not future-world prediction.

### B3. Proposal supervision and resolver

The perception-based path uses multiple online proposals. Simulator/rule-based NAVSIM scoring supplies pseudo-teacher trajectories and scorer labels. The scorer predicts driving-quality/utility scores and the final proposal is selected by argmax. These proposal scores are not factual-future likelihoods and are not produced by an online predicted future world state.

## C. Five-question pilot projection

Status: `READY-FOR-REVIEW`

| Question | Provisional answer | Evidence status |
|---|---|---|
| Q1. Where does future-related computation occur? | In the V-JEPA masked video-latent pretraining branch, before the planning encoder is transferred. The deployment planner instead uses the transferred encoder plus a proposal/refinement/scoring path. | `PAPER FACT` + `CODE FACT` |
| Q2. What is the future object, target, or intermediate representation? | A latent video representation at randomly masked spatiotemporal positions, produced from a target-view EMA encoder. It is not established as an explicit chronological physical future state. | `PAPER FACT` + `CODE FACT` + `EVIDENCE BOUNDARY` |
| Q3. Does the future-related signal enter the forward action chain? | **No for the JEPA future predictor.** The predictor is discarded before planning inference. The online scorer uses simulator/rule utility labels and proposal features, not a predicted future latent. | `PAPER FACT` + `CODE FACT` |
| Q4. What role does the future mechanism play? | Training-time predictive representation pretraining. Separately, simulator-distilled multimodal proposal supervision and online utility scoring support candidate selection; those are not the same as future prediction. | `PAPER FACT` + `CODE FACT` |
| Q5. What remains at deployment? | The transferred encoder, direct/proposal planner, WADA refinement in the perception-based path, scorer, and version-dependent momentum-aware selection remain. The JEPA predictor and target branch do not. | `CODE FACT` + `EVIDENCE BOUNDARY` |

Parallel provenance annotation: multiple proposals and simulator-derived utility labels are supported; online proposal-specific predicted world states and observed alternative-action futures are not established.

## D. Evidence boundaries and unresolved items

- V-JEPA representation transfer and proposal scoring must not be merged into one “future-aware planner” mechanism.
- Simulator-generated pseudo teachers are not multiple observed human futures or verified reactive counterfactual futures.
- NAVSIM-v1 and NAVSIM-v2 public planner paths differ in momentum calibration; the version must be named.
- The relative contribution of masked prediction, driving-video scale, proposal distillation, and scorer design is not fully isolated.
