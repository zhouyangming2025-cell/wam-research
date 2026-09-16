# Core Mechanism 12 — Phase 1 Blind Mechanism Reconstruction

Status: Phase 1 draft complete. No ontology labels are assigned in this document.

## 1. Reading convention

Each mechanism is serialized as a directed edge list. This is a lossless DAG representation for this audit because every edge carries lifecycle and evidence attributes.

Edge form:

    source -- relation --> destination [LIFECYCLE; EVIDENCE]

Special forms:

- x{1…K}: candidate-indexed objects with preserved identity;
- τ: physical/environment time;
- s: diffusion or flow solver coordinate;
- r: within-decision refinement iteration;
- stopgrad(x): no gradient through x;
- EMA(x): exponential-moving-average parameter update.

Unless explicitly stated, a repeated solver step is not a physical rollout step, and a within-decision loop is not closed-loop interaction with the environment.

## 2. P0048 — LAW

### 2.1 LAW-PF: perception-free planning

Deployment DAG:

    O(history images) -- visual encoding --> S(current latent) [RUNTIME; PAPER FACT + CODE FACT]
    S(current latent) -- waypoint decoder --> A(waypoint) [RUNTIME; PAPER FACT + CODE FACT]
    A(waypoint) -- direct output --> A* [RUNTIME; PAPER FACT + CODE FACT]

Training DAG:

    O(t) -- shared encoder --> S(t) [TRAIN; PAPER FACT + CODE FACT]
    S(t) + A(predicted waypoint) -- latent predictor --> F(predicted future latent) [TRAIN; PAPER FACT + CODE FACT]
    O(t+1) -- target encoding --> stopgrad(F(factual future latent)) [TRAIN; CODE FACT]
    F(predicted) + stopgrad(F(factual)) -- reconstruction loss --> L_latent [TRAIN; PAPER FACT + CODE FACT]
    A(predicted) + A(factual waypoint) -- waypoint loss --> L_plan [TRAIN; PAPER FACT + CODE FACT]
    L_latent + L_plan -- gradient --> shared encoder and waypoint path [TRAIN; CODE FACT]

Boundary facts:

- F is not consumed by A* in the inspected runtime path. [CODE FACT]
- V = ∅ and R = ∅ in deployed inference; there is no candidate bank or score-based resolver. [PAPER FACT + CODE FACT]
- The factual future branch is detached, while the predicted branch can shape the shared current encoder and waypoint-producing path. [CODE FACT]
- The appendix autoregressive multi-future-latent experiment is a training variant, not a different canonical deployment path. [PAPER FACT]

### 2.2 LAW-PB: perception-based planning

Deployment DAG:

    O(multiview perception input) -- perception encoder --> S(current scene latent) [RUNTIME; PAPER FACT]
    S(current scene latent) -- waypoint decoder --> A(waypoint) [RUNTIME; PAPER FACT]
    A(waypoint) -- direct output --> A* [RUNTIME; PAPER FACT]

Learning DAG:

    O(t) -- perception supervision --> S(t) [TRAIN; PAPER FACT]
    S(t) + A(predicted waypoint) -- latent predictor --> F(predicted future latent) [TRAIN; PAPER FACT]
    O(t+1) -- future encoding --> F(factual future latent) [TRAIN; PAPER FACT]
    F(predicted) + F(factual) -- latent objective --> L_latent [TRAIN; PAPER FACT]
    A(predicted) + A(factual) -- planning objective --> L_plan [TRAIN; PAPER FACT]
    perception targets -- detection/map objectives --> L_perception [TRAIN; PAPER FACT]

Boundary facts:

- As in LAW-PF, the learned future latent is training-side relative to deployed A*. [PAPER FACT]
- Exact detach topology for the perception-based target branch is UNKNOWN because this implementation path was not independently verified.
- V = ∅ and R = ∅ at runtime. [PAPER FACT]

## 3. P0001 — Epona

### 3.1 EPO-PLAN: planning-only evaluation

Deployment DAG:

    O(RGB history) + O(prior ego motion) -- encoders and MST --> S(shared history carrier) [RUNTIME; PAPER FACT + CODE FACT]
    S + I(route/command) -- TrajDiT action-flow solver over s --> A(trajectory) [RUNTIME; PAPER FACT + CODE FACT]
    A -- output --> A* [RUNTIME; PAPER FACT + CODE FACT]

