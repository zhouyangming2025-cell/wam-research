# NEXT_TASK

## 唯一下一任务

> **Adversarially validate the Tier-1 WAM scientific tensions against broader literature and falsification logic before any research-gap or method proposal.**

The 11-anchor consolidation gate is now complete.

Completed synthesis artifacts:

```text
landscape/WAM_MECHANISM_FAMILIES_V2.md
landscape/WAM_DESIGN_SPACE_MAP_V2.md
audits/research_synthesis/WAM_11_ANCHOR_COMPARABILITY_QA.md
landscape/WAM_EVIDENCE_STRENGTH_MATRIX.md
landscape/WAM_RESEARCH_TENSIONS_V1.md
```

Canonical coordinate system remains Ontology V1.3.

---

# Why the next step changes

The anchor set is now sufficiently normalized that reading paper 12 by default has lower value than attacking the scientific tensions already exposed.

The objective is no longer:

```text
find another interesting mechanism
```

but:

```text
determine whether an apparent tension is already resolved by prior art,
merely benchmark-specific,
or genuinely survives adversarial falsification.
```

---

# Tier-1 tensions to validate

## T2 — Explicit consequence rollout vs compact world-state conditioning

Competing hypotheses:

```text
H1 explicit action-conditioned rollout is necessary for hard interactive decisions
H2 compact decision-relevant world state is sufficient for most decisions
```

Core anchors:

```text
WoTE / WorldDrive / World4Drive
vs
GraphWorld / Epona
```

Required broader search:

```text
model-based RL / latent planning
MPC / value-equivalent models
policy distillation from world models
compact sufficient-state / bisimulation-like representations
end-to-end AD consequence modeling
```

Mandatory question:

> Has the field already tested rollout-vs-compact-conditioning under matched compute/data and interaction difficulty?

---

## T3 — Training-time world modeling vs deployment-time model-basedness

Competing hypotheses:

```text
H1 world modeling is mainly useful as a training regularizer / representation teacher
H2 online world inference is necessary for rare, OOD, or interaction-heavy decisions
```

Core anchors:

```text
LAW / Drive-JEPA / Metis / DynFlowDrive / Discrete-WAM
vs
WorldDrive / World4Drive / WoTE / SeerDrive / GraphWorld
```

Required broader search:

```text
world-model distillation
policy learning from imagined data
Dreamer-style latent planning vs actor-only deployment
teacher-student model-based control
test-time planning vs compiled policy
```

Mandatory question:

> Under matched training information, what failures remain after world knowledge is compressed into policy parameters?

---

## T5 — Factual-future learning vs intervention-correct consequence modeling

Competing hypotheses:

```text
H1 large factual datasets + action conditioning generalize adequately to intervention consequences
H2 observational/factual training is insufficient when ego action changes other agents' responses
```

Core anchors:

```text
World4Drive / Epona / Metis / DynFlowDrive / Discrete-WAM
WoTE as partial pseudo-simulation control
```

Required broader search:

```text
causal world models
counterfactual prediction
interactive motion forecasting
game-theoretic prediction
reactive simulation
interventional imitation / offline RL
causal representation learning for control
```

Mandatory question:

> Is there direct evidence that factual future prediction accuracy transfers to intervention-response accuracy in autonomous driving?

---

## T6 — Structured interaction semantics vs true reactive dynamics

Competing hypotheses:

```text
H1 strong interaction representation captures most practical safety benefit
H2 negotiation-heavy scenarios require explicit response-to-ego modeling
```

Core anchors:

```text
GraphWorld
vs
WoTE / reactive-simulation literature
```

Required broader search:

```text
interactive prediction
joint multi-agent forecasting
conditional response prediction
negotiation / merging / yielding
closed-loop reactive simulation
multi-agent planning
```

Mandatory question:

> On which scenario classes does static/observational interaction encoding fail relative to ego-conditioned reactive prediction?

---

# Required output

Create:

```text
audits/research_synthesis/WAM_TIER1_TENSION_ADVERSARIAL_REVIEW.md
```

For each tension include:

```text
1. exact competing hypotheses
2. broader prior-art search space
3. strongest evidence for H1
4. strongest evidence for H2
5. benchmark/evaluation confounds
6. whether the tension survives prior art
7. falsification experiment
8. minimum data/simulator/source requirements
9. novelty risk
10. verdict:
   RESOLVED / PARTIALLY RESOLVED / SURVIVES / INSUFFICIENT EVIDENCE
```

Optional supporting file if needed:

```text
landscape/WAM_TIER1_PRIOR_ART_MATRIX.md
```

---

# Search policy

Do not restrict the search to papers already in the 11-anchor set.

Use broader adjacent literatures when scientifically relevant:

```text
autonomous-driving WAM
interactive motion prediction
reactive simulation
model-based RL
latent dynamics / value-equivalent models
counterfactual/causal learning
planning distillation
multi-agent decision making
```

But every imported paper must be used for a specific tension/question, not added merely to enlarge the corpus.

---

# Evidence policy

Prioritize:

```text
matched ablations
controlled benchmark comparisons
source-code evidence
intervention/reactive evaluation
negative results
```

over:

```text
headline SOTA tables
author positioning
survey taxonomy alone
```

Keep benchmark regimes normalized:

```text
open-loop
non-reactive pseudo-simulation
reactive simulator closed loop
real-world closed loop
```

---

# Stop condition

A Tier-1 tension can advance toward `candidate research problem` only if:

```text
1. it survives broader prior-art attack;
2. the unresolved part is stated narrowly;
3. a falsifying experiment is feasible;
4. success/failure criteria are measurable;
5. the claim is not merely an ontology empty cell;
6. there is evidence that solving it matters for planning.
```

Until then:

```text
NO final research-gap declaration
NO method design
NO claim that risk field is the solution
NO novelty claim
```
