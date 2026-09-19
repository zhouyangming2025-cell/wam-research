# RESEARCH_QA_GATE_CLOSEOUT — Waves 1–3

Last updated: 2026-09-14

Status: **HISTORICAL CLOSEOUT — the prior Wave-4 authorization was later superseded by the field-reconstruction pause.**

Purpose: close the post-Wave-3 evidence-reliability gate before expanding into closed-loop / simulation-realism / VLA / reactivity anchors.

Canonical detailed record:

```text
audits/literature/RESEARCH_QA_GATE_WAVES1_3.md
```

The former Priority-A progress snapshot was a one-time working log; its claim verdicts are retained in this closeout and the detailed register, so it is not a second entry point.

## 1. Gate verdict

All eight Priority-A items have been exhausted against available public primary sources and, where decision-critical and available, source code.

```text
A1 Epona      VERIFIED
A2 OccWorld   VERIFIED
A3 WoTE       VERIFIED + prior CODE VERIFIED supervision boundary
A4 LAW        VERIFIED + prior CODE VERIFIED inference boundary
A5 DriveLaW   VERIFIED + one material semantic CORRECTION
A6 Auto-JEPA  VERIFIED
A7 DA-WAM     VERIFIED
A8 DrivingGPT PAPER-LEVEL VERIFIED / exact optimized runtime path UNRESOLVED
```

The remaining DrivingGPT uncertainty is explicitly scoped and no field-level conclusion depends on silently assuming either runtime behavior.

**Authorization:** proceed to Wave 4.

---

## 2. Claims verified unchanged

### Epona

Matched joint-vs-trajectory-only planning evidence is real:

```text
w/o Joint Training 78.1 PDMS
full Epona          86.2 PDMS
```

This supports joint predictive representation / multi-task coupling. It does **not** prove online future-video evaluation causes the gain.

### OccWorld

The matched tokenizer counterexample is verified:

```text
better reconstruction
can coexist with worse future forecasting and worse planning.
```

Spatial and temporal dynamics ablations also materially degrade forecast/planning.

### WoTE

Matched planning decomposition is verified:

```text
trajectory only               81.0
+ learned evaluator           83.2
+ predicted future state      85.6 PDMS
```

Predicted future state adds value beyond evaluator-only in that setup. Prior code audit still shows the audited target-generation path does not provide candidate-specific reactive surrounding-agent futures.

### LAW

Action-aware future-latent auxiliary training improves its matched planner family, while horizon is non-monotonic:

```text
0.5s  0.61 / 0.30
1.5s  0.58 / 0.25
3.0s  0.63 / 0.27
10s   0.72 / 0.43
```

The code-verified deployment fact remains: the predicted future latent is not consumed to select the current trajectory at test time.

### Auto-JEPA

Its future target is an ego-trajectory latent, and the system materially depends on candidate retrieval/ranking:

```text
fixed medoid intent                    52.6
intent retrieval + gate, no scorer    87.6
intent + scorer, no gate              91.0
full                                  91.3 PDMS
```

Dynamic-agent semantic occlusion changes intent more than equal-area random masking (`0.080` vs `0.027`, `2.97×`; larger in `71.1%` of samples). This is evidence of selective planning sensitivity, not proof of causal/reactive world understanding.

### DA-WAM

The candidate-specific action→future→score architecture and expert-only observed-future supervision boundary are verified. Matched table:

```text
No Future Prediction                  93.31
Shared Global Future                  92.81
Current-Latent Conditioning           93.25
Action-Conditioned Future             93.46
Action-Conditioned Future + hard neg  93.68 PDMS
```

Candidate-specific future output is not equivalent to candidate-specific observed counterfactual ground truth.

### Think2Drive

Official ECCV paper verifies Dreamer-style RSSM world modeling and imagined actor/critic learning from privileged structured simulator state. It is a distinct WM role: latent imagination for policy training, rather than online candidate consequence scoring.

---

## 3. Material correction discovered by QA

### DriveLaW Stage-3 training semantics

Earlier synthesis conservatively left open whether the Video DiT was frozen during trajectory fine-tuning. That ambiguity is now resolved and the old wording must not be reused.

The paper explicitly states that Stage-3 trajectory fine-tuning updates **both the Video DiT and Planning DiT**. The official public repository reinforces this:

```text
train_mode: 'action_full'
```

and the corresponding training branch makes the unified diffusion-model parameters trainable under trajectory/action loss.

Correct interpretation:

```text
video pretraining
→ Stage-3 joint adaptation of Video-DiT + Action-DiT for planning
→ deployed Video-DiT hidden state conditions Action DiT
```

Incorrect interpretation now forbidden:

```text
pretrained/frozen video generator
→ fixed hidden features
→ separately trained action head
```

This correction **strengthens inference-time/training coupling**, but weakens any attempt to attribute the video-pretraining scaling table purely to fixed-representation transfer, because subsequent joint planning adaptation co-varies.

Verified DriveLaW internal evidence remains:

```text
video pretraining size: 0 / 76k / 3.8M / 7.6M
PDMS:                  85.9 / 87.0 / 87.8 / 89.1

representation:
BEV 84.1 / VLM hidden 86.5 / Video latent 89.1

denoising state:
t=1 89.1 / t=5 86.9 / t=10 23.2
```

Use these as pipeline-specific evidence, not universal laws about visual fidelity or world understanding.

---

## 4. Explicit unresolved item

### DrivingGPT optimized NAVSIM planning runtime path

Paper-level facts are secure:

```text
interleaved visual/action tokens
one causal autoregressive Transformer
standard next-token prediction
image-token generation documented for video inference
```

But the implementation-level question remains unresolved:

```text
Does the optimized NAVSIM planning path necessarily generate every intervening future visual token,
or can it use a planning-specific bypass/shortcut?
```

The project page's official code link points to `RogerChern/DrivingGPT`, which currently returns 404, and no accessible official repository was found.

Therefore future synthesis may say:

```text
DrivingGPT unifies world/action at sequence/objective level.
```

It may **not** say either runtime-path alternative is source-code proven.

This unresolved detail is not a Wave-4 blocker.

---

## 5. Cross-wave field claims after hardening

### F-01 — World-prediction quality is not itself planning evidence

**Verdict: STRONGLY SUPPORTED.**

Independent support includes:

```text
What Truly Matters: prediction metrics can disagree with driving performance; runtime matters.
OccWorld: better reconstruction can forecast/plan worse.
Drive-WM: system planning result does not isolate visual fidelity from detector/map/reward/candidate set.
Strong non-WM controls: good planning can arise without explicit world rollout.
```

Allowed as a field-level methodological rule; not a theorem that prediction quality never matters.

### F-02 — Future information is not automatically beneficial

**Verdict: STRONGLY SUPPORTED.**

Independent matched examples:

```text
M2I: an erroneous predicted influencer future can underperform marginal prediction.
LAW: 1.5s target outperforms 3s and 10s.
DA-WAM: shared-global future (92.81) underperforms no-future (93.31).
DriveLaW: inappropriate denoising state can collapse planning quality (t=10 → 23.2 PDMS).
```

Correct formulation:

```text
future information has value conditional on representation, accuracy, horizon, conditioning, supervision and decision interface.
```

### F-03 — Candidate-specific output is not candidate-specific oracle supervision

**Verdict: STRONGLY SUPPORTED.**

Two independent mechanisms:

```text
WoTE code audit: alternative ego candidates are evaluated with one cached logged/GT surrounding future in the audited target path.
DA-WAM paper: observed-future latent prediction loss applies only to expert-matched candidate.
```

### F-04 — WM-assisted planning is not synonymous with online model-based planning

**Verdict: STRONGLY SUPPORTED.**

The corpus contains clearly different roles:

```text
ViDAR / LAW     future prediction mainly shapes training representation
DriveLaW        online WM hidden state conditions action generator
WoTE / DA-WAM   online predicted future participates in candidate evaluation
Think2Drive     WM supplies imagined rollout environment for policy learning
```

### F-05 — Architectural coupling strength is not causal-evidence strength

**Verdict: SUPPORTED CROSS-PAPER INFERENCE.**

DrivingGPT has very tight token/objective unification but lacks a clean same-model action-only vs joint-world/action matched control in the reviewed evidence and its optimized planning runtime path is unavailable. DA-WAM has a highly explicit candidate→future→score path but only `+0.15 PDMS` future gain over its strong no-future matched baseline before hard negatives.

Do not turn this into a universal quantitative law.

### F-06 — Decision relevance and world completeness are different objectives

**Verdict: SUPPORTED FIELD TENSION; NOT YET A UNIVERSAL PRINCIPLE.**

Evidence cluster:

```text
OccWorld     richer/better reconstruction can plan worse
LAW          longer future target can hurt
DriveLaW     planning is highly representation-state-specific
Auto-JEPA    deliberately predicts future ego intent instead of full future scene and remains competitive
```

Wave 4 should test how this tension changes when evaluation includes interactive closed-loop behavior and simulation realism.

---

## 6. Statements no longer allowed in future synthesis

```text
1. "DriveLaW freezes its video world model during planner training."
   → FALSE for the audited Stage-3 configuration; both Video DiT and Planning DiT are updated.

2. "DrivingGPT's NAVSIM runtime definitely generates every future image token before each action."
   → UNRESOLVED; code unavailable.

3. "DA-WAM has ground-truth counterfactual future latents for every candidate."
   → FALSE; observed-future latent supervision is expert-matched only.

4. "WoTE's alternative candidates have candidate-reactive ground-truth surrounding futures."
   → NOT ESTABLISHED; audited path uses fixed logged surrounding future.

5. "NAVSIM PDMS is reactive closed-loop validation."
   → FALSE; NAVSIM is non-reactive pseudo-simulation.

6. "Better/longer/richer world prediction should monotonically improve planning."
   → CONTRADICTED by multiple matched controls; future value is interface-conditional.
```

---

## 7. QA outcome and Wave-4 authorization

The evidence base is now sufficiently hardened for field reconstruction to proceed.

```text
OCR/table ambiguity at field-critical points  = cleared or explicitly scoped
source-code ambiguities                       = resolved where public code exists
remaining unresolved detail                   = marked, non-blocking
material correction                           = propagated into canonical QA state
```

### Decision

```text
RESEARCH QA GATE — CLOSED
WAVE 4 — AUTHORIZED
```

Next anchors:

```text
Bench2Drive
HUGSIM
ORION
ReactSim-Bench
CausalDrive
```

Wave-4 purpose is not gap hunting. It is to reconstruct the distinctions among:

```text
sensor / visual realism
physical scene evolution
other-agent behavior realism
ego-action feedback
reactivity
closed-loop policy evaluation
VLA / semantic reasoning
world-model behavioral validity
```

The next synthesis must preserve the evidence taxonomy and evaluation-regime boundaries established by this QA gate.
