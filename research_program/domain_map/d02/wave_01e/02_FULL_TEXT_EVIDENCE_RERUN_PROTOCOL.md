# D02-W1E Full-Text Evidence Rerun Protocol

Status: completed as a paper-first rerun; ontology changes are not applied.

Baseline: D02 Wave 1 shallow map and `wave_01/04_ESCALATED_CASES.md`.
Primary evidence layer: local MinerU `*.raw.md`.

## Purpose

This rerun revisits the seven W1 pressure points after full paper text became available locally. It is an evidence-closure pass, not a new census and not an ontology redesign.

The old Wave 1 documents remain unchanged. The rerun records whether full text supports the old route, changes the route, or still leaves the route unresolved.

## Evidence rule

For every case:

1. Read the local MinerU raw Markdown, including method, inference, training, appendix, and conclusion sections.
2. Use the existing `pdftext.md` only as a searchable secondary extraction; it does not override the raw layer.
3. Keep the existing R/W/E/L code set frozen.
4. Use only `KEEP`, `REMAP`, or `REMAIN-UNKNOWN` as route dispositions.
5. Separate paper evidence from code evidence. This rerun is paper-first; a code claim is not inferred from a paper diagram.
6. Preserve the distinction between a shared future carrier and a candidate-indexed consequence. Do not add `X3` merely because a resolver scores a candidate against a shared prediction.

## Cases

```text
P0004 BeTop
P0010 TOAD
P0021 Hydra-MDP
P0029 GenAD
P0034 HUGSIM
P0038 Vista
P0058 VAD
```

## Acceptance boundary

The rerun may revise an artifact route, but it may not:

- add or delete a route code;
- add or delete a normative axis;
- modify `outputs/core_mechanism_12_v1/`;
- retroactively insert P0066 Safe-Sim into the blind Wave 1 selection;
- turn a world-model reward capability into a deployed resolver without final-action evidence.

P0066 is now text-complete, but remains deferred from the sealed blind Wave 1 because it was opened during task setup. It can be used in a later non-blind application pass.
