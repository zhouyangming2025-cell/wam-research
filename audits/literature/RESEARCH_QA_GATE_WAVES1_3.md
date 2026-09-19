# RESEARCH_QA_GATE_WAVES1_3 — Evidence Reliability Register

Last updated: 2026-09-14

Status: **HISTORICAL QA REGISTER — retain evidence boundaries; any remaining PDF checks are conditional on reusing the claim.**

Purpose: prevent field-level conclusions from silently upgrading paper language, OCR-derived tables, proxy metrics, or our inference into hard facts.

This gate runs **before Wave 4**.

---

## 1. Evidence-status vocabulary

```text
CODE VERIFIED
= source implementation directly resolves the mechanism/path.

PDF VERIFIED
= official/venue/canonical PDF directly checked for the claim.

PRIMARY-TEXT VERIFIED
= paper raw text / trusted primary-text derivative directly checked;
  no known ambiguity for the claim, but exact visual/table details may still merit PDF confirmation.

SYSTEM-EVIDENCE ONLY
= result is valid at system level but causal attribution to one module is not isolated.

OUR INFERENCE
= cross-paper interpretation consistent with evidence but not directly reported by one paper.

NEEDS PDF VERIFY
= important claim currently rests on a table/figure/OCR-sensitive detail that should be checked from canonical PDF before becoming a final field-level citation.

NEEDS CODE VERIFY
= paper formulation leaves deployment/source-path ambiguity that matters scientifically.
```

---

## 2. Wave-1 core claims

| ID | claim | current status | QA verdict |
|---|---|---|---|
| W1-01 | M2I explicitly conditions reactor prediction on influencer future trajectory | PRIMARY-TEXT VERIFIED | stable historical fact |
| W1-02 | M2I GT-influencer future improves reactor mAP while one predicted influencer future can underperform marginal prediction | PRIMARY-TEXT VERIFIED | strong matched mechanism evidence; exact table can be PDF-checked later if cited numerically |
| W1-03 | M2I conditional response is not equivalent to identified intervention/causality | OUR INFERENCE | valid boundary; do not call M2I causal counterfactual simulation |
| W1-04 | GameFormer raw planning gain is much smaller than the gain from downstream cost-based refinement in the selected WOMD experiment | PRIMARY-TEXT VERIFIED | strong decomposition; exact percentages should remain tied to that protocol |
| W1-05 | What Truly Matters shows static prediction quality can disagree strongly with driving performance and runtime matters | PRIMARY-TEXT VERIFIED | stable field-level evidence |
| W1-06 | UniAD planning path combines future interaction representation, collision loss and occupancy-based post-optimization | PRIMARY-TEXT VERIFIED | stable architecture fact |
| W1-07 | UniAD safety improvements can coincide with worse L2 imitation error | PRIMARY-TEXT VERIFIED | stable counterexample to `lower L2 = better planning` |
| W1-08 | NAVSIM is non-reactive pseudo-simulation; other-agent future does not respond to ego action | PRIMARY-TEXT VERIFIED | stable benchmark fact |
| W1-09 | DiffusionDrive is a strong non-WM control for multimodal action generation | PRIMARY-TEXT VERIFIED | stable field-control role |
| W1-10 | DriveSuprim demonstrates large headroom from candidate ranking alone | PRIMARY-TEXT VERIFIED | stable field-control role; exact oracle table should remain protocol-scoped |

Wave-1 QA summary:

```text
NO blocking contradiction found.
Main risk = numeric over-comparison across benchmark/backbone variants, already controlled by comparability audit.
```

---

## 3. Wave-2 core claims

