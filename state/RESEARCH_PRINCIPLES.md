# RESEARCH_PRINCIPLES

Canonical scientific operating rules for this project.

Last updated: 2026-09-14

## 1. Scope

Primary research scope:

```text
World Model + End-to-End + Planning-centric autonomous driving
```

The project is not perception-centric and is not a generic world-generation project. A paper can be technically impressive yet peripheral if its contribution does not materially affect planning, decision making, interaction reasoning, evaluation of planning, or the coupling between future modeling and action selection.

## 2. Field understanding comes before gap hunting

This is now the highest-priority rule.

Forbidden workflow:

```text
read a few papers
→ guess a gap
→ search for papers that support/refute the guessed gap
→ design a method around the surviving wording
```

Required workflow:

```text
reconstruct the field
→ understand major method families and historical transitions
→ understand representations, supervision, planner interfaces and evaluation regimes
→ identify recurring trade-offs / contradictions / under-measured capabilities
→ only then formulate research problems
→ falsify them
→ only then design methods
```

P1/P2-R/P3 are historical probes. They must not determine the field map.

Canonical reconstruction plan:

`landscape/FIELD_RECONSTRUCTION_PLAN.md`

Canonical taxonomy:

`landscape/PLANNING_WAM_TAXONOMY.md`

## 3. Prior expertise is an asset, not a destination

The owner has strong prior expertise in driving risk, predictive risk fields, safety representation, future interaction compression and trajectory-based risk analysis.

This expertise may become useful, but **risk field is not a required component of the final research direction**.

Forbidden workflow:

```text
we know risk fields
→ search for a place to insert a risk field into WAM
```

Required workflow:

```text
field understanding
→ observed/recurrent planning problem
→ failure cause / missing capability
→ why existing methods do not already solve it
→ research question
→ test / falsification
→ only then inspect whether prior risk knowledge helps
```

A final contribution that uses none of the legacy risk-field machinery is acceptable if the problem is stronger.

## 4. Understand papers before judging them

Do not reduce papers to "supports our hypothesis" / "hurts our hypothesis".

For every anchor paper first reconstruct:

```text
What problem did the authors actually face?
Why did their design make sense at the time?
What is the exact data flow?
What is directly supervised?
What remains at inference?
How does the world model enter planning?
What benchmark regime is used?
What is the strongest evidence for the method?
What is the strongest limitation / alternative explanation?
What trade-off did the method choose?
What later work changed that trade-off?
```

Only after this understanding may the paper be used for research-problem synthesis.

## 5. Symmetric treatment of every paper

Every paper has strengths, limitations, assumptions and evaluation boundaries.

For every core paper, explicitly record:

```text
Strongest evidence in favor of the paper's claim
Strongest limitation / alternative explanation
What the paper proves
What the paper does NOT prove
Which trade-off it exposes
Which later papers support or contradict it
Which residual question remains
```

Do not attack papers merely because they threaten an existing idea; do not excuse weaknesses merely because they support one.

## 6. Evidence taxonomy

Keep separate:

```text
AUTHOR CLAIM
DIRECT EXPERIMENTAL EVIDENCE
OUR INFERENCE
```

If the paper does not report a failure, say:

```text
NO DIRECT OBSERVED FAILURE REPORTED
```

If a mechanism is plausible but untested, label it inference. If a metric is only a proxy, do not silently upgrade it into the target property.

## 7. Evaluation regimes must remain distinct

Never collapse:

```text
visual generation / reconstruction evaluation
motion-prediction evaluation
open-loop ego trajectory evaluation
NAVSIM / data-driven non-reactive evaluation
closed-loop non-reactive simulation
reactive closed-loop simulation
CARLA / Bench2Drive-style interactive simulation
real-vehicle closed-loop testing
```

A multi-step rollout is not automatically closed-loop. A candidate-conditioned predictor is not automatically reactive. A reactive simulator is not proof that a policy learned correct counterfactual dynamics.

## 8. Planning coupling must be traced concretely

For planning-centric WAM papers, always ask:

