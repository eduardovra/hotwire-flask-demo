from collections import defaultdict
from typing import DefaultDict
from flask import Flask, render_template, request
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)

INGREDIENTS = ["avocado","apple","allspice","almonds","aspargus","aubergine","arugula","ananas",
"butter", "bread", "beef", "baking soda", "bell peper", "basil", "brown sugar","broccoli","banana",
"cinnamon", "carrot", "chicken", "cream", "cheese","cauliflower",
"dijon", "dill", "dark chocolate", "dry mustard",
"egg", "entrecote", "egg yolk", "eggplant",
"flour", "fusilli", "farfalle",
"garlic", "ginger", "ground beef", "green pepper", "ground meat",
"honey", "heavy cream", "hot pepper sauce", "hot sauce",
"ice", "ice cream", "italian herbs",
"jalapeno", "jam",
"ketchup", "kale", "kiwi", "kosher salt",
"lemon", "lime", "light cream", "lettuce", "lentils", "leek",
"mayonnaise", "mustard", "meat", "milk", "mushrooms",
"nutmeg", "noodles", "nutella",
"olive oil", "onion", "olives", "oregano", "orange",
"pear", "peach", "parmesan", "potatoes", "pineapple",
"quinoa", "red lentils", "red pepper", "romaine lettuce",
"sugar", "sour cream", "soy sauce",
"tomatoes", "thyme", "tomato sauce","tuna",
"vegetable oil", "vanilla", "vodka", "vinegar", "vegetable broth",
"wheat", "walnut", "white wine", "whipped cream", "worcestershire sauce",
"yoghurt", "yeast", "zuchinni"]

INGREDIENTS = [ingredient.capitalize() for ingredient in INGREDIENTS]
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
        {"name": ingredient, "strong": ingredient[:len(q)], "non_strong": ingredient[len(q):]}
        for ingredient in INGREDIENTS
        if q and ingredient.lower().startswith(q.lower())
    ]

    return render_template('_autocomplete.html', ingredients=ingredients)
