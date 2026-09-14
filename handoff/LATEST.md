# LATEST — Handoff

Session: 2026-09-14 — Waves 1–4 closed; Phase-C field synthesis first pass complete; Phase D next.

## New-session fast path

```text
1. START_HERE.md
2. state/CURRENT_STATE.md
3. state/NEXT_TASK.md
4. landscape/PHASE_C_WAVES1_4_FIELD_SYNTHESIS.md
5. audits/literature/RESEARCH_QA_GATE_CLOSEOUT.md
6. landscape/PHASE_B_WAVE4_SYNTHESIS.md
```

Do not default to P2-R/P3. Do not reload the whole corpus or old chats by default.

## Research identity

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Risk-field / predictive-risk expertise is optional prior knowledge, not a required destination.

Active methodology:

```text
UNDERSTAND FIELD FIRST
→ comparative deep reads
→ cross-family synthesis
→ adversarial problem discovery
→ falsification
→ only then method design
```

## Corpus / reconstruction status

```text
P0001–P0060 = 60 registered
58 RAW_MD_READY
F1–F11 coverage = PASS
broad acquisition = FROZEN

Wave 1            CLOSED
Wave 2            CLOSED
Wave 3            CLOSED
Research QA Gate  CLOSED
Wave 4            CLOSED
Phase C synthesis COMPLETE FIRST PASS
Phase D           NEXT
```

## Canonical Phase-C synthesis

`landscape/PHASE_C_WAVES1_4_FIELD_SYNTHESIS.md`

Its central field map is:

```text
I1 training-only predictive shaping
I2 online predictive state → direct planner
I3 joint world-action generation
I4 planning-oriented future compression
I5 candidate consequence evaluation
I6 imagined environment for policy learning
I7 learned interactive simulator
```

Planning-centric WAM is therefore not one architecture; the key variable is where predictive/world information enters the decision process.

## Stable project-wide distinctions

```text
world prediction quality != planning evidence
future information is not automatically beneficial
world completeness != decision relevance
candidate-specific output != candidate-specific observed counterfactual supervision
WM-assisted planning != online model-based planning
action conditioning != reactive supervision != counterfactual truth
closed-loop must be decomposed into feedback channels
sensor photorealism != behavioral realism
log realism != reactive robustness
simulator quality != planner quality
```

## Wave-4 feedback coordinate system

```text
F_e = ego-state / dynamics feedback
F_s = sensor / viewpoint feedback
F_a = surrounding-agent state feedback
F_b = surrounding-agent behavioral-response feedback
```

Key placements:

```text
Bench2Drive    = standardized interactive CARLA policy benchmark
HUGSIM         = reconstructed photorealistic closed-loop simulator + external actor behavior
ORION          = VLA semantic/reasoning planner; no explicit world rollout
ReactSim-Bench = learned behavior-WM reactivity benchmark under off-log ego behavior
CausalDrive    = real-time learned action-conditioned reactive visual simulator
```

ReactSim/CausalDrive boundary:

```text
REALISM / LOG-LIKENESS
!= REACTIVE FEASIBILITY
!= COUNTERFACTUAL BEHAVIORAL TRUTH
```

## Important QA facts

```text
LAW predicted future latent not consumed for current test-time action selection = CODE VERIFIED
WoTE audited target path uses fixed logged surrounding futures                 = CODE VERIFIED
DA-WAM directly supervises observed future only for expert-matched candidate  = PAPER VERIFIED
DriveLaW Stage-3 updates both Video DiT and Action/Planning DiT                = PAPER + CODE VERIFIED
DrivingGPT exact optimized NAVSIM runtime decode path                          = UNRESOLVED
```

## Phase-C evidence gaps — not research gaps

```text
1. real alternative-action surrounding-agent ground truth
2. reactive simulator quality → planner decision quality
3. simultaneous sensor-realistic + behaviorally validated closed loop
4. intervention-conditioned uncertainty calibration
5. long-horizon compounding under ego/sensor/agent/model feedback
6. compute-normalized planning benefit
7. representation semantics vs scale/capacity
8. real-vehicle closed-loop validation
9. standardized feedback-semantic reporting
10. planner robustness to world-model error
```

No item is selected as the research problem.

## Immediate next task

Read `state/NEXT_TASK.md`.

Execute **Phase D — Adversarial Problem Discovery** and create:

```text
landscape/PHASE_D_PROBLEM_DISCOVERY_ROUND1.md
```

Use 5–8 candidate problem statements maximum. Every candidate must be attacked by historical precedent, strongest current method, strongest non-WM explanation, counterexample, measurement feasibility and realistic evaluation relevance.

Verdicts:

```text
SURVIVES / WEAK / KILLED / EVIDENCE INSUFFICIENT
```

No method proposals in Round 1.

## Still forbidden

```text
no method design
no broad paper accumulation
no automatic P2-R/P3 revival
no forced risk-field insertion
no gap declaration from a missing module or missing metric alone
```

The repo, not conversation memory, is the canonical research authority.
