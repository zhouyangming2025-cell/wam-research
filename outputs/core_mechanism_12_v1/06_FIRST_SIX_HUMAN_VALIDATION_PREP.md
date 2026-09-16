# Core Mechanism 12 — First-Six Human Validation Preparation

Status: corrected reviewer worksheet for LAW, Epona, DriveLaW, World4Drive, WorldDrive, and WoTE. It preserves artifact/mode splits and leaves the row checkboxes blank; the completed decision is recorded in `08_FIRST_SIX_HUMAN_REVIEW_VERDICT.md`.

## 1. Reviewer instructions

For each row, verify:

1. the semantic input/output and lifecycle;
2. whether the cited edge actually changes A* or the declared generation output;
3. whether the nearest alternative was rejected for a causal reason rather than terminology;
4. whether ∅, UNKNOWN, and N/A are used correctly.

Human-decision options:

    □ ACCEPT
    □ REVISE
    □ UNKNOWN / NEED EVIDENCE

Evidence aliases:

| Alias | Repository evidence |
|---|---|
| LAW-P | papers/raw_md/P0048_LAW/P0048_LAW.raw.md |
| LAW-S | audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md |
| EPO-P | papers/raw_md/P0001_Epona/P0001_Epona.raw.md |
| EPO-S | audits/literature/PHASE_C5_EPONA_SOURCE_AUDIT.md |
| DLAW-P | papers/raw_md/P0009_DriveLaW/P0009_DriveLaW.raw.md |
| DLAW-S | audits/literature/PHASE_C6_DRIVELAW_AUDIT.md |
| W4D-P | papers/raw_md/P0046_World4Drive/P0046_World4Drive.raw.md |
| W4D-S | audits/literature/PHASE_C5_WORLD4DRIVE_AUDIT.md |
| WD-P | papers/raw_md/P0042_WorldDrive/P0042_WorldDrive.raw.md |
| WD-S | audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md |
| WOTE-P | papers/raw_md/P0045_WoTE/P0045_WoTE.raw.md |
| WOTE-S | audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md |

## 2. LAW

### 2.1 LAW-PF

Boundary: tracked raw paper revision UNKNOWN; inspected perception-free source BraveGroup/LAW at b2f6a….

| Field | Category | One-sentence semantic definition | Semantic input | Semantic output | Lifecycle | Causal role | Evidence | Nearest alternative | Why not the alternative | Confidence | Human decision |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C | C2@T direct | one factual/predicted future endpoint latent exists only to train the planner representation | current latent + predicted waypoint; factual next frame | predicted/target future latent | TRAIN_ONLY | future loss shapes deployed parameters; no runtime carrier | LAW-P §method/loss; LAW-S [PAPER+CODE FACT] | C2@R | deployed waypoint is produced before/without consuming F | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| X | {@T:X2,@R:N/A} | the model’s one predicted waypoint conditions the train-time future predictor | predicted waypoint | controlled future-latent prediction | TRAIN; runtime inapplicable | creates action-mediated learning edge | LAW-P; LAW-S [PAPER+CODE FACT] | X1 factual control | factual future is target; the conditioning action is predicted | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| D | D∅ | no qualifying runtime future/world carrier changes A* | current latent | waypoint A* | RUNTIME | direct planner only | LAW-P; LAW-S [PAPER+CODE FACT] | D1 | future predictor output is not an A* ancestor | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| P | P∅ | action is formed directly without semantic hierarchy or explicit bank/resolver | current latent | one waypoint trajectory | RUNTIME | direct commitment | LAW-P; LAW-S [PAPER+CODE FACT] | PB | no preserved candidate identities/common resolver | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| V | N/A | resolver semantics do not apply because no candidate resolver exists | N/A | N/A | RUNTIME | none | inferred from P∅ [OUR INFERENCE] | VM | nearest-mode loss is not a runtime resolver | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| T | all absent | no explicit runtime solver, reciprocal loop, model horizon rollout, or cross-cycle dependency | current observation | waypoint | RUNTIME | one direct decision graph | LAW-P; LAW-S [PAPER+CODE FACT] | Ts present | appendix/training recurrence is not canonical runtime solving | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| L | LA ordered program | predicted action→future prediction→future loss updates action/shared path; target is detached; future branch is dropped | predicted waypoint + factual future target | updated encoder/planner parameters | TRAIN→DEPLOY | action-mediated future supervision | LAW-S [CODE FACT] | LS | future branch depends on predicted waypoint, not only shared S | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |

