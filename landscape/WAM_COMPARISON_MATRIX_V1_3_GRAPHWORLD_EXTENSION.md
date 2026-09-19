# WAM Comparison Matrix V1.3 — GraphWorld Extension

Last updated: 2026-09-15

Status: **HISTORICAL PROJECTION SNAPSHOT — not current state or final route authority; retain only as a traceable comparison aid.**

Anchors:

```text
LAW | WoTE | Epona | WorldDrive | World4Drive
| SeerDrive | Drive-JEPA | Metis | DynFlowDrive | Discrete-WAM | GraphWorld
```

GraphWorld full projection:

```text
landscape/P0065_GRAPHWORLD_ONTOLOGY_PROJECTION.md
```

This file extends rather than replaces:

```text
landscape/WAM_COMPARISON_MATRIX_V1_3_DISCRETE_WAM_EXTENSION.md
```

---

# 1. Canonical planning-interface taxonomy

| Paper | Canonical world/planning interface |
|---|---|
| LAW | predictive training signal / future-latent auxiliary |
| WoTE | online learned consequence model + explicit utility |
| Epona | shared world representation + direct generative policy |
| WorldDrive | predictive representation inheritance + distilled online consequence evaluation |
| World4Drive | online compact latent foresight + factual-mode matching |
| SeerDrive | online bidirectional feature co-refinement |
| Drive-JEPA | predictive representation pretraining + simulator-distilled proposal/selection planner |
| Metis | asymmetric world-action co-training + action-only deployment |
| DynFlowDrive | training-only flow-dynamics mode/score supervision |
| Discrete-WAM | shared discrete world-policy pretraining + hierarchical direct token policy |
| **GraphWorld** | **online interaction-structured future-aware latent state + direct multimodal planner** |

GraphWorld adds a useful family:

```text
world state directly conditions policy
without
explicit candidate→future-consequence→utility selection
```

---

# 2. What is the world object?

| Paper | World object used for planning/scientific claim |
|---|---|
| LAW | current/future visual latent |
| WoTE | structured BEV state sequence |
| Epona | shared historical latent + generated visual latent |
| WorldDrive | generative/distilled future scene latent |
| World4Drive | intention-conditioned future latent |
| SeerDrive | future BEV |
| Drive-JEPA | masked predictive representation |
| Metis | future video latent/feature during training |
| DynFlowDrive | flow-transported future latent teacher |
| Discrete-WAM | discrete visual/world tokens |
| **GraphWorld** | **agent-centric node-level interaction latent W={w_agents,w_ego}** |

GraphWorld is the strongest current anchor for:

```text
structured relational world representation
```

rather than appearance-centric world substrate.

---

# 3. Long-horizon claim decomposition

| Paper | Long physical output horizon | Explicit multi-step world rollout | Historical memory/context | Persistent online world state |
|---|---:|---:|---:|---:|
| WoTE | YES | **YES recurrent** | YES | rollout-local |
| Epona | visual rollout can be long | **YES visual autoregressive** | YES | generated visual context |
| World4Drive | planning horizon finite | NO, endpoint latent | short history | NO persistent sequence |
| SeerDrive | future endpoint | NO | current/history BEV | internal refinement only |
| DynFlowDrive | next/future endpoint | NO physical rollout | current latent | training-only WM |
| Discrete-WAM | future token sequence capability | optional generative sequence | context sequence | optional generation mode |
| **GraphWorld** | **YES 6s trajectory evaluation** | **NO — paper explicitly rejects explicit multi-step rollout** | **YES GRU over past agent/ego states** | **single online refined latent W, not 6s state sequence** |

Binding conclusion:

```text
GraphWorld long horizon = long-horizon POLICY CONDITIONING
not long-horizon WORLD SIMULATION
```

---

# 4. Action / planner → world coupling

