# CURRENT_STATE

> **2026-09-19 operational note.** Field Reconstruction, 17 anchors and Wave C.7 remain the program state recorded below. The fixed canonical-12 mechanism audit is a temporary evidence-consolidation gate: it may repair or remove derived material, but it does not replace this program, authorize route conclusions, or cancel ProSim. After that gate, resume the ProSim task described in `state/NEXT_TASK.md`.


Last substantive scientific update: **2026-09-16 — SAFE-SIM COMPLETE; 17 NORMALIZED ANCHORS; WAVE C.7 ACTIVE; PROSIM NEXT**

## Research north star

```text
WAM / World Model + one-stage End-to-End + Planning-centric autonomous driving
```

Core WAM remains primary. Risk/safety/reward/simulation/VLA papers are included when they expose mechanisms required to understand planning-centric WAM; they are not selected to support a preferred future method.

## Methodology in force

```text
FIELD UNDERSTANDING FIRST
→ broad core-WAM coverage
→ comparative anchor deep reads
→ dimension-first normalization
→ periodic consolidation
→ evidence/source QA
→ ONLY AFTER sufficient field maturity: adversarial problem discovery
→ falsification
→ method design
```

Binding status:

```text
research-direction convergence      PAUSED
candidate-problem promotion         PAUSED
method design                       FORBIDDEN
broad literature expansion          ACTIVE
```

Working maturity gate:

```text
~24–30 deeply normalized papers
+
multiple independent anchors across major mechanism families
+
ontology saturation / diminishing new residues
```

Diversity and saturation matter more than raw count.

---

# Canonical normalized anchors — 17

```text
P0048 LAW           COMPLETE v2
P0045 WoTE          COMPLETE v2
P0001 Epona         COMPLETE v2 + source audit
P0042 WorldDrive    COMPLETE v2 + source audit
P0046 World4Drive   COMPLETE v2 + core source audit
P0061 SeerDrive     COMPLETE v2 + version/source audit
P0049 Drive-JEPA    COMPLETE v2 + source audit
P0062 Metis         COMPLETE v2 + paper/repo audit
P0063 DynFlowDrive  COMPLETE v2 + paper/repo audit
P0064 Discrete-WAM  COMPLETE v2 + paper/source-status audit
P0065 GraphWorld    COMPLETE v2 + paper/source-status audit
P0009 DriveLaW      COMPLETE v2 + official-source audit
P0012 DA-WAM        COMPLETE v2 + official-repo-status audit
P0002 SafeDrive     COMPLETE v2 + NAVSIM source audit
P0005 RiskWorld     COMPLETE v2 + paper/source-status audit
P0007 DriveReward   COMPLETE v2 + reward/value boundary audit
P0066 SAFE-SIM      COMPLETE v2 + official source/code audit
```

Canonical ontology:

```text
V1.3 ACTIVE
NO V1.4 authorized by SAFE-SIM
```

---

# Latest scientific correction — P0066 SAFE-SIM

Canonical files:

```text
papers/raw_md/P0066_SafeSim/P0066_SafeSim.source_note.md
papers/deep_analysis/P0066_SAFESIM_DEEP_ANALYSIS_V2.md
audits/literature/P0066_SAFESIM_SOURCE_CODE_AUDIT.md
audits/literature/PHASE_C7_SAFESIM_AUDIT.md
landscape/P0066_SAFESIM_ONTOLOGY_PROJECTION.md
landscape/WAM_COMPARISON_MATRIX_V1_3_SAFESIM_EXTENSION.md
```

Canonical subtype:

```text
REACTIVE CLOSED-LOOP TRAFFIC BEHAVIOR SIMULATOR
+
PLANNER-CONDITIONED ADVERSARIAL DIFFUSION GENERATOR
```

Core closed loop:

```text
current scene
→ ego planner produces current ego future plan
→ ego plan explicitly enters reactive-agent generation/guidance
→ non-ego trajectories are generated / guided / filtered
→ joint actions execute in physical environment
→ new scene state
→ planner and reactive agents replan
→ repeat
```

