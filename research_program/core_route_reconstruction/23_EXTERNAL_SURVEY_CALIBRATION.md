# External survey calibration for WAM + one-stage autonomous driving

Status: **external calibration only; no ontology update, no route promotion.**

Branch: `research/core-route-reconstruction`

Date: 2026-09-17

Goal:

Search for recent external surveys/reviews that independently organize autonomous-driving world models / world-action models, with special attention to whether they cover the project's canonical 12:

- LAW
- Epona
- DriveLaW
- World4Drive
- WorldDrive
- WoTE
- SeerDrive
- Drive-JEPA
- Metis
- DynFlowDrive
- Discrete-WAM
- GraphWorld

The purpose is not to adopt an external taxonomy automatically. The purpose is to use independent surveys as calibration evidence against self-generated ontology structure.

---

## 1. Bottom line

No single survey located in this search simultaneously satisfies all three conditions:

1. covers all 12 canonical papers;
2. focuses specifically on WAM + one-stage autonomous-driving planning;
3. provides a sufficiently fine-grained mechanism taxonomy for how world knowledge changes planning.

The current external literature is still fragmented by scope and publication cutoff.

However, several surveys are highly valuable calibration sources.

The strongest combination appears to be:

- **peer-reviewed autonomous-driving WM survey** for broad legitimacy and ecosystem coverage;
- **planning/MPC-oriented AD survey** for world-to-decision interfaces;
- **general WAM surveys** for world-action factorization and future-to-action definitions;
- our own paper-first reconstruction for detailed target-domain mechanism fidelity.

External surveys should therefore be treated as independent pressure tests, not ground truth.

---

# 2. Highest-value surveys found

## 2.1 The Role of World Models in Shaping Autonomous Driving: A Comprehensive Survey

Authors: Sifan Tu et al.

Venue/status:

- Frontiers of Computer Science
- accepted 2026-08-23
- published online 2026-09-01
- DOI: 10.1007/s11704-026-60102-1

Main organization:

- predicts scenes in different modalities;
- video;
- point cloud;
- occupancy;
- latent feature;
- traffic map;
- then discusses applications, datasets, simulators and metrics.

This is the strongest **peer-reviewed/current autonomous-driving-specific survey** found.

Associated living repository:

`https://github.com/LMD0311/Awesome-World-Model`

The living repository currently contains exact entries for at least:

- LAW
- Epona
- DriveLaW
- World4Drive
- WorldDrive
- WoTE
- Drive-JEPA
- Discrete-WAM
- GraphWorld

Exact-string searches did not locate:

- SeerDrive
- Metis
- DynFlowDrive

Thus the associated current paper collection covers roughly **9/12** canonical papers by exact title/name at audit time.

Important caveat:

> the living repository is a continuously updated supplement, not identical to the peer-reviewed survey manuscript's frozen reference list.

### Value to this project

High authority for:

- what the wider autonomous-driving world-model community considers in scope;
- representation/modality families;
- ecosystem and evaluation organization.

Lower value for our core question:

> “What are the fundamentally different ways that world-model capability changes one-stage planning?”

Its taxonomy is primarily prediction-modality/application oriented rather than planner-causal-program oriented.

Do not use its modality categories as our route categories.

---

## 2.2 A Survey of World Models for Autonomous Driving

Authors: Tuo Feng, Wenguan Wang, Yi Yang

Latest located version:

- arXiv:2501.11260v4
- 2025-09-10

Main taxonomy:

1. Generation of Future Physical World
2. Behavior Planning for Intelligent Agents
3. Interaction between Behavior Planning and Future Prediction

This survey is conceptually closer to our planning question than a pure modality review.

Confirmed canonical coverage in the accessible v4 text includes:

- LAW
- Epona
- World4Drive
- WoTE

The accessible text did not contain the later canonical papers such as DriveLaW, WorldDrive, Drive-JEPA, Metis, Discrete-WAM or GraphWorld, which is unsurprising given the September-2025 cutoff.

### Value to this project

Useful because it independently reaches an important high-level split:

```text
future-world generation
vs
behavior planning
vs
prediction-planning interaction
```

But it is too early to adjudicate the 2026 WAM wave and too coarse for distinctions now visible in our paper-first Sets A–E.

It should be used as **historical independent taxonomy evidence**, not as the final route map.

---

## 2.3 Latent World Models for Automated Driving: A Unified Taxonomy, Evaluation Framework, and Open Challenges

Authors: Rongxiang Zeng, Yongqi Dong

Status:

- arXiv:2603.09086
- March 2026
- under review at IEEE T-ITS according to author/public metadata

