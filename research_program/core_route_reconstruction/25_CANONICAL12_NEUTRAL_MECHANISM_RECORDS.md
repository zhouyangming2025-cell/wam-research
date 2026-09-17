# Canonical-12 Neutral Mechanism Records
Status: **phase-1 neutral reconstruction; no old route code and no ontology projection**.

The unit below is an artifact: paper or code version × task mode × planning or generation path. A paper may therefore have several records. The records are intentionally written as causal programs rather than labels.

## Record schema

Each record answers:

1. problem and intended contribution;
2. input and final output;
3. deployment causal graph;
4. training forward graph;
5. supervision/backward graph;
6. world or predictive object semantics;
7. deployment lifecycle;
8. action/world dependency;
9. candidate birth, identity, and commitment;
10. commitment supervision;
11. clock types;
12. deletion test and evidence boundary.

`Current/history` means a state computed from present or past observations. `Future-derived` means a state produced by a prediction/generation computation. `Candidate-conditioned` means the object is separately indexed by an action hypothesis. `Internal denoising state` means a generator intermediate, not necessarily a rendered future scene.

## LAW

### LAW-PLAN-PF — perception-free planning artifact

- **Problem / output:** Improve raw-camera end-to-end planning by exploiting temporal information and ego action, outputting one future waypoint sequence. The paper says the latent world model predicts future visual latents from current visual latents and predicted waypoints; see `papers/raw_md/P0048_LAW/P0048_LAW.raw.md:21-38,65-99`.
- **Deployment graph:** `current images/history → visual latent → waypoint decoder → trajectory`. The future-latent predictor is not an online trajectory evaluator and does not select among identity-preserved candidates.
- **Training graph:** `current latent + predicted waypoints → predicted next latent`; the next-frame latent is the target. Future-latent loss jointly pressures the representation and waypoint path.
- **World object:** action-conditioned predicted next latent, used as a training target pathway; it is not a deployed counterfactual branch.
- **Lifecycle / dependency:** training-only future branch; action→future prediction is present in training, but future→action is a loss-mediated effect rather than an inference edge.
- **Candidates / commitment:** one direct decoded trajectory; no explicit candidate bank or common resolver established.
- **Supervision / clocks:** future-frame latent MSE and waypoint loss; the future step is a physical next-frame target, but no online rollout is required.
- **Deletion / confidence:** deleting the latent-world loss removes the paper's central self-supervised representation-shaping contribution while leaving a normal planner. **Confidence: high.**

### LAW-PLAN-PB — perception-based planning artifact

- Same causal program as LAW-PLAN-PF, with BEV latents and perception heads added. The raw paper explicitly separates the perspective-view and BEV variants at `papers/raw_md/P0048_LAW/P0048_LAW.raw.md:101-154`.
- The BEV perception tasks are representation-supporting outputs, not a candidate resolver. The world branch still predicts a future latent from current latent plus waypoints only for training.
- **Confidence: high for shared mechanism; modality/perception differences are profile attributes.**

## Epona

### EPONA-PLAN — real-time trajectory planning path

- **Problem / output:** Reconcile long-horizon video generation with trajectory planning. Given historical observations and actions, the model produces a trajectory policy and a conditional next-frame distribution; see `papers/raw_md/P0001_Epona/P0001_Epona.raw.md:20-38,100-112`.
- **Deployment graph:** `history observations/actions → multimodal spatiotemporal latent F → TrajDiT → trajectory`. A separate VisDiT can generate the next frame, but the paper explicitly says planning can run with video prediction deactivated (`:34-36,114-153,183-211`).
- **Training graph:** the shared temporal trunk receives trajectory loss and video loss; the two specialized heads generate action and visual futures in parallel.
- **World object:** a shared temporal latent encoding history and dynamics, not a candidate-indexed future consequence consumed by a resolver.
- **Lifecycle / dependency:** the video branch is optional for planning deployment; the shared temporal representation remains on the action path. Action can condition the visual branch for controllable generation, but the planner is not selected by evaluating generated videos.
- **Candidates / commitment:** TrajDiT generates one trajectory sample per sampling run; no explicit identity-preserving candidate pool with a common resolver is established in the planning path.
- **Supervision / clocks:** rectified-flow losses for trajectory and visual streams; autoregressive physical time for video generation and internal diffusion/flow solver steps. These clocks must not be conflated.
- **Deletion / confidence:** disabling video prediction reduces planning performance in the ablation, so the visual training branch is important, but it is not an online consequence resolver. **Confidence: high.**

