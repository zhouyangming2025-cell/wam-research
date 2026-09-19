# WAM Research Tensions V2 — Adversarially Validated

Last updated: 2026-09-15

Status: **HISTORICAL PRIOR-ART / TENSION AUDIT — retained for evidence and counterexamples; not the current task or an authorization to formulate a research problem.**

Authority:

```text
audits/research_synthesis/WAM_TIER1_TENSION_ADVERSARIAL_VALIDATION_V1.md
```

This file retains the post-adversarial tension record. The former pre-adversarial V1 snapshot was removed from the working tree after its useful history was preserved in Git; this file must still be read against its cited audits and primary sources.

---

# Validated Tier-1 status

| ID | Original tension | Validated verdict | Surviving/narrowed scientific question |
|---|---|---|---|
| T2 | explicit consequence rollout vs compact world-state conditioning | **SURVIVES — NARROWED** | When does online action-conditional branching add decision information that cannot be amortized into a compact state/policy under matched compute/data? |
| T3 | training-time world modeling vs deployment-time model-basedness | **PARTIALLY RESOLVED** | Which consequence computations can be distilled/amortized, and which must be recomputed online under scene-specific uncertainty, OOD or interaction? |
| T5 | factual-future learning vs intervention-correct consequence modeling | **PARTIALLY RESOLVED — H2 strengthened** | How can WAMs identify/validate intervention-correct outcomes when episode identity and reactive agents both matter? |
| T6 | structured interaction semantics vs true reactive dynamics | **SURVIVES — NARROWED** | What marginal planning value does explicit ego-conditioned reaction modeling add beyond a strong interaction-aware latent, as response dependence increases? |

---

# T2 update

External controls:

```text
Value Equivalence Principle
Value-Aware Model Learning
DeepMDP / bisimulation representations
MuZero
TD-MPC2
I2A
```

Stable correction:

```text
full / observation-faithful environment modeling
is NOT universally necessary for good planning
```

But value-equivalent compact models can still be used for online planning, and there is no matched autonomous-driving experiment that isolates:

```text
compact direct conditioning
vs endpoint branching
vs recurrent consequence rollout
```

under identical data/backbone/compute.

Verdict remains `SURVIVES`.

---

# T3 update

External controls:

```text
MBPO
Dreamer / DreamerV3
WPT (CVPR 2026)
MuZero
TD-MPC2
```

Stable correction:

```text
online world reasoning is NOT universally required at deployment
```

WPT directly establishes an autonomous-driving teacher→student world-to-policy transfer path with substantial inference acceleration while retaining most performance benefit.

However:

```text
rare/OOD/interaction-heavy teacher-student gap
```

has not been cleanly mapped under matched training information.

Therefore the useful scientific object is no longer `world model online: yes/no`, but:

```text
AMORTIZABLE FUTURE INFORMATION
vs
SCENE-SPECIFIC ONLINE REASONING NEED
```

---

# T5 update

External controls:

```text
Causal Confusion in Imitation Learning
How Can Driving World Models Do Counterfactual Prediction? (2026-08)
TrafficBots counterfactual simulation formulation
WOSAC / Waymax reactive simulation infrastructure
```

Strong new conclusion:

```text
action-conditioned future generation
!=
episode-specific counterfactual prediction
```

This is no longer merely an evidence caution inferred from the 11 anchors. A controlled CARLA benchmark with matched counterfactual outcomes demonstrates failure of direct action-conditioned predictions from representative driving WMs.

Critical remaining boundary:

```text
short-horizon same-environment counterfactual
!=
reactive multi-agent intervention consequence
```

The latter remains unresolved and is harder.

---

# T6 update

External controls:

```text
M2I
GameFormer
DIPP / planning-centric prediction
TrafficBots
WOSAC / Waymax
Reaction-Uncertainty-Aware Motion Planning (2026)
```

Novelty guard:

```text
conditional response prediction is prior art
reactive multi-agent simulation is prior art
game-theoretic interaction modeling is prior art
reaction uncertainty is prior art
```

What remains unresolved is not whether reactions can be modeled, but whether they provide measurable marginal decision value beyond a strong structured representation when all other components are matched.

A key hypothesis is now conditional:

```text
low response-dependence scenes:
compact interaction representation may be sufficient

high response-dependence / negotiation scenes:
explicit conditional reaction distribution may become necessary
```

This must be tested, not assumed.

---

# Cross-tension convergence

T2, T3 and T6 now converge on a deeper scientific axis:

> **Adaptive / conditional future reasoning: what must be computed online for the current scene, versus what can be amortized into policy/state representations?**

Candidate gating variables supported by prior art and anchor evidence include:

```text
interaction response dependence
reaction uncertainty / multimodality
OOD / rarity
candidate ambiguity
irreversibility / safety cost
model confidence / epistemic uncertainty
```

This is a scientific organizing principle, NOT yet an authorized method proposal.

---

# Counterfactual vocabulary rule

Going forward the project must distinguish:

```text
1. conditional prediction
   p(Y | H, a)

2. interventional prediction
   p(Y | H, do(a))

3. episode-specific counterfactual
   p(Y_a | H, factual outcome/evidence)

4. reactive multi-agent counterfactual simulation
   alternative ego intervention + endogenous agent responses
```

Do not call level 1 evidence for levels 2–4 without direct validation.

---

# Gate

The Tier-1 prior-art attack is complete enough to begin **candidate problem formulation**, but not method design.

Next task:

```text
for T2/T3/T5/T6:
→ write minimal falsifiable problem statement
→ identify nearest-neighbor 2025–2026 autonomous-driving papers
→ define positive/negative controls
→ define minimum experimental assets
→ assess novelty overlap
→ rank researchability
```

Still prohibited:

```text
no architecture proposal yet
no forced risk-field answer
no claim that a tension itself is novel
```
