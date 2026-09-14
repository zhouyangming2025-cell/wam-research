# NEXT_TASK

## 唯一下一任务

> Execute the **Phase-B Wave-4 first comparative block: Bench2Drive → HUGSIM**, using the closed Research QA Gate as the evidence standard.

Waves 1–3 and the Research QA Gate are closed. Broad corpus acquisition remains frozen.

Canonical plan:

```text
landscape/PHASE_B_WAVE4_PLAN.md
```

## Completed immediately before this task

```text
Priority-A evidence verification A1–A8 = COMPLETE
Research QA Gate                     = CLOSED
Wave 4 authorization                 = GRANTED
```

Canonical QA closeout:

```text
audits/literature/RESEARCH_QA_GATE_CLOSEOUT.md
```

Important correction carried forward:

```text
DriveLaW Stage-3 planner training updates both Video DiT and Planning/Action DiT.
Do not describe it as a frozen video feature extractor plus separately trained planner.
```

Explicit unresolved item carried forward:

```text
DrivingGPT exact optimized NAVSIM decode path = UNRESOLVED because official code link is unavailable.
Do not assume either mandatory visual-token generation or a planning bypass.
```

## Wave-4 status

```text
Bench2Drive      = NEXT
HUGSIM           = PENDING
ORION            = PENDING
ReactSim-Bench   = PENDING
CausalDrive      = PENDING
Wave 4           = OPEN
```

## First comparative block — Bench2Drive → HUGSIM

The first block must establish a clean evaluation/simulator baseline before reading reactive-WM claims.

### Bench2Drive audit

Trace exactly:

```text
1. simulator / CARLA version and benchmark protocol
2. sensor inputs available to the policy
3. planner/control outputs
4. ego feedback loop
5. surrounding-traffic behavior and whether it responds to ego
6. scenario/route composition and long-tail events
7. metrics and infraction semantics
8. distinction from CARLA Leaderboard v1/v2
9. policy evaluation frequency / runtime constraints
10. what Bench2Drive does and does NOT validate about a world model
```

### HUGSIM audit

Trace exactly:

```text
1. scene-reconstruction representation
2. novel-view / sensor rendering mechanism
3. ego dynamics and pose feedback
4. surrounding-agent replay / behavior model / reactivity
5. whether other agents respond to ego deviation
6. photorealism metrics vs behavioral metrics
7. planner evaluated inside HUGSIM, if any
8. closed-loop protocol and runtime
9. what comes from logged scene reconstruction vs generated behavior
10. strongest realism claim and strongest boundary
```

### Required comparison

Produce one explicit matrix:

| axis | Bench2Drive | HUGSIM |
|---|---|---|
| ego feedback | | |
| sensor feedback | | |
| surrounding-agent feedback | | |
| photorealistic rendering | | |
| learned behavior model | | |
| policy/planner evaluated | | |
| main realism target | | |

The synthesis must explain why:

```text
interactive closed-loop policy benchmark
!=
photorealistic reconstructed closed-loop simulator
```

unless the evidence shows their feedback semantics actually coincide.

## Subsequent order

```text
Bench2Drive → HUGSIM
→ ORION
→ ReactSim-Bench
→ CausalDrive
```

ReactSim-Bench and CausalDrive must not be interpreted until the baseline meaning of feedback/reactivity has been fixed by Bench2Drive/HUGSIM.

## Stop condition for first block

Do not move to ORION until we can state in one unambiguous sentence for both Bench2Drive and HUGSIM:

```text
what the ego controls,
what changes after the ego acts,
what the next observation contains,
and whether surrounding agents behaviorally respond to ego intervention.
```

## Still forbidden

```text
no gap declaration
no method design
no broad paper accumulation
no P2-R/P3 rescue program
no forced risk-field insertion
no conflation of rendering realism with behavioral realism
no conflation of action conditioning with causal counterfactual validity
```
