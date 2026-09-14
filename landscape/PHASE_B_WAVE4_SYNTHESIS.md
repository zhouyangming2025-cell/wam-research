# PHASE_B_WAVE4_SYNTHESIS — What Does “Closed Loop / Reactive” Actually Mean?

Last updated: 2026-09-14

Status: **FIRST BLOCK COMPLETE — Bench2Drive ↔ HUGSIM**

Wave 4:

```text
Bench2Drive      COMPLETE
HUGSIM           COMPLETE
ORION            NEXT
ReactSim-Bench   PENDING
CausalDrive      PENDING
```

Canonical detailed audit:

`audits/literature/PHASE_B_WAVE4_BENCH2DRIVE_HUGSIM_AUDIT.md`

---

## 1. First field correction: “closed loop” is too coarse a binary label

The first two anchors show that evaluation feedback should be decomposed into at least four axes:

```text
F_e = ego-state / dynamics feedback
F_s = sensor / viewpoint feedback
F_a = surrounding-agent state feedback
F_b = surrounding-agent behavioral-response feedback
```

The usual label `closed-loop` hides whether each of these is actually present and what mechanism supplies it.

A provisional map:

| regime | F_e | F_s | F_a | F_b |
|---|---|---|---|---|
| open-loop logged trajectory evaluation | no sequential control loop | no | logged only | no |
| NAVSIM | short ego rollout/scoring but not repeated sensor-policy interaction | no novel sensor | fixed/logged environment approximation | no reactive response |
| Bench2Drive | yes | yes, CARLA synthetic sensors | yes | scenario-dependent scripted/adaptive |
| HUGSIM | yes | yes, reconstructed photorealistic views | yes | regime-dependent: replay=no; IDM/attack=yes by controller |

This decomposition is now binding for later Wave-4 work.

---

## 2. Bench2Drive — interaction-rich policy evaluation, not a world-model benchmark

Bench2Drive is best understood as a **standardized, scenario-disentangled CARLA closed-loop E2E benchmark**.

Its key design is:

```text
44 interactive scenarios
× 5 short routes
= 220 evaluation routes
~150 m each
```

rather than long routes that mix many skills and compound infraction penalties.

The policy acts repeatedly in CARLA, so ego action changes physics and future observations. The environment also contains scenario-specific actor logic. Source inspection confirms that at least some actors directly depend on ego state; e.g. `YieldToEmergencyVehicle` uses an `AdaptiveConstantVelocityAgentBehavior` linked to the ego vehicle and ego-relative trigger/end conditions.

Therefore Bench2Drive is not merely “replay with a driving score.”

But its traffic interactions are supplied by CARLA/ScenarioRunner logic, not a learned real-driver response distribution. Its main realism strength is **interactive coverage and evaluation structure**, not real-camera photorealism or counterfactual behavioral identification.

---

## 3. HUGSIM — sensor realism and traffic reactivity must be separated

HUGSIM takes a complementary route:

```text
real driving logs
→ reconstruct 3D dynamic scene with Gaussian Splatting
→ render from ego's new closed-loop viewpoints
→ update ego + actors
→ repeat
```

Its principal advance is that when ego deviates, the simulator can render a plausible new camera observation from a reconstructed real scene instead of replaying the logged camera stream.

But actor behavior is heterogeneous:

```text
replayed actor
→ explicitly non-interactive with ego

IDM / constant-speed actor
→ hand-designed normal behavior; IDM may yield to ego

aggressive actor
→ online candidate planning against predicted ego future
→ explicitly ego-dependent / adversarial
```

Thus HUGSIM simultaneously demonstrates:

```text
photorealistic closed-loop sensor feedback
and
controller-defined interactive traffic
```

but does not establish that the controller responses reproduce the conditional distribution of real human reactions.

---

## 4. Two forms of realism already diverge

The first block exposes an important two-axis space:

```text
VISUAL / SENSOR REALISM
vs
BEHAVIORAL / INTERACTION REALISM
```

Bench2Drive emphasizes:

```text
high scenario/interactivity coverage
but synthetic CARLA rendering
```

HUGSIM emphasizes:

```text
real-scene photorealistic rendering
while actor behavior is replayed or hand-designed/controller-generated
```

Therefore:

```text
more photorealistic != more behaviorally realistic
more interactive != more sensor-realistic
```

This is a field-understanding distinction, not a claim that one benchmark is superior overall.

---

## 5. What “reactive world model” must now mean more precisely

After Bench2Drive/HUGSIM, merely showing:

```text
ego action → different next world state
```

is too weak to distinguish a modern reactive world model from established simulator capabilities.

For ReactSim-Bench / CausalDrive we must ask a stricter sequence:

```text
A. Does ego intervention alter other-agent predicted behavior?
B. Is that behavior learned or scripted?
C. What supervision identifies the response?
D. Is the response consistent with the same observed episode/history?
E. Is behavioral accuracy explicitly evaluated?
F. What reference exists for unexecuted alternatives?
G. Does improved reaction quality matter to policy/planning outcomes?
```

`action-conditioned` answers only A partially. It does not answer C–G.

---

## 6. Why this changes how we read Wave 4

The historical story is no longer:

```text
open loop
→ closed loop
→ reactive world models
```

A more accurate story is multi-dimensional:

```text
logged-data evaluation
→ interactive physics/game-engine simulation
→ standardized scenario-level E2E evaluation
→ photorealistic reconstructed sensor simulation
→ learned/reactive behavior simulation
→ action-conditioned world modeling
```

These lines overlap rather than forming one simple ladder.

The remaining Wave-4 anchors must be placed in this space rather than ranked by publication date.

---

## 7. Next — ORION

ORION is next because it supplies a different control:

```text
Can high-level semantic / language reasoning improve closed-loop planning
without the paper's main contribution being a reactive world simulator?
```

Audit ORION for:

```text
observation input
language/reasoning representation
trajectory/action generator
training supervision
whether reasoning representation is causally consumed at inference
closed-loop benchmark(s)
comparison against strong non-language planners
whether any world-model component exists or the method should remain a VLA control
```

Only after that should ReactSim-Bench and CausalDrive be read as the explicitly reactive-world branch.

---

## Current stable Wave-4 statement

```text
Closed-loop evaluation must be described by the feedback channels it closes,
not by the binary label alone.
Photorealistic sensor feedback and behaviorally valid agent reaction are independent capabilities.
```

No research gap is declared.
