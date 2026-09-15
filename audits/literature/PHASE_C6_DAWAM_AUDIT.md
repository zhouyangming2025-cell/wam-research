# Phase C.6 DA-WAM Audit

Last updated: 2026-09-15

Status: **COMPLETE FIRST PASS — PAPER VERIFIED / OFFICIAL IMPLEMENTATION NOT YET RELEASED**

Paper:

```text
DA-WAM: Decision-Aligned Future Latents for Driving World Models
arXiv:2608.19085v2
```

Official repository:

```text
LeapWM/da-wam
latest observed commit: 1edbe555146a2d1fe9484f5c11f120860b8a4858
```

Observed public repo state:

```text
README.md only
"comming soon"
```

Therefore exact implementation details remain SOURCE-UNVERIFIED.

Canonical deep read:

```text
papers/deep_analysis/P0012_DAWAM_DEEP_ANALYSIS_V2.md
```

---

# 1. Stable mechanism judgment

DA-WAM is an online candidate-specific future-latent evaluator, but it is **not** a system with observed counterfactual future truth for every candidate.

Training:

```text
X_t → online V-JEPA 2.1 encoder (+ LoRA) → Z_t
X_{t+0.5s} → EMA target encoder → stop-grad factual future latent Z_{t+Δ}

proposal module → 32 trajectories τ_i → action embeddings a_i

for each i:
(a_i, Z_t) → shared predictor → Zhat_i

closest candidate to expert trajectory:
Zhat_i_exp → dense future-latent loss vs factual Z_{t+Δ}

all candidates + hard negatives:
(Z_t, a_i, Zhat_i)
→ factorized scorer
→ NC/DAC/EP/TTC/Comfort + scalar utility
→ factor + utility + ranking losses
```

Inference:

```text
current observation
→ online encoder
→ 32 candidate trajectories
→ 32 candidate-specific future latents
→ factorized utility scorer
→ argmax
```

Training-only:

```text
EMA target encoder
observed future frame
expert matching
hard-negative retrieval
```

Canonical subtype:

```text
ONLINE CANDIDATE-SPECIFIC FUTURE-LATENT UTILITY SCORING WAM
```

---

# 2. CLAIM → EVIDENCE → INTERPRETATION → UNPROVEN

## Claim A — one-to-one candidate/future alignment improves trajectory scoring

**AUTHOR CLAIM**

Every candidate should be scored with the future predicted specifically under that candidate rather than a future representation shared across proposals.

**DIRECT PAPER EVIDENCE**

Matched Table 3:

```text
No Future Prediction          93.31 PDMS
Shared Global Future          92.81
Current-Latent Conditioning   93.25
Action-Conditioned Future     93.46
+ Hard Negatives              93.68
```

**OUR INTERPRETATION**

The cleanest evidence is:

```text
shared-global future → action-conditioned future
92.81 → 93.46
```

and:

```text
no future → action-conditioned future
93.31 → 93.46
```

Candidate-specific future conditioning is useful in the matched planner, but the gain over the strong no-future baseline is modest (+0.15 PDMS).

**REMAINS UNPROVEN**

The ablation does not establish that each candidate-specific latent is a physically correct counterfactual future.

---

## Claim B — DA-WAM solves the offline counterfactual-supervision problem

**DIRECT PAPER EVIDENCE**

The paper explicitly states that each offline scene contains only:

```text
one expert trajectory
+
one observed future
```

It therefore applies dense future-latent loss only to the candidate nearest the expert by ADE.

**OUR INTERPRETATION**

DA-WAM correctly avoids the invalid supervision pattern:

```text
one factual future target
→ supervise every unexecuted action branch as though it were factual
```

This is a scientifically cleaner treatment of observational data.

**REMAINS UNPROVEN**

Avoiding false labels does not provide the missing alternative-action labels. The N−1 unexecuted branches remain without direct world-state counterfactual truth.

Binding vector:

```text
candidate-specific output              YES
candidate-specific factual future GT   ONLY factual/expert-matched branch
alternative intervention truth         NO
reactive other-agent truth             NO / NOT ESTABLISHED
```

---

## Claim C — non-expert future latents are useful consequence representations

**DIRECT PAPER EVIDENCE**

All candidate latents enter the scorer and receive factor, utility and ranking supervision. Hard negatives are also assigned their own predicted latent and scorer targets.

**OUR INTERPRETATION**

The non-expert branches are decision-shaped by downstream supervision.

**REMAINS UNPROVEN**

There is no independent prediction metric or matched alternative-world target validating these branches as physically faithful future-world states. They may function partly as candidate-conditioned decision features.

---

## Claim D — hard negatives sharpen safety discrimination

**DIRECT PAPER EVIDENCE**

Matched Table 3:

```text
Action-conditioned future, no HN   93.46
+ hard negatives                   93.68
```

Hard negatives are selected to be close to expert geometry but substantially worse on safety metrics.

**OUR INTERPRETATION**

Hard-negative supervision contributes +0.22 PDMS and improves NC/DAC/TTC/Comfort while reducing EP slightly.