Boundary facts:

- The visual DiT is skipped by the inspected planning-only evaluation path. [CODE FACT]
- R = ∅ and V = ∅; action-flow iterations refine one action sample rather than score a candidate bank. [CODE FACT]
- Action-flow coordinate s is not physical time τ.

### 3.2 EPO-SELF: self-generated visual rollout

Deployment DAG:

    O(history) -- encoders and MST --> S(τ) [RUNTIME; PAPER FACT + CODE FACT]
    S(τ) -- TrajDiT --> A(predicted first-step ego motion at τ+1) [RUNTIME; PAPER FACT + CODE FACT]
    S(τ) + A(first step) -- visual DiT over s --> F(predicted visual latent at τ+1) [RUNTIME; PAPER FACT + CODE FACT]
    F(τ+1) + A(τ+1) -- append to context --> O(history at τ+1) [RUNTIME; PAPER FACT + CODE FACT]
    O(history at τ+1) -- repeat across outer τ --> F(τ+2…) [RUNTIME; PAPER FACT + CODE FACT]

Boundary facts:

- Inner visual denoising iterations s and outer physical rollout index τ are distinct.
- Only the first predicted trajectory step conditions the next visual state in the inspected implementation. [CODE FACT]
- This is a generation/rollout mode; it is not evidence that generated futures are consumed by the planning-only benchmark path.

### 3.3 EPO-CTRL: externally controlled visual rollout

Deployment DAG:

    O(history) -- encoders and MST --> S(τ) [RUNTIME; PAPER FACT + CODE FACT]
    I(external pose/yaw at τ+1) + S(τ) -- visual DiT over s --> F(predicted visual latent at τ+1) [RUNTIME; PAPER FACT + CODE FACT]
    F(τ+1) -- decoder --> generated frame/video [RUNTIME; PAPER FACT]

Boundary facts:

- A* = N/A for this controlled generation mode.
- TrajDiT is not required to provide the control variable. [CODE FACT]

### 3.4 Shared Epona learning DAG

    O(history) -- shared encoders and MST --> S [TRAIN; PAPER FACT + CODE FACT]
    S + action-flow noise -- TrajDiT --> A(predicted action flow) [TRAIN; PAPER FACT + CODE FACT]
    A(target) -- action-flow target --> L_action [TRAIN; PAPER FACT + CODE FACT]
    S + I(factual future pose/yaw) + visual noise -- visual DiT --> F(predicted visual flow) [TRAIN; PAPER FACT + CODE FACT]
    O(factual future frame) -- visual target encoding --> F(target visual flow) [TRAIN; PAPER FACT + CODE FACT]
    F(predicted) + F(target) -- visual-flow objective --> L_visual [TRAIN; PAPER FACT + CODE FACT]
    L_action + L_visual -- joint gradient --> shared MST representation [TRAIN; PAPER FACT + CODE FACT]
    self-generated rollout context -- periodic chain-of-forward training --> detached next context [TRAIN; CODE FACT]

The standard visual-training edge uses factual motion, not the TrajDiT-predicted action. [PAPER FACT + CODE FACT]

## 4. P0009 — DriveLaW

### 4.1 DLAW-PAPER

Deployment DAG:

    O(video/history) -- Video-DiT first denoising iteration --> F(internal generative hidden states) [RUNTIME; PAPER FACT]
    F(hidden states) + I(command) -- Action DiT flow over s --> A(trajectory) [RUNTIME; PAPER FACT]
    A(after five paper-specified action steps) -- output --> A* [RUNTIME; PAPER FACT]

Boundary facts:

- Full video denoising and pixel/video decoding are not required in planning inference. [PAPER FACT]
- F is an internal future-generative carrier, not a completed future video.
- There is no candidate bank, V = ∅, and R = ∅. [PAPER FACT]

### 4.2 DLAW-CODE

Deployment DAG:

    O(video/history) -- released Video-DiT early block pass --> F(hidden states) [RUNTIME; CODE FACT]
    F(hidden states) + I(command) -- released Action DiT flow over s --> A(trajectory) [RUNTIME; CODE FACT]
    A -- output --> A* [RUNTIME; CODE FACT]

The released agent, validation settings, and paper are not fully aligned on action-flow step count; therefore no single numeric runtime step count is asserted for DLAW-CODE. [CODE FACT + UNKNOWN]

