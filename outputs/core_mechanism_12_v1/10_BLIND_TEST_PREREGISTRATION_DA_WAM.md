# Core Mechanism 12 — DA-WAM Blind-Test Preregistration

Status: preregistered before reading DA-WAM paper or audit contents in this review session.

Preregistration date: 2026-09-16

## 1. Frozen ontology

```text
git commit:
414b5756bbf2d9089a94da44f174d60ff0cb5436

normative specification:
outputs/core_mechanism_12_v1/09_ONTOLOGY_SPEC_S1_PLUS.md

SHA256:
34c14ea6d8f7c6869f50240d968d1f070d9dfc36e5247cf113542db938a6abdf
```

The normative specification must not be edited during this blind test. If DA-WAM cannot be represented, the test fails; the ontology may be revised only in a later, explicitly post-failure phase.

## 2. Blind-test object

Paper: DA-WAM, repository identity P0012.

Reason for selection:

- it is a planning-centric WAM/E2E driving paper;
- it was not one of the 12 papers or 21 artifacts used to derive and attack C–X–D–P–V–T–L;
- it can test candidate-conditioned consequence modeling and resolver semantics without moving to an adjacent simulator-only or reward-only family.

Provisional artifact boundary to resolve from primary evidence:

```text
DAWAM-PLAN-PAPER@paper-revision
DAWAM-PLAN-CODE@source-commit, only if an attributable executable source is evidenced
```

Paper/code records will be split if their deployment or learning DAGs differ materially.

## 3. Evidence protocol

Allowed after this preregistration is committed:

- `papers/raw_md/P0012_DAWAM/P0012_DAWAM.raw.md`;
- attributable official source or the repository's source-code audit with pinned commit;
- factual source notes required to establish version and availability.

Excluded until the blind verdict is written:

- `landscape/P0012_DAWAM_ONTOLOGY_PROJECTION.md`;
- `landscape/WAM_COMPARISON_MATRIX_V1_3_DAWAM_EXTENSION.md`;
- `papers/deep_analysis/P0012_DAWAM_DEEP_ANALYSIS_V2.md`;
- paper cards and synthesis documents that already interpret DA-WAM taxonomically.

The blind projection must be reconstructed from primary paper/source facts, not copied from an earlier ontology projection.

## 4. Required output

The result must contain:

1. frozen artifact/version boundary;
2. deployment DAG;
3. learning DAG with stages, gradients, freeze/detach, and retain/drop;
4. C–X–D–P–V–T–L assignment;
5. evidence and UNKNOWN boundary for every field;
6. type-constraint audit;
7. nearest-signature collision test against the frozen 21 artifacts;
8. implementation-invariance test;
9. explicit list of ontology categories that would have been needed but were absent;
10. PASS/FAIL verdict.

## 5. Preregistered pass criteria

PASS requires all of the following:

- DA-WAM is classifiable without editing the frozen normative specification;
- no paper-named or implementation-named category is introduced;
- every field uses a legal value and distinguishes ∅, N/A, and UNKNOWN;
- the compact signature plus canonical L program reconstructs the core deployment and learning DAG;
- all global type constraints pass;
- the nearest existing artifact is similar for a causal reason and remains distinguishable where the core mechanism differs;
- replacing representation/backbone/generator implementation while preserving semantic interfaces leaves the signature unchanged.

## 6. Preregistered fail criteria

FAIL if any of the following occurs:

- a new top-level research question is required;
- an existing axis cannot express a decision-relevant distinction without a paper-specific exception;
- the artifact forces contradictory values under the current type constraints;
- correct classification requires changing `09_ONTOLOGY_SPEC_S1_PLUS.md`;
- the short signature and canonical L program cannot reconstruct the mechanism at the promised level;
- unavailable evidence is silently converted into ∅ or a confident category.

## 7. S2 gate

One successful blind test permits discussion of S2 but does not automatically grant S2.

After PASS, S2 still requires an explicit judgment of:

- whether unresolved SEER-PAPER/GW-PLAN commitment affects ontology completeness;
- whether source-unverified papers create material untested regions;
- whether the blind test exercised more than an already saturated candidate-consequence family;
- whether an independent reader can reproduce the assignment from the normative specification.

