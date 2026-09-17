# D02-W1E Escalated-Case Full-Text Rerun

## Results

| Case | Full-text finding | Previous route | Rerun route | Disposition | Confidence |
|---|---|---|---|---|---|
| P0004 BeTop | Method Sec. 3.3 and Appendix C.1–C.2 define multimodal ego trajectories, branched contingency sets, prediction-aware costs, and a final `argmax`/`argmin` selection. | `R0 + W4 + E0` | `RB + W4 + ED` | `REMAP`; structural pressure recorded below | HIGH |
| P0010 TOAD | Sec. 3.1–3.2 explicitly defines a CEM population, elite updates, and a final common comparison between searched mean and base trajectory. The scorer is a learned reward, not a world carrier. | `RB + W0 + EV` | `RB + W0 + EV` | `KEEP` | HIGH |
| P0021 Hydra-MDP | Sec. 2.1–2.4 defines a fixed candidate vocabulary, human imitation scores, distilled metric heads, assembled cost, and final lowest-cost selection. | `RB + W0 + (EF+ED)` | `RB + W0 + (EF+ED)` | `KEEP` | HIGH |
| P0029 GenAD | Sec. 3.2–3.4 generates agent and ego futures from a shared trajectory-prior/generative process and discards the future encoder at inference; no downstream common resolver is described. | `RJ + W5 + E0` | `RJ + W5 + E0` | `KEEP` | HIGH |
| P0034 HUGSIM | Sec. 1, 4, and 6 describe a photorealistic closed-loop simulator that takes planner waypoints/control, updates ego and actor states, renders observations, and emits simulation rollouts. It is not itself a one-stage action policy. | `UNKNOWN` | `RG{external} + W4 + E0` | `REMAP` from unresolved boundary to simulator/world-generation boundary | HIGH |
| P0038 Vista | Sec. 3.1–3.3 and Appendix C define autoregressive future video rollout under supplied action conditions and a model-uncertainty reward. The reward is evaluated experimentally; no final deployed policy resolver is shown. | `RG + W4 + E0` | `RG{external} + W4 + E0` | `KEEP`; boundary retained | HIGH |
| P0058 VAD | Sec. 3.1–3.4 defines online vectorized map and future-agent-motion prediction consumed by the planning head and vectorized planning constraints. The highest-confidence non-ego forecast is an internal prediction choice, not an ego candidate bank. | `R0 + W4 + E0` provisional | `R0 + W4 + E0` | `KEEP`; carrier gate now supported | HIGH |

## Case notes

### P0004 BeTop

The full paper changes the output-commitment interpretation. The planning head generates multiple short and branched ego trajectories. Contingency learning evaluates each against marginal/joint future predictions and defines a selected trajectory. Appendix C.2 further states that inference selects the full trajectory by `argmax` over the combined confidence and prediction-aware cost.

This satisfies the semantic candidate-bank test for `RB`; random sampling or multiple decoder queries alone would not have been enough. The selected criterion is a decomposed driving interaction/safety cost, hence `ED`, not `E0`.

The remaining issue is not whether BeTop has a resolver. It is whether its future-agent prediction is a candidate-indexed consequence or a shared `W4` carrier. The inference equation uses shared marginal predictions `Y_M` when scoring the ego candidates, while joint branch predictions are paired with branches during contingency training. This is recorded as a type-constraint pressure, not resolved by inventing `X3`.
### P0010 TOAD

TOAD is a clean example of `RB + W0 + EV`: CEM samples continuous controls, retains candidate identity through elite selection, optimizes the learned scorer plus comfort/anchor terms, and returns the best final trajectory. No online world/future carrier is required by the method.

### P0021 Hydra-MDP

Hydra-MDP confirms that teacher provenance belongs in learning/audit attributes, not in a new route code. The deployed student scores each fixed trajectory candidate with imitation and distilled simulation-derived metric heads, then selects the lowest assembled cost.

### P0029 GenAD

GenAD is not merely a direct policy with a hidden future feature. Its trajectory prior and recurrent latent generator produce future trajectories for ego and other agents in one generative mechanism. Since the paper does not describe a downstream common resolver over joint samples, `RJ + W5 + E0` remains the correct coarse route.

### P0034 HUGSIM

The full text closes the previous evidence gap. HUGSIM reconstructs a dynamic scene, generates actor behavior, accepts planner waypoints, applies control, updates states, and returns the next observation in a closed loop. Its terminal object is the simulated world rollout, so `RG` is appropriate; its action source is external to the simulator, so the route carries the `external` modifier.

### P0038 Vista

Vista's reward is a world-model-derived action-evaluation capability. The paper samples perturbed actions and reports reward correlation, but does not show a deployed planner that uses the reward to commit one action. Therefore promoting it to `EV` would overread the paper.

### P0058 VAD

VAD clears the existing carrier gate at the paper level: motion is a separately predicted temporal object, has trajectory supervision, and reaches the planning path through ego-agent interaction and vectorized collision constraints. Its internal non-ego mode selection does not become `RB` because the selected object is not the final ego action candidate.
