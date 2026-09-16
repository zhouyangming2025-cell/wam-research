# Core Mechanism 12 — Route Compression and Collision Audit

Status: internal compression audit complete; human adoption gate remains open.

Audited proposal:

```text
R–W–E ⊕ L
```

Source baseline:

```text
branch = codex/gpt6-mechanism-handoff
baseline commit before this compression phase = 0408ef76b38d371a5cabbb9c14cd4ae354379c27
normative audit specification = 09_ONTOLOGY_SPEC_S1_PLUS.md
frozen specification SHA256 = 34c14ea6d8f7c6869f50240d968d1f070d9dfc36e5247cf113542db938a6abdf
```

The audit ontology was not edited during this phase.

## 1. Audit question

Can the seven-field audit ontology be compressed into a route map that is:

- readable in one line;
- faithful to deployment causality and learning direction;
- invariant to representation and network implementation;
- complete over all 21 frozen artifacts;
- honest about paper/code/mode and UNKNOWN boundaries;
- capable of grouping functionally equivalent papers without claiming full DAG identity?

The target is not lossless reconstruction. The target is controlled, documented information loss with a deterministic path back to the evidence ledger.

## 2. Coverage test

| Test | Result |
|---|---|
| Frozen artifacts projected | 21/21 |
| Base papers represented | 12/12 |
| Paper/code splits retained | DriveLaW and SeerDrive |
| Required mode splits retained | LAW, Epona, Drive-JEPA, Discrete-WAM |
| Paper-named R/W/E category introduced | 0 |
| Implementation-named R/W/E category introduced | 0 |
| Artifact requiring a fifth headline field | 0 |
| `UNKNOWN` silently converted to absence | 0 |

Verdict: **PASS** for corpus coverage.

## 3. Compression-budget test

The audit headline had seven fields:

```text
C + X + D + P + V + T + L
```

The human headline has four questions:

```text
R + W + E ⊕ L
```

Compression operations:

| Audit information | Human treatment |
|---|---|
| D plus action-relevant P | merged into R |
| runtime C and its output ancestry | compressed into primary W |
| V semantic atoms/composition | renamed E |
| ordered L program | retained in shortened form |
| X candidate identity | implied by RB/RR and verified below; self/external generation control retained as RG modifier |
| T reciprocal/horizon clocks | preserved through RR/W4 when route-defining |
| T solver/cross-cycle clocks | demoted to audit unless they change E semantics |
| supporting carriers | retained only in audit notes |

Each projected row contains exactly one R, one W, one E expression, and one shortened learning program.

Verdict: **PASS** for structural compression. The L expression remains intentionally richer than the three runtime fields.

## 4. Reconstruction test

Representative signatures were reconstructed without consulting architecture names.

### 4.1 `R0 + W0 + E0 ⊕ LA/drop`

Reconstructed mechanism:

```text
one direct action path
+ no qualifying online world carrier
+ predicted action conditions a train-time future/world loss
+ world branch absent from deployed action computation
```

Matches: LAW and Metis at the intended functional granularity.

### 4.2 `R0 + W2 + E0 ⊕ LG/retain`

Reconstructed mechanism:

```text
one direct action path
+ online future-generative internal state conditions action
+ generative trunk is pretrained/adapted and retained
```

Matches: DriveLaW.

### 4.3 `RB + W0 + EV ⊕ LP→LC`

Reconstructed mechanism:

```text
explicit candidates reach one resolver
+ no future/world carrier remains online
+ scorer estimates holistic planning utility
+ predictive pretraining transfers representation and simulator labels train the scorer
```

Matches: Drive-JEPA PB1.

### 4.4 `RB + W3 + EW ⊕ LC/retain`

Reconstructed mechanism:

```text
one endpoint consequence per candidate
+ factual-future world agreement defines preference
+ future path and resolver remain online
```

Matches: World4Drive.

### 4.5 `RB + W4 + (EF+ED) ⊕ LC/retain`

Reconstructed mechanism:

```text
one future horizon per candidate
+ imitation and decomposed driving outcomes determine preference
+ rollout/reward/resolver remain online
```

Matches: WoTE.

