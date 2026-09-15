# NEXT_TASK

## 唯一下一任务

> **Deep-read P0012 DA-WAM as the second paper in Wave C.6, using the existing WAM reading stack. Keep research-direction convergence paused.**

Canonical expansion plan:

```text
landscape/WAM_DEEP_READ_EXPANSION_QUEUE_V1.md
```

Current phase:

```text
broad WAM literature expansion     ACTIVE
research-direction convergence     PAUSED
candidate-problem promotion        PAUSED
method design                      FORBIDDEN
```

Current normalized count:

```text
12 anchors complete
DriveLaW = latest completed anchor
DA-WAM   = NEXT
```

---

# Why DA-WAM is next

DA-WAM introduces an interface almost orthogonal to DriveLaW:

```text
DriveLaW:
one common generative world representation
→ direct trajectory policy

DA-WAM:
N candidate trajectories
→ N action-conditioned future latents
→ one-to-one future-latent-conditioned scoring
→ select candidate
```

This makes DA-WAM a strong pressure test for the current distinctions among:

```text
candidate-specific future output
candidate-specific future truth
future representation learning
future-conditioned scoring
explicit decision factors / utility
hard-negative safety supervision
online world-model consumption
```

---

# Mandatory reconstruction

## 1. Source/version boundary

Resolve:

```text
canonical paper version
official repo: https://github.com/LeapWM/da-wam
paper↔code version relation
latest public commit / code completeness
```

Lock a source commit if implementation is available.

## 2. Host planner and candidate construction

Reconstruct before touching the world model:

```text
current observation X_t
→ planner representation
→ N trajectory candidates tau_i
```

Determine:

```text
how candidates are generated
N / candidate support
whether candidates are anchors, diffusion samples or refined proposals
whether scoring and proposal features are shared
```

## 3. Online / EMA predictive representation adaptation

Trace:

```text
online encoder E_theta(X_t) → Z_t
EMA target encoder E_bar(X_{t+Delta}) → Z_{t+Delta}
```

Determine exactly:

```text
what is pretrained (V-JEPA 2.1?)
what LoRA/adapters are trained
what remains frozen
whether planner/scorer gradients update the online encoder
how EMA target is updated
whether predictive loss persists throughout planner optimization
```

## 4. One-to-one trajectory ↔ future latent path

For every candidate `tau_i`, reconstruct:

```text
tau_i → action representation a_i
(Z_t, a_i) → shared predictor P_phi
→ candidate-specific future latent Zhat_i
```

Mandatory distinction:

```text
N candidate-specific predictions       YES/NO
N factual alternative future targets   YES/NO
```

Do not allow the first to imply the second.

## 5. Factual-future supervision coverage

The paper explicitly acknowledges the offline-log limitation.

Lock down:

```text
expert trajectory tau_exp
→ nearest candidate i*
→ only Zhat_i* receives dense future-latent target?
```

Then determine what all non-expert candidates receive:

```text
factor labels
utility labels
ranking loss
hard-negative supervision
no future-latent supervision
```

This is central to the counterfactual vector.

## 6. Future-latent-conditioned scorer

Trace exact scorer inputs:

```text
current latent Z_t
+ action representation a_i
+ predicted future latent Zhat_i
→ scorer S_psi
→ interpretable planning factors q_i
+ overall utility score s_i
```

Determine:

```text
factor semantics
utility target provenance
ranking target provenance
how final score aggregates factors
whether future latent can be ablated while keeping same scorer capacity
```

## 7. Safety-critical hard negatives

Reconstruct exactly:

```text
how hard negatives are generated / selected
what makes them expert-proximate
which safety dimensions differ
whether future-latent supervision is attached to them
whether they train factor heads, score ranking, or both
```

Compare immediately with:

```text
DriveSuprim / BeyondDrive-style negative mining
WoTE explicit utility supervision
World4Drive factual-mode matching
```

## 8. Inference graph

Verify deployment path:

```text
online encoder
→ N candidate trajectories
→ N future-latent predictions
→ future-conditioned scorer
→ argmax
```

EMA target network and observed future must be absent.

Measure/record:

```text
N
predictor cost per candidate
shared batching
latency/FPS
future-latent dimensionality
```

## 9. Counterfactual vector

Force explicit answers:

```text
I01 candidate-specific future output?
I02 candidate-specific alternative-future supervision?
I03 intervention truth for unexecuted candidates?
I04 reactive other-agent response truth?
I05 external intervention-validity evidence?
```

Expected pressure point:

```text
one-to-one prediction architecture
!= one-to-one factual future supervision
```

## 10. Strongest matched ablations

Prioritize controls that isolate:

```text
frozen predictive encoder vs continued JEPA adaptation
shared future latent vs per-candidate future latent
trajectory-only scorer vs + future latent
future latent without factorization vs factorized scorer
without hard negatives vs + hard negatives
EMA target / predictive loss contribution
```

Do not use headline SOTA delta as primary evidence.

## 11. Evaluation regime

Separate:

```text
NAVSIM-v1
NAVSIM-v2
open-loop / non-reactive pseudo-simulation semantics
any actual reactive closed-loop evidence
```

Do not upgrade NAVSIM results into reactive intervention validation.

## 12. Full Ontology V1.3 projection

Force-fill A–P and explicitly record:

```text
ABSENT
NOT REPORTED
NOT EVALUATED
NOT APPLICABLE
SOURCE-UNVERIFIED
```

Residue must survive merge testing and back-projection before any V1.4 proposal.

---

# Required immediate cross-paper comparisons

For every important DA-WAM mechanism, compare:

```text
DA-WAM vs WoTE
DA-WAM vs World4Drive
DA-WAM vs WorldDrive
DA-WAM vs SeerDrive
DA-WAM vs Drive-JEPA
DA-WAM vs DriveLaW
```

Key questions:

```text
Is DA-WAM genuinely more candidate-specific than World4Drive, or only architecturally?
Does its one-to-one future/scorer path have one-to-one supervision truth?
Is continued JEPA adaptation materially different from Drive-JEPA frozen/pretrained transfer?
Are factor heads true utility/value modeling or proxy classification?
Does predicted future add information beyond trajectory geometry/current scene?
```

---

# Required artifacts

After the deep read create at minimum:

```text
papers/deep_analysis/P0012_DAWAM_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_DAWAM_AUDIT.md
landscape/P0012_DAWAM_ONTOLOGY_PROJECTION.md
landscape/WAM_COMPARISON_MATRIX_V1_3_DAWAM_EXTENSION.md
```

Update:

```text
state/CURRENT_STATE.md
state/NEXT_TASK.md
landscape/WAM_DEEP_READ_EXPANSION_QUEUE_V1.md
state/DECISION_LOG.md
```

only after the mechanism is stable.

---

# After DA-WAM

Current core queue:

```text
P0002 SafeDrive
P0005 RiskWorld
P0007 DriveReward
```

Then proceed into simulation/reactivity/evaluation and WAM+VLA control waves defined in the expansion queue.

---

# Guardrail

Do not use DA-WAM or DriveLaW to revive parked research candidates.

This phase asks:

```text
What does the field contain?
How do mechanisms differ?
What evidence supports them?
```

not:

```text
What should our method be?
```
