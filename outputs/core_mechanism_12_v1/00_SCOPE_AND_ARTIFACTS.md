# Core Mechanism 12 — Phase 0 Scope and Artifact Lock

Status: Phase 0 complete; Phase 1 graph reconstruction is recorded in 01_PAPER_MECHANISM_GRAPHS.md.

## 1. Frozen task boundary

This checkpoint covers only:

1. Phase 0 — fix the evidence snapshot, paper/code versions, task modes, and artifact identities.
2. Phase 1 — reconstruct deployment and learning DAGs without importing the old taxonomy.

Explicitly out of scope at this checkpoint:

- mechanism ontology or category assignment;
- cross-paper collision tests;
- review or reuse of old taxonomy drafts;
- engineering blueprints or experiment plans;
- edits to handoff/LATEST.md, state/CURRENT_STATE.md, or state/NEXT_TASK.md.

The reconstruction unit is:

    artifact = paper or code version × task mode × planning-inference path

A training recipe is not promoted to a separate deployment artifact unless it changes the inference path. Conversely, paper and code are split when their deployed inference paths materially differ.

## 2. Evidence snapshot

- Repository: zhouyangming2025-cell/wam-research
- Working branch: codex/gpt6-mechanism-handoff
- Branch head inspected before writing: 80a29d2622be032fdcb32afffcfb89fee7b7ab4a
- Primary corpus: the 12 raw-paper text artifacts pinned by the recursive tree at that commit.
- Task contract: handoff/core_mechanism_12/GPT6_TASK_PROMPT.md
- Protocol: handoff/core_mechanism_12/RESEARCH_PROTOCOL.md
- Paper locator: handoff/core_mechanism_12/PAPER_EVIDENCE_INDEX.md and PAPER_SET_12.tsv

Evidence was read in this order:

1. raw paper text;
2. official source at a pinned commit, where available;
3. repository source audits for version and implementation boundaries.

Old mechanism drafts and prior taxonomy conclusions were not used to build these graphs.

## 3. Evidence labels and graph vocabulary

Every graph edge carries:

- lifecycle: TRAIN, RUNTIME, or BOTH;
- evidence: PAPER FACT, CODE FACT, OUR INFERENCE, or UNKNOWN.

Node symbols:

| Symbol | Meaning |
|---|---|
| O | observation or history |
| S | current state or current-scene representation |
| I | intent, command, or decision variable |
| A | proposal or action representation |
| W | current-world carrier |
| F | future or consequence carrier |
| V | value, reward, score, compatibility, or selection criterion |
| R | resolver or selection/refinement operator |
| A* | final deployed action or trajectory |

Absence notation is strict:

- ∅: verified absent from the artifact path;
- UNKNOWN: evidence is insufficient;
- N/A: the question does not apply to this mode.

Solver coordinates are never silently interpreted as physical time. Diffusion/flow denoising steps, within-decision refinement iterations, and outer physical rollout steps are separately named.

## 4. Version and source lock

| Paper ID | Work | Paper identity fixed for this checkpoint | Official source boundary | Source status |
|---|---|---|---|---|
| P0048 | LAW | raw corpus copy; exact PDF revision UNKNOWN | BraveGroup/LAW at b2f6a… | perception-free path inspected; perception-based implementation not independently established |
| P0001 | Epona | ICCV 2025 raw corpus copy; exact arXiv revision UNKNOWN | Kevin-thu/Epona at 69b24c… | model and evaluation paths inspected |
| P0009 | DriveLaW | arXiv:2512.23421v3, CVPR 2026 | official code at 243e0e… | paper/code action-step mismatch retained |
| P0046 | World4Drive | ICCV 2025; arXiv:2507.00603 | official code at cffb51… | core path inspected; public benchmark coverage boundary retained |
| P0042 | WorldDrive | arXiv:2603.14948 | official code at c375ee… | deployment distillation path inspected |
| P0045 | WoTE | raw corpus copy; exact PDF revision UNKNOWN | liyingyanUCAS/WoTE at 298957… | recurrent candidate-world evaluation inspected |
| P0061 | SeerDrive | NeurIPS 2025; official page links arXiv:2510.11092 | initial official release at 1cfb7ec… | release differs materially from paper loop |
| P0049 | Drive-JEPA | arXiv:2601.22032 | official code at e21f474… | perception-free, perception-based v1 and v2 inspected |
| P0062 | Metis | arXiv:2606.15869v1 | official README at 7677b62… | executable source unavailable in evidence snapshot |
| P0063 | DynFlowDrive | arXiv:2603.19675v2 | official README-only snapshot at c665dc… | executable source unavailable |
| P0064 | Discrete-WAM | arXiv:2606.05645v2, dated 2026-06-09 | no verified official source snapshot | paper-only reconstruction |
| P0065 | GraphWorld | arXiv:2606.16274v1, dated 2026-06-15 | no verified official source snapshot | paper-only reconstruction |

Ellipses in commit display are presentation-only; the repository audits retain the full hashes. No claim marked CODE FACT is derived from a README-only or unavailable implementation.

