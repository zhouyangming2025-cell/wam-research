# PHASE_B_WAVE4_REACTSIMBENCH_AUDIT

Last updated: 2026-09-14

Status: **COMPLETE**

Paper: `ReactSim-Bench: Benchmarking Reactive Behavior World Model Simulation in Autonomous Driving`

Role in Wave 4: **behavior-world-model reactivity benchmark**, not a new planner or simulator architecture by itself.

---

## 1. Executive verdict

ReactSim-Bench makes a genuinely useful methodological move:

```text
AV control is externalized and deliberately deviated from the log
→ surrounding-agent simulator must respond to the realized AV behavior
→ response is evaluated for safety / rule compliance / kinematic feasibility
```

This is stricter than realism benchmarks such as WOSAC, where the same simulator controls both AV and surrounding agents and is mainly rewarded for log-likeness.

But the benchmark does **not** possess ground-truth surrounding-agent futures for those unexecuted deviated AV behaviors.

Therefore its strongest scientific claim is:

```text
REACTIVE FEASIBILITY / ROBUSTNESS UNDER EGO DEVIATION
```

not:

```text
IDENTIFIED COUNTERFACTUAL HUMAN RESPONSE TRUTH.
```

This distinction is central.

---

## 2. Exact task formulation

A logged scenario provides:

```text
HD map M
logged AV + agent history
logged future
```

ReactSim-Bench then replaces the future AV behavior with a fixed, externally supplied deviated AV trajectory:

```text
S_deviated_AV[0:T]
```

At rollout step t:

```text
AV next state
= fixed external deviated trajectory state

surrounding-agent next state
= q(map,
    logged history,
    realized deviated AV states so far,
    simulated surrounding-agent states so far)
```

The key causal-interface change relative to WOSAC is:

```text
AV is NOT controlled by q.
```

The world-agent model cannot jointly choose an ego trajectory that makes its own agent predictions easy or collision-free. It must absorb an external ego behavior and react.

This is a meaningful simulation-interface advance.

---

## 3. Why WOSAC/log-realism is not sufficient for this question

The paper contrasts two protocols.

### Realism-style joint simulation

```text
q controls AV + surrounding agents
→ rollout judged by similarity to logged driving
```

If all agents including AV stay near the log, a model can perform well without being stress-tested by externally imposed ego deviation.

### ReactSim protocol

```text
external AV behavior differs from log
q controls only surrounding agents
→ q must adapt to realized AV behavior
```

This changes the distribution seen by the simulator and removes the ability to coordinate the ego prediction with its own world-agent rollout.

Hence:

```text
LOG REALISM != REACTIVE ROBUSTNESS
```

is directly testable here.

---

## 4. Where the deviated AV behaviors come from

The benchmark does not arbitrarily inject physically impossible ego trajectories.

The paper constructs candidate AV behaviors with an AV planner, then filters them with rules and manual verification to retain behaviors that:

```text
- differ materially from the logged AV future;
- remain kinematically feasible;
- create meaningful pressure requiring surrounding-agent response.
```

Final test set:

```text
2,636 scenarios total
937 longitudinal deviations
799 directional deviations
900 lateral deviations
```

Each scenario contains:

```text
1 s history
8 s future rollout
10 Hz sampling
up to 64 total agents in the unified cache
```

This is a targeted stress set, not a generic random perturbation set.

---

## 5. Reactive pressure is directly demonstrated

A particularly strong benchmark-design check is to pair the deviated AV with **logged surrounding-agent replay**.

Result:

```text
≥1 AV-agent collision in 83.46% of scenarios
minimum TTC < 0.5 s in 98.14% of scenarios
```

So the selected AV trajectories genuinely invalidate simple surrounding-agent log replay in most cases.

This verifies:

```text
the benchmark creates conditions where a surrounding-agent response is necessary for a safe/feasible rollout.
```

It does **not** say what exact real-human response would occur.

---

## 6. Metrics: what is actually measured

The benchmark measures whether generated surrounding behavior is safe and feasible under the deviated ego.

Reported dimensions include:

```text
Agent–AV collision count
Agent–AV risky-TTC count
Agent–Agent collision
Off-road rate
Driving-direction violations
Acceleration infeasibility
Steering/curvature infeasibility
```

The Agent–AV collision metric includes a fault-assignment rule rather than counting every geometric overlap indiscriminately.

This is a practical reactive-simulation scorecard.

However these metrics are **constraint/proxy metrics**. They do not compare the simulated surrounding trajectory against a true alternative-world trajectory because that trajectory was never observed.

Thus:

```text
safe + feasible response
!=
verified true counterfactual response.
```

---

## 7. Main results: learned models do react beyond log replay

At 2 Hz replanning, representative results are:

```text
                        A-AV collision   risky TTC
Log Replay                  0.9829        1.5380
MTR                         0.1457        0.5819
CTG                         0.6195        0.9476
VBD                         0.2276        0.4711
SMART                       0.1419        0.3976
CATK                        0.1426        0.4029
TrajTok                     0.1407        0.4173
```

