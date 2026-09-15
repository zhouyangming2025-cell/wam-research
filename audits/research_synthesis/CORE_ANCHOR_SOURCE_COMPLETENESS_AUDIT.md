# Core Anchor Source Completeness Audit

Last updated: 2026-09-15

Status: **ACTIVE — source-layer completeness gate before GraphWorld**

Purpose: separate four different notions that must not be conflated:

```text
paper text available
!= deep analysis complete
!= official implementation exists
!= source-code mechanism verified
```

Canonical intent remains to preserve provenance, audited commit, decision-critical files/functions, source facts, and unresolved implementation questions. A local/exported source snapshot may exist under `repos/`, but scientific completeness is determined by the audit record rather than mere code presence.

## Status legend

```text
PAPER     canonical/raw paper text available in wam-research
ANALYSIS  normalized deep analysis available
CODE      attributable official implementation exists publicly
AUDIT     decision-critical implementation paths audited at a locked commit
BLOCKED   source audit cannot currently be completed because implementation is unavailable/not identifiable
PARTIAL   source exists/audit exists but does not fully cover the paper's reported mechanism/benchmark branch
```

## Ten normalized anchors

| Paper | Paper/raw MD | Deep analysis | Official code status | Source audit status | Current source-layer judgment |
|---|---|---|---|---|---|
| P0048 LAW | PRESENT | COMPLETE | `BraveGroup/LAW` | **COMPLETE**, commit `b2f6a784247072923c477ab92324d3aa5a9759bf` | HIGH completeness |
| P0045 WoTE | PRESENT | COMPLETE | `liyingyanUCAS/WoTE` | **COMPLETE for decision-critical target/reactivity path**, commit `298957c128a91d41a1c6075bd0bb6e7e845e093f` | HIGH completeness |
| P0001 Epona | PRESENT | COMPLETE | `Kevin-thu/Epona` | **COMPLETE for core mechanism**, commit `69b24c55f5ab8b3ffde8fa55e9f833bfe64d2c68` | **SOURCE-COMPLETE for planning/world interface** |
| P0042 WorldDrive | PRESENT | COMPLETE | `TabGuigui/WorldDrive` | COMPLETE/CORE audited, commit `c375ee1e1fe86ace175609db1ed90fd6db89673b` | HIGH completeness |
| P0046 World4Drive | PRESENT | COMPLETE | `ucaszyp/World4Drive` | COMPLETE core-interface audit, commit `cffb51adeb1f7d02b49c4b74d7262ded62a33ac8`; NAVSIM implementation equivalence remains PARTIAL | HIGH with benchmark-branch caveat |
| P0061 SeerDrive | PRESENT | COMPLETE | `LogosRoboticsGroup/SeerDrive` | COMPLETE version/source audit for released implementation | **PARTIAL by design:** released code integrates WoTE-style online evaluation and removes the original paper's iterative interaction, so code cannot be used as a drop-in verification of the paper graph |
| P0049 Drive-JEPA | PRESENT | COMPLETE | `linhanwang/Drive-JEPA` | COMPLETE first-pass source audit across released NAVSIM paths | HIGH completeness |
| P0062 Metis | PRESENT | COMPLETE | official repo attributable, but implementation code not released in audited state | **BLOCKED** | PAPER/README verified; implementation SOURCE-UNVERIFIED |
| P0063 DynFlowDrive | PRESENT | COMPLETE | `xiaolul2/DynFlowDrive`, repo currently README/teaser level in audited state | **BLOCKED** | PAPER verified; implementation SOURCE-UNVERIFIED |
| P0064 Discrete-WAM | PRESENT | COMPLETE | no attributable official implementation repository identified in current audit | **BLOCKED / MONITOR** | PAPER verified; code-level scheduler/detach/task-sampling SOURCE-UNVERIFIED |

## Immediate conclusion

The source layer is **not globally complete**, but the previously actionable Epona gap is now closed.

### A. Closed actionable gap — Epona

Canonical audit:

```text
audits/literature/PHASE_C5_EPONA_SOURCE_AUDIT.md
evidence/P0001_EPONA_SOURCE_EVIDENCE.md
```

Locked source:

```text
Kevin-thu/Epona@69b24c55f5ab8b3ffde8fa55e9f833bfe64d2c68
```

Source-verified core conclusions:

```text
shared STT/MST representation feeds TrajDiT and visual FluxDiT;
planning trajectory is produced before the visual branch and can run with traj_only=True;
future visual output is not consumed by same-step planning;
training visual condition is factual/logged future ego motion;
self-generated rollout uses predicted ego motion to condition visual generation;
visual loss backpropagates into shared STT/MST but not directly into TrajDiT parameters;
long rollout recurs on generated visual latents + predicted ego motion;
outer physical-frame rollout is distinct from inner diffusion/flow sampling iterations;
training includes periodic detached self-generated multi-forward conditioning, so it is not pure teacher forcing.
```

Final label:

```text
P0001 Epona = SOURCE-COMPLETE FOR CORE MECHANISM
```

Non-blocking residuals remain around exact checkpoint/table parity and runtime reproduction.

### B. Secondary optional follow-up

```text
P0046 World4Drive NAVSIM branch equivalence
```

The core implementation is already source-verified. Only attempt a further NAVSIM-specific audit if a distinct released NAVSIM implementation can be identified; do not downgrade the completed core audit merely because that branch is not found.

### C. Not currently fillable from official source

```text
P0062 Metis
P0063 DynFlowDrive
P0064 Discrete-WAM
```

Do not substitute unofficial reimplementations for missing official code. Retain explicit states:

```text
PAPER-VERIFIED
OFFICIAL-README-VERIFIED where applicable
SOURCE-UNVERIFIED
```

These belong on a periodic source-release watchlist rather than blocking field reconstruction indefinitely.

## Source snapshot governance note

On 2026-09-15 an Epona source snapshot was imported under:

```text
repos/Epona/
wam-research commit a9926b905247505df01ddc4ce28fb71b193303d9
```

This differs from the earlier convention that external repositories remain only local/ignored. The snapshot is MIT-licensed and commit-pinned, so there is no immediate scientific-evidence problem, but repository-governance policy should be normalized later:

```text
Option A: keep selected official source snapshots vendored and manifest them consistently;
Option B: restore external repos to local-only and retain only audit/evidence Markdown in wam-research.
```

Do not mix the two policies silently across anchors.

## Canonical source-completeness rule going forward

For every new core anchor, record independently:

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
paper↔code mechanism consistency?
unresolved source questions
```

Completion labels:

```text
PAPER-COMPLETE
SOURCE-COMPLETE
SOURCE-PARTIAL
SOURCE-BLOCKED
```

No paper should be called simply `COMPLETE` when source-level evidence is decision-critical unless the relevant completeness qualifier is explicit.
