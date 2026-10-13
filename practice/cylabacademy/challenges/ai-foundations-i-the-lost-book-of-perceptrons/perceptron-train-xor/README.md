# Perceptron Train XOR

## Metadata

- Platform: CyLab Academy
- Learning Path: AI Foundations I - The Lost Book of Perceptrons
- Category: Artificial Intelligence
- Difficulty: Easy
- Status: Solved
- Started: 2026-10-13
- Completed: 2026-10-13
- Re-solve: 2026-10-20
- Files: none (browser-only service)
- Skills Learned: XOR and linear separability

## Problem Summary

The service trains one perceptron on four XOR points. The `1` labels sit on
opposite corners; the `0` labels sit on the other two. The service allows up
to 16 updates and accepts 75% accuracy, since one straight line cannot get
all four points right.

| y | x = -2 | x = 2 |
| --- | ---: | ---: |
| 2 | 1 | 0 |
| -2 | 0 | 1 |

## Prediction

- Guess: not recorded in this session
- Score: n/a

## Solve Log

I changed the learning rate from `0.02` to `0.2` and ran training. It reached
`75%` after two updates and showed the flag.

## Why 0.2 Worked

The log showed two mistakes. Both points had target `0`, but the perceptron
predicted `1`. The update error was `0 - 1 = -1`.

On the first point, `(-2, -2)`, a rate of `0.2` changes each weight by
`0.2 × -1 × -2 = +0.4` and the bias by `-0.2`. The next mistake, `(2, 2)`,
changes both weights by `-0.4` and the bias by `-0.2`.

| After update | w1 | w2 | b | Accuracy |
| --- | ---: | ---: | ---: | ---: |
| `(-2, -2)` | 1.40 | -0.60 | -0.20 | 50% |
| `(2, 2)` | 1.00 | -1.00 | -0.40 | 75% |

The final score is `x - y - 0.4`. Here is what it gives each point:

| Input | Expected | Score | Prediction |
| --- | ---: | ---: | ---: |
| `(-2, -2)` | 0 | -0.4 | 0 |
| `(-2, 2)` | 1 | -4.4 | 0 |
| `(2, -2)` | 1 | 3.6 | 1 |
| `(2, 2)` | 0 | -0.4 | 0 |

Three of the four predictions are correct, so accuracy is `75%`. In this run,
`0.2` moved the weights to that result in two updates.

## Why 100% Is Impossible

The labels alternate around the square. A straight boundary would need to put
both `1` corners on one side and both `0` corners on the other. The segment
between each same-label pair would stay with its label, but those two segments
cross at the center. The center cannot be on opposite sides at once. Changing
the weights moves the line; it cannot make XOR linearly separable.

## Solution Walkthrough

1. Set the learning rate to `0.2`.
2. Run training.
3. Confirm the service reports `75%` and returns:

```text
academy{x0r_unl34rn4bl3_by_p3rc3ptr0ns_d11b363c}
```

The CyLab page accepted the flag and marked the challenge solved.

## Commands Or Script

None. The run happened in the browser.

## Lessons Learned

- `75%` is the accepted target for this XOR dataset; 100% is impossible for one perceptron.
- The learning rate changes the update path. It cannot change what a straight line can separate.

## Follow-Up

- Cold re-solve due 2026-10-20.
- Next: Perceptron Train XNOR.
