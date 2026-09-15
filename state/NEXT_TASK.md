# NEXT_TASK

## 唯一下一任务

> **Attack CP-T5 for promotion: determine whether `episode-specific reactive counterfactual consequence validity for planning` survives a deep nearest-neighbor/source audit and has a feasible paired-intervention evaluation protocol.**

Current candidate ranking:

```text
#1 CP-T5  SURVIVES — CANDIDATE RESEARCH PROBLEM
#2 CP-T2  SURVIVES — CANDIDATE RESEARCH PROBLEM

CP-T3     REJECT — PRIOR ART standalone
CP-T6     REJECT — PRIOR ART standalone
```

Canonical candidate files:

```text
landscape/WAM_CANDIDATE_PROBLEMS_V1.md
landscape/WAM_CANDIDATE_PROBLEM_OVERLAP_MATRIX_V1.md
landscape/WAM_CANDIDATE_PROBLEM_RESEARCHABILITY_V1.md
```

---

# CP-T5 promotion question

Candidate statement:

> **Can a planning-centric WAM trained mainly on factual trajectories recover intervention-correct consequences when an alternative ego action changes both the episode-specific outcome and surrounding-agent responses?**

The hypothesized failure has two independent components:

```text
A. episode-specific identification / abduction
   The model must preserve latent facts specific to this realized episode.

B. reactive intervention response
   Surrounding agents may respond differently under the alternative ego action.
```

The research problem survives only if neither component nor their planning-relevant conjunction is already adequately solved.

---

# Task 1 — Deep audit the closest paper: Counterfactual Driving World Models (2026-08)

Paper:

```text
How Can Driving World Models Do Counterfactual Prediction?
arXiv:2608.11601
```

Mandatory reconstruction:

```text
1. exact factual / alternative / reference rollout construction
2. what latent/world variables are held fixed across paired CARLA runs
3. whether background agents are scripted or reactive
4. why direct p(Y | H, a') fails the counterfactual target
5. exact abduction-inspired evidence-transfer pipeline
6. which representative WMs are tested
7. metrics and failure modes
8. whether any planning downstream task is evaluated
9. whether longer horizons / reactive agents are explicitly excluded
10. code/data release status
```

Final boundary must state exactly what remains after this paper.

---

# Task 2 — Deep audit ReactSim-Bench as infrastructure and scientific control

Canonical project raw source already exists:

```text
papers/raw_md/P0014_ReactSimBench/P0014_ReactSimBench.raw.md
```

Official open benchmark identified:

```text
Thinklab-SJTU/ReactSim-Bench
```

Mandatory reconstruction:

```text
1. exact AV-agent decoupled rollout protocol
2. how the 2,636 deviated-AV scenarios are generated / filtered
3. what counts as reactive pressure
4. longitudinal / directional / lateral categories
5. whether there is a unique ground-truth response for a deviated AV trajectory
6. what metrics measure safety/feasibility vs true response accuracy
7. which baseline behavior WMs are provided
8. replan-frequency effects
9. whether protocol can be reused for planning consequence validation
10. source/data/checkpoint availability
```

Critical question:

> Can ReactSim-Bench supply the **reactive intervention axis** for CP-T5, or does it only score plausible responses without matched counterfactual truth?

---

# Task 3 — Deep audit CausalDrive as nearest reactive world-model prior art

Canonical project raw source:

```text
papers/raw_md/P0015_CausalDrive/P0015_CausalDrive.raw.md
```

Mandatory reconstruction:

```text
1. exact inputs: initial frame / ego trajectory / sociology prompt
2. what future NPC information is deliberately withheld
3. what `causal` / `reactive` means operationally
4. how driving-sociology labels are produced
5. whether identical initial state + identical ego action can yield controlled alternative NPC reactions
6. whether reactions have factual/matched counterfactual truth or are prompt-controlled plausible variants
7. closed-loop / RL / real-world evidence
8. action controllability metrics
9. reactive validity metrics
10. code/data release status
```

