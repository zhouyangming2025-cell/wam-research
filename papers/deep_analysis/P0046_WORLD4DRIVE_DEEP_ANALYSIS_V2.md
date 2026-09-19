# P0046 World4Drive — Dimension-first Deep Analysis v2

> Paper: **World4Drive: End-to-End Autonomous Driving via Intention-aware Physical Latent World Model**  
> Purpose: re-project World4Drive into the common WAM dimension space and determine what its K predicted futures, selector scores, and planning gains actually mean.  
> Sources: `papers/raw_md/P0046_World4Drive/P0046_World4Drive.raw.md`; `audits/literature/PHASE_C5_WORLD4DRIVE_AUDIT.md`; released-code audit at `ucaszyp/World4Drive@cffb51adeb1f7d02b49c4b74d7262ded62a33ac8` recorded in the audit.  
> Reading rule: every module/design is immediately compared against LAW / WoTE / Epona / WorldDrive rather than discussed only inside World4Drive's own narrative.

---

# 0. Executive verdict

World4Drive is best classified as an **online compact latent foresight planner with factual-mode matching supervision**.

Its deployed planning path is genuinely future-conditioned:

```text
current multi-view observations/history
→ physical world latent L_t
+ intention vocabulary/query
→ K trajectory candidates T^1...T^K
→ K action tokens A^1...A^K
→ K intention-conditioned future world latents L^1_{t+n}...L^K_{t+n}
→ ScoreNet
→ highest-score mode
→ selected trajectory
```

Thus it is materially different from LAW and Epona:

```text
LAW:
future prediction shapes training representation;
future output does not select deployed action.

Epona:
visual future jointly trains shared latent;
planning can run MST→TrajDiT without visual-future generation.

World4Drive:
predicted future latent is directly on the deployed action-selection path.
```

However, its training semantics are **not** equivalent to K counterfactual action-consequence labels. The core supervision is:

```text
K predicted candidate-conditioned future latents
vs
ONE factual future latent extracted from the actually observed future
```

The branch `j` whose predicted latent is closest to that one factual future becomes:

```text
1. the branch receiving latent reconstruction/alignment loss;
2. the target class for ScoreNet;
3. the trajectory mode receiving expert trajectory supervision.
```

Therefore the selector is not cleanly learning an externally defined utility such as collision risk, TTC, or PDMS. Its primary training target is closer to:

> **Which candidate-conditioned future hypothesis is most consistent with the single demonstrated future?**

This forces a major ontology correction:

```text
post-future scorer semantics
!= always utility/value
```

A scorer can represent:

```text
utility/value
factual-demonstration consistency
mode posterior / likelihood
risk/safety
hybrid combinations
```

World4Drive is primarily a **factual-consistency / mode-selection scorer**, even though it is operationally used as a trajectory selector at inference.

---

# 1. What problem does World4Drive actually solve?

The paper combines three concerns that must be separated scientifically:

```text
A. perception-label dependence
B. weak current-scene representation
C. single-modal / non-future-aware trajectory planning
```

Its response is correspondingly three-part:

```text
foundation priors
→ improve current physical latent

intention vocabulary
→ produce multimodal planning modes

latent world predictor + selector
→ use predicted future latent to choose among those modes
```

This is already a warning against attributing the entire system gain to `world modeling`.

The system can improve because of:

```text
better spatial prior
better semantic prior
better temporal state
better candidate support
future-conditioned branch prediction
future-mode selector
```

Each is a separate causal candidate.

---

# 2. Current world state: `L_t` is not learned from dynamics alone

World4Drive's physical latent is constructed from several sources:

```text
multi-view image backbone feature F_t
+
metric-depth prior
+
open-vocabulary semantic pseudo-supervision/prior
+
previous-frame feature through temporal cross-attention
→ L_t
```

The paper explicitly uses a metric-depth model to provide 3D geometry-aware positional encoding and Grounded-SAM / vision-language priors for semantics. Temporal aggregation then forms:

```text
L_t = CrossAttention(F_hat_t, F_hat_{t-1})
```

## 2.1 Dimension correction: representation origin stack

`world latent = latent` is scientifically useless without provenance.

World4Drive's current state is better represented as:

```text
learned image backbone
+ imported depth foundation prior
+ imported semantic/VLM prior
+ short temporal aggregation
```

Compare:

```text
LAW
= planner visual/BEV latent, primarily shaped by host planner + future-latent objective

WoTE
= learned compact BEV state from camera+LiDAR, with semantic future decoding supervision

Epona
= continuous compressed visual latent + historical ego motion summarized by MST

WorldDrive
= CogVideoX VAE prior + driving visual adapter + trajectory-aware WM specialization

World4Drive
= image representation + explicit foundation depth/semantic priors + temporal context
```

