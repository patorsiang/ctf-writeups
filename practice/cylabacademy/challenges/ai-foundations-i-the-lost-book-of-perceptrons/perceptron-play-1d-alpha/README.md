# Perceptron Play 1D Alpha

## Metadata

- Platform: CyLab Academy
- Learning Path: AI Foundations I - The Lost Book of Perceptrons
- Category: AI / Networking
- Difficulty: Beginner
- Status: Solved
- Started: 2026-09-20
- Completed: 2026-09-20
- Files: `solve.py`, `test_solve.py`
- Skills Learned: Controlled parameter trials, threshold placement, perceptron bias

## Problem Summary

The challenge provides an interactive one-dimensional perceptron playground:

```sh
nc aureolin-pixie.cylabacademy.net 64300
```

The goal is to choose a weight `w` and bias `b` that classify every labeled
point correctly. The service uses this rule:

```text
activation = w*x + b

activation >= 0 -> class 1
activation < 0  -> class 0
```

The labeled points are:

```text
Class 0: -4, -2, 0
Class 1:  2,  3, 4
```

## First Observation

The starting parameters are `w = 1` and `b = 0`. They classify every point
correctly except `x = 0`:

```text
x = 0
activation = 1*0 + 0 = 0
```

An activation of exactly zero belongs to class `1` because the rule uses
`>= 0`. The target label at `x = 0` is class `0`, so the activation must be
moved below zero.

## Controlled Trial Process

This challenge does not provide source code or local files to search with
`grep`. The useful method is to change one parameter, inspect the table, and
keep the change only when it improves the classifications.

The first attempted command was:

```text
SET 1 b
```

The service rejected it because `b` was a placeholder, while `SET` requires
two numeric values.

The next trial used a positive bias:

```text
SET 1 2
```

This made the result worse. At `x = 0`:

```text
activation = 1*0 + 2 = 2
```

The activation became more positive, so `x = 0` remained in class `1`.
`x = -2` also moved to activation zero and became incorrectly classified as
class `1`.

The useful direction was therefore to decrease the bias:

```text
SET 1 -1
```

## Why `w = 1, b = -1` Works

With these parameters, the formula becomes:

```text
activation = x - 1
```

The nearest points on opposite sides are `0` and `2`:

```text
x = 0:  0 - 1 = -1 -> class 0
x = 2:  2 - 1 =  1 -> class 1
```

The decision boundary is where the activation equals zero:

```text
x - 1 = 0
x = 1
```

This places the boundary between the final class `0` point and the first
class `1` point:

```text
-4  -2   0   |   2   3   4
  class 0    |    class 1
```

All six calculations confirm the result:

| `x` | Target | Activation `x - 1` | Prediction |
| ---: | ---: | ---: | ---: |
| -4 | 0 | -5 | 0 |
| -2 | 0 | -3 | 0 |
| 0 | 0 | -1 | 0 |
| 2 | 1 | 1 | 1 |
| 3 | 1 | 2 | 1 |
| 4 | 1 | 3 | 1 |

## Other Valid Bias Values

Keeping `w = 1`, the two closest points give the required conditions:

```text
x = 0 must be class 0: 0 + b < 0  -> b < 0
x = 2 must be class 1: 2 + b >= 0 -> b >= -2
```

Therefore, any bias in this range works:

```text
-2 <= b < 0
```

`b = -1` is a convenient choice in the middle. It is not the only solution.

## Manual Solution

Connect to the service and submit:

```text
SET 1 -1
CHECK
```

The server verifies every point and returns the flag.

## Helper Script

Run the automated helper from this challenge directory:

```sh
python3 solve.py
```

Run its protocol test with:

```sh
python3 -m unittest test_solve.py
```

## Flag

```text
academy{0n3_d_thr35h0ld_4d654a9a}
```

## Lessons Learned

- Use the table to find the misclassified point before changing parameters.
- Change one parameter at a time so the effect is easy to observe.
- A positive bias moves activations upward; a negative bias moves them
  downward.
- The decision boundary for a one-dimensional perceptron is a threshold on a
  number line.
- An activation of zero is class `1` in this challenge because the comparison
  is `>= 0`.
- A valid classifier can have several different weight and bias pairs.
