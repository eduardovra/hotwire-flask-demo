from flask import Flask, render_template, redirect, url_for, request
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)

@app.route("/", methods=["GET",])
def index():
    ingredients = []
    return render_template("index.html", ingredients=ingredients)
