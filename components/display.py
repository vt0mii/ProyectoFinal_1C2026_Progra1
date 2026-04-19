from db.data_crud import *
from components.validation import *
from lib.colors import *

def display_recipes(user_id):
    if user_exists_id(user_id):
        my_recipes = get_user_recipes(user_id)
        if my_recipes:
            num = 1
            for rec in my_recipes:
                print(f"{BOLD}{num}.{END} {rec[2]}")
                num += 1
        return True
    return False


def display_ingredients(user_id):
    if user_exists_id(user_id):
        my_ingredients = get_user_ingredients(user_id)
        if my_ingredients:
            num = 1
            for ing in my_ingredients:
                print(f"{BOLD}ID {ing[0]:<2}{END}| {ing[2]} ({get_unit_by_id(ing[3])})")
                num += 1
        return True
    return False


def display_plan(userid):
    uid = userid
    if not is_plan_owner(uid):
        print(f"{RED}\n[!] El usuario {uid} no tiene un plan.{END}")
        return

    ancho_col = 22
    tipos_comida = get_mealtype_list()
    user = get_user(uid)
    plan = get_user_plan(uid)

    if plan is None:
        print(f"{RED}\n[!] No se pudo obtener el plan del usuario {uid}.{END}")
        return

    ancho_total = ancho_col * 7
    nombre_usuario = user["username"].upper() if user else "DESCONOCIDO"

    print(f"\n{CYAN}{'=' * ancho_total}{END}")
    print(f"{CYAN}{'PLAN SEMANAL DE: ' + nombre_usuario:^{ancho_total}}{END}")
    print(f"{CYAN}{'=' * ancho_total}{END}\n")

    cabecera = "".join(
        f"{(get_days_by_id(i) or f'DIA {i}').upper():<{ancho_col}}" for i in range(7)
    )
    print(cabecera)
    print(f"{'-' * ancho_total}")

    for meal in tipos_comida:
        max_recetas = max(len(plan[str(i)][meal]) for i in range(7))
        if max_recetas == 0:
            fila = "".join(f"{'---':<{ancho_col}}" for _ in range(7))
            print(f"{fila} | {meal.upper()}")
            continue

        for pos in range(max_recetas):
            fila = ""
            for i in range(7):
                recipe_ids = plan[str(i)][meal]
                if pos < len(recipe_ids):
                    receta_data = get_recipe(recipe_ids[pos])
                    if receta_data:
                        nombre = receta_data[2]
                        nombre = (
                            f"{nombre[:ancho_col - 3]}.."
                            if len(nombre) > ancho_col - 3
                            else nombre
                        )
                    else:
                        nombre = "ID No encontrado"
                else:
                    nombre = ""
                fila += f"{nombre:<{ancho_col}}"

            etiqueta = meal.upper() if pos == 0 else ""
            print(f"{fila} | {etiqueta}")

    print(f"{'-' * ancho_total}")
