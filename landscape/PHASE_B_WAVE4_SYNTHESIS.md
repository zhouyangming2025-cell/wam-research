# PHASE_B_WAVE4_SYNTHESIS — What Does “Closed Loop / Reactive” Actually Mean?

Last updated: 2026-09-14

Status: **THREE ANCHORS COMPLETE — Bench2Drive ↔ HUGSIM ↔ ORION**

Wave 4:

```text
Bench2Drive      COMPLETE
HUGSIM           COMPLETE
ORION            COMPLETE
ReactSim-Bench   NEXT
CausalDrive      PENDING
```

Canonical detailed audits:

```text
audits/literature/PHASE_B_WAVE4_BENCH2DRIVE_HUGSIM_AUDIT.md
audits/literature/PHASE_B_WAVE4_ORION_AUDIT.md
```

---

## 1. First field correction: “closed loop” is too coarse a binary label

Evaluation feedback should be decomposed into at least four axes:

```text
F_e = ego-state / dynamics feedback
F_s = sensor / viewpoint feedback
F_a = surrounding-agent state feedback
F_b = surrounding-agent behavioral-response feedback
```

A provisional map:

| regime | F_e | F_s | F_a | F_b |
|---|---|---|---|---|
| open-loop logged trajectory evaluation | no sequential control loop | no | logged only | no |
| NAVSIM | short ego rollout/scoring but not repeated sensor-policy interaction | no novel sensor | fixed/logged environment approximation | no reactive response |
| Bench2Drive | yes | yes, CARLA synthetic sensors | yes | scenario-dependent scripted/adaptive |
| HUGSIM | yes | yes, reconstructed photorealistic views | yes | regime-dependent: replay=no; IDM/attack=yes by controller |
| ORION | inherits Bench2Drive | inherits Bench2Drive | inherits Bench2Drive | inherits Bench2Drive; ORION itself is not the behavior simulator |

This decomposition is binding for the rest of Wave 4.

---

## 2. Bench2Drive — interaction-rich policy evaluation, not a world-model benchmark

Bench2Drive is a **standardized, scenario-disentangled CARLA closed-loop E2E benchmark**:

```text
44 interactive scenarios
× 5 short routes
= 220 evaluation routes
~150 m each
```

The policy repeatedly acts in CARLA, so ego action changes physics and future observations. Source inspection confirms that at least some ScenarioRunner actors are ego-adaptive; e.g. `YieldToEmergencyVehicle` uses an `AdaptiveConstantVelocityAgentBehavior` tied to ego and ego-relative trigger conditions.

Its traffic interactions are therefore more than fixed replay, but they come from CARLA/ScenarioRunner scripted/controller logic rather than a learned real-driver response distribution.

Bench2Drive’s primary contribution is:

```text
interactive closed-loop E2E evaluation
+ standardized training data
+ short-route skill decomposition
```

not photorealistic real-camera simulation or learned world dynamics.

---

## 3. HUGSIM — sensor realism and traffic reactivity must be separated

HUGSIM reconstructs real captured driving scenes with 3D Gaussian Splatting and closes the sensor loop:

```text
reconstructed world
→ render observation at current ego pose
→ planner outputs waypoints
→ LQR updates ego
→ actors update
→ render next observation
→ repeat
```

Its actor behavior is heterogeneous:

```text
replayed actor
→ explicitly non-interactive with ego

IDM / constant-speed actor
→ hand-designed normal behavior; IDM may yield to ego

aggressive actor
→ plans candidate trajectories against predicted ego future
→ explicit ego-dependent adversarial interaction
```

Therefore HUGSIM demonstrates photorealistic sensor feedback plus controller-defined interaction, but not statistical validation of real human counterfactual responses.

---

## 4. Visual realism and behavioral realism already diverge

The first block exposes an important two-axis space:

```text
VISUAL / SENSOR REALISM
vs
BEHAVIORAL / INTERACTION REALISM
```

Bench2Drive emphasizes high scenario/interactivity coverage with synthetic CARLA appearance.

HUGSIM emphasizes reconstructed-real-scene appearance while behavior is replayed or supplied by hand-designed/optimization controllers.

Therefore:

```text
more photorealistic != more behaviorally realistic
more interactive != more sensor-realistic
```

---

## 5. ORION — semantic reasoning can be a strong planning route without world rollout

ORION is best classified as a **VLA planner**, not a world-model planner.

Its deployed path is:

```text
multi-view images
→ vision encoder
→ QT-Former
   → scene/perception/history queries
   → explicit traffic-state + motion auxiliary supervision
   → long-term memory
→ scene/history tokens
→ LLM hierarchical VQA / driving reasoning
→ special planning-token embedding
→ generative trajectory planner
→ multimodal ego trajectories
```

