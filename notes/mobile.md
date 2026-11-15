# Mobile Notes

## Triage playbook (easy, ≤1 page)

Fill from drills — each new line must cite the drill that taught it.

First look at an APK (tools checked by `tools/check_kit.sh`):

- `file app.apk`: confirm it's a zip/APK.
- `jadx -d out app.apk`: decompile it to Java source and resources.
- `apktool d app.apk -o out-apktool`: decode `AndroidManifest.xml` and the smali.
- Read `AndroidManifest.xml` first: exported activities, permissions, the main activity.
- `grep -rniE 'flag|secret|key|password|http' out/`: hardcoded strings and endpoints.
- Check `res/values/strings.xml` and `assets/` for stored data.

## Repo Examples