### EPONA-GEN — self-rollout and externally controlled generation path

- **Deployment graph:** `history → shared temporal latent → VisDiT → next frame`, repeated autoregressively; an external or model-predicted action can control the visual branch.
- **Role:** terminal world/video generation or simulation capability, not the trajectory-planning commitment path. It is kept as a separate artifact so that generation is not mistaken for planning.
- **Evidence:** `papers/raw_md/P0001_Epona/P0001_Epona.raw.md:106-112,141-153,155-171`.
- **Confidence: high.**

## DriveLaW

### DRIVELAW-PLAN — chained generator-state planning

- **Problem / output:** Existing unified systems keep generation and planning parallel; DriveLaW claims the planner should consume the video generator's learned internal representation. See `papers/raw_md/P0009_DriveLaW/P0009_DriveLaW.raw.md:9-25,45-68`.
- **Deployment graph:** `history + ego/command → Video DiT denoising states → cached intermediate video features → Action DiT → trajectory`. The relevant carrier is an online generator-internal state; decoding a future video is not required for the action head.
- **Training graph:** video generator is trained on scene generation, then its intermediate features condition the action planner in a later training stage; the paper uses a three-stage progressive curriculum (`:137-145`).
- **World object:** future-generation internal state, not a rendered future and not a candidate-specific consequence.
- **Lifecycle / dependency:** retained online because the action head needs cached Video DiT features. The action output is one-way conditioned by the generator state; no downstream common resolver is shown.
- **Candidates / commitment:** diffusion/flow sampling of the action variable does not by itself create an explicit candidate pool. The final trajectory is the action head output.
- **Supervision / clocks:** video-generation losses, action flow-matching loss, and staged transfer. Internal denoising/flow steps are solver clocks, not separate physical future rollout.
- **Deletion / confidence:** deleting the video-latent→Action-DiT edge removes the stated planning contribution, while keeping a video generator and a planner. **Confidence: high for paper topology; code numeric details remain secondary.**

## World4Drive

### WORLD4DRIVE-PLAN — intention-indexed endpoint-future plausibility selection

- **Problem / output:** A single future cannot represent multimodal driving intentions. The system builds multiple intention-conditioned trajectories and future world latents, then commits one trajectory.
- **Deployment graph:** `current visual/physical latent + intention queries → trajectories {T_k}; (current latent, T_k) → predicted future latent L_k → ScoreNet → argmax k → T_k*`. The paper states this explicitly at `papers/raw_md/P0046_World4Drive/P0046_World4Drive.raw.md:101-136`.
- **World object:** candidate-indexed future latent at a selected future interval (`n=3` by default), closer to an endpoint/summary consequence than a recurrent physical-time sequence.
- **Training graph:** actual future latent is compared with each predicted modality; the closest mode supplies a reconstruction target and a score target; trajectory and semantic losses are added (`:138-148`).
- **Lifecycle / dependency:** the candidate-specific predictor and score path remain online; the actual future latent is a training reference, not an inference observation.
- **Candidates / commitment:** candidate identity is preserved through `L_k` and ScoreNet to one final trajectory. This is a genuine common resolver, not merely multiple random samples.
- **Supervision / clocks:** factual future compatibility, semantic representation, and trajectory supervision; no evidence of multi-step physical rollout in the main planning path.
- **Deletion / confidence:** deleting intention-conditioned future prediction collapses the paper toward a single-mode LAW-like planner; deleting the selector removes the multimodal commitment mechanism. **Confidence: high.**

## WorldDrive

### WORLDDRIVE-PLAN — distilled candidate-specific future surrogate selection

- **Problem / output:** Unify scene-generation and motion representations while retaining future foresight at real-time cost.
- **Deployment graph:** `history → frozen visual/motion encoders → top-K candidates {v_k}; (history, v_k) → Future-aware Rewarder surrogate zhat_k → candidate reward r_k → argmax → v_k*`. See `papers/raw_md/P0042_WorldDrive/P0042_WorldDrive.raw.md:45-53,65-102`.
- **World object:** candidate-conditioned future scene latent, produced by a lightweight online surrogate. The heavy TA-DWM is not sampled for every candidate at deployment.
- **Training graph:** TA-DWM is trained with expert-motion-conditioned future scene targets; encoders transfer to the planner; FAR is trained to match frozen-world future latents and rank candidate preferences (`:104-128`).
- **Lifecycle / dependency:** a candidate-specific future surrogate remains online; the original world generator is distilled/removed from the hot path.
- **Candidates / commitment:** top-K candidate identity survives through the surrogate and reward head to a common resolver.
- **Supervision / clocks:** world diffusion target, latent alignment with stop-gradient, and preference ranking using an oracle driving score. The reward semantics and future-latent provenance are distinct attributes.
- **Deletion / confidence:** deleting FAR preserves representation inheritance but removes the online future-informed selection mechanism. **Confidence: high.**

