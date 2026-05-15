import json
import os

user_cache = (0, {})


def load_file(filename):
    with open(f"./{filename}", encoding="utf-8") as f:
        return json.load(f)


static = load_file("static.json")
units = static["units"]
meal_types = static["meal_types"]
days = static["days"]

users = load_file("users.json")
recipes = load_file("recipes.json")
ingredients = load_file("ingredients.json")
recipe_ingredients = load_file("recipe_ingredients.json")
recipe_plan = load_file("recipe_plan.json")
