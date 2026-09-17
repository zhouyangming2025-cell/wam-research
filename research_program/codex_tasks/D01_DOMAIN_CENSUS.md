# D01 — WAM + One-Stage Domain Census Pilot

Status: **READY FOR CODEX**

Executor: Codex
Reviewer: ChatGPT research lead
Base branch: `research/wam-domain-ontology`
Recommended task branch: `codex/domain-census-d01`

## 0. Mission

Validate the research workflow on a bounded, mechanism-diverse pilot batch before scaling to the full 80–120-paper corpus.

This task is **not** an ontology-classification task.

Do not assign:

```text
R/W/E/L
C/X/D/P/V/T/L
W0/W1/...
RB/RR/...
```

The objective is to determine:

1. which candidate works are truly in the WAM + one-stage domain;
2. what artifact/mode splits they require;
3. what their neutral mechanism skeleton is;
4. which are boundary/control/theory papers rather than Tier-1 domain evidence;
5. whether the extraction protocol is robust enough to scale.

## 1. Read before working

Read these repository files first:

```text
research_program/README.md
research_program/MASTER_PLAN.md
research_program/CODEX_EXECUTION_PROTOCOL.md
research_program/ONTOLOGY_FREE_CARD_V2.md
landscape/FIELD_RECONSTRUCTION_PLAN.md
landscape/FIELD_ATLAS.md
landscape/PHASE_B_ANCHORS.md
```

Use existing repo cards/raw text/deep analyses where they already contain verified evidence. Do not duplicate work blindly.

Also inspect the canonical 12 only to understand what has already been deeply audited. Do not modify their ontology outputs.

## 2. Pilot candidate set

Process the following works. The labels below are **candidate groupings for sampling only**, not scope verdicts. You must independently decide `IN-DOMAIN`, `BOUNDARY`, or `EXCLUDE` from the protocol.

### A. Likely WAM + one-stage candidates

```text
1. Drive-WM
2. OccWorld
3. Think2Drive
4. DrivingGPT
5. Drive-OccWorld
6. ViDAR
7. DriveWorld
8. Auto-JEPA
9. WorldRFT
10. ReWorld
11. WA-JEPA
12. DA-WAM
13. SafeDrive
14. Gen-Drive
15. DriveReward
16. RiskWorld
17. SimWAM
18. DriveFuture
19. Policy World Model / From Forecasting to Planning via Collaborative State-Action Prediction
20. CausalDrive
21. Risk-Aware World Model Predictive Control for Generalizable End-to-End Autonomous Driving (RaWMPC or exact verified title)
```

If a title/acronym is ambiguous or changed between versions, verify the exact primary paper identity and record it. Do not guess.

### B. Deliberate boundary/control probes

```text
22. DiffusionDrive
23. DriveSuprim
24. GameFormer
25. GAIA-1
26. DriveArena
```

These are intentionally included to test whether the scope protocol distinguishes:

```text
strong one-stage planner without explicit WM
interactive prediction/planning predecessor
world generator without strong deployed one-stage planning coupling
generative/closed-loop simulator platform
```

Do not force them into Tier 1.

## 3. Do not redo the canonical 12 as the pilot batch

The frozen canonical set remains the deep regression/explanation suite.

Where one of the pilot papers overlaps existing repo analysis, reuse the evidence and note the source path.

The purpose of D01 is to widen and normalize the broader domain corpus, not to replace or rewrite the canonical set.

## 4. Required output directory

Create only under:

```text
research_program/domain_corpus/d01/
```

Required files:

```text
00_D01_REPORT.md
01_PAPER_SCOPE_TABLE.md
02_ARTIFACT_LEDGER.md
03_MECHANISM_SKELETONS.md
04_BOUNDARY_AND_EXCLUSION_LOG.md
05_SOURCE_AND_DEPTH_LOG.md
06_PROTOCOL_ISSUES.md
```

Do not edit the master protocol files during this task. If you find a problem, describe the proposed correction in `06_PROTOCOL_ISSUES.md`.

## 5. Paper scope table

For all 26 works, record:

| field | requirement |
|---|---|
| exact title | verified primary title |
| year/version | version used |
| primary source | paper URL/arXiv/venue |
| code | official code if available |
| repo evidence | existing wam-research path if applicable |
| scope verdict | IN-DOMAIN / BOUNDARY / EXCLUDE |
| evidence tier | Tier 1 / Tier 2 / Tier 3 |
| reason | 2–5 sentences, mechanism-specific |
| reading depth achieved | RD0–RD4 |
| confidence | HIGH/MEDIUM/LOW |

`IN-DOMAIN` is not awarded because the authors use the phrase “world model.”

## 6. Artifact ledger

For every `IN-DOMAIN` paper, enumerate materially distinct artifacts/modes.

Required fields:

```text
artifact ID
paper/version
mode/task path
terminal deployed output
world/predictive branch lifecycle: training-only / runtime / both / unclear
planning connection
whether paper/code topology differs
whether mode split is required
why the split is mechanistic rather than implementation-only
```

