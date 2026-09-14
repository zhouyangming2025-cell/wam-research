# PHASE_B_WAVE2_COMPARABILITY_AUDIT — Planning Attribution, Supervision, and Interface Boundaries

Last updated: 2026-09-14

Status: **COMPLETE — closes the Wave-2 comparability gate**

Scope:

```text
GAIA-1
Drive-WM
OccWorld
WoTE
ViDAR
LAW
```

Purpose: determine how strongly each paper supports the claim that **future/world modeling itself** improves planning, rather than a competing mechanism such as reward design, state representation, pretraining initialization, candidate scoring, or benchmark choice.

This audit supplements:

- `landscape/PHASE_B_WAVE2_SYNTHESIS.md`
- `audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md`

---

## 1. Evidence-strength rubric used in this audit

For a planning-centric WM mechanism, evidence is stronger when the paper isolates:

```text
same observations / backbone
same planner / candidate set
a future-model component changed
same supervision except for the target mechanism
same post-processing/reward
a planning-side metric changed
```

Evidence is weaker when the comparison simultaneously changes input quality, planner architecture, supervision, candidate set, reward, or metric implementation.

The rubric is not a paper-quality ranking; it grades only the causal specificity of the planning claim.

---

## 2. GAIA-1 — generation capability, planning evidence absent

### What is demonstrated

GAIA-1 demonstrates an action/text-conditioned generative driving model that can roll out visually plausible future scenes and respond qualitatively to changed conditions/actions.

### Planning-attribution status

```text
operational planner interface: NO
planning benchmark:           NO
generated-future selection:   NO
```

Therefore there is no quantitative attribution problem to solve: GAIA-1 should not be used as direct evidence that generated future video improves planning.

### Evidence grade for planning value

```text
D0/D1 — capability precursor only
```

### Stable field interpretation

GAIA-1 establishes that a generative model can represent controllable driving-world evolution. It does not establish decision utility.

---

## 3. Drive-WM — future-based selection is real, but generation quality is not isolated from reward/perception

### Planning setup actually compared

The planning experiment replaces the ground-truth VAD driving command with three candidate trajectories corresponding to `go straight / turn left / turn right`, generates candidate-specific future video, extracts map/object information from the generated future, computes image-based rewards, and selects the candidate.

Reported average planning rows:

```text
VAD + GT command       L2 0.72 / collision 0.22
VAD + random command   L2 1.02 / collision 0.93
VAD + sampled command  L2 0.87 / collision 0.47
Drive-WM selection     L2 0.80 / collision 0.26
```

This is useful evidence that **using generated futures to choose among candidate commands** improves over random or distribution-sampled command choice and approaches the oracle-like GT-command upper reference.

### Reward ablation

The paper separately ablates map/object rewards. The combined reward reaches about:

```text
L2 0.80 / collision 0.26
```

and improves especially over weaker reward choices on collision.

This establishes that the downstream reward interface materially contributes to the final planning result.

### Generation-quality ablations are on a different experimental axis

Drive-WM reports video-generation ablations such as:

```text
FID / FVD / KPM
unified conditions
multiview temporal tuning
factorized generation
```

For example, factorized generation dramatically raises KPM (`45.8 → 94.4`) while FVD/FID remain similar.

But the paper does **not** provide a matched table showing that this generation-quality improvement produces a corresponding planning improvement with reward/candidates held fixed.

Therefore the chain:

```text
better FID/FVD/KPM
→ better planner
```

is not directly established.

### Main confounds that remain inseparable

Drive-WM's final selection depends jointly on:

```text
future-video model
3D object detection on generated images
online HD-map perception
map/object reward definitions
three-command candidate set
```

The paper isolates reward composition better than it isolates world-model fidelity.

### Evidence grade

```text
D2 for “generated future can be used to improve candidate choice”
D1 for “better visual-generation fidelity causes better planning”
```

### Stable interpretation

Drive-WM is a valid early **future-as-evaluator interface**, but its experiment should not be read as a pure world-dynamics ablation.

---

## 4. OccWorld — main SOTA table is heterogeneous; internal ablations are the scientifically clean evidence

### Metric-normalization issue

Table 2 contains two metric families in the same visual table:

```text
standard/default computation
and
rows marked † using the VAD metric computation
```

Examples:

```text
OccWorld-O      avg L2 1.17 / collision 0.60
OccWorld-O†     avg L2 0.64 / collision 0.24

VAD-Base        avg L2 1.22 / collision 0.53
VAD-Base†       avg L2 0.72 / collision 0.22
```

These numbers must not be mixed across metric implementations.

### Main-table method comparisons also change inputs/supervision

The named variants differ substantially:

```text
OccWorld-O  input = GT 3D occupancy; aux supervision = none
OccWorld-D  input = camera;          aux supervision = 3D occupancy
OccWorld-T  input = camera;          aux supervision = semantic LiDAR
OccWorld-S  input = camera;          aux supervision = none
UniAD       input = camera;          many auxiliary labels
```

Therefore the main SOTA table does not isolate “world-model architecture” from input/label quality.

### Cleanest evidence 1 — tokenizer representation ablation

Within OccWorld-O and one metric protocol, scene-tokenizer settings change while the same downstream task is evaluated.

Default:

```text
reconstruction mIoU/IoU = 66.38 / 62.29
forecast mIoU           = 17.14
planning avg L2         = 1.17
```

Higher-resolution tokenizer:

```text
reconstruction mIoU/IoU = 78.12 / 71.63
forecast mIoU           = 12.38
planning avg L2         = 1.36
```

This is strong matched evidence that maximizing reconstruction is not the same as maximizing predictable/decision-useful state quality.

### Cleanest evidence 2 — spatial/temporal world-model ablation

Full OccWorld-O:

```text
forecast mIoU 17.14
planning L2   1.17
collision     0.60
```

Without temporal attention:

```text
forecast mIoU 8.98
planning L2   2.06
collision     2.56
```

Without spatial attention:

```text
forecast mIoU 10.07
planning L2   1.42
collision     1.21
```

This is materially cleaner evidence that the spatial-temporal generative mechanism contributes jointly to future forecasting and ego planning within the structured-world setup.

### Evidence grade

```text
D3 for internal tokenizer / temporal-model mechanism evidence
D1–D2 for broad cross-method “OccWorld beats planner X because WM” claims
```

### Stable interpretation

OccWorld is strongest as evidence for **representation/predictive-dynamics design**, not as a clean SOTA proof of world-model superiority over all end-to-end planners.

---

## 5. WoTE — strongest Wave-2 evidence that an online predicted future adds value beyond scorer-only

### Matched ablation

The same NAVSIM input/backbone/candidate family is evaluated while adding trajectory evaluation and then future states:

```text
Traj. Eval × / Future ×   81.0 PDMS
Traj. Eval ✓ / Future ×   83.2 PDMS
Traj. Eval ✓ / Future ✓   85.6 PDMS
```

This yields two distinct increments:

```text
learned evaluator alone: +2.2 PDMS
future-state input:       +2.4 PDMS on top
```

This is one of the cleanest current controls against the Wave-1 alternative explanation “the method only has a better scorer.”

### But the supervision is richer than factual driving logs

For fast training the paper states it pre-computes simulation results including BEV semantic maps and scores for trajectory anchors. The rewarder also receives imitation plus NAVSIM simulation-derived supervision.

Thus the matched future-state ablation supports the usefulness of future states **within this enriched supervision pipeline**, not the necessity of world modeling under equal supervision to a simple imitation-only planner.

### Source-code reactivity finding

At public commit:

```text
liyingyanUCAS/WoTE
298957c128a91d41a1c6075bd0bb6e7e845e093f
```

multi-candidate PDM target generation:

1. simulates each candidate **ego** trajectory;
2. scores all candidates against `metric_cache.observation`;
3. builds `metric_cache.observation` from `scenario.get_tracked_objects_at_iteration(...)` and interpolates the logged/GT future tracks;
4. does not regenerate/react surrounding-agent futures per ego candidate.

Hence:

```text
online candidate-specific WM:                 TRUE
future-state used by planner:                 TRUE
candidate-specific ego simulation/reward:     TRUE
reactive oracle target for surrounding agents: NOT PRESENT in audited path
```

### Evidence grade

```text
D3 for “predicted future state adds value beyond evaluator-only on NAVSIM”
D1 for “candidate future is behaviorally correct reactive counterfactual response”
```

The latter is an absence of evidence, not evidence that the learned candidate branches are necessarily wrong.

### Stable interpretation

WoTE is the strongest Wave-2 anchor for **online candidate-specific future-state evaluation**, but not a benchmarked reactive social world model.

---

## 6. ViDAR — transfer mechanism is encoder pretraining; future decoder is not the downstream planner

### What is actually transferred

The paper explicitly defines the **History Encoder** as the target structure for pretraining. In the default setup it matches the BEVFormer-base encoder used by downstream systems.

ViDAR adds:

```text
History Encoder
→ Latent Rendering
→ autoregressive Future Decoder
→ future point-cloud target
```

For downstream tasks, the pretrained BEV/history encoder is transferred. The ViDAR Future Decoder is a pretraining head, not the downstream UniAD planning interface.

### UniAD downstream protocol

For UniAD:

```text
ViDAR pretraining
→ fine-tune BEVFormer for 3D detection
→ use it as initialization for the standard UniAD two-stage fine-tuning pipeline
```