## WoTE

### WOTE-PLAN — online recurrent candidate-consequence evaluation

- **Problem / output:** A trajectory should be evaluated by the future state it induces, not only by current-state similarity.
- **Deployment graph:** `sensor input → BEV state → candidate trajectories {A_k}; (BEV_t,A_k) → recurrent future BEV/action states O_{k,1:H} → reward model → argmax k → A_k*`. The paper gives this program at `papers/raw_md/P0045_WoTE/P0045_WoTE.raw.md:42-44,46-105`.
- **World object:** candidate-conditioned time-expanded BEV state/action sequence, not a single endpoint.
- **Training graph:** simulated future BEV states and simulator rewards supervise the world/reward branches; expert distance supplies an imitation preference signal (`:107-144`).
- **Lifecycle / dependency:** the world model and reward model are online and candidate-specific. The recurrent prediction is an internal physical-future clock, distinct from a transformer's layer iterations.
- **Candidates / commitment:** trajectory anchors are refined into a bank; identity is retained through future rollouts and one shared reward resolver.
- **Supervision / clocks:** simulator future states, simulation rewards, expert-trajectory compatibility, and trajectory loss. The simulator is a training supervisor; the online BEV rollouts are still part of deployment.
- **Deletion / confidence:** deleting the recurrent candidate consequence branch leaves an ordinary multimodal planner but removes the paper's central online evaluation claim. **Confidence: high.**

## SeerDrive

### SEERDRIVE-PAPER — reciprocal scene/planning refinement

- **Problem / output:** One-shot current-scene planning misses mutual dependence between future scene evolution and ego action.
- **Deployment graph:** `current BEV + ego state → future BEV → plan using current+future → refined ego feature feeds back to world model → updated future BEV and plan`, repeated before the final trajectory. Raw evidence: `papers/raw_md/P0061_SeerDrive/P0061_SeerDrive.raw.md:13-28,65-101`.
- **World object:** predicted future BEV feature, with multimodal mode association; the central mechanism is the feedback loop, not merely the presence of a future feature.
- **Action/world dependency:** future scene→plan and refined plan/ego feature→future scene occur within the same decision computation.
- **Candidates / commitment:** mode-specific outputs exist, but the paper does not establish a separate common resolver with the same clarity as WoTE. Final commitment semantics remain **UNKNOWN**.
- **Training graph:** current/future BEV losses and trajectory losses are applied across iterations; the paper describes end-to-end joint learning.
- **Clocks:** internal refinement rounds are not automatically physical-time rollout or cross-cycle environment feedback; the audit explicitly records this boundary in `audits/literature/PHASE_C5_SEERDRIVE_AUDIT.md:142-152`.
- **Deletion / confidence:** deleting the feedback edge leaves future-aware planning but removes the claimed bidirectional paradigm. **Confidence: high for paper loop; medium for final resolver.**

### SEERDRIVE-CODE — released implementation boundary

- **CODE FACT:** the source audit says the released implementation integrated an online trajectory evaluation/selection path and did not preserve the paper's iterative planning↔scene-modeling interaction. See `audits/literature/PHASE_C5_SEERDRIVE_AUDIT.md:23-73`.
- **Reconstructed graph:** `anchors/candidates → latent future evaluation → selection`, followed by a refinement path that is not re-scored as the paper loop would require.
- **Binding rule:** this is a separate code artifact. It must not replace the paper record, and it must not be used to claim that the paper's reciprocal loop was reproduced.
- **Confidence:** high for the existence of the paper/code boundary; medium for undocumented implementation details.

## Drive-JEPA

### DRIVEJEPA-PF — predictive pretraining plus direct planner

