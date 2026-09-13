# CURRENT_STATE

Last updated: 2026-09-13 (Integration Gate 0)

## Hypothesis status (owner ruling 2026-09-13)

| slot | hypothesis | status |
|---|---|---|
| Primary candidate | **P2R_PRIMARY — Reactive Action-Ordering Gap in Planning-centric WAMs** | PRIMARY CANDIDATE, NOT CONFIRMED GAP |
| Backup | **P3_HOLD — Decision Sufficiency of World Representations** | HOLD AS BACKUP |
| Retired | **P1_RETIRED — Planner-Induced Model Exploitation / Search-Support Gap** | RETIRED AS MAIN PROBLEM |

## Current stage

**Targeted Failure Deep Read** (stage of P2R_PRIMARY). Not started. No new scientific
analysis was performed at Integration Gate 0.

## Current evidence status

- Batch 0A corpus ingestion complete: 12 papers registered, 11 with canonical PDF +
  MinerU raw MD (`RAW_MD_READY`), 1 blocked (P0008 NPPC, paywalled, no open version).
- Integration Gate 0 staged, then expanded to the **full corpus text layer**: full
  manifest, all 11 raw MD + their figures, card skeletons for the three gated papers
  (P0001, P0002, P0010), scripts, logs and reports. All card verdict fields are
  `PENDING SCIENTIFIC REVIEW`; none were auto-generated. Target: the private repo
  `zhouyangming2025-cell/wam-research`.
- No observed-failure, counterevidence, hypothesis-impact, prior-art-occupancy or
  research verdicts exist yet for any paper. The agent produces source extraction only.

## Architecture in force (owner ruling 2026-09-13)

1. Canonical PDFs live **only** on local/NAS. Never uploaded anywhere.
2. No ChatGPT Library or GitHub upload of PDFs, ever.
3. GPT-readable primary-text layer = **MinerU raw Markdown**.
4. Raw MD may enter the GitHub **private repo** as the cross-session full-text layer.
5. ChatGPT Library is an optional convenience copy of raw MD only — not a system dependency.
6. `pdf_sha256` is computed over the logical document bytes read by the canonical
   Python corpus I/O path.
7. The Windows native/.NET +1024 framed view of workspace files is a
   **KNOWN_HOST_QUIRK** — recorded, not investigated further.
8. Where raw MD is insufficient for exact wording, formulas or figures, a source extract
   is generated on demand **from the local canonical PDF**.
9. The agent does source extraction, not scientific judgement.

## Superseded prior state (provenance note)

`论文调研/P1_Agent_Bootstrap_Pack/01_RESEARCH_CONTEXT.md` records P1 as the primary
hypothesis with the boxed verdict "P1 — SURVIVES". That document is **superseded** by
the owner ruling of 2026-09-13: P1 is now `RETIRED AS MAIN PROBLEM`, P2R_PRIMARY is the
primary candidate. The old document is retained unread as a historical record and is
not evidence of the current state.
