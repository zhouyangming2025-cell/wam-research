# WAM Reading Skill Stack

Last updated: 2026-09-19

Status: **ACTIVE WAM-NATIVE METHOD CONTRACT**

Purpose: convert the external reference skills under `skills/external/` into a controlled workflow for planning-centric WAM research without blindly importing all external rules.

---

# 1. Governing principle

External skills are **method references**, not canonical scientific authority. The working tree keeps only four bundles that directly support paper reading or evidence control: `paper-deep-reader-skill`, `academic-research-agent-skill`, `literature-reading-and-synthesis`, and `agent-paper-reader`. Generic writing, grant, career, visualization, mentoring, feedback, publishing, and project-design snapshots were removed from the active tree because they are not part of the current evidence chain.

Use them selectively:

```text
external skill method
→ extract useful reasoning/evidence interface
→ adapt to WAM project rules
→ write canonical result into papers/audits/landscape/state
```

Do not let a generic research skill override:

```text
state/RESEARCH_PRINCIPLES.md
WAM_DIMENSION_ONTOLOGY_V1.md
project evidence taxonomy
project evaluation-regime taxonomy
Phase-D gate
```

---

# 2. Default stack for every core WAM anchor

## Layer A — `paper-deep-reader-skill`

Scientific function:

```text
SINGLE-PAPER MECHANISM RECONSTRUCTION
```

Use for:

- mainline map;
- prerequisite/term map;
- exact data flow;
- modules, tensors, formulas;
- figures/tables as evidence objects;
- Before / After / Diff / Trade-off;
- assumptions/failure conditions;
- training vs inference graph separation.

Required output before cross-paper judgment:

```text
What enters?
What numerical object is produced?
What each module changes?
What is supervised?
What remains at inference?
```

Do not use it as a research-gap generator.

---

## Layer B — `academic-research-agent-skill` source/claim discipline

Scientific function:

```text
SOURCE GROUNDING + CLAIM GATE
```

Use only the relevant parts:

- source must be inspected before evidence use;
- official/full source preferred;
- source version recorded;
- paper vs code vs later release separated;
- source says / agent infers / researcher hypothesizes separated;
- unsupported causal upgrades forbidden.

WAM-specific source order:

```text
canonical/official paper PDF or repo raw_md
→ supplement
→ exact official source-code commit when needed
→ secondary sources only for navigation/context
```

This layer was critical for SeerDrive because the public code release is a WoTE-integrated variant and cannot overwrite the original paper architecture.

---

## Layer C — `literature-reading-and-synthesis`

Scientific function:

```text
CLAIM–EVIDENCE EXTRACTION + CROSS-PAPER SYNTHESIS
```

Use for:

- claim → evidence object;
- result vs author interpretation;
- confounder / alternative explanation;
- synthesis matrices;
- evidence consistency across papers;
- reusable scientific statements.

WAM-specific extension:

```text
new module/design appears
→ identify scientific function
→ immediately ask which prior anchor performs same function
→ compare implementation / supervision / deployment / evidence
```

This is the bridge from a deep paper read to the WAM coordinate system.

---

## Layer D — WAM Dimension Ontology

Scientific function:

```text
CROSS-PAPER SCIENTIFIC COORDINATE SYSTEM
```

Authority:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
+ active minor amendments
```

Mandatory workflow:

```text
paper mechanism reconstructed
→ fill all A–P dimensions
→ use ABSENT / NOT REPORTED / NOT EVALUATED / NOT APPLICABLE explicitly
→ identify residue not expressible by ontology
```

A paper may not remain inside its own preferred narrative.

---

## Layer E — Ontology residue gate

A new dimension is allowed only when:

```text
1. V1 cannot express an important scientific distinction;
2. the distinction changes supervision / mechanism / deployment / evidence interpretation;
3. it is not merely a module name;
4. prior anchors can be meaningfully re-examined under it;
5. back-projection succeeds.
```

If residue survives:

```text
new dimension proposal
→ backfill prior anchors
→ minor ontology amendment/version
```

SeerDrive example:

```text
survived:
- inference iteration semantics
- planner→world feedback carrier
- iterative-state supervision coverage

