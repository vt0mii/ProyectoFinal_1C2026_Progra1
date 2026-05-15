import json
import os

user_cache = (0, {})


def load_file(filename):
    try:
        with open(f"./{filename}", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, OSError) as e:
        print("Ha ocurrido un error: ", e)
        return None


def save_file(filename, data):
    try:
        with open(f"./{filename}", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except (FileNotFoundError, OSError) as e:
        print("Ha ocurrido un error: ", e)


static = load_file("static.json")

static = load_file("static.json") or {}
units = static.get("units", [])
meal_types = static.get("meal_types", [])
days = static.get("days", [])

users = load_file("users.json") or []
recipes = load_file("recipes.json") or []
ingredients = load_file("ingredients.json") or []
recipe_ingredients = load_file("recipe_ingredients.json") or []
recipe_plan = load_file("recipe_plan.json") or []
