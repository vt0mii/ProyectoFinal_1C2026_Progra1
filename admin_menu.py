from menu import recetas_menu, ingredientes_menu, plan_menu
from lib.utils import menu_options
import db.data as data
import lib.constants as c
import db.data_crud as f
from lib.colors import *
from functools import reduce

def admin_menu():
    flag = True
    while flag:
        print(f"\n\n{CYAN}---------- PANEL DE ADMIN -----------{END}")
        adm_opt = menu_options(c.ADMIN_OPTIONS)

        if adm_opt == 0:
            flag = False
        elif adm_opt == 1:
            stats_menu()
        elif adm_opt == 2:
            gestionar_usuarios_menu()


def stats_menu():
    flag = True
    while flag:
        print("\n\n-------- ESTADÍSTICAS --------")
        opt = menu_options(c.STATS_OPTIONS)

        if opt == 0:
            flag = False
        elif opt == 1:
            stats_resumen_general()
        elif opt == 2:
            stats_recetas()
        elif opt == 3:
            stats_ingredientes()
        elif opt == 4:
            stats_planes()


def stats_resumen_general():
    total_usuarios = len(data.users)
    total_recetas = len(data.recipes)
    total_ings = len(data.ingredients)
    total_ri = len(data.recipe_ingredients)
    total_con_plan = len(data.recipe_plan)
    total_asignaciones_plan = reduce(
        lambda acc, uid: acc + f.contar_recetas_en_plan(uid),
        data.recipe_plan.keys(),
        0
    )
    
    largo = 40
    print("\n===== RESUMEN GENERAL =====")
    print(f"{'Usuarios registrados':<{largo}}: {total_usuarios}")
    print(f"{'Usuarios con plan':<{largo}}: {total_con_plan}")
    print(f"{'Recetas totales':<{largo}}: {total_recetas}")
    print(f"{'Ingredientes totales':<{largo}}: {total_ings}")
    print(f"{'Asignaciones receta-ingrediente':<{largo}}: {total_ri}")
    print(f"{'Recetas asignadas en planes':<{largo}}: {total_asignaciones_plan}")

    if total_usuarios > 0:
        print(
            f"{'Promedio recetas/usuario':<{largo}}: {total_recetas / total_usuarios:.2f}"
        )
    if total_recetas > 0:
        print(f"{'Promedio ings/receta':<{largo}}: {total_ri / total_recetas:.2f}")

    input("\nPresione Enter para continuar...")


def stats_recetas():
    print("\n===== ESTADÍSTICAS DE RECETAS =====")

    if not data.recipes:
        print("No hay recetas registradas.")
        input("\nPresione Enter para continuar...")
        return

    total = len(data.recipes)
    W = 35

    conteo_por_usuario = reduce(
        lambda acc, uid: acc.update({uid: acc.get(uid, 0) + 1}) or acc,
        map(lambda r: str(r[1]), data.recipes),
        {}
    )

    try:
        max_uid = max(conteo_por_usuario, key=lambda k: conteo_por_usuario[k])
        min_uid = min(conteo_por_usuario, key=lambda k: conteo_por_usuario[k])
    except ValueError:
        print("No hay suficientes datos para calcular estadisticas.")
        return
        
    max_user = f.get_user(max_uid)
    min_user = f.get_user(min_uid)
    max_nombre = max_user["username"] if max_user else max_uid
    min_nombre = min_user["username"] if min_user else min_uid

    print(f"{'Total de recetas':<{W}}: {total}")
    print(f"{'Usuarios con al menos una receta':<{W}}: {len(conteo_por_usuario)}")
    print(f"{'Promedio de recetas por usuario':<{W}}: {total / len(data.users):.2f}")
    print(
        f"{'Usuario con mas recetas':<{W}}: {max_nombre} ({conteo_por_usuario[max_uid]})"
    )
    print(
        f"{'Usuario con menos recetas':<{W}}: {min_nombre} ({conteo_por_usuario[min_uid]})"
    )

    print(f"\n{'Usuario':<20} {'Recetas':>7} {'Porcentaje':>10}")
    print(f"{'-'*20} {'-'*7} {'-'*10}")
    for uid, cant in conteo_por_usuario.items():
        user = f.get_user(uid)
        nombre = user["username"] if user else uid
        print(f"{nombre:<20} {cant:>7} {(cant / total * 100):>9.1f}%")

    if data.recipe_ingredients:
        conteo_ri = {}
        for ri in data.recipe_ingredients:
            conteo_ri[ri[1]] = conteo_ri.get(ri[1], 0) + 1

        max_rid = max(conteo_ri, key=lambda k: conteo_ri[k])
        min_rid = min(conteo_ri, key=lambda k: conteo_ri[k])
        max_rec = f.get_recipe(max_rid)
        min_rec = f.get_recipe(min_rid)

        print()
        print(
            f"{'Receta con mas ingredientes':<{W}}: {max_rec[2] if max_rec else max_rid} ({conteo_ri[max_rid]})"
        )
        print(
            f"{'Receta con menos ingredientes':<{W}}: {min_rec[2] if min_rec else min_rid} ({conteo_ri[min_rid]})"
        )
        print(
            f"{'Promedio de ings por receta':<{W}}: {len(data.recipe_ingredients) / len(data.recipes):.2f}"
        )

    input("\nPresione Enter para continuar...")


