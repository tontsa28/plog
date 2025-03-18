from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index() -> str:
    return render_template("index.html")

@app.route("/page/<int:id>")
def page(id: int) -> str:
    return f"Welcome to page {id}"