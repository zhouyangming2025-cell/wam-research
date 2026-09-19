# PHASE_C_WAVES1_4_FIELD_SYNTHESIS — Planning-Centric WAM Field Reconstruction

Last updated: 2026-09-14

Status: **HISTORICAL PHASE-C SYNTHESIS — problem discovery remains paused; retain comparative evidence only.**

Scope:

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Evidence base:

```text
Phase A census: P0001–P0060, F1–F11 coverage
Wave 1: historical interaction / non-WM planning / evaluation controls
Wave 2: world prediction → planning-interface transition
Wave 3: world–action coupling and latent/imagination interfaces
Wave 4: closed-loop / simulator / reactivity / VLA controls
Research QA Gate: Waves 1–3 Priority-A verification CLOSED
```

Canonical source artifacts:

```text
landscape/PHASE_B_WAVE1_COMPARABILITY_AUDIT.md
landscape/PHASE_B_WAVE2_COMPARABILITY_AUDIT.md
audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md
audits/literature/RESEARCH_QA_GATE_CLOSEOUT.md
audits/literature/PHASE_B_WAVE3_AUTOJEPA_AUDIT.md
audits/literature/PHASE_B_WAVE4_BENCH2DRIVE_HUGSIM_AUDIT.md
audits/literature/PHASE_B_WAVE4_CAUSALDRIVE_AUDIT.md
audits/literature/PHASE_B_WAVE4_ORION_AUDIT.md
audits/literature/PHASE_B_WAVE4_REACTSIMBENCH_AUDIT.md
```

This document reconstructs the field. It is **not** a gap claim and does not authorize method design.

---

# 1. Executive synthesis

The central result of Waves 1–4 is that **planning-centric driving world models are not one model family**. They are a collection of ways in which predictive knowledge about the world, future, interaction, or consequences enters decision making.

The most useful common abstraction is:

```text
history / observation H_t
→ current representation R_t
→ predictive mechanism Φ
→ planning interface I
→ action / trajectory / policy
```

But `Φ` and `I` vary fundamentally.

A learned future may be used to:

```text
A. shape a representation during pretraining/training;
B. remain online as a predictive hidden state that conditions a direct planner;
C. be generated jointly with action in one world-action model;
D. predict one planning-oriented future intent rather than the full scene;
E. generate one future per candidate and score actions;
F. provide an imagined environment for actor/critic or RL policy improvement;
G. provide an interactive learned simulator for planner evaluation/training.
```

Therefore the scientifically useful question is not:

```text
“Does the method use a world model?”
```

but:

```text
WHAT is predicted,
UNDER WHICH action/intent condition,
WITH WHAT supervision,
WHERE does that predictive information enter planning,
AND WHAT evaluation regime validates the claimed benefit?
```

The field’s major recurring lesson is equally important:

```text
more prediction
more complete reconstruction
longer horizon
stronger world/action architectural coupling
more photorealism
more candidate-specific outputs
```

are **not monotonic proxies for better planning**.

Planning value is conditional on:

```text
representation
× prediction accuracy
× horizon
× action conditioning
× supervision
× planner interface
× candidate/scorer quality
× rollout feedback
× evaluation regime
× compute budget
```

---

# 2. Historical evolution: what problem caused each shift?

## 2.1 Before modern WAM: interaction, coupling, ranking and evaluation were already first-class problems

Wave 1 establishes that most conceptual verbs later reused by WAM research already existed:

```text
condition on another agent’s future
model interaction
branch over futures
reason iteratively
jointly predict and plan
score trajectories
refine actions
close the planning loop
```

### M2I / GameFormer

The field already knew that agent futures are dependent and that future-conditioned response can improve prediction/planning. But it also knew that conditioning on a wrong predicted future can hurt. Thus the problem was never merely “predict interaction”; it was how to represent and use uncertain dependent futures robustly.

### UniAD

Planning-oriented task coordination showed that future motion/occupancy and explicit safety objectives could shape an E2E stack without a modern generative WM.

### DiffusionDrive / DriveSuprim

Strong planning gains came from action-distribution modeling, scene-conditioned decoding, hard negatives and candidate ranking without explicit world rollout. DriveSuprim’s top-K oracle analysis showed large headroom can already exist inside the candidate set, making ranking an independent bottleneck.

### What Truly Matters / nuPlan / NAVSIM