### 2.2 LAW-PB

Boundary: paper mode; perception-based implementation and exact detach topology not independently verified.

| Field | Category | One-sentence semantic definition | Semantic input | Semantic output | Lifecycle | Causal role | Evidence | Nearest alternative | Why not the alternative | Confidence | Human decision |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C | C2@T direct | future latent supervises training but is absent from deployed waypoint inference | perception/current latent + predicted waypoint | future latent target/prediction | TRAIN_ONLY | auxiliary world/future shaping | LAW-P [PAPER FACT] | C1 current world | perception supervision alone does not pass the tightened C1 gate | MEDIUM | □ ACCEPT □ REVISE □ UNKNOWN |
| X | {@T:X2,@R:N/A} | predicted waypoint controls future prediction in training | predicted waypoint | future prediction | TRAIN | action-mediated branch | LAW-P [PAPER FACT] | X1 | conditioning action is policy-predicted | MEDIUM | □ ACCEPT □ REVISE □ UNKNOWN |
| D | D∅ | deployed perception path emits waypoint without future-carrier consumption | current perception state | A* | RUNTIME | no runtime future route | LAW-P [PAPER FACT] | D1 | no paper evidence that predicted F feeds A* | MEDIUM | □ ACCEPT □ REVISE □ UNKNOWN |
| P | P∅ | direct waypoint formation | perception state | waypoint | RUNTIME | direct action | LAW-P [PAPER FACT] | PB | no candidate bank/resolver | MEDIUM | □ ACCEPT □ REVISE □ UNKNOWN |
| V | N/A | no runtime resolver | N/A | N/A | RUNTIME | none | P∅ implication [OUR INFERENCE] | VX | evidence supports absence of resolver, not unknown semantics | MEDIUM | □ ACCEPT □ REVISE □ UNKNOWN |
| T | all absent | no runtime typed loop established | observation | waypoint | RUNTIME | direct inference | LAW-P [PAPER FACT] | UNKNOWN | paper path is sufficiently explicit for absence | MEDIUM | □ ACCEPT □ REVISE □ UNKNOWN |
| L | LA + perception stages; detach UNKNOWN | predicted waypoint conditions future learning alongside planning/perception objectives | perception, action and future targets | planner/perception parameters | TRAIN→DEPLOY | action-mediated future shaping | LAW-P [PAPER FACT]; U-002 | LAW-PF exact LA | same family, but target detach/parameter scope cannot be copied from PF source | MEDIUM | □ ACCEPT □ REVISE □ UNKNOWN |

## 3. Epona

### 3.1 EPO-PLAN

Boundary: ICCV 2025 raw copy; exact arXiv revision UNKNOWN; Kevin-thu/Epona at 69b24c…; planning-only traj_only path.

| Field | Category | One-sentence semantic definition | Semantic input | Semantic output | Lifecycle | Causal role | Evidence | Nearest alternative | Why not the alternative | Confidence | Human decision |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C | C2@T base + C3@T chain | factual one-step future learning is augmented by a detached self-generated context sequence, while both are bypassed during planning-only inference | history, factual next frame, periodic predicted contexts | future endpoint plus train-time chain context | TRAIN_ONLY | shared-state representation shaping and rollout-robustness curriculum | EPO-P; EPO-S §§6,9 [PAPER+CODE FACT] | C2@T only | chain-of-forward creates and reuses an ordered generated sequence during training | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| X | X(C2@T,base)=X1; X(C3@T,chain)=X2; @R:N/A | factual motion conditions base visual training; detached predicted motion conditions chain training | factual or predicted motion by stage | controlled future visual state | TRAIN | separates base teacher forcing from chain curriculum | EPO-P; EPO-S §§5,9 [PAPER+CODE FACT] | one @T:X1 value | it would erase predicted-control chain training | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| D | D∅ | planning path is history/MST→TrajDiT→A* | shared history state | trajectory | RUNTIME | no visual-future ancestor of A* | EPO-P; EPO-S [PAPER+CODE FACT] | D1 | visual generator is skipped | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| P | P∅ | action-flow decoding has no verified common candidate resolver | MST state | trajectory | RUNTIME | direct/implicit formation | EPO-S [CODE FACT] | PB | flow samples/iterations do not establish identity-preserving selection | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| V | N/A | no runtime candidate resolver | N/A | N/A | RUNTIME | none | P∅ implication [OUR INFERENCE] | VU | no utility scorer selects among candidates | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| T | Ts present only | action-flow numerical solver iterates without advancing physical time | noise/action estimate | trajectory estimate | RUNTIME | numerical sample refinement | EPO-P; EPO-S [PAPER+CODE FACT] | Th | solver coordinate is not rollout horizon | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| L | LS + detached chain-forward | sibling action/visual objectives update shared MST; periodic detached self-generated contexts augment the curriculum; visual branch is bypassed at planning deployment | factual targets and generated detached contexts | shared/action/visual parameters | TRAIN→DEPLOY | sibling multitask plus rollout-robustness training | EPO-P; EPO-S §§6,9 [PAPER+CODE FACT] | LA | predicted action is not the base visual-loss condition even though it is reused in the detached chain curriculum | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |

### 3.2 EPO-SELF

Boundary: same paper/source; self-generated future rollout mode.

| Field | Category | One-sentence semantic definition | Semantic input | Semantic output | Lifecycle | Causal role | Evidence | Nearest alternative | Why not the alternative | Confidence | Human decision |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C | C2@T base + C3@B | one-step visual learning is augmented by a train-time generated chain, while runtime performs the full self-generated horizon | history + factual or predicted motion | future endpoint and ordered visual-state sequence | TRAIN and RUNTIME | rollout training context and deployed generation output/context | EPO-P; EPO-S §§5,8,9 [PAPER+CODE FACT] | C2@T + C3@R | omits the train-time generated chain carrier | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| X | X(C2@T,base)=X1; X(C3@T,chain)=X2; X(C3@R,self)=X2 | factual motion trains the base visual objective; detached predicted motion controls chain training and predicted motion controls runtime self-rollout | factual or predicted motion by stage/lifecycle | controlled next visual state | BOTH with stage-specific values | separates teacher forcing, chain curriculum, and self-control | EPO-P; EPO-S §§5,9 [PAPER+CODE FACT] | one unqualified lifecycle value | would erase the X1/X2 switch within training | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| D | D5 | consequence generation is this mode’s terminal output rather than planning A* | history + predicted motion | generated future video/latent sequence | RUNTIME | generation/simulation output | EPO-P; EPO-S [PAPER+CODE FACT] | D3 | no world→policy→world refinement toward one A* | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| P | N/A | no action-commitment task is evaluated in this generation mode | N/A | N/A | RUNTIME | none | mode boundary [OUR INFERENCE] | P∅ | P∅ would imply a planning A* exists | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| V | N/A | no candidate resolver | N/A | N/A | RUNTIME | none | P=N/A [OUR INFERENCE] | VX | resolver is inapplicable, not unknown | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| T | Ts + Th present | inner diffusion/flow solving is nested inside outer modelled future steps | solver state; generated state at τ | next estimate; next physical-horizon model state | RUNTIME | numerical generation plus model rollout | EPO-P; EPO-S [PAPER+CODE FACT] | Tr | no reciprocal policy refinement before commitment | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| L | LS + detached chain-forward | sibling multitask is augmented with periodic detached self-generated contexts | factual and generated contexts | updated shared/visual/action parameters | TRAIN→DEPLOY | supports rollout robustness | EPO-S [CODE FACT] | LA | standard loss still uses factual motion; generated context is detached | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |

### 3.3 EPO-CTRL

Boundary: same paper/source; externally controlled generation mode.

