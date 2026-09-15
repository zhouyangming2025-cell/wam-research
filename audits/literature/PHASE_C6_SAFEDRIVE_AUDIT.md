# Phase C.6 SafeDrive Audit

Last updated: 2026-09-15

Status: **COMPLETE FIRST PASS — PAPER + OFFICIAL NAVSIM SOURCE VERIFIED; BENCH2DRIVE SOURCE PARTIAL**

Paper:

```text
SafeDrive: Fine-Grained Safety Reasoning for End-to-End Driving in a Sparse World
CVPR 2026 Highlight
arXiv:2602.18887
```

Canonical deep read:

```text
papers/deep_analysis/P0002_SAFEDRIVE_DEEP_ANALYSIS_V2.md
```

Official implementation:

```text
SPA-junghokim/SafeDrive@ea7791d6c2ebdeedfb6ed514f080cdfa1675b76f
```

---

# 1. Stable mechanism judgment

SafeDrive is not simply a dense world model with an extra safety head. Its deployed NAVSIM mechanism is:

```text
ProposalNet
→ multimodal BEV / objects / 256 ego anchors
→ coarse trajectory refinement + scene-level safety pruning

selected ego candidate j
+ copied surrounding-agent queries
→ sparse world j
→ intra-world interaction + trajectory-guided future feature sampling
→ joint ego / agent motion refinement

sparse world j
→ FRNet
→ scene safety
 + pair-wise no-collision(agent,time)
 + time-wise drivable-area compliance
→ learned weighted safety score
→ select trajectory
```

Canonical subtype:

```text
ONLINE TRAJECTORY-CONDITIONED SPARSE-WORLD SAFETY EVALUATOR
```

---

# 2. Source/version boundary

Audited release contains:

```text
model/training/evaluation code
Phase-1/2/3 configs
NAVSIM PDM target generator
released checkpoints
NAVSIM reproduction script
```

Official README reports the released checkpoint reproducing ~91.6 PDMS.

Current source caveat:

```text
NAVSIM core mechanism and score path        SOURCE-VERIFIED
Bench2Drive paper result                    PAPER-VERIFIED
Bench2Drive public execution path           NOT IDENTIFIED
```

Do not infer the CARLA/Bench2Drive implementation from the NAVSIM code.

---

# 3. Claim → evidence → interpretation → unproven

## Claim A — sparse worlds are trajectory-conditioned

**DIRECT PAPER EVIDENCE**

Each selected planning query is combined with copied surrounding-instance queries to build an independent sparse world.

**SOURCE EVIDENCE**

`safedrive_model.py` builds 256 frozen anchor priors, a two-stage planning decoder, SWNet `MotionTransformer`, and candidate/world-specific query tensors. The released Phase-3 config enables 2-stage proposals, top-128 stage-2 selection, and 25-agent filtering.

**INTERPRETATION**

Candidate identity persists into structured ego/agent world reasoning rather than being pooled before evaluation.

**UNPROVEN**

Candidate-specific representation does not establish candidate-specific intervention-valid environment truth.

---

## Claim B — SafeDrive performs explicit fine-grained safety reasoning

**DIRECT PAPER EVIDENCE**

FRNet defines Pair-wise No Collision (PwNC) and Time-wise Drivable Area Compliance (TwDAC), localizing safety by agent and/or future time.

**SOURCE EVIDENCE**

`safedrive_model.py` constructs:

```text
pwnc_heads     → num_pose outputs from ego-agent paired features
twdac_heads    → num_pose outputs from ego/world features
scene safety   → NC/DAC/TTC/EP and optional DDC/TLC/LK/PDM score
```

`test.sh` explicitly includes PwNC and TwDAC in final candidate ranking weights.

**INTERPRETATION**

SafeDrive has explicit online safety semantics, unlike methods where safety is only observed in final PDMS/EPDMS.

**UNPROVEN**

The learned heads are not formal safety guarantees or calibrated physical-risk probabilities.

---

## Claim C — safety targets are candidate-specific

**SOURCE EVIDENCE**

`SafeDrive_Agent.compute_loss()` detaches the model's own final plan candidates and calls the PDM scorer. The scorer returns per-proposal:

```text
NC / DAC / EP / TTC / comfort / DDC
(+ TLC / LK in EPDMS mode)
pair_collision_gt
twdac_gt
```

`compute_navsim_score.py` records at-fault collision token/time and off-road pose indices.

**INTERPRETATION**

SafeDrive has genuine candidate-specific **decision consequence labels** under NAVSIM/PDM semantics.

**BOUNDARY**

The PDM world uses logged/static surrounding-agent semantics; this is not reactive alternative-agent simulation.

---

## Claim D — sparse world predicts candidate-dependent future agent behavior

**ARCHITECTURE FACT**

Different ego candidates create different sparse-world branches and can produce different refined agent-motion outputs.

**SUPERVISION AUDIT**

In the active `all_motion_predidction_loss=true` training path, logged surrounding-agent future motion targets are expanded/reused across the ego-anchor dimension.

Therefore:

```text
candidate-specific predicted world/motion output    YES
candidate-specific safety labels                    YES
candidate-specific factual alternative-agent truth  NO
reactive other-agent intervention truth              NO
```