Therefore final ontology must separate:

```text
representation substrate
representation semantics
representation origin / imported priors
WM-specific dynamics learning
```

## 2.2 Evidence boundary

If World4Drive improves over LAW, the delta cannot automatically be interpreted as evidence that its future predictor is better. The current state itself is materially stronger before future prediction begins.

The component ablation confirms this: depth/semantic priors alter planning performance independently of the future selector.

---

# 3. Intention system: candidate generation happens before world prediction

World4Drive constructs a large trajectory vocabulary:

```text
V ∈ R^{N×S×2}
N = 8192
```

Trajectories are grouped by high-level command and endpoint clustering produces:

```text
K = 6 intention points per command
commands = left / right / straight
```

The intention query is combined with the ego query:

```text
Q_plan = SelfAttention(Q_ego + Q_I)
```

Then current world latent `L_t` is used to generate K trajectories:

```text
T = MLP(CrossAttention(Q_plan, L_t))
T = {T^1,...,T^K}
```

## 3.1 Critical ordering

The K trajectories exist **before** the K future world latents.

So the system is:

```text
intention prior
→ candidate trajectory generation
→ future prediction per candidate
→ selector
```

not:

```text
world model searches action space by itself
```

This places candidate support as an independent bottleneck.

## 3.2 Horizontal comparison

```text
WoTE
256 K-means anchors → scene-conditioned refinement → future BEV rollout

WorldDrive
256 anchors → first-stage scoring/refinement → top-K → distilled future re-ranking

World4Drive
large vocabulary → 6 command-conditioned intention modes → 6 trajectories → 6 future latents

Epona
no explicit scored candidate bank; diffusion policy directly generates trajectory distribution

LAW
single planner output, not a candidate bank
```

Thus `multimodality` must remain separate from `candidate evaluation` and from `candidate-set breadth`.

---

# 4. Action representation: trajectory becomes the world-model condition

Each predicted candidate trajectory is encoded by an MLP:

```text
A = E_action(T)
A ∈ R^{K×D}
```

The future predictor receives:

```text
current world latent L_t
+
K action tokens A
+
learnable future queries Q_future
```

and predicts:

```text
L_{t+n} = CrossAttention(Q_future, Concat(A, L_t))
```

producing K candidate-specific future latents.

## 4.1 What is shared across branches?

The branches are not K independently trained world models. They are outputs of a **shared predictor architecture**, conditioned by different intention/action tokens.

This yields another useful dimension:

```text
branch parameterization
= independent models / shared transition with different conditions / shared trunk + branch heads
```

World4Drive = shared latent predictor, multiple conditioned modes.

## 4.2 Dynamics semantics

The core predictor is a compact cross-attention mapping rather than:

```text
WoTE recurrent temporal transition
WorldDrive diffusion generation teacher
Epona frame-autoregressive visual generator
```

World4Drive therefore pays very little online imagination depth:

```text
one compact candidate-conditioned latent prediction per mode
```

rather than recurrent/full decoded rollout.

---

# 5. The most important section: what do K future latents actually mean?

The paper's language suggests:

```text
intention A → future world A
intention B → future world B
...
```

Operationally this is true at the output level: each mode receives a different action token and produces a different future latent.

But supervision reveals a weaker epistemic status.

Training has only one factual future observation. That future frame is encoded into:

```text
L_hat_{t+n}
```

For every predicted mode `k`:

```text
d_k = ||L^k_{t+n} - L_hat_{t+n}||^2
```

and:

```text
j = argmin_k d_k
```

Only the nearest mode is treated as the factual matching mode.

Therefore we need three distinct levels:

```text
OUTPUT SEMANTICS
K action-conditioned future hypotheses = YES

SUPERVISION SEMANTICS
K real alternative-action future targets = NO

IDENTIFICATION SEMANTICS
which branch is physically correct under each intervention = NOT ESTABLISHED
```

This makes World4Drive one of the clearest examples of the project principle:

> candidate-specific output != candidate-specific observed counterfactual supervision.

---

# 6. World Model Selector: this is not the same thing as WoTE's reward model

After nearest-future assignment, World4Drive trains a ScoreNet:

```text
S = Softmax(C(L_{t+n}))
```

with focal loss using `j`, the nearest-to-factual-future mode, as the class label.

At inference:

```text
j_hat = argmax_k S_k
→ output T^{j_hat}
```

## 6.1 What ScoreNet is explicitly supervised to predict

It is not given direct targets such as:

```text
collision probability
TTC
comfort
progress
PDMS
human preference
```

