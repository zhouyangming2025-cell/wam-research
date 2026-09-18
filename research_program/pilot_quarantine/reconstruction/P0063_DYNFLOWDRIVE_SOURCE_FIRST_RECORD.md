# P0063 DynFlowDrive — Source-First Record

Status: `READY-FOR-REVIEW`

Primary source: `papers/raw_md/P0063_DynFlowDrive/P0063_DynFlowDrive.raw.md`

Pinned source audit: `audits/literature/PHASE_C5_DYNFLOWDRIVE_AUDIT.md`

Official repository state in the audit: `xiaolul2/DynFlowDrive@c665dc577a0939543fa7abe64d28eadaec28283c`; runnable implementation was unavailable at audit time.

Historical route labels are intentionally absent.

## A. Author problem / gap ledger

| ID | Author-stated problem or gap | Evidence location | Status |
|---|---|---|---|
| DF-P1 | Pixel/appearance generation is computationally expensive and may emphasize visual details rather than action-relevant geometry and dynamics. | Abstract; Introduction | `AUTHOR CLAIM` |
| DF-P2 | One-step latent regression is described as a static mapping that neglects the transition process and trajectory-dependent evolution. | Introduction; Sec. 2 | `AUTHOR CLAIM` |
| DF-G1 | The proposed gap is continuous trajectory-conditioned latent dynamics plus a stability-aware multi-mode selection criterion. | Abstract; Introduction; Contributions | `AUTHOR CLAIM` |

## B. Neutral mechanism record

### B1. Candidate planner and training world model

The planner first produces multiple trajectory proposals and their ordinary mode scores. For each candidate, a rectified-flow latent world model conditions a velocity field on the current world latent and that candidate trajectory, then integrates over an internal flow coordinate to obtain a future latent and flow velocities.

The target future latent is a single factual next-timestep latent extracted from the observed next frame. Candidate-specific outputs therefore exist, but candidate-specific observed alternative-action future ground truth does not.

### B2. Stability criterion and deployment

During training, each candidate receives a criterion combining trajectory error, latent reconstruction discrepancy, and angular consistency of successive flow velocities. The selected best mode supervises the score head.

At inference, the world model, latent integration, and flow-stability computation are removed. The planner directly outputs candidate trajectories and learned scores, then selects the highest-scoring candidate.

The flow coordinate is an internal transport variable, not established as physical future time.

## C. Five-question pilot projection

Status: `READY-FOR-REVIEW`

| Question | Provisional answer | Evidence status |
|---|---|---|
| Q1. Where does future-related computation occur? | In the candidate-conditioned rectified-flow latent world-model branch and stability criterion used during training, between trajectory proposals and score-head supervision. | `PAPER FACT` |
| Q2. What is the future object, target, or intermediate representation? | A candidate-conditioned latent endpoint/transport path toward a factual next-step world latent; intermediate flow states are indexed by internal flow time, not proven physical future timestamps. | `PAPER FACT` + `EVIDENCE BOUNDARY` |
| Q3. Does the future-related signal enter the forward action chain? | **Not at deployment.** The world-derived candidate criterion shapes score-head supervision during training; deployment uses the learned score head without computing the future latent or flow stability. | `PAPER FACT` |
| Q4. What role does the future mechanism play? | Training-only world-derived candidate-label/selector supervision, including flow-dynamics and stability losses; it is not an online candidate-consequence evaluator. | `PAPER FACT` + `OUR INFERENCE` |
| Q5. What remains at deployment? | Candidate trajectory generation, the learned score head, and highest-score resolution remain. The rectified-flow world model and future-latent computation are removed. | `PAPER FACT` |

Parallel provenance annotation: candidates are separately conditioned during training, but one factual next-step target supervises them; physical counterfactual validity is not established.

## D. Evidence boundaries and unresolved items

- The full selection bundle improves the reported planning metrics, but the incremental flow-stability contribution is small in the reported ablation.
- Paper equations/procedure contain unresolved flow-target and sampling ambiguities; no code was available to settle them.
- “No additional inference overhead” means no online world-model depth, not zero cost for the whole planner/scorer.
