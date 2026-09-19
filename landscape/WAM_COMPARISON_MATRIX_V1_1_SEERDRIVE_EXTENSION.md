# WAM Comparison Matrix V1.1 — SeerDrive Extension

Last updated: 2026-09-15

Status: **HISTORICAL PROJECTION SNAPSHOT — not current state or final route authority; retain only as a traceable comparison aid.**

Base:

```text
landscape/WAM_COMPARISON_MATRIX_V1.md
landscape/P0061_SEERDRIVE_ONTOLOGY_V1_PROJECTION.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
```

Anchors:

```text
LAW | WoTE | Epona | WorldDrive | World4Drive | SeerDrive
```

This file contains the dimensions where SeerDrive most materially changes or sharpens the cross-paper picture. Its full A–P projection remains in `P0061_SEERDRIVE_ONTOLOGY_V1_PROJECTION.md`.

---

# 1. Core planning-interface matrix

| Axis | LAW | WoTE | Epona | WorldDrive | World4Drive | **SeerDrive** |
|---|---|---|---|---|---|---|
| Future's main role | training representation teacher | online consequence for utility | joint visual predictive shaping; simulator sibling | representation inheritance + distilled consequence | online compact future mode | **online future BEV for planner feature refinement** |
| Final action mechanism | waypoint head | candidate→reward→argmax | direct diffusion/flow policy | candidate→coarse score→FAR rerank | six future modes→ScoreNet | **current/future planner branches→feature fusion→trajectory** |
| Predicted future consumed online? | NO | YES | visual future not required | YES, distilled | YES | **YES** |
| Explicit scalar future utility? | NO | YES | NO | YES/preference | NO: factual-mode consistency | **NO in original paper core mechanism** |
| Planner→world feedback? | single predicted action conditions WM after waypoint is produced | candidate action conditions temporal transition | action conditions visual generator | candidate conditions teacher/student future | candidate action token conditions predictor | **YES: refined ego/planner feature fed back to WM** |
| World→planner feedback? | NO for current selection | YES via reward | NO same-step visual→planner | YES via FAR reward | YES via ScoreNet | **YES via future-BEV planner branch** |
| Mutual repeated co-refinement? | NO | NO | NO | NO | NO | **YES** |

---

# 2. Iteration semantics — V1.1 axis

| Paper | What one “iteration” means | Does physical future time advance? | Does planner/world representation co-refine? |
|---|---|---:|---:|
| LAW | no iterative deployed reasoning | NO | NO |
| WoTE | recurrent latent world transition | **YES** | NO |
| Epona | diffusion denoising; simulation can autoregress generated observations | generative time advances in simulation AR | NO same-step planner/world co-refinement |
| WorldDrive | no deployed iterative world reasoning; teacher diffusion removed online | NO online | NO |
| World4Drive | one endpoint latent prediction per candidate | NO iterative depth | NO |
| **SeerDrive** | **repeat world prediction ↔ planner-feature refinement for same planning horizon** | **NO** | **YES** |

**Key correction:** SeerDrive's `N=2` best refinement iterations must not be compared with WoTE's recurrent 0→2→4 s rollout depth or Epona's visual autoregressive horizon.

---

# 3. Future temporal object and decision relevance

| Paper | Future object used for planning | Temporal structure | Evidence about more future detail |
|---|---|---|---|
| LAW | training target latent | single selected endpoint | 1.5s target beats nearer/farther settings; non-monotonic |
| WoTE | BEV future sequence | recurrent ~2s,4s | recurrent intermediate states improve over direct endpoint in reported evaluator |
| Epona | none required in planning; visual AR for simulation | frame-autoregressive visual | long visual rollout evidence separate from planning |
| WorldDrive | distilled candidate future summary | compact summary | avoids full rollout by design |
| World4Drive | candidate endpoint latent | one `t+n` endpoint | compact endpoint used by ScoreNet |
| **SeerDrive** | **future BEV endpoint** | **4s NAVSIM / 3s nuScenes default** | **1-2-3-4s sequence 88.8 vs 4s only 88.9: richer temporal sequence adds no gain** |

This strengthens the cross-paper principle:

```text
more world temporal completeness != more planning value
```

---

# 4. Multimodal future branch supervision

