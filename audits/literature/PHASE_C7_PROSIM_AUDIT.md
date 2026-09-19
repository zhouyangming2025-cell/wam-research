# Phase C.7 ProSim Audit

Last updated: 2026-09-19

Status: **COMPLETE FIRST PASS — PAPER + OFFICIAL PROJECT + OFFICIAL SOURCE VERIFIED**

Paper:

~~~
Promptable Closed-loop Traffic Simulation
CoRL 2024
arXiv:2409.05863v1
~~~

Official source:

~~~
Ariostgx/ProSim
78a398c1859b10fbabcc455f1266cf0103f51605
~~~

Canonical analysis:

~~~
papers/deep_analysis/P0067_PROSIM_DEEP_ANALYSIS_V2.md
papers/raw_md/P0067_ProSim/P0067_ProSim.source_note.md
~~~

No separate source-code audit file is created: the code audit below is the minimum evidence-bearing phase record, and the A–P audit remains in the deep-analysis file.

---

# 1. Source gate

| Gate | Result | Evidence |
|---|---|---|
| Canonical paper/version | PASS | arXiv:2409.05863v1, submitted 2024-09-09, CoRL 2024 |
| Attributable project | PASS | ariostgx.github.io/ProSim |
| Official code | PASS | github.com/Ariostgx/ProSim |
| Code pin | PASS | 78a398c1859b10fbabcc455f1266cf0103f51605, 2024-10-22 |
| Readable source note | PASS | papers/raw_md/P0067_ProSim/P0067_ProSim.source_note.md |
| Full training reproducibility | NOT ESTABLISHED | README says training pipeline is still to be released |
| Canonical manifest row | PENDING | CORPUS_MANIFEST.csv is binary/non-UTF-8 through connector; no bytes changed |

---

# 2. Stable mechanism judgment

ProSim is a:

~~~
PROMPTABLE CLOSED-LOOP TRAFFIC BEHAVIOR SIMULATOR
+ SOFT MULTIMODAL AGENT/SCENE CONTROL
~~~

Core cycle:

~~~
map + histories
→ scene tokens
→ prompt-conditioned policy tokens
→ parallel k-step state chunks
→ generated observations
→ updated scene tokens
→ repeat
~~~

It is not primarily a planning WAM, a candidate scorer, or a sensor-rendering simulator.

---

# 3. Evidence ledger

| Claim | Paper evidence | Code evidence | Audit judgment |
|---|---|---|---|
| Initial state is map + agent histories | σ=(M,A), encoder section | encode_scene; init_obs/init_map | VERIFIED |
| Policy tokens are generated once | Encoder/Generator/Policy decomposition | generate_policy before rollout_batch | VERIFIED |
| Dynamic state is refreshed | Policy dynamic observation update | step_env → update_scene_emb | VERIFIED |
| Agents interact | shared scene/agent tokens | scene encoder agent-agent attention; parallel policy calls | VERIFIED, next-chunk |
| Prompts are multimodal | goal/route/action/text | condition_encoders.py; text attention paths | VERIFIED |
| Prompts are soft | learned embeddings, no projection/feasibility solver | policy-token addition and cross-attention | VERIFIED |
| Training uses logged trajectory | full-rollout imitation | io_pairs_batch and compute_rollout_loss | VERIFIED |
| Prompt labels reflect GT | prompt labeling section | goal/route/tag/text data formatters | VERIFIED |
| Alternative response truth exists | no such paper claim | no intervention-response target path | ABSENT |
| Paper claims closed-loop training | full rollout and BPTT described | source supports switch | QUALIFIED |
| Public default performs full BPTT | not stated as release config | MODEL.BPTT=False; detach branch | NOT ESTABLISHED / default NO |
| WOSAC interaction score proves reactive validity | benchmark result | GPU rollout path | NO; distributional benchmark only |

---

# 4. Feedback coordinates

~~~
F_e  YES
     Generated state is appended to each controlled agent history and re-encoded.

F_s  NO / NOT CORE
     No camera, LiDAR, viewpoint or renderer feedback in the ProSim model path.

F_a  YES
     Refreshed agent tokens and agent-agent attention expose surrounding states.

F_b  YES, simulator-level
     A generated agent can change another generated agent's next chunk through
     shared scene tokens; this is not real intervention-response truth.
~~~

Most important qualification:

~~~
step_env starts from batch.extras.fut_obs[t] and overwrites controlled IDs.
Non-target valid IDs can retain logged future observations.
~~~

The full-all-agent demo is stronger than a mixed generated/logged rollout, but the source path must be checked per experiment.

---

# 5. Training truth and inference truth

| Layer | ProSim status |
|---|---|
| Logged factual behavior | WOMD agent futures |
| Prompt augmentation | noisy route, temporal tags, text paraphrases, random masking |
| Synthetic condition | yes, but conditions are tied to the logged scene |
| Alternate action target | no |
| Reactive intervention target | no |
| Generated simulator response | yes at inference/rollout |
| Causal identification | no |

Do not upgrade “generated response” to “counterfactual ground truth.”

---

# 6. Configuration and release audit

## 6.1 BPTT

The paper says the closed-loop design can backpropagate through time. The public default is:

~~~
config.MODEL.BPTT = False
step_agent_traj: pred_trajs.detach()
~~~

Therefore the audited release supports the mechanism but does not establish full differentiable state feedback in its default demo configuration.

## 6.2 Auxiliary losses

The paper reports imitation + collision + off-road terms. The released with_text/no_text/waymo_demo YAMLs set:

~~~
USE_OFFROAD_LOSS: False
USE_COLLISION_LOSS: False
~~~

Those YAMLs are demos, not proof that the paper’s private/full training configuration omitted the terms.

## 6.3 Rollout paths

~~~
GPU/distributed batch rollout → implemented and source-auditable
trajdata rollout callback   → rollout_scene_loop is TODO/returns None
standalone distributed CLI  → contains a stale registry-name path
~~~

The scientific mechanism is retained, but reproducibility claims must name the path used.

## 6.4 Prompt injection at rollout

ImitationBatchFormat does not populate general condition data for the ROLLOUT split. The GPU distributed path can add sampled goal conditions, but the trainer-level path does not automatically reproduce every text/action-tag prompt evaluation. Promptable notebook demos and training/evaluation callbacks are not interchangeable evidence.

---

# 7. Evaluation boundary

ProSim’s strongest quantitative controls are:

~~~
ADE against the prompt-aligned logged rollout
% Gain against the unprompted rollout
WOSAC composite / kinematic / interactive / map-based scores
~~~

These establish:

~~~
prompt adherence and distributional rollout quality
~~~

They do not establish:

~~~
response correctness to an independently controlled AV
paired intervention-response accuracy
causal validity of a generated reaction
~~~

ReactSimBench is retained as the relevant external control because it decouples AV control and supplies deviated AV behaviors. BridgeSim is retained as the platform control for log-replay/IDM/adversarial evaluation modes. Neither is silently merged into ProSim’s evidence.

---

# 8. Comparison decision

~~~
ProSim vs SAFE-SIM
  ProSim = promptable all-agent simulator.
  SAFE-SIM = planner-conditioned adversarial reactive simulator.
  Both have generated behavioral response but no paired real intervention truth.

ProSim vs RiskWorld / SafeDrive / WoTE / DA-WAM
  ProSim is an external simulator; these are planner-facing representation,
  consequence or safety/value systems. Their logged/teacher targets cannot
  be treated as ProSim-style endogenous reaction.

ProSim vs BridgeSim / ReactSimBench
  BridgeSim is an evaluation platform with multiple traffic modes.
  ReactSimBench is a direct reactive-validity benchmark with deviated AV input.
  They are controls for evaluation semantics, not additional ProSim modules.
~~~

---

# 9. Residue and ontology decision

Prompt-conditioned multi-agent simulation maps onto existing:

~~~
D/H  control and branch provenance
E/I/J/P  feedback, interaction and reactivity
G/O   truth-source and evaluation semantics
L/M   training/deployment lifecycle
~~~

No irreducible residue survives back-projection. Decision:

~~~
V1.3 retained
NO V1.4
NO projection artifact
NO comparison-matrix extension
~~~

---

# 10. Completion and next task

ProSim meets the Wave C.7 stop condition:

~~~
source/version gate resolved
prompt/control semantics explicit
feedback graph explicit
interaction mechanism explicit
truth boundary explicit
evaluation limitations explicit
A–P audit in the canonical deep analysis
SAFE-SIM comparison complete
~~~

Wave C.7 can advance to:

~~~
P0013 BridgeSim
~~~

Research-direction convergence remains paused, candidate promotion remains paused, and method design remains forbidden.