### 4.3 DriveLaW staged learning DAG

    O(long low-resolution clips) -- video pretraining --> Video-DiT [TRAIN; PAPER FACT]
    O(shorter high-resolution clips) -- video refinement --> Video-DiT [TRAIN; PAPER FACT]
    O(history) -- Video-DiT hidden states --> F(generative features) [TRAIN; PAPER FACT + CODE FACT]
    F + action-flow noise -- Action DiT --> A(predicted flow) [TRAIN; PAPER FACT + CODE FACT]
    A(target trajectory) -- flow-matching target --> L_action [TRAIN; PAPER FACT + CODE FACT]
    L_action -- gradient in action_full configuration --> Action DiT and trainable Video-DiT path [TRAIN; CODE FACT]

No simultaneous video-generation loss is established for the final action adaptation stage. [PAPER FACT + CODE FACT]

## 5. P0046 — World4Drive

### 5.1 W4D-PLAN deployment DAG

    O(multiview history) -- scene encoder --> W(current physical-world latent) [RUNTIME; PAPER FACT + CODE FACT]
    I{1…6}(intention queries) + W -- trajectory decoder --> A{1…6}(candidate trajectories) [RUNTIME; PAPER FACT + CODE FACT]
    W + A{k} -- candidate-conditioned world model --> F{k}(predicted future latent) [RUNTIME; PAPER FACT + CODE FACT]
    W + F{k} + A{k} -- ScoreNet --> V{k}(candidate score) [RUNTIME; PAPER FACT + CODE FACT]
    V{1…6} -- argmax --> R(selected index k*) [RUNTIME; PAPER FACT + CODE FACT]
    A{k*} -- select --> A* [RUNTIME; PAPER FACT + CODE FACT]

### 5.2 W4D-PLAN learning DAG

    O(t) -- current encoder --> W(t) [TRAIN; PAPER FACT + CODE FACT]
    O(t+1) -- future encoder --> F(factual future latent) [TRAIN; PAPER FACT + CODE FACT]
    W(t) + A{k} -- candidate-conditioned predictor --> F{k}(predicted future latent) [TRAIN; PAPER FACT + CODE FACT]
    A{1…6} + A(factual) -- nearest-trajectory match --> R_train(index j) [TRAIN; PAPER FACT]
    F{j} + F(factual) -- future reconstruction --> L_future [TRAIN; PAPER FACT]
    V{1…6} + j -- focal classification --> L_score [TRAIN; PAPER FACT]
    A{j} + A(factual) -- selected trajectory imitation --> L_plan [TRAIN; PAPER FACT]
    semantic labels -- scene supervision --> L_sem [TRAIN; PAPER FACT + CODE FACT]
    L_future + L_score + L_plan + L_sem -- joint gradient --> planner/world/scorer [TRAIN; PAPER FACT]

Boundary facts:

- Candidate identity is preserved from intention query through F{k}, V{k}, and the final selection.
- The one factual future target is shared evidence for supervising candidate predictions; it is not six observed counterfactual futures.
- Public-source benchmark coverage beyond the inspected path remains bounded in 07_UNRESOLVED_EVIDENCE.md.

## 6. P0042 — WorldDrive

### 6.1 WD-PLAN deployment DAG

    O(current scene) -- visual encoder --> W(current visual state) [RUNTIME; PAPER FACT + CODE FACT]
    W + I(anchor bank) -- proposal/scoring planner --> A{1…256}(trajectory anchors) [RUNTIME; PAPER FACT + CODE FACT]
    A{1…256} -- top-K filtering --> A{1…K} [RUNTIME; PAPER FACT + CODE FACT]
    W + A{k} -- lightweight future scene-query predictor --> Ftilde{k}(surrogate future embedding) [RUNTIME; PAPER FACT + CODE FACT]
    W + Ftilde{k} + A{k} -- reward head --> V{k} [RUNTIME; PAPER FACT + CODE FACT]
    V{1…K} -- argmax --> R(k*) [RUNTIME; PAPER FACT + CODE FACT]
    A{k*} -- select --> A* [RUNTIME; PAPER FACT + CODE FACT]

Heavy trajectory-aware diffusion and future image generation are absent from the deployed path. [PAPER FACT + CODE FACT]

### 6.2 WD-PLAN learning DAG

