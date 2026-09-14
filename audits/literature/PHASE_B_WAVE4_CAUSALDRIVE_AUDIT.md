# PHASE_B_WAVE4_CAUSALDRIVE_AUDIT

Last updated: 2026-09-14

Status: **COMPLETE**

Paper: `CausalDrive: Real-time Causal World Models for Autonomous Driving`

Role in Wave 4: **real-time action-conditioned visual world simulator with semantic control over synthesized surrounding-agent reactions**.

Important semantic warning:

```text
paper title/terminology uses “causal” and “counterfactual” strongly;
our audit does NOT equate this automatically with causal identification in the potential-outcome / intervention-ground-truth sense.
```

---

## 1. Executive verdict

CausalDrive is substantially more than a passive video generator:

```text
initial front-view frame
+ streaming ego trajectory/control
+ semantic “driving sociology” prompt
→ autoregressive visual future
→ surrounding vehicles may synthesize different reactions
→ real-time ~12 FPS
```

It deliberately avoids future NPC layouts, so surrounding-agent futures are not directly supplied as oracle geometry. This makes it meaningfully closer to an interactive learned simulator than layout-conditioned renderers.

However its evidence supports:

```text
ACTION-CONDITIONED + SEMANTICALLY CONTROLLABLE REACTIVE SYNTHESIS
```

more strongly than:

```text
IDENTIFIED TRUE CAUSAL COUNTERFACTUAL RESPONSE.
```

The model can generate “polite yield” vs “aggressive rush” responses to the same ego action by changing a text prompt. That proves controlled alternative synthesis; it does not establish which alternative a particular real driver would actually have taken under an unobserved intervention.

---

## 2. Exact world-model interface

CausalDrive models an autoregressive latent-video transition:

```text
p_theta(C_1:K | C_0, A_1:K)
```

where:

```text
C_0       = initial visual context / front-view frame
C_k       = generated latent visual chunk
A_1:K     = streaming external control / ego trajectory condition
B         = macroscopic sociology prompt
```

Condition injection:

```text
ego trajectory / geometric pose → AdaLN conditioning
sociology prompt                → cross-attention
past generated chunks           → block-causal temporal context
```

This differs from layout-conditioned renderers because future NPC boxes/trajectories are intentionally omitted.

Thus the model must synthesize surrounding-agent motion from current context + ego behavior + semantic condition rather than merely render a fully specified future scene.

---

## 3. Three-stage training / acceleration structure

### Stage 0 — causal streaming architecture

The base video model is converted to block-causal temporal processing suitable for streaming generation.

### Stage 1 — causal AR flow-matching teacher

The teacher is trained autoregressively with ground-truth historical context (teacher forcing) using continuous flow matching.

### Stage 2 — Self-Corrective / Context-Forced DMD

The student first produces its own imperfect autoregressive rollout. The frozen teacher then evaluates distillation guidance while conditioned on the student’s flawed context.

Intended effect:

```text
teacher learns to provide correction signal under the actual student rollout distribution
rather than only under clean GT context.
```

The distilled model uses ≤4 denoising/function-evaluation steps and reports ~12.4 FPS.

This is important because interactive simulation needs feedback bandwidth, not only high single-video quality.

---

## 4. What is “Driving Sociology” supervision?

SocioDrive-Bench contains approximately:

```text
20K video clips
80% real nuPlan-derived interactions
20% CARLA safety-critical / collision scenarios
```

The authors mine/annotate interaction categories such as:

```text
Ego-Initiated / Active Pressure
  e.g. ego cut-in → rear car braking

Ego-Reactive / Defensive Driving
  e.g. neighbor cut-in → ego emergency braking

Complex Negotiation
  e.g. unprotected intersection / narrow-passage yielding
```

Annotation is built through a VLM→LLM pipeline:

```text
multi-view clip
→ VLM structured micro-analysis
→ LLM sequence-level interaction summary
→ sociology prompt / interaction labels
```

Important boundary:

These labels are mined from **observed logs / generated CARLA clips** according to kinematic/event triggers plus VLM/LLM semantic annotation.

They are not randomized controlled interventions where the same real scene is executed under several ego actions and the corresponding real NPC responses are all observed.

Therefore:

```text
OBSERVED INTERACTION PAIR / SEMANTIC LABEL
!=
GROUND-TRUTH RESPONSE FUNCTION FOR UNEXECUTED EGO ACTIONS.
```

