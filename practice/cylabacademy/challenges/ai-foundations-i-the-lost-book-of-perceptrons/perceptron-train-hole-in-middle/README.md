# Perceptron Train Hole in Middle

## Metadata

- Platform: CyLab Academy
- Learning Path: AI Foundations I - The Lost Book of Perceptrons
- Challenge: [Perceptron Train Hole in Middle](https://learn.cylabacademy.org/learning-paths/20/224)
- Category: Artificial Intelligence
- Difficulty: Easy
- Status: Solved
- Started: 2026-10-13
- Completed: 2026-10-13
- Re-solve: due 2026-10-20
- Files: none (browser-only service)
- Skills Learned: perceptron limits, linear separability, accuracy on imbalanced data

## Problem Summary

The trainer has eight class `1` points arranged in a ring and one class `0` point at the center. I needed to tune a single perceptron. The challenge accepts `88.9%` accuracy because one straight line cannot draw a boundary around the center point.

## Prediction

- Guess: not recorded before the first run
- Score: n/a

## First Observations

- The ring points have label `1`; the center point has label `0`.
- The trainer allows up to 16 updates per run.
- The success target is `88.9%`.

## Solve Log

The default rate, `0.02`, finished all 16 updates at `44.4%`. At `0.20`, training reached `88.9%` at step 12 and stopped. The final weights were different, but the second run met the target.

| Learning rate | Final step | w1 | w2 | b | Accuracy |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `0.02` | 16 | `0.80` | `-0.88` | `0.10` | `44.4%` |
| `0.20` | 12 | `0.20` | `0.20` | `1.00` | `88.9%` |

## Key Idea

At `0.20`, the perceptron scores each point with `0.20x + 0.20y + 1`. Its decision line is `x + y = -5`. Every ring point has `x + y >= -4`, so all eight ring points score above zero and get prediction `1`. The center scores `1` too, so it gets prediction `1` despite its true label being `0`. That gives eight correct predictions out of nine: `8 / 9 = 88.9%`.

The successful run does not isolate the center. It predicts the majority label for every point. A single straight line splits the plane into two half-planes; it cannot make a closed boundary around the center while leaving the ring on the other side. Changing the learning rate moves the line, but it cannot give the perceptron that missing shape.

## Solution Walkthrough

1. Open the challenge and start its training instance.
2. Run the default learning rate, `0.02`, as a baseline. This run reached `44.4%` in 16 updates.
3. Set the learning rate to `0.20` and run training again.
4. Confirm the trainer stops at step 12 with `88.9%` accuracy and weights `w1 = 0.20`, `w2 = 0.20`, and `b = 1.00`.
5. Submit the displayed flag. CyLab accepted it and marked the challenge solved.

## Commands Or Script

None. The training runs happened in the browser.

## Flag

`academy{h0l3_1n_m1ddl3_unl34rn4bl3_l1n34rly_5af09722}`

## Lessons Learned

- A learning rate changes the training path, not the shapes a single perceptron can represent.
- Accuracy can hide a missed minority example. Here, predicting `1` for every point gets `8 / 9` correct but still fails to identify the center point.
- A model needs a nonlinear boundary or additional features to represent a hole in the data.

## Follow-Up

- Cold re-solve due 2026-10-20.
- Next: Perceptron Train 3-Bit Parity.
