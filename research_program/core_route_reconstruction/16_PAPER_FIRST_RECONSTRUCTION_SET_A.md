# Paper-first reconstruction — Set A

Status: evidence reconstruction only; **no route naming, no ontology update, no M0–M4 assignment**.

Branch context: `research/core-route-reconstruction`

Papers in this set:

1. World4Drive — *End-to-End Autonomous Driving via Intention-aware Physical Latent World Model*
2. WoTE — *End-to-End Driving with Online Trajectory Evaluation via BEV World Model*
3. WorldDrive — *Bridging Scene Generation and Planning: Driving with World Model via Unifying Vision and Motion Representation*
4. DA-WAM — *Decision-Aligned Future Latents for Driving World Models*
5. SafeDrive — *Fine-Grained Safety Reasoning for End-to-End Driving in a Sparse World*

Primary evidence:

- `papers/raw_md/P0046_World4Drive/P0046_World4Drive.raw.md`
- `papers/raw_md/P0045_WoTE/P0045_WoTE.raw.md`
- `papers/raw_md/P0042_WorldDrive/P0042_WorldDrive.raw.md`
- `papers/raw_md/P0012_DAWAM/P0012_DAWAM.raw.md`
- `papers/raw_md/P0002_SafeDrive/P0002_SafeDrive.raw.md`
- SafeDrive source-level clarification: `papers/deep_analysis/P0002_SAFEDRIVE_DEEP_ANALYSIS_V2.md`

---

## 0. Why this audit exists

The previous work repeatedly made the same methodological mistake in different forms:

1. observe a recurring pattern in a small number of papers;
2. give the pattern a name;
3. start reading later papers through that name;
4. interpret ambiguity in favor of the existing pattern;
5. mistake successful projection for evidence that the pattern is a real field-level route.

This document deliberately breaks that loop.

For this set, the old `R/W/E/L` language and the later provisional `M0–M4` language are **not admissible as classification devices**. They may be mentioned only as historical hypotheses that motivated re-reading the papers.

The unit of analysis is the paper's actual program:

- what problem the authors say they are solving;
- what computation occurs during training;
- what computation remains at deployment;
- which intermediate objects are produced;
- how ego action and predicted future depend on one another;
- where candidate trajectories come from;
- where supervision comes from;
- which module actually changes the final committed trajectory;
- what disappears if a claimed core mechanism is removed.

The goal is **not** to make five papers fit one common diagram. The goal is to reconstruct five mechanisms faithfully first, and only then inspect what similarities and differences survive.

---

# 1. World4Drive

## 1.1 The paper's own problem statement

World4Drive is not introduced merely as “a candidate-future evaluator.” Its starting complaint is broader and specifically targets LAW-like latent-world planning:

- latent self-supervision can remove expensive perception annotations;
- but a single latent extracted from raw visual features may lack rich spatial-semantic physical understanding;
- and a single-modal latent/planning path does not represent multi-modal driving intentions well.

The paper therefore tries to solve two intertwined problems:

1. construct a richer *physical* latent world representation without manual perception annotations;
2. make the latent world model explicitly intention-aware so that different plausible driving intentions produce different trajectories and different predicted futures.

This already warns against reducing World4Drive to its last-stage selector.

## 1.2 What is constructed before planning

The current world latent `L_t` is not a plain image feature.

World4Drive injects:

- semantic priors from a vision-language/segmentation foundation model;
- metric depth / 3D positional information;
- temporal aggregation from the previous visual frame.

Separately, an intention encoder derives `K` intention queries from a predefined trajectory vocabulary.

Thus, before future prediction, the system already has two structured ingredients:

```text
current physical-world latent L_t
+
multi-modal intention queries Q_plan^1 ... Q_plan^K
```

## 1.3 How trajectories and predicted futures are coupled

The intention-aware planning queries first interact with the current world latent and produce `K` trajectories:

```text
Q_plan^k + L_t
→ trajectory T^k
```

Each trajectory is then encoded into an action token `A^k`.

The future predictor uses the current world latent together with these action/intention tokens to predict `K` future latents:

```text
(L_t, A^k)
→ predicted future latent L_{t+n}^k
```

This matters: the future branches are not attached to an arbitrary externally produced candidate bank. The candidate trajectory and the future latent are born from the same intention branch.

A faithful deployment-oriented sketch is therefore:

```text
images/history
→ physical world latent L_t

trajectory vocabulary
→ K intention queries

for each intention k:
    intention k + L_t
    → trajectory T^k
    → action token A^k
    → predicted future latent L_{t+n}^k

ScoreNet(predicted future latents)
→ choose k*
→ execute T^{k*}
```

## 1.4 The unusual training signal

Training has access to the factual future observation. The physical latent encoder extracts an actual future latent `L_hat_{t+n}`.

For every intention branch, World4Drive compares:

```text
predicted future latent L_{t+n}^k
vs
actual future latent L_hat_{t+n}
```

The branch whose predicted future is closest to the factual future is selected as `j`.

That selected branch provides three different training signals:

1. its latent distance becomes the reconstruction loss;
2. its index `j` becomes the target for the ScoreNet;
3. its trajectory `T^j` receives expert trajectory supervision.

At inference, the factual future is unavailable. The model therefore uses the learned ScoreNet to predict which intention-conditioned future branch should be selected.

This is more specific than saying “future agreement is a reward.” The factual future creates the training-time identity of the preferred *intention branch*.

## 1.5 What the paper does **not** have

The paper does not have factual counterfactual future observations for all alternative intentions.

Only one actual future occurs in the logged data. The model generates several intention-conditioned future latents and uses closeness to that one observed future to decide which branch is plausible.

Therefore:

```text
multiple predicted alternatives          YES
one factual future target                YES
observed truth for every alternative     NO
```

## 1.6 Core-deletion observations

Deleting only the spatial-semantic priors would weaken physical-world representation, but the intention-aware future branching and selector would still exist.

Deleting only multi-modal intention/future branching would move the method much closer to the LAW-like single-world-latent setting that the paper explicitly criticizes.

This suggests that World4Drive has at least **two co-primary contributions**:

- physical-world representation enrichment;
- intention-aware multi-modal future/trajectory coupling and selection.

Forcing the paper to have exactly one “route-defining module” would already lose part of its own claim.

---

# 2. WoTE

## 2.1 The paper's own problem statement

WoTE starts from a much narrower and more operational question than World4Drive:

> once an end-to-end planner already produces multiple trajectories, how should those trajectories be evaluated safely?

Its main criticism is that current-state trajectory evaluation is insufficient because the safety/value of a trajectory depends on the future caused by executing it.

The paper explicitly positions itself as **model-based online trajectory evaluation**.

## 2.2 Candidate generation precedes world reasoning

WoTE first constructs the current BEV state from sensors and generates/refines trajectory candidates from trajectory anchors.

Only after candidates exist does the BEV world model enter:

```text
current BEV state B_t
→ trajectory candidates tau_1 ... tau_N

for each candidate i:
    (B_t, tau_i)
    → future BEV state sequence
```

This ordering is important. Unlike World4Drive, the candidate branch is not primarily created by an intention-aware world-model branch. WoTE takes a candidate planner and augments it with future-based evaluation.

## 2.3 The predicted future is a recurrent physical-time sequence

For each trajectory candidate, WoTE builds a state-action pair and recurrently predicts multiple future BEV states:

```text
(B_t, a_t^i)
→ (B_{t+1}^i, a_{t+1}^i)
→ ...
→ (B_{t+K}^i, a_{t+K}^i)
```

The Reward Model then receives current plus predicted future BEV states and action embeddings.

This is not merely a single latent endpoint. The temporal sequence itself is used by the evaluator.

## 2.4 What is evaluated online

The reward model predicts two families of quantities:

- imitation reward;
- simulator-derived driving rewards such as collision, drivable-area compliance, TTC, comfort, and progress.

At deployment:

```text
candidate i
→ recurrent predicted future BEV sequence i
→ learned reward vector i
→ aggregate reward
```

The highest-reward trajectory is executed.

The paper's ablation is especially informative:

- trajectory evaluation without predicted future states improves over trajectory prediction alone;
- adding predicted future states improves again;
- finer recurrent future prediction improves further.

So the future rollout is not merely an auxiliary training objective; its online use is directly tested against current-state-only evaluation.

## 2.5 Counterfactual supervision is simulator-supported

WoTE faces the offline-log problem explicitly: logged data contain only one realized future, while the planner wants to evaluate many hypothetical trajectories.

Its answer is to use a BEV traffic simulator during training.

For candidate trajectories, the simulator supplies:

- future BEV semantic maps;
- simulator reward targets.

