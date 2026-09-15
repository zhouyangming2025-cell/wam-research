# Phase C.5 Discrete-WAM Audit

Last updated: 2026-09-15

Status: **COMPLETE FIRST PASS — PAPER VERIFIED / SOURCE IMPLEMENTATION NOT IDENTIFIED**

Paper:

```text
Discrete-WAM: Unified Discrete Vision-Action Token Editing for World-Policy Learning
arXiv:2606.05645v2
v2: 2026-06-09
```

Canonical deep read:

```text
papers/deep_analysis/P0064_DISCRETE_WAM_DEEP_ANALYSIS_V2.md
```

Source status:

```text
paper + appendix             VERIFIED
official implementation repo NOT IDENTIFIED as of 2026-09-15
code-level details           SOURCE-UNVERIFIED
```

---

# 1. Stable mechanism judgment

Discrete-WAM should not be summarized as a single-codebook world-action model or as an online future-imagination planner.

Canonical lifecycle:

```text
PRETRAINING / CAPABILITY MODEL

visual VQ tokens            action acceleration tokens
(separate vocabulary)       (separate vocabulary)
           \                 /
            \               /
             shared Transformer
                    ↓
       world / policy / world-policy tasks
                    ↓
        shared hidden/parameter learning

DOWNSTREAM PLANNING

current context
→ high-level decision token
→ iterative parallel action-token editing
→ trajectory

future visual-token generation = NOT REQUIRED
```

Canonical subtype:

```text
SHARED-BACKBONE MULTI-TASK DISCRETE WORLD-POLICY PRETRAINING
→ HIERARCHICAL DECISION-CONDITIONED ACTION TOKEN EDITING
→ POLICY-ONLY PLANNING INFERENCE
```

---

# 2. CLAIM → EVIDENCE → INTERPRETATION → UNPROVEN

## Claim A — vision and action are unified in a shared discrete space

**AUTHOR CLAIM**

Discrete visual states and ego actions are aligned as a unified discrete world-policy representation.

**DIRECT PAPER EVIDENCE**

The appendix defines separate visual and action vocabularies:

```text
visual vocabulary: VQ visual codebook, K_V ≈ 16,384
action vocabulary: discretized (a_x,a_y), 60×60 = 3,600 prototypes
```

Both are embedded/projected into the same decoder-only Transformer hidden space and can coexist in the same world-policy token sequence.

**OUR INTERPRETATION**

The useful unification is:

```text
shared hidden/backbone/interface/sequence machinery
```

not:

```text
one literal shared codebook
```

**REMAINS UNPROVEN**

That visual and action token indices share semantic meaning or that the two modalities occupy one learned quantization vocabulary.

---

## Claim B — Discrete-WAM jointly models world and policy

**DIRECT PAPER EVIDENCE**

Three training families are present:

```text
world modeling:
C + A_future → V_future

policy modeling:
C + D → A_future

world-policy modeling:
C → [A_{t+1},V_{t+1},...,A_{t+H},V_{t+H}]
```

The same shared Transformer is used with task-specific masks/conditioning.

Stage-2 training activates visual and action losses jointly.

**OUR INTERPRETATION**

Discrete-WAM exhibits strong sequence/parameter/gradient-level world-policy jointness compared with separate-expert WAMs.

**REMAINS UNPROVEN**

That the downstream planning score requires online future-world generation. The policy planning graph can run as decision→action token editing only.

---

## Claim C — action-conditioned world modeling enables counterfactual reasoning

**DIRECT PAPER EVIDENCE**

World generation is conditioned on ego action tokens. The paper perturbs ego actions and measures changes in generated world distributions using surprise/divergence and pixel-level differences; surprise correlates negatively with planning-quality metrics and increases around poor/violating action perturbations.

**COUNTERFACTUAL AUDIT**

```text
candidate/action-conditioned generated world    YES
per-action observed alternative future truth    NO
reactive other-agent truth                      NO / NOT ESTABLISHED
external intervention-validity evidence         ABSENT
```

**OUR INTERPRETATION**

The model has useful action-sensitive imagination and self-consistency/surprise analysis.

**REMAINS UNPROVEN**

That the alternative generated future is the real consequence that would occur under the unexecuted action.

---

