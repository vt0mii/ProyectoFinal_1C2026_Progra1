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
        lambda acc, p: acc + f.contar_recetas_en_plan(p["user_id"]),
        data.recipe_plan,
        0,
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
        print(f"{'Promedio recetas/usuario':<{largo}}: {total_recetas / total_usuarios:.2f}")
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
        lambda acc, r: acc.update({r["user_id"]: acc.get(r["user_id"], 0) + 1}) or acc,
        data.recipes,
        {},
    )

    try:
        max_uid = max(conteo_por_usuario, key=lambda k: conteo_por_usuario[k])
        min_uid = min(conteo_por_usuario, key=lambda k: conteo_por_usuario[k])
    except ValueError:
        print("No hay suficientes datos para calcular estadisticas.")
        return

    max_user = f.get_user(max_uid)
    min_user = f.get_user(min_uid)
    max_nombre = max_user["username"] if max_user else str(max_uid)
    min_nombre = min_user["username"] if min_user else str(min_uid)

    print(f"{'Total de recetas':<{W}}: {total}")
    print(f"{'Usuarios con al menos una receta':<{W}}: {len(conteo_por_usuario)}")
    print(f"{'Promedio de recetas por usuario':<{W}}: {total / len(data.users):.2f}")
    print(f"{'Usuario con mas recetas':<{W}}: {max_nombre} ({conteo_por_usuario[max_uid]})")
    print(f"{'Usuario con menos recetas':<{W}}: {min_nombre} ({conteo_por_usuario[min_uid]})")

    print(f"\n{'Usuario':<20} {'Recetas':>7} {'Porcentaje':>10}")
    print(f"{'-'*20} {'-'*7} {'-'*10}")
    for uid, cant in conteo_por_usuario.items():
        user = f.get_user(uid)
        nombre = user["username"] if user else str(uid)
        print(f"{nombre:<20} {cant:>7} {(cant / total * 100):>9.1f}%")

    if data.recipe_ingredients:
        conteo_ri = reduce(
            lambda acc, ri: acc.update({ri["recipe_id"]: acc.get(ri["recipe_id"], 0) + 1}) or acc,
            data.recipe_ingredients,
            {},
        )

        max_rid = max(conteo_ri, key=lambda k: conteo_ri[k])
        min_rid = min(conteo_ri, key=lambda k: conteo_ri[k])
        max_rec = f.get_recipe(max_rid)
        min_rec = f.get_recipe(min_rid)
        cant_total_max = f.calcular_cantidad_total_receta(max_rid)

        print()
        print(f"{'Receta con mas ingredientes':<{W}}: {max_rec['title'] if max_rec else max_rid} ({conteo_ri[max_rid]} ings, total cantidad: {cant_total_max})")
        print(f"{'Receta con menos ingredientes':<{W}}: {min_rec['title'] if min_rec else min_rid} ({conteo_ri[min_rid]})")
        print(f"{'Promedio de ings por receta':<{W}}: {len(data.recipe_ingredients) / len(data.recipes):.2f}")

    input("\nPresione Enter para continuar...")


