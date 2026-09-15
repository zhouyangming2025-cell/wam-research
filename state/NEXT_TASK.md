# NEXT_TASK

## 唯一下一任务

> **Re-project World4Drive under the dimension-first WAM framework** as the fifth ontology-discovery anchor.

## Current status

```text
P0048 LAW          COMPLETE v2
P0045 WoTE         COMPLETE v2
P0001 Epona        COMPLETE v2
P0042 WorldDrive   COMPLETE v2
P0046 World4Drive  NEXT — dimension-first re-projection
```

Canonical analyses:

```text
papers/deep_analysis/P0048_LAW_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0045_WOTE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0001_EPONA_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0042_WORLDDRIVE_DEEP_ANALYSIS_V2.md
landscape/WAM_DIMENSION_DISCOVERY_LOG.md
landscape/WAM_DIMENSION_DISCOVERY_ADDENDUM_EPONA_WORLDDRIVE.md
```

Existing World4Drive audit:

```text
audits/literature/PHASE_C5_WORLD4DRIVE_AUDIT.md
```

## Why World4Drive is the final pre-ontology anchor

The four completed anchors now expose four different future-knowledge lifecycles:

```text
LAW
= future prediction as auxiliary representation shaping

WoTE
= compact learned world transition stays online
  → recurrent candidate future → reward → select

Epona
= visual future jointly shapes shared historical latent
  → direct generative trajectory policy at planning inference

WorldDrive
= heavy generative future teacher
  → distilled compact future surrogate
  → online candidate reward/ranking
```

World4Drive appears to provide a fifth configuration:

```text
candidate/intention trajectory
→ compact predicted future world latent online
→ ScoreNet
→ select trajectory
```

But its supervision is unusual: K predicted candidate futures are compared against one factual observed future latent. This must be analyzed without calling it true counterfactual supervision.

## World4Drive re-projection target

Trace and compare at minimum:

```text
1. current physical/world latent construction
2. spatial/depth foundation prior contribution
3. semantic/VLM prior contribution
4. temporal-history aggregation
5. intention vocabulary construction and support
6. number K of intentions/candidates and how each candidate is produced
7. candidate trajectory representation → action token
8. exact candidate-specific future-latent predictor
9. whether future prediction is one-step, recurrent, deterministic, stochastic
10. whether K future branches share parameters/queries
11. exact observed future latent used as target
12. how one factual future supervises K candidate-conditioned outputs
13. reconstruction/alignment loss and which candidate receives it
14. ScoreNet target construction
15. whether ScoreNet learns value, factual-mode matching, or both
16. candidate trajectory supervision and winner selection
17. consequence truth source vs value/classification truth source
18. counterfactual output level vs counterfactual supervision level
19. other-agent reactivity evidence
20. inference graph: what future computation remains active online
21. future-object explicitness and deployment cost
22. candidate generation vs future predictor vs ScoreNet attribution
23. representation-prior attribution vs WM attribution
24. strongest matched ablations
25. relation to LAW/WoTE/Epona/WorldDrive on every stable dimension
```

## Special hypotheses to test

### H1 — World4Drive may be online latent foresight, but not true alternative-future supervision

Audit the distinction:

```text
K candidate-specific predicted future latents = YES
K observed/simulated ground-truth alternative futures = likely NO
```

Do not infer causal counterfactual correctness from branch multiplicity.

### H2 — ScoreNet may be closer to mode/factual-future matching than consequence value estimation

Existing audit indicates the training target is based on which predicted future latent is closest to the single factual future latent.

Test whether the deployed score means:

```text
“this action leads to a good/safe future”
```

or more narrowly:

```text
“this candidate's predicted future most resembles the factual demonstrated future”
```

This distinction is central when comparing World4Drive with WoTE/WorldDrive reward models.

### H3 — foundation priors may explain part of the gain independently of future modeling

Separate:

```text
metric-depth prior
semantic/VLM prior
temporal latent construction
future prediction
ScoreNet selection
```

before assigning performance gains to the world model.

### H4 — World4Drive may force a new split between `value` and `factual-consistency score`

Current ontology has consequence model vs value model. World4Drive may show that the post-future scorer can instead learn **which imagined mode matches the observed demonstration**, which is not identical to safety/utility value.

If confirmed, add a distinct dimension:

```text
scorer semantics:
utility/value
imitation/factual consistency
mode posterior
risk/safety
hybrid
```

## Required output

Create:

```text
papers/deep_analysis/P0046_WORLD4DRIVE_DEEP_ANALYSIS_V2.md
```

and record any new/split dimensions in the discovery addendum.

## Stop condition

World4Drive is complete only when we can state without ambiguity:

```text
what each of K future latents means
what supervises each branch
what ScoreNet's probability/score semantically represents
why the selected trajectory is preferred
what part is genuinely world modeling
what part is intention/candidate generation
what part is factual-future matching/value learning
```

## After World4Drive — mandatory synthesis before new papers

Do NOT immediately move to SeerDrive.

First perform:

```text
LAW + WoTE + Epona + WorldDrive + World4Drive
→ merge/split provisional dimensions
→ WAM_DIMENSION_ONTOLOGY_V1.md
→ WAM_COMPARISON_MATRIX_V1.md
```

Only then resume:

```text
SeerDrive
Drive-JEPA
Metis
DynFlowDrive
Discrete-WAM
GraphWorld
```

## Still forbidden

```text
no research-gap declaration
no method design
no forced risk-field insertion
no novelty conclusion from missing cells
```