| Paper | Multi-branch future outputs | How branch/mode becomes positive | K alternative-action factual/reactive futures? |
|---|---:|---|---:|
| LAW | NO multi-candidate bank | single planner action | NO |
| WoTE | YES candidate branches | expert/candidate targets + simulator reward | ego-specific simulation, but audited surrounding future fixed/logged |
| Epona | stochastic/generative, no scored bank | trajectory distribution training | NO K matched intervention truths |
| WorldDrive | YES teacher-generated candidate futures | planner top-K + teacher latent + PDMS ranking | NO real K alternatives |
| World4Drive | YES six future latents | nearest predicted latent to one factual future | NO |
| **SeerDrive** | **YES M future BEV modes** | **same current-ego mode probability selects trajectory + corresponding future-BEV WTA branch** | **NO** |

SeerDrive therefore adds another distinct mode-assignment mechanism; it does not change the project's counterfactual warning.

---

# 5. Counterfactuality vector

| Paper | Candidate-specific output | Alternative consequence supervision | Reactive other-agent truth | Intervention-validity evidence |
|---|---|---|---|---|
| LAW | NO multi-candidate output | factual single future | NO | NO |
| WoTE | YES | simulator/semantic per ego candidate | **NO in audited NAVSIM path** | NO direct causal validation |
| Epona | controllable world generation | factual demonstrations | NOT ESTABLISHED | NO |
| WorldDrive | YES teacher-generated | learned teacher alternatives | NOT ESTABLISHED | NO |
| World4Drive | YES | one factual future assigns mode | NOT ESTABLISHED | NO |
| **SeerDrive** | **YES M future BEVs** | **WTA factual mode supervision** | **NOT ESTABLISHED** | **NO** |

---

# 6. Strongest matched mechanism evidence

| Paper | Strongest matched control | What it isolates reasonably well | Main remaining confound |
|---|---|---|---|
| LAW | ± future-latent/action-aware auxiliary task | predictive representation shaping | exact representation semantics |
| WoTE | 81.0 trajectory only →83.2 evaluator no future→85.6 +future | evaluator vs future consequence contribution | reactive counterfactual validity |
| Epona | trajectory-only 78.1→joint visual+trajectory 86.2 | cross-modal predictive shaping | which visual property causes gain |
| WorldDrive | 86.9 base→87.0 traj scorer→88.1 +distilled future | future feature beyond extra scorer | teacher dynamics vs PDMS ranking semantics |
| World4Drive | priors+intentions no WM 0.61/0.36→+WM 0.50/0.16 | future-latent-selector bundle beyond intentions | prediction vs mode matching vs regularization |
| **SeerDrive** | **2×2: 87.1 neither; 87.9 iterative only; 88.1 future-aware only; 88.9 both** | **future-BEV use and internal co-refinement are separately useful and complementary** | **does not prove causal/reactive world correctness** |

SeerDrive has one of the cleaner component decompositions among the six anchors.

---

# 7. Future-knowledge lifecycle after six anchors

```text
LAW
predictive target → representation shaping → future absent from selection

Epona
visual predictive task → shared latent shaping → visual branch optional in planning

WoTE
compact learned temporal world transition → stays online → reward selection

WorldDrive
heavy generative future teacher → distillation → lightweight online surrogate → preference ranking

World4Drive
compact candidate future predictor → stays online → factual-mode selector

SeerDrive
compact future BEV → stays online → planner feature refinement
→ refined planner feature feeds back to future predictor
→ repeated internal co-refinement
```

SeerDrive therefore adds a new lifecycle/interface subtype:

```text
ONLINE BIDIRECTIONAL FEATURE CO-REFINEMENT
```

This label describes computation topology only. It does not imply externally validated bidirectional causal traffic response.

---

# 8. Source/version comparison warning unique to SeerDrive

Original paper:

```text
future-aware planning + iterative scene/planning interaction
```

Released official code/README:

```text
WoTE-integrated online trajectory evaluation/selection
reported 88.88 PDMS
without iterative interaction between planning and scene modeling
```

Therefore all future comparisons must include a `method version` field when using SeerDrive numbers or source details.

Do not mix:

```text
paper ablation 88.9
with
released-code 88.88 WoTE-integrated architecture
```

as though they were the same computational graph.
