# Paper-first reconstruction — Set E

Status: evidence reconstruction only; **no route naming, no ontology update, no R/W/E/L or M0–M4 assignment**.

Branch context: `research/core-route-reconstruction`

Papers in this set:

1. SeerDrive — *Future-Aware End-to-End Driving: Bidirectional Modeling of Trajectory Planning and Scene Evolution*
2. Drive-OccWorld — *Driving in the Occupancy World: Vision-Centric 4D Occupancy Forecasting and Planning via World Models for Autonomous Driving*
3. PPAD — *Iterative Interactions of Prediction and Planning for End-to-End Autonomous Driving*
4. GraphAD — *Interaction Scene Graph for End-to-end Autonomous Driving*
5. iPad — *Iterative Proposal-centric End-to-End Autonomous Driving*

Primary evidence:

- `papers/raw_md/P0061_SeerDrive/P0061_SeerDrive.raw.md`
- `papers/raw_md/P0044_DriveOccWorld/P0044_DriveOccWorld.raw.md`
- PPAD official ECCV 2024 paper / arXiv 2311.08100 (no local raw-paper artifact in this set)
- `papers/raw_md/P0003_GraphAD/P0003_GraphAD.raw.md`
- `papers/raw_md/P0023_iPad/P0023_iPad.raw.md`

---

## 0. Audit contract

This set was selected to attack another tempting surface abstraction:

> `iterative`, `interaction`, or `refinement` implies one recurring planning mechanism.

That proposition is **not** accepted.

For each paper we independently reconstruct:

- what exact state/object is iterated;
- what information is fed back;
- whether the loop is inside a planner, inside prediction, between prediction and planning, or between a world model and planning;
- whether iteration unfolds across algorithmic refinement rounds or physical future timesteps;
- whether the iterated predictive object remains online at deployment;
- whether auxiliary prediction is merely training supervision;
- how final ego commitment is produced;
- what disappears under the core-mechanism deletion test.

Only after all five reconstructions do we compare them.

A deliberate negative-control principle is used: **being iterative is not sufficient evidence of a world-model planning loop.**

---

# 1. SeerDrive

## 1.1 Author-stated scientific problem

SeerDrive explicitly attacks the one-shot planning paradigm.

Its motivating claim is stronger than “future features help planning”:

- future scene evolution affects the ego plan;
- the ego's prospective behavior can in turn affect how the future scene should be modeled;
- therefore world modeling and planning should not remain a one-way pipeline.

The paper proposes two related mechanisms:

1. Future-Aware Planning: predicted future BEV features are consumed by the planner;
2. Iterative Scene Modeling and Vehicle Planning: planning-refined ego features are fed back into the world model and the loop repeats.

## 1.2 First-pass future-aware computation

Current multi-modal observations produce a current BEV feature. Anchored multimodal ego trajectories and ego status produce a current ego feature.

The BEV world model receives current scene + ego information and predicts a future BEV feature:

```text
current BEV feature
+ current ego feature
→ BEV world model
→ future BEV feature
```

The planner then reasons using both current and future scene information:

```text
current ego feature
+ current BEV
+ future BEV
→ planning network
→ trajectory / refined ego feature
```

The paper includes an ablation removing future-BEV injection; planning performance degrades. Thus predicted future BEV is not merely an auxiliary training target in the paper design—it is an online planning input.

## 1.3 What is actually iterative

The key loop is feature-level mutual refinement.

After one planning pass, the planner produces a refined ego representation. That refined ego feature is fed back into the BEV world model, which produces a revised future BEV feature. The new future BEV feature then informs the next planning pass.

Simplified:

```text
future BEV^(1)
→ planner
→ refined ego feature^(1)
→ world model
→ future BEV^(2)
→ planner
→ refined ego feature^(2)
→ ...
```

The paper repeats this process `N` times and supervises the future semantic map and planning outputs from the iterations.

Important precision:

> this is not merely a planner repeatedly polishing the same trajectory. A world-prediction state is updated from planning-derived ego information and then re-enters planning.

## 1.4 Refinement rounds are not the same as temporal rollout

SeerDrive's loop should not be casually described as a physical rollout over `t+1, t+2, ...`.

The paper predicts a future BEV reference and repeats the world/planning interaction for a small number of refinement rounds. Its ablation studies 1/2/3 iterations, with two giving the best trade-off.

