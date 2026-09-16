# Core Mechanism 12 — DA-WAM Blind-Test Result

Status: blind projection complete against the ontology frozen at `414b5756bbf2d9089a94da44f174d60ff0cb5436`.

Blind-test verdict: **PASS**.

S2 verdict after discussion: **HOLD — successful blind interpolation, insufficient for S2 promotion**.

## 1. Protocol and evidence boundary

Preregistration commit:

```text
1370d0c — Preregister DA-WAM ontology blind test
```

Frozen normative specification:

```text
outputs/core_mechanism_12_v1/09_ONTOLOGY_SPEC_S1_PLUS.md
SHA256 34c14ea6d8f7c6869f50240d968d1f070d9dfc36e5247cf113542db938a6abdf
```

Evidence read after preregistration:

- `papers/raw_md/P0012_DAWAM/P0012_DAWAM.raw.md`;
- `audits/literature/PHASE_C6_DAWAM_AUDIT.md`, used for paper/repository version and public-source availability boundary.

Deliberately not read for the blind classification:

- `landscape/P0012_DAWAM_ONTOLOGY_PROJECTION.md`;
- `landscape/WAM_COMPARISON_MATRIX_V1_3_DAWAM_EXTENSION.md`;
- `papers/deep_analysis/P0012_DAWAM_DEEP_ANALYSIS_V2.md`;
- `papers/cards/P0012_DAWAM.md`;
- `audits/literature/PHASE_B_WAVE3_DAWAM_AUDIT.md`.

The source-status audit contains a prose mechanism summary but no C–X–D–P–V–T–L assignment. The typed projection below was reconstructed from the primary method equations and the frozen specification.

## 2. Artifact boundary

### 2.1 Classified artifact

```text
DAWAM-PLAN-PAPER
paper = DA-WAM: Decision-Aligned Future Latents for Driving World Models
version = arXiv:2608.19085v2
mode = planning inference with online candidate-specific future prediction
terminal output = selected ego trajectory τ*
```

### 2.2 Code artifact

```text
official repository = LeapWM/da-wam
observed commit = 1edbe555146a2d1fe9484f5c11f120860b8a4858
public content = README only / implementation announced as forthcoming
```

No `DAWAM-PLAN-CODE` mechanism artifact is created. A repository shell without executable implementation cannot verify a deployment or learning DAG.

Consequences:

- core paper mechanism can be classified;
- exact proposal implementation, solver clock, detach edges, parameter scope, and batching remain SOURCE-UNVERIFIED;
- paper facts are not promoted to CODE FACT.

## 3. Deployment DAG

Primary paper reconstruction:

```text
X_t(current image history)
→ online V-JEPA encoder Eθ
→ Z_t(current scene tokens)

proposal module
→ {τ_i}_{i=1..N}, N=32

τ_i
→ trajectory encoder Eτ
→ a_i(action representation)

Z_t + a_i
→ shared action-conditioned predictor Pφ
→ Zhat_i(candidate-specific future endpoint latent at t+0.5s)

Z_t + a_i + Zhat_i
→ shared scoring transformer
→ qhat_i = [NC,DAC,EP,TTC,Comfort]
→ shat_i(overall utility)

argmax_i shat_i
→ τ*
```

Paper facts:

- candidate identity `i` persists from proposal through future prediction and scoring;
- each candidate receives a distinct predicted future latent;
- the future latent is a direct runtime ancestor of the candidate score;
- the EMA target encoder and factual future frame are absent at inference;
- no recurrent physical-future rollout is part of the stated method.

## 4. Learning DAG

```text
pretrained V-JEPA 2.1
→ initialize online encoder Eθ and target encoder Ebar

base online encoder weights = frozen
LoRA online parameters = trainable

Eθ -- EMA update --> Ebar
X_{t+Δ} -- Ebar + stop-gradient --> Z_target

proposal module → {τ_i}
τ_expert + {τ_i} -- nearest ADE --> i_exp

Z_t + a_i -- shared predictor --> Zhat_i, for every i

Zhat_{i_exp} + stopgrad(Z_target)
→ L_pred

all generated candidates + training-only hard negatives
→ factor targets [NC,DAC,EP,TTC,Comfort]
→ utility targets
→ pairwise preferences
→ L_factor || L_score || L_rank

L_pred || L_factor || L_score || L_rank
→ joint end-to-end paper training
→ online LoRA + predictor + scorer
→ additional proposal/trajectory-encoder gradient scope UNKNOWN without code

deploy retain{
  online encoder,
  proposal path,
  trajectory encoder,
  candidate future predictor,
  factor/utility scorer
}

deploy drop/bypass{
  EMA target encoder,
  observed future frame,
  expert matcher,
  hard-negative retrieval
}
```

