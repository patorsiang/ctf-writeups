# Perceptron Train 3-Bit Parity

## Metadata

- Platform: CyLab Academy
- Learning Path: AI Foundations I - The Lost Book of Perceptrons
- Challenge: [Perceptron Train 3-Bit Parity](https://learn.cylabacademy.org/learning-paths/20/225)
- Category: Artificial Intelligence
- Difficulty: Easy
- Status: Solved
- Started: 2026-10-21
- Completed: 2026-10-21
- Re-solve: due 2026-10-28
- Files: none (browser-only service)
- Skills Learned: parity, linear separability, learning-rate experiments
- CyLab submission: pending; the flag field was empty when checked

## Problem Summary

The service trains one perceptron on the eight vertices of a 3D cube. Each bit
is represented by `-2` or `2`; the label is `1` when the input has an odd
number of `1` bits, and `0` otherwise. The service allows up to 16 training
steps and accepts `75%` accuracy. One plane cannot separate every odd-parity
vertex from every even-parity vertex.

## Prediction

- Guess: not recorded before training
- Score: n/a

## First Observations

- The service starts with learning rate `0.02`.
- The target is `75%` accuracy.
- The model is a single perceptron, so its decision boundary is one plane.
- Each run has a 16-step training limit.

## Solve Log

I tried learning rates `0.02` and `0.20`. The `0.02` run reached `25%`
accuracy and did not reveal the flag. I did not record its final weights. The
`0.20` run reached the target and displayed the flag.

| Learning rate | Outcome | Final weights (`w1`, `w2`, `w3`, `b`) | Accuracy |
| ---: | --- | --- | ---: |
| `0.02` | No flag | Not recorded | `25%` |
| `0.20` | Flag revealed | `0.60`, `0.60`, `-0.20`, `0.20` | `75.0%` |

## Why 0.20 Worked

The final perceptron score was:

```text
0.60x1 + 0.60x2 - 0.20x3 + 0.20
```

It predicts class `1` for a positive score and class `0` for a negative score.
The service represents bit `0` as `-2` and bit `1` as `2`.

| Bits | Point | Expected | Score | Prediction |
| --- | --- | ---: | ---: | ---: |
| `000` | `(-2, -2, -2)` | 0 | -1.8 | 0 |
| `001` | `(-2, -2, 2)` | 1 | -2.6 | 0 |
| `010` | `(-2, 2, -2)` | 1 | 0.6 | 1 |
| `011` | `(-2, 2, 2)` | 0 | -0.2 | 0 |
| `100` | `(2, -2, -2)` | 1 | 0.6 | 1 |
| `101` | `(2, -2, 2)` | 0 | -0.2 | 0 |
| `110` | `(2, 2, -2)` | 0 | 3.0 | 1 |
| `111` | `(2, 2, 2)` | 1 | 2.2 | 1 |

The plane classifies six of the eight points correctly. It misses `001` and
`110`, giving `6 / 8 = 75%` accuracy.

## Why 100% Is Impossible

Parity labels alternate across the cube's vertices: changing any one bit
flips the label. A single plane divides 3D space into two half-spaces and
cannot separate all odd-parity vertices from all even-parity vertices. The
learning rate changes the updates and the final plane, but it does not give a
single perceptron a nonlinear boundary.

## Solution Walkthrough

1. Open the challenge and launch its instance.
2. Run training with the default rate, `0.02`; record its `25%` accuracy.
3. Set the learning rate to `0.20` and run training again.
4. Confirm the service reports `75.0%` accuracy and displays the flag.
5. Submit the flag on the CyLab learning-path page to record platform
   completion. That page still had an empty flag field when I checked it.

## Commands Or Script

None. The runs happened in the browser.

## Flag

```text
academy{3b1t_p4r1ty_unl34rn4bl3_l1n34rly_2a4a71a5}
```

## Lessons Learned

- A single perceptron can reach `75%` on this dataset, but no learning rate can
  make its plane classify all eight points correctly.
- Learning rate affects how training moves through weight space. It does not
  change which patterns one linear boundary can represent.
- Check predictions across the full dataset. The `75%` result hides two
  misclassified vertices.

## Follow-Up

- Submit the flag on the CyLab page and confirm the learning-path progress
  updates.
- Cold re-solve due `2026-10-28`.
- Next: Ethics Reflection - Guarding the Archive.
