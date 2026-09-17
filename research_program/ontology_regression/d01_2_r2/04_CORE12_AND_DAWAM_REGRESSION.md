# D01.2-R2 Core-12, Canonical-21, and DA-WAM Regression

## 1. Acceptance counters

```text
23-artifact legal projections          PASS
A16/A17 separation                    PASS
A13/A17 direct joint emission         PASS
A19 D3/RR                              PASS
canonical 21 artifacts                PASS
core-12 human map                     PASS
DA-WAM                                PASS
SeerDrive paper/code                  PASS
Drive-JEPA PF/PB                      PASS
Discrete-WAM policy/world/joint       PASS
```

## 2. Canonical 21-artifact regression

The amendment does not change any of these headline routes. The table records the final expected projection and the regression result.

| Canonical artifact/mode | Final human route | Regression |
|---|---|---|
| LAW-PF | `R0+W0+E0 ⊕ LA` | KEEP |
| LAW-PB | `R0+W0+E0 ⊕ LA` | KEEP |
| EPO-PLAN | `R0+W0+E0 ⊕ LS` | KEEP |
| EPO-SELF | `RG{self}+W4+E0` | KEEP |
| EPO-CTRL | `RG{external}+W4+E0` | KEEP |
| DLAW-PAPER | `R0+W2+E0 ⊕ LG` | KEEP |
| DLAW-CODE | `R0+W2+E0 ⊕ LG` | KEEP |
| W4D-PLAN | `RB+W3+EW` | KEEP |
| WD-PLAN | `RB+W3+EV ⊕ LP->joint(LT,LC)` | KEEP |
| WOTE-PLAN | `RB+W4+(EF+ED)` | KEEP |
| SEER-PAPER | `RR+W3+E?` | KEEP; resolver UNKNOWN remains visible |
| SEER-CODE | `RB+W3+(EF+ED)` | KEEP |
| DJEPA-PF | `R0+W0+E0 ⊕ LP` | KEEP |
| DJEPA-PB1 | `RB+W0+EV ⊕ LP->LC` | KEEP |
| DJEPA-PB2 | `RB+W0+weighted(EV,ED) ⊕ LP->LC` | KEEP |
| METIS-PLAN | `R0+W0+E0 ⊕ LA` | KEEP |
| DFD-PLAN | `RB+W0+(EW+EF+EY) ⊕ LC` | KEEP |
| DWAM-POLICY | `RH+W0+E0 ⊕ LQ->LR` | KEEP |
| DWAM-WORLD | `RG{external}+W4+E0 ⊕ LQ` | KEEP |
| DWAM-JOINT | `RJ+W5+E0 ⊕ LQ` | KEEP |
| GW-PLAN | `RU+W1+E? ⊕ LS->LN` | KEEP; final commitment UNKNOWN remains visible |

No canonical-21 row receives a new R/W/E code or a changed headline.

## 3. Core-12 human map

| Core paper | Final route | R2 result |
|---|---|---|
| LAW | `R0+W0+E0` with LA | KEEP |
| Epona | planning `R0+W0+E0`; rollout `RG+W4+E0` | KEEP |
| DriveLaW | `R0+W2+E0` | KEEP |
| World4Drive | `RB+W3+EW` | KEEP |
| WorldDrive | `RB+W3+EV` | KEEP |
| WoTE | `RB+W4+(EF+ED)` | KEEP |
| SeerDrive | paper `RR+W3+E?`; code `RB+W3+(EF+ED)` | KEEP |
| Drive-JEPA | PF `R0+W0+E0`; PB `RB+W0+EV/ED` | KEEP |
| Metis | `R0+W0+E0` with LA | KEEP |
| DynFlowDrive | `RB+W0+(EW+EF+EY)` | KEEP |
| Discrete-WAM | policy RH; world RG; joint RJ+W5 | KEEP |
| GraphWorld | `RU+W1+E?` | KEEP |

The amendment only makes a non-core composition legal: `RB+W5` for A16. It does not alter the core-12 map.

## 4. DA-WAM regression

DA-WAM is A14 in the 23-artifact ledger. Its final projection remains:

```text
C2@R{direct}; X3; D2; PB; V=VD->VU; T=(A,A,A,U)
L=LP->joint(LA,LN,LC)
```

Human route:

```text
RB + W3 + (ED->EV) ⊕ LP->joint(LA,LN,LC)
```

It is not C5, does not use X4, and does not inherit W5. The A16 amendment therefore creates no DA-WAM collision.

## 5. Required mode-specific checks

### A16/A17

```text
A16 = RB+W5+EV
A17 = RJ+W5+E0
```

The former has candidate identity and a common resolver; the latter directly emits one joint sample. PASS.

### A13/A17

Both remain direct joint emission with C5, X4, D4, and RJ+W5. Their ordered L programs differ (`LP->LQ` versus `LC->LR`), so the learning distinction is preserved. PASS.

### A19

`C2@R{direct}; X2; D3; P=∅; V=N/A; T=(P,P,A,U)` maps to `RR+W3+E0`. Endpoint feedback is preserved; no physical-horizon clock leaks into Th. PASS.

### SeerDrive paper/code

The paper remains `RR+W3+E?`; released code remains `RB+W3+(EF+ED)`. The amendment does not collapse the version split. PASS.

### Drive-JEPA PF/PB

PF remains `R0+W0+E0`; PB remains `RB+W0+EV/ED`. Candidate scoring without an online world carrier is not reclassified as W3/W4. PASS.

### Discrete-WAM

Policy, world, and joint modes remain `RH`, `RG`, and `RJ+W5`. The new RB+W5 rule does not convert direct joint emission into candidate resolution. PASS.

## Regression verdict

```text
core-12 headline changes = 0
DA-WAM route changes = 0
canonical-21 route changes = 0
paper/code or mode collapses = 0
```
