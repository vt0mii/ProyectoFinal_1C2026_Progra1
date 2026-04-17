from db.data_crud import *
from components.validation import *

def display_recipes(user_id):
    if user_exists_id(user_id):
        my_recipes = get_user_recipes(user_id)
        if my_recipes:
            num = 1
            for rec in my_recipes:
                print(f'{num}. {rec[2]}')
                num += 1
        return True
    return False

def display_ingredients(user_id):
    if user_exists_id(user_id):
        my_ingredients = get_user_ingredients(user_id)
        if my_ingredients:
            num = 1
            for ing in my_ingredients:
                print(f'{ing[0]}. {ing[2]} ({get_unit_by_id(ing[3])})')
                num += 1
        return True
    return False

def display_plan(userid):
    uid = str(userid)
    if not is_plan_owner(uid):
        print(f"\n[!] El usuario {uid} no tiene un plan.")
        return

    ancho_col = 22
    tipos_comida = get_mealtype_list()
    user = get_user(uid)
    plan = get_user_plan(uid)

    if plan is None:
        print(f"\n[!] No se pudo obtener el plan del usuario {uid}.")
        return

    ancho_total = ancho_col * 7
    nombre_usuario = user['username'].upper() if user else "DESCONOCIDO"

    print(f"\n{'=' * ancho_total}")
    print(f"{'PLAN SEMANAL DE: ' + nombre_usuario:^{ancho_total}}")
    print(f"{'=' * ancho_total}\n")

    cabecera = "".join(
        f"{(get_days_by_id(i) or f'DIA {i}').upper():<{ancho_col}}"
        for i in range(7)
    )
    print(cabecera)
    print(f"{'-' * ancho_total}")

    for meal in tipos_comida:
        fila = ""
        for i in range(7):
            recipe_ids = plan[str(i)][meal]
            if recipe_ids:
                receta_data = get_recipe(recipe_ids[0])
                if receta_data:
                    nombre = receta_data[2]
                    nombre = f"{nombre[:ancho_col - 5]}.." if len(nombre) > ancho_col - 3 else nombre
                else:
                    nombre = "ID No Encontrado"
            else:
                nombre = "---"
            fila += f"{nombre:<{ancho_col}}"
        print(f"{fila} | {meal.upper()}")

    print(f"{'-' * ancho_total}")
