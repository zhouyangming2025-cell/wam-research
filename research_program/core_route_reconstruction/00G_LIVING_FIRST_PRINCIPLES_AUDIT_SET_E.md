# Living first-principles audit — Set E continuation

Status: living research memory; records why judgments changed. This file does not amend ontology.

---

## 56. Why Set E was chosen

After Set D showed that `joint` is too overloaded to define a route, another dangerous surface word remained: `iterative`.

Several papers seemed to support a neat story about reciprocal world/planning loops. But earlier project history showed that neat stories can become ontology before the papers have actually been separated.

Set E therefore froze five deliberately confusable papers:

- SeerDrive
- Drive-OccWorld
- PPAD
- GraphAD
- iPad

The working hypothesis was not “they are one family” but:

> if their iteration means different computations, the word itself must be prohibited from category formation.

---

## 57. First correction: iteration count is almost meaningless without the iterated state

The five papers all repeat computation, yet they repeat different objects.

SeerDrive repeats:

```text
future scene representation ↔ planner-refined ego representation
```

Drive-OccWorld repeats:

```text
future occupancy forecast → plan → plan-conditioned next future forecast
```

PPAD repeats:

```text
surrounding-agent prediction ↔ ego planning
```

GraphAD repeats:

```text
interaction graph ↔ predicted trajectories/features
```

iPad repeats:

```text
proposal geometry ↔ proposal-anchored image feature extraction
```

Therefore the existence of a loop or multiple rounds is not a mechanism identity.

---

## 58. Second correction: two real world/planning feedback methods still need not be the same mechanism

SeerDrive and Drive-OccWorld are the strongest pair in this set for genuine online world/planning feedback.

Initially this looked like evidence for one reciprocal route.

Deep reconstruction shows a material difference.

SeerDrive closes the loop in **algorithmic refinement space**:

```text
future BEV^(k)
→ planning^(k)
→ refined ego feature^(k)
→ future BEV^(k+1)
```

Drive-OccWorld closes the loop in **predicted future time**:

```text
state_(t+1)
→ choose trajectory_(t+1)
→ trajectory_(t+1) conditions state_(t+2)
→ choose trajectory_(t+2)
```

Both express the scientific intuition that future world and ego decision should interact, but their computation is not identical.

Do not decide yet whether this is one family with subtypes or two separate families.

---

## 59. Third correction: reciprocal prediction/planning is not sufficient for WAM membership

PPAD is an essential counterexample.

It performs a real deployed bidirectional interaction:

```text
ego plan so far
→ next surrounding-agent motion prediction
→ updated agent motion
→ next ego planning step
→ ...
```

Yet its predictive carrier is primarily structured agent motion and scene context, not necessarily an independently qualifying learned world/dynamics state under the WAM gate.

Therefore:

```text
reciprocal prediction/planning
≠ automatically a WAM mechanism
```

This reinforces the separation between:

1. domain/world qualification;
2. mechanism reconstruction after qualification.

A beautiful causal topology cannot substitute for a world-model gate.

---

## 60. Fourth correction: planner self-refinement can masquerade as world/planning feedback

iPad is the clean negative control.

Its central loop is:

```text
proposal
→ choose where to sample visual evidence
→ refine proposal query
→ updated proposal
```

The model also has proposal-centric future-agent prediction, which makes it easy to over-read as action-conditioned future reasoning.

But those prediction/map heads are auxiliary training tasks. The main iterative deployed computation is proposal-aware feature extraction and proposal refinement.

Therefore:

> a method can contain candidates, prediction, scoring, and iteration and still not execute a world-model consequence loop online.

This is exactly the kind of case that old coordinate systems were liable to misread.

---

## 61. Fifth correction: GraphAD's loop closes inside interaction modeling

GraphAD is another important negative/control case.

Future trajectory prediction affects Dynamic Scene Graph interactions; revised graph features affect future trajectories. This is a genuine reciprocal structure.

But the loop's scientific purpose is to improve explicit sparse interaction representation among agents and map elements. The final ego planning head consumes the graph-refined ego representation afterward.

So:

```text
graph ↔ prediction iteration
```

must not be silently rewritten as:

```text
world ↔ planning iteration
```

just because ego is one of the graph nodes and future trajectories are involved.

---

## 62. Emerging audit concept: loop-closure location

Set E suggests a useful *question*—not an axis:

> Where does the feedback loop close?

Observed answers include:

- inside proposal/feature extraction;
- inside graph/trajectory interaction modeling;
- between surrounding-agent prediction and ego planning;
- between predicted future scene and planner refinement;
- across selected action and the next temporal world forecast.

This question has high explanatory value because it prevents false equivalence.

However, it is explicitly **not promoted** to an ontology dimension. It remains a paper-reading diagnostic until broader evidence shows that it partitions the domain in a stable and scientifically meaningful way.

---

## 63. Core deletion tests sharpen the distinction

The shared surface word `iterative` disappears under different deletions:

SeerDrive:

> remove planner→world feedback and the method becomes a one-pass future-aware planner.

Drive-OccWorld:

> remove selected-plan→next-world conditioning and continuous temporal forecasting/planning disappears.

PPAD:

> remove ego-plan→next-agent-prediction feedback and the method becomes ordinary one-shot prediction→planning.

GraphAD:

> remove graph↔trajectory refinement and the explicit dynamic interaction mechanism weakens, though graph-based planning can remain.

iPad:

> remove proposal-anchored feature feedback and proposal iterations no longer organize perception around the developing plan.

Different collapse targets imply different underlying mechanisms.

---

## 64. Methodological update after Set E

Add one rule to the paper-first protocol:

> **For every recurrent/iterative architecture, write the feedback edge in variables before using any natural-language label.**

Examples:

```text
F_future^k → Ego^k → F_future^(k+1)
τ_t → s_(t+1) → τ_(t+1)
Ego_t → Agent_(t+1) → Ego_(t+1)
Graph^k → Traj^k → Graph^(k+1)
Proposal^k → ImageEvidence^k → Proposal^(k+1)
```

Only variable-level reconstruction makes the mechanisms comparable.

---

## 65. Current discipline remains unchanged

Set E does not create:

- an `Iterative` route;
- a `Reciprocal` ontology axis;
- a `LoopClosureProfile`;
- any new code.

The purpose is understanding before compression.

Detailed evidence reconstruction is in:

`21_PAPER_FIRST_RECONSTRUCTION_SET_E.md`
