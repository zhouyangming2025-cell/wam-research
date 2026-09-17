# Normalized Collision and Counterexample Audit

The audit uses three views, because “same route” has three legitimate meanings:

1. **human route collision** — same R–W–E deployment family;
2. **runtime backend collision** — same deployment-relevant C–X–D–P–V–T structure;
3. **full mechanism collision** — same runtime structure and ordered L program.

An expected collision is a functional equivalence class. A false collision is a pair that requires a different answer to the same semantic question.

## Normalized groups

| Normalized group | Members | Why the collision is acceptable | What still separates them |
|---|---|---|---|
| R0+W0+E0 direct/no online carrier | A04, A08, A09, A12, A18, A22 | All deploy a direct action path with no qualifying online world carrier. | L, lifecycle, training objective, simulator/video fate, and representation provenance. |
| R0+W4+E0 direct/future horizon | A03, A07, A20 | All use an online future horizon to condition direct action without candidate identity or resolver. | Occupancy versus autoregressive token realization; LS versus LP→LQ. |
| R0+W1+E0 direct/current world | A11 | Singleton current-world family. | RFT and paper/code evidence attributes. |
| RB+W3+ED candidate endpoint/horizon resolver | A01, A15, A23 | All preserve candidate identity, materialize online candidate consequences, and resolve using decomposed driving outcomes. | A01/A15/A23 differ in horizon semantics and learning/deployment fate. |
| RB+W3+ED endpoint candidate resolver | A10, A14 after resolver normalization | Both retain candidates and a common resolver with driving-outcome information. | A10 is D1 intent retrieval without candidate consequence; A14 is D2 candidate endpoint consequence. The backend split prevents a false merge. |
| RJ+W5+E0 joint world/action generation | A13, A17 | Both use one joint world/action process to emit the action without a common candidate resolver. | LP→LQ versus LC→LR; future prediction and reward fine-tuning are different learning DAGs. |
| RG+W4+E0 generation-only future output | A02, A06, A21 | All terminate in a generated future world sequence rather than a committed planning action. | Controllable-video versus simulator semantics and target/reaction attributes. |

A05 remains outside normalized groups because runtime fate is unresolved. A16 is not silently placed in RJ+W5+E0; its PB resolver is the pressure case.

## Required split tests

### Candidate retrieval is not candidate consequence

A10 retrieves multiple executable trajectories and scores them, but the inspected evidence does not establish one predicted world consequence per candidate. It remains D1, not D2. A14/A15/A23 are D2 because a candidate-specific future consequence is materialized before resolution.

### Training rollout is not online carrier

A04, A08, A09, A12, A18, and A22 may all use future/world material during training, but their corrected runtime human route is W0. This is exactly the lifecycle distinction the two-layer signature is intended to preserve.

### Solver steps are not reciprocal policy/world refinement

A19 is D3 because a provisional action hypothesis is used to recompute the future carrier, and that carrier changes the next action update. Ordinary diffusion steps in A01/A02/A06/A13/A16/A17 do not receive D3 merely because they iterate.

### Joint generation is not candidate selection

A13 and A17 are D4/RJ: the joint process emits world/action content. A16 adds candidate identity and a common evaluator, so it needs PB and the held D2⟨C5{k}⟩ composition. This is a genuine topology split.

### Generation output is not planning

A02, A06, and A21 are D5/RG; their generated world is the terminal product. They must not be grouped with A13/A17, where action is a terminal output, or with A01/A15/A16/A23, where candidates are resolved.

## Invariance tests

The following substitutions do not change the corrected route when semantic interfaces stay fixed:

- regression ↔ diffusion ↔ flow;
- RGB/video ↔ BEV/occupancy ↔ latent/token;
- transformer ↔ DiT ↔ recurrent implementation;
- direct versus surrogate realization when both expose the same carrier lifecycle and output role.

The substitutions do change attributes or learning edges when they alter deployment fate, candidate identity, resolver semantics, or action/world gradient direction. This is the intended boundary.

## Version and mode tests

- SeerDrive paper versus released code remains two projections: paper RR+W3+E?, code RB+W3+(EF+ED).
- Drive-JEPA PF versus PB remains separate: PF is direct R0+W0+E0; PB retains RB+W0+EV without an online world carrier.
- Gen-Drive A16 versus A17 remains separate: common resolver versus single joint sample.
- DrivingGPT A05 planning/generation boundary remains unresolved rather than being collapsed to the architecture headline.

## Collision verdict

The normalized collisions are mostly the intended functional equivalence classes. No collision requires a new axis or a second taxonomy. A16 is the only counterexample where the current global admissibility rule is narrower than the observed mechanism composition.
