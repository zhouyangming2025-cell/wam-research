# P0049 Drive-JEPA — Deep Analysis V2

Last updated: 2026-09-15

Status: **COMPLETE FIRST PASS — paper + official source audited; ontology residue tested**

Paper: **Drive-JEPA: Video JEPA Meets Multimodal Trajectory Distillation for End-to-End Driving**

Canonical research role in this repository:

```text
PREDICTIVE REPRESENTATION PRETRAINING
+
PROPOSAL-CENTRIC SIMULATOR-DISTILLED PLANNING
```

Do **not** compress these into one undifferentiated “world model planner” mechanism.

---

# 0. Source and version contract

Primary paper source:

```text
papers/raw_md/P0049_DriveJEPA/P0049_DriveJEPA.raw.md
```

Official repository audited:

```text
linhanwang/Drive-JEPA
latest audited source commit:
e21f47410b4d26b61f05f9bd23e169c0390cae2a
```

Relevant release history:

```text
2026-01-29  initial public repository
2026-02-09  NAVSIM-v1 code release
2026-03-22  NAVSIM-v2 code release
```

Important numerical version note:

```text
one raw-paper abstract occurrence: 93.7 PDMS on NAVSIM-v1
latest official arXiv / official README / paper checklist: 93.3 PDMS
```

Use **93.3 PDMS** as the current canonical headline value; do not silently mix the stale 93.7 occurrence with current released claims.

---

# 1. One-sentence scientific position

Drive-JEPA does **not** deploy a JEPA future predictor to imagine consequences before choosing an action. It first uses V-JEPA-style masked latent prediction to pretrain/adapt a video encoder, then transfers that encoder into a separate proposal-centric planner whose multimodal proposals and simulator-trained scoring system perform action selection.

The cleanest mechanism decomposition is therefore:

```text
large-scale masked video latent prediction
→ predictive spatiotemporal encoder
→ transfer/fine-tune or freeze encoder for driving planning

PLUS

32 proposal modes
→ repeated proposal refinement
→ human + simulator-selected pseudo-teacher supervision
→ PDM/EPDMS-style scorer
→ temporal/momentum comfort recalibration
→ argmax trajectory
```

The first chain is the JEPA contribution. The second chain is the deployed planner.

---

# 2. What problem is Drive-JEPA actually solving?

The paper attacks two different bottlenecks.

## 2.1 Representation bottleneck

The authors argue that generic image pretraining and dense generative world modeling are not the only ways to obtain planning-relevant visual features. V-JEPA provides self-supervised video representation learning by predicting latent target features instead of reconstructing RGB pixels.

Scientific function:

```text
video predictive objective
→ force encoder to capture temporal/spatiotemporal regularities
→ transfer encoder into planning
```

This is primarily a **representation-learning** claim.

## 2.2 Imitation-learning modal-collapse bottleneck

A logged driving scene normally contains one demonstrated human future, although multiple trajectories may be feasible. A proposal planner supervised only by the single logged trajectory can collapse toward a narrow behavior distribution.

Drive-JEPA therefore adds:

```text
large offline trajectory vocabulary
→ simulator evaluates many trajectories for each scene
→ high-quality alternatives become pseudo teachers
→ proposal set trained toward human + pseudo teachers
→ diversity increases
```

This is a **candidate-support / policy-supervision** claim, not a world-prediction claim.

The paper then adds momentum-aware trajectory selection because increased diversity can worsen temporal smoothness/comfort.

---

# 3. What exactly does the JEPA pretraining predict?

## 3.1 V-JEPA objective

The paper states the V-JEPA objective as:

```text
masked spatiotemporal video view x
→ online encoder E_theta(x)
→ predictor P_phi
→ predict target representation at masked locations

full/target view y
→ EMA target encoder E_bar_theta(y)
→ stop-gradient target latent
```

The core loss is an L1 distance between predicted target embeddings and the stop-gradient EMA target embeddings at masked positions.

Key target-network facts:

```text
prediction target       = latent video representation
source of target        = EMA target encoder
stop-gradient           = YES
predictor trained       = YES
online encoder trained  = YES during JEPA pretraining
RGB reconstruction      = NO
```

## 3.2 Critical semantic correction: masked prediction != necessarily future dynamics

The paper repeatedly uses `predictive representation` and `latent world model` language. But its stated V-JEPA pretraining objective is **random masked spatiotemporal completion**: some patches in a video clip are hidden and the model predicts their latent features from the remaining visible context.

