# Source / Markdown Completion — Local Agent Prompt

Copy the prompt below to the local corpus/source agent.

---

You are working inside the local checkout of:

```text
wam-research
```

Your task is **source completeness and paper-text completeness only**. Do not redesign the research taxonomy, do not declare research gaps, and do not rewrite scientific conclusions unless source evidence directly contradicts an existing claim.

Before acting, read:

```text
README.md
state/CURRENT_STATE.md
state/NEXT_TASK.md
state/RESEARCH_PRINCIPLES.md
audits/literature/SOURCE_COMPLETENESS_AUDIT.md
.gitignore
```

## Goal

Bring the current ten normalized WAM anchors as close as possible to:

```text
canonical paper/raw MD
+ official supplement/appendix text when available
+ official source repository identity
+ local ignored source clone when code exists
+ pinned commit SHA
+ source-level mechanism audit when not already done
```

Do **not** vendor upstream repositories into the GitHub knowledge repo. Full source clones belong under:

```text
repos/
```

which is intentionally gitignored.

Canonical PDFs also remain local/NAS only and must not be committed.

---

# Scope: current canonical 12 anchors

```text
P0001 Epona
P0009 DriveLaW
P0042 WorldDrive
P0045 WoTE
P0046 World4Drive
P0048 LAW
P0049 Drive-JEPA
P0061 SeerDrive
P0062 Metis
P0063 DynFlowDrive
P0064 Discrete-WAM
P0065 GraphWorld
```

---

# Task A — Primary-paper and supplement Markdown completeness

For each anchor:

1. Confirm the existing `papers/raw_md/<paper>/...raw.md` is present and corresponds to the canonical paper/version used by the current deep analysis.
2. Check whether an **official supplement, appendix PDF, camera-ready supplementary file, or separate technical appendix** exists.
3. Determine whether that supplement's scientific content is already contained in the existing raw MD.
4. If scientifically relevant supplement text is missing, download the canonical supplement **locally only**, convert/extract it to Markdown, and add a committed text layer such as:

```text
papers/raw_md/PXXXX_Name/PXXXX_Name.supp.raw.md
```

5. Preserve headings, equations, tables and figure captions as well as practical conversion permits.
6. Do not commit PDFs, MinerU intermediate PDFs/JSON, datasets, checkpoints, or large binaries.
7. Record source URL/version/date in the Markdown header.

Produce/update a compact inventory:

```text
audits/literature/PAPER_TEXT_COMPLETENESS_AUDIT.md
```

with columns:

```text
Paper
primary raw MD
canonical version
supplement exists?
supplement raw MD present?
missing content?
action taken
```

Do not re-convert material already complete.

---

# Task B — Local official-source clone inventory

For every paper with a trustworthy official implementation:

1. Verify the repository is attributable to the paper/authors/project page.
2. Clone/update it under:

```text
repos/<short-name>/
```

3. Record:

```text
official repo URL
HEAD commit
commit used by existing wam-research source audit
branch/tag
clone date
whether training code exists
whether inference code exists
whether evaluation code exists
whether configs/checkpoints links exist
```

4. If an existing audit already pins a commit, **do not silently switch scientific evidence to a newer commit**. Keep the audited commit reproducible and separately note newer upstream HEAD.
5. Do not commit anything under `repos/`.

Create/update:

```text
audits/literature/LOCAL_SOURCE_CLONE_INVENTORY.md
```

---

# Task C — HIGH PRIORITY: Epona source audit

Official repository:

```text
https://github.com/Kevin-thu/Epona
```

Current upstream commit observed by GPT on 2026-09-15:

```text
69b24c55f5ab8b3ffde8fa55e9f833bfe64d2c68
```

Clone and pin that commit first unless upstream history proves a different paper-release commit should be used. If you choose a different commit, explain exactly why.

Inspect at minimum:

```text
models/model.py
models/stt.py
models/traj_dit.py
models/flux_dit.py
models/diffusion/
configs/
scripts/
dataset/
data_preparation/
```

Resolve these questions with exact file/function references:

```text
1. How are historical images and historical ego motion encoded?
2. What exact tensor/object corresponds to the paper's shared historical latent F?
3. Where does the architecture split into trajectory and visual branches?
4. What parameters are shared, and what parameters are branch-specific?
5. How does predicted/provided ego action condition VisDiT?
6. Which losses attach to TrajDiT, VisDiT and the shared historical representation?
7. Does visual loss backpropagate through the shared representation/MST/STT path?
8. Are any target paths detached/frozen?
9. What exact code path is used for planning-only inference?
10. Is VisDiT actually bypassed/disabled in planning evaluation, or merely its output ignored?
11. What exact code path performs autoregressive visual rollout?
12. Is rollout teacher-forced, self-generated, or hybrid across steps?
13. What are the default trajectory/video diffusion sampling steps?
14. Which configuration/checkpoint corresponds to the reported planning experiment?
15. Which configuration/checkpoint corresponds to world/video generation experiments?
16. Are there any paper↔code mismatches in tensor shapes, horizon, conditioning, losses, or inference mode?
```

