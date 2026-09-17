# Paper-first reconstruction — Set D

Status: evidence reconstruction only; **no route naming, no ontology update, no R/W/E/L or M0–M4 assignment**.

Branch context: `research/core-route-reconstruction`

Papers in this set:

1. OccWorld — *Learning a 3D Occupancy World Model for Autonomous Driving*
2. DrivingGPT — *Unifying Driving World Modeling and Planning with Multi-modal Autoregressive Transformers*
3. GenAD — *Generative End-to-End Autonomous Driving*
4. Gen-Drive — *Enhancing Diffusion Generative Driving Policies with Reward Modeling and Reinforcement Learning Fine-tuning*
5. Discrete-WAM — *Unified Discrete Vision-Action Token Editing for World-Policy Learning*

Primary evidence:

- `papers/raw_md/P0043_OccWorld/P0043_OccWorld.raw.md`
- `papers/raw_md/P0040_DrivingGPT/P0040_DrivingGPT.raw.md`
- `papers/raw_md/P0029_GenAD/P0029_GenAD.raw.md`
- `papers/raw_md/P0006_GenDrive/P0006_GenDrive.raw.md`
- `papers/raw_md/P0064_Discrete-WAM/P0064_Discrete-WAM.raw.md`

---

## 0. Audit contract

This set was deliberately selected to attack one tempting abstraction:

> these papers all “jointly model world and action”, therefore they belong to one route.

That statement is **not** accepted as a starting point.

The word `joint` is treated as an unresolved claim. For each paper, the audit independently reconstructs:

- what variables are jointly represented, predicted, or generated;
- whether the jointness is architectural, probabilistic, temporal, multi-agent, or only multi-task;
- the exact factorization/order of prediction;
- whether world and action are coupled during training only or during deployed planning;
- whether final ego commitment is direct generation, sampling, hierarchical decoding, or generation followed by evaluation;
- what is removed at inference;
- which mechanism would have to be deleted for the paper's central scientific claim to collapse.

Only after all five papers are reconstructed independently do we compare them.

---

# 1. OccWorld

## 1.1 Author-stated scientific problem

OccWorld rejects the conventional serial perception → prediction → planning decomposition for two reasons. First, object-box motion prediction is too coarse to represent the full 3D scene evolution. Second, scene evolution and ego motion should not be treated as unrelated outputs: the ego is part of the evolving driving world.

Its central proposal is therefore a 3D occupancy world model that predicts **surrounding-scene evolution and ego movement together**.

The paper formalizes the world transition as approximately:

```text
past scene representations + past ego positions
→ next scene representation + next ego position
```

and then recursively feeds the predicted next state back to obtain longer-horizon futures.

## 1.2 What is actually “joint”

OccWorld first tokenizes the 3D semantic occupancy scene with a VQ-VAE. It then introduces an ego token into the token set representing the current world.

The resulting world state contains:

```text
scene tokens
+
ego token
```

The spatial-temporal generative transformer mixes scene and ego tokens spatially and applies temporal causal attention to predict the next token set. The ego token is decoded into ego displacement while scene tokens decode into future occupancy.

So OccWorld's jointness is best described factually as:

> **the next world state contains both environment state tokens and an ego-motion token, and both are predicted by the same autoregressive world-state transition.**

This is not merely “two heads trained together”. The ego token participates in the same token dynamics as scene tokens, and the paper reports that corrupting/removing ego temporal modeling affects not only planning but also occupancy forecasting.

## 1.3 Training computation

Simplified training path:

```text
past occupancy
→ occupancy tokenizer
→ past scene tokens

past ego positions
→ ego token

(scene tokens + ego token) across time
→ spatial mixing + temporal causal attention
→ next scene tokens + next ego token

next scene tokens → occupancy/token prediction loss
next ego token   → ego displacement decoder → L2 trajectory loss
```

The paper's stage-2 objective therefore supervises both world-state token forecasting and ego displacement.

## 1.4 Inference/deployment computation

OccWorld autoregressively predicts its own future token states. Predicted scene and ego tokens are appended to the history and become input to the next prediction step.

Planning is not performed by a separate downstream candidate generator or resolver. Ego motion is decoded directly from the predicted ego token that lives inside the autoregressive world state.

A conservative inference reconstruction is:

