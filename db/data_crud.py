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


def get_mealtype_list():
    return list(map(lambda mt: mt["name"], meal_types))


def get_days_list():
    return list(map(lambda day: day["name"], days))


# CRUD Recetas


def add_recipe(user_id, title, instructions):
    if user_exists_id(user_id):
        newid = max((r["id"] for r in recipes), default=-1) + 1
        recipes.append(
            {
                "id": newid,
                "user_id": user_id,
                "title": title,
                "instructions": instructions,
            }
        )
        save_file("recipes.json", recipes)
        return True
    return False


def delete_recipe(user_id, recipe_id):
    if is_recipe_owner(user_id, recipe_id):
        target = get_recipe(recipe_id)
        if target is not None:
            huerfanos = get_ingredientlist_from_recipe(recipe_id)
            for ri in huerfanos:
                recipe_ingredients.remove(ri)
            save_file("recipe_ingredients.json", recipe_ingredients)

            for entry in recipe_plan:
                for day in entry["plan"]:
                    for mealtype in ["desayuno", "almuerzo", "merienda", "cena"]:
                        if recipe_id in day[mealtype]:
                            day[mealtype].remove(recipe_id)
            save_file("recipe_plan.json", recipe_plan)

            recipes.remove(target)
            save_file("recipes.json", recipes)
            return True
    return False


def update_recipe(user_id, recipe_id, title, instructions):
    if is_recipe_owner(user_id, recipe_id):
        recipe = get_recipe(recipe_id)
        if recipe is not None:
            recipe["title"] = title
            recipe["instructions"] = instructions
            save_file("recipes.json", recipes)
            return True
    return False


def get_recipe(recipe_id):
    results = list(filter(lambda r: r["id"] == recipe_id, recipes))
    return results[0] if results else None


def get_recipe_by_name(recipe_name):
    results = list(filter(lambda r: r["title"] == recipe_name, recipes))
    return results[0] if results else None


def get_user_recipes(user_id):
    if user_exists_id(user_id):
        ing = [r for r in recipes if r["user_id"] == int(user_id)]
        return ing if ing else None
    return None


# CRUD Ingredientes


def add_ingredient(user_id, title, unit_id):
    if user_exists_id(user_id):
        newid = max((i["id"] for i in ingredients), default=-1) + 1
        ingredients.append(
            {"id": newid, "user_id": user_id, "name": title, "unit_id": unit_id}
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


def update_ingredient(user_id, ingredient_id, title, unit_id):
    if is_ingredient_owner(user_id, ingredient_id):
        ingredient = get_ingredient(ingredient_id)
        if ingredient is not None:
            ingredient["name"] = title
            ingredient["unit_id"] = unit_id
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
            {"user_id": newid, "username": name, "password": password, "level": level}
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
    recetas_id = set(day[mealtype])
    recetas_usuario = get_user_recipes(user_id)
    if recetas_usuario:
        return list(filter(lambda r: r["id"] in recetas_id, recetas_usuario))
    return []


# Extras


def get_recipe_ingredient_names(recipe_id):
    ri_list = get_ingredientlist_from_recipe(recipe_id)
    ids_en_receta = set(map(lambda ri: ri["ingredient_id"], ri_list))
    ingredientes_receta = list(filter(lambda i: i["id"] in ids_en_receta, ingredients))
    return list(
        map(
            lambda i: f"{i['name']} ({get_unit_by_id(i['unit_id'])})",
            ingredientes_receta,
        )
    )


def calcular_cantidad_total_receta(recipe_id):
    ri_list = get_ingredientlist_from_recipe(recipe_id)
    cantidades = list(
        map(
            lambda ri: ri["quantity"],
            filter(lambda ri: ri["quantity"] is not None, ri_list),
        )
    )
    if not cantidades:
        return 0
    return reduce(lambda acc, cantidad: acc + cantidad, cantidades)


def contar_recetas_en_plan(user_id):
    plan = get_user_plan(user_id)
    if not plan:
        return 0
    mealtypes = ["desayuno", "almuerzo", "merienda", "cena"]
    recetas_por_dia = list(
        map(
            lambda day: reduce(lambda acc, mt: acc + len(day[mt]), mealtypes, 0),
            plan,
        )
    )
    return reduce(lambda acc, n: acc + n, recetas_por_dia, 0)
