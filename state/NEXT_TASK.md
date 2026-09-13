# NEXT_TASK

## 唯一下一任务

> Build the first neutral **planning-centric WAM field census** before any further gap selection.

Active plan:

`landscape/FIELD_RECONSTRUCTION_PLAN.md`

Taxonomy:

`landscape/PLANNING_WAM_TAXONOMY.md`

Living atlas:

`landscape/FIELD_ATLAS.md`

## Phase A — census construction

Target roughly **50–80 decision-relevant papers** at metadata / abstract / method-overview depth, sufficient to place each paper accurately in the common taxonomy.

The census must cover the field families rather than follow a preselected hypothesis:

```text
F1  visual/video generative driving world models
F2  BEV / occupancy / geometric predictive world models
F3  latent / JEPA / predictive-representation world models
F4  world-model-assisted direct end-to-end planning
F5  candidate-conditioned / action-conditioned future evaluation
F6  unified world-action / trajectory-and-world generation
F7  interactive prediction + planning / contingency / game-theoretic predecessors
F8  reactive world simulation / closed-loop policy training
F9  reward / value / safety / cost interfaces
F10 strong end-to-end planners without explicit world models
F11 evaluation / benchmark / simulator papers
```

Use recent high-quality DWM surveys and planning-oriented E2E surveys to seed coverage, but verify representative primary papers directly.

## Per-paper census output

For each paper record only what is needed for field placement:

```text
Paper
Year / venue
Family labels
World state representation
Predictive/generative mechanism
World-model role
Action conditioning
Interaction/reactivity level
Planning interface
Planning output
Supervision
Evaluation regime
Decision-evidence strength
Main contribution
Main stated limitation
Historical importance / transition role
Placement confidence
```

Do **not** write a novelty/gap verdict during census placement.

## Phase B selection gate

After the census has reasonable coverage, choose roughly **15–25 representative anchor papers** for full deep reading.

Anchor selection must explain the field, not merely attack P2-R. Include:

- foundational generation/simulation WMs;
- occupancy/BEV planning WMs;
- latent/JEPA planning WMs;
- unified world/action models;
- action-conditioned/candidate-specific planners;
- interactive prediction/planning predecessors;
- reactive/closed-loop simulator work;
- strong non-WM E2E planning baselines;
- benchmark/evaluation papers;
- strong counterexamples that invalidate common claims.

## Existing targeted P2-R set

BridgeSim, ReactSim-Bench, CausalDrive, *How Can Driving World Models Do Counterfactual Prediction?*, CRAFT, GameFormer, M2I, and Bahram et al. 2016 remain useful. They now populate F7/F8/F11 and historical-continuity coverage; they are **not** the organizing principle of the whole reading program.

## Stop condition for this task

Stop the first census pass when:

1. F1–F11 each have enough representative papers to explain the family;
2. major 2023–2026 planning-centric transitions are visible;
3. strong non-WM planner baselines and evaluation papers are represented;
4. the 15–25 anchor set can be justified from coverage rather than hypothesis preference.

Then update `FIELD_ATLAS.md` and select the anchor deep-read set.

Do not design methods. Do not declare a gap. Do not optimize the census to rescue or kill P2-R. Do not force risk-field knowledge into the map.
