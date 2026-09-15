# P0065 GraphWorld — Ontology V1 + V1.1 + V1.2 + V1.3 Projection

Last updated: 2026-09-15

Status: **FULL DIMENSION-FIRST PROJECTION — COMPLETE FIRST PASS**

Canonical analysis:

```text
papers/deep_analysis/P0065_GRAPHWORLD_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_GRAPHWORLD_AUDIT.md
```

Method-version scope:

```text
arXiv:2606.16274v1
2026-06-15
implementation source not identified as of 2026-09-15
```

Core warning:

```text
long-horizon planning
!= long-horizon world rollout

interaction-aware latent world state
!= reactive counterfactual environment model
```

---

# A. Problem and role of world knowledge

| ID | GraphWorld value | Evidence / interpretation |
|---|---|---|
| A01 | **improve long-horizon, interaction-heavy planning without expensive explicit future-scene rollout** | Paper targets long-horizon planning and runtime efficiency. |
| A02 | **online structured world-state conditioning + representation shaping** | World state remains on the deployed planner path and also receives temporal supervision. |
| A03 | **direct multimodal planner conditioned by refined world state** | No deployed future-consequence scorer/argmax loop. |
| A04 | **agent-centric relational latent world modeling** | Main scientific identity is interaction-structured world state rather than pixel/video generation. |

---

# B. Observation and current-state representation

| ID | GraphWorld value | Evidence / interpretation |
|---|---|---|
| B01 | **instance-level multi-agent features + ego state/history + local map** | Sensor specifics vary by benchmark/backbone; world module consumes perception-level instance features. |
| B02 | **YES historical ego/agent motion context** | Historical motion states over past L frames feed GRU. |
| B03 | **structured node-level latent world state** | `W={w_1...w_N,w_ego}`. |
| B04 | **explicit agent identity, relative geometry, motion history, map-conditioned interaction semantics** | More structured than visual latent. |
| B05 | **current/refined world state is directly consumed online** | Refined W conditions motion/planning queries. |

---

# C. Representation provenance and imported priors

| ID | GraphWorld value | Evidence / interpretation |
|---|---|---|
| C01 | **E2E perception/planning backbone + learned ECIG/GRU/world projections** | Exact backbone variant differs across benchmarks; code unavailable. |
| C02 | **instance features and planning/motion queries projected into shared latent interaction space** | No discrete codebook. |
| C03 | **two-stage end-to-end training; exact freeze schedule SOURCE-UNVERIFIED** | Paper states Stage I standard E2E, Stage II temporal world supervision. |
| C04 | **PARTIALLY ISOLATED** | ECIG/WSCP/stage/flow/graph topology ablations exist; full backbone/data attribution remains bundled. |

---

# D. Action, intention and candidate space

| ID | GraphWorld value | Evidence / interpretation |
|---|---|---|
| D01 | **generated multimodal ego trajectories; no explicit candidate bank fed into separate world model** | Direct planner head. |
| D02 | **ego trajectory / planning-query representation** | Action is not represented as a distinct control token for world transition. |
| D03 | **multi-modal ego planning queries** | Planning modes exist. |
| D04 | **M multimodal planning hypotheses** | Modes are jointly decoded rather than consequence-evaluated one by one. |
| D05 | **candidate/mode support determined by underlying E2E planner** | Paper does not expose WoTE-style large external trajectory bank. |
| D06 | **world-conditioned query modulation + direct decoding; no explicit prune→world-evaluate stage** | Refinement occurs in latent query/world state. |

---

# E. Action → world coupling

| ID | GraphWorld value | Evidence / interpretation |
|---|---|---|
| E01 | **PARTIAL / indirect** | `W_tgt` is conditioned on aggregated ego planning hypotheses, but there is no one action-conditioned future world per candidate. |
| E02 | **planning-query aggregate enters target-world construction** | `mean_m(Q_tilde_ego)` contributes to `W_tgt`. |
| E03 | **shared W_tgt across aggregated modes** | No separately parameterized or branched candidate worlds. |
| E04 | **NO persistent candidate branch identity through world evolution** | Mode aggregation occurs before target-state construction. |
| E05 | **training support comes from supervised planning/motion hypotheses; intervention extrapolation not validated** | No counterfactual action truth. |