Prediction/open-loop metrics were already known to mis-rank downstream driving. The field explored several evaluation compromises:

```text
logged/open-loop evaluation
→ abstract closed-loop planning simulators
→ non-reactive real-data pseudo-simulation
→ later sensor-realistic / reactive / learned simulators
```

**Historical implication:** modern WAM research entered a field where interaction, future modeling, action selection and evaluation mismatch were already active problems. A WAM contribution must be more specific than reintroducing those concepts under a new representation.

---

## 2.2 World generation becomes useful only when a planning interface is defined

Wave 2 captures the transition from “can we generate a plausible future world?” to “how does that future change an action?”

### GAIA-1

Established controllable large-scale driving-world generation, but not an operational planning loop.

### Drive-WM

Introduced a recognizable model-based planning chain:

```text
candidate ego action
→ candidate-specific generated future video
→ detector/map extraction
→ reward
→ action selection
```

This is a major conceptual transition: the imagined world becomes a decision variable.

### OccWorld

Moved the predictive state toward structured occupancy and jointly modeled ego/world futures, but did not perform explicit alternative-action consequence evaluation.

### WoTE

Made the future state an online candidate-evaluation input and, importantly, isolated a future-state increment beyond evaluator-only:

```text
trajectory only       81.0 PDMS
+ evaluator           83.2
+ future world state  85.6
```

This is among the cleanest evidence that a predicted future itself can add planning value in a matched planner family.

### ViDAR / LAW

Established another branch entirely:

```text
future prediction
→ representation learning / auxiliary supervision
→ future output not needed to choose the deployed action
```

So “world-model-assisted planning” already split into:

```text
online model-based planning
vs
predictive representation shaping.
```

---

## 2.3 World–action “unification” fragments into multiple interfaces

Wave 3 shows that `WAM` / `unified world-action model` does not identify a unique architecture.

```text
Epona
= shared historical predictive latent
→ separate visual + trajectory generators

DrivingGPT
= image/action tokens
→ one causal autoregressive language

DriveLaW
= online Video-DiT hidden state
→ Action DiT

Auto-JEPA
= predicted future ego-intent latent
→ trajectory retrieval / scoring

DA-WAM
= candidate_i
→ future latent_i
→ score_i

Think2Drive
= latent transition/reward model
→ imagined actor/critic rollouts
→ improved policy
```

The important historical shift is therefore not “models became more unified.” It is:

```text
world knowledge moved into different locations of the decision process.
```

Training coupling and inference coupling also diverge. Epona can benefit from joint visual/trajectory learning while visual generation is not required in deployment. DriveLaW keeps the world-generator hidden state on the deployed planner path. DrivingGPT is tightly unified at sequence/objective level, but its exact optimized NAVSIM decode path remains unresolved because official code is unavailable.

---

## 2.4 Closed-loop and reactive simulation become their own scientific objects

Wave 4 shows that stronger evaluation cannot be described as one scalar progression from open loop to closed loop.

### Bench2Drive

Standardizes interactive CARLA policy evaluation over many short skills/scenarios.

### HUGSIM

Adds photorealistic sensor/viewpoint feedback from reconstructed real scenes, while actor behavior remains replayed or controller-defined.

### ORION

Provides a strong non-WM control: semantic/traffic-state reasoning, long-term memory and a good reasoning→action interface can produce strong interactive policy performance without explicit world rollout.

### ReactSim-Bench

Makes **learned surrounding-agent reactivity under externally deviated ego behavior** the direct evaluation target.

### CausalDrive

Moves learned behavior generation inside a real-time action-conditioned visual world model and supports planner-in-loop / RL / human-in-loop simulation.

The historical shift is not simply:

```text
open loop → closed loop → reactive WM → causal WM
```

but several overlapping advances in:

```text
policy feedback
sensor feedback
behavior simulation
visual realism
action controllability
learned reactivity
semantic control
simulation speed
```

---

# 3. Architecture map: what kind of “world” is represented?

A planning-centric world state can be arranged along two largely independent axes.

## 3.1 Representation completeness

From rich scene reconstruction toward task compression:

```text
RGB / video
↓
3D geometry / Gaussian / point cloud
↓
occupancy / BEV state
↓
latent predictive state
↓
agent trajectories / behavior
↓
future ego intent / decision latent
↓
reward / value / cost
```

