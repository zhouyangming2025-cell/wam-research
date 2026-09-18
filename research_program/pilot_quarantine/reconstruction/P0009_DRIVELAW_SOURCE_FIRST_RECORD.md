# P0009 DriveLaW — Source-First Record

Status: `SOURCE-FIRST-DRAFT`

Primary source: `papers/raw_md/P0009_DriveLaW/P0009_DriveLaW.raw.md`

Pinned source audit: `audits/literature/PHASE_C6_DRIVELAW_AUDIT.md`

Paper/code version differences are kept visible. Historical route labels are intentionally absent.

## A. Author problem / gap ledger

| ID | Author-stated problem or gap | Evidence location | Status |
|---|---|---|---|
| DLW-P1 | Existing world-model contributions to planning are described as indirect, auxiliary, or parallel rather than tightly coupled to decision making. | Introduction | `AUTHOR CLAIM` |
| DLW-P2 | Simulator/data-generation world models are described as not transmitting their physical understanding directly into the planner's state. | Introduction; Related Works | `AUTHOR CLAIM` |
| DLW-P3 | Future visual/affordance supervision is described as improving foresight while leaving planning externally specified. | Introduction | `AUTHOR CLAIM` |
| DLW-P4 | Unified generation/planning methods are described as keeping video and trajectory output streams independent, creating a representation disconnect. | Introduction; Related Works | `AUTHOR CLAIM` |
| DLW-P5 | The authors specifically identify a gap in using a video generator's internal latent features as the planning state. | Introduction; Sec. 2.1 | `AUTHOR CLAIM` |
| DLW-P6 | High-fidelity video synthesis and real-time stable planning are described as being in tension. | Introduction | `AUTHOR CLAIM` |
| DLW-G1 | The proposed gap is to chain a video generator's latent denoising representation into an action planner instead of treating video and planning as parallel outputs. | Abstract; Introduction; Sec. 3.2 | `AUTHOR CLAIM` |

These are author-stated motivations, not independent conclusions about the field.

## B. Neutral mechanism record

### B1. Material modes

At minimum, two terminal roles must remain visible:

1. Video-generation mode: the video model completes the denoising/decoding path to generate future video.
2. Planning mode: the action planner consumes selected internal Video-DiT features and outputs a trajectory; full future-video generation is not required on the audited canonical path.

The paper's general formulation and the pinned code path are recorded separately because the exact denoising step used by the planner is version/configuration sensitive.

### B2. Input and encoder/generator output

- Historical driving frames, ego/action context, and planning conditions enter the video model.
- A spatiotemporal VAE and Video-DiT form the video-generation representation.
- The paper defines a mid-denoising feature `h_t` and selects one or a small set of timesteps as the perception/planning latent.

Evidence: `PAPER FACT`, Sec. 3.1–3.2.

### B3. Future object and construction

The planning path does not need to materialize a complete future RGB video. It uses an internal hidden representation from the video denoising process as a conditioning carrier for the Action-DiT.

The pinned source audit specifies the canonical audited path more narrowly: historical frames enter a VAE-conditioned latent/noise canvas, the first Video-DiT denoising iteration is run, hidden states are cached, and Action-DiT blocks cross-attend those hidden states. Full video denoising and RGB decoding are off in that path.

Evidence: paper-level statement is `PAPER FACT`; exact canonical implementation is `CODE FACT`.

### B4. Action entry

The Action-DiT receives the video-generator hidden representation and generates/refines the ego trajectory through a flow/diffusion planning process. The audited canonical path does not show an action-conditioned candidate being fed back through a future predictor for per-candidate consequence scoring.

Evidence: `CODE FACT` for the audited path; the absence of candidate scoring is an audited-path observation.

### B5. Deployment output and planner input

Planner output is the future ego trajectory. The planner reads selected internal Video-DiT hidden states rather than a decoded future RGB sequence.

Evidence: `PAPER FACT` plus pinned `CODE FACT`.

### B6. Candidate and resolver status

- Explicit candidate bank: `NOT REPORTED` in the audited canonical path.
- Candidate-specific future consequence evaluator: `NOT REPORTED`.
- Separate scorer or argmax resolver: `NOT REPORTED`; the paper emphasizes direct trajectory generation without auxiliary scorers.
- Final output: direct action/trajectory generation.

### B7. Training/deployment lifecycle

The paper reports a three-stage progressive training strategy that first develops the video/action components and then chains video latents into the planner. The deployment path retains the selected internal video features but does not require the full visual-generation rollout.

Evidence: `PAPER FACT` and pinned `CODE FACT`.

## C. Evidence boundaries

- The paper supports the claim that video-generator internal features are used to condition the action planner.
- The code audit supports the stronger lifecycle statement that the canonical planning path uses early hidden states and does not decode a complete future RGB sequence.
- Planning gains do not prove that video-generation fidelity itself is the causal source of the gain.
- An internal denoising state is not automatically a physical future state or a calibrated counterfactual consequence.

## D. Unresolved

- Whether all released configurations use the same early denoising step as the audited canonical path.
- How the paper's selected `t*` feature maps onto the exact source/configuration path.
- Whether the planner's diffusion/flow sampling produces multiple meaningful candidates or only iterative refinement of one output; no separate resolver is established.
- The relative contribution of video pretraining, hidden-state conditioning, and the progressive training schedule.

## E. Five-question pilot projection

Status: `VALIDATION-DRAFT`

This projection keeps the paper-level formulation and the audited canonical code path separate where their exact denoising-step correspondence is unresolved.

| Question | Answer | Evidence status |
|---|---|---|
| Q1. Where does future-related computation happen? | In the Video-DiT denoising computation and its video-to-action hidden-state interface. A selected intermediate hidden state is exposed to Action-DiT; complete video decoding is not required on the audited planning path. | `PAPER FACT + CODE FACT` |
| Q2. What future object, target, or intermediate representation is involved? | The planner consumes an internal video-generation hidden representation at a selected denoising stage. It is not a decoded future RGB sequence or an explicit future BEV rollout, and is not established as an explicit future-time state/endpoint target. | `PAPER FACT + CODE FACT` |
| Q3. Does the future-related signal enter the forward action chain? | **Yes.** The Video-DiT hidden signal directly conditions Action-DiT trajectory generation. No candidate-specific future feedback or candidate scorer is established. | `PAPER FACT + CODE FACT` |
| Q4. What is the future mechanism's lifecycle/decision role? | Online single-path conditioning/action decoding, supported by a staged training program that connects video and action components. It is not confirmed as online candidate-consequence evaluation. | `PAPER FACT + CODE FACT + OUR INFERENCE` |
| Q5. What remains at deployment? | Partial Video-DiT hidden-state computation and Action-DiT remain; full video denoising and RGB decoding are omitted on the audited canonical planning path. The exact invocation cadence is not fully reported. | `CODE FACT + NOT REPORTED` |

Parallel annotations: the hidden state is a future-generation process representation, not an established physical future state. Candidate-specific provenance and counterfactual validity are not established. The primary task is direct planning with video-world representation transfer, not future-consequence ranking.
