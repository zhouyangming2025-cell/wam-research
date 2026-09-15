# P0012 DA-WAM — Dimension-first Deep Analysis V2

Last updated: 2026-09-15

Status: **COMPLETE FIRST PASS — arXiv v2 paper normalized; official implementation not yet released**

Paper: **DA-WAM: Decision-Aligned Future Latents for Driving World Models**

Canonical research role in this repository:

```text
ONLINE CANDIDATE-SPECIFIC FUTURE-LATENT SCORING
→ ONE FUTURE LATENT PER TRAJECTORY CANDIDATE
→ ONLY EXPERT-MATCHED BRANCH HAS DIRECT FUTURE-LATENT TRUTH
→ ALL BRANCHES RECEIVE FACTOR / UTILITY / RANKING SUPERVISION
```

Do **not** summarize DA-WAM as:

```text
32 candidate trajectories
→ 32 ground-truth counterfactual futures
→ choose the safest true future
```

The paper explicitly says the opposite: offline logs contain only one executed expert trajectory and one observed future. Only the candidate closest to the expert receives dense JEPA future-latent supervision. The other candidate-specific future latents are learned indirectly through downstream factor, utility and ranking objectives.

---

# 0. Source and version contract

Primary paper source:

```text
papers/raw_md/P0012_DAWAM/P0012_DAWAM.raw.md
arXiv:2608.19085v2
v1: 2026-08-19
v2: 2026-08-20
```

Official repository named by the paper:

```text
LeapWM/da-wam
```

Observed repository state on 2026-09-15:

```text
latest commit: 1edbe555146a2d1fe9484f5c11f120860b8a4858
commit date: 2026-08-17
contents: README.md only
README: "comming soon"
```

Therefore:

```text
paper architecture / equations / ablations    PAPER-VERIFIED
implementation / detach / exact tensor path    SOURCE-UNVERIFIED
paper↔code consistency                         NOT AUDITABLE YET
```

No unofficial reproduction is used as implementation evidence.

---

# 1. Executive verdict

DA-WAM combines four mechanisms that must be kept separate:

```text
A. V-JEPA 2.1 predictive representation adaptation
B. candidate-specific action-conditioned future-latent prediction
C. future-latent-conditioned factorized trajectory scoring
D. safety-critical hard-negative / utility / ranking supervision
```

Training graph:

```text
current visual observation X_t
→ online V-JEPA encoder E_theta (+ LoRA)
→ current scene tokens Z_t

observed future X_{t+Δ}
→ EMA target encoder E_bar
→ stop-grad factual future latent Z_{t+Δ}

proposal module
→ N=32 candidate trajectories τ_i
→ trajectory encoder E_tau
→ action embeddings a_i

for every candidate i:
(a_i as query, Z_t as key/value)
→ shared predictor P_phi
→ candidate-specific future latent Zhat_i

only i_exp = argmin ADE(τ_i, τ_exp):
Zhat_i_exp ↔ factual target Z_{t+Δ}
→ dense JEPA prediction loss

all candidates + training-only hard negatives:
(Z_t, a_i, Zhat_i)
→ shared scorer
→ NC / DAC / EP / TTC / Comfort factors
→ utility score
→ factor + score + pairwise ranking losses
```

Inference graph:

```text
current observation
→ online encoder
→ 32 candidate trajectories
→ 32 action embeddings
→ 32 candidate-specific future latents
→ 32 future-latent-conditioned factor / utility scores
→ argmax utility
→ selected trajectory

EMA target encoder       = ABSENT
future observation       = ABSENT
expert matching          = ABSENT
hard-negative retrieval  = ABSENT
```

Canonical subtype:

```text
ONLINE CANDIDATE-SPECIFIC LATENT CONSEQUENCE FEATURES
+ FACTORIZED UTILITY SCORER
```

