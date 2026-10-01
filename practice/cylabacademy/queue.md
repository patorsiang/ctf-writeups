# CyLab Academy Queue

Use this file as the lightweight inbox for new learning challenges.

## Active

| Learning Path | Challenge | Category | Status | Next Step |
| --- | --- | --- | --- | --- |

## Backlog

| Learning Path | Challenge | Category | Why Save It |
| --- | --- | --- | --- |
|  |  |  |  |

## Re-solve

If I needed hints or a solve path, it isn't a skill yet. Add it here, and
about 7 days after the solve redo it cold: no notes, no
writeup, no AI, timer running. Record the result here and in the writeup's
`Re-solve` line. A failed re-solve goes back in the queue for another 7 days.

| Due | Challenge | Link | Result |
| --- | --- | --- | --- |
| 2026-10-08 | LA CTF 2025 Bigram Times | [writeup](../../events/2025/la-ctf/crypto/bigram-times/README.md) | |
| 2026-10-08 | LA CTF 2025 Crypto Civilization | [writeup](../../events/2025/la-ctf/crypto/crypto-civilization/README.md) | |
| 2026-10-08 | picoGym EVEN RSA CAN BE BROKEN??? | [writeup](../picogym/even-rsa-can-be-broken/README.md) | |
| 2026-10-08 | picoGym Mini RSA | [writeup](../picogym/mini-rsa/README.md) | |

## Done Recently

