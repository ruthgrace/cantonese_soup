import json

from flask import Flask, render_template

CURES_FILE = "cures.json"
RECIPE_FILE = "recipes.json"
INGREDIENTS_FILE = "ingredients.json"

def load_from_file(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

CURES = load_from_file(CURES_FILE)
RECIPES = load_from_file(RECIPE_FILE)
INGREDIENTS = load_from_file(INGREDIENTS_FILE)

app = Flask(__name__)

def get_recipe(recipe_name):
    return RECIPES[recipe_name]

def get_recipe_for_ailment(ailment):
    return CURES[ailment]

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/ingredients")
def ingredients():
    return render_template('ingredients.html')

@app.route("/ailments")
def ailments():
    return render_template('ailments.html')

@app.route("/recipe/<recipe_name>")
def recipe(recipe_name):
    return render_template("recipe.html", recipe=get_recipe(recipe_name))

@app.route("/ailment/<ailment_name>")
def ailment(ailment_name):
    return redirect('recipe/' + get_recipe_for_ailment(ailment_name), code=302)

@app.route("/recipeindex")
def recipe_index():
    return render_template('recipeindex.html', recipes=RECIPES.keys())