Teacher stage:

    O(t) + A(factual or conditioned trajectory) -- trajectory-aware diffusion world model --> F_teacher(future latent) [TRAIN; PAPER FACT]
    O(t+1) -- factual future encoding/noise target --> world diffusion objective [TRAIN; PAPER FACT]
    inherited visual and motion encoders -- frozen --> teacher training boundary [TRAIN; PAPER FACT]

Distillation and ranking stage:

    W + A{k} -- frozen heavy teacher --> F_teacher{k} [TRAIN; PAPER FACT + CODE FACT]
    W + A{k} -- lightweight predictor --> Ftilde{k} [TRAIN; PAPER FACT + CODE FACT]
    Ftilde{k} + stopgrad(F_teacher{k}) -- alignment --> L_align [TRAIN; PAPER FACT]
    A{k} -- simulator/oracle PDMS ordering --> pairwise preference labels [TRAIN; PAPER FACT]
    V{k} + preference labels -- Bradley–Terry ranking --> L_rank [TRAIN; PAPER FACT]
    L_align + L_rank -- gradient --> lightweight future predictor and reward head [TRAIN; PAPER FACT]

Boundary facts:

- Runtime consequence evaluation uses a distilled future surrogate, not the heavy teacher.
- Candidate-specific teacher outputs are generated conditionally; they are not K separately observed futures.

## 7. P0045 — WoTE

### 7.1 WOTE-PLAN deployment DAG

    O(multimodal history) -- encoder --> W(current BEV/world state) [RUNTIME; PAPER FACT + CODE FACT]
    W + I(command) -- trajectory decoder --> A{1…N}(refined candidate trajectories) [RUNTIME; PAPER FACT + CODE FACT]
    W + A{k} -- initialize candidate state-action pair --> S{k,0} [RUNTIME; PAPER FACT + CODE FACT]
    S{k,h} -- recurrent world transition for h=1…H --> F{k,h}(future BEV/action state) [RUNTIME; PAPER FACT + CODE FACT]
    W + F{k,1…H} + A{k} -- decomposed imitation and simulator reward heads --> V{k} [RUNTIME; PAPER FACT + CODE FACT]
    V{1…N} -- highest final reward --> R(k*) [RUNTIME; PAPER FACT + CODE FACT]
    A{k*} -- select --> A* [RUNTIME; PAPER FACT + CODE FACT]

The recurrence index h is modelled horizon within one decision, not repeated interaction with a changing environment.

### 7.2 WOTE-PLAN learning DAG

    O(t) -- current BEV encoder --> W(t) [TRAIN; PAPER FACT + CODE FACT]
    A{k} + W(t) -- recurrent transition --> F{k,1…H} [TRAIN; PAPER FACT + CODE FACT]
    simulator-produced future semantics under candidate ego motion -- target maps --> L_BEV [TRAIN; PAPER FACT + CODE FACT]
    simulator scores for five reward components -- labels --> L_sim_reward [TRAIN; PAPER FACT + CODE FACT]
    A(factual expert) + candidate set -- imitation winner/labels --> L_imitation [TRAIN; PAPER FACT]
    A{k*} + A(factual) -- winner-take-all trajectory loss --> L_plan [TRAIN; PAPER FACT]
    L_BEV + L_sim_reward + L_imitation + L_plan -- joint gradient --> planner/world/reward modules [TRAIN; PAPER FACT]

Boundary facts:

- Candidate ego states vary, but surrounding agents in the inspected supervision setup follow logged/fixed futures; this is not a fully interactive multi-agent counterfactual simulator. [CODE FACT]
- Candidate identity is maintained through recurrent futures and decomposed rewards.

## 8. P0061 — SeerDrive

### 8.1 SEER-PAPER: iterative world–planner co-refinement

Deployment DAG:

    O(multimodal history) -- encoder --> W(current BEV) [RUNTIME; PAPER FACT]
    W + I(command/mode queries) -- initial planner --> A{m,0}(trajectory hypotheses) [RUNTIME; PAPER FACT]
    W + A{m,r} -- world model --> F{m,r}(candidate future BEV) [RUNTIME; PAPER FACT]
    W -- current-scene planner branch --> S_cur{m,r} [RUNTIME; PAPER FACT]
    F{m,r} -- future-scene planner branch --> S_fut{m,r} [RUNTIME; PAPER FACT]
    S_cur + S_fut -- MLN fusion --> A{m,r+1}(refined trajectories/features) [RUNTIME; PAPER FACT]
    A{m,r+1} -- feedback for next r --> world model input [RUNTIME; PAPER FACT]
    A{m,N} -- final mode resolution --> A* [RUNTIME; UNKNOWN]