| ID | claim | current status | QA verdict |
|---|---|---|---|
| W2-01 | GAIA-1 demonstrates controllable generation but no operational planning loop/benchmark in the reviewed paper | PRIMARY-TEXT VERIFIED | stable |
| W2-02 | Drive-WM uses candidate command → generated future video → detector/map reward → candidate selection | PRIMARY-TEXT VERIFIED | stable architecture fact |
| W2-03 | Drive-WM does not cleanly isolate better visual-generation fidelity → better planning | SYSTEM-EVIDENCE ONLY | stable attribution boundary |
| W2-04 | OccWorld higher-resolution tokenizer reconstructs better but forecasts/plans worse | NEEDS PDF VERIFY | scientifically important counterexample; exact cells should be checked from canonical PDF before final cross-field citation |
| W2-05 | OccWorld temporal/spatial dynamics ablations degrade forecasting and planning | NEEDS PDF VERIFY | likely stable; exact table/protocol must be PDF-confirmed |
| W2-06 | WoTE future-state-on/off ablation separates scorer-only gain from additional future-state gain | PRIMARY-TEXT VERIFIED | strong matched evidence; exact 81.0/83.2/85.6 table should receive PDF spot-check |
| W2-07 | WoTE target-generation path scores alternative ego candidates against one cached logged/GT surrounding-agent future | **CODE VERIFIED** | high-confidence source fact |
| W2-08 | ViDAR transfers pretrained history/BEV encoder; future decoder is not deployed planner interface | PRIMARY-TEXT VERIFIED | stable; code not currently necessary |
| W2-09 | ViDAR predictive pretraining benefit is entangled with latent-rendering/LiDAR-geometric supervision | OUR INFERENCE | valid attribution boundary |
| W2-10 | LAW future latent is computed after current waypoint and discarded by test-time planning path | **CODE VERIFIED** | high-confidence source fact |
| W2-11 | LAW future-latent training improves planning within matched model family | PRIMARY-TEXT VERIFIED | stable, but exact ablation table merits PDF spot-check |
| W2-12 | LAW longer future target is non-monotonic; 1.5 s outperforms 3 s/10 s in shown experiment | NEEDS PDF VERIFY | important field-level counterexample; verify canonical table before final synthesis |

Wave-2 QA summary:

```text
Mechanism classification is strong.
Highest-priority PDF checks = OccWorld quantitative counterexample + LAW horizon/ablation + WoTE future-state table.
```

---

## 4. Wave-3 core claims

| ID | claim | current status | QA verdict |
|---|---|---|---|
| W3-01 | Epona uses one shared historical latent with separate trajectory and visual diffusion heads | PRIMARY-TEXT VERIFIED | stable |
| W3-02 | Epona visual generator can be disabled for planning; generated visual future is not required for current trajectory selection | PRIMARY-TEXT VERIFIED | stable paper-level architecture fact |
| W3-03 | Epona joint visual+trajectory training improves planning over trajectory-only training | NEEDS PDF VERIFY | critical evidence; raw Markdown stores key table as image |
| W3-04 | DrivingGPT interleaves discrete image and framewise action tokens in one causal sequence | PRIMARY-TEXT VERIFIED | stable |
| W3-05 | exact optimized DrivingGPT planning decode path / whether visual-token generation is bypassed at deployment | **NEEDS CODE VERIFY** | do not overstate until source path is audited |
| W3-06 | DriveLaW feeds an internal Video-DiT representation directly to Action DiT rather than requiring decoded RGB | PRIMARY-TEXT VERIFIED | stable mechanism classification |
| W3-07 | DriveLaW planning quality changes strongly with video-pretraining scale / representation / denoising state | NEEDS PDF VERIFY | exact tables are field-level evidence and deserve canonical check |
| W3-08 | Auto-JEPA target is future ego-trajectory latent, not future surrounding-world reconstruction | PRIMARY-TEXT VERIFIED | stable |
| W3-09 | Auto-JEPA uses predicted intent as retrieval key, then scorer/gate select final trajectory | PRIMARY-TEXT VERIFIED | stable online interface |
| W3-10 | Auto-JEPA strong result depends materially on memory coverage/candidate ranking, not intent prediction alone | PRIMARY-TEXT VERIFIED | supported by component/K ablations |
| W3-11 | Auto-JEPA dynamic-agent occlusion causes 2.97× mean intent change vs matched random masks | NEEDS PDF VERIFY | useful evidence; check canonical table/analysis if used as final field claim |
| W3-12 | DA-WAM predicts one future latent per candidate and consumes it in candidate scoring | PRIMARY-TEXT VERIFIED | stable architecture fact |
| W3-13 | DA-WAM direct observed-future latent supervision is applied only to expert-matched candidate | PRIMARY-TEXT VERIFIED | high-confidence method fact |
| W3-14 | DA-WAM no-future 93.31 → action-conditioned future 93.46 → + hard negatives 93.68; shared future 92.81 | NEEDS PDF VERIFY | central attribution table; must be canonical-PDF checked before final synthesis |
| W3-15 | Think2Drive learns Dreamer-style latent transition/reward/termination and trains actor/critic in imagined rollouts | **PDF VERIFIED** | official ECCV 2024 PDF checked |
| W3-16 | Think2Drive uses privileged BEV/structured simulator state rather than raw-sensor end-to-end input | **PDF VERIFIED** | official ECCV 2024 PDF checked |
| W3-17 | Think2Drive CARLA-v2 official test reports PPO 0.7 DS / 1.0% RC vs Think2Drive 56.8 DS / 98.6% RC | **PDF VERIFIED** | official ECCV 2024 PDF checked |
| W3-18 | Think2Drive multi-step WM imagination is primarily a training mechanism; deployed actor acts from inferred latent state rather than documented online candidate search | PDF VERIFIED + OUR INFERENCE | supported by method formulation; runtime source graph not code-audited |

