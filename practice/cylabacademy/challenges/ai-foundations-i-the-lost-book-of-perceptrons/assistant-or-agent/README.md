# Assistant or Agent?

## Metadata

- Platform: CyLab Academy
- Learning Path: AI Foundations I - The Lost Book of Perceptrons (Interlude - AI Modalities)
- Category: Artificial Intelligence
- Difficulty: Easy
- Status: Solved
- Started: 2026-10-05
- Completed: 2026-10-05
- Re-solve: n/a (no hints on the challenge itself; Claude only helped with the netcat setup)
- Files: [transcript.txt](transcript.txt) (full session). Service: `nc xebec.cylabacademy.net 41278`, 15-minute instance). Challenge page: https://learn.cylabacademy.org/learning-paths/20/220
- Skills Learned: Telling assistant-style AI (advises) apart from agent-style AI (acts); scoping agent autonomy with approval gates, allowlists, and budget caps

## Problem Summary

Interactive fiction set at Westbrook High (author: LT 'syreal' Jones). The scenario
asks when an AI assistant should advise, when an AI agent should act, and how
permissions, guardrails, and review checkpoints keep autonomous actions safe.
The flag comes from working through the story over netcat. Three hints were
available; none were revealed.

## Prediction

Write this before any hint, tool, or AI help, and don't edit it afterward:
"I think this is X because Y." Score it once solved: right / partly / wrong,
and say what you missed.

- Guess: not written before the run (missed this step)
- Score: n/a

## First Observations

- Service: Python interactive fiction (`/app/assistant_vs_agent.py`) over netcat.
- It blocks on `input()` at every "Press Enter to continue" prompt.
- Running it through Claude Code's `!` prefix crashed at the first prompt with
  `EOFError: EOF when reading a line`. That shell has no stdin, so `input()`
  hits end-of-file at once. It works fine in a real terminal.

## Solve Log

Write this while you solve, in your own words, including wrong guesses. Don't
tidy it up afterward. One entry per hypothesis:

The Tried and Result lines come from [transcript.txt](transcript.txt). The
Thought lines are still mine to write.

- **Thought:** TODO (why I picked C)
  - **Tried:** Scene 1, schedule for 27 volunteers in 10 minutes. Picked **C**: agent with a human approval checkpoint before messages are sent.
  - **Result:** ARIA drafted the schedule and queued messages. Ren fixed 3 flagged edge cases, then approved. "Autonomy for the tedious parts, human checkpoint for high-impact actions."
- **Thought:** TODO (why I picked B)
  - **Tried:** Scene 2, three trustworthy facts for a poster. Picked **B**: agent browses approved sites and attaches citations.
  - **Result:** Evidence packet with quotes, link snapshots, and a confidence note per claim.
- **Thought:** TODO (why I picked B)
  - **Tried:** Scene 3, snack order with a $120 budget. Picked **B**: agent orders with a $120 cap, approved stores, and confirmation for substitutions.
  - **Result:** One item was out of stock. ARIA asked before substituting and finished at $119.42.
- **Thought:** TODO (did I expect the flag at the end, or a quiz?)
  - **Tried:** Pressed Enter through the ending.
  - **Result:** The flag was printed in the final dialogue and again in the takeaways.

## Key Idea

There is no exploit. The challenge checks one idea:

- An **assistant** only produces output. A human still takes every action.
- An **agent** plans and acts through tools in real systems. Its actions have
  side effects.
- So give an agent autonomy for low-impact, reversible steps. Put a guardrail
  in front of each high-impact step:
  - Sending messages to people: **human approval gate** (Scene 1).
  - Trusting information: **source allowlist + citations** (Scene 2).
  - Spending money: **budget cap + store allowlist + escalate on exceptions**
    (Scene 3).

In every scene, the rejected options were the two extremes: no autonomy
(assistant only, slow or unverified) or unlimited autonomy ("handle it however
you want").

## Solution Walkthrough

1. Launch the instance and run `nc xebec.cylabacademy.net 41278` in a real
   terminal. It needs a keyboard on stdin.
2. Press Enter through the intro.
3. Scene 1: `c` (agent + human approval before sending).
4. Scene 2: `b` (agent + approved sources + citations).
5. Scene 3: `b` (agent + $120 cap, approved stores, confirm substitutions).
6. Press Enter through the ending. The flag is printed twice.

Only this path was played. I did not test whether a wrong choice blocks the flag.

## Commands Or Script

```sh
nc xebec.cylabacademy.net 41278   # run in a real terminal, not a non-interactive shell
```

No script: the solve is the choices made in the story (see Solve Log).

## Flag

`academy{4551574n7_0r_463n7_846d23d5}`

## Lessons Learned

- "Assistant vs agent" is about who acts, not how smart the model is ("same brain, different level of hands").
- Match the guardrail to the side effect: approval for messages, allowlists for sources, caps for money.
- `EOFError: EOF when reading a line` means stdin is closed. Run interactive services in a real terminal, not through a non-interactive shell such as Claude Code's `!` prefix.
- Process miss: the Prediction was not written before the run, the 4th solve in a row.

## Follow-Up

- No `notes/ai.md` exists yet. After the Perceptron Problems block, consider one for AI/ML challenge patterns.
- Optional: replay with B in Scene 1 or C in Scene 3 to see how the story handles unsafe autonomy.
