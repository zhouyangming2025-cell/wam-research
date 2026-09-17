# Living first-principles audit — Set D continuation

Status: living research memory; records why judgments changed. This file does not amend ontology.

---

## 47. Why Set D was chosen

After Sets A–C, a recurring temptation remained: papers that generate or model world and action together looked like they might form a coherent “joint world-action” route.

That temptation was strengthened by earlier ontology labels such as `RJ`, `W5`, and `C5`.

The methodological risk was obvious: `joint` might be another word like `future`, `candidate`, or `coupling`—a surface similarity that hides several different scientific mechanisms.

Set D therefore froze five papers **before** comparative interpretation:

- OccWorld
- DrivingGPT
- GenAD
- Gen-Drive
- Discrete-WAM

The audit rule was: reconstruct each independently before asking whether “jointness” is shared.

---

## 48. First correction: “joint” does not identify the joint variable

Deep reading immediately showed that the five papers do not even join the same objects.

OccWorld:

```text
joint variable ≈ next occupancy-world state
               = scene tokens + ego-motion token
```

DrivingGPT:

```text
joint object ≈ one interleaved multimodal token language
             z1,q1,z2,q2,...
```

GenAD:

```text
joint object ≈ ego + surrounding-agent future trajectories
             in a structural trajectory latent space
```

Gen-Drive:

```text
joint object ≈ generated multi-agent social future scenario
```

Discrete-WAM:

```text
jointness ≈ shared discrete world/action representation
          + a world-policy co-modeling task
          among several task modes
```

Thus the phrase `joint world-action` was already too lossy before deployment or commitment was considered.

---

## 49. Second correction: joint representation is not joint inference

Discrete-WAM exposed a particularly important error mode.

The paper genuinely has a world-policy task that jointly models future visual and action tokens. But it also has a distinct policy task:

```text
context → high-level decision → future action tokens
```

and the final downstream planner is emphasized as hierarchical decision prediction plus confidence-guided parallel action-token editing.

Therefore:

> A paper can use joint world/action generation as a training program without the final deployed planner being reducible to “joint world-action emission”.

This is direct pressure on any ontology that infers deployment topology from the existence of a joint training mode.

---

## 50. Third correction: joint generation can still have very different commitment mechanisms

GenAD and Gen-Drive are a useful matched contrast.

Both generate ego together with surrounding-agent futures.

But GenAD uses the generated ego future itself as the plan:

```text
sample latent future → generate ego+agents → ego trajectory
```

Gen-Drive instead makes evaluation a central planning stage:

```text
generate several ego+agent futures
→ learned reward model
→ select future
→ commit its ego trajectory
```

Thus even when the generated future object is similar, final decision logic can differ in a scientifically central way.

This reinforces a lesson from Set A: evaluator semantics/structure are not globally a headline axis, but in some papers the evaluator is part of the paper's defining mechanism and cannot be dismissed as a cosmetic profile.

---

## 51. Fourth correction: shared sequence modeling still has factorization

DrivingGPT initially looks like the cleanest example of “world and action generated together”.

But the actual model is an autoregressive sequence:

```text
z1 → q1 → z2 → q2 → ...
```

under causal next-token prediction.

So “joint” at the sequence level does not mean simultaneous or symmetric causal dependence at each step.

Discrete-WAM makes this even clearer: its world-policy factorization explicitly predicts the current action token before the corresponding future visual token.

Therefore future audits must record **factorization/order**, not just whether variables share a model.

---

## 52. Fifth correction: OccWorld's ego is part of the modeled world state

OccWorld is different again.

Its ego token is not merely an action conditioning input. Scene tokens and ego token together form the tokenized state whose next step is autoregressively predicted.

The paper's ablation is unusually useful: weakening/removing ego temporal modeling harms occupancy forecasting as well as planning.

This supports the interpretation that ego evolution is structurally part of the learned world dynamics rather than a separate output head attached for convenience.

---

## 53. Current status of old `RJ/W5` thinking

Do not delete or edit historical ontology yet.

But the old compression:

```text
joint world-action carrier
```

must now be treated as **under-defined** for research-route reconstruction.

At minimum, a future legitimate use of “joint” would need to specify:

1. joint variables;
2. shared representation or state space;
3. prediction factorization/order;
4. training vs deployment lifecycle;
5. whether world prediction is actually executed during final planning;
6. whether the generated joint object is directly committed or subsequently evaluated/selected.

Without these, “joint” risks repeating the same mistake as the earlier R/W/E axes: compressing scientifically different mechanisms because they share one visible property.

---

## 54. Methodological update from Set D

The paper-first protocol gains one additional rule:

> **Surface-unification words are audit triggers, not categories.**

Words such as:

- joint
- unified
- generative
- world-policy
- world-action
- future-aware

should trigger decomposition questions rather than immediate family assignment.

The correct response to a paper saying “joint world-action modeling” is now:

```text
What is joint?
At what lifecycle stage?
With what factorization?
What remains online?
How is final action committed?
What disappears under the core deletion test?
```

Only after those answers are known should cross-paper similarity be discussed.

---

## 55. Set D does not create a new route

The strongest Set D result is deliberately negative:

> There is currently insufficient basis for a generic `Joint` CoreRoute.

The five papers share a high-level aspiration to reduce the separation between world understanding and action generation, but their concrete mechanisms differ too much to justify collapsing them at this stage.

This is a useful outcome. The purpose of paper-first reconstruction is not to force every set to yield a category; it is to stop weak similarities from becoming ontology.

Detailed evidence reconstruction is in:

`20_PAPER_FIRST_RECONSTRUCTION_SET_D.md`