## 5. Artifact registry

The registry intentionally separates modes that answer different deployment questions.

| Artifact ID | Base work | Frozen mode | Deployed planning path | Split rationale |
|---|---|---|---|---|
| LAW-PF | LAW | perception-free planning | image/history latent → waypoint | future-latent branch is training-side with respect to A* |
| LAW-PB | LAW | perception-based planning | perception/current latent → waypoint | paper mode; implementation boundary differs from LAW-PF |
| EPO-PLAN | Epona | planning-only evaluation | history/MST → TrajDiT → trajectory | visual generator is skipped |
| EPO-SELF | Epona | self-generated world rollout | predicted first-step motion → visual DiT → next latent, recurrent over physical steps | rollout capability, not the planning-only benchmark path |
| EPO-CTRL | Epona | externally controlled rollout | supplied pose/yaw → visual DiT → next latent/video | no TrajDiT decision is required |
| DLAW-PAPER | DriveLaW | paper planning path | early Video-DiT hidden state → Action DiT flow → trajectory | paper specifies five action steps |
| DLAW-CODE | DriveLaW | released planning path | early Video-DiT hidden state → Action DiT flow → trajectory | released agent/config step count is not fully consistent with paper |
| W4D-PLAN | World4Drive | candidate planning | six intentions → candidate future latents → ScoreNet → argmax | online candidate-specific latent foresight |
| WD-PLAN | WorldDrive | distilled deployment | candidate → lightweight future surrogate → reward → argmax | heavy trajectory-aware diffusion teacher is absent at runtime |
| WOTE-PLAN | WoTE | online candidate evaluation | candidates → recurrent future BEV/action → decomposed reward → argmax | explicit multi-step candidate consequence evaluation |
| SEER-PAPER | SeerDrive | paper iterative co-refinement | future BEV ↔ planner feature, repeated within one decision | canonical paper mechanism |
| SEER-CODE | SeerDrive | released WoTE-integrated evaluator/refiner | 256 candidates → one-step future BEV/rewards → fixed-index refinement | materially different inference graph from paper |
| DJEPA-PF | Drive-JEPA | perception-free planning | frozen V-JEPA history feature → direct trajectory | JEPA predictor/target encoder discarded |
| DJEPA-PB1 | Drive-JEPA | perception-based v1 | proposal refinement → learned scorer → argmax | no cross-frame recalibration |
| DJEPA-PB2 | Drive-JEPA | perception-based v2 | proposal refinement → learned score + previous-trajectory comfort → argmax | deployed resolver differs from v1 |
| METIS-PLAN | Metis | action-only planning | observation/instruction → action expert flow → trajectory | video expert bypassed at runtime |
| DFD-PLAN | DynFlowDrive | distilled planning | candidates + learned score → argmax | flow world model is training-only |
| DWAM-POLICY | Discrete-WAM | primary policy-only planning | context → decision token → iterative action-token editing → trajectory | reported planning path need not emit visual tokens |
| DWAM-WORLD | Discrete-WAM | action-conditioned world generation | context + supplied action → future visual tokens | world-generation capability; A* is N/A |
| DWAM-JOINT | Discrete-WAM | world-policy generation | interleaved action and visual token generation/editing | distinct generative capability path |
| GW-PLAN | GraphWorld | structured-world planning | current structured world → two-step flow refinement → motion/planning heads | internal transport, not explicit physical rollout |

## 6. Artifact boundary decisions

### 6.1 Aligned paper and code are evidence layers, not duplicate artifacts

World4Drive, WorldDrive, and WoTE retain one mode artifact each because the inspected code corroborates rather than changes the planning-inference path. Their graph edges still distinguish PAPER FACT from CODE FACT.

### 6.2 Required paper/code splits

- DriveLaW is split because solver-step settings and paper/source descriptions are not identical.
- SeerDrive is split because the paper describes repeated world–planner co-refinement, while the initial released source implements a WoTE-style candidate evaluator followed by fixed-index trajectory refinement.

### 6.3 Required mode splits

- LAW: perception-free versus perception-based.
- Epona: planning-only, self-generated rollout, and externally controlled rollout.
- Drive-JEPA: perception-free, perception-based v1, and perception-based v2.
- Discrete-WAM: policy-only planning, action-conditioned world generation, and joint world-policy generation.

### 6.4 Candidate identity policy

A tensor with a candidate dimension is not automatically a counterfactual world bank. The registry records candidate-specific futures only when the artifact computes a consequence representation conditioned on each candidate. A single factual future target reused across candidates remains one observed future, not K ground-truth counterfactual futures.

## 7. Phase gate

Phase 0 is complete if reviewers accept:

- the evidence snapshot and versions above;
- the 21 artifact identities;
- the explicit paper/code and mode splits;
- the rule that Phase 1 graphs are reconstructed before any ontology label is assigned.

No Phase 2 classification should begin until 01_PAPER_MECHANISM_GRAPHS.md and 07_UNRESOLVED_EVIDENCE.md are reviewed.
