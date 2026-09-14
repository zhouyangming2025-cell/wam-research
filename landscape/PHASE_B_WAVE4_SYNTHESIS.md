# PHASE_B_WAVE4_SYNTHESIS — What Does “Closed Loop / Reactive” Actually Mean?

Last updated: 2026-09-14

Status: **COMPLETE — WAVE 4 CLOSED**

Wave 4:

```text
Bench2Drive      COMPLETE
HUGSIM           COMPLETE
ORION            COMPLETE
ReactSim-Bench   COMPLETE
CausalDrive      COMPLETE
```

Canonical detailed audits:

```text
audits/literature/PHASE_B_WAVE4_BENCH2DRIVE_HUGSIM_AUDIT.md
audits/literature/PHASE_B_WAVE4_ORION_AUDIT.md
audits/literature/PHASE_B_WAVE4_REACTSIMBENCH_AUDIT.md
audits/literature/PHASE_B_WAVE4_CAUSALDRIVE_AUDIT.md
```

Purpose: reconstruct what `closed-loop`, `interactive`, `reactive`, `photorealistic`, and `causal` actually mean in planning-centric evaluation and learned driving worlds. This is a field-understanding artifact, not a gap declaration.

---

## 1. Executive result: “closed loop” is not one property

Evaluation feedback should be decomposed into at least four channels:

```text
F_e = ego-state / dynamics feedback
F_s = sensor / viewpoint feedback
F_a = surrounding-agent state feedback
F_b = surrounding-agent behavioral-response feedback
```

A compact map:

| regime / system | F_e | F_s | F_a | F_b | primary object being tested |
|---|---|---|---|---|---|
| open-loop logged evaluation | no sequential control loop | no | logged only | no | trajectory/prediction fit |
| NAVSIM | short ego rollout/scoring, not repeated sensor-policy interaction | no novel sensor | fixed/logged approximation | no reactive response | short-horizon planning quality |
| nuPlan reactive mode | yes in abstract simulator state | no novel raw sensor synthesis | yes | simulator/controller dependent | planner closed-loop behavior |
| Bench2Drive | yes | yes, CARLA synthetic sensors | yes | scenario-dependent scripted/adaptive | E2E policy capability |
| HUGSIM | yes | yes, reconstructed photorealistic views | yes | replay=no; IDM/attack=controller-defined yes | sensor-realistic closed-loop evaluation |
| ReactSim-Bench | AV future externally fixed | state/trajectory level, not visual rendering target | yes | **learned simulator is the evaluation target** | reactive feasibility under ego deviation |
| CausalDrive | yes, streaming ego condition | yes, learned video generation | implicitly synthesized | learned/prompt-conditioned | interactive learned visual world simulation |

The binary label `closed-loop` is therefore scientifically insufficient. Later claims must name which feedback channel is closed and by what mechanism.

---

## 2. Bench2Drive — interaction-rich policy evaluation, not a world-model benchmark

Bench2Drive is best understood as a standardized, scenario-disentangled CARLA closed-loop E2E benchmark:

```text
44 interactive scenarios
× 5 short routes
= 220 evaluation routes
~150 m each
```

The policy repeatedly acts in CARLA, so ego action changes physics and future observations. Source inspection confirms that at least some ScenarioRunner actors are ego-adaptive; for example `YieldToEmergencyVehicle` uses an `AdaptiveConstantVelocityAgentBehavior` tied to the ego vehicle and ego-relative trigger/end conditions.

Therefore Bench2Drive is not fixed replay. But its interaction comes from CARLA / ScenarioRunner controller logic, not a learned distribution of real-driver reactions.

Its primary contribution is:

```text
interactive closed-loop E2E evaluation
+ standardized training data
+ short-route skill decomposition
```

not photorealistic real-camera simulation or learned world dynamics.

A key benchmark result is that open-loop L2 can disagree with closed-loop ranking, reinforcing the older Wave-1 result that imitation distance alone is not sufficient planning evidence.

---

## 3. HUGSIM — photorealistic sensor feedback and traffic reactivity are separate axes

HUGSIM reconstructs real captured driving scenes with 3D Gaussian Splatting and closes the sensor loop:

```text
reconstructed scene
→ render observation at current ego pose
→ planner outputs waypoints
→ controller updates ego
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
→ online candidate planning against predicted ego future
→ explicit ego-dependent adversarial interaction
```

Thus HUGSIM combines strong sensor/viewpoint feedback with controller-defined actor behavior. It does not establish that those actor responses match the conditional distribution of real human reactions.

This exposes the first major Wave-4 two-axis distinction:

```text
VISUAL / SENSOR REALISM
!=
BEHAVIORAL / INTERACTION REALISM
```

More photorealistic does not automatically mean more behaviorally realistic, and more interactive does not automatically mean more sensor-realistic.

---

## 4. ORION — strong closed-loop planning can improve without an explicit world rollout

ORION is best classified as a VLA planner rather than a world-model planner.

Deployed path:

```text
multi-view images
→ vision encoder
→ QT-Former
   → scene/perception/history queries
   → traffic-state + motion auxiliary supervision
   → long-term memory
→ scene/history tokens
→ LLM reasoning
→ special planning-token embedding
→ generative trajectory planner
→ multimodal ego trajectories
```

There is surrounding-agent motion prediction as auxiliary supervision, but no explicit environment transition of the form:

```text
(current world, ego candidate)
→ candidate-specific future world
→ evaluate candidate
```

nor recursive latent environment rollout.

The strongest matched evidence concerns the reasoning-to-action interface:

```text
plain-text output with traffic+motion+memory:
42.23 DS / 13.14% SR

generative planning-token interface with same high-level components:
77.74 DS / 54.62% SR
```

Within the generative branch:

```text
baseline                       56.33 DS / 26.05 SR
+ traffic-state supervision    74.65 / 49.31
+ motion prediction            74.07 / 49.77
+ memory bank                  77.74 / 54.62
```

The largest staged jump comes from explicit traffic-state supervision, not auxiliary motion prediction. The defensible mechanism statement is therefore:

```text
semantic/traffic-state alignment
+ temporal memory
+ differentiable reasoning-token → trajectory-generation interface
jointly support strong closed-loop performance.
```

ORION is a necessary control against any claim that explicit future-world rollout is required for strong interactive planning.

---

## 5. ReactSim-Bench — reactivity becomes an explicit measurement target

ReactSim-Bench makes a precise protocol change relative to realism benchmarks such as WOSAC:

```text
logged history
+ externally supplied ego future that deliberately deviates from the log
→ learned simulator controls surrounding agents only
→ surrounding agents must react to realized ego behavior
```

The AV is not controlled by the same simulator being evaluated. This removes an important shortcut: the simulator cannot choose both ego and agent futures so they remain mutually compatible and close to the log.

The 2,636-scenario test set contains:

```text
937 longitudinal deviations
799 directional deviations
900 lateral deviations
```

and is deliberately filtered for feasible ego deviations that impose interaction pressure.

### Direct benchmark-design evidence

If the deviated ego is paired with logged surrounding-agent replay:

```text
≥1 AV-agent collision occurs in 83.46% of scenarios
minimum TTC < 0.5 s occurs in 98.14%
```

Therefore simple log replay is invalidated in most selected cases and a response is genuinely required.

### Realism and reactive performance can disagree

Representative comparison:

```text
MTR realism ADE         2.5498
CTG realism ADE         1.9405   ← better log realism

MTR reactive collision  0.1457
CTG reactive collision  0.6195   ← much worse under ego deviation
```

This directly establishes:

```text
LOG REALISM != REACTIVE ROBUSTNESS
```

for behavior simulators.

### Crucial boundary

For the unexecuted deviated ego trajectory there is no real recorded surrounding-agent alternative future. ReactSim therefore evaluates:

```text
safety
rule compliance
kinematic feasibility
```

under ego deviation, not exact agreement with an unobserved real counterfactual trajectory.

The binding distinction becomes:

```text
REALISM / LOG-LIKENESS
!=
REACTIVE FEASIBILITY
!=
COUNTERFACTUAL BEHAVIORAL TRUTH
```

---

## 6. CausalDrive — learned reactive visual simulation is real, causal identification is not established

CausalDrive is substantially more than a passive video generator:

```text
initial front-view frame
+ streaming ego trajectory/control
+ semantic driving-sociology prompt
→ autoregressive visual future
→ synthesized surrounding-agent reactions
→ real-time ~12 FPS
```

A key architectural choice is to omit future NPC boxes/trajectories. Unlike layout-conditioned renderers, surrounding-agent future behavior is therefore a model output rather than an oracle geometry input.

This establishes a genuine learned interactive-world capability:

```text
ACTION-CONDITIONED + SEMANTICALLY CONTROLLABLE REACTIVE SYNTHESIS
```

### Driving-sociology supervision

SocioDrive-Bench uses roughly:

```text
20K clips
80% nuPlan-derived real interactions
20% CARLA safety-critical/collision cases
```

with kinematic/event mining plus VLM→LLM semantic annotation for categories such as active pressure, defensive driving and complex negotiation.

These are observed interaction labels. They are not multiple experimentally observed potential outcomes from the same real scene under different ego interventions.

### Reactivity evidence

Reported aggressive-ego evaluation:

```text
                     Yielding Compliance   False Collision
Log Replay                  0.0%              100.0%
Vista                      12.5%               87.5%
CausalDrive (“Polite”)     82.0%               18.0%
```

The model also supports:

```text
same initial scene + same ego trajectory
+ “Polite” vs “Aggressive” prompt
→ different surrounding-agent future
```

This is strong evidence for controllable alternative reactive synthesis.

It is not evidence that a particular real driver’s unobserved response has been identified.

Binding language:

```text
NO ORACLE FUTURE LAYOUT
+
ACTION-CONDITIONED GENERATION
+
SEMANTIC RESPONSE CONTROL

!=

COUNTERFACTUAL CAUSAL IDENTIFICATION
```

CausalDrive should therefore be classified as a real-time learned action-conditioned reactive visual simulator, not an unqualified “causally correct simulator.”

