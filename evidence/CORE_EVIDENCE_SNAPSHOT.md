# CORE_EVIDENCE_SNAPSHOT

Purpose: compact cross-session memory of the strongest paper-level findings that materially shaped P1/P2-R/P3. This is **not** a substitute for the canonical deep analyses, source audits, or primary-text re-reading.

Last updated: 2026-09-13

Evidence status labels:

- `REPO_REVERIFIED` — re-read from raw MD in the current Research Brain takeover.
- `LEGACY_DEEP_READ` — carried over from prior scientific deep reads; preserve as research provenance, but re-open primary text before using a fine-grained number/claim in a publication or final hypothesis verdict.
- `SOURCE_AUDIT` — based on prior source-code audit, not only paper text.

## Compact matrix

| paper | status | strongest useful evidence | strongest limitation / counterevidence | current research effect |
|---|---|---|---|---|
| **Epona** | LEGACY_DEEP_READ + raw MD available | Unified autoregressive diffusion WM with trajectory planning; important planning-centric WAM anchor. | Strong world/video capability does not by itself prove reactive counterfactual correctness or decision sufficiency. | General/P3 landscape anchor, not direct P2-R evidence. |
| **SafeDrive** | REPO_REVERIFIED | Candidate-conditioned Sparse Worlds; SWNet jointly refines ego/agent futures; FRNet uses pair-wise collision and time-wise drivable-area reasoning; closed-loop Bench2Drive evaluation. | Candidate-conditioned interaction is not the same as matched intervention-response correctness; no direct fixed-candidate factual-vs-reactive ordering test. | Strong neighbor; kills broad novelty claims around candidate-conditioned interaction/safety scoring. |
| **GraphAD** | REPO_REVERIFIED | Explicit future-trajectory interaction graph improves motion/planning; future geometry affects interaction edges. | Final planning uses a planning head; occupancy post-optimization contributes heavily to collision reduction; no reactive matched-action test. | Background interaction evidence, not direct P2-R. |
| **BeTop** | REPO_REVERIFIED | Explicit future behavioral topology; joint prediction/planning; evaluates OL, closed-loop non-reactive and reactive regimes; strong interactive planning results. | Reactive performance does not isolate fixed-state/fixed-candidate action-order reversal caused by agent response. | Strong counterexample to generic "reactivity missing" framing. |
| **RiskWorld** | REPO_REVERIFIED | Object-centric latent rollout of future ego-object relations can preserve planning-relevant risk information without full-scene reconstruction. | History-only risk monitor; no candidate ego action input; not a closed-loop planner. | Shows relation-aware future modeling ≠ counterfactual planning. Useful boundary, not P2-R proof. |
| **Gen-Drive** | LEGACY_DEEP_READ | Learned reward + RL can convert generated/world knowledge into planning improvements. | Longer optimization/fine-tuning can degrade performance; reward exploitation remains plausible. | Weakens universal claim that learned reward cannot provide planning value; historical P1 evidence only. |
| **DriveReward** | LEGACY_DEEP_READ | Candidate-conditioned learned reward exposes candidate-ranking as a concrete bottleneck; oracle candidate selection can outperform learned selector. | Ranking error may be ordinary evaluator accuracy/calibration rather than a structural need for explicit risk fields. | Weakens any jump from "ranking imperfect" to a specific risk architecture. |
| **NPPC** | LEGACY_DEEP_READ; current PDF unavailable | Continuous learned planning cost + candidate sampling/refinement provides strong explicit value interface; optimization can improve plans. | Strong counterexample to universal "learned model optimization inevitably exploits errors" claim. | Important reason P1 was retired as main. Reverify if lawful PDF becomes available. |
| **DriveLaW** | LEGACY_DEEP_READ | Strong planning-centric WM route without explicit risk/reward/cost interface; video/world latent supports high planning score. | No candidate re-rollout; planning consumes hidden video-model representation rather than proving visually accurate rollout is the key decision variable. | Strong counterexample to explicit-risk-interface necessity; P3 pressure. |
| **TOAD** | LEGACY_DEEP_READ + SOURCE_AUDIT | Test-time trajectory optimization exposes scorer/search interaction; more optimization iterations can hurt under some settings. | Deployment includes mitigations/gating; source audit weakened chain from optimizer vulnerability to deployed planner failure; problem is not strongly WAM-specific. | Central reason P1 was retired as main; retain as robustness diagnostic. |
| **Sensitivity Shaping** | LEGACY_DEEP_READ | Provides a mechanism by which low action diversity can yield misleadingly low model sensitivity around unsafe controls. | Robotics/general latent-model result, not direct autonomous-driving P2-R evidence; also proposes its own regularization. | Mechanism precedent for P1, not current primary. |
| **DA-WAM** | REPO_REVERIFIED | Distinct future latent per candidate + future-conditioned scorer; explicitly respects offline counterfactual supervision constraint by supervising observed future only for expert-matched candidate; matched ablation shows action-conditioned future helps NAVSIM score. | Unexecuted candidates lack direct observed counterfactual-future target; reviewed evaluation is NAVSIM v1/v2, not a matched reactive ordering test. | Strongest current planning-centric WAM nearest prior to P2-R; kills novelty around per-candidate future scoring itself. |

## High-level lessons already earned

### 1. Explicit risk/value interface is not a default requirement

DriveLaW and other strong planning-centric WAMs show that a planner can benefit from world-model representations without an explicit hand-designed risk field or explicit scalar value interface.

Therefore:

```text
World Model → explicit Risk/Value → Planning
```

must not be treated as the project's default mother hypothesis.

### 2. Interaction modeling is already mature enough that generic claims are weak

GraphAD, BeTop, SafeDrive and historical interactive-prediction/planning work make it unsafe to claim novelty from merely adding interaction, action conditioning, contingency, or reactive evaluation.

### 3. Candidate-specific future prediction is already occupied

DA-WAM is the strongest current evidence. The remaining P2-R question, if any, is about whether the **induced action ordering is correct under intervention-dependent reactions**, not whether a candidate can have its own predicted future.

### 4. Learned scoring / reward failure is real but not automatically WAM-specific

DriveReward, Gen-Drive and TOAD show ranking/optimization vulnerabilities. NPPC provides an important counterexample where learned costs and local refinement work well. This is why P1 is no longer the main research problem.

### 5. World fidelity is not automatically decision sufficiency

DriveLaW, Epona and P3-related evidence motivate the question, but the broad formulation "planning-oriented representations are better than reconstruction-oriented ones" is already crowded. A defensible P3 would need to identify specific future distinctions whose loss changes action preference.

## Current caution

Do not quote fine-grained `LEGACY_DEEP_READ` numbers from this snapshot as publication evidence. Before using a number, ablation, or exact mechanism in a final argument, open the corresponding raw MD / canonical PDF and upgrade the item into the corresponding canonical deep analysis or source audit with explicit source locations.

The snapshot exists to prevent cross-session forgetting, not to bypass verification.