The downstream architecture remains UniAD; the initialization changes.

Reported planning:

```text
UniAD       avg L2 1.12 / avg collision 0.27
ViDAR-init  avg L2 0.91 / avg collision 0.23
```

The paper notes these are averaged over future timestamps and explicitly warns about metric-reporting conventions versus some prior 3 s-only numbers.

### What is isolated and what is not

This is good evidence for:

```text
future point-cloud forecasting pretraining can produce a stronger initialization for the same downstream E2E stack
```

It is not a clean decomposition of which part of the pretext task caused the gain:

```text
future temporal prediction
vs LiDAR geometric supervision
vs latent rendering geometry
vs simply additional pretraining exposure
```

### Critical negative/matched control

The paper's forecasting-structure ablation is highly informative:

```text
no forecasting pretrain             NDS 44.11
differentiable ray-casting pretrain NDS 40.20
latent-rendering ViDAR pretrain      NDS 47.58
```

So “future forecasting pretraining” alone can actually make a transferred representation worse. The representation interface determines whether the predictive objective is useful.

### Evidence grade

```text
D3 for predictive-pretraining / representation-transfer benefit
D1–D2 for isolating temporal-dynamics learning from LiDAR/geometric pretraining effects
```

### Stable interpretation

ViDAR is a world-model **pretraining** result, not online model-based planning. Its strongest scientific lesson is that the future objective must be mediated by a downstream-useful latent representation.

---

## 7. LAW — source audit upgrades the role classification and narrows the planning claim

### Matched planning ablation

Perception-free branch:

```text
no WM                       0.71 L2 / 0.41 collision
visual-latent prediction    0.68    / 0.37
+ ego-trajectory condition  0.61    / 0.30
```

Perception-based branch:

```text
0.54 / 0.25
0.52 / 0.21
0.49 / 0.19
```

The paper therefore provides reasonably matched evidence that:

```text
future-latent auxiliary prediction helps
and action-aware conditioning helps further
```

### Inference-path source fact

At public commit:

```text
BraveGroup/LAW
b2f6a784247072923c477ab92324d3aa5a9759bf
```

`WaypointHead.forward` computes the current waypoint first, then calls the WM branch using that waypoint. Training uses a future-latent reconstruction loss. `simple_test_pts` returns/uses the ego trajectory and discards both latent outputs.

Thus there is no audited test-time causal path:

```text
predicted future latent → current trajectory selection
```

The planning gain comes through parameters/features shaped during training.

### Horizon evidence

The action-aware prediction horizon is non-monotonic:

```text
0.5 s   0.61 L2 / 0.30 collision
1.5 s   0.58    / 0.25
3.0 s   0.63    / 0.27
10.0 s  0.72    / 0.43
```

This is direct internal evidence that more distant future supervision can become less useful or harder to learn for the planner.

### Evidence grade

```text
D3 for “action-aware future-latent auxiliary learning improves the same planner family”
D0 for “online future latent is evaluated to choose the current action” — this mechanism is absent in audited code path
```

### Stable interpretation

LAW is an important **representation-shaping** WAM, not an online rollout evaluator.

---

## 8. Cross-paper supervision matrix

| paper | factual future target | alternative-action branches | direct candidate-specific supervision | surrounding-agent response per candidate | planner consumes future online |
|---|---|---|---|---|---|
| GAIA-1 | real video | generated from altered condition | no matched oracle per branch | not behaviorally oracle-validated | no planner |
| Drive-WM | real video | yes | no reactive oracle for every candidate | generated/inferred | **yes** |
| OccWorld | occupancy + ego future | no explicit candidate set | no | factual joint future | joint generation, not candidate evaluation |
| WoTE | simulator/log-derived BEV/reward | **yes** | ego/reward labels yes | **fixed logged tracks in audited PDM path** | **yes** |
| ViDAR | future LiDAR/point cloud | no | no | n/a | no |
| LAW | factual future latent | no candidate set | no | n/a | **no** for WM output |

This table makes the core evidence boundary explicit:

```text
candidate-specific model output
!= candidate-specific oracle supervision
!= reactive counterfactual supervision
```

---

## 9. Cross-paper comparability verdicts