---

## 7. Five-anchor comparison

| axis | Bench2Drive | HUGSIM | ORION | ReactSim-Bench | CausalDrive |
|---|---|---|---|---|---|
| scientific object | E2E benchmark | reconstructed simulator | VLA planner | behavior-WM benchmark | learned visual WM |
| ego feedback | repeated CARLA loop | repeated simulated loop | inherits Bench2Drive | externally fixed deviated ego future | streaming action condition |
| sensor feedback | CARLA synthetic | reconstructed photorealistic | CARLA synthetic | not main target | generated video |
| surrounding behavior | scripted/adaptive | replay / IDM / attack | environment-provided | **learned model under test** | **learned inside visual WM** |
| learned behavior model required? | no | no | no | yes for evaluated simulator | yes |
| direct reactive metric? | policy outcome | simulator outcome | policy outcome | **yes, agent-response proxies** | YCR/FCR + system outcomes |
| alternative-action GT response? | simulator-defined | controller-defined | simulator-defined | **no real-world GT** | **no real-world GT** |
| strongest contribution | interactive skill evaluation | sensor-realistic loop | reasoning→action policy | reactivity measurement | real-time reactive generation |
| strongest boundary | synthetic/controller interaction | behavior model not human distribution | not a WM rollout | feasibility ≠ counterfactual truth | controllability ≠ causal identification |

---

## 8. What Wave 4 changes in interpretation of planning-centric WAMs

### C1 — evaluation realism is multi-dimensional

At minimum separate:

```text
sensor/view realism
physical dynamics realism
surrounding-agent state realism
behavioral response realism
policy feedback realism
```

One scalar label `closed-loop` hides these differences.

### C2 — simulator realism and policy quality are different scientific targets

Bench2Drive/ORION ask whether the policy succeeds in an interactive environment.
ReactSim asks whether the learned surrounding-agent simulator responds safely/feasibly.
CausalDrive additionally asks whether a visual WM can synthesize those responses while remaining controllable and fast.

A good policy score does not validate the simulator’s human-response distribution; a good simulator-reactivity score does not automatically prove planner improvement.

### C3 — action conditioning is only the first step toward behavioral validity

The required evidence ladder is:

```text
action affects generated future
→ other-agent behavior changes
→ response is learned rather than externally scripted
→ response remains safe/feasible under off-log ego behavior
→ response distribution is calibrated to real behavior
→ planner decisions improve because of that response model
```

Current anchors reach different rungs. They should not be collapsed.

### C4 — the key logged-data supervision boundary remains unresolved by architecture alone

Offline driving logs reveal one realized future under one realized ego behavior. They do not reveal all surrounding-agent outcomes for unexecuted ego actions.

ReactSim-Bench works around this for evaluation using feasibility/safety proxies.
CausalDrive expands learned alternative synthesis using semantic labels and synthetic hard cases.
Neither creates real alternative-action ground truth.

This is a structural evidence constraint, not a criticism unique to either paper.

### C5 — feedback bandwidth matters

ReactSim-Bench shows replan rate materially affects measured reactivity: more frequent replanning generally helps above ~1 Hz because the simulator observes realized ego behavior more often, but very frequent replanning can compound model error.

Therefore simulator update frequency belongs in the scientific protocol, not only the implementation appendix.

---

## 9. Historical placement after all four waves

Wave 4 does not support a simple story:

```text
open loop → closed loop → reactive WM → causal WM
```

The actual development is multi-dimensional:

```text
interactive prediction/planning
planning-specific evaluation
non-reactive real-data planning benchmarks
controllable visual world generation
future-model-assisted planning
world-action unification
latent imagination for policy learning
interactive CARLA policy benchmarks
photorealistic reconstructed simulators
VLA semantic reasoning policies
reactive behavior-WM evaluation
real-time learned reactive visual simulation
```

These branches overlap and solve different pieces of the overall planning problem.

---

## 10. Stable Wave-4 statements carried into field synthesis

```text
1. Closed-loop evaluation must be described by the feedback channels it closes, not by a binary label.

2. Photorealistic sensor feedback and behaviorally valid agent reaction are independent capabilities.

3. Strong closed-loop planning can improve through semantic/reasoning-action interfaces without explicit world rollout.

4. Log realism and reactive feasibility are distinct behavior-simulator properties.

5. Reactive feasibility is still weaker than validated counterfactual behavioral truth.

6. Removing oracle future NPC layouts is necessary for learned reactive prediction but does not identify the true response function.

7. Learned reactive visual simulation is now an operational capability, including planner-in-loop / RL / human-in-loop use, but real alternative-action behavioral ground truth remains unavailable in ordinary logs.
```

No research gap is declared.

---

## 11. Wave-4 closeout verdict

```text
Bench2Drive       COMPLETE
HUGSIM            COMPLETE
ORION             COMPLETE
ReactSim-Bench    COMPLETE
CausalDrive       COMPLETE
Wave 4            CLOSED
```

The four-wave anchor program is now sufficient to enter **Phase C — full field synthesis** under the existing research principles.
