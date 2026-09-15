# Phase C.6 RiskWorld Audit

Last updated: 2026-09-15

Status: **COMPLETE FIRST PASS — PAPER VERIFIED; SOURCE BLOCKED / MONITOR**

Paper:

```text
RiskWorld: Object-Centric Latent World Modeling for Autonomous Driving Risk Identification
arXiv:2608.21414v1
submitted 2026-08-12
```

Canonical deep read:

```text
papers/deep_analysis/P0005_RISKWORLD_DEEP_ANALYSIS_V2.md
```

---

# 1. Stable mechanism judgment

RiskWorld is a task-oriented object-centric latent world model for **risk-source identification**, not an integrated planner.

Core inference graph:

```text
observed 16-frame RGB history
+ object tracks / boxes
+ ego-motion history
→ frozen V-JEPA2 global + object-aligned features
→ structured ego/object state encoder
→ relation attention
→ one relation-aware token per observed object
→ object-wise RSSM-style 60-step / 3 s future rollout
→ future relative position / distance / temporal-risk curve
→ pooled object-risk score
→ identify risky object(s)
```

Canonical subtype:

```text
OBJECT-CENTRIC FACTUAL-RELATION ROLLOUT RISK WORLD MODEL
```

---

# 2. Source/version boundary

In-repo raw paper:

```text
papers/raw_md/P0005_RiskWorld/P0005_RiskWorld.raw.md
```

Public source:

```text
arXiv:2608.21414v1
```

No attributable official implementation was identified in this audit.

False-positive guard:

```text
KevinWjk/RiskWorld
```

is unrelated: the repository README is an Alpamayo 1.5 autonomous-driving release. It MUST NOT be attached to the RiskWorld paper.

Final source label:

```text
PAPER-COMPLETE
SOURCE-BLOCKED / MONITOR
```

---

# 3. Risk semantics audit

RiskWorld predicts risk explicitly rather than computing it only after motion prediction.

Two outputs must be separated:

```text
r_t^i
= horizon-level object-risk probability
= which object is the ego-relevant risk source

R_hat_{t+k}^i
= time-indexed future risk curve
= when risk emerges over the imagined future
```

However the latent transition state itself is a relation/world state, not a hand-defined scalar risk state. Risk is decoded from the rollout.

Therefore:

```text
explicit learned risk output       YES
post-hoc geometric rule only       NO
continuous risk field              NO
planner value / reward             NO
```

---

# 4. Future rollout truth

Physical rollout:

```text
H = 60
3 s at 20 FPS
```

Future prior recursion is a genuine physical-time prediction sequence:

```text
h_1 → h_2 → ... → h_60
```

and must not be confused with diffusion/flow solver iterations.

Training future relation targets come from logged future ego/object tracks:

```text
future ego-relative position
future ego-object distance
minimum future distance
```

Thus the supervision is factual under the logged episode.

---

# 5. Temporal-risk target provenance

The future risk curve is not a directly observed probability.

For the annotated risk object and event interval, the target is constructed from event timing using an exponential pre-event rise, unit value during the event interval, and zero for other objects.

Therefore:

```text
temporal risk target
= event-annotation-derived shaped target
```

This is important when comparing RiskWorld against SafeDrive's simulator-derived NC/DAC/TTC labels or DA-WAM's learned factor/value targets.

---

# 6. Action-conditioning / counterfactual audit

RiskWorld consumes only observed history:

```text
RGB history
object history
ego-motion history
```

It does NOT consume:

```text
hypothetical future ego trajectory
planning candidate
semantic action token
```

Hence:

```text
action-conditioned future                    NO
multiple ego-action branches                 NO
alternative-action future supervision        NO
reactive other-agent intervention truth      NO
```

The model learns a history-conditioned factual-distribution future, not candidate-specific counterfactual consequence.

---

# 7. Training objective audit

Losses:

```text
L_obj    object-risk BCE
L_xy     future relative-position regression
L_dist   future distance regression
L_min    minimum-distance regression
L_curve  temporal-risk BCE
L_KL     initial posterior/prior regularization
```

Composite objective:

```text
L = λ_obj L_obj
  + λ_xy L_xy
  + λ_dist L_dist
  + λ_min L_min
  + λ_curve L_curve
  + β L_KL
```

