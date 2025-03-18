from flask import Flask
from flask import render_template, request, flash, redirect
import sqlite3

import users

app = Flask(__name__)

@app.route("/")
def index() -> str:
    return render_template("index.html")

@app.route("/login")
def login() -> str:
    return render_template("login.html")

@app.route("/register")
def register() -> str:
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        flash("ERROR: salasanat eivät täsmää")
        return redirect("/register")
    
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("ERROR: tunnus on jo varattu")
        return redirect("/register")

    return redirect("/")