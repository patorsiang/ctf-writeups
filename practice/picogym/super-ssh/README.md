# picoCTF - Super SSH

## Challenge

Connect to the picoCTF server over SSH and retrieve the flag printed after login.

## Given

- Host: `titan.picoctf.net`
- Port: `61484`
- Username: `ctf-player`
- Password: `6abf4a82`

## Solution

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

## Notes

SSH normally connects on port `22`. In this challenge, the service is exposed on
port `61484`, so omitting `-p 61484` would try the wrong port.