---

# F. Dynamics and future temporal modeling

| ID | GraphWorld value | Evidence / interpretation |
|---|---|---|
| F01 | **structured latent world state** | Future-aware substrate is agent-centric latent state, not RGB/BEV rollout. |
| F02 | **interaction dynamics / motion-relevant / map-conditioned semantics** | Semantics are latent and task-shaped. |
| F03 | **GRU historical dynamics + flow-matching latent refinement** | Two distinct temporal mechanisms. |
| F04 | **single refined world state; no explicit multi-step physical future sequence** | Paper explicitly rejects explicit multi-step rollout. |
| F05 | **planning horizon evaluated to 6 s; world-state physical prediction horizon not explicitly rolled to 6 s** | Long planning horizon ≠ long WM rollout. |
| F06 | **multimodal motion/planning hypotheses; no calibrated world uncertainty** | Mode weights are planning/motion confidence, not calibrated latent uncertainty. |
| F07 | **CURRENT/HISTORY → future-aware hypothesis-derived target + t+1 consistency target** | Not random-mask completion, but also not clean history→factual future-world prediction. |
| F08 | **FLOW COORDINATE IS INTERNAL LATENT TRANSPORT TIME; physical time exists separately in t/t+1 supervision and trajectory horizon** | Critical GraphWorld distinction. |

---

# G. Future supervision and truth sources

| ID | GraphWorld value | Evidence / interpretation |
|---|---|---|
| G01 | **MIXED: flow target is hypothesis-derived; Stage-II target uses future-observation-derived W_{t+1}** | Must not collapse these two truths. |
| G02 | **stop-gradient future latent for Stage II** | `W_{t+1}` is detached. |
| G03 | **NO per-action factual future world targets** | One future observation stream, no alternate ego interventions. |
| G04 | **benchmark planning metrics only; no online value teacher central to world state** | Unlike WorldDrive/WoTE reward supervision. |
| G05 | **direct expert/planning/motion task losses** | Policy/motion supervision independent of L_world. |
| G06 | **multimodal branch supervision inherited from underlying planner; exact assignment SOURCE-UNVERIFIED** | Paper does not make branch identity the world-model centerpiece. |
| G07 | **perception + motion + planning + world consistency + flow objective** | Dense multi-task supervision. |
| G08 | **reactive alternative-agent response truth ABSENT for world training** | Bench2Drive evaluates final policy but is not branch-wise world truth. |

---

# H. Multimodal branch identity and assignment

| ID | GraphWorld value | Evidence / interpretation |
|---|---|---|
| H01 | **multi-modal agent motion modes + ego planning modes** | Modes are task-head hypotheses. |
| H02 | **mode queries from E2E motion/planning backbone** | Not semantic intention labels explicitly tied to world branches. |
| H03 | **mode aggregation (mean) contributes to W_tgt; importance network later reweights agent motion modes** | Target world loses per-mode branch identity. |
| H04 | **no reported best-of-N future-world oracle ceiling** | Candidate ranking gap not isolated. |

---

# I. Counterfactuality and reactivity

| ID | GraphWorld value | Evidence / interpretation |
|---|---|---|
| I01 | **NO candidate-specific future-world output** | One shared refined world state. |
| I02 | **NO candidate-specific alternative-future GT** | No intervention dataset per ego action. |
| I03 | **NO simulator truth for each candidate intervention** | NAVSIM non-reactive; Bench2Drive evaluates executed final policy, not all imagined branches. |
| I04 | **final-policy reactive evaluation YES on Bench2Drive; world-model reactive truth NO** | Keep policy evidence separate from WM truth. |
| I05 | **ABSENT** | No direct intervention-validity world benchmark. |

---

# J. World → planning interface

