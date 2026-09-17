# D01.1 Protocol Pause Handoff

Date: 2026-09-17 (Asia/Shanghai)

Status: **PAUSED BY USER — DO NOT START D02**

This document freezes the current state after D01 and the provisional D01.1 protocol patch. The pause is deliberate: continuing directly into an 80–120-paper census may recreate the project's rejected early pattern of dense paper-by-dimension bookkeeping instead of producing a compact mechanism map.

## 1. Research objective

The project is not trying to build the largest comparison table. Its target is a compact, extensible mechanism account of WAM + one-stage autonomous driving:

```text
evidence and source audit
-> artifact/mode-level causal reconstruction
-> functional equivalence classes
-> compact mechanism signatures
-> canonical-paper regression and unseen-paper blind tests
```

Two papers should share a mechanism class when their semantic inputs, outputs, decision role, and relevant lifecycle are functionally equivalent, even if their internal implementation uses different backbones, representations, losses, or solvers.

The 12-paper ontology is a deep regression/explanation suite. It must not determine the broader domain structure by itself.

## 2. Completed work

### D01 domain census

Branch: `codex/domain-census-d01`

Commit: `19c0e59ec9c902a47c3b5e1ec7d193fee6c87142`

GitHub: <https://github.com/zhouyangming2025-cell/wam-research/tree/codex/domain-census-d01>

Results:

- 26/26 prescribed papers accounted for;
- 19 `IN-DOMAIN`, 7 `BOUNDARY`, 0 `EXCLUDE`;
- 23 materially distinct artifacts/modes;
- 23 ontology-free mechanism skeletons;
- reading depth: 19 at RD2 and 7 at RD3;
- no projection of the existing compact or seven-field ontology codes;
- no modification to the 12-paper ontology or its handoff;
- D01 result files are under `research_program/domain_corpus/d01/`.

D01's useful result is not a new taxonomy. It shows that scope decisions and artifact/mode splitting are workable, while exposing unresolved differences among training-time prediction, representation transfer, deployed predictive state, online rollout, simulation, and generation-only modes.

### D01.1 provisional protocol patch

Branch: `codex/domain-census-d01-1`

Commit: `302d3355eda077ef2ae456b7f55158a907654a0a`

GitHub: <https://github.com/zhouyangming2025-cell/wam-research/tree/codex/domain-census-d01-1>

Changed files:

- `research_program/ONTOLOGY_FREE_CARD_V2.md`
- `research_program/codex_tasks/D01_1_PROTOCOL_PATCH.md`

The patch adds three controlled artifact-level fields:

```text
runtime role
world dependency type
action commitment relation
```

The patch does not alter D01 results and does not alter the 12-paper ontology.

Important status boundary:

> D01.1 is implemented and pushed, but it is not approved as the basis for D02.

It has not yet passed an independent compactness/regression audit across the 23 D01 artifacts.

## 3. Why work is paused

The project previously rejected a structure equivalent to:

```text
many audit dimensions × many papers
```

That structure accumulated evidence but obscured functional equivalence. Sensor type, representation, architecture, training method, lifecycle, deployment role, and evidence strength appeared at the same level. Nearly every paper looked unique, so the system failed to explain reusable technical routes.

D01.1 was intended to prevent lifecycle mistakes. However, if its three fields are treated as three new ontology axes, combined into cross-products, or expanded with more exceptions during D02, the project will return to the same rejected structure under new names.

The danger is therefore not that the three questions are irrelevant. The danger is promoting diagnostic questions into the final public mechanism signature.

## 4. Principal risks

### Risk 1 — Routing fields become final taxonomy axes

The three D01.1 fields were designed to stop category errors. They must not automatically become permanent signature slots. Concatenating all possible values would create a mechanical code space before the field has demonstrated that each distinction changes the core mechanism.

### Risk 2 — Detail grows faster than explanatory power

The ontology-free card already contains detailed DAG, state, future, action, objective, learning, deployment, timing, uncertainty, interaction, evidence, deletion, and invariance sections. Applying the full card mechanically to 80–120 papers would produce a large evidence database, not necessarily a clearer map.

### Risk 3 — Audit attributes are mistaken for mechanism modules

Training target provenance, detach/freeze boundaries, representation substrate, implementation family, source completeness, and evidence confidence remain important. They do not all belong in the mechanism signature.

### Risk 4 — Training and deployment are separated by adding categories rather than causal reasoning

`training improvement`, `representation transfer`, and `runtime decision` can be useful routing labels. But a paper can improve training and still retain an online predictive path. Forcing one label without a principled primary-role rule can hide rather than resolve the mechanism.

### Risk 5 — Missing non-applicability in action commitment

