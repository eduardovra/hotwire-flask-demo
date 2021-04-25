from collections import defaultdict
from typing import DefaultDict
from flask import Flask, render_template, request
from turbo_flask import Turbo

from ingredients import INGREDIENTS

app = Flask(__name__)
turbo = Turbo(app)

recipe: DefaultDict[str, int] = defaultdict(int)

@app.route("/")
def index():
    return render_template("index.html", recipe=recipe)

@app.route("/add/<ingredient>")
def add(ingredient):
    recipe[ingredient] += 1

    html = render_template('_recipe.html', recipe=recipe)

    return turbo.stream([
        turbo.replace(html, target='recipe'),
    ])

@app.route("/exclude/<ingredient>")
def exclude(ingredient):
    del recipe[ingredient]

    return render_template('_recipe.html', recipe=recipe)

@app.route("/search")
def search():
    q = request.args.get("q")

    ingredients = [
        {
            "name": ingredient,
            "strong": ingredient[:len(q)],
            "non_strong": ingredient[len(q):],
        }
        for ingredient in INGREDIENTS
        if q and ingredient.lower().startswith(q.lower())
    ]

    return render_template('_search.html', ingredients=ingredients)
