# WAM Comparison Matrix V1.3 — SafeDrive Extension

Last updated: 2026-09-15

Status: **FOURTEEN-ANCHOR EXTENSION — ONTOLOGY V1.3 RETAINED**

Anchors now include:

```text
LAW | WoTE | Epona | WorldDrive | World4Drive | SeerDrive
| Drive-JEPA | Metis | DynFlowDrive | Discrete-WAM | GraphWorld
| DriveLaW | DA-WAM | SafeDrive
```

SafeDrive full projection:

```text
landscape/P0002_SAFEDRIVE_ONTOLOGY_PROJECTION.md
```

---

# 1. Canonical planning-interface taxonomy

| Paper | Canonical world/planning interface |
|---|---|
| LAW | predictive training signal / future-latent auxiliary |
| WoTE | online recurrent consequence model + explicit utility |
| Epona | shared world representation + direct generative policy |
| WorldDrive | predictive representation inheritance + distilled online consequence evaluation |
| World4Drive | online compact latent foresight + factual-mode matching |
| SeerDrive | online bidirectional future-feature / planner co-refinement |
| Drive-JEPA | predictive representation pretraining + simulator-distilled proposal/selection planner |
| Metis | asymmetric world-action co-training + action-only deployment |
| DynFlowDrive | training-only flow-dynamics mode/score supervision |
| Discrete-WAM | shared discrete world-policy pretraining + direct token policy |
| GraphWorld | online structured world state → direct multimodal planner |
| DriveLaW | online generative hidden state → direct Action-DiT policy |
| DA-WAM | online candidate-specific short future latent → factorized utility scorer |
| **SafeDrive** | **online candidate-specific sparse interaction world → fine-grained safety evaluator → selection** |

SafeDrive adds a strong anchor for:

```text
structured future consequence
+
explicit localized safety semantics
```

---

# 2. Candidate-specific output vs truth

| Paper | Candidate-specific future/world output | Candidate-specific value/safety label | Candidate-specific observed alternative-world truth | Reactive other-agent truth |
|---|---:|---:|---:|---:|
| WoTE | YES | YES | partial/simulator-pseudo | NO in audited NAVSIM path |
| World4Drive | YES | factual-mode label | NO | NO |
| DynFlowDrive | YES training branches | hybrid mode teacher | NO | NO |
| DA-WAM | YES | YES factor/utility/rank | NO except one expert factual branch | NO |
| **SafeDrive** | **YES** | **YES — PDM per-proposal + agent/time safety** | **NO — logged agent future reused across ego branches** | **NO in audited NAVSIM path** |

Binding conclusion sharpened by SafeDrive:

```text
candidate-specific consequence labels
can be much richer than
candidate-specific environment-future truth
```

Do not use `counterfactual` as a scalar label.

---

# 3. Safety / scorer semantics

| Paper | Explicit decision semantics | Granularity |
|---|---|---|
| WoTE | NC/DAC/TTC/comfort/progress/imitation utility | trajectory / rollout aggregate |
| WorldDrive | preference / PDMS-like ranking | trajectory-level |
| World4Drive | factual-future mode consistency | mode-level, NOT explicit utility |
| DA-WAM | NC/DAC/EP/TTC/Comfort + utility | candidate-level factorization |
| GraphWorld | no explicit online utility | representation-conditioned direct policy |
| **SafeDrive** | **scene NC/DAC/TTC/EP/etc + PwNC + TwDAC** | **scene + agent×time + time-wise road-compliance** |

SafeDrive is the strongest current anchor showing that `explicit safety` itself has a granularity axis.

---

# 4. Structured world representation

| Paper | World substrate | Planning use |
|---|---|---|
| WoTE | recurrent BEV | consequence → reward |
| GraphWorld | structured interaction latent | direct policy conditioning |
| DA-WAM | implicit V-JEPA future latent | utility scoring |
| **SafeDrive** | **ego planning query + sparse agent queries + explicit future motions** | **localized safety reasoning + selection** |

SafeDrive and GraphWorld both move away from appearance-centric world states, but their decision interfaces differ:

