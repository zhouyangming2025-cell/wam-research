# D01.2 Core-12 Regression

This file checks that the already accepted 12-paper route map survives the D01.2 freeze. It is a regression check, not a new projection exercise. The existing canonical headline signatures are reproduced exactly in the human-route column; no signature is rewritten to fit D01.

| Paper / scoped mode | Existing human route baseline | Backend preservation check | Regression result |
|---|---|---|---|
| LAW / planning | `R0+W0+E0 ⊕ LA/drop-future` | Future branch is train-time and action-mediated; deployed path remains direct. | KEEP |
| Epona / planning | `R0+W0+E0 ⊕ LS/bypass-visual` | Shared-state sibling world learning is not promoted to an online carrier. | KEEP |
| Epona / self or external rollout | `RG+W4+E0` | Generation-only terminal output remains separate from Epona planning. | KEEP |
| DriveLaW / paper and code | `R0+W2+E0 ⊕ LG/retain-trunk` | Future-generative internal state remains online and conditions direct action. | KEEP |
| World4Drive / planning | `RB+W3+EW ⊕ joint(LC,LA?)/retain` | Candidate endpoint consequence and factual-world agreement remain the resolver semantics. | KEEP |
| WorldDrive / planning | `RB+W3+EV ⊕ LP→joint(LT,LC)/surrogate` | Teacher-to-surrogate compression remains in ordered learning, not in a new runtime axis. | KEEP |
| WoTE / planning | `RB+W4+(EF+ED) ⊕ joint(LC,world)/retain` | Horizon consequence and factual/decomposed outcome evaluation remain distinct from endpoint routes. | KEEP |
| SeerDrive / paper | `RR+W3+E?` | Reciprocal world–policy decision loop is retained; unresolved resolver semantics remain `E?`. | KEEP |
| SeerDrive / public code | `RB+W3+(EF+ED)` | Code path is allowed to differ from the paper because the artifact/version boundary is explicit. | KEEP |
| Drive-JEPA / PF | `R0+W0+E0 ⊕ LP` | Predictive transfer with no online world carrier remains a direct route. | KEEP |
| Drive-JEPA / PB | `RB+W0+EV` or `RB+W0+(EV+ED) ⊕ LP→LC` | Candidate scoring without an online world carrier remains legal and does not become `W3/W4`. | KEEP |
| Metis / policy | `R0+W0+E0 ⊕ LA/bypass-video` | Action-mediated train-time world branch is preserved as learning, not deployment world. | KEEP |
| DynFlowDrive / planning | `RB+W0+(EW+EF+EY) ⊕ LC/drop-world` | Offline world-flow criterion compressed into the deployed candidate scorer; `W0` is preserved. | KEEP |
| Discrete-WAM / policy | `RH+W0+E0 ⊕ LQ→LR` | Semantic decision token before action remains `RH`, not candidate selection. | KEEP |
| Discrete-WAM / joint | `RJ+W5+E0 ⊕ LQ` | Joint world–action generation remains separate from policy mode and candidate resolver modes. | KEEP |
| GraphWorld / planning | `RU+W1+E? ⊕ LS→LN/retain-current-world` | Current structured-world modulation is distinct from future rollout and final commitment stays unresolved. | KEEP |

## Core-12 invariance result

The route map retains all intended separations:

- LAW versus Epona remains a learning-edge distinction under a shared direct deployment route.
- Direct train-time world learning remains distinct from DriveLaW's retained online future-generative state.
- World4Drive, WorldDrive, and WoTE remain separated by resolver semantics and endpoint versus horizon consequence.
- SeerDrive paper/code remains split because its deployment topology differs.
- Drive-JEPA PF/PB remains split by candidate commitment and scorer use, even when both have `W0`.
- Discrete-WAM policy/world/joint modes remain distinct artifact modes.
- GraphWorld remains current-world modulation with unresolved commitment, not a future rollout route.

```text
canonical headline changes: 0
core-12 required separations lost: 0
core-12 false merges introduced: 0
```
