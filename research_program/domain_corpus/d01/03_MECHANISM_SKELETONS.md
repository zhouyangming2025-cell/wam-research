# D01 Neutral Mechanism Skeletons

These skeletons intentionally use semantic interfaces rather than taxonomy labels. Each entry states the terminal action, predictive object, lifecycle, future conditioning, action formation/commitment, learning transfer, deployment retention, intervention response, and uncertainty use. `UNKNOWN` is evidence-bounded.

## A01 — Drive-WM planning

`multi-view history + route -> scene latent -> ego-candidate-conditioned future views -> planning cost per candidate -> minimum-cost ego trajectory`

- The explicit horizon future is online and branches by candidate trajectory; the final output is one trajectory.
- Candidate identity persists to a shared cost-based resolver. Multimodal futures are useful only insofar as that resolver consumes the generated branch.
- Training-only: future-video supervision. Retained: encoder, conditional generator, cost/selection path. Dropped: pixel decoding may be avoidable for some internal computation, but exact code path is UNKNOWN.
- Other-agent response is conditioned through candidate-controlled generation; causal validity outside logged support is not established.

## A02 — Drive-WM generation

`multi-view history + external action/control -> conditional world generator -> multiview future video`

- The terminal product is future video, not a vehicle action; there is no action resolver in this mode.
- Generator is retained online. Training uses future video reconstruction/generation targets.
- Control-dependent world response exists in the generator; planning consumption and uncertainty commitment are not applicable to this terminal mode.

## A03 — OccWorld planning

`camera history -> 3D occupancy state -> recurrent future occupancy horizon -> planning head/optimization -> ego trajectory`

- A separately traceable occupancy future exists and is used by planning at runtime; history and ego context condition it.
- Action formation is planning over the predicted geometric state; the exact treatment of multiple occupancy futures in commitment is UNKNOWN.
- Training retains occupancy forecasting and planning supervision. Runtime keeps occupancy dynamics and planning modules; no teacher-only surrogate relationship was established.
- Explicit intervention-conditioned response of other agents is not established.

## A04 — Think2Drive policy learning

`privileged structured state -> latent recurrent state + policy action -> imagined next latent/reward/termination horizon -> actor/critic updates -> deployed policy action`

- The world object is an action-conditioned latent transition used during training; the terminal runtime output is control from the learned policy.
- Imagined alternatives are optimized through expected return during actor-critic learning, not through an online candidate resolver.
- Runtime keeps state inference and policy; long imagined rollouts and learning heads are dropped/bypassed. Exact optimized deployment graph is UNKNOWN.
- Environment response depends on action in imagination; social-reaction fidelity is not separately proven. Stochasticity is learned and consumed through return learning.

## A05 — DrivingGPT planning

`visual/history tokens + navigation context -> shared autoregressive state -> action-token generation -> decoded ego trajectory`

- Future/world and action tokens share a generative backbone; the terminal output in this mode is trajectory.
- Action is formed autoregressively rather than by an evidenced common candidate resolver. How much generated world content is explicitly consumed before each action token is partly architecture-dependent and code-unverified.
- World/action token objectives train the shared model; runtime retains the autoregressive planner. External teacher/surrogate relation is not established.
- Multimodality may arise from sampling, but decision-time consumption of uncertainty is UNKNOWN.

## A06 — DrivingGPT generation

`visual/history tokens + optional action context -> shared autoregressive state -> future visual tokens -> future video`

- The terminal output is generated world content. No final driving action is committed in this mode.
- The same world/action training backbone is retained. Planning selector, value, and uncertainty consumption are not applicable here.

## A07 — Drive-OccWorld planning

`multi-camera history -> occupancy representation -> 4D occupancy forecast -> planning decoder -> ego trajectory`

- The explicit horizon occupancy future is online and conditions trajectory formation.
- The checked evidence supports direct trajectory decoding, not a candidate bank with a common resolver.
- Forecasting and planning losses train the shared representation; both predictive and planning components are retained. Teacher/surrogate relation is UNKNOWN.
- Ego-intervention-conditioned reaction and planning use of multimodal uncertainty are UNKNOWN.

## A08 — ViDAR downstream planning

`image history -> BEV latent -> future point-cloud/occupancy prediction during pretraining -> transferred encoder -> downstream planner -> ego trajectory`

