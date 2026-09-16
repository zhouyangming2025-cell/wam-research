# External Ontology Evidence Corpus

Status: **ACTIVE INDEPENDENT ONTOLOGY-AUDIT TRACK**

Created: 2026-09-17

## 1. Purpose

This directory builds an external evidence base for mechanism ontology discovery in **world models + planning/control + end-to-end autonomous systems**.

It is deliberately broader than the frozen 12-paper core-mechanism exercise. The goal is not to make additional papers fit the existing `R–W–E ⊕ L` or `C–X–D–P–V–T–L` schemes. The goal is to determine, from a much broader literature base, whether those dimensions are necessary, orthogonal, complete, stable, and understandable.

The causal direction is:

```text
large external literature
→ ontology-free mechanism reconstruction
→ recurring mechanism questions
→ candidate dimensions
→ collision / counterexample / invariance attacks
→ holdout blind tests
→ only then ontology revision or promotion
```

Not:

```text
existing ontology
→ search for supporting papers
```

## 2. Non-interference rule

This track must **not modify** the current 12-paper ontology while evidence is being accumulated.

Protected current track:

```text
outputs/core_mechanism_12_v1/
handoff/core_mechanism_12/
```

Those files remain a historical/provisional hypothesis and a useful internal benchmark. This directory may cite and attack them, but may not silently rewrite them.

## 3. Relationship to the existing field reconstruction

The repository already contains a strong planning-centric field-reconstruction program:

```text
landscape/FIELD_RECONSTRUCTION_PLAN.md
landscape/FIELD_ATLAS.md
landscape/CENSUS_PHASE_A_ROUND1.md
landscape/CENSUS_PHASE_A_ROUND2.md
landscape/PHASE_B_ANCHORS.md
papers/deep_analysis/
```

This external corpus does **not** duplicate that atlas. It extends it in three ways:

1. adds foundational model-based RL, predictive-state, latent-dynamics, search/planning and robotics literature outside autonomous driving;
2. stores an ontology-free mechanism ledger designed specifically for cross-domain mechanism comparison;
3. subjects candidate ontology dimensions to explicit necessity, orthogonality, coverage, collision, invariance and blind-holdout tests.

The existing driving atlas is therefore an important domain-specific evidence source inside a larger mechanism study.

## 4. Main research question

> What is the smallest set of independent research questions needed to describe how learned world models affect planning, control, action formation and policy learning across embodied decision systems?

The target is not a taxonomy of architecture names such as Transformer, diffusion, BEV, RGB, occupancy or latent tokens. A useful ontology should be invariant to implementation substitutions that do not change the mechanism.

## 5. Scope

Primary evidence domains:

```text
A. foundational state / predictive-state theory
B. model-based reinforcement learning
C. latent dynamics and online planning
D. imagination-based policy/value learning
E. tree search / trajectory optimization with learned models
F. robotics and embodied world models
G. autonomous-driving world models
H. end-to-end planning with and without explicit world models
I. world-model simulators / policy training / evaluation
J. world-action and joint generation systems
K. strong non-world-model controls
```

Pure generation papers enter only when they clarify state construction, dynamics, controllability, decision coupling, or historical transitions relevant to embodied decision making.

## 6. Evidence depth

Every source is assigned a reading-depth label:

```text
RD0 = metadata / discovery only
RD1 = abstract + introduction screened
RD2 = method / figures / core equations inspected
RD3 = full mechanism reconstruction from paper
RD4 = paper + source/code verification of decision-critical mechanism
```

A large RD0/RD1 registry is useful for coverage but **cannot** by itself justify an ontology claim. Major ontology changes should be supported primarily by RD2–RD4 evidence plus explicit counterexamples.

## 7. Evidence labels

Mechanism ledgers separate:

```text
PRIMARY FACT     directly supported by primary paper / official source
CODE FACT        supported by inspected implementation
SURVEY SYNTHESIS supported by a survey, used for coverage/context
OUR INFERENCE    derived mechanism interpretation
UNKNOWN          evidence does not establish the fact
```

Survey taxonomies are treated as competing hypotheses, not ground truth.

## 8. Files

```text
00_CORPUS_PROTOCOL.md
01_SOURCE_MAP.md
02_EXTERNAL_REGISTRY.md
03_ONTOLOGY_FREE_MECHANISM_TEMPLATE.md
04_FOUNDATIONAL_MECHANISM_LEDGER.md
05_DRIVING_MECHANISM_LEDGER.md
06_EXTERNAL_ONTOLOGY_PRESSURE_TEST_V0.md
07_HOLDOUT_PLAN.md
```

## 9. Current provisional lesson

The first external pass already shows why this track is necessary:

- classic Dyna separates model-assisted learning/planning from fully reactive execution;
- PlaNet, MuZero, TreeQN and TD-MPC2 expose online search/optimization topologies weakly represented by the current 12-paper `R` sample;
- VPN and MuZero show that a planning-sufficient world model need not reconstruct observations;
- Dreamer shows that imagined world trajectories may train policy/value functions without surviving as a decision-time rollout;
- modern Physical-AI surveys explicitly treat state abstraction, temporal dynamics and decision coupling as separable design questions;
- modern autonomous-driving work contains generation-only, training-only, online latent, candidate-consequence, rollout, simulator and joint world-action roles that should not be conflated.

These observations are **pressure-test evidence**, not a replacement ontology yet.

## 10. Promotion rule

No candidate dimension is considered stable merely because it fits the current corpus. Promotion requires:

```text
necessity test
orthogonality test
coverage test
collision test
implementation-invariance test
counterexample attack
held-out-paper blind test
human interpretability test
```

A dimension may be KEEP, MODIFY, SPLIT, MERGE or DELETE. Existing names and codes have no protected status.
