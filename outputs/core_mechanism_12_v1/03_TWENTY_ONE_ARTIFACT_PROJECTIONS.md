# Core Mechanism 12 — Phase 3 Twenty-One Artifact Projections

Status: complete first-pass projection of all 21 frozen artifacts. Projection was performed before reading the old V1 drafts.

## 1. Projection rules used after first-pass attacks

The Phase 2 C–X–D–P–V–T–L structure is retained provisionally, with five mechanical corrections discovered during projection:

1. C1 requires a stateful world operation or explicit temporal/relational world grounding; ordinary BEV/perception features do not qualify merely from detection/map supervision.
2. X is lifecycle-qualified: X={@T:value, @R:value}. A category is exclusive per carrier edge and lifecycle, not necessarily per whole artifact.
3. P is widened to action formation and commitment: direct/implicit, semantic hierarchy, or explicit candidate commitment. The old P2/P3/P4 variants are projected as PB plus ordered audit attributes such as prefilter, postselect_refine, and rescore.
4. V uses semantic target atoms plus provenance, measure, and composition. Geometric error and previous-cycle reference are attributes, not standalone semantic atoms.
5. T records clock topology as present/absent/UNKNOWN. Exact solver steps, horizon length, and refinement rounds are audit parameters.

These changes are justified in 04_COLLISION_AND_COUNTEREXAMPLE_AUDIT.md and formally judged in 05_ONTOLOGY_REVISION_VERDICT.md.

Notation:

    C1 current structured world
    C2 future endpoint consequence
    C3 future horizon consequence
    C4 future generative-process state
    C5 joint world–action sequence

    X∅ no control conditions an applicable consequence carrier
    X1 factual/external control
    X2 predicted single control
    X3 candidate-preserving control
    X4 joint/interleaved control

    D∅ no runtime carrier influence on A*
    D1 carrier-conditioned action
    D2 candidate consequence selection
    D3 reciprocal within-decision refinement
    D4 joint world–action generation
    D5 consequence-generation output

    P∅ direct/implicit action formation; no semantic intermediate or bank
    PH semantic decision/intent→action hierarchy
    PB explicit identity-preserving bank→resolver
    PU commitment topology unknown
    N/A no action-commitment task in this generation mode

Revised V atoms:

    VM expert/factual behavior compatibility
    VU holistic task utility/preference
    VD decomposed driving outcomes
    VW world/future fidelity
    VY dynamics or physical validity
    VP model confidence/likelihood
    VX unknown criterion

T core:

    T=(Ts solver/edit, Tr reciprocal refinement, Th physical-horizon model rollout, Tc cross-cycle dependency)

L macros remain family abbreviations only:

    LP predictive representation transfer
    LS shared-state sibling multitask
    LA action-mediated future supervision
    LG generative-carrier pretraining and retained-trunk adaptation
    LN factual next-state/temporal consistency with stopped target
    LT teacher-to-surrogate distillation
    LC criterion-to-proposal/resolver supervision
    LQ shared world–action sequence learning
    LR reward-based policy optimization

The full ordered L program, not the macro list, is authoritative.

## 2. Compact projection matrix

