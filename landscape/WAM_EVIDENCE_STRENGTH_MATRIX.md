# WAM Evidence Strength Matrix

Last updated: 2026-09-15

Status: **ELEVEN-ANCHOR EVIDENCE QA**

Purpose: separate scientific evidence strength from source-code availability and from headline benchmark performance.

---

# 1. Evidence grades

```text
A = direct matched internal ablation / controlled comparison
B = source-code verified mechanism at locked commit
C = paper equation / architecture / training graph only
D = cross-paper headline comparison
E = author interpretation / qualitative claim only
```

Multiple grades can apply to one claim.

Source certainty is tracked independently:

```text
SOURCE-COMPLETE
SOURCE-PARTIAL
SOURCE-BLOCKED
```

A paper with unreleased code can still have strong A-level experimental evidence; it simply has lower implementation certainty.

---

# 2. Central mechanism evidence

| Anchor | Central mechanism claim | Best evidence grade | Source status | Confidence |
|---|---|---|---|---|
| LAW | factual future-latent auxiliary shapes planner representation; future output not required online | **A+B** | SOURCE-COMPLETE | HIGH |
| WoTE | online predicted future consequence improves evaluator; explicit utility drives selection | **A+B** | SOURCE-COMPLETE for decision-critical path | HIGH |
| Epona | shared historical representation feeds trajectory and visual branches; visual future optional for planning | **A+B** | SOURCE-COMPLETE core mechanism | HIGH |
| WorldDrive | distilled/lightweight future feature improves online trajectory ranking | **A+B** | SOURCE-COMPLETE core | HIGH |
| World4Drive | candidate-conditioned compact future latent + factual-mode scoring improves selection | **A+B** | SOURCE-COMPLETE core; benchmark branch caveat | HIGH core / MEDIUM benchmark equivalence |
| SeerDrive | future BEV and planner hidden state co-refinement improve planning | **A+C; B only for later released variant** | SOURCE-PARTIAL by design | MEDIUM-HIGH paper mechanism |
| Drive-JEPA | predictive representation pretraining and simulator-distilled proposal/selection planner are separable mechanisms | **A+B** | SOURCE-COMPLETE first pass | HIGH |
| Metis | asymmetric world-action co-training lets world loss shape action while deployment is action-only | **A+C** | SOURCE-BLOCKED | HIGH paper-level / MEDIUM implementation certainty |
| DynFlowDrive | candidate-conditioned flow WM acts as training-only mode/score teacher | **A+C** | SOURCE-BLOCKED | MEDIUM-HIGH paper-level |
| Discrete-WAM | shared discrete world-policy backbone supports world/action generation while primary planning can be policy-only | **A+C** | SOURCE-BLOCKED / MONITOR | MEDIUM-HIGH paper-level |
| GraphWorld | structured online world state directly conditions motion/planning queries without explicit long rollout | **A+C** | SOURCE-BLOCKED / MONITOR | MEDIUM-HIGH paper-level |

---

# 3. Strongest mechanism-isolating control

| Anchor | Strongest internal control | Evidence grade | Interpretation confidence |
|---|---|---|---|
| LAW | ± future-latent auxiliary | A | HIGH |
| WoTE | evaluator without future → + predicted future | A | HIGH |
| Epona | trajectory-only → joint trajectory+visual | A | HIGH |
| WorldDrive | trajectory-feature rewarder → + distilled future feature | A | HIGH |
| World4Drive | same intention/prior setting without WM → + WM | A | HIGH |
| SeerDrive | future-aware × iterative 2×2 | A | HIGH for component contribution |
| Drive-JEPA | pretraining decomposition + proposal/selection controls | A | HIGH |
| Metis | no-video co-training→video co-training; joint/isolated/asymmetric | A | HIGH paper-level |
| DynFlowDrive | Static WM→Flow WM; selection-factor ladder | A | HIGH paper-level |
| Discrete-WAM | scratch/FT/world-oriented pretraining + decision/RL ladders | A | MEDIUM because full joint world-policy effect not cleanly isolated |
| GraphWorld | baseline→ECIG→WSCP; Stage I→II; diffusion→flow; dense→ego-star | A | HIGH for bundle/component contribution |

---

# 4. World→planning causality strength

This section asks a narrower question:

> How directly does the evidence isolate that the world-related mechanism, rather than unrelated architecture/training changes, causes planning improvement?

