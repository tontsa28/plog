import secrets
import sqlite3
import importlib

from flask import Flask, flash, redirect, render_template, request, session, abort

import users

app = Flask(__name__)

# Import the secret key and if it's invalid or not present, create it automatically
try:
    import config
    if len(config.secret_key) < 128:
        raise AttributeError
    app.secret_key = config.secret_key
except ModuleNotFoundError:
    with open("config.py", "w", encoding="UTF-8") as file:
        file.write(f"secret_key = '{secrets.token_hex(64)}'")

    import config
    app.secret_key = config.secret_key
except AttributeError:
    import os
    os.remove("config.py")

    with open("config.py", "w", encoding="UTF-8") as file:
        file.write(f"secret_key = '{secrets.token_hex(64)}'")

    import config
    importlib.reload(config)
    app.secret_key = config.secret_key

def require_login() -> None:
    if "user_id" not in session:
        abort(403)

def check_csrf() -> None:
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index() -> str:
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("ERROR: invalid username or password")
            return redirect("/login")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            flash("ERROR: salasanat eivät täsmää")
            return redirect("/register")
        
        try:
            users.register_user(username, password1)
        except sqlite3.IntegrityError:
            flash("ERROR: tunnus on jo varattu")
            return redirect("/register")

        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")