The learned BEV world model and learned reward model then replace the external simulator at inference.

Thus the lifecycle is:

```text
TRAIN:
    candidate
    → external BEV simulator
    → candidate future map + candidate reward target
    → train world model + reward model

INFERENCE:
    candidate
    → learned BEV world model
    → learned reward model
    → selection
```

This is a materially different supervision program from World4Drive's one-factual-future branch matching.

## 2.6 Core-deletion observations

If future-state prediction is removed but trajectory evaluation remains, WoTE becomes a current-state candidate scorer; the paper reports a clear performance drop.

If trajectory evaluation itself is removed, it collapses toward the underlying multi-trajectory predictor.

Therefore the paper's central proposition survives a strict deletion test:

> evaluate a proposed ego trajectory through its predicted future, not only through the current scene.

The exact reward mixture matters for performance, but the paper's core argument is stronger than any one reward term.

---

# 3. WorldDrive

## 3.1 The paper's own problem statement

WorldDrive does **not** begin from “trajectory evaluation needs future states.”

Its headline problem is a schism between scene generation and motion planning:

- driving world models optimize visual scene generation;
- planners separately optimize motion/action representations;
- therefore the world model's learned dynamics do not automatically transfer into the planner.

The paper's stated philosophy is **representation unification**:

> the latent features capable of generating the future should be the same features used to decide the future.

This makes WorldDrive structurally more composite than a simple candidate-future scorer.

## 3.2 Phase 1: trajectory-aware world-model pretraining

WorldDrive first trains a trajectory-aware diffusion world model (TA-DWM).

Inputs include:

- historical visual latent `f`;
- motion/trajectory embedding `c` derived from a trajectory vocabulary and residual offsets.

The diffusion world model learns:

```text
(history visual representation f, trajectory/motion representation c)
→ future scene latent
```

The important point is not only that trajectories condition generation. The visual encoder and trajectory encoder themselves are optimized inside this generation program.

## 3.3 Phase 2A: representation inheritance into the planner

The downstream planner directly inherits and freezes the visual and trajectory encoders learned by the world model.

The planner then uses:

```text
inherited visual latent
+
inherited motion-anchor embedding
+
ego status
→ top-K trajectory candidates
```

This is already one world-model-to-planning transfer path, before the Future-aware Rewarder is considered.

Therefore any reconstruction of WorldDrive that only writes

```text
candidate → future → score
```

misses one of the paper's headline mechanisms.

## 3.4 Phase 2B: Future-aware Rewarder

The heavy diffusion world model can generate a future latent `z^k` for every trajectory candidate, but doing full diffusion sampling for each candidate is too slow.

WorldDrive therefore trains a lightweight future-scene decoder to predict/distill a candidate-specific feature:

```text
(current visual latent f, candidate motion embedding c^k)
→ distilled future feature z_hat^k
```

During training, `z_hat^k` is aligned with future latents generated by the frozen TA-DWM.

A second decoder lets the candidate embedding query this distilled future feature, and a scalar reward head produces the candidate score.

Inference therefore keeps:

```text
candidate k
→ lightweight candidate-specific future feature
→ future-aware reward
→ selection
```

but removes the expensive diffusion generation process.

## 3.5 The reward target and the future target come from different places

This separation is easy to miss.

The FAR future feature is trained to imitate a future latent produced by the frozen world model.

The scalar preference/reward is trained using trajectory preference pairs based on an oracle driving score (PDMS in the reported implementation).

So two distinct teachers are involved:

```text
future representation target  ← frozen TA-DWM
trajectory preference target  ← oracle driving score
```

Conflating these into one “world-derived value” loses important causal provenance.

## 3.6 Deployment

At inference:

- the representation encoders inherited from TA-DWM remain;
- the planner produces candidates;
- the lightweight FAR predicts candidate-specific future features and scores candidates;
- the heavy diffusion future generator is absent.

Thus WorldDrive retains **two consequences of world-model training** online:

1. inherited vision/motion representations;
2. a distilled candidate-specific future surrogate for re-ranking.

## 3.7 Core-deletion observations

WorldDrive is a warning against requiring every paper to have one single core bridge.

If FAR is removed, the representation-unified planner still remains and still instantiates much of the paper's stated philosophy.

If representation inheritance is removed but FAR is kept, a future-aware re-ranking system still remains, but the paper's main “unify vision and motion representation” thesis is broken.

