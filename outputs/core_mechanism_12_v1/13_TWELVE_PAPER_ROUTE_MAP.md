# Core Mechanism 12 — Twelve-Paper Human Route Map

Status: complete provisional projection of the 12-paper corpus into the human route signature defined in `12_HUMAN_ROUTE_SIGNATURE_PROPOSAL.md`.

Normative evidence remains in `03_TWENTY_ONE_ARTIFACT_PROJECTIONS.md` and `09_ONTOLOGY_SPEC_S1_PLUS.md`. This file is a presentation and comparison layer.

## 1. Reading the map

```text
R = output formation/commitment route
W = primary online world role
E = semantic resolver criterion
L = directed learning route and deployment fate
```

Compact form:

```text
Artifact = R + W + E ⊕ L[...]
```

Core codes used here:

```text
R0 direct action
RH semantic decision→action
RB candidate bank→resolver
RR reciprocal world↔policy refinement
RJ joint world–action generation
RG world/consequence generation output
RU unresolved final commitment

W0 no online world carrier
W1 current structured world
W2 future-generative internal state
W3 future endpoint consequence
W4 future-horizon consequence
W5 joint world–action carrier

E0 no resolver criterion
EF expert/factual behavior compatibility
EV holistic planning utility/preference
ED decomposed driving outcomes
EW world/future agreement
EY dynamics/physical validity
E? unresolved resolver/criterion
```

## 2. Twelve-paper headline map

A paper is not forced into one signature when its paper/code versions or deployed modes differ materially.

| Paper | Headline human route | One-sentence mechanism |
|---|---|---|
| LAW | `R0 + W0 + E0 ⊕ LA/drop-future` | Direct policy; predicted action is trained through a future-latent loss, but the future branch is removed at deployment. |
| Epona | planning: `R0 + W0 + E0 ⊕ LS/bypass-visual`; rollout: `RG + W4 + E0` | Planning is direct and does not consume generated future; the same system separately supports self-controlled or externally controlled world rollout. |
| DriveLaW | `R0 + W2 + E0 ⊕ LG/retain-trunk` | A future-generative internal state remains online and conditions direct action generation. |
| World4Drive | `RB + W3 + EW ⊕ joint(LC,LA?)/retain` | Candidate endpoint futures are resolved by agreement with the factual future latent. |
| WorldDrive | `RB + W3 + EV ⊕ LP→joint(LT,LC)/surrogate` | A heavy future teacher is compressed into an online candidate-future surrogate that ranks candidates by planning preference. |
| WoTE | `RB + W4 + (EF+ED) ⊕ joint(LC,world)/retain` | Candidate-specific future horizons are evaluated by imitation and decomposed planning outcomes. |
| SeerDrive | paper: `RR + W3 + E?`; code: `RB + W3 + (EF+ED)` | The paper proposes reciprocal world–policy refinement; the released code instead performs candidate-future evaluation followed by non-rescored refinement. |
| Drive-JEPA | PF: `R0 + W0 + E0 ⊕ LP`; PB: `RB + W0 + EV/EV+ED ⊕ LP→LC` | Predictive representation learning transfers into planning; PB modes use a candidate scorer without retaining an online future predictor. |
| Metis | `R0 + W0 + E0 ⊕ LA/bypass-video` | Predicted actions condition a train-time video branch whose loss shapes the action path; the video expert is bypassed at deployment. |
| DynFlowDrive | `RB + W0 + (EW+EF+EY) ⊕ LC/drop-world` | A train-time world-flow criterion selects supervision for a deployed candidate scorer; the world model is removed online. |
| Discrete-WAM | policy: `RH + W0 + E0 ⊕ LQ→LR`; joint: `RJ + W5 + E0 ⊕ LQ` | The primary policy uses a semantic decision token before action editing; separate modes generate worlds or jointly edit world–action tokens. |
| GraphWorld | `RU + W1 + E? ⊕ LS→LN/retain-current-world` | A temporally grounded structured current-world state modulates planning, but final multimodal commitment remains unresolved. |

## 3. Complete 21-artifact projection