merged into existing dimensions:
- mutual-refinement topology → J04
- iteration performance curve → N06
```

This prevents ontology inflation.

---

# 3. Skills that are NOT default during paper understanding

## `research-strategy-and-project-design`

Activate only when the scientific question/project direction is being selected or redesigned.

Current Phase C.5:

```text
OFF by default
```

Reason: premature strategy framing can bias literature understanding toward a desired gap.

## `scientific-feedback`

Activate when reviewing a finished artifact/argument for a specific audience or adversarial critique.

```text
OFF during first-pass mechanism reconstruction
OPTIONAL during QA
```

## `publishing-and-peer-review`

Activate for manuscript/reviewer/rebuttal/publication workflows.

```text
OFF during field reconstruction
```

## writing / communication / figures / grant / career / mentoring skills

Use only for their named downstream artifact tasks. They are not paper-understanding engines.

---

# 4. Required artifact pipeline for a core anchor

```text
RAW_MD / official paper / supplement / exact source version
        ↓
[paper-deep-reader]
mechanism + tensors + figures + formula ledger
        ↓
[source/claim gate]
version map + AUTHOR CLAIM / DIRECT EVIDENCE / OUR INFERENCE
        ↓
[literature synthesis]
module-by-module horizontal comparison
        ↓
[WAM comparison inside the deep analysis]
A–P fields + residue test
        ↓
[residue gate]
keep / merge / split new dimensions
        ↓
canonical artifacts
```

Canonical outputs for an Anchor/Decision paper:

```text
papers/deep_analysis/<ID>_<PAPER>_DEEP_ANALYSIS_V2.md
audits/literature/<PHASE>_<PAPER>_AUDIT.md
state update

Any A–P normalization and residue test belongs inside the deep analysis. Do not create a separate ontology projection or per-paper comparison-matrix extension.
```

---

# 5. Minimum per-module horizontal trigger

For every important module/query/loss/representation/scorer:

```text
1. What exactly does it do?
2. What scientific function does it serve?
3. Which prior paper serves the same function?
4. Is the implementation different?
5. Is supervision different?
6. Is inference usage different?
7. Is evidence stronger/weaker/different?
8. Does this expose a new dimension or only a new implementation?
```

Example:

```text
SeerDrive Future BEV

not enough:
“future BEV helps planning”

required:
LAW future latent       → training shaping only
WoTE future BEV         → utility evaluator
WorldDrive future latent→ distilled reward ranking
World4Drive future latent→ factual-mode selector
SeerDrive future BEV    → planner feature refinement + internal co-refinement
```

---

# 6. Mandatory evidence discipline

Every strong statement must fall into one of:

```text
AUTHOR CLAIM
DIRECT PAPER EVIDENCE
SOURCE/CODE VERIFIED
OUR INFERENCE
```

For WAM claims, always search for the strongest matched control immediately before the claimed mechanism is added.

Never substitute:

```text
headline SOTA
visual quality
large model scale
closed-loop benchmark label
```

for mechanism-specific evidence.

---

# 7. Current active stack

For Phase C.5 core-WAM anchors:

```text
DEFAULT ON:
paper-deep-reader
academic-research-agent source/claim gate
literature-reading-and-synthesis
WAM Ontology baseline + provisional five-question review interface

CONDITIONAL:
source-code audit when a decision-critical ambiguity exists
scientific-feedback for QA

OFF UNTIL LATER PHASE:
research strategy / gap design
peer review / publishing
method design
```

This is the default for Drive-JEPA, Metis, DynFlowDrive, Discrete-WAM and GraphWorld unless a paper demands a specialized extension.
