# WAM Candidate Problem Overlap Matrix V1

Last updated: 2026-09-15

Purpose: attack novelty by comparing each candidate research problem against the nearest 2025–2026 work before any method design.

Legend:

```text
SAME       materially the same scientific problem
PARTIAL    overlaps one mechanism/axis but not the full candidate
DIFFERENT  adjacent but different scientific question
```

---

# CP-T2 — Conditional value of online consequence branching

| Nearest work | Same problem? | Same supervision? | Same intervention? | Same planner interface? | Same evaluation regime? | What remains different? | Novelty risk |
|---|---|---|---|---|---|---|---|
| WoTE | PARTIAL | PARTIAL | PARTIAL | recurrent consequence + utility | NAVSIM non-reactive | no matched compact-state vs endpoint vs rollout comparison | MEDIUM |
| World4Drive | PARTIAL | PARTIAL | PARTIAL | endpoint latent → selector | NAVSIM | no recurrent-vs-compact matched ladder | MEDIUM |
| GraphWorld | PARTIAL | PARTIAL | NO | compact W → direct policy | mixed | opposite paradigm, not matched against rollout | MEDIUM |
| ProDrive (2026) | PARTIAL | PARTIAL | candidate-conditioned future | candidate future evaluation | NAVSIM | demonstrates proactive future coupling, not when it is necessary | MEDIUM |
| ForeSight (2026) | PARTIAL | NO | explicit future imagination | imagined future → action | NAVSIM/nuScenes | no matched compact-state control and no response-dependence stratification | MEDIUM |
| CF-VLA (CVPR 2026) | PARTIAL | NO | adaptive counterfactual reasoning on hard scenes | VLA reasoning/editing | large-scale driving datasets | establishes adaptive reasoning principle, not WM-branching necessity | HIGH for `hard scenes think more` claim |
| UTMR (IV Workshops 2026) | PARTIAL | PARTIAL | uncertainty-triggered short rollout/reranking | WoTE-style selector refinement | NAVSIM + AWSIM | already claims selective extra WM compute under uncertainty | HIGH for `uncertainty-triggered rollout` method |

### Surviving boundary

```text
matched mechanism ladder under equal training information and deployment budget
+
response-dependence / ambiguity stratification
```

No identified nearest work closes this exact comparison.

---

# CP-T3 — Non-amortizable world reasoning after distillation

| Nearest work | Same problem? | Same supervision? | Same intervention? | Same planner interface? | Same evaluation regime? | What remains different? | Novelty risk |
|---|---|---|---|---|---|---|---|
| WPT (CVPR 2026) | **SAME core lifecycle** | online WM teacher + distillation | teacher→student transfer | lightweight student policy | open + closed loop | does not fully map residual gap vs rarity/OOD, but occupies central problem | **HIGH** |
| Fast-WAM (2026, robotics) | SAME broad question | video/world co-training | remove test-time imagination | action-only inference | robotics | different domain, same scientific lifecycle question | HIGH |
| Metis | PARTIAL | joint video/action co-training | skip future video at deployment | action-only | driving | not teacher-student distillation but same amortization principle | HIGH |
| DynFlowDrive | PARTIAL | WM-derived labels | remove WM at deployment | score head | driving | world consequence compressed into scorer | HIGH |
| CF-VLA | PARTIAL | filtered reasoning labels | adaptive online reasoning | selective deliberation | driving | generic reasoning rather than WM distillation | HIGH |
| UTMR | PARTIAL | WM selector | uncertainty-triggered extra online compute | selective reranking | driving | directly overlaps fallback-on-uncertainty idea | HIGH |

### Judgment

The scientifically interesting residual `what cannot be amortized?` remains, but the obvious method family is densely occupied. Treat as a diagnostic axis inside CP-T2, not a standalone candidate.

---

# CP-T5 — Episode-specific reactive counterfactual consequences