Instead, its class target means:

```text
which predicted future latent was closest to the one observed future latent during training
```

Therefore its most defensible semantics are:

> **factual-future consistency / demonstrated-mode classification**

rather than a general environment utility function.

## 6.2 Why the distinction matters

Suppose two trajectories are both safe:

```text
A = continue behind slow car
B = safe lane change
```

If the logged expert chose A, the factual future corresponds to A.

A demonstration-matching selector tends to learn:

```text
A is the mode most consistent with observed expert future
```

A true utility model would instead ask:

```text
how safe/efficient/legal/comfortable is A?
how safe/efficient/legal/comfortable is B?
```

Those are different learning problems.

## 6.3 New mandatory ontology dimension: scorer semantics

Post-future scoring must be classified as:

```text
utility/value score
risk/safety score
imitation/expert-likeness score
factual-consistency / mode-posterior score
hybrid score
```

Current anchors:

```text
WoTE
= explicit utility/reward semantics: imitation + NC/DAC/TTC/comfort/progress

WorldDrive FAR
= hybrid: future-latent distillation + PDMS preference ranking

World4Drive
= factual-consistency / mode classification from one observed future
```

This is a major correction to the earlier broad category `future → score`.

---

# 7. Training objective couples mode assignment, future reconstruction, and trajectory imitation

For selected branch `j`:

```text
L_recon
= align selected predicted future latent with factual future latent

L_score
= focal loss teaching ScoreNet that j is the preferred mode

L_traj
= L1 expert trajectory supervision for T^j

L_sem
= semantic supervision from foundation-generated pseudo labels
```

Total loss:

```text
L = αL_sem + βL_recon + γL_score + ηL_traj
```

with the reported weighting:

```text
α=.2, β=.2, γ=.5, η=1.0
```

## 7.1 Self-reinforcing latent assignment loop

A subtle but important mechanism is:

```text
model predicts K future modes
→ model chooses nearest mode to factual future
→ only that mode gets factual latent alignment
→ same mode index becomes ScoreNet class
→ same mode trajectory gets expert L1 supervision
```

The latent predictor therefore participates in generating its own mode assignment target.

This is conceptually related to winner-take-all / latent assignment in multimodal prediction, not to supervised counterfactual consequence labels.

## 7.2 New dimension: mode-assignment mechanism

For multimodal WAMs, record how branch identity is established:

```text
fixed semantic mode labels
nearest expert trajectory
nearest factual future latent
simulator value ranking
learned assignment / EM-like
oracle best-of-N
```

World4Drive = **nearest factual future latent assignment**.

This dimension did not appear cleanly in LAW/Epona and is only indirectly present in candidate planners such as WoTE/WorldDrive.

---

# 8. Counterfactual ladder: World4Drive occupies different levels depending on what is measured

Using the provisional ladder:

```text
CF0 no action-conditioned future
CF1 single action-conditioned factual future
CF2 multiple candidate-conditioned model futures
CF3 candidate-specific ego simulation under fixed logged agents
CF4 reactive simulator alternative futures
CF5 externally validated intervention-response correctness
```

World4Drive should not be assigned one single level.

## 8.1 Output form

```text
K candidate-conditioned future latent outputs
≈ CF2
```

## 8.2 Training supervision

```text
one observed factual future latent
no K matched alternative-action futures
```

So supervision does not establish CF3/CF4.

## 8.3 Other-agent reactivity

No matched evidence demonstrates that surrounding agents in each latent branch respond correctly to the ego intervention.

Therefore:

```text
reactive counterfactual validity = NOT ESTABLISHED
```

## 8.4 Scientific consequence

World4Drive is an online imagination mechanism, but `imagination` here should not be automatically upgraded to `causal counterfactual simulation`.

---

# 9. Strongest matched ablation: what World4Drive actually proves

The most useful component table is not the SOTA table.

The crucial matched comparison is:

```text
physical priors + intentions, without WM   0.61 L2 / 0.36 collision
physical priors + intentions + WM          0.50 L2 / 0.16 collision
```

This is strong evidence that the **whole future-latent + selector mechanism** adds value beyond merely generating six intention-conditioned trajectories.

It directly attacks a simpler explanation:

```text
"the improvement is only because World4Drive has multimodal trajectory candidates"
```

## 9.1 What this ablation does NOT isolate

The added `WM` block combines:

```text
future latent prediction
+
nearest-factual latent mode assignment
+
ScoreNet classification
+
reconstruction coupling
```

Therefore the result does not tell us whether the gain comes from:

```text
more physically accurate future dynamics
better latent-mode separation
an expert-demonstration matching classifier
extra regularization
```

