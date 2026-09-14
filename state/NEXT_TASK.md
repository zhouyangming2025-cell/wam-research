# NEXT_TASK

## 唯一下一任务

> Continue the **Phase-B Wave-3 comparative deep read** with **DA-WAM**, using the completed Epona ↔ DrivingGPT ↔ DriveLaW ↔ Auto-JEPA interface map as the baseline.

Wave 1 and Wave 2 are closed. Broad corpus acquisition remains frozen.

Canonical Wave-3 artifacts:

```text
landscape/PHASE_B_WAVE3_PLAN.md
landscape/PHASE_B_WAVE3_SYNTHESIS.md
audits/literature/PHASE_B_WAVE3_AUTOJEPA_AUDIT.md
```

## Wave-3 status

```text
Epona primary-text first pass       = COMPLETE
DrivingGPT primary-text first pass  = COMPLETE
DriveLaW primary-text first pass    = COMPLETE
Auto-JEPA primary-text first pass   = COMPLETE
DA-WAM                              = NEXT
Think2Drive                         = PENDING
Wave 3                              = OPEN
```

## Stable four-way result

“World-action unification” now splits into at least four mechanisms:

```text
Epona:
shared historical latent F
→ separate TrajDiT / VisDiT
→ joint training, modular generation
→ visual generation can be disabled for planning

DrivingGPT:
interleaved image/action tokens
→ one causal Transformer
→ world/action unified as one driving language

DriveLaW:
Video-DiT denoising latent
→ direct condition for Action DiT
→ online generative hidden state becomes planner state

Auto-JEPA:
scene/history/route
→ predicted future ego-intent latent
→ trajectory-memory retrieval
→ scorer/gate
→ final trajectory
```

New stable distinction introduced by Auto-JEPA:

```text
WORLD/SCENE FUTURE REPRESENTATION
!=
EGO-ACTION FUTURE REPRESENTATION
```

Auto-JEPA deliberately compresses the former into a latent target defined by future ego motion. Its strong NAVSIM result therefore supports planning-oriented compression, not classical full environment-transition modeling.

Important Auto-JEPA evidence:

```text
fixed medoid intent                    52.6 PDMS
intent retrieval + gate, no scorer    87.6
intent + scorer, no gate              91.0
full                                  91.3

K=1 / 200 / 300:
87.6 / 91.1 / 91.3 PDMS
```

Semantic occlusion:

```text
dynamic-agent mask mean intent change = 0.080
matched random mask                    = 0.027
ratio                                  = 2.97×
dynamic-agent intervention larger      = 71.1% of samples
```

Interpret conservatively: the predicted intent is selectively sensitive to planning-relevant visual content, but this does not establish universal decision sufficiency or reactive causal understanding.

## Immediate DA-WAM audit

DA-WAM is now the crucial contrast because it returns from a single compressed ego-intent latent to **per-candidate future latent prediction + candidate scoring**.

Trace exactly:

```text
1. current observation representation
2. candidate trajectory representation
3. how each candidate conditions the future latent
4. exact future-latent tensor and target source
5. which candidate(s) receive direct future-state supervision
6. what supervision unexecuted candidates receive
7. candidate scorer/reward/value heads and labels
8. inference path: candidate → future latent → score → selected action
9. whether future latent is genuinely consumed online
10. matched ablations: no future / shared global future / current latent / action-conditioned future / hard negatives
11. what gains are due to future-state modeling vs scorer/ranking supervision
12. NAVSIM evaluation semantics and any reactive/closed-loop evidence
13. strongest alternative explanation
14. exact relation to WoTE and Auto-JEPA
```

The comparison should explicitly answer:

```text
Auto-JEPA:
one scene-conditioned ego-intent latent
→ retrieve nearby actions
→ score candidates

DA-WAM:
for each candidate action
→ predict candidate-specific future latent
→ score candidate
```

Do not assume the latter is automatically more counterfactual or more behaviorally correct. Audit where its candidate-specific future supervision actually comes from.

## Subsequent order

```text
DA-WAM
→ Think2Drive
```

Think2Drive will then separate a learned world used for **policy training inside imagination** from WMs whose representations/futures are directly consumed by the deployed planner.

## Stop condition

Wave 3 closes when all six anchors can be placed on one inference-interface map and their planning gains can be discussed without the generic explanation “they use a world model.” After Wave 3, proceed to Wave 4 before any gap or method selection.

Do not declare a research gap. Do not design a method. Do not broaden the corpus. Do not reactivate P2-R/P3. Do not force risk-field knowledge into the interpretation.