def stats_ingredientes():
    print("\n===== ESTADÍSTICAS DE INGREDIENTES =====")

    if not data.ingredients:
        print("No hay ingredientes registrados.")
        input("\nPresione Enter para continuar...")
        return

    total = len(data.ingredients)
    W = 32

    conteo_unidad = {}
    for ing in data.ingredients:
        conteo_unidad[ing[3]] = conteo_unidad.get(ing[3], 0) + 1

    conteo_por_usuario = {}
    for ing in data.ingredients:
        uid = str(ing[1])
        conteo_por_usuario[uid] = conteo_por_usuario.get(uid, 0) + 1

    max_uid = max(conteo_por_usuario, key=lambda k: conteo_por_usuario[k])
    min_uid = min(conteo_por_usuario, key=lambda k: conteo_por_usuario[k])
    max_user = f.get_user(max_uid)
    min_user = f.get_user(min_uid)
    max_nombre = max_user["username"] if max_user else max_uid
    min_nombre = min_user["username"] if min_user else min_uid

    print(f"{'Total de ingredientes':<{W}}: {total}")
    print(f"{'Promedio de ings por usuario':<{W}}: {total / len(data.users):.2f}")
    print(
        f"{'Usuario con mas ingredientes':<{W}}: {max_nombre} ({conteo_por_usuario[max_uid]})"
    )
    print(
        f"{'Usuario con menos ingredientes':<{W}}: {min_nombre} ({conteo_por_usuario[min_uid]})"
    )

    print(f"\n{'Unidad':<14} {'Cantidad':>8} {'Porcentaje':>10}")
    print(f"{'-'*14} {'-'*8} {'-'*10}")
    for unit_id, cant in sorted(conteo_unidad.items(), key=lambda x: -x[1]):
        unit_name = f.get_unit_by_id(unit_id) or str(unit_id)
        print(f"{unit_name:<14} {cant:>8} {(cant / total * 100):>9.1f}%")

    input("\nPresione Enter para continuar...")