Therefore WorldDrive appears genuinely **compositional**: at least two world→planning mechanisms are deliberately combined.

A taxonomy that demands exactly one route per paper would distort this paper.

---

# 4. DA-WAM

## 4.1 The paper's own problem statement

DA-WAM begins from a different criticism:

> future prediction is useful only if the predicted future is *decision-informative* and directly changes candidate-level trajectory scoring.

It identifies two failures in prior approaches:

1. predictive representation learning can be stage-separated or frozen, so the latent does not adapt to the needs of planning;
2. predicted future states may be shared, pooled, or only weakly tied to specific trajectory candidates.

Its central design target is therefore a one-to-one correspondence:

```text
candidate i
↔
its own predicted future latent i
↔
its own score i
```

## 4.2 Predictive representation is co-adapted with planning

The current scene is encoded by an online V-JEPA-based encoder.

A momentum/EMA target encoder processes the observed future frame during training only.

Unlike a frozen pretrain→planner pipeline, the online representation is updated during planner optimization through LoRA parameters, so predictive representation and trajectory scoring co-evolve.

## 4.3 Every candidate gets its own future latent

For each trajectory candidate `tau_i`:

```text
a_i = trajectory encoder(tau_i)

(Z_t, a_i)
→ predicted future latent Z_hat_i
```

The scorer then consumes:

```text
current scene Z_t
+ candidate action a_i
+ candidate-specific predicted future Z_hat_i
```

and produces:

- interpretable factor predictions (NC, DAC, EP, TTC, comfort);
- an overall scalar utility.

Deployment selects the maximum utility candidate.

## 4.4 The crucial offline-data asymmetry

DA-WAM predicts a future latent for every candidate, but logged data reveal the actual future only for the executed expert trajectory.

The paper explicitly avoids pretending otherwise.

Only the candidate closest to the expert trajectory receives direct future-feature alignment to the observed future latent.

For all other candidates:

```text
predicted counterfactual future latent
has NO observed counterfactual future feature target
```

Those latent predictions are trained indirectly through factor, utility, and ranking losses.

Hard-negative candidates receive safety/value supervision, but still do not receive observed future-image/latent truth.

This distinction is fundamental when comparing DA-WAM with WoTE:

- both produce candidate-specific future representations online;
- but the counterfactual future supervision program is very different.

## 4.5 Hard negatives are not world-state targets

DA-WAM adds trajectories geometrically close to the expert but with worse safety outcomes.

These hard negatives query their own future latent and pass through the same scorer.

However, their labels supervise planning factors / utility / ranking—not an observed alternative future state.

Therefore:

```text
candidate-specific decision supervision     YES
candidate-specific predicted future latent   YES
candidate-specific observed future truth     NO (except expert-matched branch)
```

## 4.6 Core-deletion observations

The paper includes controlled variants for:

- no future prediction;
- shared/global future;
- current latent;
- action-conditioned candidate-specific future.

That experimental design is unusually well aligned with the paper's central claim.

Removing candidate-specific future correspondence destroys the defining “decision-aligned future” proposition even if a strong candidate scorer remains.

Removing hard negatives or factorized heads weakens safety discrimination, but the main candidate↔future alignment mechanism still exists.

---

# 5. SafeDrive

## 5.1 The paper's own problem statement

SafeDrive is easiest to misread if we focus only on “trajectory-conditioned world model.”

Its actual starting point is safety reasoning.

It criticizes two existing approaches simultaneously:

1. candidate scorers give scene-level safety numbers but cannot localize *which agent* and *which future time* creates risk;
2. dense BEV/occupancy world models do not explicitly organize interaction around the critical entities needed for fine-grained safety reasoning.

The paper's key hypothesis is therefore not simply “predict futures.” It is:

> instance-centric sparse world interaction + fine-grained agent/time safety reasoning is needed for reliable trajectory selection.

## 5.2 A strong candidate planner exists before sparse-world reasoning

ProposalNet already performs substantial work:

```text
sensors/history
→ BEV + object queries
→ 256 trajectory anchors
→ trajectory refinement
→ imitation + scene-level safety scores
→ prune to top K' candidates
```

This means SafeDrive's world reasoning is not the source of all planning competence. It is applied after a strong coarse planner has already proposed and filtered trajectories.

## 5.3 One surviving candidate creates one sparse interaction world

For every surviving ego plan, SafeDrive copies surrounding-instance queries and combines them with that planning query.

