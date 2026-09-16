# Core Mechanism 12 — First-Six Human Review Verdict

Status: independent human-gate review completed against the tracked paper text and source-audit records.

Reviewed commit: `a6a197166cd48c51648e630ebb479f0bed483415`

Review scope:

- 21-artifact projection and collision claims;
- all 70 C–X–D–P–V–T–L cells for the first six papers, represented by ten version/mode artifacts;
- the underlying paper/source evidence for every disputed field;
- consistency between the Phase 1 DAG, compact signature, detailed projection, and reviewer worksheet.

## 1. Gate verdict

The submitted Phase 3 commit does **not** pass the human gate unchanged.

Mechanical completeness is valid:

- 21/21 detailed artifact projections exist;
- the compact matrix has 21 rows;
- the first-six worksheet has 10 artifacts and 70 field rows;
- the requested collision, lifecycle, candidate, invariance, hybrid-objective, version/mode, completeness, and anti-marketing attacks are present.

Scientific acceptance required fifteen first-six field/encoding corrections and one cross-corpus UNKNOWN type correction. Those corrections are now applied in the working tree.

Rating:

```text
a6a1971 as submitted     = HOLD AT S1
corrected working tree  = provisional S1+
S2                      = NOT JUSTIFIED
```

## 2. Blocking findings and corrections

### F1 — World4Drive resolver semantics were inverted

Submitted projection:

```text
V = VM
candidate trajectory vs factual trajectory
nearest geometric match creates j
```

Primary evidence instead states:

```text
j = argmin_k ||F{k} - F_hat||²
ScoreNet is trained against j
```

The resolver label is therefore produced by candidate-future versus factual-future latent agreement. The separate L1 loss on `T{j}` shapes the selected proposal but does not create ScoreNet's class label.

Corrected projection:

```text
V = VW
compared objects = predicted candidate future latent, factual future latent
measure = latent MSE
target class = j
```

Evidence:

- `papers/raw_md/P0046_World4Drive/P0046_World4Drive.raw.md`, World Model Selector;
- `audits/literature/PHASE_C5_WORLD4DRIVE_AUDIT.md`, §4.

Impact: changes a core field and the W4D/WorldDrive/WoTE collision explanation.

### F2 — WorldDrive learning was neither complete nor correctly ordered

Submitted projection:

```text
L = LT→LC
```

This loses the paper's representation-inheritance path and incorrectly serializes FAR's two complementary losses.

Evidence supports:

```text
TA-DWM pretraining
→ transfer/freeze visual and motion encoders into planner
→ planner training
→ FAR joint training {
     future-latent alignment LT
     || PDMS preference ranking LC
   }
→ retain encoders/planner/surrogate/reward
→ drop heavy generator
```

Corrected family:

```text
LP→joint(LT,LC)
```

Evidence:

- `papers/raw_md/P0042_WorldDrive/P0042_WorldDrive.raw.md`, §§3.2–3.4 and training details;
- `audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md`, §§3, 5, 7.

Impact: changes the canonical learning DAG and prevents reconstruction from omitting one of WorldDrive's two central mechanisms.

### F3 — Multi-carrier X syntax violated its own binding rule

The Phase 3 text correctly required `X(carrier@lifecycle)=value`, but the matrix used lifecycle-only values for artifacts whose current and future carriers share the same lifecycle.

For example, this was ambiguous:

```text
C = C1@B + C2@B
X = @T:X3; @R:X3
```

It can falsely imply that the current world carrier is candidate-indexed. Correct forms include:

```text
W4D: X(C1@B)=N/A; X(C2@B)=X3
WoTE: X(C1@B)=N/A; X(C3@B)=X3
```

The same carrier binding was applied to SeerDrive and GraphWorld projections.

For a `@B` carrier, both lifecycle edges must be explicit even when the value is unchanged. DriveLaW therefore records `X(C4@T)=X∅` and `X(C4@R)=X∅` rather than only the runtime half.

Impact: notation/reconstruction defect, not a change to the underlying paper mechanism.

### F4 — PU and VX conflated two different unknowns

`VX` means:

```text
a resolver is known to exist, but its semantic criterion is unknown
```

When `P=PU`, resolver applicability may itself be unresolved. In that case `VX` is too strong and `N/A` is also unjustified.

Correct rule:

```text
P=PU and resolver applicability unresolved  → V=UNKNOWN
known resolver, unknown criterion           → V=VX
resolver ruled out by task/topology         → V=N/A
```

This correction applies to SEER-PAPER and GW-PLAN.

Impact: restores the required separation of absence, inapplicability, and insufficient evidence.

### F5 — Epona's chain-of-forward training carrier was omitted from mode signatures

The shared Epona learning DAG already records periodic multi-forward training in which predicted visual latents and predicted trajectories are detached and reused as the next context. That sequence passes the carrier gate during training because it is a traceable generated horizon that conditions later losses.

The submitted mode records were incomplete:

- EPO-PLAN recorded only C2@T/X1/LS even though its trained checkpoint includes the chain curriculum;
- EPO-SELF recorded C3 only at runtime, omitting C3@T;
- EPO-CTRL omitted the same shared chain curriculum.

Corrected distinction:

```text
base visual training                 = C2@T, X1 factual motion
chain-of-forward training            = C3@T, X2 predicted detached motion/context
self-generated runtime rollout       = C3@R, X2 predicted motion
externally controlled runtime rollout = C3@R, X1 supplied motion
```

Impact: changes C/X/L fields but preserves the deployment conclusions D∅ for planning and D5 for generation modes.

### F6 — WorldDrive X changed within the training lifecycle

The teacher carrier is controlled differently by stage:

```text
TA-DWM pretraining = factual/conditioned trajectory, X1
FAR target generation = candidate k, X3
runtime surrogate = candidate k, X3
```

Therefore `X(C2@T)=X3` was too coarse. X binding must accept a stage qualifier when one lifecycle contains multiple incoming control edges.

Impact: expands the binding grammar; no new X category is needed.

### F7 — No consolidated post-Phase-3 normative specification existed

`02_ONTOLOGY_SPEC.md` is explicitly a Phase 2 candidate and still contains the superseded P2/P3/P4, VG/VC, old T grammar, and old stability ceiling. Files 03–05 described revisions but did not provide one executable current specification.

Correction:

- preserve `02_ONTOLOGY_SPEC.md` as historical Phase 2 evidence;
- add `09_ONTOLOGY_SPEC_S1_PLUS.md` as the only normative post-review specification.

Impact: prevents two incompatible grammars from being used to classify the next paper.

## 3. First-six 70-cell result

The table reports the submitted worksheet after evidence review. “REVISE” includes a semantically correct idea whose compact encoding was not valid under the stated grammar.

| Artifact | C | X | D | P | V | T | L | Result |
|---|---|---|---|---|---|---|---|---|
| LAW-PF | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT | 7/7 |
| LAW-PB | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT | 7/7 with stated UNKNOWN boundaries |
| EPO-PLAN | REVISE add C3@T chain | REVISE bind base/chain | ACCEPT | ACCEPT | ACCEPT | ACCEPT | REVISE add chain curriculum | 4 accept + 3 revise |
| EPO-SELF | REVISE C3@R→C3@B | REVISE split base/chain/runtime | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT | 5 accept + 2 revise |
| EPO-CTRL | REVISE add C3@T chain | REVISE split base/chain/runtime | ACCEPT | ACCEPT | ACCEPT | ACCEPT | REVISE add chain curriculum | 4 accept + 3 revise |
| DLAW-PAPER | ACCEPT | REVISE add train lifecycle binding | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT | 6 accept + 1 revise |
| DLAW-CODE | ACCEPT | REVISE add train lifecycle binding | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT | 6 accept + 1 revise |
| W4D-PLAN | ACCEPT | REVISE binding | ACCEPT | ACCEPT | REVISE VM→VW | ACCEPT | ACCEPT after label wording fix | 5 accept + 2 revise |
| WD-PLAN | ACCEPT | REVISE split pretrain/FAR/runtime | ACCEPT | ACCEPT | ACCEPT | ACCEPT | REVISE LT→LC to LP→joint(LT,LC) | 5 accept + 2 revise |
| WOTE-PLAN | ACCEPT | REVISE binding | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT | 6 accept + 1 revise |

Totals:

```text
ACCEPT = 55
REVISE = 15
UNKNOWN / NEED EVIDENCE as a field decision = 0
```

The accepted LAW-PB rows retain explicit internal UNKNOWN attributes; accepting the row means the category and its uncertainty boundary are correct, not that missing evidence has been invented.

## 4. Pairwise human decisions

### LAW versus Epona planning

Decision: ACCEPT SPLIT.

- deployment is world-carrier-free for both planning paths;
- LAW uses predicted-action-mediated future supervision (LA);
- Epona's base visual branch uses factual motion and sibling shared-state learning (LS), augmented by detached chain-of-forward training;
- Epona additionally has a runtime action solver clock.

They are close at deployment but not core-mechanism-equivalent.

### LAW/Epona versus DriveLaW

Decision: ACCEPT SPLIT.

DriveLaW retains an online future-generative internal carrier that conditions Action DiT. LAW and Epona planning do not consume a future carrier online.

### World4Drive versus WorldDrive versus WoTE

Decision: ACCEPT THREE-WAY SPLIT after correction.

Shared trunk:

```text
candidate bank
→ candidate-indexed consequence
→ learned resolver
→ A*
```

Separating mechanisms:

```text
World4Drive = endpoint latent + factual-future world agreement (VW)
WorldDrive  = distilled endpoint surrogate + planning utility preference (VU)
WoTE        = recurrent horizon rollout + imitation and decomposed driving outcomes (VM+VD)
```

## 5. Stability decision

The seven questions C–X–D–P–V–T–L survive the human attack. The discovered failures were errors inside field values, binding grammar, and learning-stage reconstruction; none proves that an entire axis should be deleted or merged.

S1+ is acceptable only for the corrected specification because:

- all 21 artifacts remain representable without paper-specific categories;
- the first-six human gate now closes against primary/source evidence;
- implementation substitutions remain invariant;
- training-only futures are not leaked into runtime routes;
- candidate banks require identity preservation and a common resolver;
- full learning programs retain stage order, parallel losses, gradients, and retain/drop boundaries.

S2 remains blocked by:

- unresolved SEER-PAPER and GW-PLAN final commitment;
- unavailable executable source for Metis, DynFlowDrive, Discrete-WAM, and GraphWorld;
- unresolved detach/gradient edges listed in `07_UNRESOLVED_EVIDENCE.md`;
- absence of a blind external-paper classification test by an independent reader.

## 6. Human sign-off

| Review item | Result |
|---|---|
| All ten paper/version/mode artifacts reviewed | YES |
| Every accepted ∅ has positive topology evidence | YES within the stated artifact boundaries |
| UNKNOWN was not silently converted to ∅ | YES after F4 correction |
| N/A follows task/mode type constraints | YES |
| Carrier gate rejects ordinary perception state | YES |
| PB always reaches a common resolver | YES |
| Learning programs preserve ordering/parallelism and retain/drop | YES after F2 correction |
| Phase 3 rating | corrected tree: provisional S1+; submitted commit: hold at S1 |

Reviewer: Codex independent review

Date: 2026-09-16
