# D01 Protocol Issues

This file proposes protocol changes but does not enact them. Each issue admits more than one defensible global rule.

## 1. World model used to train a policy but absent from deployment

**Cases:** Think2Drive, CausalDrive policy post-training, SimWAM.

**Ambiguity:** The current scope asks for a material planning connection but does not set a single threshold for a predictive model whose influence is carried only in learned policy parameters. Excluding these works would erase a major model-based policy-learning lineage; including every simulator-trained policy would over-expand the domain.

**Primary evidence:** Think2Drive arXiv 2402.16720; CausalDrive arXiv 2606.15341; SimWAM arXiv 2608.07468.

**Possible fixes:**

1. Require the predictive model to remain on the deployed action path; place all training-only uses in the boundary corpus.
2. Admit training-only use when a named predictive operation supplies imagined transitions/rewards or a future-prediction loss directly optimizes the deployed policy, and record lifecycle explicitly.
3. Maintain two coequal domain strata: online decision-time use and policy-learning use.

**Recommendation:** adopt option 3. It preserves causal differences without declaring one lifecycle non-domain.

## 2. Predictive pretraining transferred to a conventional planner

**Cases:** ViDAR, DriveWorld, ReWorld, WA-JEPA.

**Ambiguity:** A broad rule can accidentally admit any video-pretrained encoder, while a strict online-use rule discards papers that experimentally connect predictive pretraining to planning.

**Primary evidence:** ViDAR CVPR 2024; DriveWorld CVPR 2024; ReWorld arXiv 2606.27504; WA-JEPA arXiv 2608.20974.

**Possible fixes:**

1. Exclude all pretraining-only prediction from Tier 1.
2. Admit only when the paper defines a driving-specific predictive objective, transfers the learned state into an evaluated one-stage planner, and supplies a matched ablation against non-predictive initialization.
3. Admit any backbone with future-data pretraining.

**Recommendation:** option 2. It is narrow enough to reject generic representation pretraining and auditable at census depth.

## 3. Action-adjacent future representations versus environment futures

**Cases:** Auto-JEPA and, to a lesser degree, DA-WAM.

**Ambiguity:** A latent derived from future ego trajectory can be predictive and useful while containing little independent environment dynamics. Calling every future action embedding a world object would collapse planning labels into world modeling.

**Primary evidence:** Auto-JEPA arXiv 2607.29031 and `PHASE_B_WAVE3_AUTOJEPA_AUDIT.md`; DA-WAM arXiv 2608.19085.

**Possible fixes:**

1. Require the predictive object to contain at least one non-ego environment variable.
2. Admit planning-oriented future latents but tag whether their semantic support is ego-only, environment-only, or joint.
3. Exclude only exact encodings of the target trajectory and admit compressed intent predictions.

**Recommendation:** option 2, with an explicit evidence field for semantic support. This avoids a brittle binary judgment while preserving the distinction.

## 4. Reward model attached to an otherwise non-world planner

**Cases:** DriveReward versus Gen-Drive and WorldRFT.

**Ambiguity:** A learned reward can strongly affect action selection or fine-tuning without predicting consequences. Treating reward as world modeling admits ordinary scorers; excluding any reward-centric mechanism hides cases where reward evaluates generated future worlds.

**Primary evidence:** DriveReward arXiv 2606.08525; Gen-Drive arXiv 2410.05582; WorldRFT arXiv 2512.19133.

**Possible fixes:**

1. Reward models are always boundary artifacts.
2. Reward models qualify only as part of a larger artifact when they evaluate a separately generated future/consequence object; the rewarder alone remains boundary.
3. Any learned reward that improves a planner qualifies.

**Recommendation:** option 2. It distinguishes DriveReward as an adjunct from Gen-Drive's generate-then-evaluate planning artifact.

## 5. Joint multi-agent futures versus intervention-dependent reaction

**Cases:** Gen-Drive, SafeDrive, CausalDrive, RaWMPC; GameFormer as a control.

**Ambiguity:** Joint generation under shared noise can capture correlation without learning how other agents would change under alternative ego actions. Candidate conditioning can also be present while supervision reuses the same factual future.

**Primary evidence:** Gen-Drive arXiv 2410.05582; SafeDrive arXiv 2602.18887 and its repository audit; CausalDrive arXiv 2606.15341; RaWMPC arXiv 2602.23259; GameFormer ICCV 2023.

**Possible fixes:**

1. Mark response as intervention-dependent whenever ego action enters the predictor.
2. Require alternative-action supervision or interactive simulation validation before making a causal/reactive claim.
3. Separate architectural conditioning, supervision support, and evaluation support into three fields.

**Recommendation:** option 3. Architectural conditioning is factual, while causal validity should remain `UNKNOWN` unless independently supported.

## 6. Paper with both simulator and planner-facing modes

**Cases:** Drive-WM, DrivingGPT, CausalDrive.

**Ambiguity:** Paper-level scope tiers obscure that one mode may terminate in world generation while another terminates in action, and that a simulator can be runtime for evaluation but training-only for the final policy.

**Primary evidence:** Drive-WM CVPR 2024; DrivingGPT ICCV 2025; CausalDrive arXiv 2606.15341.

**Possible fixes:**

1. Assign one scope verdict to the whole paper and describe modes narratively.
2. Keep paper-level corpus membership but require artifact-level terminal output and lifecycle records whenever modes differ.
3. Split each mode into independent paper records.

**Recommendation:** option 2. It preserves bibliographic identity while making mechanism evidence count at artifact granularity.

## Protocol surprise

The pilot did not require a new mechanism taxonomy. It did reveal that lifecycle and terminal-output fields must be mandatory before any later classification: without them, SimWAM can be mistaken for an online generator, CausalDrive's simulator can be mistaken for its deployed policy, and DrivingGPT's generation result can be mistaken for a planning result.
