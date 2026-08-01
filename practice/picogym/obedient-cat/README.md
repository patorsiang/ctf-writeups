# picoCTF - Obedient Cat

## Challenge

The challenge provides a file named `flag`.

## Solution

List the files in the challenge directory:

```bash
ls
```

The only file is:

```text
flag
```

Since the challenge hint is essentially telling us to read the file, use `cat`:

```bash
cat flag
```

Output:

```text
picoCTF{s4n1ty_v3r1f13d_9b8fa0bc}
```

## Flag

```text
picoCTF{s4n1ty_v3r1f13d_9b8fa0bc}
```

## What I Learned

`cat` prints the contents of a file to the terminal. In beginner CTF challenges, sometimes the goal is simply to practice basic Linux commands and verify that you can inspect files from the command line.
