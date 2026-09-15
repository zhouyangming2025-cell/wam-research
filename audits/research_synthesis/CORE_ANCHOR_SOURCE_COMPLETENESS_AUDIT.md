# Core Anchor Source Completeness Audit

Last updated: 2026-09-15

Status: **ACTIVE — thirteen-anchor source-layer completeness tracking during WAM expansion**

Purpose: keep separate:

```text
paper text available
!= deep analysis complete
!= official implementation exists
!= source-code mechanism verified
```

Scientific completeness is determined by provenance + evidence audit, not merely by whether a source tree is present under `repos/`.

## Status legend

```text
PAPER     canonical/raw paper text available
ANALYSIS  normalized deep analysis available
CODE      attributable official implementation exists publicly
AUDIT     decision-critical source paths audited at locked commit
PARTIAL   source exists/audit exists but does not fully cover reported mechanism/benchmark branch
BLOCKED   implementation unavailable/not identifiable
```

## Thirteen normalized anchors

| Paper | Paper/raw MD | Deep analysis | Official code status | Source audit status | Current source-layer judgment |
|---|---|---|---|---|---|
| P0048 LAW | PRESENT | COMPLETE | `BraveGroup/LAW` | **COMPLETE**, `b2f6a784247072923c477ab92324d3aa5a9759bf` | HIGH |
| P0045 WoTE | PRESENT | COMPLETE | `liyingyanUCAS/WoTE` | **COMPLETE for decision-critical target/reactivity path**, `298957c128a91d41a1c6075bd0bb6e7e845e093f` | HIGH |
| P0001 Epona | PRESENT | COMPLETE | `Kevin-thu/Epona` | **COMPLETE for core mechanism**, `69b24c55f5ab8b3ffde8fa55e9f833bfe64d2c68` | **SOURCE-COMPLETE for planning/world interface** |
| P0042 WorldDrive | PRESENT | COMPLETE | `TabGuigui/WorldDrive` | COMPLETE/CORE, `c375ee1e1fe86ace175609db1ed90fd6db89673b` | HIGH |
| P0046 World4Drive | PRESENT | COMPLETE | `ucaszyp/World4Drive` | COMPLETE core interface, `cffb51adeb1f7d02b49c4b74d7262ded62a33ac8`; NAVSIM branch equivalence PARTIAL | HIGH with benchmark-branch caveat |
| P0061 SeerDrive | PRESENT | COMPLETE | `LogosRoboticsGroup/SeerDrive` | COMPLETE version/source audit for released implementation | **PARTIAL by design:** public code is WoTE-integrated variant, not clean original-paper iterative graph |
| P0049 Drive-JEPA | PRESENT | COMPLETE | `linhanwang/Drive-JEPA` | COMPLETE first-pass source audit across released NAVSIM paths | HIGH |
| P0062 Metis | PRESENT | COMPLETE | attributable official repo, implementation unreleased in audited state | **BLOCKED** | PAPER/README verified; implementation SOURCE-UNVERIFIED |
| P0063 DynFlowDrive | PRESENT | COMPLETE | `xiaolul2/DynFlowDrive`, README/teaser only in audited state | **BLOCKED** | PAPER verified; implementation SOURCE-UNVERIFIED |
| P0064 Discrete-WAM | PRESENT | COMPLETE | no attributable official implementation identified | **BLOCKED / MONITOR** | PAPER verified; scheduler/detach/task-routing SOURCE-UNVERIFIED |
| P0065 GraphWorld | PRESENT | COMPLETE | no attributable official autonomous-driving implementation identified | **BLOCKED / MONITOR** | PAPER verified; graph/flow/runtime implementation SOURCE-UNVERIFIED |
| **P0009 DriveLaW** | PRESENT | COMPLETE | `xiaomi-research/drivelaw` | **COMPLETE FIRST-PASS core training/inference audit**, `243e0e41148bdb1ae39ce1adf17d026e7cbd4348` | **SOURCE-COMPLETE for core world→policy interface, with paper-commit/version caveat** |
| **P0012 DA-WAM** | PRESENT | COMPLETE | `LeapWM/da-wam`, README-only placeholder | **BLOCKED** | **PAPER-COMPLETE; official implementation SOURCE-UNVERIFIED** |

---

# Epona actionable gap — CLOSED

Canonical audit:

```text
audits/literature/PHASE_C5_EPONA_SOURCE_AUDIT.md
evidence/P0001_EPONA_SOURCE_EVIDENCE.md
```

