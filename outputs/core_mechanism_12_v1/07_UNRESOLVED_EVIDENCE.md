# Core Mechanism 12 — Unresolved Evidence Ledger after Phase 0–1

Status: open issues only. These entries bound claims in 00_SCOPE_AND_ARTIFACTS.md and 01_PAPER_MECHANISM_GRAPHS.md; they are not permission to infer missing facts.

## 1. Severity convention

- BLOCKS ARTIFACT: artifact identity or deployment path cannot be fixed without resolution.
- BLOCKS EDGE: a specific graph edge must remain UNKNOWN.
- VERSION BOUNDARY: paper and source can both be represented, but must not be collapsed.
- NON-BLOCKING: the Phase 0–1 graph is stable; the issue matters for later classification or replication.

No current item blocks the existence of the 21 frozen artifacts. Several items block stronger edge or implementation claims.

## 2. Open evidence items

| ID | Artifact(s) | Severity | Unresolved point | Current safe statement | Next evidence needed |
|---|---|---|---|---|---|
| U-001 | LAW-PF, LAW-PB | VERSION BOUNDARY | exact arXiv/PDF revision of the raw corpus copy | title/mode identity is fixed; PDF revision is UNKNOWN | first-page metadata or source PDF checksum mapped to arXiv revision |
| U-002 | LAW-PB | BLOCKS EDGE | perception-based target detach and exact gradient topology | paper-level training edges only; do not copy LAW-PF code detach as fact | official perception-based training implementation at pinned commit |
| U-003 | LAW-PF | NON-BLOCKING | whether appendix autoregressive future-latent variant was used in any reported primary result | canonical deployed path remains direct waypoint output | exact experiment/config mapping |
| U-004 | EPO-PLAN/SELF/CTRL | VERSION BOUNDARY | exact arXiv revision represented by the ICCV 2025 raw text | conference identity and inspected source path are fixed | PDF front page/version metadata |
| U-005 | EPO-SELF | NON-BLOCKING | full schedule/frequency of chain-of-forward detached-context training | detached periodic self-context use is established; frequency details should not be generalized | training config and scheduler trace |
| U-006 | DLAW-PAPER, DLAW-CODE | VERSION BOUNDARY | paper says five action-flow steps while released code/config surfaces ten and five in different places | retain separate paper and code artifacts; avoid one universal step count | exact checkpoint config and evaluation command used for each reported table |
| U-007 | DLAW-PAPER/CODE | BLOCKS EDGE | sign convention differs between paper flow equation and source target | source target and paper equation must be quoted separately; do not algebraically normalize without provenance | author clarification or corrected revision |
| U-008 | W4D-PLAN | NON-BLOCKING | public source benchmark coverage, especially whether every reported NAVSIM path is represented by the inspected release | core candidate-future-score path is verified; benchmark-wide code coverage is not | official benchmark-specific config/checkpoint mapping |
| U-009 | W4D-PLAN | BLOCKS EDGE | exact detach/freeze placement for factual future encoding across all stages/configs | losses and candidate matching are established; unspecified detach edges remain UNKNOWN | forward/loss code for each training stage and active config |
| U-010 | WD-PLAN | NON-BLOCKING | exact number K after top-K filtering for every reported checkpoint | runtime uses top-K candidates; no universal K asserted | checkpoint config per result table |
| U-011 | WD-PLAN | BLOCKS EDGE | full teacher-output detach and encoder-freeze topology across distillation variants | heavy teacher is frozen and absent at runtime at paper level; variant-specific gradients remain bounded | exact trainer and config for each ablation |
| U-012 | WOTE-PLAN | VERSION BOUNDARY | exact arXiv/PDF revision of the raw corpus copy | mechanism and pinned source are fixed; paper revision is UNKNOWN | front-page metadata or PDF checksum mapping |
| U-013 | WOTE-PLAN | NON-BLOCKING | exact semantics of all surrounding-agent futures in every simulator/config variant | inspected setup varies candidate ego motion while using logged/fixed surroundings | simulator config and data-generation scripts for each benchmark |
| U-014 | WOTE-PLAN | BLOCKS EDGE | paper reward-selection formula/wording has sign or ordering ambiguity in places | deployed source selects highest final learned reward; preserve paper wording separately | corrected equation or author clarification |
| U-015 | SEER-PAPER | BLOCKS EDGE | exact deployed final resolver among trajectory modes | final-mode resolution remains UNKNOWN | official evaluation code matching paper mechanism or explicit algorithm statement |
| U-016 | SEER-PAPER, SEER-CODE | VERSION BOUNDARY | initial release implements a WoTE-style evaluator/refiner rather than the paper’s repeated co-refinement loop | keep two artifacts; never use release code as proof of the paper loop | later official commit implementing paper loop or author mapping |
| U-017 | SEER-CODE | NON-BLOCKING | whether later source commits change num_fut_timestep or rescore after refinement | initial release has one future endpoint and no second resolution | audit later tagged releases/checkpoints |
| U-018 | DJEPA-PF/PB1/PB2 | NON-BLOCKING | exact paper-table mapping to code v1 versus v2 perception-based directories | three source paths are fixed; result attribution may vary | official evaluation commands/checkpoint manifest |
| U-019 | DJEPA-PB2 | NON-BLOCKING | provenance of previous trajectory under each evaluation harness: executed, simulated, or cached planned | comfort recalibration consumes a previous-trajectory signal; its harness-specific provenance must be stated | agent runner/evaluator trace |
| U-020 | METIS-PLAN | BLOCKS EDGE | executable implementation and exact detach/freeze topology unavailable | paper asserts visual loss can backpropagate through predicted action conditioning | official source release and pinned training code |
| U-021 | METIS-PLAN | VERSION BOUNDARY | paper text surfaces inconsistent VGE capacity labels, including Wan2.2-5B versus 14B ablation wording | no single capacity is treated as universal | corrected model card/config per result |
| U-022 | DFD-PLAN | BLOCKS EDGE | flow interpolation derivative, equation sign, and sampling anchor are mutually ambiguous in the paper text | flow model is training-only and supervises scorer; numerical update rule remains bounded | official source or corrected derivation |
| U-023 | DFD-PLAN | BLOCKS EDGE | executable source unavailable for detach and joint-gradient verification | paper-level joint objectives only | official repository with pinned commit |
| U-024 | DWAM-POLICY/JOIN | BLOCKS EDGE | whether headline planning metrics invoke policy-only decoding or generate visual tokens jointly | paper identifies policy-only as the primary path; joint generation is a separate capability artifact | exact evaluation command and checkpoint mode |
| U-025 | DWAM-POLICY | NON-BLOCKING | decision-token decoding details: deterministic argmax, sampling, or another rule | one of 400 decision labels conditions action editing; do not treat labels as scored trajectory candidates | source/evaluation pseudocode |
| U-026 | DWAM all | BLOCKS EDGE | no verified official executable source, including token-edit schedule and cache behavior | paper-level edges only | official source and pinned commit |
| U-027 | GW-PLAN | BLOCKS EDGE | exact final resolver among ego planning modes | final ego-mode resolution remains UNKNOWN | official evaluation source or explicit algorithm |
| U-028 | GW-PLAN | BLOCKS EDGE | exact temporal alignment of W_t, W_t+1, flow endpoint, and stopped target | stage-II stopped temporal consistency is established; endpoint semantics remain bounded | source implementation or corrected notation |
| U-029 | GW-PLAN | BLOCKS EDGE | executable source unavailable for two-step solver and gradient verification | paper-level structured carrier and two-step flow only | official source and pinned commit |
| U-030 | all candidate methods | NON-BLOCKING | candidate-specific predictions are sometimes trained against one factual future and should not be described as observed counterfactual futures | candidate identity and factual-target multiplicity are separately recorded | no new evidence required; enforce terminology in later phases |

