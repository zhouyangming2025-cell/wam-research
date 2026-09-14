# WAM Paper Position Matrix

Purpose: compare representative methods by scientific position, not by publication order.

| Paper | World Model Role | Future Object | Planning Interface | Main Contribution | Main Limitation |
|---|---|---|---|---|---|
| LAW | Teacher | Future latent representation | Training-time representation shaping | Future latent prediction improves planner learning | Not an online future evaluator |
| WoTE | Evaluator | Action-conditioned future state | Candidate trajectory evaluation | Uses predicted futures for planning selection | Counterfactual supervision boundary requires care |
| Epona | Generator | Visual future + trajectory | Joint world generation | Unified generative world representation | Planning validation remains challenging |
| WorldDrive | Representation Learner | Future-aware representation | Planning-oriented features | Future prediction improves representation | Interface between representation and planning remains key |

## Analysis Rule

The important scientific variable is not whether a method is called a world model, but:

```
Where does future information enter decision making?
```
