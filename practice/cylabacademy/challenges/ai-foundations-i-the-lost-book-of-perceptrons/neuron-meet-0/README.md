# Neuron Meet 0

## Metadata

- Platform: CyLab Academy
- Learning Path: AI Foundations I - The Lost Book of Perceptrons
- Category: AI / Networking
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-22
- Completed: 2026-08-22
- Files: `solve.py`
- Skills Learned: Netcat-style TCP probing, binary search, decision boundaries, simple automation

## Problem Summary

The challenge provides a raw TCP service:

```sh
nc aureolin-pixie.cylabacademy.net 50261
```

The service is a one-dimensional perceptron. We can send numbers and observe
whether the perceptron outputs `0` or `1`. The goal is to make the last eight
outputs read:

```text
01110000
```

That bit pattern is ASCII `p`.

## First Observations

On connect, the service prints the useful rules:

```text
Bounds: [-10.0, 10.0]
Output rule: w*x + b >= 0 -> 1, else 0.
No back-to-back repeats of the same number.
Goal: make the last 8 outputs read 01110000 (ASCII 'p').
Command: RESET to clear the firing history.
```

The important detail is that this is a threshold function. There is some
boundary on the number line where the output changes from one bit to the other.

## What I Tried

First, probe the extremes:

```text
x=-10.00000000 -> 0
x= 10.00000000 -> 1
```

That proves low values are on the `0` side and high values are on the `1` side
for this connection.

Then binary-search the boundary:

```text
x= 0.00000000 -> 0
x= 5.00000000 -> 1
x= 2.50000000 -> 1
x= 1.25000000 -> 0
...
x= 1.99996948 -> 0
x= 2.00004578 -> 1
```

So the boundary is very close to `2.0`.

## Key Idea

The perceptron uses:

```text
w*x + b >= 0 -> 1
```

For a one-dimensional perceptron, that creates one decision boundary. Values on
one side produce `0`; values on the other side produce `1`.

Binary search works because each probe tells us which half of the current range
contains the boundary. Once we know safe values on both sides, we do not need
the exact weights. We only need values that reliably produce each desired bit.

The "no back-to-back repeats" rule means repeated output bits must use different
numbers on the same side. For example, `10.0`, `9.9`, and `9.8` are different
inputs but all still safely produce `1`.

## Solution Walkthrough

1. Connect to the service.
2. Send `-10.0` and `10.0` to learn which extreme produces `0` and which
   produces `1`.
3. Binary-search between the extremes to locate the decision boundary.
4. Send `RESET` so earlier probes do not affect the final eight-output history.
5. Send distinct numbers from the correct sides to produce `01110000`.

For this run, the final sequence was:

```text
x=-10.00000000 -> 0
x= 10.00000000 -> 1
x= 9.90000000 -> 1
x= 9.80000000 -> 1
x=-9.90000000 -> 0
x=-9.80000000 -> 0
x=-9.70000000 -> 0
x=-9.60000000 -> 0
```

The service accepted the pattern:

```text
Recent outputs (8/8): 01110000
Pattern matched! ASCII 'p' unlocked.
```

## Commands Or Script

Run the solver from this challenge directory:

```sh
python3 solve.py
```

The same idea can also be done manually with `nc`, but a script prevents typing
mistakes and makes it easy to avoid sending the same number twice in a row.

## Flag

```text
academy{n3ur0n_m3t_227803d1}
```

## Lessons Learned

- A perceptron with one numeric input behaves like a threshold on a number line.
- Binary search is useful when feedback only says which side of a boundary a
  probe landed on.
- Repeated output bits do not require repeated inputs. Use different values on
  the same side of the boundary.
- `RESET` is useful when a service keeps history and the final answer depends
  only on the last few interactions.

## Follow-Up

- Practice recognizing monotonic threshold problems before trying random
  guesses.
- For later AI/security challenges, separate "learn the model behavior" from
  "submit the required output pattern."
