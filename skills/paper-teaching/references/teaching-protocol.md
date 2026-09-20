# Mechanism Deep-Dive and Confusion-Repair Protocol

Use this reference only after the detail-value gate has identified a mechanism, computation, or mathematical dependency worth teaching. The default claim-and-evidence workflow is defined in `SKILL.md` and `claim-evidence-note.md`.

## 1. Define the bounded gate

Before drafting, record:

```text
Established — reference only:
Question resolved this round:
Primary mechanism:
Necessary supporting concepts (maximum two):
Deferred:
Exit condition:
```

For a broad synthesis or research note, do not use the one-mechanism restriction. It applies to mechanism deep dives and confusion repair.

## 2. Trace necessity, not just sequence

Explain each step as:

```text
current problem
→ why the next operation is needed
→ operation
→ resulting object
→ boundary or failure mode
```

For each relevant module or task stage, identify:

| Item | Required description |
|---|---|
| Known condition | What information is supplied? |
| Unknown/noisy state | What is missing, masked, corrupted, sampled, or latent? |
| Operation | What transformation or interaction occurs? |
| Output | What exact object is produced? |
| Target | What should be recovered or predicted? |
| Supervision source | Where does the target come from? |
| Gradient destination | Which parameters can this loss change? |
| Deployment status | Is this component or output used at inference? |

Name modules only after establishing their jobs.

## 3. Keep lifecycles and clocks separate

Do not mix:

1. **Data time** — past, current, and future states within one sample.
2. **Solver time** — diffusion, flow, token-edit, or refinement iterations over the same prediction.
3. **Optimization time** — minibatches and parameter updates.
4. **Curriculum time** — training stages, task-mixture changes, freezing, adapters, or post-training.
5. **Deployment lifecycle** — modules and outputs retained, bypassed, distilled, or removed at inference.

Do not infer sequential stages merely because a paper lists several objectives. Verify whether tasks are mixed, alternated, staged, frozen, or fine-tuned; otherwise mark the schedule unknown.

## 4. Preserve notation and realistic structure

Maintain a local notation ledger. Keep these namespaces distinct:

- physical time;
- sequence or spatial position;
- token ID;
- vector coordinate;
- class candidate;
- probability/logit entry;
- optimization step;
- editing or denoising round.

At each computational step, state the input object and shape, operation, output object and shape, semantic axis, and whether each value is observed, sampled, predicted, targeted, or learned.

Use realistic vocabulary sizes, tensor ranks, and sequence structure when they matter. Show a sparse subset of a large vector rather than shrinking a 16,384-class problem into a four-class world that changes what an index means.

Before using numbers, label their provenance once:

- `paper value` — reported configuration or result;
- `teaching construction` — invented solely to expose a mechanism;
- `inference` — deduced from verified facts;
- `unknown` — not determined by the source.

Run a pseudo-concreteness check: if removing the numbers leaves the same understanding, remove them. Do not replace a soft target with one-hot merely to simplify arithmetic unless the simplification and its limits are explicit.

## 5. Training computation trace

Use only the portion required by the learner's question:

1. raw sample;
2. encoding/tokenization;
3. corruption, masking, or conditioning;
4. effective model input;
5. prediction or logits;
6. target construction;
7. per-position loss;
8. total-loss aggregation;
9. computation graph to affected parameters;
10. optimizer update;
11. changed behavior on later samples.

For every loss, answer: “If this term decreases, what observable behavior is encouraged?”

Do not describe clean targets as absent when they may remain in the computation but be isolated by an attention mask.

## 6. Inference computation trace

When relevant, walk through:

1. available observations and commands;
2. initialization of unknown variables;
3. one prediction/editing step;
4. confidence or uncertainty computation;
5. selection, freezing, replacement, or resampling rule;
6. stopping condition;
7. decoding into the deployed output.

If confidence is the maximum predicted probability, say that it measures confidence in the model's current preferred candidate, not automatically confidence that the current input token is correct.

## 7. Formula discipline

Never present a compact formula as if it were an explanation.

- Define each symbol where it first appears in the current round.
- Separate learned parameters, intermediate variables, constants, targets, and observed values.
- Distinguish a function such as `L(theta)` from an evaluated value such as `L(theta_current)=2.00`.
- If a result such as `dL/ds = p - q` is required, derive it only after its prerequisites are established, or explicitly label it as a temporarily used result.
- Before connecting one scalar loss to many parameters, establish multivariable dependence, partial derivatives, the computation graph, and the chain rule or automatic differentiation.
- For soft-target cross-entropy, do not claim the minimum is zero. When relevant, use `H(q,p)=H(q)+KL(q||p)`: matching `p` to `q` minimizes the loss at `H(q)`.

If the prerequisite chain is large, open a bounded foundation detour and bookmark the exact paper location to resume.

## 8. Foundation detours

Open a detour only when the unresolved prerequisite blocks the paper question. Teach one dependency at a time. A detour must contain:

- why this prerequisite is needed now;
- one realistic, bounded example;
- one reconstruction check;
- the bookmark for returning to the paper.

Do not use “the optimizer handles it” to conceal the mechanism, and do not derive unrelated theory merely because it is adjacent.

## 9. Confusion repair

When the learner reports confusion:

1. Restate the first failing link precisely.
2. Classify the gap as vocabulary, mechanism, computation, mathematics, evidence, lifecycle, or notation.
3. Remove concepts introduced downstream of that link.
4. Check for an omitted reason, unstable symbol, mixed clock, pseudo-concrete number, or teaching simplification that changed the real structure.
5. Re-explain with the same scenario at one lower dependency level.
6. Ask one bounded reconstruction question rather than “懂了吗?”.
7. Resume only after the link is stable.

Do not restart the whole chapter or replay the established ledger.

## 10. Round and handoff contract

For a deep-dive round:

- resolve one exact question;
- add one primary mechanism and at most two necessary supporting concepts;
- reuse stable notation without replaying setup;
- separate training from inference and teaching constructions from paper facts;
- finish with one newly established link and one next unresolved link, without a full recap.

For a multi-round internal handoff, record only changed state:

```text
Established:
Partially understood:
Blocked by prerequisite:
Paper location paused at:
Do not introduce yet:
Next reconstruction check:
```
