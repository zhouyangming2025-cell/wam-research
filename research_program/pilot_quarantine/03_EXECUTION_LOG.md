# Pilot Quarantine Execution Log

Date: 2026-09-18

Working branch: `codex/pilot-quarantine-law-epona-drivelaw`

Baseline: `368c9a848e241bfb7bf2e2d61242269d5e438af6`

## State

| Phase | Status | Result |
|---|---|---|
| P0 repository/source freeze | `COMPLETE` | Three raw papers and three pinned source audits locked in `01_SOURCE_MANIFEST.md`. |
| P0 history access boundary | `COMPLETE` | Old cards, deep analyses, route maps, ontology, and matrices quarantined by procedure. |
| P1 source-first reconstruction | `COMPLETE` | Three records created without route labels. |
| P2 historical claim collision | `COMPLETE-LOCAL` | Only the three papers' directly connected historical claims were checked; no global cleanup was attempted. |
| P3 Chinese human review interface | `READY-FOR-REVIEW` | A single Chinese brief reduces the review to five mechanism/boundary confirmations. |
| P3 human acceptance gate | `PASSED` | User confirmed all five items; no ontology or route promotion. |
| P4 problem × mechanism crosswalk | `ACCEPTED-WITH-MINOR-EDIT` | User accepted the draft; two wording tightenings applied, with no route taxonomy or global matrix. |
| P5 WoTE source-first reconstruction | `PASSED` | Raw paper and pinned official-code audit were read first; candidate/future correspondence, future use, resolver, and supervision-reactivity boundary recorded. |
| P5 WoTE Chinese review gate | `PASSED` | User confirmed all five mechanism/boundary items; one wording was tightened to avoid implying an explicit candidate-ID data structure. |
| P6 World4Drive source-first reconstruction | `PASSED` | Raw paper and pinned official-code audit were read first; candidate/future correspondence, fixed-time future latent, selector, factual-future supervision, and benchmark/code boundaries recorded. |
| P6 World4Drive Chinese review gate | `PASSED` | User confirmed all five items; the shared coarse deployment skeleton and the distinct future/supervision semantics remain explicitly separated. |
| P7 WorldDrive source-first reconstruction | `READY-FOR-REVIEW` | Raw paper and pinned official-code audit were read first; author problem ledger, TA-DWM teacher, FAR distillation, deployment surrogate, resolver, and counterfactual-supervision boundary recorded. |
| P7 WorldDrive Chinese review gate | `PENDING` | A single Chinese brief is ready for review; no route, ontology, or matrix change is proposed. |
| P8 six-paper core-bridge deletion review | `READY-FOR-REVIEW` | Existing six source-first records were re-read using the Core-Bridge Deletion Test; the common candidate/future/score/select interface was demoted to a terminal-structure observation, with no route, matrix, or ontology change. |
| P9 five-question primary-source projection | `READY-FOR-REVIEW` | The frozen five-question frame was projected onto LAW, Epona, and DriveLaW only. Q1–Q5 answers, evidence labels, mode splits, provenance limits, and UNKNOWN fields were recorded in the three source-first records and the existing Chinese brief. |
| P10 five-question collision and deletion test | `READY-FOR-REVIEW` | Q1/Q2, Q3/Q4, and Q4/Q5 collisions were checked against the three records; the existing core-bridge deletion evidence was re-expressed as a five-question deletion test. No new axis, route label, matrix, or ontology change was needed. |
| P11 five-question result visibility repair | `COMPLETE-LOCAL` | The existing Chinese brief now exposes the three-paper results before the detailed appendix, and the frozen protocol explicitly maps legacy B3–B7 evidence fields to Q1–Q5. Validation status remains `READY-FOR-REVIEW`; no new layer was created. |
| P12 five-question wording and deletion-test repair | `READY-FOR-REVIEW` | Q1 was separated from Q5 by removing lifecycle content from the computation-location question; DriveLaW hidden-state wording and LAW's action-conditioned future-latent wording were tightened; the deletion test was demoted from runnable-system language to a mechanism-identity test. No new axis, route label, matrix, or ontology change was made. |
| P13 five-question extension pilot | `READY-FOR-REVIEW` | The repaired Q1–Q5 frame was projected onto the accepted WoTE and World4Drive source-first records. The extension separates training-only/online single-path mechanisms from online candidate selection, and distinguishes WoTE's recurrent BEV rollout from World4Drive's fixed-time factual-future latent matching. No new axis, route label, matrix, or ontology change was made. |

## Mutation audit

- Existing raw paper Markdown: unchanged.
- Existing code audits: unchanged.
- Existing cards, deep analyses, route maps, ontology, and state files: unchanged.
- Files added: only under `research_program/pilot_quarantine/`; WoTE continuation added its record/brief/source appendix, World4Drive added one source-first record plus one Chinese review brief, WorldDrive added one source-first record plus one Chinese review brief, and P8 adds one core-bridge review record.
- Deletions: none.

## Current interpretation boundary

The source-first records are working records, not final scientific conclusions. `AUTHOR CLAIM` remains separate from `PAPER FACT`, and all unresolved deployment or causal questions remain visible.

WoTE, World4Drive, and WorldDrive are the fourth, fifth, and sixth source-first records in the controlled pilot. WoTE is the first positive control; World4Drive is a candidate-selection contrast; WorldDrive is a teacher-to-surrogate candidate-selection contrast. They are evidence records, not a six-paper route classification, and none has been added to the ontology, route taxonomy, or global matrix.

## Latest scope decisions

These decisions consolidate the latest pilot discussion; they do not create a new taxonomy layer.

- The pilot now contains three contrastive records (LAW, Epona, DriveLaW), WoTE as the first positive control, World4Drive as a candidate-selection contrast, and WorldDrive as a teacher-to-surrogate candidate-selection contrast. This is a controlled evidence set, not a six-paper route classification.
- Human-level comparison should retain only differences that change causal structure, deployment dependency, candidate commitment/selection, or the training-to-deployment relation.
- Global query versus spatial waypoint sampling, token naming, representation substrate, attention variant, and refinement-count differences remain implementation notes unless they change one of the four items above.
- “Candidate–scene feature interaction” may be recorded as a local planner-side note, but it is not a new ontology axis, route label, or matrix dimension.
- The existing three-paper crosswalk remains frozen as the accepted three-paper draft. WoTE and World4Drive are recorded through their source-first records, Chinese briefs, and this execution log; no parallel summary hierarchy is introduced.
- World4Drive review passed: its source-first record is accepted; the common `candidate → future representation → score/reward → select` structure is retained only as a terminal deployment observation. Its fixed-time latent and factual-future matching are mechanism facts, not optional route notes, and it is not added to the crosswalk or promoted as a route.
- WorldDrive remains review-ready: its earlier shared-interface wording is now demoted to a terminal deployment observation. Its TA-DWM representation inheritance and teacher → FAR surrogate lifecycle must be evaluated as the core bridge, not treated as a minor comparison note. It is not added to the crosswalk or promoted as a route before human review.
- P8 review correction: `candidate → future representation → score/reward → select` is retained only as a terminal deployment-structure observation. It is not evidence of route equivalence. The six papers must be compared first by their indispensable core bridge and deletion-test result.
- No new paper audit is authorized until the six-paper core-bridge review is accepted. No matrix or ontology modification is authorized by P8.
