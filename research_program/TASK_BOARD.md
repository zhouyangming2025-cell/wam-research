# TASK BOARD — WAM + One-Stage Domain Ontology

Status: **ACTIVE**

## Governance

Task states:

```text
PLANNED
READY
IN_PROGRESS
SUBMITTED
UNDER_REVIEW
ACCEPTED
REVISE
REJECTED
BLOCKED
```

Only `ACCEPTED` evidence is treated as canonical research state.

## Current board

| Task | State | Executor | Purpose | Output branch/path | Review owner |
|---|---|---|---|---|---|
| D01 Domain Census Pilot | READY | Codex | Validate scope, artifact splitting, ontology-free extraction on first in-domain batch | `codex/domain-census-d01` | ChatGPT research lead |
| D01 Review | PLANNED | ChatGPT | Audit D01 scope/evidence quality and revise protocol if needed | `research_program/reviews/D01_REVIEW.md` | User + ChatGPT |
| D02 Domain Census Scale-1 | BLOCKED | Codex | Expand after D01 protocol passes | TBD | ChatGPT |
| D03 Domain Census Scale-2 | BLOCKED | Codex | Expand toward mechanism saturation | TBD | ChatGPT |
| H01 Holdout Freeze | PLANNED | ChatGPT/Codex | Reserve 15–25 in-domain papers before axis finalization | `research_program/holdout/` | User + ChatGPT |
| W01 W Mechanism Deep-Read Wave | BLOCKED | Codex | 15–20 W-focused in-domain deep reads after census normalization | `codex/deepread-w01` | ChatGPT |
| W-AUDIT | BLOCKED | ChatGPT | Necessity/orthogonality/coverage/collision/invariance audit of W | `research_program/decisions/W_AXIS_AUDIT.md` | User |
| R01 R Mechanism Deep-Read Wave | BLOCKED | Codex | Action formation/search/commitment evidence wave | `codex/deepread-r01` | ChatGPT |
| R-AUDIT | BLOCKED | ChatGPT | Audit R and possible factorization/search gap | `research_program/decisions/R_AXIS_AUDIT.md` | User |
| E-AUDIT | BLOCKED | ChatGPT | Audit evaluator/objective semantics | TBD | User |
| L-AUDIT | BLOCKED | ChatGPT | Audit learning-to-deployment program | TBD | User |
| X-AXES | BLOCKED | ChatGPT/Codex | Test interaction/reactivity, uncertainty, search as independent questions | TBD | User |
| C12 Regression | BLOCKED | ChatGPT | Reproject frozen canonical 12 under candidate ontology | TBD | User |
| Blind Holdout | BLOCKED | Codex + ChatGPT | Execute frozen in-domain blind test without ontology edits | TBD | User |
| Ontology V2 Candidate | BLOCKED | ChatGPT | Final KEEP/MODIFY/SPLIT/MERGE/DELETE/ADD verdict | TBD | User |

## Immediate next action

Run:

```text
research_program/codex_tasks/D01_DOMAIN_CENSUS.md
```

Codex must create a task branch from:

```text
research/wam-domain-ontology
```

Recommended branch:

```text
codex/domain-census-d01
```

After completion, return only:

```text
branch
commit SHA
brief summary
unresolved issues
```

The research lead will inspect the repository diff directly.

## Protected paths during D01

Codex must not change:

```text
outputs/core_mechanism_12_v1/
handoff/core_mechanism_12/
research_program/MASTER_PLAN.md
research_program/CODEX_EXECUTION_PROTOCOL.md
research_program/ONTOLOGY_FREE_CARD_V2.md
```

unless D01 explicitly requests a proposed patch in a separate suggestion file.

## Canonical 12 status

The frozen 12-paper mechanism set remains:

```text
canonical core
regression suite
explanation/teaching suite
```

It is not the breadth corpus and must not be silently replaced by newer papers.

## Acceptance rule for scaling

D02 remains blocked until D01 demonstrates:

```text
scope precision is acceptable
artifact splitting is consistent
evidence labels are honest
ontology codes did not leak into extraction
runtime vs training roles are separated
boundary/non-WM papers are not counted as Tier-1 votes
repository output is reviewable and non-duplicative
```