These remain competing explanations.

## 9.2 Intention contribution

The reported single-modal vs intention-aware comparison:

```text
0.61 / 0.30
→ 0.55 / 0.25
```

supports that multiple intention modes help the WM/planner stack.

But again:

```text
more trajectory modes
!=
more true future-world modes
```

unless alternative-future supervision exists.

---

# 10. Representation-prior attribution: imported physical knowledge is not world-dynamics evidence

World4Drive claims improved physical-world understanding, but its `physical` latent deliberately imports strong priors:

```text
metric depth foundation model
Grounded-SAM / VLM semantics
```

These may improve:

```text
current geometry
object awareness
road/scene semantics
planning convergence
```

before any future dynamics are learned.

This mirrors WorldDrive's generic-pretraining lesson:

```text
WorldDrive:
generic CogVideoX prior must be separated from TA-DWM-specific gains

World4Drive:
foundation depth/semantic prior must be separated from future-latent WM gains
```

Therefore ontology v1 needs a stable evidence field:

> **strongest matched control immediately before the claimed WM mechanism is added**

For World4Drive, the cleanest WM control is the matched `physical priors + intentions ± WM` comparison, not LAW vs World4Drive headline numbers.

---

# 11. Future-knowledge lifecycle: World4Drive provides the fifth distinct pattern

The five anchors now give:

```text
LAW
future prediction → auxiliary training signal
→ no future consumed in deployed selection

Epona
visual-future loss → shared historical representation
→ planning uses direct generative TrajDiT policy
→ visual future optional/off in planning

WoTE
learned compact transition model
→ remains online
→ recurrent candidate future sequence → reward → selection

WorldDrive
heavy generative WM
→ frozen consequence teacher
→ distilled compact future surrogate
→ online future reward/ranking

World4Drive
compact candidate-conditioned latent predictor
→ remains online directly
→ future-mode ScoreNet
→ selection
```

World4Drive's lifecycle is therefore:

> **direct online compact latent foresight — no heavy teacher and no explicit distillation stage.**

This makes it a useful deployment midpoint between:

```text
WoTE = richer recurrent BEV future, more online transition depth
WorldDrive = expensive future learned offline, lightweight surrogate online
```

---

# 12. Planning-compute frontier

World4Drive reasons over only six intention modes and predicts one compact future latent per mode.

This is computationally very different from:

```text
WoTE
256 candidate branches × recurrent BEV transition

WorldDrive
256 first-stage candidates → top-K → lightweight future surrogate

Epona
no candidate scoring bank; diffusion policy sampling
```

This suggests a general planning compute law:

```text
online planning cost
≈ candidate breadth
× future representation richness
× rollout depth
× transition-model cost
× scoring cost
```

World4Drive chooses:

```text
small K
compact latent
single future endpoint
shared predictor
lightweight classification
```

which is an aggressive low-cost point in this design space.

The scientific question is not whether this is "better" generally, but what decision-relevant information is lost by such compression.

---

# 13. Safety/risk semantics: World4Drive is future-aware without explicit value semantics

World4Drive's world latent may contain safety-relevant information, and its collision metric improves strongly in the matched WM ablation.

But the training target does not explicitly encode:

```text
collision risk
TTC
uncertainty
severity
comfort
progress
```

Unlike WoTE, there is no explicit decomposed safety/utility head.

Therefore:

```text
future-aware = YES
explicit risk/value semantics = NO
```

This matters for later research analysis: risk need not be a channel inside the world state, but World4Drive also shows that future matching alone does not tell us what the selector values beyond resemblance to demonstrations.

Do **not** turn this into a research gap yet; other anchors and prior art must be checked first.

---

# 14. Strongest cross-paper comparison

| Dimension | LAW | WoTE | Epona | WorldDrive | World4Drive |
|---|---|---|---|---|---|
| primary future role | training representation shaping | online consequence | joint representation shaping / visual simulation sibling | representation inheritance + distilled foresight | online compact latent foresight |
| explicit action candidates | no | 256 | no scored bank | 256 → top-K | 6 intentions |
| future model at inference | not consumed | yes, recurrent BEV | visual future optional/off | distilled surrogate, heavy teacher removed | yes, compact latent predictor |
| future object | planner latent | BEV state sequence | visual next-frame latent/image | distilled future latent | one latent future per intention |
| selector semantics | N/A | explicit imitation + simulator utility | N/A | PDMS/preference-informed reward | factual-future mode classification |
| consequence/value separation | N/A | explicit | N/A | explicit teacher + reward model | partially collapsed through mode assignment + ScoreNet |
| alternative-future truth | no | simulator/semantic targets; audited logged-agent limitation | no candidate alternatives | learned teacher futures | one factual future for K hypotheses |
| counterfactual output | one | many | not candidate evaluator | many teacher/surrogate futures | many latent hypotheses |
| counterfactual supervision | factual | non-reactive alternative ego targets in audited path | factual trajectory/video data | learned-teacher alternatives + oracle preference | one factual latent only |
| current representation prior | host planner | BEV camera+LiDAR | compressed visual + history | CogVideoX + TA-DWM | depth + semantic foundation priors |
| strongest matched WM evidence | ± future latent task | evaluator ± future states | trajectory-only vs joint visual training | future-feature rewarder vs trajectory-only rewarder | physical+intentions ± WM selector |

