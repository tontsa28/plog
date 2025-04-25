import secrets
import sqlite3
import importlib

from flask import Flask, flash, redirect, render_template, request, session, abort
from werkzeug.wrappers.response import Response

import users
import items

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
    all_items = items.get_items()
    all_likes = items.get_all_likes()
    return render_template("index.html", items=all_items, likes=all_likes)

@app.route("/login", methods=["GET", "POST"])
def login() -> Response | str:
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
def register() -> Response | str:
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
def logout() -> Response:
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

@app.route("/new_item", methods=["GET", "POST"])
def new_item() -> Response | str:
    require_login()

    if request.method == "POST":
        check_csrf()

        manufacturer = request.form["manufacturer"]
        if not manufacturer or len(manufacturer) > 30:
            abort(403)
        model = request.form["model"]
        if not model or len(model) > 20:
            abort(403)
        registration = request.form["registration"]
        if not registration or len(registration) > 10:
            abort(403)
        category = request.form["category"]
        if not category or len(category) > 20:
            abort(403)
        airline = request.form["airline"]
        if not airline or len(airline) > 30:
            abort(403)
        try:
            times_onboard = int(request.form["times_onboard"])
        except ValueError:
            times_onboard = 0
        try:
            times_seen = int(request.form["times_seen"])
        except ValueError:
            times_seen = 0
        user_id = session["user_id"]

        items.add_item(user_id, manufacturer, model, registration, category, airline, times_onboard, times_seen)

        return redirect("/")
    else:
        manufacturers = items.get_all_manufacturers()
        categories = items.get_all_categories()
        return render_template("new_item.html", manufacturers=manufacturers, categories=categories)

@app.route("/item/<int:item_id>")
def show_item(item_id: int) -> str:
    item = items.get_item(item_id)
    if not item:
        abort(404)
    likes = items.get_likes(item_id)

    return render_template("show_item.html", item=item, likes=likes)

@app.route("/item/<int:item_id>/remove", methods=["GET", "POST"])
def remove_item(item_id: int) -> Response | str:
    require_login()

    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect(f"/item/{item_id}")
    else:
        return render_template("remove_item.html", item=item)

@app.route("/item/<int:item_id>/edit", methods=["GET", "POST"])
def edit_item(item_id: int) -> Response | str:
    require_login()

    if request.method == "POST":
        check_csrf()

        item_id = int(request.form["item_id"])
        item = items.get_item(item_id)
        if not item:
            abort(404)
        if item["user_id"] != session["user_id"]:
            abort(403)

        manufacturer = request.form["manufacturer"]
        if not manufacturer or len(manufacturer) > 30:
            abort(403)
        model = request.form["model"]
        if not model or len(model) > 20:
            abort(403)
        registration = request.form["registration"]
        if not registration or len(registration) > 10:
            abort(403)
        category = request.form["category"]
        if not category or len(category) > 20:
            abort(403)
        airline = request.form["airline"]
        if not airline or len(airline) > 30:
            abort(403)
        try:
            times_onboard = int(request.form["times_onboard"])
        except ValueError:
            times_onboard = 0
        try:
            times_seen = int(request.form["times_seen"])
        except ValueError:
            times_seen = 0

        items.update_item(item_id, manufacturer, model, registration, category, airline, times_onboard, times_seen)

        return redirect(f"/item/{item_id}")
    else:
        item = items.get_item(item_id)
        if not item:
            abort(404)
        if item["user_id"] != session["user_id"]:
            abort(403)

        manufacturers = items.get_all_manufacturers()
        categories = items.get_all_categories()

        return render_template("edit_item.html", item=item, manufacturers=manufacturers, categories=categories)

@app.route("/item/<int:item_id>/like", methods=["POST"])
def like_item(item_id: int) -> Response:
    require_login()
    check_csrf()

    user_id = session["user_id"]
    if items.has_liked(item_id, user_id):
        items.remove_like(item_id, user_id)
    else:
        items.add_like(item_id, user_id)

    if request.form["source"] == "index":
        return redirect("/")
    return redirect(f"/item/{item_id}")

@app.route("/search")
def search_item() -> str:
    query = request.args.get("query")
    if query:
        results = items.search_items(query)
    else:
        query = ""
        results = []
    return render_template("search_item.html", query=query, results=results)

@app.route("/user/<int:user_id>")
def show_user(user_id) -> str:
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_items = users.get_items(user_id)
    return render_template("show_user.html", user=user, items=user_items)