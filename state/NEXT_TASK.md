# NEXT_TASK

## 当前唯一下一任务

> **Verify, ingest and deep-read P0013 BridgeSim as the next Wave C.7 evaluation/control anchor. Keep research-direction convergence paused.**

## Current phase

~~~
broad WAM literature expansion     ACTIVE
Wave C.6                           CLOSED
Wave C.7                           ACTIVE
research-direction convergence     PAUSED
candidate-problem promotion        PAUSED
method design                      FORBIDDEN
~~~

## Completed immediately before this task

~~~
P0066 SAFE-SIM  COMPLETE
P0067 ProSim    COMPLETE
~~~

Canonical ProSim evidence:

~~~
papers/raw_md/P0067_ProSim/P0067_ProSim.source_note.md
papers/deep_analysis/P0067_PROSIM_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C7_PROSIM_AUDIT.md
~~~

ProSim’s retained mechanism judgment:

~~~
promptable closed-loop traffic behavior simulator
shared scene-token feedback
generated-agent response across rollout chunks
logged-future supervision
no paired real intervention-response truth
~~~

## Why BridgeSim is next

BridgeSim is the next retained raw source because it supplies an evaluation/control anchor for the open-loop → closed-loop gap:

~~~
cross-simulator policy evaluation
log-replay vs IDM vs adversarial traffic modes
long-horizon execution and replan frequency
objective mismatch and temporal covariate shift
~~~

The task is not to promote a method or reopen route selection. It is to determine which evaluation changes are caused by traffic reactivity, sensor/domain shift, controller/dynamics alignment, and horizon/replan frequency.

## Mandatory reconstruction

1. State, map, sensor and controller representation.
2. Traffic modes: log replay, IDM, adversarial and their control ownership.
3. Open-loop versus closed-loop protocol and exact action execution.
4. Replan frequency, horizon, dynamics/controller alignment and physical time.
5. Feedback coordinates F_e, F_s, F_a, F_b.
6. What BridgeSim measures that WOSAC/ADE do not.
7. Which claims are platform/evaluation claims versus policy claims.
8. Comparison against ProSim, SAFE-SIM and ReactSimBench where evidence allows.
9. Full A–P normalization inside one deep-analysis file; no projection or matrix extension.

## Source gate

Before normalization:

~~~
verify canonical BridgeSim paper/version/venue
verify attributable official project/code, if available
pin source ref/commit or record source-status boundary
use the retained raw layer as evidence; do not create a duplicate raw copy
~~~

## Planned artifacts

Create only the minimum evidence-bearing files:

~~~
papers/deep_analysis/P0013_BRIDGESIM_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C7_BRIDGESIM_AUDIT.md
~~~

Add a source note only if the existing raw layer does not already satisfy the source gate. Do not create an ontology projection, comparison-matrix extension, template, or candidate-problem document.

## Stop condition

BridgeSim is complete only when:

~~~
source/version and code-status gate resolved
traffic-mode/control ownership explicit
OL→CL protocol and time semantics explicit
feedback and truth-source boundaries explicit
evaluation attribution explicit
A–P audit and residue test included
ProSim/SAFE-SIM/ReactSimBench comparison bounded by evidence
~~~

Then advance to P0014 ReactSimBench.