```text
history occupancy + ego history
→ current world tokens
→ predict next {scene, ego} token set
→ decode ego displacement
→ feed predicted {scene, ego} state back
→ repeat
→ ego trajectory
```

## 1.5 Core mechanism deletion test

If the scene and ego processes are separated into:

```text
scene forecast
→ independent downstream planner
```

then OccWorld loses the paper's central claim that autonomous driving can be formulated as joint autoregressive evolution of the environment and ego vehicle in one occupancy-world state.

The paper's own ablation supports this: removing ego prediction or ego temporal modeling degrades not just planning but world forecasting.

## 1.6 What OccWorld is not

OccWorld is not proposal-conditioned counterfactual evaluation. It does not first produce multiple ego plans and then simulate their consequences.

It is also not a learned scene scorer. Its planning output is generated as part of the future world-state sequence itself.

---

# 2. DrivingGPT

## 2.1 Author-stated scientific problem

DrivingGPT starts from a different integration problem. Existing visual world models—especially diffusion-based ones—are good at video generation but awkward at representing and generating heterogeneous modalities such as driving actions.

The paper asks whether **world modeling and planning can be reduced to one ordinary next-token prediction problem**.

Its answer is to build a discrete multimodal driving language.

## 2.2 What is actually “joint”

DrivingGPT separately tokenizes:

```text
image frame → visual tokens z_t
drive motion → action tokens q_t
```

and forms an interleaved driving sequence:

```text
z_1, q_1, z_2, q_2, ..., z_T, q_T
```

A single causal autoregressive Transformer models this entire sequence by standard next-token prediction.

This means DrivingGPT's jointness is not mathematical simultaneity. It is a **shared autoregressive language with an explicit causal token order**.

At a coarse level world/action are unified; at a fine level one token still precedes another and therefore conditions it.

## 2.3 Training computation

Simplified:

```text
driving video frames → VQ image tokens z
frame-to-frame relative ego motion → binned action tokens q

interleave z and q
→ one autoregressive Transformer
→ cross-entropy next-token prediction over a unified vocabulary
```

Image-token losses and action-token losses are instances of the same next-token objective.

The representation unification is therefore stronger than merely sharing a backbone: image and action symbols inhabit one sequence-modeling problem.

## 2.4 Planning/inference computation

For planning, generated action tokens are decoded back into framewise relative driving motion. The same model can also generate visual tokens, which are decoded by the VQ-VAE.

The important fact is that action generation is not a separate learned planner attached after an already-completed world forecast. Action tokens are native elements of the autoregressive driving sequence.

However, this should not be over-described as “world and action emitted simultaneously”. The sequence factorization still imposes a causal order through the interleaved token stream.

## 2.5 Core mechanism deletion test

If image and action streams are separated into two task-specific models or heads with no common driving-language sequence, the main contribution collapses. DrivingGPT's scientific claim is precisely that both tasks can be represented in one autoregressive token language and optimized by one next-token objective.

Removing video/image prediction while leaving a conventional action-only autoregressive policy would still produce a planner, but it would no longer test the paper's main unification thesis.

## 2.6 What DrivingGPT is not

DrivingGPT is not equivalent to OccWorld merely because both generate “world and ego”. OccWorld's joint variable is a next occupancy-world state containing scene and ego tokens. DrivingGPT's primitive object is an **interleaved multimodal temporal token sequence** with a next-token causal factorization.

It is also not Gen-Drive-style generate-many-scenes-then-score planning: there is no separate learned scene evaluator as the core commitment mechanism in the paper's main formulation.

---

# 3. GenAD

## 3.1 Author-stated scientific problem

GenAD attacks the conventional prediction-before-planning decomposition from the perspective of interaction and trajectory structure.

Its argument is:

- the future ego motion changes the reactions of surrounding agents;
- serially predicting other agents before planning ego motion therefore misses high-order interaction;
- realistic multi-agent trajectories have strong structural priors that ordinary direct decoders underuse.

GenAD therefore casts end-to-end driving as **future-trajectory generation**.

## 3.2 What is actually “joint”

GenAD does not generate future RGB or occupancy worlds. Its future object is a set of trajectories for ego and surrounding agents.

