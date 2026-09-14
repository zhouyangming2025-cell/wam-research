# PHASE_B_WAVE3_DAWAM_AUDIT — Per-Candidate Future Latents and the Supervision Asymmetry of Offline Planning

Last updated: 2026-09-14

Status: **PRIMARY-TEXT FIRST PASS COMPLETE**

Role in Wave 3: contrast Auto-JEPA's single scene-conditioned ego-intent latent with DA-WAM's per-candidate future-latent prediction and candidate-level scoring.

Comparative baseline:

```text
Auto-JEPA:
scene/history/route
→ one future ego-intent latent
→ retrieve action candidates
→ scorer/gate

DA-WAM:
current scene + candidate_i
→ future latent_i
→ scorer(current, candidate_i, future_i)
→ rank candidates
```

The key scientific question is not whether DA-WAM is `more counterfactual`, but what supervision supports each candidate-specific future and how much of the planning gain is actually attributable to future-state modeling rather than ranking/scorer supervision.

---

## 1. Exact architecture

Given current observation `X_t`, the online encoder produces scene tokens:

```text
Z_t = E_theta(X_t) ∈ R^(M×D)
```

The online encoder starts from V-JEPA 2.1. The base is frozen while selected layers receive LoRA adaptation jointly trained by prediction and planning losses.

For candidate set:

```text
T = {tau_i}_{i=1..N}
```

each candidate trajectory is mapped into an action representation `a_i`.

A shared predictor uses the candidate action as query and current scene tokens as key/value:

```text
Zhat_i = P_phi(Q=a_i, K=Z_t, V=Z_t)
```

so every candidate receives its own predicted future latent.

The shared scorer then evaluates:

```text
(Z_t, a_i, Zhat_i)
→ planning factors qhat_i
→ utility score shat_i
```

and the highest-scoring candidate is selected.

This is a genuine online interface:

```text
candidate_i
→ candidate-specific future latent_i
→ candidate-specific score_i
→ selection
```

Unlike LAW/ViDAR, the future latent remains on the deployed decision path.

---

## 2. What is actually unified?

DA-WAM unifies three learning signals in one planner:

```text
predictive latent learning
+ candidate-specific future prediction
+ trajectory scoring/ranking
```

The online representation is allowed to adapt during planner optimization through LoRA, while an EMA target encoder provides a stable future target during training.

This is different from:

```text
Auto-JEPA — frozen visual + frozen trajectory target space
LAW       — future-latent auxiliary loss but no latent→action inference path
DriveLaW  — world-generator hidden state conditions one action generator
WoTE      — future BEV state conditions trajectory evaluator
```

DA-WAM's distinctive interface is the explicit one-to-one mapping:

```text
tau_i ↔ Zhat_i ↔ score_i
```

---

## 3. Predictive target and target-network mechanics

During training the observed future frame `X_(t+Δ)` is encoded by a stop-gradient EMA target network:

```text
Z_(t+Δ) = sg(E_bar_theta(X_(t+Δ)))
```

with EMA update:

```text
bar_theta ← μ bar_theta + (1-μ) theta
```

The target branch is training-only; inference keeps only:

```text
online encoder + action-conditioned predictor + scorer
```

This differs from Auto-JEPA, whose future target is a frozen trajectory encoder, and from LAW, where the predicted future latent does not control current action choice.

---

## 4. The central supervision asymmetry

Offline logs contain only:

```text
executed expert trajectory tau_exp
+ its observed future X_(t+Δ)
```

They do **not** contain observed futures for unexecuted alternatives.

DA-WAM explicitly acknowledges this and avoids assigning the expert future to every candidate.

It finds the closest candidate:

```text
i_exp = argmin_i ADE(tau_i, tau_exp)
```

and applies dense latent prediction loss only to:

```text
Zhat_(i_exp)
```

against the observed future target.

Therefore:

```text
expert-matched candidate future latent:
DIRECT observed-future supervision = YES

all other candidate future latents:
DIRECT alternative-future latent supervision = NO
```

This is one of the most important facts in the paper.

DA-WAM predicts `N` alternative future latents online, but only one branch per logged scene has a direct future-state target.

---

## 5. What supervision do unexecuted candidates receive?

All candidates participate in planning-oriented objectives:

```text
factor loss
utility-score loss
ranking loss
```

Hard negatives are additionally retrieved near the expert trajectory but with different safety outcomes.

The paper is explicit that hard-negative labels are:

