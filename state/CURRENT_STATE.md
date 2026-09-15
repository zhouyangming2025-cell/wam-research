# CURRENT_STATE

Last updated: **2026-09-15 — Tier-1 WAM adversarial validation COMPLETE; candidate-problem formulation NEXT**

## Research north star

```text
WAM / World Model + one-stage End-to-End + Planning-centric autonomous driving
```

Core WAM remains primary. WAM+VLA is secondary/control. Risk/predictive-risk remains optional prior knowledge, not a required destination.

## Methodology in force

```text
FIELD UNDERSTANDING FIRST
→ core-WAM coverage
→ comparative anchor deep reads
→ dimension-first normalization
→ comparability/evidence QA
→ adversarial prior-art attack
→ falsifiable candidate-problem formulation
→ falsification
→ only then method design
```

Current phase:

```text
Phase C.5 core-anchor stress tests       COMPLETE
11-anchor Design Space Consolidation     COMPLETE
Comparability / evidence QA              COMPLETE
Tier-1 broader-literature adversarial QA COMPLETE
Candidate research-gap declaration       NOT YET AUTHORIZED
Method design                            NOT YET AUTHORIZED
```

---

# Canonical anchor set

```text
LAW | WoTE | Epona | WorldDrive | World4Drive | SeerDrive
Drive-JEPA | Metis | DynFlowDrive | Discrete-WAM | GraphWorld
```

Canonical ontology:

```text
WAM Ontology V1.3 — RETAINED
```

Canonical synthesis:

```text
landscape/WAM_MECHANISM_FAMILIES_V2.md
landscape/WAM_DESIGN_SPACE_MAP_V2.md
audits/research_synthesis/WAM_11_ANCHOR_COMPARABILITY_QA.md
landscape/WAM_EVIDENCE_STRENGTH_MATRIX.md
landscape/WAM_RESEARCH_TENSIONS_V1.md
```

Latest adversarial validation:

```text
audits/research_synthesis/WAM_TIER1_TENSION_ADVERSARIAL_VALIDATION_V1.md
landscape/WAM_RESEARCH_TENSIONS_V2_VALIDATED.md
```

Source completeness authority:

```text
audits/research_synthesis/CORE_ANCHOR_SOURCE_COMPLETENESS_AUDIT.md
```

---

# Stable field-level design-space conclusions

Do not use a scalar `world-model strength` notion. Keep separate:

```text
1. environmental future-modeling strength
2. decision relevance of the world representation
3. training-time jointness / gradient coupling
4. deployment-time online world dependence
```

Also keep separate:

```text
representation shaping
online world-state conditioning
online candidate consequence prediction
explicit utility/value
search/selection over alternatives
```

Training-time unification and deployment-time model-basedness remain orthogonal.

---

# Tier-1 tension verdicts after broader prior-art attack

## T2 — Explicit rollout vs compact conditioning

```text
VERDICT: SURVIVES — NARROWED
```

External controls from value-equivalent modeling, value-aware model learning, DeepMDP/bisimulation, MuZero, TD-MPC2 and I2A establish that full observation-faithful world modeling is not universally necessary.

Still unresolved:

```text
When does online action-conditioned branching add decision information
that cannot be amortized into a compact world state/policy under matched compute/data?
```

---

## T3 — Training-time world modeling vs deployment-time model-basedness

```text
VERDICT: PARTIALLY RESOLVED
```

MBPO / Dreamer-family work shows useful world-model reasoning can train a policy without per-decision online rollout. WPT (CVPR 2026) directly demonstrates autonomous-driving world-to-policy distillation with substantial inference acceleration while retaining most gains.

Online planning remains strongly viable in MuZero / TD-MPC2 and in WAM anchors such as WoTE / World4Drive.

Surviving question:

```text
Which consequence information is amortizable into policy weights,
and which must be recomputed online under uncertainty / OOD / interaction?
```

---

## T5 — Factual future vs intervention-correct consequence

```text
VERDICT: PARTIALLY RESOLVED — H2 STRONGLY STRENGTHENED
```

The project rule:

```text
action-conditioned output != counterfactual truth
```

is now supported by direct external evidence, not only anchor synthesis.

`How Can Driving World Models Do Counterfactual Prediction?` (arXiv:2608.11601, 2026-08) constructs matched CARLA counterfactual ground truth and shows representative direct action-conditioned driving WMs fail to recover episode-specific counterfactuals.

Important remaining boundary:

```text
episode-specific short-horizon counterfactual
!=
reactive multi-agent intervention consequence
```

The reactive case remains unresolved.

---

## T6 — Structured interaction semantics vs true reactive dynamics

```text
VERDICT: SURVIVES — NARROWED
```

Prior art already includes:

```text
M2I conditional influencer→reactor prediction
GameFormer game-theoretic interaction reasoning
DIPP joint prediction-planning
TrafficBots recurrent reactive simulation
WOSAC / Waymax interactive sim-agent evaluation
reaction-uncertainty-aware conditional planning
```

Therefore `model reactions to ego plans` is NOT a novelty claim.

Surviving question:

```text
What marginal planning value does explicit ego-conditioned reaction modeling add
beyond a strong interaction-aware latent representation,
as response dependence / negotiation difficulty increases?
```

---

# New counterfactual vocabulary rule

Always distinguish:

```text
conditional prediction
p(Y | H, a)

interventional prediction
p(Y | H, do(a))

episode-specific counterfactual
p(Y_a | H, factual evidence)

reactive multi-agent counterfactual simulation
alternative ego intervention + endogenous agent responses
```

Never infer a higher level from action-conditioning alone.

---

# Cross-tension convergence

T2 + T3 + T6 now point to a deeper question:

> **What future reasoning must be computed online for THIS scene, and what can be amortized into compact state/policy representations?**

Potential discriminating variables:

```text
interaction response dependence
reaction uncertainty / multimodality
scene rarity / OOD distance
candidate ambiguity
irreversibility / safety cost
model confidence / epistemic uncertainty
```

This is an organizing scientific question, NOT yet a method proposal.

---

# Immediate next task

See `state/NEXT_TASK.md`.

Next phase:

```text
candidate-problem formulation + nearest-neighbor 2025–2026 overlap check
```

Still forbidden:

```text
NO final research-gap declaration yet
NO method architecture proposal
NO forced risk-field insertion
NO novelty claim from terminology alone
```