Critical novelty boundary:

```text
reactive visual simulation
!=
episode-specific matched reactive counterfactual identification
```

Verify rather than assume this boundary.

---

# Task 4 — Audit ReactSim / CausalDrive / counterfactual-WM intersection

Create a three-way matrix:

| Property | Counterfactual-WM 2608.11601 | ReactSim-Bench | CausalDrive | CP-T5 required |
|---|---|---|---|---|
| same underlying episode paired across actions | | | | YES |
| alternative ego intervention | | | | YES |
| surrounding agents react to intervention | | | | YES |
| matched consequence truth | | | | YES |
| visual/latent world prediction | | | | optional / representation-dependent |
| planning consequence use | | | | YES |
| planning regret measurable | | | | YES |
| open reproducible infra | | | | strongly preferred |

If any single prior work already fills the CP-T5 column, reject the candidate.

---

# Task 5 — Latest 2026 overlap attack

Search explicitly for papers combining:

```text
reactive counterfactual autonomous driving world model
matched ego intervention ground truth
counterfactual reactive traffic simulation
causal driving world model planning
interactive counterfactual planning world model
multi-agent counterfactual world model autonomous driving
```

Must include at least:

```text
CausalDrive
ReactSim-Bench
How Can Driving World Models Do Counterfactual Prediction?
World Models as Adversaries (AWM)
Reaction-Uncertainty-Aware Motion Planning
ProDrive
```

Do not assume our current search is exhaustive.

---

# Task 6 — Define a minimum paired-intervention protocol WITHOUT designing a method

Specify only the experimental object:

```text
initial world state / simulator seed z
factual ego action a
alternative ego action a'
fixed environment mechanism E

Y(a)  = rollout(E, z, a)
Y(a') = rollout(E, z, a')
```

For multiple a' branches, record:

```text
ego consequence
agent response trajectories
collision / TTC / right-of-way / progress outcome
```

Then define what a learned WAM must predict/evaluate.

Do not yet choose:

```text
network architecture
tokenization
risk-field representation
loss design
```

---

# Task 7 — Feasibility gate

Evaluate concrete infrastructure options:

```text
CARLA / Bench2Drive
nuPlan + reactive simulator / InterPlan-like setup
ReactSim-Bench baselines
other open 2026 reactive simulation infrastructure
```

Score:

```text
paired-ground-truth capability
reactivity
scenario diversity
planning integration
source openness
compute/data burden
reproducibility
```

If unique matched reactive counterfactual truth is infeasible with accessible infrastructure, mark:

```text
HOLD — INFRA TOO HEAVY
```

rather than inventing a weak proxy.

---

# Required outputs

Create:

```text
audits/research_synthesis/CP_T5_PROMOTION_AUDIT_V1.md
landscape/CP_T5_NEAREST_PRIOR_ART_MATRIX_V1.md
landscape/CP_T5_PAIRED_INTERVENTION_PROTOCOL_V1.md
```

Final verdict must be one of:

```text
PROMOTE — CANDIDATE RESEARCH GAP
REJECT — PRIOR ART
REJECT — EVIDENCE DOES NOT SUPPORT PROBLEM
HOLD — INFRA TOO HEAVY
```

If promoted, the novelty boundary must be one sentence and falsifiable.

---

# Secondary candidate

Do not advance CP-T2 in parallel unless CP-T5 is rejected/held or its audit exposes a direct link requiring T2.

CP-T2 remains:

```text
When does online action-conditioned branching add information beyond compact world-state/direct-policy conditioning under matched budgets?
```

---

# Still forbidden in this round

```text
NO final method architecture
NO paper title
NO claim that `risk` is the solution
NO claim that reactive WM itself is novel
NO claim that counterfactual conditioning itself is novel
NO promotion without nearest-neighbor + infrastructure audit
```