It builds an instance-centric representation containing agent tokens, ego token, and map information, then learns a VAE structural latent space from future trajectories. A GRU evolves instances through that latent space and a waypoint decoder reconstructs future motion.

Thus GenAD's jointness is:

> **ego future trajectories and surrounding-agent future trajectories are sampled/generated together in one learned structural trajectory space.**

The “world” here is fundamentally interaction geometry in multi-agent trajectory space, not a visual or dense scene state.

## 3.3 Training computation

Simplified:

```text
multi-camera observations
→ BEV features
→ map tokens + agent tokens + ego token
→ instance-centric scene representation I

GT ego + agent future trajectories
→ future trajectory encoder
→ structural latent trajectory distribution Z

Z + instance representation
→ temporal GRU generator
→ waypoint decoder
→ reconstructed ego + agent futures
→ trajectory / prior losses
```

## 3.4 Inference computation

The future trajectory encoder is discarded at inference. The model predicts/samples a latent state from the instance-conditioned distribution and passes it through the latent trajectory generator and waypoint decoder.

```text
current instance-centric scene representation
→ sample z ~ p(z | I)
→ GRU future generator
→ decode ego + agent trajectories
→ ego trajectory is the plan
```

There is no later candidate-world evaluator in the main method.

## 3.5 Core mechanism deletion test

If ego planning is separated from other-agent future generation and placed downstream of a completed motion-prediction module, GenAD collapses toward the serial paradigm it explicitly criticizes.

If the structural trajectory latent prior is removed, another major paper contribution disappears, but the high-order interaction claim and the structural-prior claim should be kept conceptually distinct: GenAD contains both.

## 3.6 What GenAD is not

GenAD's “joint future” is not the same object as DrivingGPT's image/action token language and not the same object as OccWorld's occupancy+ego world state.

It is also not Gen-Drive despite both generating ego and surrounding-agent futures: GenAD directly obtains planning from the generated latent future, whereas Gen-Drive makes explicit scenario evaluation a central planning operation.

---

# 4. Gen-Drive

## 4.1 Author-stated scientific problem

Gen-Drive argues that deterministic prediction-and-planning does not adequately capture uncertainty, multimodality, and mutual interaction among agents.

Its proposed planning paradigm is explicitly:

```text
generation → evaluation
```

The method therefore contains three coupled scientific components:

1. a diffusion generator for joint multi-agent future scenarios;
2. a learned scene evaluator/reward model;
3. RL fine-tuning of the generator using that learned reward.

## 4.2 What is actually “joint”

The diffusion process operates in the joint future-action space of all modeled objects, including ego. Noise is applied to the full multi-agent future action tensor and denoised into a coherent future scenario.

So the generation component's jointness is:

> **ego and surrounding agents are co-generated as one interactive multi-agent future scenario.**

Again, this is not visual-world/action joint token modeling. The generated object is multi-agent future motion/state.

## 4.3 Training computation

Base generator:

```text
current/history object trajectories + map
→ query-centric scene encoder
→ diffusion denoiser over joint multi-agent future actions
→ future multi-agent scenario
```

Evaluator:

```text
generated future scenes
→ VLM-assisted pairwise preference labels
→ learned scene evaluator / reward model
```

Post-training:

```text
learned reward
→ RL fine-tuning of diffusion generator
→ shift generator toward high-reward future scenarios
```

The evaluator therefore has both a **selection role** and a **training-shaping role**.

## 4.4 Inference/planning computation

Gen-Drive supports single-sample planning, but the paper's generation-then-evaluation claim is clearest in the multi-sample regime:

```text
current scene
→ generate multiple joint ego+agent future scenarios in parallel
→ learned evaluator scores each generated scene/plan
→ choose the best scenario
→ use its ego component as the plan
```

The paper reports 16 generated scenes in parallel for the multiple-sample setting.

RL fine-tuning changes an important secondary fact: after the generator is sufficiently preference-shaped, even single-sample inference can become competitive, showing that evaluation knowledge can be partially compiled back into generation quality.

## 4.5 Core mechanism deletion test

Two deletions produce different collapses.

Delete joint interactive future generation but keep a trajectory scorer: the paper collapses toward ordinary proposal ranking and loses its “social future as the planning object” thesis.

Delete learned evaluation but keep the joint generator: the system remains a scenario generator, but loses the generation-then-evaluation decision mechanism that the paper presents as central for planning.