This is an **algorithmic mutual-refinement loop for one planning decision**, even though the predicted BEV refers to the future.

That distinction becomes important when compared with Drive-OccWorld.

## 1.5 Core mechanism deletion test

Two deletions produce distinct collapses.

Delete future BEV from the planner:

```text
current scene → planner → trajectory
```

The paper loses Future-Aware Planning.

Keep one future BEV pass but delete the planner→world feedback:

```text
current scene
→ one future BEV
→ planner
→ trajectory
```

The paper retains future-aware planning but loses its claimed bidirectional/iterative paradigm.

Thus the reciprocal update is a separately meaningful contribution rather than a synonym for future-aware planning.

## 1.6 What SeerDrive is not

It is not iPad-style proposal self-refinement: the feedback edge crosses from planning back into a predictive world-model state.

It is not GraphAD-style graph/trajectory mutual refinement: the repeatedly updated predictive object is a future BEV scene representation, not an interaction-graph structure.

It is also not automatically equivalent to Drive-OccWorld; their feedback loops unfold at different levels and timescales.

## 1.7 Evidence caveat

This section reconstructs the **paper mechanism**. Earlier project work found pressure between SeerDrive paper semantics and code-level behavior. That paper/code issue is intentionally not resolved by silently replacing the paper method here; a dedicated code re-audit would be required if deployment implementation equivalence becomes decisive.

---

# 2. Drive-OccWorld

## 2.1 Author-stated scientific problem

Drive-OccWorld asks how a learned 4D occupancy forecasting world model can be turned into an actual planning mechanism rather than serving only data generation or pretraining.

Its central ingredients are:

- future occupancy and flow forecasting;
- controllable world generation conditioned on ego actions/trajectories;
- an occupancy-based planner that evaluates candidate trajectories against predicted future state;
- continuous forecasting and planning, where the selected plan conditions later world prediction.

## 2.2 World-model computation

Historical camera observations are encoded into BEV features and accumulated in a memory mechanism. The world decoder predicts future occupancy and flow.

Flexible ego-action conditions can be injected into the world decoder:

```text
history BEV / memory
+ action condition
→ world decoder
→ future occupancy + flow
```

The action condition can take different forms such as velocity, steering angle, trajectory, or high-level command.

## 2.3 Planner computation

The planner uses an occupancy-based cost function to evaluate trajectory proposals against a predicted future state.

Simplified one-step structure:

```text
world model
→ predicted state s_(t+1)

candidate trajectories τ*_(t+1)
+ s_(t+1)
→ occupancy-based cost
→ planner
→ selected τ_(t+1)
```

Here predicted world state is not merely a representation input to a neural policy; it is explicitly part of the candidate-evaluation calculation.

## 2.4 What is actually iterative

The selected trajectory is reintroduced as an action condition for predicting the next world state:

```text
predict s_(t+1)
→ select τ_(t+1)
→ use τ_(t+1) as action condition
→ predict s_(t+2)
→ select τ_(t+2)
→ ...
```

The paper calls this continuous forecasting and planning.

The crucial distinction from SeerDrive is temporal structure:

- SeerDrive repeats world/planning **refinement rounds around a planning decision**;
- Drive-OccWorld alternates forecasting and planning **while rolling the modeled future forward in time**.

Both contain planning→world feedback, but the feedback does not mean the same computation.

## 2.5 Core mechanism deletion test

Delete occupancy-based planning while keeping forecasting:

```text
history/action condition → future occupancy/flow
```

The system becomes a controllable 4D world forecaster and loses the paper's planning integration claim.

Keep one forecast→planner step but remove feeding the selected trajectory into the next world prediction:

```text
forecast once → plan once
```

The model retains world-model-assisted planning but loses continuous forecasting/planning rollout.

Thus the temporal closure is a meaningful additional mechanism.

## 2.6 What Drive-OccWorld is not

It is not merely “future occupancy → planner”. Its paper-level planning proposal explicitly closes the loop by using the selected trajectory as a subsequent world-model condition.

It is not SeerDrive's same-round feature refinement: the planner produces an explicit selected future action/trajectory that conditions the next temporal world prediction.

It is not PPAD's agent-motion game because its predictive carrier is a learned 4D occupancy/flow world state and candidate evaluation uses an occupancy cost.

---

# 3. PPAD

## 3.1 Author-stated scientific problem

PPAD predates the current WAM-specific ontology effort and attacks the standard one-shot prediction→planning pipeline.