The r loop is an intra-decision co-refinement loop. It is not physical closed-loop rollout.

Learning DAG:

    O(t) -- encoder --> W(t) [TRAIN; PAPER FACT]
    W(t) + A{m,r} -- world model --> F{m,r} [TRAIN; PAPER FACT]
    O(t+1) -- factual future BEV labels --> semantic supervision for F [TRAIN; PAPER FACT]
    current BEV labels -- semantic supervision --> L_current [TRAIN; PAPER FACT]
    A(factual) -- supervision at initial/intermediate/final heads --> L_traj{r} [TRAIN; PAPER FACT]
    nearest factual trajectory mode -- winner-take-all index m* --> aligned F{m*,r} and A{m*,r} losses [TRAIN; PAPER FACT]
    all losses -- end-to-end gradient through iterations --> encoder/world/planner [TRAIN; PAPER FACT]

Boundary facts:

- One factual future selects/supervises a mode; it is not evidence for multiple observed counterfactual futures.
- The exact deployed final-mode resolver is not sufficiently fixed by the available paper text and is marked UNKNOWN.

### 8.2 SEER-CODE: initial released evaluator/refiner

Deployment DAG:

    O(history) -- released encoder --> W(current BEV) [RUNTIME; CODE FACT]
    W + I(anchor bank) -- proposal decoder --> A{1…256} [RUNTIME; CODE FACT]
    W + A{k} -- released latent world model --> F{k}(one endpoint future BEV) [RUNTIME; CODE FACT]
    W + F{k} + A{k} -- decomposed reward heads --> V{k} [RUNTIME; CODE FACT]
    V{1…256} -- argmax --> R(fixed selected index k*) [RUNTIME; CODE FACT]
    F{k*} + A{k*} -- offset refinement and MLN fusion --> A_refined{k*} [RUNTIME; CODE FACT]
    A_refined{k*} -- output without rescoring --> A* [RUNTIME; CODE FACT]

Learning DAG:

    W + A{k} -- future predictor --> F{k} [TRAIN; CODE FACT]
    semantic map targets -- current/future map losses --> L_map [TRAIN; CODE FACT]
    candidate simulator and imitation labels -- reward heads --> L_reward [TRAIN; CODE FACT]
    A(factual) -- initial and refined offset losses --> L_offset [TRAIN; CODE FACT]
    L_map + L_reward + L_offset -- gradient --> released joint model [TRAIN; CODE FACT]

Boundary facts:

- The selected future BEV refines the trajectory after scoring, but the same k* is retained; there is no second candidate resolution. [CODE FACT]
- num_fut_timestep = 1 in the inspected release. [CODE FACT]
- The paper’s repeated world–planner feedback loop is not present in this initial release path. [CODE FACT]

## 9. P0049 — Drive-JEPA

### 9.1 Shared V-JEPA pretraining graph

    O(masked video context) -- online encoder --> S(context tokens) [TRAIN; PAPER FACT]
    S -- predictor --> F(predicted target-region representation) [TRAIN; PAPER FACT]
    O(unmasked target video) -- EMA target encoder --> stopgrad(F(target representation)) [TRAIN; PAPER FACT]
    F(predicted) + stopgrad(F(target)) -- representation loss --> L_JEPA [TRAIN; PAPER FACT]
    online encoder -- EMA parameter update --> target encoder [TRAIN; PAPER FACT]

The predictor and target encoder do not appear in the inspected downstream deployment paths. [PAPER FACT + CODE FACT]

### 9.2 DJEPA-PF

Deployment DAG:

    O(two-frame history) -- V-JEPA encoder, frozen/no-grad by default --> S(current history feature) [RUNTIME; CODE FACT]
    S -- downstream transformer --> A(trajectory) [RUNTIME; CODE FACT]
    A -- direct output --> A* [RUNTIME; CODE FACT]

Learning DAG:

    pretrained encoder -- frozen/no-grad default --> S [TRAIN; CODE FACT]
    S + A(factual) -- imitation objective --> downstream planner update [TRAIN; PAPER FACT + CODE FACT]

F = ∅, V = ∅, and R = ∅ in deployed planning. The JEPA future-prediction machinery is pretraining-only.

