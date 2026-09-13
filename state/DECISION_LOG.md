# DECISION_LOG

Newest entry first.

---

## 2026-09-13 — Planning-centric scope + problem-first rule + targeted corpus freeze

**Decision**

1. Research identity is fixed as:

```text
World Model + End-to-End + Planning-centric autonomous driving
```

2. Risk field / predictive risk field is **not** a required destination. The owner's prior risk/safety expertise is optional prior knowledge, to be used only if a surviving planning problem genuinely benefits from it.
3. Every paper must be evaluated symmetrically: strongest evidence, strongest limitation, what it proves, what it does not prove, observed failure vs our inference, prior-art pressure, residual question.
4. Broad corpus expansion is paused. Add only the frozen targeted set in `state/TARGETED_READING_QUEUE.md`: five direct P2-R papers plus three historical interactive-planning controls, then stop and adjudicate.
5. No method design before this gate closes.

**Why**

The active risk is no longer lack of papers; it is path dependence and premature solution design. Existing Batch 0A evidence already shows that broad architectural claims are heavily occupied. The next papers must therefore have high discrimination value for the narrow P2-R question rather than merely share WAM/risk keywords.

A second risk is confirmation bias: papers that resemble our ideas must not be treated more harshly, and papers that support our hypothesis must not be treated more generously. Scientific review must preserve both strengths and weaknesses.

**What would reverse this decision**

- Broader expansion becomes justified only when a specific unresolved scientific question identifies a missing paper family.
- Risk-field machinery becomes central only if a validated planning failure yields a missing capability for which that machinery offers a defensible advantage.

Canonical rules: `state/RESEARCH_PRINCIPLES.md`.

---

## 2026-09-13 — P2-R Round-1 adjudication: survives as question, not confirmed gap

**Decision**

```text
P2-R SURVIVES ROUND 1 AS A QUESTION, NOT AS A CONFIRMED GAP.
```

No method design is authorized.

**Why**

The existing repo corpus is sufficient to show that several broad formulations are already occupied:

- interaction-aware planning;
- reactive / closed-loop evaluation;
- ego-action-conditioned world modeling;
- candidate-specific future prediction;
- future-conditioned candidate scoring.

SafeDrive, BeTop and especially DA-WAM directly occupy these broad directions.

However, the reviewed papers do not directly measure the narrower quantity:

```text
P[ rank_factual/nonreactive(A) != rank_reactive(A)
   | fixed state, fixed candidate set, interaction-critical regime ]
```

with the difference causally attributable to surrounding-agent response to ego intervention.

**Evidence reviewed**

- P0002 SafeDrive
- P0004 BeTop
- P0003 GraphAD
- P0005 RiskWorld
- P0012 DA-WAM

Full audit:

`audits/literature/P2R_TARGETED_FAILURE_DEEP_READ_ROUND1.md`

**Strongest counterevidence / prior-art pressure**

- DA-WAM already predicts a separate future latent for every candidate and scores that candidate using its corresponding future.
- SafeDrive already constructs candidate-conditioned sparse worlds and performs safety-based candidate selection.
- BeTop already demonstrates interaction-aware planning under reactive closed-loop evaluation.

Therefore any future P2-R contribution that collapses to "make the model action-conditioned/reactive" is not novel enough.

**What would reverse / kill this decision**

Kill P2-R rather than widen it if direct literature or a minimal controlled test shows any of the following:

1. matched-state / matched-candidate factual-vs-reactive ordering is already directly measured and substantially solved;
2. ordering inversions are rare or cause negligible planning regret;
3. apparent inversions are mostly caused by observation shift, control error, temporal compounding, or candidate-set change rather than surrounding-agent response;
4. current candidate-conditioned methods already preserve reactive ordering under a direct controlled evaluation;
5. the only remaining contribution is a new name / metric for an already-established interactive-planning phenomenon.

**Next gate**

Direct literature attack: BridgeSim, ReactSim-Bench, CausalDrive, How Can Driving World Models Do Counterfactual Prediction?, CRAFT, plus historical controls GameFormer, M2I, and Bahram et al. 2016.

---

## 2026-09-13 — Scientific workflow takeover

**Decision**

The private GitHub repo becomes the canonical cross-session Research Brain.

- GPT-5.6 Sol handles scientific deep reading, adversarial review, hypothesis adjudication, evidence synthesis, paper-card scientific content and direct repo state updates.
- The local corpus agent handles acquisition, MinerU conversion, metadata/QC, local-PDF source extraction, source-code execution, datasets/checkpoints and experiments.

**Why**

The GitHub connector has been verified to read the private repo, its state files and full raw Markdown papers directly. This removes the need for each new chat to reload long conversation history.

**Boundary**

Canonical PDFs remain local/NAS only. GitHub stores raw Markdown, figures, research cards, audits, hypothesis state, manifests and decisions.

---

## 2026-09-13 — Hypothesis status reset (P1 retired, P2R primary, P3 hold)

**Decision**

- P1_RETIRED — Planner-Induced Model Exploitation / Search-Support Gap: `RETIRED AS MAIN PROBLEM`
- P2R_PRIMARY — Reactive Action-Ordering Gap in Planning-centric WAMs: `PRIMARY CANDIDATE, NOT CONFIRMED GAP`
- P3_HOLD — Decision Sufficiency of World Representations: `HOLD AS BACKUP`

**Rationale**

- P1: real failure mode but low WAM specificity; scorer/reward optimization and mitigation space are already heavily occupied, and source audit weakened the chain from optimizer exploit to deployed-planner failure.
- P3: highly WAM-native but its broad "planning-oriented rather than reconstruction-oriented representation" framing is under strong 2025–2026 prior-art pressure.
- P2-R: the narrowed matched-action, reaction-induced ordering question survived the prior-art attack and has clean falsification criteria, but is not yet a confirmed gap.

**What would reverse this decision**

P2-R should be killed if direct evidence does not establish a distinct action-ordering failure attributable to reactive other-agent responses. In that case, returning `NONE` is preferred over protecting the candidate by widening its definition.

---

## 2026-09-13 — Long-term architecture ruling (PDF locality, text layers, hash authority)

**Decision**

1. Canonical PDFs stored only on local/NAS; never uploaded to ChatGPT Library or GitHub.
2. GPT-readable primary-text layer = MinerU raw Markdown.
3. Raw MD may live in the GitHub private repo as the cross-session full-text layer.
4. ChatGPT Library = optional convenience copy of raw MD, never a system dependency.
5. `pdf_sha256` = SHA256 over logical document bytes from the canonical Python corpus I/O path.
6. Windows native/.NET +1024 framed file view = `KNOWN_HOST_QUIRK`; no further investigation.
7. Insufficient raw MD (exact wording, complex formulas, figures) → on-demand source extract from the local canonical PDF.
8. Corpus agent = source/infrastructure worker; scientific judgement is maintained in the Research Brain by GPT-5.6 Sol + owner.

**Why**

This establishes which artifacts may cross which boundary and fixes a reproducible content-hash basis despite the host's API-dependent file framing.
