# D01.2 Existing Ontology Stabilization Regression

## 0. Decision status

This document freezes the D01.2 test before projection.

The task is a preservation-first regression of the existing mechanism ontology. It is not a redesign and it does not create a second taxonomy.

The final decision vocabulary is deliberately closed:

```text
PASS-STABLE
PASS-MINOR-PATCH
HOLD-STRUCTURAL-PRESSURE
FAIL-ABSTRACTION
```

The present run is limited to the 23 frozen D01 artifacts A01–A23. It does not start D02, enlarge the corpus, or alter any D01 artifact record.

## 1. Git and baseline freeze

```text
repository: zhouyangming2025-cell/wam-research
base branch: codex/domain-census-d01-1
base commit: 88da1cda4c58d107fea5176f4f28eff6c3fc4bfb
working branch: codex/ontology-stabilization-d01-2
```

Protected paths:

```text
outputs/core_mechanism_12_v1/
handoff/core_mechanism_12/
research_program/domain_corpus/d01/
```

No ontology file is modified in D01.2. No commit or push is authorized by this task.

## 2. Read-in protocol

The following were read before projection:

1. `handoff/D01_1_PROTOCOL_PAUSE_HANDOFF.md`
2. `handoff/core_mechanism_12/RESEARCH_PROTOCOL.md`
3. `outputs/core_mechanism_12_v1/05_ONTOLOGY_REVISION_VERDICT.md`
4. `outputs/core_mechanism_12_v1/09_ONTOLOGY_SPEC_S1_PLUS.md`
5. `outputs/core_mechanism_12_v1/12_HUMAN_ROUTE_SIGNATURE_PROPOSAL.md`
6. `outputs/core_mechanism_12_v1/13_TWELVE_PAPER_ROUTE_MAP.md`
7. `outputs/core_mechanism_12_v1/14_ROUTE_COMPRESSION_AND_COLLISION_AUDIT.md`
8. `research_program/domain_corpus/d01/00_D01_REPORT.md`
9. `research_program/domain_corpus/d01/02_ARTIFACT_LEDGER.md`
10. `research_program/domain_corpus/d01/03_MECHANISM_SKELETONS.md`
11. `research_program/domain_corpus/d01/06_PROTOCOL_ISSUES.md`
12. `research_program/codex_tasks/D01_1_PROTOCOL_PATCH.md`
13. `research_program/ONTOLOGY_FREE_CARD_V2.md`

## 3. Frozen objects and projection order

The frozen artifact set is:

```text
A01–A23
```

Projection order is fixed:

1. deployment route;
2. ordered learning route;
3. normative `C–X–D–P–V–T–L` projection;
4. human `R–W–E ⊕ L` projection;
5. nearest canonical route;
6. confidence and disposition.

The first pass is closed-set. A pressure case must first be represented with existing codes, modifiers, composition, multi-carrier notation, and ordered-L notation. `UNKNOWN` records insufficient evidence; `N/A` records a type that does not apply. Neither is permission to invent a category.

## 4. Baseline being tested

Human route layer:

```text
R–W–E ⊕ L
```

Normative audit backend:

```text
C–X–D–P–V–T–L
```

The D01.1 three-field patch (`runtime role`, `world dependency type`, `action commitment relation`) is used only as a diagnostic probe. Its fields are not composed into a new signature and do not replace either baseline.

## 5. Regression rules

- A classification unit is the scoped artifact: paper/code version × task mode × planning or generation path.
- `C` is granted only when the carrier passes the four existing world-carrier gates: localizable identity, stateful world operation beyond ordinary encoding, carrier-level grounding, and an interface to deployed planning/output or a learning edge that updates the deployed planning component.
- Training-only carriers do not become runtime `W` values.
- Random samples become `P=PB` only when candidate identity survives to a common resolver.
- Diffusion/flow/AR steps are `T=Ts`; they are not automatically `D3` or `R=RR`.
- `D3`/`R=RR` requires an action or control hypothesis to affect a world/consequence carrier and that carrier to affect a revised action within the same decision before commitment.
- `D2`/`RB` requires identity-preserving candidate consequences and a common resolver.
- A generation-only artifact may use `D5`/`R=RG` with `P=N/A`, not a planning resolver.
- `L` records the ordered learning DAG, including retain/drop and stop-gradient/freeze facts when known. Runtime and learning routes are not inferred from one another.

## 6. Acceptance and change budget

```text
new axis: 0
deleted axis: 0
canonical headline signature changes: target 0
automatic ontology edits: forbidden
structural patch: HOLD pending human approval
commit/push: forbidden in this run
```

`FIT` means the baseline expresses the mechanism without a material caveat. `CLARIFY` means a wording/modifier or evidence boundary should be made explicit, but no axis is missing. `EVIDENCE_GAP` means the artifact cannot be safely resolved from the frozen evidence. `COLLISION` means two mechanismally distinct artifacts collapse to the same full baseline signature. `STRUCTURAL_MISS` means no legal existing projection can express the mechanism without changing an axis or its semantics.

## 7. Expected result

The regression passes only if the 23 artifacts can be projected without adding or deleting axes, and every apparent pressure case is either resolved by the existing ontology or isolated as a human-review HOLD rather than silently patched.
