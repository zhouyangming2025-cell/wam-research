# DECISION_LOG

Newest entry first.

---

## 2026-09-14 — Phase-A breadth target reached; stop bulk acquisition and close by scientific placement

**Decision**

The corpus has reached the planned Phase-A breadth scale at infrastructure level:

```text
P0001–P0060 registered
58 RAW_MD_READY
2 lawful-source blockers
```

Therefore broad acquisition is paused. The next task is not another paper-download batch; it is to scientifically place the newly ingested coverage works, audit F1–F11 coverage, freeze Phase A, and select the representative Phase-B deep-read anchors.

**Why**

The local agent has now supplied the missing text layer for:

- P0013–P0020 interactive/reactive/counterfactual branch;
- P0021–P0034 Round-2 coverage holes (non-WM controls, VLA, WM-RL, representation bridges, benchmarks);
- P0035–P0060 works already named in the Phase-A Round-1 census.

Continuing to accumulate papers before integrating these records would recreate the original failure mode: corpus growth faster than scientific understanding.

**Immediate gate**

1. census-place P0021–P0034;
2. create `landscape/CENSUS_PHASE_A_ROUND2.md`;
3. update `FIELD_ATLAS.md` and run an explicit F1–F11 coverage audit;
4. add another paper only if that audit reveals a concrete missing family/transition;
5. finalize roughly 15–25 Phase-B anchor papers.

`Hydra-MDP++` and `NAVSIM-v2` remain optional unresolved follow-ups rather than automatic blockers.

No gap/novelty selection is reopened by this decision.

---

## 2026-09-14 — Field-reconstruction reset: stop hypothesis-first gap hunting

**Decision**

The project will no longer organize literature review around finding, rescuing, or killing a preselected gap.

Active stage becomes:

```text
FIELD RECONSTRUCTION — Planning-centric WAM Atlas
```

P1/P2-R/P3 are retained only as historical probes:

```text
P1 = retired historical hypothesis
P2-R = parked probe, not active search target
P3 = parked backup probe
```

Before formal research-problem selection, the project will reconstruct the field at two depths:

```text
~50–80 paper census at placement/overview depth
~15–25 representative anchor deep reads
```

followed by cross-family synthesis of historical evolution, planning interfaces, supervision, evaluation regimes, recurring trade-offs, counterexamples and under-measured capabilities.

**Why**

The previous process was structurally too narrow: it started from a small, hypothesis-biased paper set and quickly generated candidate gaps. Even careful falsification afterward could not remove the initial path dependence. A narrow claim could survive simply because the search coordinates were narrow, not because the field had been understood.

The earlier analyses are not discarded: paper facts, counterexamples and source audits remain useful evidence. What is withdrawn is their use as sufficient basis for choosing the research problem.

**New canonical artifacts**

- `landscape/FIELD_RECONSTRUCTION_PLAN.md`
- `landscape/PLANNING_WAM_TAXONOMY.md`
- `landscape/FIELD_ATLAS.md`

**Research discipline**

During the census phase:

- no gap/novelty verdict per paper;
- no reading list optimized around P2-R;
- no forcing risk-field expertise into the map;
- include strong non-WM end-to-end planners and benchmark/evaluation papers;
- check historical interactive-prediction/planning predecessors so modern terminology does not hide old ideas.

**Reopen gap selection only when**

The atlas can coherently explain major planning-centric WAM families, their historical transitions, observation→future→planner interfaces, supervision availability, action-conditioning/reactivity distinctions, evaluation meanings, strong counterexamples and recurring trade-offs.

---

## 2026-09-13 — Planning-centric scope + problem-first rule + targeted corpus freeze

**Decision**

1. Research identity is fixed as:

```text
World Model + End-to-End + Planning-centric autonomous driving
```

