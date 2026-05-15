import components.validation as v
from lib.constants import *
from components.auth import *
import db.data as data
import db.data_crud as f
import components.display as d
from lib.colors import *
from lib.utils import menu_options

def plan_menu(user_id):
    flag = True
    while flag:
        d.display_plan(user_id)
        print(f"\n\n{CYAN}-------- GESTIÓN DE PLAN SEMANAL -------{END}")
        selected = menu_options(PLAN_OPTIONS)

        if selected == 0:
            flag = False

        elif selected == 1:
            mis_recetas = f.get_user_recipes(user_id)
            if mis_recetas:
                day = menu_options(
                    f.get_days_list(), "Por favor, seleccione el dia donde agregar: "
                )
                if int(day) != 0:
                    mt = menu_options(
                        f.get_mealtype_list(),
                        "Por favor, seleccione el tipo de comida: ",
                        False,
                    )

                    recipe_selected = menu_options(
                        [r[2] for r in mis_recetas],
                        "Seleccione la receta a agregar: ",
                        False,
                    )
                    f.add_recipe_to_plan(
                        user_id,
                        mis_recetas[recipe_selected - 1][0],
                        day - 1,
                        mt - 1,
                    )
            else:
                print(f"\n{RED}{"X===X NO SE ENCUENTRAN RECETAS X===X":^40}{END}")

        elif selected == 2:
            mis_recetas = f.get_user_recipes(user_id)
            if mis_recetas:
                day = menu_options(
                    f.get_days_list(),
                    "Por favor, seleccione el dia donde eliminar la receta: ",
                )
                if int(day) != 0:
                    day_name = f.get_day_by_id(int(day))
                    mt = menu_options(
                        f.get_mealtype_list(),
                        "Por favor, seleccione el tipo de comida: ",
                        False,
                    )
                    selected_recipes = f.get_day_recipes_mealtype(
                        user_id, int(day) - 1, int(mt) - 1
                    )
                    if selected_recipes:
                        target = menu_options(
                            [r[2] for r in selected_recipes],
                            "Selecciona la receta a eliminar: ",
                            False,
                        )
                        old_recipe = f.get_recipe(selected_recipes[target - 1][0])
                        if old_recipe:
                            f.remove_recipe_from_plan(
                                user_id, old_recipe[0], int(day) - 1, int(mt) - 1
                            )
                    else:
                        print(
                            f"\n{RED}{f"X===X NO SE ENCUENTRAN RECETAS EN EL DIA {day_name.upper() if day_name else ""} X===X":^40}{END}"
                        )
            else:
                print(f"\n{RED}{"X===X NO SE ENCUENTRAN RECETAS X===X":^40}{END}")

        elif selected == 3:
            mis_recetas = f.get_user_recipes(user_id)
            if mis_recetas:
                day = menu_options(
                    f.get_days_list(),
                    "Por favor, seleccione el dia donde reemplazar la receta: ",
                )
                if int(day) != 0:
                    day_name = f.get_day_by_id(int(day))
                    mt = menu_options(
                        f.get_mealtype_list(),
                        "Por favor, seleccione el tipo de comida: ",
                        False,
                    )
                    selected_recipes = f.get_day_recipes_mealtype(
                        user_id, int(day) - 1, int(mt) - 1
                    )
                    if selected_recipes:
                        recipe_names = [r[2] for r in selected_recipes]

                        target = menu_options(
                            [r[2] for r in selected_recipes],
                            "Selecciona la receta a reemplazar: ",
                            False,
                        )

                        old_id = selected_recipes[target - 1][0]
                        new_recipe_list = [r for r in mis_recetas if r[0] != old_id]
                        new_recipe_names = [r[2] for r in new_recipe_list]

                        new_target = menu_options(
                            new_recipe_names, "Selecciona la nueva receta: ", False
                        )
                        old_recipe = f.get_recipe(selected_recipes[target - 1][0])
                        new_recipe = f.get_recipe(new_recipe_list[new_target - 1][0])

                        if old_recipe and new_recipe:
                            replace_result = f.replace_recipe_from_plan(
                                user_id,
                                old_recipe[0],
                                int(day) - 1,
                                int(mt) - 1,
                                new_recipe[0],
                            )
                            if replace_result:
                                print(
                                    f"{GREEN}Se ha reemplazado {old_recipe[2]} por {new_recipe[2]} con exito.{END}"
                                )
                            else:
                                print(f"{RED}Ha ocurrido un error, abortando...{END}")
                    else:
                        print(
                            f"\n{RED}{f"X===X NO SE ENCUENTRAN RECETAS EN EL DIA {day_name.upper() if day_name else ""} X===X":^40}{END}"
                        )
            else:
                print(f"\n{RED}{"X===X NO SE ENCUENTRAN RECETAS X===X":^40}{END}")


