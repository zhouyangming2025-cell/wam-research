# PURE_WAM_PRIORITY_CORRECTION

Last updated: 2026-09-14

Status: **HISTORICAL SCOPE CORRECTION — retained as a boundary; current program and next task are controlled by `state/CURRENT_STATE.md` and `state/NEXT_TASK.md`.**

## 1. Why this correction exists

The project completed a broad first-pass field synthesis across planning-centric world models, strong non-WM controls, evaluation, reactivity, and one VLA control branch. A new scope review identified a material risk: the current anchor set may be **under-complete on the core WAM branch itself**, while some effort was spent on VLA/semantic-planning controls.

The primary research target is therefore tightened to:

```text
CORE PRIORITY:
World Model / WAM + End-to-End + Planning-centric autonomous driving

SECONDARY / CONTROL ONLY:
WAM + VLA / VLA-centric planning
```

This does NOT mean VLA work is scientifically irrelevant. It means VLA papers should be used mainly as controls or neighboring paradigms unless they materially alter the core WAM architecture, supervision, world-action interface, or planning mechanism.

## 2. User-supplied core-WAM reading map to audit

The following items were identified as the main 2.2 WAM branch and must be checked before formal problem discovery:

```text
2.2.1 code-available / implementation-oriented
- Epona
- WorldDrive
- WoTE
- World4Drive
- DriveLaW
- LAW
- SeerDrive
- Drive-JEPA
- Metis

2.2.2 no-code / paper-only candidates shown in the reading map
- DynFlowDrive
- Discrete-WAM
- GraphWorld
```

Names / years / institutions from the external reading map are **navigation hints only** until verified against primary sources.

## 3. Current repo coverage audit

Already well represented in the current deep-read program:

```text
Epona
WoTE
DriveLaW
LAW
```

Potentially related but NOT substitutes without verification:

```text
Auto-JEPA != automatically Drive-JEPA
Drive-WM != automatically WorldDrive
DA-WAM != automatically Discrete-WAM
```

Repository code/text search on 2026-09-14 found no current indexed mention for:

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

Therefore the prior statement that the field reconstruction was ready to move directly into Phase-D problem discovery is now **too strong**.

## 4. Revised interpretation of the completed Waves 1–4

The existing Waves 1–4 remain scientifically useful and should NOT be discarded.

They establish robust control coordinates:

```text
Wave 1: historical interaction / non-WM planning / evaluation controls
Wave 2: world prediction → planning-interface taxonomy
Wave 3: world-action coupling variants
Wave 4: feedback / closed-loop / simulator / reactivity semantics
```

But they are now treated as:

```text
FIRST-PASS FIELD FRAMEWORK
```

not yet:

```text
FINAL CORE-WAM COVERAGE COMPLETE
```

The missing 2.2 papers may:

```text
- fill a currently missing WAM family;
- strengthen an existing family;
- falsify one of the current cross-paper conclusions;
- reveal that an apparent evidence gap has already been addressed;
- change the historical sequence of WAM development.
```

Hence Phase D is paused.

## 5. VLA policy

Papers such as ORION and the broader WAM+VLA list remain useful for specific control questions:

```text
Can semantic reasoning / memory / action interfaces produce strong planning without explicit world rollout?
Does a VLA representation solve a capability currently attributed to WAM?
```

But they no longer consume equal deep-read priority with the core 2.2 WAM branch.

Operational rule:

```text
Core WAM paper missing from atlas  >  new VLA paper
```

until the 2.2 core branch is closed.

## 6. New gate before Phase D

Create a **Phase C.5 — Core-WAM Coverage Correction**.

For each missing 2.2 item:

```text
1. verify exact title / authors / year / venue / official source;
2. determine whether it is truly planning-centric WAM;
3. determine code availability;
4. place it on the existing planning-interface taxonomy;
5. identify whether it duplicates an existing anchor or adds a new mechanism;
6. deep-read only if decision-relevant;
7. update the field synthesis if it changes any stable claim.
```

No gap mining until this gate closes.

## 7. Stop condition

Phase C.5 closes only when every listed core-WAM item is assigned one of:

```text
ANCHOR — deep read required / completed
CENSUS — accurately placed; no deep read required
DUPLICATE / NEAR-DUPLICATE — covered by existing mechanism family
OUT-OF-SCOPE — not actually planning-centric WAM
UNVERIFIED — primary source cannot yet be established
```

Then rerun the core synthesis with emphasis on WAM-only evolution before reopening Phase D.

## Decision

```text
PHASE D PROBLEM DISCOVERY = PAUSED
PHASE C.5 CORE-WAM COVERAGE CORRECTION = ACTIVE
WAM+VLA = SECONDARY CONTROL BRANCH
```
