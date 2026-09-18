# P0048 LAW — Source-First Record

Status: `SOURCE-FIRST-DRAFT`

Primary source: `papers/raw_md/P0048_LAW/P0048_LAW.raw.md`

Pinned source audit: `audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md`

Historical route labels are intentionally absent.

## A. Author problem / gap ledger

| ID | Author-stated problem or gap | Evidence location | Status |
|---|---|---|---|
| LAW-P1 | End-to-end planners use raw sensor data, but the paper frames better scene-feature representation as an open problem. | Abstract; Introduction | `AUTHOR CLAIM` |
| LAW-P2 | Conventional self-supervision often focuses on static images, while driving depends on continuous video and temporal information. | Introduction | `AUTHOR CLAIM` |
| LAW-P3 | Existing future-prediction tasks may overlook the effect of ego actions on the future. | Introduction | `AUTHOR CLAIM` |
| LAW-P4 | Image-based driving world models relying on diffusion may take seconds to generate future images, which the authors present as inefficient for scene-feature enhancement. | Introduction; Related Works | `AUTHOR CLAIM` |
| LAW-P5 | Perception-free end-to-end methods are described as having inadequate scene representation, while perception-based methods commonly use perception annotations. | Related Works | `AUTHOR CLAIM` |
| LAW-G1 | The proposed gap is an action-aware, latent future-feature prediction task that can shape scene representation and trajectory prediction without manual future-scene annotations. | Introduction; Contributions | `AUTHOR CLAIM` |

These are records of what LAW criticizes or claims to address. They are not yet accepted as objective field gaps.

## B. Neutral mechanism record

### B1. Scope and mode boundary

The paper presents two implementation settings: a perception-free framework using perspective-view latents and a perception-based framework using BEV latents. The shared future-latent task is the mechanism under comparison; these settings are not treated as separate routes.

### B2. Input and encoder output

- Current input: multi-view images at time `t`; the appendix also studies multiple history frames.
- Visual encoder output: a set of current visual latent vectors `V_t`.
- A waypoint decoder uses `V_t` to predict the ego waypoint sequence `W_t`.

Evidence: `PAPER FACT`, Sections 3–4 of the raw paper.

### B3. Future object and construction

The paper constructs an action-aware latent `A_t` by concatenating the current visual latent with the flattened predicted waypoint sequence, then predicts future visual latents `V_hat_{t+1}` with a transformer latent world model. The target `V_{t+1}` is extracted from the future frame and used in an MSE latent-prediction loss.

Evidence: `PAPER FACT`, Section 4.1.

### B4. Action entry

The predicted waypoint sequence enters before future-latent prediction through the action-aware latent construction. This establishes action-conditioned prediction in the training graph; it does not by itself establish causal or counterfactual validity.

Evidence: `PAPER FACT` plus `OUR INFERENCE` for the causal limitation.

### B5. Deployment output and planner input

The pinned code audit reports that the waypoint/trajectory output is computed before the future-latent output, and that the future-latent output is discarded in `simple_test_pts`. No audited inference path feeds the predicted future latent into waypoint selection or a candidate scorer.

Evidence: `CODE FACT`, pinned audit; the absence of a scorer is a code-path observation.

### B6. Candidate and resolver status

- Explicit candidate bank: `NOT REPORTED`.
- Candidate-specific future consequence evaluation: `NOT REPORTED`.
- Separate resolver/scorer: `NOT REPORTED`.
- Final planning output: direct waypoint/trajectory prediction.

### B7. Training/deployment lifecycle

The future-latent branch is supervised during training. The pinned code audit records a detached future target and a reconstruction/prediction loss; at test time the future-latent return is not consumed by the planner.

Evidence: `CODE FACT`. The exact contribution of every shared parameter to the trajectory branch is not independently re-derived here and remains an evidence detail for later review.

## C. Evidence boundaries

- The paper supports future latent prediction and reported planning gains.
- The code audit supports the training-only use of the returned future latent in the audited inference path.
- The paper and audit do not establish that LAW evaluates alternative actions through alternative future consequences.
- Closed-loop CARLA performance is an evaluation result, not proof that the latent branch is an online candidate evaluator.

## D. Unresolved

- Whether any un-audited configuration uses the predicted future latent differently.
- How much of the reported planning gain comes from the future-latent objective versus other joint losses and architecture changes.
- Whether the latent target preserves decision-relevant semantics in a way that generalizes beyond the reported benchmarks.

## E. Five-question pilot projection

Status: `VALIDATION-DRAFT`

This is a projection of the frozen five-question audit frame onto the source-first record. It is not a route label or an ontology update.

| Question | Answer | Evidence status |
|---|---|---|
| Q1. Where does future-related computation happen? | In the action-conditioned future-latent prediction branch attached to the planner during training: the predicted waypoint sequence conditions future visual-latent prediction. This answer identifies the computation location; it does not claim a complete world model or deployment retention. | `PAPER FACT + CODE FACT` |
| Q2. What future object, target, or intermediate representation is involved? | A future visual latent extracted from a future frame, predicted from the current visual latent plus the predicted ego waypoint sequence. | `PAPER FACT` |
| Q3. Does the future-related signal enter the forward action chain? | **No in the audited deployment path.** The training graph contains waypoint-conditioned future-latent prediction, but the predicted future latent is not shown feeding deployment-time waypoint selection or a candidate resolver. | `PAPER FACT + CODE FACT` |
| Q4. What is the future mechanism's lifecycle/decision role? | Training-only action-aware representation shaping / auxiliary future prediction. Candidate-conditioned consequence evaluation is not reported. | `PAPER FACT + CODE FACT + OUR INFERENCE` |
| Q5. What remains at deployment? | The direct waypoint/trajectory path remains; the future-latent output is discarded or not consumed by the audited test path. | `CODE FACT` |

Parallel annotations: the target future is a factual/logged future-frame latent; no candidate-specific future or counterfactual resolver is established. The primary task is planning/representation improvement, while the reported planning gain is not causally isolated to this branch.