---

# 15. What World4Drive changes in the ontology

World4Drive confirms several existing axes and forces at least six refinements.

## W4D-D01 — scorer semantics

```text
utility/value
risk/safety
imitation/expert-likeness
factual-consistency / mode posterior
hybrid
```

World4Drive = factual-consistency / mode-selection scorer.

## W4D-D02 — mode-assignment mechanism

```text
nearest factual future latent
```

Branch supervision must record how a multimodal mode acquires its identity/target.

## W4D-D03 — output counterfactuality vs supervision counterfactuality

World4Drive proves these cannot be one field.

```text
output: K candidate-specific futures
supervision: one factual future
```

## W4D-D04 — endpoint future vs rollout sequence

World4Drive predicts a compact future latent at a selected offset; WoTE consumes a recurrent future sequence. This must remain explicit.

## W4D-D05 — branch parameter sharing

K modes arise from one shared conditioned predictor, not K independent dynamics models.

## W4D-D06 — self-generated target assignment / winner-take-all coupling

The predicted modes are compared to factual future to choose which mode receives reconstruction, selector, and trajectory supervision. This creates a distinct optimization topology from externally labeled action-value supervision.

---

# 16. Claim–evidence boundary

## Claim A — intentions improve planning

**Direct evidence:** matched component table shows improvement from single-modal WM to intention-aware WM.  
**Interpretation:** multimodal motion structure helps.  
**Unproven:** whether the improvement is specifically due to more causally valid alternative futures.

## Claim B — world model helps select better trajectories

**Direct evidence:** with physical priors + intentions held present, adding the WM/selector improves L2 and collision strongly.  
**Interpretation:** future-latent/selector machinery adds planning value beyond candidate multimodality.  
**Unproven:** whether the gain is from accurate world dynamics versus factual-mode classification/regularization.

## Claim C — model imagines worlds under different intentions

**Direct evidence:** architecture outputs K action-conditioned future latents.  
**Interpretation:** branch-specific latent imagination exists computationally.  
**Unproven:** real counterfactual correctness for unexecuted actions and surrounding-agent response.

## Claim D — physical latent improves world understanding

**Direct evidence:** depth/semantic priors improve matched planning configurations and convergence.  
**Interpretation:** imported spatial-semantic priors are useful.  
**Unproven:** that the gain arises from learned temporal world dynamics rather than stronger current perception features.

---

# 17. Final scientific placement

World4Drive should not be summarized as merely:

```text
latent world model + multimodal trajectories
```

Its more precise placement is:

> **A compact online candidate-conditioned latent predictor whose multimodal branches are anchored to one factual future through nearest-latent assignment, with a deployed ScoreNet trained to identify the factual-consistent mode.**

Its real contribution to the field is twofold:

```text
1. it moves latent future prediction from training-only representation shaping into the deployed trajectory-selection loop;
2. it demonstrates a cheap six-branch latent-foresight design that avoids decoded/recurrent world rollout.
```

Its main scientific limitation is equally precise:

```text
multiple future outputs
!=
multiple intervention-grounded future labels
```

and its ScoreNet is not equivalent to an explicit utility/value function.

---

# 18. Consequence for the five-anchor synthesis

With World4Drive complete, the five-anchor discovery set is now sufficiently diverse to freeze **ontology v1** provisionally:

```text
LAW          = predictive training teacher
WoTE         = online consequence → explicit utility
Epona        = shared world representation → direct generative policy
WorldDrive   = WM representation inheritance + distilled consequence/value
World4Drive  = online compact latent foresight + factual-mode selector
```

Next step must be:

```text
merge/split all provisional dimensions
→ WAM_DIMENSION_ONTOLOGY_V1.md
→ audits/research_synthesis/WAM_PLANNING_INTERFACE_FRAMEWORK.md (provisional five-question review)
```

Do not resume new-paper acquisition before this synthesis is complete.
