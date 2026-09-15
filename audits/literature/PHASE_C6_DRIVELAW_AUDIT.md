# Phase C.6 DriveLaW Audit

Last updated: 2026-09-15

Status: **COMPLETE FIRST PASS — PAPER + OFFICIAL SOURCE AUDITED**

Paper:

```text
DriveLaW: Unifying Planning and Video Generation in a Latent Driving World
arXiv:2512.23421v3
CVPR 2026
```

Official repository:

```text
xiaomi-research/drivelaw
main commit audited:
243e0e41148bdb1ae39ce1adf17d026e7cbd4348
```

Canonical deep read:

```text
papers/deep_analysis/P0009_DRIVELAW_DEEP_ANALYSIS_V2.md
```

---

# 1. Stable mechanism judgment

DriveLaW is **not** `future RGB video → planner` and is **not** an action-conditioned candidate consequence evaluator.

Canonical inference path:

```text
historical camera frames
→ VAE-conditioned latent/noise canvas
→ FIRST Video-DiT denoising iteration
→ cache hidden states after each Video-DiT block
→ Action-DiT blocks cross-attend corresponding cached video states
→ iterative action flow refinement
→ future ego trajectory

full video denoising rollout = OFF
future RGB decode            = OFF
explicit candidate scorer    = OFF in canonical paper/config path
```

Canonical subtype:

```text
ONLINE GENERATIVE-LATENT DIRECT-POLICY WAM
```

---

# 2. CLAIM → EVIDENCE → INTERPRETATION → UNPROVEN

## Claim A — video-generator internal latents are useful planning representations

**AUTHOR CLAIM**

The internal latent representation learned by the video generator provides richer planning state than conventional BEV or VLM representations.

**DIRECT PAPER EVIDENCE**

Representation ablation:

```text
BEV Features        84.1 PDMS
VLM Hidden State    86.5
Video Latents       89.1
```

Video-pretraining scale:

```text
0 samples       85.9 PDMS
76k            87.0
3.8M           87.8
7.6M           89.1
```

**SOURCE EVIDENCE**

Action blocks cross-attend the corresponding hidden state produced by each Video-DiT block rather than merely consuming a final pooled VAE representation.

**OUR INTERPRETATION**

DriveLaW provides strong evidence that a driving-video generative backbone can serve as an online planning representation and that increasing its video-pretraining exposure improves planning inside this architecture.

**REMAINS UNPROVEN**

```text
higher RGB-generation fidelity itself causes the planning gain;
video latents are universally superior to matched-capacity BEV/VLM states;
the internal latent is a calibrated physical future state.
```

---

## Claim B — generation and planning are tightly chained

**DIRECT PAPER EVIDENCE**

The paper places the Action DiT after the Video DiT and conditions action generation on video-generator latents.

**SOURCE EVIDENCE**

`transformer_ltx.py` performs, block by block:

```text
VideoBlock_i → h_video_i
ActionBlock_i(action_hidden, encoder_hidden_states=h_video_i)
```

**INTERPRETATION**

The online planner directly depends on internal Video-DiT states. This is more tightly chained than Epona's sibling visual/action branches.

**BOUNDARY**

The coupling is primarily:

```text
world/video → action
```

not:

```text
action → candidate-specific world → action evaluation.
```

---

## Claim C — planning does not require full future-video generation

**SOURCE EVIDENCE**

The released NAVSIM agent uses:

```text
return_action=True
return_video=False
```

and the pipeline computes:

```text
compute_video = i == 0 or return_video
store_buffer  = i == 0 and not return_video
```

After the first Video-DiT pass, later action solver steps reuse `video_states_buffer`.

**INTERPRETATION**

The generative backbone stays online, but full denoising and RGB rendering do not.

**BOUNDARY**

Do not call this `world model removed at inference`; that would be wrong. A substantial Video-DiT computation remains on the deployed path.

---

## Claim D — staged training avoids gradient interference

**PAPER CLAIM**

The chained/staged recipe avoids optimization conflict between high-fidelity video generation and stable trajectory planning.

**SOURCE EVIDENCE**

Released config:

```text
train_mode: action_full
return_action: true
return_video: false
```

Released training code:

```text
action_full → every diffusion-model parameter requires_grad=True
loss = action flow loss only
```

The action blocks cross-attend Video-DiT hidden states without a detach.

**OUR INTERPRETATION**

Stage 3 is not a frozen-video-backbone regime. The planner's action loss can update the Video DiT. The more precise reading of `avoid gradient interference` is:

```text
video objectives first
→ then action-only task adaptation of the chained network
```

rather than simultaneous video-loss + action-loss competition.

**REMAINS UNPROVEN**

