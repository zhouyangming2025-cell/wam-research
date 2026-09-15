# NEXT_TASK

## 唯一下一任务

> **Deep-read Discrete-WAM under the WAM reading skill stack + Ontology V1/V1.1/V1.2/V1.3, as the next core-WAM stress test.**

## Completed normalization / stress tests

```text
P0048 LAW          COMPLETE v2
P0045 WoTE         COMPLETE v2
P0001 Epona        COMPLETE v2
P0042 WorldDrive   COMPLETE v2
P0046 World4Drive  COMPLETE v2
P0061 SeerDrive    COMPLETE v2 first pass
P0049 Drive-JEPA   COMPLETE v2 first pass
P0062 Metis        COMPLETE v2 first pass
P0063 DynFlowDrive COMPLETE v2 first pass
```

Canonical method stack:

```text
landscape/WAM_READING_SKILL_STACK.md
```

Canonical coordinate system:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_3_AMENDMENT.md
```

Current comparison layer:

```text
landscape/WAM_COMPARISON_MATRIX_V1.md
landscape/WAM_COMPARISON_MATRIX_V1_1_SEERDRIVE_EXTENSION.md
landscape/WAM_COMPARISON_MATRIX_V1_2_DRIVEJEPA_EXTENSION.md
landscape/WAM_COMPARISON_MATRIX_V1_2_METIS_EXTENSION.md
landscape/WAM_COMPARISON_MATRIX_V1_3_DYNFLOWDRIVE_EXTENSION.md
```

DynFlowDrive artifacts:

```text
papers/deep_analysis/P0063_DYNFLOWDRIVE_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_DYNFLOWDRIVE_AUDIT.md
landscape/P0063_DYNFLOWDRIVE_ONTOLOGY_PROJECTION.md
```

---

# Why Discrete-WAM is next

Discrete-WAM is currently positioned as a **unified discrete vision-action world-policy model**, but that phrase is too coarse to be scientifically useful.

The next audit must determine whether `unified` means any or all of:

```text
same tokenizer / codebook?
same token sequence?
same autoregressive Transformer?
same hidden representation?
same parameters?
same training loss?
same causal sequence factorization?
world tokens conditioning action tokens online?
action tokens conditioning future-world tokens online?
both world and action tokens generated at deployment?
```

The core question is:

> **Does Discrete-WAM genuinely make world evolution and policy actions part of one deployed generative process, or does it merely place discretized world/action targets under partially shared training machinery?**

---

# Mandatory audit targets

Resolve at minimum:

```text
1. sensor/history input and current-scene representation
2. vision/world tokenizer architecture and codebook provenance
3. action tokenizer / trajectory discretization and codebook provenance
4. whether world and action share token vocabulary or only a Transformer
5. exact token sequence ordering during training
6. exact causal attention mask / visibility graph
7. what future-world token represents physically
8. what action token represents physically
9. world-token target truth source
10. action-token / policy target truth source
11. whether future world is history-only predicted, action-conditioned, jointly generated, or autoregressive with action
12. F07 prediction temporal/observability geometry
13. F08 internal generative-token time vs physical future time
14. world→action forward information path during training
15. action→world forward information path during training
16. world→action / action→world paths at inference
17. shared representations vs shared parameters vs shared loss/gradients
18. whether world and action tokens are both generated at deployment
19. if world token generation can be skipped, what remains of world knowledge
20. autoregressive order: world-first, action-first, interleaved, parallel, iterative, or hierarchical
21. candidate/action multimodality and branch semantics
22. consequence truth under alternative action tokens
23. scorer/value model presence or absence
24. online generation latency and token count
25. matched ablations isolating discretization, world tokens, action tokens, and joint training
26. prediction/token quality → planning relevance evidence
27. source/version status
28. evaluation regime / reactivity
29. relation to DrivingGPT / Epona / Metis / DriveLaW / DynFlowDrive / World4Drive
```

---

# Required semantic attack: `unified` is vector-valued

Do not accept:

```text
world + action tokens in one paper
→ unified world-action model
```

Instead explicitly fill:

```text
representation sharing
parameter sharing
tokenizer/codebook sharing
sequence sharing
attention visibility
loss/gradient coupling
physical-time coupling
active-together-at-inference
```

A shared Transformer with separate vocabularies and masked information paths is scientifically different from one joint world-action token process.

---

# Required discrete-token attack

For every discrete latent/token, trace:

```text
continuous source object
→ tokenizer / quantizer
→ codebook index
→ token sequence position
→ prediction loss
→ decoder / downstream use
```

Then ask:

```text
what semantics are preserved by quantization?
what reconstruction information is lost?
are world/action codebooks aligned or independent?
does token likelihood have planning semantics?
```

Do not infer that discrete tokens are planning-relevant merely because they are efficiently autoregressive.

---

# Required temporal attack

Use both:

```text
F07 — what temporal information is visible when predicting target tokens?
F08 — does internal generation index correspond to physical scene time?
```

Separate:

```text
physical world timestep
AR token position
denoising / refinement step
world/action alternation step
```

Token generation order must not be confused with physical dynamics order.

---

# Required counterfactual attack

If alternative action tokens generate alternative world tokens, fill:

```text
candidate-specific world output?
per-action factual/simulated consequence target?
reactive surrounding-agent truth?
intervention-validity evidence?
```

Again:

```text
action token controls future generation
!= true counterfactual dynamics
```

---

# Required comparisons

Especially compare:

```text
DrivingGPT
= multimodal autoregressive world/action token modeling

Epona
= shared history latent + separate trajectory/visual generative branches

Metis
= specialized world/action experts + asymmetric training coupling + action-only deployment

DynFlowDrive
= candidate-conditioned world teacher removed at deployment

DriveLaW
= online learned world hidden state participates directly in action generation

World4Drive
= compact candidate endpoint future + online selector
```

The objective is to determine whether Discrete-WAM occupies a genuinely different interface/lifecycle cell or is a discretized implementation of an already known mechanism.

---

# Required workflow

```text
official paper / RAW_MD / supplement / official repo
→ mechanism + formula + token-sequence reconstruction
→ source/version gate
→ claim/evidence extraction
→ fill all Ontology V1 + V1.1 + V1.2 + V1.3 dimensions
→ immediate horizontal comparison
→ residue test
→ back-project any proposed new dimension before ontology extension
```

## Required output

```text
papers/deep_analysis/P0064_DISCRETE_WAM_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_DISCRETE_WAM_AUDIT.md
landscape/P0064_DISCRETE_WAM_ONTOLOGY_PROJECTION.md
comparison matrix extension/update
```

Add a new ontology dimension only if existing axes cannot express a scientifically important distinction and the residue survives back-projection.

---

# Stop condition

Do not move to GraphWorld until we can state without ambiguity:

```text
what exactly is discrete;
how world/action tokens are produced and supervised;
what `unified` means in representation/parameters/sequence/gradients;
what the training token order is;
what the inference token order is;
whether world tokens causally affect action selection online;
whether action tokens causally condition world prediction online;
whether both branches remain active at deployment;
what physical time each generated token corresponds to;
what consequence truth exists under alternative actions;
which ablation isolates the world-policy coupling;
what is proven vs author framing.
```

## After Discrete-WAM

```text
GraphWorld
```

## Still forbidden

```text
no research-gap declaration
no method design
no broad VLA expansion
no forced risk-field insertion
no novelty conclusion from empty ontology cells
```