---

## 5. Why omission of future NPC layouts matters

This is a real architectural distinction.

Layout-conditioned generators receive something close to:

```text
future ego + future NPC geometry
→ render video
```

so NPC “reaction” is externally specified.

CausalDrive receives:

```text
initial image + ego trajectory + sociology prompt
→ infer/render NPC future
```

Thus surrounding-agent future is genuinely a model output, not an oracle rendering input.

Allowed conclusion:

```text
CausalDrive performs predictive surrounding-world synthesis under ego/action conditions.
```

Not allowed:

```text
because NPC future is not an input, the learned NPC future is necessarily causally correct.
```

Removing oracle leakage is necessary for reactive prediction, not sufficient for identifying the true response.

---

## 6. Action controllability evidence

The paper explicitly evaluates whether generated pixels reflect the injected ego trajectory.

A pretrained inverse-dynamics / tracking model recovers ego motion from generated video, then the recovered trajectory is compared with the injected condition through displacement-style metrics.

CausalDrive reports strong action controllability and real-time speed while maintaining competitive visual fidelity.

Table-level speed:

```text
CausalDrive ≈ 12.4 FPS
```

compared with much slower video-generation baselines in the reported setup.

This supports:

```text
streaming control actually affects generated visual dynamics
```

at the ego level.

It does not by itself prove surrounding-agent reactions are correct.

---

## 7. Reactivity evidence: YCR / FCR

The paper evaluates aggressive ego maneuvers and asks whether neighboring generated vehicles yield.

Reported table:

```text
                     Yielding Compliance   False Collision
Log Replay                  0.0%              100.0%
Vista                      12.5%               87.5%
CausalDrive (“Polite”)     82.0%               18.0%
```

This is useful evidence that the model can synthesize a prompt-conditioned yield response and reduce ghost collisions relative to log replay / a simple action-conditioned visual predictor.

But the target semantics matter:

```text
YCR asks whether generated neighbors perform the requested/expected yielding behavior.
```

It does not compare with a recorded true reaction under that same unexecuted aggressive ego trajectory.

Therefore the strongest defensible interpretation is:

```text
CausalDrive has high controllable reactive-compliance under the benchmark’s semantic target.
```

not:

```text
82% of its generated responses match the true human counterfactual response.
```

---

## 8. Same ego action + different text prompt is controllable counterfactual synthesis, not causal identification

The paper highlights examples where the initial scene and ego trajectory are held fixed while a prompt changes:

```text
“Polite”       → surrounding car yields
“Aggressive”   → surrounding car rushes / competes
```

This demonstrates that the model supports a controllable family of alternative futures.

Conceptually:

```text
same (s, a_ego)
+ different semantic mode b
→ different generated NPC future
```

This is valuable for simulation diversity and stress testing.

But causal identification would require evidence closer to:

```text
same factual history
same well-defined intervention
→ observed target response distribution under that intervention
```

which ordinary logs do not provide.

Thus:

```text
SEMANTIC COUNTERFACTUAL GENERATION
!=
IDENTIFIED COUNTERFACTUAL TRUTH.
```

---

## 9. Closed-loop simulation application

The paper evaluates planners inside CausalDrive under a PDM-Closed-style protocol and reports better planner scores / reduced ghost artifacts than other generative simulation baselines.

The raw table formatting is partially ambiguous, so this audit does not overquote every column.

System-level conclusion allowed:

```text
CausalDrive can function as an iterative planner-in-the-loop visual simulator rather than only an offline video generator.
```

Boundary:

```text
better simulator aggregate score does not isolate whether the gain comes from visual fidelity,
action controllability, sociology conditioning, or reduced ghost collisions.
```

---

## 10. RL post-training application

The paper also treats generated video as an RL environment:

```text
state = generated visual chunk
policy action = ego trajectory/control
Video2Reward = collision + lane reward terms
policy optimized inside CausalDrive
```

Reported NAVSIM evaluation after RL:

```text
RL in CausalDrive: 90.7 PDMS
```

with strong TTC/comfort metrics in the shown table.

This establishes a useful system-level role:

```text
learned reactive visual WM → imagined/pseudo-simulated experience → policy post-training.
```

