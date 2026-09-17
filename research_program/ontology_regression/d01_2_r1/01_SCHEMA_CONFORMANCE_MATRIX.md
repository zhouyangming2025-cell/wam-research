# D01.2-R1 Schema Conformance Matrix

This matrix audits the first-round D01.2 projection against the frozen schema. It is a closed-set matrix: no category was added while projecting the 23 artifacts.

Legend:

- `PASS`: legal under the frozen schema; any remaining uncertainty is recorded as an attribute.
- `TYPE_CONSTRAINT_ERROR`: a value is not legal for the carrier/lifecycle/topology shown.
- `EVIDENCE_REQUIRED`: the syntax is legal, but the first-round value is too weak or unresolved for the available evidence.
- `POSSIBLE_COMPOSITION_GAP`: an existing composition is not expressible without a normative clarification.
- `A/P/U` in `T=(Ts,Tr,Th,Tc)` means absent/present/unknown.

| Artifact | First-round issue inspected | Conformance result | R1 correction or disposition |
|---|---|---|---|
| A01 | Resolver shown but `V` left unresolved | `EVIDENCE_REQUIRED` | Keep `C3@R`, `X3`, `D2`, `PB`; close resolver as `VD`. |
| A02 | Generation-only path | `PASS` | Keep `C3@R`, `X1`, `D5`, `P=N/A`, `V=N/A`; separate `Ts` and `Th`. |
| A03 | Applicable future carrier marked `X=N/A` | `TYPE_CONSTRAINT_ERROR` | Use `X=∅`; keep direct carrier-to-policy `D1`. |
| A04 | Training-only action-conditioned rollout | `PASS` | Keep runtime `D=∅`; bind `X2` to `@T`, not deployment. |
| A05 | Runtime joint generation inferred from shared architecture | `EVIDENCE_REQUIRED` | Use `C5@U`, `XU`, `DU`, `PU`, `V=UNKNOWN`; preserve `LQ`. |
| A06 | Generation-only path | `PASS` | Keep `D5/P=N/A/V=N/A`; make solver and physical horizon explicit. |
| A07 | Applicable future carrier marked `X=N/A` | `TYPE_CONSTRAINT_ERROR` | Use `X=∅`; keep `D1`. |
| A08 | Training future carrier marked `X=N/A` | `TYPE_CONSTRAINT_ERROR` | Use `X=∅@T`; runtime remains `D=∅`. |
| A09 | Training future carrier marked `X=N/A` | `TYPE_CONSTRAINT_ERROR` | Use `X=∅@T`; heads dropped/bypassed remain a lifecycle attribute. |
| A10 | Resolver known but `P=PU`, `V=UNKNOWN` | `EVIDENCE_REQUIRED` | Use `C2@R` surrogate, `X=∅`, `D1`, `PB`, `VD`; retain candidate retrieval/scoring/gate. |
| A11 | Paper/code and deployment boundary unresolved | `EVIDENCE_REQUIRED` | Close to conservative `C1@R`, `X=∅`, `D1`; retain uncertainty in learning/fate fields. |
| A12 | Applicable future carrier marked `X=N/A` | `TYPE_CONSTRAINT_ERROR` | Use `X=∅@T`; runtime planning remains outside the carrier. |
| A13 | `X=N/A` obscured joint world/action runtime | `TYPE_CONSTRAINT_ERROR` | Use `C5@R`, `X4`, `D4`, `P=∅`; future/action process emits the direct trajectory. |
| A14 | Candidate endpoint path | `PASS` | Keep `C2@R`, `X3`, `D2`, `PB`; expand `V` composition. |
| A15 | Candidate horizon path | `PASS` | Keep `C3@R`, `X3`, `D2`, `PB`; retain factual/decomposed resolver attributes. |
| A16 | Same semantic object duplicated as `C3+C5`; D2/C5 composition not admitted | `POSSIBLE_COMPOSITION_GAP` | Replace with one `C5{k}@R`; use `X4@birth+X3@resolver`; hold `D2⟨C5{k}⟩` clarification. |
| A17 | Single joint generated sample | `PASS` | Keep `C5@R`, `X4`, `D4`, `P=∅`, `V=N/A`; no common resolver. |
| A18 | Training-only future branch marked `X=N/A` | `TYPE_CONSTRAINT_ERROR` | Use `X2@T`; runtime is direct action after video branch drop. |
| A19 | Endpoint carrier given a physical horizon clock | `TYPE_CONSTRAINT_ERROR` | Set `Th=A`; keep `Tr=P` for action-hypothesis→future→revised-action coupling. |
| A20 | Applicable forecast carrier marked `X=N/A`; learning order under-described | `TYPE_CONSTRAINT_ERROR` | Use `X=∅`; retain `C3@R/D1`, update `L=LP→LQ`. |
| A21 | Generation-only terminal output | `PASS` | Keep `D5/P=N/A`; action/control is external `X1`. |
| A22 | Training simulator branch | `PASS` | Keep runtime `D=∅`; `C3@T` and `X1@T` do not create `W4` online. |
| A23 | Candidate rollout/scoring | `PASS` | Keep `C3@R`, `X3`, `D2`, `PB`; retain proposal-distillation attributes. |