def ingredientes_menu(user_id):
    flag = True
    while flag:
        print(f"\n\n{CYAN}----------- MIS INGREDIENTES -----------{END}")
        mis_ingredientes = f.get_user_ingredients(user_id)

        if mis_ingredientes:
            d.display_ingredients(user_id)
            print()  # Blank Line
        else:
            print(f"{RED}No hay ingredientes para mostrar.\n{END}")

        selected = menu_options(INGREDIENT_OPTIONS)
        if selected == 0:  # Cancelar
            flag = False

        elif selected == 1:  # Agregar Ingrediente
            nombre = input(f"{LIGHT_BLUE}Nombre del ingrediente: {END}")
            while not v.validate_alphabetic(nombre) or nombre == "":
                nombre = input(f"{RED}Error, ingrese un nombre valido: {END}")

            units = [i[1] for i in data.units]
            unit_id = menu_options(
                units, "Por favor ingrese el ID de la unidad: ", False
            )
            f.add_ingredient(int(user_id), nombre, unit_id - 1)

        elif selected == 2:  # Eliminar Ingrediente
            if mis_ingredientes:
                print(f"{CYAN}Mis ingredientes:{END}")
                ingredient_opt = menu_options(
                    [i[2] for i in mis_ingredientes],
                    "Por favor ingrese el numero del ingrediente a eliminar: ",
                )
                if ingredient_opt != 0:
                    selected_ing = mis_ingredientes[ingredient_opt - 1]

                    ingredient_deleted = f.delete_ingredient(user_id, selected_ing[0])
                    if ingredient_deleted:
                        print(
                            f"El ingrediente {selected_ing[2]} ha sido eliminado correctamente."
                        )
                    else:
                        print(f"{RED}Error al eliminar el ingrediente {selected_ing[2]}.{END}")
            else:
                print("No hay ingredientes para eliminar.")

        elif selected == 3:  # Editar Ingrediente
            if mis_ingredientes:
                print("Mis ingredientes:")
                ingredient_opt = menu_options(
                    [i[2] for i in mis_ingredientes],
                    "Por favor ingrese el numero del ingrediente a editar: ",
                )
                if ingredient_opt:
                    selected = mis_ingredientes[ingredient_opt - 1]
                    ingredient_id = selected[0]

                    new_ingredient_name = input(f"{LIGHT_BLUE}Ingrese el nuevo nombre o presione enter para no modificar: {END}")
                    while not v.validate_edit_name(new_ingredient_name):
                        new_ingredient_name = input(
                            f"{LIGHT_BLUE}Ingrese un nombre valido o presione enter para no modificar: {END}"
                        )

                    units = [i[1] for i in data.units]
                    for i in range(len(units)):
                        print(f"{i + 1} - {units[i]}")

                    new_ingredient_unit_id = input(
                        f"{LIGHT_BLUE}Ingrese el numero de la unidad o presione enter para no modificar: {END}"
                    )

                    while not v.validate_edit_unit(new_ingredient_unit_id):
                        new_ingredient_unit_id = input(
                            f"{LIGHT_BLUE}Ingrese una opcion correcta o presione enter para no modificar: {END}"
                        )
                    if new_ingredient_unit_id != "":
                        while int(new_ingredient_unit_id) <= 0 or int(
                            new_ingredient_unit_id
                        ) > len(units):
                            new_ingredient_unit_id = input(
                                F"{LIGHT_BLUE}Por favor, ingrese una opcion valida: {END}"
                            )

                    if (
                        len(new_ingredient_name) == 0
                        and len(new_ingredient_unit_id) == 0
                    ):
                        print("No se ha modificado el ingrediente.")
                    else:
                        ingredient_name = selected[2]
                        ingredient_unit = selected[3]

                        if len(new_ingredient_name) > 0:
                            ingredient_name = new_ingredient_name
                        if len(new_ingredient_unit_id) > 0:
                            ingredient_unit = int(new_ingredient_unit_id) - 1

                        f.update_ingredient(
                            user_id, ingredient_id, ingredient_name, ingredient_unit
                        )
                        print(
                            f"{GREEN}El ingrediente {selected[2]} ha sido modificado correctamente.{LIGHT_BLUE}"
                        )
            else:
                print(f"{RED}No hay ingredientes para editar.{END}")