| Field | Category | One-sentence semantic definition | Semantic input | Semantic output | Lifecycle | Causal role | Evidence | Nearest alternative | Why not the alternative | Confidence | Human decision |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C | C2@T base + C3@T chain + C3@R controlled | shared training contains factual one-step prediction and detached self-generated chains; deployment emits an externally controlled horizon | history, factual/predicted train motion, supplied runtime poses | future endpoint and generated visual sequence | TRAIN and RUNTIME | training curriculum plus terminal controlled generation | EPO-P; EPO-S §§5,8,9 [PAPER+CODE FACT] | C2@T + C3@R | omits the train-time generated chain carrier | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| X | X(C2@T,base)=X1; X(C3@T,chain)=X2; X(C3@R,controlled)=X1 | base training uses factual motion, chain training uses predicted motion, and controlled rollout uses supplied motion | factual, predicted, or external pose/yaw by stage | next visual state | BOTH with stage-specific values | separates training curriculum from external-control deployment | EPO-P; EPO-S §§5,9 [PAPER+CODE FACT] | one @T:X1 value | it erases the chain stage's predicted control | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| D | D5 | generated visual future is terminal output | controlled history | future frames/latents | RUNTIME | generation only | EPO-P; EPO-S [PAPER+CODE FACT] | D1 | no planning A* consumes carrier | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| P | N/A | external control means no action commitment | N/A | N/A | RUNTIME | none | mode boundary [OUR INFERENCE] | PH | supplied pose is not a model-selected semantic decision | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| V | N/A | no resolver | N/A | N/A | RUNTIME | none | P=N/A [OUR INFERENCE] | V∅ | no resolver exists to have an empty criterion | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| T | Ts + Th present | numerical visual solving repeats across modelled future steps | solver state and future context | controlled future sequence | RUNTIME | generation clock topology | EPO-P; EPO-S [PAPER+CODE FACT] | Tc | supplied future controls are not previous-cycle state | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| L | LS + detached chain-forward | factual-motion visual training shares MST with action task and periodic detached predicted contexts augment training; deploy visual path for this mode | factual targets and generated detached contexts | shared and visual parameters | TRAIN→DEPLOY | shared-state world learning plus rollout curriculum | EPO-P; EPO-S §§6,9 [PAPER+CODE FACT] | LA | predicted policy action is not the base visual-loss condition | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |

## 4. DriveLaW

### 4.1 DLAW-PAPER

Boundary: arXiv:2512.23421v3/CVPR 2026; paper planning path.

| Field | Category | One-sentence semantic definition | Semantic input | Semantic output | Lifecycle | Causal role | Evidence | Nearest alternative | Why not the alternative | Confidence | Human decision |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C | C4@B internal | early Video-DiT denoising state is an online future-generative carrier | history/noise/text context | cached blockwise video-generative state | BOTH | conditions Action DiT | DLAW-P [PAPER FACT] | C1 | state belongs to future-video generation, not only current relational world | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| X | X(C4@T)=X∅; X(C4@R)=X∅ | no future action/control variable conditions the video carrier in pretraining or planning | observation/noise/history context | generative carrier | TRAIN and RUNTIME | observation-driven carrier production | DLAW-P [PAPER FACT] | @R:X∅ only | C4 exists at both lifecycles and action is downstream consumer, not upstream control | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| D | D1 | generative carrier directly conditions one action-generation path | C4 + command/status + action noise | trajectory A* | RUNTIME | carrier-conditioned action | DLAW-P [PAPER FACT] | D2 | no A{k}→F{k}→resolver topology | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| P | P∅ | Action DiT implicitly forms a trajectory without a common candidate resolver | conditioned action noise | trajectory | RUNTIME | direct/implicit formation | DLAW-P [PAPER FACT] | PB | diffusion sampling is not proven candidate commitment | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| V | N/A | no explicit resolver | N/A | N/A | RUNTIME | none | P∅ [OUR INFERENCE] | VU | paper emphasizes no post scorer | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| T | Ts present only | action flow solver iterates; full future horizon is not rolled out for planning | action estimate | refined trajectory sample | RUNTIME | numerical solving | DLAW-P [PAPER FACT] | Th | denoising index is not physical time | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| L | LG | video-generative trunk is pretrained, then action loss adapts/uses it; early carrier retained while full decode is skipped | driving videos then planning trajectories | Video-DiT/Action-DiT parameters | PRETRAIN→FINETUNE→DEPLOY | retained generative carrier transfer | DLAW-P [PAPER FACT] | LP | predictive head is not simply dropped; generative trunk remains online | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |

### 4.2 DLAW-CODE

Boundary: official source at 243e0e…; solver/sign discrepancies retained.