Conceptually:

```text
candidate j
→ sparse world j
   {ego plan j + surrounding agent queries}
```

Within each sparse world, self-attention and trajectory-guided future feature sampling refine ego/agent interaction representations and motions.

This object is neither a dense global BEV future nor a single latent endpoint. It is an instance-centric structured interaction world.

## 5.4 Fine-grained safety reasoning is the decision mechanism

FRNet uses the candidate-specific sparse world to predict:

- Pair-wise No Collision: agent × future timestep collision-free probability;
- Time-wise Drivable Area Compliance: future-timestep / ego-footprint compliance.

These fine-grained terms are combined with scene-level planning terms such as imitation, progress, comfort, and TTC.

The final candidate score is therefore explicitly structured around *where*, *when*, and *with whom* risk occurs.

This is not a generic opaque reward head.

## 5.5 Source-level supervision caveat

The released NAVSIM path reveals an important asymmetry.

SafeDrive does have candidate-specific safety/value labels. Each candidate is scored by the training-time PDM/NAVSIM simulator, producing targets including:

- overall safety/value terms;
- which agent causes collision;
- when collision occurs;
- which future ego poses leave drivable area.

However, the surrounding-agent motion targets used by the world branches are still the same logged future reused across different ego candidate branches.

Therefore:

```text
candidate-specific sparse-world branch              YES
candidate-specific safety/value consequence target   YES
candidate-specific reactive other-agent future truth NO
```

This prevents an overclaim that SafeDrive observes a true alternative interactive world for every ego intervention.

## 5.6 Ablation changes the interpretation of the paper

The matched ablation is especially important:

```text
BEV + scene-level safety      ≈ 90.9
Sparse + scene-level safety   ≈ 90.9
Sparse + fine-grained safety   91.6
```

Sparse representation by itself does not explain the main gain.

The strongest evidence supports an interaction:

```text
instance-centric sparse world
×
agent/time fine-grained safety reasoning
```

Therefore treating “sparse world” alone as the paper's route would be misleading.

## 5.7 Core-deletion observations

Remove fine-grained reasoning and SafeDrive loses the mechanism that the paper argues fixes scene-level safety scoring.

Remove the sparse interaction representation while retaining only coarse/BEV safety and the matched ablation shows little advantage.

Thus its core innovation appears to be a **mechanism combination**, not one isolated arrow.

---

# 6. Put the five mechanisms side by side — without classifying them

The following comparisons are observations, not proposed axes.

## 6.1 Where do the candidates come from?

### World4Drive

Candidates are generated inside intention-conditioned branches that are already coupled to future latent prediction.

### WoTE

A trajectory predictor produces/refines candidates first; world-model reasoning is added to evaluate them afterwards.

### WorldDrive

A planner using world-model-inherited vision/motion representations creates top-K candidates; FAR then performs a second future-aware re-ranking stage.

### DA-WAM

A proposal module creates candidates; candidate-specific future prediction and scoring are deliberately co-optimized afterwards.

### SafeDrive

ProposalNet creates, refines, scores, and prunes a large candidate set first. Sparse-world reasoning is reserved for surviving candidates.

**Observation:** writing all five as `candidate → future → score` erases a real difference: in some papers world modeling helps *form the candidate representation itself*; in others it acts mainly after candidate generation; in others both happen.

---

## 6.2 What does “future” mean in each paper?

| Paper | Future object actually used |
|---|---|
| World4Drive | one intention-conditioned future latent at `t+n` per branch |
| WoTE | recurrent sequence of future BEV states/actions over physical time |
| WorldDrive | lightweight candidate-specific future latent surrogate distilled from a heavy diffusion WM |
| DA-WAM | candidate-specific planning-adapted latent future, typically a short fixed horizon |
| SafeDrive | instance-centric sparse interaction world with refined ego/agent future motion and explicit agent×time risk features |

These objects are not interchangeable merely because all can be called “future representation.”

---

## 6.3 Where does counterfactual supervision come from?

This is one of the strongest differences exposed by the deep read.

### World4Drive

```text
one factual future observation
→ choose which predicted intention future is closest
```

Alternative branches do not have observed alternative-future truth.

### WoTE

```text
external BEV simulator
→ per-candidate future BEV supervision
→ per-candidate simulator reward supervision
```

This is the strongest explicit per-candidate future-state teacher among the five.