Inference uses posterior mean for the observed boundary and prior means for future rollout; stochastic samples are training-time machinery.

---

# 8. Evidence attribution

## Main benchmark

```text
FLaRA*     61.8 overall F1 / 4.1% FA
RiskWorld  63.0 overall F1 / 2.1% FA
```

The cleanest headline gain over the strongest adapted learned baseline is therefore:

```text
+1.2 F1
-2.0 pp FA
```

## Representation ablations

```text
w/o world features        50.6 F1 / 21.3 FA
w/o object visual token   54.6 / 3.3
w/o relation attention    54.3 / 1.2
RiskWorld                 63.0 / 2.1
```

These large gaps mostly establish the importance of pretrained predictive context, object visual grounding and relational contextualization.

Do NOT call `63.0 - 50.6` a pure RSSM world-model gain.

## Future-model ablations

```text
Deterministic GRU        62.0 / 6.0
w/o future rollout      60.2 / 5.9
w/o future supervision  61.6 / 4.4
RiskWorld               63.0 / 2.1
```

The more relevant matched interpretation is:

```text
recursive rollout contributes about +2.8 overall F1 over no-rollout;
future-oriented supervision contributes about +1.4;
stochastic RSSM improves aggregate trade-off by about +1.0 over deterministic GRU.
```

Per-category behavior is mixed, so do not claim universal superiority.

---

# 9. Future-risk evidence

Compared with current-state persistence, RiskWorld has lower horizon-wise Brier score across the 3 s future on annotated risk objects and reports a 59.8% error reduction at the 3 s horizon.

This directly supports temporal structure in the risk rollout.

It does NOT establish calibrated alternative-action consequence prediction.

---

# 10. Planning-aware evaluation audit

The paper uses LBC as a diagnostic planner.

Protocol:

```text
planner observes all objects
vs only GT risk object
vs objects retained by a risk selector
```

Unselected actors are masked.

This tests whether the selector preserves planning-relevant information.

It is NOT:

```text
RiskWorld risk → planner score → improved online planning policy
```

Paper itself states the protocol measures planning relevance, not planner improvement.

Therefore:

```text
planning relevance of selected objects        SUPPORTED
online planner coupling                       ABSENT
planning improvement caused by RiskWorld      NOT EVALUATED
```

---

# 11. Immediate cross-paper judgments

## vs SafeDrive

```text
SafeDrive:
ego trajectory candidate
→ candidate sparse world
→ explicit safety consequence
→ score / select

RiskWorld:
observed history
→ object relation rollout
→ explicit risk prediction
→ identify object
```

SafeDrive is action-conditioned and decision-facing. RiskWorld is history-conditioned and monitoring-facing.

## vs DA-WAM

DA-WAM branch identity is an **ego trajectory candidate**. RiskWorld branch identity is an **observed object**. Both are called candidates in prose, but their scientific meaning is different.

## vs WoTE

Both make multi-step future predictions. WoTE uses rollout to choose among actions; RiskWorld uses rollout to classify risk objects.

## vs GraphWorld

GraphWorld has strong world→planner coupling with no explicit long rollout. RiskWorld has explicit 60-step physical rollout with no world→planner coupling. This reinforces that rollout depth and planning coupling are orthogonal.

---

# 12. What RiskWorld proves

- object-wise relation rollout is useful for risk-source localization;
- future geometry/risk supervision adds value over current/static representations;
- risk can be a learned explicit prediction over a compact latent world rather than only a post-hoc geometric rule;
- selected objects can preserve planning-relevant information under a filtered-observation diagnostic.

# 13. What RiskWorld does not prove

- correct consequence under a changed ego plan;
- reactive agent responses to ego interventions;
- direct planning improvement;
- planning-optimality of its risk score;
- calibrated physical simulation;
- risk-field dynamics.

---

# Final audit verdict

```text
RiskWorld is a valuable boundary anchor because it makes risk explicit inside a predictive world-model pipeline,
but it remains a risk monitor rather than a planning WAM.

future relation rollout       YES
explicit risk state           YES
action-conditioned future     NO
online planning selection     NO
reactive intervention truth   NO
```