| Field | Category | One-sentence semantic definition | Semantic input | Semantic output | Lifecycle | Causal role | Evidence | Nearest alternative | Why not the alternative | Confidence | Human decision |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C | C4@B internal | released planning path consumes early Video-DiT block states | history/noise | cached generative states | BOTH | planner condition | DLAW-S [CODE FACT] | ordinary hidden S | states are grounded in video-generative training/process | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| X | X(C4@T)=X∅; X(C4@R)=X∅ | carrier is not future candidate/action controlled in training or deployment | observation/noise/history | C4 | TRAIN and RUNTIME | upstream carrier | DLAW-S [CODE FACT] | @R:X∅ only | C4 exists at both lifecycles and no per-candidate future carrier is present | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| D | D1 | C4 conditions released Action DiT | C4 + ego/command | trajectory | RUNTIME | direct carrier route | DLAW-S [CODE FACT] | D2 | no resolver | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| P | P∅ | no verified bank→resolver | action noise/context | trajectory | RUNTIME | implicit formation | DLAW-S [CODE FACT] | PB | multiple solver states are not candidate identities | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| V | N/A | resolver absent | N/A | N/A | RUNTIME | none | source topology [CODE FACT] | VX | source verifies absence rather than leaving target unknown | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| T | Ts present only | released action-flow solver iterates; exact count is audit-ambiguous | solver state | trajectory | RUNTIME | numerical solve | DLAW-S [CODE FACT+UNKNOWN count] | separate T class by 5/10 steps | count does not change semantics | MEDIUM-HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| L | LG | action_full lets action loss update Video-DiT and Action-DiT; early carrier retained | planning loss | both trunks | FINETUNE→DEPLOY | retained generative adaptation | DLAW-S [CODE FACT] | frozen LP | Video-DiT is trainable in inspected configuration | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |

## 5. World4Drive

### 5.1 W4D-PLAN

Boundary: ICCV 2025/arXiv:2507.00603; official source at cffb51…; benchmark/config gradient boundary retained.

| Field | Category | One-sentence semantic definition | Semantic input | Semantic output | Lifecycle | Causal role | Evidence | Nearest alternative | Why not the alternative | Confidence | Human decision |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C | C1@B + C2@B direct | a physical current world state is transitioned into candidate-specific future endpoints | multiview history + A{k} | current W and F{k} | BOTH | supplies candidate consequence evidence | W4D-P; W4D-S [PAPER+CODE FACT] | ordinary BEV + C2 only | current carrier passes stateful transition/grounding gate | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| X | X(C1@B)=N/A; X(C2@B)=X3 | each candidate identity k controls its matching future endpoint, not the current carrier | A{k}+W | F{k} | BOTH | preserves counterfactual branch identity without mislabelling C1 | W4D-P; W4D-S [PAPER+CODE FACT] | unbound @B:X3 | two carriers share BOTH lifecycle, so carrier binding is mandatory | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| D | D2 | candidate consequence enters learned score then argmax | A{k},F{k},W | selected A{k*} | RUNTIME | online consequence selection | W4D-P; W4D-S [PAPER+CODE FACT] | D1 | action conditions consequence before selection | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| P | PB | six candidate identities reach one resolver | intention queries/candidates | k* and A* | RUNTIME | explicit commitment | W4D-P; W4D-S [PAPER+CODE FACT] | PH | simultaneous alternatives are compared, not one intent decoded | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| V | single VW | ScoreNet learns which candidate future latent best matches the factual future latent | predicted F{k} vs factual F_hat; latent MSE creates j | learned candidate score | TRAIN→RUNTIME | selects the mode predicted to best agree with the factual future world | W4D-P §3.3.2; W4D-S §4 [PAPER+CODE FACT] | VM | trajectory L1 shapes T{j}, but ScoreNet's class label j comes from future-latent MSE rather than trajectory geometry | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| T | all absent | candidate parallelism contains no typed online loop | current state/candidates | future endpoints/scores | RUNTIME | feedforward candidate evaluation | W4D-P; W4D-S [PAPER+CODE FACT] | Th | one endpoint per candidate is not a horizon rollout | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| L | retained joint graph; LA route partly UNKNOWN | future, score, trajectory and semantic losses train retained world/planner/scorer; future-loss path into A is config-uncertain | factual future/expert trajectory/semantic targets | deployed joint parameters | TRAIN→DEPLOY | retained online world-policy learning | W4D-P; W4D-S; U-009 | fully verified LA | candidate→F is known, exact gradient through A is not universal | MEDIUM-HIGH | □ ACCEPT □ REVISE □ UNKNOWN |

## 6. WorldDrive

### 6.1 WD-PLAN

Boundary: arXiv:2603.14948; official source at c375ee….

