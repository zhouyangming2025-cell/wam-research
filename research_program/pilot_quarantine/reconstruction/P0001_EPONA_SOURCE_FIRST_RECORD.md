# P0001 Epona — Source-First Record

Status: `SOURCE-FIRST-DRAFT`

Primary source: `papers/raw_md/P0001_Epona/P0001_Epona.raw.md`

Pinned source audit: `audits/literature/PHASE_C5_EPONA_SOURCE_AUDIT.md`

Historical route labels are intentionally absent.

## A. Author problem / gap ledger

| ID | Author-stated problem or gap | Evidence location | Status |
|---|---|---|---|
| EPONA-P1 | Existing video-diffusion world models are described as modeling fixed-length global joint distributions rather than per-timestep local distributions. | Abstract; Introduction; Sec. 3.2 | `AUTHOR CLAIM` |
| EPONA-P2 | The authors associate that formulation with weak variable-length and long-horizon prediction and infeasible trajectory planning. | Introduction | `AUTHOR CLAIM` |
| EPONA-P3 | GPT-style driving world models are described as suffering visual-quality and planning-precision degradation from quantization/tokenization. | Introduction; Related Works | `AUTHOR CLAIM` |
| EPONA-P4 | Autoregressive token models are described as limited to next-action prediction rather than long-horizon trajectory planning. | Introduction | `AUTHOR CLAIM` |
| EPONA-P5 | Prior methods are described as lacking planning modules, being low-resolution/short-horizon, or being too computationally demanding for practical use. | Related Works | `AUTHOR CLAIM` |
| EPONA-P6 | Autoregressive generation suffers teacher-forcing/inference mismatch and error accumulation. | Introduction; Long Video Generation | `AUTHOR CLAIM` |
| EPONA-G1 | The proposed gap is a continuous-representation system combining causal temporal modeling, long-horizon video generation, and trajectory planning. | Abstract; Introduction; Conclusion | `AUTHOR CLAIM` |

These entries preserve the authors' framing and do not validate the claims against the rest of the field.

## B. Neutral mechanism record

### B1. Material modes

The paper describes distinct uses that must not be collapsed:

1. Planning mode: historical context is processed by MST/STT and TrajDiT produces a future trajectory; the source audit reports that the visual branch can be skipped.
2. World-rollout mode: the visual branch predicts the next visual latent/frame conditioned on an action, and the result can be fed into the next autoregressive step.
3. Trajectory-controlled video mode: an externally supplied trajectory can control visual generation.

These modes have different terminal outputs and deployment roles.

### B2. Input and shared representation

- Input: historical visual observations and ego-motion/action history.
- MST/STT encodes the historical visual latents and actions into a compact temporal representation.
- The shared representation feeds a trajectory branch and a visual next-frame branch.

Evidence: `PAPER FACT`, Sections 3.2–3.3; the exact source-level interface is `CODE FACT` in the pinned audit.

### B3. Future objects

- Trajectory branch: TrajDiT predicts a future multi-step ego trajectory using a rectified-flow objective.
- Visual branch: VisDiT predicts the next-frame visual latent conditioned on the historical representation and either a predicted or externally provided action; the latent is decoded to an image.
- Autoregressive rollout repeats next-frame prediction to produce long videos.

Evidence: `PAPER FACT`.

### B4. Action entry

Historical actions enter the shared temporal representation. In world-rollout mode, the next-frame visual branch is additionally conditioned on the predicted or externally supplied action. This is action-conditioned generation, not evidence by itself of a counterfactual environment model.

Evidence: `PAPER FACT`; causal limitation is `OUR INFERENCE`.

### B5. Deployment output and planner input

In planning-only mode, the trajectory branch consumes the shared historical representation and produces the trajectory. The pinned source audit states that VisDiT/FluxDiT is skipped for planning-only execution. Therefore the planning path does not require a visual future to be generated and then scored against the trajectory.

Evidence: `CODE FACT`.

### B6. Candidate and resolver status

- Explicit candidate bank with per-candidate future rollout: `NOT REPORTED`.
- Candidate-specific consequence score: `NOT REPORTED`.
- Separate argmax/scorer: `NOT REPORTED`.
- Trajectory output: direct generative trajectory branch.

### B7. Training/deployment lifecycle

The paper reports joint training of the world model and trajectory/video branches, including chain-of-forward training to expose autoregressive prediction errors. The deployment role differs by mode: planning can omit the visual branch, while world rollout retains it.

Evidence: `PAPER FACT` and pinned `CODE FACT`.

## C. Evidence boundaries

- Epona provides paper-level evidence for a shared historical representation feeding separate trajectory and visual-generation branches.
- Source evidence supports the planning-only bypass of the visual branch.
- Long-horizon visual rollout is not the same as online evaluation of alternative planning candidates.
- Reported planning performance does not establish that the video branch is necessary during planning inference.

## D. Unresolved

- The exact gradient and parameter-sharing contribution between the trajectory and visual branches under every training configuration.
- Whether any unreported deployment configuration keeps the visual branch active for planning.
- Whether generated visual rollouts are intended as physical counterfactuals or primarily as controlled visual generation; the paper does not establish this to the required standard.

## E. Five-question pilot projection

Status: `VALIDATION-DRAFT`

Epona requires mode-aware answers because planning-only execution and visual world-rollout execution have different terminal artifacts.

| Question | Answer | Evidence status |
|---|---|---|
| Q1. Where does future-related computation happen? | In the shared historical MST/STT representation and the corresponding TrajDiT/VisDiT computation branches. This answer identifies the computational locations; deployment mode is recorded separately in Q5. | `PAPER FACT + CODE FACT` |
| Q2. What future object, target, or intermediate representation is involved? | Two future objects must remain visible: a multi-step ego trajectory from TrajDiT, and a next-frame visual latent/frame that can be autoregressively rolled out by VisDiT. | `PAPER FACT` |
| Q3. Does the future-related signal enter the forward action chain? | No evidence shows that generated visual futures are fed back to generate, score, or select the planning trajectory. Historical actions and the shared history representation enter TrajDiT; the generated visual future is used in the world-rollout mode. | `PAPER FACT + CODE FACT` |
| Q4. What is the future mechanism's lifecycle/decision role? | Joint training of trajectory and visual branches; online single-path trajectory generation in planning mode; independently runnable action-conditioned visual rollout in world-generation mode. Candidate-consequence evaluation is not reported. | `PAPER FACT + CODE FACT` |
| Q5. What remains at deployment? | Mode-dependent: planning deployment can skip VisDiT/visual rollout and retain the shared representation plus TrajDiT; world-rollout deployment retains the visual predictor and autoregressive feedback. | `CODE FACT` |

Parallel annotations: visual future supervision/rollout is action-conditioned, but its causal or counterfactual status is unresolved. There is no evidence of a per-candidate future resolver in the audited modes. The primary task differs by mode: trajectory planning versus controllable long-horizon visual generation.
