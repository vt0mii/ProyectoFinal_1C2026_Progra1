from db.data_crud import *
from components.validation import *


def display_plan(userid):
    uid = str(userid)
    if not is_plan_owner(uid):
        print(f"\n[!] El usuario {uid} no tiene un plan.")
        return

    ancho_col = 22
    tipos_comida = ["desayuno", "almuerzo", "merienda", "cena"]

    user = get_user(uid)
    plan = get_user_plan(uid)

    if plan is None:
        print(f"\n[!] No se pudo obtener el plan del usuario {uid}.")
        return

    print(f"\n{'='*ancho_col*7}")
    if user:
        print(f"PLAN SEMANAL DE: {user['username'].upper()}".center(ancho_col * 7))
    else:
        print(f"PLAN SEMANAL DE: DESCONOCIDO".center(ancho_col * 7))
    print(f"{'='*ancho_col*7}\n")

    cabecera = ""
    for i in range(7):
        nombre_dia = get_days_by_id(i)
        txt_dia = nombre_dia.upper() if nombre_dia else f"DIA {i}"
        cabecera += f"{txt_dia:<{ancho_col}}"

    print(cabecera)
    print("-" * (ancho_col * 7))

    for meal in tipos_comida:
        fila_texto = ""
        for i in range(7):

            recipe_ids = plan[str(i)][meal]

            if recipe_ids:
                receta_data = get_recipe(recipe_ids[0])
                if receta_data:
                    nombre = receta_data[2]
                    if len(nombre) > (ancho_col - 3):
                        nombre = nombre[: ancho_col - 5] + ".."
                else:
                    nombre = "ID No Encontrado"
            else:
                nombre = "---"

            fila_texto += f"{nombre:<{ancho_col}}"

        print(f"{fila_texto} | {meal.upper()}")

    print("-" * (ancho_col * 7))