Its claim is that driving is a game in which:

- surrounding agents' next motion should depend on the ego's developing plan;
- ego planning should depend on the newly predicted motions of surrounding agents;
- this interaction should be modeled step-by-step over the future horizon rather than predicting all agent trajectories once and planning afterward.

PPAD therefore interleaves **Prediction** and **Planning** at every future timestep.

## 3.2 Scene representation

A perception transformer produces:

- BEV queries/features;
- agent queries;
- map queries;
- an ego query.

The Iterative Prediction-Planning module then operates over these structured representations.

## 3.3 What is actually iterative

At each future step, PPAD alternates two computations.

Prediction process:

```text
agent query / intention
+ ego query updated by previous planning step
+ map
+ BEV
→ agent's next-step motion state
```

Planning process:

```text
updated surrounding-agent motion states
+ ego/map/BEV context
→ ego next-step planning state / motion
```

Then that newly updated ego planning result conditions the next prediction step.

So the core sequence is roughly:

```text
agent prediction(t+1 | ego plan so far)
→ ego planning(t+1 | updated agents)
→ agent prediction(t+2 | updated ego)
→ ego planning(t+2 | updated agents)
→ ...
```

The paper explicitly describes ego and agents as alternately optimizing their motion based on each other's forecasting.

## 3.4 What PPAD's “dynamic environment” means here

PPAD is a strong adjacent contrast for WAM analysis because it has a real deployed prediction↔planning loop without requiring a separately learned generative environment/world-state model.

The predictive object is primarily **surrounding-agent motion state/trajectory**, supported by map and BEV context.

This matters:

> reciprocal prediction/planning does not by itself establish that a method is a WAM route.

A route taxonomy for WAM must first establish the domain/world criterion, then reason about the interaction topology.

## 3.5 Core mechanism deletion test

If prediction is performed once for the entire future horizon and planning runs afterward, PPAD collapses toward the one-shot prediction→planning paradigm that the paper explicitly criticizes.

If the ego result does not feed the next surrounding-agent prediction, the bidirectional game is lost even if both prediction and planning remain present.

Thus the alternating ego↔agent update is central to the paper.

## 3.6 What PPAD is not

PPAD is not iPad: its loop crosses between surrounding-agent prediction and ego planning, whereas iPad mainly refines proposal geometry/queries against sensor features.

PPAD is not GraphAD: GraphAD iteratively refines an interaction graph and agent trajectories before a downstream planning head; PPAD explicitly alternates an ego Planning process and an agent Prediction process at each future timestep.

PPAD is not automatically SeerDrive either. It gives an important conceptual predecessor/adjacent case for reciprocal planning, but SeerDrive introduces an explicit predicted future BEV world representation that is repeatedly regenerated from planner-derived ego features.

---

# 4. GraphAD

## 4.1 Author-stated scientific problem

GraphAD's main problem is not world-model rollout. It argues that generic attention is a weak and inefficient way to represent the geometrically structured interactions among:

- ego;
- traffic agents;
- map/lane elements.

It introduces an Interaction Scene Graph (ISG) with sparse directed edges and explicit geometric priors.

## 4.2 Dynamic Scene Graph

The Dynamic Scene Graph models agent-agent interaction. Edge weights represent how strongly one agent should attend to another.

The important iterative relationship is:

- interaction importance depends on predicted future trajectories (e.g. possible collision);
- updated trajectory predictions can therefore change graph connectivity/weights;
- refined graph features can in turn update predicted trajectories.

Simplified:

```text
interaction graph
→ agent trajectory predictions
→ revise interaction relevance / graph
→ refine agent features/trajectories
→ ...
```

The Static Scene Graph separately models agent↔lane/map relationships.

## 4.3 Planning computation

After graph construction/refinement, the graph-aggregated ego query is combined with ego status and high-level command and passed to a planning head:

```text
structured scene
→ interaction graph refinement
→ graph-aggregated ego feature
→ planning head
→ ego trajectory
```

This is an important distinction from SeerDrive and PPAD.

GraphAD certainly includes the ego as a graph node and predicts future trajectories for multiple agents, but the paper's highlighted iterative loop is primarily within **interaction modeling / motion prediction**. The final planning head is downstream of that refined representation.

## 4.4 Core mechanism deletion test

If the explicit Interaction Scene Graph is replaced with generic dense attention, the paper loses its defining scientific claim even though prediction and planning can still run.

