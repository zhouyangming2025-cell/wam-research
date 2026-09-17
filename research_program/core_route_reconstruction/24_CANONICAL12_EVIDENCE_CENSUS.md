# Canonical-12 Relevant Evidence Census

Status: **working audit record; not an ontology update and not a route taxonomy**.

Branch: `codex/canonical12-mechanism-reconstruction`
Base: `origin/research/core-route-reconstruction` @ `5a775472fae2815cf306e8cb4a5a10073e921f9b`
## 0. Freeze and restoration check

The repository was fetched before selecting the working branch. The selected base is the branch that contains the canonical-route reconstruction lineage, rather than the older D02 census branch.

Read-only checks at the start of this run:

```text
git status --short                 clean
git diff --cached --name-status    empty
git diff --cached --summary        empty
```

No staged `R* old_path new_path` rename existed. No restore operation was needed. The raw paper directory was not rewritten. No commit or push is part of this run.

## 1. Evidence hierarchy

The following order is used for mechanism claims:

1. canonical paper Markdown under `papers/raw_md/`;
2. pinned official source audits, only for implementation and version facts;
3. prior deep analyses, mechanism graphs, relationship matrices, and collision audits, used as hypotheses to verify or reject;
4. external surveys and broader-corpus material, used only for pressure tests and completeness checks.

Each claim in the reconstruction is marked implicitly or explicitly as one of:

```text
PAPER FACT       stated or equation-supported by the raw paper
CODE FACT        supported by a source/version audit
AUTHOR CLAIM     paper framing not by itself sufficient to prove the graph
OUR INFERENCE    reconstruction from several paper facts
UNKNOWN          the frozen evidence cannot close the boundary
```

## 2. Canonical raw-paper corpus

All twelve canonical raw Markdown files were found locally and read for the mechanism-relevant sections, including method, training, inference, ablation, and limitations where present. The line count is included so that a later audit can detect a changed source artifact.

| Paper | Raw Markdown | Lines | Full-read status | Primary mechanism sections |
|---|---|---:|---|---|
| LAW | `papers/raw_md/P0048_LAW/P0048_LAW.raw.md` | 377 | READ | §1, §3, §4.1–§4.3, Appendix A |
| Epona | `papers/raw_md/P0001_Epona/P0001_Epona.raw.md` | 387 | READ | Abstract, §1, §3.2–§3.5, §4.3–§4.4 |
| DriveLaW | `papers/raw_md/P0009_DriveLaW/P0009_DriveLaW.raw.md` | 385 | READ | Abstract, §1, §3.1–§3.5 |
| World4Drive | `papers/raw_md/P0046_World4Drive/P0046_World4Drive.raw.md` | 343 | READ | Abstract, §3.1–§3.4, §4.4 |
| WorldDrive | `papers/raw_md/P0042_WorldDrive/P0042_WorldDrive.raw.md` | 405 | READ | Abstract, §3.1–§3.4, Appendix §6.1–§6.3 |
| WoTE | `papers/raw_md/P0045_WoTE/P0045_WoTE.raw.md` | 338 | READ | §1, §3.1–§3.4, §4.4 |
| SeerDrive | `papers/raw_md/P0061_SeerDrive/P0061_SeerDrive.raw.md` | 437 | READ | Abstract, §1, §3.2–§3.6, Appendix §E–§F |
| Drive-JEPA | `papers/raw_md/P0049_DriveJEPA/P0049_DriveJEPA.raw.md` | 721 | READ | §1, §3.1–§3.6, Appendix §A–§C |
| Metis | `papers/raw_md/P0062_Metis/P0062_Metis.raw.md` | 522 | READ | Abstract, §1, §3.1–§3.4, Appendix §A–§D |
| DynFlowDrive | `papers/raw_md/P0063_DynFlowDrive/P0063_DynFlowDrive.raw.md` | 410 | READ | §1, §3.1–§3.4 |
| Discrete-WAM | `papers/raw_md/P0064_Discrete-WAM/P0064_Discrete-WAM.raw.md` | 1172 | READ | §2, §3.1–§3.2, Appendix §7.2 |
| GraphWorld | `papers/raw_md/P0065_GraphWorld/P0065_GraphWorld.raw.md` | 616 | READ | §1, §3, §4.1–§4.3, §6 |

## 3. Prior reconstruction and audit corpus

| Corpus | Files read or checked | Role in this run | Final read status |
|---|---|---|---|
| Core route lineage | `research_program/core_route_reconstruction/00*.md` and `01–23*.md` | prior hypotheses, paper-first resets, counterexamples, and open debts | READ |
| Mechanism-graph baseline | `outputs/core_mechanism_12_v1/00_SCOPE_AND_ARTIFACTS.md`, `01_PAPER_MECHANISM_GRAPHS.md`, `02_ONTOLOGY_SPEC.md`, `03–09*.md`, `12–15*.md` | historical projections and collision claims to audit, not authority | READ |
| D01/D01.2 regression | `research_program/ontology_regression/d01_2/**`, `d01_2_r1/**`, `d01_2_r2/**` | frozen pressure cases, composition amendment, and known false-merge tests | READ |
| D01.3 blind test | `research_program/ontology_blind_test/d01_3/**` | unseen-paper validation and D02 entry boundary | READ |
| Deep analysis | the twelve matching files under `papers/deep_analysis/` | paper-specific claim ledger and evidence cross-check | READ |
| Source audits | matching `audits/literature/PHASE_C5_*` and `PHASE_C6_*` files; especially SeerDrive, Epona, Drive-JEPA, Metis, DynFlowDrive, Discrete-WAM, GraphWorld, World4Drive, WorldDrive, DriveLaW | code/version and paper/code separation | READ where present |
| Synthesis audits | relevant files under `audits/research_synthesis/` | previous comparison conclusions and evidence-completeness warnings | READ |
| External calibration | `research_program/core_route_reconstruction/23_EXTERNAL_SURVEY_CALIBRATION.md` and cited broader-corpus audits | counterexample and domain-pressure only | READ |

The old material is deliberately not treated as a ready-made label map. In particular, old route codes and old field signatures are not used in the neutral records below.

## 4. Evidence boundaries found before synthesis

1. A paper's world-generation capability, planning deployment path, and optional simulator path are often different artifacts.
2. A future target used for loss is not automatically an online future carrier.
3. A shared backbone is not automatically a world-to-action edge; the semantic object consumed by the action head must be identified.
4. Candidate identity is decisive: multiple outputs become a candidate route only when identities survive to a common resolver and one output is committed.
5. A scorer's preference semantics alone is not a stable route axis. Future construction, lifecycle, and commitment topology carry more information.
6. Paper/code divergence is material for SeerDrive and must not be silently repaired by replacing the paper graph with the released implementation.
7. Drive-JEPA PF/PB and Discrete-WAM policy/world/joint modes are artifact boundaries first; they are not automatically separate paper lineages.
