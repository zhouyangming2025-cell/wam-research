# CODEX EXECUTION PROTOCOL

Status: **MANDATORY FOR CODEX BATCHES**

## 1. Role

Codex acts as a research engineer, not the ontology authority.

Its job is to produce traceable evidence and mechanism reconstructions that another reviewer can independently audit.

## 2. Default workflow

For every assigned task:

```text
read task brief
read referenced repo protocols/templates
inspect existing repo evidence to avoid duplication
collect primary sources
perform requested extraction/audit
write outputs only to task-authorized paths
run self-consistency checks
commit changes
report commit SHA + concise completion summary + unresolved items
```

## 3. Branch rule

Never work directly on `research/wam-domain-ontology` unless the task explicitly says so.

Default:

```text
create task branch from research/wam-domain-ontology
commit all task work there
return SHA for review
```

Recommended branch naming:

```text
codex/domain-census-d01
codex/domain-census-d02
codex/deepread-w01
codex/deepread-r01
codex/codeaudit-<paper>
```

## 4. Evidence priority

Use sources in this order when mechanism details matter:

```text
1. primary paper
2. official appendix/supplement/project page
3. official released code
4. author technical report
5. high-quality survey for discovery/context only
```

Do not use a survey sentence as proof of a paper's detailed runtime topology when the primary paper can be checked.

## 5. Required evidence labels

Every nontrivial mechanism claim should be marked conceptually as one of:

```text
PAPER FACT
CODE FACT
AUTHOR CLAIM
OUR INFERENCE
UNKNOWN
```

Do not convert inference into fact.

## 6. Reading depth honesty

Use:

```text
RD0 metadata only
RD1 abstract/introduction screened
RD2 method/figures/core equations inspected
RD3 full mechanism reconstruction
RD4 paper + source/code verification of decision-critical topology
```

Never label a paper RD3 after only reading abstract/project page snippets.
Never label RD4 without inspecting the relevant implementation path.

## 7. Ontology-free first pass

Unless a task explicitly requests ontology projection, **do not assign R/W/E/L or C/X/D/P/V/T/L codes**.

Record what the mechanism does in neutral terms:

```text
state objects
future/consequence objects
action objects
transition/generation operators
candidate birth and identity
search/optimization/refinement
criterion/value/reward
training gradients and teachers
runtime retained/dropped/bypassed modules
clock/iteration structure
uncertainty/branching
interaction/reactivity
```

The point is to prevent the current ontology from shaping the evidence extraction.

## 8. Artifact splitting rule

Classification/extraction unit:

```text
paper/code version × task/mode × planning/generation path
```

Split modes when they materially change deployment topology or decision mechanism.

Examples:

```text
planning mode vs world-generation mode
self rollout vs externally controlled rollout
paper topology vs released-code topology
proposal-free path vs candidate-bank path
```

Do not split solely for different hyperparameters, tensor sizes, solver-step counts, or backbone variants unless the task specifically studies them.

## 9. Domain-scope discipline

Primary corpus target is WAM + one-stage/end-to-end autonomous driving.

A paper belongs to Tier 1 only if world/predictive modeling materially affects at least one of:

```text
planning/action generation at deployment
candidate evaluation/selection
search/optimization over actions
one-stage planning representation consumed at deployment
training of the deployed one-stage planning mechanism
joint world-action generation used as the action mechanism
world-model environment used to train a deployed end-to-end policy, when the task explicitly includes this lineage
```

Pure visual generation/data synthesis without a meaningful planning connection is normally Tier 2/3 context, not main ontology evidence.

Strong non-WM planners and interactive prediction/planning methods are controls/boundaries, not Tier-1 WAM votes.

## 10. Forbidden shortcuts

Do not:

```text
classify from titles or keywords alone
infer runtime use because a paper says "world model"
infer world state because a feature contains scene information
infer candidate selection because multiple trajectories are generated
infer causality from action conditioning alone
infer code behavior from paper diagrams when code is available and task requires RD4
invent a new ontology category during extraction
change protected 12-paper ontology files
```

## 11. Required mechanism questions

For every RD2+ in-domain artifact, answer at least:

1. What is the task and final deployed output?
2. What state/representation objects are separately traceable?
3. Which objects have explicit temporal/predictive/world semantics?
4. What conditions future prediction/generation?
5. Is the future object training-only or online?
6. What exactly reaches the planner/action path at deployment?
7. How is the action formed: direct decode, hierarchy, candidate bank, search, optimization, iterative refinement, joint sequence, other?
8. If alternatives exist, how is identity preserved and commitment performed?
9. What criterion/value/reward determines preference or search direction?
10. What learning signal reaches which deployed component?
11. What is retained, dropped, bypassed, frozen, or distilled at deployment?
12. What clocks/iterations exist: physical horizon, solver loop, reciprocal update, previous cycle?
13. Is uncertainty/branching represented explicitly?
14. Is environment/agent response conditional on ego action, and is that response used for the decision?
15. What evidence is primary fact vs inference?

## 12. Batch quality checks

Before commit, verify:

```text
all requested papers accounted for
no duplicate paper IDs
all source URLs/IDs recorded
all RD labels justified
all Tier-1 inclusions have a planning connection
artifact modes split where necessary
no ontology codes leaked into ontology-free outputs unless authorized
UNKNOWN used instead of guessing
existing repo evidence reused/cited rather than duplicated blindly
```

## 13. Completion report format

Every Codex task must end with a concise report containing:

```text
branch
commit SHA
files added/changed
papers/artifacts processed
RD depth counts
scope exclusions/boundaries
major unresolved mechanism questions
any evidence conflicts
whether protected paths were untouched
```

## 14. Review outcomes

The research lead may return:

```text
ACCEPT
ACCEPT WITH CORRECTIONS
REVISE
REJECT
```

Only accepted evidence should be treated as canonical research state.
