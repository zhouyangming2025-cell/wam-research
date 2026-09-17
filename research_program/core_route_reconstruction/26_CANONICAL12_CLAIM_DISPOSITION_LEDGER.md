# Canonical-12 Claim Disposition Ledger
Status: **audit of prior claims; no ontology update**.

The ledger does not treat a previous label as evidence. It checks each recurring conclusion against the neutral records and assigns one disposition:

```text
RETAIN              supported at the same abstraction level
RETAIN_AS_PROFILE   valid, but too low-level or too local for a headline route
MERGE               previous split is a false route split at the paper-family level
SPLIT               previous merge hides a material causal/artifact boundary
CORRECT             wording or lifecycle interpretation was wrong
UNKNOWN             evidence cannot close the boundary
ADMIN               repository/process fact only
```

| Claim ID | Prior claim or pressure point | Evidence checked | Disposition | Reason and route impact |
|---|---|---|---|---|
| CL-01 | LAW's future-prediction branch improves the planner | LAW raw `:21-38,65-99`; Set C reconstruction | RETAIN | It is a real action-conditioned training bridge, but not an online future carrier. It belongs in the learning program of a direct planner. |
| CL-02 | LAW and Drive-JEPA share “predictive learning helps planning” | LAW raw `:23-34`; Drive-JEPA raw `:81-99`; `core_route_reconstruction/18` | RETAIN_AS_PROFILE | The shared research family is real; LAW's action-conditioned co-training and Drive-JEPA's scalable pretraining/transfer are different learning programs. Do not call them identical mechanisms. |
| CL-03 | Drive-JEPA PF and PB are two unrelated world-model routes | Drive-JEPA raw `:92-166`; `core_route_reconstruction/18` and `19` | MERGE + SPLIT | Merge at paper-family/genealogy level; split at artifact deployment topology because PB has proposals and a resolver while PF does not. |
| CL-04 | Epona planning is online future-scene evaluation | Epona raw `:34-36,100-153,183-211`; Set B | CORRECT | The video branch is parallel and can be disabled for planning. The action head consumes shared temporal context, not candidate-indexed generated futures. |
| CL-05 | DriveLaW is merely a stronger shared latent | DriveLaW raw `:45-68,113-145`; Set B | CORRECT | The planning edge specifically consumes cached internal Video DiT states. This is a retained online generator-state bridge, not only a shared training representation. |
| CL-06 | Epona, DriveLaW, and Metis are one “joint WAM” route | Epona raw; DriveLaW raw; Metis raw `:46-115`; Set B | SPLIT | Their causal learning/deployment programs disagree: parallel shared context, chained generator state, and asymmetric action-only deployment. Keep a common debate family, not one mechanism. |
| CL-07 | World4Drive, WoTE, and WorldDrive are identical because all are candidate→future→score | three raw method sections; Set A | SPLIT | Candidate identity is shared, but future object and lifecycle differ: factual endpoint plausibility, online recurrent horizon, and distilled online surrogate. E/scorer semantics alone do not cause the split; consequence construction does. |
| CL-08 | Resolver semantics are a universal headline axis | `core_route_reconstruction/00` and `22`; first-six audit | REJECT | Expert compatibility, value, and decomposed reward may be interchangeable resolver implementations for one broader candidate-consequence function. Preserve provenance/criterion as a profile. |
| CL-09 | WorldDrive is only a candidate scorer | WorldDrive raw `:45-128`; Set A | CORRECT | It contains both representation inheritance and candidate-specific online future-surrogate evaluation. A one-label summary loses an independent bridge. |
| CL-10 | DynFlowDrive is an online dynamic-world evaluator | DynFlowDrive raw `:90-213`; prior deep analysis | CORRECT | The world-flow criterion exists during training and is compiled into a deployed scorer; the world model is explicitly absent at inference. |
| CL-11 | WoTE and DynFlowDrive have the same world-to-action program | WoTE raw `:62-105`; DynFlow raw `:173-213` | SPLIT | They share candidate identity and a final scorer but differ in whether the candidate-conditioned world computation survives deployment. This is a lifecycle/causal-bridge difference, not a flow-vs-transformer difference. |
| CL-12 | SeerDrive's paper and code can be represented as one artifact | paper raw `:13-28,65-101`; `audits/literature/PHASE_C5_SEERDRIVE_AUDIT.md:23-73` | SPLIT | The paper has an explicit reciprocal world↔planning loop; the released code audit reports a later WoTE-like evaluation path without the paper loop. |
| CL-13 | SeerDrive is simply future-conditioned direct planning | paper raw `:89-101`; Set E; source audit | CORRECT | The feedback edge is route-defining. Whether its final resolver is candidate-based remains UNKNOWN, but it cannot be reduced to one-way future conditioning. |
| CL-14 | SeerDrive refinement iterations are physical future rollout | source audit `:142-152`; raw `:89-101` | CORRECT | The iterations are internal decision computation. They are not automatically physical-time transitions or environment feedback cycles. |
| CL-15 | GraphWorld performs explicit future rollout | GraphWorld raw `:18-31,43-81,229-247` | CORRECT | It learns a compact relational current-world state and uses target state for temporal supervision; the paper expressly rejects explicit multistep rollout. |
| CL-16 | GraphWorld is ordinary BEV/context and should not count as world reasoning | GraphWorld raw `:88-128,130-224`; Set C/E | CORRECT | ECIG/WSCP creates a relational, temporally grounded world object that conditions planning. It is a world-state bridge, though final commitment remains UNKNOWN. |
| CL-17 | Discrete-WAM's joint world-policy mode is its deployed planner route | Discrete-WAM raw `:55-67,85-190`; Set D | SPLIT | World, joint, and policy tasks are separate artifacts in one unified framework. The policy path is hierarchical decision→action; joint generation is not sufficient evidence of routine deployment. |
| CL-18 | A joint world/action objective automatically creates a joint-emission route | Discrete-WAM and Set D; Epona raw | REJECT | “Joint” must be unpacked into shared representation, training factorization, deployment generation, and final commitment. The word alone is not a mechanism. |
| CL-19 | Multiple random/diffusion samples create a candidate resolver | Epona/DriveLaW raw; D01.2 collision audit | REJECT | Candidate status requires identity preservation to a common resolver and final commitment. Sampling steps are solver mechanics. |
| CL-20 | RGB/BEV/latent/token, diffusion/flow, or encoder family define routes | all twelve raw files; Set A–E | REJECT | These are representation or solver choices unless they change the semantic causal interface. They remain audit attributes. |
| CL-21 | Training-only future branches can be marked as online future carriers | LAW, Metis, DynFlowDrive, WorldDrive lifecycle sections | CORRECT | Training graph and deployment graph must be written separately. A dropped branch can still be central to learning without being an online world object. |
| CL-22 | One paper must have one route | World4Drive/WorldDrive; Drive-JEPA; Discrete-WAM; SeerDrive paper/code | REJECT | The correct unit is a scoped artifact; paper-level lineage and artifact-level causal topology are related but not identical. |
| CL-23 | The previous compressed map is already the final field ontology | `outputs/core_mechanism_12_v1/14_ROUTE_COMPRESSION_AND_COLLISION_AUDIT.md`; `core_route_reconstruction/22` | UNKNOWN / HOLD | It is a useful regression baseline, but the canonical raw reconstruction shows unresolved route-vs-profile boundaries. No normative change is justified in this task. |

## Ledger conclusion

The strongest corrections are not new coordinate axes. They are ordering rules:

```text
paper/mode boundary
→ deployment graph
→ training graph
→ world-object lifecycle
→ candidate identity and commitment
→ only then family/profile comparison
```
