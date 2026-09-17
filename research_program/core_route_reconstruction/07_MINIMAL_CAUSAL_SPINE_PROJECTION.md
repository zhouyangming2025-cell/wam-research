# Minimal Causal Spine Projection Across Canonical and Broader Target-Domain Evidence

Status: **PROVISIONAL PROJECTION — NOT AN ONTOLOGY SPEC**  
Branch: `research/core-route-reconstruction`  
Date: 2026-09-17  
Parents: `05_MINIMAL_BRANCH_RECONSTRUCTION.md`, `06_ADVERSARIAL_MOTIF_REGRESSION.md`

## 0. Purpose

This document asks whether the surviving causal spine can reconstruct the known target-domain evidence **without forcing every paper into one exclusive class**.

Provisional spine:

- `M0` — compiled world knowledge: world/predictive computation changes deployed components through learning, with no required online world/future mediator;
- `M1` — online world-first mediation: `O -> Z -> A`;
- `M2` — action-conditioned consequence mediation: `O -> A~ -> Z(A~) -> A*`;
- `M3` — joint world-action co-generation under a strict jointness gate;
- `M4` — reciprocal world-action refinement before commitment.

Allowed projection states:

- one primary motif;
- primary + secondary motif when the paper genuinely synthesizes mechanisms;
- `NOT-WAM-BRIDGE` for ordinary planner mechanisms that do not carry world-model capability into action;
- `BOUNDARY` for world generation/simulation without a final one-stage planning commitment;
- `UNRESOLVED` when evidence is insufficient;
- paper-level and mode-level projections may differ.

A projection success is **not** evidence that the spine is correct. The important tests are false merge, false split, explanatory loss, and held-out predictiveness.

---

## 1. Projection gates

### M0 gate

Use only when a separately traceable world/predictive/simulation process causally changes the deployed planner/policy/scorer through learning, while the relevant future/world computation is not required on the deployed action path.

Do not use M0 merely because a model was pretrained.

### M1 gate

Use when a qualifying online world/future state `Z` is formed before final action reasoning and directly conditions planning, **without requiring a provisional ego alternative to instantiate a distinct consequence branch**.

### M2 gate

Use only when a provisional/candidate ego behavior `A~_k` indexes a distinct predicted consequence `Z(A~_k)`, and that candidate-specific consequence causally affects selection or refinement.

Candidate generation/scoring alone is insufficient.

### M3 gate

Use only when world/future and ego-action variables are generated/predicted inside one common generative program or joint sampled future. Shared encoder, shared latent, parallel heads, or multitask loss alone are insufficient.

### M4 gate

Use only when a revised action/planning state feeds back into a world update and this updated world state again changes planning before commitment. Iterative refinement inside only one side is insufficient.

---

## 2. Canonical-set projection