| ID | GraphWorld value | Evidence / interpretation |
|---|---|---|
| J01 | **direct online latent-state conditioning** | W modifies motion and ego planning queries. |
| J02 | **YES online world-state computation/refinement** | World machinery is active at inference. |
| J03 | **YES refined W is consumed before trajectory decoding** | Stronger online dependence than LAW/Epona planning-only visual branch. |
| J04 | **BIDIRECTIONAL INTERNAL COUPLING: planning/motion hypotheses → W_tgt; refined W → planning/motion queries** | Not candidate-specific causal rollout. |
| J05 | **direct generative/multimodal policy, not consequence evaluator** | Final trajectory from planning head. |
| J06 | **NO explicit deployed utility/reward model** | Importance weights are reliability modulation, not trajectory utility score. |
| J07 | **world-conditioned planning graph is the main deployment graph** | No separate heavy teacher removed at deployment. |
| J08 | **FLOW-SOLVER REFINEMENT** | Iterations update latent W; do not advance physical environment time. |
| J09 | **aggregated ego planning/motion query features** | Planner→world carrier is hidden hypothesis representation, not executed action. |

---

# K. Scorer and decision semantics

| ID | GraphWorld value | Evidence / interpretation |
|---|---|---|
| K01 | **NO dedicated candidate consequence scorer** | Direct multimodal decoding. |
| K02 | **importance network estimates motion-mode reliability/relevance** | Not explicit safety utility. |
| K03 | **importance network sees world-conditioned motion/ego features** | Internal query weighting rather than future-world scoring. |
| K04 | **NO explicit collision/TTC utility decomposition inside deployed scorer** | Safety is implicit/task-level. |
| K05 | **standard motion/planning labels; exact mode-label semantics SOURCE-UNVERIFIED** | No separate oracle value teacher described. |

---

# L. Training topology, jointness and gradient coupling

| ID | GraphWorld value | Evidence / interpretation |
|---|---|---|
| L01 | **two-stage E2E training** | Stage I base tasks; Stage II adds temporal world-state consistency. |
| L02 | **shared instance/planning/motion/world latent interfaces** | Strong integration with E2E backbone. |
| L03 | **shared parameters / gradients likely across world and task modules; exact detach topology SOURCE-UNVERIFIED** | Paper equations imply joint optimization except explicit stopgrad on W_{t+1}. |
| L04 | **world/flow/task losses shape online planner representation; W_{t+1} target branch stopped** | Exact implementation pending code. |
| L05 | **no teacher-student distillation lifecycle** | World state remains online. |
| L06 | **L_percep + L_motion + L_plan + λL_world plus flow objective in WSCP** | Performance is multi-loss bundle. |
| L07 | **flow intermediate states supervised by velocity objective; physical t+1 consistency only at endpoint representation level** | Distinguish solver-state supervision from physical-time target. |

---

# M. Future-knowledge lifecycle and deployment path

| ID | GraphWorld value | Evidence / interpretation |
|---|---|---|
| M01 | **joint E2E training → temporal consistency stage → online world-conditioned planner** | World knowledge retained explicitly, not only in weights. |
| M02 | **refined structured world state** | Online future-aware object is latent W, not decoded scene. |
| M03 | **YES online world-state path retained** | Contrast Metis/DynFlowDrive training-only WM. |
| M04 | **lightweight 1–2 step flow refinement; no distillation** | Efficiency achieved by compact latent rather than deleting WM. |
| M05 | **partially inspectable at node/world-state level but semantics remain latent** | More structured than opaque global latent, less explicit than BEV. |
| M06 | **NO optional sibling world branch; world-state conditioning is part of primary planner** | Main execution graph depends on it. |

---

# N. Compute, pruning and latency

| ID | GraphWorld value | Evidence / interpretation |
|---|---|---|
| N01 | **K selected neighbors + M motion/planning modes + 2 flow steps** | Sparse interaction + shallow latent solver. |
| N02 | **lightweight graph/GRU/projection/flow modules over perception backbone** | Exact parameter count not central/reported in audited text. |
| N03 | **spatial neighbor pruning and mode aggregation before world target** | Reduces graph/branch complexity. |
| N04 | **2-step Euler flow integration** | Default efficient refinement. |
| N05 | **~51 FPS in NAVSIM sampling-step table** | Paper reports favorable efficiency. |
| N06 | **more solver steps reduce FPS and do not monotonically improve PDMS** | 2 steps is best shown trade-off. |

