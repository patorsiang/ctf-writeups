# Bandit

## Installation

```bash
brew install sshpass
sshpass -p<pwd> ssh <user>@bandit.labs.overthewire.org -p 2220
```

## Level 0 → Level 1

```bash
sshpass -pbandit0 ssh bandit0@bandit.labs.overthewire.org -p 2220
ls -al
cat readme
exit
```

pwd: `ZjLjTmM6FvvyRnrb2rfNWOZOTa6ip5If`

## Level 1 → Level 2

Note: Google Search for “dashed filename”

```bash
sshpass -pZjLjTmM6FvvyRnrb2rfNWOZOTa6ip5If ssh bandit1@bandit.labs.overthewire.org -p 2220
ls -al
cat ./-
exit
```

pwd: `263JGJPfgU6LtdEvgfWU1XP5yac29mFx`

## Level 2 → Level 3

Note: Google Search for “spaces in filename”

```bash
sshpass -p263JGJPfgU6LtdEvgfWU1XP5yac29mFx ssh bandit2@bandit.labs.overthewire.org -p 2220
ls -al
cat "spaces in this filename"
exit
```

pwd: `MNk8KNH3Usiio41PRUEoDFPqfxLPlSmx`

## Level 3 → Level 4

```bash
sshpass -pMNk8KNH3Usiio41PRUEoDFPqfxLPlSmx ssh bandit3@bandit.labs.overthewire.org -p 2220
ls -al
cd inhere
ls -al
cat "...Hiding-From-You"
exit
```

pwd: `2WmrDFRmJIq3IPxneAaMGhap0pFhF3NJ`

## Level 4 → Level 5

```bash
sshpass -p2WmrDFRmJIq3IPxneAaMGhap0pFhF3NJ ssh bandit4@bandit.labs.overthewire.org -p 2220
ls -al
cd inhere
ls -al
file ./* # find only human-readable file
cat ./-file07
exit
```

pwd: `4oQYVPkxZOOEOO5pTW81FB8j8lxXGUQw`

## Level 5 → Level 6

```bash
sshpass -p4oQYVPkxZOOEOO5pTW81FB8j8lxXGUQw ssh bandit5@bandit.labs.overthewire.org -p 2220
find . -type f -size 1033c ! -executable
"""
human-readable
1033 bytes in size
not executable
"""
cat ./inhere/maybehere07/.file2
exit
```

pwd: `HWasnPhtq9AVKe0dmk45nxy20cvUa6EG`

## Level 6 → Level 7

```bash
sshpass -pHWasnPhtq9AVKe0dmk45nxy20cvUa6EG ssh bandit6@bandit.labs.overthewire.org -p 2220
find / -user bandit7 -group bandit6 -size 33c 2>/dev/null
cat /var/lib/dpkg/info/bandit7.password
exit
```

**description:**

```bash
find / -user bandit7 -group bandit6 -size 33c 2>/dev/null
```

`/` → search from the root directory

`-user bandit7` → owned by user bandit7

`-group bandit6` → group bandit6

`-size 33c` → exactly 33 bytes (c means bytes)

`2>/dev/null` → hide permission denied errors (makes output cleaner)

pwd: `morbNTDkSW6jIlUc0ymOdMaLnOlFVAaj`

## Level 7 → Level 8

```bash
sshpass -pmorbNTDkSW6jIlUc0ymOdMaLnOlFVAaj ssh bandit7@bandit.labs.overthewire.org -p 2220
ls -al
grep millionth data.txt # the word next to millionth
exit
```

pwd: `dfwvzFQi4mU0wfNbFOe9RoWskMLg7eEc`

## Level 8 → Level 9

```bash
sshpass -pdfwvzFQi4mU0wfNbFOe9RoWskMLg7eEc ssh bandit8@bandit.labs.overthewire.org -p 2220
sort data.txt | uniq -u
exit
```

- `sort data.txt`: sorts the file so duplicate lines are next to each other.
- `uniq -u`: filters out lines that appear more than once, printing only lines that appear once.

pwd: `4CKMh1JI91bUIZZPXDqGanal4xvAg0JM`

## Level 9 → Level 10

