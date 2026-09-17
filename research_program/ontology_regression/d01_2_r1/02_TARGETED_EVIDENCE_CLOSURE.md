# D01.2-R1 Targeted Evidence Closure

This document records only the requested pressure points. It does not reopen the D01 corpus or add papers.

## A01 — Drive-WM candidate-conditioned forecasting

Evidence inspected: `papers/raw_md/P0037_DriveWM/P0037_DriveWM.raw.md`, especially the candidate sampling, future-scenario generation, reward construction, and trajectory-selection passages.

The planner samples possible trajectory candidates, generates predicted future scenarios per candidate, computes map/object rewards, and selects the ego prediction with the maximum combined reward. The reward is not merely an unspecified scorer: it contains decomposed driving outcomes such as road/map consistency and road-user safety. The corrected backend is:

```text
C3@R{direct}
X3
D2
P=PB
V=VD[map/object driving outcomes; candidate futures; perception-derived; reward; argmax]
```

This closes the first-round `V=UNKNOWN`. It does not claim calibrated counterfactual traffic response.

## A05 — DrivingGPT planning/generation split

Evidence inspected: `papers/raw_md/P0040_DrivingGPT/P0040_DrivingGPT.raw.md` and `audits/literature/RESEARCH_QA_GATE_CLOSEOUT.md`.

The paper defines an interleaved visual/action-token model and documents both planning and future-video generation behavior. The closeout audit explicitly preserves an unresolved boundary: the available evidence does not establish whether the deployed NAVSIM planning path generates and consumes every future visual token before final action output. The official code boundary was not available in the audited record.

Therefore R1 does not promote the paper to `RJ`, `D4`, or runtime `C5` merely because the architecture is joint. The conservative projection is:

```text
C5@U{direct}
XU
DU
PU
V=UNKNOWN
T=(P,A,U,U)
L=LQ
```

This is an evidence boundary, not evidence that the joint mechanism is absent.

## A10 — Auto-JEPA intent retrieval and scoring

Evidence inspected: `audits/literature/PHASE_B_WAVE3_AUTOJEPA_AUDIT.md`.

The inspected audit establishes a runtime chain: predicted future ego-intent latent → retrieval from a fixed memory → trajectory candidates → scene-conditioned scorer → drivable-area feasibility gate → final trajectory. Candidate identity is preserved to a common resolver. The scored object is the executable proposal, not a candidate-conditioned predicted environment consequence.

The corrected distinction is therefore `D1`, not `D2`:

```text
C2@R{surrogate; ego-intent endpoint}
X=∅
D1
P=PB
V=VD[scene score + drivable gate; candidate trajectories; offline simulator/metric provenance; score/filter; feasible argmax]
T=(A,A,A,U)
L=LP→LC
```

The `C2` label is retained as a decision-sufficient ego-intent endpoint, not as proof of an action-conditioned environment rollout.

## A11 — WorldRFT

Evidence inspected: `papers/raw_md/P0050_WorldRFT/P0050_WorldRFT.raw.md` and the D01 mechanism skeleton.

The spatial-aware world encoder supplies a structured current latent to the planning path. Reinforcement fine-tuning samples trajectory groups and applies collision-aware driving rewards during training; this does not, by itself, establish a deployed common candidate bank or runtime reward resolver. The conservative runtime projection is:

```text
C1@R{direct}
X=∅
D1
P=∅
V=N/A
T=(A,A,A,U)
L=LP→LS→LR
```

The deployment fate of particular RFT/reward components remains an audit attribute. A runtime candidate resolver must not be inferred from group sampling during training.

## A16 — Gen-Drive

Evidence inspected: `papers/raw_md/P0006_GenDrive/P0006_GenDrive.raw.md`.

The generator produces joint ego/agent future scenarios. Independent samples retain candidate identity and are passed to one learned scene evaluator; the selected ego trajectory comes from the best evaluated joint future. The evaluator scores the joint future itself. There is no evidence for an independent `C3` carrier alongside a separate `C5` carrier.

This closes H1/H3 in favor of H2. The remaining issue is normative composition, documented in `03_A16_COMPOSITION_DECISION.md`.

## A19 — DriveFuture

Evidence inspected: primary paper HTML/PDF for arXiv:2605.09701 (`https://arxiv.org/html/2605.09701`) together with the D01 mechanism skeleton.

At each trajectory-denoising step, a provisional action/trajectory estimate conditions a future-latent predictor; the predicted future latent is then fed back into the trajectory update. This satisfies D3 and `Tr=P`. It is an endpoint carrier, not a physical time-unrolled future sequence, so `Th=A`.

```text
C2@R{direct}
X2
D3
P=∅
V=N/A
T=(P,P,A,U)
L=joint(LN,LS)
```

The ground-truth future-latent adapter is a training-side alignment mechanism and is bypassed at inference; this is recorded in `L`, not promoted to a second runtime carrier.

## A20 — Policy World Model

Evidence inspected: `papers/raw_md/P0041_PolicyWM/P0041_PolicyWM.raw.md`, including the action-free pretraining, collaborative future/action training, and planning-inference passages.

The model rolls out future state tokens online and fuses the resulting future features into a direct trajectory decoder. The future branch is not action/control-indexed; therefore its binding is `X=∅`, not `N/A`. The learning order is action-free predictive pretraining followed by joint future/action training:

```text
C3@R{direct}
X=∅
D1
P=∅
V=N/A
T=(P,A,P,U)
L=LP→LQ
```

Pixel/video decoding is not required to establish the decision-critical carrier path.

## X=N/A boundary closure

The same schema rule resolves the requested N/A cases:

| Artifact | Correct binding | Reason |
|---|---|---|
| A03 | `X=∅` | Runtime future occupancy is applicable but not action-indexed. |
| A07 | `X=∅` | Runtime occupancy forecast has no demonstrated candidate/control condition. |
| A08 | `X=∅@T` | Training future geometry target is not action-indexed. |
| A09 | `X=∅@T` | Training world representation is predictive, not action-conditioned in the artifact boundary. |
| A12 | `X=∅@T` | Predictive representation path has no demonstrated action/control index. |
| A13 | `X4@R` | The runtime joint predictor contains world and action streams in one process; this is not N/A. |
| A18 | `X2@T` | Predicted action conditions the training video branch; runtime drop does not erase the training binding. |
| A20 | `X=∅@R` | Future token forecast conditions policy but is not itself indexed by a candidate/control. |

`N/A` remains available for a field that is genuinely not applicable to the carrier type/lifecycle, such as `P=N/A` for generation-only terminal output.
