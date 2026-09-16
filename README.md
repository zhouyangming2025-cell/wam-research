# wam-research

Cross-session Research Brain for **World Model + End-to-End + Planning-centric autonomous driving**.

Text and extracted figures only — canonical PDFs remain local/NAS when archived.

## New session: start here

```text
1. START_HERE.md
2. state/CURRENT_STATE.md
3. state/NEXT_TASK.md
4. state/RESEARCH_PRINCIPLES.md
5. landscape/FIELD_RECONSTRUCTION_PLAN.md
6. landscape/FIELD_ATLAS.md
```

The repo is designed so a fresh GPT-5.6 Sol session can recover the project without re-reading old chats.

A copy-ready fresh-session prompt is in `handoff/NEW_SESSION_PROMPT.md`.

## Isolated task: 12-paper core-mechanism ontology

An independent handoff package for reconstructing the WAM + one-stage E2E core-mechanism ontology from 12 fixed papers is available at:

```text
handoff/core_mechanism_12/README.md
handoff/core_mechanism_12/GPT6_TASK_PROMPT.md
```

This task does **not** replace the live field-reconstruction state above. Its existing A/B/C/D signatures are historical drafts to falsify, not canonical answers.

## Current research stage

```text
FIELD RECONSTRUCTION — Planning-centric WAM Atlas
```

The project has deliberately paused hypothesis-first gap hunting. P1/P2-R/P3 are retained as historical probes, but they no longer organize the reading program.

Current principle:

```text
understand the field
→ map major method families / historical transitions / planning interfaces / supervision / evaluation
→ synthesize recurring trade-offs and contradictions
→ only then reopen problem/gap discovery
```

## Research scope

```text
World Model + End-to-End + Planning-centric
```

Planning is the center of gravity. Risk/safety modeling, perception, generation, VLA and representation learning matter only insofar as they contribute to planning capability or explain planning behavior.

**Risk field is optional, not a required destination.**

## Field reconstruction

Canonical documents:

```text
landscape/FIELD_RECONSTRUCTION_PLAN.md
landscape/PLANNING_WAM_TAXONOMY.md
landscape/FIELD_ATLAS.md
```

Planned depth:

```text
~50–80 paper field census
~15–25 representative anchor deep reads
cross-family synthesis
then research-problem discovery
```

This avoids both blind gap guessing from too few papers and undigested 100+ paper accumulation.

## Hypothesis status

```text
P1_RETIRED = retired historical hypothesis
P2-R       = parked probe, not active search target
P3         = parked backup probe
```

Historical P2-R work remains available under `hypotheses/` and `audits/literature/`.

## Repository layout

```text
START_HERE.md                         one-file new-session bootstrap
state/CURRENT_STATE.md               current project stage/state
state/NEXT_TASK.md                   single next task + stop condition
state/RESEARCH_PRINCIPLES.md         canonical scientific operating rules
state/DECISION_LOG.md                decision provenance
state/RESEARCH_LEDGER.md             factual corpus/gate ledger
landscape/                           field reconstruction plan, taxonomy, atlas
hypotheses/                          historical/parked hypotheses
papers/cards/                        curated per-paper scientific cards
papers/raw_md/<PXXXX_Short>/         MinerU raw Markdown + images
audits/literature/                   cross-paper scientific audits
evidence/                            compact evidence snapshots / legacy capability assets
manifests/CORPUS_MANIFEST.csv        corpus registry
handoff/LATEST.md                    latest session handoff
handoff/NEW_SESSION_PROMPT.md        copy-ready fresh-session bootstrap
scripts/                             ingestion/verification scripts
experiment_logs/                     conversion logs
```

## Source hierarchy

```text
Official/canonical PDF       = exact source authority
GitHub raw MD + figures      = GPT-readable primary-text layer
Paper Card                   = curated paper understanding
Field Atlas                  = cross-paper field understanding
State files                  = canonical research decisions
Chat                         = temporary reasoning workspace
```

If raw MD is ambiguous, verify against official/canonical PDF rather than guessing.

## Scientific discipline

Every anchor paper must be assessed symmetrically:

```text
what problem it actually solves
why its design made sense
exact observation → future → planner data flow
what is supervised vs inferred
strongest direct evidence
strongest limitation / alternative explanation
what it proves
what it does NOT prove
historical role / trade-off
relation to later supporting or contradicting work
```

Use `AUTHOR CLAIM`, `DIRECT EXPERIMENTAL EVIDENCE`, and `OUR INFERENCE` separately.

## Corpus state

Batch 0A contains 12 registered papers; 11 are readable as raw MD in this repo. Existing papers are useful anchors but are **not** treated as a representative sample of the field because they were partly selected to test earlier hypotheses.

## Division of labor

**GPT-5.6 Sol:** field census, deep reading, cross-paper synthesis, atlas/taxonomy maintenance, scientific judgement, direct GitHub write-back.

**Local corpus agent:** bulk acquisition, local PDF archive, MinerU conversion, metadata/QC, local source extraction, code execution, datasets/checkpoints/experiments.

The repo — not conversation history — is the canonical research memory.