| Paper | Planner/action→world carrier | Per-candidate world branch? |
|---|---|---:|
| WoTE | candidate trajectory/action | YES |
| WorldDrive | candidate trajectory embedding | YES teacher/surrogate |
| World4Drive | candidate trajectory/action token | YES |
| SeerDrive | planner hidden feature / mode | multiple mode futures |
| Metis | action hidden representation | action-conditioned video, not candidate evaluator |
| DynFlowDrive | candidate trajectory | YES during training |
| Discrete-WAM | action tokens | YES in generation capability |
| **GraphWorld** | **mode-aggregated ego planning + motion query representations** | **NO — hypotheses are aggregated before W_tgt** |

GraphWorld therefore has planner→world coupling but not candidate-specific counterfactual consequence branching.

---

# 5. World → planning interface

| Paper | Online world object consumed by planner? | How? |
|---|---:|---|
| LAW | NO | future loss only |
| WoTE | YES | reward over recurrent future BEV |
| Epona | shared history latent YES; visual future NO | direct TrajDiT |
| WorldDrive | YES lightweight distilled future | reward/ranking |
| World4Drive | YES | ScoreNet selects mode |
| SeerDrive | YES | future BEV refines planner hidden feature |
| Drive-JEPA | NO JEPA future online | transferred encoder + scorer |
| Metis | NO future video online | shared/action expert only |
| DynFlowDrive | NO WM online | learned score head |
| Discrete-WAM | NO future visual required | decision→action token policy |
| **GraphWorld** | **YES** | **agent W refines/reweights motion modes; ego W is added to planning query** |

GraphWorld is thus model-conditioned planning, but not online consequence scoring.

---

# 6. Future-target truth provenance

| Paper | Primary future/world target truth |
|---|---|
| LAW | encoded factual future frame latent |
| WoTE | factual/structured future BEV + non-reactive reward semantics |
| Epona | factual future visual frame / ego trajectory during training |
| WorldDrive | factual video for WM; teacher-generated candidate futures for FAR |
| World4Drive | one factual future latent assigns K hypotheses |
| SeerDrive | factual future BEV with WTA mode supervision |
| Drive-JEPA | EMA masked-token representation inside video window |
| Metis | factual future video |
| DynFlowDrive | one factual future latent endpoint for candidate-conditioned flow |
| Discrete-WAM | factual future visual tokens under logged action |
| **GraphWorld** | **MIXED: flow target is motion/planning-hypothesis-derived; Stage-II stop-grad target is W inferred from actual t+1 input** |

GraphWorld is unusual because the main flow endpoint is not itself a direct factual future observation encoding.

---

# 7. F07/F08 temporal geometry

| Paper | F07 observability geometry | F08 internal-step meaning |
|---|---|---|
| Drive-JEPA | random-mask same-window completion | no physical rollout |
| Epona | history→unseen future frames | inner diffusion step ≠ frame time |
| WoTE | recurrent next-state future | rollout step ≈ predicted physical-time advance |
| DynFlowDrive | current→factual future endpoint | rectified-flow s ≠ physical time |
| Discrete-WAM | context/action→unseen future visual tokens | token-edit round ≠ physical time |
| **GraphWorld** | **current/history→hypothesis-derived target + adjacent-future representation consistency** | **flow interpolation/solver step ≠ physical seconds; t+1 supervision is a separate physical-time axis** |

GraphWorld strongly confirms the necessity of F08.

---

# 8. Counterfactual / reactive vector

| Paper | Action-specific world output | Alternative-action truth | Reactive other-agent truth | Reactive final-policy evaluation |
|---|---:|---:|---:|---:|
| WoTE | YES | partial/non-reactive target semantics | NO in audited path | NAVSIM non-reactive |
| World4Drive | YES | NO | NO | NAVSIM non-reactive |
| Metis | action-conditioned | NO | NOT ESTABLISHED | benchmark-dependent |
| DynFlowDrive | YES training branches | NO | NO | NAVSIM non-reactive |
| Discrete-WAM | action-conditioned generations | NO matched truth | NOT ESTABLISHED | NAVSIM non-reactive |
| **GraphWorld** | **NO per-candidate world branch** | **NO** | **NO world-model intervention truth** | **YES on Bench2Drive final policy** |

Important:

```text
Bench2Drive proves reactive policy competence
!=
reactive counterfactual world-model validity
```

---

# 9. Safety / risk semantics