Thus the evaluator cannot be dismissed as a peripheral profile in this paper.

## 4.6 What Gen-Drive is not

Gen-Drive is not equivalent to GenAD merely because both include ego in a jointly generated multi-agent future. In Gen-Drive, **the generated future is an alternative to be evaluated and selected**. In GenAD, generation itself directly produces the planning result.

This is an example where similar future objects do not imply the same complete planning program.

---

# 5. Discrete-WAM

## 5.1 Author-stated scientific problem

Discrete-WAM is especially dangerous for premature classification because the paper deliberately contains multiple modes under one architecture.

Its stated bottlenecks are:

- observations, future states, decisions, and actions are poorly aligned in continuous latent spaces;
- world prediction and policy learning are often trained as separate modules/objectives;
- driving policy itself has hierarchical structure that a flat action decoder underuses.

The proposed framework therefore unifies **representation, world modeling, world-policy modeling, and policy generation** in one discrete token architecture.

## 5.2 What is actually “joint”

There is no single answer. The paper has three task families.

### World modeling

```text
context C_t + future action sequence A_{t+1:t+H}
→ predict future visual sequence V_{t+1:t+H}
```

This is action-conditioned world prediction. Future action is a condition, not a co-generated policy output.

### World-policy modeling

The model forms an interleaved future sequence:

```text
[A_{t+1}, V_{t+1}, ..., A_{t+H}, V_{t+H}]
```

with factorization:

```text
predict A_{t+h} from context + earlier world/action tokens
then predict V_{t+h} from the same history + current A_{t+h}
```

Action and future vision are both editing targets during joint training. This is genuine world-policy co-modeling, but still with a specified conditional structure.

### Policy modeling

```text
context
→ high-level decision D_t
→ future action sequence A_{t+1:t+H}
```

The deployed planning mechanism emphasized by the paper is hierarchical decision-conditioned action-token editing with confidence-guided iterative refinement.

## 5.3 Multi-stage training lifecycle

Discrete-WAM makes lifecycle separation unavoidable.

Stage 1:

```text
world modeling + world-policy context
→ vision prediction supervision only
```

Stage 2:

```text
joint visual + action prediction
→ stronger world-policy alignment
```

Stage 3:

```text
action-focused LoRA fine-tuning
→ discrete-diffusion policy generation/refinement
→ preserve world representations learned earlier
```

Therefore, the existence of a joint world-policy training mode does **not** prove that final planning inference must always jointly emit world and action.

## 5.4 Planning/inference computation

For downstream planning, the paper emphasizes:

```text
scene context
→ high-level decision token
→ parallel future action-token editing
→ confidence-based multi-round refinement
→ continuous acceleration / trajectory
```

The world model remains an important learned capability and enables separate counterfactual generation/surprise analysis, but the evidence read here does not justify reducing the complete downstream planner to “runtime joint world-action emission”.

That distinction matters because earlier project summaries treated the joint world-policy mode as if it uniquely defined the paper's final commitment topology.

## 5.5 Core mechanism deletion test

Several deletions target different paper claims.

Remove the shared discrete visual/action representation: the representation-alignment thesis collapses.

Remove joint world-policy training but keep policy editing: a planner still exists, but the paper loses its central claim that policy generation can be aligned with action-conditioned future dynamics in one training framework.

Remove hierarchical decision-conditioned action editing: the unified world-policy model still exists, but the paper loses its main structured downstream policy construction mechanism.

This paper therefore cannot be faithfully summarized by one “joint world-action” bit.

## 5.6 What Discrete-WAM is not

It is not automatically equivalent to DrivingGPT even though both use discrete visual/action tokens and interleaved sequences. DrivingGPT's main architecture is one causal next-token driving language. Discrete-WAM uses task-specific masks, discrete diffusion/token editing, multiple task families, staged world-policy alignment, and a distinct hierarchical policy decoder.

Nor is its final planner equivalent to OccWorld's autoregressive scene+ego evolution or Gen-Drive's multiple generated future scenarios + evaluator.

---

# 6. Cross-paper comparison — only after independent reconstruction

The five papers share a broad ambition:

> stop treating “world understanding” and “driving action” as completely unrelated tasks.