| Paper / scoped planning mode | Primary motif | Secondary / composition | Confidence | Reason |
|---|---|---|---|---|
| LAW | `M0-A predictive representation shaping` | — | HIGH | Action-conditioned future latent prediction shapes representation/planner during learning; future predictor is not the online decision mediator. |
| Epona planning | `M1 world-first shared temporal state` | joint world/trajectory training profile | MEDIUM-HIGH | Shared causal temporal latent supports trajectory generation; video rendering can be disabled, but the learned temporal world state remains the planning substrate. |
| DriveLaW | `M1 generator-latent mediation` | `M0-A` pretraining inheritance | HIGH | Video-generator internal latent is explicitly injected into Action DiT; chained latent-to-planner bridge is the paper thesis. |
| World4Drive | `M2 intention-conditioned consequence` | predictive/self-supervised latent learning | HIGH | Different intentions/candidates induce distinct future latents; latent-world selector ranks trajectories. |
| WorldDrive | `M2 distilled candidate consequence` | `M0-A` representation inheritance | HIGH | Candidate-specific future latent remains online through FAR, while world-generation-pretrained visual/motion encoders are also inherited. Genuine synthesis. |
| WoTE | `M2 explicit rollout evaluation` | — | HIGH | Candidate trajectory conditions recurrent BEV world rollout; future states feed reward-based selection. |
| SeerDrive paper | `M4 reciprocal refinement` | contains M1/M2-like steps inside loop | HIGH for paper claim; replication LOW | Bidirectional scene/planning iteration is the claimed paradigm shift. |
| SeerDrive code | `M2-like candidate/future selection` | — | MEDIUM | Existing code audit suggests a shallower candidate-future-selection path than the paper's reciprocal program. Preserve paper/code divergence. |
| Drive-JEPA PF | `M0-A predictive representation transfer` | — | HIGH | V-JEPA representation transfers to simple planner. |
| Drive-JEPA PB | `M0-A predictive representation transfer` | `NOT-WAM-BRIDGE`: multimodal proposal/distillation/scorer | HIGH | PB adds candidate planning, but candidates do not instantiate per-candidate world consequences. Same WAM bridge family as PF. |
| Metis | `M0-D joint training / future bypass` | shared latent / asymmetric information-flow profile | HIGH | Future observation prediction is training-side; action inference is explicitly independent of generated future-video tokens. |
| DynFlowDrive | `M0-B world-derived scorer supervision` | — | HIGH | Dynamic WM creates stability/reconstruction supervision; WM is absent at inference and scorer remains. |
| Discrete-WAM joint world-policy mode | `M3 joint world-action generation` | unified discrete representation paradigm | HIGH for joint mode | Future visual and action tokens are joint prediction/editing targets in one world-policy mode. |
| Discrete-WAM policy mode | `M0-D/M0-A unresolved mixture` | hierarchical decision->action policy profile | MEDIUM | World-policy pretraining shapes shared backbone, but deployed policy mode predicts decision/action without necessarily jointly generating future visual tokens. Do not inherit M3 automatically. |
| GraphWorld | `M1 relational world-state mediation` | future-target temporal learning | HIGH | Ego-centric relational world state directly conditions long-horizon planning; no candidate-specific rollout required. |

### Canonical result

The projection repairs three old distortions:

1. Drive-JEPA PF/PB preserve one WAM bridge lineage while retaining planner differences outside the bridge.
2. WorldDrive can legitimately receive `M0 + M2` rather than being forced into one label.
3. Discrete-WAM can have different mode-level route evidence without reducing the entire paper to one “joint” code.

---

## 3. D01 neutral-mechanism projection

Source basis: `research_program/domain_corpus/d01/03_MECHANISM_SKELETONS.md`.

