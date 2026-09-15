# WAM Comparison Matrix V1.3 — DA-WAM Extension

Last updated: 2026-09-15

Status: **THIRTEEN-ANCHOR EXTENSION — ONTOLOGY V1.3 RETAINED**

Anchors:

```text
LAW | WoTE | Epona | WorldDrive | World4Drive | SeerDrive
| Drive-JEPA | Metis | DynFlowDrive | Discrete-WAM | GraphWorld
| DriveLaW | DA-WAM
```

DA-WAM full projection:

```text
landscape/P0012_DAWAM_ONTOLOGY_PROJECTION.md
```

This file extends rather than replaces prior matrix extensions.

---

# 1. Canonical planning-interface taxonomy

| Paper | Canonical world/planning interface |
|---|---|
| LAW | predictive training signal / future-latent auxiliary |
| WoTE | online learned consequence model + explicit utility |
| Epona | shared world representation + direct generative policy |
| WorldDrive | predictive representation inheritance + distilled online consequence evaluation |
| World4Drive | online compact latent foresight + factual-mode matching |
| SeerDrive | online bidirectional feature co-refinement |
| Drive-JEPA | predictive representation pretraining + simulator-distilled proposal/selection |
| Metis | asymmetric world-action co-training + action-only deployment |
| DynFlowDrive | training-only flow-dynamics mode/score supervision |
| Discrete-WAM | shared discrete world-policy pretraining + direct token policy |
| GraphWorld | online interaction-structured world state + direct multimodal planner |
| DriveLaW | online generative-backbone latent → direct Action-DiT policy |
| **DA-WAM** | **online per-candidate future latent → factorized utility scorer → argmax** |

DA-WAM therefore belongs to the consequence-feature / explicit utility branch rather than the direct-policy branch.

---

# 2. Candidate-specific future truth

| Paper | Candidate-specific output | Direct future truth for every candidate? | What supervises alternatives? |
|---|---:|---:|---|
| WoTE | YES | partial/pseudo; not validated reactive truth | structured future/reward supervision |
| WorldDrive | YES teacher/surrogate | NO observed intervention GT | teacher-generated future + preference/value |
| World4Drive | YES | **NO — one factual future** | factual-mode matching / ScoreNet |
| SeerDrive | YES modes | **NO — one factual future / WTA** | future-BEV mode supervision |
| DynFlowDrive | YES training branches | **NO — one factual next latent** | mode-label / scorer teacher |
| Discrete-WAM | action-conditioned generation | NO matched alternative truth | generative/task losses |
| **DA-WAM** | **YES, one Zhat_i per trajectory** | **NO — direct future latent only for expert-matched branch** | **factor + utility + ranking losses; hard negatives** |

DA-WAM is unusually explicit about this asymmetry:

```text
avoid false counterfactual labeling
!=
obtain counterfactual world truth
```

---

# 3. Branch assignment semantics

| Paper | How factual supervision chooses a branch |
|---|---|
| World4Drive | choose predicted future latent nearest the one factual future; selected mode also defines trajectory branch |
| SeerDrive | WTA / mode-based future supervision |
| DynFlowDrive | hybrid criterion using trajectory error + reconstruction + flow stability |
| **DA-WAM** | **first choose trajectory candidate nearest expert by ADE; only that branch gets factual future-latent target** |

This is a meaningful distinction:

```text
World4Drive: future similarity helps decide branch identity
DA-WAM: expert trajectory geometry determines factual branch before future regression
```

---

# 4. Scorer semantics

| Paper | Future/world input to scorer | Meaning of high score |
|---|---|---|
| WoTE | recurrent BEV future sequence | explicit driving utility/reward |
| WorldDrive | distilled future feature | learned preference / PDMS-like quality |
| World4Drive | candidate future latent | factual-future/mode consistency |
| DynFlowDrive | no future online | learned preference distilled from training teacher |
| Drive-JEPA | no JEPA future online | simulator-derived driving quality |
| **DA-WAM** | **candidate-specific 0.5s future latent** | **NC/DAC/EP/TTC/Comfort-informed utility** |

DA-WAM is therefore much closer to WoTE than to World4Drive on scorer meaning, despite both DA-WAM and World4Drive predicting multiple latent futures.

---

# 5. Future temporal object

| Paper | Future object | Physical factorization |
|---|---|---|
| WoTE | structured BEV sequence | recurrent multi-step physical future |
| WorldDrive | video/future latent teacher + distilled summary | future-window / distilled summary |
| World4Drive | compact future latent | endpoint hypothesis |
| SeerDrive | future BEV | endpoint / selected future time |
| DynFlowDrive | future latent endpoint | one physical endpoint + internal flow transport |
| DriveLaW | generative hidden state | first solver-step representation, full video future not needed for planning |
| **DA-WAM** | **V-JEPA latent endpoint** | **single 0.5s future endpoint per candidate** |

Thus:

```text
32 candidates
!=
32 multi-step rollouts
```

---

# 6. Online future dependence

