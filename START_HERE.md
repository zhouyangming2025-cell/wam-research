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

The project previously moved too quickly from a small paper set to candidate gaps (P1/P2-R/P3). That workflow is suspended.

Active rule:

```text
UNDERSTAND THE FIELD FIRST
→ reconstruct planning-centric WAM families and historical evolution
→ understand representations, supervision, planner interfaces, interaction/reactivity and evaluation
→ identify recurring trade-offs / contradictions / under-measured capabilities
→ only then reopen research-problem / gap discovery
```

Canonical plan: `landscape/FIELD_RECONSTRUCTION_PLAN.md`

Taxonomy: `landscape/PLANNING_WAM_TAXONOMY.md`

Living atlas: `landscape/FIELD_ATLAS.md`

## 3. Current hypothesis state

Hypotheses are not driving the reading program.

```text
P1_RETIRED  = retired historical hypothesis
P2-R        = parked probe — not active search target
P3          = parked backup probe
```

## 4. Current active stage

```text
FIELD RECONSTRUCTION — Phase-A closeout
```

The breadth-acquisition target has been reached:

```text
60 stable IDs: P0001–P0060
58 RAW_MD_READY
2 lawful-source blockers: P0008 NPPC, P0020 Bahram 2016
```

So the current task is **not more bulk ingestion**. It is to finish scientific census placement, audit family coverage, freeze Phase A, and select the representative Phase-B deep-read anchors.

## 5. Current map status

`landscape/CENSUS_PHASE_A_ROUND1.md` provisionally places roughly 45 works / benchmarks / controls across the field.

The local agent has since added full text for:

- P0013–P0020 interactive/reactive/counterfactual branch;
- P0021–P0034 Round-2 coverage works;
- P0035–P0060 works already named in the Round-1 census.

The infrastructure is ahead of the scientific map. The newly ingested P0021–P0034 still need neutral census placement by GPT/owner.

## 6. Immediate task

Read `state/NEXT_TASK.md`.

In short:

1. census-read P0021–P0034;
2. create `landscape/CENSUS_PHASE_A_ROUND2.md`;
3. update `FIELD_ATLAS.md` and run an explicit F1–F11 coverage audit;
4. add another paper only if a concrete missing family/transition remains;
5. freeze Phase-A breadth expansion;
6. select ~15–25 representative Phase-B anchor papers.

Do not design a method and do not declare a gap during this closeout.

## 7. What the field atlas must eventually explain

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

## 8. Fast new-session read order

```text
1. START_HERE.md
2. state/CURRENT_STATE.md
3. state/NEXT_TASK.md
4. state/RESEARCH_PRINCIPLES.md
5. landscape/FIELD_ATLAS.md
6. landscape/CENSUS_PHASE_A_ROUND1.md
```

Then read only the raw MD needed for the active census-placement or anchor-deep-read task.

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

**GPT-5.6 Sol:** census placement, field synthesis, primary-paper reading, anchor selection/deep reads, atlas/state maintenance, scientific judgement.

**Local corpus agent:** bulk acquisition, canonical local PDF archive, MinerU conversion, metadata/QC, source extraction, local code execution, datasets/checkpoints/experiments.

The repo — not conversation memory — is the research authority.