### WorldDrive

```text
frozen heavy TA-DWM
→ per-candidate future latent teacher

oracle driving score / PDMS
→ preference target for FAR reward
```

Future-feature teacher and decision-preference teacher are different.

### DA-WAM

```text
observed future latent
→ only expert-matched candidate

all candidates
→ factor / utility / ranking supervision
```

Unexecuted candidates have decision supervision but no observed alternative-future target.

### SafeDrive

```text
training-time PDM simulator
→ candidate-specific safety/value labels

logged future agent motion
→ reused across ego candidate worlds
```

Candidate-specific consequence labels exist, but candidate-specific reactive environment truth does not.

**Observation:** “action-conditioned future” is not enough to characterize a method. The epistemic grounding of that future is radically different across papers.

---

## 6.4 What remains online at deployment?

### World4Drive

- physical current world encoder;
- intention-conditioned future latent predictor;
- ScoreNet;
- multi-modal trajectories.

Actual future observations disappear.

### WoTE

- BEV world model recurrent rollout;
- learned reward model;
- candidate trajectory predictor.

External simulator disappears.

### WorldDrive

- encoders inherited from TA-DWM;
- multi-modal planner;
- lightweight future-latent surrogate / FAR.

Heavy diffusion world generation disappears.

### DA-WAM

- online encoder;
- per-candidate future predictor;
- factorized scorer.

EMA target, expert matching, and hard-negative retrieval disappear.

### SafeDrive

- ProposalNet;
- candidate-specific SWNet sparse worlds;
- FRNet fine-grained safety heads.

External PDM scoring used for targets disappears.

**Observation:** all five remove some training-time teacher, but they remove *different levels of the world-model computation*. “Teacher removed at deployment” is therefore not by itself a route.

---

# 7. The superficially similar pairs are not yet justified as the same route

## 7.1 World4Drive vs WoTE

Common surface feature:

```text
multiple ego trajectories
→ trajectory-conditioned future
→ choose one
```

But the paper-level programs differ:

- World4Drive builds multi-modal *intentions* and uses factual-future matching to train a selector over intention-conditioned future branches.
- WoTE starts from an existing multi-trajectory planner and explicitly adds model-based *trajectory evaluation* through recurrent future BEV simulation and reward prediction.

The difference is not merely BEV versus latent.

The role of future reasoning in the planning program is different.

No merge decision is justified yet.

## 7.2 WoTE vs WorldDrive

Both evaluate candidates using future information.

But:

- WoTE keeps the learned recurrent BEV world model online and trains it against simulator-generated future BEV scenarios.
- WorldDrive deliberately removes heavy world generation online, distills future latent foresight into FAR, and simultaneously transfers world-model-trained vision/motion representations into candidate generation.

WorldDrive therefore combines representation inheritance with future-aware re-ranking; WoTE is a cleaner online model-based evaluator.

Again, no merge decision is justified merely from the shared candidate-future-score shell.

## 7.3 WorldDrive vs DA-WAM

Both use a lightweight candidate-specific future latent at inference.

The similarity is real.

However:

- WorldDrive's future surrogate is distilled from a separately pretrained/frozen heavy generative world model, and its encoders are inherited from that model.
- DA-WAM keeps predictive representation adaptation inside planner optimization and gives only the expert-matched branch direct observed-future latent supervision.

Thus one method emphasizes **inherit/distill from a mature world generator**, while the other emphasizes **co-adapt predictive representation and candidate scoring end-to-end**.

Whether that is a route-level split or a learning/program-level split remains open.

## 7.4 DA-WAM vs SafeDrive

Both give each candidate its own future-conditioned representation before final scoring.

But SafeDrive's central scientific claim is explicit fine-grained safety localization over agents and time, using a structured sparse interaction world.

DA-WAM's central claim is one-to-one prediction–action alignment and co-adaptation of the latent with the scorer.

This is a useful warning: two papers can share a causal shell while attacking different scientific bottlenecks.

## 7.5 World4Drive vs DA-WAM

DA-WAM explicitly cites methods such as World4Drive as steps toward future-aware planning, but argues that candidate/future correspondence can still be weak, shared, or insufficiently decision-aligned.

This relationship is more informative than assigning two labels:

```text
World4Drive:
intention-conditioned future branches + factual-future-based branch selection

DA-WAM:
explicit candidate-by-candidate future latent + candidate-specific scorer + co-adaptive predictive learning
```