```bash
sshpass -p4CKMh1JI91bUIZZPXDqGanal4xvAg0JM ssh bandit9@bandit.labs.overthewire.org -p 2220
strings data.txt | grep -E '=+.*[a-zA-Z0-9]'
exit
```

pwd: `FGUW5ilLVJrxX9kMYMmlN4MgbpfMiqey`

## Level 10 → Level 11

```bash
sshpass -pFGUW5ilLVJrxX9kMYMmlN4MgbpfMiqey ssh bandit10@bandit.labs.overthewire.org -p 2220
base64 -d data.txt
exit
```

pwd: `dtR173fZKb0RRsDFSGsg2RWnpNVj3qRr`

## Level 11 → Level 12

```bash
sshpass -pdtR173fZKb0RRsDFSGsg2RWnpNVj3qRr ssh bandit11@bandit.labs.overthewire.org -p 2220
tr 'A-Za-z' 'N-ZA-Mn-za-m' < data.txt
exit
```

pwd: `7x16WNeHIi5YkIhWsfFIqoognUTyj9Q4`

## Level 12 → Level 13

```bash
#  Login to Level 12
sshpass -p7x16WNeHIi5YkIhWsfFIqoognUTyj9Q4 ssh bandit12@bandit.labs.overthewire.org -p 2220

# Create a temporary work directory
cd /tmp
workdir=$(mktemp -d)
cd "$workdir"

# Copy and rename the file
cp ~/data.txt .
mv data.txt data.hex

# Convert hex back to binary
xxd -r data.hex data.bin

# Repeatedly decompress
file data.bin
mv <> <> && <>

exit
```

| File Type | Command                                    |
| --------- | ------------------------------------------ |
| gzip      | `mv data.bin data.gz && gunzip data.gz`    |
| bzip2     | `mv data.bin data.bz2 && bunzip2 data.bz2` |
| POSIX tar | `mv data.bin data.tar && tar -xf data.tar` |
| ASCII     | `cat <filename>` or `strings <filename>`   |

pwd: `FO5dwFsc0cbaIiH0h8J2eUks2vdTDwAn`

## Level 13 -> Level 14

```bash
sshpass -pFO5dwFsc0cbaIiH0h8J2eUks2vdTDwAn ssh bandit13@bandit.labs.overthewire.org -p 2220
ls
ssh -i sshkey.private bandit14@localhost -p 2220ls
cat /etc/bandit_pass/bandit14
exit
```

pwd: `MU4VWeTyJk8ROof1qqmcBPaLh7lDCPvS`

## Level 14 -> Level 15

```bash
sshpass -pMU4VWeTyJk8ROof1qqmcBPaLh7lDCPvS ssh bandit14@bandit.labs.overthewire.org -p 2220
cat /etc/bandit_pass/bandit14 | nc localhost 30000
exit
```

pwd: `8xCjnmgoKbGLhHFAZlGE5Tmu4M2tKJQo`

## Level 15 -> Level 16

```bash
sshpass -p8xCjnmgoKbGLhHFAZlGE5Tmu4M2tKJQo ssh bandit15@bandit.labs.overthewire.org -p 2220
cat /etc/bandit_pass/bandit15 # 8xCjnmgoKbGLhHFAZlGE5Tmu4M2tKJQo
openssl s_client -connect localhost:30001
8xCjnmgoKbGLhHFAZlGE5Tmu4M2tKJQo
exit
```

pwd: `kSkvUpMQ7lBYyCM4GBPvCvT1BfWRy0Dx`

## Level 16 -> Level 17

```bash
sshpass -pkSkvUpMQ7lBYyCM4GBPvCvT1BfWRy0Dx ssh bandit16@bandit.labs.overthewire.org -p 2220
cat /etc/bandit_pass/bandit16 # kSkvUpMQ7lBYyCM4GBPvCvT1BfWRy0Dx
nmap -p31000-32000 localhost

"""
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-06-07 14:16 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00018s latency).
Not shown: 996 closed tcp ports (conn-refused)
PORT      STATE SERVICE
31046/tcp open  unknown
31518/tcp open  unknown
31691/tcp open  unknown
31790/tcp open  unknown
31960/tcp open  unknown
"""

openssl s_client -connect localhost:31046 # no client
openssl s_client -connect localhost:31518
openssl s_client -connect localhost:31691 # no client
openssl s_client -connect localhost:31790
openssl s_client -connect localhost:31960 # no client

PASS=$(cat /etc/bandit_pass/bandit16)

for port in 31046 31518 31691 31790 31960; do
  echo "Testing port $port..."
  echo "$PASS" | timeout 10 openssl s_client -connect localhost:$port
  echo -e "\n======\n"
done

# or

cat /tmp/bandit17.key
```