## 3. Verified negative facts that should not be reopened without new evidence

These are not unknowns:

- LAW future-latent prediction is not consumed by the inspected deployed waypoint output.
- Epona planning-only evaluation can skip visual generation.
- DriveLaW does not require full future-video denoising/decoding for planning.
- WorldDrive’s heavy trajectory-aware diffusion teacher is absent at runtime.
- Drive-JEPA’s JEPA predictor and EMA target encoder are absent from downstream deployment.
- Metis action-only deployment bypasses its visual-generation expert.
- DynFlowDrive removes the flow world model from deployment.
- Discrete-WAM’s GRPO groups are training samples, not by themselves a runtime candidate bank.
- GraphWorld’s two flow steps are not two physical future-time transitions.

Any later reversal requires newly cited paper or code evidence, not a reinterpretation of terminology.

## 4. Phase 0–1 review checklist

A reviewer should verify:

1. Every artifact in 00_SCOPE_AND_ARTIFACTS.md has at least one deployment DAG and its relevant learning DAG.
2. Every runtime candidate set preserves or explicitly loses candidate identity before A*.
3. Every future/world carrier is marked runtime, training-only, output-only, or absent.
4. Every score/resolver is placed before A* or explicitly marked UNKNOWN.
5. Solver coordinate, intra-decision refinement, and physical time are not conflated.
6. Paper/code mismatches are represented by separate artifacts or explicit version boundaries.
7. No ontology labels have entered the Phase 1 reconstruction.

## 5. Stop gate

Phase 0–1 is ready for user review. Work must stop here.

Do not begin ontology construction, cross-paper category assignment, collision testing, old-draft comparison, or engineering synthesis until explicit approval is received.