If the iterative dependency between predicted trajectories and dynamic graph interactions is removed, GraphAD loses one of its key interaction-modeling mechanisms but can still retain an ordinary graph-based end-to-end planner.

This asymmetry is useful: the iteration is important, but “iteration” alone is not the whole identity of GraphAD.

## 4.5 What GraphAD is not

It is not evidence that every future-trajectory refinement constitutes a world↔planning feedback route.

It is not equivalent to PPAD: PPAD explicitly alternates the surrounding-agent prediction process with the ego planning process timestep by timestep. GraphAD refines structured interaction representations/trajectory predictions and then feeds the processed ego node to a planner.

It is also not iPad despite both performing iterative feature refinement; the state being refined and scientific purpose are different.

---

# 5. iPad

## 5.1 Author-stated scientific problem

iPad argues that conventional dense BEV representations are computationally expensive and insufficiently planning-aware.

Its proposal is to make candidate ego plans themselves the organizing structure for feature extraction.

Thus its central innovation is **proposal-centric representation learning**, not future-world simulation.

## 5.2 ProFormer loop

At each refinement iteration:

```text
proposal query Q_k
→ predict trajectory proposal P_k
→ use proposal positions/corners as spatial anchors
→ sample relevant multi-view image features
→ update query Q_(k+1)
→ predict refined proposal
→ repeat
```

The predicted plan changes where the model looks in the images; new image evidence then changes the plan.

This is a genuine feedback loop, but its feedback variable is the **planning proposal / proposal-conditioned feature query**.

## 5.3 Final commitment

After the final ProFormer iteration, a lightweight scorer assigns a planning score to refined proposals and selects the highest-scoring trajectory.

```text
iteratively refined proposals
→ scorer
→ argmax / final trajectory
```

No deployed world rollout is required for this loop.

## 5.4 Proposal-centric prediction auxiliary task

iPad also predicts future states of agents most relevant to each proposal, particularly likely collision agents.

This could superficially make the system look like proposal-conditioned consequence prediction.

But the paper explicitly frames mapping/prediction as **auxiliary tasks used during training** to improve planning-oriented representation learning. The main deployed proposal-refinement loop is driven by proposal-anchored visual feature extraction and the final scorer.

Therefore:

> proposal-conditioned future-agent prediction does not automatically place an online predicted world/consequence object on the final commitment path.

## 5.5 Core mechanism deletion test

Remove proposal-anchored feature extraction but retain iterative proposal prediction:

- the paper's ablation shows much of the benefit disappears;
- the core proposal-centric representation thesis is damaged.

Remove proposal-centric auxiliary tasks:

- planning still operates;
- performance falls, but the main ProFormer proposal-refinement mechanism remains.

This helps separate iPad's central mechanism from its auxiliary prediction supervision.

## 5.6 What iPad is not

It is not SeerDrive just because both iterate: iPad does not regenerate an explicit predicted future world state from a planner-derived ego feature at each refinement round.

It is not Drive-OccWorld: no selected plan is rolled forward through an online occupancy world model to create the next future state.

It is not PPAD: surrounding-agent motion prediction does not alternate online with ego planning as the main deployed loop.

---

# 6. Cross-paper comparison — what exactly is being iterated?

Only after the independent reconstructions can the surface word `iterative` be decomposed.

| Paper | Iterated object/process | Feedback edge | Algorithmic/temporal role | Final ego commitment |
|---|---|---|---|---|
| SeerDrive | future BEV representation ↔ planner-refined ego feature | planner-derived ego feature returns to world model; revised future BEV returns to planner | repeated refinement rounds around a planning decision | final trajectory after iterative future-aware planning |
| Drive-OccWorld | future occupancy/flow forecast ↔ selected trajectory across rollout steps | selected trajectory becomes action condition for next world forecast | temporal future rollout | occupancy-cost planner selects trajectory at each step |
| PPAD | surrounding-agent prediction ↔ ego planning | previous ego plan conditions next agent motion prediction; updated agents condition ego | timestep-wise future interaction game | ego future constructed step-by-step |
| GraphAD | interaction graph ↔ predicted agent trajectories/features | predicted motion alters interaction relevance; graph update alters motion | internal structured interaction refinement | downstream planning head reads graph-aggregated ego representation |
| iPad | ego proposals ↔ proposal-anchored visual features | current proposal changes feature-sampling anchors; features refine proposal | planner/representation self-refinement | final proposal scorer selects trajectory |