def stats_planes():
    print("\n===== ESTADÍSTICAS DE PLANES =====")

    if not data.recipe_plan:
        print("No hay planes registrados.")
        input("\nPresione Enter para continuar...")
        return

    W = 36
    total_slots = 0
    slots_ocupados = 0
    conteo_por_tipo = {mt[1]: 0 for mt in data.meal_types}
    conteo_por_dia = {day[1]: 0 for day in data.days}
    receta_freq = {}

    for uid, plan in data.recipe_plan.items():
        for day_id, mealtypes in plan.items():
            day_name = f.get_days_by_id(int(day_id)) or day_id
            for mealtype, recetas in mealtypes.items():
                total_slots += 1
                if recetas:
                    slots_ocupados += len(recetas)
                    conteo_por_tipo[mealtype] = conteo_por_tipo.get(mealtype, 0) + len(
                        recetas
                    )
                    conteo_por_dia[day_name] = conteo_por_dia.get(day_name, 0) + len(
                        recetas
                    )
                    for rid in recetas:
                        receta_freq[rid] = receta_freq.get(rid, 0) + 1

    porcentaje_ocupacion = (
        (slots_ocupados / total_slots * 100) if total_slots > 0 else 0
    )

    print(f"{'Usuarios con plan activo':<{W}}: {len(data.recipe_plan)}")
    print(f"{'Total de slots disponibles':<{W}}: {total_slots}")
    print(f"{'Slots ocupados':<{W}}: {slots_ocupados}")
    print(f"{'Porcentaje de ocupacion':<{W}}: {porcentaje_ocupacion:.1f}%")

    if conteo_por_tipo:
        tipo_max = max(conteo_por_tipo, key=lambda k: conteo_por_tipo[k])
        tipo_min = min(conteo_por_tipo, key=lambda k: conteo_por_tipo[k])
        print(
            f"\n{'Tipo con mas recetas asignadas':<{W}}: {tipo_max} ({conteo_por_tipo[tipo_max]})"
        )
        print(
            f"{'Tipo con menos recetas asignadas':<{W}}: {tipo_min} ({conteo_por_tipo[tipo_min]})"
        )

        print(f"\n{'Tipo de comida':<14} {'Recetas':>7} {'Porcentaje':>10}")
        print(f"{'-'*14} {'-'*7} {'-'*10}")
        for tipo, cant in conteo_por_tipo.items():
            porcentaje = (cant / slots_ocupados * 100) if slots_ocupados > 0 else 0
            print(f"{tipo:<14} {cant:>7} {porcentaje:>9.1f}%")

    if conteo_por_dia:
        dia_max = max(conteo_por_dia, key=lambda k: conteo_por_dia[k])
        dia_min = min(conteo_por_dia, key=lambda k: conteo_por_dia[k])
        print(
            f"\n{'Dia con mas recetas asignadas':<{W}}: {dia_max} ({conteo_por_dia[dia_max]})"
        )
        print(
            f"{'Dia con menos recetas asignadas':<{W}}: {dia_min} ({conteo_por_dia[dia_min]})"
        )

        print(f"\n{'Dia':<12} {'Recetas':>7} {'Porcentaje':>10}")
        print(f"{'-'*12} {'-'*7} {'-'*10}")
        for dia, cant in conteo_por_dia.items():
            porcentaje = (cant / slots_ocupados * 100) if slots_ocupados > 0 else 0
            print(f"{dia:<12} {cant:>7} {porcentaje:>9.1f}%")

    if receta_freq:
        rid_max = max(receta_freq, key=lambda k: receta_freq[k])
        rec_max = f.get_recipe(rid_max)
        print(
            f"\n{'Receta mas usada en planes':<{W}}: {rec_max[2] if rec_max else rid_max} ({receta_freq[rid_max]} veces)"
        )

    input("\nPresione Enter para continuar...")


def gestionar_usuarios_menu():
    flag = True
    while flag:
        print("\n\n-------- GESTIONAR USUARIOS --------")
        opt = menu_options(c.GESTIONAR_USUARIOS_OPTIONS)

        if opt == 0:
            flag = False
        elif opt == 1:
            listar_usuarios()
        elif opt == 2:
            uid = seleccionar_usuario()
            if uid:
                recetas_menu(uid)
        elif opt == 3:
            uid = seleccionar_usuario()
            if uid:
                ingredientes_menu(uid)
        elif opt == 4:
            uid = seleccionar_usuario()
            if uid:
                plan_menu(uid)


def listar_usuarios():
    W_id = 4
    W_name = 20
    W_level = 8
    W_num = 7

    print("\n===== USUARIOS REGISTRADOS =====")
    print(
        f"{'ID':<{W_id}} {'Usuario':<{W_name}} {'Nivel':<{W_level}} {'Recetas':>{W_num}} {'Ings':>{W_num}} {'Plan':>{W_num}}"
    )
    print(f"{'-'*W_id} {'-'*W_name} {'-'*W_level} {'-'*W_num} {'-'*W_num} {'-'*W_num}")

    for uid, u in data.users.items():
        recetas = f.get_user_recipes(uid)
        ings = f.get_user_ingredients(uid)
        tiene_plan = "si" if uid in data.recipe_plan else "no"
        print(
            f"{uid:<{W_id}} {u['username']:<{W_name}} {u['level']:<{W_level}}"
            f" {len(recetas) if recetas else 0:>{W_num}}"
            f" {len(ings) if ings else 0:>{W_num}}"
            f" {tiene_plan:>{W_num}}"
        )
    input("\nPresione Enter para continuar...")


def seleccionar_usuario():
    user_list = list(data.users.items())
    if not user_list:
        print("No hay usuarios registrados.")
        return None

    nombres = [f"{uid} - {u['username']}" for uid, u in user_list]
    opt = menu_options(nombres, "Seleccione el usuario: ")
    if opt == 0:
        return None
    return user_list[opt - 1][0]