- **Problem / output:** Scale predictive video representation learning and use it for direct end-to-end planning.
- **Deployment graph:** `front-view/history → pretrained ViT features → waypoint decoder → one trajectory`. Raw evidence: `papers/raw_md/P0049_DriveJEPA/P0049_DriveJEPA.raw.md:81-99`.
- **Training graph:** V-JEPA/video pretraining shapes the encoder; downstream human trajectory MSE trains the decoder. The V-JEPA predictor/target branch is not retained as an online future simulator.
- **World object:** predictive representation transfer, not an online future consequence.
- **Candidates / commitment:** no explicit proposal bank or common resolver in the PF artifact.
- **Supervision / clocks:** masked predictive pretraining, driving-video pretraining, and waypoint MSE; no online physical rollout.
- **Deletion / confidence:** deleting V-JEPA weakens the paper's central scalable predictive-learning claim but leaves a direct planner. **Confidence: high.**

### DRIVEJEPA-PB — proposal-centric planner with compiled simulator guidance

- **Problem / output:** Mitigate single-human-trajectory mode collapse by generating and selecting diverse proposals.
- **Deployment graph:** `features + ego status → iterative proposal bank {A_k} → learned proposal scorer (+ previous-trajectory comfort) → argmax k → A_k*`. See `papers/raw_md/P0049_DriveJEPA/P0049_DriveJEPA.raw.md:100-157`.
- **World object / lifecycle:** simulator-based EPDMS produces pseudo-teachers and score targets during training; no V-JEPA world rollout or simulator is shown on the deployed action path.
- **Candidates / commitment:** identity is preserved to a common scorer and final argmax.
- **Training graph:** V-JEPA transfer; simulator-scored multimodal trajectory distillation; scorer training; auxiliary map/collision losses.
- **Supervision / clocks:** proposal refinement rounds and previous-cycle comfort recalibration; those are not future physical rollout. The simulator criterion is a teacher, not a runtime world carrier.
- **Deletion / confidence:** deleting proposal/distillation/selection changes the full planner mechanism, but not the paper's predictive-pretraining lineage. **Confidence: high for paper artifact; exact released-code path remains a separate evidence boundary.**

## Metis

### METIS-PLAN — asymmetric joint learning with action-only deployment

- **Problem / output:** Previous WAMs require expensive future-video sampling or suffer interference between video and action distributions.
- **Deployment graph:** `current observation + context → shared latent/backbone forward pass → action expert → action chunk`. The paper formally states future observations are training-only and action uses the current-observation latent (`papers/raw_md/P0062_Metis/P0062_Metis.raw.md:46-77`).
- **Training graph:** action tokens and future video tokens share a latent interface; future video tokens may attend to predicted future actions, while action tokens cannot attend to future video tokens (`:79-115`).
- **World object:** action-conditioned future video sequence exists in training, not deployment. The asymmetric visibility direction is the key learning mechanism.
- **Candidates / commitment:** direct action generation; diffusion/flow sampling is not an explicit identity-preserving candidate resolver.
- **Supervision / clocks:** action and video flow-matching losses; video branch can be bypassed at inference. Solver iterations are not a physical rollout.
- **Deletion / confidence:** remove asymmetric co-training and the method loses its controlled world/action transfer claim, although an action planner remains. **Confidence: high.**

## DynFlowDrive

### DYNFLOWDRIVE-PLAN — world-dynamics criterion compiled into a scorer

- **Problem / output:** Geometric trajectory error does not reveal whether a trajectory induces stable world dynamics.
- **Training graph:** `candidate trajectories {A_k} → trajectory-conditioned latent flow → future latent evolution/velocities → reconstruction, trajectory, and stability criterion → selected training mode → scorer supervision`. See `papers/raw_md/P0063_DynFlowDrive/P0063_DynFlowDrive.raw.md:56-58,90-213`.
- **Deployment graph:** `current images → candidate bank + score head → argmax score → trajectory`; the paper explicitly states the world model is not involved during inference (`:203-213`).
- **World object:** candidate-conditioned dynamic world sequence exists in training only; it is not an online carrier.
- **Candidates / commitment:** candidate identity is preserved to a learned scorer and final selection, even after the flow model is removed.
- **Supervision / clocks:** flow solver steps describe latent transition simulation during training; they are not deployment future rollouts. Stability is one part of the training selection criterion, not automatically a separate top-level route.
- **Deletion / confidence:** deleting the flow world criterion leaves a proposal scorer but removes the paper's dynamics-aware selection mechanism. **Confidence: high for lifecycle; medium for exact gradient reach.**

## Discrete-WAM