Main organization:

- latent worlds;
- latent actions;
- latent generators;
- continuous/discrete/hybrid representations;
- structural priors;
- several cross-cutting internal mechanics such as temporal stability, semantic alignment, value alignment and adaptive deliberation.

Confirmed canonical coverage in accessible text:

- LAW
- Epona
- DriveLaW
- World4Drive

Not located by exact-string search:

- WorldDrive
- WoTE
- SeerDrive
- Drive-JEPA
- Metis
- Discrete-WAM
- GraphWorld

### Value to this project

Very useful for understanding **latent representation design** and deployment concerns.

But the taxonomy is representation-centric and therefore risks reproducing exactly one of our current warnings:

> a representation distinction can be scientifically important without necessarily defining a planning route.

Use as a profile/design-space calibration source, not a route authority.

---

## 2.4 World Models for Autonomous Driving: From Future Generation to Decision Making

Authors: Han Huang et al.

Status from project page:

- 2026 survey manuscript
- project page cites IEEE Transactions on Intelligent Transportation Systems
- current page still labels it `Manuscript`

This is conceptually the **closest external survey to our actual research question**.

It takes an MPC-oriented view and treats a world model as a predictive transition interface.

Its top-level roles are:

1. Future World Generation
2. Planning With World Models
3. Hybrid Prediction-Planning

It explicitly emphasizes:

```text
state rollout
candidate consequence
cost / constraint exposure
closed-loop utility
```

Representative methods include:

- OccWorld
- Drive-OccWorld
- Think2Drive
- WoTE
- Drive-WM
- GenAD
- DrivingGPT

Among our canonical 12, the project page explicitly contains WoTE but does not currently expose most of the later canonical set by exact name.

### Value to this project

Very high **conceptual value**, lower coverage value.

Its central claim:

> generated futures matter only when planners can consume them

is strongly aligned with our first-principles question.

But its three-role taxonomy remains broad. It does not resolve differences such as:

- Epona shared upstream temporal state vs DriveLaW generator-internal state;
- WoTE explicit simulator-grounded rollout vs WorldDrive distilled future surrogate;
- SeerDrive same-decision mutual refinement vs Drive-OccWorld temporal rollout;
- Drive-JEPA predictive representation vs proposal-selection actionization.

Thus it is a valuable external scaffold, not a replacement for deep mechanism audit.

---

# 3. General WAM surveys — especially important external pressure

## 3.1 World Action Models: A Survey

Authors: Qiuhong Shen et al., National University of Singapore

Status:

- arXiv:2606.20781
- June 2026 preprint

This survey is important because it independently formalizes the notion that future prediction should become **action-facing**.

Its public project page states three simplified shapes:

```text
1. Predict then act
   future first -> action second

2. Score actions
   candidate action -> predicted consequence -> action selection

3. Joint prediction
   future and action in one coupled model
```

It also provides a second, component-level view with:

- predictive substrate;
- backbone;
- action coupling;
- deployment style;
- density.

This is strikingly close to several structures our project independently explored before the paper-first reset.

### Why this is useful

It demonstrates that our earlier attention to:

- future -> action;
- action -> predicted consequence -> selection;
- coupled world/action generation;

was not purely idiosyncratic.

### Why this is NOT validation of M0–M4 or old R/W/E/L

The survey uses a broader embodied-AI literature and a different WAM boundary.

Its public wording itself contains a definition tension:

- one statement says predicted future may help `produce, score, or train` action;
- another says an auxiliary future head discarded before action use does not satisfy the WAM contract.

This tension is directly relevant to our LAW / Drive-JEPA / Latent-WAM / Metis discussion.

Therefore the survey should be audited, not adopted.

Its current public paper list is heavily robotics/embodied oriented and does not appear to provide complete coverage of our canonical driving set.

---

## 3.2 World-Action Models for Robot Learning and Control: A Survey

Authors: Zuxing Lu et al.

Status:

- arXiv:2609.16074
- submitted 2026-09-13
- only a few days old at audit time

This is the newest survey found.

It is robotics-oriented but explicitly includes autonomous driving applications.

Its public taxonomy uses two independent dimensions:

### Architecture

- One Model
- Dual-system

### Transition / action relation

- Joint prediction
- Inverse dynamics / future-to-action style

The project also explicitly notes that WAMs may be useful through:

- representation learning before policy training;
- imagined look-ahead at inference;
- synthetic trajectories for policy improvement.

