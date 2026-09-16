# P0066 SAFE-SIM — Ontology V1 + V1.1 + V1.2 + V1.3 Projection

Last updated: 2026-09-16

Status: **FULL DIMENSION-FIRST PROJECTION — COMPLETE FIRST PASS**

Canonical analysis:

```text
papers/deep_analysis/P0066_SAFESIM_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C7_SAFESIM_AUDIT.md
audits/literature/P0066_SAFESIM_SOURCE_CODE_AUDIT.md
```

Core warning:

```text
reactive closed-loop generated response
!=
paired real-world intervention-response truth
```

---

# A. Problem / role

| ID | SAFE-SIM value |
|---|---|
| A01 | planner safety evaluation under rare/long-tail interactive traffic behavior |
| A02 | learned reactive simulator / evaluation environment; future behavior is generated to challenge an external planner |
| A03 | external ego planner interacting sequentially with simulator; not an internal candidate-bank planner |
| A04 | traffic behavior simulation + guided diffusion + adversarial scenario generation lineage |

# B. Current-state representation

| ID | SAFE-SIM value |
|---|---|
| B01 | agent-centric rasterized map + traffic-agent histories / kinematic states |
| B02 | fixed historical agent context before each replanning call; exact history length depends on implementation/configuration |
| B03 | raster scene features + current multi-agent physical state |
| B04 | geometry, lane/map structure, agent motion and interaction context; no photorealistic sensor appearance target |
| B05 | planner/reactive policy consume updated current/history state every loop; generated future trajectories are executed partially then refreshed |

# C. Representation provenance

| ID | SAFE-SIM value |
|---|---|
| C01 | learned diffusion behavior prior built on traffic-behavior-simulation / trajdata stack; ResNet raster encoder + temporal U-Net diffusion |
| C02 | training on real trajectory data; map/history enter conditioning; safety-criticality added mainly by test-time guidance |
| C03 | simulator behavior model is pretrained/trained before evaluation; evaluated ego planner is separate; guidance changes samples, not model weights |
| C04 | base-prior vs guidance contribution is partially separated through guidance/regularization/partial-diffusion ablations, but no complete causal decomposition of all source components |

# D. Action / candidate space

| ID | SAFE-SIM value |
|---|---|
| D01 | ego action condition comes from the currently evaluated planner; non-ego trajectories come from diffusion samples; optional adversarial proposals are rule/domain generated |
| D02 | ego future path as planned positions; reactive-agent diffusion operates over action trajectories that induce state trajectories |
| D03 | no language command; route/centerline geometry can constrain or guide traffic behavior |
| D04 | multiple non-ego future trajectory samples exist for filtering; this is simulator behavior sampling, not ego candidate-bank planning |
| D05 | behavior diversity comes from diffusion samples, adversarial parameters and partial-diffusion proposals; exact sample count is config-dependent |
| D06 | sample filtering selects a low-guidance-cost reactive trajectory; optional partial diffusion seeds controllable collision proposals |

# E. Action → world coupling

| ID | SAFE-SIM value |
|---|---|
| E01 | **PRESENT** — current ego plan explicitly influences surrounding-agent generation/guidance |
| E02 | ego planner trajectory is inserted into non-ego observation as `ego_plan` and consumed in collision/TTC guidance |
| E03 | shared reactive diffusion model generates multiple agents/samples with control masks / per-agent parameters rather than one independent world model per branch |
| E04 | alternatives are resampled/replanned over repeated physical closed-loop steps; no persistent fixed candidate-world tree is retained |
| E05 | simulator is deliberately queried under safety-critical / off-log ego-adversary configurations; extrapolation validity is only partially checked via realism proxies and cross-dataset tests |

# F. Dynamics / future time

| ID | SAFE-SIM value |
|---|---|
| F01 | future non-ego action trajectories + induced physical state trajectories |
| F02 | traffic behavior, geometry, interaction and collision-related future motion |
| F03 | trajectory diffusion + explicit vehicle dynamics + repeated environment simulation |
| F04 | each policy call generates a finite-horizon trajectory; simulator executes only first few actions then replans |
| F05 | paper visualization discusses ~3.2 s plans; both planner and reactive agents update at 2 Hz in reported experiments; intermediate states directly drive the next simulation cycle |
| F06 | stochastic/multimodal diffusion sampling; no calibrated probabilistic intervention uncertainty is reported |
| F07 | future is generated from current/history state and current ego plan; surrounding behavior is endogenous to updated closed-loop context rather than a fixed logged future |
| F08 | diffusion denoising step k is an internal generative coordinate; physical simulation time t is distinct; partial diffusion k_p=γK is not physical time |

