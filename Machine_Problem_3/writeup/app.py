import secrets
import sqlite3
import hashlib
from bleach import clean
from flask import Flask, request, render_template, redirect, session, abort

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
con = sqlite3.connect("app.db", check_same_thread=False)

def input_validation(data):
    for elem in data:
        if elem == "session_token":
            val = request.cookies.get(elem)
            if ' ' in val or '--' in val or len(val) == 0:
                return False
        elif elem != "message":
            val = request.form[elem]
            if ' ' in val or len(val) == 0:
                return False
    return True

def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = hashlib.sha256(secrets.token_bytes(32)).hexdigest()
    return session['csrf_token']

@app.route("/login", methods=["GET", "POST"])
def login():
    cur = con.cursor()
    if request.method == "GET":
        if request.cookies.get("session_token"):
            res = cur.execute("SELECT username FROM users INNER JOIN sessions ON users.id = sessions.user WHERE sessions.token = ?;",
                              (request.cookies.get("session_token"),))
            user = res.fetchone()
            if user:
                return redirect("/home")

        return render_template("login.html")
    else:
        if input_validation(["username", "password"]):
            res = cur.execute("SELECT id from users WHERE username = ? AND password = ?;",
                              (request.form["username"], request.form["password"]))
            user = res.fetchone()
            if user:
                token = secrets.token_hex()
                cur.execute("INSERT INTO sessions (user, token) VALUES (?, ?);",
                            (str(user[0]), token))
                con.commit()
                response = redirect("/home")
                response.set_cookie("session_token", token)
                return response
        else:
            return render_template("login.html", error="Invalid username and/or password!")

@app.route("/")
@app.route("/home")
def home():
    cur = con.cursor()
    if request.cookies.get("session_token") and input_validation(["session_token"]):
        res = cur.execute("SELECT users.id, username FROM users INNER JOIN sessions ON users.id = sessions.user WHERE sessions.token = ?;",
                          (request.cookies.get("session_token"),))
        user = res.fetchone()
        if user:
            res = cur.execute("SELECT message FROM posts WHERE user = ?;", (str(user[0])))
            posts = res.fetchall()
            return render_template("home.html", username=user[1], posts=posts, csrf_token=generate_csrf_token())

    return redirect("/login")


@app.route("/posts", methods=["POST"])
def posts():
    cur = con.cursor()
    if request.cookies.get("session_token") and input_validation(["session_token"]):
        res = cur.execute("SELECT users.id, username FROM users INNER JOIN sessions ON users.id = sessions.user WHERE sessions.token = ?;",
                          (request.cookies.get("session_token"),))
        user = res.fetchone()
        if user:
            if request.form.get('csrf_token') != session.pop('csrf_token', None):
                abort(403)

            sanitized_input = clean(request.form["message"], tags=[], attributes={})
            cur.execute("INSERT INTO posts (message, user) VALUES (?,?);",
                        (sanitized_input, str(user[0])))
            con.commit()
            return redirect("/home")

    return redirect("/login")


@app.route("/logout", methods=["GET"])
def logout():
    cur = con.cursor()
    if request.cookies.get("session_token") and input_validation(["session_token"]):
        res = cur.execute("SELECT users.id, username FROM users INNER JOIN sessions ON "
                          "users.id = sessions.user WHERE sessions.token = ?;",
                          (request.cookies.get("session_token"),))
        user = res.fetchone()
        if user:
            cur.execute("DELETE FROM sessions WHERE user = ?", (str(user[0])))
            con.commit()

    response = redirect("/login")
    response.set_cookie("session_token", "", expires=0)

    return response
