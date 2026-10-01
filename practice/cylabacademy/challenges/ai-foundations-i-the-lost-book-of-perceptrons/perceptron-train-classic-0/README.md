# Perceptron Train Classic 0

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
- Skills Learned: Perceptron learning algorithm, learning rate as a hyperparameter

## Problem Summary

A web service (`http://xebec.cylabacademy.net:30300/`) trains a 2D perceptron
with the classic update rule: only misclassified points change `w1`, `w2`, `b`.
I choose only the learning rate. A run is capped at 16 updates, and the flag
appears when every point is classified correctly.

## Prediction

Write this before any hint, tool, or AI help, and don't edit it afterward:
"I think this is X because Y." Score it once solved: right / partly / wrong,
and say what you missed.

- Guess: not written before the run (missed this step)
- Score: n/a

## First Observations

- Starting line: `w1 = 1.00, w2 = -1.00, b = 0.00`.
- Default learning rate: `0.02`.
- Limit: 16 updates per run.

## Solve Log

Write this while you solve, in your own words, including wrong guesses. Don't
tidy it up afterward. One entry per hypothesis:

- **Thought:** what I suspected and why
  - **Tried:** command, input, or code
  - **Result:** what happened, and what it ruled in or out

## Key Idea

The starting line was already close to separating the classes, so even
small steps (`0.02`) were enough to reach 100% within 16 updates. Final:
`w1 = 1.20, w2 = -0.72, b = 0.00`.

## Solution Walkthrough

1. Open the service.
2. Keep the learning rate at `0.02`.
3. Press **Run training** and wait for step 16/16 at 100% accuracy.

## Commands Or Script

None. The whole solve is in the browser UI.

## Flag

`academy{perceptron_classic_mode_4ef55864}`

## Lessons Learned

- A small learning rate is fine when the start is already close.
- The default can be a valid answer; try it before tuning.

## Follow-Up

- Optional: compare `0.02` vs `1.0` vs max rate to see how the step size changes the line.
- Next: Perceptron Train Classic 1.
