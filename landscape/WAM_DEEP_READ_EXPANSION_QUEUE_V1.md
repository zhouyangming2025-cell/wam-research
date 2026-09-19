# WAM Deep-Read Expansion Queue V1

Last updated: 2026-09-16

Status: **HISTORICAL EXPANSION QUEUE — retained for ID/provenance; current work is controlled by `state/NEXT_TASK.md`.**

## Binding rule

```text
17 normalized anchors
= stronger coordinate system
!= mature field understanding
!= authorization to promote research direction
```

Paper selection remains coverage-driven, not hypothesis-driven.

Working gate before another research-direction discussion:

```text
~24–30 deeply normalized papers total
+
multiple independent anchors across major mechanism families
+
new papers mostly map into the coordinate system without repeatedly exposing major blind spots
```

Required diversity remains:

```text
planning-centric online WAM interfaces
world→policy latent interfaces
candidate-specific future/scoring
explicit safety/risk/value reasoning
reactive behavior simulation / world simulation
evaluation-regime controls
WAM+VLA boundary methods
alternative world representations
training-only vs deployment-time world knowledge
```

---

# Wave C.6 — CLOSED

```text
P0009 DriveLaW      COMPLETE
P0012 DA-WAM        COMPLETE
P0002 SafeDrive     COMPLETE
P0005 RiskWorld     COMPLETE
P0007 DriveReward   COMPLETE
```

C.6 established that these mechanisms must remain separate:

```text
future/world modeling
risk/safety modeling
value/reward modeling
candidate scoring
training-time teacher knowledge
online deployed world knowledge
```

---

# Wave C.7 — Simulation / reactivity / evaluation controls — ACTIVE

## P0066 SAFE-SIM — COMPLETE

Canonical subtype:

```text
REACTIVE CLOSED-LOOP TRAFFIC BEHAVIOR SIMULATOR
+
PLANNER-CONDITIONED ADVERSARIAL DIFFUSION GENERATOR
```

Mechanism:

```text
current scene
→ external ego planner → ego plan
→ learned reactive non-ego diffusion + planner-conditioned guidance
→ selected actions
→ physical environment update
→ new scene
→ repeat
```

Feedback:

```text
F_e YES
F_a YES
F_b YES
F_s NO / not photorealistic core
```

Critical boundary:

```text
model-generated reactive response        YES
paired real intervention-response truth  NO
```

Scientific lesson:

```text
reactive closed-loop generation
is stronger than fixed/logged conditional future prediction
but weaker than intervention-grounded counterfactual truth
```

Key attribution lesson:

```text
more induced collisions != better simulator
```

because stronger adversarial pressure can also increase invalid/off-road behavior and slightly worsen aggregate realism.

Canonical files:

```text
papers/deep_analysis/P0066_SAFESIM_DEEP_ANALYSIS_V2.md
audits/literature/P0066_SAFESIM_SOURCE_CODE_AUDIT.md
audits/literature/PHASE_C7_SAFESIM_AUDIT.md
landscape/P0066_SAFESIM_ONTOLOGY_PROJECTION.md
landscape/WAM_COMPARISON_MATRIX_V1_3_SAFESIM_EXTENSION.md
```

Ontology:

```text
V1.3 RETAINED
NO V1.4
```

Source status:

```text
paper verified
official source/code verified
full local raw-MD extraction pending
canonical CSV manifest reconciliation pending because current file is not exposed as UTF-8 text
```

See:

```text
manifests/P0066_SAFESIM_REGISTRATION_PENDING.md
```

## P0067 ProSim — NEXT

Purpose:

```text
second independent reactive-simulation anchor
```

Main comparison pressure:

```text
SAFE-SIM
= safety-critical planner-conditioned adversarial closed loop

ProSim
= promptable / controllable multi-agent closed-loop simulation
```

The key question is whether SAFE-SIM's reactivity findings generalize beyond collision-seeking adversarial guidance.

Mandatory questions for ProSim:

```text
what is promptable / controllable?
what is jointly generated?
how are non-ego agents conditioned on ego / one another?
what is re-generated each closed-loop step?
what data supervises interaction?
what is the actual feedback carrier?
what metrics validate realism and reactivity?
is planner evaluation performed or is simulation quality the endpoint?
```

## Existing later C.7 anchors

```text
P0013 BridgeSim       RAW_MD_READY / DEEP READ PENDING
P0014 ReactSimBench   RAW_MD_READY / DEEP READ PENDING
P0015 CausalDrive     RAW_MD_READY / DEEP READ PENDING
```

Recommended order:

```text
P0067 ProSim
→ P0013 BridgeSim
→ P0014 ReactSimBench
→ P0015 CausalDrive
```

---

# Wave C.8 — WAM+VLA / reasoning boundary controls

Reserved targets:

```text
P0068 AutoVLA       RESERVED / INGEST PENDING
P0069 ReCogDrive    RESERVED / INGEST PENDING
P0070 LINGO-2       RESERVED / INGEST PENDING
P0071 DriveGPT4     RESERVED / INGEST PENDING
```

Stable-ID rule remains binding:

```text
existing corpus IDs are immutable
```

---

# Reading protocol

```text
paper-deep-reader reconstruction
→ source/version gate
→ architecture/training/inference graph
→ strongest matched ablations
→ immediate cross-paper comparison
→ force-fill Ontology V1.3
→ residue/back-projection test
```

Every paper must answer:

```text
what exactly the module does
what prior anchors do the same scientific job
whether supervision/deployment role is truly comparable
strongest matched evidence
what the paper does NOT prove
```

For C.7 specifically, every paper must also explicitly fill:

```text
F_e / F_s / F_a / F_b
observational future truth
model-generated response
intervention-response truth
```

---

# Parked work

```text
research-direction convergence = PAUSED
problem promotion              = PAUSED
method design                  = FORBIDDEN
```

---

# Next task

```text
P0067 ProSim
```

Required source gate:

```text
verify canonical paper/version
verify attributable official project/code
create readable source layer / source note
record source status
then deep-read
```
