# Planning-centric WAM Taxonomy

## Dimension 1: Role of World Model

| Role | Representative | Core idea |
|---|---|---|
| Teacher | LAW | Future latent prediction supervises planner learning |
| Simulator / Evaluator | WoTE | Predict future outcomes under candidate actions |
| Generator | Epona | Generate future trajectory and visual world |
| Representation Learner | WorldDrive | Learn future-aware representations for planning |

## Dimension 2: Future Representation

World models may predict:

- RGB/video future
- latent future state
- object/agent future
- trajectory future
- uncertainty/risk future

## Dimension 3: Planning Interface

Unified view:

```
Observation
    ↓
World Model
    ↓
Future Representation
    ↓
Planner
    ↓
Action
```

For each method analyze:

- What is observed?
- What future is predicted?
- What supervision is used?
- How does planning consume future information?
- What limitation remains?