Therefore the training objective, as specified, does **not by itself establish**:

```text
history-only observation
→ chronologically unseen future world
```

and it does not establish:

```text
ego action
→ future environment response
```

The most precise description is:

> self-supervised masked spatiotemporal latent prediction that learns predictive video representations.

This distinction matters because a model can exploit spatial and temporal context around a masked token without being a causal next-state transition model.

---

# 4. Driving Video Pretraining

Drive-JEPA initializes from V-JEPA 2 and continues/adapts video pretraining on a large driving corpus.

Paper-reported corpus:

```text
~330 h front-camera driving video
sources include CoVLA, DrivingDojo, OpenScene trainval
8-frame clips
512 × 256
2 Hz
```

The intended transfer object is the **ViT encoder**, not the JEPA predictor.

This yields an important lifecycle:

```text
JEPA pretraining:
encoder + predictor + EMA target encoder

↓ transfer

downstream planner:
pretrained encoder retained
JEPA predictor discarded
EMA target encoder discarded
masked-target objective absent from action selection
```

This is the same broad lifecycle family as predictive pretraining, but with a different target geometry from ViDAR.

---

# 5. Perception-free planner: strongest proof of representation transfer

The paper deliberately evaluates a very simple downstream decoder to test whether the pretrained visual representation itself is useful.

Official source verifies:

```text
2 front images
→ pretrained V-JEPA/Drive-JEPA image encoder
→ pooled/projected image tokens
+ ego status token
→ ordinary Transformer
→ waypoint queries
→ direct trajectory
```

Important source fact:

```text
freeze_encoder = True by default in perception-free implementation
```

and the frozen encoder is executed under `torch.no_grad()`.

No JEPA predictor appears in this deployed planner graph.

Therefore:

```text
predicted future latent at inference = NO
masked completion at inference       = NO
world rollout at inference           = NO
```

The representation learned through prediction remains; the predictive mechanism itself does not.

---

# 6. Perception-based full planner

The full planner is better understood as a proposal-centric planning architecture using a predictive-pretrained visual backbone.

## 6.1 Inputs

Paper/source configuration uses:

```text
front camera only
current + previous image
current/history ego status
no LiDAR in the reported Drive-JEPA setup
```

## 6.2 Waypoint-anchored proposal generation

Source-verified default:

```text
proposal_num = 32
ref_num      = 4
planning horizon = 4 s
8 poses at 0.5 s interval
```

The model creates proposal/waypoint query features, repeatedly decodes trajectories, and refines proposal features using image features.

Crucial source detail:

```python
shared_refiner = Traj_refiner(config)
ModuleList([shared_refiner for _ in range(ref_num)])
```

Thus the four refinement passes share the same `Traj_refiner` parameters.

One refinement means:

```text
proposal feature
→ decode explicit trajectory
→ trajectory-conditioned/anchored interaction with image feature
→ updated proposal feature
```

This is **planner proposal refinement**. It is not physical-time world rollout and not a world↔planner co-refinement loop like SeerDrive.

## 6.3 Multimodal Trajectory Distillation (MTD)

Drive-JEPA constructs an offline vocabulary of 8192 trajectories from more than 100k training trajectories by clustering.

For each training scene:

```text
8192 vocabulary trajectories
→ NAVSIM-v2 rule-based pseudo-simulation / EPDMS evaluation
→ keep high-quality trajectories (threshold 0.95 in appendix)
→ sample pseudo-teacher alternatives
```

Proposal supervision then includes:

```text
nearest proposal to logged human trajectory
+
nearest proposals to sampled high-scoring pseudo-teacher trajectories
+
diversity term / iterative proposal losses
```

Official source verifies the training code samples up to four pseudo-target anchors from the simulator-qualified index set and adds them to the min-over-proposals trajectory objective.

Scientific meaning:

```text
multi-modal supervision source
= simulator/rule-filtered candidate trajectories
```

not:

```text
multiple observed human futures
```

and not:

```text
multiple reactive real-world counterfactual futures
```

## 6.4 Scorer

The deployed full planner ranks the 32 proposals with a learned scorer.

Source verifies:

```text
proposal features
→ MLP score heads
→ PDM/EPDMS-style score prediction
→ sigmoid score
→ argmax proposal
```

