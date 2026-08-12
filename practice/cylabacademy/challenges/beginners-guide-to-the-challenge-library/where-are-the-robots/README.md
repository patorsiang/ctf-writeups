# Where Are The Robots

## Metadata

- Platform: CyLab Academy / picoCTF
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: Web
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-12
- Completed: 2026-08-12
- Target: `http://fickle-tempest.picoctf.net:51948`
- Skills Learned: `robots.txt`, web enumeration, `curl`, `grep`

## Problem Summary

The challenge asks:

```text
Can you find the robots?
```

The target is a small website. The title points directly at `robots.txt`, a
standard file websites use to give web crawlers crawl instructions.

## First Observations

Open the site normally first, then check the common web-discovery file:

```bash
curl http://fickle-tempest.picoctf.net:51948/robots.txt
```

Output:

```text
User-agent: *
Disallow: /cc6b1.html
```

That `Disallow` line is the useful clue. It tells crawlers not to visit
`/cc6b1.html`, which makes it exactly the page worth checking in a CTF.

## What I Tried

After finding the disallowed path, request that page and filter for the picoCTF
flag pattern:

```bash
curl http://fickle-tempest.picoctf.net:51948/cc6b1.html | grep -o 'picoCTF{[^}]*}'
```

## Key Idea

`robots.txt` is not access control. It is only a public instruction file for
crawlers. If a sensitive path appears there, anyone can still request that path
directly unless the server enforces real authentication or authorization.

For CTF web challenges, `robots.txt` is one of the cheapest first checks:

```text
/robots.txt
/sitemap.xml
/admin
/login
```

## Solution Walkthrough

Fetch `robots.txt`:

```bash
curl http://fickle-tempest.picoctf.net:51948/robots.txt
```

Find the hidden path:

```text
Disallow: /cc6b1.html
```

Fetch that path and extract the flag:

```bash
curl http://fickle-tempest.picoctf.net:51948/cc6b1.html | grep -o 'picoCTF{[^}]*}'
```

Output:

```text
picoCTF{ca1cu1at1ng_Mach1n3s_cc6b1}
```

## Commands Or Script

```bash
curl http://fickle-tempest.picoctf.net:51948/robots.txt
curl http://fickle-tempest.picoctf.net:51948/cc6b1.html | grep -o 'picoCTF{[^}]*}'
```

## Flag

```text
picoCTF{ca1cu1at1ng_Mach1n3s_cc6b1}
```

## Lessons Learned

- Check `/robots.txt` early on beginner web challenges.
- `Disallow` means "please do not crawl this," not "users cannot access this."
- Public metadata files can reveal hidden routes, admin pages, old assets, or
  challenge-specific flag pages.
- Reuse `grep -o 'picoCTF{[^}]*}'` to extract just the flag from HTML.

## Follow-Up

- Add `robots.txt` to the beginner web enumeration checklist.
