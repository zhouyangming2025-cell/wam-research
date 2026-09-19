# Core Anchor Source Completeness Audit

Last updated: 2026-09-15

Status: **HISTORICAL FIFTEEN-ANCHOR SOURCE SNAPSHOT — current paper scope and task authority live in `state/CURRENT_STATE.md` and `state/NEXT_TASK.md`.**

Purpose: keep separate:

```text
paper text available
!= deep analysis complete
!= official implementation exists
!= source-code mechanism verified
```

Scientific completeness is determined by provenance + evidence audit, not merely by whether a source tree exists locally.

## Status legend

```text
PAPER     canonical/raw paper text available
ANALYSIS  normalized deep analysis available
CODE      attributable official implementation exists publicly
AUDIT     decision-critical source paths audited at locked commit
PARTIAL   source exists/audit exists but does not fully cover reported mechanism/benchmark branch
BLOCKED   implementation unavailable/not identifiable
```

## Fifteen normalized anchors

| Paper | Paper/raw MD | Deep analysis | Official code status | Source audit status | Current source-layer judgment |
|---|---|---|---|---|---|
| P0048 LAW | PRESENT | COMPLETE | `BraveGroup/LAW` | COMPLETE, `b2f6a784247072923c477ab92324d3aa5a9759bf` | HIGH |
| P0045 WoTE | PRESENT | COMPLETE | `liyingyanUCAS/WoTE` | COMPLETE for decision-critical target/reactivity path, `298957c128a91d41a1c6075bd0bb6e7e845e093f` | HIGH |
| P0001 Epona | PRESENT | COMPLETE | `Kevin-thu/Epona` | COMPLETE core, `69b24c55f5ab8b3ffde8fa55e9f833bfe64d2c68` | SOURCE-COMPLETE core |
| P0042 WorldDrive | PRESENT | COMPLETE | `TabGuigui/WorldDrive` | COMPLETE/CORE, `c375ee1e1fe86ace175609db1ed90fd6db89673b` | HIGH |
| P0046 World4Drive | PRESENT | COMPLETE | `ucaszyp/World4Drive` | COMPLETE core; NAVSIM branch equivalence PARTIAL | HIGH with benchmark caveat |
| P0061 SeerDrive | PRESENT | COMPLETE | `LogosRoboticsGroup/SeerDrive` | released implementation audited | PARTIAL by design; public code is WoTE-integrated variant |
| P0049 Drive-JEPA | PRESENT | COMPLETE | `linhanwang/Drive-JEPA` | COMPLETE first-pass released NAVSIM paths | HIGH |
| P0062 Metis | PRESENT | COMPLETE | official repo attributable; implementation unreleased in audited state | BLOCKED | PAPER/README verified; SOURCE-UNVERIFIED |
| P0063 DynFlowDrive | PRESENT | COMPLETE | `xiaolul2/DynFlowDrive`, README/teaser only | BLOCKED | PAPER verified; SOURCE-UNVERIFIED |
| P0064 Discrete-WAM | PRESENT | COMPLETE | no attributable official implementation identified | BLOCKED / MONITOR | PAPER verified; SOURCE-UNVERIFIED |
| P0065 GraphWorld | PRESENT | COMPLETE | no attributable official autonomous-driving implementation identified | BLOCKED / MONITOR | PAPER verified; SOURCE-UNVERIFIED |
| P0009 DriveLaW | PRESENT | COMPLETE | `xiaomi-research/drivelaw` | COMPLETE core, `243e0e41148bdb1ae39ce1adf17d026e7cbd4348` | SOURCE-COMPLETE core / VERSION-PARTIAL exact paper reproduction |
| P0012 DA-WAM | PRESENT | COMPLETE | `LeapWM/da-wam`, README-only placeholder | BLOCKED | PAPER-COMPLETE / SOURCE-BLOCKED |
| P0002 SafeDrive | PRESENT | COMPLETE | `SPA-junghokim/SafeDrive` | COMPLETE core NAVSIM, `ea7791d6c2ebdeedfb6ed514f080cdfa1675b76f`; Bench2Drive PARTIAL | SOURCE-COMPLETE NAVSIM CORE / SOURCE-PARTIAL BENCH2DRIVE |
| **P0005 RiskWorld** | **PRESENT** | **COMPLETE** | **no attributable official implementation identified** | **BLOCKED / MONITOR** | **PAPER-COMPLETE / SOURCE-BLOCKED** |

