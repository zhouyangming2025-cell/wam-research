# External Ontology Audit — Execution Report

Date: 2026-09-17

Branch: `codex/gpt6-mechanism-handoff`

## 1. User-authorized objective

Build a broader literature evidence base for future ontology discovery/audit, write it into `wam-research`, and do not modify the existing 12-paper ontology.

## 2. Repository mutation audit

Base before this track:

```text
b56f26aef30a5c137ef491152ad70e8081e8a2ab
```

After initial track construction, comparison against that base showed only additions under:

```text
papers/external_ontology_corpus/
```

No file under `outputs/core_mechanism_12_v1/` or `handoff/core_mechanism_12/` was modified.

## 3. Files created

```text
README.md
00_CORPUS_PROTOCOL.md
01_SOURCE_MAP.md
02_EXTERNAL_REGISTRY.md
03_ONTOLOGY_FREE_MECHANISM_TEMPLATE.md
04_FOUNDATIONAL_MECHANISM_LEDGER.md
05_DRIVING_MECHANISM_LEDGER.md
06_EXTERNAL_ONTOLOGY_PRESSURE_TEST_V0.md
07_HOLDOUT_PLAN.md
08_EXECUTION_REPORT.md
```

## 4. What was accomplished

### 4.1 Independent protocol

Created a protocol that reverses the previous risk of confirmation bias:

```text
large literature
→ ontology-free mechanism reconstruction
→ candidate dimensions
→ stress tests
→ holdout blind tests
```

Existing R/W/E/L is now explicitly treated as one candidate hypothesis rather than the answer.

### 4.2 Cross-domain source map

Expanded beyond autonomous driving into:

```text
predictive-state / belief-state foundations
Dyna / model-assisted learning
latent online planning
imagination-trained actor/value learning
learned-model tree search
MPC / trajectory optimization
JEPA predictive representations
robotics / embodied world models
autonomous-driving generation / planning / simulation
strong non-WM controls
```

### 4.3 Breadth registry

Seeded a 100+ work/family registry when combined with the repo's existing Phase-A driving census. The registry explicitly distinguishes discovery/census from actual deep reading.

### 4.4 Ontology-free mechanism template

Added a detailed reconstruction schema for:

- state objects;
- dynamics/transition operators;
- future construction;
- action formation;
- search/optimization/commitment;
- criterion semantics;
- learning gradients;
- retain/drop/bypass/distillation;
- clocks;
- uncertainty/branching;
- evidence boundaries;
- deletion/substitution tests.

Candidate ontology projection is intentionally the final step.

### 4.5 Foundational external ledger

Initial mechanism-level pressure-test batch includes:

```text
Dyna
Value Prediction Network
TreeQN / ATreeC
World Models
PlaNet
Dreamer
MuZero
TD-MPC / TD-MPC2
Predictive State Representations (initial depth)
V-JEPA action-conditioned lineage (initial depth)
```

This batch already exposes mechanism families absent from the original 12-paper derivation set.

### 4.6 Driving mechanism ledger

Reused existing high-depth repo evidence without rewriting it, and aligned it with the external questions. Key contrast pairs are explicitly recorded:

```text
LAW vs DriveLaW
Drive-JEPA PB vs World4Drive
DynFlowDrive vs WorldDrive
GraphWorld vs ordinary BEV planners
World4Drive vs WoTE
WoTE vs PlaNet
SeerDrive paper vs code
Discrete-WAM joint vs world mode
Think2Drive vs PlaNet
```

### 4.7 First external ontology pressure test

Provisional result:

```text
W  = KEEP + MODIFY
R  = necessary question, but current codebook incomplete
E  = KEEP + BROADEN beyond separate resolver
L  = KEEP; ordered directed program strongly supported

possible missing question:
I? interaction / intervention / reactivity
U? uncertainty / stochastic branching
```

Most important new failure:

```text
PlaNet / MuZero / TreeQN / TD-MPC2 / VPN
```

show that online search / MCTS / MPC / differentiable lookahead is a major action-formation/commitment family not naturally covered by the current human R set.

### 4.8 Holdout discipline

Created a real blind-test protocol with reserved recent driving, robotics, model-based-control and boundary methods. A future candidate ontology cannot count a paper as holdout once it has already been used at RD2+ for ontology design.

## 5. Main scientific findings so far

### Finding A — deployment world use is real and important

Dyna versus PlaNet/MuZero independently validates the need to distinguish:

```text
world/model knowledge used to train/compile behavior
vs
learned world/model actively used during online decision computation
```

This supports the core purpose of W.

### Finding B — world state cannot require observation reconstruction

VPN, MuZero, TreeQN and TD-MPC2 use planning-sufficient abstract/latent dynamics. Therefore a valid `world/model object` gate must admit reward/value/planning-grounded states, not only RGB/BEV/factual-future reconstruction.

### Finding C — human W5 is likely redundant

`joint world-action` describes coupling, already carried by R/D-like questions. The world side of a joint future sequence still has a temporal role such as horizon/rollout. Current hypothesis: keep detailed backend joint object type if useful, but remove human W5 and represent jointness in R/D.

### Finding D — W1/W2 distinction gained external support

GraphWorld/DriveLaW is no longer the only evidence. Ha & Schmidhuber's `z_t` versus predictive RNN hidden `h_t`, plus recurrent model-state traditions, support distinguishing current model state from predictive internal state—subject to deeper boundary audit.

### Finding E — current R is the most urgent weakness

Driving-derived R is missing online search/optimization mechanisms. Two candidate repairs are retained, not decided:

```text
add one online-search/optimization R class
or
factor action formation and commitment/search into separate subquestions
```

### Finding F — E should describe decision objective, not only resolver criterion

Return/value/Q/reward semantics can control search/optimization without a separately typed finite-bank resolver.

### Finding G — L is strongly supported

Dyna, Dreamer, predictive pretraining, auxiliary future loss and teacher/surrogate distillation independently validate an ordered learning→deployment route with explicit retain/drop fate.

## 6. What is NOT complete

This is a serious first external audit, not the final large-corpus ontology.

Not yet complete:

1. 50–100 external papers at RD2/RD3 mechanism depth;
2. source/code verification for most new external anchors;
3. formal R search/optimization adjudication wave;
4. formal W1/W2 boundary wave;
5. interaction/reactivity independence test;
6. uncertainty/risk independence test;
7. robotics deep-read wave;
8. true blind holdout execution;
9. final replacement ontology.

No claim of final completeness is made.

## 7. Recommended next execution order

```text
Wave F1: PlaNet / MuZero / TreeQN / VPN / TD-MPC2
         → settle R search/optimization representation

Wave F2: World Models / Dreamer / V-JEPA2-AC / GraphWorld / DriveLaW
         → settle W1 vs W2 and predictive-state admission gate

Wave F3: M2I / GameFormer / BeTop / Drive-WM / ReactSim-Bench / CausalDrive
         → test independent interaction/reactivity axis

Wave F4: PILCO / ensemble MBRL / risk-sensitive MPC / safety WMs
         → test uncertainty/risk axis

Wave F5: robotics world-action and video-WM policy systems
         → cross-domain generalization attack
```

Only after F1–F5 should a replacement human ontology be frozen and tested on the reserved holdouts.

## 8. Integrity statement

The track is intentionally allowed to falsify the existing project ontology. The goal is a domain mechanism map, not preservation of R/W/E/L or C–X–D–P–V–T–L.
