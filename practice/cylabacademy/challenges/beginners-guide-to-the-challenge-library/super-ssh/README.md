# Super SSH

## Metadata

- Platform: CyLab Academy / picoCTF
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: Networking
- Difficulty: Beginner
- Status: Solved
- Started:
- Completed: 2026-08-01
- Files:
- Skills Learned: SSH login, non-default ports, remote service connection

## Problem Summary

Connect to the picoCTF server over SSH and retrieve the flag printed after login.

## First Observations

- Host: `titan.picoctf.net`
- Port: `61484`
- Username: `ctf-player`
- Password: `6abf4a82`

The service uses SSH, but it is not on the default SSH port.

## What I Tried

The challenge gives all connection details, so the important part is choosing the correct SSH syntax for a custom port.

## Key Idea

SSH uses port `22` by default. When a challenge gives a different port, pass it with `-p <port>`.

## Solution Walkthrough

The challenge gives all of the SSH connection details. Since the SSH service is
running on a non-default port, use `-p` to specify the port:

```bash
ssh ctf-player@titan.picoctf.net -p 61484
```

When prompted, enter the provided password:

```text
ctf-player@titan.picoctf.net's password: 6abf4a82
```

After successful authentication, the server prints the flag and closes the
connection:

```text
Welcome ctf-player, here's your flag: picoCTF{s3cur3_c0nn3ct10n_65a7a106}
Connection to titan.picoctf.net closed.
```

## Flag

```text
picoCTF{s3cur3_c0nn3ct10n_65a7a106}
```

## Lessons Learned

- SSH normally connects on port `22`.
- In this challenge, the service is exposed on port `61484`, so omitting `-p 61484` would try the wrong port.
- When a CTF challenge provides a host, username, password, and port, write the connection command carefully before debugging anything else.

## Follow-Up

- Practice recognizing command options like `-p` because many networking tools have similar host/port patterns.