| D01 artifact | Projection | Confidence | Comment |
|---|---|---|---|
| Drive-WM planning | `M2` | HIGH | Ego candidate -> candidate-conditioned future views -> planning cost -> selected trajectory. |
| Drive-WM generation | `BOUNDARY` | HIGH | Terminal output is world/video, not action commitment. |
| OccWorld planning | `M1` | HIGH | Online occupancy future horizon conditions planning; no established candidate-indexed consequence bank. |
| Think2Drive policy learning | `M0-C policy optimization via imagination` | HIGH | Imagined latent rollouts/reward train actor/critic; long imagination is training-side. |
| DrivingGPT planning | `M3` | HIGH | World/action tokens share one autoregressive generative language/process. |
| DrivingGPT generation | `BOUNDARY` | HIGH | Generation terminal only. |
| Drive-OccWorld planning | `M1` | HIGH | Forecast occupancy -> planner. |
| ViDAR downstream planning | `M0-A predictive representation transfer` | HIGH | Future geometry prediction is pretraining-side; representation transferred to planner. |
| DriveWorld downstream planning | `M0-A predictive representation transfer` | MEDIUM-HIGH | Predictive world pretraining principally transfers through adapted backbone. |
| Auto-JEPA intent planning | `UNRESOLVED: M1-like` | MEDIUM | Online future-intent latent guides retrieval/refinement, but object is compressed ego-motion intent rather than clearly environmental world consequence. Preserve qualification uncertainty. |
| WorldRFT planning | `UNRESOLVED M0/M1` | MEDIUM | Predictive latent and reward fine-tuning shape planner; exact runtime status of predictive mediator not sufficiently closed. |
| ReWorld planning | `M0-A` | HIGH | Predictive representation -> trajectory generator; prediction machinery can be dropped. |
| WA-JEPA planning | `M0-A` | HIGH | Future/action predictive targets shape shared representation; deployed action path retained while target machinery removed. |
| DA-WAM planning | `M2` | HIGH | One distinct future latent per candidate enters scorer. Strong positive anchor. |
| SafeDrive planning | `M2` | HIGH | Ego proposal -> proposal-conditioned sparse future world -> safety reasoning -> selected/refined trajectory. |
| Gen-Drive multi-sample | `M3` | HIGH | Joint ego/agent future scenes are sampled together; evaluator ranks generated joint futures downstream. |
| Gen-Drive single-sample | `M3` | HIGH | Joint future remains online; reward may be compiled into generator parameters but joint generation still defines deployed sample. |
| SimWAM action-only | `M0-D joint training / future bypass` | HIGH | Future video is training-side and isolated from deployed action dependency. |
| DriveFuture planning | `M2 solver-internal consequence guidance` | MEDIUM-HIGH | Provisional trajectory conditions future latent; future latent guides diffusion planning. No full reciprocal alternation established. |
| Policy World Model planning | `M1` | HIGH | Online future state-token horizon -> latent future features -> trajectory decoder. |
| CausalDrive simulator/evaluator | `BOUNDARY` | HIGH | Terminal simulator/evaluation world response. |
| CausalDrive policy post-training | `M0-C` | HIGH | Simulator/reward rolls out during training; deployed policy drops simulator. |
| RaWMPC planning | `M2` | HIGH | Candidate sequence -> action-conditioned horizon rollout -> risk/progress cost -> selected sequence. |

### D01 result

The broad census independently populates every mature motif except `M4` and supplies clean boundary modes. This supports recurrence of `M0/M1/M2/M3`, but does not establish that their current internal granularity is final.

---

## 4. D01.3 blind-set projection

Source basis: `research_program/ontology_blind_test/d01_3/03_ONTOLOGY_FREE_BLIND_CARDS.md`.

| Blind artifact | Projection | Confidence | Comment |
|---|---|---|---|
| GraphAD planning | `M1-pressure` | MEDIUM-HIGH | Future agent-motion predictions shape interaction graph then direct ego planning. Iterative graph refinement is not sufficient for M4. |
| DriveDreamer future-video | `BOUNDARY` | HIGH | Terminal future video. |
| DriveDreamer action path | `M1` | MEDIUM | Recurrent predicted structural/world features feed direct action decoder; exact video-decoder retention remains unresolved but candidate-indexed world branching is absent. |
| DrivoR planning | `NOT-WAM-BRIDGE` | HIGH | Candidate -> decomposed scorer -> weighted selection; no separately predicted future world/consequence. Critical negative control for M2. |

### Blind-set result

The blind set reinforces the distinction between:

- future/world-mediated direct planning (`M1`), and
- ordinary candidate selection with no world consequence (`NOT-WAM-BRIDGE`).

It does not independently replicate M4.

---

## 5. D02-W1 in-domain pressure projection

Important: old `R-W-E-L` family labels are ignored here. Only the neutral mechanism descriptions are reused.

