# P2-R Targeted Failure Deep Read — Round 1

Date: 2026-09-13

Status: **HISTORICAL TARGETED REVIEW — P2-R is parked and this round never established a confirmed gap.** This round uses only primary-text material already present in this private repo.

## 1. Question under test

P2-R is the **Reactive Action-Ordering Gap in Planning-centric WAMs**.

For the same current state `s` and the same ego candidate set `A = {a_i}`, ask whether the candidate ordering obtained from factual / non-reactive futures differs from the ordering under reactive counterfactual futures:

```text
rank_factual/nonreactive(A) ?= rank_reactive(A)
```

The mechanism of interest is narrower than a generic open-loop / closed-loop gap:

```text
ego action
→ surrounding-agent response changes
→ candidate action ordering reverses
→ non-trivial planning regret
```

The following are explicitly **not sufficient** evidence for P2-R by themselves:

- closed-loop is harder than open-loop;
- a planner benefits from interaction modeling;
- an action-conditioned world model exists;
- a reactive simulator improves evaluation;
- prediction metrics correlate imperfectly with planning;
- candidate-specific futures improve a non-reactive benchmark.

## 2. Paper-by-paper audit

### P0002 — SafeDrive

Source: `papers/raw_md/P0002_SafeDrive/P0002_SafeDrive.raw.md`

**PAPER FACTS**

- SafeDrive constructs a separate Sparse World for each retained ego trajectory candidate.
- SWNet jointly refines ego and surrounding-agent future motions inside each candidate-conditioned world.
- FRNet then scores each candidate with pair-wise no-collision and time-wise drivable-area terms.
- It is evaluated on NAVSIM and on the closed-loop Bench2Drive benchmark.
- The paper shows a qualitative case where the highest-scored ProposalNet trajectory collides while FRNet selects a safer alternative.

**WHAT THIS SUPPORTS**

SafeDrive is strong evidence that **candidate-conditioned interaction modeling is already an occupied design direction**. Therefore P2-R cannot be framed as "world models should condition on ego candidates" or "interactive future modeling is missing".

**WHAT IT DOES NOT SHOW**

The paper does not isolate a matched-state / matched-candidate comparison between factual/non-reactive and reactive other-agent futures. It does not directly measure whether the relative ordering of the same candidate set reverses because surrounding agents respond differently to different ego interventions.

**P2-R EFFECT**

- Weakens broad versions of P2.
- Does not kill the narrow action-ordering formulation.
- Provides an important near-neighbor architecture that any later P2-R study must compare against.

---

### P0004 — BeTop

Source: `papers/raw_md/P0004_BeTop/P0004_BeTop.raw.md`

**PAPER FACTS**

- BeTop explicitly supervises future multi-agent behavioral topology and combines it with joint prediction and contingency planning.
- The nuPlan evaluation distinguishes open-loop, closed-loop non-reactive, and closed-loop reactive simulation.
- BeTopNet reports gains in reactive simulation and on a dedicated interactive benchmark.

**WHAT THIS SUPPORTS**

BeTop is a strong counterexample to any claim that logged future supervision or learning-based planning is inherently unable to produce useful reactive closed-loop behavior. It also shows that explicit future-interaction structure can materially improve interactive planning.

**WHAT IT DOES NOT SHOW**

Its evaluation compares planner-level outcomes across regimes, not the ordering of a fixed candidate set under factual/non-reactive versus reactive counterfactual futures. It therefore does not isolate `other-agent reaction → preference reversal` from other differences between evaluation regimes.

**P2-R EFFECT**

- Strongly occupies the generic "reactivity / interaction-aware planning matters" framing.
- Leaves the narrower matched-action ordering question open in the material reviewed here.

---

### P0003 — GraphAD

Source: `papers/raw_md/P0003_GraphAD/P0003_GraphAD.raw.md`

**PAPER FACTS**

- GraphAD iteratively couples predicted future agent trajectories with a dynamic interaction graph.
- The final ego plan is produced by a planning head from the graph-processed ego feature, ego status, and command.
- The paper evaluates planning on nuScenes with displacement error and collision rate.
- An occupancy-based post-optimization step contributes substantially to collision reduction.

**WHAT THIS SUPPORTS**

Future geometry and explicit inter-agent relations are useful planning representations.

**WHAT IT DOES NOT SHOW**

GraphAD does not construct and re-simulate distinct other-agent responses for a fixed set of alternative ego actions before ranking those actions. Its reported planning evaluation is not a reactive matched-action test.

**P2-R EFFECT**

GraphAD is background evidence for interaction relevance, not direct evidence for P2-R.

---

### P0005 — RiskWorld

Source: `papers/raw_md/P0005_RiskWorld/P0005_RiskWorld.raw.md`

**PAPER FACTS**

- RiskWorld performs history-only object-centric latent rollout of future ego-object relations and decodes object-level risk.
- Inference uses observations up to the current time; logged futures supervise training.
- The method is a risk monitor, not a closed-loop planner.
- Its discussion explicitly lists planner-conditioned counterfactual rollouts as future work.

**WHAT THIS SUPPORTS**

