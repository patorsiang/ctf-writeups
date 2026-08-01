# picoCTF - what's a net cat?

## Challenge

Connect to the remote picoCTF service with `nc` and read the flag returned by
the server.

## Given

- Host: `fickle-tempest.picoctf.net`
- Port: `64689`

## Solution

The challenge provides a hostname and port. Use `nc`, also known as Netcat, to
open a TCP connection to that service:

```bash
nc fickle-tempest.picoctf.net 64689
```

The server responds with a short message and the flag:

```text
You're on your way to becoming the net cat master
picoCTF{nEtCat_Mast3ry_95035DAa}
```

## Flag

```text
picoCTF{nEtCat_Mast3ry_95035DAa}
```

## Notes

`nc` is useful in CTFs because it lets you connect directly to services running
on specific ports. The basic syntax is:

```bash
nc <host> <port>
```