**BOUNDARY**

The hard-negative label is a planning metric/value target, not an observed future-state target. `counterfactual safety supervision` must not be conflated with counterfactual world supervision.

---

## Claim E — predictive representation should co-evolve with planning

**DIRECT PAPER EVIDENCE**

Table 4:

```text
Frozen, non-dense   91.26
Frozen, dense       91.95
LoRA, non-dense     92.74
LoRA, dense         92.98
Full FT, dense      92.62

LoRA+dense target policy:
Frozen              92.98
Separate            93.10
Shared              93.34
EMA                 93.68
```

**OUR INTERPRETATION**

Dense JEPA supervision, LoRA task adaptation and EMA target design are all useful in the reported matched settings.

**BOUNDARY**

The final performance is a bundle. Do not call the entire Table-4 improvement a pure world-dynamics gain.

---

# 3. Supervision truth audit

## Factual future latent

```text
source: observed future frame X_{t+Δ}
encoder: EMA target encoder
Δ: 0.5 s
coverage: expert-matched branch only
```

## Other generated candidates

```text
direct future-feature GT: NO
factor targets: YES
utility targets: YES
ranking targets: YES
```

## Hard negatives

```text
direct future-feature GT: NO
safety/value targets: YES
```

Therefore:

```text
future latent semantics are heterogeneous across branches during training:

factual branch   = predictive + decision supervised
other branches   = decision supervised, no direct future truth
```

This distinction is central to interpreting DA-WAM.

---

# 4. Scorer semantics audit

The scorer predicts:

```text
NC
DAC
EP
TTC
Comfort
```

followed by overall utility.

Thus DA-WAM belongs on the explicit value/utility side of the WAM landscape.

Comparison:

```text
WoTE       future consequence → explicit reward/utility
DA-WAM     future latent → explicit metric factors + utility
World4Drive future latent → factual-mode consistency score
```

Do not collapse these into one generic `future score` category.

---

# 5. Candidate support audit

Reported candidate count:

```text
N = 32
```

Candidate-count Table 5:

```text
1    87.11
8    90.76
16   91.89
32   93.68
64   93.68
```

This confirms that candidate support is itself a major source of planning performance.

Therefore headline final score must be decomposed into:

```text
proposal/candidate support
+
representation prior/adaptation
+
future predictor
+
scorer/value supervision
+
hard-negative supervision
```

---

# 6. Temporal audit

Core future target:

```text
one endpoint latent at t+0.5s
```

No recurrent physical future rollout is central to the method.

Hence:

```text
32 branches
!=
32 multi-step world rollouts
```

and:

```text
candidate multiplicity
!=
future temporal depth
```

---

# 7. Evaluation audit

Benchmarks:

```text
NAVSIM-v1 navtest
NAVSIM-v2 navtest
```

Project-standard evaluation label:

```text
NON-REACTIVE DATA-DRIVEN / PSEUDO-SIMULATION PLANNING
```

Headline:

```text
93.7 PDMS
87.7 EPDMS
```

These do not validate reactive counterfactual world responses.

---

# 8. Source audit status

Official code repository exists but implementation is not yet released.

Observed:

```text
LeapWM/da-wam@1edbe555146a2d1fe9484f5c11f120860b8a4858
README.md only
"comming soon"
```

Therefore unresolved until code release:

```text
exact LoRA layer placement
exact predictor depth/shape
exact scorer attention topology
exact gradient detach boundaries
exact candidate proposal implementation
hard-negative bank construction code
factor/utility target implementation
runtime / batching details
```

Status:

```text
PAPER-COMPLETE FOR CORE MECHANISM
SOURCE-UNVERIFIED IMPLEMENTATION
```

---

# 9. Cross-anchor controls

```text
World4Drive:
one factual future, K candidate futures, factual-mode matching scorer

DA-WAM:
one factual future, N candidate futures,
expert branch direct predictive target + all-branch metric utility scorer

WoTE:
recurrent future BEV sequence + explicit utility

DA-WAM:
0.5s endpoint latent + explicit factorized utility

DynFlowDrive:
candidate-conditioned WM only during training; deployed scorer retains behavior

DA-WAM:
candidate-conditioned future predictor remains online

Drive-JEPA:
JEPA predictive branch removed before planning inference

DA-WAM:
predictive encoder adaptation continues during planner training and predictor remains online
```

---

# 10. Final evidence judgment

```text
PROVES REASONABLY WELL:
- one-to-one candidate↔future-latent conditioning is better than a shared-global future in the matched setup;
- online predictive representation adaptation helps;
- EMA target policy helps;
- expert-proximate hard-negative supervision improves scorer performance;
- a short endpoint latent can be useful as an online utility-scoring feature.

DOES NOT PROVE:
- N candidate futures correspond to N true counterfactual environment futures;
- non-expert future latents are physically faithful;
- surrounding agents react correctly to each ego candidate;
- world prediction is the dominant source of final PDMS;
- NAVSIM validates reactive world-model correctness.
```