### 4.6 `RR + W3 + E? ⊕ LA/retain`

Reconstructed mechanism:

```text
action and predicted endpoint repeatedly revise each other inside one decision
+ reciprocal path is retained
+ final resolver semantics are unresolved
```

Matches: SeerDrive paper.

### 4.7 `RJ + W5 + E0 ⊕ LQ/retain`

Reconstructed mechanism:

```text
world and action are one joint online generation/editing process
+ shared world–action sequence learning creates the retained model
```

Matches: Discrete-WAM joint mode.

Verdict: **PASS** for route-family reconstruction. Exact detach edges, solver clocks, and support carriers are not reconstructible by design.

## 5. Collision audit

### 5.1 Expected runtime collisions

| Collision group | Shared R–W–E | Why the collision is desirable | Split retained in L/audit |
|---|---|---|---|
| LAW-PF / LAW-PB / EPO-PLAN / DJEPA-PF / METIS-PLAN | `R0+W0+E0` | all deploy a direct policy without an online world carrier or resolver | LA vs LS vs LP; paper modes and exact DAGs remain separate |
| DLAW-PAPER / DLAW-CODE | `R0+W2+E0` | same semantic planning route despite solver/config differences | paper/code numeric and source discrepancies remain audit attributes |
| EPO-CTRL / DWAM-WORLD | `RG{external}+W4+E0` | both externally control a generated future horizon | LS curriculum versus LQ/world-sequence learning |

These are runtime-family equivalences, not claims of full mechanism identity.

### 5.2 Expected full human-family collisions

After normalizing “drop” and “bypass” to “world branch absent from deployed action path”:

```text
LAW-PF / LAW-PB / METIS-PLAN
= R0 + W0 + E0 ⊕ LA/world-branch-absent
```

This is an intentional collision. All three use the same functional learning edge:

```text
predicted action
→ future/world branch
→ world loss reaches action-producing computation
→ world branch is not consumed online
```

Their latent predictor, asymmetric video expert, flow solver, and exact gradient scopes remain implementation/full-DAG distinctions.

Also intentional:

```text
DLAW-PAPER = DLAW-CODE
```

at the human mechanism-family level. The known paper/code differences are numerical or implementation-bound rather than semantic route changes.

### 5.3 Required non-collisions

| Pair/group | Separating code | Verdict |
|---|---|---|
| LAW vs Epona planning | `LA` vs `LS` | correctly split learning mechanism |
| LAW/Epona vs DriveLaW | `W0` vs `W2` | correctly split offline learning from online future-generative conditioning |
| W4D vs WorldDrive | `EW` vs `EV`; LC/direct-retained vs LP→LT/LC surrogate | correctly split resolver target and learning route |
| WorldDrive vs WoTE | `W3+EV` vs `W4+(EF+ED)` | correctly split endpoint utility from horizon outcome evaluation |
| W4D vs WoTE | `W3+EW` vs `W4+(EF+ED)` | correctly split consequence extent and criterion semantics |
| Seer paper vs code | `RR+E?` vs `RB+(EF+ED)` | correctly preserves paper/code mechanism mismatch |
| DJEPA PF vs PB1 | `R0+E0` vs `RB+EV` | correctly preserves task-mode commitment change |
| DJEPA PB1 vs PB2 | `EV` vs `weighted(EV,ED)` | correctly preserves comfort recalibration semantics |
| DFD vs W4D | `W0` vs `W3` | correctly separates train-time world criterion from online consequence evaluation |
| DWAM policy vs joint | `RH+W0` vs `RJ+W5` | correctly preserves semantic hierarchy versus joint world–action generation |
| Epona self vs controlled rollout | `RG{self}` vs `RG{external}` | correctly preserves control provenance that defines the mode |
| GraphWorld vs DriveLaW | `RU+W1` vs `R0+W2` | correctly separates current structured world modulation from future-generative conditioning |

No mechanically identified false collision remains among the 21 artifacts at the stated functional granularity.

Verdict: **PASS provisionally**, pending human judgment that the LAW/Metis merge and other expected collisions match the intended research granularity.

## 6. Counterexample tests

### 6.1 Ordinary BEV consumed by a planner

