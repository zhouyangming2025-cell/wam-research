# P0002 — SafeDrive

## Metadata

- **Title:** SafeDrive: Fine-Grained Safety Reasoning for End-to-End Driving in a Sparse World
- **Year:** 2026
- **Authors:** Jungho Kim, Jiyong Oh, Seunghoon Yu, Hongjae Shin, Donghyuk Kwak, Jun Won Choi
- **Venue:** CVPR 2026
- **arXiv:** 2602.18887
- **Canonical PDF:** local/NAS only — `papers/pdf/P0002_SafeDrive.pdf`
- **Raw MD:** `papers/raw_md/P0002_SafeDrive/P0002_SafeDrive.raw.md`
- **Evidence level:** DOCUMENT_VERIFIED
- **Last scientific review:** 2026-09-13

## 1. Role in our research

Strong nearest prior for candidate-conditioned interaction modeling and explicit safety-based trajectory selection. SafeDrive is especially important because it prevents P2-R from degenerating into the broad claim that planners should build a separate future world for each ego candidate.

## 2. Exact problem

SafeDrive targets coarse, scene-level safety evaluation in end-to-end planning. The paper argues that a trajectory should be evaluated with explicit agent- and timestep-level safety reasoning over a trajectory-conditioned sparse future world.

## 3. System / data flow

```text
camera + LiDAR + ego / scene state
→ ProposalNet
→ safety-aware ego trajectory candidates
→ for each retained candidate: candidate-conditioned Sparse World
→ SWNet jointly refines ego + surrounding-agent futures
→ FRNet computes PwNC + TwDAC + planning factors
→ weighted candidate score
→ select final trajectory
```

The critical architectural fact is that each retained ego trajectory candidate receives its own sparse world.

## 4. Training

The total objective combines detection/motion, BEV segmentation, planning, pair-wise no-collision, time-wise drivable-area compliance and scene-level safety losses.

Important limitation for P2-R: the reviewed text demonstrates trajectory-conditioned world construction but does not establish direct ground-truth supervision for alternative ego interventions paired with the corresponding real surrounding-agent reactions.

## 5. Inference / planning coupling

Strong and explicit.

- Candidate trajectories are generated and filtered first.
- SWNet constructs an independent sparse world for each retained candidate.
- Ego and surrounding-agent motions are jointly refined inside that world.
- FRNet evaluates candidate-specific future interactions.
- The final plan is the candidate with the highest integrated safety / planning score.

Therefore:

```text
candidate action → candidate-conditioned world → candidate score
```

is already occupied prior art.

## 6. Evaluation regime

- NAVSIM: predictive / non-reactive planning metrics (PDMS / EPDMS).
- Bench2Drive: CARLA-based closed-loop evaluation.

The paper reports 66.8 Driving Score on Bench2Drive and strong NAVSIM safety metrics.

Important distinction: planner-level closed-loop success does not by itself show that the ordering of a fixed candidate set changes specifically because other agents react differently to alternative ego actions.

## 7. Observed failures

### Direct qualitative failure inside SafeDrive's own pipeline

The paper shows a qualitative case where the highest-scored trajectory from ProposalNet collides, while FRNet identifies the risk using fine-grained pair-wise / temporal reasoning and selects a safer alternative.

This is a real failure of coarse scene-level evaluation.

### Not established

No direct matched-state / matched-candidate factual-vs-reactive action-order inversion is reported in the reviewed text.

## 8. Direct evidence relevant to current hypotheses

### P2R_PRIMARY

**Strengthens relevance:** surrounding-agent futures are explicitly conditioned on ego candidate motion, so action-dependent interaction modeling is planning-relevant.

**Weakens novelty:** candidate-conditioned world modeling and candidate-specific safety evaluation already exist.

**Does not prove:** that factual/non-reactive future assumptions systematically reverse ego-action ordering relative to a reactive counterfactual oracle.

### P3_HOLD

SafeDrive supports the broader idea that compact interaction-centric representations can be more useful for planning than dense scene representations, but it does not establish a general decision-sufficiency principle.

### P1_RETIRED

Only indirect relevance; not a primary P1 paper.

## 9. Counterevidence against our current P2-R framing

SafeDrive is a strong reviewer citation against any statement like:

```text
"current planners do not model action-conditioned reactions"
```

or:

```text
"a separate future should be predicted for every ego candidate"
```

It also shows strong closed-loop performance, so "logged-data-trained interaction models cannot work reactively" is too broad.

## 10. Author Claim vs Evidence vs Our Inference

### AUTHOR CLAIM

Trajectory-conditioned sparse worlds plus fine-grained agent/timestep safety reasoning improve safety and planning robustness.

### DIRECT EXPERIMENTAL EVIDENCE

- strong NAVSIM PDMS / EPDMS;
- closed-loop Bench2Drive improvement;
- component ablations;
- qualitative case where coarse candidate scoring collides and FRNet selects a safer alternative.

### OUR INFERENCE

SafeDrive occupies the architecture-level solution space near P2-R but does not isolate the scientific variable `rank_F(A) != rank_R(A)` under a fixed candidate set and reactive other-agent interventions.

## 11. Prior-art occupancy

**STRONG_NEIGHBOR** for P2-R.

It would become closer to `DIRECT_OCCUPATION` only if it directly evaluated matched candidate ordering under factual/non-reactive versus reactive counterfactual futures. That evidence has not been found in the reviewed text.

## 12. Research verdict

```text
COUNTEREVIDENCE + STRONG_NEIGHBOR
```

SafeDrive weakens broad P2 formulations but does not currently kill the narrow Reactive Action-Ordering Gap.

## 13. Source locations

Primary text:

`papers/raw_md/P0002_SafeDrive/P0002_SafeDrive.raw.md`

Key sections:

- Abstract / Introduction — trajectory-conditioned Sparse World framing
- §3.2 ProposalNet
- §3.3 Sparse World Network
- §3.4 Fine-grained Reasoning Network
- §3.5 Loss Function
- §4.3 Performance Comparison
- §4.4 Ablation / qualitative PwNC analysis

Canonical local PDF hash (Python logical-byte view):

`77b057a6687abd7f080eaf29fc58b99e0f8dcf401a866928ae4fe56be8429290`

## 14. Open questions

1. What exact supervision makes surrounding-agent futures change across alternative ego candidates?
2. Does Bench2Drive contain cases where the same candidate set would be ranked differently under non-reactive versus reactive agent responses?
3. Can candidate-conditioned interaction quality be audited separately from FRNet's learned safety scoring?
4. Is any same-scene intervention-consistency experiment reported in supplementary material or code?

## 15. Change log

```text
2026-09-13 — initial metadata skeleton
2026-09-13 — GPT-5.6 Sol scientific review for P2-R Round 1
```
