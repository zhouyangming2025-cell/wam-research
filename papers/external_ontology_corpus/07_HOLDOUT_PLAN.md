# Holdout and Blind-Test Plan

Status: enforceable protocol for future ontology promotion.

## 1. Why holdouts are mandatory

A taxonomy can always be repaired after reading each new paper. That does not demonstrate completeness. A candidate ontology must be frozen before evaluating a set of papers that did not participate in category design.

## 2. Holdout pools

Maintain at least four independent pools.

### H-A — recent autonomous-driving WAM

Reserve recent works not used to define the candidate revision, for example:

```text
SimWAM
WAM-Flow
recent risk-aware WM predictive-control papers
selected 2026 world-action / reactive driving WMs
```

Exact membership is frozen immediately before blind test to avoid leakage.

### H-B — robotics / manipulation

Reserve methods such as:

```text
Ctrl-World
ST-WAM
robot video-world-model policy evaluation
recent action-conditioned robot world models
```

Purpose: test whether a driving-derived ontology generalizes to another embodied-control domain.

### H-C — classical / non-driving model-based control

Reserve several methods not used in final candidate-codebook design, selected from:

```text
probabilistic learned dynamics
risk-sensitive MPC
ensemble MBRL
planning with uncertainty
model-based offline RL
```

Purpose: expose hidden driving-specific assumptions.

### H-D — strong boundary / non-WM systems

Reserve strong planners with predictive representations, simulators or candidate scoring that authors may or may not call world models.

Purpose: test admission criteria and false positives.

## 3. Freeze requirements before blind test

Before opening holdout methods at mechanism depth, record a signed/frozen candidate document containing:

```text
axis research questions
category definitions
admission/exclusion gates
projection priority if any
unknown / N/A semantics
examples already used in derivation
explicit non-examples
allowed attributes versus core categories
```

No silent edits are allowed during blind classification.

## 4. Blind-test record per artifact

For every holdout artifact:

```text
1. ontology-free mechanism reconstruction
2. projection under frozen codebook
3. classification confidence
4. information materially lost
5. collision with existing class?
6. requires new category?
7. requires definition edit?
8. requires new attribute only?
9. human-readable reconstruction true/false?
```

## 5. Outcome codes

```text
PASS-A
  clean classification; no codebook or definition changes

PASS-B
  classification clean; only non-core audit attribute needed

WARN
  coarse class works but important mechanism distinction is lost

FAIL-DEF
  existing category requires definition change

FAIL-SPLIT
  one category must split

FAIL-NEW
  genuinely new category required

FAIL-AXIS
  missing independent research question / axis
```

## 6. Promotion thresholds

A human-level ontology should not be promoted to stable domain map if:

- any holdout produces `FAIL-AXIS`;
- more than one independent holdout forces the same `FAIL-NEW` or `FAIL-SPLIT`;
- categories depend on architecture names to resolve ambiguity;
- unknowns are silently converted to absence;
- a human-readable mechanism sentence is materially false even when the code is syntactically valid.

Recommended S2-like external gate:

```text
>=15 holdout artifacts
>=3 evidence domains
>=80% PASS-A
remaining mostly PASS-B
zero unresolved FAIL-AXIS
zero repeated FAIL-NEW
```

The exact threshold is a project policy, not a statistical guarantee.

## 7. Counterexample attack before holdout

Before freezing the candidate ontology, adversarially search derivation papers for:

```text
training-only world → reactive runtime
current belief/model state → direct actor
predictive hidden state → direct actor
single future endpoint → direct action
multi-step future rollout → scorer
continuous MPC / CEM
MCTS / tree search
differentiable learned tree
joint world-action generation
world generation terminal output
model used only as simulator for policy training
surrogate future state after teacher deletion
direct scorer distilled from world criterion
reactive versus non-reactive environment response
stochastic/risk-sensitive planning
```

If any has no natural representation before holdout, the codebook is not ready.

## 8. Leakage policy

A paper mentioned by title in a survey can still be a holdout if its decision-critical method details were not inspected. A paper already reconstructed at RD2+ for ontology design cannot be used as a true holdout.

Maintain a ledger:

```text
UNSEEN
DISCOVERY_ONLY (RD0)
ABSTRACT_SEEN (RD1)
DERIVATION_USED (RD2+)
HOLDOUT_OPENED
```

## 9. Current reserved candidates

As of creation, the external track should avoid mechanism-deep-reading the following until a revised candidate codebook is frozen, unless they are explicitly removed from holdout first:

```text
SimWAM
WAM-Flow
one recent risk-aware WM-MPC driving paper
Ctrl-World
ST-WAM
at least two recent robotics world-action papers
at least three probabilistic/risk-sensitive MBRL methods not yet in the foundational ledger
```

This list is intentionally mixed across domains.

## 10. Final criterion

The goal is not to achieve zero surprises. The goal is to make surprises scientifically diagnostic.

A good ontology should absorb implementation novelty while changing only when a paper introduces a genuinely new causal/semantic mechanism.