The exact best model depends on metric; no architecture dominates all safety/map/kinematic dimensions.

The important field result is simpler:

```text
learned world-agent models substantially outperform fixed log replay under ego deviation,
so some reactive capability can emerge from learned behavior models even when training is predominantly log-based.
```

This is a useful counterweight to overly strong claims that logged-data training cannot produce any useful reactivity.

---

## 8. Realism and reactivity can disagree

The paper directly compares realism and reactive protocols.

Example:

```text
MTR realism ADE        2.5498
CTG realism ADE        1.9405  (better realism)

MTR reactive collision 0.1457
CTG reactive collision 0.6195  (much worse reactivity)
```

Likewise, CATK slightly improves realism over SMART but is slightly worse on the shown reactive collision/risky-TTC metrics.

Therefore the paper provides direct experimental evidence that:

```text
better log-likeness / realism metrics
!=
better behavior under an externally deviated AV.
```

This is analogous to the planning-side result:

```text
prediction fidelity != decision utility.
```

but it applies to behavior simulators:

```text
realism fidelity != reactive validity.
```

Do not upgrade this into a claim that realism is irrelevant; both dimensions matter.

---

## 9. Replanning frequency is part of the simulator behavior

ReactSim-Bench finds that higher replanning rates, generally above 1 Hz, improve reactive capability because the world-agent model observes the newly realized AV behavior more frequently.

However the relation is not perfectly monotonic because frequent replanning can also compound model errors.

The paper contrasts this with WOSAC-style realism evaluation, where lower replanning frequency can sometimes improve realism by reducing autoregressive accumulation when the model controls all agents.

Thus:

```text
replanning frequency is not merely an engineering hyperparameter;
it changes the effective feedback bandwidth between ego intervention and simulated response.
```

This becomes important when comparing reactive simulators.

---

## 10. The benchmark does not contain alternative-action ground truth

This is the strongest evidence boundary.

For the deviated AV trajectory, the real log contains only the surrounding-agent behavior that occurred under the original logged AV trajectory.

Therefore ReactSim-Bench cannot directly ask:

```text
Did this exact surrounding agent brake 1.8 m/s² in the real world
when the ego performed this unexecuted deviation?
```

Instead it asks:

```text
Did the simulated surrounding response remain safe, rule-compliant and kinematically plausible
under a deviation that makes log replay unsafe?
```

Formal distinction:

```text
REACTIVE FEASIBILITY
!=
COUNTERFACTUAL BEHAVIORAL TRUTH
```

The benchmark substantially improves evaluation of the former while leaving the latter fundamentally unobserved in logged data.

---

## 11. Relation to historical interaction work

ReactSim-Bench should not be narrated as inventing the concept that agent behavior depends on ego behavior.

Historical predecessors already include:

```text
M2I       conditional reactor prediction
GameFormer iterative interactive prediction/planning
What Truly Matters interactive task-driven prediction evaluation
```

ReactSim-Bench’s more specific contribution is evaluation protocol:

```text
force ego off the logged path
+ decouple ego from the world-agent simulator
+ quantitatively stress surrounding-agent response.
```

That is a narrower and more defensible historical placement.

---

## 12. Relation to Bench2Drive and HUGSIM

### Bench2Drive

```text
interactive actors exist through CARLA/ScenarioRunner controllers
but benchmark target is policy capability, not learned-agent behavioral fidelity.
```

### HUGSIM

```text
IDM/aggressive actors can react to ego
but reactions are hand-designed / optimization-based controllers.
```

### ReactSim-Bench

```text
target of evaluation is specifically the learned behavior simulator's response to ego deviation.
```

So it fills a measurement role not provided by the first two anchors.

---

## 13. What ReactSim-Bench proves / does not prove

### Strongest direct evidence

```text
- fixed log replay becomes unsafe for most selected ego deviations;
- learned behavior models reduce those failures substantially;
- realism ranking and reactive ranking can disagree;
- feedback/replan rate materially affects measured reactivity.
```

### What it proves

```text
Reactive capability is an independent behavior-simulation evaluation dimension that is not captured by log-realism metrics alone.
```

### What it does not prove

```text
- any tested model learns the true causal human response distribution;
- collision avoidance alone implies realistic social behavior;
- generated alternative futures are ground-truth counterfactuals;
- better reactive benchmark score necessarily improves a downstream planner.
```

The last point is especially important: ReactSim-Bench evaluates the simulator, not matched planner regret/orderings induced by simulator quality.

---

## 14. Stable Wave-4 distinction introduced

```text
REALISM / LOG-LIKENESS
!=
REACTIVE FEASIBILITY
!=
COUNTERFACTUAL BEHAVIORAL TRUTH
```

This three-way separation is now required for CausalDrive and later field synthesis.

## Verdict

```text
ReactSim-Bench deep read = COMPLETE
role = measurement benchmark for learned world-agent reactivity under external ego deviation
```

No research gap is declared.
