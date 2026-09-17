# Canonical-12 Minimal Mechanism Routes
Status: **provisional route synthesis from neutral records; not a normative ontology and not a replacement for the existing audit backend**.

The goal is not to produce one unique code for every paper. The goal is to identify the smallest set of recurring causal programs that survive the deletion and collision tests. A route family can contain mechanism subbranches; a subbranch is promoted only when it changes the indispensable bridge, not merely the substrate or the resolver's vocabulary.

## 1. Route-family decision rule

Separate two questions:

```text
Deployment bridge:
What computation reaches the final action commitment?

Learning bridge:
What world/predictive computation changes the deployed planner during training?
```

The same deployment family may contain different learning programs. Conversely, the same learning idea may attach to direct action, a candidate resolver, or a hierarchical policy. This is why a flat “one paper = one route” map is unsafe.

## 2. Minimal recurring planning programs

### Route A — direct action after world knowledge is compiled into the policy

```text
context/history → action or trajectory
```

There is no identity-preserved candidate bank and no online candidate-specific world consequence needed for the final action. The world/predictive branch may be central during training, but its influence reaches action through learned parameters or shared representation.

**Canonical artifacts:** LAW-PLAN-PF, LAW-PLAN-PB, EPONA-PLAN, DRIVEJEPA-PF, METIS-PLAN.

**Important subbranches, not automatic top-level splits:**

- action-conditioned latent future supervision (LAW);
- parallel shared temporal world/action learning (Epona);
- scalable predictive pretraining followed by transfer (Drive-JEPA PF);
- asymmetric world/action co-training with action-only inference (Metis).

These subbranches are scientifically different learning programs. They are not five different final decision topologies.

### Route B — retained online world state or generator state directly conditions action

```text
context/history → online world-derived state → action/trajectory
```

No candidate identity is carried through separate future consequences to a common resolver. The decisive difference from Route A is lifecycle: a semantically world-derived state/process remains on the action path at deployment.

**Canonical artifacts:** DRIVELAW-PLAN and GRAPHWORLD-PLAN.

**State-role subbranches:**

- DriveLaW: cached intermediate state of an online video generator's denoising process;
- GraphWorld: ego-centric relational current-world state with temporal/world-state refinement;
- a future-aware state may be online without being a physical-time rollout.

Whether these subbranches should later become separate field routes remains open. At the current sample size, the final commitment topology is the same, so they remain a controlled subbranch rather than a new top-level family.

### Route C — candidate-conditioned consequence evaluation with a retained common resolver

```text
context → {A_k}
       → {world/consequence O_k}
       → common resolver
       → A_k*
```

The candidate identity is born before the consequence computation, remains bound to its consequence, and reaches a common resolver that commits one candidate. This is the key route-level distinction from direct policy generation.

**Canonical artifacts:** WORLD4DRIVE-PLAN, WORLDDRIVE-PLAN, WOTE-PLAN.

**Mechanism subbranches:**

- World4Drive: intention-indexed future-latent plausibility/compatibility at an endpoint-like future interval;
- WorldDrive: candidate-specific lightweight future surrogate distilled from a heavier world generator;
- WoTE: recurrent candidate-conditioned BEV/action future sequence evaluated online.

The three should not be split merely because one calls the result a score, reward, or compatibility. They should not be merged into one identical mechanism either, because consequence construction, lifecycle, and physical-time expansion differ.

### Route D — candidate selection with world dynamics compiled into the deployed scorer

```text
training: {A_k} → world/dynamics criterion → preferred candidate → scorer learning
deployment: context → {A_k} → learned scorer → A_k*
```

Candidate identity and final resolver remain deployment mechanisms, but the world computation that created the selection criterion is removed from the online path.

**Canonical artifacts:** DRIVEJEPA-PB and DYNFLOWDRIVE-PLAN.

**Why this is not Route C:** both have candidate identity and a resolver, but Route C retains candidate-specific future information online. In Route D, world reasoning survives only through training labels, distillation, or parameter learning. The difference is not BEV versus latent or simulator versus flow; it is lifecycle and causal placement.

### Route E — reciprocal world/planning refinement within one decision

```text
current state → world estimate → plan
             ↖ refined plan/ego state
repeat → final commitment
```

The plan changes the world computation used to obtain the next plan within the same decision. This is stronger than one-way future-state conditioning and is not defined by iteration count alone.

**Canonical artifact:** SEERDRIVE-PAPER.

**Boundary:** SEERDRIVE-CODE must remain a separate artifact because the source audit reports a different deployed path. Its current reconstruction is closer to Route C but the exact re-scoring/refinement boundary is not fully closed.

### Route F — semantic decision formation followed by action generation