`simulation` and `generation only` artifacts may have no terminal action commitment. The current controlled values contain `unknown` but not `not applicable`. Treating non-applicability as unknown would conflate two different evidence states.

### Risk 6 — Training imagination and deployed rollout can be conflated

The current `online rollout` description allows both training-time imagination and runtime rollout, relying on another field to disambiguate them. This may be adequate as routing metadata, but it is risky as a standalone mechanism category.

### Risk 7 — Artifact splitting can become an escape hatch

Artifact/mode splitting is necessary when terminal output, lifecycle, or causal topology changes. It can also be overused to avoid choosing the correct abstraction, multiplying records until every configuration becomes unique.

### Risk 8 — D01.1 has not been independently stress-tested

The same execution session designed and documented the patch. It has not been challenged by an independent reviewer or by a frozen, exhaustive projection across the D01 artifacts. Confirmation bias remains possible.

### Risk 9 — Premature D02 expansion would fossilize mistakes

Once 80–120 papers are encoded, changing the schema becomes expensive and psychologically difficult. Scale must follow abstraction validation, not substitute for it.

## 5. Frozen boundaries during the pause

Until the user explicitly resumes the program:

- do not start D02;
- do not acquire or census the 80–120-paper corpus for this program;
- do not backfill the three new fields into the frozen D01 result files;
- do not treat D01.1 as approved or merge-ready;
- do not add more controlled categories to repair individual papers;
- do not modify `outputs/core_mechanism_12_v1/`;
- do not modify `handoff/core_mechanism_12/`;
- do not project D01 papers into the existing compact or seven-field ontology;
- do not claim that the field or ontology is saturated.

## 6. Required review before resumption

The next reviewer should decide the role of the three D01.1 fields before any scale-up:

```text
Option A: diagnostic routing metadata only
Option B: audit attributes attached to a smaller mechanism signature
Option C: candidate ontology axes
Option D: discard or replace one or more fields
```

The current safety recommendation is **Option A or B**, not Option C.

The review should answer:

1. Can the final route for a paper still be explained in one short causal sentence?
2. Does each retained distinction prevent a real causal collision between papers?
3. If a field is removed, do genuinely different training/deployment graphs become indistinguishable?
4. Can simulation and generation-only modes use an explicit non-applicable commitment state without polluting action mechanisms?
5. Can the 23 D01 artifacts collapse into a small number of understandable equivalence classes?
6. Does a new field change the core route, or is it only an audit attribute?
7. Can a reader understand the final map without reading the full evidence card?

## 7. Anti-regression acceptance test

Before D02, require all of the following:

- the three fields are explicitly declared either routing metadata, audit attributes, or core mechanism fields;
- no uncontrolled cross-product signature is created;
- final human-facing mechanism descriptions contain no more than three or four causal stages;
- implementation swaps such as RGB/BEV/latent, Transformer/diffusion/flow, or solver-step changes do not create new routes by themselves;
- all fine-grained evidence remains in the backend audit layer;
- only papers involved in collisions or boundary decisions receive deeper cards;
- a census row remains readable without horizontal dimension sprawl;
- the 23 D01 artifacts demonstrate compression rather than category proliferation.

Failure of the compression test means the patch must be simplified or demoted to audit metadata. It must not be repaired by adding more categories.

## 8. Recommended resumption sequence

When the user resumes:

1. Review D01.1 conceptually; do not edit the D01 result set.
2. Create a separate scratch/regression document that applies the three fields to the 23 D01 artifacts.
3. Count collisions and unique combinations, but do not equate combinations with mechanisms.
4. Compress the results into short causal route descriptions.
5. Reject or demote any field that does not improve those descriptions.
6. Resolve the `unknown` versus `not applicable` issue.
7. Obtain explicit user approval of the compact output format.
8. Only then draft and execute D02.

D02 itself should begin with a shallow one-row census and promote only collision/boundary representatives to deeper reading. It should not produce 80–120 full 18-section cards.

## 9. Repository state at pause

Working directory:

```text
D:\zym_information\ZYM\wam\workspace\domain-census-d01
```

Current branch before this handoff commit:

```text
codex/domain-census-d01-1
```

Current D01.1 implementation commit before this handoff:

```text
302d3355eda077ef2ae456b7f55158a907654a0a
```

Remote tracking was clean at pause. The only intended additional change after that commit is this handoff document.

## 10. Bottom line

D01 succeeded as a bounded census and exposed the correct problems. D01.1 captured those problems in three useful questions, but the questions have not earned a place in the final mechanism signature.

The program should remain paused until it can demonstrate:

> more evidence produces fewer, clearer functional routes—not more fields, more codes, and more paper-specific categories.
