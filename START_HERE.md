# START_HERE — WAM Research Brain

**Purpose:** a fresh GPT-5.6 Sol session should recover the project direction and active scientific task in under a minute without reconstructing old chats.

Last updated: 2026-09-14 — Wave 3 active through DriveLaW

## 1. Research north star

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Planning is the center of gravity. Perception, video generation, JEPA/latent prediction, VLA, safety/risk modeling and simulation matter only insofar as they affect planning capability, decision quality, closed-loop behavior, or scientific understanding of planning.

**Risk field is NOT a required destination.** Prior risk/predictive-risk expertise is an optional capability pool, not a research commitment.

## 2. Methodological rule

```text
UNDERSTAND THE FIELD FIRST
→ representative comparative deep reads
→ cross-family synthesis
→ only then research-problem / gap discovery
```

P1/P2-R/P3 are parked historical probes. No gap declaration or method design is authorized yet.

## 3. Current stage

```text
FIELD RECONSTRUCTION — PHASE B: WAVE 3 ACTIVE
```

Phase A:

```text
60 stable IDs: P0001–P0060
58 RAW_MD_READY
2 lawful-source blockers: P0008 NPPC, P0020 Bahram 2016
F1–F11 coverage PASS
broad ingestion FROZEN
25 representative anchors FIXED
```

Wave 1 and Wave 2 are closed.

## 4. Binding field distinctions from Waves 1–2

Do not collapse:

```text
controllable generation
!= predictive pretraining
!= auxiliary future supervision
!= online hidden future representation
!= candidate-specific future evaluator
!= joint world-action generation
!= WM as RL imagination environment
```

Also:

```text
conditional future != causal/interventional response
action-conditioned != reactively supervised
candidate-specific output != candidate-specific oracle supervision
multimodal trajectory planner != automatically a WM
candidate scorer != automatically a WM
world fidelity != decision utility
longer horizon != better planning
generation quality != planning evidence
WM-assisted planning != online model-based planning
```

Evaluation regimes remain distinct: nuScenes open-loop logs; nuPlan OL/CL-NR/CL-R; NAVSIM non-reactive pseudo-simulation; Bench2Drive interactive CARLA closed loop; HUGSIM reconstructed photorealistic closed loop; real-vehicle closed loop remains sparse.

## 5. Wave-2 baseline

Read when needed:

```text
landscape/PHASE_B_WAVE2_SYNTHESIS.md
landscape/PHASE_B_WAVE2_COMPARABILITY_AUDIT.md
audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md
```

Stable role map:

```text
GAIA-1   = controllable generation; no operational planner interface
Drive-WM = candidate → visual future → perception/reward → selection
OccWorld = joint future occupancy + ego generation
WoTE     = candidate → future BEV → learned reward → selection
ViDAR    = predictive pretraining
LAW      = action-aware future-latent representation shaping
```

Key evidence: better OccWorld reconstruction can worsen forecasting/planning; WoTE future state adds value over scorer-only but audited PDM alternative-action targets share logged surrounding-agent futures; ViDAR future decoder is not deployed; LAW future latent is training supervision, not test-time plan input.

## 6. Wave 3 — current scientific state

Canonical files:

```text
landscape/PHASE_B_WAVE3_PLAN.md
landscape/PHASE_B_WAVE3_SYNTHESIS.md
```

Status:

```text
Epona       = COMPLETE first pass
DrivingGPT  = COMPLETE first pass
DriveLaW    = COMPLETE first pass
Auto-JEPA   = NEXT
DA-WAM      = PENDING
Think2Drive = PENDING
```

World-action unification already splits into:

```text
Epona
= shared historical latent F
→ separate trajectory/video diffusion generators
→ visual generation can be disabled for planning

DrivingGPT
= interleaved discrete image/action language
→ one causal next-token Transformer

DriveLaW
= Video-DiT internal denoising latent
→ direct condition for Action DiT
→ online generative hidden state becomes planner representation
```

Important DriveLaW evidence:

```text
video-pretraining scale: 85.9 → 87.0 → 87.8 → 89.1 PDMS
BEV / VLM / video-latent condition: 84.1 / 86.5 / 89.1
Video-DiT denoise state t=1 / 5 / 10: 89.1 / 86.9 / 23.2
```

Interpret this as representation-state-specific planning utility, not as a universal fidelity law.

Do not rank Epona/DrivingGPT/DriveLaW by headline PDMS without matched split/input/training conditions.

## 7. Immediate task

Read `state/NEXT_TASK.md`.

The next paper is **Auto-JEPA**. Compare it directly against:

```text
OccWorld — better reconstruction can be worse for planning
LAW      — predictive supervision can help without online rollout; longer horizon not monotonic
DriveLaW — online WM hidden state can be useful, but exact latent choice matters sharply
```

Question to answer: what future information does Auto-JEPA preserve/discard, what survives at inference, and what matched evidence shows planning-oriented compression rather than generic auxiliary/pretraining benefit?

Then continue `DA-WAM → Think2Drive`.

## 8. Evidence discipline

Always separate:

```text
AUTHOR CLAIM
DIRECT EXPERIMENTAL EVIDENCE
OUR INFERENCE
```

Always ask:

```text
What exactly is predicted?
What gets direct supervision?
What is the supervision source for alternative actions?
What survives at inference?
How does planning consume it?
What competing mechanism explains the gain?
What evaluation regime supports the claim?
```

Every anchor gets both strongest evidence and strongest limitation.

## 9. Fast new-session read order

```text
1. START_HERE.md
2. state/CURRENT_STATE.md
3. state/NEXT_TASK.md
4. landscape/PHASE_B_WAVE3_PLAN.md
5. landscape/PHASE_B_WAVE3_SYNTHESIS.md
6. landscape/PHASE_B_WAVE2_COMPARABILITY_AUDIT.md  # only as control when needed
```

Then read only the primary texts needed for the active comparison.

## 10. Source hierarchy

```text
Official/canonical PDF       = exact source authority
GitHub raw MD + figures      = GPT-readable primary-text layer
Paper Card                   = curated paper understanding
Wave synthesis / Field Atlas = cross-paper understanding
State files                  = canonical project decisions
Chat                         = temporary reasoning workspace
```

If raw MD is ambiguous, verify against the official/canonical PDF rather than guessing.

## 11. Division of labor

**GPT-5.6 Sol:** comparative anchor deep reads, cross-paper synthesis, atlas/cards/state maintenance, targeted source audit only when decision-critical.

**Local corpus agent:** on-demand acquisition/extraction, MinerU/QC, local code execution, datasets/checkpoints/experiments.

The repo — not conversation memory — is the research authority.