### 9.3 DJEPA-PB1

Deployment DAG:

    O(current perception/history) -- backbone --> S(current scene feature) [RUNTIME; PAPER FACT + CODE FACT]
    S + I(proposal queries) -- iterative proposal refiner --> A{1…N} [RUNTIME; CODE FACT]
    S + A{k} -- learned trajectory scorer --> V{k} [RUNTIME; CODE FACT]
    V{1…N} -- argmax --> R(k*) [RUNTIME; CODE FACT]
    A{k*} -- select --> A* [RUNTIME; CODE FACT]

The proposal-refinement iterations are ordinary query/trajectory refinement, not world rollout. F = ∅ at runtime.

### 9.4 DJEPA-PB2

Deployment DAG:

    O(current perception/history) -- backbone --> S(current scene feature) [RUNTIME; CODE FACT]
    S + I(proposal queries) -- iterative proposal refiner --> A{1…N} [RUNTIME; CODE FACT]
    S + A{k} -- learned scorer --> V_pdm{k} [RUNTIME; CODE FACT]
    A{k} + O(previous executed/simulated trajectory) -- comfort evaluator --> V_comfort{k} [RUNTIME; CODE FACT]
    V_pdm{k} + V_comfort{k} -- (14·V_pdm + 2·V_comfort)/16 --> V_recal{k} [RUNTIME; CODE FACT]
    V_recal{1…N} -- argmax --> R(k*) [RUNTIME; CODE FACT]
    A{k*} -- select --> A* [RUNTIME; CODE FACT]

This resolver carries information across frames through the previous-trajectory comfort term, but it still does not construct a future-world carrier.

### 9.5 Perception-based downstream learning

    offline trajectory vocabulary of 8192 entries -- simulator evaluation --> quality labels [TRAIN; PAPER FACT]
    high-quality pseudo trajectories + proposal set -- min-over-N distillation --> L_proposal [TRAIN; PAPER FACT]
    A{k} -- simulator EPDMS --> scorer labels [TRAIN; PAPER FACT]
    V{k} + labels -- scoring loss --> L_score [TRAIN; PAPER FACT]
    map/collision targets -- auxiliary objectives --> L_aux [TRAIN; PAPER FACT]
    L_proposal + L_score + L_aux -- gradient --> proposal refiner/scorer [TRAIN; PAPER FACT]

The offline vocabulary and training groups are not a runtime counterfactual-world bank.

## 10. P0062 — Metis

### 10.1 METIS-PLAN deployment DAG

    O(history) + I(instruction) -- shared latent interface --> S [RUNTIME; PAPER FACT]
    S + action noise -- action expert flow over s --> A(trajectory/actions) [RUNTIME; PAPER FACT]
    A -- output --> A* [RUNTIME; PAPER FACT]

Boundary facts:

- The visual-generation expert is bypassed in action-only planning inference. [PAPER FACT]
- F = ∅ in deployed action-only planning, even though future-video generation is jointly trained.
- R = ∅ and V = ∅; flow iterations refine an action sample.

### 10.2 METIS-PLAN learning DAG

    O + I -- shared latent interface --> S [TRAIN; PAPER FACT]
    S + action-flow noise -- action expert --> A(predicted action tokens) [TRAIN; PAPER FACT]
    action target -- flow objective --> L_action [TRAIN; PAPER FACT]
    S + A(predicted action tokens) + video noise -- visual-generation expert --> F(predicted future-video flow) [TRAIN; PAPER FACT]
    factual future video -- video-flow target --> L_video [TRAIN; PAPER FACT]
    L_video -- gradient through predicted action conditioning --> action expert [TRAIN; PAPER FACT]
    future-video tokens -- blocked by asymmetric attention --> action-token path [TRAIN; PAPER FACT]
    L_action + L_video -- joint update --> shared/action/video modules [TRAIN; PAPER FACT]

Exact implementation-level detach placement is UNKNOWN because executable source was unavailable. The paper asserts the action-to-video gradient route.

## 11. P0063 — DynFlowDrive

### 11.1 DFD-PLAN deployment DAG

    O(history) -- planner encoder --> S(current scene feature) [RUNTIME; PAPER FACT]
    S + I(mode queries) -- proposal decoder --> A{1…N} [RUNTIME; PAPER FACT]
    S + A{k} -- learned score head --> V{k} [RUNTIME; PAPER FACT]
    V{1…N} -- argmax --> R(k*) [RUNTIME; PAPER FACT]
    A{k*} -- select --> A* [RUNTIME; PAPER FACT]

