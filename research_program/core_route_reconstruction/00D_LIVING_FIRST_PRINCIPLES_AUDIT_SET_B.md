# Living First-Principles Audit — Set B continuation

Status: **APPEND-ONLY RESEARCH MEMORY — NOT AN ONTOLOGY SPEC**  
Continues: `00C_LIVING_FIRST_PRINCIPLES_AUDIT_PAPER_FIRST_RESET.md`  
Detailed evidence: `17_PAPER_FIRST_RECONSTRUCTION_SET_B.md`  
Date: 2026-09-17

---

## 45. Set B tested an apparent “coupling debate” without assuming it

Set B deep-read:

- Epona;
- DriveLaW;
- Metis;
- ReWorld;
- SimWAM.

The pre-audit temptation was to place these papers on a simple spectrum such as:

```text
parallel -> chained -> tightly coupled -> decoupled
```

The paper-first reconstruction shows that this scalar picture is unsafe.

The papers are genuinely related by a broad question — how future/world-generation knowledge should become useful to planning — but the mechanisms differ along several independent relations that the word `coupling` hides.

No new route labels are accepted from this set.

---

## 46. Important correction: Epona is not “just parallel heads”

Earlier shorthand repeatedly described Epona as parallel video/action generation.

That is true at the specialized output-head level but incomplete at the planning mechanism level.

Epona first computes a shared Multimodal Spatiotemporal Transformer state `F` from historical visual latents and historical action/motion context.

Then:

```text
F -> TrajDiT -> trajectory
F -> VisDiT  -> next future frame
```

The planner can run with VisDiT deactivated, but it still uses the online shared temporal latent `F`.

Video prediction and trajectory prediction jointly shape this upstream state during training, and the paper reports a planning drop when video prediction is removed from training.

Therefore:

> `future video output absent at planning inference` does not mean `world-model state absent from planning`.

This correction must be preserved because it prevents Epona from being incorrectly collapsed with every training-only video-supervision method.

---

## 47. DriveLaW’s claim is narrower and stronger than “more coupled”

DriveLaW explicitly criticizes Epona-like designs, but the scientifically precise disagreement is not simply parallel versus chained boxes.

Epona already gives the planner a shared world/temporal state.

DriveLaW’s stronger claim is:

> the **internal state of the video generator itself** should become the planner state.

The Action DiT reads intermediate Video-DiT denoising features online.

ReWorld later makes this implementation relation especially explicit: it instantiates the DriveLaW bridge and retains Video-DiT block states from the first discrete video denoising step within the current forward pass for Action-DiT conditioning.

Thus the paper-level difference concerns **which learned representation is trusted to carry world knowledge into action**, not merely whether two heads are parallel on a diagram.

---

## 48. ReWorld is a clean example of “important innovation without a new bridge”

ReWorld deliberately keeps a DriveLaW-style world-to-action interface and changes how the intermediate representations are learned.

Its three-stage curriculum:

1. makes Video-DiT intermediate states explicitly future-predictive;
2. aligns Action-DiT states with attended video readouts;
3. shapes both sides with behavior-oriented hard negatives.

The collapse test is unusually clean:

```text
ReWorld
- explicit representation curriculum
= DriveLaW-style chained WAM
```

This is strong evidence that future research must separate:

- innovation in the **bridge topology**;
- innovation in the **content/training of representations travelling through that bridge**.

An ontology that promotes every major paper contribution into a new route will over-split the field.

---

## 49. Metis and SimWAM invalidate “training-only future video” as one mechanism family

Both papers can be summarized casually as:

> use video prediction during training and remove explicit future-video generation during action inference.

Deep reconstruction shows this is too coarse.

### Metis

Metis uses asymmetric visibility:

```text
action tokens -> read current observation only
future-video tokens -> read current observation + future action tokens
```

The paper explicitly argues that future-video loss can therefore backpropagate into the action expert during joint training, while action inference remains independent of future-video tokens.

### SimWAM

SimWAM uses isolated visibility:

```text
action tokens -> current observation
future-video tokens -> current observation
future-video tokens X action tokens
```