But that common ambition is too abstract to define a route.

The word `joint` expands into at least the following empirically different constructions in this set:

| Paper | Variables linked | Concrete meaning of “joint” | Final ego commitment |
|---|---|---|---|
| OccWorld | 3D occupancy scene + ego motion | scene tokens and ego token form one autoregressive next-world state | ego motion decoded directly from generated ego token |
| DrivingGPT | visual tokens + action tokens | interleaved multimodal sequence under one causal next-token model | generated action tokens decode to trajectory |
| GenAD | ego + surrounding-agent trajectories | co-generation in a shared structural trajectory latent space | generated ego trajectory is the plan |
| Gen-Drive | ego + surrounding-agent future scenarios | joint diffusion generation of social futures | multiple generated scenes can be scored; best future selected |
| Discrete-WAM | visual + action + decision token streams | shared discrete architecture with separate world, world-policy, and policy task modes | hierarchical decision + action-token editing for planning |

This table is **not a taxonomy**. It is a warning against treating one surface word as a mechanism category.

---

# 7. What Set D changes in our understanding

## 7.1 “Joint world-action” is currently too coarse to be a route label

The strongest finding from Set D is negative:

```text
joint(world, action)
```

is not yet a sufficiently defined mechanism statement.

Before using such a label, one must answer:

1. What exactly is the world variable?
2. What exactly is the action variable?
3. Are they one state, one sequence, one latent distribution, or merely two task targets?
4. What is the conditional/factorization order?
5. Is the jointness present at training, deployed planning, or both?
6. Does final commitment come directly from generation or from a later evaluator?

The five papers give materially different answers.

## 7.2 Representation unification, training unification, generative coupling, and decision coupling are different claims

DrivingGPT strongly unifies representation and autoregressive sequence modeling.

Discrete-WAM strongly unifies representation and training, but final policy generation has its own hierarchical action-editing path.

OccWorld jointly evolves environment and ego as one future world state.

GenAD jointly generates interactive multi-agent trajectories.

Gen-Drive jointly generates futures **and then makes explicit evaluation/selection a separate central decision step**.

These should not be collapsed simply because all authors use language such as “joint”, “unified”, or “generative”.

## 7.3 A paper may contain several scientifically central bridges

Discrete-WAM is the clearest case: representation alignment, world-policy co-training, and hierarchical policy construction are all central, but they live at different causal/lifecycle layers.

Gen-Drive likewise combines joint future generation, learned evaluation, and RL preference shaping.

This reinforces the Set C lesson that the comparison unit cannot always be “one paper = one route”.

## 7.4 The old joint-emission abstraction receives pressure, not a verdict

Earlier human/backend ontology used concepts such as `RJ`, `W5`, and a joint world-action carrier. Set D shows that such a compression may hide distinctions that are central to the papers.

However, this audit does **not** modify or delete those codes. The correct conclusion is only:

> the old joint-emission abstraction must not be treated as validated until it survives reconstruction of the actual joint variables, factorization, lifecycle, and final action-commitment mechanism.

---

# 8. Core mechanism deletion-test summary

OccWorld:

> Remove joint scene+ego autoregressive evolution → collapses toward separate forecast + planner.

DrivingGPT:

> Remove unified interleaved image/action driving language → collapses toward separate world model and planner.

GenAD:

> Remove co-generation of ego and other agents in structural trajectory space → collapses toward serial prediction/planning and loses high-order-interaction thesis.

Gen-Drive:

> Remove joint social-future generation or remove learned future evaluation → loses one of the two essential halves of generation-then-evaluation planning.

Discrete-WAM:

> Remove shared discrete world/action representation or world-policy joint training → policy decoder can remain, but the paper loses world-policy alignment; remove hierarchical action editing → world-policy model remains but downstream planning claim changes materially.

This asymmetry is itself informative. The five papers do not lose the same thing when “jointness” is removed.

---

# 9. Provisional methodological conclusion

Set D does **not** support creation of a `Joint` route.

It supports a stricter audit rule:

> Whenever a paper claims joint/unified world-action modeling, reconstruct the **joint variable, factorization, lifecycle, and commitment path** before comparing it with another paper.

The next comparison stage should continue to preserve this factual decomposition rather than compressing it into a new axis.

No ontology files were modified in this set.
