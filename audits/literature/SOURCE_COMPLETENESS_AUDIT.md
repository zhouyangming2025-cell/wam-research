# SOURCE_COMPLETENESS_AUDIT

Last updated: **2026-09-15**

Purpose: distinguish **paper-text completeness**, **official-source availability**, **source-code audit completeness**, and **local clone availability** for the normalized core-WAM anchors.

Binding principle:

```text
paper-verified != source-verified
source repo exists != source audit complete
source audit complete != local clone committed to wam-research
```

The canonical repository intentionally excludes full external source checkouts:

```text
repos/
```

is gitignored. Therefore full official repositories should remain as **local ignored clones** when needed; only source provenance, audited commit, decisive files/functions, and scientific conclusions belong in `wam-research`.

---

# 1. Current ten-anchor status

| Paper | Paper/raw-MD layer | Official repository | Public implementation status | Source audit status in wam-research | Current completeness class | Immediate action |
|---|---|---|---|---|---|---|
| **LAW** | PRESENT | `BraveGroup/LAW` | code available | **SOURCE-VERIFIED** at `b2f6a784247072923c477ab92324d3aa5a9759bf` | **A — paper + decisive source path closed** | optional local clone/pin only |
| **WoTE** | PRESENT | `liyingyanUCAS/WoTE` | code available | **SOURCE-VERIFIED** at `298957c128a91d41a1c6075bd0bb6e7e845e093f` | **A** | optional local clone/pin only |
| **Epona** | PRESENT | `Kevin-thu/Epona` | **full code available** (`configs/`, `models/`, `dataset/`, `scripts/`, `data_preparation/`) | **NOT YET SOURCE-AUDITED TO CURRENT STANDARD** | **B — actionable gap** | **HIGH PRIORITY: clone/pin + source audit now** |
| **WorldDrive** | PRESENT | `TabGuigui/WorldDrive` | code/checkpoints available | **SOURCE-VERIFIED** at `c375ee1e1fe86ace175609db1ed90fd6db89673b` | **A** | optional local clone/pin only |
| **World4Drive** | PRESENT | `ucaszyp/World4Drive` | released code available | **SOURCE-VERIFIED** at `cffb51adeb1f7d02b49c4b74d7262ded62a33ac8` | **A**, with NAVSIM branch caveat | optionally search for missing NAVSIM-specific implementation path |
| **SeerDrive** | PRESENT | `LogosRoboticsGroup/SeerDrive` | code available, but public release is a **post-paper WoTE-integrated variant** | **VERSION-BOUNDARY SOURCE AUDIT COMPLETE**; initial public release commit `1cfb7ecdbdbbe52fd598949efe4edf8f6fb12b69` | **B+ — source exists but does not reproduce original paper graph exactly** | keep paper/source artifacts separate; no forced reconciliation |
| **Drive-JEPA** | PRESENT | `linhanwang/Drive-JEPA` | code available | **SOURCE-VERIFIED** at `e21f47410b4d26b61f05f9bd23e169c0390cae2a` | **A**, with Bench2Drive code still TODO in audited release | optional local clone/pin; monitor Bench2Drive release |
| **Metis** | PRESENT | `LogosRoboticsGroup/Metis` | **implementation not released**; repo still README/assets-level | **SOURCE-UNVERIFIED by external blockage** | **C — blocked by authors** | monitor only; do not fabricate implementation evidence |
| **DynFlowDrive** | PRESENT | `xiaolul2/DynFlowDrive` | **implementation not released**; repo says code after acceptance | **SOURCE-UNVERIFIED by external blockage** | **C — blocked by authors** | monitor only; do not fabricate implementation evidence |
| **Discrete-WAM** | PRESENT | official implementation repo **not identified** as of audit date | no attributable public implementation found | **SOURCE-UNVERIFIED** | **C/D — repo identity unresolved** | monitor/search; do not use similarly named repos |

---

# 2. Evidence behind the classification

## LAW / WoTE

Canonical source audit:

```text
audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md
```

LAW decisive source facts include:

```text
cur_waypoint is computed before wm_next_latent
future-latent loss is training supervision
test-time trajectory path discards latent outputs
```

WoTE decisive source facts include:

```text
candidate ego trajectories are simulated separately
shared cached surrounding observation is used across candidates in audited NAVSIM/PDM path
```

## Epona — actionable gap

Official repository confirmed:

```text
Kevin-thu/Epona
latest observed main commit:
69b24c55f5ab8b3ffde8fa55e9f833bfe64d2c68
```

Repository exposes real implementation directories including:

```text
models/model.py
models/stt.py
models/traj_dit.py
models/flux_dit.py
models/diffusion/
configs/
dataset/
scripts/
data_preparation/
```

Current normalized paper analysis:

```text
papers/deep_analysis/P0001_EPONA_DEEP_ANALYSIS_V2.md
```

is principally paper/raw-MD based and should now receive a source-level companion audit.

Required source questions:

```text
1. exact MST/STT historical-state construction
2. exact shared latent F tensor and where it splits
3. whether TrajDiT and VisDiT share any parameters beyond MST/shared representation
4. action-conditioning path into VisDiT
5. exact training loss attachment and detach/freeze boundaries
6. whether visual loss backpropagates through shared F/MST
7. exact planning-only inference graph
8. whether VisDiT is actually skipped in planning evaluation code
9. autoregressive visual rollout path and teacher-forcing/self-generated-context semantics
10. sampling-step defaults and planning latency path
11. checkpoints/configs corresponding to reported planning vs video experiments
12. any paper↔code mismatch
```

## WorldDrive / World4Drive

Canonical source audits:

```text
audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md
audits/literature/PHASE_C5_WORLD4DRIVE_AUDIT.md
```

Both have commit-locked mechanism evidence. World4Drive still carries one bounded gap: the released source audit verifies the core W4D implementation, but a distinct NAVSIM-specific implementation path was not established.

## SeerDrive

Canonical source/version audit:

```text
audits/literature/PHASE_C5_SEERDRIVE_AUDIT.md
```

Important boundary:

```text
NeurIPS paper = iterative future-BEV <-> planner co-refinement
public release = WoTE-integrated online evaluation/selection path
```

The available source must not be used to overwrite the paper mechanism.

## Drive-JEPA

Canonical source audit:

```text
audits/literature/PHASE_C5_DRIVEJEPA_AUDIT.md
```

Implementation-level planner, proposal refinement, scorer, and NAVSIM-v2 momentum recalibration are source-verified. Bench2Drive implementation remained TODO in the audited official release.

## Metis / DynFlowDrive

As of 2026-09-15:

```text
Metis:
official repo exists, but training/inference/evaluation implementation is still unreleased.

DynFlowDrive:
official repo exists, but README still states code will be released after acceptance.
```

These are **external evidence gaps**, not local research-work failures.

## Discrete-WAM

Raw paper text and normalized analysis are present:

```text
papers/raw_md/P0064_Discrete-WAM/P0064_Discrete-WAM.raw.md
papers/deep_analysis/P0064_DISCRETE_WAM_DEEP_ANALYSIS_V2.md
```

No attributable official implementation repository has been identified. Until an author/project link appears:

```text
paper mechanism = PAPER-VERIFIED
implementation details = SOURCE-UNVERIFIED
```

---

# 3. Paper / Markdown completeness

For the ten normalized anchors above, the **primary paper text layer is present** in the repository and each normalized analysis has a paper/raw-MD source path.

What has **not** yet been audited systematically is **supplement completeness**.

This is now a separate completeness field:

```text
primary paper raw MD         = PRESENT for current anchors
supplement raw MD            = NOT SYSTEMATICALLY AUDITED
appendix inside main raw MD   = paper-dependent
canonical PDF                = local/NAS only, intentionally not GitHub
```

A local agent may therefore audit whether an official supplementary PDF / appendix exists and whether its scientific content is already present in the raw-MD layer. Missing supplements may be converted to text/Markdown while keeping PDFs local/NAS only.

---

# 4. Local source-clone policy

`wam-research/.gitignore` excludes:

```text
repos/
```

Therefore the preferred source arrangement is:

```text
wam-research/
  repos/                         # LOCAL ONLY, ignored
    LAW/
    WoTE/
    Epona/
    WorldDrive/
    World4Drive/
    SeerDrive/
    Drive-JEPA/

  audits/literature/             # committed scientific source audits
  evidence/                      # compact committed source evidence if needed
```

Do **not** vendor entire upstream repositories into GitHub merely to make the knowledge repo self-contained. Pin source identity by:

```text
repo URL
commit SHA
audit date
key files/functions
paper↔source consistency result
```

---

# 5. Immediate source-completion queue

Priority order:

```text
P0  Epona source audit                 DO NOW
P1  ten-anchor supplement/raw-MD audit DO NOW
P1  local clone/pin inventory          DO NOW if local machine has network/storage
P2  World4Drive NAVSIM source path     SEARCH / VERIFY
P2  Drive-JEPA Bench2Drive source      MONITOR / SEARCH
P3  Metis implementation               BLOCKED — monitor
P3  DynFlowDrive implementation        BLOCKED — monitor
P3  Discrete-WAM official repo         IDENTITY SEARCH / monitor
```

---

# 6. Completion definitions going forward

Use these labels consistently:

```text
PAPER-COMPLETE
    canonical paper/raw-MD available and mechanism can be reconstructed

PAPER+SUPPLEMENT-COMPLETE
    primary text + official supplementary material audited

SOURCE-AVAILABLE
    attributable official implementation exists

SOURCE-VERIFIED
    decisive mechanism claims traced to a pinned source commit

VERSION-BOUNDARY-VERIFIED
    source exists but does not correspond exactly to the paper mechanism; difference recorded

SOURCE-BLOCKED
    official authors have not released implementation

SOURCE-IDENTITY-UNRESOLVED
    no trustworthy official implementation repository identified
```

A paper is **not** promoted to `SOURCE-VERIFIED` merely because a GitHub link exists.

---

# 7. Current overall verdict

```text
paper/raw-MD completeness:          HIGH
normalized deep-analysis coverage: HIGH
source-code availability:          MIXED
source-code audit completeness:    GOOD but NOT COMPLETE
```

The largest currently actionable gap is **Epona**. The remaining major source gaps are mostly externally blocked rather than forgotten local work.