The phrase `counterfactual world modeling` should be treated cautiously: candidate-specific output exists, but direct counterfactual future truth exists only for the factual/expert-matched branch.

---

# 2. Host planner and candidate support exist before the world model

The paper starts with a proposal module that produces:

```text
N = 32 candidate ego trajectories
8 future ego poses per candidate
```

Each trajectory is encoded as:

```text
τ_i
→ E_tau
→ a_i
```

The future predictor does **not** create the action space. It receives an already generated candidate set.

This is the same causal ordering that must be preserved when comparing against WoTE / WorldDrive / DynFlowDrive:

```text
candidate support quality
→ exists before candidate-specific world prediction
```

Candidate-count ablation:

```text
1 candidate   87.11 PDMS
8             90.76
16            91.89
32            93.68
64            93.68
```

Thus a substantial part of planning quality depends on candidate support / multiplicity. The gain cannot be attributed to future modeling alone.

---

# 3. Current representation: V-JEPA 2.1 + online adaptation

Current scene tokens:

```text
Z_t = E_theta(X_t)
Z_t ∈ R^{M×D}
```

Input in the reported NAVSIM setup:

```text
2 historical front-camera frames
```

The online encoder is initialized from pretrained V-JEPA 2.1. The base network is frozen and LoRA modules are injected into selected Transformer layers.

Crucially, LoRA parameters receive gradients from both:

```text
future-prediction objective
+
trajectory-planning objectives
```

This means the representation is neither:

```text
frozen generic JEPA feature
```

nor:

```text
purely world-prediction feature
```

It is a **decision-adapted predictive representation**.

Horizontal comparison:

```text
Drive-JEPA
JEPA predictor mainly belongs to pretraining; deployed planner uses transferred encoder

DA-WAM
predictive target supervision remains active during planner optimization;
online encoder is task-adapted and its future predictor remains online at inference
```

This is a meaningful lifecycle distinction.

---

# 4. EMA target encoder and future truth

Training target:

```text
Z_{t+Δ} = stopgrad(E_bar(X_{t+Δ}))
```

with:

```text
E_bar ← μ E_bar + (1-μ) E_theta
```

The target branch therefore provides a slowly moving factual future representation.

Reported physical future interval:

```text
Δ = 0.5 s
```

Important distinction:

```text
physical future interval = 0.5 s
JEPA/encoder update dynamics = training optimization dynamics
```

There is no multi-step physical world rollout in the core formulation. The future object is a short-horizon endpoint latent.

---

# 5. Candidate-specific future prediction

For candidate i:

```text
a_i = E_tau(τ_i)
```

The predictor uses:

```text
Q = a_i
K = Z_t
V = Z_t
```

and outputs:

```text
Zhat_i = P_phi(Q=a_i, K=Z_t, V=Z_t)
```

All candidates share the same predictor parameters. Candidate specificity comes from the action query, not from independent world models.

Thus:

```text
32 trajectories
→ 32 predicted future latents
```

is architecture-true.

But:

```text
32 predicted future latents
!=
32 observed counterfactual future truths
```

---

# 6. The central supervision asymmetry

Offline logs contain:

```text
one executed expert trajectory τ_exp
+
one observed future X_{t+Δ}
```

DA-WAM explicitly avoids assigning that future to every hypothetical candidate.

It first computes:

```text
i_exp = argmin_i ADE(τ_i, τ_exp)
```

and applies the dense future-latent prediction loss only to:

```text
Zhat_{i_exp}
```

against:

```text
Z_{t+Δ}
```

Therefore:

```text
expert-matched future branch:
DIRECT factual future-latent supervision = YES

other N-1 branches:
DIRECT future-latent supervision = NO
```

This is one of DA-WAM's strongest methodological improvements over naive multi-branch supervision: it does not falsely label unexecuted alternatives with the factual future.

However, the scientific boundary is equally important:

> avoiding an incorrect label does not create the missing counterfactual label.

The other future latents are still not identified against alternative-action environment outcomes.