## Claim D — unified world-policy pretraining improves planning

**AUTHOR CLAIM**

The paper states that unified world-policy pretraining and token editing contribute to planning gains.

**DIRECT PAPER EVIDENCE**

Policy-training strategy ablation:

```text
From scratch   89.8 EPDMS
FT             89.7
LoRA-SFT       90.0
```

But the paper explicitly describes the LoRA-SFT pretraining path as:

```text
future actions teacher-forced
+ vision-oriented world-policy pretraining
+ ONLY vision prediction losses
→ LoRA policy finetuning
```

**OUR INTERPRETATION**

There is modest evidence that world/vision-oriented pretraining plus lightweight adaptation helps relative to from-scratch training in this setting.

**REMAINS UNPROVEN**

A clean causal benefit from the full Stage-2 joint world+action pretraining objective. Full finetuning (89.7) is not better than from-scratch (89.8), and the best 90.0 row changes the adaptation regime as well as the pretraining history.

---

## Claim E — world/policy pretraining is a major source of the final 90.4 EPDMS

**DIRECT PAPER EVIDENCE AGAINST MONOLITHIC ATTRIBUTION**

Decision-modeling ablation:

```text
Base       84.7 EPDMS
Base-D_t   87.2
```

Post-training ladder:

```text
SFT       89.1
SFT-D_t   90.0
RL        90.4
```

**INTERPRETATION**

High-level decision supervision and policy post-training are major independent contributors. The +2.5 EPDMS decision-modeling control is substantially larger than the cleanest world-pretraining delta visible in Table 4.

**BOUNDARY**

Do not report 90.4 as a monolithic `world-model gain`.

---

# 3. Unified is vector-valued

Canonical audited vector:

```text
shared world/action codebook          NO
shared token vocabulary               NO
separate modality vocabularies        YES
common token-sequence interface       YES
shared Transformer hidden space       YES
shared Transformer parameters         YES
joint multi-task losses/gradients     YES during joint stage
action→world forward coupling         YES in world/world-policy tasks
world→later-action sequence context    YES in joint world-policy task
future world mandatory for planning   NO
world/action both active in primary NAVSIM planning graph NO
```

This vector should replace the binary label:

```text
unified = YES
```

---

# 4. Token-semantics audit

## Visual tokens

```text
continuous visual feature
→ VQ quantization
→ visual codebook index
→ shared Transformer embedding
```

Semantics are implicit visual/world representations; no direct object/risk/occupancy meaning is established per token.

## Action tokens

```text
trajectory
→ planar acceleration sequence
→ 60×60 acceleration prototype grid
→ soft neighboring token targets
```

Action-token semantics are substantially more physically interpretable than visual-token semantics.

## Decision tokens

```text
path candidate × speed profile
→ EPDMS-style candidate evaluation
→ winning high-level decision target
```

This creates a methodological tension with a strong interpretation of decision tokens as purely upstream causal latent variables: the target itself is selected by downstream planning-quality evaluation.

---

# 5. Training / inference graph separation

## Joint training capability

```text
context
→ shared Transformer
→ future visual tokens and/or future action tokens
```

## Primary planning inference

```text
context
→ p(D|C)
→ p(A|D,C) via iterative token editing
→ trajectory
```

Absent from the mandatory planning path:

```text
online future visual generation
online future visual→utility scorer
online candidate-world rollout
```

This is the principal lifecycle finding.

---

# 6. Temporal audit

## F07

Future-world prediction is genuinely chronological:

```text
current/history context + action
→ unseen future visual tokens
```

This is stronger future-directionality than Drive-JEPA random-mask same-window completion.

## F08

Physical future index and token-edit iteration must be separated:

```text
h = future physical timestep
r = editing / discrete-diffusion refinement round
```

Binding rule:

```text
more editing rounds != more physical future horizon
```

The paper's scheduling ablation is a solver/refinement-quality curve, not a world-horizon experiment.

---

# 7. Planning and world-generation evidence

## Planning

```text
NAVSIM-v2  ≈ 90.4 EPDMS
NAVSIM-v1  ≈ 92.2 PDMS
```

Project-standard evaluation label:

```text
NAVSIM = NON-REACTIVE DATA-DRIVEN / PSEUDO-SIMULATION PLANNING
```

