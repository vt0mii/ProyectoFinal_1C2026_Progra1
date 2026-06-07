from db.data_crud import *
from components.validation import *
from lib.colors import *
import db.data as data

def display_recipes(user_id):
    if user_exists_id(user_id):
        my_recipes = get_user_recipes(user_id)
        if my_recipes:
            num = 1
            for rec in my_recipes:
                print(f"{BOLD}{num}.{END} {rec['title']}")
                num += 1
        return True
    return False


def display_ingredients(user_id):
    if user_exists_id(user_id):
        my_ingredients = get_user_ingredients(user_id)
        if my_ingredients:
            fav_ingredients = data.user_cache["favourites"]["ingredients"]
            
            groups = {}
            for ing in my_ingredients:
                category_name = get_category_by_id(ing.get("category")) or "Sin categoría"
                groups.setdefault(category_name, []).append(ing)
        
            for category_name, ingredients in groups.items():
                print(f"\n{BOLD}── {category_name} ──{END}")
                for ing in ingredients:
                    star = f"{YELLOW}*{END} " if ing["id"] in fav_ingredients else ""
                    print(
                        f"  {star}{BOLD}ID {ing['id']:<2}{END}| {ing['name']} ({get_unit_by_id(ing['unit_id'])})"
                    )
        return True
    return False


def display_plan(user_id):
    if not is_plan_owner(user_id):
        print(f"{RED}\n[!] El usuario {user_id} no tiene un plan.{END}")
        return

    col_width = 22
    meal_types = get_mealtype_list()
    user = get_user(user_id)
    plan = get_user_plan(user_id)

    if plan is None:
        print(f"{RED}\n[!] No se pudo obtener el plan del usuario {user_id}.{END}")
        return

    total_width = col_width * 7
    username = user["username"].upper() if user else "UNKNOWN"

    print(f"\n{CYAN}{'=' * total_width}{END}")
    print(f"{CYAN}{'PLAN SEMANAL DE: ' + username:^{total_width}}{END}")
    print(f"{CYAN}{'=' * total_width}{END}\n")

    header = "".join(
        f"{(get_day_by_id(i) or f'DIA {i}').upper():<{col_width}}" for i in range(7)
    )
    print(header)
    print(f"{'-' * total_width}")

    for meal in meal_types:
        max_recipes = max(len(plan[i][meal]) for i in range(7))
        if max_recipes == 0:
            row = "".join(f"{'---':<{col_width}}" for _ in range(7))
            print(f"{row} | {meal.upper()}")
            continue

        for pos in range(max_recipes):
            row = ""
            for i in range(7):
                recipe_ids = plan[i][meal]
                if pos < len(recipe_ids):
                    recipe_data = get_recipe(recipe_ids[pos])
                    if recipe_data:
                        name = recipe_data["title"]
                        name = (
                            f"{name[:col_width - 3]}.."
                            if len(name) > col_width - 3
                            else name
                        )
                    else:
                        name = "ID not found"
                else:
                    name = "---" if pos == 0 else ""
                row += f"{name:<{col_width}}"

            label = meal.upper() if pos == 0 else ""
            print(f"{row} | {label}")

    print(f"{'-' * total_width}")
    

