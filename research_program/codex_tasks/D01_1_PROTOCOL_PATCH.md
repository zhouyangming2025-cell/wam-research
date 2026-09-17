# D01.1 — Protocol Patch: Lifecycle and World-Dependency Routing

Status: **READY FOR REVIEW**

Parent baseline: `codex/domain-census-d01`
Patch branch: `codex/domain-census-d01-1`

## Purpose

D01 established that scope and artifact granularity are workable, but it exposed a recurring ambiguity: the same paper-level phrase can refer to a deployed decision path, a training-only predictive branch, a transferred representation, a simulator, or a generation-only product. D01.1 adds a compact artifact-level routing layer before any large-corpus census.

This patch does not reclassify D01 and does not modify the 12-paper ontology outputs. It changes the reusable ontology-free card only and records the field semantics here.

## Added fields

Every RD2+ artifact record must contain exactly one value for each field.

### Field 1 — Runtime role

```text
runtime decision
training improvement
representation transfer
simulation
generation only
```

This separates what the artifact produces or improves from the paper's title and from the existence of a training branch.

### Field 2 — World dependency type

```text
none
training-only predictive
online predictive state
online rollout
candidate-conditioned consequence
joint generation
```

This distinguishes predictive representation transfer from an online state, a horizon rollout, candidate-indexed consequences, and coupled scene generation.

### Field 3 — Action commitment relation

```text
before world
after world
through world
independent
unknown
```

This records whether final action commitment occurs before, after, through, or independently of the separately traceable world operation. For simulation/generation-only artifacts, terminal-action relation is not applicable; the card keeps the controlled field for schema uniformity and explains that exception in prose.

## Single-value and split rules

1. Values are assigned per artifact/mode, not per paper title.
2. A paper with a planner, simulator, and generation path receives separate artifact records when terminal output or lifecycle differs.
3. `training-only predictive` must not be promoted to an online value merely because a prediction head exists in the training graph.
4. Direct action denoising, ordinary temporal encoding, and sampling do not create a world dependency without a separately traceable predictive/world object.
5. Candidate-conditioned consequence requires candidate identity to reach a common evaluator, optimizer, or commitment step.
6. Action commitment relation describes the operative role named by Field 1; Sections 8–9 remain authoritative for training/deployment residue.
7. If the source cannot resolve the relation, use `unknown`. Do not create compound values.

## Examples from the D01 pilot

| artifact pattern | runtime role | world dependency type | action commitment relation |
|---|---|---|---|
| action-only deployment after video co-training | training improvement | training-only predictive | independent |
| pretrained future geometry encoder used by a downstream planner | representation transfer | training-only predictive | independent |
| online future state fed to direct trajectory planning | runtime decision | online predictive state | after world |
| candidate trajectory rolled out and scored before commitment | runtime decision | candidate-conditioned consequence | after world |
| latent dynamics used to train an actor, then removed at deployment | training improvement | online rollout | through world |
| reactive renderer hosting an external policy | simulation | joint generation | unknown |
| multi-agent future generator with no final action mode | generation only | joint generation | unknown |

These examples are routing illustrations, not new classifications of the D01 outputs. The D01 artifacts remain frozen evidence and are not backfilled by this patch.

## D02 entry gate

D02 may begin only after review of this patch confirms:

- each artifact has one role, one world-dependency value, and one commitment relation;
- training-time and deployment-time descriptions remain separate;
- representation transfer is not silently counted as online world use;
- simulator/generation-only products are not counted as deployed planners;
- a new paper can be routed without adding a paper-specific category;
- unresolved cases are retained as `unknown` plus source evidence.

## Protected paths

D01.1 does not modify:

- `research_program/domain_corpus/d01/`;
- `outputs/core_mechanism_12_v1/`;
- `handoff/core_mechanism_12/`;
- existing 12-paper ontology projections;
- master ontology outputs or paper evidence.