This is not a quality ranking. Moving downward discards scene detail but may retain more decision-relevant structure per token/parameter.

Examples:

```text
GAIA-1 / Drive-WM / CausalDrive   video/RGB future
HUGSIM                            reconstructed 3D Gaussian scene
OccWorld                          occupancy future
WoTE                              BEV future
LAW / DriveLaW / DA-WAM           latent predictive future/state
ReactSim-Bench baselines          trajectory/behavior world
Auto-JEPA                         future ego-motion intent latent
Think2Drive                       compact latent transition/reward state
```

## 3.2 Decision orientation

The orthogonal question is not how rich the world state is, but how directly it is aligned with action choice.

```text
world-complete / renderer-oriented
↕
shared predictive representation
↕
planning-conditioned latent
↕
candidate-conditioned future
↕
value / intent / policy-oriented state
```

The corpus provides direct counterexamples to assuming the two axes are identical:

```text
OccWorld:
better reconstruction can yield worse forecast/planning.

Auto-JEPA:
very compressed future ego-intent representation can support strong planning.

DriveLaW:
planning quality changes dramatically with the exact internal denoising state.
```

Stable conclusion:

```text
WORLD COMPLETENESS != DECISION RELEVANCE
```

This is a field tension, not a theorem that richer worlds are useless.

---

# 4. Planning-coupling map: where does world knowledge enter the planner?

The most useful planning-centric taxonomy after Waves 1–4 is the following.

| interface | mechanism | representative anchors | world future required online? | main causal claim that can be tested |
|---|---|---|---|---|
| **I1 Training-only predictive shaping** | predict future as pretext/auxiliary objective; deployed planner need not consume predicted future | ViDAR, LAW; Epona partly | no | predictive supervision improves representation/policy |
| **I2 Online predictive state → direct planner** | world-model hidden/latent state conditions trajectory decoder | DriveLaW | yes, hidden state | predictive/generative representation improves direct action generation |
| **I3 Joint world-action generation** | world and action generated from shared latent/sequence | Epona, DrivingGPT, OccWorld | varies | joint modeling helps temporal/world-action consistency |
| **I4 Planning-oriented future compression** | predict future ego intent / decision latent then retrieve/select | Auto-JEPA | yes | compressed predictive target is enough for useful action selection |
| **I5 Candidate consequence evaluation** | one candidate → one predicted future → scorer/value | Drive-WM, WoTE, DA-WAM | yes | alternative predicted consequences improve ranking |
| **I6 Imagined environment for policy learning** | learned transition/reward supports actor/critic/RL rollouts | Think2Drive | mainly training-time imagination | model-based imagination improves policy learning |
| **I7 Learned interactive simulator** | action-conditioned world generates next observations/reactions for policy evaluation/training | CausalDrive | simulator is the world | learned world can replace/augment external simulator loop |

ORION is an important control outside this map:

```text
semantic reasoning / traffic-state alignment
→ planning token
→ generative trajectory planner
```

It shows that planning gains attributed loosely to “future understanding” can also arise from strong semantic state representation and action interface without explicit world transition modeling.

---

# 5. Supervision map: what is actually observable?

This is one of the most important structural results of the field reconstruction.

## 5.1 Offline logs give one realized future, not a response function

For a logged scene/history `h`, ordinary driving data provides approximately:

```text
executed ego action a*
realized surrounding future y*
```

It does **not** provide:

```text
y(a_1), y(a_2), ..., y(a_N)
```

for all ego alternatives.

This fact matters little for a factual future predictor but becomes central when a planner asks for candidate-specific futures.

## 5.2 Supervision demand increases with planner interface

### Training-only prediction

LAW / ViDAR / Epona can train against the one observed future because their core predictive objective is factual.

### Candidate-conditioned future evaluation

WoTE / DA-WAM produce many action-conditioned futures, but direct observed supervision is limited:

```text
WoTE audited target path:
alternative ego candidates
+ same logged surrounding future in the target-generation observation.

DA-WAM:
N candidate futures are predicted,
but direct observed-future latent loss is expert-matched only.
```

Therefore:

```text
CANDIDATE-SPECIFIC OUTPUT
!=
CANDIDATE-SPECIFIC OBSERVED COUNTERFACTUAL SUPERVISION
```

## 5.3 Simulators can supply alternatives, but introduce a new realism problem

CARLA / Bench2Drive can execute alternative actions and produce new futures, but actor behavior is simulator/controller-defined.