The two experts share no weights. Video co-training nevertheless raises the reported imitation-planner PDMS from 86.6 to 90.3, and the paper attributes this to dynamics-prior transfer through the shared/current observation interface.

A source-level follow-up is still needed before making a stronger parameter-level statement about the exact gradient carrier in SimWAM.

Therefore lifecycle alone (`video branch removed`) cannot establish mechanism sameness.

---

## 50. Major conceptual lesson: “coupling” is not one variable

Set B exposes at least four distinct relations that previous discussion repeatedly collapsed into one word:

```text
1. STATE/PARAMETER SHARING
   Do world and action use a common representation or separate experts?

2. FORWARD DEPENDENCY
   Does action read a world/future-generation state?

3. BACKWARD / LEARNING DEPENDENCY
   Can world/future objectives update the planner-facing representation or action parameters?

4. DEPLOYMENT DEPENDENCY
   Must world/future-generation computation remain active when action is produced?
```

Two systems can be tightly connected under one relation and disconnected under another.

Examples:

- DriveLaW: strong online forward generator-state dependency; planning also fine-tunes the bridge.
- Epona: shared upstream temporal state; future visual head optional at deployment.
- Metis: no future-video->action forward dependency, but deliberate training/gradient dependency.
- SimWAM: no future/action token visibility and no shared expert weights, yet joint video training improves the current-observation-based action expert.
- ReWorld: same forward bridge as DriveLaW, but much stronger explicit representation supervision.

Therefore a future `coupling axis` should be presumed invalid unless evidence later discovers a deeper variable that truly subsumes these relations without loss.

---

## 51. Forward graph and learning graph must be reconstructed separately

Earlier work alternated between two incomplete extremes:

- deployment-only causal graphs;
- training/lifecycle descriptions.

Set B shows that neither alone is sufficient.

For future paper-first reconstruction, preserve two graphs before abstraction:

```text
FORWARD / DEPLOYMENT GRAPH
What state does the action computation actually consume at runtime?

LEARNING / BACKWARD GRAPH
Which world/future losses and teachers can change the representation/parameters used by the deployed action computation?
```

Metis is the clearest reason: the runtime action path intentionally excludes future-video tokens, while the paper’s claimed world-model benefit is transmitted through training-time information/gradient flow.

Epona gives the complementary case: one shared online state is jointly shaped by both visual and trajectory prediction even though the visual output head is absent in planning mode.

This two-graph discipline is a **reading protocol**, not a new ontology.

---

## 52. “Future generation off at inference” is demoted to a lifecycle fact

Set B decisively shows that this property cannot be a core route criterion by itself.

Epona, Metis and SimWAM can all avoid explicit future-video generation in planning mode, yet:

- Epona retains a jointly trained shared temporal state online;
- Metis retains a dedicated action expert and current-context path shaped by asymmetric joint training;
- SimWAM retains a standalone action expert trained with an isolated video/action future-token interface.

DriveLaW/ReWorld also do not require decoding a final future video, but they retain **Video-DiT internal generative computation** as the planner’s online state source.

Hence the correct question is never simply:

> “is video generation present at inference?”

It is:

> “what exact computation/state survives, what does action read, and how was that state/action path shaped by world learning?”

---

## 53. Current research posture after Set B

No route taxonomy is accepted.

No `coupling family` is accepted.

What has improved is the reconstruction vocabulary.

For WAM papers combining generation/world prediction with planning, future audits should explicitly recover:

```text
planner-facing runtime state
future-output requirement
world/action parameter sharing
forward token/state visibility
world-loss gradient reachability
training-only vs retained computation
bridge-topology innovation vs bridge-training innovation
post-training additions (RL/scorer/reward) vs identity-defining mechanism
```

These remain observational questions.

The next small paper set should stress a different scientific question rather than repeatedly sampling video-generator WAMs and prematurely turning Set B into the center of the field.

Correct research posture:

> deepen paper understanding first; let repeated structure appear across independently reconstructed sets; abstract only after the structure survives without being used as the reading prompt.
