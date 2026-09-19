# WAM Comparison Matrix V1.3 — DriveLaW Extension

Last updated: 2026-09-15

Status: **HISTORICAL PROJECTION SNAPSHOT — not current state or final route authority; retain only as a traceable comparison aid.**

Anchors:

```text
LAW | WoTE | Epona | WorldDrive | World4Drive
| SeerDrive | Drive-JEPA | Metis | DynFlowDrive | Discrete-WAM | GraphWorld | DriveLaW
```

DriveLaW full projection:

```text
landscape/P0009_DRIVELAW_ONTOLOGY_PROJECTION.md
```

This file extends:

```text
landscape/WAM_COMPARISON_MATRIX_V1_3_GRAPHWORLD_EXTENSION.md
```

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
| Drive-JEPA | predictive representation pretraining + simulator-distilled proposal/selection planner |
| Metis | asymmetric world-action co-training + action-only deployment |
| DynFlowDrive | training-only flow-dynamics mode/score supervision |
| Discrete-WAM | shared discrete world-policy pretraining + hierarchical direct token policy |
| GraphWorld | online interaction-structured future-aware latent state + direct multimodal planner |
| **DriveLaW** | **online Video-DiT internal generative state → blockwise Action-DiT conditioning → direct flow policy** |

DriveLaW adds a distinct interface family:

```text
retain the generative backbone online
but tap internal hidden states before full world generation is complete
```

---

# 2. Is a complete future world object required online?

| Paper | Complete future object required for planning? | What is actually consumed? |
|---|---:|---|
| LAW | NO | current representation; future only as training target |
| WoTE | YES | recurrent future BEV sequence |
| Epona | NO visual future | shared historical latent F |
| WorldDrive | YES, lightweight | distilled future representation |
| World4Drive | YES | intention-conditioned endpoint future latent |
| SeerDrive | YES | future BEV hidden state |
| Drive-JEPA | NO | transferred predictive encoder + planner/scorer |
| Metis | NO | action expert only at inference |
| DynFlowDrive | NO | planner score head only |
| Discrete-WAM | NO future visual required for direct policy | discrete world/policy representation |
| GraphWorld | YES as online refined world latent, but not explicit multi-step rollout | interaction world state W |
| **DriveLaW** | **NO complete future** | **first-pass Video-DiT block hidden states; full denoising and RGB decode skipped** |

New control:

```text
online world-model use
!= complete future rollout
```

DriveLaW occupies the middle category:

```text
world generator present online
+
partial internal generative computation
+
no completed rendered future
```

---

# 3. Forward information-flow direction

| Paper | Dominant forward world/action direction during the mechanism of interest |
|---|---|
| LAW | action → predicted future latent; future does not return to same action |
| WoTE | candidate action → future → value → selection |
| Epona | shared history latent → action and visual siblings; optional action→visual control |
| WorldDrive | candidate → future surrogate → rank |
| World4Drive | candidate → future latent → ScoreNet → select |
| SeerDrive | planner ↔ future-world internal co-refinement |
| Metis | action → future video during joint training |
| DynFlowDrive | candidate → flow future during training |
| GraphWorld | planner/motion hypotheses → world refinement → planner conditioning |
| **DriveLaW** | **Video/world hidden state → action trajectory** |

DriveLaW therefore reverses the dominant forward direction seen in many action-conditioned WAMs.

---

# 4. Backward gradient direction

| Paper | Mechanistically important gradient path |
|---|---|
| Epona | trajectory + visual losses jointly shape shared historical representation |
| LAW | future-latent loss shapes action-aware/current representation path |
| Metis | **world/video loss → action expert** despite no future-video→action forward path |
| DynFlowDrive | world/selection losses shape training-time planner/scorer; exact code unavailable |
| **DriveLaW** | **action loss → Action DiT → Video-DiT hidden states → Video DiT** under `action_full` |

Mirror comparison:

