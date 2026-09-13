# DECISION_LOG

Newest entry first. Entries record decisions and their basis; the agent does not
supply rationale the owner did not state, and does not derive reversibility conditions
on the owner's behalf.

---

## 2026-09-13 — Hypothesis status reset (P1 retired, P2R primary, P3 hold)

**Decision**

- P1_RETIRED — Planner-Induced Model Exploitation / Search-Support Gap:
  `RETIRED AS MAIN PROBLEM`
- P2R_PRIMARY — Reactive Action-Ordering Gap in Planning-centric WAMs:
  `PRIMARY CANDIDATE, NOT CONFIRMED GAP`, current stage = Targeted Failure Deep Read
- P3_HOLD — Decision Sufficiency of World Representations: `HOLD AS BACKUP`

**Why**

Owner ruling, 2026-09-13. No rationale was restated by the owner; the agent does not
infer one.

**Evidence**

- Owner ruling (this date).
- Superseded prior state: `论文调研/P1_Agent_Bootstrap_Pack/01_RESEARCH_CONTEXT.md`
  (P1 as primary, "P1 — SURVIVES") — retained as historical record only.

**Counterevidence considered**

Recorded by the owner at decision time; not restated here.

**What would reverse this decision**

Owner's call. No agent-defined condition.

---

## 2026-09-13 — Long-term architecture ruling (PDF locality, text layers, hash authority)

**Decision**

1. Canonical PDFs stored only on local/NAS; never uploaded to ChatGPT Library or GitHub.
2. GPT-readable primary-text layer = MinerU raw Markdown.
3. Raw MD may live in the GitHub private repo as the cross-session full-text layer.
4. ChatGPT Library = optional convenience copy of raw MD, never a system dependency.
5. `pdf_sha256` = SHA256 over logical document bytes from the canonical Python corpus
   I/O path.
6. Windows native/.NET +1024 framed file view = `KNOWN_HOST_QUIRK`; no further
   investigation.
7. Insufficient raw MD (exact wording, complex formulas, figures) → on-demand source
   extract from the local canonical PDF.
8. Agent role = source extraction; scientific judgement stays with the owner.

**Why**

Owner ruling, 2026-09-13. Establishes which artifacts may cross which boundary and
fixes the hash basis so integrity checks are reproducible.

**Evidence**

- Observed host defect this ruling closes: two read paths of the same workspace file
  (mediated Python vs Windows native/.NET) differ by a +1024 framed representation;
  documented with measurements in `BATCH_0A_INGEST_REPORT.md` §D.3 (Batch 0A).
- Verified pipeline fact: MinerU raw MD of all 11 ingested papers is complete text,
  0 mojibake, all referenced images present (Batch 0A ingest report §C.2).

**Counterevidence considered**

None applicable — architecture ruling, not a scientific claim.

**What would reverse this decision**

Owner's call.