Code-verified feedback:

```text
F_e ego-state/dynamics feedback                 YES
F_a surrounding-agent state feedback           YES
F_b surrounding behavioral-response feedback   YES
F_s sensor/viewpoint photorealistic feedback   NO / NOT CORE
```

Critical truth boundary:

```text
reactive model-generated response              YES
paired real intervention-response truth        NO
causal counterfactual identification           NO
```

SAFE-SIM therefore establishes a stronger reactivity level than fixed/logged-future WAM branches without establishing real counterfactual truth.

Diffusion semantics:

```text
K=100 denoising steps
!= physical future time
!= closed-loop episode steps
```

Paper experiment replans planner + reactive agents at 2 Hz.

Partial diffusion:

```text
collision-type proposal
→ partially noise in diffusion coordinate
→ guided denoise
→ controllable adversarial trajectory
```

Strongest ablation lesson:

```text
partial diffusion ↑ collision diversity
regularization ↓ pathological/off-road adversarial behavior
more collision generation != better simulator
```

SAFE-SIM's main realism evidence is distributional trajectory-profile similarity, not paired intervention-response validation.

---

# Cross-paper synthesis after 17 anchors

The corpus now separates at least these mechanisms:

```text
training-only predictive representation shaping
online world/latent representation for policy
candidate-specific future consequence prediction
explicit risk/safety modeling
direct value/reward modeling
external reactive world simulation
```

The latest pair of controls is especially useful:

```text
DriveReward
= direct value/reward without explicit future world

SAFE-SIM
= explicit interactive behavior simulation outside planner
```

A planner can therefore receive consequence knowledge through very different interfaces.

Reactivity/counterfactual ladder currently supported by anchors:

```text
Level 0  factual logged future only                     RiskWorld-type
Level 1  output changes with hypothetical ego action    many action-conditioned WAMs
Level 2  surrounding behavior regenerates after ego change  SAFE-SIM
Level 3  paired real intervention-response truth        not yet established
```

This is a truth/feedback classification, not a quality ranking.

---

# Wave C.7 — ACTIVE

```text
P0066 SAFE-SIM       COMPLETE
P0067 ProSim         NEXT / SOURCE GATE PENDING
P0013 BridgeSim      RAW_MD_READY / DEEP READ PENDING
P0014 ReactSimBench  RAW_MD_READY / DEEP READ PENDING
P0015 CausalDrive    RAW_MD_READY / DEEP READ PENDING
```

Wave C.7 purpose:

```text
reactive environment modeling
behavior simulation
log replay vs endogenous reaction
generative simulator vs planning WAM
simulation / intervention truth
evaluation-regime semantics
```

Carry-forward questions:

```text
what closes the loop?
which feedback channels exist?
what is generated once vs regenerated?
what supervises behavior under changed ego action?
what metric validates reaction quality?
does realism mean distributional similarity or intervention validity?
```

---

# Source / manifest status

SAFE-SIM paper and official code are verified; official repo was audited at:

```text
27c96a84e7bf5fbca4b47f6edde386811d76c6e7
```

A normal full local raw-MD extraction is still pending.

`CORPUS_MANIFEST.csv` could not be safely edited through the GitHub text connector because it is not exposed as UTF-8 text. Registration is therefore explicitly pending local reconciliation:

```text
manifests/P0066_SAFESIM_REGISTRATION_PENDING.md
```

Stable ID remains binding:

```text
P0066 = SAFE-SIM
P0067 = ProSim
P0068 = AutoVLA
P0069 = ReCogDrive
P0070 = LINGO-2
P0071 = DriveGPT4
```

---

# Parked provisional synthesis

Research-direction artifacts remain historical/provisional during expansion.

```text
research-direction convergence = PAUSED
problem promotion              = PAUSED
method design                  = FORBIDDEN
```

---

# Canonical next task

Read:

```text
state/NEXT_TASK.md
```

Current target:

```text
P0067 ProSim
```

First verify source/version/code and ingest a readable source layer; then deep-read as the second independent reactive-simulation anchor.
