# D01 Domain Census Report

## Result

D01 accounts for all 26 prescribed works without assigning any ontology signature. The census finds 19 in-domain papers, 7 boundary papers, and no outright exclusions. The in-domain set expands to 23 materially distinct artifacts/modes: 19 planning or policy-learning paths and four separately traceable generation/simulation/direct-policy modes whose terminal output or deployment lifecycle differs.

The evidence-depth distribution is 19 at RD2 and 7 at RD3. No work is claimed at code-audited depth. Existing repository evidence was reused before external lookup; the three papers absent from the local corpus (SimWAM, DriveFuture, and RaWMPC) were checked against their primary arXiv records. Exact identities, sources, and limitations are in `01_PAPER_SCOPE_TABLE.md` and `05_SOURCE_AND_DEPTH_LOG.md`.

## Domain rule applied

A work is in-domain only when a separately traceable predictive/world operation has a material connection to one-stage driving action formation, selection, optimization, or policy learning. Author terminology alone is insufficient. A predictive branch may be retained online, removed after transferring information into the deployed policy, or used as an action-conditioned training environment; these lifecycle variants are recorded explicitly rather than collapsed.

Boundary placement was used for: a risk monitor without a planner connection, a standalone reward model, direct trajectory planners without a separately traceable predictive object, an interactive prediction/planning predecessor, a world generator without a demonstrated one-stage planning path, and a simulator platform rather than a deployed planner.

## Main findings

1. The broad domain is not synonymous with online rollout. ViDAR, DriveWorld, ReWorld, WA-JEPA, and SimWAM transfer predictive information into a deployed planner while dropping or bypassing part of the predictive machinery.
2. Joint world/action generation needs mode-level accounting. Drive-WM, DrivingGPT, Gen-Drive, and CausalDrive each contain paths with different terminal outputs or decision roles.
3. Candidate generation is not enough to establish planning use of uncertainty. Several methods produce multiple futures, but only methods with an evidenced evaluator, cost, value, or optimization step are recorded as consuming alternatives.
4. Reactive claims remain fragile under logged-data supervision. SafeDrive, Gen-Drive, CausalDrive, and RaWMPC condition predicted consequences on ego choices, but behavioral validity under unseen interventions is not uniformly established.
5. The protocol successfully rejects strong adjacent systems without forcing them into the domain, but three global rules still need review: training-environment membership, planning-oriented pretraining membership, and reward-model attachment. These are documented in `06_PROTOCOL_ISSUES.md`.

## Completeness check

- Prescribed works accounted for: 26/26.
- Scope verdicts: 26/26.
- In-domain papers with artifact enumeration: 19/19.
- Enumerated artifacts/modes: 23.
- Neutral mechanism skeletons: 23/23.
- Training/runtime lifecycle stated: 23/23.
- Boundary items kept out of Tier 1 evidence: 7/7.
- Insufficient evidence is recorded as `UNKNOWN`; no gap was repaired by inference.
- No existing ontology output or research-program protocol file was modified.

## Deliverables

- `01_PAPER_SCOPE_TABLE.md`: paper-level identity, scope, evidence tier, depth, and confidence.
- `02_ARTIFACT_LEDGER.md`: mode-level lifecycle and planning topology.
- `03_MECHANISM_SKELETONS.md`: ontology-free mechanism DAGs and census fields.
- `04_BOUNDARY_AND_EXCLUSION_LOG.md`: auditable missing-property record.
- `05_SOURCE_AND_DEPTH_LOG.md`: evidence provenance and achieved reading depth.
- `06_PROTOCOL_ISSUES.md`: unresolved global rules and proposed fixes.
