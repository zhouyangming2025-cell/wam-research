# External Ontology Corpus Protocol

Status: normative protocol for the external ontology-audit track.

## 1. Objective

Build a literature evidence base large and diverse enough to decide whether the project's mechanism dimensions should be kept, modified, split, merged, renamed, or deleted.

The corpus is not a bibliography contest. It is a mechanism-evidence program.

## 2. Unit of analysis

The default unit is an **artifact**, not a paper title:

```text
artifact = paper/version × task mode × deployment route × material implementation variant
```

A paper may therefore contribute several artifacts when planning, world generation, policy learning, code and paper materially differ.

## 3. Two-stage recording rule

### Stage A — ontology-free reconstruction

Record only what the paper/system does:

```text
observations
explicit state objects
action/control variables
transition/prediction operators
future objects
candidate identity
search/optimization/selection
reward/value/cost/criterion
policy/action output
training targets and gradient routes
runtime retained/dropped/bypassed modules
online clocks / physical horizon / control cycles
```

Do **not** assign R/W/E/L or C/X/D/P/V/T/L while doing the first reconstruction.

### Stage B — candidate-ontology projection

Only after the mechanism graph is frozen may the artifact be projected into candidate ontology versions. Disagreement between the graph and the projection is evidence against the ontology, not against the paper.

## 4. Inclusion strategy

Use stratified evidence, not popularity sampling.

Required strata:

1. predictive-state / belief-state foundations;
2. classic model-based RL and Dyna-style planning;
3. latent-state online MPC / trajectory optimization;
4. tree-search learned models;
5. imagination-based actor/value learning;
6. world-model policy training where the model disappears at deployment;
7. video/generative world models;
8. geometric/occupancy/BEV world models;
9. latent/JEPA predictive world models;
10. candidate-conditioned consequence evaluators;
11. unified/joint world-action systems;
12. reactive simulators and learned environment agents;
13. robotics manipulation/navigation world models;
14. autonomous-driving planning world models;
15. strong non-WM planners and model-free controls.

## 5. Corpus tiers

### Tier C — census

Target: 150–300 entries.

Purpose: coverage and novelty detection. RD0–RD1 is acceptable. Tier C cannot justify a major ontology revision by itself.

### Tier A — anchor

Target: 50–100 mechanism-relevant papers. Minimum RD2, preferred RD3.

Purpose: cover major mechanism families with enough detail to reconstruct causal graphs.

### Tier D — decision-critical

Target: 25–50 papers. RD3–RD4.

Purpose: adjudicate difficult boundaries, collisions and apparent ontology failures.

### Tier H — holdout

At least 15–25 papers must remain outside ontology construction until a candidate codebook is frozen.

Purpose: genuine blind classification and change-pressure test.

## 6. Reading-depth standard

```text
RD0 metadata only
RD1 abstract + intro + contribution claims
RD2 method figures + core equations + inference/training overview
RD3 full mechanism reconstruction including losses, inference, ablations and evidence limits
RD4 RD3 + source/code audit for decision-critical edges
```

Every synthesis claim should state the minimum evidence depth on which it rests.

## 7. Source hierarchy

Preferred order:

```text
1. primary paper / official proceedings
2. official project page / author repository
3. released source code
4. authoritative survey used for discovery/context
5. secondary commentary only for navigation
```

Do not infer deployment topology from a survey when the primary source is available.

## 8. Copyright and storage policy

The repository stores:

- bibliographic metadata;
- source URLs;
- our own mechanism reconstructions;
- evidence ledgers;
- short quotations where needed;
- derived DAGs and comparison tables;
- legally reusable source/code material when appropriate.

Do not mass-copy copyrighted full papers into the repository merely because they are publicly readable. Existing user-owned/raw paper assets are unaffected.

## 9. Mechanism evidence standard

A proposed distinction is admitted only if at least one artifact pair satisfies:

```text
same neighboring fields / implementation substrate
+ one targeted mechanism difference
+ materially different decision or learning causal graph
```

A proposed distinction is demoted when deleting/changing it preserves the mechanism-level explanation across tested artifacts.

## 10. Ontology tests

Every candidate dimension must pass all of the following.

### Necessity

Remove the dimension. Do scientifically important mechanisms collapse?

### Orthogonality

Can the information already be reconstructed from another dimension? If yes, merge/demote unless the duplication is deliberate and useful.

### Coverage

Can diverse papers be represented without paper-specific rescue categories?

### Collision

Do causally different methods map to the same code in a misleading way?

### Invariance

Changes that should not change the mechanism must not change the core code:

```text
RGB ↔ BEV ↔ latent substrate
Transformer ↔ diffusion ↔ flow solver
5 ↔ 10 numerical solver steps
heavy generator ↔ surrogate with same semantic consequence output
backbone width / token count / candidate count
```

### Counterexample

Search actively for classic or recent works that violate the category definition.

### Holdout blind test

Classify previously unseen papers without changing the codebook. Any required new category or definition edit is a failure signal that must be logged.

### Human interpretability

A researcher should be able to explain the category using the mechanism graph, without first accepting unexplained project-specific jargon.

## 11. Anti-confirmation-bias rules

- Survey taxonomies are hypotheses, never authority.
- Existing project ontologies have no protected status.
- Prefer counterexamples over supportive examples during stress testing.
- A successful modern method outside autonomous driving can falsify a driving-derived category.
- Architecture names cannot define core categories unless architecture itself changes causal semantics.
- Training-only world knowledge cannot silently become a runtime world object.
- Paper titles and author use of the phrase `world model` do not determine classification.

## 12. External-axis discovery procedure

For each 10–20 anchor batch:

1. reconstruct mechanism graphs;
2. list questions required to distinguish them;
3. compare those questions with current R/W/E/L and C/X/D/P/V/T/L;
4. log missing distinctions and redundant distinctions;
5. propose the smallest correction;
6. attack the correction on older and newer anchors;
7. do not mutate the frozen 12-paper ontology during this track.

## 13. Stop condition

A candidate human-level ontology should not be promoted until:

- at least ~50 RD2+ external anchor papers are represented;
- at least 20 are outside the original driving-12 derivation set;
- foundational MBRL/predictive-state/search/planning works are included;
- at least 15 true holdouts classify without codebook changes;
- no unresolved high-severity collision remains;
- every human code has a one-question explanation and at least two independent exemplars where the field actually contains them.