## Constraint checks

1. Every applicable `C` has an `X` binding or explicit `X=∅`; all corrected projections satisfy this.
2. No corrected row uses `C3+C5` for one semantic object; A16 is represented as a single `C5{k}` with stage-specific binding.
3. All D2 rows have candidate identity, common resolver, and non-`N/A` `V`; A16 is held only because the frozen text excludes candidate-indexed C5 from D2.
4. D3 is retained only for A19, where an action hypothesis is reintroduced into the future predictor before final action commitment.
5. D4 is retained only where a joint world/action process itself emits the runtime action/world pair; it is not used for ordinary diffusion denoising.
6. `Th` is present only when a physical future horizon is actually represented. Diffusion or flow solver steps populate `Ts`, not `Th`.
7. Learning edges remain ordered and lifecycle-aware; no learning edge is inferred from a runtime route alone.

## Closed-set artifact projection record

The following table supplies the required per-artifact record. The backend and human signatures in this table are the **first-round values under review**; corrected values are in `04_CORRECTED_ARTIFACT_PROJECTIONS.md`.

| Artifact | Deployment route in one sentence | Ordered learning route in one sentence | First-round `C–X–D–P–V–T–L` | First-round `R–W–E ⊕ L` | Nearest canonical route | Confidence | Result |
|---|---|---|---|---|---|---|---|
| A01 | Candidate trajectories receive generated future scenarios and a reward-based selection. | Retained future generator is trained with planning-relevant reward/representation objectives. | `C3@R;X3;D2;PB;V=UNKNOWN;T=(U,A,P,U);L=LG` | `RB+W4+E? ⊕ LG` | WoTE | M | `EVIDENCE_REQUIRED` |
| A02 | A controllable future video is generated as the terminal product. | A generative world model is trained and retained for controlled rollout. | `C3@R;X1;D5;P=N/A;V=N/A;T=(U,A,P,U);L=LG` | `RG+W4+E0 ⊕ LG` | Epona rollout | H | `PASS` |
| A03 | Predicted occupancy futures condition a direct ego-trajectory policy. | Predictive occupancy learning shapes the retained planning representation. | `C3@R;X=N/A;D1;P=∅;V=N/A;T=(U,A,P,U);L=LS` | `R0+W4+E0 ⊕ LS` | direct online future route | M | `TYPE_CONSTRAINT_ERROR` |
| A04 | The deployed policy emits action/control directly; imagined rollout is training-side. | A learned world rollout supplies imagined transitions/rewards to actor-critic optimization. | `C3@T;X2;D∅;P=∅;V=N/A;T=(A,A,P,U);L=LR` | `R0+W0+E0 ⊕ LR` | LAW/Epona direct | M | `PASS` |
| A05 | The planning mode’s exact online use of generated visual tokens is unresolved. | One shared autoregressive sequence objective learns visual and action tokens. | `C5@R;X4;D4;P=∅;V=N/A;T=(P,A,P,U);L=LQ` | `RJ+W5+E0 ⊕ LQ` | Discrete-WAM joint | M | `EVIDENCE_REQUIRED` |
| A06 | A future visual sequence is generated as the terminal output under control. | A future-video generator is trained as a retained generative branch. | `C3@R;X1;D5;P=N/A;V=N/A;T=(U,A,P,U);L=LQ` | `RG+W4+E0 ⊕ LQ` | Epona rollout | H | `PASS` |
| A07 | A forecasted occupancy horizon directly conditions trajectory formation. | Occupancy prediction and policy objectives share a retained representation. | `C3@R;X=N/A;D1;P=∅;V=N/A;T=(U,A,P,U);L=LS` | `R0+W4+E0 ⊕ LS` | direct online future route | M | `TYPE_CONSTRAINT_ERROR` |
| A08 | No predictive world carrier remains online; a downstream planner acts directly. | Future-geometry predictive pretraining transfers an encoder to the planner. | `C3@T;X=N/A;D∅;P=∅;V=N/A;T=(A,A,P,U);L=LP` | `R0+W0+E0 ⊕ LP` | Drive-JEPA PF | M | `TYPE_CONSTRAINT_ERROR` |
| A09 | No pretraining future head is consumed online; the transferred backbone supports direct planning. | World-model pretraining transfers a spatiotemporal backbone, with heads dropped/bypassed. | `C3@T;X=N/A;D∅;P=∅;V=N/A;T=(A,A,P,U);L=LP` | `R0+W0+E0 ⊕ LP` | Drive-JEPA PF | M | `TYPE_CONSTRAINT_ERROR` |
| A10 | A predicted ego-intent representation retrieves, scores, gates, and returns a trajectory. | Predictive intent learning is followed by offline scorer/gate learning retained for selection. | `C2@R;X=N/A;D1;P=PU;V=UNKNOWN;T=(A,A,A,U);L=LP` | `RB+W3+E? ⊕ LP→LC` | Drive-JEPA PB | H | `EVIDENCE_REQUIRED` |
| A11 | A structured spatial world state conditions a direct policy; no common resolver is evidenced. | World representation learning and reward fine-tuning jointly shape the action path. | `CU@U;XU;DU;PU;V=UNKNOWN;T=(U,U,U,U);L=LU` | `RU+WU+E? ⊕ LU` | GraphWorld/current-world route | M | `EVIDENCE_REQUIRED` |
| A12 | The downstream planner acts directly after predictive representation learning. | Predictive representation learning transfers into the trajectory planner. | `C3@T;X=N/A;D∅;P=∅;V=N/A;T=(A,A,P,U);L=LP` | `R0+W0+E0 ⊕ LP` | Drive-JEPA PF | M | `TYPE_CONSTRAINT_ERROR` |
| A13 | A joint future-scene/action process directly emits the future trajectory. | Future representation pretraining is followed by shared world/action sequence learning. | `C3@T;X=N/A;D∅;P=∅;V=N/A;T=(A,A,P,U);L=LQ` | `R0+W0+E0 ⊕ LQ` | Discrete-WAM joint | H | `TYPE_CONSTRAINT_ERROR` |
| A14 | Candidate-specific future latents are scored by one common resolver. | Predictive future alignment, action/world losses, and candidate scoring are jointly retained. | `C2@R;X3;D2;PB;V=VD→VU;T=(A,A,A,U);L=LP→joint(LA,LN,LC)` | `RB+W3+(ED→EV) ⊕ L` | World4Drive/WorldDrive endpoint | M | `PASS` |
| A15 | Candidate horizon consequences are compared by a common resolver. | World/policy objectives and outcome-based scoring retain the proposal and evaluator. | `C3@R;X3;D2;PB;V=VD;T=(U,A,P,U);L=joint(LS,LC)` | `RB+W4+ED ⊕ L` | WoTE | H | `PASS` |
| A16 | Multiple joint future samples are scored by a common scene evaluator before commitment. | A learned scene preference is used to fine-tune the joint generator by reward optimization. | `C3+C5@R;X4;D2;PB;V=VU;T=(P,A,P,U);L=LC→LR` | `RB+W4+EV{joint-generation modifier} ⊕ L` | no exact canonical route | H | `POSSIBLE_COMPOSITION_GAP` |
| A17 | One joint world/action sample emits the action without a common runtime resolver. | A reward/criterion shapes the joint generator; selection is not required at deployment. | `C5@R;X4;D4;P=∅;V=N/A;T=(P,A,P,U);L=LC→LR` | `RJ+W5+E0 ⊕ L` | Discrete-WAM joint | M | `PASS` |
| A18 | The action expert emits a direct trajectory after the future-video branch is dropped. | Joint action/video flow training is followed by reward optimization of the retained action path. | `C3@T;X=N/A;D∅;P=∅;V=N/A;T=(A,A,P,U);L=LS→LR` | `R0+W0+E0 ⊕ LS→LR` | Metis | M | `TYPE_CONSTRAINT_ERROR` |
| A19 | A provisional action hypothesis and predicted future latent refine one another during denoising. | Future-latent alignment and shared planner/world training shape the retained reciprocal path. | `C2@R;X2;D3;P=∅;V=N/A;T=(P,P,P,A);L=LS` | `RR+W3+E0 ⊕ LS` | SeerDrive paper | H | `TYPE_CONSTRAINT_ERROR` |
| A20 | An online forecast token horizon is fused into a direct trajectory decoder. | Action-free predictive pretraining is followed by collaborative future/action learning. | `C3@R;X=N/A;D1;P=∅;V=N/A;T=(P,A,P,U);L=LQ` | `R0+W4+E0 ⊕ LQ` | DriveLaW / direct future route | H | `TYPE_CONSTRAINT_ERROR` |
| A21 | A reactive world renderer generates sensor/video futures as the terminal output. | A generative simulator is trained/retained for external-control world rollout. | `C3@R;X1;D5;P=N/A;V=N/A;T=(P,A,P,U);L=LG` | `RG+W4+E0 ⊕ LG` | Epona rollout | M | `PASS` |
| A22 | The final policy acts directly; simulator/world generation is training-only. | Simulator-derived outcomes provide the reward/criterion for policy optimization. | `C3@T;X1;D∅;P=∅;V=N/A;T=(A,A,P,U);L=LC→LR` | `R0+W0+E0 ⊕ LC→LR` | Metis/LAW direct | M | `PASS` |
| A23 | Candidate trajectories are rolled out through future consequences and the minimum-cost one is committed. | A proposal network is distilled and a runtime risk/progress criterion scores candidates. | `C3@R;X3;D2;PB;V=VD;T=(U,A,P,U);L=LT→LC` | `RB+W4+ED ⊕ LT→LC` | WoTE | M | `PASS` |