| Artifact | C | X | D | P | V | T core | L family | Confidence |
|---|---|---|---|---|---|---|---|---|
| LAW-PF | C2@T | @T:X2; @R:N/A | D∅ | P∅ | N/A | ∅,∅,∅,∅ | LA | HIGH |
| LAW-PB | C2@T | @T:X2; @R:N/A | D∅ | P∅ | N/A | ∅,∅,∅,∅ | LA + perception stages | MEDIUM |
| EPO-PLAN | C2@T | @T:X1; @R:N/A | D∅ | P∅ | N/A | present,∅,∅,∅ | LS | HIGH |
| EPO-SELF | C2@T + C3@R | @T:X1; @R:X2 | D5 | N/A | N/A | present,∅,present,∅ | LS + detached chain-forward | HIGH |
| EPO-CTRL | C2@T + C3@R | @T:X1; @R:X1 | D5 | N/A | N/A | present,∅,present,∅ | LS | HIGH |
| DLAW-PAPER | C4@B | @R:X∅ | D1 | P∅ | N/A | present,∅,∅,∅ | LG | HIGH |
| DLAW-CODE | C4@B | @R:X∅ | D1 | P∅ | N/A | present,∅,∅,∅ | LG | HIGH |
| W4D-PLAN | C1@B + C2@B | @T:X3; @R:X3 | D2 | PB | VM | ∅,∅,∅,∅ | joint graph; LA route partly UNKNOWN | MEDIUM-HIGH |
| WD-PLAN | C2@T direct + C2@R surrogate | @T:X3; @R:X3 | D2 | PB[prefilter] | VU | ∅,∅,∅,∅ | LT→LC | HIGH |
| WOTE-PLAN | C1@B + C3@B | @T:X3; @R:X3 | D2 | PB | fusion(VM,VD) | ∅,∅,present,∅ | retained joint graph + LC | HIGH |
| SEER-PAPER | C1@B + C2@B | @T:X3; @R:X3 | D3 | PU | VX | ∅,present,∅,∅ | retained joint graph/LA | MEDIUM |
| SEER-CODE | C1@B + C2@B | @T:X3; @R:X3 | D2 | PB[postselect_refine,no_rescore] | fusion(VM,VD) | ∅,∅,∅,∅ | retained joint graph + LC | HIGH |
| DJEPA-PF | C2@T | @T:X∅; @R:N/A | D∅ | P∅ | N/A | ∅,∅,∅,∅ | LP | HIGH |
| DJEPA-PB1 | C2@T | @T:X∅; @R:N/A | D∅ | PB | VU | ∅,∅,∅,∅ | LP→LC | HIGH |
| DJEPA-PB2 | C2@T | @T:X∅; @R:N/A | D∅ | PB | weighted(VU,VD-comfort@previous-cycle) | ∅,∅,∅,present | LP→LC | HIGH |
| METIS-PLAN | C2@T | @T:X2; @R:N/A | D∅ | P∅ | N/A | present,∅,∅,∅ | LA | MEDIUM |
| DFD-PLAN | C2@T | @T:X3; @R:N/A | D∅ | PB | compose(VW,VM,VY) | ∅,∅,∅,∅ | LC; gradient scope UNKNOWN | MEDIUM |
| DWAM-POLICY | C5@T | @T:X4; @R:N/A | D∅ | PH | N/A | present,∅,∅,∅ | LQ→finetune→LR | MEDIUM |
| DWAM-WORLD | C3@R | @R:X1 | D5 | N/A | N/A | present,∅,present,∅ | world/LQ pretraining | MEDIUM |
| DWAM-JOINT | C5@B | @T:X4; @R:X4 | D4 | P∅ | N/A | present,∅,present,∅ | LQ | MEDIUM |
| GW-PLAN | C1@B + C2@T | @T:X∅; @R:N/A | D1 | PU | VX | present,∅,∅,∅ | LS + stopped temporal consistency | MEDIUM |

Here @T means TRAIN_ONLY or training lifecycle, @R means runtime, and @B means both. Exact paper/source boundaries follow.

## 3. Detailed projections

### 3.1 LAW-PF

- Artifact: LAW-PF; raw paper copy, exact PDF revision UNKNOWN; BraveGroup/LAW source at b2f6a…; perception-free planning.
- Evidence boundary: paper plus inspected perception-free source. The perception-based path is not borrowed into this record.
- C: C2@T{direct}. The predicted/factual next latent is a training-only future endpoint; deployed A* does not consume it. [PAPER FACT: papers/raw_md/P0048_LAW/P0048_LAW.raw.md, method/loss; CODE FACT: audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md]
- X: {@T:X2, @R:N/A}. Predicted waypoint conditions future-latent prediction during training; no runtime future carrier exists. [PAPER FACT + CODE FACT, same sources]
- D: D∅. Runtime is current latent→waypoint→A*. [PAPER FACT + CODE FACT]
- P: P∅. No identity-preserving proposal bank reaches a common resolver. [PAPER FACT + CODE FACT]
- V: N/A because P=P∅. [OUR INFERENCE from verified topology]
- T: Ts=absent, Tr=absent, Th=absent, Tc=absent. Appendix autoregressive future training is not the canonical deployment clock. [PAPER FACT]
- L: joint_train(A_pred→F_pred→L_latent→θshared,θwaypoint; stopgrad(F_target) || L_plan→θwaypoint) => retain{encoder,waypoint decoder}/drop{future predictor,target branch}. Family=LA. [CODE FACT]
- Confidence: HIGH for the inspected source path; paper revision boundary remains UNKNOWN.