| Field | Category | One-sentence semantic definition | Semantic input | Semantic output | Lifecycle | Causal role | Evidence | Nearest alternative | Why not the alternative | Confidence | Human decision |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C | C2@T direct + C2@R surrogate | a heavy teacher future endpoint is distilled into a deployed candidate future surrogate | current state + A{k} | teacher F{k}; surrogate F̃{k} | TRAIN then RUNTIME | lightweight online consequence evidence | WD-P; WD-S [PAPER+CODE FACT] | separate surrogate class | temporal semantics are unchanged; realization differs | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| X | X(C2@T direct,pretrain)=X1; X(C2@T direct,FAR)=X3; X(C2@R surrogate)=X3 | factual/conditioned motion trains TA-DWM, then candidate k indexes FAR teacher targets and the runtime surrogate | factual trajectory or A{k} by stage | F/F{k}/F̃{k} | TRAIN and RUNTIME | preserves both pretraining provenance and candidate branch | WD-P §§3.2–3.4; WD-S §§2,5,7 [PAPER+CODE FACT] | one @T:X3 value | it erases the factual-control pretraining stage | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| D | D2 | surrogate consequence feeds reward and argmax | A{k},F̃{k},current state | selected candidate | RUNTIME | online consequence selection | WD-P; WD-S [PAPER+CODE FACT] | D∅ | heavy teacher is absent, but surrogate remains causal | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| P | PB{prefilter=top-K} | candidates are filtered for compute then share one reward resolver | anchor bank | k* and A* | RUNTIME | explicit commitment | WD-P; WD-S [PAPER+CODE FACT] | distinct filter class | deleting filter preserves reward semantics/argmax topology | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| V | pairwise VU | reward represents simulator/oracle planning utility preference | candidates/outcomes | scalar ordering/reward | TRAIN→RUNTIME | ranks best planning outcome | WD-P [PAPER FACT] | VM | target is PDMS/oracle preference, not factual trajectory likeness | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| T | all absent | heavy diffusion is dropped and deployed surrogate/reward is feedforward | current state/candidate | surrogate/reward | RUNTIME | no online typed loop | WD-P; WD-S [PAPER+CODE FACT] | Ts | teacher’s training/inference diffusion is not deployed planning | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| L | LP→joint(LT,LC) | TA-DWM first supplies transferred frozen encoders; FAR then learns future alignment and PDMS preference ranking as complementary objectives | pretrained encoders, teacher F targets and PDMS preferences | planner, surrogate and reward parameters | PRETRAIN→PLANNER TRAIN→JOINT FAR TRAIN→DEPLOY | representation transfer followed by joint distillation/ranking; heavy generator dropped | WD-P §§3.2–3.4; WD-S §§3,7 [PAPER+CODE FACT] | LT→LC | FAR's two losses are co-objectives, and omitting LP erases the paper's representation-inheritance mechanism | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |

## 7. WoTE

### 7.1 WOTE-PLAN

Boundary: tracked raw paper revision UNKNOWN; official source at 298957…; paper reward-sign wording remains bounded.

| Field | Category | One-sentence semantic definition | Semantic input | Semantic output | Lifecycle | Causal role | Evidence | Nearest alternative | Why not the alternative | Confidence | Human decision |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C | C1@B + C3@B direct | current semantic BEV is recurrently transitioned into candidate-specific future BEV/action horizons | current BEV + A{k} | ordered F{k,h} | BOTH | online rollout evidence | WOTE-P; WOTE-S [PAPER+CODE FACT] | C2 endpoint | identity persists across multiple modelled horizon states | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| X | X(C1@B)=N/A; X(C3@B)=X3 | each candidate ego trajectory controls its recurrent consequence sequence, not the current BEV carrier | A{k} | F{k,1…H} | BOTH | candidate branch control | WOTE-P; WOTE-S [PAPER+CODE FACT] | unbound @B:X3 | two carriers share BOTH lifecycle, so carrier binding is mandatory | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| D | D2 | each rollout is evaluated before candidate commitment | A{k},F{k,h},current state | selected A{k*} | RUNTIME | consequence-based selection | WOTE-P; WOTE-S [PAPER+CODE FACT] | D3 | rollout does not refine policy then feed back to world before selection | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| P | PB | candidate identities survive world rollout to common reward resolver | proposal set | k* and A* | RUNTIME | explicit commitment | WOTE-P; WOTE-S [PAPER+CODE FACT] | random rollout samples | candidates originate as explicit trajectories and remain keyed | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| V | fusion(VM,VD) | resolver combines imitation compatibility with decomposed simulator driving outcomes | candidate/rollout vs expert and simulator labels | final candidate reward | TRAIN→RUNTIME | selects by mixed factual and driving-value evidence | WOTE-P; WOTE-S [PAPER+CODE FACT] | pure VU | explicit components and imitation provenance must be retained | MEDIUM-HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| T | Th present only | recurrent transition advances modelled physical future horizon inside one decision | F{k,h} | F{k,h+1} | RUNTIME | candidate consequence rollout | WOTE-P; WOTE-S [PAPER+CODE FACT] | Tr | no consequence→policy→consequence co-refinement loop | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |
| L | retained joint graph + LC | BEV, reward, imitation, and trajectory objectives train modules all retained online | semantic future maps, simulator components, expert trajectory | world/planner/reward parameters | TRAIN→DEPLOY | joint online evaluator learning | WOTE-P; WOTE-S [PAPER+CODE FACT] | DFD LC-only | WoTE retains its world rollout; DFD drops it | HIGH | □ ACCEPT □ REVISE □ UNKNOWN |