Training target scores are generated from NAVSIM metric-cache simulation/rule evaluation. The source also contains auxiliary agent/area/map heads used in training according to configuration.

This scorer is a **utility / driving-quality estimator**. It should not be confused with a world model consequence predictor.

## 6.5 Momentum-aware trajectory selection

The paper adds a temporal consistency/comfort correction using the previously selected/executed trajectory context.

NAVSIM-v2 released source verifies:

```text
past ego simulated states
+ each current candidate trajectory
→ simulate/align overlapping states
→ compute two-frame extended comfort
→ recalibrate PDM score
→ argmax
```

The source weighting is:

```text
(14 * learned_PDM_score + 2 * two_frame_comfort) / 16
```

which is the same 7:1 ratio described by the paper-level formulation.

NAVSIM-v1 released `drive_jepa_model.py` does not expose this recalibration path, so source-level claims about momentum selection must be version-scoped.

---

# 7. Training graph vs inference graph

## 7.1 Pretraining

```text
video clip
→ random spatiotemporal masking
→ online encoder
→ JEPA predictor
→ masked latent prediction
↕
EMA target encoder + stop-gradient latent targets
```

## 7.2 Downstream planner training

Perception-based:

```text
2 front frames
→ Drive-JEPA/V-JEPA visual encoder (smaller LR; fine-tuned)
→ 32 proposal features
→ 4 shared-weight refinement passes
→ proposal trajectories

logged trajectory
+ simulator-qualified pseudo teachers
→ proposal trajectory losses

proposal trajectories
→ NAVSIM simulator/rule score targets
→ learned scorer losses

optional auxiliary agent/area/BEV losses
```

Perception-free source differs:

```text
pretrained encoder is frozen by default
→ simple Transformer waypoint decoder
```

## 7.3 Deployment

```text
2 front images + ego status
→ pretrained/fine-tuned visual encoder
→ proposal generator/refiner
→ scorer
→ optional temporal comfort calibration
→ argmax trajectory
```

Absent from deployment:

```text
JEPA predictor
EMA target encoder
masked-target loss
future video/latent reconstruction
future scene rollout
```

This training/inference separation is the central Drive-JEPA mechanism fact.

---

# 8. Strongest evidence: decompose the gains

## 8.1 Pretraining comparison — representation evidence

With a simple downstream decoder, paper Table 5 reports approximately:

| Pretraining / encoder | PDMS |
|---|---:|
| ImageNet ResNet34 | 76.0 |
| DINOv2 ViT/L | 76.1 |
| SigLIP ViT/L | 83.4 |
| V-JEPA 2 ViT/L | 86.1 |
| **Drive-domain V-JEPA / Ours ViT/L** | **89.0** |

DepthAnything and MAE are reported as failing/not converging under this setup.

### DIRECT EVIDENCE

The V-JEPA-family encoder transfers substantially better than several generic visual-pretraining alternatives under the authors' simple planning decoder; adapting/pretraining on the 330 h driving-video corpus further raises PDMS from 86.1 to 89.0.

### WHAT IT DOES NOT PROVE

The 86.1→89.0 difference does not isolate a pure `JEPA objective` effect because it also changes domain/data exposure. The cross-paper Epona comparison is even less causal because architecture, scale and training differ.

The evidence supports:

```text
predictive video representation + driving-domain adaptation is useful
```

more directly than:

```text
an online world dynamics model improves planning
```

## 8.2 Full-module ablation — planner evidence

NAVSIM-v2 Table 6:

| V-JEPA / driving pretrain | MTD | Momentum | Diversity | EC | EPDMS |
|---|---:|---:|---:|---:|---:|
| baseline | NO | NO | 25% | 68.2 | 84.1 |
| generic V-JEPA2 | NO | NO | 21% | 74.6 | 85.8 |
| driving video pretrain | NO | NO | 24% | 69.7 | 86.1 |
| driving video pretrain | YES | NO | **40%** | **47.9** | 84.5 |
| driving video pretrain | YES | YES | **40%** | **84.8** | **87.8** |

The paper flags the first two pretraining variants as separate module configurations; do not add their deltas as independent effects.

Most important scientific pattern:

```text
MTD
→ diversity 24% → 40%
→ but comfort collapses and EPDMS falls 86.1 → 84.5

Momentum-aware selection
→ preserves 40% diversity
→ EC 47.9 → 84.8
→ EPDMS 84.5 → 87.8
```