### 3.2 LAW-PB

- Artifact: LAW-PB; raw paper copy, exact PDF revision UNKNOWN; perception-based paper mode.
- Evidence boundary: paper-level mechanism; no independently verified perception-based implementation.
- C: C2@T{direct}. Future latent is supervised in training and absent from deployed waypoint path. [PAPER FACT: papers/raw_md/P0048_LAW/P0048_LAW.raw.md]
- X: {@T:X2, @R:N/A}. Predicted waypoint conditions future prediction. [PAPER FACT]
- D: D∅. [PAPER FACT]
- P: P∅. No semantic hierarchy or explicit candidate resolver is present. [PAPER FACT]
- V: N/A because P=P∅. [OUR INFERENCE]
- T: all four runtime clocks absent. [PAPER FACT]
- L: perception_pretrain/perception_train; joint_train(A_pred→F_pred→L_future plus L_plan plus perception losses) => retain{perception encoder,waypoint path}/drop{future branch}. Exact target detach and gradient scope=UNKNOWN. Family=LA with LU edges. [PAPER FACT; UNKNOWN per U-002]
- Confidence: MEDIUM.

### 3.3 EPO-PLAN

- Artifact: EPO-PLAN; ICCV 2025 paper copy, exact arXiv revision UNKNOWN; Kevin-thu/Epona at 69b24c…; planning-only evaluation.
- Evidence boundary: source step_eval with traj_only behavior is included.
- C: C2@T{direct}. Future visual latent is learned but visual DiT is skipped in planning-only deployment. [PAPER FACT: papers/raw_md/P0001_Epona/P0001_Epona.raw.md; CODE FACT: audits/literature/PHASE_C5_EPONA_SOURCE_AUDIT.md]
- X: {@T:X1, @R:N/A}. Standard visual training uses factual future pose/yaw, not TrajDiT output. [PAPER FACT + CODE FACT]
- D: D∅. Runtime history/MST→TrajDiT→trajectory. [PAPER FACT + CODE FACT]
- P: P∅. Action-flow samples are not a verified bank/resolver or semantic hierarchy. [CODE FACT + OUR INFERENCE]
- V: N/A because P=P∅. [OUR INFERENCE]
- T: Ts=present for action-flow solving; Tr/Th/Tc=absent. Solver count is an audit parameter. [PAPER FACT + CODE FACT]
- L: joint_train(L_action→θTraj,θMST || factual_motion→visual DiT→L_visual→θVis,θMST) => retain{encoders,MST,TrajDiT}/bypass{VisDiT}. Family=LS. [PAPER FACT + CODE FACT]
- Confidence: HIGH.

### 3.4 EPO-SELF

- Artifact: EPO-SELF; same paper/source boundary; self-generated visual rollout.
- C: C2@T{direct} + C3@R{direct}. One-step visual learning supports a recurrent ordered rollout at runtime. [PAPER FACT + CODE FACT, Epona sources]
- X: {@T:X1, @R:X2}. Training uses factual motion; runtime TrajDiT-predicted first-step motion controls the next visual state. [PAPER FACT + CODE FACT]
- D: D5. Generated future visual sequence is the declared mode output/context; this is not the planning-only A*. [PAPER FACT + CODE FACT]
- P: N/A because this generation mode has no action-commitment task.
- V: N/A because P=N/A.
- T: Ts=present inside action/visual solvers; Tr=absent; Th=present for outer modelled physical-horizon rollout; Tc=absent. [PAPER FACT + CODE FACT]
- L: EPO-PLAN LS program plus periodic chain-forward with detached self-generated context. retain{MST,TrajDiT,VisDiT}. [CODE FACT]
- Confidence: HIGH.

### 3.5 EPO-CTRL