```text
training-only planning targets
```

not observed future representations.

Thus unexecuted candidates are supervised indirectly through:

```text
trajectory-level quality / safety / ranking labels
```

rather than a direct latent target representing what the world would actually look like under that candidate.

This distinction is fundamental:

```text
candidate-specific future latent OUTPUT
!=
candidate-specific future latent GROUND TRUTH
```

The system can still learn useful branch-specific features through shared predictor parameters and downstream scoring gradients, but the alternative latent futures are not directly validated against counterfactual world-state oracle targets.

---

## 6. Hard negatives: useful planning supervision, not counterfactual-world supervision

DA-WAM retrieves trajectories satisfying approximately:

```text
close to expert in trajectory geometry
AND
meaningfully different in safety outcome
```

The purpose is to prevent the scorer from learning trivial geometry cues and sharpen safety boundaries.

This is scientifically sensible, but the correct interpretation is:

```text
hard negatives strengthen ACTION RANKING supervision
```

not:

```text
hard negatives provide direct ground-truth future worlds for alternative actions
```

This matters because the paper sometimes uses `counterfactual` language at the trajectory/safety level. The counterfactual signal here is primarily **planning-label contrast**, not directly observed alternative world evolution.

---

## 7. Matched future-configuration ablation — the most important table

NAVSIM-v1 navtest:

```text
No Future Prediction             93.31 PDMS
Shared Global Future             92.81
Current-Latent Conditioning      93.25
Action-Conditioned Future        93.46
Action-Conditioned + hard neg.   93.68
```

This table is much more informative than the SOTA headline.

### 7.1 Strong baseline matters

The no-future planner is already:

```text
93.31 PDMS
```

So the action-conditioned future without hard negatives contributes only:

```text
+0.15 PDMS
```

over no-future prediction.

Adding hard negatives yields another:

```text
+0.22 PDMS
```

for a total difference of:

```text
+0.37 PDMS
```

versus the no-future baseline.

Therefore DA-WAM does **not** support a story in which candidate-specific world prediction is the dominant source of planning performance. The underlying candidate planner/scorer is already extremely strong.

### 7.2 Shared future can be worse than no future

```text
Shared Global Future = 92.81
No Future            = 93.31
```

This is useful evidence that merely injecting a future representation can harm candidate discrimination when the same future is reused across different actions.

This strengthens the field-level rule:

```text
FUTURE INFORMATION != AUTOMATIC PLANNING VALUE
```

and more specifically:

```text
future representation must match the decision unit that consumes it
```

### 7.3 Current-latent control

```text
Current-Latent Conditioning = 93.25
```

is essentially the same as no-future 93.31, suggesting that simply adding another latent conditioning pathway is not enough.

### 7.4 Action-conditioned future effect

```text
93.31 → 93.46
```

is positive but modest.

This is still useful matched evidence that branch-specific future prediction can improve ranking in this setup, but the magnitude requires conservative interpretation.

### 7.5 Hard-negative effect

```text
93.46 → 93.68
```

shows that local safety discrimination adds comparable or larger incremental gain than the future-state mechanism itself.

Hence the final method's success should be decomposed as:

```text
very strong base candidate planner
+ small branch-specific future-state gain
+ additional hard-negative ranking gain
+ representation adaptation gain
```

rather than being credited wholesale to `world modeling`.

---

## 8. Predictive-representation adaptation evidence

The paper separately studies online-encoder adaptation and dense predictive objectives.

Reported NAVSIM-v1 examples include:

```text
Frozen + old/no dense objective      91.26
Frozen + dense objective             91.95
LoRA + old/no dense objective        92.74
LoRA + dense objective               92.98
Full fine-tune + dense objective     92.62
```

This suggests:

```text
predictive objective helps
LoRA task adaptation helps strongly
full fine-tuning is not automatically better
```

The important scientific interpretation is that representation adaptation is an independent contributor from candidate-specific future scoring.

DA-WAM therefore combines two separable ideas:

```text
A. make the latent representation co-evolve with planning
B. make the future prediction candidate-specific and feed it to scoring
```

These should not be collapsed into one mechanism.

---

## 9. Comparison with Auto-JEPA

### Auto-JEPA

```text
predict ONE scene-conditioned future ego-intent latent
→ retrieve trajectories close to that intent
→ score/filter retrieved candidates
```

The predicted future latent defines the *region of action space* to search.

### DA-WAM

```text
generate candidate set first
→ predict ONE future latent PER candidate
→ score each candidate with its own future latent
```