Thus multimodality alone is not monotonically good. Candidate diversity creates a **selection / temporal-consistency burden** that must be solved by the decision layer.

This reinforces an existing project principle:

```text
candidate support != candidate selection quality
```

## 8.3 Pseudo-teacher count

Table 7:

```text
N_pseudo: 0    1    2    4    8
EPDMS:   87.2 87.8 87.7 87.8 87.5
```

Pseudo alternatives help over zero in this experiment, but the relation is weak and non-monotonic. More pseudo trajectories are not automatically better.

---

# 9. Drive-JEPA vs LAW — same broad family, different predictive semantics

The two papers can both be casually summarized as “latent predictive learning helps planning,” but their causal graphs are different.

| Axis | LAW | Drive-JEPA |
|---|---|---|
| When prediction occurs | during planner training | separate video pretraining stage |
| Prediction target | factual future visual/planner latent | EMA target latent at masked spatiotemporal positions |
| Temporal geometry | current→chronological future | random masked same-video completion as specified |
| Ego action condition | **YES**: current predicted waypoint/action | **NO** in JEPA video pretraining |
| Target network | detached future target pathway | EMA target encoder + stop-gradient |
| Predictive loss shapes | shared end-to-end representation during planner training | pretrained encoder before transfer/fine-tuning |
| Predictor retained for planning inference | NO | NO |
| Online predicted future used to choose action | NO | NO |

Therefore:

```text
LAW
= action-aware future-latent auxiliary shaping

Drive-JEPA
= action-agnostic masked-video predictive representation pretraining
```

They should not occupy the same ontology cell without recording the prediction geometry.

---

# 10. Drive-JEPA vs ViDAR — predictive pretraining is not one mechanism

ViDAR explicitly defines:

```text
historical visual sequence
→ History Encoder
→ autoregressive Future Decoder
→ chronologically future point clouds
```

Its pretext task is deliberately **past→future forecasting**.

Drive-JEPA pretraining instead uses V-JEPA random masked spatiotemporal latent prediction.

Both transfer an encoder and discard the future/predictor machinery for downstream planning, but they differ in what temporal causal information the pretext task is forced to learn.

This comparison motivates the new ontology axis `F07 Prediction temporal/observability geometry`.

---

# 11. Drive-JEPA vs later JEPA driving variants

These later works are used only as comparative controls, not as evidence about Drive-JEPA itself.

## Auto-JEPA

Auto-JEPA predicts a **future ego-trajectory latent** from history/current visual context and uses the predicted intent online as a trajectory-memory retrieval key.

So its prediction remains in the deployed decision path.

```text
Drive-JEPA: predictive encoder transfer; predictor discarded
Auto-JEPA: future-intent predictor directly retrieves actions online
```

## WA-JEPA

WA-JEPA explicitly identifies original V-JEPA random-mask completion as insufficiently future-directed for planning and changes the objective to hybrid future masking, including a full-mask branch where history alone predicts unseen future tokens; it further adds latent flow generation and joint future-action prediction.

This independently confirms that the scientific distinction between:

```text
masked spatiotemporal completion
vs
causal future prediction
```

is decision-relevant and not merely terminological.

---

# 12. Evaluation semantics

## NAVSIM v1 / v2

```text
data-driven non-reactive planning evaluation / pseudo-simulation
```

Do not upgrade NAVSIM to reactive closed-loop evaluation.

The pseudo-teacher generator and PDM/EPDMS scorer rely on simulator/rule evaluation over logged/scenario context. This creates candidate-specific ego evaluation, but it does not establish correct reactive other-agent responses to every alternative ego action.

## Bench2Drive

```text
CARLA reactive closed-loop simulation
```

Paper Table 4 reports:

```text
Driving Score 64.52
Success Rate  36.82
```

Official repository currently marks Bench2Drive code/checkpoints as not yet released. Therefore this is paper-level closed-loop evidence, not source-reproduced evidence in the audited public release.

---

# 13. Counterfactual / intervention boundary

Drive-JEPA has many action candidates and simulator-generated labels, but this should not be narrated as observed counterfactual world modeling.

```text
candidate-specific trajectories                     YES
candidate-specific rule/simulation scores            YES
candidate-specific observed real alternative futures NO
reactive real other-agent responses for each action  NOT ESTABLISHED
online consequence/world state prediction            NO
```