HUGSIM closes realistic sensor feedback but uses replay/IDM/attack controllers for behavior.

Think2Drive gains interactive transition/reward data from CARLA and then learns a latent imagination model.

Thus simulation resolves **observability** at the cost of a potential **sim-to-real / behavior-model validity** problem.

## 5.4 Learned reactive simulation still lacks real alternative-action GT

ReactSim-Bench deliberately forces off-log ego behavior and can evaluate safety/feasibility of learned reactions, but there is no true real-world trajectory for the unexecuted intervention.

CausalDrive can generate alternate reactions under ego action + sociology prompt, but its semantic labels are mined from observed logs/CARLA clips, not repeated interventions on the same real scene.

Hence the supervision ladder is:

```text
factual observed future
→ proxy candidate labels / rule metrics
→ simulator-generated alternatives
→ reactive-feasibility evaluation under ego deviation
→ semantically controlled alternative synthesis
→ [missing in ordinary logs] real alternative-action response distribution
```

The last step is an evidence limitation of the data-generating process, not merely a missing architecture module.

---

# 6. Action conditioning, reactivity and counterfactual validity are different properties

A recurring source of terminology inflation is to collapse these levels.

A stricter ladder is:

```text
L0: no action condition
L1: action/trajectory is an input
L2: changing ego action changes generated world
L3: surrounding-agent behavior changes with ego action
L4: response is generated by a learned model rather than a fixed script
L5: response remains safe/feasible under off-log ego deviations
L6: response distribution is validated against real behavior under matching intervention
L7: improved response model demonstrably improves planner action choice / policy outcome
```

Examples:

```text
GAIA-1 / Drive-WM:
strong evidence around L1–L2; weaker behavioral counterfactual validation.

WoTE / DA-WAM:
L1–L2 candidate-specific latent futures; no candidate-specific reactive oracle supervision.

Bench2Drive:
L3 exists through scenario/controller logic, not necessarily learned.

HUGSIM:
L3 can exist through IDM/attack controller; replay actors remain non-reactive.

ReactSim-Bench:
directly tests L5 for learned behavior simulators using feasibility/safety proxies.

CausalDrive:
L1–L5 operationally strong and visually rendered, but L6 is not identified.
```

Thus:

```text
ACTION-CONDITIONED
!= REACTIVE
!= REACTIVELY SUPERVISED
!= COUNTERFACTUALLY VALIDATED
!= PLANNING-USEFUL
```

Each transition needs separate evidence.

---

# 7. Evaluation map: what does each benchmark actually validate?

## 7.1 Evaluation regime ladder

```text
E0 generation quality
E1 motion/world prediction quality
E2 open-loop ego trajectory matching
E3 NAVSIM-style non-reactive data-driven planning evaluation
E4 closed-loop non-reactive simulation
E5 reactive abstract closed-loop simulation
E6 CARLA / Bench2Drive-style sensor-policy closed loop
E7 real-vehicle closed loop
```

No regime dominates all others; each makes different compromises.

## 7.2 Four feedback channels

For simulation/evaluation, record:

```text
F_e = ego dynamics feedback
F_s = sensor/viewpoint feedback
F_a = surrounding-agent state feedback
F_b = surrounding-agent behavioral-response feedback
```

Examples:

```text
NAVSIM:
limited ego rollout scoring; F_s absent; F_b absent.

nuPlan:
abstract planner feedback; raw sensor regeneration absent.

Bench2Drive:
F_e/F_s/F_a strong; F_b scenario-controller dependent.

HUGSIM:
F_e/F_s strong; F_b depends on replay vs IDM/attack actor.

ReactSim-Bench:
F_b is directly the learned-model evaluation target; visual F_s is not the point.

CausalDrive:
learned F_s + learned action-conditioned F_b are integrated in one visual world generator.
```

The correct question is therefore not “is this closed loop?” but:

```text
what changes after the ego acts,
what is re-rendered or re-predicted,
who controls surrounding actors,
and what target validates their response?
```

## 7.3 Planner evidence and simulator evidence must not be conflated

A planner can perform well in an interactive simulator without validating the simulator’s real-human response model.

A simulator can achieve good reactive-feasibility metrics without proving that planner rankings improve when using it.

Therefore two separate arrows are required:

```text
simulator fidelity/reactivity → validated simulator property

simulator/world model → changed planner decision → validated planning benefit
```

Many papers establish only one arrow.

---

# 8. Strong non-WM controls: why they remain essential

The full WAM field cannot be understood without methods that achieve strong planning through other mechanisms.

## DiffusionDrive

Shows that multimodal generative **action modeling** can yield strong planning without environment future prediction.

## DriveSuprim

Shows candidate ranking, hard negatives and scorer training can recover large performance without explicit world rollout.

## UniAD

Shows structured prediction, occupancy and explicit collision-aware optimization can improve planning inside an E2E stack.

## ORION

Shows semantic traffic-state supervision, long-term memory and a good reasoning→continuous-action interface can produce strong interactive closed-loop performance without explicit model-based world rollout.

These controls force every WAM paper to answer:

```text
Does the gain come from predicting the world,
or from a stronger representation, action decoder, scorer, reward, training objective, candidate set or evaluation setup?
```

The stronger the non-WM planner becomes, the smaller and more informative the residual incremental value of explicit world modeling may become.

DA-WAM illustrates this directly:

```text
No Future Prediction       93.31 PDMS
Action-Conditioned Future  93.46
+ hard negatives           93.68
```

A candidate-future interface can be scientifically meaningful even when the matched incremental gain over a very strong planner is small.

---

# 9. Recurring trade-offs across independent families

| structural trade-off | gain | cost / risk | evidence anchors |
|---|---|---|---|
| **world completeness ↔ decision relevance** | richer scene reconstruction may preserve broad semantics | capacity spent on visually accurate but decision-irrelevant detail | OccWorld, Auto-JEPA, DriveLaW |
| **long horizon ↔ predictability** | more foresight | uncertainty/error accumulation and weaker useful supervision | LAW; M2I; reactive autoregressive simulators |
| **candidate branching ↔ supervision coverage** | supports explicit alternative-action evaluation | real logs reveal only one executed future | WoTE, DA-WAM, ReactSim-Bench |
| **architectural unification ↔ causal attribution** | shared representation may improve consistency/scale | harder to isolate why planning improves | DrivingGPT, Epona, DriveLaW |
| **photorealism ↔ behavioral validity** | realistic sensor distribution | actor response may still be replayed/scripted/wrong | HUGSIM, CausalDrive |
| **reactivity ↔ verifiability** | off-log agents can respond to ego | exact real counterfactual target is missing | ReactSim-Bench, CausalDrive |
| **online world rollout ↔ efficiency** | direct model-based consequence reasoning | latency/compute/compounding error | Drive-WM, WoTE, CausalDrive |
| **compact latent ↔ interpretability** | efficient decision-oriented state | harder to diagnose physical failure semantics | LAW, DriveLaW, Auto-JEPA, Think2Drive |
| **learned flexibility ↔ assurance** | data-driven multimodal response | difficult to guarantee rules/calibration | learned behavior WMs vs scripted simulators |
| **strong planner baseline ↔ visible WM effect size** | realistic attribution test | future-model increment may appear small | WoTE, DA-WAM, DriveLaW controls |

These are recurrent field structures, not yet selected research problems.

---

# 10. Contradiction / counterexample map

Broad claims that no longer survive the evidence base:

## Claim A — “More / longer future information should improve planning”

Counterexamples:

```text
M2I: wrong predicted influencer future can hurt conditional prediction.
LAW: 1.5 s target > 3 s / 10 s for planning.
DA-WAM: shared global future < no-future baseline.
DriveLaW: t=10 denoising state collapses planning vs t=1.
```

Allowed replacement:

```text
future information is useful only when represented, conditioned and consumed appropriately.
```

## Claim B — “Better world reconstruction means better planning”

Counterexample:

```text
OccWorld higher-resolution tokenizer:
better reconstruction
but worse forecasting and planning.
```

Allowed replacement:

```text
reconstruction fidelity and decision utility are separate objectives.
```

## Claim C — “A WM must roll out explicit future states online to help planning”

Counterexamples:

```text
ViDAR: future forecasting pretraining improves downstream planner.
LAW: auxiliary future latent improves planner while predicted latent is discarded for current test-time action selection.
Epona: joint visual/trajectory learning improves planning although visual generation can be disabled for deployed planner.
```

Allowed replacement:

```text
world modeling can help through representation learning, online state, candidate evaluation or policy imagination.
```

