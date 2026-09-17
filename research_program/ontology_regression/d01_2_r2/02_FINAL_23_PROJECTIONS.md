# D01.2-R2 Final 23-Artifact Projections

All rows below are checked after the approved amendment. `T=(Ts,Tr,Th,Tc)` uses `A=absent`, `P=present`, and `U=UNKNOWN`. All realization modifiers are from the legal set `direct | surrogate | generative_internal | unknown`.

`retain/drop` records the deployment boundary; it is not a new axis.

| Artifact | Deployment route | Ordered learning route | Final `C-X-D-P-V-T-L` | Human route | Retain/drop boundary | Result |
|---|---|---|---|---|---|---|
| A01 | Candidate trajectories receive future-horizon scenarios and a common decomposed reward selects A*. | Retained future generation and planning objectives train the online branch. | `C3@R{direct};X3;D2;PB;VD;T=(P,A,P,U);L=LG` | `RB+W4+ED ⊕ LG` | retain{candidate future generator,resolver}; drop{training-only target details} | PASS |
| A02 | A controlled future multiview video is the terminal output. | A generative carrier is trained and retained for controlled rollout. | `C3@R{generative_internal};X1;D5;P=N/A;V=N/A;T=(P,A,P,U);L=LG` | `RG+W4+E0 ⊕ LG` | retain{world generator}; drop{action commitment path} | PASS |
| A03 | Runtime occupancy futures condition direct trajectory formation. | Occupancy prediction shapes the retained policy representation. | `C3@R{direct};X=∅;D1;P=∅;V=N/A;T=(A,A,P,U);L=LS` | `R0+W4+E0 ⊕ LS` | retain{occupancy forecast,policy}; drop{none evidenced} | PASS |
| A04 | A direct policy action deploys; imagined rollout is not online. | Learned rollout supplies imagined transitions/rewards for actor-critic optimization. | `C3@T{direct};X2@T;D∅;P=∅;V=N/A;T=(A,A,A,U);L=LC->LR` | `R0+W0+E0 ⊕ LC->LR` | retain{policy}; drop{world rollout,training reward computation} | PASS |
| A05 | The inspected planning path's online use of future visual tokens remains unresolved. | One autoregressive objective learns visual and action tokens jointly. | `C5@U{direct};XU;DU;PU;V=UNKNOWN;T=(P,A,U,U);L=LQ` | `RU+WU+E? ⊕ LQ` | retain/drop{runtime fate UNKNOWN} | PASS (UNKNOWN preserved) |
| A06 | A controlled future visual sequence is the terminal output. | A future-video generator is trained as the retained output branch. | `C3@R{generative_internal};X1;D5;P=N/A;V=N/A;T=(P,A,P,U);L=LG` | `RG+W4+E0 ⊕ LG` | retain{future generator}; drop{action resolver} | PASS |
| A07 | Forecasted occupancy conditions direct trajectory formation. | Occupancy and policy objectives share a retained representation. | `C3@R{direct};X=∅;D1;P=∅;V=N/A;T=(A,A,P,U);L=LS` | `R0+W4+E0 ⊕ LS` | retain{occupancy path,policy}; drop{candidate resolver} | PASS |
| A08 | The downstream planner acts directly; predictive future geometry is not online. | Future geometry pretraining transfers an encoder to the planner. | `C3@T{direct};X=∅@T;D∅;P=∅;V=N/A;T=(A,A,A,U);L=LP` | `R0+W0+E0 ⊕ LP` | retain{transferred encoder,planner}; drop{predictive decoder/head} | PASS |
| A09 | A transferred spatiotemporal backbone supports direct planning. | World-model pretraining transfers the retained backbone. | `C3@T{direct};X=∅@T;D∅;P=∅;V=N/A;T=(A,A,A,U);L=LP` | `R0+W0+E0 ⊕ LP` | retain{backbone,planner}; drop{pretraining future heads} | PASS |
| A10 | Predicted ego intent retrieves candidates, then scene score and feasibility gate select one. | Intent prediction is followed by scorer/gate training retained for selection. | `C2@R{surrogate};X=∅;D1;PB;VD;T=(A,A,A,U);L=LP->LC` | `RB+W3+ED ⊕ LP->LC` | retain{intent predictor,memory,scorer,gate}; drop{predictive target branch} | PASS |
| A11 | A structured current world representation conditions a direct policy; no resolver is evidenced. | World representation and reward fine-tuning shape the retained action path. | `C1@R{direct};X=N/A;D1;P=∅;V=N/A;T=(A,A,A,U);L=LP->LS->LR` | `R0+W1+E0 ⊕ LP->LS->LR` | retain{current-world encoder,policy}; drop{training-only reward machinery as applicable} | PASS |
| A12 | The downstream planner acts directly after predictive representation learning. | Predictive representation learning transfers into the planner. | `C3@T{direct};X=∅@T;D∅;P=∅;V=N/A;T=(A,A,A,U);L=LP` | `R0+W0+E0 ⊕ LP` | retain{encoder,planner}; drop{predictive target/head} | PASS |
| A13 | One joint future-scene/action flow process directly emits the trajectory. | Future predictive pretraining is followed by shared world/action learning. | `C5@R{direct};X4;D4;P=∅;V=N/A;T=(P,A,P,U);L=LP->LQ` | `RJ+W5+E0 ⊕ LP->LQ` | retain{joint predictor,action stream}; drop{training target branch as applicable} | PASS |
| A14 | Candidate endpoint future latents reach a common resolver. | Predictive alignment, world/action learning, and candidate scoring are retained. | `C2@R{direct};X3;D2;PB;VD->VU;T=(A,A,A,U);L=LP->joint(LA,LN,LC)` | `RB+W3+(ED->EV) ⊕ L` | retain{candidate predictor,scorer}; drop{target/factual teacher branches} | PASS |
| A15 | Candidate horizon consequences are evaluated by a common resolver. | Shared world/policy objectives and decomposed outcomes shape the evaluator. | `C3@R{direct};X3;D2;PB;VD;T=(A,A,P,U);L=joint(LS,LC)` | `RB+W4+ED ⊕ L` | retain{future rollout,evaluator,resolver}; drop{training-only target details} | PASS |
| A16 | Candidate-indexed joint futures are scored by one evaluator before commitment. | Scene preference trains/fine-tunes the joint generator through reward optimization. | `C5@R{direct}[k];X4;D2⟨C5{k}->V{k}->resolver->A*⟩;PB;VU;T=(P,A,P,U);L=LC->LR` | `RB+W5+EV ⊕ LC->LR` | retain{joint generator,evaluator}; drop{VLM preference labels/training-only reward pipeline} | PASS |
| A17 | One joint world/action sample emits action without a common resolver. | Reward/criterion learning shapes the joint generator. | `C5@R{direct};X4;D4;P=∅;V=N/A;T=(P,A,P,U);L=LC->LR` | `RJ+W5+E0 ⊕ LC->LR` | retain{joint generator,action output}; drop{optional evaluator at deployment} | PASS |
| A18 | The action expert emits a direct trajectory after future-video drop. | Joint action/video flow training is followed by reward optimization of the action path. | `C3@T{direct};X2@T;D∅;P=∅;V=N/A;T=(A,A,A,U);L=LS->LR` | `R0+W0+E0 ⊕ LS->LR` | retain{action expert,observation path}; drop{future-video expert/output} | PASS |
| A19 | A provisional action conditions a future endpoint predictor that guides the next denoising update. | Future-latent alignment and shared world/policy learning retain reciprocal guidance; GT adapter is bypassed online. | `C2@R{direct};X2;D3;P=∅;V=N/A;T=(P,P,A,U);L=joint(LN,LS)` | `RR+W3+E0 ⊕ joint(LN,LS)` | retain{future predictor,planner}; drop{GT future adapter/target input} | PASS |
| A20 | Online future tokens are fused into a direct trajectory decoder. | Action-free predictive pretraining is followed by collaborative future/action learning. | `C3@R{direct};X=∅;D1;P=∅;V=N/A;T=(P,A,P,U);L=LP->LQ` | `R0+W4+E0 ⊕ LP->LQ` | retain{future token forecast,action decoder}; drop{optional pixel visualization} | PASS |
| A21 | A reactive world renderer generates sensor/video futures as the terminal product. | A generative simulator is trained and retained for external-control rollout. | `C3@R{generative_internal};X1;D5;P=N/A;V=N/A;T=(P,A,P,U);L=LG` | `RG+W4+E0 ⊕ LG` | retain{world renderer}; drop{policy commitment path} | PASS |
| A22 | The final policy acts directly; simulator/world generation is training-only. | Simulator-derived outcomes provide reward/criterion for policy optimization. | `C3@T{generative_internal};X1@T;D∅;P=∅;V=N/A;T=(A,A,A,U);L=LC->LR` | `R0+W0+E0 ⊕ LC->LR` | retain{policy}; drop{simulator/world generator at deployment} | PASS |
| A23 | Candidate trajectories roll through consequences and the minimum-cost candidate is committed. | Proposal distillation is followed by runtime risk/progress criterion scoring. | `C3@R{direct};X3;D2;PB;VD;T=(U,A,P,U);L=LT->LC` | `RB+W4+ED ⊕ LT->LC` | retain{proposal,rollout,scorer}; drop{heavy teacher/distillation source} | PASS |

## Conformance summary

```text
23/23 legal projections
illegal realization modifiers = 0
illegal training-only Th=P leaks = 0
incorrect A11 X binding = 0
rejected resolver-binding occurrences in A16 = 0
```

A05 remains an honest UNKNOWN boundary, not a schema error. A16 is now a legal existing-axis composition.
