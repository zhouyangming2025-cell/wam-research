# NEXT_TASK

## 唯一下一任务

> Complete **Phase-A census placement closeout** and freeze breadth expansion before Phase-B deep reads.

The corpus has already reached the planned breadth scale:

```text
P0001–P0060 registered
58 RAW_MD_READY
2 lawful-source blockers (P0008 NPPC, P0020 Bahram 2016)
```

So the next step is **not another broad acquisition batch**.

## Step 1 — scientifically place the newly ingested Round-2 coverage set

Read `P0021–P0034` at census depth only:

```text
P0021 HydraMDP
P0022 DriveSuprim
P0023 iPad
P0024 DriveVLM
P0025 OmniDrive
P0026 ORION
P0027 Think2Drive
P0028 ViDAR
P0029 GenAD
P0030 nuScenes
P0031 nuPlan
P0032 NAVSIM
P0033 Bench2Drive
P0034 HUGSIM
```

For each record, place it using `landscape/PLANNING_WAM_TAXONOMY.md`:

```text
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
Historical transition role
Placement confidence
```

Do not write novelty/gap verdicts.

Create:

`landscape/CENSUS_PHASE_A_ROUND2.md`

## Step 2 — field-coverage audit

Update `landscape/FIELD_ATLAS.md` and explicitly check whether F1–F11 are now sufficiently represented to explain the field.

Required checks:

- strong non-WM planning controls are not underrepresented;
- WM-RL / policy-learning lineage is represented;
- representation-pretraining bridges are represented;
- benchmark evolution from nuScenes/nuPlan to NAVSIM/Bench2Drive/HUGSIM is explicit;
- visual, geometric, latent, world-action, candidate-conditioned, interactive/reactive and value/safety interfaces are all distinguishable;
- evaluation regimes are not conflated;
- historical predecessors are visible.

`Hydra-MDP++` and `NAVSIM-v2` remain unresolved optional follow-ups. Do not block Phase-A closeout on them unless the coverage audit shows they are essential to explain a transition.

## Step 3 — freeze Phase A and select Phase-B anchors

If the coverage audit passes, stop broad expansion and choose roughly **15–25 anchor papers** for full deep reading.

Anchor selection must optimize for explaining the field, not for supporting a prior hypothesis. The final anchor set should jointly cover:

```text
historical interaction/prediction-planning roots
planning-oriented E2E baseline era
visual/video WM
occupancy/BEV/geometric WM
latent/JEPA predictive representation
WM-assisted direct planning
action/candidate-conditioned future evaluation
world-action unified modeling
WM-RL / policy improvement
reactive simulation / closed-loop evaluation
strong non-WM controls
benchmark/evaluation transitions
```

For every selected anchor, record **why this paper is necessary to explain the field** and which other papers it makes redundant at deep-read depth.

## Stop condition

Phase A closes only when:

1. `CENSUS_PHASE_A_ROUND2.md` exists;
2. `FIELD_ATLAS.md` reflects the new placements;
3. F1–F11 coverage audit is explicit;
4. broad ingestion is frozen;
5. a justified 15–25 anchor set is written down.

Then begin Phase B deep reads.

Do not design methods. Do not declare a gap. Do not reactivate P2-R/P3 as search targets. Do not force risk-field knowledge into the atlas.