```text
Metis:
forward  ACTION → WORLD
backward WORLD LOSS → ACTION

DriveLaW:
forward  WORLD → ACTION
backward ACTION LOSS → WORLD
```

This confirms that forward information flow and backward gradient flow must remain separate ontology dimensions.

---

# 5. Consequence model vs representation model

| Paper | Does world model answer "what happens if I take candidate a_i"? | Planning role |
|---|---:|---|
| WoTE | YES architecturally | online consequence + explicit utility |
| WorldDrive | YES through teacher/surrogate | online candidate ranking |
| World4Drive | YES architecturally | online future-mode scoring |
| DynFlowDrive | YES training-only | candidate-label teacher |
| Metis | action-conditioned future during training | policy co-training, not online evaluator |
| GraphWorld | NO per-candidate branch | online structured representation |
| **DriveLaW** | **NO** | **online generative representation conditions direct policy** |

Binding conclusion:

```text
world-model-based planning
has at least two independent families:

A. consequence reasoning
B. generative/predictive representation conditioning
```

DriveLaW is a strong anchor for B.

---

# 6. Generative-state maturity / tap location

| Paper | What stage of a generative/predictive process reaches planning? |
|---|---|
| Epona | historical shared latent; visual generation branch not consumed |
| WorldDrive | distilled future summary after teacher training |
| Metis | no video state at deployed action inference |
| Discrete-WAM | discrete world/policy tokens; future generation optional for policy |
| **DriveLaW** | **internal Video-DiT hidden states from the first video denoising iteration** |

DriveLaW matched ablation:

```text
video denoise step 1   89.1 PDMS
step 5                 86.9
step 10                23.2
```

This exposes a candidate future ontology residue:

```text
GENERATIVE-STATE TAP LOCATION / SOLVER DEPTH
```

but it is not promoted yet because F08 + J01/J03 + N already encode most of the distinction and another independent anchor is needed.

---

# 7. F08 — internal solver coordinates vs physical time

| Paper | Internal-step semantics | Physical-time interpretation? |
|---|---|---|
| Epona | inner diffusion step + outer frame AR | inner NO; outer YES |
| WoTE | recurrent world step | YES, advances predicted physical future |
| Metis | video/action flow denoising | NO |
| DynFlowDrive | rectified-flow transport s | NO |
| GraphWorld | flow/refinement iteration | NO |
| **DriveLaW** | **video denoising solver `s_video` + action-flow solver `s_action`** | **both NO; separate from physical future trajectory/video time** |

DriveLaW adds an important dual-solver example:

```text
physical time tau
!= video solver time
!= action solver time
```

---

# 8. Training lifecycle

| Paper | World/policy training lifecycle | Deployment |
|---|---|---|
| Epona | joint trajectory+visual shared-representation training | planner can run without visual generation |
| WorldDrive | heavy generative pretrain/teacher → distillation | lightweight future scorer online |
| Drive-JEPA | predictive representation pretrain → planner/scorer fine-tune | JEPA predictor absent |
| Metis | asymmetric joint world-action co-training | action-only |
| DynFlowDrive | training-only flow WM + score teaching | planner/scorer only |
| **DriveLaW** | **video generation pretrain stages 1–2 → stage-3 action-only objective with all Video/Action DiT params trainable** | **Video DiT retained for one pass + Action DiT** |

DriveLaW is neither frozen-transfer nor simultaneous multitask training.

Best description:

```text
generative pretraining
→ end-to-end policy task adaptation of the same backbone
```

---

# 9. Strongest matched planning evidence

| DriveLaW mechanism | Matched result | What it supports | Main boundary |
|---|---|---|---|
| video pretraining scale | `85.9→87.0→87.8→89.1` PDMS for 0/76k/3.8M/7.6M | larger driving-video pretraining helps planning | data exposure / representation quality confounded with "world fidelity" |
| representation source | BEV `84.1`, VLM `86.5`, video latent `89.1` | video-generator representation useful | feature producers not perfectly matched priors |
| video denoise tap | step 1 `89.1`, step 5 `86.9`, step 10 `23.2` | early generative state is more decision-useful | does not explain exactly which latent semantics matter |