The paper does not provide a clean frozen-vs-action-full ablation that isolates the value of backpropagating action loss into Video DiT.

---

# 3. Paper/source action-flow equation discrepancy

Paper defines:

```text
a_t = (1-t)a_0 + t epsilon
```

Therefore:

```text
da_t/dt = epsilon - a_0
```

Paper Eq. 9 nevertheless writes the target as:

```text
a_0 - epsilon
```

Official training source uses:

```text
target_vel = noise_actions - actions
           = epsilon - a_0
```

Status:

```text
PAPER EQUATION SIGN ERROR / CONVENTION AMBIGUITY
SOURCE IMPLEMENTATION RESOLVES TO epsilon - a0
```

This is kept explicitly rather than silently correcting the paper.

---

# 4. Paper/source action-step mismatch

Paper:

```text
5 action sampling steps
```

Released config / validation routine:

```text
5 steps
```

Current `VideoDriveAgent.forward_test()`:

```text
num_inference_steps=10
```

hard-coded in the pipeline call.

Status:

```text
CURRENT MAIN ≠ PAPER-DECLARED REPRODUCTION SETTING
```

The exact benchmark commit is not tagged/pinned, so the 89.1 PDMS result should remain attributed to the paper configuration, not automatically to current-main `forward_test` behavior.

---

# 5. Denoising-step ablation changes the interpretation of "world reasoning"

Paper Table 6:

```text
Video denoise step 1   89.1 PDMS
Video denoise step 5   86.9
Video denoise step 10  23.2
```

This directly rejects a monotonic-imagination story:

```text
more completed denoising
!= better planning
```

The useful planning object is an **internal generative representation**, not necessarily a high-fidelity future image.

This is one of the strongest mechanistic results in DriveLaW.

---

# 6. Counterfactual audit

Canonical DriveLaW planning does not branch the world by candidate ego actions.

```text
candidate-specific world output                NO
candidate-specific alternative-future truth    NO
reactive other-agent intervention truth         NO
intervention-response validation                NO
```

The action policy samples/refines a trajectory from one common world representation.

Therefore:

```text
generative/predictive representation
!= action-conditioned consequence model
```

---

# 7. Time-axis audit

DriveLaW contains three distinct axes:

```text
physical future time tau
video denoising / generative solver time s_video
action flow solver time s_action
```

Binding controls:

```text
10 video denoising steps != 10 physical future frames
5 action solver steps     != 5 physical trajectory timesteps
```

Existing Ontology F08 covers this distinction; no new dimension is authorized from the first pass.

---

# 8. Noise Reinjection attribution

Noise Reinjection is a video-generation mechanism targeted at high-frequency detail and structural consistency.

The audited main tables do not provide a matched planning ablation isolating:

```text
+ Noise Reinjection → planning PDMS
```

Therefore keep:

```text
video-quality contribution  PAPER-SUPPORTED
planning contribution       NOT ISOLATED
```

---

# 9. Evaluation correction

Paper wording uses `closed-loop metrics` for NAVSIM PDMS.

Project-standard classification:

```text
NAVSIM v1 = NON-REACTIVE DATA-DRIVEN / PSEUDO-SIMULATION PLANNING
```

Therefore DriveLaW does not validate reactive alternative-agent responses or intervention-valid world simulation.

---

# 10. Cross-paper scientific position

```text
LAW
future prediction → training representation shaping
future object not consumed online

Epona
shared history latent → trajectory branch + visual branch
visual future not needed by planner

WorldDrive
heavy generative prior/teacher → inherited/distilled future representation → scorer

Metis
action → video during training; video loss shapes action; video removed online

DriveLaW
Video-DiT internal generative state → action directly online;
action loss can reshape Video DiT during stage-3 adaptation
```

The closest concise distinction is:

```text
DriveLaW keeps the generative backbone itself on the deployed planning path,
but taps it early and avoids full future-video rollout.
```

---

# 11. Ontology decision

No V1.4 amendment from the first DriveLaW pass.

Candidate residue retained for future back-projection:

```text
GENERATIVE-STATE TAP LOCATION / SOLVER-DEPTH OF POLICY CONDITION
```

Reason not yet promoted:

```text
F08 + J01/J03 + N + L/M already encode most of the scientific distinction;
need another independent anchor (e.g. ReWorld or another generative-latent planner)
before deciding that tap-location deserves a stable dimension.
```

---

# 12. Final audit verdict

```text
DriveLaW
= video-generative pretraining
→ online first-pass Video-DiT block states
→ direct blockwise conditioning of Action DiT
→ action-only end-to-end task adaptation
→ direct trajectory policy

NOT:
full video rollout → visual inspection → planning
NOT:
candidate action → candidate world → utility selection
NOT:
world model removed at inference
```
