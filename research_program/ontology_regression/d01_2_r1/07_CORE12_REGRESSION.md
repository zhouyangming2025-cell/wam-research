# Core-12 Regression

This is a preservation-first check against the twelve-paper human route map. The core map is not rebuilt from the 23-artifact census. A paper/code or mode split remains a split where the existing map already requires one.

| Core paper/mode | Preserved route | R1 observation | Regression result |
|---|---|---|---|
| LAW | R0+W0+E0 ⊕ LA | Training-only action/future gradient remains distinct from runtime world use. | KEEP |
| Epona planning | R0+W0+E0 ⊕ LS | Direct planning with future branch bypassed remains valid. | KEEP |
| Epona self/external rollout | RG+W4+E0 | Generation terminal modes remain separate from planning mode. | KEEP |
| DriveLaW paper/code | R0+W2+E0 ⊕ LG | Online future-generative internal state remains distinct from W0 and W4. | KEEP |
| World4Drive | RB+W3+EW | Candidate endpoint plus factual/world agreement remains a distinct resolver family. | KEEP |
| WorldDrive | RB+W3+EV ⊕ LP→LT/LC | Teacher/surrogate learning remains an ordered learning distinction, not a new runtime axis. | KEEP |
| WoTE | RB+W4+(EF+ED) | Candidate horizon plus factual/decomposed outcomes remains intact. | KEEP |
| SeerDrive paper | RR+W3+E? | Paper-level reciprocal refinement remains separate from code-level candidate resolution. | KEEP; resolver evidence gap visible |
| SeerDrive code | RB+W3+(EF+ED) | Code path is not collapsed into the paper’s reciprocal route. | KEEP |
| Drive-JEPA PF | R0+W0+E0 ⊕ LP | Predictive representation transfer remains W0 when predictor is dropped. | KEEP |
| Drive-JEPA PB | RB+W0+EV/ED ⊕ LP→LC | Candidate scoring without online world carrier remains distinct from online consequence planning. | KEEP |
| Metis | R0+W0+E0 ⊕ LA | Action→video training influence and action-only deployment remain correctly separated. | KEEP |
| DynFlowDrive | RB+W0+(EW+EF+EY) ⊕ LC | World/simulator criterion retained only in scorer remains a learning/provenance distinction. | KEEP |
| Discrete-WAM policy/world/joint modes | RH, RG, RJ+W5 | Semantic decision, generation-only, and joint generation remain separate terminal modes. | KEEP |
| GraphWorld | RU+W1+E? | Current structured world remains distinguishable from future consequence; unresolved final commitment is not silently filled. | KEEP; resolver evidence gap visible |

## Core-12 result

No core route requires a new axis, deleted axis, or headline signature change. The R1 corrections outside the core map reinforce existing distinctions:

- lifecycle corrections protect W0 from training-only future branches;
- A19 validates the existing RR meaning;
- A13 validates RJ+W5 for a joint world/action process;
- A16 exposes a composition clarification, not a core-route collision.

The core map therefore passes preservation regression, subject to the held A16 amendment and the already visible SeerDrive/GraphWorld evidence boundaries.
