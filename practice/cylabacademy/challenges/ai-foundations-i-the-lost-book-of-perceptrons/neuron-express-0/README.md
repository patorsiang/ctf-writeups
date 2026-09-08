# Neuron Express 0

## Metadata

- Platform: CyLab Academy
- Learning Path: AI Foundations I - The Lost Book of Perceptrons
- Category: AI / Networking
- Difficulty: Beginner
- Status: Solved
- Started: 2026-09-08
- Completed: 2026-09-08
- Files: `solve.py`
- Skills Learned: Netcat-style TCP probing, decision-boundary discovery, perceptron inequalities

## Problem Summary

The challenge provides a raw TCP service:

```sh
nc aureolin-pixie.cylabacademy.net 51643
```

The service is a one-dimensional perceptron. We send an integer `x` and observe
whether the neuron fires (`1`) or stays quiet (`0`). The goal is to infer a
weight `w` and bias `b`, then submit them with the `TEST w b` command.

The service accepts a guess only if it produces the same output for every
integer in the range `[-10, 10]`.

## First Observations

The connection banner gives the decision rule:

```text
Bounds: [-10, 10]
Output rule: w*x + b >= 0 -> 1, else 0.
Command: TEST w b to submit a weight and bias guess.
```

This is a threshold function. In one dimension, the perceptron has one
decision boundary on the number line.

## Probing the Boundary

Start with the extremes to confirm which side produces each output:

```text
x = 10  -> 1
x = -10 -> 0
```

Then narrow the transition with midpoint-style probes:

```text
x = 0 -> 0
x = 4 -> 1
x = 2 -> 1
x = 1 -> 0
```

The exact integer behavior is therefore:

```text
x <= 1 -> 0
x >= 2 -> 1
```

The boundary is between `1` and `2`.

## Deriving the Weight and Bias

We need a formula that is negative at `x = 1` and non-negative at `x = 2`:

```text
w*1 + b < 0
w*2 + b >= 0
```

Choose the simplest positive integer weight, `w = 1`:

```text
1 + b < 0  -> b < -1
2 + b >= 0 -> b >= -2
```

The integer bias satisfying both inequalities is `b = -2`. The resulting
formula is:

```text
x - 2
```

It produces `0` for every integer `x <= 1` and `1` for every integer `x >= 2`,
which matches the observed behavior across the complete range. The solution is
not necessarily unique; any `w` and `b` pair that gives the same outputs over
`[-10, 10]` should be accepted. `w = 1`, `b = -2` is the simplest choice.

## Solution Walkthrough

1. Connect to the service.
2. Probe `10` and `-10` to find opposite output sides.
3. Probe `0`, `4`, `2`, and `1` to locate the integer transition.
4. Translate the transition into inequalities for `w` and `b`.
5. Submit:

```text
TEST 1 -2
```

The service accepted the formula and returned:

```text
academy{n3ur0n_expr_f075f57b}
```

## Commands Or Script

Manual connection:

```sh
nc aureolin-pixie.cylabacademy.net 51643
```

Then send the probes and final command:

```text
10
-10
0
4
2
1
TEST 1 -2
```

Or run the helper script from this challenge directory:

```sh
python3 solve.py
```

## Flag

```text
academy{n3ur0n_expr_f075f57b}
```

## Lessons Learned

- A one-dimensional perceptron is a threshold classifier on a number line.
- Extreme probes quickly identify opposite sides of the decision boundary.
- Binary-search-style probing is more efficient than random guessing.
- The observed transition can be translated directly into inequalities for the
  weight and bias.
- The simplest matching formula is often enough; recovering the hidden model's
  original parameters is not required when the validator checks behavior.

## Follow-Up

- Practice finding thresholds with fewer probes.
- Compare this one-dimensional formula with the straight-line boundary from
  `neuron-meet-2d-0`.
- For future black-box models, separate behavioral equivalence from recovering
  the exact internal parameters.