Future relation rollout can preserve planning-relevant risk information without reconstructing a full scene.

**WHAT IT DOES NOT SHOW**

There is no candidate ego action input and therefore no `a_1 → W_1`, `a_2 → W_2` intervention comparison. It cannot test action-dependent response or action-order inversion.

**P2-R EFFECT**

RiskWorld defines a useful boundary: relation-aware world modeling alone is not the same as reactive counterfactual planning.

---

### P0012 — DA-WAM

Source: `papers/raw_md/P0012_DAWAM/P0012_DAWAM.raw.md`

**PAPER FACTS**

- DA-WAM predicts a distinct future latent for each ego trajectory candidate and scores each candidate with its corresponding predicted latent.
- The paper explicitly recognizes the offline counterfactual-supervision limitation: only the expert-matched candidate has an observed future latent target.
- Dense future-prediction supervision is therefore applied only to that expert-matched candidate; unexecuted candidates receive factor / utility / ranking supervision rather than observed counterfactual-future targets.
- Action-conditioned future prediction improves NAVSIM planning relative to shared-future and no-future controls in the reported matched ablation.
- Evaluation is on NAVSIM-v1/v2; the reviewed text does not report reactive closed-loop evaluation.

**WHAT THIS SUPPORTS**

DA-WAM is the strongest nearest prior in the current corpus for the WAM side of P2-R. It already occupies:

```text
candidate action
→ candidate-specific imagined future latent
→ candidate-specific score
```

Therefore neither "per-candidate world prediction" nor "action-conditioned future scoring" can be our research novelty.

**UNRESOLVED MECHANISM**

For unexecuted candidates, the model has no direct observed counterfactual future target. The paper demonstrates planning gains, but the reviewed evaluation does not establish whether candidate-specific imagined futures preserve the **true reactive ordering** of alternative ego actions when other agents would respond differently.

**P2-R EFFECT**

- Strong prior-art pressure on solution-side novelty.
- Simultaneously sharpens the surviving scientific question from "can we predict a future per action?" to "is the induced ordering correct under intervention-dependent reactions?"

## 3. Cross-paper adjudication after Round 1

### What is already occupied

The current corpus is sufficient to reject several broad formulations:

```text
"Planning should model interactions."                    OCCUPIED
"Closed-loop/reactive evaluation matters."               OCCUPIED
"World models should be conditioned on ego actions."      OCCUPIED
"Each candidate should receive its own future."           OCCUPIED
"Future information can improve candidate scoring."       OCCUPIED
```

SafeDrive and DA-WAM are especially dangerous if P2-R drifts back toward architecture novelty; BeTop is especially dangerous if it drifts toward generic reactive planning.

### What still survives

The specific variable below remains unmeasured in the five papers reviewed here:

```text
P[ rank_F(A) != rank_R(A) | fixed state, fixed candidate set, interaction-critical regime ]
```

with the causal attribution restricted to:

```text
other-agent response to ego intervention
```

rather than observation shift, controller error, generic temporal compounding, or a changed candidate set.

### Evidence status

**No direct observed P2-R failure has yet been established in this repo.**

The present corpus establishes architecture relevance and strong nearest priors, but not the existence, prevalence, or planning regret of reaction-induced action-order inversion.

Therefore the correct status remains:

```text
P2R_PRIMARY = PRIMARY CANDIDATE, NOT CONFIRMED GAP
```

## 4. Hard kill criteria

P2-R should be killed rather than widened if any of the following holds after targeted literature review / minimal testing:

1. A strong prior already measures matched-state, matched-candidate factual-vs-reactive ordering and substantially resolves the issue.
2. Ordering inversions are rare or produce negligible planning regret in interaction-critical scenes.
3. Apparent inversions are mainly explained by observation shift, control error, changed candidate coverage, or temporal compounding rather than other-agent response.
4. Existing candidate-conditioned methods such as DA-WAM / SafeDrive already preserve reactive ordering under a direct controlled evaluation.
5. The only remaining contribution is a new metric name for an already-established interactive-planning phenomenon.

## 5. Next high-discrimination corpus

The existing Batch 0A corpus is not sufficient for a final verdict. The next review should prioritize the direct papers previously identified for P2-R:

1. BridgeSim — overall OL/CL gap and objective mismatch.
2. ReactSim-Bench — behavior of world agents after AV deviation.
3. CausalDrive — causal/reactive world simulation conditioned on ego trajectory.
4. How Can Driving World Models Do Counterfactual Prediction? — matched counterfactual consistency.
5. CRAFT — counterfactual-to-interactive policy optimization.

Secondary targets: What Truly Matters, Policy World Model, BeyondDrive, ELF-VLA if needed to separate interaction effects from other OL/CL failure mechanisms.

## 6. Decision after Round 1

```text
P2-R SURVIVES ROUND 1 AS A QUESTION, NOT AS A CONFIRMED GAP.
```

No method design is authorized yet. The next step is to attack P2-R with the direct reactive/counterfactual literature above. If that literature already isolates the same ranking variable, or if no direct failure evidence emerges, return `NONE` rather than broadening the problem.
