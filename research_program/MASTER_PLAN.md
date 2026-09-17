# MASTER PLAN — WAM + One-Stage Mechanism Ontology

Status: **ACTIVE EXECUTION PLAN**

## 0. Research objective

Build a mechanism ontology for **world-model-assisted one-stage / end-to-end autonomous driving** that is:

```text
domain-grounded
mechanism-level
implementation-invariant
causally interpretable
broadly covering
counterexample-resistant
human-explainable
```

The large domain corpus determines scientific coverage. The frozen canonical 12 provide deep regression and explanation acceptance. External theory literature only supports concepts and boundary reasoning.

## 1. Completion target

Target evidence base:

```text
80–120 in-domain papers at census depth
~150–220 mechanism artifacts after mode/version splitting
40–60 RD3 mechanism deep reads
15–25 RD4 paper+code audits
12 canonical-core papers/artifacts retained as regression/explanation suite
15–25 in-domain held-out papers for blind testing
```

These numbers are targets, not quotas. Saturation and mechanism diversity matter more than raw count.

## 2. Phase structure

### Phase 0 — protocol freeze

Outputs:

```text
scope boundary
evidence hierarchy
artifact unit rule
reading-depth rule
ontology-free extraction schema
branch/review workflow
```

Exit condition: Codex and ChatGPT can independently apply the same inclusion/extraction protocol to a pilot batch without material ambiguity.

### Phase 1 — in-domain breadth census

Goal: reconstruct the WAM + one-stage design space without projecting R/W/E/L.

For every paper/artifact record:

```text
paper/version/mode
one-stage planning relevance
world/predictive mechanism
training-only vs deployment-time role
planning interface
action formation / candidate / search topology
criterion/value interface
learning-to-deployment fate
evaluation regime
source confidence
```

No ontology code is assigned.

Exit condition: successive batches add few or no new first-order mechanism patterns and all major field families are represented.

### Phase 2 — mechanism deep reads

Select 40–60 mechanism-diverse papers for RD3, with 15–25 RD4 code audits.

Selection favors mechanism boundary cases, not citation count.

Priority contrasts include:

```text
training-only world supervision vs runtime world use
current model state vs predictive internal state vs explicit future consequence
single future endpoint vs horizon/rollout
candidate consequence vs direct score
heavy world generator vs distilled future surrogate
world-derived scorer vs explicit future object
joint world-action vs sequential coupling
paper vs code topology divergence
search/MPC/iterative optimization if present in-domain
reactive/counterfactual world response if present in-domain
```

Exit condition: each recurring mechanism family has at least one high-depth anchor and key boundary cases have primary-source evidence.

### Phase 3 — ontology-free recurring-question induction

Temporarily ignore R/W/E/L labels.

Across the mechanism ledgers, ask which independent questions repeatedly separate artifacts.

Candidate questions must emerge from repeated domain evidence, not architecture names.

For each candidate question record:

```text
what information it preserves
what deletion would collapse
which papers force it to exist
which other candidate axes may duplicate it
what substitutions should leave it invariant
```

Exit condition: a finite set of candidate mechanism questions is proposed with evidence maps and known counterexamples.

### Phase 4 — axis-by-axis deep audit

Audit current and newly proposed axes independently.

Required tests:

1. `NECESSITY` — deleting the axis merges important mechanisms.
2. `ORTHOGONALITY` — the axis is not duplicating another question.
3. `COVERAGE` — in-domain artifacts classify without proliferating exceptions.
4. `COLLISION` — mechanically distinct systems do not collapse incorrectly.
5. `INVARIANCE` — implementation substitutions do not spuriously change class.
6. `DELETION TEST` — removing the claimed distinguishing component changes the mechanism in the predicted way.
7. `HUMAN INTERPRETABILITY` — the distinction can be explained concretely.

Initial priority:

```text
1. W
2. R
3. E
4. L
5. test possible extra questions such as interaction/reactivity, uncertainty, search/optimization
```

No axis name has protected status.

Allowed verdicts:

```text
KEEP
MODIFY
SPLIT
MERGE
DELETE
ADD
UNRESOLVED
```

### Phase 5 — canonical-12 regression and explanation acceptance

Re-run the frozen 12-paper suite after every material ontology revision.

Required contrast checks include:

```text
LAW vs DriveLaW
LAW vs World4Drive
WorldDrive vs DynFlowDrive
World4Drive vs WoTE
Epona planning vs rollout modes
SeerDrive paper vs released code
Drive-JEPA PF vs PB modes
Discrete-WAM policy vs world vs joint
GraphWorld vs ordinary planning representations
```

A revision fails regression if it erases a primary-evidence mechanism distinction without an explicit justified merge.

Explanation acceptance:

- each major human-layer class should have a canonical-12 example when available;
- the mechanism difference must be teachable from architecture and causal path, not only code labels;
- inability to explain the axis cleanly is evidence the human layer may be badly factored.

### Phase 6 — in-domain blind holdout

Freeze 15–25 in-domain papers before ontology finalization.

Once candidate ontology is frozen:

```text
classify all holdout artifacts without changing the ontology
log unknowns/collisions
measure whether new top-level axes/classes are needed
only after the batch is complete may revisions be considered
```

A paper ceases to be blind if used at RD2+ during ontology design.

### Phase 7 — ontology verdict

Produce a new candidate version only after Phases 1–6.

Do not overwrite historical ontology files.

Required outputs:

```text
candidate backend mechanism ontology
human-facing compressed axes
mapping from backend -> human layer
canonical-12 projection
large-corpus projection statistics
blind-holdout failure report
known unresolved boundaries
revision history
```

### Phase 8 — human-layer reconstruction

Target human layer:

```text
roughly 3–6 primary questions
roughly 4–6 top-level classes per question where possible
```

This is a readability target, not a forced numerical rule.

The human layer must compress the backend without inventing unsupported distinctions or duplicating the same mechanism across axes.

## 3. Evidence tiers

### Tier 1 — domain evidence

Determines ontology existence/coverage.

In scope when world/predictive modeling materially affects one-stage planning/action/trajectory decision, training of the deployed planning mechanism, or a unified world-action mechanism.

### Tier 2 — adjacent driving evidence

Includes strong non-WM one-stage planners, interactive prediction/planning, simulators, benchmarks, reward/scorer controls.

Used for boundary tests and alternative explanations, not direct class-frequency evidence.

### Tier 3 — theory support

Includes MBRL, POMDP/belief states, predictive-state theory, robotics world models, general world models.

Used to test conceptual defensibility and inspire missing-mechanism searches. It cannot by itself create a WAM-domain class.

## 4. Reading depth

```text
RD0 metadata only
RD1 abstract/introduction screened
RD2 method/figures/core equations inspected
RD3 full mechanism reconstruction
RD4 RD3 + source/code verification of decision-critical topology
```

Major ontology claims should be anchored in RD2–RD4 domain evidence.

## 5. Unit of classification

Primary unit:

```text
Artifact = paper/code version × task/mode × planning/generation path
```

Split modes when deployment topology, action formation, world use, criterion, or retained components materially differ.

Do not split solely because of implementation substrate, sampling count, tensor shape, backbone family, or numerical hyperparameter.

## 6. Canonical 12 contract

The canonical 12 are frozen as deep mechanism anchors. They do not define domain completeness.

A new paper becomes an `extension anchor` only if it exposes an important stable mechanism absent from all canonical examples.

Do not replace canonical papers merely because a newer paper appears.

## 7. Research-agent governance

Codex may:

```text
collect
extract
trace
normalize
compare
lint
summarize evidence
```

Codex may not, unless explicitly authorized:

```text
change canonical ontology
invent new top-level axes
silently reinterpret protected 12-paper verdicts
upgrade evidence depth without actually reading required material
use survey statements as primary-paper facts
```

ChatGPT research lead reviews evidence and performs ontology-level adjudication.

## 8. Immediate execution sequence

```text
D01 pilot domain census
-> review D01
-> revise protocol if needed
-> D02–D04 scale census toward saturation
-> select W deep-read wave
-> W axis audit
-> R deep-read wave and audit
-> E audit
-> L audit
-> candidate-extra-axis tests
-> canonical-12 regression
-> blind holdout
-> ontology V2 candidate
```

## 9. Non-goals

This program is not trying to:

```text
build a taxonomy of all autonomous driving
build a taxonomy of all robotics/world models
rank papers by quality
prove the current R/W/E/L ontology correct
maximize paper count
replace deep reading with automated summaries
```

The objective is a defensible mechanism basis for WAM + one-stage autonomous driving.