# G. Future supervision / truth

| ID | SAFE-SIM value |
|---|---|
| G01 | observational real-world future trajectories supervise/define the learned behavior distribution; no paired alternative-ego intervention response truth |
| G02 | future target is trajectory/action/state behavior rather than latent pseudo-target |
| G03 | factual logged behavior supports base model training, but adversarial guided futures are not directly factual targets |
| G04 | safety-criticality comes from differentiable test-time objectives (collision, TTC, relative speed, route/interaction regularization), not from a learned future-risk label head |
| G05 | no imitation of ego expert is central to simulator role; surrounding agents learn observational behavior prior |
| G06 | many generated alternative trajectories exist, but candidate-specific direct future truth for each guided alternative is absent |
| G07 | training support is observational traffic; aggressive guided behavior can move off support; realism/off-road metrics are used as partial checks |
| G08 | **reactive alternative-agent behavior is generated**, but **ground-truth intervention-response supervision is absent** |

# H. Branch identity / assignment

| ID | SAFE-SIM value |
|---|---|
| H01 | branch identity = diffusion sample / agent / optional adversarial proposal, not semantic ego-intention mode |
| H02 | sample identity exists only during generation/filtering; selected behavior is executed and loop refreshes |
| H03 | no oracle assignment of alternative branches to observed counterfactual futures |
| H04 | filtering picks low guidance cost; no explicit oracle best-of-N behavioral-truth ceiling reported |

# I. Counterfactuality / reactivity

| ID | SAFE-SIM value |
|---|---|
| I01 | output surrounding behavior is conditioned on current ego plan and changed scene state |
| I02 | no direct ground-truth alternative-action future supervision |
| I03 | no paired intervention world-state GT |
| I04 | **PRESENT — endogenous surrounding-agent response is regenerated after environment/ego change** |
| I05 | intervention validity assessed indirectly via distributional realism, off-road/collision behavior, controllability and qualitative examples; no causal intervention benchmark |

# J. World → planning interface

| ID | SAFE-SIM value |
|---|---|
| J01 | generated world behavior is primarily an external evaluation environment, not an internal ego planner feature |
| J02 | learned traffic behavior model remains online during simulation |
| J03 | ego planner consumes updated simulated scene state indirectly through normal observation loop, not a privileged learned future latent |
| J04 | repeated external environment feedback shapes subsequent planner decisions; no joint end-to-end planner training in audited setup |
| J05 | simulator does not directly choose ego candidate; it evaluates/challenges whatever planner acts |
| J06 | no explicit ego utility/value scorer is the primary interface |
| J07 | simulator must remain online for closed-loop evaluation; not a training-only discarded world model in the reported experiments |
| J08 | two nested iterations: diffusion denoising/guidance internally and physical closed-loop replanning externally; these must remain semantically separate |
| J09 | **explicit planner→world feedback carrier = current ego plan (`ego_plan`) plus physically updated scene state** |

# K. Scorer semantics

| ID | SAFE-SIM value |
|---|---|
| K01 | guidance/filtering costs score non-ego trajectory samples; not an ego planning scorer |
| K02 | guidance semantics include collision induction, TTC/aggressiveness, relative speed, route/interaction plausibility |
| K03 | scorer/guidance consumes generated agent trajectory plus current ego plan / scene geometry |
| K04 | hybrid multi-term guidance cost with different regularization/adversarial weights |
| K05 | objectives are hand-designed differentiable simulation controls rather than learned human preference/value labels |

# L. Training topology

| ID | SAFE-SIM value |
|---|---|
| L01 | behavior diffusion model training precedes planner evaluation; adversarial guidance occurs at inference |
| L02 | raster context encoder + diffusion trajectory model + dynamics/guidance pipeline |
| L03 | external ego planner, behavior model, dynamics/environment and guidance are separable modules |
| L04 | training gradients fit diffusion behavior prior; inference guidance gradients alter sampled non-ego actions; planner parameters do not receive audited guidance gradients |
| L05 | ego planner remains external/frozen relative to simulator; source does not indicate joint planner fine-tuning through SAFE-SIM |
| L06 | diffusion denoising objective for behavior prior + inference-time differentiable guidance costs |
| L07 | no explicit supervised target for every repeated free-running closed-loop state beyond base observational behavior learning; loop validity mainly tested by rollout metrics |

