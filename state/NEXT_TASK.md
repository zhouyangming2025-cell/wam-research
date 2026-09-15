# NEXT_TASK

## 唯一下一任务

> **Re-project WorldDrive under the dimension-first WAM framework** using the existing paper+code audit, instead of treating the prior audit as a finished isolated-paper analysis.

## Why this is next

The first three ontology-discovery anchors are now complete at v2 first-pass depth:

```text
P0048 LAW    COMPLETE — predictive auxiliary / representation shaping
P0045 WoTE   COMPLETE — online consequence → value → candidate selection
P0001 Epona  COMPLETE — shared world representation + direct generative policy + sibling visual generator
```

Canonical analyses:

```text
papers/deep_analysis/P0048_LAW_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0045_WOTE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0001_EPONA_DEEP_ANALYSIS_V2.md
landscape/WAM_DIMENSION_DISCOVERY_LOG.md
```

The next step is not broad reading. WorldDrive already has a strong primary-paper + source-code audit:

```text
audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md
```

What is missing is projection onto the common dimension space.

## WorldDrive re-projection target

Trace and compare at minimum:

```text
1. historical/current world representation and its semantics
2. TA-DWM future target and dynamics operator
3. trajectory vocabulary construction: anchor source, count, residual refinement, train/test support
4. expert trajectory vs candidate trajectory conditioning in different stages
5. which representations are learned in Phase 1 and transferred/frozen in Phase 2
6. exact parameter/representation ownership across world model and planner
7. candidate generator before FAR: what planning capability exists without future-aware rewarder
8. FAR teacher: what exact candidate-conditioned future latent is produced by frozen TA-DWM
9. FAR student: what representation is distilled and which gradients flow where
10. reward/value semantics: simulator rewards, imitation score, future-aware reward
11. consequence model vs value model separation
12. whether expensive visual diffusion is active at deployment
13. candidate breadth × future richness × deployment latency trade-off
14. factual/candidate-specific/counterfactual supervision level
15. other-agent reactivity of candidate-future supervision
16. world-state truth source vs reward/value truth source
17. representation inheritance gain vs future-aware scoring gain: keep attribution separate
18. strongest matched ablations for generic VAE pretraining, TA-DWM vision, TA-DWM motion, FAR
19. quality/fidelity evidence vs planning evidence
20. exact relation to LAW / WoTE / Epona on every relevant dimension
```

## Special hypotheses to test

### H1 — WorldDrive may be a hybrid of LAW/Epona-like training shaping and WoTE-like online selection

Test:

```text
Phase 1 world generation
→ learned vision/motion representation
→ transferred/frozen planner representation
```

versus:

```text
candidate
→ distilled future representation
→ future-aware reward
→ selection
```

Do not collapse these into one “world model helps planning” claim.

### H2 — distillation may be the key deployment mechanism

Compare:

```text
WoTE       full compact BEV rollout online
World4Drive compact latent predictor online
WorldDrive expensive generative WM teacher offline/training
           → lightweight future surrogate online
Epona      visual branch disabled in planning mode
LAW        future branch not consumed by action selection
```

This may expose a stable dimension around **where expensive world imagination is paid**.

### H3 — candidate vocabulary may be an independent source of gain

WorldDrive has a large trajectory vocabulary and a strong pre-FAR planner. Separate:

```text
candidate support
candidate refinement
simulator/reward heads
future-aware distillation
```

before attributing performance to the world model.

## Required output

Create:

```text
papers/deep_analysis/P0042_WORLDDRIVE_DEEP_ANALYSIS_V2.md
```

Then use the WorldDrive + existing three anchors to refine the dimension system. Do not freeze ontology yet; World4Drive remains the fifth required anchor.

## Stop condition

WorldDrive re-projection is complete only when the following statement can be decomposed into separately evidenced mechanisms:

> “WorldDrive bridges generation and planning.”

Specifically, we must know exactly what part is:

```text
representation pretraining
representation transfer/freeze
candidate generation
candidate scoring
future representation teacher
future representation distillation
online value/ranking
```

and how each differs from LAW, WoTE and Epona.

## After WorldDrive

```text
World4Drive re-projection
→ first merge/split pass
→ WAM_DIMENSION_ONTOLOGY_V1.md
→ WAM_COMPARISON_MATRIX_V1.md
```

Only after that resume SeerDrive / Drive-JEPA / Metis / DynFlowDrive / Discrete-WAM / GraphWorld.

## Still forbidden

```text
no research-gap declaration
no method design
no forced risk-field insertion
no novelty conclusion from empty dimensions
```
