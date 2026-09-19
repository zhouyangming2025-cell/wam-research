# DECISION_LOG

Newest entry first.

**读取规则：**本文件是按日期保留的决策历史，不是当前任务队列。发生冲突时，先读 `state/CURRENT_STATE.md` 和 `state/NEXT_TASK.md`；本文件只能提供当时的依据、修正与可追溯性。历史条目中的“authorized / active / next”均不自动恢复效力。

> Integrity note — 2026-09-15: this file had been accidentally truncated during an earlier update. The recoverable project decisions below have been restored conservatively from the project state/history. When a later decision supersedes an earlier one, both are retained and explicitly marked rather than deleting history.

---

## 2026-09-15 — DynFlowDrive normalized; flow transport separated from physical time; Ontology V1.3 authorized

**Decision**

P0063 DynFlowDrive completed the next Phase C.5 dimension-first stress test using the WAM reading skill stack, arXiv v2, official repository state, matched-ablation decomposition and ontology residue/back-projection.

Canonical artifacts:

```text
papers/deep_analysis/P0063_DYNFLOWDRIVE_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_DYNFLOWDRIVE_AUDIT.md
landscape/P0063_DYNFLOWDRIVE_ONTOLOGY_PROJECTION.md
landscape/WAM_COMPARISON_MATRIX_V1_3_DYNFLOWDRIVE_EXTENSION.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_3_AMENDMENT.md
```

**Source/version boundary**

```text
paper: arXiv:2603.19675v2, 2026-05-03
official repo: xiaolul2/DynFlowDrive
latest observed public commit: c665dc577a0939543fa7abe64d28eadaec28283c
```

As of 2026-09-15, the official repository still contains only README/teaser material and states that code will be released once accepted. Implementation-level gradient, solver and freeze details therefore remain `SOURCE-UNVERIFIED`.

Two paper-level mathematical/procedure ambiguities are retained rather than repaired by inference:

```text
Eq.7:
x_s = (1-s)a + s z_{t+1}
→ mathematically dx_s/ds = z_{t+1}-a

Eq.10 target as written:
(1-s)(z_{t+1}-a)

and:
training constructs a noised anchor a,
while sampling prose says integration starts from current latent z_t.
```

**Stable mechanism judgment**

DynFlowDrive must not be summarized as an online `candidate→future→score` planner. Its canonical lifecycle is:

```text
TRAINING:
multimodal planner → candidate trajectories
candidate + current world latent → rectified-flow consequence model
→ reconstruction / flow / transport-stability signals
+ GT trajectory error
→ hybrid positive mode n*
→ supervise planner score head

DEPLOYMENT:
current observation → candidates + learned scores → argmax
world model / future latent / flow integration = REMOVED
```

Canonical subtype:

```text
TRAINING-ONLY FLOW-DYNAMICS MODE-SUPERVISION WAM
```

**Counterfactual boundary**

```text
N candidate-conditioned flow outputs        YES
N observed alternative-action future truths NO
reactive other-agent response truth          NO / NOT ESTABLISHED
```

All candidate-conditioned flow branches ultimately reference one factual next-world latent from the logged sequence. Action conditioning and continuous flow therefore do not establish intervention-valid counterfactual dynamics.

**Strongest matched evidence**

World-model parameterization:

```text
Static WM   0.61 Avg L2 / 0.30 Avg CR
Flow WM     0.59        / 0.26
```

Representation prior:

```text
Flow WM                    0.59 / 0.26
+ pretrained World Feature 0.57 / 0.22
```

Mode-selection teacher:

```text
none              0.61 / 0.30
L2 only           0.59 / 0.24
+ reconstruction  0.58 / 0.22
+ flow stability  0.57 / 0.22
```

Thus the final gain is a bundle of flow parameterization, foundation latent quality, future-state supervision and world-derived positive-mode/score supervision. The final angular flow-stability term is only a modest incremental contributor in the reported ablation.

**Ontology correction**

One new dimension survived merge testing and back-projection:

```text
F08 — Internal transition-coordinate / physical-time alignment
```

It distinguishes:

```text
physical future-time transitions
vs
internal diffusion/flow/transport coordinates
vs
internal representation refinement
```

DynFlowDrive value:

```text
RECTIFIED-FLOW TRANSPORT COORDINATE BETWEEN t AND t+1;
INTERMEDIATE s STATES ARE NOT PHYSICALLY TIME-SUPERVISED
```

Binding controls:

```text
K flow/diffusion steps != K future physical timesteps
smooth latent transport != validated smooth physical evolution
dz/ds != dz/dτ unless s is explicitly identified with physical time τ
```

Back-projection changes interpretation for WoTE, Epona, WorldDrive, SeerDrive, Metis and other anchors, so Ontology V1.3 is authorized.

**Evaluation correction**

The paper calls NAVSIM `closed-loop`; the project-standard label remains:

```text
NAVSIM v1 = NON-REACTIVE DATA-DRIVEN / PSEUDO-SIMULATION PLANNING
```

Therefore 88.7 PDMS does not validate reactive alternative-agent dynamics.

The headline SSR improvement also contains an input confound:

```text
SSR*                            0.39 / 0.15
DynFlowDrive(SSR)               0.35 / 0.14
DynFlowDrive(SSR)+ego status    0.31 / 0.11
```

The more matched WM delta is the 0.39→0.35 row rather than the full 0.39→0.31 headline.

**Next**

```text
Discrete-WAM
```

The next stress test will decompose `unified discrete world-policy learning` into tokenizer/codebook sharing, sequence factorization, parameter sharing, attention visibility, gradient coupling, physical-time semantics and deployment graph.

Phase D remains **PAUSED**. No research-gap declaration or method design is authorized.

---

## 2026-09-15 — Metis normalized; asymmetric world-action co-training separated from online world reasoning; Ontology V1.2 retained

**Decision**

P0062 Metis completed the next post-ontology stress test using the WAM reading skill stack, paper equations/appendix, official repository state and dimension-first back-projection.

Canonical artifacts:

```text
papers/deep_analysis/P0062_METIS_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_METIS_AUDIT.md
landscape/P0062_METIS_ONTOLOGY_PROJECTION.md
landscape/WAM_COMPARISON_MATRIX_V1_2_METIS_EXTENSION.md
```

**Source/version boundary**

```text
paper: arXiv:2606.15869 v1
official repo: LogosRoboticsGroup/Metis
latest observed public commit: 7677b62d786cff8bb2044b489bd41f3d59514b43
```

As of 2026-09-15, the official repository still does not expose training/inference/evaluation implementation despite an earlier August release plan. Therefore implementation details remain `SOURCE-UNVERIFIED`.

An unresolved reporting inconsistency is retained rather than repaired by inference:

```text
main method/README VGE: Wan2.2-5B
expert-capacity table labels: Wan2.2-14B
```

**Stable mechanism judgment**

Metis must not be summarized as an online future-video planner. Its asymmetric training graph is:

```text
FORWARD:
current context → action expert → action representation → future-video expert
future-video → action expert = MASKED

BACKWARD:
future-video loss → VGE → action expert through action-conditioned dependence

DEPLOYMENT:
current context → action expert flow denoising → trajectory
explicit future-video generation = bypassed
```

Canonical subtype:

```text
TRAINING-ONLY ASYMMETRIC WORLD-ACTION CO-TRAINING
→ WORLD-LOSS-SHAPED ACTION EXPERT
→ ACTION-ONLY FLOW POLICY
```

This adds an important stable distinction:

```text
world→action gradient influence
!=
world→action forward information flow
```

**Strongest evidence**

World-task co-training:

```text
w/o video co-training   87.4 PDMS / 87.9 EPDMS
w/  video co-training   89.1 PDMS / 89.5 EPDMS
```

Matched attention topology at 320×384:

```text
Joint       87.4 navtest / 28.0 navhard EPDMS
Isolated    88.3         / 29.4
Asymmetric  88.8         / 31.6
```

Therefore tighter/symmetric coupling is not automatically better; the asymmetric training route is useful relative to full isolation in the reported architecture.

No dedicated quantitative future-video fidelity metric was identified, so:

```text
video co-training benefit
!=
proof that better world-prediction fidelity causes better planning
```

**Historical boundary**

Metis cites Fast-WAM and describes the decoupled inference formulation as inspired by it. The broad principle:

```text
world/video co-training during training
→ skip explicit future generation at inference
```

is therefore prior art. Metis's differentiating mechanism is the specific MoT expert separation + asymmetric attention + video-loss→AE gradient route, not the lifecycle idea alone.

**Ontology stress-test result**

No new dimension survived residue testing. Metis's distinctive directional asymmetry is already expressible by:

```text
E01/E02  action→world forward conditioning
J04      causal/computational coupling direction
L04      gradient coupling direction
M01-M03  future-knowledge lifecycle / model transformation
```