def stats_ingredientes():
    print("\n===== ESTADÍSTICAS DE INGREDIENTES =====")

    if not data.ingredients:
        print("No hay ingredientes registrados.")
        input("\nPresione Enter para continuar...")
        return

    total = len(data.ingredients)
    W = 32

    conteo_unidad = reduce(
        lambda acc, ing: acc.update({ing["unit_id"]: acc.get(ing["unit_id"], 0) + 1}) or acc,
        data.ingredients,
        {},
    )

    conteo_por_usuario = reduce(
        lambda acc, ing: acc.update({ing["user_id"]: acc.get(ing["user_id"], 0) + 1}) or acc,
        data.ingredients,
        {},
    )

    max_uid = max(conteo_por_usuario, key=lambda k: conteo_por_usuario[k])
    min_uid = min(conteo_por_usuario, key=lambda k: conteo_por_usuario[k])
    max_user = f.get_user(max_uid)
    min_user = f.get_user(min_uid)
    max_nombre = max_user["username"] if max_user else str(max_uid)
    min_nombre = min_user["username"] if min_user else str(min_uid)

    print(f"{'Total de ingredientes':<{W}}: {total}")
    print(f"{'Promedio de ings por usuario':<{W}}: {total / len(data.users):.2f}")
    print(f"{'Usuario con mas ingredientes':<{W}}: {max_nombre} ({conteo_por_usuario[max_uid]})")
    print(f"{'Usuario con menos ingredientes':<{W}}: {min_nombre} ({conteo_por_usuario[min_uid]})")

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
    mealtypes_keys = ["desayuno", "almuerzo", "merienda", "cena"]
    conteo_por_tipo = {mt: 0 for mt in mealtypes_keys}
    conteo_por_dia = {d["name"]: 0 for d in data.days}
    receta_freq = {}

    for plan_entry in data.recipe_plan:
        for day_entry in plan_entry["plan"]:
            day_name = f.get_day_by_id(day_entry["day_id"]) or str(day_entry["day_id"])
            for mealtype in mealtypes_keys:
                recetas = day_entry[mealtype]
                total_slots += 1
                if recetas:
                    slots_ocupados += len(recetas)
                    conteo_por_tipo[mealtype] = conteo_por_tipo.get(mealtype, 0) + len(recetas)
                    conteo_por_dia[day_name] = conteo_por_dia.get(day_name, 0) + len(recetas)
                    for rid in recetas:
                        receta_freq[rid] = receta_freq.get(rid, 0) + 1

    porcentaje_ocupacion = (slots_ocupados / total_slots * 100) if total_slots > 0 else 0

    print(f"{'Usuarios con plan activo':<{W}}: {len(data.recipe_plan)}")
    print(f"{'Total de slots disponibles':<{W}}: {total_slots}")
    print(f"{'Slots ocupados':<{W}}: {slots_ocupados}")
    print(f"{'Porcentaje de ocupacion':<{W}}: {porcentaje_ocupacion:.1f}%")

    if conteo_por_tipo:
        tipo_max = max(conteo_por_tipo, key=lambda k: conteo_por_tipo[k])
        tipo_min = min(conteo_por_tipo, key=lambda k: conteo_por_tipo[k])
        print(f"\n{'Tipo con mas recetas asignadas':<{W}}: {tipo_max} ({conteo_por_tipo[tipo_max]})")
        print(f"{'Tipo con menos recetas asignadas':<{W}}: {tipo_min} ({conteo_por_tipo[tipo_min]})")

        print(f"\n{'Tipo de comida':<14} {'Recetas':>7} {'Porcentaje':>10}")
        print(f"{'-'*14} {'-'*7} {'-'*10}")
        for tipo, cant in conteo_por_tipo.items():
            porcentaje = (cant / slots_ocupados * 100) if slots_ocupados > 0 else 0
            print(f"{tipo:<14} {cant:>7} {porcentaje:>9.1f}%")

    if conteo_por_dia:
        dia_max = max(conteo_por_dia, key=lambda k: conteo_por_dia[k])
        dia_min = min(conteo_por_dia, key=lambda k: conteo_por_dia[k])
        print(f"\n{'Dia con mas recetas asignadas':<{W}}: {dia_max} ({conteo_por_dia[dia_max]})")
        print(f"{'Dia con menos recetas asignadas':<{W}}: {dia_min} ({conteo_por_dia[dia_min]})")

        print(f"\n{'Dia':<12} {'Recetas':>7} {'Porcentaje':>10}")
        print(f"{'-'*12} {'-'*7} {'-'*10}")
        for dia, cant in conteo_por_dia.items():
            porcentaje = (cant / slots_ocupados * 100) if slots_ocupados > 0 else 0
            print(f"{dia:<12} {cant:>7} {porcentaje:>9.1f}%")

    if receta_freq:
        rid_max = max(receta_freq, key=lambda k: receta_freq[k])
        rec_max = f.get_recipe(rid_max)
        print(f"\n{'Receta mas usada en planes':<{W}}: {rec_max['title'] if rec_max else rid_max} ({receta_freq[rid_max]} veces)")

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
            if uid is not None:
                editar_usuario_menu(uid)
        elif opt == 3:
            uid = seleccionar_usuario()
            if uid is not None:
                recetas_menu(uid)
        elif opt == 4:
            uid = seleccionar_usuario()
            if uid is not None:
                ingredientes_menu(uid)
        elif opt == 5:
            uid = seleccionar_usuario()
            if uid is not None:
                plan_menu(uid)


