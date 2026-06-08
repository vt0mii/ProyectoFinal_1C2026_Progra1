from db.data import *
from components.validation import *
from functools import reduce

# CRUD Estatico


def get_unit_by_id(unit_id):
    for u in units:
        if u["id"] == unit_id:
            return u["name"]
    return None


def get_mealtype_by_id(mealtype_id):
    for m in meal_types:
        if m["id"] == mealtype_id:
            return m["name"]
    return None


def get_day_by_id(day_id):
    for d in days:
        if d["id"] == day_id:
            return d["name"]
    return None


def get_category_by_id(category_id):
    for c in categories:
        if c["id"] == category_id:
            return c["name"]
    return None

def get_categories():
    return list(map(lambda c: c["name"], categories))

def get_mealtype_list():
    return list(map(lambda mt: mt["name"], meal_types))


def get_days_list():
    return list(map(lambda day: day["name"], days))


def get_category_list():
    return list(map(lambda category: category["name"], categories))


# CRUD Recetas


def add_recipe(user_id, title, instructions, difficulty):
    if user_exists_id(user_id):
        newid = max((r["id"] for r in recipes), default=-1) + 1
        recipes.append(
            {
                "id": newid,
                "user_id": user_id,
                "title": title,
                "instructions": instructions,
                'difficulty': difficulty
            }
        )
        save_file("recipes.json", recipes)
        return True
    return False


def delete_recipe(user_id, recipe_id):
    if is_recipe_owner(user_id, recipe_id):
        target = get_recipe(recipe_id)
        if target is not None:
            orphan_ingredients = get_ingredientlist_from_recipe(recipe_id)
            for ri in orphan_ingredients:
                recipe_ingredients.remove(ri)
            save_file("recipe_ingredients.json", recipe_ingredients)

            for entry in recipe_plan:
                for day in entry["plan"]:
                    for mealtype in get_mealtype_list():
                        if recipe_id in day[mealtype]:
                            day[mealtype].remove(recipe_id)
            save_file("recipe_plan.json", recipe_plan)

            recipes.remove(target)
            save_file("recipes.json", recipes)
            return True
    return False


def update_recipe(user_id, recipe_id, title, instructions, difficulty):
    if is_recipe_owner(user_id, recipe_id):
        recipe = get_recipe(recipe_id)
        if recipe is not None:
            recipe["title"] = title
            recipe["instructions"] = instructions
            recipe['difficulty'] = difficulty
            save_file("recipes.json", recipes)
            return True
    return False


def get_recipe(recipe_id):
    results = list(filter(lambda r: r["id"] == recipe_id, recipes))
    return results[0] if results else None


def get_user_recipes(user_id):
    if user_exists_id(user_id):
        ing = [r for r in recipes if r["user_id"] == int(user_id)]
        return ing if ing else None
    return None


# CRUD Ingredientes


def add_ingredient(user_id, title, unit_id, category_id):
    if user_exists_id(user_id):
        newid = max((i["id"] for i in ingredients), default=-1) + 1
        ingredients.append(
            {
                "id": newid,
                "user_id": user_id,
                "name": title,
                "unit_id": unit_id,
                "category": category_id,
            }
        )
        save_file("ingredients.json", ingredients)
        return True
    return False


def delete_ingredient(user_id, ingredient_id):
    if is_ingredient_owner(user_id, ingredient_id):
        target = get_ingredient(ingredient_id)
        if target is not None:
            ingredients.remove(target)
            save_file("ingredients.json", ingredients)
            return True
    return False


def update_ingredient(user_id, ingredient_id, title, unit_id, category_id):
    if is_ingredient_owner(user_id, ingredient_id):
        ingredient = get_ingredient(ingredient_id)
        if ingredient is not None:
            ingredient["name"] = title
            ingredient["unit_id"] = unit_id
            ingredient["category"] = category_id
            save_file("ingredients.json", ingredients)
            return True
    return False


def get_ingredient(ingredient_id):
    results = list(filter(lambda i: i["id"] == ingredient_id, ingredients))
    return results[0] if results else None


def get_user_ingredients(user_id):
    if user_exists_id(user_id):
        ing = [i for i in ingredients if i["user_id"] == int(user_id)]
        return ing if ing else None
    return None


# CRUD Ingredientes en Recetas