---

# 7. What trains the unobserved candidate futures?

The paper states that all candidate future latents participate in downstream scoring losses.

For candidate i:

```text
(Z_t, a_i, Zhat_i)
→ scorer encoder h_i
```

Then the scorer predicts five factors:

```text
NC       no-at-fault collision
DAC      drivable-area compliance
EP       ego progress
TTC      time-to-collision
Comfort
```

and an overall utility score:

```text
s_hat_i
```

Losses:

```text
L_pred    dense future latent, expert-matched branch only
L_factor  planning factors, all candidates
L_score   scalar utility, all candidates
L_rank    pairwise ranking, all candidates
```

Total:

```text
L = λ_pred L_pred
  + λ_factor L_factor
  + λ_score L_score
  + λ_rank L_rank
```

Because scorer losses depend on `Zhat_i`, the paper-level training graph implies that unobserved branches can be shaped by decision supervision.

This creates an important interpretation:

```text
expert branch Zhat
≈ factual predictive latent

non-expert branch Zhat
≈ candidate-conditioned decision feature
   shaped by value/factor/ranking losses
```

The paper does **not** independently prove that every non-expert `Zhat_i` remains a physically faithful future-world representation.

Without released code, exact detach boundaries remain SOURCE-UNVERIFIED, but the stated end-to-end objective implies this downstream gradient route.

---

# 8. Hard negatives are decision supervision, not future truth

DA-WAM retrieves expert-proximate trajectories from an offline trajectory bank subject to:

```text
trajectory distance to expert < ε_geo
AND
safety degradation relative to expert > ε_safety
```

The purpose is to create trajectories that are geometrically close but differ strongly in safety outcome.

Each hard negative:

```text
τ_i^-
→ action embedding
→ its own predicted Zhat_i^-
→ same shared scorer
```

But the paper is explicit:

```text
hard-negative visual future = unobserved
therefore hard negative is EXCLUDED from dense future-feature supervision
```

It still receives:

```text
factor target
utility target
ranking target
```

Thus the phrase `counterfactual safety supervision` refers to **trajectory-level value/safety supervision**, not observed counterfactual world-state supervision.

This is a critical distinction.

---

# 9. Scorer semantics: much closer to WoTE than World4Drive

DA-WAM's deployed score has explicit utility semantics.

It predicts:

```text
NC / DAC / EP / TTC / Comfort
```

and then a learned scalar utility.

Therefore a high DA-WAM score means approximately:

```text
high predicted planning quality under metric-derived supervision
```

not:

```text
high probability that this branch matches the one factual future
```

This makes scorer semantics closer to WoTE:

```text
WoTE:
future BEV sequence → explicit reward/utility heads → argmax

DA-WAM:
candidate future latent → factorized planning metrics + utility → argmax
```

and fundamentally different from World4Drive:

```text
World4Drive ScoreNet
≈ factual-future mode consistency / branch assignment
not an explicit utility decomposition
```

---

# 10. Strongest matched ablation: action alignment is useful, but modest

Table 3 is the strongest matched control because training data, initialization, proposal generator, optimization, checkpoint selection and evaluation protocol are held fixed.

Results:

```text
No Future Prediction          93.31 PDMS
Shared Global Future          92.81
Current-Latent Conditioning   93.25
Action-Conditioned Future     93.46
+ Hard Negatives              93.68
```

Interpretation:

```text
No Future → Action-conditioned future
93.31 → 93.46
+0.15 PDMS

Shared future → action-conditioned future
92.81 → 93.46
+0.65

Action-conditioned → + hard negatives
93.46 → 93.68
+0.22
```

Therefore the evidence supports:

1. merely adding another current-latent path is insufficient;
2. a single shared future can hurt candidate discrimination;
3. candidate-specific future conditioning helps in the matched setup;
4. hard-negative/value supervision contributes at least as much incremental PDMS as candidate-specific future prediction over the strong no-future baseline.

