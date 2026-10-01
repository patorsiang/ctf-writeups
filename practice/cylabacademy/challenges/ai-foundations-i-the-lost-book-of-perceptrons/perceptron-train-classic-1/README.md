# Perceptron Train Classic 1

## Metadata

- Platform: CyLab Academy
- Learning Path: AI Foundations I - The Lost Book of Perceptrons
- Category: Artificial Intelligence
- Difficulty: Easy
- Status: Solved
- Started: 2026-10-01
- Completed: 2026-10-01
- Re-solve: n/a
- Files: none (browser-only service)
- Skills Learned: Learning-rate range, perceptron learning algorithm

## Problem Summary

A web service (`http://chatelaine.cylabacademy.net:24090/`) trains a 2D
perceptron with the classic update rule (only misclassified points update the
model). I choose the learning rate; each run is capped at 16 updates. The flag
appears after 5 different rates each reach 100% accuracy.

## Prediction

Write this before any hint, tool, or AI help, and don't edit it afterward:
"I think this is X because Y." Score it once solved: right / partly / wrong,
and say what you missed.

- Guess: not written before the runs
- Score: n/a

## First Observations

- Same start as Classic 0: `w1 = 1.00, w2 = -1.00, b = 0.00`.
- Limit: 16 updates per run.
- Counter: "Successful learning rates: 0/5".
- Every run animates all 16 steps before showing the result, so the flag appears after a short delay.

## Solve Log

Write this while you solve, in your own words, including wrong guesses. Don't
tidy it up afterward. One entry per hypothesis:

- **Thought:** what I suspected and why
  - **Tried:** command, input, or code
  - **Result:** what happened, and what it ruled in or out

## Key Idea

The dataset is gentle and the start is close to a separating line, so a whole
range of small rates works. Rates `0.02` to `0.07` all reached 100%
(6/5 successful). Final run at `0.07`: `w1 = 1.21, w2 = -0.72, b = -0.07`.

## Solution Walkthrough

1. Open the service.
2. Run training at `0.02`, `0.03`, `0.04`, `0.05`, `0.06`, `0.07`.
3. Wait for each run to finish its 16 steps; the flag unlocks after 5 successes.

## Commands Or Script

None. The whole solve is in the browser UI.

## Flag

`academy{perceptron_classic_5rates_813951f0}`

## Lessons Learned

- Many learning rates can work on easy data.
- Close-together rates pass the challenge but don't show the range; test far-apart rates to find where training breaks.

## Follow-Up

- Open question: does `1.0` or the max rate still reach 100%?
- Next: More Challenging Datasets (reading), then Perceptron Train Classic 2 Alpha.