Therefore:

```text
Ontology V1.2 remains active.
NO V1.3 amendment is authorized from Metis.
```

This is treated as evidence that the ontology is becoming stable rather than requiring paper-specific growth.

**Next**

```text
DynFlowDrive
```

Primary next stress test: separate rectified-flow transport time from physical future time and isolate flow-dynamics contribution from stability-aware trajectory selection.

Phase D remains **PAUSED**. No research-gap declaration or method design is authorized.

---

## 2026-09-15 — Drive-JEPA normalized; predictive completion separated from causal future forecasting; Ontology V1.2 authorized

**Decision**

P0049 Drive-JEPA completed the second post-ontology stress test using the WAM reading skill stack, official paper and version-locked source audit.

Canonical artifacts:

```text
papers/deep_analysis/P0049_DRIVEJEPA_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_DRIVEJEPA_AUDIT.md
landscape/P0049_DRIVEJEPA_ONTOLOGY_PROJECTION.md
landscape/WAM_COMPARISON_MATRIX_V1_2_DRIVEJEPA_EXTENSION.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
```

**Stable mechanism judgment**

Drive-JEPA must not be summarized as an online future-world evaluator. Its predictive component is:

```text
V-JEPA random spatiotemporal masked latent prediction
→ driving-domain video pretraining
→ transfer visual encoder into planner
→ JEPA predictor / EMA target branch discarded
```

The deployed full planner is separately:

```text
32 proposals
→ 4 shared-weight proposal refinements
→ human + simulator-selected pseudo-teacher supervision
→ learned PDM/EPDMS utility scorer
→ temporal comfort calibration in NAVSIM-v2 release
→ argmax
```

Therefore its canonical subtype is:

```text
PREDICTIVE REPRESENTATION PRETRAINING
+ SIMULATOR-DISTILLED PROPOSAL POLICY
```

It is retained as a core/boundary anchor because it separates `world/predictive knowledge learned during pretraining` from `world consequence prediction used online`.

**Ontology correction**

One new dimension survived back-projection:

```text
F07 Prediction temporal / observability geometry
```

It distinguishes:

```text
random-mask same-window spatiotemporal completion
past/history-only → unseen future
current → future endpoint
recurrent next-state / autoregressive future
partial-future-context completion
hybrid future masking
```

Back-projection succeeded on LAW, WoTE, Epona, WorldDrive, World4Drive, SeerDrive and ViDAR.

No duplicate dimensions were added for EMA targets, predictor removal, encoder freezing/fine-tuning or repeated proposal refinement because G02, M01–M03, C03/L05 and J08 already represent them.

**Evidence boundary**

Strong evidence supports that V-JEPA-family predictive video representation and driving-domain adaptation improve downstream planning representations. The paper/source do **not** establish that Drive-JEPA deploys a causal world-transition model or that random-mask completion is equivalent to history-only future forecasting.

The full planning score is a bundle of:

```text
predictive visual representation
+
multimodal candidate support
+
simulator-derived utility supervision
+
temporal selection
```

and must not be reported as a monolithic `world-model gain`.

**Additional control strengthened**

Drive-JEPA Table-6 ablation shows:

```text
MTD increases diversity 24% → 40%
but EPDMS falls 86.1 → 84.5 and EC falls 69.7 → 47.9;
adding momentum-aware selection raises EPDMS to 87.8 and EC to 84.8.
```

Thus:

```text
candidate diversity != planning quality
candidate support != candidate selection quality
```

**Next**

```text
Metis
```

Phase D remains **PAUSED**. No research-gap declaration or method design is authorized.

---

## 2026-09-15 — Five-anchor dimension-first synthesis complete; Ontology V1 authorized

**Decision**

LAW, WoTE, Epona, WorldDrive and World4Drive have been re-read/re-projected under the dimension-first protocol. The project must now consolidate the discovered axes before reading additional core papers.

```text
LAW          COMPLETE v2
WoTE         COMPLETE v2
Epona        COMPLETE v2
WorldDrive   COMPLETE v2
World4Drive  COMPLETE v2

NEXT:
merge/split dimensions
→ WAM_DIMENSION_ONTOLOGY_V1.md
→ WAM_COMPARISON_MATRIX_V1.md
```

**Methodological rule added**

Every important module/design choice must trigger an immediate horizontal question:

```text
What scientific function does this serve?
Who else performs the same function?
How do implementation, supervision, deployment and evidence differ?
```