## 8. Required pairwise review

### 8.1 LAW ↔ Epona

| Check | LAW-PF | EPO-PLAN | Human question |
|---|---|---|---|
| Runtime | D∅,P∅,V=N/A | D∅,P∅,V=N/A | Are their planning deployment routes equivalent after ignoring Ts? |
| Carrier lifecycle | C2@T | C2@T | Are both correctly excluded from runtime carrier claims? |
| Control edge | X2 predicted action | X1 factual action | Does this justify LA vs LS? |
| Learning | action-mediated, target detached | sibling multitask on shared MST | Can the reviewer reconstruct the distinct gradient paths? |
| Decision | — | — | □ ACCEPT SPLIT □ MERGE □ NEED EVIDENCE |

### 8.2 LAW/Epona ↔ DriveLaW

| Check | LAW/EPO planning | DriveLaW | Human question |
|---|---|---|---|
| Runtime carrier | none | C4@R | Is early Video-DiT state sufficiently grounded to pass C gate? |
| Runtime route | D∅ | D1 | Does the carrier actually condition A*? |
| Candidate topology | P∅ | P∅ | Is absence of resolver consistent across all three? |
| Learning | LA or LS | LG retained trunk | Does DriveLaW require a separate retained-generative learning family? |
| Decision | — | — | □ ACCEPT SPLIT □ MERGE □ NEED EVIDENCE |

### 8.3 World4Drive ↔ WorldDrive ↔ WoTE

| Check | World4Drive | WorldDrive | WoTE | Human question |
|---|---|---|---|---|
| Shared route | D2/PB/X3 | D2/PB/X3 | D2/PB/X3 | Is this a genuine common candidate-consequence route? |
| Carrier | current+C2 direct | C2 teacher/surrogate | current+C3 horizon | Are direct/surrogate/horizon distinctions sufficient? |
| Resolver | VW | VU | VM+VD | Do target provenance and composition preserve the key difference? |
| Clock | no horizon | no online solver/horizon | Th | Is recurrent future time separated from model depth? |
| Learning | retained joint; gradient partial | LP→joint(LT,LC), teacher generator dropped | retained joint world/reward | Can each deployment be reconstructed? |
| Decision | — | — | — | □ ACCEPT THREE-WAY SPLIT □ REVISE □ NEED EVIDENCE |

## 9. Human sign-off

| Review item | Result |
|---|---|
| All ten paper/version/mode artifacts reviewed | □ YES □ NO |
| Every ∅ is supported by positive absence evidence | □ YES □ NO |
| UNKNOWN was not silently converted to ∅ | □ YES □ NO |
| N/A follows task/mode type constraints | □ YES □ NO |
| Carrier gate rejects ordinary perception state | □ YES □ NO |
| Candidate identity reaches a common resolver wherever PB is used | □ YES □ NO |
| Learning programs preserve order, gradients, freeze/detach and retain/drop | □ YES □ NO |
| Phase 3 rating S1+ is acceptable | □ YES □ NO □ HOLD AT S1 |

Reviewer:

Date:

Blocking revisions:
