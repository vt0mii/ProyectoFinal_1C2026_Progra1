from db.data import *
from components.validation import *
from functools import reduce

# CRUD Tuplas


## Unidades
def get_unit_by_id(unit_id):
    for u in units:
        if u[0] == unit_id:
            return u[1]
    return None


def get_mealtype_by_id(mealtype_id):
    for m in meal_types:
        if m[0] == mealtype_id:
            return m[1]
    return None


def get_days_by_id(day_id):
    for d in days:
        if d[0] == day_id:
            return d[1]
    return None


def get_mealtype_list():
    return list(map(lambda mt: mt[1], meal_types))


def get_days_list():
    return list(map(lambda day: day[1], days))


# CRUD Matrices Dinamicas


## Recetas


def add_recipe(user_id, title, instructions):
    if user_exists_id(user_id):
        newid = max((r[0] for r in recipes), default=-1) + 1
        recipes.append([newid, user_id, title, instructions])
        return True
    return False


def delete_recipe(user_id, recipe_id):
    if is_recipe_owner(user_id, recipe_id):
        target = get_recipe(recipe_id)
        if target is not None:
            huerfanos = get_ingredientlist_from_recipe(recipe_id)
            for ri in huerfanos:
                recipe_ingredients.remove(ri)

            for uid, plan in recipe_plan.items():
                for day in plan.values():
                    for mealtype, recetas in day.items():
                        if recipe_id in recetas:
                            recetas.remove(recipe_id)

            recipes.remove(target)
            return True
    return False


def update_recipe(user_id, recipe_id, title, instructions):
    if is_recipe_owner(user_id, recipe_id):
        recipe = get_recipe(recipe_id)
        if recipe is not None:
            recipe[2] = title
            recipe[3] = instructions
            return True
    return False


def get_recipe(recipe_id):
    def criteria(r):
        return r[0] == recipe_id

    results = list(filter(criteria, recipes))
    return results[0] if results else None


def get_recipe_by_name(recipe_name):
    def criteria(r):
        return r[2] == recipe_name

    results = list(filter(criteria, recipes))
    return results[0] if results else None


def get_user_recipes(user_id):
    ing = []
    if user_exists_id(user_id):
        ing = [i for i in recipes if i[1] == int(user_id)]
    return ing if len(ing) > 0 else None


## Ingredientes


def add_ingredient(user_id, title, unit_id):
    if user_exists_id(user_id):
        newid = max((i[0] for i in ingredients), default=-1) + 1
        ingredients.append([newid, user_id, title, unit_id])
        return True
    return False


def delete_ingredient(user_id, ingredient_id):
    if is_ingredient_owner(user_id, ingredient_id):
        target = get_ingredient(ingredient_id)
        if target is not None:
            ingredients.remove(target)
            return True
    return False


def update_ingredient(user_id, ingredient_id, title, unit_id):
    if is_ingredient_owner(user_id, ingredient_id):
        ingredient = get_ingredient(ingredient_id)
        if ingredient is not None:
            ingredient[2] = title
            ingredient[3] = unit_id
            return True
    return False


def get_ingredient(ingredient_id):
    results = list(filter(lambda i: i[0] == ingredient_id, ingredients))
    return results[0] if results else None


def get_user_ingredients(user_id):
    ing = []
    if user_exists_id(user_id):
        ing = [i for i in ingredients if i[1] == int(user_id)]
    return ing if len(ing) > 0 else None


## Ingredientes en Recetas
def add_ingredient_to_recipe(user_id, recipe_id, ingredient_id, quantity):
    if is_ingredient_owner(user_id, ingredient_id) and is_recipe_owner(
        user_id, recipe_id
    ):
        newid = max((r[0] for r in recipe_ingredients), default=-1) + 1
        recipe_ingredients.append([newid, recipe_id, ingredient_id, quantity])
        return True
    return False


def delete_ingredient_from_recipe(user_id, recipe_id, ingredient_id):
    if is_ingredient_owner(user_id, ingredient_id) and is_recipe_owner(
        user_id, recipe_id
    ):
        target = get_ingredient_from_recipe(recipe_id, ingredient_id)
        if target is not None:
            recipe_ingredients.remove(target)
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
            target[2] = newingredient_id
            target[3] = quantity
            return True
    return False


# Esto va a ser util para el momento de mostrar todos
def get_ingredientlist_from_recipe(recipe_id):
    results = list(filter(lambda r: r[1] == recipe_id, recipe_ingredients))
    return results


def get_ingredient_from_recipe(recipe_id, ingredient_id):
    ingredient_list = get_ingredientlist_from_recipe(recipe_id)
    results = list(filter(lambda i: i[2] == ingredient_id, ingredient_list))
    return results[0] if results else None


# Diccionarios


## Usuarios
def add_user(name, password, level="user"):
    if not user_exists_name(name):
        newid = (max(int(id) for id in users.keys()) + 1) if users else 0
        users[str(newid)] = {
            "username": name,
            "password": password,
            "level": level,
        }
        return True
    return False


def delete_user(user_id):
    if user_exists_id(user_id):
        users.pop(user_id)
        return True
    return False


def update_user(user_id, name, password, level):
    if user_exists_id(user_id):
        users[user_id] = {"username": name, "password": password, "level": level}
        return True
    return False


def get_user(user_id):
    if user_exists_id(user_id):
        return users[user_id]
    return None


def get_user_by_name(username):
    results = list(filter(lambda item: item[1]["username"] == username, users.items()))
    return results[0] if results else None


## Recipe Plan


def add_recipe_to_plan(user_id, recipe_id, day_id, mealtype_id):
    mealtype = get_mealtype_by_id(mealtype_id)
    if (
        is_plan_owner(user_id)
        and is_recipe_owner(user_id, recipe_id)
        and not is_recipe_on_day(user_id, recipe_id, day_id, mealtype)
    ):
        recipe_plan[str(user_id)][str(day_id)][mealtype].append(recipe_id)
        return True
    return False


def remove_recipe_from_plan(user_id, recipe_id, day_id, mealtype_id):
    mealtype = get_mealtype_by_id(mealtype_id)
    if (
        is_plan_owner(user_id)
        and is_recipe_owner(user_id, recipe_id)
        and is_recipe_on_day(user_id, recipe_id, day_id, mealtype)
    ):
        recipe_plan[str(user_id)][str(day_id)][mealtype].remove(recipe_id)
        return True
    return False


def get_user_plan(user_id):
    if is_plan_owner(user_id):
        return recipe_plan[str(user_id)]
    return None


def get_recipe_from_plan(user_id, recipe_id, day_id, mealtype_id):
    mealtype = get_mealtype_by_id(mealtype_id)
    if (
        is_plan_owner(user_id)
        and is_recipe_owner(user_id, recipe_id)
        and is_recipe_on_day(user_id, recipe_id, day_id, mealtype)
    ):
        recipe = list(filter(lambda r: r[0] == recipe_id, recipes))
        return recipe[0] if recipe else None
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
        recipe_indx = recipe_plan[str(user_id)][str(day_id)][mealtype].index(recipe_id)
        recipe_plan[str(user_id)][str(day_id)][mealtype][recipe_indx] = newrecipe_id
        return True
    return False


def get_day_recipes_mealtype(user_id, day_id, mealtype_id):
    plan = get_user_plan(user_id)
    mealtype = get_mealtype_by_id(mealtype_id)
    if plan and mealtype:
        recetas_id = set(plan[str(day_id)][mealtype])
        recetas_usuario = get_user_recipes(user_id)
        if recetas_usuario:
            recetas_filtradas = list(
                filter(lambda r: r[0] in recetas_id, recetas_usuario)
            )
            return recetas_filtradas
    else:
        return None


# Extras


def get_recipe_ingredient_names(recipe_id):
    ri_list = get_ingredientlist_from_recipe(recipe_id)
    ingredientes_receta = list(
        filter(lambda i: i[0] in map(lambda ri: ri[2], ri_list), ingredients)
    )
    return list(map(lambda i: f"{i[2]} ({get_unit_by_id(i[3])})", ingredientes_receta))


def calcular_cantidad_total_receta(recipe_id):
    ri_list = get_ingredientlist_from_recipe(recipe_id)
    cantidades = list(
        map(lambda ri: ri[3], filter(lambda ri: ri[3] is not None, ri_list))
    )
    if not cantidades:
        return 0
    return reduce(lambda acc, cantidad: acc + cantidad, cantidades)


def contar_recetas_en_plan(user_id):
    plan = get_user_plan(user_id)
    if not plan:
        return 0
    recetas_por_dia = list(
        map(
            lambda day: reduce(lambda acc, lista: acc + len(lista), day.values(), 0),
            plan.values(),
        )
    )
    return reduce(lambda acc, n: acc + n, recetas_por_dia, 0)