def listar_usuarios():
    W_id = 4
    W_name = 20
    W_level = 8
    W_num = 7

    print("\n===== USUARIOS REGISTRADOS =====")
    print(f"{'ID':<{W_id}} {'Usuario':<{W_name}} {'Nivel':<{W_level}} {'Recetas':>{W_num}} {'Ings':>{W_num}} {'Plan':>{W_num}}")
    print(f"{'-'*W_id} {'-'*W_name} {'-'*W_level} {'-'*W_num} {'-'*W_num} {'-'*W_num}")

    for u in data.users:
        uid = u["user_id"]
        recetas = f.get_user_recipes(uid)
        ings = f.get_user_ingredients(uid)
        tiene_plan = "si" if f.get_plan(uid) else "no"
        print(
            f"{uid:<{W_id}} {u['username']:<{W_name}} {u['level']:<{W_level}}"
            f" {len(recetas) if recetas else 0:>{W_num}}"
            f" {len(ings) if ings else 0:>{W_num}}"
            f" {tiene_plan:>{W_num}}"
        )
    input("\nPresione Enter para continuar...")


def seleccionar_usuario():
    if not data.users:
        print("No hay usuarios registrados.")
        return None

    nombres = [f"{u['user_id']} - {u['username']}" for u in data.users]
    opt = menu_options(nombres, "Seleccione el usuario: ")
    if opt == 0:
        return None
    return data.users[opt - 1]["user_id"]


def editar_usuario_menu(user_id):
    usuario = f.get_user(user_id)
    if usuario is None:
        print(f"{RED}Usuario no encontrado.{END}")
        return

    flag = True
    while flag:
        print(f"\n{CYAN}--- Editando usuario: {usuario['username']} (nivel: {usuario['level']}) ---{END}")
        opt = menu_options(c.EDITAR_USUARIO_OPTIONS)

        if opt == 0:
            flag = False

        elif opt == 1:  # Cambiar nombre
            nuevo_nombre = input(f"{LIGHT_BLUE}Nuevo nombre de usuario (Enter para mantener '{usuario['username']}'): {END}").strip()
            if nuevo_nombre == "":
                nuevo_nombre = usuario["username"]

            nuevo_nivel = input(f"{LIGHT_BLUE}Nuevo nivel (user/admin, Enter para mantener '{usuario['level']}'): {END}").strip()
            if nuevo_nivel not in ("user", "admin"):
                nuevo_nivel = usuario["level"]

            nueva_pass = input(f"{LIGHT_BLUE}Nueva contraseña (Enter para mantener la actual): {END}").strip()
            if nueva_pass == "":
                nueva_pass = usuario["password"]

            if f.update_user(user_id, nuevo_nombre, nueva_pass, nuevo_nivel):
                usuario = f.get_user(user_id)
                
                if usuario is None:
                    print(f"{RED}Error al actualizar el usuario.{END}")
                    return
    
                print(f"{GREEN}Usuario actualizado correctamente.{END}")
            else:
                print(f"{RED}Error al actualizar el usuario.{END}")

        elif opt == 2:  # Eliminar usuario
            confirmacion = input(f"{RED}¿Seguro que desea eliminar al usuario '{usuario['username']}'? (s/n): {END}").strip().lower()
            if confirmacion == "s":
                if f.delete_user(user_id):
                    print(f"{GREEN}Usuario '{usuario['username']}' eliminado correctamente.{END}")
                    flag = False
                else:
                    print(f"{RED}Error al eliminar el usuario.{END}")