def recetas_menu(user_id):
    flag = True
    while flag:

        print(f"\n\n{CYAN}-------------- MIS RECETAS -------------{END}")
        selected = menu_options(RECIPE_OPTIONS)

        if selected == 0:
            flag = False
        elif selected == 1:
            user_recipes = f.get_user_recipes(user_id)
            if user_recipes:
                recipe_opt = menu_options(
                    [r[2] for r in user_recipes],
                    "Seleccione la receta a ver: ",
                )
                if recipe_opt != 0:
                    receta = user_recipes[recipe_opt - 1]
                    nombres_ingredientes = f.get_recipe_ingredient_names(receta[0])
                    print(f"\n{CYAN}========== {receta[2].upper()} =========={END}")
                    print(f"{LIGHT_BLUE}Instrucciones:{END} {receta[3]}")
                    print(f"{LIGHT_BLUE}Ingredientes:{END}")
                    if nombres_ingredientes:
                        for nombre in nombres_ingredientes:
                            print(f"  - {nombre}")
                    else:
                        print(f"  {RED}Sin ingredientes cargados.{END}")
                    input(f"\n{LIGHT_BLUE}Presione Enter para continuar...{END}")
            else:
                print(f"\n{RED}{'X===X NO SE ENCUENTRAN RECETAS X===X':^40}{END}")
                
        elif selected == 2:
            title = input(f"{LIGHT_BLUE}Porfavor, ingrese el nombre de la receta: {END}")
            while not v.validate_alphabetic(title) or title == "":
                title = input(f"{LIGHT_BLUE}Ingrese un nombre valido: {END}")

            instructions = input(f"{LIGHT_BLUE}Ingrese las instrucciones de la receta: {END}")

            mis_ingredientes = f.get_user_ingredients(user_id)
            ingredient_opts = []

            if mis_ingredientes:
                ingredient_opt = menu_options(
                    [i[2] for i in mis_ingredientes],
                    "Seleccione el ingrediente, 0 para terminar: ",
                )
                while ingredient_opt != 0:
                    selected_ingredient = mis_ingredientes[ingredient_opt - 1]
                    unit_name = f.get_unit_by_id(selected_ingredient[3])
                    try:
                        cantidad = float(input(f"Ingrese la cantidad en {unit_name}: "))
                    except ValueError:
                        print("Ingrese un numero valido.")
                        continue
                    ingredient_opts.append((selected_ingredient, cantidad))

                    ingredient_opt = menu_options(
                        [i[2] for i in mis_ingredientes],
                        "Seleccione el ingrediente, 0 para terminar: ",
                    )

                f.add_recipe(user_id, title, instructions)
                nueva_receta = f.get_user_recipes(user_id)

                if nueva_receta:
                    recipe_id = nueva_receta[-1][0]
                    for ing, cantidad in ingredient_opts:
                        f.add_ingredient_to_recipe(user_id, recipe_id, ing[0], cantidad)
                    print(
                        f"\n{GREEN}Receta '{title}' creada con {len(ingredient_opts)} ingrediente(s).{END}"
                    )

            else:
                print(
                    f"{RED}{"No puedes crear una receta sin ingredientes.\nAgrega algunos primero":^40}{END}"
                )

        elif selected == 3:
            user_recipes = f.get_user_recipes(user_id)
            if user_recipes:
                recipe_opt = menu_options(
                    [i[2] for i in user_recipes],
                    "Porfavor seleccione la receta que desea eliminar: ",
                )
                result = f.delete_recipe(user_id, user_recipes[recipe_opt - 1][0])
                if result:
                    print(
                        f"\n{GREEN}La receta {user_recipes[recipe_opt - 1][2]} ha sido eliminada correctamente{END}"
                    )
            else:
                print(f"\n{RED}{"X===X NO SE ENCUENTRAN RECETAS X===X":^40}{END}")

        elif selected == 4:
            user_recipes = f.get_user_recipes(user_id)
            if user_recipes:
                recipe_opt = menu_options(
                    [r[2] for r in user_recipes], "Seleccione la receta a editar: "
                )
                if recipe_opt:
                    selected_recipe = user_recipes[recipe_opt - 1]
                    branch_opt = menu_options(
                        [
                            "Editar datos (nombre e instrucciones)",
                            "Editar Ingredientes",
                        ],
                        "Seleccione el item a editar: ",
                        False,
                    )

                    if branch_opt == 1:
                        print(
                            f"{LIGHT_BLUE}Receta:{END} {selected_recipe[2]}\n{LIGHT_BLUE}Instrucciones:{END} {selected_recipe[3]}"
                        )

                        new_recipe_name = input(
                            f"{LIGHT_BLUE}Ingrese el nuevo nombre o Enter para saltear: {END}"
                        )
                        while not v.validate_edit_name(new_recipe_name):
                            new_recipe_name = input(
                                f"{LIGHT_BLUE}Ingrese un nombre valido o Enter para saltear: {END}"
                            )

                        new_recipe_instructions = input(
                            f"{LIGHT_BLUE}Ingrese las nuevas instrucciones o Enter para saltear: {END}"
                        )
                        while not v.validate_edit_name(new_recipe_instructions):
                            new_recipe_instructions = input(
                                f"{LIGHT_BLUE}Ingrese unas instrucciones validas o Enter para saltear: {END}"
                            )

                        final_name = (
                            new_recipe_name if new_recipe_name else selected_recipe[2]
                        )
                        final_instructions = (
                            new_recipe_instructions
                            if new_recipe_instructions
                            else selected_recipe[3]
                        )

                        f.update_recipe(
                            user_id, selected_recipe[0], final_name, final_instructions
                        )
                        print(f'{GREEN}Se han realizado los cambios a "{final_name}".{END}')

                    elif branch_opt == 2:
                        edit_ing_opt = menu_options(
                            ["Agregar Ingrediente", "Eliminar Ingrediente"]
                        )

                        if edit_ing_opt == 1:
                            mis_ingredientes = f.get_user_ingredients(user_id)
                            if mis_ingredientes:
                                ingredient_opt = menu_options(
                                    [i[2] for i in mis_ingredientes],
                                    "Seleccione el ingrediente a agregar, 0 para terminar: ",
                                )
                                while ingredient_opt != 0:
                                    selected_ingredient = mis_ingredientes[
                                        ingredient_opt - 1
                                    ]
                                    unit_name = f.get_unit_by_id(selected_ingredient[3])
                                    cantidad = float(
                                        input(f"{LIGHT_BLUE}Ingrese la cantidad en {unit_name}: {END}")
                                    )
                                    f.add_ingredient_to_recipe(
                                        user_id,
                                        selected_recipe[0],
                                        selected_ingredient[0],
                                        cantidad,
                                    )
                                    ingredient_opt = menu_options(
                                        [i[2] for i in mis_ingredientes],
                                        "Seleccione el ingrediente a agregar, 0 para terminar: ",
                                    )
                                print(
                                    f'{RED}Ingredientes agregados a "{selected_recipe[2]}".{END}'
                                )
                            else:
                                print(f"{RED}No hay ingredientes disponibles para agregar.{END}")

                        elif edit_ing_opt == 2:
                            recipe_ingredients = f.get_ingredientlist_from_recipe(
                                selected_recipe[0]
                            )
                            if recipe_ingredients:
                                ingredient_names = []
                                for ri in recipe_ingredients:
                                    ing = f.get_ingredient(ri[2])
                                    nombre = ing[2] if ing else f"ID {ri[2]}"
                                    unit_name = f.get_unit_by_id(ing[3]) if ing else ""
                                    cantidad = ri[3] if ri[3] is not None else "a gusto"
                                    ingredient_names.append(
                                        f"{nombre} ({cantidad} {unit_name})"
                                    )

                                ingredient_opt = menu_options(
                                    ingredient_names,
                                    "Seleccione el ingrediente a eliminar: ",
                                )
                                if ingredient_opt != 0:
                                    target_ri = recipe_ingredients[ingredient_opt - 1]
                                    f.delete_ingredient_from_recipe(
                                        user_id, selected_recipe[0], target_ri[2]
                                    )
                                    print(
                                        f'{GREEN}Ingrediente eliminado de "{selected_recipe[2]}".{END}'
                                    )
                            else:
                                print(
                                    f"{RED}Esta receta no tiene ingredientes para eliminar.{END}"
                                )
            else:
                print(f"\n{RED}{'X===X NO SE ENCUENTRAN RECETAS X===X':^40}{END}")