- Artifact: EPO-CTRL; same paper/source boundary; externally controlled visual rollout.
- C: C2@T + C3@R. [PAPER FACT + CODE FACT, Epona sources]
- X: {@T:X1, @R:X1}. Factual poses supervise training and externally supplied pose/yaw controls deployment rollout. [PAPER FACT + CODE FACT]
- D: D5; A*=N/A because control is supplied. [PAPER FACT + CODE FACT]
- P: N/A because external control replaces action commitment.
- V: N/A because P=N/A.
- T: Ts=present, Tr=absent, Th=present, Tc=absent. [PAPER FACT + CODE FACT]
- L: shared Epona LS program; deploy/retain visual generation path, TrajDiT not required for this mode. [CODE FACT]
- Confidence: HIGH.

### 3.6 DLAW-PAPER

- Artifact: DLAW-PAPER; arXiv:2512.23421v3/CVPR 2026; paper planning path.
- C: C4@B{internal}. Cached first-denoising Video-DiT block states are grounded by video generation and consumed by Action DiT. [PAPER FACT: papers/raw_md/P0009_DriveLaW/P0009_DriveLaW.raw.md, Fig. 1 and action-planning section]
- X: {@R:X∅}. The generative carrier is observation/noise conditioned; action consumes it rather than conditioning it. [PAPER FACT]
- D: D1. C4→Action DiT→A*. [PAPER FACT]
- P: P∅. Action DiT forms the trajectory without semantic hierarchy or explicit resolver. [PAPER FACT]
- V: N/A because P=P∅. [OUR INFERENCE]
- T: Ts=present; Tr/Th/Tc=absent. Five paper-specified action steps are an audit parameter, not a core value. [PAPER FACT]
- L: pretrain(video generation→θVideo); finetune(L_action→θAction,θVideo) => retain{early Video-DiT carrier,Action DiT}/drop_or_skip{full video denoising,video decode in planning}. Family=LG. [PAPER FACT]
- Confidence: HIGH.

### 3.7 DLAW-CODE

- Artifact: DLAW-CODE; official source at 243e0e…; released planning path.
- C: C4@B{internal}. Released planning consumes early Video-DiT block states. [CODE FACT: audits/literature/PHASE_C6_DRIVELAW_AUDIT.md]
- X: {@R:X∅}. No candidate/action control conditions the carrier. [CODE FACT]
- D: D1. C4 conditions the released Action DiT path. [CODE FACT]
- P: P∅. Solver states do not form an identity-preserving bank/resolver. [CODE FACT + OUR INFERENCE]
- V: N/A because P=P∅. [OUR INFERENCE]
- T: Ts=present; exact released step count is version/config ambiguous between five and ten. [CODE FACT + UNKNOWN]
- L: action_full permits action loss to update both Action DiT and Video-DiT; full video output remains unnecessary for planning. Family=LG. [CODE FACT]
- Evidence boundary: paper/source flow-sign and solver-count differences are retained as audit discrepancies, not ontology categories.
- Confidence: HIGH for source topology; MEDIUM for exact numeric solver setting.

### 3.8 W4D-PLAN

- Artifact: W4D-PLAN; ICCV 2025/arXiv:2507.00603; official source at cffb51….
- C: C1@B{direct} + C2@B{direct}. The physical current latent participates in an explicit candidate-conditioned world transition; F{k} is a separate future endpoint record. [PAPER FACT: papers/raw_md/P0046_World4Drive/P0046_World4Drive.raw.md; CODE FACT: audits/literature/PHASE_C5_WORLD4DRIVE_AUDIT.md]
- X: {@T:X3, @R:X3}. Candidate identity k conditions F{k} and survives to scoring. [PAPER FACT + CODE FACT]
- D: D2. A{k}→F{k}→V{k}→argmax→A*. [PAPER FACT + CODE FACT]
- P: PB. Six intention/candidate identities reach one resolver. [PAPER FACT + CODE FACT]
- V: single(VM){referent=factual/expert trajectory; label_measure=nearest geometric trajectory; provenance=winner index j}. Future reconstruction shapes F but does not by itself change the resolver target to VW. [PAPER FACT]
- T: all core clocks absent. Candidate parallelism is not a clock. [OUR INFERENCE]
- L: joint_train(factual future→L_future on selected F{j} || nearest expert candidate→L_score || trajectory/perception losses). A{k}→F{k} is known; whether L_future reaches θA in every config is UNKNOWN. retain{current/future world path,planner,scorer}. Family=LA/LU + LC. [PAPER FACT; CODE boundary U-009]
- Confidence: MEDIUM-HIGH.

