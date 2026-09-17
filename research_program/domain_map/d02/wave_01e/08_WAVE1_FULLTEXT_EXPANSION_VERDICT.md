# D02-W1E Full-Text Expansion Verdict

## Verdict

**FULL-TEXT WAVE-1 COVERAGE COMPLETE — HOLD STRUCTURAL PRESSURE, NO ONTOLOGY CHANGE**

All twenty sealed D02 Wave-1 artifacts have now been reviewed against their
local raw Markdown. The expansion found one additional real route-pressure case
(UniAD) beyond the previously identified BeTop case. It did not reveal a new
causal topology, a missing human route code, or a need to enlarge the ontology.

## Counts

| Check | Result |
|---|---:|
| Wave-1 artifacts fully covered | 20/20 |
| Additional artifacts reviewed here | 13 |
| Total KEEP after full-text review | 17 |
| Total REMAP after full-text review | 3 |
| Remaining UNKNOWN route | 0 |
| In-domain / boundary | 10 / 10 |
| New axis | 0 |
| New R/W/E code | 0 |
| False collision | 0 |
| Structural pressure cases | 2: BeTop, UniAD |

## What the additional thirteen prove

1. **Boundary discipline holds.** ReactSim-Bench, counterfactual prediction,
   M2I, task-driven predictor evaluation, and SLEDGE use world models,
   candidate sets, or simulator loops without becoming deployed ego decision
   routes.
2. **Training-only future use stays out of W.** CRAFT and OmniDrive both use
   future/counterfactual material to improve learning or data, while deployment
   remains `W0`.
3. **Semantic hierarchy is stable.** DriveVLM and ORION support `RH` without
   turning multimodal generation into `RB`.
4. **Generation-only modes remain terminal.** DriveDreamer-2 remains a
   generation boundary, not a planner route.
5. **The candidate gate catches a genuine hidden distinction.** UniAD's
   multiple-shooting plus occupancy-cost selection changes its final commitment
   topology from `R0` to `RB`.

## What is still unresolved

BeTop and UniAD both have:

```text
shared future-horizon carrier + explicit ego candidate resolver
```

The backend can represent this as a shared `C3@B` feeding the resolver path,
with `P=PB` and `D1`; the human layer currently has a rule that normally
requires `X3` whenever `W4` and `RB` coexist. Since the future carrier is not
candidate-indexed in these two papers, applying `X3` would be false evidence.
The options remain:

- retain the rule and keep these as recorded structural pressure;
- clarify the compression rule so shared carriers may coexist with `RB`;
- require code evidence before deciding the exact backend ancestry.

This pass chooses none of the three. It records the issue for human review and
does not modify `outputs/core_mechanism_12_v1/`.

## Recommended next step

Do not start D02 Wave 2 yet. The next safe action is a focused human decision on
the shared-carrier-plus-resolver constraint, followed—if approved—by a small,
fixed-code audit of BeTop and UniAD only. After that, a larger corpus expansion
can proceed with the stabilized rule. No new ontology axis should be added based
on this twenty-artifact pass.

## Evidence boundary

This verdict is stronger than the previous shallow census because it uses full
local MinerU Markdown for all twenty selected artifacts. It is still not a claim
that the remaining local corpus has been exhaustively audited, nor is it a
code-level reproduction result. It is a full-text Wave-1 validation result.
