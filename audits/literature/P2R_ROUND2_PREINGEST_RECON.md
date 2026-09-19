# P2-R Round 2 — Pre-ingest Reconnaissance

Date: 2026-09-13

Status: **ABSTRACT / PROJECT-PAGE RECONNAISSANCE ONLY**. This is not a deep read and must not be used as a final scientific verdict. Full papers must be ingested and read before upgrading claims.

Purpose: rank the targeted papers by discrimination value and identify what each can or cannot answer before spending deep-read effort.

## 1. A4 — How Can Driving World Models Do Counterfactual Prediction?

arXiv:2608.11601

### Public abstract-level claim

The paper argues that direct action-conditioned prediction may generate a plausible future without preserving the factual episode-specific continuation. It formalizes counterfactual prediction using abduction–action–prediction and constructs matched factual/counterfactual outcomes.

### Important scope boundary

The abstract explicitly studies a **short-horizon setting where the alternative ego action does not alter how surrounding agents evolve**.

This is crucial: the paper is highly relevant to counterfactual correctness, but its controlled setting intentionally removes the very reaction mechanism central to P2-R.

### Current implication

- Strong pressure against naive "action-conditioned prediction = correct counterfactual" assumptions.
- Does **not**, at abstract level, directly establish reaction-induced action-order reversal.
- May provide the cleanest causal language and benchmark design ideas for separating factual evidence from counterfactual prediction.

### Deep-read question

Can its abduction/action/prediction framework be extended conceptually to reactive-agent interventions, and does the paper discuss that boundary explicitly?

---

## 2. A2 — ReactSim-Bench

arXiv:2606.14058

### Public abstract/project-level claim

The benchmark is designed specifically to evaluate whether behavior world-model agents respond feasibly when the AV deviates from logged behavior. It decouples AV control from world-agent control and evaluates 2,636 scenarios across longitudinal, directional and lateral AV deviations.

### Current implication

This is the **closest direct benchmark evidence** for the reaction leg:

```text
ego deviation → surrounding-agent response quality
```

However, the public description evaluates safety, feasibility and compliance of world-agent reactions, not ego candidate preference ordering.

### Deep-read question

Does the benchmark expose paired outcomes that would allow the same ego action set to be ranked under log replay vs reactive agents, or is it purely simulator-quality evaluation?

---

## 3. A1 — BridgeSim

arXiv:2604.10856

### Public abstract-level claim

BridgeSim analyzes the open-loop to closed-loop gap and attributes it to two causes: observational domain shift and objective mismatch. The authors argue that objective mismatch creates a structural inability of open-loop policies to model complex reactive behaviors and temporal effects, and that standard OL evaluation has blind spots.

### Current implication

BridgeSim is a major threat to any framing of P2-R as simply "OL objectives miss reactive CL behavior". That broad idea is already directly occupied.

At abstract level, it does not yet show whether the authors isolate **fixed-action-set ordering reversals caused specifically by other-agent reaction**.

### Deep-read question

What exactly is the claimed biased Q-value estimator, how are reactive dynamics represented in their analysis, and do they measure preference/ranking changes for matched actions or only policy-level CL degradation?

---

## 4. A5 — CRAFT

arXiv:2605.04470

### Public abstract/project-level claim

CRAFT frames dense counterfactual supervision as a proxy for real closed-loop advantages and adds grounded residual correction from true interaction-critical closed-loop events. The paper explicitly states that counterfactual fine-tuning inherits bias from imperfect future estimates while closed-loop RL provides grounded executed-action feedback but sparse informative events.

### Current implication

CRAFT is potentially strong evidence that:

```text
counterfactual proxy value != real interactive closed-loop value
```

This is conceptually close to P2-R, though it may operate at policy-gradient/advantage level rather than fixed-candidate ordering.

### Deep-read question

How is counterfactual advantage constructed, what exactly creates proxy bias, and is any bias decomposed into agent reaction versus other closed-loop effects such as state-distribution shift and temporal compounding?

---

## 5. A3 — CausalDrive

arXiv:2606.15341

### Public abstract-level claim

CausalDrive removes future NPC layouts and conditions on an initial frame, ego trajectory and macro text prompt, claiming this forces the model to predict causal interactions and enables diverse counterfactual reactions under the same ego action. It targets real-time reactive world simulation and downstream closed-loop evaluation / RL.

### Current implication

CausalDrive strongly occupies generic "reactive action-conditioned generative world model" novelty.

But the abstract emphasizes generative simulation realism/control, not matched action-ranking correctness for planning.

### Deep-read question

How are reactions supervised and validated? Are they causally grounded or primarily judged by realism/collision artifacts? Does downstream policy improvement show decision correctness, or only utility of a better simulator?

---

## 6. Historical controls — pre-ingest rationale

### H3 Bahram et al. 2016

Public metadata/abstract states that the method explicitly models other drivers' replanning capabilities and incorporates expected reactions of traffic participants into cooperative planning. This makes it a high-value historical warning against claiming that "planning should account for how others react to ego plans" is new.

### H1 GameFormer (ICCV 2023)

Public paper/project text describes hierarchical game-theoretic interactive prediction and joint prediction/planning. Its project page also notes that some closed-loop demonstrations replay other agents from logs / use non-reactive agents, which is itself useful for distinguishing interaction modeling from reactive evaluation.

### H2 M2I (CVPR 2022)

Public paper text factorizes interacting agents into influencer and reactor and predicts the reactor conditionally on influencer motion. This is a direct conceptual precedent for conditional response modeling, though not a planning-centric WAM.

## 7. Pre-ingest pressure ranking

Based only on public abstracts/project pages:

```text
Most likely to directly threaten P2-R broad framing:
BridgeSim ≈ CRAFT

Most direct evidence on reaction quality:
ReactSim-Bench

Strongest threat to "action-conditioned = counterfactual" assumption:
Counterfactual Prediction

Strongest occupation of reactive generative-WM solution space:
CausalDrive

Strongest historical novelty control:
Bahram 2016 + GameFormer + M2I
```

## 8. What we still do NOT know

No public abstract reviewed here yet establishes the full P2-R chain:

```text
fixed state
+ fixed ego candidate set
+ intervention-dependent surrounding-agent response
→ direct action-order reversal
→ quantified planning regret
```

This absence at abstract level is **not evidence of a gap**. It only justifies full-paper deep reading.

## 9. Next action

Ingest A1–A5 + H1–H3 according to `state/TARGETED_READING_QUEUE.md`, then replace this reconnaissance with primary-text deep analyses and a Round-2 adversarial audit; do not create a parallel paper-card layer.
