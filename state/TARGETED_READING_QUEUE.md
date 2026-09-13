# TARGETED_READING_QUEUE

Status: **FROZEN TARGETED EXPANSION**

Purpose: add only papers with high discrimination value for the current planning-centric WAM question, then stop corpus expansion and deep-read them.

All entries below are `DISCOVERED_NOT_INGESTED` unless already present elsewhere. Do not allocate Paper IDs until actual ingestion.

## A. Core P2-R attack set — ingest first

| priority | title | year | primary metadata | why it matters |
|---|---|---:|---|---|
| A1 | **BridgeSim: Unveiling the OL-CL Gap in End-to-End Autonomous Driving** | 2026 | arXiv:2604.10856; Seth Z. Zhao et al. | Separates observational domain shift from objective mismatch and directly studies OL→CL transfer. Needed to determine whether P2-R is merely one instance of a broader already-established objective mismatch. |
| A2 | **ReactSim-Bench: Benchmarking Reactive Behavior World Model Simulation in Autonomous Driving** | 2026 | arXiv:2606.14058; Zhiyuan Zhang et al. | Direct benchmark of world-agent reactions when AV behavior deviates from logs. High value for testing whether action-conditioned behavior models actually react correctly. |
| A3 | **CausalDrive: Real-time Causal World Models for Autonomous Driving** | 2026 | arXiv:2606.15341; Tianyi Yan et al. | Explicitly targets reactive / causal world simulation under ego trajectories and removes oracle future NPC layouts. Strong prior-art pressure on generic "reactive world model" novelty. |
| A4 | **How Can Driving World Models Do Counterfactual Prediction?** | 2026 | arXiv:2608.11601; Jiaru Zhang et al. | Constructs matched factual and counterfactual outcomes and argues direct action-conditioned prediction can miss episode-specific counterfactual truth. Critical for distinguishing plausibility from causal/counterfactual correctness. |
| A5 | **CRAFT: Counterfactual-to-Interactive Reinforcement Fine-Tuning for Driving Policies** | 2026 | arXiv:2605.04470; Keyu Chen et al. | Explicitly decomposes dense counterfactual proxy supervision and grounded closed-loop residual correction. Strong evidence that counterfactual estimates can be biased and need interaction-grounded correction. |

### Acquisition sources

```text
BridgeSim
  arXiv: https://arxiv.org/abs/2604.10856
  code:  https://github.com/VAIL-UCLA/BridgeSim

ReactSim-Bench
  arXiv: https://arxiv.org/abs/2606.14058
  code:  https://github.com/Thinklab-SJTU/ReactSim-Bench

CausalDrive
  arXiv: https://arxiv.org/abs/2606.15341

How Can Driving World Models Do Counterfactual Prediction?
  arXiv: https://arxiv.org/abs/2608.11601

CRAFT
  arXiv: https://arxiv.org/abs/2605.04470
  code:  https://github.com/CurryChen77/CraftPolicy
```

Metadata above is **WEB-VERIFIED DISCOVERY**, not yet `DOCUMENT_VERIFIED`. Front-page verification occurs only after canonical PDF ingestion.

## B. Historical controls — ingest after A1–A5

These are not WAM papers. Their purpose is to prevent us from renaming long-standing interactive prediction/planning ideas with 2026 WAM terminology.

| priority | title | year | primary metadata | why it matters |
|---|---|---:|---|---|
| H1 | **GameFormer: Game-theoretic Modeling and Learning of Transformer-based Interactive Prediction and Planning for Autonomous Driving** | 2023 | ICCV 2023; arXiv:2303.05760; Zhiyu Huang, Haochen Liu, Chen Lv | Joint interactive prediction/planning with game-theoretic response structure. Tests whether reaction-aware planning concepts predate WAM framing. |
| H2 | **M2I: From Factored Marginal Trajectory Prediction to Interactive Prediction** | 2022 | CVPR 2022; arXiv:2202.11884; Qiao Sun et al. | Influencer→reactor conditional prediction is an important precedent for action/agent-conditioned response modeling. |
| H3 | **A Game-Theoretic Approach to Replanning-Aware Interactive Scene Prediction and Planning** | 2016 | IEEE TVT 65(6), 3981–3992; DOI 10.1109/TVT.2015.2508009; Mohammad Bahram et al. | Explicitly models other drivers' replanning/reactions in prediction-planning loops. High-value historical novelty control. |

H3 may be paywalled. If no lawful open copy is available, keep metadata + abstract evidence and do not use unofficial mirrors.

## C. Deferred — only if a specific unresolved question survives

Do **not** ingest automatically:

```text
What Truly Matters
Policy World Model
BeyondDrive
ELF-VLA
WorldRFT / ReWorld / Auto-JEPA / WA-JEPA / Drive-JEPA
```

These become active only if Round 2 exposes a concrete unresolved issue related to P3, representation sufficiency, or planning-oriented WAM design.

## D. Reading order after ingestion

Deep-read in this order:

```text
A4 Counterfactual Prediction
A2 ReactSim-Bench
A1 BridgeSim
A5 CRAFT
A3 CausalDrive
H3 Bahram 2016
H1 GameFormer
H2 M2I
```

Reason: start from the cleanest counterfactual-identification question, then reaction benchmark, then policy OL/CL causes, then interactive correction, then reactive generative WM; finish with historical novelty controls.

## E. Per-paper P2-R extraction table

For every A/H paper answer exactly:

| question | required answer |
|---|---|
| Evaluation regime | OL / non-reactive CL / reactive CL / matched counterfactual / real vehicle |
| Ego intervention explicit? | yes/no + exact representation |
| Other-agent response intervention-dependent? | yes/no + mechanism |
| Fixed current state? | yes/no |
| Fixed ego candidate/action set? | yes/no |
| Factual vs reactive ordering compared? | yes/no |
| Ordering reversal directly measured? | yes/no |
| Planning regret from reversal measured? | yes/no |
| Strongest evidence against P2-R | exact experiment / result |
| Strongest evidence consistent with P2-R | exact experiment / result |
| Prior-art occupancy | CONCEPT_PRECEDENT / STRONG_NEIGHBOR / DIRECT_OCCUPATION / EFFECTIVELY_SOLVED / NOT_RELEVANT |
| Remaining uncertainty | concise |

## F. Stop condition

After A1–A5 + H1–H3 are adjudicated:

```text
STOP CORPUS EXPANSION.
```

Then issue one of:

```text
P2-R SURVIVES
P2-R KILLED
NONE / EVIDENCE INSUFFICIENT
```

Do not protect P2-R by widening its definition. Do not begin method design before this gate closes.