| Paper | Explicit future/world predictor online? | Future object consumed for current decision? |
|---|---:|---:|
| LAW | NO | NO |
| Epona | visual future optional; shared F online | visual future NO |
| Drive-JEPA | NO JEPA predictor | NO |
| Metis | NO future-video branch | NO |
| DynFlowDrive | NO | NO |
| Discrete-WAM | future visual not required | NO |
| DriveLaW | Video DiT hidden extraction YES | YES as representation, not completed future |
| GraphWorld | world-state refinement YES | YES |
| WorldDrive | lightweight future surrogate YES | YES |
| World4Drive | YES | YES |
| WoTE | YES | YES |
| **DA-WAM** | **YES: candidate-specific latent predictor** | **YES: scorer receives Zhat_i** |

DA-WAM is unambiguously deployment-time future-dependent.

---

# 7. Training gradient / lifecycle comparison

| Paper | Predictive/world loss relation to policy | Deployed world machinery |
|---|---|---|
| LAW | future loss shapes current representation/planner | removed |
| Drive-JEPA | predictive pretraining shapes encoder | predictor removed |
| Metis | video loss shapes action expert | video generation removed |
| DynFlowDrive | world losses teach mode scorer | world model removed |
| DriveLaW | action loss can fine-tune Video DiT | partial Video DiT online |
| **DA-WAM** | **future + factor + utility + ranking jointly adapt online LoRA/predictor/scorer per paper** | **online encoder + future predictor + scorer retained; EMA target removed** |

DA-WAM combines persistent predictive supervision during planner training with persistent future prediction during deployment.

---

# 8. Strongest matched attribution

| Mechanism/control | Result | Interpretation |
|---|---:|---|
| no future → current-latent extra path | 93.31 → 93.25 | extra pathway alone does not help |
| shared global future → action-specific future | 92.81 → 93.46 | candidate/future alignment matters |
| no future → action-specific future | 93.31 → 93.46 | direct incremental future-prediction gain is modest (+0.15) |
| action future → + hard negatives | 93.46 → 93.68 | safety/value supervision contributes +0.22 |
| frozen V-JEPA2.0 → frozen dense2.1 | 91.26 → 91.95 | dense predictive objective helps |
| frozen dense → LoRA dense | 91.95 → 92.98 | decision adaptation helps |
| LoRA+dense frozen target → EMA target | 92.98 → 93.68 | target policy matters strongly |

Binding interpretation:

```text
DA-WAM final gain
!= pure future-world prediction gain
```

It is a bundle of representation prior, decision adaptation, predictor alignment, value supervision and candidate support.

---

# 9. Hard-negative semantics

DA-WAM adds a distinction worth carrying across future papers:

```text
counterfactual trajectory/value label
!=
counterfactual world-state truth
```

Hard negative:

```text
near expert in trajectory geometry
+
substantially worse safety metric
→ factor / utility / ranking supervision
```

but:

```text
observed visual/world future for hard negative = ABSENT
```

This is stronger decision supervision without stronger environment-dynamics truth.

---

# 10. Comparison with World4Drive

Superficially:

```text
both:
N actions → N future latents → score/select
```

Scientifically:

```text
World4Drive
score semantics = factual-mode consistency
one factual future chooses matching mode

DA-WAM
score semantics = explicit utility
expert trajectory chooses factual branch
non-expert branches get value/ranking labels
```

Therefore they occupy different scorer/teacher coordinates despite similar diagrams.

---

# 11. Comparison with WoTE

```text
WoTE
candidate → recurrent BEV future sequence
→ explicit reward heads
→ utility aggregation
→ select

DA-WAM
candidate → 0.5s latent endpoint
→ factorized metric heads + utility
→ select
```

DA-WAM is more compact and directly aligned candidate↔latent; WoTE models more explicit temporal consequence sequences.

Neither audited setup establishes branch-specific reactive other-agent intervention truth.

---

# 12. Evaluation semantics

DA-WAM:

```text
NAVSIM-v1 / NAVSIM-v2
= non-reactive data-driven / pseudo-simulation planning
```

Therefore:

```text
high NC/TTC/PDMS/EPDMS
!= validated reactive counterfactual environment model
```

---

# 13. Ontology decision

Potential novelty residue:

```text
one factual branch receives world-state supervision;
other branches receive only decision/value supervision
```

This is already represented by:

```text
G07 branch supervision coverage
I02 alternative-action future supervision
K05 scorer target provenance
```

Decision:

```text
ONTOLOGY V1.3 RETAINED
NO V1.4 FROM DA-WAM
```

---

# 14. New cross-anchor conclusion after DA-WAM

DA-WAM makes a distinction especially explicit:

```text
A predicted latent can serve two scientific roles:

1. ENVIRONMENT-PREDICTION OBJECT
   judged against observed future world state

2. DECISION FEATURE
   shaped by factor/value/ranking losses
```

In DA-WAM the expert branch has both roles, while non-expert branches are directly verified only in the second role.

This must be checked in future WAM papers whenever authors call a candidate-conditioned latent a `counterfactual future`.
