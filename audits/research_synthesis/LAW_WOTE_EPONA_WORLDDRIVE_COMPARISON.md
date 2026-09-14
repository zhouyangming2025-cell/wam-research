# LAW / WoTE / Epona / WorldDrive Unified Comparison

## Core Question

These papers should not be compared by architecture names alone. The key question is how future information is used for planning.

## High-level positioning

| Paper | Future role | Planning relation |
|---|---|---|
| LAW | Future-aware representation learning | Future mainly improves training |
| WoTE | Future evaluation | Future judges candidate actions |
| Epona | Future world generation | Future visual and motion generation |
| WorldDrive | Future-aware planning representation | Future latent supports decision making |

## Evolution View

```
Future as learning signal
        |
        v
Future as decision evaluator
        |
        v
Future as generated world
        |
        v
Future as planning state
```

## Fundamental Research Question

A complete world model for driving should not only answer:

`What will happen?`

but:

`What will happen if I take this action?`

Therefore the key interface is:

`History + Candidate Action -> Future World Representation -> Planning`

## Audit Focus

For every future WAM paper, evaluate:

1. Does the world model participate during inference?
2. Is action a true causal condition?
3. Are alternative futures supervised?
4. Does future representation improve decision quality?
