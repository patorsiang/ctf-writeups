# Magikarp Ground Mission

## Metadata

- Platform: CyLab Academy / picoCTF 2021
- Learning Path: General Skills in CTF's
- Category: General Skills / SSH
- Difficulty: Easy
- Status: Solved
- Started: 2026-10-24
- Completed: 2026-10-24
- Re-solve: due 2026-10-31
- Files: None
- Skills Learned: SSH port syntax, shell navigation, `ls`, `cat`

## Problem Summary

Connect to a challenge host over SSH, follow instructions in files, and collect three flag fragments from the home directory and `/`. Source: [CyLab Academy challenge](https://learn.cylabacademy.org/learning-paths/14/101).

## Prediction

- Guess: Not recorded before connecting.
- Score: n/a

## First Observations

- The challenge provided the username `ctf-player`, a host, a port, a password, and a first instruction to log in and run `ls`.
- SSH needs the port as an option: `ssh -p <port> ctf-player@<host>`. Writing `<host>:<port>` after `@` makes SSH treat the whole string as the hostname.
- A non-interactive command runner could not handle SSH's host-key prompt. In an interactive terminal, SSH displayed an unknown ED25519 key; I accepted it for the challenge endpoint, and SSH saved it to `known_hosts`. I did not compare the fingerprint against an independent trusted source.
- The initial `ls` showed `1of3.flag.txt` and `instructions-to-2of3.txt`.

## Solve Log

- **Thought:** Connect to the supplied host and port with SSH.
  - **Tried:** First used `ssh ctf-player@<host>:<port>`.
  - **Result:** SSH could not resolve the hostname because it parsed the port as part of the hostname. Using `-p <port>` fixed the syntax.
- **Thought:** SSH needs an interactive terminal to ask about the unknown host key and password.
  - **Tried:** Ran `ssh -p <port> ctf-player@<host>` in an interactive terminal, accepted the challenge endpoint's host key, and entered the challenge password.
  - **Result:** The login opened a shell as `ctf-player`.
- **Thought:** The first instruction file tells me where to find the next fragment.
  - **Tried:** Listed the home directory, read `1of3.flag.txt`, and read `instructions-to-2of3.txt`.
  - **Result:** The first fragment was `academy{xxsh_`. The instruction said to go to `/`.
- **Thought:** The second fragment should be at the filesystem root.
  - **Tried:** Ran `cd /`, listed the directory, then read `2of3.flag.txt` and `instructions-to-3of3.txt`.
  - **Result:** The second fragment was `0ut_0f_//4t3r_`. The instruction said to go home, or `~`.
- **Thought:** The last fragment should be in the home directory.
  - **Tried:** Ran `cd`, listed the directory, and read `3of3.flag.txt`.
  - **Result:** The last fragment was `47c47679}`. The file had no trailing newline, so the shell prompt appeared right after `}`. Joining all three fragments in order produced the flag.

## Key Idea

SSH starts the session in the user's home directory. The instruction files guide navigation to `/` and back to `~`; `ls` reveals files in each location, and `cat` reads their contents. The flag is split across three files.

## Solution Walkthrough

1. Connect with the host and port shown by the active challenge instance:

   ```sh
   ssh -p <port> ctf-player@<host>
   ```

2. Enter the challenge password when SSH prompts for it. On first connection, compare the host and port with the challenge page and verify the fingerprint against a trusted source when available. No independent fingerprint comparison was recorded for this run.
3. In the home directory, run `ls`, then read `1of3.flag.txt` and `instructions-to-2of3.txt`.
4. Follow the instruction with `cd /`. Run `ls`, then read `2of3.flag.txt` and `instructions-to-3of3.txt`.
5. Follow the instruction with `cd` to return home. Run `ls` and read `3of3.flag.txt`.
6. Join the three fragments in order without changing their characters.

## Commands Or Script

Use the current host and port from the challenge instance; these values can change after a restart.

```sh
ssh -p <port> ctf-player@<host>
ls
cat 1of3.flag.txt
cat instructions-to-2of3.txt
cd /
ls
cat 2of3.flag.txt
cat instructions-to-3of3.txt
cd
ls
cat 3of3.flag.txt
```

I accidentally used `&` between two `cat` commands once. `&` runs the first command in the background; use `;` for sequential commands.

## Flag

```text
academy{xxsh_0ut_0f_//4t3r_47c47679}
```

## Verification

The three service fragments join to the flag above. CyLab flag submission and learning-path completion were not confirmed.

## Lessons Learned

- Pass SSH ports with `-p`; `user@host:port` is not SSH port syntax.
- SSH may need an interactive terminal for host-key confirmation and password entry.
- Use `ls` to inspect the current directory and `cat` to read the files named by the challenge.
- `cd /` goes to the filesystem root; `cd` with no argument returns to the user's home directory.
- A shell command followed by `&` runs in the background. Use `;` to run commands sequentially.

## Follow-Up

- Re-solve this challenge from the instructions and file names without notes on 2026-10-31.