| Paper | Explicit risk state? | Explicit online safety/value scorer? | Safety evidence |
|---|---:|---:|---|
| WoTE | NO field, but explicit reward semantics | YES | TTC/collision/progress/etc. utility |
| WorldDrive | NO field | YES ranking/value | PDMS preference supervision |
| World4Drive | NO | factual-mode score, not utility | collision/planning gains |
| SeerDrive | NO | NO explicit utility | planning/PDMS gains |
| DynFlowDrive | NO | learned mode score | NAVSIM gains |
| Discrete-WAM | NO | decision/RL reward, no future scorer | EPDMS/post-training |
| **GraphWorld** | **NO** | **NO** | **interaction representation + collision reduction + Bench2Drive reactive performance** |

GraphWorld's phrase `safety-relevant world state` should therefore not be upgraded to `explicit risk representation`.

---

# 10. Strongest matched attribution controls

| Mechanism | Matched result | Interpretation |
|---|---|---|
| ECIG alone | NAVSIM PDMS `85.1→85.5`; nuScenes 6s L2 `2.95→2.76` | interaction graph helps, but modestly on NAVSIM |
| full WSCP after ECIG | NAVSIM `85.5→90.1`; 6s L2 `2.76→2.29` | major planning gain is in world-state refinement/conditioning bundle |
| Diffusion→Flow | NAVSIM `88.1→90.1`; 6s Col `2.23→1.95` | flow parameterization beneficial vs tested diffusion |
| Stage I→II | 6s L2 `2.40→2.29`; Col `2.04→1.95` | factual t+1 latent consistency contributes modestly |
| Dense→ego-star graph | NAVSIM `85.0→90.1` | ego-focused graph inductive bias strongly helps tested architecture |
| 1→2 flow steps | NAVSIM `88.3→90.1` | shallow refinement helpful |
| >2 steps | PDMS falls to ~`89.2–89.3`, FPS drops | more internal refinement not monotonic |

The main scientific attribution is therefore:

```text
interaction structure
+
world-state refinement
+
planner/motion query conditioning
```

rather than a clean isolated `future world prediction fidelity` effect.

---

# 11. Evaluation semantics

| Benchmark | Correct project label | What it proves |
|---|---|---|
| Bench2Drive | **reactive CARLA closed loop** | final policy handles interactive execution |
| NAVSIM v1/v2 | **non-reactive data-driven pseudo-simulation** | strong planning quality under logged-agent semantics |
| nuScenes | **open loop** | long-horizon trajectory/collision proxy |
| Adv-nuScenes / nuScenes-C / Turning-nuScenes | **open-loop robustness subsets** | robustness of planner outputs, not reactive WM validity |

---

# 12. New cross-anchor conclusions after GraphWorld

## 12.1 World-model `strength` has at least two orthogonal meanings

```text
A. strength of environmental future prediction
B. strength of decision-relevant world representation
```

WoTE is stronger on explicit consequence rollout; GraphWorld is stronger on structured interaction representation. These are not points on one scalar ladder.

## 12.2 Online world dependence also has two forms

```text
CONSEQUENCE DEPENDENCE
candidate → future → value → select

REPRESENTATION DEPENDENCE
current/future-aware W → condition direct policy
```

GraphWorld occupies the second.

## 12.3 Long-horizon evidence must specify which object is long

```text
trajectory horizon
world rollout horizon
history horizon
latent memory horizon
closed-loop execution horizon
```

GraphWorld has long trajectory evaluation + historical recurrent context, but not long explicit world rollout.

## 12.4 Safety-aware representation is not risk modeling

GraphWorld demonstrates that collision improvements can emerge from interaction-aware representation without explicit risk variables. This is an important control for any later risk-aware WAM hypothesis.

---

# 13. Ontology decision

GraphWorld does not force a new stable dimension.

Potential residues:

```text
graph topology / interaction structure
hypothesis-derived vs factual-future target
```

are already expressible through:

```text
B03/B04/P04
F01/F02/F07
G01/G03
J04/J09
F08
```

Decision:

```text
ONTOLOGY V1.3 RETAINED
NO V1.4
```