- Future geometry is explicitly materialized during pretraining, but not required online in the downstream planner.
- The predictive objective transfers information through encoder weights; action formation is delegated to the downstream planning head.
- Runtime drops/bypasses the forecasting decoder and retains the pretrained representation plus planner.
- No online intervention response or uncertainty consumption is established.

## A09 — DriveWorld downstream planning

`multi-view temporal input -> 4D pretrained world representation -> downstream planning adaptation -> ego trajectory`

- The separately traceable predictive program is principally pretraining-time; exact survival of individual predictive heads at planning inference is UNKNOWN.
- Action is directly decoded by the downstream planner. World knowledge transfers through pretrained spatiotemporal parameters.
- Runtime retains the adapted backbone and planner and may drop pretraining-only decoders.
- No candidate-specific response or consumed future uncertainty is established.

## A10 — Auto-JEPA intent planning

`front-camera history + route/ego context -> predicted future-intent latent -> trajectory-memory retrieval -> refinement/ranking -> ego trajectory`

- The online future object is a compressed future ego-motion intent, not a full environment future.
- Retrieval creates alternatives; checked evidence supports scene-conditioned retrieval and final planning, while exact tie-breaking/ranker topology is UNKNOWN.
- Training uses future-trajectory-derived latent targets; runtime retains the predictor and trajectory memory while a visual generator can be disabled.
- Other-agent intervention response is not modeled explicitly. The planner consumes retrieval alternatives, but calibrated uncertainty is not established.

## A11 — WorldRFT planning

`observation/history -> latent predictive state -> planning-conditioned latent evolution -> reward-aligned action generation -> ego trajectory`

- Predictive latent learning and reinforcement fine-tuning jointly shape the deployed planner.
- The checked paper supports reward/value-driven action preference; whether a persistent runtime candidate bank is always present is UNKNOWN.
- Runtime retains latent/planning modules; reward computation used for fine-tuning may be dropped or simplified at deployment.
- Explicit reactive other-agent conditioning and calibrated uncertainty consumption remain UNKNOWN.

## A12 — ReWorld planning

`driving observations -> predictive representation learning -> world-action representation -> trajectory generator -> ego trajectory`

- Prediction is separately trained to improve a representation used for planning; pixel-space future generation is not required.
- Action formation is direct trajectory generation at checked depth; final resolver semantics are not separately evidenced.
- Training-only predictive targets/heads can be dropped while the learned representation and action head remain.
- Ego-intervention-conditioned response and planning use of uncertainty are UNKNOWN.

## A13 — WA-JEPA planning

`video/history + action context -> joint predictive world/action representation -> trajectory head -> ego trajectory`

- Future/action targets shape a shared representation, with the deployed action path retained and some prediction machinery removed.
- Action is directly formed; no evidenced online candidate consequence resolver is assumed.
- Teacher/target encoders are training-side; retained modules are the context representation and action decoder. Exact released-code detach boundaries are UNKNOWN.
- Reactive response and consumed uncertainty are not established.

## A14 — DA-WAM candidate planning

`observation/history -> current representation + candidate trajectories -> candidate-specific predicted future latents -> common score/rank -> selected trajectory`

- An online future latent is materialized per candidate; ground-truth future latent alignment is training-only.
- Candidate identity survives through shared scoring. Preference combines planning labels/hard negatives and learned future alignment, rather than proving alternative-world ground truth.
- Runtime keeps current encoder, future predictor, candidates, and scorer; target branch is dropped.
- Other-agent response under ego intervention is not directly supervised. Alternatives are consumed, but probabilistic calibration is not established.

## A15 — SafeDrive sparse-world planning

`sensor features -> ego proposals -> proposal-conditioned sparse worlds over agents/road -> collision and drivable-area reasoning -> selected/refined trajectory`

- Explicit proposal-specific horizon consequences are online. A common safety-aware planning path commits the final trajectory.
- Training uses agent motion and fine-grained safety targets; runtime retains sparse-world construction and reasoning.
- Released configuration differs in operational details from broad paper language but not in the observed high-level planning topology.
- Predicted agents depend on ego proposal, yet supervision reuses logged motion across branches; genuine counterfactual reactivity remains unverified. Multiple proposals are consumed by selection.

## A16 — Gen-Drive generate-then-evaluate

`historical vector scene + map + diffusion noise -> multiple joint ego/agent future scenes -> learned scene reward -> highest-valued ego trajectory`

