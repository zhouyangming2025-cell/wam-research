# D02-W1 Route Family Map

This map is a verification of route families already admitted by the frozen human layer. It is not a proposal for new codes. The purpose is to answer whether the 20-paper wave can be explained by a small number of functional routes while preserving meaningful differences in `E` and ordered `L`.

## Family inventory

| Family | Human route pattern | Wave-1 members | Interpretation |
|---|---|---|---|
| F1 | `R0 + W0 + E0 ⊕ L[training-only predictive/interactive supervision]` | P0017, P0025 | A world, counterfactual, or simulator branch improves learning, but no qualifying online carrier remains in the deployed direct policy. The papers are functionally close at runtime while their learning routes remain distinguishable. |
| F2 | `R0 + W4 + E0 ⊕ L[LS→retain{prediction/planning path}]` | P0004, P0057, P0058 | A direct ego trajectory is conditioned by a future-horizon structured consequence. BeTop, UniAD, and VAD are grouped by deployment role, not by representation or network architecture. P0058 remains carrier-gate evidence-limited. |
| F3 | `RB + W0 + E[resolver] ⊕ L[...]` | P0010, P0021 | An explicit candidate bank reaches a common resolver, but the resolver does not consume a qualifying online world carrier. P0010 is holistic reward/CEM search; P0021 combines human and rule/simulation-derived decomposed criteria. `E` and `L` preserve that difference. |
| F4 | `RH + W0 + E0 ⊕ L[LP→retain{semantic/action bridge}]` | P0024, P0026 | A semantically meaningful decision or planning token sits between context and numeric trajectory/action generation. This is different from direct action generation even when both ultimately output a single trajectory. |
| F5 | `RJ + W5 + E0 ⊕ L[LQ→retain{joint generator}]` | P0029 | World/agent and ego action outputs are born from one joint generative carrier. No downstream common resolver is evidenced, so this remains `RJ`, not `RB`. |
| F6 | boundary: generation/simulation terminal | P0014, P0038, P0039, P0055 | These works produce future videos, simulated traffic, or evaluation signals. They are useful neighboring mechanisms, but a generation/simulation terminal is not automatically a deployed one-stage driving policy route. P0038 is specifically held at the boundary because its action reward is not yet shown to be a final resolver. |
| F7 | boundary: prediction/analysis/evaluation only | P0011, P0013, P0016, P0019, P0054 | These works expose dynamics, counterfactual, interactive prediction, adaptation, or evaluation mechanisms without an independently evidenced one-stage ego commitment path. They should not be forced into WAM route classes. |
| F8 | boundary: simulator with insufficient local evidence | P0034 | HUGSIM is selected as a simulator boundary probe, but the local raw artifact lacks enough method text for even a defensible nearest route. It remains `UNKNOWN` pending evidence closure. |

## Route-family membership is not paper identity

The same paper can support different modes in a deeper audit. Wave 1 intentionally keeps one row per selected paper and does not split modes unless the shallow source already makes the terminal role unambiguous. The family map therefore records the dominant selected artifact, not every training or demonstration mode.

Examples:

- P0010 belongs to the candidate-resolver family even though CEM iteratively changes the proposal distribution. Iterative search is not a new route family; the identity of the candidate and the common reward resolver are the relevant facts.
- P0017 belongs to the direct-runtime family even though counterfactual groups are evaluated during post-training. A training-only future branch does not create an online `W` carrier.
- P0029 belongs to joint emission because its world/agent and ego trajectories are generated together. It would be a different route if an externally proposed ego candidate were used to condition a separate consequence model and then passed to a resolver.
- P0038 is not promoted to `RB + W4 + EV` merely because it defines an action-evaluation reward. The shallow evidence establishes a reward capability, not necessarily a deployed final selection topology.

## Coverage against the intended mechanism space

Wave 1 deliberately covers the main pressure directions needed before corpus expansion:

1. direct policy with no online carrier;
2. direct policy with future-horizon carrier;
3. explicit candidate selection with and without a world carrier;
4. semantic decision before action;
5. joint world/action generation;
6. generation-only and simulator terminals;
7. training-only counterfactual/world use;
8. prediction/evaluation works that must remain outside the WAM planner map.

All eight directions are represented without adding a new `R`, `W`, or `E` code. The remaining uncertainty is evidentiary and mode-specific, not a demonstrated need for another axis.

## Family-level verdict

The route layer remains compact enough for human use. The apparent variety of the 20 papers is explained by five deployed route families plus explicit boundary families. Differences that matter are retained in `E`, ordered `L`, scope, and escalation attributes. Differences that do not change the causal interface—RGB versus BEV, latent versus vectorized state, transformer versus diffusion, or regression versus search—remain implementation attributes.
