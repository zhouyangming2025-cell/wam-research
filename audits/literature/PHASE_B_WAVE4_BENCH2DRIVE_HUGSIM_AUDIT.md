# PHASE_B_WAVE4_BENCH2DRIVE_HUGSIM_AUDIT

Last updated: 2026-09-14

Status: **FIRST WAVE-4 COMPARATIVE BLOCK COMPLETE**

Sources:

```text
P0033 Bench2Drive canonical raw primary text
Thinklab-SJTU/Bench2Drive public source tree, pinned observed commit 7ec25d1c9f7522d923ce5f3420986cef1cb2d956
P0034 HUGSIM canonical raw primary text
HUGSIM public project/repository for implementation availability context
```

Purpose: establish what “closed loop”, “interactive”, “sensor realism”, and “actor reactivity” mean before auditing modern reactive world models.

---

## 1. Executive conclusion

Bench2Drive and HUGSIM are both legitimately closed-loop, but they close different realism gaps.

```text
Bench2Drive
= CARLA game-engine closed-loop E2E policy benchmark
+ synthetic sensor feedback
+ CARLA physics
+ many scripted/adaptive interactive scenario actors
+ standardized short-route multi-ability evaluation

HUGSIM
= reconstructed-real-scene photorealistic closed-loop simulator
+ ego-pose-dependent novel-view RGB feedback
+ reconstructed/inserted actors
+ replay / IDM / optimization-based aggressive actor controllers
+ real-time 3DGS rendering
```

Therefore:

```text
CLOSED LOOP != one property
```

At minimum we need to ask separately whether the loop closes over:

```text
ego dynamics
sensor observations
surrounding-agent states
surrounding-agent behavior
```

Both benchmarks close ego and sensor feedback. Both can include surrounding-agent interaction. But the source of actor behavior is different and neither benchmark, by itself, establishes that simulated reactions are statistically faithful counterfactual responses of real human drivers.

---

# 2. Bench2Drive

## 2.1 What problem does it solve?

Bench2Drive attacks two evaluation problems that were already visible before modern WAM:

```text
open-loop L2/collision metrics do not reliably represent driving quality;
long CARLA routes + exponentially compounded penalties produce noisy/coarse system comparisons.
```

It changes the evaluation unit from long mixed-scenario routes to short, scenario-isolated routes.

Primary benchmark design:

```text
44 interactive scenarios
5 routes per scenario
220 evaluation routes
~150 m per route
one main scenario per route
```

The official training corpus contains roughly two million annotated frames collected from 13,638 clips, with broad scenario/weather/town coverage.

The benchmark is therefore best understood as:

```text
closed-loop + scenario-disentangled + standardized-training-data E2E evaluation
```

rather than as a world-model benchmark.

## 2.2 What exactly is closed?

The paper explicitly states that the AD system’s actions directly influence the environment. Operationally:

```text
current CARLA world
→ render current sensors to policy
→ policy produces its driving output / control path
→ ego executes in CARLA physics
→ world advances
→ next sensors are rendered from the new ego/environment state
→ repeat
```

Thus ego deviation changes future observations. This is a genuine sequential policy loop, unlike NAVSIM’s one-shot non-reactive pseudo-simulation.

## 2.3 Sensor feedback

The official training/evaluation ecosystem supports raw simulated sensors. The paper lists:

```text
6 cameras
1 LiDAR
5 radars
IMU/GNSS
plus HD-map/debug signals in the dataset/tooling
```

Different E2E baselines consume different permitted subsets. The next sensor observation comes from the CARLA world after the ego has moved.

Therefore:

```text
sensor feedback = YES
photorealistic real-world sensor reconstruction = NO
```

It is CARLA/game-engine visual realism, not reconstructed-real-scene photorealism.

## 2.4 Surrounding-agent feedback is not uniform across all scenarios

It would be wrong to compress Bench2Drive into either:

```text
“all traffic is fixed replay”
or
“all traffic is fully reactive learned behavior.”
```

The benchmark inherits/extends CARLA ScenarioRunner behavior trees and scenario-specific actor controllers.

A source-code spot check gives a concrete example. In `YieldToEmergencyVehicle`, the emergency vehicle uses:

```text
AdaptiveConstantVelocityAgentBehavior(
    emergency_vehicle,
    ego_vehicle,
    ...
)
```

and trigger/end conditions explicitly depend on ego-relative distance and whether the emergency vehicle has moved in front of ego.

So at least some scenario actors are behaviorally conditioned on the ego state during the rollout.

However this is:

```text
scripted / controller-based interaction
```

not:

```text
learned real-driver response distribution
or identified counterfactual human behavior.
```

This distinction will matter when ReactSim-Bench/CausalDrive claim “reactivity”.

## 2.5 Metrics and why they matter

Bench2Drive uses:

```text
Success Rate (SR)
= fraction of routes completed without rule infractions

Driving Score (DS)
= route completion with CARLA-style infraction penalties
```

and additionally reports efficiency, comfort/smoothness, and skill-group scores such as merging, overtaking, emergency braking, give-way, and traffic-sign behavior.

A useful paper-level demonstration of open-loop/closed-loop mismatch is:

```text
UniAD-Base open-loop L2 = 0.73
VAD        open-loop L2 = 0.91

but closed-loop:
UniAD-Base DS = 45.81 / SR = 16.36%
VAD        DS = 42.35 / SR = 15.00%
```

The exact ordering in this example is not itself dramatic; the broader table shows models with similar or reasonable imitation fit can have materially different closed-loop skills. Bench2Drive’s stronger contribution is evaluation structure, not one isolated ranking reversal.

## 2.6 What Bench2Drive proves / does not prove

**Strongly supports:**

```text
repeated policy-environment interaction matters for E2E evaluation;
scenario-isolated short routes expose skill-specific failures;
open-loop trajectory fit is insufficient as the sole planning metric;
synthetic closed-loop environments can provide standardized algorithm-level comparison.
```

**Does not establish:**

```text
CARLA appearance matches real camera distribution;
scenario actor reactions match real-driver conditional behavior distributions;
a learned world model has correct counterfactual dynamics;
any one WM architecture is necessary for strong closed-loop driving.
```

---

# 3. HUGSIM

## 3.1 What problem does it solve?

HUGSIM starts from a different weakness of conventional simulators:

```text
game-engine closed loop is interactive,
but its rendered sensor distribution has a substantial real-world domain gap.
```

It reconstructs captured real driving scenes with 3D Gaussian Splatting and extends reconstruction into a simulator that can render from ego poses not present in the original log.

This makes its primary contribution:

```text
real-scene reconstruction
+ extrapolated-view rendering
+ real-time closed-loop sensor feedback
```

rather than simply “another planning benchmark.”

## 3.2 Exact ego loop

The paper gives a concrete loop:

```text
reconstructed world state
→ render RGB / supported modalities at current ego pose
→ AD algorithm predicts future waypoints
→ LQR converts waypoints to control
→ ego pose is updated
→ actor states are updated
→ next observation rendered from updated state
→ repeat
```

So HUGSIM closes both:

```text
ego dynamics feedback
sensor-viewpoint feedback
```

The latter is precisely what log replay and NAVSIM cannot provide after ego deviates from the recorded path.

## 3.3 Photorealism target

The rendering model addresses simulator-specific view problems:

```text
extrapolated views beyond logged camera trajectory
lane/ground distortion
360° rendering of movable actors
continuous trajectories from discrete observations
```

The paper reports roughly `89.15 FPS` rendering in the cited reconstruction comparison on RTX 3090, supporting its real-time objective.

This is genuine evidence for visual/sensor simulation efficiency and reconstruction quality.

It is **not** evidence that surrounding-agent behavior is realistic.

## 3.4 HUGSIM has three different actor-behavior regimes

This is the most important scientific detail for Wave 4.

### Replayed actors

Native actors may follow reconstructed logged trajectories.

The paper explicitly states:

```text
replayed driving behavior does NOT interact with the ego vehicle.
```

So those scenarios close ego/sensor feedback but not traffic behavioral feedback.

### Normal actors

On nuScenes, HUGSIM uses IDM with HD maps; the paper states IDM actors can yield to ego. On other datasets without paired HD maps it uses a simpler predefined-direction / constant-speed alternative.

Thus:

```text
some normal actors are ego-responsive,
but response comes from a hand-designed IDM controller.
```

### Aggressive actors

Hard/extreme scenarios use an optimization-based attack planner. Candidate actor trajectories are generated and scored to approach/attack ego while avoiding other actors. The cost explicitly depends on predicted ego future trajectory.

The paper further states hard/extreme configurations can increase replanning frequency.

Therefore aggressive actors are genuinely policy-dependent/interactively replanned in the simulator.

But again:

```text
reactive = YES in the control-loop sense
real-human behavioral validity = NOT ESTABLISHED
```

The actor is intentionally adversarial, not a learned estimate of what a human NPC would have done under the same ego intervention.

## 3.5 Difficulty levels are also feedback regimes

HUGSIM’s four levels are not merely visual difficulty:

```text
Easy:
mostly static or replayed actors
→ little/no behavioral interaction

Medium:
IDM / constant-speed normal actors
→ limited controller-defined interaction

Hard:
aggressive attack actors
→ ego-dependent adversarial interaction

Extreme:
more aggressive actors / more frequent replanning / more aggressive candidate selection
→ stronger ego-dependent adversarial interaction
```

Hence an aggregate HUGSIM score mixes qualitatively different traffic-response mechanisms unless difficulty is reported separately.

## 3.6 Planner evaluation

