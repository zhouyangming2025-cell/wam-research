# LAW / Epona / DriveLaW Pilot: Protocol and Freeze

Status: `PILOT-SETUP-FROZEN`

Date: 2026-09-18

Working branch: `codex/pilot-quarantine-law-epona-drivelaw`

Baseline commit: `368c9a848e241bfb7bf2e2d61242269d5e438af6`

This is a process boundary for a three-paper pilot. It is not a new ontology, route map, or scientific verdict.

## 1. Scope

The pilot is limited to these canonical paper records:

| ID | Paper | Raw source |
|---|---|---|
| P0048 | LAW | `papers/raw_md/P0048_LAW/P0048_LAW.raw.md` |
| P0001 | Epona | `papers/raw_md/P0001_Epona/P0001_Epona.raw.md` |
| P0009 | DriveLaW | `papers/raw_md/P0009_DriveLaW/P0009_DriveLaW.raw.md` |

The pilot does not expand the paper set, modify the existing ontology, reconcile the global 12-paper artifact count, or decide the final technical routes.

## 2. Evidence order

The order is mandatory:

1. Read and record the raw paper Markdown.
2. Read the pinned official source/code audit only for lifecycle and deployment facts that the paper cannot settle.
3. Produce a source-first record without route labels.
4. Reopen existing deep analyses, cards, route maps, ontology projections, and old synthesis documents only as adversarial material.
5. Record agreement, correction, split, or unresolved status at claim level.

Existing historical conclusions are never allowed to silently fill an `UNKNOWN` field.

## 3. Required records

Each paper receives one source-first record containing:

- author-stated problem and gap ledger;
- scoped mode/artifact boundary;
- current input and encoder output;
- future object and how it is constructed;
- action entry point;
- planner-consumed object at deployment;
- candidate identity and resolver status;
- training objective and deployment lifecycle;
- evidence label for every non-trivial claim;
- unresolved questions and evidence debt.

The cross-paper comparison is performed only after all three records exist. It compares functional obligations and lifecycle facts; it does not assign route names.

### 3.1 Five-question audit projection

For human review, the existing source-first facts are projected onto the frozen five-question frame. This projection is an audit view, not a new ontology, route taxonomy, matrix, or additional paper record. The Chinese brief is the review entry point; the source-first records remain the evidence-bearing records.

The relationship to the legacy fields is:

| Existing source-first field | Five-question coverage |
|---|---|
| Future object and how it is constructed | Q1: where future prediction happens; Q2: what future object is predicted |
| Action entry point; planner-consumed object at deployment | Q3: whether future information enters the forward action chain; Q5: what remains at deployment |
| Candidate identity and resolver status | Q3/Q4: whether future is used for candidate-specific consequence evaluation or selection |
| Training objective and deployment lifecycle | Q4: lifecycle/decision role; Q5: deployment residue |

Every Q1–Q5 answer must retain its evidence label, `UNKNOWN`, `NOT REPORTED`, and mode/version splits. The projection must not convert a training target into an online planner input, or a future-generation branch into candidate-consequence evaluation without candidate identity and resolver evidence.

## 4. Evidence labels

Use only these labels:

- `PAPER FACT`: directly stated or defined in the raw paper.
- `CODE FACT`: directly supported by the pinned official source audit.
- `AUTHOR CLAIM`: the authors' interpretation or claimed benefit, not independently accepted.
- `OUR INFERENCE`: a transparent interpretation derived from recorded facts.
- `UNKNOWN`: the available paper and pinned source do not settle it.
- `NOT REPORTED`: the paper does not report it.
- `NOT EVALUATED`: the paper reports no experiment that tests it.

## 5. Mode-splitting rule

Split a paper into multiple records only when the terminal output, deployment lifecycle, or decision role materially changes. Do not split for an optimizer, backbone, loss weight, or ordinary implementation variant.

The pilot must explicitly preserve paper/code/version differences. A paper-level description and a code-level deployment path may coexist without being forced into one statement.

## 6. Prohibited operations during the pilot

- no deletion, renaming, or rewriting of historical documents;
- no new route category, ontology axis, modifier, or matrix;
- no use of a historical route label as an input field;
- no conversion of `UNKNOWN` into absence or presence;
- no claim that action conditioning proves causal or counterfactual validity;
- no claim that multi-step generation proves a reactive closed loop;
- no claim that a generated future is an evaluated consequence unless candidate identity and resolver evidence exist.

## 7. Stop conditions

Pause and record a protocol failure if:

1. a conclusion can only be obtained by importing an old ontology label;
2. the raw paper and source audit refer to materially different modes or versions;
3. a document-level judgment is being made even though its individual claims differ in evidence status;
4. a candidate, future object, or terminal output cannot be identified;
5. the comparison requires a scalar ranking of representation richness, generation quality, or planning usefulness without a matched experiment;
6. the record would need to replace `UNKNOWN` with a guessed value.

## 8. Pilot acceptance gate

The pilot is successful only if a reviewer can trace every important comparison back to a raw-paper section or a pinned source fact, and if the three records can be compared without a route taxonomy. Only after this gate may a later phase ask whether stable cross-paper mechanism structure exists.