But NAVSIM remains non-reactive evaluation. So this result does not itself prove the resulting policy has superior reactive behavior under a matched real interactive benchmark.

The paper’s broader real-world interaction claim should therefore remain `AUTHOR CLAIM` unless separately supported by a documented real-vehicle protocol/table; the primary sections inspected here do not provide enough detail to upgrade it to a quantitative field-level fact.

---

## 11. Comparison with Think2Drive

Both use learned worlds to improve a policy, but the world representation and deployment goal differ sharply.

```text
Think2Drive:
privileged structured BEV state
→ RSSM latent dynamics / reward / termination
→ actor-critic imagination

CausalDrive:
front-view visual world
→ action/prompt-conditioned streaming video simulation
→ Video2Reward / planner-in-the-loop / human-in-loop
```

Think2Drive is a compact control-oriented latent model.
CausalDrive is a photorealistic interactive visual simulator.

Both show that WM value can come through **training environment construction**, not only through direct deployed action selection.

---

## 12. Comparison with HUGSIM

```text
HUGSIM
visual world = reconstructed real 3D scene
agent behavior = replay / IDM / optimization-based attack controller

CausalDrive
visual world = learned generative video transition
agent behavior = implicitly synthesized by the same learned world model under ego trajectory + sociology prompt
```

Thus CausalDrive moves behavioral generation inside the learned visual world model, whereas HUGSIM composes high-fidelity reconstruction with explicit external actor controllers.

But HUGSIM’s hand-designed controller semantics can be inspected exactly; CausalDrive’s learned reactions are more stochastic/data-driven but harder to validate as true human responses.

---

## 13. Comparison with ReactSim-Bench

ReactSim-Bench asks:

```text
Given a fixed deviated ego trajectory, can a learned agent simulator produce safe/feasible responses?
```

CausalDrive asks/provides:

```text
Given ego trajectory + semantic interaction mode, can a visual world generator synthesize a plausible controlled reactive future?
```

They are complementary:

```text
ReactSim-Bench = measurement protocol centered on ego-deviation pressure
CausalDrive    = learned visual simulator with semantic reactive control
```

Neither has true real-world alternative-action response labels.

This is a key Wave-4 result.

---

## 14. What “causal” is justified by evidence?

### Evidence supports

```text
- ego trajectory is an explicit intervention-like conditioning variable;
- future NPC layout is not given as oracle input;
- generated NPC behavior changes under ego condition / semantic sociology prompt;
- model is autoregressive and receives its generated history;
- reaction proxies and downstream simulator applications improve.
```

### Evidence does not establish

```text
- causal-effect identification from observational data;
- true potential outcomes for unexecuted ego actions;
- calibrated probability of real human response modes;
- episode-specific ground-truth counterfactual reactions.
```

Therefore in our own taxonomy, prefer:

```text
ACTION-CONDITIONED LEARNED REACTIVE WORLD SIMULATOR
```

over an unqualified statement such as:

```text
“causally correct simulator.”
```

---

## 15. Strongest evidence and strongest alternative explanation

### Strongest evidence

```text
1. no future NPC layout input;
2. strong injected-action controllability;
3. prompt-controlled alternative NPC reactions;
4. YCR/FCR improvement vs log replay / Vista;
5. real-time ~12 FPS streaming generation;
6. actual planner/RL/human-in-loop applications.
```

### Strongest alternative explanation / boundary

The “reactive sociology” result may reflect:

```text
semantic prompt obedience
+ interaction-label priors
+ synthetic CARLA hard-case augmentation
+ visual generative prior
```

without establishing that the generated reaction matches the actual conditional response distribution of real traffic participants under an unseen ego intervention.

That is not a defect unique to CausalDrive; it is a fundamental supervision boundary of logged driving data.

---

## 16. Stable distinction introduced

```text
NO ORACLE FUTURE LAYOUT
+
ACTION-CONDITIONED GENERATION
+
SEMANTIC RESPONSE CONTROL

!=

COUNTERFACTUAL CAUSAL IDENTIFICATION
```

At the same time, the left-hand side is still a substantial simulator capability and should not be dismissed merely because the right-hand side is unavailable.

## Verdict

```text
CausalDrive deep read = COMPLETE
classification = real-time learned action-conditioned reactive visual simulator
causal-truth claim = bounded / not identified from alternative-action GT
```

No research gap is declared.
