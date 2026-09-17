# D01.3 Blind Projections

Only the vocabulary frozen in 00_FREEZE_MANIFEST.md is used here. No paper-specific code, temporary modifier, new axis, or ontology amendment is introduced.

## 1. Projection table

| artifact | deployment route | ordered learning route | normative C–X–D–P–V–T–L projection | human R–W–E ⊕ L projection | retain/drop | confidence | nearest existing route | result |
|---|---|---|---|---|---|---|---|---|---|
| GAD-PLAN | Future motion sequences of surrounding agents shape the interaction graph and then direct one ego trajectory; no evidenced common ego resolver. | Staged perception/map/tracking learning → shared motion prediction + planning/occupancy multi-task training; intermediate backbone freeze. | C3@R{direct}; X=∅; D1; P=∅; V=N/A; T=(A,A,P,U); L=LS | R0+W4+E0 ⊕ LS | retain{motion graph, planner, occupancy path if used}; drop{none evidenced} | high | A03/A07 direct online future-horizon conditioning | BLIND-FIT |
| DD-VIS | Supplied actions condition a future structural sequence and a diffusion video generator whose terminal product is future driving video. | structured image generation → structured video generation → action-conditioned future structural/video prediction. | C3@R{direct}; X1; D5; P=N/A; V=N/A; T=(P,A,P,U); L=LG | RG+W4+E0 ⊕ LG | retain{future video generator}; drop{action commitment path} | high | A02/A06/A21 generation-only terminal output | BLIND-FIT |
| DD-ACT | The full second-stage model jointly produces future video and future action sequence; action trajectory is the evaluated planning output and no common resolver is shown. | generative world pretraining → shared future-video/future-action sequence learning. | C5@R{direct}; X4; D4; P=∅; V=N/A; T=(P,A,P,U); L=LG→LQ | RJ+W5+E0 ⊕ LG→LQ | retain{joint world/action generator, action output}; drop{exact video-decoder fate in action-only inference UNKNOWN} | medium | A13/A17 direct joint world/action emission | BLIND-FIT-UNKNOWN |
| DRV-PLAN | Multiple trajectory proposals retain identity through a common sub-score resolver, which commits the weighted maximum. No separately predicted future scene consequence is evidenced. | pretrained visual initialization → WTA proposal learning || oracle sub-score learning; scorer→perception gradient retained, scorer→proposal gradient stopped. | C=∅; X=N/A; D=∅; P=PB; V=VD; T=(A,A,A,U); L[proposal regression || oracle scorer training; retain{proposal,scorer}] | RB+W0+ED ⊕ L[proposal regression || oracle scorer; retain{both}] | retain{scene encoder, proposal decoder, scorer}; drop{oracle at deployment} | high | DJEPA-PB2 / planning resolver with W0 | BLIND-FIT |

Legend: A=absent, P=present, U=UNKNOWN in the online clock tuple.

## 2. Artifact-level reasoning

### GAD-PLAN

The carrier gate is met by the explicitly supervised, temporally organized future trajectories used to construct interaction edges and feed the planning route through graph aggregation. The six modalities are not promoted to a final ego candidate bank. The repeated graph layers do not automatically create reciprocal world–policy topology: the paper shows predicted trajectories refining graph features, but not a committed ego action being fed into a future model and returned to a policy. Therefore D1 and absent Tr are the conservative legal projection. The physical future horizon remains present.

### DD-VIS

The terminal future video is treated as the semantic generated consequence itself, so the realization is direct. Hidden diffusion states are not separately promoted to a carrier without evidence that they are an independently traceable deployed world state. Supplied actions are an external control interface, not candidate-preserving controls. The generation mode has no action commitment task.

### DD-ACT

The paper explicitly describes joint future-video and future-action prediction and gives a joint factorization, so the full planning mode is projected as a direct joint world/action emission. The open-loop action evaluation does not establish a common resolver, so P is direct. The action-only implementation boundary is unresolved because the paper does not fully specify whether the video decoder is retained or only its internal features are used; this is recorded as an evidence modifier, not a new route.

### DRV-PLAN

The proposal bank and shared scorer satisfy all PB requirements. The proposal time horizon is an action output, not a world/consequence carrier. The human layer therefore permits RB+W0. Decomposed oracle sub-scores support VD; the exact benchmark aggregation is retained as a composition/measure detail. Training-time oracle supervision is not an online world carrier.

## 3. Type and lifecycle checks

| check | result |
|---|---|
| all C values are frozen legal values with legal realization/lifecycle | PASS |
| X is bound only where a carrier has a control interface | PASS |
| D2/D3 are not inferred from diversity or neural iteration | PASS |
| D4 is used only for a direct joint world/action output without resolver | PASS |
| PB is used only where identity reaches a common resolver | PASS |
| training-only targets do not enter W or online Th | PASS |
| terminal future video is distinguished from hidden generative state | PASS |
| no new R/W/E code or modifier | PASS |
| unknown code/source boundaries remain UNKNOWN | PASS |

## 4. Blind result before adversarial review

The selected papers can be expressed using existing legal combinations. The only material uncertainty is DriveDreamer's action/video deployment boundary, and the existing joint-emission versus internal-carrier distinctions preserve that uncertainty without schema change. No artifact currently requires a new axis or paper-named category.