Examples of legitimate reasons for splitting:

```text
planning path vs generation path
self-conditioned vs external-control world rollout
direct planner vs candidate-evaluation mode
paper mechanism vs released-code mechanism
```

Do not split only because of solver steps, model scale, backbone, or tensor format.

## 7. Neutral mechanism skeletons

For every Tier-1 artifact, provide a compact ontology-free DAG using the concepts in `ONTOLOGY_FREE_CARD_V2.md`.

Minimum content:

```text
observation/history
-> separately traceable state/representation
-> predictive/world operation if any
-> future/consequence object if any
-> action formation/candidate/search process
-> criterion/value/reward if any
-> terminal action/trajectory
```

Then separately state:

```text
training-only branches
runtime-retained modules
runtime-dropped/bypassed modules
teacher/surrogate relationships
```

Do not use existing ontology codes as shorthand.

## 8. Mechanism fields required at census depth

For each Tier-1 artifact answer, at minimum:

```text
A. What is the terminal planning/action output?
B. Does a predictive/world object exist separately from ordinary perception features?
C. Is that object train-only, runtime, or both?
D. Is a future explicitly materialized? If yes: endpoint / horizon / branching / internal-predictive / unclear.
E. What conditions the future: history, route, action, candidate trajectory, intent, other?
F. How is the action formed: direct, hierarchy, bank, refinement, search/optimization, joint sequence, retrieval/ranking, other?
G. If alternatives exist, what actually commits/selects/optimizes the final action?
H. What semantic objective/reward/value drives preference, if any?
I. What learning path transfers world/predictive information into deployed planning?
J. What is retained/dropped/bypassed/distilled at deployment?
K. Is other-agent/world response conditioned on ego intervention? Is that response used by planning?
L. Is uncertainty/multimodality represented and actually consumed by planning?
```

Use `UNKNOWN` rather than guessing.

## 9. Reading depth for D01

D01 is a census pilot, not a 26-paper RD3 project.

Target:

```text
all 26 >= RD1
all likely Tier-1 papers >= RD2 where lawful/available
promote to RD3 only when necessary to resolve scope/artifact topology
reuse existing repo RD3/RD4 evidence where already available
```

Do not falsely upgrade depth.

## 10. Sources

Prefer primary sources.

For papers already represented in `wam-research`, inspect existing:

```text
papers/raw_md/
papers/deep_analysis/
papers/cards/
landscape/
```

before re-downloading/re-extracting.

If public sources are inaccessible, mark the evidence limitation. Do not fill gaps from a survey as if it were primary evidence.

## 11. Boundary log

For every BOUNDARY or EXCLUDE item, record exactly which required property is missing.

Examples:

```text
world generation but no material one-stage planning connection
direct trajectory generation with no world/predictive mechanism
interactive prediction/planning predecessor but not WAM by project scope
simulator/evaluation platform rather than one-stage deployed planner
world-model pretraining whose connection to the selected domain definition is ambiguous
```

The purpose is to make the domain boundary auditable.

## 12. Protocol stress test

In `06_PROTOCOL_ISSUES.md`, report any case where the current rules are insufficient, for example:

```text
unclear whether policy trained in a WM but deployed without WM belongs in main domain
unclear whether planning-oriented pretraining-only WM belongs in Tier 1
joint world/action model whose final action path is ambiguous
a paper with multiple released modes needing different scope tiers
world-model rewarder attached to otherwise non-WM planner
```

For each issue provide:

```text
case
why current rule is ambiguous
primary evidence
2+ possible rule fixes
recommended fix
```

Do not silently choose a new global rule.

## 13. Explicit prohibitions

Do not:

```text
modify outputs/core_mechanism_12_v1/
modify handoff/core_mechanism_12/
modify research_program master/protocol/template files
assign ontology labels
rank papers by importance
claim corpus saturation
create a final taxonomy
use general MBRL/robotics papers as Tier-1 domain evidence
```

## 14. Self-check before commit

Verify:

```text
26/26 works accounted for
scope verdict supplied for all
all IN-DOMAIN papers have artifact enumeration
all Tier-1 artifacts have neutral mechanism skeletons
train/runtime separated
boundary cases not counted as Tier-1 votes
no R/W/E/L or C/X/D/P/V/T/L codes in extraction tables
UNKNOWN used where evidence is insufficient
all existing repo evidence paths cited where reused
protected paths untouched
```

## 15. Completion report

Commit the D01 files on the task branch.

Return to the user/reviewer only:

```text
branch name
commit SHA
number of IN-DOMAIN / BOUNDARY / EXCLUDE papers
number of artifacts
RD depth distribution
3–8 major protocol ambiguities or mechanism surprises
confirmation that protected ontology paths were untouched
```

Do not paste the full reports into chat; the reviewer will inspect GitHub directly.
