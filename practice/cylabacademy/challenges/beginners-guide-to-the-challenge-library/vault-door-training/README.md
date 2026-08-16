# Vault Door Training

## Metadata

- Platform: CyLab Academy / picoCTF
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: Reverse Engineering
- Difficulty: Beginner
- Status: Solved
- Started: 2026-08-16
- Completed: 2026-08-16
- Files: `VaultDoorTraining.java`
- Skills Learned: Java source review, hard-coded password checks, input wrapping

## Problem Summary

The challenge gives the Java source code for a training vault door. The goal
is to read the source and recover the password that opens the vault.

This is beginner reverse engineering, but there is no binary analysis yet.
The source code is available, so the first move is to read the password check.

## First Observations

The program asks for one input:

```java
System.out.print("Enter vault password: ");
String userInput = scanner.next();
```

Then it removes the flag wrapper before checking the password:

```java
String input = userInput.substring("picoCTF{".length(),userInput.length()-1);
```

That means if the full input is:

```text
picoCTF{example}
```

the value passed into `checkPassword` is only:

```text
example
```

## Key Idea

**Read the validation function before guessing.**

The important function is:

```java
public boolean checkPassword(String password) {
    return password.equals("w4rm1ng_Up_w1tH_jAv4_000HPpgh7Ph");
}
```

`password.equals(...)` compares the user-controlled password to the exact
string inside the quotes. So the inner password is:

```text
w4rm1ng_Up_w1tH_jAv4_000HPpgh7Ph
```

Because `main` strips off `picoCTF{` and the final `}`, the full flag wraps
that inner password back in the picoCTF format.

## Solution Walkthrough

Open the Java file:

```bash
sed -n '1,120p' VaultDoorTraining.java
```

Find `checkPassword`:

```bash
rg -n "checkPassword|equals" VaultDoorTraining.java
```

Output:

```text
public boolean checkPassword(String password) {
    return password.equals("w4rm1ng_Up_w1tH_jAv4_000HPpgh7Ph");
}
```

Build the full flag:

```text
picoCTF{w4rm1ng_Up_w1tH_jAv4_000HPpgh7Ph}
```

## Commands Or Script

No script needed. The solve is source inspection:

```bash
sed -n '1,120p' VaultDoorTraining.java
rg -n "checkPassword|equals" VaultDoorTraining.java
```

Optional verification if Java is installed:

```bash
javac VaultDoorTraining.java
printf 'picoCTF{w4rm1ng_Up_w1tH_jAv4_000HPpgh7Ph}\n' | java VaultDoorTraining
```

Expected output:

```text
Enter vault password: Access granted.
```

## Flag

```text
picoCTF{w4rm1ng_Up_w1tH_jAv4_000HPpgh7Ph}
```

## Lessons Learned

- Source code is often the fastest path in beginner reverse engineering.
- Look for comparison functions like `equals`, `==`, `strcmp`, or
  password-checking functions.
- Pay attention to input preprocessing. Here, the program removes
  `picoCTF{` and `}` before checking the password.
- Hard-coded secrets are not secret once an attacker can read the source.

## Follow-Up

- Later vault-door challenges usually hide the password less directly.
  Keep starting from `checkPassword`, then work backward from whatever
  transformation it applies.