Wave-3 QA summary:

```text
Six-interface taxonomy is stable.
Main unresolved source-path issue = DrivingGPT optimized planning decode.
Main numeric PDF checks = Epona / DriveLaW / Auto-JEPA / DA-WAM.
```

---

## 5. Cross-wave field claims and their status

### F-01 — `world prediction accuracy != planning evidence`

Status: **STRONGLY SUPPORTED**.

Independent support:

```text
What Truly Matters
OccWorld representation counterexample
Drive-WM attribution limits
non-WM action/scoring controls
```

This is a field-understanding statement, not a universal theorem.

### F-02 — `future information is not automatically beneficial`

Status: **SUPPORTED, pending PDF hardening for some quantitative examples**.

Current examples:

```text
M2I wrong conditional future can hurt
OccWorld better reconstruction can plan worse
LAW too-long target can hurt
DA-WAM shared future can underperform no future
DriveLaW wrong internal denoising state can collapse planner quality
```

The pattern is credible; several numeric anchor points remain on the PDF queue.

### F-03 — `candidate-specific output != candidate-specific oracle supervision`

Status: **STRONGLY SUPPORTED**.

Direct support:

```text
WoTE code audit
DA-WAM explicit expert-matched future supervision formulation
```

### F-04 — `WM-assisted planning != online model-based planning`

Status: **STRONGLY SUPPORTED**.

Directly separated by:

```text
ViDAR / LAW     = training representation shaping
DriveLaW        = online WM hidden state
WoTE / DA-WAM   = online candidate future evaluator
Think2Drive     = WM imagination for policy training
```

### F-05 — `architectural coupling strength != causal evidence strength`

Status: **SUPPORTED / OUR CROSS-PAPER INFERENCE**.

DrivingGPT is architecturally maximally unified but lacks a clean action-only-vs-world+action matched control in the reviewed evidence; DA-WAM has a very explicit action→future→score chain but a small matched future gain over a strong no-future planner.

### F-06 — `decision relevance and world completeness are different objectives`

Status: **SUPPORTED, not yet a universal principle**.

Evidence cluster:

```text
OccWorld reconstruction-vs-planning counterexample
LAW horizon result
DriveLaW representation-state sensitivity
Auto-JEPA future-ego-intent design and occlusion analysis
```

This should remain a field tension until Wave 4 and QA hardening are complete.

---

## 6. Current QA blockers before Wave 4

The evidence base is strong enough to close Wave 3, but not yet clean enough to skip verification.

Required targeted checks:

```text
1. Epona: exact joint-vs-traj-only ablation from canonical PDF.
2. OccWorld: tokenizer + spatial/temporal ablation tables and † metric footnote.
3. WoTE: future-state-on/off matched table from canonical PDF.
4. LAW: action-aware/no-WM and horizon tables from canonical PDF.
5. DriveLaW: video-pretraining / representation / denoising-step tables; Stage-3 freeze semantics if available.
6. Auto-JEPA: component/K/occlusion tables from canonical public source if available.
7. DA-WAM: future-configuration table + expert-matched future-loss wording from canonical public source if available.
8. DrivingGPT: source-code/runtime decode audit only if public implementation can resolve the deployment ambiguity.
```

None of these requires the user to upload a PDF unless the public/canonical source is unavailable.

---

## 7. Gate rule

Wave 4 begins only after the high-priority items above are either:

```text
VERIFIED
or
explicitly marked UNRESOLVED with no further lawful/public source available.
```

The purpose is not to obtain perfect certainty. It is to prevent fragile details from becoming the foundation of later problem discovery.

Still forbidden during QA:

```text
no gap declaration
no method design
no broad corpus expansion
no hypothesis rescue
```