def add_ingredient_to_recipe(user_id, recipe_id, ingredient_id, quantity):
    if is_ingredient_owner(user_id, ingredient_id) and is_recipe_owner(
        user_id, recipe_id
    ):
        newid = max((r["id"] for r in recipe_ingredients), default=-1) + 1
        recipe_ingredients.append(
            {
                "id": newid,
                "recipe_id": recipe_id,
                "ingredient_id": ingredient_id,
                "quantity": quantity,
            }
        )
        save_file("recipe_ingredients.json", recipe_ingredients)
        return True
    return False


def delete_ingredient_from_recipe(user_id, recipe_id, ingredient_id):
    if is_ingredient_owner(user_id, ingredient_id) and is_recipe_owner(
        user_id, recipe_id
    ):
        target = get_ingredient_from_recipe(recipe_id, ingredient_id)
        if target is not None:
            recipe_ingredients.remove(target)
            save_file("recipe_ingredients.json", recipe_ingredients)
            return True
    return False


def update_ingredient_from_recipe(
    user_id, recipe_id, ingredient_id, newingredient_id, quantity
):
    if is_ingredient_owner(user_id, ingredient_id) and is_recipe_owner(
        user_id, recipe_id
    ):
        target = get_ingredient_from_recipe(recipe_id, ingredient_id)
        if target is not None:
            target["ingredient_id"] = newingredient_id
            target["quantity"] = quantity
            save_file("recipe_ingredients.json", recipe_ingredients)
            return True
    return False


def get_ingredientlist_from_recipe(recipe_id):
    return list(filter(lambda r: r["recipe_id"] == recipe_id, recipe_ingredients))


def get_ingredient_from_recipe(recipe_id, ingredient_id):
    ingredient_list = get_ingredientlist_from_recipe(recipe_id)
    results = list(
        filter(lambda i: i["ingredient_id"] == ingredient_id, ingredient_list)
    )
    return results[0] if results else None


# CRUD Usuarios


def add_user(name, password, level="user"):
    if not user_exists_name(name):
        newid = (max(u["user_id"] for u in users) + 1) if users else 0
        users.append(
            {"user_id": newid, "username": name, "password": password, "level": level, "favourites": {"recipes": [], "ingredients": []}}
        )
        save_file("users.json", users)
        return True
    return False


def delete_user(user_id):
    target = get_user(user_id)
    if target is not None:
        users.remove(target)
        save_file("users.json", users)
        return True
    return False


def update_user(user_id, name, password, level):
    target = get_user(user_id)
    if target is not None:
        target["username"] = name
        target["password"] = password
        target["level"] = level
        save_file("users.json", users)
        return True
    return False


def get_user(user_id):
    results = list(filter(lambda u: u["user_id"] == int(user_id), users))
    return results[0] if results else None


def get_user_by_name(username):
    results = list(filter(lambda u: u["username"] == username, users))
    return results[0] if results else None


# CRUD Plan de Recetas


def get_plan(user_id):
    results = list(filter(lambda p: p["user_id"] == int(user_id), recipe_plan))
    return results[0] if results else None


def get_day_from_plan(plan, day_id):
    results = list(filter(lambda d: d["day_id"] == int(day_id), plan["plan"]))
    return results[0] if results else None


def add_user_plan(user_id):
    recipe_plan.append(
        {
            "user_id": int(user_id),
            "plan": [
                {
                    "day_id": day_id,
                    "desayuno": [],
                    "almuerzo": [],
                    "merienda": [],
                    "cena": [],
                }
                for day_id in range(7)
            ],
        }
    )
    save_file("recipe_plan.json", recipe_plan)


def add_recipe_to_plan(user_id, recipe_id, day_id, mealtype_id):
    mealtype = get_mealtype_by_id(mealtype_id)
    if (
        is_plan_owner(user_id)
        and is_recipe_owner(user_id, recipe_id)
        and not is_recipe_on_day(user_id, recipe_id, day_id, mealtype)
    ):
        plan = get_plan(user_id)
        day = get_day_from_plan(plan, day_id)
        if day:
            day[mealtype].append(recipe_id)
            save_file("recipe_plan.json", recipe_plan)
            return True
    return False


def remove_recipe_from_plan(user_id, recipe_id, day_id, mealtype_id):
    mealtype = get_mealtype_by_id(mealtype_id)
    if (
        is_plan_owner(user_id)
        and is_recipe_owner(user_id, recipe_id)
        and is_recipe_on_day(user_id, recipe_id, day_id, mealtype)
    ):
        plan = get_plan(user_id)
        day = get_day_from_plan(plan, day_id)
        if day:
            day[mealtype].remove(recipe_id)
            save_file("recipe_plan.json", recipe_plan)
            return True
    return False


