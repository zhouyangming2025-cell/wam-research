# WAM Dimension Ontology V1.1 Amendment — SeerDrive

Last updated: 2026-09-15

Status: **STABLE MINOR AMENDMENT — three dimensions survive back-projection**

Base ontology:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
```

Trigger paper:

```text
P0061 SeerDrive
```

This amendment follows the V1 extension rule: fill V1 first, isolate residue, merge anything already expressible, then back-project surviving additions onto earlier anchors.

---

# 1. Candidate residues tested

SeerDrive initially exposed five candidate additions:

```text
inference iteration semantics
planner→world feedback carrier
mutual-refinement topology
per-iteration supervision
refinement-depth saturation
```

After merge testing:

```text
mutual-refinement topology
→ already expressible by J04 Causal coupling direction

refinement-depth saturation
→ already expressible by N06 Quality–latency / scale operating curve
```

These are NOT added as duplicate dimensions.

Three residues survive.

---

# 2. New stable dimensions

## J08 — Inference iteration semantics

**Scientific question**

When a paper says the model/planner “iterates,” what scientific state advances in one iteration?

**Why it matters**

The word `iteration` currently conflates fundamentally different processes:

```text
physical future-time transition
internal world↔planner feature refinement
candidate search / optimization depth
diffusion / flow denoising step
autoregressive generated-observation step
external environment execution-feedback step
```

Treating them as one notion can falsely upgrade internal neural refinement into temporal rollout or closed-loop interaction.

**Typical values**

```text
NONE / one-shot
PHYSICAL-TIME LATENT ROLLOUT
AUTOREGRESSIVE OBSERVATION ROLLOUT
INTERNAL WORLD↔PLANNER CO-REFINEMENT
GENERATIVE DENOISING ITERATION
SEARCH / OPTIMIZATION ITERATION
ENVIRONMENT EXECUTION-FEEDBACK ITERATION
HYBRID
```

**Evidence required**

Trace the tensors between two consecutive iterations. Identify whether time index changes, environment observation changes, action is executed, or only hidden features are updated.

**Common trap**

```text
N internal refinement passes
!=
N future timesteps
!=
N closed-loop environment interactions
```

**SeerDrive**

```text
INTERNAL WORLD↔PLANNER CO-REFINEMENT
```

The same final-horizon future BEV is repeatedly reconsidered as the ego/planning feature is refined.

---

## J09 — Planner→world feedback carrier

**Scientific question**

When planning influences world prediction, what exact object is fed back?

**Why it matters**

`planner→world` can mean very different causal interfaces:

```text
executed low-level action
candidate trajectory
ego state / pose
planner hidden feature / query
mode/intention token
selected policy action
new environment observation
```

A hidden planner feature should not be described as equivalent to an executed intervention.

**Typical values**

```text
NONE
EXPERT/LOGGED ACTION
PREDICTED/CANDIDATE TRAJECTORY
EGO STATE / POSE
PLANNER HIDDEN FEATURE / QUERY
INTENTION / MODE TOKEN
EXECUTED CONTROL
NEW OBSERVATION AFTER EXECUTION
HYBRID
```

**Evidence required**

Identify the precise numerical tensor/object entering the world/dynamics model from the planning side at inference.

**Common trap**

Calling any planning-conditioned future `closed-loop environment interaction` without checking whether the feedback carrier is a real executed action or merely an internal representation.

**SeerDrive**

```text
PLANNER HIDDEN FEATURE / EGO-MODE FEATURE
```

The refined current ego feature is fed back into the BEV world model.

---

## L07 — Iterative-state supervision coverage

**Scientific question**

When a model contains recurrent/refinement iterations, which intermediate states are directly supervised during training?

**Why it matters**

Two architectures with the same inference loop may learn very differently if:

```text
only final state receives loss
vs
all intermediate states receive losses
```

Intermediate supervision can itself explain convergence or planning gains and changes gradient flow through the loop.

**Typical values**

```text
NOT APPLICABLE
FINAL ITERATION ONLY
ALL ITERATIONS
SELECTED ITERATIONS
SELF-CONSISTENCY ONLY
MIXED
NOT REPORTED
```

**Evidence required**

Trace loss attachment to iteration-indexed world/planner outputs.

**SeerDrive**

```text
ALL ITERATIONS
```

The paper states that each iteration's predicted future semantic map and ego trajectories are supervised.

---

# 3. Back-projection onto ontology anchors

| Paper | J08 Inference iteration semantics | J09 Planner→world feedback carrier | L07 Iterative-state supervision |
|---|---|---|---|
| **LAW** | NONE / one-shot future-latent auxiliary prediction | planner's predicted waypoint trajectory conditions WM once; no iterative online feedback | NOT APPLICABLE |
| **WoTE** | **PHYSICAL-TIME LATENT ROLLOUT**: recurrent future BEV/state-action transitions | candidate/action embedding enters world transition; reward/planner does not repeatedly co-refine same decision state | future-state/reward supervision belongs to temporal rollout; no SeerDrive-style internal refinement loop |
| **Epona** | planning: generative denoising iterations; simulation: **AUTOREGRESSIVE OBSERVATION ROLLOUT**; no world↔planner co-refinement | predicted/external action conditions VisDiT; no visual-future→planner→world repeated feedback | NOT APPLICABLE to world↔planner refinement; visual Chain-of-Forward has separate rollout training semantics |
| **WorldDrive** | NONE for internal co-refinement; heavy diffusion teacher sampling only during training, lightweight one-pass surrogate at deployment | candidate trajectory embedding conditions teacher/student future models; no iterative planner-hidden feedback | NOT APPLICABLE |
| **World4Drive** | NONE / one-pass candidate endpoint latent prediction and ScoreNet selection | candidate trajectory/action token conditions future predictor | NOT APPLICABLE |
| **SeerDrive** | **INTERNAL WORLD↔PLANNER CO-REFINEMENT** | **refined ego/planner hidden feature** | **ALL ITERATIONS** |

This back-projection confirms that the additions are cross-paper scientific axes rather than SeerDrive-specific module names.

---

# 4. Why the amendment matters

Before SeerDrive, the matrix could distinguish:

```text
action→world
world→action
bidirectional
```

but it could still blur the *meaning of repetition*.

V1.1 now distinguishes:

```text
WoTE:
iteration advances physical predicted time

Epona:
iteration may be denoising or autoregressive generated observation time

SeerDrive:
iteration advances internal planner/world representation refinement

closed-loop simulator:
iteration advances the real/simulated environment after execution
```

This is a scientifically important distinction for planning-centric WAM because all four can be casually described as “iterative world model reasoning” while implying very different capabilities.

---

# 5. Version rule

Until a fully consolidated `WAM_DIMENSION_ONTOLOGY_V1_1.md` is generated, use:

```text
WAM_DIMENSION_ONTOLOGY_V1.md
+
WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
```

as the canonical coordinate system.

Do not silently alter the meaning of existing V1 IDs.