## Claim D — “Candidate-specific future output means candidate-specific counterfactual supervision”

Counterexamples:

```text
WoTE audited targets use fixed logged surrounding futures across ego candidates.
DA-WAM directly supervises observed future latent only for expert-matched candidate.
```

## Claim E — “Closed-loop means realistic interaction”

Counterexamples:

```text
Bench2Drive interaction is simulator/scenario-controller defined.
HUGSIM combines realistic rendering with replay/IDM/attack behavior models.
```

Allowed replacement:

```text
closed-loop must be decomposed into feedback channels and actor-response semantics.
```

## Claim F — “More realistic/log-like behavior simulation means more reactive behavior”

Counterexample:

```text
ReactSim-Bench shows realism rankings can disagree strongly with ego-deviation reactive rankings.
```

## Claim G — “No future NPC layout + action conditioning proves causal counterfactual correctness”

Counterexample/boundary:

```text
CausalDrive removes oracle NPC futures and generates controllable reactions,
but no real alternative-action response ground truth exists for episode-specific causal validation.
```

## Claim H — “A VLM/world model is required for strong interactive E2E driving”

Control:

```text
ORION is a VLA rather than WM planner and obtains large closed-loop gains from semantic traffic-state alignment, memory and action interface.
```

More generally, Bench2Drive has strong non-WM policy baselines and the field contains interactive planners predating modern WAMs.

---

# 11. Evidence-quality map: architecture sophistication and evidence strength are orthogonal

A useful field correction is:

```text
architectural novelty
!= planning effect size
!= evidence quality
```

Examples:

```text
DrivingGPT:
highly unified world/action sequence,
but no clean same-model action-only vs world+action matched control identified.

WoTE:
less architecturally fashionable,
but clean evaluator-only vs evaluator+future ablation isolates a future-state increment.

DA-WAM:
explicit candidate→future→score architecture,
but matched future increment over no-future is small.

Think2Drive:
older Dreamer/RSSM-style latent world,
but genuine repeated CARLA closed-loop policy evidence.

ReactSim-Bench:
not a new WM architecture at all,
but contributes a strong measurement protocol for a property architectures often claim.
```

Field synthesis should therefore rank **claims by evidence**, not papers by architectural sophistication.

---

# 12. Under-measured / weakly identified properties after Waves 1–4

These are **evidence gaps**, not yet research gaps.

## EVIDENCE-GAP 1 — real alternative-action surrounding-agent ground truth

Offline logs contain one realized outcome. ReactSim-Bench and CausalDrive expose the problem but do not create real episode-specific alternative outcomes.

Current proxies include:

```text
collision / TTC / rule compliance
kinematic feasibility
simulator-generated responses
semantic yielding labels
prompt compliance
```

What remains weakly identified is the real conditional response distribution under unexecuted ego interventions.

## EVIDENCE-GAP 2 — reactive simulator quality → planner decision quality

ReactSim-Bench measures simulator response quality.
CausalDrive shows planner/RL applications.
WoTE/DA-WAM show planning interfaces.

But the field still rarely isolates a matched chain:

```text
same state
same candidate action set
better validated surrounding-agent response model
→ different candidate ordering / lower planning regret
```

Do not infer this arrow from either simulator metrics or planner scores alone.

## EVIDENCE-GAP 3 — simultaneous sensor-realistic and behaviorally validated closed loop

HUGSIM is strong on real-scene sensor rendering but behavior is controller-defined.
ReactSim-Bench is behavior-reactivity-focused but not a visual sensor simulator.
CausalDrive integrates visual + learned reaction, but real counterfactual behavioral validation remains proxy-based.

Thus the joint target:

```text
realistic next observation
+ behaviorally valid other-agent response
+ repeated planner interaction
```

is difficult to validate end-to-end.

## EVIDENCE-GAP 4 — intervention-conditioned uncertainty calibration

Many models are multimodal, but the field more often reports best-of-K, generation quality or aggregate safety than calibrated probability over alternative behavior modes conditioned on ego intervention.

For planning, probability calibration can matter differently from mode coverage.

## EVIDENCE-GAP 5 — long-horizon compounding under all feedback channels

NAVSIM removes repeated sensor feedback and surrounding reaction.
LAW shows long horizon can hurt as supervision.
ReactSim shows replan frequency alters reactive quality.
CausalDrive addresses autoregressive exposure bias.

