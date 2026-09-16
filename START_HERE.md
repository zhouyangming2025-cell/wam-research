# START_HERE — WAM Research Brain

**Purpose:** a fresh GPT-5.6 Sol session should recover the project direction and active scientific task in under a minute without reconstructing old chats.

Last updated: **2026-09-16 — 16 normalized anchors; Wave C.6 closed; Wave C.7 active; SAFE-SIM next**

## 1. Research north star

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Planning is the center of gravity. Perception, video generation, JEPA/latent prediction, VLA, safety/risk modeling, reward learning and simulation matter only insofar as they affect planning capability, decision quality, closed-loop behavior, or scientific understanding of planning.

**Risk field is NOT a required destination.** Prior risk/predictive-risk expertise is an optional capability pool, not a research commitment.

---

## 2. Methodological rule

```text
UNDERSTAND THE FIELD FIRST
→ broad comparative deep reads
→ dimension-first normalization
→ cross-family synthesis
→ only after sufficient maturity: research-problem discovery
→ falsification
→ method design
```

Binding status:

```text
research-direction convergence   PAUSED
candidate-problem promotion      PAUSED
method design                    FORBIDDEN
literature expansion             ACTIVE
```

Working maturity gate:

```text
~24–30 normalized papers
+
major-family diversity
+
ontology saturation / diminishing new residues
```

Paper selection is coverage-driven, not hypothesis-driven.

---

## 3. Current scientific state

Normalized anchor count:

```text
16
```

Current comparison set:

```text
P0048 LAW
P0045 WoTE
P0001 Epona
P0042 WorldDrive
P0046 World4Drive
P0061 SeerDrive
P0049 Drive-JEPA
P0062 Metis
P0063 DynFlowDrive
P0064 Discrete-WAM
P0065 GraphWorld
P0009 DriveLaW
P0012 DA-WAM
P0002 SafeDrive
P0005 RiskWorld
P0007 DriveReward
```

Canonical ontology:

```text
WAM_DIMENSION_ONTOLOGY V1.3
```

No V1.4 is currently authorized.

---

## 4. Binding distinctions already established

Never collapse:

```text
controllable generation
!= predictive pretraining
!= auxiliary future supervision
!= online hidden future representation
!= candidate-specific future evaluator
!= joint world-action generation
!= direct value/reward modeling
!= reactive traffic simulation
```

Also:

```text
conditional future != causal/interventional response
action-conditioned != reactively supervised
candidate-specific output != candidate-specific future-world truth
multimodal trajectory planner != automatically a WM
candidate scorer != automatically a WM
explicit risk predictor != trajectory value model
world fidelity != decision utility
longer horizon != better planning
generation quality != planning evidence
world rollout depth != planner-coupling strength
```

Evaluation regimes remain distinct:

```text
nuScenes open-loop logs
nuPlan OL / CL-NR / CL-R
NAVSIM non-reactive data-driven pseudo-simulation
Bench2Drive interactive CARLA closed loop
HUGSIM reconstructed photorealistic closed loop
traffic-simulator closed-loop behavioral evaluation
real-vehicle closed loop
```

---

## 5. Latest completed wave — C.6

```text
P0009 DriveLaW      COMPLETE
P0012 DA-WAM        COMPLETE
P0002 SafeDrive     COMPLETE
P0005 RiskWorld     COMPLETE
P0007 DriveReward   COMPLETE
```

C.6 forced separation of several mechanisms that had previously been easy to narrate as one generic `world-model benefit`:

```text
online generative hidden representation
candidate-specific future latent
candidate-specific safety consequence
factual future risk prediction
direct semantic value/reward learning
```

The latest control, DriveReward, establishes:

```text
current/short-history visual context + candidate trajectory
→ learned factorized semantic reward
→ RL reward teacher OR test-time scorer
```

without an explicit future-world state.

Its reported evidence is stronger for **training-time RL reward** than online reranking:

```text
AdaThinkDrive Original     90.3 PDMS
Best-of-4                  93.0
DriveReward                90.5
```

Therefore:

```text
future/world modeling
!=
value/reward modeling
```

Canonical DriveReward artifacts:

```text
papers/deep_analysis/P0007_DRIVEREWARD_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_DRIVEREWARD_AUDIT.md
landscape/P0007_DRIVEREWARD_ONTOLOGY_PROJECTION.md
landscape/WAM_COMPARISON_MATRIX_V1_3_DRIVEREWARD_EXTENSION.md
```