It does **not** support the stronger statement:

```text
world modeling is the dominant source of the final 93.68 PDMS
```

because the no-future planner already reaches 93.31.

---

# 11. Predictive-representation ablation

Table 4 shows multiple independently useful representation/training choices.

Dense prediction objective:

```text
Frozen encoder:
V-JEPA 2.0-style   91.26
Dense 2.1          91.95
+0.69

LoRA encoder:
non-dense          92.74
dense              92.98
+0.24
```

Adaptation under dense objective:

```text
Frozen    91.95
LoRA      92.98
Full FT   92.62
```

Target policy with LoRA + dense objective:

```text
Frozen target    92.98
Separate         93.10
Shared           93.34
EMA              93.68
```

These controls support the paper's representation-adaptation story.

However, they should not be cross-subtracted casually against Table 3 as if all rows isolate the same single factor. The final score bundles:

```text
foundation V-JEPA prior
+
LoRA adaptation
+
dense predictive objective
+
EMA target policy
+
candidate-specific future predictor
+
factorized utility scorer
+
hard-negative supervision
```

---

# 12. Counterfactual vector

DA-WAM should be normalized as:

```text
I01 candidate-specific future output?            YES
I02 alternative-action future supervision?       NO, except factual/expert-matched branch
I03 observed/simulated intervention truth?        NO
I04 reactive other-agent alternative truth?       NO / NOT ESTABLISHED
I05 external intervention-validity evidence?      NO
```

The paper uses `counterfactual` in the architectural sense of hypothetical candidate-conditioned futures.

Project-level interpretation must remain:

```text
candidate-specific latent evidence
!=
identified candidate-specific world consequence truth
```

---

# 13. Training graph vs inference graph

Training-only objects:

```text
future frame X_{t+Δ}
EMA target encoder
expert-matching index i_exp
hard-negative trajectory retrieval
factual future-latent target
```

Online deployment retains:

```text
online V-JEPA encoder
candidate generator
trajectory encoder
candidate-conditioned future predictor
future-latent-conditioned scorer
factor heads
utility head
argmax
```

Thus unlike DynFlowDrive / Metis / Drive-JEPA:

```text
DA-WAM retains the explicit future predictor online.
```

Unlike WorldDrive:

```text
it does not distill a heavy future teacher into a lightweight surrogate;
the action-conditioned predictor itself remains part of selection.
```

---

# 14. Cross-paper comparison

## 14.1 DA-WAM vs World4Drive

Common:

```text
multiple ego candidates
→ candidate/intention-conditioned future latents
→ online future-aware selection
```

Difference:

```text
World4Drive:
one factual future chooses/matches one future mode;
ScoreNet learns factual-mode consistency

DA-WAM:
expert trajectory first identifies factual branch;
only that branch gets future-latent GT;
all branches get metric utility/factor/ranking supervision;
scorer is explicit utility, not factual-mode likelihood
```

DA-WAM is more explicit about the one-factual-future problem but still does not create alternative-future truth.

## 14.2 DA-WAM vs WoTE

Common:

```text
candidate-specific online future information
→ explicit planning factors / utility
→ argmax
```

Difference:

```text
WoTE:
recurrent structured BEV rollout / consequence sequence

DA-WAM:
0.5s endpoint latent from action-conditioned JEPA-style predictor
```

WoTE has stronger temporal consequence rollout; DA-WAM has cleaner one-to-one candidate↔latent scorer conditioning and explicit expert-only future supervision.

## 14.3 DA-WAM vs WorldDrive

```text
WorldDrive:
heavy generative WM teacher
→ distilled future feature
→ online lightweight reranking

DA-WAM:
no heavy teacher/distillation lifecycle;
online predictor directly constructs candidate-specific future latent
```

## 14.4 DA-WAM vs DynFlowDrive

