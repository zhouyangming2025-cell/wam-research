# D01.3 Blind Selection Preregistration

Status: **registered before method/source inspection**

## 1. Selection objective

Select three papers that were not used in the 12-paper ontology, the 21-artifact canonical projection, D01's 26-work census, or earlier ontology pressure tests. The selected set must contain:

1. at least two plausible planning/policy artifacts;
2. at least one generation, simulation, or boundary artifact;
3. at least one paper with an official code or a sufficiently detailed primary source.

The final classification unit may split a selected paper into modes only if the paper/code evidence proves that the terminal output or planning path is materially different. A split is not a way to replace a difficult paper.

## 2. Exclusion audit applied before selection

The following exclusions were checked from local scope records and filenames before reading selected methods:

- all 26 works in \`research_program/domain_corpus/d01/01_PAPER_SCOPE_TABLE.md\`;
- all canonical 12 papers and canonical 21 artifacts;
- DA-WAM and the D01 artifact ledger;
- papers with existing \`landscape/*ONTOLOGY_PROJECTION.md\` files;
- papers already named as ontology pressure cases in the D01.3 handoff/task text.

No candidate below appears in those excluded sets or has a local ontology projection file. Candidate presence in the broad text-layer corpus is not deep ontology analysis and is not, by itself, an exclusion.

## 3. Candidate pool

The pool was built from the local raw-paper directory, exact title, year, source/official-code metadata, abstract, and scope relevance. The abstract-level rationale below is intentionally not a mechanism classification.

### Layer A — abstract claims an online future/interaction object used for planning

| registered order | ID | paper | abstract-level reason | source signal |
|---:|---|---|---|---|
| 0 | P0003 | GraphAD: Interaction Scene Graph for End-to-end Autonomous Driving | future trajectories and interaction graph are described as mutually refining and supporting prediction/planning | detailed local paper; code URL in abstract |
| 1 | P0004 | Reasoning Multi-Agent Behavioral Topology for Interactive Autonomous Driving | future behavioral topology is described as guiding joint prediction and planning | detailed local paper; official code/model URL |
| 2 | P0058 | VAD: Vectorized Scene Representation for Efficient Autonomous Driving | vectorized motion/map scene representation is described as a planning constraint and guide | detailed local paper; official code/models URL |
| 3 | P0057 | Planning-oriented Autonomous Driving (UniAD) | prediction/occupancy tasks are described as coordinated toward planning | detailed local paper; public code stated |

### Layer B — abstract claims world-model prediction, training, policy learning, or representation transfer

| registered order | ID | paper | abstract-level reason | source signal |
|---:|---|---|---|---|
| 0 | P0036 | DriveDreamer: Towards Real-world-driven World Models for Autonomous Driving | world model is presented for real-world-driven driving generation/prediction | detailed local paper |
| 1 | P0038 | Vista: A Generalizable Driving World Model with High Fidelity and Versatile Applications | abstract-level world-model generation/application claim | detailed local paper |
| 2 | P0039 | DriveDreamer-2: LLM-Enhanced World Models for Diverse Driving Scenarios | world model and diverse driving scenario generation claim | detailed local paper |
| 3 | P0011 | Sensitivity Shaping for Latent Modeling | generative dynamics/world-model sensitivity is linked to safer closed-loop planning; non-AD boundary candidate | detailed local paper |

### Layer C — generation, simulation, joint-policy, or boundary stress cases

| registered order | ID | paper | abstract-level reason | source signal |
|---:|---|---|---|---|
| 0 | P0013 | BridgeSim: Unveiling the OL-CL Gap in End-to-End Autonomous Driving | closed-loop simulation and test-time adaptation of driving policies | detailed local paper; project page |
| 1 | P0029 | GenAD: Generative End-to-End Autonomous Driving | generative driving/world-model boundary candidate | detailed local paper |
| 2 | P0060 | Driving on Registers (DrivoR) | end-to-end planner generates and scores trajectory proposals; useful no-world-carrier boundary | detailed local paper; code/checkpoint project page |
| 3 | P0034 | HUGSIM: A Real-time, Photo-realistic and Closed-loop Simulator for Autonomous Driving | simulator and closed-loop evaluation boundary | detailed local paper |
| 4 | P0055 | SLEDGE: Synthesizing Driving Environments with Generative Models and Rule-Based Traffic | generative simulator for motion-planning environments | detailed local paper; official code |
| 5 | P0066 | SafeSim: A Generalizable and Controllable Simulator for Autonomous Driving | controllable simulator boundary | detailed local paper; local project metadata |

The pool has 14 candidates, with at least three candidates in every required layer. The selected set will be drawn before opening methods.

## 4. Fixed selection rule

Seed:

\`\`\`text
20260917
\`\`\`

For each layer independently, compute the first unsigned 32-bit word of:

\`\`\`text
SHA256("20260917|<layer-letter>")
\`\`\`

and select the candidate at \`word mod layer-size\`, using the registered order above. The reproducible indices are:

\`\`\`text
A: 3779577924 mod 4 = 0  → P0003 GraphAD
B: 2047270356 mod 4 = 0  → P0036 DriveDreamer
C: 3812445354 mod 6 = 2  → P0060 DrivoR
\`\`\`

No selected paper may be replaced because its methods, source, or code are incomplete. If a selected identity or primary source is invalid, the original selection and exclusion reason must be retained and a substitute may be drawn only under the same frozen rule after recording whether any method detail had already been read.

## 5. Locked selected set

| selected artifact seed | exact paper identity | intended stress role | provisional source boundary |
|---|---|---|---|
| P0003 | GraphAD: Interaction Scene Graph for End-to-end Autonomous Driving | possible online interaction/future-to-planning planner | paper first; code status to be verified after seal |
| P0036 | DriveDreamer: Towards Real-world-driven World Models for Autonomous Driving | world-model generation/training/planning boundary | paper first; code/version to be verified after seal |
| P0060 | Driving on Registers (DrivoR) | candidate-generation/scoring planner with possible no-world-carrier boundary | paper plus official project/code status to be verified after seal |

At least two selected papers (GraphAD and DrivoR) are plausible planning/policy artifacts. DriveDreamer supplies a world-model generation/training boundary; if it has no deployed one-stage action path, that is a valid blind result rather than an exclusion. The set includes detailed primary sources and a code/project signal; source strength will be recorded later without changing the set.

## 6. Seal

This preregistration fixes the selected set and the selection rule. From this point onward, method sections, formulas, figures, source code, and primary artifacts may be opened only to reconstruct the selected papers' evidence. No ontology file may be changed in response to what they reveal.