The predicted future latent helps *differentiate alternatives already in the candidate set*.

Thus they solve different subproblems:

```text
Auto-JEPA: future representation as action-retrieval query
DA-WAM:    future representation as candidate-evaluation context
```

Neither architecture alone establishes behaviorally correct counterfactual world evolution.

---

## 10. Comparison with WoTE

Both are online candidate-conditioned WM planners:

```text
candidate_i → future_i → score_i
```

but their future state differs:

```text
WoTE   → future BEV states
DA-WAM → future V-JEPA latent state
```

And the supervision distinction is revealing:

```text
WoTE:
candidate-specific ego/reward targets under NAVSIM fixed logged-agent semantics

DA-WAM:
direct future-latent target only for expert-matched candidate;
all candidates get factor/utility/ranking supervision
```

Both expose the same fundamental offline limitation from different angles:

```text
alternative actions are easy to enumerate,
but alternative world futures are not directly observed.
```

This is a field fact, not yet a gap claim.

---

## 11. Evaluation boundary

The core ablations are on NAVSIM-v1; the paper also reports NAVSIM-v2.

NAVSIM remains non-reactive pseudo-simulation. Therefore:

```text
candidate-specific latent improves NAVSIM ranking
```

is supported, while:

```text
candidate-specific latent predicts true reactive other-agent response
```

is not established by these results.

Qualitative conflict examples can illustrate selected trajectories, but they do not substitute for reactive counterfactual ground truth.

---

## 12. Strongest evidence and strongest limitation

### Strongest evidence

The matched configuration table is unusually good because it compares:

```text
no future
shared future
current latent
candidate-specific future
candidate-specific future + hard negatives
```

within one planner family.

This establishes that **future/action alignment matters more than simply having an extra future/global latent**, and that branch-specific future input provides a small positive incremental planning benefit.

### Strongest limitation

The candidate-specific latent is directly supervised only for the expert-matched branch.

Hence:

```text
DA-WAM has strong architectural action–future alignment,
without equally strong direct supervision for the semantic correctness of every alternative future latent.
```

This is not a flaw unique to DA-WAM; it is a consequence of offline logged driving data.

---

## 13. What DA-WAM proves and does not prove

### Directly supported

```text
1. Candidate-specific future latent can be consumed online by a trajectory scorer.
2. Shared/global future conditioning can be worse than no future in candidate ranking.
3. Candidate-specific future conditioning slightly improves a strong no-future baseline.
4. Hard-negative ranking supervision adds further safety/planning value.
5. Predictive representation adaptation and candidate-future scoring are separable contributors.
6. Offline expert-only future observations require asymmetric future-state supervision.
```

### Not established

```text
1. Every unexecuted candidate future latent corresponds to the true world that would occur under that action.
2. Candidate-specific latent correctness is directly validated against reactive counterfactual oracle futures.
3. World modeling is the dominant source of DA-WAM's final planning performance.
4. The +0.37 PDMS total improvement over the no-future baseline implies a broadly large effect across evaluation regimes.
5. NAVSIM evidence establishes reactive closed-loop correctness.
```

---

## 14. Five-way Wave-3 interface map

```text
Epona
shared history latent → modular trajectory / visual generation

DrivingGPT
interleaved image/action tokens → one causal driving language

DriveLaW
online video-generator hidden state → Action DiT

Auto-JEPA
predicted future ego-intent latent → action-memory retrieval → score

DA-WAM
candidate_i → candidate-specific future latent_i → score_i
```

This map now makes a crucial distinction explicit:

```text
future representation can guide
A. shared representation learning
B. action generation
C. action retrieval
D. action evaluation
```

These are different planning interfaces even when all are called WAMs.

---

## 15. Evidence verdict

```text
online candidate-specific future used by scorer:      STRONG
matched evidence future/action alignment helps:       MODERATE-STRONG
magnitude over strong no-future baseline:             SMALL
hard-negative ranking is independent contributor:     STRONG
alternative future latent direct supervision:         EXPERT-MATCHED ONLY
reactive counterfactual correctness:                  NOT ESTABLISHED
world modeling as dominant source of final score:     NOT ESTABLISHED
```

Wave-3 status after this audit:

```text
Epona       COMPLETE
DrivingGPT  COMPLETE
DriveLaW    COMPLETE
Auto-JEPA   COMPLETE
DA-WAM      COMPLETE
Think2Drive NEXT
```
