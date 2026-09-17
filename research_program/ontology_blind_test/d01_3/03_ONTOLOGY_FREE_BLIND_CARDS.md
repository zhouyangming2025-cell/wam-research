# D01.3 Ontology-Free Blind Cards

These cards were written after the source/artifact freeze. They intentionally describe mechanism objects without assigning any human-route or normative ontology code. They are the input to the blind projection stage.

## Card GAD-PLAN — GraphAD planning path

### Deployment route

A temporally aggregated scene is converted into structured agent/map objects; predicted future motion proposals define interaction edges, iterative graph updates refine those predictions, and the processed ego object directly produces one planning trajectory, optionally followed by occupancy-based safety optimization.

### Ordered learning route

Detection and map learning precede tracking, map, and graph-based motion learning; the image backbone is frozen in the intermediate stage; occupancy and planning are added in a final multi-task stage with motion, occupancy, and planning losses.

### Object/evidence table

| object | semantic role | lifecycle | evidence |
|---|---|---|---|
| multi-frame BEV and structured agent/map nodes | current scene representation and structured environment description | deployed | PAPER FACT |
| multi-modal future trajectories for dynamic agents | temporally organized predicted consequences used to determine graph neighbors | deployed | PAPER FACT |
| graph edge construction from future trajectory distances | future-aware interaction operation | deployed | PAPER FACT |
| planning head | direct ego trajectory formation | deployed | PAPER FACT |
| occupancy prediction and post-optimization | collision-avoidance refinement of the planning output | paper says available; exact implementation boundary unresolved | PAPER FACT / UNKNOWN |
| final ego trajectory | terminal action representation | deployed | PAPER FACT |

### Candidate/resolver status

The paper exposes multiple future trajectories for traffic agents, but does not establish that the final ego trajectory is selected from an identity-preserving bank by one common resolver. The final planning head is described as directly predicting the ego trajectory.

### Key UNKNOWNs

- Whether the occupancy post-optimization enumerates final ego candidates or only continuously refines one trajectory.
- Whether the repeated graph layers should be interpreted as reciprocal policy/world refinement or as internal predictive feature refinement.
- Exact released-code behavior.

### Why no paper/mode split

The paper's planning path is the scoped terminal artifact. Motion prediction and occupancy are supporting branches in that path, not separate terminal modes on the available evidence.

---

## Card DD-VIS — DriveDreamer controllable future-video path

### Deployment route

An initial image and structured road scene, optional text, and supplied driving actions are used to recursively predict future traffic structure, which conditions a diffusion generator that emits future driving video.

### Ordered learning route

A structured single-frame image generator is trained first, then extended to multi-frame video; a second stage trains action-conditioned future structural prediction together with future video and action prediction.

### Object/evidence table

| object | semantic role | lifecycle | evidence |
|---|---|---|---|
| initial image and road structure | current scene input | deployed | PAPER FACT |
| action-conditioned structural future sequence | predicted future scene condition | deployed in generation mode | PAPER FACT |
| diffusion video generator and internal denoising representations | future-world generation process | deployed in generation mode | PAPER FACT |
| future driving video | terminal generated world output | deployed | PAPER FACT |
| external/supplied action stream | control supplied to the generator | deployed input | PAPER FACT |

### Candidate/resolver status

No terminal action commitment or common selection stage is described for this mode. The action is supplied as control; the output is future video.

### Key UNKNOWNs

- Whether downstream planning consumes any internal generation state in an official implementation.
- Exact controller relationship and control-cycle use.
- Exact code version and parameter retention boundary.

### Why this is a separate mode

The terminal product is future video rather than an ego action trajectory. Combining it with the action-generation path would erase a change in output semantics and deployment role.

---

## Card DD-ACT — DriveDreamer future-action path

### Deployment route

An initial image/road structure and past actions feed recurrent future structural prediction and the world-model video stack; pooled world-model features and action history are decoded into a future action trajectory, while future video is generated in the same second-stage model.

### Ordered learning route

Structured image and video generation training is followed by action-conditioned future structural prediction and joint future-video/future-action prediction; the paper reports open-loop action trajectory evaluation.

### Object/evidence table

| object | semantic role | lifecycle | evidence |
|---|---|---|---|
| initial image and road structure | current scene input | deployed | PAPER FACT |
| recurrent predicted structural sequence | action-conditioned future scene evolution | deployed in the described predictive path | PAPER FACT |
| multi-scale world-model features | intermediate future-world information supplied to the action decoder | deployed in the described path | PAPER FACT |
| action decoder | future action trajectory formation | deployed/evaluated | PAPER FACT |
| future video decoder | jointly trained world-output branch; exact inference fate for action-only use unresolved | deployed in full model; action-only fate UNKNOWN | PAPER FACT / UNKNOWN |

### Candidate/resolver status

The paper reports direct future-action generation and does not describe a common resolver over multiple action candidates. The trajectory time points are generated action outputs; the visual branch provides world-model computation rather than a candidate-specific consequence bank.

### Key UNKNOWNs

- Whether the action and visual outputs are one semantically joint emission or a world-conditioned action head.
- Whether the full video decoder remains active when only action prediction is evaluated.
- Closed-loop control-cycle behavior and exact gradient/retention boundaries.

### Why this is a separate mode

The terminal output changes from a generated world video to a future driving-action trajectory, and the planning interpretation of the shared model therefore changes.

---

## Card DRV-PLAN — DrivoR planning path

### Deployment route

Camera observations, ego status, and a driving command are compressed into scene tokens; a trajectory decoder emits multiple ego trajectory proposals, a separate scoring decoder evaluates each proposal with decomposed driving-quality outputs, and a weighted maximum selects the committed trajectory.

### Ordered learning route

A pretrained visual backbone is adapted with camera-aware registers; trajectory proposals are trained with winner-takes-all regression; the scoring branch is trained against oracle sub-scores; the shared perception encoder receives both losses, while scorer gradients are blocked from the trajectory decoder.

### Object/evidence table

| object | semantic role | lifecycle | evidence |
|---|---|---|---|
| camera-aware register scene tokens | compact perceptual representation | deployed | PAPER FACT |
| multiple decoded ego trajectories | identity-preserving action proposals | deployed | PAPER FACT |
| separate scoring decoder | common proposal evaluator | deployed | PAPER FACT |
| safety/comfort/progress and related sub-scores | decomposed driving-quality criterion | deployed | PAPER FACT |
| oracle scorer and human reference trajectory | training supervision | training only | PAPER FACT |
| weighted maximum-score choice | final commitment | deployed | PAPER FACT |

### Candidate/resolver status

Candidate identity is explicit from proposal generation through common scoring. The score determines the selected final trajectory. There is no separately predicted future scene or consequence state in the paper's planning path.

### Key UNKNOWNs

- Any undocumented project-page post-processing.
- Exact code commit and reproducibility boundary.
- Whether the scorer's oracle construction has additional runtime inputs not described in the paper.

### Why no paper/mode split

The paper presents one planning artifact; behavior-conditioned score weights alter the resolver preference but not the terminal topology.



