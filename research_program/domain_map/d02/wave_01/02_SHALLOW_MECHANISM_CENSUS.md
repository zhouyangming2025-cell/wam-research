# D02-W1 Shallow Mechanism Census

Status: frozen Wave-1 census. This is a shallow, one-row-per-selected-paper inventory; it is not a new ontology and it does not amend the 12-paper mechanism map.

## Reading rule

The primary record is the human delivery layer:

```text
R–W–E ⊕ L
```

`R` describes the final commitment topology, `W` only records a qualifying online world/future carrier, `E` records the semantics of a final resolver when one exists, and `L` records the ordered learning/deployment fate. The table deliberately does not expose the full `C–X–D–P–V–T–L` backend for ordinary rows. That backend is reserved for the pressure cases in `04_ESCALATED_CASES.md`.

`N/A` means that the selected work is a boundary work and does not expose a one-stage driving decision route. `UNKNOWN` is used when the local source does not support a defensible route assignment. A route written for a boundary work is a nearest functional comparison only, not a claim that the work is a WAM planner.

## Selected papers

| ID | Paper / local version | Scope | Artifact or mode | Terminal output | One-sentence causal mechanism | Human route `R–W–E ⊕ L` | Evidence | Confidence | Nearest existing route family | Escalation |
|---|---|---|---|---|---|---|---|---|---|---|
| P0004 | *Reasoning Multi-Agent Behavioral Topology for Interactive Autonomous Driving* (BeTop; local raw-md version) | IN-DOMAIN | joint prediction/planning | ego and multi-agent trajectories | A topology distilled from future multi-agent trajectories guides a direct trajectory generator and imitative contingency learning. | `R0 + W4 + E0 ⊕ L[LS→retain{topology/trajectory path}]` | PAPER-SUFFICIENT | HIGH | BeTop/UniAD-like direct future-horizon conditioning | YES—carrier gate and final ego commitment |
| P0010 | *Test-Time Trajectory Optimization for Autonomous Driving* (TOAD; local raw-md version) | IN-DOMAIN | direct planner plus test-time CEM | selected trajectory | CEM repeatedly proposes and re-fits trajectory distributions against a learned trajectory-level reward, then commits the best candidate. | `RB + W0 + EV ⊕ L[LC→retain{scorer}/drop{search-time proposal}]` | PAPER-SUFFICIENT | HIGH | Drive-JEPA-PB / candidate resolver without online world carrier | YES—candidate identity and resolver boundary |
| P0011 | *Sensitivity Shaping for Latent Modeling* (local raw-md version) | BOUNDARY | generic robotic generative dynamics/OOD detection | dynamics model and OOD signal | Control-sensitivity regularization changes a generative dynamics model so unsupported action-induced transitions are easier to detect. | `N/A (boundary; nearest WAM analogue is W2/W4 predictive dynamics)` | PAPER-SUFFICIENT | HIGH | predictive dynamics, not a one-stage driving route | NO |
| P0013 | *BridgeSim: Unveiling the OL-CL Gap in End-to-End Autonomous Driving* (local raw-md version) | BOUNDARY | simulator/TTA and planner adaptation | adapted policy and closed-loop evaluation | Test-time adaptation calibrates observations, state-action bias, and temporal consistency against a reactive simulator. | `N/A (boundary; nearest route RB + W0 + EV)` | PAPER-SUFFICIENT | HIGH | candidate/scorer evaluation without a qualifying WAM carrier | NO |
| P0014 | *ReactSim-Bench: Benchmarking Reactive Behavior World Model Simulation in Autonomous Driving* (local raw-md version) | BOUNDARY | benchmark for reactive world-model simulation | simulated reactive responses | The benchmark generates candidate AV behaviors and measures whether a simulator produces plausible reactive responses from other agents. | `N/A (boundary; nearest route RG + W4 + E0)` | PAPER-SUFFICIENT | HIGH | generation/simulation terminal, not deployed policy | NO |
| P0016 | *How Can Driving World Models Do Counterfactual Prediction?* (local raw-md version) | BOUNDARY | counterfactual prediction analysis | counterfactual future observation | Abduction plus factual evidence is used to test whether action-conditioned world-model predictions recover the matched counterfactual future. | `N/A (boundary; nearest route RG + W4 + E0)` | PAPER-SUFFICIENT | HIGH | counterfactual world prediction without final resolver | NO |
| P0017 | *CRAFT: Counterfactual-to-Interactive Reinforcement Fine-Tuning for Driving Policies* (local raw-md version) | IN-DOMAIN | policy post-training | deployed policy action | Counterfactual group advantages provide dense policy-gradient proxy supervision while closed-loop residuals correct its bias and an EMA teacher stabilizes updates. | `R0 + W0 + E0 ⊕ L[LC→LR→retain{policy}/drop{counterfactual world}]` | PAPER-SUFFICIENT | HIGH | LAW/Metis-like training-only world or future supervision | NO |
| P0019 | *M2I: From Factored Marginal Trajectory Prediction to Interactive Prediction* (local raw-md version; CVPR 2022) | BOUNDARY | multi-agent prediction | joint likelihood-selected agent trajectories | Influencer trajectories condition reactor trajectories and joint likelihood selects a coherent multi-agent prediction set. | `N/A (boundary; nearest route RB + W4 + EF)` | PAPER-SUFFICIENT | HIGH | multi-agent consequence prediction, not ego commitment | NO |
| P0021 | *Hydra-MDP: End-to-end Multimodal Planning with Multi-target Hydra-Distillation* (local raw-md version) | IN-DOMAIN | multimodal end-to-end planner | selected trajectory | Multiple trajectory heads are trained against human and rule/simulation teachers, and their metric-specific outputs are combined into a final planning choice. | `RB + W0 + (EF+ED) ⊕ L[LT→LC→retain{proposal/scorer}/drop{teachers}]` | PAPER-SUFFICIENT | HIGH | WoTE / candidate resolver with decomposed driving criteria | YES—teacher/scorer and resolver semantics |
| P0024 | *DRIVEVLM: The Convergence of Autonomous Driving and Large Vision-Language Models* (local raw-md version) | IN-DOMAIN | DriveVLM / DriveVLM-Dual | hierarchical decision and trajectory/waypoint output | Scene description and analysis feed an explicit meta-action or decision layer before waypoint/trajectory generation. | `RH + W0 + E0 ⊕ L[LP→retain{reasoner/action bridge}]` | PAPER-SUFFICIENT | HIGH | Discrete-WAM policy / semantic decision→action | NO |
| P0025 | *OmniDrive: A Holistic Vision-Language Dataset for Autonomous Driving with Counterfactual Reasoning* (local raw-md version) | IN-DOMAIN | Omni-L/Omni-Q planning agent | action/trajectory-oriented VLM output | Counterfactual synthetic QA exposes alternative outcomes during training, while the deployed VLM directly maps scene context and language-aligned reasoning to driving outputs. | `R0 + W0 + E0 ⊕ L[LP→retain{VLM/planner}/drop{counterfactual data generator}]` | PAPER-SUFFICIENT | MEDIUM | Drive-JEPA-PF / training-only predictive supervision | NO |
| P0026 | *ORION: A Holistic End-to-End Autonomous Driving Framework by Vision-Language Instructed Action Generation* (local raw-md version) | IN-DOMAIN | VLM reasoning plus generative planner | semantic planning token and trajectory | A language-model reasoning stage emits a planning token/decision representation that conditions a generative trajectory planner. | `RH + W0 + E0 ⊕ L[LP→retain{reasoning token/planner}]` | PAPER-SUFFICIENT | HIGH | Discrete-WAM policy / semantic decision→action | NO |
| P0029 | *GenAD: Generative End-to-End Autonomous Driving* (local raw-md version) | IN-DOMAIN | joint scene/ego trajectory generation | jointly generated world-agent and ego trajectories | A latent future trajectory prior and recurrent generator jointly emit other-agent and ego trajectories in one generative process. | `RJ + W5 + E0 ⊕ L[LQ→retain{joint generator}]` | PAPER-SUFFICIENT | HIGH | Discrete-WAM joint / C5 joint emission | YES—joint output versus future-conditioned action |
| P0034 | *HUGSIM: A Real-Time, Photo-Realistic and Closed-Loop Simulator for Autonomous Driving* (local raw-md version) | BOUNDARY | simulator | simulator rollouts | The local raw source exposes the simulator title but not enough method text to establish a defensible mechanism route. | `UNKNOWN` | UNKNOWN | LOW | simulator/generation boundary | YES—source/evidence closure |
| P0038 | *Vista: A Generalizable Driving World Model with High Fidelity and Versatile Controllability* (local raw-md version) | BOUNDARY | controllable world model and action evaluation | controllable future video/reward signal | A controllable video world model rolls out future observations for commands, goals, trajectories, and low-level controls, and uses model uncertainty as an action-evaluation reward. | `RG + W4 + E0 ⊕ L[LP→LG→retain{world generator}]` | PAPER-SUFFICIENT | MEDIUM | Epona self-rollout / generation-and-evaluation boundary | YES—reward capability versus final resolver |
| P0039 | *DriveDreamer-2: LLM-Enhanced World Models for Diverse Driving Video Generation* (local raw-md version) | BOUNDARY | video generation | generated driving video | Language and driving controls condition a world model that generates diverse multi-view driving videos for downstream data augmentation. | `RG + W4 + E0 ⊕ L[LP→LG→retain{video generator}]` | PAPER-LIMITED | MEDIUM | generation-only world-model route | NO |
| P0054 | *What Truly Matters in Trajectory Prediction for Autonomous Driving?* (local raw-md version) | BOUNDARY | task-driven predictor evaluation | predictor assessment under interactive dynamics | The work shows that predictor quality must be judged through ego–other-agent interaction and downstream closed-loop task effects rather than fixed-log error alone. | `N/A (boundary; nearest route W4 consequence evaluation)` | PAPER-SUFFICIENT | HIGH | dynamics/evaluation audit, not a WAM planner | NO |
| P0055 | *SLEDGE: Synthesizing Driving Environments with Generative Models and Rule-Based Traffic* (local raw-md version) | BOUNDARY | generative simulator | generated lanes, agents, and traffic rollouts | A latent generative model creates lane graphs and agents that seed a rule-based traffic simulator for long-route evaluation. | `N/A (boundary; nearest route RG + W4 + E0)` | PAPER-SUFFICIENT | HIGH | simulator/world-generation terminal | NO |
| P0057 | *Planning-oriented Autonomous Driving* (UniAD; local raw-md version) | IN-DOMAIN | unified perception/prediction/planning | planned ego trajectory | Agent motion and occupancy forecasts are exposed through unified queries so a direct planner can condition ego trajectory output on predicted future scene structure. | `R0 + W4 + E0 ⊕ L[LS→retain{prediction/planning path}]` | PAPER-SUFFICIENT | HIGH | BeTop-like direct future-horizon conditioning | NO |
| P0058 | *VAD: Vectorized Scene Representation for Efficient Autonomous Driving* (local raw-md version) | IN-DOMAIN | vectorized prediction plus direct planning | planned ego trajectory | Vectorized map and agent-motion representations, including predicted future motion, are used as structured constraints/guidance for direct trajectory prediction. | `R0 + W4 + E0 ⊕ L[LS→retain{vectorized prediction/planning path}]` | PAPER-LIMITED | MEDIUM | UniAD/BeTop-like direct future-horizon conditioning | YES—whether vectorized state passes the WAM carrier gate |

## Census totals

| Measure | Result |
|---|---:|
| Selected papers / one-row artifacts | 20 / 20 |
| IN-DOMAIN | 10 |
| BOUNDARY | 10 |
| Route unresolved | 1 (P0034 remains a boundary probe but route `UNKNOWN`) |
| PAPER-SUFFICIENT | 17 |
| PAPER-LIMITED | 2 |
| UNKNOWN evidence | 1 |
| CODE-VERIFIED | 0 |
| Escalation flags | 6 |
| New R/W/E code or new axis | 0 |

The scope count treats P0034 as a selected boundary probe even though its route remains `UNKNOWN`; therefore the operational scope total is 10 in-domain and 10 boundary probes, with one boundary probe unresolved at the route level.

## Deliberate non-claims

This wave does not claim that every predictive representation is a world carrier. In particular, P0058 is recorded as an evidence-limited pressure case, and ordinary simulator/generation works remain outside the deployed one-stage route map. It also does not treat a candidate bank by itself as a world model: P0010 and P0021 receive `W0` because their online resolver operates on trajectories and scores, not on a qualifying world/future carrier.