**BINDING CONTROL**

```text
candidate-conditioned agent prediction
!=
reactive counterfactual dynamics supervision
```

---

# 4. Training lifecycle

Official release documents:

```text
Phase 1  perception pretraining
Phase 2  planner + safety, perception frozen
Phase 3  end-to-end full fine-tune
```

Released script schedule:

```text
90 → 5 → 10 epochs
```

Phase 2 and 3 both enable live PDM-derived safety targets. Phase 2 freezes perception prefixes; Phase 3 is the canonical full-train setup.

Important teacher/student separation:

```text
TRAINING:
model candidates → external PDM simulator/scorer → fine-grained labels

DEPLOYMENT:
model candidates → learned safety heads → weighted score
external PDM teacher = absent online
```

---

# 5. Strongest matched evidence

## Representation × safety granularity

Reported controls are approximately:

```text
baseline/no world                 90.1 PDMS
BEV + basic/coarse safety         90.3
BEV + scene-level safety          90.9
Sparse + scene-level safety       90.9
Sparse + fine-grained safety      91.6
```

Main attribution:

```text
Sparse + scene-level ≈ BEV + scene-level
```

Therefore sparse representation alone is not isolated as the source of gain. The cleanest contribution is the combination of sparse relational structure and fine-grained evaluator semantics.

## Fine-grained heads

```text
scene-level baseline   ~90.9
+ PwNC                 ~91.5
+ TwDAC                ~91.4
+ both                 ~91.6
```

Both help; gains are not additive.

---

# 6. Cross-paper controls

## vs WoTE

Both are online candidate consequence/value selectors.

```text
WoTE      recurrent BEV future → explicit utility
SafeDrive sparse ego-agent world → localized safety/value
```

WoTE is stronger on recurrent future rollout; SafeDrive is stronger on safety localization. Audited NAVSIM paths of both remain non-reactive with respect to alternative-agent intervention truth.

## vs DA-WAM

DA-WAM gives every candidate its own latent but only the expert branch receives future-latent truth. SafeDrive gives all candidates candidate-specific PDM safety labels, while still reusing logged agent-motion truth across ego branches.

Thus:

```text
DA-WAM: supervision asymmetry primarily future-latent vs value
SafeDrive: candidate-specific value/safety truth stronger than candidate-specific world truth
```

## vs GraphWorld

GraphWorld uses structured interaction state to condition a direct policy. SafeDrive uses structured candidate worlds to feed an explicit evaluator.

## vs World4Drive

World4Drive scorer means factual-mode consistency. SafeDrive scorer means explicit safety/compliance/progress.

---

# 7. Counterfactual / reactivity vector

```text
candidate-specific world branch?                 YES
candidate-specific safety/value target?           YES
candidate-specific alternative-agent future GT?   NO
reactive other-agent response truth?               NO in audited NAVSIM path
external intervention-valid world validation?      NO
reactive final-policy evaluation?                  YES at paper level via Bench2Drive
```

Do not collapse the final item into world-model intervention validity.

---

# 8. Evaluation semantics

```text
NAVSIM v1/v2
= NON-REACTIVE DATA-DRIVEN / PSEUDO-SIMULATION PLANNING

Bench2Drive
= REACTIVE CARLA CLOSED LOOP
```

NAVSIM establishes strong candidate safety selection under PDM/logged-world semantics. Bench2Drive establishes final policy competence under interactive execution. Neither alone validates SWNet's branch-specific surrounding-agent predictions as causal counterfactuals.

---

# 9. Paper↔code consistency

| Claim | Paper | Source | Verdict |
|---|---|---|---|
| ProposalNet→SWNet→FRNet | yes | explicit classes/configs | CONSISTENT |
| sparse world per ego candidate | yes | candidate/world query expansion | CONSISTENT |
| joint ego-agent refinement | yes | MotionTransformer world interaction | CONSISTENT |
| fine-grained PwNC | yes | pwnc heads + PDM pair GT | CONSISTENT |
| fine-grained TwDAC | yes | twdac heads + off-road pose GT | CONSISTENT |
| 3-stage training | yes | train docs/configs | CONSISTENT |
| training safety from model-plan PDM rollout | yes/release docs | explicit compute_score | CONSISTENT |
| reactive candidate-specific agent truth | implied cautiously by simulation wording | logged motion GT reused across branches | **NOT ESTABLISHED / IMPORTANT BOUNDARY** |
| Bench2Drive code path | result reported | not found in audited repo | SOURCE-PARTIAL |

---

# 10. Ontology decision

Potential residue:

```text
safety-localization granularity
(scene → agent → agent×time → footprint/time)
```

Existing ontology already represents this through B04, K02/K04/K05 and P01/P02/P04 plus supervision-provenance dimensions.

Decision:

```text
ONTOLOGY V1.3 RETAINED
NO V1.4
```

---

# 11. Final source status

```text
P0002 SafeDrive
PAPER-COMPLETE
SOURCE-COMPLETE FOR NAVSIM CORE MECHANISM
SOURCE-PARTIAL FOR BENCH2DRIVE IMPLEMENTATION
```
