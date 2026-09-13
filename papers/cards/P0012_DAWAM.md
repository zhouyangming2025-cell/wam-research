# P0012 — DA-WAM

## Metadata

- **Title:** DA-WAM: Decision-Aligned Future Latents for Driving World Models
- **Year:** 2026
- **Authors:** Ruiguo Zhong, Benshan Ma, Xiaolong Chen, Lang Zhang, Mingyue Feng, Yaonong Wang, Pei Liu, Jun Ma
- **Raw MD:** `papers/raw_md/P0012_DAWAM/P0012_DAWAM.raw.md`
- **Official code:** `https://github.com/LeapWM/da-wam`
- **Last scientific review:** 2026-09-13

## 1. Role in our research

Strongest current nearest prior for P2-R on the WAM side. DA-WAM already implements the chain:

```text
candidate ego trajectory
→ candidate-specific predicted future latent
→ candidate-specific scorer
→ trajectory selection
```

Therefore per-candidate future prediction and future-conditioned trajectory scoring are not available as novelty.

## 2. Exact problem

DA-WAM argues that future prediction is only useful for planning if the future representation is decision-informative and aligned one-to-one with the ego action being evaluated.

It targets two failure modes:

1. predictive representation learning is decoupled from planner optimization;
2. multiple trajectory candidates share or weakly associate with future representations, causing prediction–action mismatch.

## 3. System / data flow

```text
current observation X_t
→ online visual encoder Z_t
→ N ego trajectory candidates tau_i
→ action encoding a_i
→ action-conditioned predictor P_phi(Z_t, a_i)
→ candidate-specific future latent Zhat_i
→ shared scorer S_psi(Z_t, a_i, Zhat_i)
→ planning factors + utility score
→ select argmax candidate
```

## 4. Training

The critical supervision asymmetry is explicit in the paper.

Offline logs provide only one observed future: the future corresponding to the executed expert trajectory.

Therefore:

```text
expert-matched candidate
→ direct future-latent target
```

while unexecuted candidates do **not** receive observed counterfactual-future targets. They receive factor / utility / ranking supervision, including safety-critical hard negatives.

This is scientifically important for P2-R because the model predicts counterfactual futures for all candidates without direct observed-future supervision for those alternative actions.

## 5. Inference / planning coupling

Very strong.

At inference, every candidate trajectory is mapped to a distinct future latent and scored jointly with that latent. No future observation or expert prior is required.

This occupies:

```text
action-conditioned world prediction
candidate-specific imagined future
candidate-specific future-conditioned scoring
```

## 6. Evaluation regime

NAVSIM-v1 and NAVSIM-v2.

The reviewed text reports PDMS / EPDMS and controlled ablations among:

- no future prediction;
- shared global future;
- current-latent conditioning;
- action-conditioned future;
- action-conditioned future + hard negatives.

The reviewed evaluation does **not** establish a reactive closed-loop matched-action comparison.

## 7. Observed failures / controlled evidence

### Direct controlled evidence

The matched ablation reports:

- No Future Prediction: PDMS 93.31
- Shared Global Future: 92.81
- Current-Latent Conditioning: 93.25
- Action-Conditioned Future: 93.46
- Action-Conditioned Future + hard negatives: 93.68

This supports the author's prediction–action alignment claim within NAVSIM.

### Not established

No direct evidence in the reviewed text that the same candidate set is ranked differently when surrounding agents are allowed to respond to alternative ego interventions.

## 8. Direct evidence relevant to current hypotheses

### P2R_PRIMARY

**Strong prior-art pressure:** DA-WAM already performs candidate-specific future prediction and candidate-specific scoring.

**Potential unresolved mechanism:** alternative-action future latents lack direct observed counterfactual future targets in offline logs.

**Missing P2-R evidence:** no matched factual/non-reactive versus reactive oracle ranking comparison.

### P3_HOLD

DA-WAM also supports the idea that predictive representations should be shaped by planning objectives and used directly for candidate discrimination. This increases prior-art pressure on broad P3 formulations.

### P1_RETIRED

Only secondary relevance through learned scoring / hard-negative boundaries.

## 9. Counterevidence against P2-R

DA-WAM is the strongest current reviewer attack against any claim that WAMs fail because they do not imagine a separate future for each candidate.

It also shows that candidate-specific imagined futures can improve planning without requiring direct future supervision for every candidate.

Therefore P2-R must focus on **ordering correctness under reactive intervention**, not the mere existence of candidate-specific counterfactual futures.

## 10. Author Claim vs Evidence vs Our Inference

### AUTHOR CLAIM

World-model planning improves when each candidate is evaluated against its own predicted future and when predictive representation learning co-evolves with planner optimization.

### DIRECT EXPERIMENTAL EVIDENCE

Matched NAVSIM ablations show action-conditioned future prediction outperforming no-future, shared-future and current-latent controls; hard negatives provide additional gains.

### OUR INFERENCE

The supervision structure leaves a specific scientific uncertainty: predicted futures for unexecuted candidate actions are not directly checked against their true intervention-dependent environment responses. NAVSIM planning gains do not by themselves validate reactive action-order correctness.

## 11. Prior-art occupancy

**STRONG_NEIGHBOR bordering on DIRECT_OCCUPATION** for architecture-level P2 ideas.

Not direct occupation of the narrow P2-R question because the reviewed evaluation does not measure fixed-state / fixed-candidate factual-vs-reactive ordering inversion.

## 12. Research verdict

```text
STRONG COUNTEREVIDENCE TO BROAD P2
+ STRONGEST CURRENT NEAREST PRIOR FOR NARROW P2-R
```

P2-R survives only if it remains about the correctness of action ordering under reactive intervention, not about candidate-specific future modeling itself.

## 13. Source locations

Primary text:

`papers/raw_md/P0012_DAWAM/P0012_DAWAM.raw.md`

Key sections:

- Abstract / Introduction
- §2.2 Action-Conditioned Driving World Models
- §3.1 Problem Formulation and Framework Overview
- §3.3 Action-Conditioned Counterfactual World Modeling
- Expert Matching for Counterfactual Futures
- §4.3 Ablation Studies / Table 3

## 14. Open questions

1. How sensitive is candidate ranking to errors in unsupervised alternative-action future latents?
2. Do alternative candidate futures represent other-agent behavioral response, or mainly candidate-conditioned scene features useful to the scorer?
3. Is there any hidden / supplementary same-scene intervention-consistency evaluation?
4. How would DA-WAM rank the same candidate set under a reactive simulator that exposes action-dependent other-agent responses?

## 15. Change log

```text
2026-09-13 — GPT-5.6 Sol scientific review for P2-R Round 1
```