Its accompanying library currently contains 564 entries and full-text reading reports for hundreds of works. It explicitly includes detailed reports for Epona and Metis, among many other driving/robotics methods.

### Value to this project

Very high as a **latest independent conceptual pressure source**.

Especially useful because it separates:

- architecture;
- transition modeling;
- training pipeline;
- action interface;

instead of forcing all of these into one label.

This strongly echoes the lesson from our Sets B–E that words such as `coupling`, `joint`, and `iterative` are overloaded.

However:

- it is extremely recent;
- it is not peer-reviewed yet;
- it is robotics-wide rather than WAM+one-stage-driving-specific.

Use it as fresh external evidence, not authority.

---

# 4. No survey found that can replace our canonical-12 reconstruction

The search result is important precisely because it does **not** yield an authoritative “answer key”.

The surveys split the field differently:

```text
modality / representation
application role
prediction-planning interaction
MPC transition interface
rendered vs latent future
architecture
joint vs inverse-dynamics factorization
training/deployment use
```

That disagreement itself supports our current caution.

There is no obvious community consensus that one particular set of axes constitutes the correct route ontology.

Therefore the project should not stop paper-first reconstruction and simply import a survey taxonomy.

---

# 5. What external surveys can legitimately do for us

Use them for four purposes.

## 5.1 Domain calibration

Check whether papers we call WAM/world-model planning are considered central or boundary cases by independent authors.

## 5.2 Candidate distinction discovery

When multiple independent surveys repeatedly distinguish something, record it as a pressure question.

Do **not** promote it automatically.

## 5.3 Negative control against self-invention

If we discover a structure that no survey, paper framing, or independent mechanism analysis recognizes, that is not proof we are wrong—but it should raise the evidentiary bar.

## 5.4 External counterexample generation

Use survey taxonomies to generate adversarial pairs:

- methods surveys merge that our paper-first reading separates;
- methods surveys separate that our deep reading finds scientifically continuous.

Those pairs are particularly valuable for ontology testing.

---

# 6. Recommended reading priority

### Priority 1 — peer-reviewed broad AD calibration

**The Role of World Models in Shaping Autonomous Driving: A Comprehensive Survey**

Reason:

- current;
- peer-reviewed;
- AD-specific;
- associated living corpus already contains most canonical papers.

Read it for scope/evaluation/ecosystem, not blindly for route taxonomy.

### Priority 2 — closest conceptual fit to our planning question

**World Models for Autonomous Driving: From Future Generation to Decision Making**

Reason:

- explicitly planner-facing;
- MPC/transition perspective;
- distinguishes generation, planning use, and hybrid prediction-planning.

Read it as an external route hypothesis.

### Priority 3 — general WAM factorization pressure

**World Action Models: A Survey**

Reason:

- independently proposes predict-then-act / score-actions / joint-prediction structures;
- useful comparison with our abandoned/provisional factorization attempts.

Audit its boundary conditions carefully.

### Priority 4 — newest cross-domain WAM synthesis

**World-Action Models for Robot Learning and Control: A Survey**

Reason:

- newest (Sep 2026);
- explicit architecture × transition-modeling distinction;
- strong living library with full-text reading reports.

Use for external conceptual pressure, not as peer-reviewed authority.

### Priority 5 — latent design-space calibration

**Latent World Models for Automated Driving: A Unified Taxonomy, Evaluation Framework, and Open Challenges**

Useful for latent design and evaluation questions, but less suitable as the primary planning-route taxonomy.

---

# 7. Immediate consequence for our research program

Do **not** return immediately to ontology construction.

Before the next adversarial pair audit, perform a dedicated **survey-vs-paper-first calibration** on a very small set of cases.

Recommended cases:

```text
LAW
Epona
DriveLaW
WoTE
GenAD / OccWorld as external controls
```

For each:

1. record how each survey classifies/describes the paper;
2. compare that description to our full-paper reconstruction;
3. identify what the survey preserves and what it compresses away;
4. determine whether any external distinction reveals something our reconstruction missed;
5. determine whether any survey merge creates a false equivalence.

Only after this external calibration should we resume closure of evidence debts and the planned adversarial pair audits.

---

# 8. Current verdict

**FOUND-USEFUL-SURVEYS-BUT-NO-AUTHORITATIVE-CANONICAL12-ROUTE-MAP**

The absence of a single complete survey is not a failure.

It means the target problem remains genuinely open:

> the literature has several independent ways to organize autonomous-driving world models, but no current source fully resolves the mechanism-level routes of recent one-stage WAM planners.

That makes external surveys valuable calibration evidence while preserving the need for careful paper-first reconstruction.