---

## 6. Current wave — C.7 simulation / reactivity controls

Correct queue:

```text
P0066 SAFE-SIM       RESERVED / INGEST NEXT
P0067 ProSim         RESERVED / INGEST PENDING
P0013 BridgeSim      RAW_MD_READY / DEEP READ PENDING
P0014 ReactSimBench  RAW_MD_READY / DEEP READ PENDING
P0015 CausalDrive    RAW_MD_READY / DEEP READ PENDING
```

Purpose:

```text
reactive environment modeling
behavior simulation
log replay vs endogenous reaction
generative simulator vs planning WAM
simulation / intervention truth
evaluation-regime semantics
```

Feedback coordinates to track:

```text
F_e = ego-state / dynamics feedback
F_s = sensor / viewpoint feedback
F_a = surrounding-agent state feedback
F_b = surrounding-agent behavioral-response feedback
```

A closed-loop simulator is not automatically evidence of causally correct counterfactual response.

---

## 7. Stable-ID integrity correction

On 2026-09-16 the expansion queue was audited and corrected.

Existing corpus IDs are immutable. In particular:

```text
P0003 = GraphAD
P0004 = BeTop
P0006 = GenDrive
P0010 = TOAD
P0011 = SensitivityShaping
```

The old queue had accidentally reused these IDs for future targets.

New reservations:

```text
P0066 SAFE-SIM
P0067 ProSim
P0068 AutoVLA
P0069 ReCogDrive
P0070 LINGO-2
P0071 DriveGPT4
```

See:

```text
audits/research_synthesis/REPO_STATE_INTEGRITY_AUDIT_20260916.md
```

Reserved IDs are not yet ingested corpus entries.

---

## 8. Immediate task

Read:

```text
state/NEXT_TASK.md
```

The unique next task is:

```text
P0066 SAFE-SIM
```

Before deep reading:

```text
register corpus ID
verify canonical paper/version
verify attributable official source/code
create readable raw primary-text layer
```

Then reconstruct exactly:

```text
what closes the loop
which agents react to whom
what is generated once vs regenerated each step
how diffusion/adversarial guidance relates to physical time
what realism evidence exists
what counterfactual truth does NOT exist
how traffic simulation differs from planning WAM
```

Then compare directly against ProSim, RiskWorld, SafeDrive, WoTE/DA-WAM and closed-loop benchmarks where appropriate.

---

## 9. Evidence discipline

Always separate:

```text
AUTHOR CLAIM
DIRECT EXPERIMENTAL EVIDENCE
OUR INFERENCE
```

Always ask:

```text
What exactly is represented / predicted?
What gets direct supervision?
What is the truth source?
What survives at inference?
How does planning consume it?
Which feedback loop is actually closed?
What competing mechanism explains the gain?
What evaluation regime supports the claim?
```

Every anchor gets both strongest evidence and strongest limitation.

---

## 10. Fast new-session read order

```text
1. START_HERE.md
2. state/CURRENT_STATE.md
3. state/NEXT_TASK.md
4. landscape/WAM_DEEP_READ_EXPANSION_QUEUE_V1.md
5. landscape/WAM_DIMENSION_ONTOLOGY_V1.md
6. landscape/WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
7. landscape/WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
8. landscape/WAM_DIMENSION_ONTOLOGY_V1_3_AMENDMENT.md
```

For recent state-integrity history:

```text
audits/research_synthesis/REPO_STATE_INTEGRITY_AUDIT_20260916.md
```

Then read only the primary texts and normalized anchors required for the active comparison.

---

## 11. Source hierarchy

```text
Official/canonical PDF       = exact source authority
GitHub raw MD + figures      = GPT-readable primary-text layer
Deep analysis / Paper Card   = curated paper understanding
Ontology / comparison matrix = normalized cross-paper understanding
State files                  = canonical research decisions
Chat                         = temporary reasoning workspace
```

If raw MD is ambiguous, verify against the official/canonical PDF or attributable source rather than guessing.

---

## 12. Division of labor

**GPT-5.6 Sol:** comparative deep reads, cross-paper synthesis, ontology/state maintenance, targeted source/code audit, direct GitHub write-back.

**Local corpus agent:** bulk acquisition/extraction, MinerU/QC, local code execution, datasets/checkpoints/experiments.

The repo — not conversation memory — is the research authority.
