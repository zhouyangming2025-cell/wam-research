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

The project repository is a research brain, not a mirror of every external codebase. Full external repositories should remain outside GitHub under ignored/local paths such as `repos/`; the canonical GitHub record should preserve repository provenance, audited commit, decision-critical files/functions, source facts, and unresolved implementation questions.

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
| P0001 Epona | PRESENT | COMPLETE | **PUBLIC OFFICIAL CODE EXISTS: `Kevin-thu/Epona`** | **MISSING dedicated commit-locked source audit** | **ACTIONABLE GAP** |
| P0042 WorldDrive | PRESENT | COMPLETE | `TabGuigui/WorldDrive` | COMPLETE/CORE audited, commit `c375ee1e1fe86ace175609db1ed90fd6db89673b` | HIGH completeness |
| P0046 World4Drive | PRESENT | COMPLETE | `ucaszyp/World4Drive` | COMPLETE core-interface audit, commit `cffb51adeb1f7d02b49c4b74d7262ded62a33ac8`; NAVSIM implementation equivalence remains PARTIAL | HIGH with benchmark-branch caveat |
| P0061 SeerDrive | PRESENT | COMPLETE | `LogosRoboticsGroup/SeerDrive` | COMPLETE version/source audit for released implementation | **PARTIAL by design:** released code integrates WoTE-style online evaluation and removes the original paper's iterative interaction, so code cannot be used as a drop-in verification of the paper graph |
| P0049 Drive-JEPA | PRESENT | COMPLETE | `linhanwang/Drive-JEPA` | COMPLETE first-pass source audit across released NAVSIM paths | HIGH completeness |
| P0062 Metis | PRESENT | COMPLETE | official repo attributable, but implementation code not released in audited state | **BLOCKED** | PAPER/README verified; implementation SOURCE-UNVERIFIED |
| P0063 DynFlowDrive | PRESENT | COMPLETE | `xiaolul2/DynFlowDrive`, repo currently README/teaser level in audited state | **BLOCKED** | PAPER verified; implementation SOURCE-UNVERIFIED |
| P0064 Discrete-WAM | PRESENT | COMPLETE | no attributable official implementation repository identified in current audit | **BLOCKED / MONITOR** | PAPER verified; code-level scheduler/detach/task-sampling SOURCE-UNVERIFIED |

## Immediate conclusion

The source layer is **not fully complete**.

However, the missing cases split into two fundamentally different classes:

### A. Actionable now

```text
P0001 Epona
```

An official implementation is publicly available and appears substantial (`configs/`, `models/`, `dataset/`, `data_preparation/`, `scripts/`, checkpoints/inference instructions). The project currently lacks a LAW/WoTE-style commit-locked code audit for Epona. This should be filled before claiming paper+code completeness for the first ten anchors.

Secondary optional follow-up:

```text
P0046 World4Drive NAVSIM branch equivalence
```

The core implementation is already source-verified. Only attempt a further NAVSIM-specific audit if a distinct released NAVSIM implementation can be identified; do not downgrade the completed core audit merely because that branch is not found.

### B. Not currently fillable from source

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

These should enter a periodic source-release watchlist rather than block field reconstruction indefinitely.

## Epona source-audit targets

The Epona agent audit should resolve at minimum:

```text
1. exact official repo HEAD/commit audited
2. MST/history encoder data flow
3. exact construction of shared historical latent F
4. TrajDiT inputs/outputs and trajectory generation path
5. VisDiT inputs/outputs and action-conditioning carrier
6. whether TrajDiT output directly conditions VisDiT and at which tensor/interface
7. training loss attachment and gradient paths into MST/shared F
8. trainability/freeze state of encoder, MST, TrajDiT, VisDiT, VAE/DCAE components
9. planning inference path: whether VisDiT is instantiated/executed/disabled and whether any visual-future tensor is consumed by trajectory generation
10. simulation/video rollout path and autoregressive state update
11. teacher forcing vs self-generated context across rollout/training
12. sampling/denoising iteration semantics vs physical-frame time
13. source support for the paper's claim that pure planning can disable visual generation
14. code/paper mismatches, stale configs, or multiple task modes
15. exact checkpoint/config corresponding to reported planning experiments when identifiable
```

Required source-evidence format:

```text
repo + locked commit
→ file path
→ class/function
→ minimal code fact
→ scientific implication
→ unresolved boundary
```

Do not paste whole source files into the research repository.

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