The later paper is not simply “the same diagram with another scorer”; it is making a scientific claim about stronger action–future identity.

---

# 8. Important correction to the earlier E/ResolverProfile discussion

Previous auditing concluded that `E` should probably not be a universal headline axis because changing a scorer from future agreement to utility to decomposed outcomes often leaves the larger candidate/world interface unchanged.

That conclusion still has force at the **global taxonomy** level.

But this five-paper read adds an essential qualification:

> scorer semantics can still be a paper's core scientific contribution even if it should not be a universal independent axis.

SafeDrive is the clearest case.

Its agent×time safety decomposition is not a cosmetic ResolverProfile. The paper's matched ablations show that sparse-world representation only becomes useful when paired with the fine-grained reasoning mechanism.

Therefore:

```text
“not a universal headline axis”
!=
“always a minor profile”
```

The same distinction may apply to other properties previously pushed into profiles.

This is another reason to stop designing universal axes before paper mechanisms are understood deeply.

---

# 9. What this set teaches about the audit method

## 9.1 Outer topology is necessary but insufficient

`candidate → predicted future → score → select` is a useful observation, but it is far too coarse to establish sameness.

It hides:

- where candidates come from;
- whether world modeling shapes candidate generation itself;
- whether future prediction is recurrent rollout, endpoint latent, distilled surrogate, or structured interaction world;
- how alternative futures are supervised;
- whether the evaluator's structure is itself the scientific novelty.

## 9.2 Author problem statements matter, but are not decisive alone

The paper's own framing helps identify what mechanism deserves deeper scrutiny:

- World4Drive: physical world understanding + multi-modal intention;
- WoTE: online model-based trajectory evaluation;
- WorldDrive: unify generation/planning representations + retain foresight efficiently;
- DA-WAM: decision-aligned candidate-specific futures;
- SafeDrive: fine-grained interaction safety reasoning.

But author framing must still be checked against method equations, lifecycle, and ablations.

## 9.3 One paper may legitimately contain multiple core mechanisms

WorldDrive is the strongest example in this set.

Trying to force one route label per paper would delete either representation inheritance or future-aware re-ranking.

World4Drive also appears to contain at least two co-primary contributions: physical latent enrichment and intention-aware future branching.

Therefore future ontology work must allow:

```text
paper != necessarily one atomic mechanism
```

## 9.4 Counterfactual grounding must be audited separately from architecture

A network can output a different future for every candidate without possessing candidate-specific ground-truth future supervision.

The five papers span several regimes:

- factual-future branch matching;
- simulator-generated alternative futures;
- heavy-WM-generated teacher futures;
- expert-only observed future + indirect planning supervision for alternatives;
- candidate-specific safety labels but logged agent-future truth.

This distinction is scientifically meaningful and must not be erased by the phrase “candidate-conditioned future.”

## 9.5 Deletion tests should target the paper's scientific proposition, not arbitrary modules

A module can be important for performance without defining the paper's main idea.

Conversely, a mechanism can be central even if removing it does not make the whole system unusable because modern papers often combine multiple innovations.

The useful question is:

> after removing X, does the paper still make essentially the same scientific claim?

not merely:

> does performance drop?

---

# 10. Current conclusion — deliberately weak

This set does **not** justify a new route taxonomy.

It justifies five much more faithful mechanism reconstructions and several negative conclusions:

1. The five papers must not be merged solely because all can be drawn as `candidate → future → score`.
2. They also should not be split solely by future representation substrate (BEV vs latent vs sparse world).
3. Counterfactual supervision provenance is a major hidden difference that previous route labels compressed away.
4. A scoring mechanism can be central to a paper even if “scorer semantics” is not a good universal axis.
5. Some papers are intrinsically compositional; forcing one route per paper is unsafe.
6. The provisional `M0–M4` causal spine must remain a historical hypothesis, not an admissible reading frame for the next paper-first set.

The correct next operation is not to name routes from this set.

The correct next operation is another small paper-first set chosen around a **different local scientific dispute**, reconstructed with the same discipline, and only later compare whether any recurring distinction survives across both sets.

Candidate for Set B (not yet executed):

```text
Epona
DriveLaW
Metis
ReWorld
SimWAM
```

This set is attractive because the papers appear to debate world-generation/planning coupling, but that apparent relationship must itself be treated as a hypothesis rather than assumed in advance.