| Nearest work | Same problem? | Same supervision? | Same intervention? | Same planner interface? | Same evaluation regime? | What remains different? | Novelty risk |
|---|---|---|---|---|---|---|---|
| How Can Driving World Models Do Counterfactual Prediction? (2026-08) | **PARTIAL / closest** | matched factual + counterfactual simulator outcomes | alternative ego action | WM counterfactual evaluation | controlled CARLA | explicitly assumes surrounding agents do NOT react to changed ego action | MEDIUM |
| ReactSim-Bench (2026) | PARTIAL | reactive feasibility, not paired episode CF truth | deviated AV behavior | behavior simulator | reactive closed-loop protocol on nuPlan | measures reactivity but not episode-specific factual/counterfactual identification or planning regret | MEDIUM |
| CausalDrive (2026) | PARTIAL | reactive video/world generation + sociology conditioning | ego trajectory + semantic interaction prompt | playable reactive renderer / RL environment | generative closed loop | reactive simulator, but no matched same-episode factual↔reactive-CF identification test | MEDIUM |
| TrafficBots | PARTIAL | logged multi-agent data | player deviation | reactive simulator | closed-loop behavior sim | reactive prior art, not episode-specific CF ground truth | MEDIUM |
| WOSAC / Waymax | DIFFERENT / enabling infra | realism/interactive simulation | simulator rollout | simulator benchmark | closed loop | infrastructure rather than matched counterfactual identification | LOW |
| AWM (2026) | PARTIAL | adversarial self-play / counterfactual credit | learned adversarial agents | robust planner training | nuPlan / InterPlan | seeks robust policy via adversarial WM, not matched causal consequence validity | MEDIUM |
| Causal Confusion in IL | foundational PARTIAL | interventions identify causal structure | intervention | imitation learning | driving + control | theory/prior, not modern WAM counterfactual benchmark | LOW |

### Surviving boundary

```text
episode-specific abduction
+
ego intervention
+
reactive surrounding-agent response
+
matched consequence truth
+
planning utility / regret
```

The nearest works each cover subsets of this conjunction; no identified paper closes the whole loop.

---

# CP-T6 — Reaction distributions beyond structured representation

| Nearest work | Same problem? | Same supervision? | Same intervention? | Same planner interface? | Same evaluation regime? | What remains different? | Novelty risk |
|---|---|---|---|---|---|---|---|
| Reaction-Uncertainty-Aware Motion Planning (IEEE Access 2026) | **SAME core mechanism** | ego-conditioned multimodal responses | ego-plan-conditioned prediction | tree planner | nuPlan | lacks GraphWorld-like strong structured-only matched control, but directly tests reaction uncertainty value | **HIGH** |
| Ego-conditioned prediction + gap-driven planning (2026) | SAME broad mechanism | conditional agent response | sampled ego candidates | coupled prediction/planning | driving | different planner details, same core idea | HIGH |
| M2I | PARTIAL | influencer→reactor | conditional trajectory | prediction | motion forecasting | older but establishes conditional response | HIGH |
| GameFormer | PARTIAL | interactive/game modeling | hierarchical response | joint prediction/planning | driving | established explicit interaction reasoning | HIGH |
| ProDrive | PARTIAL | ego-conditioned future BEV | ego candidates | future evaluation | NAVSIM | world-state rather than explicit response distribution | MEDIUM-HIGH |
| ReactSim-Bench | PARTIAL | reactive simulation | deviated AV | simulator | reactive | evaluation object already established | MEDIUM |

### Judgment

The exact negative control is still scientifically useful, but `ego-conditioned multimodal reaction distribution improves planning` is already a direct 2026 result. Standalone novelty risk is too high.

---

# Overall overlap verdict

```text
CP-T2  novelty risk MEDIUM      → survives as a causal comparison problem
CP-T3  novelty risk HIGH        → reject standalone; merge variable into T2
CP-T5  novelty risk MEDIUM-LOW  → strongest surviving candidate, but fast-moving
CP-T6  novelty risk HIGH        → reject standalone; merge reaction axis into T5/T2
```

Key warning:

```text
ADAPTIVE / SELECTIVE ONLINE REASONING IS ITSELF PRIOR ART.
REACTIVE EGO-CONDITIONED PREDICTION IS ITSELF PRIOR ART.
COUNTERFACTUAL ACTION CONDITIONING IS ITSELF PRIOR ART.
```

A surviving contribution must isolate a narrower unresolved causal variable, not rebrand one of these mechanisms.