| Date | Learning Path | Challenge | Link | Lesson |
| --- | --- | --- | --- | --- |
| 2026-10-01 | AI Foundations I - The Lost Book of Perceptrons | perceptron-train-classic-1 | [writeup](challenges/ai-foundations-i-the-lost-book-of-perceptrons/perceptron-train-classic-1/README.md) | Same gentle data as Classic 0: every rate from 0.02 to 0.07 reached 100% in 16 updates; the upper limit is still untested. |
| 2026-10-01 | AI Foundations I - The Lost Book of Perceptrons | perceptron-train-classic-0 | [writeup](challenges/ai-foundations-i-the-lost-book-of-perceptrons/perceptron-train-classic-0/README.md) | Gentle data: the default rate 0.02 reached 100% in 16 updates because the starting line was already close. |
| 2026-09-27 | AI Foundations I - The Lost Book of Perceptrons | perceptron-play-naught | [writeup](challenges/ai-foundations-i-the-lost-book-of-perceptrons/perceptron-play-naught/README.md) | Ignore irrelevant x by setting `w1 = 0`; use y to separate the classes with boundary `y = 0`. |
| 2026-09-27 | AI Foundations I - The Lost Book of Perceptrons | perceptron-play-2d-alpha | [writeup](challenges/ai-foundations-i-the-lost-book-of-perceptrons/perceptron-play-2d-alpha/README.md) | Set both weights positive so the line `x + y = 0` separates the two classes. |
| 2026-09-20 | AI Foundations I - The Lost Book of Perceptrons | perceptron-play-1d-alpha | [writeup](challenges/ai-foundations-i-the-lost-book-of-perceptrons/perceptron-play-1d-alpha/README.md) | Use one controlled bias change to move the threshold between the nearest opposite labels. |
| 2026-08-01 | The Beginner's Guide to the Challenge Library | obedient-cat | [writeup](challenges/beginners-guide-to-the-challenge-library/obedient-cat/README.md) | Use `cat` to inspect a simple text file. |
| 2026-08-01 | The Beginner's Guide to the Challenge Library | super-ssh | [writeup](challenges/beginners-guide-to-the-challenge-library/super-ssh/README.md) | Use `ssh -p` when the service runs on a non-default port. |
| 2026-08-01 | The Beginner's Guide to the Challenge Library | whats-a-net-cat | [writeup](challenges/beginners-guide-to-the-challenge-library/whats-a-net-cat/README.md) | Use `nc <host> <port>` to connect to a raw TCP service. |
| 2026-08-04 | The Beginner's Guide to the Challenge Library | mod-26 | [writeup](challenges/beginners-guide-to-the-challenge-library/mod-26/README.md) | Read the Caesar shift off a known crib; ROT13 is its own inverse. |
| 2026-08-04 | The Beginner's Guide to the Challenge Library | warmed-up | [writeup](challenges/beginners-guide-to-the-challenge-library/warmed-up/README.md) | `0x` is a prefix, not a digit; one byte is exactly 2 hex digits. |
| 2026-08-04 | The Beginner's Guide to the Challenge Library | 2warm | [writeup](challenges/beginners-guide-to-the-challenge-library/2warm/README.md) | Repeated division gives remainders bottom-up; 3 bits = 1 octal digit. |
| 2026-08-04 | The Beginner's Guide to the Challenge Library | bases | [writeup](challenges/beginners-guide-to-the-challenge-library/bases/README.md) | Base64 is a transport encoding, not a number base; 6 bits = 1 char. |
| 2026-08-05 | The Beginner's Guide to the Challenge Library | wave-a-flag | [writeup](challenges/beginners-guide-to-the-challenge-library/wave-a-flag/README.md) | `exec format error` = wrong OS/CPU; `docker --platform` runs it anyway. |
| 2026-08-05 | The Beginner's Guide to the Challenge Library | tab-tab-attack | [writeup](challenges/beginners-guide-to-the-challenge-library/tab-tab-attack/README.md) | Tab completes interactively, globs expand at exec; check zips before extracting. |
| 2026-08-09 | The Beginner's Guide to the Challenge Library | insp3ct0r | [writeup](challenges/beginners-guide-to-the-challenge-library/insp3ct0r/README.md) | Client-side source is public; enumerate assets, not just the page. |
| 2026-08-09 | The Beginner's Guide to the Challenge Library | strings-it | [writeup](challenges/beginners-guide-to-the-challenge-library/strings-it/README.md) | Static analysis needs no matching OS/CPU; empty `strings` output may mean UTF-16. |
| 2026-08-12 | The Beginner's Guide to the Challenge Library | first-grep | [writeup](challenges/beginners-guide-to-the-challenge-library/first-grep/README.md) | `grep -o 'picoCTF{[^}]*}' file` extracts only the flag from noisy text. |
| 2026-08-12 | The Beginner's Guide to the Challenge Library | where-are-the-robots | [writeup](challenges/beginners-guide-to-the-challenge-library/where-are-the-robots/README.md) | `robots.txt` is public crawler guidance, not access control. |
| 2026-08-13 | The Beginner's Guide to the Challenge Library | python-wrangling | [writeup](challenges/beginners-guide-to-the-challenge-library/python-wrangling/README.md) | Use a local virtualenv for challenge dependencies, then pass the password file to the decrypt script. |
| 2026-08-14 | The Beginner's Guide to the Challenge Library | pw-crack-1 | [writeup](challenges/beginners-guide-to-the-challenge-library/pw-crack-1/README.md) | Read the password check first; a hard-coded comparison reveals the expected input. |
| 2026-08-14 | The Beginner's Guide to the Challenge Library | pw-crack-2 | [writeup](challenges/beginners-guide-to-the-challenge-library/pw-crack-2/README.md) | Decode `chr(0x...)` expressions to recover characters from code points. |
| 2026-08-15 | The Beginner's Guide to the Challenge Library | pw-crack-3 | [writeup](challenges/beginners-guide-to-the-challenge-library/pw-crack-3/README.md) | Hash each candidate the same way the checker does, then compare digest bytes. |
| 2026-08-15 | The Beginner's Guide to the Challenge Library | pw-crack-4 | [writeup](challenges/beginners-guide-to-the-challenge-library/pw-crack-4/README.md) | Automate longer candidate lists by parsing the source list and hashing each candidate. |
| 2026-08-15 | The Beginner's Guide to the Challenge Library | pw-crack-5 | [writeup](challenges/beginners-guide-to-the-challenge-library/pw-crack-5/README.md) | Use a dictionary attack: hash each file candidate and compare it to the stored digest. |
| 2026-08-16 | The Beginner's Guide to the Challenge Library | enhance | [writeup](challenges/beginners-guide-to-the-challenge-library/enhance/README.md) | SVG is XML source; tiny hidden text can be easier to read in markup than in the rendered image. |
| 2026-08-16 | The Beginner's Guide to the Challenge Library | big-zip | [writeup](challenges/beginners-guide-to-the-challenge-library/big-zip/README.md) | Use recursive search for large extracted file trees instead of opening files one by one. |
| 2026-08-16 | The Beginner's Guide to the Challenge Library | vault-door-training | [writeup](challenges/beginners-guide-to-the-challenge-library/vault-door-training/README.md) | Read the validation function first; a hard-coded `equals` string reveals the inner password. |
| 2026-08-17 | The Beginner's Guide to the Challenge Library | keygenme-py | [writeup](challenges/beginners-guide-to-the-challenge-library/keygenme-py/README.md) | Read the license checker first; hash the known username and select the indexed digest characters. |
| 2026-08-17 | The Beginner's Guide to the Challenge Library | buffer-overflow-0 | [writeup](challenges/beginners-guide-to-the-challenge-library/buffer-overflow-0/README.md) | Overflowing the small `strcpy` destination triggers the custom SIGSEGV handler that prints the flag. |
| 2026-08-22 | AI Foundations I - The Lost Book of Perceptrons | neuron-meet-0 | [writeup](challenges/ai-foundations-i-the-lost-book-of-perceptrons/neuron-meet-0/README.md) | Use binary search to find a perceptron decision boundary, then choose distinct same-side inputs for repeated output bits. |
| 2026-08-25 | AI Foundations I - The Lost Book of Perceptrons | neuron-meet-2d-0 | [writeup](challenges/ai-foundations-i-the-lost-book-of-perceptrons/neuron-meet-2d-0/README.md) | Probe 2D corner points to find safe firing and quiet regions, then use distinct pairs to spell `01110000`. |
| 2026-09-08 | AI Foundations I - The Lost Book of Perceptrons | neuron-express-0 | [writeup](challenges/ai-foundations-i-the-lost-book-of-perceptrons/neuron-express-0/README.md) | Use midpoint probes to find the integer transition, then derive a simple weight and bias that reproduce the threshold. |

## Parking Lot

Use this section for challenges that look interesting but are not worth starting yet.

-
