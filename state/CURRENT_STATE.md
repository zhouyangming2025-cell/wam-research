# CURRENT_STATE

> **2026-09-19 operational note.** Field Reconstruction, the normalized anchor set and Wave C.7 remain active. The fixed canonical-12 mechanism audit is closed as a consolidation gate; it does not authorize route conclusions or method design. SAFE-SIM and ProSim are now complete. Continue with state/NEXT_TASK.md.

The only compact cross-paper review surface for that gate is `audits/research_synthesis/WAM_PLANNING_INTERFACE_FRAMEWORK.md` (Q1–Q5, provisional and non-authoritative). Do not create a second projection or matrix layer.

Last substantive scientific update: **2026-09-19 — P0067 ProSim COMPLETE; 18 NORMALIZED ANCHORS; WAVE C.7 ACTIVE**

## Research north star

~~~
WAM / World Model + one-stage End-to-End + Planning-centric autonomous driving
~~~

Core WAM remains primary. Risk/safety/reward/simulation/VLA papers are included when they expose mechanisms required to understand planning-centric WAM; they are not selected to support a preferred future method.

## Methodology in force

~~~
FIELD UNDERSTANDING FIRST
→ broad core-WAM coverage
→ comparative anchor deep reads
→ dimension-first normalization
→ periodic consolidation
→ evidence/source QA
→ ONLY AFTER sufficient field maturity: adversarial problem discovery
→ falsification
→ method design
~~~

Binding status:

~~~
research-direction convergence      PAUSED
candidate-problem promotion         PAUSED
method design                       FORBIDDEN
broad literature expansion          ACTIVE
~~~

Working maturity gate:

~~~
~24–30 deeply normalized papers
+ multiple independent anchors across major mechanism families
+ ontology saturation / diminishing new residues
~~~

## Canonical normalized anchors — 18

~~~
P0048 LAW           COMPLETE v2
P0045 WoTE          COMPLETE v2
P0001 Epona         COMPLETE v2 + source audit
P0042 WorldDrive    COMPLETE v2 + source audit
P0046 World4Drive   COMPLETE v2 + core source audit
P0061 SeerDrive     COMPLETE v2 + version/source audit
P0049 Drive-JEPA   COMPLETE v2 + source audit
P0062 Metis         COMPLETE v2 + paper/repo audit
P0063 DynFlowDrive COMPLETE v2 + paper/repo audit
P0064 Discrete-WAM COMPLETE v2 + paper/source-status audit
P0065 GraphWorld    COMPLETE v2 + paper/source-status audit
P0009 DriveLaW      COMPLETE v2 + official-source audit
P0012 DA-WAM        COMPLETE v2 + official-repo-status audit
P0002 SafeDrive     COMPLETE v2 + NAVSIM source audit
P0005 RiskWorld     COMPLETE v2 + paper/source-status audit
P0007 DriveReward   COMPLETE v2 + reward/value boundary audit
P0066 SAFE-SIM      COMPLETE v2 + official source/code audit
P0067 ProSim        COMPLETE v2 + official source/code audit
~~~

Canonical ontology:

~~~
V1.3 comparison coordinate retained for consolidation
NO V1.4 authorized; ontology is not final route authority
~~~

## Latest scientific correction — P0067 ProSim

Canonical files:

~~~
papers/raw_md/P0067_ProSim/P0067_ProSim.source_note.md
papers/deep_analysis/P0067_PROSIM_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C7_PROSIM_AUDIT.md
~~~

Canonical subtype:

~~~
PROMPTABLE CLOSED-LOOP TRAFFIC BEHAVIOR SIMULATOR
+ SOFT MULTIMODAL AGENT/SCENE CONTROL
~~~

Core feedback:

~~~
F_e ego/state feedback                 YES
F_s sensor/viewpoint feedback          NO / NOT CORE
F_a surrounding-agent state feedback   YES
F_b behavioral response feedback       YES, next-chunk simulator-level
~~~

Truth boundary:

~~~
logged factual future                 YES
prompt labels tied to logged behavior YES
generated response                    YES
paired real intervention truth        NO
causal counterfactual identification  NO
~~~

Release boundary:

~~~
paper describes differentiable closed-loop training
public default MODEL.BPTT=False detaches generated chunks
README says the full training pipeline is not yet released
trajdata rollout_scene_loop is TODO; GPU/distributed path is the auditable path
~~~

No V1.4 residue survives back-projection; no separate ontology projection or matrix extension was created.

## Wave C.7 — ACTIVE

~~~
P0066 SAFE-SIM       COMPLETE
P0067 ProSim         COMPLETE
P0013 BridgeSim      RAW_MD_READY / NEXT
P0014 ReactSimBench  RAW_MD_READY / DEEP READ PENDING
P0015 CausalDrive    RAW_MD_READY / DEEP READ PENDING
~~~

Wave C.7 purpose:

~~~
reactive environment modeling
behavior simulation
log replay vs endogenous reaction
generative simulator vs planning WAM
simulation / intervention truth
evaluation-regime semantics
~~~

Carry-forward questions:

~~~
what closes the loop?
which feedback channels exist?
what is generated once vs regenerated?
what supervises behavior under changed ego action?
what metric validates reaction quality?
does realism mean distributional similarity or intervention validity?
~~~

## Source / manifest status

P0067 source and official code are pinned in the source note and phase audit. CORPUS_MANIFEST.csv remains unchanged because the connector exposes it as binary/non-UTF-8; the explicit pending notes are:

~~~
manifests/P0066_SAFESIM_REGISTRATION_PENDING.md
manifests/P0067_PROSIM_REGISTRATION_PENDING.md
~~~

Stable IDs remain binding:

~~~
P0066 = SAFE-SIM
P0067 = ProSim
P0068 = AutoVLA
P0069 = ReCogDrive
P0070 = LINGO-2
P0071 = DriveGPT4
~~~

## Parked provisional synthesis

~~~
research-direction convergence = PAUSED
problem promotion              = PAUSED
method design                  = FORBIDDEN
~~~

## Canonical next task

Read:

~~~
state/NEXT_TASK.md
~~~

Current target:

~~~
P0013 BridgeSim
~~~