def get_user_plan(user_id):
    plan = get_plan(user_id)
    if plan and is_plan_owner(user_id):
        return plan["plan"]
    return None


def get_recipe_from_plan(user_id, recipe_id, day_id, mealtype_id):
    mealtype = get_mealtype_by_id(mealtype_id)
    if (
        is_plan_owner(user_id)
        and is_recipe_owner(user_id, recipe_id)
        and is_recipe_on_day(user_id, recipe_id, day_id, mealtype)
    ):
        return get_recipe(recipe_id)
    return None


def replace_recipe_from_plan(user_id, recipe_id, day_id, mealtype_id, newrecipe_id):
    mealtype = get_mealtype_by_id(mealtype_id)
    if (
        is_plan_owner(user_id)
        and is_recipe_owner(user_id, recipe_id)
        and is_recipe_owner(user_id, newrecipe_id)
        and is_recipe_on_day(user_id, recipe_id, day_id, mealtype)
        and not is_recipe_on_day(user_id, newrecipe_id, day_id, mealtype)
    ):
        plan = get_plan(user_id)
        day = get_day_from_plan(plan, day_id)
        if day:
            idx = day[mealtype].index(recipe_id)
            day[mealtype][idx] = newrecipe_id
            save_file("recipe_plan.json", recipe_plan)
            return True
    return False


def get_day_recipes_mealtype(user_id, day_id, mealtype_id):
    plan = get_user_plan(user_id)
    mealtype = get_mealtype_by_id(mealtype_id)
    if plan is None or mealtype is None:
        return None
    day = get_day_from_plan({"plan": plan, "user_id": user_id}, day_id)
    if day is None:
        return None
    recipe_ids = set(day[mealtype])
    user_recipes = get_user_recipes(user_id)
    if user_recipes:
        return list(filter(lambda r: r["id"] in recipe_ids, user_recipes))
    return []


# Extras


def get_recipe_ingredient_data(recipe_id):
    ri_list = get_ingredientlist_from_recipe(recipe_id)

    ingredients_id = {i["id"]: i for i in ingredients}

    result = []
    for ri in ri_list:
        ingredient = ingredients_id[ri["ingredient_id"]]
        unit = get_unit_by_id(ingredient["unit_id"])

        if ri["quantity"] is None:
            result.append(f"{ingredient['name']}: {unit}")
        else:
            result.append(f"{ingredient['name']}: {ri['quantity']} ({unit})")

    return result


def calculate_recipe_total_quantity(recipe_id):
    ri_list = get_ingredientlist_from_recipe(recipe_id)
    quantities = list(
        map(
            lambda ri: ri["quantity"],
            filter(lambda ri: ri["quantity"] is not None, ri_list),
        )
    )
    if not quantities:
        return 0
    return reduce(lambda acc, qty: acc + qty, quantities)


def count_recipes_in_plan(user_id):
    plan = get_user_plan(user_id)
    if not plan:
        return 0
    mealtypes = get_mealtype_list()
    recipes_day = list(
        map(
            lambda day: reduce(lambda acc, mt: acc + len(day[mt]), mealtypes, 0),
            plan,
        )
    )
    return reduce(lambda acc, n: acc + n, recipes_day, 0)

# Favoritos

def fav_recipe(user, recipe, action="add"):
    fav_list = user["favourites"]["recipes"]
    
    if action == "add" and recipe["id"] not in fav_list:
        fav_list.append(recipe["id"])
    elif action == "remove" and recipe["id"] in fav_list:
        fav_list.remove(recipe["id"])
    else:
        return False

    flag = False
    i = 0
    while not flag:
        if users[i]["user_id"] == user["user_id"]:
            users[i]["favourites"]["recipes"] = fav_list
            flag = True
        i += 1
    save_file("users.json", users)
    return True

def fav_ingredient(user, ingredient, action="add"):
    fav_list = user["favourites"]["ingredients"]
    
    if action == "add" and ingredient["id"] not in fav_list:
        fav_list.append(ingredient["id"])
    elif action == "remove" and ingredient["id"] in fav_list:
        fav_list.remove(ingredient["id"])
    else:
        return False

    flag = False
    i = 0
    while not flag:
        if users[i]["user_id"] == user["user_id"]:
            users[i]["favourites"]["ingredients"] = fav_list
            flag = True
        i += 1
    save_file("users.json", users)
    return True