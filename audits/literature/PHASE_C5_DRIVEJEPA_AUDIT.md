# PHASE C.5 Drive-JEPA Audit

Last updated: 2026-09-15

Status: **COMPLETE FIRST PASS — paper/source boundary resolved**

Audited paper:

```text
P0049 Drive-JEPA
Drive-JEPA: Video JEPA Meets Multimodal Trajectory Distillation for End-to-End Driving
```

Official source:

```text
linhanwang/Drive-JEPA
audited commit: e21f47410b4d26b61f05f9bd23e169c0390cae2a
```

---

# 1. Audit question

The decision-critical question is not whether the paper uses the phrase `latent world model`, but:

```text
what predictive object is learned?
what temporal information is visible when it is predicted?
what is transferred to planning?
what remains active at deployment?
which component actually selects the final trajectory?
```

---

# 2. Predictive pretraining audit

Paper §3.1 defines V-JEPA as masked spatiotemporal latent prediction:

```text
masked video view x
→ online encoder E_theta
→ predictor P_phi
→ predicted embeddings at masked positions

full target view y
→ EMA target encoder E_bar_theta
→ stop-gradient target embeddings
```

Verified semantics:

```text
target substrate       latent video feature
target source          EMA target encoder
target gradient        stop-gradient
loss                   L1 on masked positions
ego action condition   NO
explicit RGB target    NO
```

### Evidence boundary

This is a predictive representation objective, but as specified it is random spatiotemporal **completion**, not a demonstrated causal history-only→future transition objective.

Therefore:

```text
masked latent prediction
!= causal world dynamics proof
```

---

# 3. Deployment-path source audit

## 3.1 Perception-free implementation

Official `drive_jepa_perception_free/drive_jepa_model.py` verifies:

```text
2 front images
→ pretrained image_encoder
→ pooling / projection
+ ego status
→ Transformer
→ trajectory head
```

Default:

```text
freeze_encoder = True
```

When frozen, the encoder runs in `torch.no_grad()`.

Absent from downstream inference:

```text
JEPA predictor
EMA target encoder
masked-target loss
future latent prediction
world rollout
```

Verdict:

```text
JEPA mechanism at deployment
= transferred encoder representation
```

not online consequence prediction.

## 3.2 Perception-based implementation

Official source verifies:

```text
2 front frames
→ visual backbone
+ ego/status feature
→ 32 proposal features
→ 4 proposal-refinement passes
→ final proposal set
→ scorer
→ argmax
```

`shared_refiner` is inserted four times into the ModuleList, so the default refinement passes share parameters.

One refinement:

```text
proposal feature
→ decode trajectory
→ trajectory/BEV-image refinement
→ updated proposal feature
```

Classification:

```text
planner-side proposal refinement
!= physical-time rollout
!= world↔planner co-refinement
```

---

# 4. Multimodal Trajectory Distillation audit

Paper/source pipeline:

```text
8192 offline vocabulary trajectories
→ evaluate per scene with NAVSIM-v2 PDM/EPDMS machinery
→ select trajectories above quality criterion
→ sample pseudo teachers
→ add min-over-proposals supervision toward them
```

Appendix threshold:

```text
EPDMS > 0.95
```

Source verifies training samples up to four pseudo-target anchors from the qualifying index set.

Scientific semantics:

```text
pseudo teachers
= simulator/rule-selected trajectory alternatives
```

They are not multiple real human futures and not observed intervention-response world trajectories.

---

# 5. Scorer audit

Official scorer:

```text
proposal feature pooled over trajectory tokens
→ score MLP
→ 6 score outputs
→ final PDM-like score
```

Training source computes simulator/rule `target_scores` and applies BCE losses.

Thus scorer semantics:

```text
utility / driving-quality prediction
```

not factual-future likelihood and not world reconstruction.

Optional training-only heads include agent/area/BEV supervision depending configuration.

---

# 6. Momentum-aware selection source audit

Paper describes final score recalibration using previous trajectory context and a comfort/temporal-consistency score.

### NAVSIM-v1 release

Audited v1 `drive_jepa_model.py` selects directly from learned PDM score; the momentum recalibration path is not visible there.

### NAVSIM-v2 release

Audited v2 source explicitly implements `calibrate_score()`:

```text
past ego simulated states
+ each current proposal
→ simulate candidate states
→ align overlapping previous/current trajectory segments
→ two-frame extended comfort
→ recalibrate score
```

Source formula:

```text
(14 * PDM_score + 2 * two_frame_comfort) / 16
```

= 7:1 ratio.

Conclusion:

```text
momentum-aware selection is source-verified for NAVSIM-v2 release
but source claims must be version-scoped
```

---

# 7. Evidence decomposition

## 7.1 Representation pretraining evidence

Paper Table 5, simple decoder:

```text
ImageNet ResNet34       76.0
DINOv2 ViT/L            76.1
SigLIP ViT/L            83.4
V-JEPA2 ViT/L           86.1
Drive-domain JEPA ViT/L 89.0
```

### Supports

