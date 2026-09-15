# Core Anchor Source Completeness Audit

Last updated: 2026-09-15

Status: **ACTIVE — fourteen-anchor source-layer completeness tracking during WAM expansion**

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

## Fourteen normalized anchors

| Paper | Paper/raw MD | Deep analysis | Official code status | Source audit status | Current source-layer judgment |
|---|---|---|---|---|---|
| P0048 LAW | PRESENT | COMPLETE | `BraveGroup/LAW` | **COMPLETE**, `b2f6a784247072923c477ab92324d3aa5a9759bf` | HIGH |
| P0045 WoTE | PRESENT | COMPLETE | `liyingyanUCAS/WoTE` | **COMPLETE for decision-critical target/reactivity path**, `298957c128a91d41a1c6075bd0bb6e7e845e093f` | HIGH |
| P0001 Epona | PRESENT | COMPLETE | `Kevin-thu/Epona` | **COMPLETE for core mechanism**, `69b24c55f5ab8b3ffde8fa55e9f833bfe64d2c68` | SOURCE-COMPLETE for planning/world interface |
| P0042 WorldDrive | PRESENT | COMPLETE | `TabGuigui/WorldDrive` | COMPLETE/CORE, `c375ee1e1fe86ace175609db1ed90fd6db89673b` | HIGH |
| P0046 World4Drive | PRESENT | COMPLETE | `ucaszyp/World4Drive` | COMPLETE core interface, `cffb51adeb1f7d02b49c4b74d7262ded62a33ac8`; NAVSIM branch equivalence PARTIAL | HIGH with benchmark caveat |
| P0061 SeerDrive | PRESENT | COMPLETE | `LogosRoboticsGroup/SeerDrive` | released implementation audited | PARTIAL by design: public code is WoTE-integrated variant |
| P0049 Drive-JEPA | PRESENT | COMPLETE | `linhanwang/Drive-JEPA` | COMPLETE first-pass released NAVSIM paths | HIGH |
| P0062 Metis | PRESENT | COMPLETE | official repo attributable; implementation unreleased in audited state | BLOCKED | PAPER/README verified; SOURCE-UNVERIFIED |
| P0063 DynFlowDrive | PRESENT | COMPLETE | `xiaolul2/DynFlowDrive`, README/teaser only | BLOCKED | PAPER verified; SOURCE-UNVERIFIED |
| P0064 Discrete-WAM | PRESENT | COMPLETE | no attributable official implementation identified | BLOCKED / MONITOR | PAPER verified; SOURCE-UNVERIFIED |
| P0065 GraphWorld | PRESENT | COMPLETE | no attributable official autonomous-driving implementation identified | BLOCKED / MONITOR | PAPER verified; SOURCE-UNVERIFIED |
| P0009 DriveLaW | PRESENT | COMPLETE | `xiaomi-research/drivelaw` | COMPLETE core audit, `243e0e41148bdb1ae39ce1adf17d026e7cbd4348` | SOURCE-COMPLETE core / VERSION-PARTIAL exact paper reproduction |
| P0012 DA-WAM | PRESENT | COMPLETE | `LeapWM/da-wam`, README-only placeholder | BLOCKED | PAPER-COMPLETE / SOURCE-BLOCKED |
| **P0002 SafeDrive** | **PRESENT** | **COMPLETE** | **`SPA-junghokim/SafeDrive` full NAVSIM release** | **COMPLETE core NAVSIM audit, `ea7791d6c2ebdeedfb6ed514f080cdfa1675b76f`; Bench2Drive branch PARTIAL** | **SOURCE-COMPLETE NAVSIM CORE / SOURCE-PARTIAL BENCH2DRIVE** |

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

---

# DriveLaW source boundary

Canonical audits:

```text
papers/deep_analysis/P0009_DRIVELAW_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_DRIVELAW_AUDIT.md
```

Locked source:

```text
xiaomi-research/drivelaw@243e0e41148bdb1ae39ce1adf17d026e7cbd4348
```

Core verified facts:

```text
planning uses Video-DiT internal block states as Action-DiT conditioning;
return_action=true / return_video=false planning path does not require completed video;
first video pass caches blockwise states;
action refinement reuses cached states;
action_full lets action loss update Video DiT.
```

Caveat: current main is later than paper submission and exact benchmark commit is not pinned.

---

# DA-WAM source boundary

Canonical audit:

```text
audits/literature/PHASE_C6_DAWAM_AUDIT.md
```

Official repository:

```text
LeapWM/da-wam@1edbe555146a2d1fe9484f5c11f120860b8a4858
README only: "comming soon"
```

Source-unverified details include predictor/scorer implementation, LoRA placement, gradient boundaries, proposal generator, hard-negative bank, target code and runtime behavior.

Final label:

```text
P0012 DA-WAM = PAPER-COMPLETE / SOURCE-BLOCKED
```

---

# SafeDrive source boundary

Canonical audits:

```text
papers/deep_analysis/P0002_SAFEDRIVE_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_SAFEDRIVE_AUDIT.md
```

Locked source:

```text
SPA-junghokim/SafeDrive@ea7791d6c2ebdeedfb6ed514f080cdfa1675b76f
```

Decision-critical source paths audited:

```text
README.md
docs/train_eval.md
safedrive_model.py
safedrive_agent.py
safedrive_loss.py
safedrive_config.py
transformer_motion.py
compute_navsim_score.py
Phase2/Phase3 configs
train.sh
test.sh
```

Core source-verified facts:

```text
ProposalNet→SWNet→FRNet released architecture exists;
released config starts from 256 plan anchors with two-stage pruning;
SWNet builds candidate-specific sparse ego-agent worlds;
FRNet predicts scene-level and fine-grained PwNC/TwDAC safety signals;
model-generated candidates are scored online during training by PDM to create candidate-specific safety targets;
pair_collision_gt localizes at-fault collision by agent token and time;
twdac_gt localizes off-road future poses;
PDM teacher is not required for deployed learned scoring;
surrounding-agent logged motion targets are reused/expanded across ego candidate branches in the audited NAVSIM path.
```

Therefore:

```text
candidate-specific safety consequence supervision = YES
candidate-specific reactive environment truth      = NO
```

Benchmark/source split:

```text
NAVSIM main mechanism / released reproduction  SOURCE-COMPLETE
Bench2Drive paper result                       PAPER-VERIFIED
Bench2Drive implementation path                NOT IDENTIFIED / SOURCE-PARTIAL
```

Final label:

```text
P0002 SafeDrive = SOURCE-COMPLETE FOR NAVSIM CORE / SOURCE-PARTIAL FOR BENCH2DRIVE
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

---

# Secondary partial items

```text
P0046 World4Drive NAVSIM branch equivalence
P0009 DriveLaW exact paper-benchmark commit
P0002 SafeDrive Bench2Drive implementation branch
```

These caveats must not downgrade already source-verified core mechanisms.

---

# GraphWorld false-positive guard

```text
google-research/graphworld
```

is unrelated to the autonomous-driving GraphWorld paper.

---

# Source snapshot governance note

An Epona source snapshot was historically imported under `repos/Epona/` in wam-research commit `a9926b9...`, despite `.gitignore` normally excluding `repos/`. Future external source checkouts should follow a deliberate, normalized policy rather than mixing vendored snapshots and local-only clones accidentally.

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
