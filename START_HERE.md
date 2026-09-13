# START_HERE — WAM Research Brain

**Purpose:** a fresh GPT-5.6 Sol session should recover the project direction and current stage in under a minute without reconstructing old chats.

Last updated: 2026-09-14

## 1. Research north star

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Planning is the center of gravity. Perception, video generation, JEPA/latent prediction, VLA, safety/risk modeling and simulation matter only insofar as they affect planning capability, decision quality, closed-loop behavior, or scientific understanding of planning.

**Risk field is NOT a required destination.** Prior risk/predictive-risk expertise is an optional capability pool, not a research commitment.

## 2. Critical methodological reset

The project previously moved too quickly from a small paper set to candidate gaps (P1/P2-R/P3). That workflow is now suspended.

Active rule:

```text
UNDERSTAND THE FIELD FIRST
→ reconstruct planning-centric WAM families and historical evolution
→ understand representations, supervision, planner interfaces, interaction/reactivity and evaluation
→ identify recurring trade-offs / contradictions / under-measured capabilities
→ only then reopen research-problem / gap discovery
```

Canonical plan:

`landscape/FIELD_RECONSTRUCTION_PLAN.md`

Taxonomy:

`landscape/PLANNING_WAM_TAXONOMY.md`

Living atlas:

`landscape/FIELD_ATLAS.md`

## 3. Current hypothesis state

Hypotheses are no longer driving the reading program.

```text
P1_RETIRED  = RETIRED historical hypothesis
P2-R        = PARKED PROBE — not active search target
P3          = PARKED BACKUP PROBE
```

P2-R's prior formulation and Round-1 audit are retained for provenance, but do not organize the field map.

## 4. Current active stage

```text
FIELD RECONSTRUCTION — Planning-centric WAM Atlas
```

Planned depth:

```text
Phase A: ~50–80 paper census at placement/overview depth
Phase B: ~15–25 representative anchor deep reads
Phase C: cross-family synthesis, historical evolution, planning-interface map, supervision map, evaluation map, trade-off/counterexample map
Phase D: only then reopen research-problem discovery
```

This is not indiscriminate paper accumulation: census papers are placed in a common taxonomy; only representative anchors receive full deep reads.

## 5. What the field atlas must explain

A mature atlas should answer:

1. What are the major planning-centric WAM families and why did each emerge?
2. What world state does each family predict: video, BEV, occupancy, geometry, objects, latent, trajectory, reward/value, hybrid?
3. How exactly does future information reach the planner?
4. Which future/action branches receive real supervision and which are inferred/counterfactual?
5. How do action conditioning, joint prediction, reactivity, contingency and game-theoretic interaction differ?
6. What planning outputs are used: direct trajectory, candidate scoring, optimization, control, policy?
7. What do open-loop, NAVSIM, non-reactive closed-loop, reactive closed-loop, CARLA/Bench2Drive and real-vehicle evidence actually prove?
8. Which strong end-to-end planners succeed without an explicit world model?
9. What trade-offs recur across multiple independent method families?
10. Which common field claims have strong counterexamples?

No formal gap selection until these questions can be answered coherently.

## 6. Existing work that remains useful

The earlier P2-R work is not discarded. It becomes one evidence branch inside the larger atlas.

Round-1 audit:

`audits/literature/P2R_TARGETED_FAILURE_DEEP_READ_ROUND1.md`

Compact prior-paper evidence:

`evidence/CORE_EVIDENCE_SNAPSHOT.md`

The prior direct set — BridgeSim, ReactSim-Bench, CausalDrive, *How Can Driving World Models Do Counterfactual Prediction?*, CRAFT, GameFormer, M2I, Bahram et al. — remains useful for interactive/reactive/counterfactual families, but is no longer the whole agenda.

## 7. Scientific operating rules

Read:

`state/RESEARCH_PRINCIPLES.md`

Core rules:

- field understanding before gap hunting;
- every paper gets both strongest evidence and strongest limitation;
- distinguish `AUTHOR CLAIM / DIRECT EXPERIMENTAL EVIDENCE / OUR INFERENCE`;
- missing module ≠ gap;
- action-conditioned ≠ reactive correctness;
- world fidelity ≠ decision sufficiency;
- visual rollout ≠ closed-loop planning evidence;
- modern terminology must be checked against older prediction/planning concepts;
- strong counterexamples are first-class evidence.

## 8. Fast new-session read order

For an ordinary continuation:

```text
1. START_HERE.md
2. state/CURRENT_STATE.md
3. state/NEXT_TASK.md
4. state/RESEARCH_PRINCIPLES.md
5. landscape/FIELD_RECONSTRUCTION_PLAN.md
6. landscape/FIELD_ATLAS.md
```

Then read only the relevant paper cards/raw MD/surveys needed for the current atlas task.

Read hypothesis files only when their historical evidence is relevant; do not default back to P2-R.

## 9. Source hierarchy

```text
Official/canonical paper PDF = exact source authority
GitHub raw MD + figures       = GPT-readable primary-text layer
Paper Card                    = curated paper knowledge
Field Atlas                   = cross-paper field understanding
State files                   = canonical project decisions
Chat                          = temporary reasoning workspace
```

If raw MD is ambiguous, verify against official/canonical PDF rather than guessing.

## 10. Division of labor

**GPT-5.6 Sol:** field census, deep reading, cross-paper synthesis, taxonomy/atlas maintenance, scientific interpretation, direct GitHub write-back.

**Local corpus agent:** bulk acquisition, canonical local PDF archive, MinerU conversion, metadata/QC, local source extraction, source-code execution, datasets/checkpoints/experiments.

## 11. Session closeout rule

Any session that materially changes the research must update the relevant state/atlas/card files before ending.

The repo — not conversation memory — is the research authority.
