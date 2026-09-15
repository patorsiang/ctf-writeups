# Neuron Express 2D-0

## Metadata

- Platform: CyLab Academy
- Learning Path: AI Foundations I - The Lost Book of Perceptrons
- Category: AI / Networking
- Difficulty: Easy
- Status: Solved
- Started: 2026-09-15
- Completed: 2026-09-15
- Files: `solve.py`, `test_solve.py`
- Skills Learned: Query-budgeted oracle probing, version-space narrowing, active learning, closed-form bias windows, model extraction

## Problem Summary

The challenge provides a raw TCP service:

```sh
nc aureolin-pixie.cylabacademy.net 49526
```

The service is a two-dimensional perceptron. We send an integer pair `(x, y)`
and observe whether the neuron fires (`1`) or stays quiet (`0`). The goal is to
recover integer weights `w1`, `w2` and bias `b`, then submit them with
`TEST w1 w2 b`.

This is `neuron-express-0` lifted into the plane: same "express the behaviour
as an equation" idea, one more weight, and one new constraint that changes
everything.

## First Observations

The banner states the rule and, critically, the probe counter:

```text
- Bounds: [-10, 10] for both x and y
- Output rule: w1*x + w2*y + b >= 0 -> 1, else 0.
- Weights and bias are integers.
- Command: TEST w1 w2 b to submit integer weights and bias.
- The guess must match outputs for every integer (x, y) in range.

[1/128] (x,y)>
```

Two numbers matter and they are in tension:

- the guess is validated against **441** points (`21 x 21`)
- we are allowed **128** probes

## What I Tried First (And Why It Failed)

The obvious extension of the 1D solve is to probe every point and fit. In 1D
that works: 21 points, no budget mentioned. Here it cannot, and I burned two
instances finding out. The script marched to probe 128, the server closed the
connection, and the next read came back empty.

The lesson is not "probe less". It is that **verification by exhaustion is
unavailable**, so verification has to come from reasoning instead.

## Key Idea

Treat each probe as an inequality, not a data point:

```text
(x, y) -> 1   means   w1*x + w2*y + b >= 0
(x, y) -> 0   means   w1*x + w2*y + b <  0
```

Keep the set of all perceptrons still consistent with every answer so far (the
version space), and stop probing the moment **every survivor agrees on all 441
grid points**. At that instant the answer is provably the one the server will
accept, without ever having probed 441 points.

The stopping rule is sound because a genuine perceptron is always consistent
with the answers it gave, so the hidden model is always among the survivors.
If the survivors are unanimous, the hidden model is part of that unanimity.
This is conditional on the oracle really being a perceptron - against a
non-separable oracle the same rule would settle on something unverifiable.

Two observations make this cheap enough for pure Python:

**1. Never search the bias.** Fix a direction `(w1, w2)` and the constraints
collapse to a closed-form window:

```text
b >= max over firing points of -(w1*x + w2*y)          = b_lo
b <= min over quiet  points of -(w1*x + w2*y) - 1      = b_hi
```

A direction survives iff `b_lo <= b_hi`. That is ~1000 coprime directions to
consider instead of ~800k `(w1, w2, b)` triples. Directions with `gcd > 1` are
scaled copies of one already in the list and describe the same line.

**2. Only the window endpoints matter.** Labels are monotone in `b` - raising
`b` only ever turns a `0` into a `1` - so if `b_lo` and `b_hi` agree at a
point, every bias between them agrees too. Two label vectors per direction,
not thousands.

Probe selection is then greedy: ask the point that splits the surviving
hypotheses closest to 50/50. Each probe buys roughly one bit, so ~2^20
distinct behaviours fall out in ~20 questions.

## Solution Walkthrough

1. Probe the four corners and the origin to cut the space cheaply.
2. Loop: compute surviving directions and their bias windows, pick the
   unprobed point that most evenly splits them, probe it.
3. Stop when all survivors predict identically across the whole grid.
4. Fit the simplest `(w1, w2, b)` and submit.

The live run settled in 19 probes:

```text
probe   6: (3, -8)   -> 1   (510 hypotheses left)
probe   7: (-1, -10) -> 0   (347 hypotheses left)
probe   8: (2, 0)    -> 0   (230 hypotheses left)
probe   9: (2, -8)   -> 0   (164 hypotheses left)
probe  10: (5, 6)    -> 1   (139 hypotheses left)
probe  11: (3, 1)    -> 1   (77 hypotheses left)
probe  12: (2, 10)   -> 0   (49 hypotheses left)
probe  13: (2, -10)  -> 0   (26 hypotheses left)
probe  14: (3, 3)    -> 1   (21 hypotheses left)
probe  15: (3, 5)    -> 1   (17 hypotheses left)
probe  16: (3, 7)    -> 1   (13 hypotheses left)
probe  17: (3, 9)    -> 1   (9 hypotheses left)
probe  18: (3, -10)  -> 1   (5 hypotheses left)
probe  19: (3, 10)   -> 1   (2 hypotheses left)

settled after 19 probes (server allows 128)
boundary: 1*x1 + 0*x2 + -3 >= 0
Perfect match! Here is your flag:
```

This instance was degenerate: `w2 = 0`, so the boundary is vertical at `x >= 3`
and `y` is ignored completely. A "2D" perceptron that is secretly 1D.

That degeneracy explains probes 14-19, which all walk up the column `x = 3`.
Once the direction was nearly pinned, the only surviving hypotheses disagreed
about whether `w2` was exactly zero or merely small. The only way to separate
them is to check that the verdict at `x = 3` holds at both extremes of `y`.
Six probes spent proving a negative - and worth it, since a wrong `w2` would
fail the server's 441-point check on a single far corner.

## Commands Or Script

```sh
python3 solve.py --self-test        # offline proof against known perceptrons
python3 solve.py 49526 --no-test    # probe live, print the equation, do not submit
python3 solve.py 49526              # probe and submit
```

Tests (needs pytest):

```sh
uv run --with pytest python -m pytest -q test_solve.py
```

The port changes per instance. `--no-test` stops after printing the boundary
with ~100 probes of headroom, which is the safe way to check the protocol
parsing against a fresh instance without losing it.

## Flag

```text
academy{n3ur0n_expr_2d_a59ea424}
```

## Lessons Learned

- Read the banner before designing the strategy. `[1/128]` was printed on the
  first line and it invalidated the entire first approach.
- When the validation set is larger than the query budget, stop trying to
  verify by exhaustion and verify by argument instead.
- A probe is an inequality. Collecting constraints beats collecting samples.
- Fix the variables that have a closed-form answer and only search the rest;
  here that turned an 800k-candidate search into ~1000.
- Monotonicity is a pruning tool: if labels move one way as `b` grows, the two
  endpoints of a bias window summarise every bias inside it.
- Choose the probe that halves the hypothesis space. Blind sweeps waste the
  budget on questions whose answers were already implied.
- Solutions are not unique. Any positive scaling of `(w1, w2, b)` is the same
  line, and the server checks behaviour rather than parameters.
- Degenerate instances are normal. `w2 = 0` is a legal 2D perceptron and the
  solver has to handle "always fires" and "never fires" too.
- Keeping the oracle behind a callable made the whole strategy testable offline
  in under a second, which is why the redesign cost zero extra instances.

## Follow-Up

- Compare probe counts: 1D needed 6 probes, 2D needed 19. Sketch how this
  scales to `n` dimensions and why grid probing dies at `21^n`.
- Read up on model extraction attacks against ML APIs - this challenge is a
  tiny, exact version of the same query-budget-versus-fidelity trade-off.
- Try lowering `MAX_PROBES` to find the real worst case across many instances.