### 3.9 WD-PLAN

- Artifact: WD-PLAN; arXiv:2603.14948; official source at c375ee….
- C: C2@T{direct teacher} + C2@R{distilled surrogate}. Distillation changes realization, not the temporal carrier category. [PAPER FACT: papers/raw_md/P0042_WorldDrive/P0042_WorldDrive.raw.md; CODE FACT: audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md]
- X: {@T:X3, @R:X3}. Candidate trajectory indexes teacher future and deployed surrogate. [PAPER FACT + CODE FACT]
- D: D2. A{k}→surrogate F{k}→reward V{k}→argmax. [PAPER FACT + CODE FACT]
- P: PB with audit attribute prefilter=top-K. Removing the filter changes compute/search support but not criterion semantics or commitment operator. [PAPER FACT + OUR INFERENCE]
- V: pairwise_preference(VU){referent=planning outcome; provenance=PDMS/oracle ordering}. [PAPER FACT]
- T: all core clocks absent. Heavy diffusion solver is not in deployed planning. [PAPER FACT + CODE FACT]
- L: pretrain(TA-DWM future teacher); distill(LT: stopgrad F_teacher{k}→F_surrogate{k}); train(LC: PDMS preferences→reward head); deploy retain{proposal path,surrogate,reward}/drop{heavy TA-DWM}. Order=LT→LC, not an unordered set. [PAPER FACT + CODE FACT]
- Confidence: HIGH.

### 3.10 WOTE-PLAN

- Artifact: WOTE-PLAN; raw paper revision UNKNOWN; official source at 298957….
- C: C1@B{direct} + C3@B{direct}. Current semantic BEV is the source of recurrent candidate-conditioned future BEV/action states. [PAPER FACT: papers/raw_md/P0045_WoTE/P0045_WoTE.raw.md; CODE FACT: audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md]
- X: {@T:X3, @R:X3}. Candidate ego state/trajectory indexes each rollout. [PAPER FACT + CODE FACT]
- D: D2. Multi-step F{k,h} supplies candidate reward before argmax. [PAPER FACT + CODE FACT]
- P: PB. [PAPER FACT + CODE FACT]
- V: learned_fusion(VM,VD[safety,comfort,progress/rule-related components]){provenance=expert imitation plus simulator labels; surroundings=fixed/logged in inspected setup}. Exact paper sign wording remains bounded. [PAPER FACT + CODE FACT]
- T: Ts=absent, Tr=absent, Th=present, Tc=absent. Horizon length H is an audit parameter. [PAPER FACT + CODE FACT]
- L: joint_train(BEV rollout/map loss || simulator component reward losses || imitation || trajectory WTA) => retain{world rollout,planner,reward,resolver}. Gradient details beyond inspected source remain bounded. [PAPER FACT + CODE FACT]
- Confidence: HIGH for topology; MEDIUM-HIGH for exact reward formula.

### 3.11 SEER-PAPER

- Artifact: SEER-PAPER; NeurIPS 2025/arXiv link 2510.11092; paper iterative mechanism.
- C: C1@B + C2@B. [PAPER FACT: papers/raw_md/P0061_SeerDrive/P0061_SeerDrive.raw.md]
- X: {@T:X3, @R:X3}. Mode/candidate action and future BEV identity are aligned during feedback and WTA supervision. [PAPER FACT]
- D: D3. A{m,r}→F{m,r}→A{m,r+1}, repeated within one decision. [PAPER FACT]
- P: PU. Multimode outputs exist, but the exact deployed final resolver is not fixed by available evidence. [UNKNOWN U-015]
- V: VX because P is unresolved; do not import released-code rewards into the paper artifact. [UNKNOWN]
- T: Ts=absent, Tr=present, Th=absent, Tc=absent. Future endpoint prediction per round is not a physical-horizon rollout. [PAPER FACT + OUR INFERENCE]
- L: joint_train(current/future semantic losses || trajectory losses at iterative heads; WTA-aligned mode) with end-to-end gradients through rounds => retain{world/planner reciprocal path}. Family=LA plus retained joint graph. [PAPER FACT]
- Confidence: MEDIUM due final resolver.

### 3.12 SEER-CODE

