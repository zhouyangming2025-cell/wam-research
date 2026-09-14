# NEXT_TASK

## 唯一下一任务

> Execute the **Phase-B Wave-4 ORION audit**, using the completed Bench2Drive ↔ HUGSIM feedback decomposition as the control.

Waves 1–3 and the Research QA Gate are closed. Broad corpus acquisition remains frozen.

Canonical Wave-4 artifacts:

```text
landscape/PHASE_B_WAVE4_PLAN.md
landscape/PHASE_B_WAVE4_SYNTHESIS.md
audits/literature/PHASE_B_WAVE4_BENCH2DRIVE_HUGSIM_AUDIT.md
```

## Wave-4 status

```text
Bench2Drive      = COMPLETE
HUGSIM           = COMPLETE
ORION            = NEXT
ReactSim-Bench   = PENDING
CausalDrive      = PENDING
Wave 4           = OPEN
```

## Stable first-block result

Replace binary `closed-loop` wording with four feedback axes:

```text
F_e = ego-state / dynamics feedback
F_s = sensor / viewpoint feedback
F_a = surrounding-agent state feedback
F_b = surrounding-agent behavioral-response feedback
```

Bench2Drive:

```text
CARLA synthetic sensors
F_e=yes / F_s=yes / F_a=yes
F_b=scenario-dependent scripted/adaptive
```

HUGSIM:

```text
reconstructed photorealistic sensors
F_e=yes / F_s=yes / F_a=yes
F_b=regime-dependent:
  replay=no
  IDM/normal=controller-reactive
  attack=explicit ego-dependent adversarial replanning
```

Therefore:

```text
photorealistic sensor realism != behavioral realism
interactive simulator != learned real-driver response model
```

## ORION audit

ORION is a VLA/semantic-reasoning control. Do not assume it is a world-model paper.

Trace exactly:

```text
1. visual / language / navigation inputs
2. intermediate reasoning representation
3. whether reasoning is free-form text, structured token, latent, or supervision-only
4. trajectory/action representation
5. exact training stages and supervision sources
6. whether reasoning representation is consumed by the deployed planner
7. whether there is any predictive future/world-state module
8. whether future reasoning is about scene evolution, ego intent, affordance, or language explanation
9. closed-loop benchmark(s) and exact feedback semantics
10. strongest matched ablations isolating reasoning/VLA contribution
11. strongest non-language / non-WM planning baseline
12. runtime / planning frequency
13. strongest evidence and strongest alternative explanation
```

Required verdict:

```text
Is ORION primarily:
A. VLA planner,
B. world-model planner,
C. VLA + predictive world representation,
or D. another mechanism?
```

Do not allow terminology such as “reasoning” or “world understanding” to substitute for a traced data/inference path.

## After ORION

```text
ReactSim-Bench
→ CausalDrive
```

Those two papers must be read against both:

```text
historical interaction controls (M2I / GameFormer / What Truly Matters)
```

and:

```text
simulator feedback controls (Bench2Drive / HUGSIM)
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