| comparison/claim | verdict | reason |
|---|---|---|
| GAIA-1 generation metrics → planning quality | **UNSUPPORTED** | no planner experiment |
| Drive-WM random/sampled candidate vs future-based selection | **USEFUL SYSTEM EVIDENCE** | same VAD context; candidate-selection mechanism operational |
| Drive-WM better FID/FVD/KPM → better planning | **NOT ISOLATED** | generation ablations not linked to matched planning ablation |
| OccWorld main SOTA rows across all methods | **HETEROGENEOUS** | different inputs, auxiliary supervision, and `†` metric implementation |
| OccWorld tokenizer / temporal-attention internal ablations | **STRONG MATCHED** | same model family; clean representation/dynamics changes |
| WoTE scorer-only vs scorer+future | **STRONG MATCHED** | isolates future-state input inside same NAVSIM setup |
| WoTE candidate-specific future → reactive response correctness | **NOT ESTABLISHED** | audited target path uses fixed logged-agent futures |
| ViDAR UniAD vs ViDAR-pretrained UniAD | **STRONG TRANSFER RESULT** | same downstream UniAD family; initialization/pretraining differs |
| ViDAR gain → temporal dynamics specifically | **PARTIALLY ISOLATED** | future prediction, LiDAR geometry, latent rendering and extra pretraining jointly change |
| LAW no-WM vs visual-latent vs action-aware latent | **STRONG INTERNAL** | direct staged auxiliary-objective ablation |
| LAW future latent → online current action | **FALSE FOR AUDITED PATH** | future latent is computed after waypoint and discarded by test planner |
| longer future horizon → better planning | **COUNTEREXAMPLE EXISTS** | LAW 1.5 s better than 3 s/10 s |
| higher reconstruction fidelity → better planning | **COUNTEREXAMPLE EXISTS** | OccWorld high-res tokenizer reconstructs better but forecasts/plans worse |

---

## 10. Wave-2 field claims adjudicated

These are **field-understanding claims**, not research gaps.

### Claim: higher world fidelity improves planning

```text
Status: MIXED / COUNTEREXAMPLE EXISTS
```

OccWorld directly violates monotonicity between tokenizer reconstruction fidelity and downstream forecasting/planning. Drive-WM does not supply a matched fidelity→planning causal curve.

### Claim: action conditioning improves planning because it models consequences

```text
Status: TOO COARSE / ROLE-DEPENDENT
```

- Drive-WM/WoTE: action branches are used online for candidate evaluation.
- LAW: action conditioning shapes an auxiliary future-learning loss, not online consequence selection.
- GAIA-1: action controls generation but no planner is evaluated.

### Claim: online world rollout is necessary for WM-assisted planning gains

```text
Status: COUNTEREXAMPLE EXISTS
```

ViDAR and LAW improve planning without their future prediction being the deployed action-selection interface.

### Claim: longer predictive horizon improves planning

```text
Status: COUNTEREXAMPLE EXISTS
```

LAW shows a non-monotonic horizon relation.

### Claim: candidate-specific future means reactive/counterfactual correctness

```text
Status: NOT ESTABLISHED
```

WoTE source evidence shows candidate-specific ego evaluation with fixed logged surrounding-agent futures in the audited target pipeline; Drive-WM also lacks matched reactive oracle validation for alternate candidates.

### Claim: future state can add planning value beyond scorer-only

```text
Status: SUPPORTED IN WoTE/NAVSIM CONTEXT
```

WoTE's `83.2 → 85.6 PDMS` future-state ablation is the clearest current direct evidence, with the important boundary that its training/evaluation supervision is NAVSIM-style non-reactive.

---

## 11. Wave-2 gate decision

All five intended closeout questions can now be answered at sufficient precision for cross-family synthesis:

```text
1. Which future interfaces are used online?
   Drive-WM/WoTE yes; ViDAR/LAW no as decision interface; OccWorld joint generation; GAIA-1 no planner.

2. Which planning gains are cleanly matched to future modeling?
   Strongest: WoTE future-state on/off; LAW staged auxiliary objective; OccWorld internal temporal/tokenizer ablations.
   Weaker/confounded: Drive-WM fidelity attribution and broad OccWorld SOTA table.

3. Where do alternative actions receive direct supervision?
   Mostly they do not receive reactive oracle futures. WoTE generates candidate ego/reward labels via PDM; other-agent future is fixed logged data in audited path.

4. Are surrounding-agent responses factual/fixed/reactive?
   Factual/logged for most direct targets; candidate-specific learned responses may be generated, but reactive oracle correctness is not established in these anchors.

5. Do higher fidelity or longer horizon reliably improve planning?
   No. OccWorld and LAW provide direct counterexamples to monotonicity.
```

Therefore:

```text
PHASE-B WAVE 2 = CLOSED
```

Wave 2 now serves as the canonical **world-state / future-role / supervision / planner-interface coordinate system**.

Next wave should test how later models compress, unify or directly consume the future representation:

```text
Epona
DrivingGPT
DriveLaW
Auto-JEPA
DA-WAM
Think2Drive
```

The next comparison must ask whether newer unified/latent/candidate-specific designs provide decision benefits beyond the mechanisms already established in Waves 1–2.