This is stronger mechanistic evidence than the cross-method SOTA table.

---

# 10. Video fidelity vs planning utility

DriveLaW video results:

```text
FID  4.6
FVD 81.3
```

Planning result:

```text
PDMS 89.1
```

However:

```text
later / more denoised video state
→ substantially WORSE planning
```

Therefore:

```text
visual-generation maturity
!= decision representation quality
```

This strengthens an existing cross-anchor rule already suggested by Epona:

```text
video/world fidelity and planning utility must be evaluated separately.
```

---

# 11. Counterfactual / reactive vector

| Paper | Candidate-specific world output | Alternative-action truth | Reactive other-agent truth | Reactive-policy evidence |
|---|---:|---:|---:|---:|
| WoTE | YES | limited/non-reactive | NO in audited NAVSIM path | benchmark-dependent |
| World4Drive | YES | NO | NO | NAVSIM non-reactive |
| DynFlowDrive | YES training-only | NO | NO | NAVSIM non-reactive |
| Discrete-WAM | action-conditioned generation capability | NO matched truth | NOT ESTABLISHED | NAVSIM non-reactive |
| GraphWorld | NO per-candidate branch | NO | NO WM intervention truth | YES Bench2Drive policy |
| **DriveLaW** | **NO** | **NO** | **NO** | **NAVSIM non-reactive only in audited planning result** |

DriveLaW's strong planning performance therefore says little about counterfactual world validity because counterfactual branching is not its mechanism.

---

# 12. Paper/source audit contribution

DriveLaW adds two implementation-level cautions to the project methodology.

## 12.1 Flow-target sign

Paper:

```text
a_t=(1-t)a0+t epsilon
Eq.9 target: a0-epsilon
```

Source:

```text
target = epsilon-a0
```

Since the derivative of the stated interpolation is `epsilon-a0`, source and paper differ.

## 12.2 Action sampling steps

```text
paper:                  5
released config:         5
validation routine:      5
current agent forward:  10 hard-coded
```

Thus exact benchmark code/version pinning remains necessary even when an official repo is available.

---

# 13. New twelve-anchor conclusions

## 13.1 "Online world model" is not binary

We now need at least:

```text
full online consequence rollout       WoTE
compact endpoint future               World4Drive
future-aware hidden refinement        SeerDrive / GraphWorld
partial generative-backbone execution DriveLaW
no deployed world branch              LAW / Drive-JEPA / Metis / DynFlowDrive
```

## 13.2 "Unified world-action" remains non-scalar

DriveLaW:

```text
separate Video and Action parameters
strong forward representation dependence
strong backward action→video gradient coupling in stage 3
both modules active at inference
no action→world consequence branch
```

Therefore one label `joint/unified=yes` remains scientifically useless.

## 13.3 More imagination is not automatically better

Across anchors:

```text
SeerDrive: predicting more intermediate BEV times did not improve planning
DriveLaW: deeper video denoising sharply worsened planning
DynFlowDrive: more solver steps eventually worsened planning
```

The shared principle is:

```text
decision-relevant future/world computation has an optimal abstraction/depth;
more complete internal world computation is not monotonically useful.
```

This is a cross-paper observation only, not yet a research problem promotion.

---

# 14. Ontology decision

Potential residue:

```text
GENERATIVE-STATE TAP LOCATION / SOLVER-DEPTH OF POLICY CONDITION
```

Current decision:

```text
NO V1.4 AMENDMENT
```

Reason:

```text
DriveLaW provides one strong anchor,
but the distinction is still representable through F08/J01/J03/N.
Require back-projection and another independent generative-latent policy paper before splitting.
```

Ontology remains:

```text
V1.3 ACTIVE
```
