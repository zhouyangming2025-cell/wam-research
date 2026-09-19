# Progressive Paper Teaching Protocol

Use this protocol when a paper needs more than a compact summary. It is designed for learners who can understand a semantic description but cannot yet reconstruct the mechanism, computation, or mathematics.

## 1. Build the teaching map

Before answering, write an internal map with five fields:

| Field | Question |
|---|---|
| Learner state | What can the learner already explain without copying the teacher's words? |
| Established ledger | Which definitions, distinctions, and causal links must not be retaught? |
| Paper mainline | What single causal path carries the paper's central idea? |
| Dependency graph | Which concepts must be understood before the next requested detail? |
| Evidence boundary | Which claims are verified, inferred, or still unchecked? |
| Next gate | What is the smallest new capability the learner needs now? |

Choose one next gate. Do not optimize for covering pages; optimize for making that gate reconstructable.

## 2. Control repetition and concept load

Before drafting each round, create this internal three-line budget:

```text
Established — reference only:
New — one primary mechanism, up to two supporting concepts:
Deferred — explicitly exclude from this round:
```

Apply these rules:

1. **Reference, do not replay.** Refer to established material in the shortest phrase that reconnects the chain. Do not reproduce its definition, table, example, formula, or conclusion.
2. **One representation per fact.** Explain a fact once in the most useful form. Do not repeat the same content as prose, a table, a flow diagram, and a closing recap.
3. **One main mechanism per round.** A mechanism is a causal operation the learner must be able to reconstruct, such as corruption, embedding lookup, attention routing, target construction, or parameter update. These are separate rounds unless the learner already knows the supporting operations.
4. **No defensive over-explanation.** Do not add adjacent background merely because it may become relevant later. Put it in `Deferred`.
5. **Repair locally.** If the learner questions one link, remove downstream material and fix that link; do not restart the surrounding chapter.

## 3. Phase A — semantic orientation

Start with one concrete task instance. Establish:

- what information is available;
- what must be produced;
- why the existing approach is insufficient on the paper's chosen axis;
- the paper's proposed change;
- the claimed benefit and its limit.

Avoid architecture names until their role is clear. Mark broad historical statements as provisional until the relevant literature has been checked.

Exit condition: the learner can explain the problem and proposal in ordinary language and can state one thing the proposal does not prove.

## 4. Phase B — mechanism and data flow

Trace one example through the pipeline. For every task mode or stage, record:

| Item | Required description |
|---|---|
| Known condition | What is supplied to the model? |
| Hidden or corrupted state | What is masked, noised, missing, or latent? |
| Target | What exact object should be recovered or predicted? |
| Supervision source | Where does the correct target come from? |
| Gradient destination | Which parameters can change from this loss? |
| Deployment status | Is this component or output used at inference? |

Keep three clocks separate:

1. **Data time** — past, current, and future frames or actions inside one example.
2. **Optimization time** — minibatches and parameter updates.
3. **Curriculum time** — training stages, task-mixture changes, freezing, or LoRA adaptation.

Do not infer sequential training merely because a paper lists several objectives. Verify whether tasks are mixed jointly, alternated, staged, or fine-tuned. If unclear, say so.

Exit condition: the learner can narrate one sample's path and identify which outputs create learning signals for which shared or separate parameters.

## 5. Phase C — representation choices

For every key representation, answer four questions:

1. What physical or semantic object is encoded?
2. What mathematical object stores it: continuous vector, discrete ID, distribution, coordinate, spline, action primitive, or something else?
3. Which operations become natural because of this choice?
4. What information, precision, or flexibility may be lost?

Then run one counterfactual using the nearest alternative. For example, if a method uses discrete visual tokens, explain exactly which training target, output head, corruption process, and decoder would change under a continuous latent. Do not claim that one representation is universally superior unless evidence supports it.

Exit condition: the learner can explain both the advantage and the cost of the chosen representation.

## 6. Phase D — concrete computation trace

### 6.1 Start with a notation ledger

Use stable names such as:

| Symbol role | Example convention |
|---|---|
| sequence position | `i` |
| physical time | `t` |
| token ID | `v_i` |
| candidate token ID | `k` |
| logit vector | `s_i` |
| predicted distribution | `p_i` |
| target distribution | `q_i` |
| model parameters | `theta` |
| edit round | `r` |

Adapt names to the paper, but never reuse one symbol for two roles.

### 6.2 Keep a shape ledger

At each step state:

- input object and shape;
- operation;
- output object and shape;
- which axis has semantic meaning;
- whether the value is observed, sampled, predicted, or learned.

### 6.3 Use realistic examples

Retain the actual structure and show sparse values. Example: say the vocabulary has 16,384 candidates, then display the target probabilities for token IDs 831, 4207, and 12501 plus the residual mass. This preserves the distinction between a candidate ID and its probability while keeping arithmetic readable.

Before using numbers, state their provenance once:

- `paper value` for a reported configuration or result;
- `teaching construction` for an invented value used to expose a mechanism;
- `inference` for a value or behavior deduced from stated facts;
- `unknown` when the source does not determine it.

Then ask whether the example exposes a computation or only decorates a verbal claim. A useful numerical example must do at least one of the following:

- distinguish namespaces that are easy to confuse;
- show how an output changes when an input changes;
- make a target, loss, normalization, shape, or update directly traceable;
- preserve a real structural property that a tiny toy example would destroy.

Otherwise omit the numbers.

### 6.4 Training trace checklist

Use the following as a multi-round map, not as a requirement to cover everything in one answer:

1. raw sample;
2. encoding or tokenization;
3. corruption, masking, or conditioning;
4. model input;
5. logits or continuous prediction;
6. target construction;
7. per-position loss;
8. aggregation into total loss;
9. computation graph back to affected parameters;
10. optimizer update;
11. what changes for the next minibatch.

For every loss, answer: “If this term decreases, what observable behavior is being encouraged?”

### 6.5 Inference trace checklist

Walk through:

1. available observation and command;
2. initialization of unknown variables;
3. one prediction or editing round;
4. confidence computation;
5. selection or resampling rule;
6. stopping condition;
7. decoding into the deployed output.

If confidence is the maximum predicted probability, say that it is confidence in the model's current preferred candidate, not confidence that the current token is already correct. These are different quantities.

Exit condition: the learner can reproduce the trace with dimensions and can point to where each target and update originates.

## 7. Phase E — bounded foundation detours

Open a detour when the learner asks “why does this formula do that?”, confuses a scalar result with a function, or cannot identify what a derivative is taken with respect to.

Use prerequisite routing. For example, deriving the softmax-cross-entropy gradient may require:

1. function versus evaluated value;
2. derivative as local sensitivity;
3. multivariable functions and partial derivatives;
4. composition and the chain rule;
5. logits and softmax probabilities;
6. cross-entropy as a function of those probabilities;
7. only then the combined result.

Teach one dependency at a time. Each detour must include:

- why this prerequisite is needed for the paper question;
- one realistic but bounded example;
- one reconstruction check;
- an explicit bookmark for returning to the paper.

Do not use “the optimizer handles it” to hide the computation. Do not derive every theorem either; stop at the depth needed for the learner's current question.

## 8. Phase F — evidence and scientific interpretation

Maintain a claim ledger when the explanation includes novelty, superiority, or historical comparison:

| Claim | Status | Locator or basis | Scope and caveat |
|---|---|---|---|
| architecture or objective | paper fact | section/equation/figure | paper version |
| mechanism benefit | author claim or inference | passage or reasoning | may lack isolation |
| measured improvement | direct evidence | table/metric | dataset and baseline |
| implementation behavior | code fact | file/function/commit | code version |
| novelty relative to field | literature synthesis | checked comparison set | never universal by default |

When evidence does not isolate a component, say that the result supports the full system rather than proving that component caused the gain.

## 9. Phase G — selective cross-paper comparison

Compare mechanisms, not paper titles. First identify the axis under discussion, then group only relevant works into families such as:

- continuous latent prediction;
- discrete token prediction;
- direct trajectory regression;
- action primitives or discretized controls;
- auxiliary world-model supervision;
- shared generative backbone.

For each relevant family, summarize approximate prevalence within the checked set, the common mechanism, and the meaningful difference from the focal paper. Omit papers that do not address that axis.

Use three labels:

- **Common foundation** — broadly shared idea or routine practice.
- **Subset choice** — one of several established design families.
- **Paper-specific contribution** — a combination or mechanism that appears distinctive within the checked evidence.

Never infer uniqueness from absence in a small reading list.

## 10. Confusion recovery audit

When an explanation fails, inspect these likely causes before adding another example:

- The reason for an operation was omitted.
- Too many dependencies were introduced in one round.
- A symbol changed meaning or appeared before definition.
- A realistic-scale example still lacked causal logic.
- A toy example changed the real task's structure.
- Training, inference, data time, and curriculum time were mixed.
- A result was presented as a derivation.
- A scalar loss value was confused with the loss function.
- A paper statement was confused with the teacher's inference.
- A comparison included irrelevant papers or overstated scope.
- Established content was repeated in anticipation of confusion rather than because confusion was observed.
- The same claim was presented in several formats without adding a new relationship.
- Invented numbers created a concrete appearance without exposing a calculation.
- A simplified account changed “not visible because of masking” into “not present in the computation.”

Fix the earliest cause, not the latest visible symptom.

## 11. Preserve state across rounds

End a long teaching turn with an internal handoff in this form:

```text
Established:
Partially understood:
Blocked by prerequisite:
Paper location paused at:
Do not introduce yet:
Next reconstruction check:
```

The next turn should begin at the recorded gate. Do not restart the paper, replay the `Established` entries, or promise to connect everything in a single future response. A closing handoff is state, not a second summary: record only what changed during the current round.