There is auxiliary surrounding-agent motion prediction, but no explicit environment transition of the form:

```text
current world + ego candidate
→ candidate-specific future world
→ evaluate action
```

and no recursive latent environment rollout.

Thus:

```text
AUXILIARY FUTURE/MOTION SUPERVISION != WORLD-MODEL PLANNING
```

is reinforced by another family beyond LAW/ViDAR.

---

## 6. ORION’s strongest evidence is about the reasoning→action interface, not “LLM magic”

With matched QT-Former components:

```text
plain-text output:
traffic + motion + memory → 42.23 DS / 13.14% SR

generative planning-token interface:
traffic + motion + memory → 77.74 DS / 54.62% SR
```

Difference:

```text
+35.51 DS
+41.48 percentage points SR
```

This is strong evidence that the interface converting semantic/reasoning representation into continuous action matters.

But another ablation is equally important. Within the generative branch:

```text
baseline                              56.33 DS / 26.05 SR
+ traffic-state supervision           74.65 / 49.31
+ motion prediction                   74.07 / 49.77
+ memory bank                         77.74 / 54.62
```

The largest staged jump comes from explicit traffic-state supervision, not from auxiliary motion prediction. Therefore the paper does not isolate abstract VLM common-sense reasoning as the unique source of its gain.

A more defensible mechanism statement is:

```text
semantic/traffic-state alignment
+ long-term temporal context
+ differentiable reasoning-token → trajectory-generation interface
jointly produce strong closed-loop performance.
```

---

## 7. ORION independently reinforces open-loop / closed-loop mismatch

History-query ablation:

```text
Nh=0   DS 65.10 / SR 38.83 / L2 0.67
Nh=8   DS 68.09 / SR 39.09 / L2 0.66
Nh=16  DS 74.10 / SR 44.66 / L2 0.68
Nh=32  DS 62.46 / SR 37.73 / L2 0.65
```

The best open-loop L2 setting (`Nh=32`) is not the best closed-loop policy. This strengthens the historical result that trajectory imitation distance is not a sufficient planning metric.

---

## 8. Three distinct things now sit under “better closed-loop driving”

Wave 4 has already separated three routes:

```text
Bench2Drive
→ improve EVALUATION STRUCTURE and interactive scenario coverage

HUGSIM
→ improve SENSOR/RENDERING FEEDBACK REALISM and support interactive actor controllers

ORION
→ improve POLICY REPRESENTATION / SEMANTIC REASONING / ACTION GENERATION
```

These are orthogonal enough that headline driving-score improvements should not be treated as evidence for the same capability.

---

## 9. What “reactive world model” must mean more precisely

After Bench2Drive/HUGSIM/ORION, merely showing:

```text
ego action → different next world state
```

is insufficient to establish a new reactive-world capability.

For ReactSim-Bench / CausalDrive we now require:

```text
A. Does ego intervention alter other-agent predicted behavior?
B. Is that behavior learned or scripted?
C. What supervision identifies the response?
D. Is the response consistent with the same observed episode/history?
E. Is behavioral accuracy explicitly evaluated?
F. What reference exists for unexecuted alternatives?
G. Does improved reaction quality change policy/planning outcomes?
```

`action-conditioned` answers only part of A.

---

## 10. Historical picture is multi-dimensional, not a single ladder

The field should not be narrated simply as:

```text
open loop → closed loop → reactive world models
```

A more accurate set of overlapping developments is:

```text
logged-data evaluation
interactive physics/game-engine simulation
standardized scenario-level E2E evaluation
photorealistic reconstructed sensor simulation
semantic/VLA policy reasoning
learned/reactive behavior simulation
action-conditioned world modeling
```

Modern WAM papers occupy some combination of these axes rather than one scalar maturity level.

---

## 11. Next — ReactSim-Bench

ReactSim-Bench is now the critical measurement anchor.

It must be audited against both historical controls:

```text
M2I / GameFormer / What Truly Matters
```

and simulator controls:

```text
Bench2Drive / HUGSIM
```

Questions:

```text
what constitutes an ego deviation/intervention?
what exactly is predicted about other agents?
what reference reaction is available?
how is reaction quality measured?
does the benchmark distinguish visual plausibility from behavioral correctness?
are alternative-action futures true counterfactual labels or constructed proxies?
which model families fail under reactive pressure?
```

Only then should CausalDrive be judged as a reactive-WM method.

---

## Current stable Wave-4 statements

```text
Closed-loop evaluation must be described by the feedback channels it closes, not by the binary label alone.
Photorealistic sensor feedback and behaviorally valid agent reaction are independent capabilities.
Strong closed-loop planning can improve through semantic/reasoning-action interfaces without an explicit world rollout.
```

No research gap is declared.