Locked source:

```text
Kevin-thu/Epona@69b24c55f5ab8b3ffde8fa55e9f833bfe64d2c68
```

Core verified facts:

```text
shared STT/MST feature feeds TrajDiT and visual FluxDiT;
planning can run traj_only=True and skip visual generation;
future visual output is not consumed by same-step planning;
training visual condition uses factual/logged ego motion;
self-generated rollout uses predicted motion to condition visual generation;
visual loss shapes shared STT/MST but not TrajDiT directly;
long rollout feeds generated visual latent + predicted ego motion back into the next physical step;
outer physical rollout != inner diffusion/flow solver iteration.
```

Final label:

```text
P0001 Epona = SOURCE-COMPLETE FOR CORE MECHANISM
```

---

# DriveLaW source boundary

Canonical audits:

```text
papers/deep_analysis/P0009_DRIVELAW_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_DRIVELAW_AUDIT.md
```

Locked source used for current audit:

```text
xiaomi-research/drivelaw@243e0e41148bdb1ae39ce1adf17d026e7cbd4348
```

Core source-verified facts:

```text
planning uses Video-DiT internal block states as Action-DiT conditioning;
canonical evaluation configs set return_action=true, return_video=false;
planning does not require full future-video denoising or RGB decode;
first video denoising pass stores blockwise video-state buffer;
action refinement reuses the buffered world/generative states;
action_full training makes both video and action portions trainable;
released action training loop uses action loss while allowing that loss to update Video DiT.
```

Caveat:

```text
current main is later than paper submission;
exact paper benchmark tag/commit is not pinned;
paper/config action steps and current-main hard-coded path show a version discrepancy.
```

Final label:

```text
P0009 DriveLaW = SOURCE-COMPLETE FOR CORE INTERFACE / VERSION-PARTIAL FOR EXACT PAPER REPRODUCTION
```

---

# DA-WAM source boundary

Canonical audit:

```text
audits/literature/PHASE_C6_DAWAM_AUDIT.md
```

Official repository:

```text
LeapWM/da-wam@1edbe555146a2d1fe9484f5c11f120860b8a4858
```

As of 2026-09-15:

```text
README.md only
"comming soon"
```

Therefore the following remain source-unverified:

```text
exact LoRA layer placement
predictor implementation / tensor shapes
scorer attention topology
exact detach/gradient boundaries
candidate proposal implementation
hard-negative bank generation
factor / utility target code
runtime / batching behavior
```

Final label:

```text
P0012 DA-WAM = PAPER-COMPLETE / SOURCE-BLOCKED
```

---

# Current blocked/monitor set

```text
P0062 Metis
P0063 DynFlowDrive
P0064 Discrete-WAM
P0065 GraphWorld
P0012 DA-WAM
```

Do not substitute unofficial reimplementations for absent/unreleased official code.

Use:

```text
PAPER-VERIFIED
OFFICIAL-README-VERIFIED where applicable
SOURCE-UNVERIFIED
```

and keep them on periodic source-release watch.

---

# Secondary partial item

```text
P0046 World4Drive NAVSIM branch equivalence
```

Core mechanism is already source-verified. A separate NAVSIM source reconciliation is optional and must not downgrade the completed core audit merely because that implementation branch has not been identified.

---

# GraphWorld source boundary

Canonical paper audit:

```text
audits/literature/PHASE_C5_GRAPHWORLD_AUDIT.md
```

As of 2026-09-15:

```text
raw paper / figures       PRESENT
paper mechanism audit     COMPLETE FIRST PASS
official implementation  NOT IDENTIFIED
```

Important false-positive guard:

```text
google-research/graphworld
```

is an unrelated synthetic graph-learning benchmark and must not be attached to the autonomous-driving GraphWorld paper.

---

# Source snapshot governance note

An Epona source snapshot was imported under:

```text
repos/Epona/
wam-research commit a9926b905247505df01ddc4ce28fb71b193303d9
```

This differs from the earlier convention of keeping external source checkouts local/ignored. The snapshot is MIT-licensed and commit-pinned, so there is no immediate evidence-integrity issue, but repository-governance policy should eventually be normalized:

```text
A. vendor selected official source snapshots intentionally
or
B. keep external source local and store only provenance + audit evidence
```

Do not mix the two policies accidentally.

---

# Canonical source-completeness rule going forward

For every core anchor record independently:

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