### DWAM-POLICY — semantic decision followed by action-token generation

- **Problem / output:** Align visual/world and action modeling in one token-editing framework while preserving structured low-frequency driving decisions.
- **Deployment graph:** `context → high-level decision tokens D → future action-token editing → continuous action/trajectory`. Raw formulation: `papers/raw_md/P0064_Discrete-WAM/P0064_Discrete-WAM.raw.md:55-67,95-101`.
- **World object / lifecycle:** world modeling and world-policy modeling are training tasks; the policy path does not require future visual token generation before action output.
- **Candidates / commitment:** the primary policy mode is hierarchical action formation, not a candidate bank followed by a common resolver. Optional post-training samples are a separate optimization artifact.
- **Training graph:** unified token interface; visual world modeling, joint world-policy training, then action finetuning. The paper gives the staged program at `:71-190`.
- **Clocks:** token-edit rounds and optional policy post-training rounds; neither should be mislabeled as physical future time.
- **Deletion / confidence:** deleting the decision skeleton changes action formation; deleting world-policy pretraining changes the WAM training program. These are two distinct contributions in one paper. **Confidence: high for paper-level separation.**

### DWAM-WORLD — action-conditioned visual generation task

- **Graph:** `context + supplied future action tokens → future visual token sequence` under the unified Transformer. Evidence: `papers/raw_md/P0064_Discrete-WAM/P0064_Discrete-WAM.raw.md:85-94,158-160`.
- **Role:** a world-model task/capability, not automatically the deployed planning path. It may be used to learn action-conditioned dynamics, but the paper does not establish that the policy deployment must first generate these visual tokens.
- **Confidence:** high for task definition; deployment use in the primary policy path is not claimed.

### DWAM-JOINT — interleaved world-policy generation task

- **Graph:** `context → interleaved action token and visual token sequence`, where action at a step precedes the corresponding visual token and the visual token can condition on that action (`papers/raw_md/P0064_Discrete-WAM/P0064_Discrete-WAM.raw.md:140-156`).
- **Role:** joint training/generation artifact. It does not by itself prove a downstream candidate resolver or a deployed world-before-action path.
- **Post-training boundary:** the paper samples groups of action trajectories and scores them with an online reward during post-training (`:192-204`), but this is an optimization loop, not sufficient evidence that routine deployment uses the same reward as the final commitment resolver.
- **Confidence:** high for the joint task; routine deployment commitment remains **UNKNOWN**.

## GraphWorld

### GRAPHWORLD-PLAN — relational current-world state conditioning

- **Problem / output:** Improve long-horizon planning without explicit multi-step future-scene rollout.
- **Deployment graph:** `sensor history → ego-centric interaction graph + recurrent temporal state → latent world state → flow/state refinement and importance modulation → multimodal planning queries → trajectories`. The paper explicitly contrasts this with explicit multistep rollout at `papers/raw_md/P0065_GraphWorld/P0065_GraphWorld.raw.md:18-31,43-81`.
- **World object:** a current, relational, temporally grounded world state carrying future-relevant interaction semantics. A target state is used for temporal supervision; it is not an observed future at deployment.
- **Action/world dependency:** the world state conditions planning. The target-state construction uses aggregated motion/planning context, but candidate identity is not shown to persist through separate future branches.
- **Candidates / commitment:** multimodal trajectory hypotheses are decoded, but the paper does not state a definitive common resolver/final argmax in the frozen raw evidence. Final commitment is **UNKNOWN**.
- **Training graph:** end-to-end perception/motion/planning, then explicit temporal world-state consistency with stop-gradient (`:229-247`).
- **Clocks:** a small flow/state refinement clock exists online; the paper's core claim is compact state conditioning rather than physical-time rollout. The raw paper states single-step world-state prediction as a limitation (`:394-398`).
- **Deletion / confidence:** deleting ECIG/WSCP returns the method toward an ordinary interaction-aware planner; deleting explicit temporal world-state supervision weakens temporal grounding but leaves the relational encoder. **Confidence: medium-high; final resolver remains UNKNOWN.**

## Cross-record warning

The records show why “future prediction,” “joint world/action,” or “a scorer exists” cannot be used as route identities by themselves. The decisive questions are:

```text
What semantic object reaches the action path?
Does it exist at deployment?
Is it indexed by a retained action candidate?
Does a common resolver commit one candidate?
Is the world computation one-way, reciprocal, or training-only?
```