Supervision boundary:

```text
expert-matched branch:
direct factual-future latent target + decision targets

other generated candidates and hard negatives:
decision/factor/utility/ranking targets
NO directly observed alternative future latent
```

Therefore the non-expert `Zhat_i` are candidate-specific predicted carriers, but their physical counterfactual fidelity is not established by observed intervention outcomes.

## 5. Frozen-ontology signature

```text
DAWAM-PLAN-PAPER@arXiv:2608.19085v2

C =
  C2_pred@B{direct}
  + C2_target@T{EMA factual target}

X =
  X(C2_pred@T)=X3
  X(C2_pred@R)=X3
  X(C2_target@T)=X∅

D = D2

P = PB{
  candidate_count=32,
  train_only_hard_negative_augmentation=yes
}

V = hierarchical_fusion(
  VD[NC,DAC,EP,TTC,Comfort]
  → VU[overall planning utility];
  provenance=external simulator/rule-based planning metrics;
  measure=factor regression + utility regression + pairwise ranking;
  final_commit=argmax predicted utility
)

T = (
  Ts=UNKNOWN,
  Tr=absent,
  Th=absent,
  Tc=absent
)

L =
  LP(V-JEPA initialization and LoRA adaptation)
  → joint(
      LA/LN(expert-matched action-conditioned future prediction
            against stopgrad EMA factual target)
      ||
      LC(all-candidate factor, utility, ranking, and hard-negative supervision)
    )
  => retain{online encoder,proposal,predictor,scorer}
     /drop{EMA target,factual-future input,expert matching,hard-negative retrieval}
```

### 5.1 Why Z_t is not separately coded C1

`Z_t` is an online encoder feature and an input to future prediction/scoring. The paper does not establish a separate structured-current-world operation or direct carrier-level world target on `Z_t` beyond its role as predictor context. Under the tightened carrier gate, encoding plus downstream use is insufficient for C1.

The qualifying runtime world carrier is `Zhat_i`: it is separately traceable, produced by an explicit action-conditioned temporal predictor, grounded by future-target/decision losses, and consumed by the resolver.

This conservative decision prevents ordinary predictive encoder features from automatically becoming C1.

### 5.2 Why C2_target has X∅ rather than X1

The EMA target encoder maps the one observed future frame directly to a factual latent. No action/control variable conditions that encoding. Expert matching later associates the target with one candidate, but association after encoding is not an incoming control edge to the target carrier.

### 5.3 Why Ts is UNKNOWN

The paper establishes an explicit proposal bank but does not provide enough executable detail to determine whether candidate generation contains a numerical diffusion/flow/edit solver. Candidate multiplicity alone is not Ts. The future predictor and scorer themselves are feed-forward in the stated method.

## 6. Type-constraint audit

| Constraint | Result | Evidence/reason |
|---|---|---|
| D2 requires runtime consequence carrier | PASS | C2_pred@R is consumed before score/argmax |
| D2 requires X3 | PASS | every τ_i indexes its own Zhat_i |
| D2 requires PB | PASS | 32 identities persist to a common scorer and argmax |
| D2 requires non-N/A V | PASS | VD factors and VU utility determine commitment |
| train-only carrier cannot support D | PASS | D2 uses C2_pred@R, not C2_target@T |
| PB requires A* | PASS | τ*=argmax_i shat_i |
| endpoint must not imply Th | PASS | one t+0.5s latent; no recurrent physical rollout |
| candidate count must not imply Ts | PASS | Ts remains UNKNOWN because proposal implementation is unavailable |
| dropped nodes absent from runtime | PASS | target encoder/future observation/expert/HN retrieval are excluded |
| UNKNOWN not converted to ∅ | PASS | proposal solver and exact gradient scope remain UNKNOWN |

No type constraint required an exception.

## 7. Nearest-signature collision tests

### 7.1 DA-WAM versus World4Drive

Shared:

```text
C2 candidate future endpoint
X3 candidate preservation
D2 candidate consequence selection
PB common resolver
```

Different:

```text
World4Drive V = VW factual-future latent agreement
DA-WAM V      = VD factors → VU planning utility

World4Drive learning = factual-future mode matching + selected reconstruction
DA-WAM learning      = expert-branch EMA prediction + all-branch metric/ranking supervision
```

Verdict: same runtime route family, different resolver and learning mechanism. Correct near-collision, not a false split.

### 7.2 DA-WAM versus WoTE

Shared:

```text
X3 + D2 + PB
explicit driving-outcome/value supervision
```

Different:

```text
DA-WAM = C2 endpoint, Th absent, VD→VU
WoTE   = C3 recurrent future horizon, Th present, VM+VD
```

Verdict: endpoint consequence scoring is correctly separated from modelled physical-horizon evaluation.

### 7.3 DA-WAM versus WorldDrive

Shared:

```text
C2 runtime future representation
X3 + D2 + PB
VU-style utility selection
LP and LC participation
```

Different:

```text
WorldDrive = heavy generative teacher → deployed surrogate (LT), teacher generator dropped
DA-WAM     = direct predictor retained online; EMA target is a stopped factual target, not a heavy consequence teacher surrogate

WorldDrive FAR = LP→joint(LT,LC)
DA-WAM          = LP→joint(LA/LN,LC)
```

Verdict: no complete collision; LT is not incorrectly assigned to an EMA target encoder.

### 7.4 Complete-signature collision

No frozen artifact has the same complete runtime plus L program.

The ontology places DA-WAM inside the existing candidate-consequence family without collapsing its decision-target and learning-edge differences.

## 8. Implementation-invariance test

The following replacements leave the signature unchanged if semantic interfaces and causal paths are preserved:

- V-JEPA tokens → BEV or another latent endpoint representation;
- transformer predictor → MLP, diffusion, or flow predictor producing the same one-step candidate endpoint;
- LoRA → another parameter-efficient adaptation method with the same directed learning edges;
- 32 → another candidate count while retaining PB;
- MSE/BCE → another measure targeting the same VD/VU semantics.

The following changes would correctly change the signature:

- shared one-future representation replacing per-candidate futures: X3/D2 route changes;
- dropping the future predictor at deployment: remove C2_pred@R and D2;
- recurrent multi-step future prediction: C2→C3 and Th becomes present;
- replacing utility supervision with factual-future mode matching: VU/VD→VW;
- distilling a heavy teacher into the runtime predictor: add LT and surrogate realization.

Result: PASS.

## 9. Missing-category test

New top-level axis required: **NO**.

New category required within an existing axis: **NO**.

Paper-specific exception required: **NO**.

The only unresolved values use existing epistemic grammar:

- Ts=UNKNOWN;
- exact gradient reach into proposal/trajectory encoder=UNKNOWN;
- source implementation details=UNKNOWN.

Hard-negative supervision is represented inside LC target provenance and training-only P attributes. It does not require a new runtime route, carrier type, or resolver atom.

## 10. Reconstruction test

Given only the signature plus canonical L program, an independent reader can reconstruct:

```text
runtime:
candidate bank
→ one predicted endpoint latent per candidate
→ factorized driving outcomes and holistic utility
→ common argmax

training:
pretrained predictive encoder adaptation
→ one stopped factual future target for the expert-matched branch
→ metric/ranking supervision for all branches
→ target/future/HN machinery removed at deployment
```

The reconstruction does not claim:

- observed counterfactual future truth for unexecuted candidates;
- reactive surrounding-agent responses;
- exact code-level detach scope;
- a known proposal solver.

Result: PASS.

## 11. Blind-test verdict

All preregistered PASS conditions are satisfied:

- frozen specification was not edited;
- no new axis or category was introduced;
- all fields use legal values;
- the core DAG is reconstructible;
- type constraints pass;
- nearest artifacts produce meaningful causal near-collisions;
- implementation changes do not create artificial categories.

Final blind-test verdict:

```text
PASS
```

## 12. S2 discussion and decision

The PASS strengthens the claim that C–X–D–P–V–T–L generalizes beyond its 12-paper derivation set. It specifically validates an unseen combination:

```text
direct retained candidate endpoint carrier
+ decomposed driving factors
+ holistic utility
+ EMA factual target on only the expert-matched branch
+ all-branch decision supervision
```

However, promotion to S2 is held for four reasons:

1. DA-WAM is a paper-only test because executable code has not been released.
2. It is a demanding but still interpolative test inside the already populated D2/PB candidate-consequence family.
3. SEER-PAPER and GW-PLAN retain unresolved final commitment, and four derivation papers remain source-unverified.
4. The assignment has not yet been reproduced by an independent reader who sees only the normative specification and primary evidence.

Decision:

```text
S1+ = strengthened and blind-test-supported
S2 discussion = now permitted
S2 promotion = HOLD
```

The next promotion-quality test should use a source-available artifact outside the D2/PB cluster—preferably reciprocal D3, joint D4, or a difficult current-world D1 case—and should be classified independently from this review.