# M. Future-knowledge lifecycle

| ID | SAFE-SIM value |
|---|---|
| M01 | learned traffic behavior prior is retained online as simulator environment knowledge |
| M02 | future behavior generation is active during every closed-loop evaluation cycle |
| M03 | cannot remove behavior model without changing simulator; no distilled planner replacement is reported |
| M04 | no simulator-to-planner distillation demonstrated |
| M05 | generated trajectories and explicit guidance factors are relatively interpretable; diffusion internal latent itself is not the decision artifact |
| M06 | deployment lifecycle = evaluation/simulation-time environment model, not ego vehicle deployment module |

# N. Compute / pruning

| ID | SAFE-SIM value |
|---|---|
| N01 | compute scales with repeated 100-step diffusion sampling, number of agents/samples and physical replanning cycles |
| N02 | learned reactive-agent model remains online during simulator rollout |
| N03 | no lightweight distillation path reported; sample filtering/partial diffusion target controllability rather than deployment compression |
| N04 | multi-agent/sample computation can be batched within framework; exact scaling not fully normalized in paper |
| N05 | reported simulation times include ~104.5 s SAFE-SIM vs ~427.2 s STRIVE for one nuScenes experiment configuration; not a universal real-time claim |
| N06 | no matched compute-normalized planner-evaluation frontier across guidance/sample counts |

# O. Evaluation / attribution

| ID | SAFE-SIM value |
|---|---|
| O01 | reactive closed-loop traffic simulation against multiple planners; nuScenes + zero-shot nuPlan-mini; not open-loop planning accuracy |
| O02 | no future-prediction ADE/FDE centerpiece; evaluation emphasizes distributional realism, collision/off-road, controllability/diversity and runtime |
| O03 | realism target = aggregate logged trajectory-profile distributions; not paired intervention response |
| O04 | partial diffusion and regularization ablations directly isolate controllability/diversity vs invalid behavior trade-offs |
| O05 | strongest matched evidence: partial diffusion increases collision-point diversity; removing regularization raises collision/off-road rate; SAFE-SIM improves tested realism/collision metrics over baselines |
| O06 | planner-specific collision rate bundles planner vulnerability, adversarial generation and simulator objective; must not be interpreted as a pure planner score |
| O07 | no real-vehicle closed-loop validation; behavior-state simulator differs from sensor-photorealistic closed-loop evaluation |
| O08 | paper verified; official code audited; complete local full raw-MD extraction not yet ingested |

# P. Safety / uncertainty / interaction / physical validity

| ID | SAFE-SIM value |
|---|---|
| P01 | explicit safety-critical scenario objectives, collisions, TTC and adversarial-agent control |
| P02 | no direct ego trajectory reward model; safety pressure is an environment-generation objective |
| P03 | stochastic diffusion provides diversity but calibrated response uncertainty is NOT REPORTED |
| P04 | **explicit learned multi-agent behavioral interaction / response loop** |
| P05 | vehicle dynamics + route/interaction regularization + off-road metrics provide partial physical/plausibility constraints |
| P06 | long closed-loop simulation can accumulate model error; paper evaluates long-horizon behavior but does not fully isolate compounding-error calibration |
| P07 | lane/route geometry and collision constraints enter guidance; traffic-rule semantics beyond these are not the main focus |

---

# Residue / ontology decision

Potential residue:

```text
simulator feedback topology / endogenous behavioral reactivity
```

Back-projection:

```text
J09 planner→world feedback carrier
I04/I05 reactive-response + intervention validity
O01/O07 evaluation regime
P04 explicit interaction
project feedback vector F_e/F_s/F_a/F_b
```

These already represent the distinction without adding a new stable dimension.

Therefore:

```text
V1.3 RETAINED
NO V1.4
```

---

# Final normalized identity

```text
SAFE-SIM
=
current multi-agent state + map/history
+ current external ego planner trajectory
→ diffusion reactive-agent future generation
+ adversarial / realism guidance
+ optional partial diffusion
→ selected non-ego actions
→ physical environment update
→ repeated replanning

explicit surrounding future                  YES
online reactive behavior model               YES
planner→world feedback                       YES
world→planner feedback through environment   YES
paired intervention-response truth           NO
internal planner candidate scoring            NO
sensor-photorealistic closed loop            NO / NOT CORE
```
