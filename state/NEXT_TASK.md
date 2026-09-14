# NEXT_TASK

## 唯一下一任务

> Finish the **Phase-B Wave-3 comparative deep read** with **Think2Drive**, then perform the six-paper Wave-3 synthesis closeout.

Wave 1 and Wave 2 are closed. Broad corpus acquisition remains frozen.

Canonical Wave-3 artifacts:

```text
landscape/PHASE_B_WAVE3_PLAN.md
landscape/PHASE_B_WAVE3_SYNTHESIS.md
audits/literature/PHASE_B_WAVE3_AUTOJEPA_AUDIT.md
audits/literature/PHASE_B_WAVE3_DAWAM_AUDIT.md
```

## Wave-3 status

```text
Epona primary-text first pass       = COMPLETE
DrivingGPT primary-text first pass  = COMPLETE
DriveLaW primary-text first pass    = COMPLETE
Auto-JEPA primary-text first pass   = COMPLETE
DA-WAM primary-text first pass      = COMPLETE
Think2Drive                         = NEXT
Wave 3                              = OPEN
```

## Stable five-way interface map

```text
Epona
shared history latent
→ modular trajectory / visual generation

DrivingGPT
interleaved image/action tokens
→ one causal driving language

DriveLaW
online Video-DiT hidden state
→ Action DiT

Auto-JEPA
predicted future ego-intent latent
→ trajectory-memory retrieval
→ scorer/gate

DA-WAM
candidate_i
→ candidate-specific future latent_i
→ candidate-specific score_i
```

The DA-WAM audit adds three important corrections:

1. **Candidate-specific output does not imply candidate-specific future-state ground truth.** Dense future-latent supervision is applied only to the expert-matched candidate because offline logs provide only the executed future.
2. **Future-state gain is positive but modest over an already strong planner.** NAVSIM-v1 matched ablation: `93.31` no-future → `93.46` action-conditioned future → `93.68` with hard negatives.
3. **Hard-negative ranking supervision is an independent contributor.** The extra `+0.22 PDMS` is comparable to the future-state increment, so final performance must not be credited wholesale to world modeling.

Also important:

```text
Shared Global Future 92.81
< No Future 93.31
```

so simply injecting a future representation can hurt when it is mismatched to the candidate decision unit.

## Immediate Think2Drive audit

Think2Drive is the final Wave-3 anchor because it uses a world model in a fundamentally different place: **inside policy learning / imagination**, rather than as a future representation directly consumed by the deployed raw-sensor planner.

Trace exactly:

```text
1. observation / latent state representation
2. encoder and recurrent/dynamics state
3. action representation
4. transition / reward / termination prediction targets
5. what is learned from real environment interaction vs imagined rollout
6. how Dreamer-style imagination trains actor/value networks
7. exact deployed-policy path at test time
8. whether the learned world model itself runs online at deployment
9. where planning/action supervision comes from
10. data efficiency / interaction-budget evidence
11. closed-loop evaluation regime and simulator semantics
12. strongest matched ablation for world-model-based policy learning
13. strongest alternative explanation (RL objective, privileged simulator state, reward design, curriculum, etc.)
14. what Think2Drive adds beyond classic model-free driving RL and beyond the other five Wave-3 WAM interfaces
```

The key comparison is:

```text
Epona / DrivingGPT / DriveLaW / Auto-JEPA / DA-WAM
= world/future representation participates directly in the planner's inference architecture
  to different degrees

Think2Drive
= world model primarily serves as a learned imagination environment for policy optimization
```

Verify this from primary text rather than assuming it from the Dreamer label.

## Wave-3 closeout after Think2Drive

Create/finish a single six-paper comparison answering:

```text
A. What exactly is unified?
B. What predictive/world object is learned?
C. Where does it enter action selection?
D. Does it survive deployment?
E. What alternative-action supervision exists?
F. What matched evidence isolates its planning contribution?
G. What evaluation regime supports the claim?
```

Then mark Wave 3 CLOSED and proceed to Wave 4:

```text
Bench2Drive
HUGSIM
ORION
ReactSim-Bench
CausalDrive
```

Do not declare a research gap. Do not design a method. Do not broaden the corpus. Do not reactivate P2-R/P3. Do not force risk-field knowledge into the interpretation.