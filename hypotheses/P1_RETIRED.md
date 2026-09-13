# P1_RETIRED — Planner-Induced Model Exploitation / Search-Support Gap

**Status:** `RETIRED AS MAIN PROBLEM` (owner ruling, 2026-09-13)

## Prior formulation (recorded for provenance — superseded)

From `论文调研/P1_Agent_Bootstrap_Pack/01_RESEARCH_CONTEXT.md` (historical record,
superseded by the retirement ruling):

- Model trained on `(a,s) ~ p_train`, yielding `Û(a,s)` or `Ŵ(s,a)`; the planner
  generates its next query batch from model outputs, so
  `p_query(a | planner) ≠ p_train(a)` — a distribution shift the planner actively
  manufactures, not one brought by an external test set.
- Candidate mechanism chain: model error → planner search update → query shift →
  exploitable model error → wrong selected action.
- The sub-layer P1-C (planner-induced model exploitation) was the historically retained
  core; P1-A (candidate coverage) and P1-B (evaluator generalization) were already
  deprioritized.
- Historically cited supporting evidence (as recorded in that document, not re-evaluated
  here): TOAD, Gen-Drive; historical counterexample: NPPC; mechanism evidence:
  Sensitivity Shaping; structural supervision note: DA-WAM.

## Status note

`RETIRED AS MAIN PROBLEM` means P1 is no longer pursued as the main research problem.
Historical evidence records above are provenance of what was considered, not claims
about validity. Nothing in this file was re-analysed at Integration Gate 0.

## Definition body for the successor hypothesis

See `P2R_PRIMARY.md`.

## What would un-retire this hypothesis

Owner's call. No agent-defined condition.
