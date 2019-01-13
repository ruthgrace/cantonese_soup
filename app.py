import json

from flask import Flask, render_template, request

CURES_FILE = "cures.json"
RECIPE_FILE = "recipes.json"
INGREDIENTS_FILE = "ingredients.json"

def load_from_file(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def load_recipes_per_ingredient(recipes, ingredients):
    recipes_per_ingredient = {}
    for recipe in recipes:
        for ingredient in recipes[recipe]["ingredients"]:
            if ingredient not in recipes_per_ingredient:
                recipes_per_ingredient[ingredient] = set()
            if recipe not in recipes_per_ingredient[ingredient]:
                recipes_per_ingredient[ingredient].add(recipe)
    return recipes_per_ingredient

CURES = load_from_file(CURES_FILE)
RECIPES = load_from_file(RECIPE_FILE)
INGREDIENTS = load_from_file(INGREDIENTS_FILE)
RECIPES_PER_INGREDIENT = load_recipes_per_ingredient(RECIPES, INGREDIENTS)
ENGLISH = "english"
CHINESE = "chinese"

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
    return render_template('ingredients.html', ingredients=INGREDIENTS, recipes=RECIPES_PER_INGREDIENT)

@app.route("/ailments")
def ailments():
    return render_template('ailments.html', cures=CURES)

@app.route("/recipe/<recipe_name>")
def recipe(recipe_name):
    language = request.args.get('language', ENGLISH)
    language = language.lower()
    return render_template("recipe.html", recipe=get_recipe(recipe_name), ingredients=INGREDIENTS, language=language, english=ENGLISH, chinese=CHINESE, recipe_name=recipe_name)

@app.route("/ailment/<ailment_name>")
def ailment(ailment_name):
    return redirect('recipe/' + get_recipe_for_ailment(ailment_name), code=302)

@app.route("/recipeindex")
def recipe_index():
    return render_template('recipeindex.html', recipes=RECIPES.keys())