pwd: `bandit17.key`

## Level 17 -> Level 18

```bash
code bandit17.key
chmod 600 bandit17.key
ssh -i bandit17.key bandit17@bandit.labs.overthewire.org -p 2220
ls
diff passwords.old passwords.new
exit
```

pwd: `x2gLTTjFwMOhQ8oWNbMN362QKxfRqGlO`

## Level 18 -> Level 19

```bash
sshpass -px2gLTTjFwMOhQ8oWNbMN362QKxfRqGlO ssh bandit18@bandit.labs.overthewire.org -p 2220 'cat readme'
```

pwd: `cGWpMaKXVwDUNgPAVJbWYuGHVn9zl3j8`

## Level 19 -> Level 20

```bash
sshpass -pcGWpMaKXVwDUNgPAVJbWYuGHVn9zl3j8 ssh bandit19@bandit.labs.overthewire.org -p 2220
ls
./bandit20-do cat /etc/bandit_pass/bandit20
```

pwd: `0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO`

## Level 20 -> Level 21

```bash
sshpass -p0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO ssh bandit20@bandit.labs.overthewire.org -p 2220
ls
tmux splitw -h
nc -l 12345
`crtl b ->`
./suconnect 12345
`crtl b <-`
0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO
exit
```

pwd: `EeoULMCra2q0dSkYj561DX7s1CpBuOBt`

## Level 21 -> Level 22

```bash
sshpass -pEeoULMCra2q0dSkYj561DX7s1CpBuOBt ssh bandit21@bandit.labs.overthewire.org -p 2220
ls /etc/cron.d/
cat /etc/cron.d/cronjob_bandit22
cat /usr/bin/cronjob_bandit22.sh
cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fg
exit
```

pwd: `tRae0UfB9v0UzbCdn9cY0gQnds9GF58Q`

## Level 22 -> Level 23

```bash
sshpass -ptRae0UfB9v0UzbCdn9cY0gQnds9GF58Q ssh bandit22@bandit.labs.overthewire.org -p 2220
ls /etc/cron.d/
cat /etc/cron.d/cronjob_bandit23
cat /usr/bin/cronjob_bandit23.sh
echo I am user $(whoami) | md5sum | cut -d ' ' -f 1
cat /tmp/8ca319486bfbbc3663ea0fbe81326349
```

pwd: `0Zf11ioIjMVN551jX3CmStKLYqjk54Ga`

## Level 23 -> Level 24

```bash
sshpass -p0Zf11ioIjMVN551jX3CmStKLYqjk54Ga ssh bandit23@bandit.labs.overthewire.org -p 2220
ls /etc/cron.d/
cat /etc/cron.d/cronjob_bandit24
cat /usr/bin/cronjob_bandit24.sh
cd /var/spool/bandit24/foo/
vi get_pass.sh
#!/bin/bash
cat /etc/bandit_pass/bandit24 > /tmp/pass_bandit24.txt
:wq!
chmod +x get_pass.sh
ls -l get_pass.sh
cat /tmp/pass_bandit24.txt
exit
```

pwd: `gb8KRRCsshuZXI0tUuR6ypOFjiZbf3G8`

## Level 24 -> Level 25

```bash
sshpass -pgb8KRRCsshuZXI0tUuR6ypOFjiZbf3G8 ssh bandit24@bandit.labs.overthewire.org -p 2220
for pin in $(seq -w 0000 9999); do echo "gb8KRRCsshuZXI0tUuR6ypOFjiZbf3G8 $pin"; done | nc localhost 30002
exit
```

pwd: `iCi86ttT4KSNe1armKiwbQNmB3YJP3q4`