```text
V-JEPA-family video representation transfers well to planning;
driving-domain adaptation/pretraining adds planning value.
```

### Does not isolate

```text
JEPA objective vs 330h extra driving-domain exposure;
world dynamics fidelity vs representation quality;
causal future prediction vs masked completion.
```

## 7.2 Full planner module evidence

NAVSIM-v2 Table 6:

```text
baseline                                  84.1 EPDMS / 25% D / 68.2 EC
generic V-JEPA2                           85.8        / 21%   / 74.6
driving video pretraining                 86.1        / 24%   / 69.7
+ multimodal trajectory distillation      84.5        / 40%   / 47.9
+ momentum-aware trajectory selection     87.8        / 40%   / 84.8
```

Strong finding:

```text
MTD increases candidate diversity
but makes action selection/temporal comfort harder;
momentum-aware selection is required to turn diversity into final planning gain.
```

Do not attribute full 87.8 EPDMS or 93.3 PDMS to JEPA pretraining alone.

## 7.3 Pseudo-teacher number

```text
N_pseudo: 0 / 1 / 2 / 4 / 8
EPDMS:   87.2 / 87.8 / 87.7 / 87.8 / 87.5
```

More pseudo trajectories are not monotonically better.

---

# 8. Evaluation semantics

```text
NAVSIM v1/v2
= non-reactive data-driven planning / pseudo-simulation evaluation

Bench2Drive
= reactive CARLA closed-loop evaluation
```

Paper reports Bench2Drive:

```text
Driving Score 64.52
Success Rate 36.82
```

Official repo currently marks Bench2Drive code/checkpoints TODO; therefore current public-source audit cannot reproduce/verify its exact implementation path.

---

# 9. Cross-paper placement

## vs LAW

```text
LAW:
planner-time action-aware chronological future-latent auxiliary prediction
→ predictor discarded at deployment

Drive-JEPA:
pretraining-time action-agnostic random masked video latent prediction
→ predictor discarded before planner
→ encoder transferred
```

## vs ViDAR

```text
ViDAR:
historical images → autoregressive chronological future point clouds
→ transfer history encoder

Drive-JEPA:
masked video completion → transfer video encoder
```

Both are predictive pretraining; their temporal prediction obligations differ.

## vs Auto-JEPA

```text
Drive-JEPA:
predictor discarded; predictive representation remains

Auto-JEPA:
future ego-trajectory intent predictor remains online
→ predicted latent retrieves executable candidates
```

## vs WA-JEPA

WA-JEPA explicitly changes random-mask V-JEPA completion into hybrid future masking, including history-only→future prediction, then jointly models future world/action. This is useful external comparative evidence that `masked completion` and `future-directed world prediction` should be separate ontology values.

---

# 10. Counterfactuality audit

```text
multiple ego proposals                               YES
proposal-specific simulator/rule utility labels      YES
online proposal-specific predicted world states      NO
multiple observed alternative-action futures         NO
reactive other-agent intervention truths             NOT ESTABLISHED
external counterfactual validity test                 NO
```

Candidate evaluation should not be promoted into causal world-response modeling.

---

# 11. Paper/source inconsistencies and unresolved boundaries

## Headline NAVSIM-v1 value

```text
raw-paper abstract occurrence  93.7
current official README/arXiv   93.3
paper checklist                 93.3
```

Use 93.3 in current canonical notes.

## Momentum implementation

```text
NAVSIM-v1 public model file     direct score argmax
NAVSIM-v2 public model file     temporal comfort calibration verified
```

Version must be named when discussing source implementation.

## Statistical uncertainty

Paper checklist reports single-run results and no confidence intervals/error bars for main full-pipeline experiments.

---

# 12. Audit verdict

Scientific subtype:

```text
PREDICTIVE REPRESENTATION PRETRAINING
+
SIMULATOR-DISTILLED PROPOSAL POLICY / UTILITY SELECTION
```

### PROVES / strongly supports

- masked video predictive pretraining can produce planning-useful transferred features;
- driving-domain adaptation of V-JEPA representation improves the simple planning decoder in the reported setup;
- simulator-derived pseudo teachers materially increase candidate diversity;
- candidate diversity without temporal-aware selection can hurt final planning quality;
- momentum-aware selection recovers comfort and overall EPDMS in the reported ablation;
- the public planner does not require the JEPA predictor at inference.

### DOES NOT PROVE

- that Drive-JEPA deploys an online world transition model;
- that its random-mask JEPA pretext task is equivalent to causal past→future dynamics learning;
- that JEPA prediction fidelity itself causes the planning gain;
- that simulator-generated pseudo teachers represent true reactive counterfactual traffic futures;
- that the full headline planning gain is a world-model gain rather than a combination of representation, candidate support and scorer design.

### Strongest alternative explanation

A substantial part of Drive-JEPA's strength can be explained by the combination of **large-scale video representation pretraining + richer simulator-derived policy supervision + a strong proposal scorer/temporal selector**, without requiring online world imagination.

This is not a criticism of the result; it is the correct mechanism attribution.
