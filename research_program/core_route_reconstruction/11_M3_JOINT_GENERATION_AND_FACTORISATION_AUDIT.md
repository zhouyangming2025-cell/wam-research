# M3 Joint Generation and Causal Factorisation Audit

Status: **FIRST-PRINCIPLES FACTORISATION AUDIT — NOT AN ONTOLOGY SPEC**  
Branch: `research/core-route-reconstruction`  
Date: 2026-09-17  
Target: stress-test `M3` and determine whether the emerging route spine can be expressed as a causal factorisation of world/action computation.

## 0. Key insight

The strongest abstraction emerging from the previous audits is not a list of modules. It is the **implemented causal factorisation between world variables and action variables**.

Let:

- `O` = observed/history context;
- `Z` = world/future state or model state;
- `A` = ego action / trajectory;
- `A~` = provisional candidate action;
- `theta_A` = deployed action model parameters after training.

The current motifs can be written as computational factorisations:

### M0 — compiled world knowledge

Training:

`world process -> learning signal -> theta_A`

Deployment:

`A ~ p(A | O; theta_A)`

No online `Z` mediator is required.

### M1 — world-first mediation

`Z ~ p_W(Z | O)`

then

`A ~ p_A(A | O, Z)`.

### M2 — action-conditioned consequence mediation

`A~_k ~ q(A | O)`

then

`Z_k ~ p_W(Z | O, A~_k)`

then

`A* = Resolve({A~_k, Z_k})`

or an equivalent consequence-guided action update.

### M3 — joint world-action generation

`(Z, A) ~ p_G(Z, A | O)`

where both are generated variables of one future process rather than one being merely an external conditioning variable for the other.

### M4 — reciprocal refinement

Repeated alternating implemented conditionals:

`Z^(i+1) <- W(O, A^(i))`

`A^(i+1) <- P(O, Z^(i+1))`

until commitment.

This factorisation view is currently more explanatory than R/W/E/L because it describes **who conditions whom, at what stage, and whether the relation exists at deployment or has been compiled into parameters**.

Important caution:

> Any mathematical joint distribution can be algebraically factorized in multiple ways. The taxonomy concerns the **implemented computational/causal factorisation**, not abstract probability identities.

---

## 1. Strict M3 gate

A planning mode qualifies as M3 only when:

1. world/future variables and ego-action variables are both generated/predicted variables in one future generative program;
2. they belong to one coupled sample/process rather than independent heads that merely share context;
3. neither variable is only a fixed external condition supplied before the generative program;
4. the action output is a real planning output in the scoped mode;
5. shared encoders, shared latent spaces, multitask objectives, or parallel prediction heads alone are insufficient;
6. downstream ranking of jointly generated futures does not erase M3 if joint birth happened first;
7. if the implemented process is more faithfully described as world-first `Z -> A`, action-conditioned `A -> Z -> A`, or reciprocal alternation, prefer that more specific factorisation.

---

## 2. DrivingGPT — strong token-level M3 anchor

Primary source: `papers/raw_md/P0040_DrivingGPT/P0040_DrivingGPT.raw.md`.

DrivingGPT explicitly converts visual observations and driving actions into one interleaved discrete “driving language” and trains one autoregressive transformer by standard next-token prediction.

The paper's stated goal is to unify world modeling and trajectory planning into one sequence modeling problem.

Why it passes M3:

- image tokens and action tokens are generated variables in one sequence;
- the same generative program models both world evolution and driving action;
- action is not merely an external conditioning input to a separate world model in the planning mode;
- world/action jointness is architectural and objective-level, not merely shared encoder features.

Internal token order is autoregressive, but this does not reduce the program to simple M1 or M2 because the future sequence itself interleaves both modalities as one modeled process.

Verdict: **STRONG M3**.

---

## 3. GenAD — strong structured joint-future M3 anchor

Primary source: `papers/raw_md/P0029_GenAD/P0029_GenAD.raw.md`.

GenAD explicitly criticizes serial prediction-before-planning for ignoring high-order ego/other-agent interaction.

Its generative framework places ego and surrounding agents in one structural latent future trajectory space and simultaneously generates their futures.

Why it passes M3:

- ego trajectory and surrounding-agent trajectories are both generated future variables;
- ego is not merely proposed first and used to condition an external consequence model;
- surrounding-agent prediction is not merely generated first and fed to a separate planner;
- the core thesis is to model the joint evolution process itself.

Verdict: **STRONG M3**.

---

## 4. Gen-Drive — M3 plus downstream evaluation, not M2

Primary source: `papers/raw_md/P0006_GenDrive/P0006_GenDrive.raw.md`.