- Artifact: SEER-CODE; initial official release at 1cfb7ec…; WoTE-integrated evaluator/refiner.
- C: C1@B + C2@B. [CODE FACT: audits/literature/PHASE_C5_SEERDRIVE_AUDIT.md]
- X: {@T:X3, @R:X3}. [CODE FACT]
- D: D2. A{k}→one-endpoint F{k}→decomposed V{k}→argmax; selected F{k*} then refines A{k*}. [CODE FACT]
- P: PB{postselect_refine=yes,rescore=no}. The fixed selected index is not reconsidered. [CODE FACT]
- V: learned_fusion(VM,VD){provenance=imitation and simulator reward labels}. [CODE FACT]
- T: all core clocks absent. num_fut_timestep=1 and one post-selection refinement do not create Th or Tr. [CODE FACT + OUR INFERENCE]
- L: joint_train(map/future-map losses || imitation/simulator reward losses || initial/refined offset losses) => retain{candidate future evaluator,reward,resolver,selected refinement}. [CODE FACT]
- Confidence: HIGH.

### 3.13 DJEPA-PF

- Artifact: DJEPA-PF; arXiv:2601.22032; official source at e21f474…; perception-free path.
- C: C2@T{direct predictive representation}. V-JEPA predicts future latent/target representations during pretraining; no carrier survives downstream as a future predictor. [PAPER FACT: papers/raw_md/P0049_DriveJEPA/P0049_DriveJEPA.raw.md, V-JEPA section; CODE FACT: audits/literature/PHASE_C5_DRIVEJEPA_AUDIT.md]
- X: {@T:X∅, @R:N/A}. Predictive target is observation/video conditioned, not action conditioned. [PAPER FACT]
- D: D∅. [PAPER FACT + CODE FACT]
- P: P∅. Downstream transformer directly forms the trajectory. [CODE FACT]
- V: N/A because P=P∅. [OUR INFERENCE]
- T: all runtime core clocks absent. [CODE FACT]
- L: pretrain(LP: online encoder+predictor→future target representation; stopgrad EMA target); downstream train planner with encoder frozen/no-grad by default; deploy retain{encoder,planner}/drop{predictor,target encoder}. [PAPER FACT + CODE FACT]
- Confidence: HIGH.

### 3.14 DJEPA-PB1

- Artifact: DJEPA-PB1; same paper/source; perception-based v1.
- C: C2@T{direct predictive representation}. [PAPER FACT + CODE FACT, Drive-JEPA sources]
- X: {@T:X∅,@R:N/A}. [PAPER FACT + CODE FACT]
- D: D∅ because predictor/target branches are absent downstream. [PAPER FACT + CODE FACT]
- P: PB. Proposal identities survive iterative proposal refinement to a common learned scorer and argmax. Refinement is not rollout. [CODE FACT]
- V: single(VU){referent=simulated planning outcome; provenance=EPDMS labels; measure=learned scalar}. [PAPER FACT + CODE FACT]
- T: all core clocks absent. Proposal decoder depth/refinement is an audit attribute, not Ts. [CODE FACT + OUR INFERENCE]
- L: pretrain(LP); distill(multimodal safe pseudo trajectories→proposal loss); train(LC: simulator EPDMS→score head plus auxiliary losses); deploy retain{encoder,proposal refiner,scorer}/drop{JEPA predictor,target encoder}. [PAPER FACT + CODE FACT]
- Confidence: HIGH.

### 3.15 DJEPA-PB2

- Artifact: DJEPA-PB2; same paper/source; perception-based v2 with momentum-aware selection.
- C: C2@T{direct predictive representation}. [PAPER FACT + CODE FACT]
- X: {@T:X∅,@R:N/A}. [PAPER FACT + CODE FACT]
- D: D∅. [PAPER FACT + CODE FACT]
- P: PB with the same proposal-bank/argmax topology as PB1. [CODE FACT]
- V: weighted_sum(VU:14, VD[comfort]:2)/16{utility provenance=EPDMS; comfort temporal_reference=previous executed/simulated/planned trajectory UNKNOWN by harness}. Previous-cycle reference is not a separate semantic atom. [CODE FACT; provenance boundary U-019]
- T: Ts/Tr/Th=absent; Tc=present. One previous-cycle dependency suffices; exact buffer implementation is an audit detail. [CODE FACT]
- L: LP→multimodal proposal distillation→LC, with v2 runtime recalibration retained; JEPA predictor/target dropped. [PAPER FACT + CODE FACT]
- Confidence: HIGH for formula/topology; MEDIUM-HIGH for previous-trajectory provenance.