```text
What is the input?
What numerical world state is produced?
What future is predicted?
What is directly supervised?
What is latent / inferred / counterfactual?
How does the planner consume it?
Does it change candidate generation, direct decoding, scoring, refinement, optimization, reward or policy training?
What remains at inference time?
```

Do not infer decision usefulness from visual fidelity or representation richness alone.

## 9. Historical continuity matters

Do not assume a 2025–2026 WAM paper invented a planning concept merely because it uses new terminology.

Always check relevant predecessors in:

- interactive prediction + planning;
- conditional prediction;
- contingency planning;
- game-theoretic planning;
- model-predictive control;
- learned cost / value planning;
- closed-loop simulation.

Modern WAM novelty must be separated from older planning concepts enabled by new representations/models/data.

## 10. Counterexamples matter

One strong counterexample can kill a universal claim.

Examples already learned:

- DriveLaW weakens any claim that an explicit risk/value interface is always necessary.
- NPPC weakens any universal claim that optimization over a learned cost necessarily produces harmful exploitation.
- BeTop weakens broad claims that logged-data learning cannot yield useful reactive planning behavior.
- DA-WAM weakens broad claims that per-candidate action-conditioned futures are missing from planning-centric WAMs.

Use counterexamples to understand the field's conditional structure, not merely to kill hypotheses.

## 11. Reading-depth policy

Not all papers deserve equal effort.

### CENSUS
Enough to place a paper accurately in the field taxonomy and understand its historical role.

### ANCHOR
Deep read method, supervision, inference, evaluation, ablations, strengths, limitations and relation to neighboring families.

### DECISION
Anchor + targeted source/code audit only if needed to resolve a concrete scientific ambiguity.

### BACKGROUND
Retain for context without exhaustive analysis.

The field-census phase may contain ~50–80 papers, while only ~15–25 become anchor deep reads.

## 12. Corpus expansion policy

Expand by **field coverage and unresolved scientific structure**, not by keywords and not by a preselected gap.

During field reconstruction, broad expansion is allowed but must be controlled by the taxonomy: each new paper should fill a missing family, historical transition, benchmark regime, or counterexample role.

Avoid two failure modes:

```text
too few papers → blind hypothesis invention
too many papers → undigested archive
```

## 13. Problem-discovery gate

Do not formally select a gap until the field atlas can answer:

1. major method families and why they emerged;
2. exact observation→future→planner interfaces;
3. supervision availability and counterfactual limits;
4. action-conditioning/reactivity distinctions;
5. benchmark/evaluation meanings;
6. strongest non-WM planning baselines;
7. recurring trade-offs across multiple independent families;
8. strong counterexamples to common claims;
9. important capabilities that are under-measured rather than merely absent as modules;
10. contradictory evidence that remains unresolved.

Only then use the chain:

```text
Observed / recurrent planning difficulty
→ cause
→ missing capability or structural trade-off
→ why existing approaches cannot easily handle it
→ falsifiable research question
→ possible method
```

A missing module is not a gap. A new representation is not a gap. A fashionable architecture is not a gap.

## 14. Method-design gate

No method design until a problem survives:

1. field-level understanding;
2. direct prior-art attack;
3. strongest alternative explanations;
4. realistic evaluation relevance;
5. counterexamples;
6. a falsifiable test showing the problem exists and matters.

`NONE / EVIDENCE INSUFFICIENT` remains acceptable.

## 15. Status of P1 / P2-R / P3 during reconstruction

```text
P1 = RETIRED historical hypothesis
P2-R = PARKED PROBE, not active search target
P3 = PARKED BACKUP PROBE
```

Do not optimize the reading list to prove or kill P2-R. The field reconstruction may independently return to it, modify it, or make it irrelevant.

## 16. Research-state authority

The live operational order is deliberately small:

```text
README.md
state/CURRENT_STATE.md
state/NEXT_TASK.md
manifests/CORPUS_MANIFEST.csv
```

Use deep analyses, raw MD, source audits and historical records only when the live task requires them. `DECISION_LOG`, `RESEARCH_LEDGER`, `landscape/`, `hypotheses/` and `audits/` retain evidence or history; none overrides the live state above. The former `papers/cards/` layer is retired.

Conversation summaries are temporary. The repo is canonical.