```text
GraphWorld: structured W → policy
SafeDrive:  structured W_i → safety/value_i → select
```

---

# 5. World-model supervision coverage

| Paper | Direct future/world target coverage across alternatives |
|---|---|
| World4Drive | one factual future latent supervises/assigns among multiple mode futures |
| DA-WAM | only expert-matched branch receives dense future latent target |
| SafeDrive | agent-motion GT is logged/factual and reused across candidate-world branches; safety labels are candidate-specific |
| WoTE | simulator/pseudo consequence targets; audited other-agent track semantics remain largely logged/non-reactive |

SafeDrive therefore forces a three-layer supervision decomposition:

```text
WORLD STATE / MOTION TRUTH
vs
CONSEQUENCE / SAFETY TRUTH
vs
FINAL VALUE / RANKING TRUTH
```

These layers may have different candidate coverage.

---

# 6. Strongest matched attribution

| Paper | Strongest relevant matched control | Main interpretation |
|---|---|---|
| DA-WAM | No Future 93.31 → Action-Future 93.46 → +HardNeg 93.68 | future contribution modest; value supervision material |
| GraphWorld | ECIG-only 85.5 → full WSCP 90.1 NAVSIM | world-state refinement/conditioning bundle major |
| DriveLaW | Video latent 89.1 vs BEV 84.1 / VLM 86.5; denoise step 1 best | generative internal representation useful; more denoising not better |
| **SafeDrive** | **BEV+scene ≈ Sparse+scene ≈90.9; Sparse+fine-grained 91.6** | **sparse representation alone not isolated; benefit comes from representation × fine-grained safety interface** |

SafeDrive fine-grained-head controls:

```text
scene-level baseline  ~90.9
+ PwNC                ~91.5
+ TwDAC               ~91.4
+ both                ~91.6
```

---

# 7. Online deployment lifecycle

| Paper | Heavy/external teacher at training? | World/future retained online? | Online selector |
|---|---:|---:|---|
| WorldDrive | YES | lightweight future retained | ranking |
| DynFlowDrive | YES | NO world model | learned score head |
| DA-WAM | EMA target training-only | YES candidate future predictor | factorized scorer |
| **SafeDrive** | **YES PDM safety teacher** | **YES sparse world + safety heads** | **weighted explicit safety scorer** |

SafeDrive is therefore neither a fully online simulator nor a fully distilled action-only policy:

```text
external simulator teacher removed
but learned consequence representation/evaluator remains online
```

---

# 8. Evaluation semantics

| Evidence | Correct interpretation |
|---|---|
| SafeDrive NAVSIM PDMS/EPDMS | strong non-reactive candidate-selection performance under PDM/logged-world semantics |
| PwNC/TwDAC training labels | candidate-specific safety consequences under PDM, not reactive world trajectories |
| Bench2Drive 66.8 paper result | reactive final-policy competence |
| Bench2Drive result | NOT direct validation of branch-level counterfactual world dynamics |

---

# 9. Cross-anchor scientific correction after SafeDrive

Before SafeDrive it was tempting to use:

```text
candidate-specific world
→ candidate-specific safety
```

as one combined property.

SafeDrive shows these must be split:

```text
1. Is world representation branched by candidate?
2. Is environment-state/motion truth branched by candidate?
3. Is safety/consequence truth branched by candidate?
4. Is value/ranking truth branched by candidate?
5. Are surrounding agents reactively resimulated under the intervention?
```

SafeDrive values:

```text
1 YES
2 NO
3 YES
4 YES
5 NO in audited NAVSIM path
```

This is representable in Ontology V1.3 via existing G/I/K/P dimensions; no V1.4 is required.

---

# 10. Ontology decision

Potential residue:

```text
SAFETY-LOCALIZATION GRANULARITY
```

Current decision:

```text
V1.3 RETAINED
NO V1.4
```

Reason: the distinction is already captured by state/scorer semantic granularity and target-provenance dimensions. Keep it on the residue watchlist until another independent anchor makes a separate dimension scientifically necessary.