| Paper | Projection | Confidence | Comment |
|---|---|---|---|
| BeTop | `M1-pressure` | MEDIUM-HIGH | Future multi-agent trajectories/topology guide direct trajectory generation; exact WAM carrier qualification remains a scope question, not a motif question. |
| TOAD | `NOT-WAM-BRIDGE` | HIGH | Test-time candidate search against learned trajectory reward, no predicted world consequence. |
| CRAFT | `M0-C` | HIGH | Counterfactual/interative learning signal -> policy optimization; counterfactual branch not deployed. |
| Hydra-MDP | `NOT-WAM-BRIDGE` | HIGH | Candidate heads + teacher/scorer distillation without online predicted world consequence. |
| DRIVEVLM | `NOT-WAM-BRIDGE / adjacent` | HIGH | Semantic reasoner -> action; valuable decision architecture but not itself evidence of WAM causal bridge. |
| OmniDrive | `UNRESOLVED M0-like / adjacent` | MEDIUM | Counterfactual synthetic reasoning improves deployed VLM, but whether this constitutes a qualifying world-model program is unclear. |
| ORION | `NOT-WAM-BRIDGE / adjacent` | HIGH | Semantic planning token -> generative action; not a world-model bridge on current evidence. |
| GenAD | `M3` | HIGH | Ego and surrounding-agent futures generated together in structural latent future process. |
| UniAD | `M1-pressure` | MEDIUM-HIGH | Future motion/occupancy structure conditions direct planner; whether to call it WAM is a domain-membership issue separate from bridge topology. |
| VAD | `M1-pressure / scope-limited` | MEDIUM | Predicted future motion guides direct planner, but explicit WAM qualification remained evidence-limited in D02. |

### D02 result

This projection exposes an important benefit of the new reconstruction:

> ordinary candidate planning, semantic hierarchy, and world-mediated planning no longer need to be forced into the same WAM route map merely because they were useful boundary controls in the old ontology.

The causal spine can therefore coexist with a stricter domain gate.

---

## 6. False-merge audit

### 6.1 M0 is currently over-broad

`M0-A` predictive representation transfer is not equivalent to:

- `M0-B` evaluator/scorer distillation;
- `M0-C` imagination/simulator-driven policy optimization;
- `M0-D` joint world/action training with future bypass.

If these were shown as one final route, the map would repeat the old `W0` error.

Verdict: **M0 is ancestor-only, mandatory sub-branching needed.**

### 6.2 M1 may still be over-broad

Potentially distinct sublineages include:

- structured future-state -> planner: occupancy / agent motion / BEV;
- relational current world state -> planner: GraphWorld;
- generator-internal latent -> planner: DriveLaW;
- shared temporal latent -> action generator: Epona;
- autoregressive future state tokens -> planner: Policy World Model.

Current evidence proves a common `world-before-action` bridge, but not that these should be one leaf route.

Verdict: **M1 is mature ancestor, leaf structure unresolved.**

### 6.3 M2 is also ancestor-level

Potential internal forks:

- explicit rollout + reward/cost: WoTE, Drive-WM, RaWMPC;
- compact candidate-specific future latent + scorer: DA-WAM;
- intention/future plausibility matching: World4Drive;
- distilled future surrogate + reward: WorldDrive;
- future latent integrated inside trajectory solver/refinement: DriveFuture;
- sparse proposal-conditioned future world + safety reasoning: SafeDrive.

Verdict: **M2 is a strong major branch, not yet a final leaf.**

### 6.4 M3 requires mode discipline

DrivingGPT, GenAD, Gen-Drive joint mode, and Discrete-WAM joint mode satisfy the current strict gate differently. Shared jointness is real, but the “world” object varies from visual tokens to other-agent trajectories.

Verdict: **M3 survives as branch candidate; exact semantic gate needs later tightening.**

---

## 7. False-split audit

### Drive-JEPA PF vs PB

Do not split WAM route: same predictive-representation bridge; PB's proposal/scorer is downstream specialization.

### LAW vs Drive-JEPA

Both `M0-A`, but do not erase learning-program difference: LAW integrates action-conditioned prediction into E2E training; Drive-JEPA scales separate V-JEPA pretraining/transfer.