```text
context → semantic decision/skeleton → action/trajectory
```

The intermediate object has independent driving meaning, such as maneuver intent or a sparse decision skeleton. This is not the same as a candidate bank: the intermediate decision need not be individually evaluated by a common resolver.

**Canonical artifact:** DWAM-POLICY.

The unified world-policy and joint token tasks are learning/generation artifacts around this policy path. They do not automatically replace the policy route with a joint-world route.

## 3. Terminal capability, not an additional planning route

The following records are important but should not be counted as extra deployed planning routes unless a specific deployment mode consumes them for action commitment:

```text
EPONA-GEN
DWAM-WORLD
DWAM-JOINT
```

They are terminal world generation or joint world/action generation paths. A model may contain them and also contain a planning artifact. “Can generate a future world” is not equivalent to “uses candidate futures to choose the final action.”

## 4. Canonical projection table

| Paper / artifact | Minimal program | What makes it belong there | What must not be inferred |
|---|---|---|---|
| LAW-PF/PB | A | future prediction changes representation/action learning; direct deployment | no online candidate future |
| Epona-PLAN | A | parallel world/action heads share learned temporal context; planning can bypass video | no future-video resolver |
| Epona-GEN | terminal capability | video generation is the terminal output | not a planner route |
| DriveLaW-PLAN | B | online generator-internal states feed the action head | not candidate consequence selection |
| World4Drive | C | identity-preserved intention futures reach a selector | factual compatibility is not the whole route |
| WorldDrive | C | candidate-specific distilled future surrogate reaches reward resolver | heavy TA-DWM need not remain online |
| WoTE | C | recurrent candidate-specific BEV futures reach reward resolver | reward vocabulary alone defines the route |
| SeerDrive paper | E | future scene and refined plan feed each other within one decision | iteration count alone is not enough |
| SeerDrive code | C? | source audit reports a WoTE-like evaluation path | code does not prove the paper loop |
| Drive-JEPA PF | A | V-JEPA is pretraining/transfer; direct waypoint decoder | PF and PB are not same artifact |
| Drive-JEPA PB | D | candidates and scorer remain; simulator guidance is training-side | simulator is not an online world carrier |
| Metis | A | future video branch trains action expert but is bypassed at inference | future video does not condition deployed action |
| DynFlowDrive | D | world dynamics criterion trains scorer; world model dropped at inference | flow solver is not an online rollout |
| Discrete-WAM policy | F | semantic decision skeleton precedes action-token generation | joint training is not automatically a joint deployed output |
| Discrete-WAM world/joint | terminal capability | action-conditioned or interleaved world/action token generation | not the primary policy commitment route |
| GraphWorld | B | relational world state conditions planning; no explicit multistep scene rollout | final resolver is not proven |

## 5. Collision and false-split audit

### Expected compression

- LAW, Epona planning, Drive-JEPA PF, and Metis share the direct-deployment shell but remain separated by learning programs.
- World4Drive, WorldDrive, and WoTE share candidate identity plus common resolution but retain consequence/lifecycle subbranches.
- Drive-JEPA PB and DynFlowDrive share a compiled candidate-scorer family but retain distinct training criteria and source boundaries.

### Required separation

- SeerDrive paper vs code: different deployment loop.
- SeerDrive paper vs one-way future conditioning: reciprocal edge is indispensable.
- DriveLaW vs Epona: internal generator state consumed by action versus parallel shared temporal context.
- WoTE/WorldDrive vs DynFlowDrive: online consequence survives versus world criterion compiled away.
- Discrete-WAM policy vs joint/world tasks: semantic action formation versus generation/training tasks.
- GraphWorld vs explicit candidate-consequence routes: current relational world state without identity-preserved candidate futures.

### False-collision result

No pair above is forced into the same *complete mechanism statement* after artifact scope, lifecycle, candidate identity, and learning program are retained. Several pairs intentionally share a family-level deployment shell; that is functional compression, not a claim of identical DAGs.

## 6. Invariance and non-invariance tests

The following substitutions should leave the route family unchanged when semantic interfaces are preserved:

```text
regression ↔ diffusion ↔ flow for the same action interface;
RGB ↔ BEV ↔ latent ↔ token for the same world-object role;
Transformer ↔ DiT ↔ recurrent block;
expert compatibility ↔ scalar preference expression inside one common resolver.
```

The following changes must alter the route family or subbranch:

```text
training-only future → retained online future carrier;
direct output → identity-preserved candidate bank + common resolver;
one-way world→action → within-decision world↔policy feedback;
no semantic intermediate → semantic decision→action hierarchy;
online candidate consequence → world criterion removed and compiled into scorer.
```
