# NEXT_TASK

## 当前清理闸门

> **在开始 ProSim 前，完成对已删/拟删派生文档的证据复核：每一项独有事实必须能定位到存活的 raw paper、source/code audit、deep analysis 或经核验的主文档。没有完成此复核，不再删除派生材料。**

这项闸门只收口冗余，不改变 Field Reconstruction、17 anchors、Wave C.7 或 ProSim 的科学优先级。

## 闸门后唯一下一任务

> **Verify, ingest and deep-read P0067 ProSim as the second Wave C.7 reactive-simulation control. Keep research-direction convergence paused.**

Canonical expansion plan:

```text
landscape/WAM_DEEP_READ_EXPANSION_QUEUE_V1.md
```

Current phase:

```text
broad WAM literature expansion     ACTIVE
Wave C.6                           CLOSED
Wave C.7                           ACTIVE
research-direction convergence     PAUSED
candidate-problem promotion        PAUSED
method design                      FORBIDDEN
```

Current normalized count:

```text
17 anchors complete
SAFE-SIM COMPLETE
ProSim NEXT / NOT YET NORMALIZED
```

---

# Why ProSim is next

SAFE-SIM established one strong form of reactivity:

```text
external ego planner
→ current ego plan enters learned agent generator/guidance
→ surrounding trajectories regenerate
→ physical environment advances
→ ego and agents replan
```

But SAFE-SIM is safety-critical and explicitly adversarial. One paper is not enough to infer the general structure of reactive learned simulators.

ProSim is selected as an independent control because it emphasizes:

```text
promptable / controllable multi-agent closed-loop simulation
```

rather than primarily planner-specific collision generation.

Primary comparison:

```text
SAFE-SIM
= planner-conditioned adversarial reactive simulation

ProSim
= promptable interactive traffic simulation
```

The central question is:

> Which parts of SAFE-SIM's feedback/reactivity topology are generic to learned closed-loop traffic simulation, and which are artifacts of its adversarial guidance design?

---

# Pre-read source gate — mandatory

Before normalization:

```text
1. verify canonical ProSim paper/version/venue
2. identify attributable official project/code repository
3. pin source version/commit if code exists
4. create papers/raw_md/P0067_ProSim/ readable source note/layer
5. attempt canonical manifest registration; if connector/encoding blocks safe mutation, record an explicit pending note rather than corrupting the manifest
```

---

# Mandatory reconstruction

## 1. Simulator state / representation

Answer exactly:

```text
what is the current scene representation?
what agent/map/history context is encoded?
what does each generated token / trajectory / action represent?
```

## 2. Prompt semantics

Separate all prompt/control types:

```text
agent motion prompt
route / waypoint prompt
goal / destination
text / semantic prompt if any
scene-level constraint
interaction condition
```

For each ask:

```text
training-time or inference-time?
hard condition or soft guidance?
per-agent or scene-level?
```

## 3. Closed-loop feedback graph

Force-fill:

```text
F_e = ego-state / dynamics feedback
F_s = sensor / viewpoint feedback
F_a = surrounding-agent state feedback
F_b = surrounding-agent behavioral-response feedback
```

Reconstruct one full loop and identify which actors replan after the environment changes.

## 4. Joint interaction modeling

Determine whether ProSim:

```text
predicts agents independently
predicts agents jointly
uses autoregressive inter-agent conditioning
uses scene-level latent/token interaction
```

and whether changing ego behavior can change surrounding behavior within the deployed simulator.

## 5. Training truth

Separate:

```text
logged factual behavior supervision
prompt augmentation / synthetic conditions
alternative-action supervision
reactive intervention-response truth
```

Do not call model-generated response `counterfactual ground truth`.

## 6. Inference-time generation

Trace:

```text
current scene
→ prompt / conditioning
→ future/action generation
→ action execution
→ scene update
→ regeneration
```

Separate model decoding/autoregression coordinates from physical simulation time.

## 7. Evaluation

Separate:

```text
open-loop prediction quality
closed-loop behavior realism
collision/off-road validity
interaction metrics
prompt controllability
planner-evaluation usefulness
```

Identify whether ProSim validates reactions to changed ego behavior or only aggregate rollout distributions.

## 8. Immediate cross-paper comparison

Mandatory:

```text
ProSim vs SAFE-SIM
ProSim vs RiskWorld
ProSim vs SafeDrive
ProSim vs WoTE / DA-WAM
ProSim vs BridgeSim / ReactSimBench where evidence allows
```

## 9. Full Ontology V1.3 projection

Force-fill A–P.

Residue watch:

```text
Does prompt-conditioned multi-agent simulation expose a new dimension beyond existing action provenance, feedback, reactivity and truth-source axes?
```

Do not create V1.4 unless a genuine irreducible residue survives back-projection.

---

# Planned artifacts — not yet present

These are outputs of the ProSim task, not current repository files. Do not treat their absence as a broken state or create them during cleanup:

```text
P0067_PROSIM_DEEP_ANALYSIS_V2.md
PHASE_C7_PROSIM_AUDIT.md
P0067_PROSIM_ONTOLOGY_PROJECTION.md
WAM_COMPARISON_MATRIX_V1_3_PROSIM_EXTENSION.md
```

If official source is usable, the same task may additionally produce:

```text
P0067_PROSIM_SOURCE_CODE_AUDIT.md
```

Create only the minimum artifacts required by the evidence actually found; do not pre-create templates or parallel summaries.
---

# Stop condition

ProSim is complete only when:

```text
source/version gate resolved
+
prompt/control semantics explicit
+
closed-loop feedback graph explicit
+
interaction/reactivity mechanism explicit
+
truth-source boundary explicit
+
strongest matched evidence and limitations explicit
+
full A–P ontology projection complete
+
comparison against SAFE-SIM complete
```

Then advance to:

```text
P0013 BridgeSim
```

---

# Guardrail

Continue field reconstruction. Do not reopen research-direction convergence after ProSim.
