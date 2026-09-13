# CURRENT_STATE

Last updated: 2026-09-14 — field census Round 1 complete

## Research north star

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Planning is the center of gravity. Perception, video generation, JEPA/latent prediction, VLA, safety/risk modeling and simulation are supporting means, not the project identity.

**Risk field is optional, not required.** Prior risk/predictive-risk expertise is an asset, not a destination.

Canonical rules: `state/RESEARCH_PRINCIPLES.md`.

## Major methodological reset

The previous workflow moved too quickly from a small, hypothesis-biased paper set to candidate gaps (P1/P2-R/P3). That is now considered an insufficient basis for research-problem selection.

Active rule:

```text
FIELD UNDERSTANDING FIRST
→ reconstruct the planning-centric WAM landscape
→ understand method families, historical transitions, planner interfaces, supervision, evaluation and trade-offs
→ only then reopen problem/gap discovery
```

Canonical plan:

`landscape/FIELD_RECONSTRUCTION_PLAN.md`

Canonical taxonomy:

`landscape/PLANNING_WAM_TAXONOMY.md`

Living map:

`landscape/FIELD_ATLAS.md`

## Hypothesis status during reconstruction

| item | status |
|---|---|
| **P1_RETIRED — Planner-Induced Model Exploitation / Search-Support Gap** | RETIRED HISTORICAL HYPOTHESIS |
| **P2R_PRIMARY — Reactive Action-Ordering Gap** | **PARKED PROBE — NOT ACTIVE SEARCH TARGET** |
| **P3_HOLD — Decision Sufficiency of World Representations** | PARKED BACKUP PROBE |

`P2R_PRIMARY.md` retains the prior formulation for provenance, but the reading program must no longer be optimized around proving/killing P2-R.

## Current active stage

```text
FIELD RECONSTRUCTION — Planning-centric WAM Atlas
```

### Phase-A Round 1 status

The first neutral breadth census has started and is recorded in:

`landscape/CENSUS_PHASE_A_ROUND1.md`

Round 1 provisionally places roughly **45 unique works / benchmarks / controls** across the field, covering:

- visual/video generative WMs;
- occupancy/BEV/geometric WMs;
- latent/JEPA/predictive-representation WMs;
- WM-assisted direct planning;
- candidate/action-conditioned futures;
- unified world-action models;
- interactive prediction/planning predecessors;
- reactive simulation / policy-training environments;
- reward/value/safety/cost interfaces;
- strong non-WM E2E planners;
- benchmark/evaluation lineages.

No gap or innovation verdict has been issued.

### Structural distinctions already visible from census placement

These are **field-map distinctions**, not research gaps:

1. `world model` plays several non-equivalent roles: data generator, pretraining model, auxiliary objective, inference-time future model, candidate evaluator, reward/safety model, simulator, or joint world-action policy.
2. `latent world model` is also not one paradigm: some future branches disappear at inference; others directly condition the planner; newer WAMs jointly model scene/action latents.
3. `action conditioned` does not identify the planner interface: the action may condition video generation, occupancy prediction, candidate scoring, or joint action/world generation.
4. `closed loop` spans fundamentally different regimes: NAVSIM non-reactive pseudo-simulation, CARLA interactive simulation, learned reactive world agents, photorealistic reconstructed simulation, and real vehicle.
5. Modern WAM interaction ideas have substantial predecessors in conditional prediction, contingency planning and game-theoretic integrated prediction/planning.
6. Strong non-WM planners are mandatory controls because planning gains can come from representation, trajectory distribution learning, candidate scoring or supervision without an explicit world model.

These distinctions will be tested and refined through anchor deep reads rather than converted into premature problem statements.

## Field-reconstruction depth

Planned structure:

```text
Phase A: ~50–80 paper census at placement/overview depth
Phase B: ~15–25 representative anchor deep reads
Phase C: cross-family synthesis + historical evolution + evaluation map + trade-off map
Phase D: only then reopen research-problem discovery
```

Phase A is active. Round 2 now fills missing coverage rather than expanding by gap keywords.

## Immediate next task

See `state/NEXT_TASK.md`.

Round-2 coverage priorities:

- Hydra-MDP / DriveSuprim / iPad / VLA planning controls;
- Think2Drive / WM-RL lineage;
- ViDAR / GenAD representation-pretraining bridges where planning-relevant;
- benchmark evolution and operational/deployment properties;
- uncertainty / multimodal future treatment;
- credible real-vehicle closed-loop evidence, if any.

## Corpus / Research Brain architecture

1. Canonical PDFs live only on local/NAS where available.
2. GitHub raw MD + figures form the persistent GPT-readable primary-text layer.
3. Public official PDFs/web sources can be read directly during field census/deep read; local ingestion can follow asynchronously.
4. Paper Cards contain curated scientific knowledge after deep review.
5. `landscape/` now contains field-level understanding; hypothesis files are no longer the organizing center during reconstruction.
6. Local corpus agent handles acquisition/conversion/local code; GPT-5.6 Sol handles field synthesis, deep reading and direct GitHub state maintenance.

## New-session bootstrap

A fresh session should begin with:

```text
START_HERE.md
state/CURRENT_STATE.md
state/NEXT_TASK.md
landscape/FIELD_ATLAS.md
```

During field reconstruction, do not default to `hypotheses/P2R_PRIMARY.md` unless historical hypothesis context is specifically needed.