Yet systematic matched evidence for long-horizon planning under simultaneous:

```text
ego state shift
sensor shift
agent response shift
model self-rollout error
```

remains sparse.

## EVIDENCE-GAP 6 — compute-normalized planning benefit

World rollout, candidate branching and video generation can be expensive. Some methods parallelize well (WoTE), some distill for real-time speed (CausalDrive), and direct action models can be very fast (DiffusionDrive).

Planning benefit should ideally be compared under matched:

```text
latency
candidate count
model size
sensor input
training data
```

which is uncommon across papers.

## EVIDENCE-GAP 7 — representation mechanism vs scale/capacity

DriveLaW’s video-latent gains co-vary with large pretraining and Stage-3 joint adaptation. Similar confounds occur in VLM/video/BEV comparisons.

The field often knows that one representation wins, but less often why:

```text
future-prediction semantics?
data scale?
model capacity?
regularization?
architecture compatibility with planner?
```

## EVIDENCE-GAP 8 — real-vehicle closed-loop validation

Most decision evidence remains E2/E3/E5/E6. Claims about real-world interaction generalization are much less common than simulation/NAVSIM results.

## EVIDENCE-GAP 9 — standardized reporting of feedback semantics

Papers frequently use `closed-loop`, `reactive`, `counterfactual`, or `causal` with different operational meanings.

A minimum reporting template should include:

```text
F_e ego feedback?
F_s sensor feedback?
F_a agent-state feedback?
F_b behavioral-response feedback?
who generates agent response?
what supervision validates that response?
what is the replan/update rate?
```

## EVIDENCE-GAP 10 — planner robustness to world-model error

M2I already showed conditional predictions can degrade when the conditioned future is wrong. Modern candidate-world planners create even stronger opportunity for planning to exploit or overtrust incorrect model branches.

Existing evidence is mixed and architecture-specific; the field lacks one universal result connecting world-model uncertainty/error structure to robust downstream action choice.

Again, this is an evidence gap, not a preselected P1 revival.

---

# 13. Ten field-reconstruction completion questions

## Q1. What are the major planning-centric WAM families and why did each arise?

**ANSWERED.**

```text
visual generation/simulation
structured BEV/occupancy prediction
latent predictive representation
training-time future supervision
online future-state conditioning
candidate consequence evaluation
joint world-action generation
planning-oriented future compression
latent imagination / model-based RL
learned reactive visual simulation
```

They arose to solve different combinations of representation learning, future reasoning, action ranking, interactive policy learning, simulation realism and evaluation limitations.

## Q2. What exact information flows observation → future model → planner?

**ANSWERED.**

Seven planning interfaces I1–I7 are mapped above and represented by multiple anchors.

## Q3. What supervision makes each interface learnable?

**ANSWERED WITH STRUCTURAL LIMITATION.**

Factual future supervision is abundant for the executed trajectory; alternative-action response supervision is not. Candidate, simulator, rule, preference and RL signals fill the gap imperfectly.

## Q4. Which methods are truly action-conditioned, counterfactual, reactive or closed-loop?

**ANSWERED OPERATIONALLY.**

The ladder in Section 6 prevents collapsing these terms. True real-world counterfactual behavioral identification remains largely unavailable.

## Q5. Which benchmark regimes support which claims?

**ANSWERED.**

E0–E7 plus F_e/F_s/F_a/F_b provide a concrete map. NAVSIM is not reactive closed loop; Bench2Drive is interactive CARLA; ReactSim directly tests behavior-model reaction; CausalDrive integrates learned visual feedback.

## Q6. What are the strongest non-WM planning baselines and what do they show?

**ANSWERED.**

DiffusionDrive, DriveSuprim, UniAD and ORION show that action modeling, candidate ranking, safety optimization, semantic state representation and reasoning→action interfaces can all produce large gains without explicit online world rollout.

## Q7. What trade-offs recur across independent families?

**ANSWERED.**

Ten recurring structural trade-offs are listed in Section 9, especially completeness↔decision relevance, branching↔supervision, photorealism↔behavior validity, reactivity↔verifiability and rollout↔efficiency.

## Q8. Which common claims have strong counterexamples?

**ANSWERED.**

Eight broad claims are explicitly weakened/killed in Section 10.

## Q9. What capabilities are under-measured rather than merely under-architected?

**ANSWERED AT FIRST PASS.**

