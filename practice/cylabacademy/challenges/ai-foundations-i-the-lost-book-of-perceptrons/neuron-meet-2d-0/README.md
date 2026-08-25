# Neuron Meet 2D-0

## Metadata

- Platform: CyLab Academy
- Learning Path: AI Foundations I - The Lost Book of Perceptrons
- Category: AI / Networking
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-25
- Completed: 2026-08-25
- Files: `solve.py`
- Skills Learned: Netcat-style TCP probing, 2D perceptron decision boundaries, controlled output patterns, ASCII bits

## Problem Summary

The challenge provides a raw TCP service:

```sh
nc aureolin-pixie.cylabacademy.net 56279
```

The service is a two-dimensional perceptron. We send a pair of numbers, `x` and
`y`, and the service tells us whether the neuron fires (`1`) or stays quiet
(`0`). The goal is to make the last eight outputs read:

```text
01110000
```

That bit pattern is ASCII `p`.

## First Observations

On connect, the service explains the rules:

```text
Welcome to Neuron Meet 2D-0!
Probe the 2D perceptron to coax out the ASCII for 'p'.
Send two numbers (x, y) to see if the perceptron fires (1) or stays quiet (0).
- Bounds: [-10.0, 10.0] for both x and y
- Output rule: w1*x + w2*y + b >= 0 -> 1, else 0.
- No back-to-back repeats of the same (x, y) pair.
- Goal: make the last 8 outputs read 01110000 (ASCII 'p').
- Command: RESET to clear the firing history.
- Format: x,y or x y (comma or space separated)
```

The important detail is the output rule:

```text
w1*x + w2*y + b >= 0 -> 1, else 0
```

That means the hidden model separates the 2D plane with a straight decision
boundary. Points on one side produce `1`; points on the other side produce `0`.

## What I Tried

First, probe easy corner points:

```text
-10,-10 -> 0
10,10   -> 1
10,-10  -> 0
-10,10  -> 0
```

This shows that, for this instance, the positive diagonal point `(10, 10)` is
on the firing side, while the negative diagonal point `(-10, -10)` and both
mixed-sign corners are on the quiet side.

That is already enough to produce the target pattern. We do not need to recover
the exact weights `w1`, `w2`, or bias `b`; we only need a few distinct points
that reliably produce `0` and a few distinct points that reliably produce `1`.

## Key Idea

The target is:

```text
01110000
```

So we need:

- one quiet point for the first `0`
- three firing points for `111`
- four quiet points for `0000`

The "no back-to-back repeats" rule blocks sending the exact same pair twice in
a row. It does not block different points that land on the same side of the
boundary.

Safe firing points from the positive diagonal:

```text
10,10
9,9
8,8
```

Safe quiet points from the negative diagonal:

```text
-10,-10
-9,-9
-8,-8
-7,-7
-6,-6
```

One common pitfall is sending four firing points before the quiet points:

```text
-10,-10
10,10
9,9
8,8
7,7
-9,-9
-8,-8
-7,-7
-6,-6
```

At eight outputs, that gives `01111000`, and after the ninth output the last
eight become `11110000`. Neither is ASCII `p`. The challenge needs exactly one
`0`, then three `1`s, then four `0`s.

## Solution Walkthrough

1. Connect to the service with `nc`.
2. Probe corner points to find one reliable `0` side and one reliable `1` side.
3. Use distinct points from those sides to spell `01110000`.
4. Stop once the service prints the flag.

The final manual input sequence is:

```text
-10,-10
10,10
9,9
8,8
-9,-9
-8,-8
-7,-7
-6,-6
```

The verified output sequence is:

```text
Recent outputs (1/8): 0
Recent outputs (2/8): 01
Recent outputs (3/8): 011
Recent outputs (4/8): 0111
Recent outputs (5/8): 01110
Recent outputs (6/8): 011100
Recent outputs (7/8): 0111000
Recent outputs (8/8): 01110000
Pattern matched! ASCII 'p' unlocked.
```

## Commands Or Script

Manual solve:

```sh
nc aureolin-pixie.cylabacademy.net 56279
```

Then paste:

```text
-10,-10
10,10
9,9
8,8
-9,-9
-8,-8
-7,-7
-6,-6
```

Or run the helper script with the current instance port:

```sh
python3 solve.py 56279
```

## Flag

```text
academy{2d_n3ur0n_m3t_892056ff}
```

## Lessons Learned

- A 2D perceptron creates a straight-line decision boundary.
- For this challenge, finding safe points on each side matters more than
  calculating the exact model weights.
- Repeated output bits can be produced with different input pairs from the same
  side of the boundary.
- Count the exact target bits before submitting. ASCII `p` is `01110000`, which
  has three `1`s, not four.

## Follow-Up

- Practice sketching 2D threshold boundaries from corner probes.
- For later perceptron challenges, separate "map the boundary" from "spell the
  requested output pattern."
