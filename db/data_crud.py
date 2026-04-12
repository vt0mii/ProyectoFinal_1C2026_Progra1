from .data import *
from components.validation import *

# CRUD Tuplas


## Unidades
def get_unit_by_id(unitid):
    for u in units:
        if u[0] == unitid:
            return u[1]
    return None


def get_mealtype_by_id(mealtypeid):
    for m in meal_types:
        if m[0] == mealtypeid:
            return m[1]
    return None


def get_days_by_id(dayid):
    for d in days:
        if d[0] == dayid:
            return d[1]
    return None


# CRUD Matrices Dinamicas


## Recetas
def add_recipe(userid, title, instructions):
    if user_exists_id(userid):
        newid = max((r[0] for r in recipes), default=-1) + 1
        recipes.append([newid, userid, title, instructions])
        return True
    return False


def delete_recipe(userid, recipeid):
    if is_recipe_owner(userid, recipeid):
        target = get_recipe(recipeid)
        if target is not None:
            recipes.remove(target)
            return True
    return False


def update_recipe(userid, recipeid, title, instructions):
    if is_recipe_owner(userid, recipeid):
        recipe = get_recipe(recipeid)
        if recipe is not None:
            recipe[2] = title
            recipe[3] = instructions
            return True
    return False


def get_recipe(recipeid):
    def criteria(r):
        return r[0] == recipeid

    results = list(filter(criteria, recipes))
    return results[0] if results else None


## Ingredientes
def add_ingredient(userid, title, unit_id):
    if user_exists_id(userid):
        newid = max((i[0] for i in ingredients), default=-1) + 1
        ingredients.append([newid, userid, title, unit_id])
        return True
    return False


def delete_ingredient(userid, ingredientid):
    if is_ingredient_owner(userid, ingredientid):
        target = get_ingredient(ingredientid)
        if target is not None:
            ingredients.remove(target)
            return True
    return False


def update_ingredient(userid, ingredientid, title, unit_id):
    if is_ingredient_owner(userid, ingredientid):
        ingredient = get_ingredient(ingredientid)
        if ingredient is not None:
            ingredient[2] = title
            ingredient[3] = unit_id
            return True
    return False


def get_ingredient(ingredientid):
    results = list(filter(lambda i: i[0] == ingredientid, ingredients))
    return results[0] if results else None


## Ingredientes en Recetas
def add_ingredient_to_recipe(userid, recipeid, ingredientid, quantity):
    if is_ingredient_owner(userid, ingredientid) and is_recipe_owner(userid, recipeid):
        newid = max((r[0] for r in recipe_ingredients), default=-1) + 1
        recipe_ingredients.append([newid, recipeid, ingredientid, quantity])
        return True
    return False


def delete_ingredient_from_recipe(userid, recipeid, ingredientid):
    if is_ingredient_owner(userid, ingredientid) and is_recipe_owner(userid, recipeid):
        target = get_ingredient_from_recipe(ingredientid, recipeid)
        if target is not None:
            recipe_ingredients.remove(target)
            return True
    return False


def update_ingredient_from_recipe(
    userid, recipeid, ingredientid, newingredientid, quantity
):
    if is_ingredient_owner(userid, ingredientid) and is_recipe_owner(userid, recipeid):
        target = get_ingredient_from_recipe(recipeid, ingredientid)
        if target is not None:
            target[2] = newingredientid
            target[3] = quantity
            return True
    return False


# Esto va a ser util para el momento de mostrar todos
def get_ingredientlist_from_recipe(recipeid):
    results = list(filter(lambda r: r[1] == recipeid, recipe_ingredients))
    return results


def get_ingredient_from_recipe(recipeid, ingredientid):
    ingredient_list = get_ingredientlist_from_recipe(recipeid)
    results = list(filter(lambda i: i[2] == ingredientid, ingredient_list))
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


def delete_user(userid):
    if user_exists_id(userid):
        users.pop(userid)
        return True
    return False


def update_user(userid, name, password, level):
    if user_exists_id(userid):
        users[userid] = {"username": name, "password": password, "level": level}
        return True
    return False


def get_user(userid):
    if user_exists_id(userid):
        return users[userid]
    return None

def get_user_by_name(username):
    results = list(filter(lambda item: item[1]["username"] == username, users.items()))
    return results[0] if results else None


## Recipe Plan


def add_recipe_to_plan(userid, recipeid, dayid, mealtypeid):
    mealtype = get_mealtype_by_id(mealtypeid)
    if (
        is_plan_owner(userid)
        and is_recipe_owner(userid, recipeid)
        and not is_recipe_on_day(userid, recipeid, dayid, mealtype)
    ):
        recipe_plan[str(userid)][str(dayid)][mealtype].append(recipeid)
        return True
    return False


def remove_recipe_from_plan(userid, recipeid, dayid, mealtypeid):
    mealtype = get_mealtype_by_id(mealtypeid)
    if (
        is_plan_owner(userid)
        and is_recipe_owner(userid, recipeid)
        and is_recipe_on_day(userid, recipeid, dayid, mealtype)
    ):
        recipe_plan[str(userid)][str(dayid)][mealtype].remove(recipeid)
        return True
    return False


def get_user_plan(userid):
    if is_plan_owner(userid):
        return recipe_plan[str(userid)]
    return None


def get_recipe_from_plan(userid, recipeid, dayid, mealtypeid):
    mealtype = get_mealtype_by_id(mealtypeid)
    if (
        is_plan_owner(userid)
        and is_recipe_owner(userid, recipeid)
        and is_recipe_on_day(userid, recipeid, dayid, mealtype)
    ):
        recipe = list(filter(lambda r: r[0] == recipeid, recipes))
        return recipe[0] if recipe else None
    return None


def replace_recipe_from_plan(userid, recipeid, dayid, mealtypeid, newrecipeid):
    mealtype = get_mealtype_by_id(mealtypeid)
    if (
        is_plan_owner(userid)
        and is_recipe_owner(userid, recipeid)
        and is_recipe_owner(userid, newrecipeid)
        and is_recipe_on_day(userid, recipeid, dayid, mealtype)
        and not is_recipe_on_day(userid, newrecipeid, dayid, mealtype)
    ):
        recipe_indx = recipe_plan[str(userid)][str(dayid)][mealtype].index(recipeid)
        recipe_plan[str(userid)][str(dayid)][mealtype][recipe_indx] = newrecipeid
        return True
    return False
