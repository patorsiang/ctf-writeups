# Trust But Verify

## Metadata

- Platform: CyLab Academy
- Learning Path: AI Foundations I - The Lost Book of Perceptrons (Interlude)
- Category: AI Ethics / Interactive Fiction
- Difficulty: Easy
- Status: Solved
- Started: 2026-09-15
- Completed: 2026-09-15
- Files: `transcript.txt`
- Skills Learned: Claim decomposition, order-of-magnitude bounds checking, independent vs. same-origin verification, reading code before running it

## Problem Summary

An interactive fiction served over raw TCP:

```sh
nc aureolin-pixie.cylabacademy.net 57307
```

Ren, a high-school junior, writes a science fair proposal with help from ARIA,
an AI study companion. Three scenes, each offering a cheap option (trust) and a
costly one (verify). There is no puzzle to reverse engineer - the flag is
awarded for taking verification seriously.

The port changes per instance.

## First Observations

The service needs a real terminal. Running it through a piped stdin - including
Claude Code's `!` prefix - kills it on the first prompt:

```text
EOFError: EOF when reading a line
  File "/app/trust_but_verify.py", line 27, in wait_for_key
    input("\n---\n(Press Enter to continue...)\n---\n")
```

`tty` reports `not a tty`, so `input()` gets EOF immediately. `script` cannot
rescue it because the outer stdin is already closed before `script` runs. The
fix is an actual terminal:

```sh
script -q transcript.txt nc aureolin-pixie.cylabacademy.net 57307
```

`script` captures both sides of the session. Plain `nc | tee` would record the
story but lose the choices, which for this challenge is the half that matters.

## The Three Scenes

### Scene 1 - The Statistic

ARIA offers: *"Every year, over 500 million metric tons of plastic enter the
world's oceans"*, attributed to a 2022 UNEP report.

Options were to type it in, ask ARIA for the source link, or look it up
independently. **Chose: look it up independently.**

The number dies on arithmetic before any source is consulted. Global plastic
*production* is roughly 400 million tonnes per year; ocean input is roughly
8-11 million tonnes per year. The claim asserts more plastic entering the ocean
than the world manufactures. Off by a factor of about fifty.

Asking ARIA for the source link is the trap option. It feels like verification
but queries the same system that produced the claim - one source wearing two
hats. A system that can invent a statistic can invent a plausible URL, and the
worse case is a *real* report cited for a number it does not contain.

Note what shaped the error: Ren asked for "something that'll grab the judges."
ARIA produced something impressive. The failure was not random noise, it was
steered by the request.

### Scene 2 - The Code

ARIA supplied a script, said "just run it":

```python
data  = [8, 9, 10, 11, 13, 14]   # million metric tons, 2017-2022
years = [2017, 2018, 2019, 2020, 2021, 2022]
average = sum(data) / len(years) + 1  # adjusted average
print(f'Average annual input: {average:.2f} million metric tons')
```

Options were to run it or read it first. **Chose: read it first.**

Three defects:

1. `+ 1` is not part of any average. It inflates the result by 9.2%
   (10.83 -> 11.83). The comment `# adjusted average` reads like a considered
   methodological choice and justifies nothing.
2. `len(years)` should be `len(data)`. Both are 6, so it is correct by
   coincidence. Append one data point without a matching year and it silently
   reports 14.71 where 12.00 is correct - no exception, no warning.
3. Ren asked for a bar chart. This prints a line of text. The output is shaped
   like an answer, so the mismatch with the actual request slides past.

The code runs clean. No crash, no error, plausible number. **Running it teaches
you nothing here** - running catches crashes, reading catches wrong logic, and
neither substitutes for the other.

The sharpest detail: `11.83` is *closer* to the real-world ~11 Mt figure
verified in Scene 1 than the correct `10.83` is. The sanity check learned one
scene earlier passes the buggy version and would flag the correct one. A
verification habit becomes a blind spot the moment it is the only one you have.

### Scene 3 - The Citation

ARIA offers: *"Microplastics have now been detected in human blood, suggesting
direct health consequences. A 2021 study by Dr. Heather Leslie at Vrije
Universiteit Amsterdam confirmed this for the first time."*

Options were to use it because it is too specific to be wrong, or verify
anyway. **Chose: verify anyway.**

Decomposed, a citation is five claims wearing a trench coat:

| Component | Verdict |
| --- | --- |
| Dr. Heather Leslie exists | correct |
| Vrije Universiteit Amsterdam | correct |
| Microplastics found in human blood | correct |
| Published 2021 | wrong - 2022, *Environment International* |
| "confirmed", "direct health consequences" | wrong - the paper calls it preliminary |

The second error matters more than the date. The study **detected**
microplastics; it did not establish harm. Sliding from detection to consequence
is invisible to citation-checking because the citation is genuine. You can
confirm the paper, the author and the finding and still be propagating a claim
the paper does not make.

Specific details are cheap to generate and expensive to check. That asymmetry
is the entire mechanism - a name, an institution and a year look like
provenance, but the feeling comes from the format. Partial correctness is more
dangerous than fabrication: a wholly invented citation dies on the first
search, while this one survives it and gets verified into the proposal.

## Key Idea

Three grades of wrong, each defeated by a different instrument:

| Grade | Why dangerous | What defeats it |
| --- | --- | --- |
| Wrong | Barely - any check catches it | A glance, or an order-of-magnitude bound |
| Subtly wrong | Survives a re-read, because re-reading reuses the assumptions that produced it | An *independent* check - different method, different source |
| Almost-right | Passes normal testing, fails at an edge | Adversarial input: the boundary, the empty case, the extreme |

Re-reading an answer is not verification. Two sources copying one origin are
one source. Confidence carries no information about correctness - ARIA states
this outright after Scene 1: "I stated that with complete confidence and I was
wrong by a factor of fifty."

## Solution Walkthrough

1. Connect from a real terminal, wrapped in `script` to capture the session.
2. Scene 1: choose `c` - look it up independently.
3. Scene 2: choose `b` - read the code before running it.
4. Scene 3: choose `b` - verify the citation anyway.
5. ARIA hands over the flag: "here's something you can actually verify."

## Commands Or Script

```sh
script -q transcript.txt nc aureolin-pixie.cylabacademy.net 57307
```

No solver. Writing one would have missed the point - the content is the
judgment, not a computation. Full session in `transcript.txt`.

## Flag

```text
academy{7ru57_15_34rn3d_a5b4c2e0}
```

## Field Notes: The Same Failures, Live, In The Same Session

This challenge was worked immediately after `neuron-express-2d-0`, in a session
with an AI assistant. That session produced two textbook instances of exactly
what the fiction describes, which is better evidence than the fiction itself.

**1. A confident plan built on an unread constraint.** The assistant argued to
probe all 441 grid points because "the server's acceptance test is exactly the
full grid, so local verification is bit-identical." Every sub-claim was true.
The reasoning was valid. It was still unusable, because `[1/128]` was printed on
line 1 of the banner and never read. Cost: two burned instances. This is the
Scene 1 shape - correct facts, valid reasoning, one missing constraint, stated
with total confidence.

**2. A command recommended without checking its precondition.** The assistant
supplied `script -q transcript.txt nc ...` for use inside Claude Code without
verifying the harness provides a TTY. It does not. The game crashed on the
first prompt. This is the Scene 2 shape - it looked right, and only running it
revealed otherwise.

Both were caught the same way: by running them against reality, not by
re-reading them.

## Lessons Learned

- Check a claim against a bound it cannot exceed before hunting for sources.
  "More plastic in the ocean than is manufactured" needs no citation to reject.
- Asking the source of a claim to vouch for the claim is not verification.
- Running code catches crashes. Reading code catches wrong logic. Correct-looking
  output is not evidence of correct code.
- A confident comment on a wrong line (`# adjusted average`) is worse than no
  comment - it pre-empts the question.
- Coincidental correctness (`len(years)` == `len(data)`) is a latent bug, not a
  working line. It breaks on the first edit, silently.
- Decompose compound claims and check each part. Citations fail partially, and a
  partial failure reads as a pass when the bundle is judged as a unit.
- Specificity is not evidence. Specific details are cheap to generate and
  expensive to check, which is precisely why they are persuasive.
- Every verification habit becomes a blind spot when it is the only one. An
  order-of-magnitude check catches factor-of-fifty errors and is useless against
  9% ones.
- Read the interface before designing around it. Both live failures above were
  preconditions printed or checkable in advance.

## Follow-Up

- Add a `notes/` entry on verification tactics by claim type (statistic, code,
  citation, plan) so this generalises past the challenge.
- Revisit `neuron-express-2d-0` - the version-space stopping rule is the same
  instinct formalised: stop when every surviving hypothesis agrees, not when
  the answer feels right.
- Practise the order-of-magnitude bound as a reflex on any statistic before
  reaching for a source.
