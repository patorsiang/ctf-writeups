# Perceptron Train Classic 2 Alpha

## Metadata

- Platform: CyLab Academy
- Learning Path: AI Foundations I - The Lost Book of Perceptrons
- Category: Artificial Intelligence
- Difficulty: Unknown
- Status: Solved
- Started: 2026-10-01
- Completed: 2026-10-01
- Re-solve: n/a
- Files: none (browser-only service)
- Skills Learned: Learning-rate search, sensitivity of a capped training run

## Problem Summary

A web service trains a 2D perceptron with the classic update rule (only
misclassified points update the model), capped at 16 updates per run. I
choose the learning rate. The dataset is harder than Classic 0 and 1: the line
has to turn a lot. The flag appears after 5 different rates each reach 100%.

## Prediction

Write this before any hint, tool, or AI help, and don't edit it afterward:
"I think this is X because Y." Score it once solved: right / partly / wrong,
and say what you missed.

- Guess: not written before the runs
- Score: n/a

## First Observations

- Start: `w1 = 1.00, w2 = -1.00, b = 0.00`. Several points begin on the wrong side.
- Limit: 16 updates per run. Slider range `0.02` to `20`, step `0.01`.
- Rate sweep (run by Claude on a relaunched instance, 2026-10-01). Same rate gives the same result every time:

  | Rate | Accuracy | | Rate | Accuracy |
  | --- | --- | --- | --- | --- |
  | 0.02 | 58.3% | | 0.29 | **100%** |
  | 0.05 | 75.0% | | 0.30 | 91.7% |
  | 0.10 | 91.7% | | 0.35 | 91.7% |
  | 0.15 | 83.3% | | 0.40 | **100%** |
  | 0.18 | **100%** | | 0.50 | 83.3% |
  | 0.19 | **100%** | | 0.75 | **100%** |
  | 0.20 | 91.7% | | 1.0 | **100%** |
  | 0.21 | 91.7% | | 1.5 | **100%** |
  | 0.22 | 83.3% | | 2 | **100%** |
  | 0.23 | 83.3% | | 3 | **100%** |
  | 0.24 to 0.28 | **100%** | | 5, 10, 20 | 83.3% |

## Solve Log

Write this while you solve, in your own words, including wrong guesses. Don't
tidy it up afterward. One entry per hypothesis:

- **Thought:** what I suspected and why
  - **Tried:** command, input, or code
  - **Result:** what happened, and what it ruled in or out

## Key Idea

Small rates like `0.02` can't move the line far enough in 16 updates: the
weights have to flip from `w2 = -1` to about `w2 = +1.5`. A jump to `0.2`
and then a search around `0.25` found 5 working rates (`0.24` to `0.28`).

The sweep shows the working rates are not one continuous range. With a fixed
sample order and only 16 updates, a small change in rate changes the whole
path, so the line may or may not land in a good spot at step 16. For large
rates (`5`, `10`, `20`) the start weights `(1, -1)` become negligible and
the result stops changing (83.3% for all three).

## Solution Walkthrough

1. Open the service.
2. Try `0.02` (fails, 58.3%), then jump to `0.2` (fails, 91.7%).
3. Search nearby: `0.25`, `0.24`, `0.26`, `0.27`, `0.28` all reach 100%.
4. The flag unlocks at 5/5.

## Commands Or Script

None. The solve is in the browser UI.

## Flag

`academy{perceptron_classic_2_alpha_5rates_11934bdb}`

## Lessons Learned

- When the default fails, jump by 10x first, then search nearby.
- With a capped number of updates, "works" is jumpy: don't assume the rates between two working rates also work.
- Repeat a run to check it's deterministic before trusting a result.

## Follow-Up

- Next: Interlude - AI Modalities.
