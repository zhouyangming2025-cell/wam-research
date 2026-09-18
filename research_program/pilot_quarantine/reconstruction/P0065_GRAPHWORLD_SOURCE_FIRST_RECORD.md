# P0065 GraphWorld — Source-First Record

Status: `READY-FOR-REVIEW`

Primary source: `papers/raw_md/P0065_GraphWorld/P0065_GraphWorld.raw.md`

Pinned source audit: `audits/literature/PHASE_C5_GRAPHWORLD_AUDIT.md`

Source status in the audit: no attributable official autonomous-driving implementation repository identified at audit time.

Historical route labels are intentionally absent.

## A. Author problem / gap ledger

| ID | Author-stated problem or gap | Evidence location | Status |
|---|---|---|---|
| GW-P1 | Existing end-to-end planners are described as short-horizon and weak at long-term temporal dependencies in interactive scenes. | Abstract; Introduction; Sec. 3 | `AUTHOR CLAIM` |
| GW-P2 | Explicit future-scene generation and multi-step rollout are described as computationally expensive for real-time planning. | Introduction; Sec. 2.2–3 | `AUTHOR CLAIM` |
| GW-G1 | The proposed gap is a compact ego-centric relational world state that conditions long-horizon planning without explicit long-horizon rollout. | Abstract; Introduction; Contributions | `AUTHOR CLAIM` |

## B. Neutral mechanism record

### B1. Current interaction/world representation

An ego-centered sparse interaction graph selects nearby agents. A GRU aggregates historical ego/agent states and map context; cross-attention injects interaction information into node-level latent states. This produces a structured current world state `W_cur`.

The paper also constructs a future-oriented target `W_tgt` from aggregated motion/planning hypotheses and map context. `W_tgt` is a training/flow target, not an encoder of a directly observed future scene.

### B2. Online flow refinement and planning

The model applies a short flow-matching refinement from `W_cur` toward `W_tgt` using an internal interpolation coordinate. The refined world state conditions agent-motion queries and ego-planning queries through importance reweighting and residual modulation, then multimodal heads decode trajectories.

The paper explicitly rejects interpreting this as explicit multi-step long-horizon world rollout. It also does not describe one candidate-specific future world per ego trajectory followed by a separate utility scorer.

### B3. Temporal supervision

Stage II uses the world state inferred at physical time t+1 as a stop-gradient consistency target for the state at t. This is factual future representation consistency, not explicit action-conditioned transition prediction.

## C. Five-question pilot projection

Status: `READY-FOR-REVIEW`

| Question | Provisional answer | Evidence status |
|---|---|---|
| Q1. Where does future-related computation occur? | In the ECIG/GRU interaction encoder and the flow-refined latent world-state branch, whose refined agent/ego states condition the motion and planning queries. | `PAPER FACT` |
| Q2. What is the future object, target, or intermediate representation? | A current structured interaction world state `W_cur`, a future-oriented planning/motion target `W_tgt`, and their internally flow-refined latent state. The flow coordinate is not established as physical future time, and `W_tgt` is not a directly encoded future observation. | `PAPER FACT` + `EVIDENCE BOUNDARY` |
| Q3. Does the future-related signal enter the forward action chain? | Yes. The refined world state remains online and conditions agent-motion and ego-planning query generation. It is not an online candidate-specific consequence scorer. | `PAPER FACT` |
| Q4. What role does the future mechanism play? | Online world-state-conditioned planning and interaction-aware query modulation, with temporal world-state consistency and task losses during training. | `PAPER FACT` + `OUR INFERENCE` |
| Q5. What remains at deployment? | ECIG, history/map world-state construction, short flow refinement, importance reweighting/residual modulation, and multimodal planning heads remain. Explicit long-horizon rollout and a separate risk/utility scorer are not reported. | `PAPER FACT` + `NOT REPORTED` |

Parallel provenance annotation: current interaction structure and temporal consistency are supported; candidate-specific action-conditioned future world prediction and reactive surrounding-agent intervention truth are not established.

## D. Evidence boundaries and unresolved items

- Long-horizon planning performance is not evidence of a six-second explicit world rollout.
- Flow solver steps are not physical future horizon.
- Bench2Drive evaluates the final policy reactively, but does not validate the internal latent world state as an intervention-correct future simulator.
- Exact tensor routing and solver implementation remain source-unverified.