---

# O. Evaluation regime and evidence attribution

| ID | GraphWorld value | Evidence / interpretation |
|---|---|---|
| O01 | **Bench2Drive reactive CARLA closed-loop + NAVSIM non-reactive pseudo-simulation + nuScenes-family open-loop** | Paper's generic `closed-loop NAVSIM` wording normalized. |
| O02 | **NO dedicated decoded world-fidelity metric** | No FVD/PSNR/BEV prediction fidelity for W. |
| O03 | **world state trained from task hypotheses + temporal adjacent state; evaluation mainly planning/motion** | World quality inferred indirectly through downstream behavior. |
| O04 | **strong component ablations: baseline→ECIG→WSCP; stage I→II; diffusion→flow; graph topology** | Better attribution than headline SOTA alone. |
| O05 | **interaction graph, flow parameterization, temporal supervision, direct query modulation all vary** | Full gain remains a bundle. |
| O06 | **cross-paper SOTA comparisons heterogeneous** | Matched internal controls stronger. |
| O07 | **NO direct world-state fidelity→planning correlation** | Downstream planning gains do not establish physical WM accuracy. |
| O08 | **paper verified; source unavailable/not identified** | Implementation details blocked. |
| O09 | **no future-world oracle candidate ceiling** | Ranking headroom not measured in WoTE/WorldDrive sense. |
| O10 | **see normalized boundary below** | Evidence must remain symmetric. |

O10 boundary:

```text
PROVES:
interaction-focused structured latent state helps long-horizon planning;
WSCP world-state conditioning materially improves planning;
flow beats tested diffusion alternative;
Stage-II temporal consistency adds modest value;
final policy works better in reactive Bench2Drive and open/non-reactive benchmarks.

DOES NOT PROVE:
6s explicit world rollout;
action-conditioned factual future environment dynamics;
reactive counterfactual world prediction;
explicit risk representation;
physical meaning of flow solver time;
world-state fidelity as the causal source of all planning gains.
```

---

# P. Safety, uncertainty and interaction semantics

| ID | GraphWorld value | Evidence / interpretation |
|---|---|---|
| P01 | **NO explicit risk field/state** | `safety-relevant semantics` are latent/interpretive. |
| P02 | **NO explicit deployed risk/value scorer; safety shaped by planning/motion objectives and interaction representation** | Collision gains are downstream evidence. |
| P03 | **mode confidences / importance weights exist; calibrated uncertainty NOT ESTABLISHED** | Reliability weighting is not uncertainty calibration. |
| P04 | **YES explicit ego-agent relational representation; NO reactive game/response model** | Important interaction boundary. |
| P05 | **map + history + relative geometry + motion hypotheses provide physical structure; no simulator-physics constraint in world latent** | Structured does not equal causal physics. |
| P06 | **single-step world-state refinement; no recursive long WM rollout, so rollout drift is not main deployment bottleneck** | Paper itself lists multi-step world modeling as future work. |
| P07 | **map semantics explicitly condition state; traffic-rule/risk semantics not separately represented** | Safety/rules remain mostly task-induced. |

---

# Residue / ontology decision

GraphWorld exposes two tempting residues:

```text
1. explicit graph topology / structured interaction representation
2. future-hypothesis-derived latent target vs factual-future latent target
```

Both can already be represented by combinations of existing axes:

```text
B03/B04 + P04  → representation structure / interaction semantics
F01/F02 + G01/G03 + F07 → future substrate and truth provenance
J04/J09 → planner↔world coupling carrier
F08 → flow coordinate semantics
```

Decision:

```text
NO ONTOLOGY V1.4
V1.3 RETAINED
```

GraphWorld therefore acts as a successful stress test of the existing coordinate system rather than forcing another paper-specific axis.
