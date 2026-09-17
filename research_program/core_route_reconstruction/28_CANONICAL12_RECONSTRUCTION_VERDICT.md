# Canonical-12 Mechanism Reconstruction Verdict
Status: **RECONSTRUCTED-BUT-NOT-NORMATIVE**.

This file closes the current paper-first reconstruction pass. It does not modify `outputs/core_mechanism_12_v1/`, does not replace the existing ontology, and does not start D02.

## 1. What was completed

- Latest remote state was fetched before branch selection.
- The canonical reconstruction branch was selected: `origin/research/core-route-reconstruction` @ `5a775472fae2815cf306e8cb4a5a10073e921f9b`.
- A clean local work branch was created: `codex/canonical12-mechanism-reconstruction`.
- All 12 canonical raw Markdown files were found and mechanism-relevant sections were read.
- The prior reconstruction, regression, blind-test, deep-analysis, source-audit, and external-calibration corpora were inventoried.
- 18 scoped paper/mode/code artifacts were reconstructed without overwriting raw evidence.
- Prior claims were checked in a disposition ledger rather than copied as labels.
- A minimal six-program planning map plus a non-planning terminal-capability category was derived.

## 2. Main conclusion

The canonical set does not support a flat Cartesian ontology whose axes are all equally route-defining. It supports a layered mechanism map:

```text
artifact scope
→ deployment causal program
→ world-object lifecycle
→ candidate identity and commitment
→ training/transfer program
→ representation and evaluator profiles
```

The smallest currently defensible planning program set is:

1. direct action after world knowledge is compiled into the policy;
2. retained online world-state or generator-state conditioning of direct action;
3. online candidate-conditioned consequence evaluation with a common resolver;
4. candidate selection whose world criterion is compiled into a deployed scorer;
5. reciprocal world/planning refinement within one decision;
6. semantic decision formation followed by action generation.

World-only and joint world/action generation remain terminal capabilities unless the scoped deployment path proves that they determine action commitment.

## 3. Why this is not a return to the old dense table

The reconstruction does not create a field for every observed paper detail. It uses a small number of causal questions that repeatedly change the mechanism:

```text
Does a qualifying world object reach action at deployment?
Does it remain indexed by a candidate?
Is there a common resolver?
Does the plan feed back into world computation before commitment?
Is there an independent semantic decision before action?
How did training transfer world knowledge into the deployed path?
```

BEV versus latent, diffusion versus flow, RGB versus token, solver step count, teacher source, detach/freeze, and reward vocabulary remain audit attributes unless they change one of these semantic relations.

## 4. What the reconstruction corrected

1. **E-like resolver semantics are not sufficient route axes.** World4Drive, WorldDrive, and WoTE differ more importantly in consequence construction and lifecycle than in whether the scalar head is called compatibility, reward, or score.
2. **Training-only world use is not online world use.** LAW, Metis, and DynFlowDrive use future/world computation during learning while deploying without that branch.
3. **Joint is not one mechanism.** Epona, Metis, Discrete-WAM, and other joint claims differ in factorization, visibility, deployment fate, and commitment topology.
4. **Iteration is not one mechanism.** SeerDrive's feedback edge is distinct from diffusion solver steps, proposal refinement, or temporal state supervision.
5. **One paper is not one artifact.** Drive-JEPA, Discrete-WAM, Epona, and SeerDrive require scoped modes or paper/code boundaries.

## 5. Remaining unresolved issues

These are evidence debts, not automatic requests for new ontology axes:

| Issue | Why it matters | Current handling |
|---|---|---|
| SeerDrive final resolver | decides whether the paper's loop ends in a direct decoder or an explicit common resolver | paper loop retained; final commitment UNKNOWN |
| SeerDrive paper/code exact version mapping | code source reports a different topology | keep separate artifacts; do not merge |
| GraphWorld final multimodal commitment | raw paper gives hypotheses and probabilities but not an unambiguous final selection statement | retained online relational-state route; commitment UNKNOWN |
| Epona world-carrier gate | shared MST latent is world-model-trained but planning consumes it as history context, not a predicted consequence | conservative direct/compiled family placement; keep carrier qualification as a profile boundary |
| Drive-JEPA PB deployment source | paper establishes candidate scorer, but exact released implementation boundary is not the paper's PF/PB distinction | use paper artifact; code status remains separate |
| DynFlowDrive gradient/parameter reach | full end-to-end gradient path is not completely closed from raw text | retain training-only world criterion; mark edge confidence medium |
| Discrete-WAM post-training deployment fate | group sampling and reward are explicit in post-training, but routine inference commitment is not fully specified | keep post-training as an optional optimization artifact |
| World4Drive actual inference target | actual future latent supervises/teaches the scorer; it is not available as an inference observation | retain predicted candidate future online; factual target remains training provenance |

## 6. Acceptance boundary

This pass is successful as a reconstruction if “successful” means:

- the 12 raw papers can be described without reusing the old codebook;
- known false merges and false splits are exposed;
- implementation substitutions are separated from causal changes;
- paper/code/mode boundaries are explicit;
- no route is created solely to make every paper unique;
- no unresolved evidence is silently converted into absence or a new category.

It is not evidence that the six-program map is final field ontology. Promotion would require held-out, source-available papers that repeatedly instantiate the same forks and show that the fork changes the indispensable world-to-action bridge.

## 7. Repository action

No existing ontology file was modified. No raw Markdown was changed. No commit or push was performed, as required by the task boundary.