### 3.16 METIS-PLAN

- Artifact: METIS-PLAN; arXiv:2606.15869v1; executable source unavailable.
- C: C2@T{direct video consequence}. Visual expert predicts future-video flow during training and is bypassed in action-only deployment. [PAPER FACT: papers/raw_md/P0062_Metis/P0062_Metis.raw.md]
- X: {@T:X2,@R:N/A}. Predicted action tokens condition the visual branch through asymmetric attention. [PAPER FACT]
- D: D∅. [PAPER FACT]
- P: P∅. Action expert forms action without semantic hierarchy or explicit bank. [PAPER FACT]
- V: N/A because P=P∅. [OUR INFERENCE]
- T: Ts=present for deployed action-flow solving; Tr/Th/Tc=absent. [PAPER FACT]
- L: joint_train(L_action→θAction || A_pred→visual expert→L_video→θVisual,θAction,θshared; visual→action attention blocked) => retain{shared/action expert}/bypass_or_drop{visual expert}. Family=LA. Exact implementation detach/freeze=UNKNOWN. [PAPER FACT; U-020]
- Confidence: MEDIUM.

### 3.17 DFD-PLAN

- Artifact: DFD-PLAN; arXiv:2603.19675v2; executable source unavailable.
- C: C2@T{direct}. Candidate-conditioned next latent/flow path is training-only. [PAPER FACT: papers/raw_md/P0063_DynFlowDrive/P0063_DynFlowDrive.raw.md]
- X: {@T:X3,@R:N/A}. [PAPER FACT]
- D: D∅. Runtime uses learned candidate scores after world-flow removal. [PAPER FACT]
- P: PB. [PAPER FACT]
- V: weighted_or_stated_composition(VW future reconstruction, VM expert compatibility{measure=trajectory geometry}, VY dynamics stability{measure=angular flow stability}){provenance=hybrid winner n*}. Exact weights/sign=UNKNOWN. [PAPER FACT + UNKNOWN U-022]
- T: all runtime core clocks absent; training flow coordinate is not runtime Ts or Th. [PAPER FACT + OUR INFERENCE]
- L: joint_train(candidate world-flow objectives); train(LC: hybrid criterion→winner n*→runtime score head); deploy retain{proposal,score,resolver}/drop{world-flow model}. Exact gradient scope=UNKNOWN. [PAPER FACT; U-023]
- Confidence: MEDIUM.

### 3.18 DWAM-POLICY

- Artifact: DWAM-POLICY; arXiv:2606.05645v2; paper-only primary policy mode.
- C: C5@T{direct}. Joint world–action tokens are learned in pretraining, while policy-only deployment emits no future visual carrier. [PAPER FACT: papers/raw_md/P0064_Discrete-WAM/P0064_Discrete-WAM.raw.md]
- X: {@T:X4,@R:N/A}. [PAPER FACT]
- D: D∅. Context→decision token→action-token editing→A*. [PAPER FACT]
- P: PH. One selected path×speed decision token has independent semantics and conditions action-token editing; the 400 labels are a vocabulary, not 400 runtime trajectory candidates. [PAPER FACT]
- V: N/A.
- T: Ts=present for iterative token editing; Tr/Th/Tc=absent. Edit-round count is an audit parameter. [PAPER FACT]
- L: pretrain(world tokens); joint_pretrain(LQ world–action sequence); finetune(action LoRA); policy_optimize(LR: EPDMS→GRPO advantages) => retain{policy token path}/bypass{visual generation in policy-only mode}. [PAPER FACT]
- Confidence: MEDIUM because source/evaluation command is unavailable.

### 3.19 DWAM-WORLD

