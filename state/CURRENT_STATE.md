# CURRENT_STATE

Last updated: 2026-09-14 — Phase D paused; Phase C.5 Core-WAM Coverage Correction ACTIVE

## Research north star

```text
World Model / WAM + End-to-End + Planning-centric autonomous driving
```

Planning is the center of gravity. Risk/predictive-risk expertise is optional prior knowledge, not a required destination.

## Scope priority correction

The current project now distinguishes:

```text
PRIMARY:
core WAM / World Model + planning

SECONDARY CONTROL:
WAM+VLA / VLA-centric planning
```

VLA papers remain useful as controls, but they should not consume equal priority while the core WAM branch is still incomplete.

Canonical correction:

```text
landscape/PURE_WAM_PRIORITY_CORRECTION.md
```

## Methodological rule in force

```text
FIELD UNDERSTANDING FIRST
→ complete core-WAM coverage
→ comparative anchor deep reads
→ cross-family synthesis
→ evidence QA
→ only then adversarial problem discovery
→ falsification
→ method design
```

P1/P2-R/P3 remain historical probes and do not organize reading.

## Current active stage

```text
PHASE C.5 — CORE-WAM COVERAGE CORRECTION
```

Phase D problem discovery is **PAUSED**.

Reason: the Waves 1–4 synthesis is a useful first-pass framework, but a scope review identified under-coverage of several papers in the core 2.2 WAM branch.

## Completed foundation

```text
Phase A census     CLOSED
Wave 1             CLOSED
Wave 2             CLOSED
Wave 3             CLOSED
Research QA Gate   CLOSED
Wave 4             CLOSED
Phase-C synthesis  COMPLETE FIRST PASS
```

Existing synthesis remains valid as a provisional framework:

```text
landscape/PHASE_C_WAVES1_4_FIELD_SYNTHESIS.md
```

but is not yet treated as final core-WAM coverage.

## Core-WAM papers already deeply covered

```text
Epona
WoTE
DriveLaW
LAW
```

Related existing anchors include Drive-WM, OccWorld, ViDAR, Auto-JEPA, DA-WAM, Think2Drive, DrivingGPT, etc., but similar names must not be treated as substitutes for missing papers without verification.

## Core-WAM papers now requiring identity / coverage audit

User-provided 2.2 reading map identifies:

```text
WorldDrive
World4Drive
SeerDrive
Drive-JEPA
Metis
DynFlowDrive
Discrete-WAM
GraphWorld
```

Repository search on 2026-09-14 found no indexed mention of these names.

Anti-alias rules:

```text
Auto-JEPA != automatically Drive-JEPA
Drive-WM != automatically WorldDrive
DA-WAM != automatically Discrete-WAM
```

Exact paper identities, years, venues and code status must be verified from primary sources before scientific use.

## VLA branch status

ORION and other VLA/WAM+VLA work remain useful controls for questions such as:

```text
semantic reasoning vs explicit world rollout
memory / state representation vs future modeling
reasoning→action interface vs world-model interface
```

But no broad VLA expansion is authorized until the 2.2 core-WAM branch is closed.

## Existing stable field controls retained

```text
world-prediction quality != planning evidence
future information is not automatically beneficial
candidate-specific output != candidate-specific observed counterfactual supervision
WM-assisted planning != online model-based planning
world completeness != decision relevance
generative action modeling != world modeling
candidate ranking/scoring is an independent bottleneck
closed-loop must be decomposed into feedback channels
sensor photorealism != behavioral realism
reactive feasibility != counterfactual behavioral truth
```

These remain provisional field principles to be rechecked against the missing core-WAM papers.

## Immediate next task

See `state/NEXT_TASK.md`.

Execute **Phase C.5 Core-WAM Coverage Correction**:

```text
verify → classify → deep-read only decision-relevant missing WAM papers
→ revise synthesis if necessary
→ then decide whether Phase D can reopen
```

## Still forbidden

```text
no problem/gap declaration
no method design
no broad VLA expansion
no forced risk-field insertion
no assuming similar paper names are identical
no treating the first-pass synthesis as final WAM coverage
```

## Research Brain architecture

GitHub is the Research Knowledge Authority. Raw MD + figures are the persistent GPT-readable primary-text layer; canonical PDFs / official public papers remain source authority for decision-critical claims.
