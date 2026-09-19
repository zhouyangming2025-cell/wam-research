# Repository State Integrity Audit — 2026-09-16

Status: **ACTION REQUIRED — SCIENTIFIC LAYER STRONG; STATE / ID LAYER DRIFTED**

Scope: bootstrap files, canonical state, expansion queue, stable paper IDs, field atlas, handoff and current deep-analysis artifacts.

---

# 1. Executive finding

The repository's scientific deep-reading layer is substantially ahead of several project-state documents.

Current high-confidence scientific state:

```text
Ontology V1.3 active
16 normalized anchors after P0007 DriveReward
broad WAM deep-read expansion active
research-direction convergence PAUSED
method design FORBIDDEN
```

However, several bootstrap/global documents still encode earlier phases, and the expansion queue contains paper-ID collisions.

Therefore:

```text
scientific content quality = HIGH
state synchronization      = DEGRADED
stable-ID integrity        = DEGRADED in planned queue only
```

No existing ingested paper ID should be renamed or reassigned.

---

# 2. State-drift findings

## A. START_HERE.md

Observed state:

```text
2026-09-14
Wave 3 / Auto-JEPA-era bootstrap
```

Problem:

```text
intended one-file new-session bootstrap
but older than current normalized anchor program
```

Risk:

A fresh session can resume an obsolete task despite the repository being designed specifically to prevent that failure.

## B. handoff/LATEST.md

Observed state:

```text
2026-09-14
Phase D problem discovery = NEXT
```

Current binding state says:

```text
research-direction convergence = PAUSED
broad WAM deep-read expansion = ACTIVE
```

This is a direct contradiction, not merely a stale detail.

## C. state/RESEARCH_LEDGER.md

Observed state still reflects:

```text
60-paper Phase-C-era corpus
Phase D authorization
```

It predates Phase C.5 correction and the subsequent P0061–P0065 / C.6 normalized-anchor expansion.

It should currently be treated as a historical ledger snapshot unless reconciled with `CURRENT_STATE.md` and `NEXT_TASK.md`.

## D. landscape/FIELD_ATLAS.md

Scientific family map remains useful, but status/closeout text is Phase-A/Phase-B-era and says broad acquisition is frozen.

Interpretation:

```text
family taxonomy = still useful
workflow status = stale
```

## E. CORE_WAM_2_2_COVERAGE_AUDIT.md

Useful intermediate audit but stops at:

```text
Discrete-WAM complete
GraphWorld next
```

GraphWorld and five later C.6 anchors are already normalized.

---

# 3. Stable-ID collision audit

Current `papers/raw_md/` inventory establishes existing stable identities including:

```text
P0003 = GraphAD
P0004 = BeTop
P0006 = GenDrive
P0007 = DriveReward
P0010 = TOAD
P0011 = SensitivityShaping
P0013 = BridgeSim
P0014 = ReactSimBench
P0015 = CausalDrive
...
P0065 = GraphWorld
```

But `WAM_DEEP_READ_EXPANSION_QUEUE_V1.md` incorrectly proposes:

```text
P0003 Safe-Sim      COLLISION with GraphAD
P0004 PROSIM        COLLISION with BeTop
P0008 AutoVLA       COLLISION / previously occupied historical slot
P0011 ReCogDrive    COLLISION with SensitivityShaping
P0010 LINGO-2       COLLISION with TOAD
P0006 DriveGPT4     COLLISION with GenDrive
```

BridgeSim / ReactSimBench / CausalDrive are correctly aligned at P0013–P0015.

Binding rule:

> Stable IDs already used by the corpus are immutable. Planned papers must receive new IDs; existing corpus identities must never be reassigned for queue convenience.

---

# 4. Corrected reservation plan

The current raw corpus ends at P0065 GraphWorld. Reserve new IDs sequentially for not-yet-ingested expansion targets:

```text
P0066 SAFE-SIM
P0067 ProSim
P0068 AutoVLA
P0069 ReCogDrive
P0070 LINGO-2
P0071 DriveGPT4
```

Status:

```text
RESERVED FOR INGESTION
not yet RAW_MD_READY
not yet normalized anchors
```

This reservation must be reconciled into `CORPUS_MANIFEST.csv` at ingestion time rather than pretending that the papers are already present.

---

# 5. DriveReward closeout

P0007 DriveReward has now completed the required C.6 normalization bundle:

```text
papers/deep_analysis/P0007_DRIVEREWARD_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_DRIVEREWARD_AUDIT.md
papers/deep_analysis/P0007_DRIVEREWARD_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_DRIVEREWARD_AUDIT.md
(The derived projection and matrix extension were later removed after evidence consolidation.)
```

Active normalized count:

```text
16
```

Ontology result:

```text
V1.3 RETAINED
NO V1.4
```

DriveReward's main scientific control is:

```text
direct learned trajectory value/reward
!=
explicit predicted future world
```

Current evidence suggests its training-time RL reward interface is stronger than its reported online trajectory reranking interface.

---

# 6. Canonical authority until full synchronization

Until old global documents are reconciled, use this precedence:

```text
1. state/NEXT_TASK.md
2. state/CURRENT_STATE.md
3. latest normalized paper artifacts / comparison extension
4. landscape/WAM_DEEP_READ_EXPANSION_QUEUE_V1.md
5. older FIELD_ATLAS / RESEARCH_LEDGER / handoff snapshots for historical context only
```

After this audit, bootstrap files should be synchronized so this temporary precedence rule is no longer needed.

---

# 7. Correct next scientific task

Do NOT reopen Phase D or method design.

Next task:

```text
P0066 SAFE-SIM
```

Before deep reading:

```text
1. register P0066 in corpus manifest / raw source layer
2. verify canonical paper version
3. verify official code source
4. ingest readable primary text
```

Then deep-read as the first Wave C.7 simulation/reactivity control.

Primary questions:

```text
What closes the loop?
Which agents are reactive to whom?
What is generated once vs regenerated every simulation step?
How does adversarial diffusion guidance alter behavior?
What supervision represents plausible behavior rather than planner-specific attack success?
Does closed-loop realism imply counterfactual behavioral truth?
How is SAFE-SIM scientifically different from planning WAMs such as WoTE / SafeDrive / DA-WAM?
How should SAFE-SIM compare with ProSim, BridgeSim, ReactSim-Bench and CausalDrive?
```

---

# Final integrity verdict

The repository does not need a research-method reset. It needs **state synchronization and stable-ID repair**.

The scientific methodology is coherent and increasingly discriminative; the operational metadata failed to keep pace with the work.

Immediate rule:

```text
repair metadata
→ ingest P0066 SAFE-SIM
→ continue Wave C.7
→ keep research-direction convergence paused until the declared maturity gate is met
```