Gen-Drive's diffusion process operates in the **joint action space of all agents including ego**. It generates complete joint future scenes, then the scene evaluator scores those generated joint futures.

The critical factorisation is:

`O -> sample joint future (A_ego, A_agents) -> score joint sample -> choose`.

This differs from M2:

`O -> propose ego A_k -> predict world Z(A_k) -> score -> choose`.

In Gen-Drive, the world/other-agent future is not a separately generated response to an externally fixed ego candidate. Ego and other-agent futures are born from the same joint diffusion sample.

Therefore:

- multi-sample generate-then-evaluate mode = `M3 + downstream resolver profile`;
- single-sample fine-tuned mode = `M3` with reward preference partially compiled into generator parameters.

The downstream evaluator does **not** transform the route into M2.

Verdict: **STRONG M3; important M2 negative control**.

---

## 5. Discrete-WAM — M3 is mode-specific

Primary source: `papers/raw_md/P0064_Discrete-WAM/...`.

Discrete-WAM provides three task families:

- world modeling;
- joint world-policy modeling;
- policy modeling.

In joint world-policy mode, future visual tokens and future action tokens are jointly modeled/edited in one shared discrete sequence framework.

This satisfies M3 for that mode.

However, policy modeling predicts high-level decision then future action tokens. If deployed planning uses policy mode without joint future visual generation, the deployment route should not automatically be called M3.

This yields a strong rule:

> **M3 attaches to an actual joint-generation mode, not to a paper-wide “unified” marketing label.**

Verdict:

- joint world-policy mode: **M3**;
- policy-only deployment mode: separate audit required.

---

## 6. OccWorld — new M3 correction from full-paper reading

Primary source: `papers/raw_md/P0043_OccWorld/P0043_OccWorld.raw.md`.

The D01 neutral skeleton made OccWorld look like:

`future occupancy -> planner`.

Full text shows a more coupled program:

- a GPT-like spatial-temporal generative transformer predicts subsequent scene tokens;
- it also predicts ego tokens / ego movement;
- the paper explicitly states it simultaneously forecasts surrounding-scene evolution and ego movement;
- its formal world model predicts next scene representation **and** next ego position.

Thus the more faithful computational factorisation is:

`history -> joint autoregressive future process -> (future occupancy, ego future)`.

This passes the current M3 gate more naturally than M1.

### Correction

- `07_MINIMAL_CAUSAL_SPINE_PROJECTION.md`: OccWorld=M1 is **SUPERSEDED**.
- current assignment: **M3 pressure/strong candidate**, pending exact token-generation ordering details if normative precision is needed.

This correction increases confidence that M3 is not restricted to “visual-action token language” methods; it recurs in structured 3D world/ego generation as well.

---

## 7. Epona — why shared temporal latent is not automatically M3

Epona has:

- a shared causal temporal latent dynamics model;
- specialized video diffusion decoder;
- specialized trajectory diffusion decoder;
- joint training / asynchronous multimodal capability.

But the current evidence is better described as:

`shared temporal world state Z -> video head`

and

`shared temporal world state Z -> trajectory head`.

That is **parallel conditional generation from shared state**, not necessarily a single jointly sampled world-action future.

Therefore Epona remains better represented under M1-state mediation unless stronger evidence establishes one coupled world/action sample whose variables jointly evolve.

This distinction is essential:

> shared latent != joint generated future.

---

## 8. Metis — why joint training is not M3

Metis jointly trains video and action experts but explicitly masks future-video information from the action path and bypasses future generation at deployment.

Thus:

- joint objective != joint deployed generation;
- shared latent interaction != co-born future world/action sample.

Metis remains better represented as M0-R with an asymmetric coupling profile.

---

## 9. M3 internal sublineages

The following sublineages are visible:

### M3-TOKEN — unified world/action token process

Examples:

- DrivingGPT;
- Discrete-WAM joint world-policy mode.

World/action modalities share a discrete generative sequence/editing language.

### M3-SCENE — joint structured future generation

Examples:

- GenAD;
- Gen-Drive;
- OccWorld.

The generated future includes ego and environment/other-agent state in one coupled structured process.

### Are these separate CoreRoutes?

Current answer: **not yet**.

Replacing visual tokens with structured agent/occupancy variables changes representation and generative factorization details, but the high-level scientific thesis remains:

> do not place prediction and planning in a serial mediator relation; model the coupled world-action future directly.

Thus M3-TOKEN vs M3-SCENE are best treated as **representation/generation sublineages** pending stronger route-level evidence.

---

## 10. M1 vs M3 clarified by factorisation

This is now cleaner than “joint vs shared”.

### M1

Implemented process:

`Z = W(O)`

then

`A = P(O, Z)`.

World state is a mediator that exists before action generation.

### M3

Implemented process:

`(Z, A) = G(O)`

or an interleaved joint sequence in which both are variables of one future process.

No separate world-state mediator is the central planning bridge.

### Hard examples

- Policy World Model: M1 — explicitly forecast future state, then use it as rationale for action.
- DriveLaW: M1 — generator state is formed and fed into Action DiT.
- DrivingGPT: M3 — visual/action tokens share one generative language.
- GenAD: M3 — ego and other-agent futures generated together.
- OccWorld: M3 — future scene and ego tokens jointly forecast.

This is a major improvement over the old W5/RJ jointness coding because it derives jointness from **implemented conditional structure**, not labels.

---

## 11. M2 vs M3 clarified by factorisation

### M2

An ego alternative is already identifiable before world prediction:

`A~_k -> Z(A~_k)`.

The world is asked:

> “If I do this, what happens?”

Examples: WoTE, DA-WAM, World4Drive, Drive-WM.

### M3

Ego and world future are generated as one coupled possibility:

`(A, Z) ~ G(O)`.

The system asks:

> “What coherent joint future might happen, including what ego does?”

Examples: GenAD, Gen-Drive, DrivingGPT, OccWorld.

This distinction survives downstream ranking:

- rank externally action-conditioned consequences -> M2;
- rank jointly generated world-action futures -> M3 + resolver.

This is one of the strongest currently supported route distinctions.

---

## 12. The causal-factorisation spine after M3 audit

The current route discovery language can now be written compactly:

### F0 — compiled

World reasoning exists in training but is marginalized/compiled into deployed decision parameters.

### F1 — world-first

`world state -> action`.

### F2 — action-conditioned consequence

`provisional action -> world consequence -> action commitment/refinement`.

### F3 — joint future generation

`world + action co-generated as one future process`.

### F4 — reciprocal alternation

`action -> world -> revised action -> revised world -> ...`.

These `F0...F4` labels are **descriptive shorthand only**, not a renaming or acceptance of final CoreRoutes. Existing `M0...M4` working symbols remain the repo's current reconstruction labels.

---

## 13. Why factorisation may be the missing first-principles criterion

A legitimate major route distinction should ideally answer:

> **What conditional dependency must be implemented for the method's world-model planning idea to exist?**

This criterion naturally passes the Core-Bridge Deletion Test:

- remove predictive training from M0 -> world knowledge no longer reaches policy;
- remove Z->A mediation from M1 -> ordinary direct planner / disconnected world model;
- remove A->Z(A) branch from M2 -> ordinary candidate scoring/direct planning;
- separate joint generation into serial prediction/planning in M3 -> different family;
- remove feedback alternation from M4 -> one-shot M1/M2-like planning.

It also naturally ignores many fake route differences:

- RGB vs BEV vs latent;
- reward semantics;
- diffusion vs transformer vs flow;
- explicit vs compressed future, unless it changes dependency structure;
- candidate count by itself.

This is the strongest theoretical justification yet for the emerging causal spine.

---

## 14. Remaining caveats

1. The same joint probability can be algebraically refactorized. Classification must follow actual computation/dataflow, not probability notation alone.
2. Training factorisation and deployment factorisation can differ; both must be recorded.
3. A paper may contain multiple modes with different factorisations.
4. A paper may compose two bridges (WorldDrive).
5. A shared hidden representation can obscure whether a separate mediator exists; code or exact architecture may be needed.
6. Some papers called “world models” may actually provide ordinary prediction features and fail the domain/world-state gate.
7. M4 is still under-replicated.

---

## 15. Current verdict

High confidence:

- implemented world/action causal factorisation is the strongest first-principles candidate discovered so far for reconstructing WAM planning routes;
- M1, M2, and M3 are genuinely different implemented dependency structures;
- downstream candidate ranking does not by itself turn M3 into M2;
- shared latent / joint training does not by itself create M3;
- OccWorld is a material correction and strengthens M3 rather than M1.

Medium/high confidence:

- M0 can be incorporated into the same framework as the “compiled/marginalized from deployment” ancestor;
- M4 is the iterative extension of alternating M1/M2 conditionals.

Low/medium confidence:

- exact leaf hierarchy inside M0/M1/M2/M3;
- whether the final ontology should literally be expressed as probabilistic factorisations or as human-readable route names derived from them.

Next step:

> synthesize all corrections into a revised minimal causal spine and explicitly separate (1) route factorisation, (2) research genealogy, (3) profiles/realizations, and (4) paper composition. Then attack the revised spine with remaining counterexamples before any final route naming.
