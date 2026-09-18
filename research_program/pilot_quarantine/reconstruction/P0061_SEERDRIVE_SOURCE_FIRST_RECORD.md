# P0061 SeerDrive — Source-First Record

Status: `READY-FOR-REVIEW`

Primary source: `papers/raw_md/P0061_SeerDrive/P0061_SeerDrive.raw.md`

Pinned source audit: `audits/literature/PHASE_C5_SEERDRIVE_AUDIT.md`

Official release boundary recorded by the audit: `LogosRoboticsGroup/SeerDrive@1cfb7ecdbdbbe52fd598949efe4edf8f6fb12b69`

The paper mechanism and the released implementation are recorded as two artifacts and are not silently merged.

## A. Author problem / gap ledger

| ID | Author-stated problem or gap | Evidence location | Status |
|---|---|---|---|
| SD-P1 | One-shot end-to-end planners rely heavily on the current scene and may underestimate future scene evolution. | Abstract; Introduction | `AUTHOR CLAIM` |
| SD-P2 | Ego future actions can influence how the surrounding scene unfolds, but this bidirectional dependency is described as underexplored. | Introduction | `AUTHOR CLAIM` |
| SD-G1 | The proposed gap is future-aware planning plus iterative interaction between scene modeling and vehicle planning. | Abstract; Introduction; Contributions | `AUTHOR CLAIM` |

These entries record the paper's problem framing only.

## B. Neutral mechanism record

### B1. Original paper artifact

```text
current BEV + multimodal ego features
→ candidate/mode-specific future BEV
→ future-aware planner
→ refined ego feature
→ feed planner feature back to BEV world model
→ update future BEV
→ repeat internal refinement
→ final trajectory
```

The paper predicts a final-horizon future BEV by default. The future ego feature is initialized from trajectory-anchor endpoints, interacts with future BEV, and is fused back into the current ego representation through motion-aware layer normalization.

### B2. Released-code artifact

The public release states that it integrates WoTE-style online trajectory evaluation and selection without the paper's iterative planning/scene-modeling interaction. The audited implementation contains trajectory anchors, a latent world model, RewardConvNet/reward heads, and a candidate reward/selection path.

Thus the original iterative world↔planner loop and the released WoTE-integrated evaluator are separate version/mode records.

### B3. Candidate and counterfactual boundary

The paper supports mode-specific future BEV outputs and mode-aligned trajectory planning, but it does not establish K independently observed alternative-action futures or reactive surrounding-agent ground truth. The released code supports candidate reward selection, but that does not retroactively prove the original paper's iterative artifact was implemented exactly.

## C. Five-question pilot projection

Status: `READY-FOR-REVIEW`

| Question | Original paper artifact | Released-code artifact |
|---|---|---|
| Q1. Where does future-related computation occur? | BEV world-model branch between current/mode ego features and the future-aware planning branches; the refined ego feature is fed back into the world model. | Latent-world/reward-evaluation path containing trajectory anchors, world features, and RewardConvNet/reward heads; the audited release does not preserve the original iterative interaction. |
| Q2. What is the future object, target, or intermediate representation? | Mode-specific final-horizon future BEV feature/semantic map plus future ego feature. | Candidate-related future/reward representation used by the WoTE-integrated evaluator; exact equivalence to the paper's iterative future BEV is not established. |
| Q3. Does the future-related signal enter the forward action chain? | Yes. Future BEV conditions trajectory generation, and the refined ego/planning feature feeds back to update the future prediction. This is not shown to be a separately scored counterfactual for every candidate. | Yes. The audited release uses future-related features in candidate reward evaluation/selection; the original iterative bidirectional loop is not confirmed in this artifact. |
| Q4. What role does the future mechanism play? | Online future-aware trajectory generation with internal world↔planner co-refinement. | Online candidate evaluation/selection in the released WoTE-integrated path. These roles must remain version-scoped. |
| Q5. What remains at deployment? | Future BEV prediction, future-aware planner fusion, feedback refinement, and final trajectory generation remain in the paper's described mechanism. | The released candidate evaluator/reward path remains; the audited README explicitly says the iterative interaction is absent. |

Evidence status: paper columns are `PAPER FACT`; release columns are `CODE FACT`; the non-equivalence and counterfactual limits are `EVIDENCE BOUNDARY` / `OUR INFERENCE`.

## D. Evidence boundaries and unresolved items

- “Iterative” refers to internal model/planner refinement, not repeated physical environment execution.
- The paper's final-horizon future BEV is not the same as a multi-step physical rollout.
- Bench2Drive closed-loop results concern the deployed policy/system and do not validate every internal candidate future as a correct counterfactual.
- The exact paper-to-release correspondence remains unresolved and must stay visible in any cross-paper table.
