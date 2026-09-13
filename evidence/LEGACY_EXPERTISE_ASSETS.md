# LEGACY_EXPERTISE_ASSETS

Purpose: preserve what the owner's prior risk-field work can contribute **if and only if** a validated planning-centric WAM problem needs it.

This file is deliberately not a hypothesis or method proposal.

## Non-negotiable rule

```text
Prior expertise is an optional asset, not a destination.
```

Do not force any of the items below into a future method merely because they are familiar.

## Transferable capabilities from prior work

The prior MR-CTDRF / predictive-risk-field line developed useful capabilities at a higher level than any specific formula:

1. **Future interaction → safety/value semantics**
   - Turn predicted future motion into interpretable decision-relevant safety structure rather than treating prediction as an end in itself.

2. **Relative interaction reasoning**
   - Represent risk in ego-relative / interaction-relative coordinates, emphasizing relation rather than isolated actor state.

3. **Spatial queryability**
   - Make future safety information queryable by candidate ego occupancy/trajectory instead of only producing a global scene score.

4. **Risk-source and future-time attribution**
   - Preserve which actor / future time contributes to a safety concern rather than collapsing everything immediately into one scalar.

5. **Future-information compression with planning structure preserved**
   - Compress multi-agent, multi-time future information while trying to retain the distinctions a planner needs.

6. **Candidate-query perspective**
   - Evaluate a proposed ego motion against a future safety representation rather than only predicting the expert trajectory.

7. **Calibration / physical-semantics sensitivity**
   - Awareness that risk outputs need meaningful scaling/interpretation if they are to affect decisions safely.

## What should NOT be transferred by default

Do not assume any of the following belongs in a WAM solution:

```text
hand-designed risk potential
specific risk-field equations
hard max over agents/times
fixed deterministic horizon
single-mode future prediction
2D field representation
legacy warning threshold design
```

These are implementation choices from an older problem setting, not research assets in themselves.

## When this expertise becomes relevant

Only after a planning failure survives falsification and can be expressed as a missing capability such as:

- planner needs an interpretable decomposition of future consequences;
- candidate choices differ mainly through relative interaction structure;
- a world representation loses actor/time attribution needed for planning;
- future rollout is too large and needs decision-preserving compression;
- a planner needs calibrated safety/value semantics rather than an opaque latent score.

Even then, compare against simpler alternatives first.

## Strong counterexamples already known

- **DriveLaW:** strong planning without an explicit risk/value interface → explicit risk cannot be assumed necessary.
- **DA-WAM:** candidate-specific future latent + scorer → candidate-conditioned future-to-value coupling already exists without a classical risk field.
- **SafeDrive:** explicit safety decomposition is already a strong near-neighbor → any new safety/risk interface must solve a distinct observed failure rather than repackage PwNC/TwDAC-style reasoning.
- **NPPC:** learned continuous planning cost is a strong value-interface alternative → hand-designed physical risk semantics must earn its complexity.

## Method-design test if risk knowledge is later proposed

Any future proposal using risk expertise must answer:

```text
1. What observed planning failure is being fixed?
2. Why does the failure require this information rather than a stronger generic latent/scorer?
3. What exact information from the risk representation changes action selection?
4. What simpler baseline could provide the same information?
5. Is the gain still present under reactive / closed-loop evaluation?
6. Does the representation improve decision ordering, not just interpretability?
```

If these cannot be answered, do not use the risk-field asset.