A paper cannot remain inside its own preferred narrative. Missing dimensions must be filled explicitly as `ABSENT`, `NOT REPORTED`, `NOT EVALUATED`, or `NOT APPLICABLE`.

**Stable discoveries entering ontology synthesis**

```text
action-conditioned != WM-based action selection
candidate-specific output != candidate-specific alternative-future supervision
joint modeling != shared representation != shared gradients != online bidirectional feedback
future→score != necessarily value/utility
foundation-prior gain != WM-specific future-model gain
online/offline is too coarse; future knowledge has a deployment lifecycle
consequence teacher != value teacher
prediction fidelity != decision relevance
```

**Gate status**

Phase D problem discovery remains **PAUSED**. No gap declaration or method design until ontology/comparison normalization and remaining core-WAM coverage are adequate.

---

## 2026-09-14 — Phase C.5 core-WAM coverage correction activated; prior Phase-D authorization suspended

**Decision**

The prior Waves 1–4 synthesis remains a useful provisional coordinate system, but it was not sufficient to claim final core-WAM coverage. Phase C.5 was activated to correct missing core-WAM anchors and deepen mechanism/evidence comparability.

```text
Phase A census     CLOSED
Wave 1             CLOSED
Wave 2             CLOSED
Wave 3             CLOSED
Research QA Gate   CLOSED
Wave 4             CLOSED
Phase-C synthesis  COMPLETE FIRST PASS
Phase C.5           ACTIVE
Phase D             PAUSED
```

Core 2.2 WAM remains primary. WAM+VLA is secondary/control. Risk/predictive-risk is optional prior knowledge, not a required destination.

Correction queue at activation:

```text
WorldDrive      COMPLETE
World4Drive     COMPLETE
SeerDrive       NEXT
Drive-JEPA      PENDING
Metis           PENDING
DynFlowDrive    PENDING
Discrete-WAM    PENDING
GraphWorld      PENDING
```

Canonical coverage file:

- `landscape/CORE_WAM_2_2_COVERAGE_AUDIT.md`

Canonical new audits:

- `audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md`
- `audits/literature/PHASE_C5_WORLD4DRIVE_AUDIT.md`

---

## 2026-09-14 — Research OS upgrade: map-first WAM synthesis layer added

**Historical decision**

A higher-level synthesis layer was added above paper ingestion:

```text
paper collection
→ method understanding
→ WAM taxonomy
→ research map
→ problem discovery
```

Artifacts added at the time:

- `RESEARCH_MAP.md`
- `landscape/WAM_TAXONOMY.md`
- `hypotheses/RISK_AWARE_WORLD_MODEL.md`

**Later correction**

This layer was directionally useful, but several artifacts were created before the later Phase C.5 correction and dimension-first deep-read protocol. They are **not canonical scientific authority** where they conflict with `CURRENT_STATE`, `RESEARCH_PRINCIPLES`, Phase-C.5 audits, or the newer dimension-first analyses. In particular, risk-aware WAM is a candidate/probe, not the project destination.

---

## 2026-09-14 — Waves 1–4 field reconstruction synthesized; Phase D authorized

**Historical decision — later superseded by Phase C.5 pause**

At that time the representative-anchor reconstruction was judged sufficient at first-pass level to move into adversarial problem discovery.

```text
Wave 1            CLOSED
Wave 2            CLOSED
Wave 3            CLOSED
Research QA Gate  CLOSED
Wave 4            CLOSED
Phase C synthesis COMPLETE FIRST PASS
Phase D           AUTHORIZED
```

Canonical synthesis:

- `landscape/PHASE_C_WAVES1_4_FIELD_SYNTHESIS.md`
- `landscape/PHASE_B_WAVE4_SYNTHESIS.md`

Stable planning-interface taxonomy from that synthesis:

```text
training-only predictive shaping
online predictive state → direct planner
joint world-action generation
planning-oriented future compression
candidate action → predicted future → score
learned world → policy imagination
learned interactive simulator
```

Stable evidence distinctions:

```text
world completeness != decision relevance
action conditioning != reactive supervision != counterfactual truth
candidate-specific output != candidate-specific observed counterfactual supervision
closed-loop != one feedback regime
sensor photorealism != behavioral realism
log realism != reactive robustness
simulator quality != planner decision quality
```

Any candidate problem must survive historical prior art, strong non-WM controls, simpler explanations, counterexamples, measurement feasibility and realistic closed-loop relevance. Method design remains forbidden until a problem survives falsification.