- Artifact: DWAM-WORLD; same paper boundary; supplied-action world-generation mode.
- C: C3@R{direct}. Ordered future visual tokens form the terminal world rollout/output. [PAPER FACT, Discrete-WAM raw paper]
- X: {@R:X1}. Supplied action sequence controls generation. [PAPER FACT]
- D: D5; A*=N/A. [PAPER FACT]
- P: N/A because supplied action defines the generation mode.
- V: N/A because P=N/A.
- T: Ts=present for token editing; Tr=absent; Th=present for ordered future visual horizon; Tc=absent. [PAPER FACT]
- L: world/joint pretraining retains visual token generation; exact deployed editing/cache schedule=UNKNOWN. [PAPER FACT; U-026]
- Confidence: MEDIUM.

### 3.20 DWAM-JOINT

- Artifact: DWAM-JOINT; same paper boundary; joint world-policy generation mode.
- C: C5@B{direct}. [PAPER FACT, Discrete-WAM raw paper]
- X: {@T:X4,@R:X4}. World and action tokens are interleaved/edited jointly. [PAPER FACT]
- D: D4. Coupled process emits A and F sequences. [PAPER FACT]
- P: P∅. Token alternatives/edits do not form a verified bank→resolver. [PAPER FACT + OUR INFERENCE]
- V: N/A.
- T: Ts=present; Tr=absent; Th=present for generated sequence; Tc=absent. [PAPER FACT]
- L: joint_pretrain(LQ: shared world–action sequence with cross-conditioning) => retain{joint token model}. Whether headline planning metrics deploy this mode is UNKNOWN. [PAPER FACT; U-024]
- Confidence: MEDIUM.

### 3.21 GW-PLAN

- Artifact: GW-PLAN; arXiv:2606.16274v1; paper-only planning path.
- C: C1@B{direct} + C2@T{direct target}. C1 is admitted because ECIG/GRU produces entity-relational world nodes, a world-flow operator refines them, explicit temporal consistency grounds them, and planning consumes them. The stopped t+1 world target is training-only. [PAPER FACT: papers/raw_md/P0065_GraphWorld/P0065_GraphWorld.raw.md]
- X: {@T:X∅,@R:N/A}. The temporal target is factual/observation-derived rather than action-controlled; runtime has no future/joint carrier. [PAPER FACT]
- D: D1. Current structured world→mode reweighting/planning queries→trajectory. [PAPER FACT]
- P: PU. Multimodal planning outputs exist, but final ego-mode commitment is not established. [UNKNOWN U-027]
- V: VX because the exact resolver target is unknown. [UNKNOWN]
- T: Ts=present for two-step internal flow transport; Tr/Th/Tc=absent. Two is an audit parameter, not a physical horizon. [PAPER FACT]
- L: stage1 joint_train(detection/map/motion/planning→θshared,θworld); stage2 LN temporal_consistency(W_t,stopgrad(W_t+1)) plus task losses; deploy retain{ECIG,GRU,current-world flow,planner}/drop{physical t+1 target branch}. Family=LS+LN. [PAPER FACT]
- Confidence: MEDIUM due source absence and resolver.

## 4. Evidence-boundary summary

| Boundary | Affected projections | Treatment |
|---|---|---|
| exact raw-paper revision unknown | LAW, Epona, WoTE | version remains UNKNOWN; mechanism claim limited to tracked raw copy |
| paper/code runtime mismatch | SeerDrive | SEER-PAPER and SEER-CODE remain separate |
| paper/code numeric/formula mismatch | DriveLaW | core signatures may collide; numeric/sign details remain audit attributes and unresolved |
| source unavailable | Metis, DynFlowDrive, Discrete-WAM, GraphWorld | paper facts only; detach/resolver/evaluation details use UNKNOWN |
| final resolver unknown | SEER-PAPER, GW-PLAN | P=PU and V=VX; no invented ∅ |
| target detach/gradient incomplete | LAW-PB, W4D, WD variants, Metis, DFD | L retains UNKNOWN edges rather than copying another mode |

## 5. Completeness status of projection

- 21/21 artifacts projected.
- Every field distinguishes ∅, UNKNOWN, and N/A under revised type rules.
- Every artifact has an ordered L program and explicit retain/drop or bypass statement.
- No training-only future carrier is used to justify D1–D4.
- No random sample, solver iteration, token edit, or proposal-refinement layer is treated as PB without a common resolver.
- Exact evidence gaps remain visible rather than normalized.

Projection completeness does not imply ontology stability; collision and counterexample results are in the companion audit.
