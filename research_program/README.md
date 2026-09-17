# WAM + One-Stage Domain Ontology Research Program

Status: **ACTIVE**

Branch: `research/wam-domain-ontology`

Created: 2026-09-17

## Mission

Build a mechanism ontology for the **WAM + one-stage / end-to-end autonomous-driving domain**.

The ontology must be discovered and stress-tested from a large in-domain mechanism corpus, while the frozen 12-paper set remains the canonical explanation/regression benchmark.

The governing relation is:

```text
large WAM + one-stage domain corpus
    -> discover / challenge mechanism questions
    -> candidate ontology
    -> canonical-12 regression + explanation acceptance
    -> held-out in-domain blind test
    -> ontology promotion
```

External model-based RL, robotics, control, predictive-state, and general world-model literature is **theory support only**. It may provide conceptual foundations, terminology, or counterexample inspiration, but it does not vote directly on the final WAM + one-stage taxonomy.

## Evidence hierarchy

```text
Tier 1 — DOMAIN EVIDENCE
WAM + one-stage / end-to-end driving papers and artifacts.
This tier determines whether an axis/class exists and whether the ontology covers the field.

Tier 2 — ADJACENT DRIVING EVIDENCE
Strong non-WM planners, interactive prediction/planning, simulators, benchmarks.
This tier defines boundaries and controls alternative explanations.

Tier 3 — THEORY SUPPORT
MBRL, POMDP/belief state, predictive-state, robotics world models, general world models.
This tier supplies theory, vocabulary, and possible counterexample ideas only.
```

## Canonical 12 policy

The existing 12-paper set remains frozen as the **canonical core mechanism benchmark**.

It has three roles:

1. `REGRESSION`: any ontology revision must preserve all scientifically important distinctions already established in the 12-paper audit.
2. `EXPLANATION`: every major human-facing axis/class should be explainable using concrete canonical-12 mechanisms whenever the set contains a suitable example.
3. `ACCEPTANCE`: if an axis can classify papers but cannot be explained cleanly through concrete mechanisms, it is not ready for human-layer promotion.

The canonical 12 are not assumed to exhaust the domain. If the large corpus reveals an important mechanism absent from all 12, add an `extension anchor`; do not silently replace the canonical set.

Protected historical ontology paths:

```text
outputs/core_mechanism_12_v1/
handoff/core_mechanism_12/
```

Do not modify these during corpus construction or candidate-axis discovery.

## Human / agent division of labor

### ChatGPT research lead

Responsible for:

```text
scope and evidence policy
paper-batch selection strategy
mechanism-axis auditing
collision / counterexample interpretation
ontology KEEP/MODIFY/SPLIT/MERGE/DELETE decisions
canonical-12 regression review
human explanation / acceptance
final ontology promotion recommendation
```

### Codex research engineer

Responsible for:

```text
breadth census
metadata normalization
ontology-free mechanism extraction
paper/code tracing
artifact enumeration
mechanical consistency checks
contrast matrices
source/evidence collection
batch reports
```

Codex must not independently promote or rewrite the ontology unless a task explicitly authorizes projection or revision.

## Shared-memory rule

GitHub is the source of truth. Chat history is not.

Every substantial batch must leave:

```text
input task brief
source/evidence records
output files
commit SHA
batch report
review verdict
```

A fresh session should be able to recover the research state from the repository alone.

## Branch discipline

Canonical research branch:

```text
research/wam-domain-ontology
```

Recommended Codex branches:

```text
codex/domain-census-d01
codex/domain-census-d02
codex/deepread-w01
codex/deepread-r01
codex/codeaudit-<paper>
```

Codex should commit to its task branch and report the SHA. The research lead reviews the diff before accepted evidence is merged or copied into the canonical research branch.

## Program files

```text
MASTER_PLAN.md
CODEX_EXECUTION_PROTOCOL.md
ONTOLOGY_FREE_CARD_V2.md
TASK_BOARD.md
codex_tasks/
reviews/
decisions/
```

## Current immediate objective

Run `D01_DOMAIN_CENSUS.md` to validate the collaboration protocol on a bounded in-domain batch before scaling to the full 80–120-paper corpus.