---

## 2026-09-14 — Wave 2 closed; Wave 3 authorized

**Artifacts**

- `landscape/PHASE_B_WAVE2_SYNTHESIS.md`
- `landscape/PHASE_B_WAVE2_COMPARABILITY_AUDIT.md`
- `audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md`

**Mechanism coverage established**

```text
GAIA-1       controllable generation
Drive-WM     visual-future candidate evaluation
OccWorld     joint occupancy + ego generation
WoTE         online BEV-future candidate evaluation
ViDAR        predictive pretraining
LAW          action-aware auxiliary latent prediction
```

**Evidence boundaries retained**

- Drive-WM: future-based selection is operational, but visual-generation fidelity is not isolated from perception/reward/candidate design.
- OccWorld: headline SOTA rows are heterogeneous; internal representation/dynamics ablations are stronger. Better reconstruction can coexist with worse forecasting/planning.
- WoTE: future-state on/off is useful matched evidence, but audited PDM supervision uses fixed logged surrounding-agent futures across ego candidates.
- ViDAR: predictive pretraining transfers history/BEV encoder; future decoder is not the deployed planning interface.
- LAW: waypoint is generated before future-latent prediction; deployed planning discards latent output. Mechanism = representation shaping, not online rollout evaluation.
- Longer horizon / higher world fidelity are not monotonic planning-value proxies.

Wave-3 anchors authorized at the time:

```text
Epona
DrivingGPT
DriveLaW
Auto-JEPA
DA-WAM
Think2Drive
```

---

## 2026-09-14 — Wave 1 closed after historical/control comparability audit

Binding controls established:

```text
conditional future != intervention
matched controls > headline SOTA
candidate ranking is an independent planning bottleneck
multimodal action generation != world modeling
prediction accuracy != planning evidence
evaluation regime is part of the claim
```

---

## 2026-09-14 — Phase A field census closed; Phase B representative deep reads authorized

**Decision**

```text
F1–F11 audit PASS
broad acquisition FROZEN
Phase B anchors = 25 representative works
research-gap selection CLOSED
method design CLOSED
```

Canonical artifacts:

- `landscape/CENSUS_PHASE_A_ROUND2.md`
- `landscape/FIELD_ATLAS.md`
- `landscape/PHASE_B_ANCHORS.md`

Representative controls/history anchors included:

```text
Hydra-MDP / DriveSuprim / iPad      non-WM planning controls
DriveVLM / OmniDrive / ORION        VLM/VLA planning controls
Think2Drive                         latent-WM-for-RL
ViDAR                               predictive pretraining
GenAD                               trajectory-generation precursor
nuScenes / nuPlan / NAVSIM /
Bench2Drive / HUGSIM                evaluation-history anchors
```

---

## 2026-09-14 — Phase A breadth target reached

**Decision**

```text
P0001–P0060 registered
58 RAW_MD_READY
2 lawful-source blockers
```

Stop bulk acquisition. Expand only when a missing family, historical transition, benchmark regime, counterexample or unresolved scientific structure justifies it.

---

## 2026-09-14 — Field-reconstruction reset

**Decision**

The active program was reset to:

```text
reconstruct field
→ representative anchor deep reads
→ cross-family synthesis
→ only then research-problem discovery
```

Earlier P1/P2-R/P3 work remains historical only and must not determine the field map.

---

## 2026-09-13 — Planning-centric scope + problem-first research identity

**Decision**

Primary research identity:

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Risk/predictive-risk expertise may be useful later but is optional prior knowledge, not a predetermined destination.

Required scientific chain:

```text
field understanding
→ recurrent planning problem / structural trade-off
→ prior-art attack
→ falsifiable research question
→ only then method design
```

---

## 2026-09-13 — P2-R Round 1 parked

No direct observed reaction-induced action-order inversion was established in Round 1. P2-R was parked rather than promoted into an active research gap.

---

## 2026-09-13 — GitHub established as canonical Research Brain

**Decision**

Private GitHub is the cross-session scientific authority.

Source hierarchy:

```text
1. official/canonical PDF = exact authority
2. GitHub raw Markdown + figures = GPT-readable source layer
3. Paper Card = curated paper understanding
4. Field Atlas = cross-paper field understanding
5. state files = canonical research decisions
6. chat = temporary reasoning
```

Canonical PDFs remain local/NAS; repo stores readable text/extracted figures and research state. Exact decision-critical claims should be checked against official paper/source where needed.