Ten evidence gaps are identified in Section 12. The most important distinction is that several missing evidentiary properties cannot be solved merely by adding another network head.

## Q10. Where is evidence contradictory or incomplete?

**ANSWERED.**

Main unresolved zones include:

```text
world completeness vs decision sufficiency
reactive feasibility vs true intervention-conditioned behavior
simulator reactivity vs planner decision improvement
long-horizon prediction benefit vs error accumulation
representation semantics vs data/model scale
online rollout benefit vs stronger scorer/action models
```

No single universal direction is supported yet.

---

# 14. What the field now looks like from the planning viewpoint

The field is best visualized as several paths from predictive structure to action:

```text
                         ┌→ PRETRAIN / AUX LOSS → better R_t ───────┐
observation/history ─→ R_t                                          │
                         ├→ ONLINE WORLD HIDDEN STATE ─→ planner ───┤
                         │                                           │
                         ├→ WORLD+ACTION JOINT GENERATOR ────────────┤
                         │                                           ├→ ego action / trajectory
                         ├→ FUTURE INTENT / DECISION LATENT ─────────┤
                         │                                           │
                         ├→ candidate a_i → future_i → score_i ──────┤
                         │                                           │
                         └→ learned world rollout → actor/critic ────┘

external / learned simulator
→ closes selected feedback channels
→ evaluates or trains the policy
```

There is no evidence that one branch universally dominates.

Instead, the field is converging on a deeper design question:

```text
What predictive information must be preserved,
how should it be conditioned on action,
and at what interface should it influence the planner
for the available supervision and evaluation regime?
```

This is a field-level question, not yet a selected research problem.

---

# 15. Stable field principles after Waves 1–4

The following are now sufficiently supported to be used as project-wide controls:

```text
P-01  World-prediction quality is not itself planning evidence.

P-02  Future information is not automatically beneficial; value depends on representation,
      accuracy, horizon, conditioning, supervision and planner interface.

P-03  Candidate-specific future output is not candidate-specific observed counterfactual supervision.

P-04  WM-assisted planning is not synonymous with online model-based planning.

P-05  Architectural world/action coupling strength is not causal-evidence strength.

P-06  Decision relevance and world completeness are distinct objectives.

P-07  Generative action modeling is not a world model unless environment/world future is modeled.

P-08  Candidate ranking/scoring is an independent planning bottleneck and alternative explanation.

P-09  Closed-loop must be decomposed into feedback channels rather than used as a binary label.

P-10  Sensor photorealism and behavioral realism are independent simulator properties.

P-11  Log realism is not reactive robustness.

P-12  Reactive feasibility is not equivalent to counterfactual behavioral truth.

P-13  Action conditioning is necessary for many reactive interfaces but does not by itself establish causal validity.

P-14  Simulator quality and planner quality require separate evidence chains.

P-15  Strong semantic/VLA planning provides an important non-WM control for claims about explicit world rollout.
```

These principles are methodological constraints for Phase D.

---

# 16. What this synthesis does NOT authorize

Still not allowed:

```text
“the gap is counterfactual planning”
“the gap is risk/value interface”
“the gap is reactive world modeling”
“the gap is decision-oriented latent”
“we should add a risk field”
```

merely because those topics appear in the evidence-gap map.

A valid Phase-D problem must satisfy:

```text
recurrent observed/plausibly measurable planning difficulty
→ cause
→ structural missing capability or trade-off
→ survives strongest prior art
→ survives simpler non-WM explanation
→ matters under realistic evaluation
→ falsifiable before method design
```

`NONE / EVIDENCE INSUFFICIENT` remains valid.

---

# 17. Phase-C verdict

The anchor-based field reconstruction now satisfies the ten completion criteria at first-pass level.

```text
Wave 1  CLOSED
Wave 2  CLOSED
Wave 3  CLOSED
QA Gate CLOSED
Wave 4  CLOSED
Phase C full field synthesis FIRST PASS COMPLETE
```

**Authorization:** Phase D problem discovery may begin.

But the next step is **not method design**. It is an adversarial problem-discovery pass over the recurring tensions/evidence gaps above, requiring each candidate problem to be attacked by:

```text
historical precedent
strongest current method
strongest non-WM control
simpler explanation
counterexample
measurement feasibility
realistic closed-loop relevance
```

Only survivors become research-question candidates.