Do not upgrade these results to reactive closed-loop behavioral validation.

## World generation

Reported short-horizon future generation includes:

```text
FID ≈ 6.6
FVD ≈ 80.0
4 s / 8-frame setting
```

This validates a strong visual-generation capability.

No clean matched experiment establishes:

```text
better FID/FVD → better planning
```

Therefore O07 remains negative.

---

# 8. Scheduling evidence

The iterative action-token decoder shows that extra solver rounds can help or hurt depending on the update schedule.

`full_replace` can degrade with additional rounds because early acceleration-token changes amplify after temporal integration, while confidence/JS/freeze-based schedules preserve stable tokens and selectively refine uncertain ones.

Interpretation:

```text
editing compute is a policy refinement resource
not a future-world rollout depth
```

---

# 9. Horizontal comparison

## vs Metis

```text
Metis:
separate Action Expert / Video Expert
asymmetric action→world forward
world-loss→action backward
planning action-only

Discrete-WAM:
separate vocabularies
shared Transformer backbone/hidden space
joint world-policy sequence possible
planning still action-only
```

Discrete-WAM is more parameter/sequence unified but not more dependent on future-world computation at planning deployment.

## vs Epona

```text
Epona: shared historical F + separate TrajDiT/VisDiT
Discrete-WAM: shared Transformer + modality-specific vocabularies/tasks
```

Both can plan without explicit future visual generation.

## vs World4Drive / WoTE

World4Drive and WoTE are less parameter-unified but more explicitly model-based at deployment because their predicted future object remains on the action-selection path.

## vs DynFlowDrive

DynFlowDrive compresses training-time world consequences into a score head. Discrete-WAM compresses world-policy pretraining into shared policy/backbone parameters and directly generates decisions/actions online.

## vs LAW / Drive-JEPA

All can deploy without online future generation, but knowledge enters differently:

```text
LAW        auxiliary future loss during planner training
Drive-JEPA predictive video pretraining → encoder transfer
Discrete-WAM joint/shared discrete world-policy pretraining → policy generator
```

---

# 10. Ontology residue gate

Potential residue:

```text
DISCRETE REPRESENTATION ALIGNMENT TOPOLOGY
shared codebook vs separate vocabularies projected into common hidden space
```

Scientific distinction is real, but back-projection onto the existing continuous-latent anchors is mostly `NOT APPLICABLE`.

Decision:

```text
NO V1.4 amendment yet.
Add to residue watchlist.
Re-test when a second discrete-token core anchor is normalized.
```

World/action token ordering does not require a new dimension; F04 + E02 + J04 + F08 already represent it.

---

# 11. Evidence boundary

## PROVES reasonably well

```text
separate discrete visual/action vocabularies can be integrated by a shared Transformer;
action-conditioned future-token generation is effective;
world/policy multi-task training and policy token editing can coexist in one model;
hierarchical decision-conditioned token editing yields strong NAVSIM planning;
short-horizon visual generation is competitive;
action perturbations yield meaningful world-model surprise signals.
```

## DOES NOT PROVE

```text
one shared world/action codebook;
identical world/action token semantics;
online future-world generation is necessary for the reported planner;
full joint world-policy pretraining is cleanly isolated as the planning-gain source;
generated alternative futures are intervention-correct;
visual-generation fidelity is the causal reason planning improves;
NAVSIM establishes reactive learned-world validity.
```

## Strongest alternative explanation

```text
high-level decision prior
+ action discretization
+ discrete token editing
+ LoRA adaptation
+ RL post-training
+ large shared Transformer capacity
+ generic world/vision pretraining regularization
```

can explain substantial portions of final planning performance without requiring online model-based reasoning.

---

# 12. Source-audit queue

If official code is released/found, verify:

```text
visual/action embedding tables and vocabulary implementation
task-specific attention masks
joint world-policy token ordering
stage-1/2 task sampling ratios
loss masking at clean/corrupted positions
action suffix corruption
decision-token target generation
LoRA module list
GRPO reward/rollout path
whether NAVSIM planning forward ever computes future visual tokens
world-policy joint-generation inference mode
editing schedule thresholds and freeze semantics
latency batch/token counts
```