| Anchor | World→planning attribution strength | Reason |
|---|---|---|
| LAW | **STRONG** | matched future-auxiliary toggle |
| WoTE | **STRONG** | evaluator held while future input added |
| Epona | **MODERATE-STRONG** | joint visual branch toggle, but exact beneficial visual property unidentified |
| WorldDrive | **STRONG for distilled future feature; MODERATE for total WAM stack** | clean rewarder→future-feature step; large foundation/video prior confound in total score |
| World4Drive | **STRONG for compact future module contribution** | matched no-WM→WM control |
| SeerDrive | **STRONG for future/iteration modules, weaker for causal-world interpretation** | 2×2 ablation; internal loop ≠ environment causality |
| Drive-JEPA | **MODERATE** | predictive pretraining helps, but representation/domain-data effects not causal future-dynamics proof |
| Metis | **MODERATE-STRONG** | video co-training and attention topology ablations; no independent fidelity→planning link |
| DynFlowDrive | **MODERATE-STRONG** | flow-vs-static and score decomposition; paper math/code uncertainty remains |
| Discrete-WAM | **MODERATE** | world-oriented pretraining delta modest/confounded; decision and RL effects independently large |
| GraphWorld | **MODERATE-STRONG for WSCP bundle; WEAK for factual future-state supervision as main cause** | WSCP large gain, Stage-II t+1 consistency only modest gain |

---

# 5. Future/world truth evidence

| Anchor | Future/world target evidence | Grade | Key boundary |
|---|---|---|---|
| LAW | factual future frame encoded by same encoder | B+C | one factual future |
| WoTE | structured/pseudo future + audited logged surrounding-agent path | B+C | non-reactive alternative consequences |
| Epona | factual future visual + logged ego trajectory during training | B+C | alternative-action futures not factual |
| WorldDrive | factual WM training + teacher-generated candidate future representation | B+C | teacher output ≠ observed counterfactual truth |
| World4Drive | one factual future latent assigns one of K hypotheses | B+C | K hypotheses ≠ K truths |
| SeerDrive | factual future BEV / WTA mode target | C | released implementation differs from original graph |
| Drive-JEPA | EMA representation target under masking | B+C | same-window masked prediction ≠ unseen causal future |
| Metis | factual future video | C | code unavailable |
| DynFlowDrive | factual future latent endpoint | C | flow intermediate coordinate not factual intermediate time |
| Discrete-WAM | factual future visual tokens under logged action | C | perturbation outputs lack matched alternative truth |
| GraphWorld | hypothesis-derived W_tgt + actual t+1 stop-grad state consistency | C | main flow target not direct factual future encoding |

---

# 6. Counterfactual / reactive evidence strength

| Anchor | Candidate/action-specific output | Reactive alternative truth evidence | Grade for intervention validity |
|---|---:|---|---|
| LAW | limited | absent | E |
| WoTE | YES | surrounding-agent reactivity absent in audited path | B for limitation / **no positive intervention proof** |
| Epona | controllable future | not established | C only |
| WorldDrive | YES | not established | C only |
| World4Drive | YES | absent | B/C for one-factual-target structure |
| SeerDrive | YES modes | absent | C |
| Drive-JEPA | N/A | absent | N/A |
| Metis | action-conditioned | not established | C |
| DynFlowDrive | YES training branches | absent | C |
| Discrete-WAM | YES perturbable generation | not established | C |
| GraphWorld | no per-candidate world branch | absent | C |

Eleven-anchor conclusion:

```text
strong intervention-validated reactive counterfactual dynamics = NOT ESTABLISHED
```

This is an evidence boundary, not yet a final research-gap declaration.

---

# 7. Safety / value evidence strength

| Anchor | Explicit safety/value mechanism | Evidence grade | Correct interpretation |
|---|---|---|---|
| WoTE | explicit collision/DAC/TTC/comfort/progress/imitation utility | **A+B** | true online utility-based selection |
| WorldDrive | PDMS/PDM-style preference/ranking | **A+B** | value/ranking supervision, not explicit risk field |
| Drive-JEPA | simulator-distilled proposal/score supervision | **A+B** | value/scorer teacher independent of JEPA predictor |
| DynFlowDrive | world-derived positive mode / learned score | **A+C** | decision supervision, not explicit risk state |
| Discrete-WAM | high-level decision target + RL/EPDMS-like reward | **A+C** | reward/value on policy side, no online future utility head |
| World4Drive | factual-mode ScoreNet | **A+B** | consistency/mode score, not explicit safety utility |
| GraphWorld | no explicit value; collision improvements | **A+C** | safety emerges from interaction representation/planning |
| Epona | no explicit utility | A+B for planning gains | joint representation ≠ explicit risk |
| LAW | no explicit utility | A+B | auxiliary representation only |
| Metis | no explicit utility | A+C | world-action co-training |
| SeerDrive | no explicit utility | A+C | future-aware refinement |