The flow world model is removed from deployment. [PAPER FACT]

### 11.2 DFD-PLAN learning DAG

    O(t) -- world encoder --> W(t) [TRAIN; PAPER FACT]
    O(t+1) -- future encoder --> F(factual next latent) [TRAIN; PAPER FACT]
    W(t) + A{k} + flow coordinate s -- conditional flow model --> F{k}(predicted next latent/velocity path) [TRAIN; PAPER FACT]
    F{k} + F(factual) -- reconstruction term --> C_rec{k} [TRAIN; PAPER FACT]
    A{k} + A(factual) -- trajectory-error term --> C_traj{k} [TRAIN; PAPER FACT]
    conditional flow path -- angular stability term --> C_ang{k} [TRAIN; PAPER FACT]
    C_rec{k} + C_traj{k} + C_ang{k} -- hybrid criterion --> R_train(n*) [TRAIN; PAPER FACT]
    n* -- supervision --> V{1…N} score head [TRAIN; PAPER FACT]
    planning/world/scoring losses -- joint gradient --> training model [TRAIN; PAPER FACT]

Boundary facts:

- Flow coordinate s is a solver/interpolation coordinate, not physical time.
- One factual next latent supervises all candidate-conditioned predictions.
- Equation-sign and sampling-anchor ambiguities are preserved as unresolved rather than normalized by inference.
- No executable source was available to verify detach topology.

## 12. P0064 — Discrete-WAM

### 12.1 DWAM-POLICY: primary planning path

Deployment DAG:

    O(context/history) + I(instruction) -- context encoder --> S [RUNTIME; PAPER FACT]
    S -- decision classifier/token head --> I_D(one of 400 decision labels) [RUNTIME; PAPER FACT]
    S + I_D + masked/noisy action tokens -- iterative parallel token editing --> A(trajectory tokens) [RUNTIME; PAPER FACT]
    A -- decode --> A* [RUNTIME; PAPER FACT]

Boundary facts:

- The 400 decisions form a supervised discrete vocabulary; they are not established as 400 runtime trajectories passed through a common scorer.
- Token-editing iterations are solver iterations, not physical rollout.
- Future visual tokens are not required by the reported primary policy-only planning path. [PAPER FACT]
- R = ∅ and V = ∅ unless the decision-token classifier itself is viewed as a standard categorical decoder; it is not a candidate consequence resolver.

### 12.2 DWAM-WORLD: action-conditioned world generation

Deployment DAG:

    O(context/history) + I(supplied action sequence) -- world model --> masked future visual tokens [RUNTIME; PAPER FACT]
    masked future visual tokens -- iterative parallel editing --> F(future visual tokens) [RUNTIME; PAPER FACT]
    F -- visual decoder --> generated future video [RUNTIME; PAPER FACT]

A* = N/A in this mode because the action is supplied rather than selected.

### 12.3 DWAM-JOINT: world-policy generation

Deployment DAG:

    O(context/history) + I(instruction) -- shared discrete model --> S [RUNTIME; PAPER FACT]
    S -- interleaved/parallel editing --> A(action tokens) [RUNTIME; PAPER FACT]
    S + A -- interleaved/parallel editing --> F(future visual tokens) [RUNTIME; PAPER FACT]
    A + F -- repeated joint generation steps --> A and F sequences [RUNTIME; PAPER FACT]

Whether this joint mode is used for the headline planning metrics, rather than demonstrated as a generative capability, remains bounded by the paper statements and is listed as an unresolved deployment-reporting question.

### 12.4 Shared staged learning DAG

    O + supplied A + factual future frames -- visual-token world pretraining --> world model [TRAIN; PAPER FACT]
    O + actions + future visuals -- joint world-policy pretraining --> shared discrete model [TRAIN; PAPER FACT]
    action demonstrations -- action LoRA fine-tuning --> policy path [TRAIN; PAPER FACT]
    policy samples grouped per context -- EPDMS reward --> GRPO advantages [TRAIN; PAPER FACT]
    GRPO advantages -- policy update --> action-token model [TRAIN; PAPER FACT]

Training-time sample groups are not evidence of an online candidate bank or runtime score-and-select resolver.

## 13. P0065 — GraphWorld