### GraphWorld vs occupancy/prediction-conditioned planners

All currently share M1 ancestor despite radically different world substrate. The substrate alone is insufficient for a top-level split.

### WoTE vs DA-WAM

Both share M2 ancestor despite recurrent BEV rollout vs one-step candidate future latent. Whether horizon/rollout depth defines a lower subroute remains open.

### DrivingGPT vs GenAD

Both satisfy M3 but use different joint future languages. Do not split merely because one is visual/action token autoregression and one is structural trajectory generation.

---

## 8. Composition audit

The spine must permit paper composition.

Confirmed/strong examples:

- **WorldDrive:** `M0-A + M2`.
- **DriveLaW:** M1 primary with world-generation pretraining inheritance as learning support.
- **Gen-Drive multi-sample:** M3 joint future generation + downstream evaluator/resolver; evaluator does not transform it into M2 because ego proposal does not externally index a separately generated world branch before joint sample birth.
- **Discrete-WAM:** M3 in joint mode + separate policy mode + representation paradigm.
- **SeerDrive:** M4 contains alternating M1/M2-like directional steps, but M4 should remain the higher-order motif when the full reciprocal loop is active.

Rule:

> A secondary motif is recorded only when it is an independently traceable causal bridge, not merely because a substep resembles another motif.

---

## 9. Domain-gate correction

The old census deliberately included strong adjacent controls such as candidate planners and semantic planners. Under the new program, route discovery and domain membership should be separated:

1. **Domain gate:** is there a separately traceable world/predictive/dynamics program that causally contributes to one-stage planning?
2. **Bridge projection:** if yes, through which causal motif does it contribute?
3. **Planner profile:** candidate bank, semantic hierarchy, diffusion policy, resolver objective, etc.

This prevents TOAD / Hydra-MDP / DrivoR / ORION from being mistaken for world-model route evidence simply because they are useful planner comparisons.

---

## 10. Current minimal causal spine status

| Spine candidate | Recurrence | Clean negatives | Internal granularity | Current status |
|---|---|---|---|---|
| `M0` compiled world knowledge | very high | yes | far too broad | **ancestor candidate; must split** |
| `M1` world-first online mediation | high | yes | probably broad | **major branch candidate** |
| `M2` action-conditioned consequence | high | very strong | definitely broad | **major branch candidate; strongest** |
| `M3` joint world-action generation | medium/high | strong gate available | moderate | **major branch candidate** |
| `M4` reciprocal refinement | one strong anchor | near-neighbors fail gate | unknown | **provisional singleton extension** |

This is the first structure in the project that simultaneously:

- preserves Drive-JEPA PF/PB family coherence;
- separates ordinary candidate scoring from world-consequence reasoning;
- allows WorldDrive to be a synthesis paper;
- preserves Epona/DriveLaW/Metis disagreement;
- keeps SeerDrive's claimed paradigm shift visible;
- does not require resolver semantics to be a top-level route axis.

That is encouraging, but still not enough for ontology acceptance.

---

## 11. Next research gate

The next highest-value task is **sub-branch reconstruction**, not more corpus expansion.

Priority order:

1. reconstruct `M0` internal branches, because it is currently the largest false-merge risk;
2. reconstruct `M2` internal branches, because it is the strongest mature route but contains several scientifically different consequence mechanisms;
3. reconstruct `M1` only after M0/M2, because some M1 cases may actually be representation paradigms rather than distinct planning routes;
4. hold `M3` gate fixed and search for counterexamples;
5. keep `M4` provisional until independent replication appears.

For each ancestor motif, repeat:

- common ancestor;
- main scientific fork;
- Core-Bridge Deletion Test;
- Between-Paper Collapse Test;
- implementation invariance;
- negative control;
- composition with other motifs.

Do not name final CoreRoutes until at least `M0` and `M2` internal false-merge risks are resolved.