```text
encoder/BEV → planner
without stateful world operation and carrier-level world grounding
```

Result: does not qualify for `W1`; remains ordinary context below the signature.

### 6.2 Multiple random samples without a common resolver

Result: not `RB`. Sampling count is not candidate commitment.

### 6.3 Train-time future predictor removed at deployment

Result: `W0`, with the future mechanism represented in L. Verified by LAW, Epona planning, Drive-JEPA, Metis, and DynFlowDrive.

### 6.4 Runtime candidate scorer with no online world carrier

Result: `RB+W0`, not `R0` and not `RB+W3`. Verified by Drive-JEPA PB and DynFlowDrive.

### 6.5 Diffusion or flow iterations

Result: solver steps alone do not create `RR` or `W4`. Verified by DriveLaW, Metis, and Discrete-WAM policy mode.

### 6.6 Endpoint versus physical horizon

Result: one predicted future endpoint is `W3`; an ordered modelled physical future is `W4`. Verified by W4D/WorldDrive versus WoTE.

### 6.7 Semantic decision token versus candidate bank

Result: independently meaningful decision→action is `RH`; a vocabulary of decision labels is not automatically `RB`. Verified by Discrete-WAM policy mode.

### 6.8 Paper/code mismatch

Result: when deployment topology changes, signatures split. SeerDrive paper/code is the positive case; DriveLaW paper/code remains merged at the human layer because topology does not change.

Verdict: **PASS**.

## 7. Implementation-invariance test

The following substitutions must not change the human signature when semantic interfaces are preserved:

| Substitution | Expected result |
|---|---|
| RGB ↔ BEV ↔ latent ↔ token | unchanged |
| Transformer ↔ DiT ↔ MLP | unchanged |
| regression ↔ diffusion ↔ flow for the same semantic output | unchanged |
| 6 candidates ↔ 32 candidates | unchanged if `RB` identity/resolver topology remains |
| 5 solver steps ↔ 10 solver steps | unchanged |
| direct endpoint predictor ↔ lightweight surrogate endpoint predictor | W unchanged; L changes only if teacher→surrogate learning is introduced |
| scalar versus vector head | E unchanged unless target semantics/composition changes |

Changes that must alter the signature:

| Mechanism change | Required signature change |
|---|---|
| remove online future predictor but retain trained scorer | `W3/W4 → W0`; R may remain `RB` |
| endpoint → recurrent physical future sequence | `W3 → W4` |
| candidate resolver → direct action | `RB → R0` |
| one-pass candidate evaluation → action/world reciprocal revision | `RB → RR` |
| factual-future agreement → planning utility | `EW → EV` |
| independent policy/world heads → one joint world–action sequence | R/W and L change to `RJ+W5`, `LQ` |

Verdict: **PASS**.

## 8. Version and lifecycle test

| Required case | Projection behavior | Result |
|---|---|---|
| SeerDrive paper/code | split `RR` versus `RB` | PASS |
| DriveLaW paper/code | same human route, audit discrepancies retained | PASS |
| Epona plan/self/external | `R0+W0` versus `RG{self/external}+W4` | PASS |
| Drive-JEPA PF/PB1/PB2 | direct versus candidate modes and criterion composition split | PASS |
| Discrete-WAM policy/world/joint | `RH`, `RG`, and `RJ` separated | PASS |
| training-only future | projected to `W0`, not online W | PASS |

Verdict: **PASS**.

## 9. DA-WAM retrospective stress projection

DA-WAM was blind to the audit ontology but is not blind to this later human compression layer. It is therefore a retrospective stress case, not a new blind-test claim.

Projection:

```text
DAWAM-PLAN-PAPER
= RB + W3 + (ED→EV)
  ⊕ L[LP → joint(LA/LN,LC)
       → retain{candidate predictor,scorer}/drop{EMA target,factual future input}]
```

Reconstruction:

```text
candidate bank
→ one future endpoint latent per candidate
→ decomposed driving outcomes
→ holistic utility
→ common argmax
```

Nearest human routes:

- World4Drive shares `RB+W3` but differs `EW` versus `ED→EV`;
- WorldDrive shares `RB+W3+EV` but differs direct retained predictor versus teacher-surrogate `LT` route;
- WoTE shares decomposed outcome evaluation but differs `W3` endpoint versus `W4` horizon.

