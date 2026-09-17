# D02-W1E Full-Text Collision and Constraint Audit

## Collision groups

| Layer | Group | Judgment | Reason |
|---|---|---|---|
| Human runtime `R-W-E` | P0010 `RB-W0-EV`; no identical W1E peer | no collision | TOAD's learned holistic scorer is distinct from Hydra's decomposed teacher-derived metrics. |
| Human runtime `R-W-E` | P0034/P0038 `RG-W4-E0` | `EXPECTED_FUNCTIONAL_EQUIVALENCE` at coarse boundary layer | Both terminate in controlled future/world generation without a final policy resolver; simulator construction, action source, and world substrate remain audit attributes. |
| Human runtime `R-W-E` | P0004/P0058 both use future information but differ `RB-W4-ED` versus `R0-W4-E0` | `BACKEND_SEPARATED` | BeTop has an explicit ego candidate resolver; VAD has direct ego planning with predicted non-ego motion as a carrier. |
| Normative runtime `C-X-D-P-V-T` | P0010/P0021 both `W0 + PB` | `BACKEND_SEPARATED` | `VU` versus `(VM+VD)` is a mechanism-level resolver difference even though both have no online world carrier. |
| Normative runtime `C-X-D-P-V-T` | P0034/P0038 both generation terminals | `BACKEND_SEPARATED` | HUGSIM is a dynamic simulator with external planner control; Vista is an autoregressive video world model with supplied action conditioning and uncertainty reward. |
| Full mechanism | P0034/P0038 coarse route group | `L_SEPARATED` | Scene reconstruction/simulator actor generation differs from predictive/video pretraining plus action-control adaptation. |

No false collision is established after preserving `E`, control modifiers, and ordered learning provenance.

## Structural pressure from BeTop

The current compression rule says that `W3/W4 + RB` normally requires candidate-preserving `X3` in the backend. BeTop is a real boundary case:

```text
ego candidate bank + common resolver: YES
future-horizon prediction used in scoring: YES
future prediction separately regenerated for every ego candidate: not shown
shared marginal future prediction used in candidate cost: YES
```

The defensible paper-first projection is therefore:

```text
P = PB
W = W4
V = ED
D = shared future carrier -> candidate scoring/resolver -> A*
X = candidate-indexed control on W4: not evidenced
```

This is not a reason to add a new code. It is a pressure test for whether the current type constraint conflates:

```text
candidate-conditioned future consequence
```

with:

```text
shared future forecast used as a criterion while candidates are resolved
```

The rerun therefore records `HOLD-STRUCTURAL-PRESSURE` for this narrow constraint question. No normative file is changed automatically.
