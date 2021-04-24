from flask import Flask, render_template, redirect, url_for, request
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)

@app.route("/", methods=["GET",])
def index():
    return render_template("index.html")

@app.route("/signup", methods=["POST",])
def signup():
    data = request.form
    return redirect(url_for("index"))