No new R, W, E, or L category is required.

Verdict: **PASS as retrospective stress**, not an independent validation of the compression layer.

## 10. Information-loss audit

### 10.1 X is mostly hidden

Candidate preservation is implied by `RB/RR` and checked below. Stage-specific factual/predicted control remains in the audit. Self versus external control is promoted only for `RG` because it defines distinct generation modes.

Risk: readers cannot reconstruct WorldDrive's pretrain-X1 versus FAR-X3 transition from the human signature alone.

Mitigation: L retains teacher/surrogate stages and the row links back to the complete X record.

### 10.2 Supporting carriers are hidden

World4Drive and WoTE project to their decisive future consequence (`W3/W4`) while supporting current structured states remain in C.

Risk: the route map may understate the physical/current-state model.

Mitigation: W is explicitly named “primary online world role,” not the complete carrier inventory.

### 10.3 Solver and cross-cycle clocks are hidden

`Ts` is normally implementation-level for this route map. `Tc` remains audit-level unless it changes E semantics, as in Drive-JEPA PB2 comfort recalibration.

Risk: two systems with very different latency or temporal memory may share a route signature.

Mitigation: deployment engineering comparison must consult T; route equivalence is not runtime-cost equivalence.

### 10.4 L remains the densest field

Learning cannot be safely reduced to one value without recreating known collisions such as LAW/Epona and losing WorldDrive's ordered `LP→joint(LT,LC)` program.

Risk: the four-field signature still looks asymmetrical.

Mitigation: use only the macro route and deployment fate in the headline; keep the canonical learning DAG below it.

### 10.5 Unknown commitment is visible but not explanatory

`RU+E?` correctly prevents false certainty for GraphWorld, but it cannot explain the missing final resolver.

Mitigation: treat it as a research task and evidence gap, not a stable mechanism class.

Verdict: information loss is explicit and recoverable through the audit layer. No identified loss makes a current one-sentence reconstruction materially false.

## 11. First-six human acceptance sheet

| Artifact | Proposed signature | Reviewer decision | Key question |
|---|---|---|---|
| LAW-PF | `R0+W0+E0 ⊕ LA/drop` | PENDING | Does this correctly say future is a training mechanism, not an online route? |
| EPO-PLAN | `R0+W0+E0 ⊕ LS/bypass` | PENDING | Is LS versus LAW's LA a core learning distinction at the desired granularity? |
| DLAW-PAPER/CODE | `R0+W2+E0 ⊕ LG/retain` | PENDING | Does “future-generative internal state conditions direct action” capture the paper idea? |
| W4D-PLAN | `RB+W3+EW ⊕ LC/retain` | PENDING | Is factual-future latent agreement the correct resolver meaning? |
| WD-PLAN | `RB+W3+EV ⊕ LP→joint(LT,LC)` | PENDING | Does the signature preserve both teacher-surrogate alignment and PDMS preference? |
| WOTE-PLAN | `RB+W4+(EF+ED) ⊕ LC/retain` | PENDING | Is horizon rollout plus imitation/decomposed outcome evaluation the right core description? |

Acceptance choices should be:

```text
ACCEPT
REVISE CATEGORY
REVISE WORDING ONLY
NEED EVIDENCE
```

## 12. Overall verdict

```text
21-artifact coverage                  PASS
four-question compression             PASS
route-family reconstruction           PASS
counterexample handling               PASS
implementation invariance             PASS
version/mode/lifecycle handling        PASS
mechanical collision audit            PASS provisionally
first-six human acceptance             PENDING
independent unseen-paper blind test    PENDING
```

Decision:

```text
R–W–E ⊕ L internal projection = PASS
adopt as primary human route map = HOLD FOR HUMAN REVIEW
replace C–X–D–P–V–T–L = NO
S2 promotion implication = NONE
```

The next gate is human review of the six rows in §11. If accepted, the 12-paper headline map can become the primary explanatory view while the seven-field ontology remains the normative audit backend. A later unseen, source-available paper must then blind-test the human compression layer itself.