---

# Core closed/high-confidence source anchors

## Epona

```text
Kevin-thu/Epona@69b24c55f5ab8b3ffde8fa55e9f833bfe64d2c68
```

Core planning/world interface source-verified.

## DriveLaW

```text
xiaomi-research/drivelaw@243e0e41148bdb1ae39ce1adf17d026e7cbd4348
```

Core online Video-DiT hidden→Action-DiT interface source-verified; exact paper benchmark commit remains version-partial.

## SafeDrive

```text
SPA-junghokim/SafeDrive@ea7791d6c2ebdeedfb6ed514f080cdfa1675b76f
```

Core NAVSIM ProposalNet→SWNet→FRNet and simulator-target generation source-verified. Bench2Drive implementation path remains unidentified.

---

# DA-WAM source boundary

Official repository:

```text
LeapWM/da-wam@1edbe555146a2d1fe9484f5c11f120860b8a4858
README only: "comming soon"
```

Final label:

```text
P0012 DA-WAM = PAPER-COMPLETE / SOURCE-BLOCKED
```

---

# RiskWorld source boundary

Canonical audit:

```text
papers/deep_analysis/P0005_RISKWORLD_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_RISKWORLD_AUDIT.md
```

Paper/version:

```text
RiskWorld: Object-Centric Latent World Modeling for Autonomous Driving Risk Identification
arXiv:2608.21414v1
submitted 2026-08-12
```

As of this audit:

```text
raw paper text             PRESENT
deep analysis              COMPLETE FIRST PASS
official implementation   NOT IDENTIFIED
```

False-positive guard:

```text
KevinWjk/RiskWorld
```

is unrelated to the paper. Its README is an Alpamayo 1.5 autonomous-driving release and MUST NOT be treated as RiskWorld source code.

Source-unverified details therefore include:

```text
exact V-JEPA2 object pooling implementation
structured state tensor layout
relation-attention masking implementation
RSSM prior/posterior parameterization details beyond paper equations
teacher-forcing / masking edge cases
exact stochastic sampling and deterministic evaluation path
runtime / batching behavior
```

Final label:

```text
P0005 RiskWorld = PAPER-COMPLETE / SOURCE-BLOCKED-MONITOR
```

---

# Current blocked/monitor set

```text
P0062 Metis
P0063 DynFlowDrive
P0064 Discrete-WAM
P0065 GraphWorld
P0012 DA-WAM
P0005 RiskWorld
```

Do not substitute unofficial reimplementations or same-name unrelated repositories for absent official code.

---

# Secondary partial items

```text
P0046 World4Drive NAVSIM branch equivalence
P0009 DriveLaW exact paper-benchmark commit
P0002 SafeDrive Bench2Drive implementation branch
```

These caveats must not downgrade already source-verified core mechanisms.

---

# False-positive guards

```text
google-research/graphworld
```

is unrelated to autonomous-driving GraphWorld.

```text
KevinWjk/RiskWorld
```

is unrelated to the RiskWorld paper and currently contains Alpamayo 1.5 material.

---

# Source snapshot governance note

An Epona source snapshot was historically imported under `repos/Epona/` despite `.gitignore` normally excluding external `repos/`. Future external source checkouts should follow a deliberate normalized policy rather than mixing vendored snapshots and local-only clones accidentally.

---

# Canonical source-completeness rule

For every anchor record independently:

```text
canonical paper/version
raw_md present?
supplement/appendix captured?
official repo attributable?
release state: full / partial / README-only / absent
locked audited commit
training code available?
inference code available?
evaluation code available?
checkpoint/config available?
source audit complete?
paper↔code consistency?
unresolved source questions
```

Completion labels:

```text
PAPER-COMPLETE
SOURCE-COMPLETE
SOURCE-PARTIAL
SOURCE-BLOCKED
```

No paper should be called simply `COMPLETE` when source-level evidence is decision-critical unless the qualifier is explicit.
