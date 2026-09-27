# Perceptron Play 2D Alpha

## Metadata

- Platform: CyLab Academy
- Learning Path: AI Foundations I - The Lost Book of Perceptrons
- Category: AI / Networking
- Difficulty: Beginner
- Status: Solved
- Started: 2026-09-27
- Completed: 2026-09-27
- Files: `solve.py`, `test_solve.py`
- Skills Learned: 2D decision boundaries, controlled parameter trials, perceptron weights and bias

## Problem Summary

The challenge provides an interactive two-dimensional perceptron playground:

```sh
nc xebec.cylabacademy.net 38408
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

The starting parameters are `w1 = 1`, `w2 = -1`, and `b = 0`. The service
shows two misclassified points:

| Point | Target | Activation `x - y` | Prediction |
| --- | ---: | ---: | ---: |
| `(-3,-2)` | 0 | -1 | 0 |
| `(-1,-1)` | 0 | 0 | 1 |
| `(-4,-2)` | 0 | -2 | 0 |
| `(+3,+1)` | 1 | 2 | 1 |
| `(+2,+2)` | 1 | 0 | 1 |
| `(+1,+3)` | 1 | -2 | 0 |

The exact-zero rule matters: activation `0` predicts class `1`. The class 0
point `(-1,-1)` is therefore wrong, while `(+2,+2)` is correct.

## Controlled Trial Method

A trial means making one meaningful hypothesis, running `CHECK`, and reading
the new table. It does not mean guessing many random weight combinations.

For this dataset:

1. The starting table shows which points need a different boundary.
2. Compare simple coordinate combinations. The class 0 points have negative
   `x + y` values, while every class 1 point has `x + y = 4`.
3. Translate that hypothesis into weights: `w1 = 1`, `w2 = 1`, `b = 0`.
4. Run `SET 1 1 0`, then `CHECK` to test every point.

The single trial changes the boundary from `x - y = 0` to `x + y = 0`.

## Finding the Boundary

The points suggest that the two classes are separated by the sum `x + y`:

- Class 0 points have negative sums: `-5`, `-2`, and `-6`.
- Class 1 points all have sum `4`.

Set both weights to `1` and keep the bias at `0`:

```text
SET 1 1 0
CHECK
```

The activation becomes:

```text
activation = x + y
```

The decision boundary is the line `x + y = 0`, or `y = -x`. Every class 0
point lies below the class 1 side of this line, and every class 1 point lies
above it.

## Verification

| Point | Target | Activation `x + y` | Prediction |
| --- | ---: | ---: | ---: |
| `(-3,-2)` | 0 | -5 | 0 |
| `(-1,-1)` | 0 | -2 | 0 |
| `(-4,-2)` | 0 | -6 | 0 |
| `(+3,+1)` | 1 | 4 | 1 |
| `(+2,+2)` | 1 | 4 | 1 |
| `(+1,+3)` | 1 | 4 | 1 |

The service confirms:

```text
Perfect! All points are classified correctly.
academy{11n34r1y_53p4r4813_a4f2a27b}
```

## Manual Solution

Connect to the supplied instance:

```sh
nc xebec.cylabacademy.net 38408
```

Enter:

```text
SET 1 1 0
CHECK
```

## Helper Script

Run the helper with the supplied port:

```sh
python3 solve.py 38408
```

Run its protocol test with:

```sh
python3 -m unittest test_solve.py
```

## Flag

```text
academy{11n34r1y_53p4r4813_a4f2a27b}
```

## Lessons Learned

- In 2D, the perceptron boundary is a line: `w1*x + w2*y + b = 0`.
- Change one parameter or one pair of parameters, then inspect every point.
- The sign of the activation determines the class, with zero included in class 1.
- A valid solution only needs to separate the known points; it does not need to recover hidden training code.