Required artifact:

```text
audits/literature/PHASE_C5_EPONA_SOURCE_AUDIT.md
```

Structure it as:

```text
source provenance + commit
exact source files/functions
paper claim → code evidence → interpretation
training graph
inference/planning graph
visual rollout graph
parameter/gradient sharing
paper↔source mismatches
resolved questions
remaining source uncertainties
```

Then make **minimal evidence-backed updates only** to:

```text
papers/deep_analysis/P0001_EPONA_DEEP_ANALYSIS_V2.md
landscape/P0001... ontology material if such a canonical file exists
```

Do not rewrite the whole paper analysis just because source is now available.

---

# Task D — Already source-audited repositories

These already have commit-locked source evidence in `wam-research`:

```text
LAW          BraveGroup/LAW
WoTE         liyingyanUCAS/WoTE
WorldDrive   TabGuigui/WorldDrive
World4Drive  ucaszyp/World4Drive
Drive-JEPA   linhanwang/Drive-JEPA
```

For these:

```text
ensure local clone exists
ensure audited commit is fetchable/check-outable
record current upstream HEAD separately
DO NOT redo the full scientific audit unless code drift exposes a material mismatch
```

Specific bounded follow-ups:

```text
World4Drive:
search for a distinct official NAVSIM implementation/config path;
if absent, retain current caveat.

Drive-JEPA:
check whether official Bench2Drive implementation/checkpoints have since been released;
if absent, retain current caveat.
```

---

# Task E — SeerDrive version-boundary preservation

Official repo:

```text
LogosRoboticsGroup/SeerDrive
```

Existing project conclusion is binding unless disproved:

```text
paper mechanism:
iterative future-BEV <-> planner co-refinement

public release:
WoTE-integrated online trajectory evaluation/selection;
initial public release already differs from original paper mechanism
```

Do not merge these into one implementation story.

Locally preserve/check out the relevant public commit(s) and update only version provenance if needed.

---

# Task F — Externally blocked / unresolved papers

## Metis

Official repo:

```text
LogosRoboticsGroup/Metis
```

If repository still contains only README/assets and no real model/training/inference/eval implementation:

```text
DO NOT create a fake source audit
DO NOT infer implementation from paper pseudocode
mark SOURCE-BLOCKED with check date + upstream HEAD
```

If code has appeared, stop and perform a new source-release audit before modifying scientific conclusions.

## DynFlowDrive

Official repo:

```text
xiaolul2/DynFlowDrive
```

If README still says code will be released after acceptance and implementation is absent:

```text
keep SOURCE-BLOCKED
```

If code has appeared, priority audit targets are:

```text
Eq.10 velocity target implementation
flow interpolation anchor a vs z_t sampling start
alpha schedule
solver K
gradient detach/freeze boundaries
VAE/world encoder freeze state
per-candidate reconstruction/flow supervision
```

## Discrete-WAM

Paper:

```text
arXiv:2606.05645v2
```

Search only trustworthy channels:

```text
paper/arXiv author links
Xiaomi EV / Xiaomi Research project pages
author GitHub profiles
paper's official project page
Hugging Face author/project links if attributable
```

Do NOT adopt an unofficial reproduction merely because the repository name matches.

If no official repo is attributable, retain:

```text
SOURCE-IDENTITY-UNRESOLVED
```

---

# Task G — Final write-back

Update:

```text
audits/literature/SOURCE_COMPLETENESS_AUDIT.md
```

with verified results.

Do not change `state/NEXT_TASK.md` away from the current scientific reading task merely because this maintenance task was performed.

At the end, report exactly:

```text
1. files added/modified
2. official repos cloned locally
3. commit SHAs pinned
4. supplements added as Markdown
5. Epona source-audit conclusions
6. paper↔code mismatches found
7. still-blocked source gaps
8. anything requiring GPT scientific re-interpretation
```

## Non-negotiable constraints

```text
NO PDF commit
NO dataset/checkpoint commit
NO full upstream source repo commit
NO unofficial repo used as official evidence
NO silent commit/version substitution
NO scientific claim upgrade without source evidence
NO research-gap or method-design work
```
