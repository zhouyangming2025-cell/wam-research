# P0064 Discrete-WAM — Source-First Record

Status: `READY-FOR-REVIEW`

Primary source: `papers/raw_md/P0064_Discrete-WAM/P0064_Discrete-WAM.raw.md`

Pinned source audit: `audits/literature/PHASE_C5_DISCRETE_WAM_AUDIT.md`

Source status in the audit: no attributable official implementation repository identified at audit time.

Historical route labels are intentionally absent.

## A. Author problem / gap ledger

| ID | Author-stated problem or gap | Evidence location | Status |
|---|---|---|---|
| DW-P1 | Direct imitation maps observations to actions without explicitly modeling action-conditioned future dynamics; task-specific intermediate annotations limit generalization. | Abstract; Introduction | `AUTHOR CLAIM` |
| DW-P2 | Continuous representations are described as weakly aligned for comparing observations, actions, and future states; hard action quantization introduces discretization error. | Introduction; Sec. 2.3 | `AUTHOR CLAIM` |
| DW-P3 | Future prediction and policy learning are often separate or auxiliary, while hierarchical driving behavior makes fully parallel action generation difficult. | Introduction | `AUTHOR CLAIM` |
| DW-G1 | The proposed gap is a shared discrete world-policy interface plus hierarchical decision-conditioned action-token editing. | Abstract; Introduction; Contributions | `AUTHOR CLAIM` |

## B. Neutral mechanism record

### B1. Shared token interface and training modes

Visual tokens and acceleration action tokens use separate vocabularies but are embedded into a shared Transformer hidden space. The paper defines three task families:

```text
world modeling:       context + future action tokens → future visual tokens
world-policy modeling: context → joint future action/visual token sequence
policy modeling:       context → decision token → future action tokens
```

These are training/capability modes, not automatically one deployment graph.

### B2. Primary planning path

For downstream planning, the paper describes hierarchical decision prediction followed by iterative parallel action-token editing. The action tokens are decoded into continuous acceleration/trajectory values. Future visual-token generation is not required by this primary planning path.

The action-conditioned world-generation and joint world-policy modes support controllable future generation and surprise analysis, but the paper does not establish that they remain in the mandatory planning resolver.

## C. Five-question pilot projection

Status: `READY-FOR-REVIEW`

| Question | Provisional answer | Evidence status |
|---|---|---|
| Q1. Where does future-related computation occur? | In the shared decoder-only Transformer through separate world-model/world-policy token-editing tasks; the primary planning path uses decision-token prediction and action-token editing. | `PAPER FACT` |
| Q2. What is the future object, target, or intermediate representation? | Future visual token sequences, future action tokens, and high-level decision tokens. Visual and action vocabularies are separate even though their embeddings share the Transformer hidden space. | `PAPER FACT` |
| Q3. Does the future-related signal enter the forward action chain? | **Not in the mandatory planning path.** The policy path is decision → action-token editing. World-policy training provides token-level coupling, but online future visual generation or a future-visual utility resolver is not established as required for planning. | `PAPER FACT` + `EVIDENCE BOUNDARY` |
| Q4. What role does the future mechanism play? | Shared multi-task world/world-policy pretraining and action-conditioned future-generation capability; planning deployment is hierarchical decision-conditioned action generation rather than candidate-world rollout. | `PAPER FACT` + `OUR INFERENCE` |
| Q5. What remains at deployment? | Decision-token prediction, confidence/schedule-guided parallel action-token editing, and trajectory decoding remain. Future visual generation is optional capability, not required in the primary planning path. | `PAPER FACT` |

Parallel provenance annotation: action-conditioned generated futures and surprise analysis are paper-reported, but observed alternative-action futures, reactive surrounding-agent truth, and a planning-time future resolver are not established.

## D. Evidence boundaries and unresolved items

- “Unified” means shared sequence machinery/hidden space and joint tasks, not one literal visual-action codebook.
- The final planning score combines pretraining, decision supervision, token editing, adaptation, and post-training; it should not be attributed monolithically to world modeling.
- No official source was identified to verify exact masks, token ordering, or whether any optional world-policy inference mode is used in deployment.
