# Enhance!

## Metadata

- Platform: CyLab Academy / picoCTF
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: Forensics
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-16
- Completed: 2026-08-16
- Files: `drawing.flag.svg`
- Skills Learned: SVG source inspection, XML text elements, hidden tiny text

## Problem Summary

The challenge provides an SVG image and asks for the flag hidden inside it.

The title is a hint: the image looks simple when rendered, but the useful
details are in the source text that describes the image.

## First Observations

```bash
file drawing.flag.svg
```

```text
drawing.flag.svg: SVG Scalable Vector Graphics image
```

An SVG is different from a PNG or JPEG. It is an XML document: shapes,
styles, positions, and text are all stored as readable markup.

## Key Idea

**Open SVG files as text.** If the image hides tiny, white, off-canvas, or
overlapped text, the rendered view may hide it, but the XML source still
has to describe it.

In this file, the flag is stored inside a `<text>` element split across
several `<tspan>` elements. The style makes it almost invisible:

```xml
font-size:0.00352781px;
fill:#ffffff;
```

That means the text is extremely small and white. Visually it blends into
the image, but the markup gives it away.

## Solution Walkthrough

Inspect the file type first:

```bash
file drawing.flag.svg
```

Then read the SVG source:

```bash
sed -n '1,220p' drawing.flag.svg
```

This exact command is not magic. It is just one way to read part of a text
file without opening an editor:

- `sed` is a stream editor that can print selected lines.
- `-n` means "do not print every line automatically."
- `'1,220p'` means "print lines 1 through 220."
- `drawing.flag.svg` is the file being inspected.

Other commands would also work:

```bash
cat drawing.flag.svg
less drawing.flag.svg
head drawing.flag.svg
```

The important reasoning is:

1. `file drawing.flag.svg` says it is an SVG.
2. SVG is XML text, not a normal binary image format like PNG or JPEG.
3. Text-based files can be inspected directly.

Near the bottom of the file, the text is split over multiple lines:

```text
p
i
c
o
C
T
F { 3 n h 4 n
c 3 d _ d 0 a 7 5 7 b f }
```

Remove the spaces introduced by the hidden text layout:

```text
picoCTF{3nh4nc3d_d0a757bf}
```

## Commands Or Script

No script needed. The shortest useful command sequence is:

```bash
file drawing.flag.svg
sed -n '1,220p' drawing.flag.svg
```

If the flag is not obvious at first, search for SVG text nodes:

```bash
rg -n "text|tspan|picoCTF" drawing.flag.svg
```

`rg` is `ripgrep`, a fast search tool like a modern `grep`.

- `rg` means search through text.
- `-n` shows line numbers.
- `"text|tspan|picoCTF"` means search for `text`, `tspan`, or `picoCTF`.
- `drawing.flag.svg` is the file to search.

The same idea with `grep` would be:

```bash
grep -nE "text|tspan|picoCTF" drawing.flag.svg
```

## Flag

```text
picoCTF{3nh4nc3d_d0a757bf}
```

## Lessons Learned

- SVG is text-based XML, so source inspection is often more useful than
  looking at the rendered image.
- Hidden visual text still leaves evidence in markup: check `<text>`,
  `<tspan>`, font size, fill color, opacity, and coordinates.
- If a search pattern contains `{` or `}`, escape them or use a simpler
  literal search. Those characters have special meaning in regular
  expressions.

## Follow-Up

- For future image forensics, start with `file`, then decide whether the
  artifact is text-based, compressed, or binary before choosing tools.