### 13.1 GW-PLAN deployment DAG

    O(agent history, map, ego context) -- perception/motion encoders --> S [RUNTIME; PAPER FACT]
    S -- ECIG ego-star interaction and GRU --> W_cur(current structured latent world) [RUNTIME; PAPER FACT]
    S + I(motion/planning hypotheses) -- hypothesis projection --> W_tgt(target structured latent) [RUNTIME; PAPER FACT]
    W_cur + W_tgt + flow coordinate s -- two-step flow refinement --> W_ref [RUNTIME; PAPER FACT]
    W_ref(agent nodes) + A_agent{m} -- mode reweighting/refinement --> agent motion outputs [RUNTIME; PAPER FACT]
    W_ref(ego node) + planning queries -- trajectory decoder --> A_ego{m} [RUNTIME; PAPER FACT]
    A_ego{m} -- final mode resolution --> A* [RUNTIME; UNKNOWN]

Boundary facts:

- The two flow steps are internal latent transport, not two physical future steps.
- No explicit rendered/decoded future-world rollout is required.
- The carrier is explicitly structured around ego and agents and is reused by motion and planning heads. [PAPER FACT]

### 13.2 GW-PLAN learning DAG

Stage I:

    O(t) -- shared perception/interaction stack --> W_cur(t) [TRAIN; PAPER FACT]
    W_cur -- detection, mapping, motion, and planning heads --> multitask losses [TRAIN; PAPER FACT]
    multitask losses -- gradient --> shared world representation [TRAIN; PAPER FACT]

Stage II temporal consistency:

    physical inputs at t+1 -- same world encoder --> stopgrad(W_next) [TRAIN; PAPER FACT]
    physical inputs at t -- world encoder/flow path --> W_t [TRAIN; PAPER FACT]
    W_t + stopgrad(W_next) -- L2 temporal consistency --> L_consistency [TRAIN; PAPER FACT]
    L_consistency + task losses -- update --> current-time world/flow/planning path [TRAIN; PAPER FACT]

Boundary facts:

- The target world state is stopped from receiving gradients in the stated consistency path. [PAPER FACT]
- Exact temporal alignment between the paper’s W_t and W_{t+1} notation and the target-transport endpoint is not source-verified.
- Executable source and the exact final ego-mode resolver are UNKNOWN.

## 14. Cross-artifact factual matrix

This matrix records graph facts only; it is not a taxonomy.

| Artifact | Runtime F consumed before A* | Runtime candidate identity | Runtime learned V/R | Future/world branch training-only relative to A* |
|---|---:|---:|---:|---:|
| LAW-PF | no | no | no | yes |
| LAW-PB | no | no | no | yes |
| EPO-PLAN | no | no | no | visual branch yes |
| EPO-SELF | generated F is the mode output/context | no | no | no |
| EPO-CTRL | generated F is the mode output | no | no | no |
| DLAW-PAPER/CODE | internal generative hidden state yes | no | no | full video decode absent |
| W4D-PLAN | yes | yes | yes | no |
| WD-PLAN | surrogate F yes | yes | yes | heavy teacher yes |
| WOTE-PLAN | yes | yes | yes | no |
| SEER-PAPER | yes | yes/multimode | final resolver UNKNOWN | no |
| SEER-CODE | yes | yes | yes | no |
| DJEPA-PF | no | no | no | JEPA predictor yes |
| DJEPA-PB1/PB2 | no | yes | yes | JEPA predictor yes |
| METIS-PLAN | no | no | no | video expert yes |
| DFD-PLAN | no | yes | yes | flow world model yes |
| DWAM-POLICY | no | no verified bank | no consequence resolver | visual generation optional/other mode |
| DWAM-WORLD | F is output | N/A | N/A | no |
| DWAM-JOINT | F and A jointly generated | token identity | no verified score-select | no |
| GW-PLAN | structured W_ref yes; explicit future F no | motion/planning modes | final ego resolver UNKNOWN | no |

## 15. Phase 1 stop condition

The artifact-level deployment and learning DAGs are now explicit, including:

- node and edge lifecycles;
- candidate identity;
- resolver placement;
- gradient/stop-gradient boundaries where supported;
- separation of solver, refinement, and physical time;
- verified absences and bounded unknowns.

No category names or ontology decisions are introduced here. The next phase must begin only after review of this document and the unresolved evidence ledger.