MTD teaches which *trajectories* look feasible/high-quality under the evaluation machinery. It does not train an online dynamics model that predicts how the world will react to each trajectory.

---

# 14. Does Drive-JEPA qualify as a planning-centric WAM anchor?

The answer depends on what level of WAM taxonomy is being discussed.

## AUTHOR FRAMING

The paper frames V-JEPA as an efficient latent world model / predictive representation approach for planning.

## DIRECT IMPLEMENTATION FACT

The JEPA predictor and target network belong to pretraining. The deployed planner retains the encoder, not an online learned world-transition operator.

## OUR TAXONOMIC JUDGMENT

Drive-JEPA is best retained as a **boundary/core-control anchor for predictive representation learning**, not grouped with online consequence-model WAMs.

Its value to the field map is precisely that it asks:

> How much planning benefit can we obtain from a world/predictive pretraining objective when explicit future simulation is completely absent at deployment?

That makes it highly informative for distinguishing `world knowledge` from `world rollout`.

---

# 15. Ontology residue: F07 is required

Existing F04/F05 dimensions describe temporal factorization, horizon and intermediate-state use, but they do not cleanly encode what temporal information is **visible when the prediction target is generated**.

Drive-JEPA exposes the difference between:

```text
random masked same-window spatiotemporal completion
vs
causal history→future forecasting
vs
action-conditioned state transition
```

These mechanisms can all be called “predictive” while imposing fundamentally different learning obligations.

Proposed stable dimension:

```text
F07 Prediction temporal / observability geometry
```

Back-projection succeeds on prior anchors; see:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md (consolidated comparison baseline)
```

---

# 16. Claim–evidence ledger

## Claim A — JEPA video pretraining provides useful planning representations

**AUTHOR CLAIM:** V-JEPA-style video pretraining learns strong planning representations.

**DIRECT EVIDENCE:** Table 5 with the same simple decoder gives V-JEPA2 86.1 PDMS and Drive-domain V-JEPA 89.0, above several generic pretraining alternatives.

**OUR INFERENCE:** Strong evidence for representation transfer; weaker evidence for a specific `world-dynamics` interpretation.

**REMAINS UNPROVEN:** that better masked latent prediction fidelity monotonically predicts better planning, or that causal future dynamics are required for the gain.

## Claim B — Multimodal pseudo teachers solve modal collapse

**AUTHOR CLAIM:** simulator-generated pseudo trajectories improve multimodal proposal coverage.

**DIRECT EVIDENCE:** proposal diversity rises from 24% to 40% after MTD; qualitative visualizations show broader proposal modes.

**OUR INFERENCE:** strong evidence that MTD changes proposal support/diversity.

**REMAINS UNPROVEN:** that diversity alone improves final driving quality; in fact EPDMS drops without momentum-aware selection.

## Claim C — Momentum-aware selection makes diverse proposals usable

**AUTHOR CLAIM:** temporal consistency / comfort-aware selection stabilizes planning.

**DIRECT EVIDENCE:** MTD-only EC 47.9 / EPDMS 84.5; adding momentum raises EC to 84.8 and EPDMS to 87.8 while diversity stays 40%. NAVSIM-v2 source implements two-frame comfort score recalibration.

**OUR INFERENCE:** one of the paper's strongest causal component results.

**REMAINS UNPROVEN:** how much of the same benefit could be obtained by another temporal scorer independent of JEPA or MTD.

---

# 17. Final scientific judgment

Drive-JEPA should **not** be summarized as:

```text
JEPA world model predicts future → planner chooses action
```

The accurate summary is:

```text
V-JEPA masked latent prediction on large driving video
→ strong transferred visual representation

then independently:

proposal-centric planner
→ simulator-distilled multimodal candidate support
→ repeated proposal refinement
→ learned PDM/EPDMS scorer
→ momentum/comfort recalibration
→ final action
```

Its main contribution to the WAM scientific coordinate system is not a new online future→planning interface. It sharpens the **predictive-representation boundary** and forces us to distinguish **masked video completion** from **causal future forecasting**.

Scientific subtype:

```text
PREDICTIVE REPRESENTATION PRETRAINING
+ SIMULATOR-DISTILLED PROPOSAL POLICY
```

Strongest reusable principle:

```text
predictive objective != online dynamics model
masked temporal completion != causal future forecasting
world-model pretraining gain != deployed world-model reasoning
candidate diversity != planning quality without a capable selector
```
