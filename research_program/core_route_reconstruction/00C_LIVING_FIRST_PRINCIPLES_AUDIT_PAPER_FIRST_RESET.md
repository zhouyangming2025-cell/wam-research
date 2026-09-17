# Living First-Principles Audit — Paper-First Reset

Status: **APPEND-ONLY RESEARCH MEMORY — NOT AN ONTOLOGY SPEC**  
Continues: `00_LIVING_FIRST_PRINCIPLES_AUDIT.md` and `00B_LIVING_FIRST_PRINCIPLES_AUDIT_CONTINUATION.md`  
Date: 2026-09-17

This continuation records a methodological correction after the provisional causal spine (`M0–M4`) began to risk becoming a new reading frame rather than a discovery result.

Detailed evidence for the first reset batch is in:

`16_PAPER_FIRST_RECONSTRUCTION_SET_A.md`

---

## 38. Major methodological correction: successful self-correction is also evidence of instability

The causal-factorisation work produced useful insights, but repeated full-paper reversals occurred:

- OccWorld was initially compressed as forecast→planner, then full-paper reading showed joint future scene + ego generation;
- Drive-OccWorld was initially compressed as forecast→planning, then full-paper reading exposed repeated forecasting/planning alternation;
- ReWorld was predicted as compiled predictive representation, then full-paper reading showed an online DriveLaW-like Video-DiT-state→Action-DiT path.

Allowing evidence to reverse a judgment is correct research behavior.

However, several material reversals in rapid succession also imply something stronger:

> **the abstraction layer was being stabilized faster than the underlying papers were understood.**

The correct response is not “the framework has now survived corrections.”

The more conservative response is:

> **we do not yet have enough deep paper-level reconstruction to justify treating the framework as a discovery ontology.**

This supersedes the confidence language in Section 37 of `00B`.

`M0–M4` are retained as historical/provisional recurring observations only. They are prohibited as classification prompts in the paper-first reconstruction phase.

---

## 39. Paper-first rule

For the next phase, every small set is reconstructed without admissible route labels.

For each paper, record independently:

1. author-stated scientific problem;
2. training computation;
3. inference/deployment computation;
4. candidate generation and commitment path;
5. world/future objects actually materialized;
6. ego-action↔future dependency;
7. supervision provenance for factual and counterfactual branches;
8. training-only versus retained modules;
9. matched ablations / deletion evidence;
10. unresolved ambiguities.

Only after all papers in the set are reconstructed independently may they be placed side by side.

Even then, the comparison is descriptive first:

- same in what exact sense?
- different in what exact sense?
- is the difference central to the paper's scientific proposition?
- is it only representation substrate, implementation, target provenance, or evaluation semantics?

No new route name is allowed merely because a repeated pattern looks elegant.

---

## 40. Set A selection and why it is adversarial

Set A deliberately chooses five papers that are easy to over-merge under a coarse shell such as:

`candidate → future → score → select`

Papers:

- World4Drive;
- WoTE;
- WorldDrive;
- DA-WAM;
- SafeDrive.

The purpose is not to prove that these papers belong together.

The purpose is to test whether a superficially shared architecture survives deep reconstruction as a meaningful scientific commonality.

---

## 41. Set A result: the common shell is real but radically under-specified

All five can indeed be drawn with some version of an ego alternative, future-related object, and final commitment.

But deep reading shows that this shell hides at least four major kinds of difference.

### 41.1 Candidate birth differs

- World4Drive: trajectory and future latent are born from the same intention-conditioned branch.
- WoTE: candidate planner exists first; world model is added for evaluation.
- WorldDrive: world-pretrained representations help generate candidates, then FAR re-ranks them.
- DA-WAM: proposal candidates feed a deliberately co-adapted candidate-specific future predictor/scorer.
- SafeDrive: a strong ProposalNet generates and prunes candidates before sparse-world reasoning begins.

Therefore “has candidates” is not enough to establish mechanism sameness.

### 41.2 The future object differs in role, not merely substrate

- World4Drive: intention-conditioned future latent endpoint.
- WoTE: recurrent BEV future sequence used for model-based trajectory evaluation.
- WorldDrive: distilled candidate-specific future latent surrogate from a heavy generative WM.
- DA-WAM: planning-adapted candidate-specific future latent whose alternative branches lack direct observed-future supervision.
- SafeDrive: sparse agent-centric interaction world supporting agent×time safety localization.

This is more than RGB/BEV/latent implementation variation.

### 41.3 Counterfactual grounding differs sharply

- World4Drive: one factual future chooses the closest predicted intention branch.
- WoTE: a BEV simulator provides candidate-conditioned future maps and reward targets.
- WorldDrive: heavy TA-DWM provides candidate future latent teacher; PDMS/oracle score provides preference teacher.
- DA-WAM: only expert-matched candidate has direct observed-future latent target; alternatives are shaped through planning losses.
- SafeDrive: candidate-specific safety/value labels exist, but surrounding-agent motion truth is the same logged future reused across ego candidate branches.

Hence the phrase `candidate-conditioned future` hides very different epistemic programs.

### 41.4 World reasoning occupies different positions in the paper's full program

- World4Drive couples physical latent enrichment, intention-conditioned planning, and future branch selection.
- WoTE's core proposition is online model-based trajectory evaluation.
- WorldDrive combines representation inheritance with a distilled online future-aware rewarder.
- DA-WAM centers candidate↔future one-to-one alignment and co-adaptation with scoring.
- SafeDrive centers sparse interaction representation × fine-grained safety reasoning.

This directly invalidates any immediate merge solely from the outer candidate/future/score topology.

---

## 42. Important correction to the earlier E/ResolverProfile judgment

Previous work argued that scorer semantics should probably not be a universal headline axis.

Set A supports that global objection but exposes an overcorrection.

SafeDrive shows that a scoring/reasoning mechanism can itself be a paper's core scientific contribution:

`Sparse world + scene-level safety` does not outperform `BEV + scene-level safety` in the matched ablation, while `Sparse world + fine-grained agent/time safety` produces the key improvement.

Therefore:

> **not suitable as a universal independent axis**

is not equivalent to:

> **always a minor profile**.

A feature may be globally non-orthogonal yet locally route/innovation-defining for a paper or sublineage.

This distinction must be preserved in later reconstruction.

---

## 43. One-paper-one-route is now explicitly rejected as a default assumption

WorldDrive is a clear compositional counterexample.

It deliberately combines at least two planning-facing transfers from its world model:

1. representation inheritance from trajectory-aware generative pretraining;
2. candidate-specific future-latent distillation and future-aware re-ranking.

Removing one does not make the other disappear.

World4Drive also contains at least two co-primary claims:

- richer physical latent world representation;
- intention-aware multi-modal future/planning coupling.

Therefore the project must allow:

`one paper = multiple interacting core mechanisms`

until evidence shows that one bridge dominates.

Any future taxonomy that requires every paper to occupy exactly one leaf is presumptively unsafe.

---

## 44. Revised discipline after Set A

Do not ask yet:

> which route does this paper belong to?

Ask:

> what complete scientific program does this paper implement, and which parts of that program are shared with another paper in an actually consequential sense?

A recurring difference earns promotion only after it survives:

- independent full-paper reconstruction;
- matched/ablation evidence where available;
- pairwise deletion/collapse reasoning;
- replication across more than one local paper set;
- negative controls.

The next proposed local set is:

- Epona;
- DriveLaW;
- Metis;
- ReWorld;
- SimWAM.

Even here, the apparent “coupling debate” is a hypothesis, not an assumed genealogy. Each paper must first be reconstructed independently.