The paper evaluates image-based planners including UniAD, VAD and image-only Latent TransFuser through a Gymnasium interface. Their planned waypoints are sent back to the simulator.

HD-Score combines:

```text
NC
DAC
TTC
COM
route completion Rc
```

and the reported results degrade strongly from easy → extreme, showing that the benchmark actually stresses the policies under increasingly hostile interaction conditions.

This is planner-in-simulator evidence, not only rendering evaluation.

## 3.7 What HUGSIM proves / does not prove

**Strongly supports:**

```text
real captured scenes can be reconstructed into a practical closed-loop vision simulator;
ego deviations can produce new photorealistic observations rather than replayed cameras;
interactive actor controllers can be layered onto the reconstructed scene;
planning methods can be evaluated sequentially inside that environment.
```

**Does not establish:**

```text
IDM / attack-planner responses are statistically faithful real-human counterfactual responses;
higher PSNR/KID or photorealism necessarily produces better planner ranking;
all HUGSIM scenarios are behaviorally reactive;
reconstructed appearance removes all real-to-simulation gap.
```

---

# 4. Bench2Drive ↔ HUGSIM comparison

| axis | Bench2Drive | HUGSIM |
|---|---|---|
| base world | CARLA synthetic game-engine maps/assets | reconstructed real captured scenes via 3DGS |
| ego feedback | **yes** | **yes** |
| next sensor depends on ego pose | **yes** | **yes** |
| sensor realism target | synthetic E2E sensor simulation | photorealistic real-scene novel-view rendering |
| surrounding-agent mechanisms | CARLA/ScenarioRunner scripted & adaptive scenario controllers | replay, IDM/constant-speed, optimization-based aggressive planner |
| surrounding-agent feedback | **scenario dependent; yes for some adaptive controllers** | **regime dependent; none for replay, limited/yes for IDM, explicit for attack planner** |
| learned human behavior model | no | no |
| alternative-action GT | no | no |
| explicit behavioral-fidelity-to-real-reaction validation | not the benchmark target | not established as a real-human reaction benchmark |
| planner evaluated sequentially | **yes** | **yes** |
| primary scientific strength | standardized granular interactive policy evaluation | photorealistic sensor-feedback simulation on reconstructed real scenes |
| principal realism limitation | game-engine visual/domain gap | actor response realism is controller-designed; reconstruction/view extrapolation remains imperfect |

---

# 5. Exact replacement sentences for “closed loop”

### Bench2Drive

> The ego policy repeatedly acts in CARLA; ego actions update CARLA physics and future sensor observations, while scenario actors follow CARLA/ScenarioRunner controllers that can be scripted or ego-adaptive depending on the scenario.

### HUGSIM

> The image-based planner repeatedly outputs waypoints in a reconstructed 3DGS scene; LQR updates ego pose and the next rendered observation, while surrounding actors follow one of replayed, IDM/constant-speed, or ego-dependent aggressive-planning behavior regimes.

These sentences are more scientifically useful than calling both simply “closed-loop”.

---

# 6. New Wave-4 field distinction

The first block establishes a four-axis feedback decomposition:

```text
F_e = ego-state feedback
F_s = sensor/view feedback
F_a = surrounding-agent state feedback
F_b = surrounding-agent behavioral-response feedback
```

Then:

```text
NAVSIM:
F_e ≈ short simulated ego trajectory scoring, but no repeated sensor-policy loop
F_s = no
F_b = no

Bench2Drive:
F_e = yes
F_s = yes (synthetic CARLA sensors)
F_a = yes
F_b = scenario-dependent scripted/adaptive

HUGSIM:
F_e = yes
F_s = yes (photorealistic reconstructed scene)
F_a = yes
F_b = regime-dependent: no for replay / controller-reactive for IDM & attack
```

This decomposition should replace the binary `open-loop vs closed-loop` shorthand throughout later synthesis.

---

# 7. Consequence for ReactSim-Bench / CausalDrive

The bar is now clearer.

A modern reactive world model cannot claim a fundamentally new capability merely because:

```text
ego action changes the next simulated frame
```

because existing simulators already close ego/sensor loops and can contain ego-responsive traffic controllers.

The scientifically harder questions are:

```text
1. Is the OTHER-AGENT response distribution learned rather than manually scripted?
2. Is it conditioned on the ego intervention?
3. Is the response episode-consistent with the observed history?
4. Is behavioral correctness evaluated, not just visual plausibility?
5. Against what reference can an unexecuted alternative response be judged?
6. Does better reaction modeling actually change planner performance/orderings?
```

These questions should organize the ReactSim-Bench and CausalDrive audits, without turning them into a preselected gap hypothesis.

---

## Verdict

```text
Bench2Drive deep read = COMPLETE
HUGSIM deep read      = COMPLETE
first Wave-4 block    = COMPLETE
```

No research gap is declared.