| Artifact | Human route signature | Plain-language reconstruction | Confidence boundary |
|---|---|---|---|
| LAW-PF | `R0 + W0 + E0 ⊕ L[LA→drop{future}]` | Direct PF planning with action-mediated future regularization only during training. | HIGH for inspected PF source |
| LAW-PB | `R0 + W0 + E0 ⊕ L[LA→drop{future}]` | Same functional route in the paper PB mode; perception stages differ below this layer. | MEDIUM; implementation/gradient details bounded |
| EPO-PLAN | `R0 + W0 + E0 ⊕ L[LS+detached-chain→bypass{visual}]` | Direct planning from the learned state; future visual generation is training-side for this mode. | HIGH |
| EPO-SELF | `RG{control=self} + W4 + E0 ⊕ L[LS+detached-chain→retain{rollout}]` | Policy-predicted motion drives a generated future horizon whose output is the mode result. | HIGH |
| EPO-CTRL | `RG{control=external} + W4 + E0 ⊕ L[LS+detached-chain→retain{rollout}]` | Supplied pose/yaw drives an externally controlled future horizon. | HIGH |
| DLAW-PAPER | `R0 + W2 + E0 ⊕ L[LG→retain{generative trunk,action head}]` | Internal Video-DiT future-generation state conditions direct trajectory generation. | HIGH |
| DLAW-CODE | `R0 + W2 + E0 ⊕ L[LG→retain{generative trunk,action head}]` | Same functional route as the paper; solver-count/config differences remain audit attributes. | HIGH topology; numeric setting bounded |
| W4D-PLAN | `RB + W3 + EW ⊕ L[joint(LC[EW],LA?)→retain{future path,scorer}]` | Six candidate futures reach one resolver trained by factual-future latent agreement. | MEDIUM-HIGH; action-gradient reach partly UNKNOWN |
| WD-PLAN | `RB + W3 + EV ⊕ L[LP→joint(LT,LC)→retain{surrogate,scorer}/drop{teacher generator}]` | Candidate endpoint consequences are represented by a distilled surrogate and ranked by holistic planning preference. | HIGH |
| WOTE-PLAN | `RB + W4 + (EF+ED) ⊕ L[joint(LC,world losses)→retain{rollout,reward,resolver}]` | Each candidate has a recurrent future horizon scored by imitation and decomposed outcomes. | HIGH topology; exact reward formula bounded |
| SEER-PAPER | `RR + W3 + E? ⊕ L[joint(LA,world losses)→retain{reciprocal path}]` | Candidate/action state and future endpoint repeatedly refine one another before a final commitment whose resolver is not established. | MEDIUM; final resolver UNKNOWN |
| SEER-CODE | `RB + W3 + (EF+ED) ⊕ L[joint(LC,world losses)→retain{evaluator,resolver,refiner}]` | Candidate endpoint futures are scored once; the selected index is then refined without rescore. | HIGH |
| DJEPA-PF | `R0 + W0 + E0 ⊕ L[LP→retain{encoder,planner}/drop{predictor,target}]` | Predictive video pretraining transfers an encoder into a direct policy; no future predictor remains online. | HIGH |
| DJEPA-PB1 | `RB + W0 + EV ⊕ L[LP→LC→retain{proposal,scorer}/drop{predictor,target}]` | A candidate bank is resolved by learned planning utility without an online world consequence carrier. | HIGH |
| DJEPA-PB2 | `RB + W0 + weighted(EV,ED) ⊕ L[LP→LC→retain{proposal,scorer}/drop{predictor,target}]` | PB1 plus previous-cycle comfort recalibration; the cross-cycle clock remains an audit field. | HIGH; previous-reference provenance bounded |
| METIS-PLAN | `R0 + W0 + E0 ⊕ L[LA→retain{action path}/bypass{video expert}]` | Action-conditioned video loss shapes the direct policy, while online execution is action-only. | MEDIUM; no executable source |
| DFD-PLAN | `RB + W0 + (EW+EF+EY) ⊕ L[LC→retain{proposal,scorer}/drop{world flow}]` | A hybrid future/expert/dynamics criterion trains the deployed candidate scorer; online world flow is absent. | MEDIUM; composition and gradient scope UNKNOWN |
| DWAM-POLICY | `RH + W0 + E0 ⊕ L[LQ→LR→retain{decision,action path}/bypass{visual generation}]` | A semantic path×speed decision token conditions iterative action-token editing. | MEDIUM; paper-only |
| DWAM-WORLD | `RG{control=external} + W4 + E0 ⊕ L[LQ/world pretrain→retain{visual generator}]` | A supplied action sequence controls future visual-token generation. | MEDIUM; paper-only |
| DWAM-JOINT | `RJ + W5 + E0 ⊕ L[LQ→retain{joint token model}]` | One interleaved process jointly edits/generates action and world tokens. | MEDIUM; headline deployment use UNKNOWN |
| GW-PLAN | `RU + W1 + E? ⊕ L[LS→LN→retain{current-world path}/drop{future target}]` | A structured current-world state is temporally grounded and consumed by planning, but final mode commitment is unresolved. | MEDIUM; paper-only and resolver UNKNOWN |

## 4. Route families exposed by the compression