2. Risk field / predictive risk field is **not** a required destination. The owner's prior risk/safety expertise is optional prior knowledge, to be used only if a surviving planning problem genuinely benefits from it.
3. Every paper must be evaluated symmetrically: strongest evidence, strongest limitation, what it proves, what it does not prove, observed failure vs our inference, prior-art pressure, residual question.
4. Broad corpus expansion is paused. Add only the frozen targeted set in `state/TARGETED_READING_QUEUE.md`: five direct P2-R papers plus three historical interactive-planning controls, then stop and adjudicate.
5. No method design before this gate closes.

**Why**

The active risk is no longer lack of papers; it is path dependence and premature solution design. Existing Batch 0A evidence already shows that broad architectural claims are heavily occupied. The next papers must therefore have high discrimination value for the narrow P2-R question rather than merely share WAM/risk keywords.

A second risk is confirmation bias: papers that resemble our ideas must not be treated more harshly, and papers that support our hypothesis must not be treated more generously. Scientific review must preserve both strengths and weaknesses.

**Superseded note**

The 2026-09-14 field-reconstruction reset supersedes the targeted-freeze as the active program. The targeted set remains useful as one branch of the field atlas rather than the sole gate.

---

## 2026-09-13 — P2-R Round-1 adjudication: survives as question, not confirmed gap

**Decision**

```text
P2-R SURVIVES ROUND 1 AS A QUESTION, NOT AS A CONFIRMED GAP.
```

No method design was authorized.

**Why**

The existing repo corpus showed that several broad formulations were already occupied: interaction-aware planning; reactive/closed-loop evaluation; ego-action-conditioned world modeling; candidate-specific future prediction; future-conditioned candidate scoring.

The reviewed papers did not directly measure the narrower matched-state / matched-candidate reaction-induced action-ordering quantity.

**Evidence reviewed**

- P0002 SafeDrive
- P0004 BeTop
- P0003 GraphAD
- P0005 RiskWorld
- P0012 DA-WAM

Full audit: `audits/literature/P2R_TARGETED_FAILURE_DEEP_READ_ROUND1.md`

**Current provenance status**

Retained as a useful historical scientific audit, but P2-R is parked during field reconstruction and no longer organizes the reading program.

---

## 2026-09-13 — Scientific workflow takeover

**Decision**

The private GitHub repo becomes the canonical cross-session Research Brain.

- GPT-5.6 Sol handles scientific deep reading, synthesis, hypothesis adjudication, field-atlas maintenance, paper-card scientific content and direct repo state updates.
- The local corpus agent handles acquisition, MinerU conversion, metadata/QC, local-PDF source extraction, source-code execution, datasets/checkpoints and experiments.

**Boundary**

Canonical PDFs remain local/NAS when archived. GitHub stores raw Markdown, figures, research cards, audits, landscape/state files, manifests and decisions.

---

## 2026-09-13 — Hypothesis status reset (historical)

**Decision at that time**

- P1_RETIRED — `RETIRED AS MAIN PROBLEM`
- P2R_PRIMARY — `PRIMARY CANDIDATE, NOT CONFIRMED GAP`
- P3_HOLD — `HOLD AS BACKUP`

**Superseded by 2026-09-14**

P2-R is now parked as a probe while the field is reconstructed; P3 remains a parked backup probe.

---

## 2026-09-13 — Long-term architecture ruling (PDF locality, text layers, hash authority)

**Decision**

1. Canonical PDFs stored on local/NAS when archived; do not rely on GitHub for PDF binaries.
2. GPT-readable primary-text layer = MinerU raw Markdown when ingested.
3. Raw MD may live in the GitHub private repo as the cross-session full-text layer.
4. ChatGPT Library = optional convenience copy of raw MD, never a system dependency.
5. `pdf_sha256` = SHA256 over logical document bytes from the canonical Python corpus I/O path.
6. Windows native/.NET +1024 framed file view = `KNOWN_HOST_QUIRK`; no further investigation.
7. Insufficient raw MD (exact wording, complex formulas, figures) → on-demand source extract from the local canonical PDF or direct official PDF verification.
8. Corpus agent = source/infrastructure worker; scientific judgement is maintained in the Research Brain by GPT-5.6 Sol + owner.
