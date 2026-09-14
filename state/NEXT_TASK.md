# NEXT_TASK

## 唯一下一任务

> Execute **Phase C.5 — Core-WAM Coverage Correction** before any Phase-D problem discovery.

Canonical scope correction:

```text
landscape/PURE_WAM_PRIORITY_CORRECTION.md
```

## Status

```text
Wave 1            CLOSED
Wave 2            CLOSED
Wave 3            CLOSED
Research QA Gate  CLOSED
Wave 4            CLOSED
Phase-C synthesis COMPLETE FIRST PASS
Phase D           PAUSED
Phase C.5         ACTIVE
```

## Why Phase D is paused

The first-pass synthesis is useful, but the core WAM branch is not yet complete enough. The external reading map identifies several planning-centric WAM papers that are absent from the current repo/atlas, while the project spent some effort on VLA controls.

Primary priority is now:

```text
2.2 WAM core branch
```

Secondary/control priority:

```text
2.1 WAM+VLA / VLA-centric branch
```

VLA is retained as a control, not the main organizing direction.

## Core-WAM audit list

Already covered deeply:

```text
Epona
WoTE
DriveLaW
LAW
```

Must now verify and place:

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

Important anti-alias rules:

```text
Auto-JEPA != automatically Drive-JEPA
Drive-WM != automatically WorldDrive
DA-WAM != automatically Discrete-WAM
```

Do not merge papers by similar naming without primary-source verification.

## First execution block

For each missing item, establish:

```text
1. exact paper identity
2. year / venue / authors / institutions
3. official paper URL
4. official code URL if any
5. whether it is truly planning-centric WAM
6. world-state representation
7. predictive / generative mechanism
8. exact world→planning interface
9. supervision source
10. inference path
11. evaluation regime
12. strongest evidence / strongest limitation
13. relation to existing Waves 1–4 taxonomy
14. whether deep read is required
```

## Reading-depth gate

Assign each paper:

```text
ANCHOR
CENSUS
DUPLICATE / NEAR-DUPLICATE
OUT-OF-SCOPE
UNVERIFIED
```

Only ANCHOR papers receive full deep reads.

## Deliverables

Create/update:

```text
landscape/PHASE_C5_CORE_WAM_COVERAGE_AUDIT.md
landscape/PHASE_C_WAVES1_4_FIELD_SYNTHESIS.md   # only after evidence changes are known
state/CURRENT_STATE.md
state/RESEARCH_LEDGER.md
```

## Stop condition

Do not reopen Phase D until:

```text
all listed 2.2 WAM papers are verified/placed;
all decision-relevant missing WAM mechanisms are deep-read;
existing field conclusions are rechecked against them;
a WAM-only historical/interface synthesis is stable.
```

## Still forbidden

```text
no problem/gap selection yet
no method design
no broad VLA expansion
no forced risk-field insertion
no assuming similar paper names are the same work
no treating the existing first-pass field synthesis as final core-WAM coverage
```