- Full horizon joint futures are online and branch by sampled scene. The evaluator commits one alternative according to learned preference.
- Training stages: behavior diffusion, preference reward learning, then optional reward-based fine-tuning. Runtime retains generator and evaluator in this mode.
- Other agents are jointly generated with ego behavior; the degree to which their reactions are causally controlled by ego intervention rather than correlated joint sampling is unresolved.
- Multimodality is explicitly generated and consumed by ranking.

## A17 — Gen-Drive single-sample policy

`historical vector scene + map -> reward-fine-tuned joint-scene generator -> ego component -> trajectory`

- A joint future is materialized online, but there is no shared runtime resolver when only one sample is used.
- The learned reward transfers preference into generator parameters during fine-tuning; evaluator can be dropped at deployment.
- Other-agent joint generation remains, but alternative uncertainty is not consumed in single-sample commitment.

## A18 — SimWAM action-only deployment

`observation/history -> video expert and action expert under joint flow-matching training -> direct action expert -> ego trajectory`

- Future video is a training object only. Isolated attention prevents the action prediction from depending on generated future-frame tokens at inference.
- The video branch and its future output are dropped; the action expert and observation conditioning remain. Subsequent reinforcement learning optimizes a compositional driving reward.
- Action formation is direct, with no online future or candidate resolver. Other-agent response and uncertainty are not consumed at deployment.

## A19 — DriveFuture planning

`current latent + provisional ego action/trajectory -> predicted future latent endpoint -> progressive foresight guidance within diffusion planning -> ego trajectory`

- A future latent is online and action-conditioned. During training, a ground-truth future latent refines/alines it through an adapter; that adapter is bypassed at inference.
- Planning denoising and latent guidance interact during solving; the final trajectory comes from the guided diffusion planner and scorer/commitment details are only partly established.
- Runtime retains current encoder, latent dynamics predictor, and diffusion planner. Other-agent reactive content inside the latent is not directly verified.
- Multiple diffusion proposals may exist, but calibrated uncertainty use is UNKNOWN.

## A20 — Policy World Model planning

`front-view history + text/context -> autoregressive future state tokens -> latent future features -> trajectory decoder -> ego waypoints`

- An explicit future token horizon is predicted online and fused into planning. Pixel decoding is optional and not needed to establish the causal path.
- Action is directly decoded rather than selected from an evidenced common candidate bank.
- Action-free video pretraining and joint future/action fine-tuning transfer world knowledge; runtime retains token forecasting and action decoding.
- Forecast is not action-conditioned, so counterfactual response to alternative ego interventions is absent. Planning does not demonstrably consume calibrated multimodal uncertainty.

## A21 — CausalDrive simulator/evaluator

`initial front image + ego trajectory + sociology text -> distilled real-time world renderer -> reactive future video -> evaluation/reward stream`

- The explicit video horizon is online and conditioned on ego intervention plus a semantic behavior prompt.
- Terminal output is simulated sensor/world response, not a planner action. A teacher generator is distilled into a faster runtime renderer.
- The simulator can expose an external policy to action-dependent consequences; behavioral realism outside observed support remains a core limitation.
- Prompted/sampled alternatives exist, but no internal action commitment is made by this artifact.

## A22 — CausalDrive policy post-training

`policy observation -> policy action/trajectory -> CausalDrive rollout -> video-to-reward signal -> reinforcement updates -> deployed policy action`

- The world renderer and reward path are training-time infrastructure for the final policy artifact.
- Runtime retains the policy and drops/bypasses the simulator. Preference is transferred through reinforcement learning rather than an online resolver.
- Intervention-conditioned responses are consumed during training. Whether deployment retains any world-model state is not established.

## A23 — RaWMPC planning

`multi-view observation + ego state -> proposal network/candidate action sequences -> action-conditioned horizon rollouts -> semantic/risk/ego-state predictions -> progress-risk cost -> minimum-cost action sequence`

- Candidate-indexed futures are explicitly materialized online across a horizon. A shared cost selects the final sequence.
- Training exposes the world model to good, bad, and random controls; self-evaluation distills safer proposals into a generative proposal network.
- Runtime retains proposal generation, world rollout, decoders, and cost. No teacher-only future branch replaces online control.
- Other-agent/world consequences depend on ego candidates at model input; causal response quality beyond training support is not proven. Alternative consequences are directly consumed by selection.