This table is descriptive, **not a taxonomy**.

---

# 7. The key negative result: `iterative` is not a route

Set E strongly rejects a coarse statement such as:

```text
iterative methods = one mechanism family
```

The five papers iterate different state variables for different scientific reasons.

- SeerDrive iterates between a predicted future scene representation and planning.
- Drive-OccWorld closes a temporal forecast-plan-action-conditioned-forecast rollout.
- PPAD alternates agent motion prediction and ego planning.
- GraphAD iterates an interaction graph with trajectory prediction.
- iPad iterates proposal geometry with sensor feature extraction.

Therefore `iterative` must remain an **audit trigger**.

Before comparing two iterative papers we must ask:

1. What is updated?
2. What feeds back into what?
3. Does the feedback cross the world/planning boundary or remain inside a planner/representation module?
4. Is the loop over algorithmic refinement rounds or future physical timesteps?
5. Does the predictive state remain online?
6. Is the predictive module central or auxiliary?

---

# 8. SeerDrive vs Drive-OccWorld — similar feedback aspiration, different computation

These are the two papers in Set E for which a genuine deployed world/planning feedback relation is best supported.

But even here premature merging would be unsafe.

SeerDrive:

```text
future-BEV estimate
→ planning refinement
→ refined ego feature
→ revise future-BEV estimate
→ planning refinement
```

Drive-OccWorld:

```text
forecast future occupancy at next rollout step
→ evaluate/select trajectory
→ selected trajectory becomes action condition
→ forecast subsequent occupancy
→ evaluate/select next trajectory
```

The former is best understood descriptively as **mutual feature/planning refinement**; the latter as **temporal model-predictive-style world/planning rollout**.

Whether these should eventually sit under one higher-level family, two subfamilies, or remain only related mechanisms is **not decided here**.

---

# 9. PPAD as an essential adjacent counterexample

PPAD is particularly valuable because it has a strong bidirectional prediction/planning loop without requiring a WAM-style world carrier.

This protects the research program from a dangerous inference:

```text
bidirectional planning feedback
⇒ world-model route
```

That implication is false without an independent world/domain qualification test.

PPAD should therefore be preserved as a boundary/contrast case when future route hypotheses are tested.

---

# 10. GraphAD and iPad as negative controls for the word “iteration”

GraphAD shows:

```text
iterative future reasoning
```

can live inside an interaction representation/prediction mechanism while the final planner remains downstream.

iPad shows:

```text
iterative proposal refinement
```

can be a pure planning-aware feature extraction mechanism even when proposal-conditioned prediction auxiliaries exist during training.

These two cases prevent us from promoting iteration count or recurrent architecture itself into a world-planning route distinction.

---

# 11. Core mechanism deletion-test summary

SeerDrive:

> delete planner→world feedback while keeping one future prediction → future-aware planner remains, but the claimed bidirectional iterative paradigm collapses.

Drive-OccWorld:

> delete selected-plan→next-world conditioning → one-shot forecast-assisted planning remains, but continuous forecasting/planning rollout collapses.

PPAD:

> delete ego-plan→next-agent-prediction feedback → ordinary one-shot prediction→planning remains; the traffic-game thesis collapses.

GraphAD:

> delete interaction-graph↔trajectory refinement → graph-based planner can remain, but the dynamic interaction-modeling innovation is weakened; delete ISG entirely and the main paper thesis collapses.

iPad:

> delete proposal-anchored feature feedback → proposals can still be iteratively predicted, but the planning-centric representation mechanism that defines ProFormer collapses.

The five deletion outcomes are different. This is strong evidence that the shared adjective `iterative` is not sufficient for mechanism identity.

---

# 12. Methodological conclusion from Set E

Set E adds one durable paper-reading rule:

> **For every iterative method, identify the loop closure location before interpreting the mechanism.**

A loop may close at:

- proposal ↔ sensor feature extraction;
- graph ↔ trajectory prediction;
- surrounding-agent prediction ↔ ego planning;
- predicted future scene ↔ planning refinement;
- selected action ↔ next temporal world forecast.

These are observations, not new axes.

The next research step should continue paper-first reconstruction and should not turn “loop closure location” into an ontology dimension until repeated independent evidence and deletion/collision tests justify it.

No ontology files were modified in this set.