---

# 8. World fidelity → planning evidence

This is one of the weakest evidence areas across the field.

| Anchor | Dedicated world/fidelity measure | Clean monotonic fidelity→planning test? | Verdict |
|---|---:|---:|---|
| Epona | YES visual generation metrics | NO | NOT ESTABLISHED |
| WorldDrive | YES/teacher representation quality | partial/confounded | WEAK-MODERATE |
| Metis | limited/qualitative in audited paper | NO | NOT ESTABLISHED |
| DynFlowDrive | flow/reconstruction/stability objectives | NO physical-fidelity ladder | NOT ESTABLISHED |
| Discrete-WAM | YES FID/FVD | NO | NOT ESTABLISHED |
| GraphWorld | no directly comparable physical world fidelity metric | NO | NOT ESTABLISHED |
| WoTE | consequence prediction useful via evaluator ablation | planning link stronger than generic fidelity link | FUTURE-USEFULNESS ESTABLISHED, FIDELITY CAUSALITY NOT |
| World4Drive | mode/future-latent mechanism ablation | no physical-fidelity monotonic test | NOT ESTABLISHED |
| SeerDrive | future-BEV module ablation | no fidelity→planning monotonic relation | NOT ESTABLISHED |
| LAW | future-latent auxiliary ablation | no fidelity ladder | NOT ESTABLISHED |
| Drive-JEPA | predictive representation controls | no world-fidelity causal ladder | NOT ESTABLISHED |

Field-level conclusion:

> Better *decision-relevant future information* is often supported; better *generic world fidelity* as the causal source of better planning is not cleanly established by the current anchor set.

---

# 9. Evaluation evidence hierarchy

| Evidence regime | Strength for policy competence | Strength for WM causal/reactive validity |
|---|---|---|
| matched internal ablation on same benchmark | HIGH mechanism attribution | depends on target/evaluation truth |
| Bench2Drive/CARLA reactive closed loop | HIGH final-policy interaction evidence | MEDIUM/LOW internal-WM validity unless explicitly probed |
| NAVSIM non-reactive pseudo-simulation | HIGH standardized planning evidence | LOW reactive-agent validity |
| nuScenes open-loop planning | MEDIUM offline planning evidence | LOW closed-loop/reactive validity |
| visual autoregressive rollout | HIGH generative rollout evidence | LOW policy-environment evidence |
| headline cross-paper SOTA table | LOW causal attribution | LOW |

---

# 10. Source certainty matrix

| Anchor | Source status | Main implementation uncertainty |
|---|---|---|
| LAW | SOURCE-COMPLETE | low |
| WoTE | SOURCE-COMPLETE decision-critical path | broader simulator variants not exhaustively audited |
| Epona | SOURCE-COMPLETE core mechanism | exact checkpoint/table parity non-blocking |
| WorldDrive | SOURCE-COMPLETE core | full benchmark/training provenance complexity |
| World4Drive | SOURCE-COMPLETE core / PARTIAL NAVSIM equivalence | NAVSIM branch mapping |
| SeerDrive | SOURCE-PARTIAL by design | released code is later WoTE-integrated variant |
| Drive-JEPA | SOURCE-COMPLETE first pass | broader paths may remain |
| Metis | SOURCE-BLOCKED | forward/detach/freeze details |
| DynFlowDrive | SOURCE-BLOCKED | implementation and equation/procedure ambiguity |
| Discrete-WAM | SOURCE-BLOCKED/MONITOR | scheduler/detach/task routing |
| GraphWorld | SOURCE-BLOCKED/MONITOR | exact graph/flow/runtime routing |

---

# 11. Evidence QA conclusions

High-confidence findings across the eleven anchors:

```text
1. future/world knowledge can improve planning without mandatory online future generation;
2. online predicted future can improve selection/ranking in matched controls;
3. training-time jointness and deployment-time model-basedness are independent;
4. internal refinement/solver steps are not physical-time rollout;
5. multiple predicted futures do not establish multiple counterfactual truths;
6. long-horizon planning does not require long-horizon explicit world rollout;
7. lower collision does not imply explicit risk-state learning.
```

Still weakly established / unresolved at field level:

```text
1. generic world-generation fidelity → planning causality;
2. intervention-valid reactive multi-agent counterfactual dynamics;
3. whether deeper online world rollout consistently beats compact world-state conditioning under matched compute/data;
4. whether explicit value/risk modeling adds benefit beyond strong interaction representation under matched architecture;
5. which future information should be retained online versus compressed into policy parameters.
```

These unresolved items are candidates for **scientific tensions**, not yet final research gaps.
