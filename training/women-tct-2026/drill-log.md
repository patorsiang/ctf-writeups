# Drill Log

One row per drill. Each challenge's folder (`practice/...` or `events/...`)
holds its README with the Prediction and Solve Log. This log only measures.

Columns:
- `date`: `YYYY-MM-DD`
- `challenge`: a link to the folder
- `category`: one of `web` `forensics` `re-pwn` `network` `mobile` `programming` `crypto` `misc` `ai-iot`
- `source`: the platform or event
- `track`: `Q` (AI allowed) or `F` (no AI)
- `box`: the time box in minutes (easy 30, medium 60)
- `taken`: minutes actually spent
- `solved`: `yes`/`no`
- `ai`: `yes`/`no`
- `hint`: 0 none, 1 nudge, 2 technique, 3 solve path
- `note`: one line, including dead ends if unsolved

Past the time box → stop, log it as unsolved, write what was ruled out.
An F-track drill at hint ≥ 2 gets a 7-day re-solve.

| date | challenge | category | source | track | box | taken | solved | ai | hint | note |
|---|---|---|---|---|---|---|---|---|---|---|
