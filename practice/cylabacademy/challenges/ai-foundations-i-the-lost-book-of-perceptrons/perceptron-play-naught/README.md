# Perceptron Play Naught

## Metadata

- Platform: CyLab Academy
- Learning Path: AI Foundations I - The Lost Book of Perceptrons
- Category: AI / Networking
- Difficulty: Beginner
- Status: Solved
- Started: 2026-09-27
- Completed: 2026-09-27
- Files: `solve.py`, `test_solve.py`
- Skills Learned: 2D decision boundaries, ignoring an irrelevant feature, perceptron weights and bias

## Problem Summary

The challenge provides an interactive two-dimensional perceptron playground:

```sh
nc xebec.cylabacademy.net 18281
```

The goal is to choose `w1`, `w2`, and `b` so the perceptron classifies every
labeled point correctly.

The service uses this rule:

```text
activation = w1*x + w2*y + b

activation >= 0 -> class 1
activation < 0  -> class 0
```

## First Observation

The starting parameters are `w1 = 1`, `w2 = -1`, and `b = 0`, so the initial
activation is `x - y`.

The service shows these points:

| Point | Target | Activation `x - y` | Prediction |
| --- | ---: | ---: | ---: |
| `(-4,-1)` | 0 | -3 | 0 |
| `(-1,+2)` | 1 | -3 | 0 |
| `(+0,-1)` | 0 | 1 | 1 |
| `(+0,+2)` | 1 | -2 | 0 |
| `(+2,-1)` | 0 | 3 | 1 |
| `(+3,+1)` | 1 | 2 | 1 |
| `(+4,+2)` | 1 | 2 | 1 |

The starting line misclassifies four points. A threshold on `x` alone cannot
work because `x = 0` appears in both classes.

## Controlled Trial Method

A trial means making one meaningful hypothesis, running `CHECK`, and reading
the new table. It does not mean guessing many random weight combinations.

For this dataset:

1. Read the starting table and note the misclassified points.
2. Test whether `x` can separate the labels. It cannot because `x = 0` has
   both a class 0 point and a class 1 point.
3. Test the other coordinate. Every class 0 point has `y = -1`, while every
   class 1 point has positive `y`.
4. Translate that hypothesis into weights: `w1 = 0`, `w2 = 1`, `b = 0`.
5. Run `SET 0 1 0`, then `CHECK` to test every point.

This is one controlled trial: disable irrelevant `x`, use `y`, and verify all
points.

## Finding the Boundary

Look at the `y` values instead:

- Every class 0 point has `y = -1`.
- Every class 1 point has `y = 1` or `y = 2`.

The `x` coordinate is not needed for this dataset. Ignore it by setting
`w1 = 0`, use `w2 = 1`, and keep `b = 0`:

```text
SET 0 1 0
CHECK
```

The activation becomes:

```text
activation = 0*x + 1*y + 0 = y
```

The decision boundary is the horizontal line `y = 0`. All class 0 points are
below it, and all class 1 points are above it.

## Verification

| Point | Target | Activation `y` | Prediction |
| --- | ---: | ---: | ---: |
| `(-4,-1)` | 0 | -1 | 0 |
| `(-1,+2)` | 1 | 2 | 1 |
| `(+0,-1)` | 0 | -1 | 0 |
| `(+0,+2)` | 1 | 2 | 1 |
| `(+2,-1)` | 0 | -1 | 0 |
| `(+3,+1)` | 1 | 1 | 1 |
| `(+4,+2)` | 1 | 2 | 1 |

The service confirms:

```text
Perfect! All points are classified correctly.
academy{n4ught_bu7_53p4r4b13_cf9e7c6f}
```

## Manual Solution

Connect to the supplied instance:

```sh
nc xebec.cylabacademy.net 18281
```

Enter:

```text
SET 0 1 0
CHECK
```

## Helper Script

Run the helper with the supplied port:

```sh
python3 solve.py 18281
```

Run its protocol test with:

```sh
python3 -m unittest test_solve.py
```

## Flag

```text
academy{n4ught_bu7_53p4r4b13_cf9e7c6f}
```

## Lessons Learned

- A 2D perceptron can ignore a feature by setting its weight to zero.
- Check whether one coordinate already separates the labels before combining both coordinates.
- The bias and weight signs define which side of the boundary maps to class 1.
- The exact-zero rule matters, so keep training points away from the boundary when possible.
