# REVIEW PROTOCOL — ChatGPT Research Lead

Status: **MANDATORY FOR BATCH ACCEPTANCE**

## Purpose

Prevent high-volume Codex output from becoming canonical evidence without mechanism-level review.

## Review object

Every Codex submission is reviewed as a Git diff and evidence package, not by trusting its prose summary.

Required inputs:

```text
task brief
branch
commit SHA
diff against task base
batch report
source/evidence files
```

## Review sequence

### 1. Scope audit

Check whether each paper/artifact is correctly treated as:

```text
Tier 1 domain evidence
Tier 2 adjacent/boundary evidence
Tier 3 theory support
exclude
```

Reject keyword-based inclusion.

### 2. Evidence audit

Sample and fully inspect mechanism-critical claims against primary sources.

Check:

```text
RD label honesty
paper vs survey provenance
paper vs code distinctions
UNKNOWN vs unsupported certainty
source traceability
```

### 3. Artifact audit

Check whether task/mode/version splitting is neither too coarse nor implementation-fragmented.

Questions:

```text
Does a mode change deployment topology?
Does paper vs code differ materially?
Does the terminal output/task differ?
Would merging artifacts erase a mechanism distinction?
Would splitting them merely encode hyperparameters?
```

### 4. Train/runtime audit

Look specifically for leakage between:

```text
training-only future targets
runtime world/predictive objects
teacher-only branches
distilled deployed surrogates
dropped/bypassed modules
```

### 5. Ontology-bias audit

Search the batch for accidental projection language.

The extractor should not have forced evidence into current R/W/E/L or backend codes unless explicitly authorized.

### 6. Mechanism surprise audit

Identify cases that may matter for future ontology design, but do not immediately add classes.

Record each as:

```text
SURPRISE
POTENTIAL COLLISION
POTENTIAL MISSING QUESTION
BOUNDARY AMBIGUITY
EVIDENCE CONFLICT
```

### 7. Protected-path audit

Confirm task did not modify protected historical ontology or master-protocol files.

## Verdicts

### ACCEPT

Evidence quality and scope are sufficient for canonical research use.

### ACCEPT WITH CORRECTIONS

Minor identified corrections can be applied without rerunning the batch.

### REVISE

Material extraction/scope/evidence problems require a Codex correction pass.

### REJECT

Batch methodology is unreliable enough that evidence should not enter canonical state.

## Review output

Create:

```text
research_program/reviews/<TASK>_REVIEW.md
```

Required sections:

```text
Verdict
Commit reviewed
Scope findings
Evidence findings
Artifact findings
Train/runtime findings
Mechanism surprises
Corrections required
Canonical evidence admitted
Next task authorization
```

## Ontology change firewall

Batch acceptance is not ontology acceptance.

A recurring pattern discovered in a corpus batch becomes a top-level ontology candidate only after a dedicated axis audit using necessity, orthogonality, coverage, collision, invariance, deletion, holdout, and human-interpretability tests.

## User role

The user remains the final research-owner acceptance gate for major ontology decisions.

ChatGPT may recommend a verdict and write candidate decision memos, but a major human-layer ontology promotion should remain explicitly reviewable by the user.