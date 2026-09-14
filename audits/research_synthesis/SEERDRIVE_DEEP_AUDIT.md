# SeerDrive Deep Audit (Phase D-2)

## Status

This document is a research synthesis artifact. It is not a replacement for the original paper. Claims must be verified against the canonical PDF/code before final scientific conclusions.

## 1. Position in WAM evolution

SeerDrive is analyzed under the WAM Planning Interface Framework, not by its paper section order.

Core question:

> Does the method move from future prediction toward interactive action-conditioned world evolution?

The key distinction is:

- Future prediction:
  P(Future | History)
- Planning-relevant world modeling:
  P(Future | History, Action)

## 2. Main research question

A planning-centric world model should answer:

"If ego executes action A, how will the world respond?"

not only:

"What is likely to happen next?"

## 3. Framework classification (initial)

| Dimension | Initial assessment |
|---|---|
| Future role | Interactive/action-conditioned future modeling |
| World model role | World evolution model |
| Planner coupling | More coupled than simple evaluator architectures |
| Action role | Candidate action influencing future evolution |
| Inference usage | Planning-relevant |
| Main research question | Whether interaction is truly causal |

## 4. Comparison with previous WAM directions

WorldDrive:

Action -> Future representation -> Decision

Key idea: future latent becomes planning evidence.

SeerDrive direction:

Action <-> Future evolution <-> Planning

Key idea: world evolution and planning are jointly modeled.

## 5. Critical audit questions

### Q1. Does the model learn action-conditioned dynamics?

Need verify whether:

P(Future | History, Action)

is truly learned, rather than:

P(Future | History)

with trajectory information as auxiliary input.

### Q2. Does it solve counterfactual future?

Real driving data mainly provides:

(History, Expert Action, Expert Future)

Planning requires:

(History, Candidate Action, Candidate Future)

The gap remains:

alternative action supervision.

### Q3. Are other agents reactive?

A true interactive world model requires:

ego action -> environment response

not only ego-conditioned prediction with frozen agents.

## 6. Research significance

SeerDrive is important because it targets the transition:

future prediction
    ->
future evaluation
    ->
interactive world modeling

However, the central scientific question remains whether learned future evolution provides reliable counterfactual consequences for planning.

## 7. Relation to risk-aware planning (hypothesis only)

Potential connection:

Future state != planning importance.

A planner may need:

future state -> decision relevance -> action selection

This should not yet be interpreted as a risk-field proposal. It is a hypothesis requiring validation across WAM methods.
