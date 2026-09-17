# D01 Boundary and Exclusion Log

No prescribed item was excluded as irrelevant or identity-invalid. Seven works are retained as auditable boundary/control evidence and do not count as Tier 1 domain votes.

| work | verdict | required property missing | evidence and rationale | what would change the verdict |
|---|---|---|---|---|
| DriveReward | BOUNDARY | no separately traceable future/world transition in the artifact itself | The model evaluates trajectories from visual-language evidence and supplies rewards to external planners. `audits/literature/PHASE_C6_DRIVEREWARD_AUDIT.md` explicitly finds a trajectory reward/value model rather than a future-world model. | A version in which the rewarder predicts action-conditioned consequences that materially enter the attached planner would require artifact-level reconsideration. |
| RiskWorld | BOUNDARY | no evidenced causal path from predicted risk to final action formation/selection | The object-centric latent rollout ends in risk-source identification. Filtered-observation tests measure planning relevance, not online planning improvement; see `audits/literature/PHASE_C6_RISKWORLD_AUDIT.md`. | A deployed integration in which RiskWorld scores or constrains candidate actions and commits the final action. |
| DiffusionDrive | BOUNDARY | no separately traceable predictive world/consequence object | It denoises action trajectories directly. The solver's internal action state is not an environment future merely because the action distribution is generative. | An action-conditioned environment/consequence prediction actually consumed by final commitment. |
| DriveSuprim | BOUNDARY | no predictive world transition or future consequence object | It is a trajectory-vocabulary selector with coarse-to-fine filtering, hard negatives, and learned scoring. `landscape/CENSUS_PHASE_A_ROUND2.md` records it as a strong non-world-model planning control. | A candidate-specific future-state branch whose outputs enter its selector. |
| GameFormer | BOUNDARY | project-scope requirement for a distinct world/predictive object is not cleanly met | It iteratively models interacting agent and ego trajectories and is historically important, but prediction/planning are an integrated trajectory predecessor rather than the selected WAM object/lifecycle construct. | A protocol revision that explicitly admits all joint interactive prediction-planning models, or a version exposing a distinct learned transition used by commitment. |
| GAIA-1 | BOUNDARY | no demonstrated deployed one-stage planning connection | It generates driving video/world futures under multimodal conditioning, but the checked paper does not show its output forming, selecting, or optimizing a final ego action. | A primary planning experiment with an explicit world-output-to-action causal path. |
| DriveArena | BOUNDARY | platform is a simulator/evaluator, not the deployed one-stage planner | It closes the loop around external driving agents using generative simulation. Hosting and evaluating a planner does not make the platform the planner artifact. | A bundled policy whose action mechanism is part of the claimed artifact and is learned or selected through DriveArena's predictive operation. |

## Boundary consistency checks

- A strong planning score does not substitute for a predictive object: DiffusionDrive and DriveSuprim remain controls.
- A strong world generator does not substitute for a planner connection: GAIA-1 remains a world-generation boundary.
- Predictive usefulness does not substitute for action commitment: RiskWorld remains a monitor.
- A reward/value interface does not automatically become a world model: DriveReward remains an adjunct.
- A simulation platform is not counted as a deployed planner: DriveArena remains infrastructure.

## Exclusion log

`EXCLUDE = 0`. Every prescribed item has a verified identity and contributes either direct domain evidence or an intentional boundary test.