```text
DynFlowDrive:
candidate-conditioned world model TRAINING ONLY
→ world-derived mode label
→ predictor removed

DA-WAM:
candidate-conditioned future predictor TRAINING + INFERENCE
→ future latent enters scorer online
```

## 14.5 DA-WAM vs Drive-JEPA

```text
Drive-JEPA:
predictive JEPA branch belongs mainly to representation pretraining;
deployed planner does not run the JEPA predictor

DA-WAM:
JEPA-style future representation training continues jointly with planning;
action-conditioned predictor remains online
```

## 14.6 DA-WAM vs DriveLaW

```text
DriveLaW:
one shared generative hidden representation
→ directly conditions direct Action-DiT policy

DA-WAM:
N action-specific endpoint future latents
→ N factor/utility scores
→ explicit candidate selection
```

They represent two different world→planning interfaces:

```text
representation-conditioned direct policy
vs
candidate-specific consequence-feature scoring
```

---

# 15. What DA-WAM proves reasonably well

```text
1. In a matched planner, sharing one global future across candidates is worse than
   assigning each candidate its own action-conditioned future latent.

2. Online predictive-representation adaptation with LoRA + dense JEPA supervision
   improves over frozen/non-dense controls in the reported setup.

3. EMA target policy improves the reported matched representation setup.

4. Safety-critical expert-proximate hard negatives improve final scorer quality.

5. A short-horizon latent future can be useful as an online scorer condition
   without RGB/video generation.
```

---

# 16. What DA-WAM does NOT prove

```text
1. It does not provide N factual/counterfactual future world targets for N candidates.

2. It does not establish correct reactive surrounding-agent responses under
   unexecuted ego actions.

3. It does not independently validate physical fidelity of non-expert future latents.

4. It does not show that the +0.37 PDMS from no-future 93.31 to final 93.68
   is dominated by world prediction rather than scorer/hard-negative/value supervision.

5. It does not show longer or recurrent world rollout is unnecessary;
   the core future target is only 0.5 s.

6. NAVSIM evaluation is not reactive closed-loop evidence.
```

---

# 17. Evaluation semantics

Primary planning evidence:

```text
NAVSIM-v1 navtest
NAVSIM-v2 navtest
```

Project-standard label:

```text
NON-REACTIVE DATA-DRIVEN / PSEUDO-SIMULATION PLANNING
```

Reported headline:

```text
NAVSIM-v1  93.7 PDMS
NAVSIM-v2  87.7 EPDMS
```

These establish strong benchmark planning performance under NAVSIM semantics, not reactive intervention-valid world dynamics.

---

# 18. Ontology residue test

DA-WAM strongly reinforces existing dimensions:

```text
E03 candidate-shared predictor parameterization
G01/G03 factual future truth provenance
I01-I05 counterfactual vector
J02/J03 online future computation/consumption
K01-K05 scorer semantics and utility targets
L04 gradient coupling
M01-M03 future-knowledge lifecycle
```

Possible residue:

```text
DIRECT FUTURE-LATENT SUPERVISION COVERAGE ACROSS CANDIDATES
```

But this is already expressible through:

```text
G07 candidate/branch supervision coverage
I02 alternative-action future supervision
```

Decision:

```text
ONTOLOGY V1.3 RETAINED
NO V1.4 FROM DA-WAM
```

---

# Final normalized identity

```text
DA-WAM
=
32-candidate planner
+
V-JEPA 2.1 decision-adapted online encoder
+
shared action-conditioned 0.5s endpoint future predictor
+
one future latent per trajectory candidate
+
expert-matched factual future supervision on exactly one branch
+
metric-derived factor / utility / ranking supervision on all branches
+
expert-proximate safety hard negatives
+
online factorized future-latent scorer
+
argmax selection
```

Canonical subtype:

```text
ONLINE CANDIDATE-SPECIFIC FUTURE-LATENT UTILITY SCORING WAM
```