### F1 — Direct policy with train-time world learning only

```text
R0 + W0 + E0
```

Members:

- LAW: action-mediated future supervision (`LA`);
- Epona planning: shared-state sibling world learning (`LS`);
- Drive-JEPA PF: predictive representation transfer (`LP`);
- Metis: action-mediated video supervision (`LA`).

The shared deployment statement is simple: no qualifying online future/world carrier lies on the final action path. L explains why these papers are not all the same learning mechanism.

### F2 — Direct action conditioned by an online world carrier

```text
R0 + W1/W2 + E0
```

- DriveLaW: `W2`, a future-generative internal state;
- GraphWorld is nearby with `W1`, but remains `RU` because final commitment is unresolved.

### F3 — Candidate resolver without an online consequence carrier

```text
RB + W0 + E...
```

- Drive-JEPA PB1/PB2;
- DynFlowDrive.

This family is important because it proves that a candidate resolver can preserve world-derived knowledge in its scorer while dropping the world model itself.

### F4 — Online candidate-consequence planning

```text
RB + W3/W4 + E...
```

- World4Drive: endpoint + world agreement (`EW`);
- WorldDrive: endpoint + planning preference (`EV`);
- WoTE: horizon + factual/decomposed outcomes (`EF+ED`);
- SeerDrive code: endpoint + factual/decomposed outcomes;
- DA-WAM blind test, outside the 12-paper derivation set: endpoint + `ED→EV`.

### F5 — Reciprocal world–policy decision

```text
RR + W3 + E?
```

- SeerDrive paper.

The distinguishing mechanism is not extra neural-network depth. A predicted consequence revises the action, which produces another consequence within the same decision.

### F6 — Semantic hierarchy before action

```text
RH + W0 + E0
```

- Discrete-WAM policy mode.

The path×speed token is an independently meaningful decision, not an implicit hidden layer or a runtime candidate bank.

### F7 — World-generation and joint-generation capabilities

```text
RG + W4 + E0
RJ + W5 + E0
```

- Epona self/external rollout;
- Discrete-WAM world generation;
- Discrete-WAM joint world–action generation.

These are kept separate from planning signatures because their terminal outputs and commitment tasks differ.

## 5. First-six human comparison

The first six now reduce to three immediately visible deployment trunks:

```text
LAW / Epona
direct planning
+ no online world carrier
+ world knowledge enters through training

DriveLaW
direct planning
+ online future-generative internal state

World4Drive / WorldDrive / WoTE
candidate bank
+ candidate-specific online consequence
+ common resolver
```

Their decisive splits are:

| Pair/group | Same | Different |
|---|---|---|
| LAW vs Epona | `R0+W0+E0` | `LA` action-mediated future loss vs `LS` sibling shared-state learning |
| LAW vs Metis | complete human family | same functional action→future-loss→action route; latent versus video-expert realization is below this layer |
| LAW/Epona vs DriveLaW | direct output | `W0` versus online `W2` |
| W4D/WD/WoTE | `RB` candidate commitment | `W3/W4`, `EW/EV/(EF+ED)`, and different L programs |
| World4Drive vs WorldDrive | endpoint candidates | factual-future agreement versus planning preference; retained direct path versus teacher-surrogate route |
| WorldDrive vs WoTE | candidate consequence planning | endpoint utility surrogate versus recurrent horizon with decomposed outcomes |

## 6. Paper-level interpretation rules

1. A paper title may own several artifact signatures. Do not collapse Epona rollout into Epona planning, SeerDrive paper into code, or Drive-JEPA PF into PB.
2. Two artifacts with the same human signature are a proposed functional equivalence class, not proof of identical implementation or full DAG.
3. `W0` means no qualifying online world carrier, not “the model learned nothing about the world.” L may still contain strong predictive, generative, or simulator-derived learning.
4. `E0` means no separate runtime resolver criterion. It does not mean there is no trajectory loss.
5. `E?` and `RU` are visible scientific boundaries, not placeholders to be silently completed from another version.

## 7. Human-review questions

For every headline row, reviewers should answer:

1. Does the one-sentence mechanism match what the paper is trying to contribute?
2. If two papers share the signature, are their remaining differences implementation choices at the chosen research granularity?
3. If two papers differ, does the changed code correspond to a genuinely different causal or learning mechanism?
4. Is any decisive online future use hidden behind `W0`?
5. Is any random sample or proposal refinement incorrectly promoted to `RB`?
6. Does E describe the target semantics rather than the loss function or head shape?
7. Does L state whether the world branch is retained, dropped, bypassed, or distilled?

The map remains provisional until this human review is accepted.
