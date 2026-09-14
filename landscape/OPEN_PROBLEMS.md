# Open Problems — Planning-centric WAM

This document records recurring tensions found across methods. It is not a final gap claim.

## 1. World Fidelity vs Decision Value

A more realistic world simulation does not automatically produce better planning.

Question:

What future information is decision-relevant?

## 2. Prediction vs Counterfactual Reasoning

Action-conditioned generation is not automatically true counterfactual modeling.

Question:

Can a world model reliably predict futures caused by alternative ego actions?

## 3. Long Horizon vs Planning Reliability

Longer prediction horizon does not necessarily mean better long-horizon decisions.

Question:

Which future horizon matters for planning?

## 4. Representation vs Explicit Safety Reasoning

Risk and uncertainty are often implicit.

Question:

Should safety be an explicit future world representation?

## 5. Evaluation Gap

Offline metrics do not always reflect closed-loop driving capability.

Question:

How should world models be evaluated as planning systems?

## Research Rule

A candidate problem must survive:

- prior art review
- strong baseline comparison
- simpler explanation analysis
- evaluation feasibility
