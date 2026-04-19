import components.validation as v
from lib.constants import *
from components.auth import *
import db.data as data
import db.data_crud as f
import components.display as d


def menu_options(menu, message="Ingrese la opcion deseada: ", zero=True):
    for i in range(len(menu)):
        print(f"{i + 1} - {menu[i]}")
    if zero:
        print("0 - Volver/Salir")

    option = input(message)
    print()
    while not v.validate_menu_option(option, menu):
        option = input("Error. Ingrese la opcion nuevamente: ")

    return int(option)


def user_menu():
    user_id = str(data.user_cache[0])

    flag = True
    while flag:

        d.display_plan(user_id)
        print(f"\n\n---------- PANEL DE USUARIO -----------")
        selected = menu_options(USER_OPTIONS)

        if selected == 0:
            flag = False
        elif selected == 1:
            plan_menu(user_id)
        elif selected == 2:
            recetas_menu(user_id)
        elif selected == 3:
            ingredientes_menu(user_id)


def plan_menu(user_id):
    flag = True
    while flag:

        print("\n\n-------- GESTIÓN DE PLAN SEMANAL -------")
        selected = menu_options(PLAN_OPTIONS)
        mis_recetas = f.get_user_recipes(user_id)
        if selected == 0:
            flag = False

        elif selected == 1:
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
                        [r[2] for r in mis_recetas], "Seleccione la receta a agregar"
                    )
                    if int(recipe_selected) != 0:
                        f.add_recipe_to_plan(
                            user_id,
                            mis_recetas[recipe_selected - 1][0],
                            day - 1,
                            mt - 1,
                        )
            else:
                print(f"\n{"X===X NO SE ENCUENTRAN RECETAS X===X":^40}")

        elif selected == 2:
            if mis_recetas:
                day = menu_options(
                    f.get_days_list(),
                    "Por favor, seleccione el dia donde eliminar la receta: ",
                )
                if int(day) != 0:
                    day_name = f.get_days_by_id(int(day))
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
                        while target <= 0:
                            target = menu_options(
                                [r[2] for r in selected_recipes],
                                "Por favor, ingrese una receta valida: ",
                                False,
                            )
                        old_recipe = f.get_recipe(selected_recipes[target - 1][0])
                        if old_recipe:
                            f.remove_recipe_from_plan(
                                user_id, old_recipe[0], int(day) - 1, int(mt) - 1
                            )
                    else:
                        print(
                            f"\n{f"X===X NO SE ENCUENTRAN RECETAS EN EL DIA {day_name.upper() if day_name else ""} X===X":^40}"
                        )
            else:
                print(f"\n{"X===X NO SE ENCUENTRAN RECETAS X===X":^40}")

        elif selected == 3:
            if mis_recetas:
                day = menu_options(
                    f.get_days_list(),
                    "Por favor, seleccione el dia donde reemplazar la receta: ",
                )
                if int(day) != 0:
                    day_name = f.get_days_by_id(int(day))
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
                        while target <= 0:
                            target = menu_options(
                                recipe_names,
                                "Por favor, ingrese una receta valida: ",
                                False,
                            )

                        old_id = selected_recipes[target - 1][0]
                        new_recipe_list = [r for r in mis_recetas if r[0] != old_id]
                        new_recipe_names = [r[2] for r in new_recipe_list]

                        new_target = menu_options(
                            new_recipe_names, "Selecciona la nueva receta: ", False
                        )
                        while new_target <= 0:
                            new_target = menu_options(
                                new_recipe_names,
                                "Por favor, ingrese una receta valida: ",
                                False,
                            )

                        old_recipe = f.get_recipe(selected_recipes[target - 1][0])
                        new_recipe = f.get_recipe(new_recipe_list[new_target - 1][0])

                        if old_recipe and new_recipe:
                            f.replace_recipe_from_plan(
                                user_id,
                                old_recipe[0],
                                int(day) - 1,
                                int(mt) - 1,
                                new_recipe[0],
                            )
                    else:
                        print(
                            f"\n{f"X===X NO SE ENCUENTRAN RECETAS EN EL DIA {day_name.upper() if day_name else ""} X===X":^40}"
                        )
            else:
                print(f"\n{"X===X NO SE ENCUENTRAN RECETAS X===X":^40}")


def ingredientes_menu(user_id):
    flag = True
    while flag:
        print("\n\n----------- MIS INGREDIENTES -----------")
        mis_ingredientes = f.get_user_ingredients(user_id)

        if mis_ingredientes:
            d.display_ingredients(user_id)
            print()  # Blank Line
        else:
            print("No hay ingredientes para mostrar.\n")

        selected = menu_options(INGREDIENT_OPTIONS)
        if selected == 0:  # Cancelar
            flag = False

        elif selected == 1:  # Agregar Ingrediente
            nombre = input("Nombre del ingrediente: ")
            while not v.validate_alphabetic(nombre) or nombre == "":
                nombre = input("Error, ingrese un nombre valido: ")

            units = [i[1] for i in data.units]
            unit_id = (
                menu_options(units, "Por favor ingrese el ID de la unidad: ", False) - 1
            )
            while int(unit_id) <= 0 or int(unit_id) > len(units):
                unit_id = int(input("Por favor, ingrese una opcion valida: "))
            f.add_ingredient(int(user_id), nombre, unit_id)

        elif selected == 2:  # Eliminar Ingrediente
            if mis_ingredientes:
                print("Mis ingredientes:")
                ingredient_opt = (
                    menu_options(
                        [i[2] for i in mis_ingredientes],
                        "Por favor ingrese el numero del ingrediente a eliminar: ",
                    )
                    - 1
                )
                selected_ing = mis_ingredientes[ingredient_opt]

                ingredient_deleted = f.delete_ingredient(user_id, selected_ing[0])
                if ingredient_deleted:
                    print(
                        f"El ingrediente {selected_ing[2]} ha sido eliminado correctamente."
                    )
                else:
                    print(f"Error al eliminar el ingrediente {selected_ing[2]}.")
            else:
                print("No hay ingredientes para eliminar.")

        elif selected == 3:  # Editar Ingrediente
            if mis_ingredientes:
                print("Mis ingredientes:")
                ingredient_opt = (
                    menu_options(
                        [i[2] for i in mis_ingredientes],
                        "Por favor ingrese el numero del ingrediente a editar: ",
                    )
                    - 1
                )
                selected = mis_ingredientes[ingredient_opt]
                ingredient_id = selected[0]

                new_ingredient_name = input(
                    "Ingrese el nuevo nombre o presione enter para no modificar: "
                )
                while not v.validate_edit_name(new_ingredient_name):
                    new_ingredient_name = input(
                        "Ingrese un nombre valido o presione enter para no modificar: "
                    )

                units = [i[1] for i in data.units]
                for i in range(len(units)):
                    print(f"{i + 1} - {units[i]}")

                new_ingredient_unit_id = input(
                    "Ingrese el numero de la unidad o presione enter para no modificar: "
                )

                while not v.validate_edit_unit(new_ingredient_unit_id):
                    new_ingredient_unit_id = input(
                        "Ingrese una opcion correcta o presione enter para no modificar: "
                    )
                if new_ingredient_unit_id is not "":
                    while int(new_ingredient_unit_id) <= 0 or int(
                        new_ingredient_unit_id
                    ) > len(units):
                        new_ingredient_unit_id = input(
                            "Por favor, ingrese una opcion valida: "
                        )

                if len(new_ingredient_name) == 0 and len(new_ingredient_unit_id) == 0:
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
                        f"El ingrediente {selected[2]} ha sido modificado correctamente."
                    )
            else:
                print("No hay ingredientes para editar.")


def recetas_menu(user_id):
    flag = True
    while flag:

        print("\n\n-------------- MIS RECETAS -------------")
        selected = menu_options(RECIPE_OPTIONS)

        if selected == 0:
            flag = False
        elif selected == 1:
            title = input("Porfavor, ingrese el nombre de la receta: ")
            while not v.validate_alphabetic(title) or title == "":
                title = input("Ingrese un nombre valido: ")

            instructions = input("Ingrese las instrucciones de la receta: ")

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
                    cantidad = float(input(f"Ingrese la cantidad en {unit_name}: "))
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
                    print(f"\nReceta '{title}' creada con {len(ingredient_opts)} ingrediente(s).")
                    
            else:
                print(
                    f"{"No puedes crear una receta sin ingredientes.\nAgrega algunos primero":^40}"
                )

        elif selected == 2:
            user_recipes = f.get_user_recipes(user_id)
            if user_recipes:
                recipe_opt = menu_options(
                    [i[2] for i in user_recipes],
                    "Porfavor seleccione la receta que desea eliminar: ",
                )
                result = f.delete_recipe(user_id, user_recipes[recipe_opt - 1][0])
                if result:
                    print(
                        f"\nLa receta {user_recipes[recipe_opt - 1][2]} ha sido eliminada correctamente"
                    )
            else:
                print(f"\n{"X===X NO SE ENCUENTRAN RECETAS X===X":^40}")

        elif selected == 3:
            user_recipes = f.get_user_recipes(user_id)
            if user_recipes:
                recipe_opt = menu_options([r[2] for r in user_recipes], "Seleccione la receta a editar: ")
                if recipe_opt:
                    selected_recipe = user_recipes[recipe_opt - 1]
                    branch_opt = menu_options(["Editar datos (nombre e instrucciones)", "Editar Ingredientes"], "Seleccione el item a editar: ", False)
                    while branch_opt == 0:
                        branch_opt = menu_options(["Editar datos (nombre e instrucciones)", "Editar Ingredientes"], "Seleccione un item valido: ", False)
                        
                    if branch_opt == 1:
                        print(f"Receta: {selected_recipe[2]}\nInstrucciones: {selected_recipe[3]}")
                        
                        new_recipe_name = input("Ingrese el nuevo nombre o Enter para saltear: ")
                        while not v.validate_edit_name(new_recipe_name):
                            new_recipe_name = input("Ingrese un nombre valido o Enter para saltear: ")
                        
                        new_recipe_instructions = input("Ingrese las nuevas instrucciones o Enter para saltear: ")
                        while not v.validate_edit_name(new_recipe_instructions):
                            new_recipe_instructions = input("Ingrese unas instrucciones validas o Enter para saltear: ")

                        final_name = new_recipe_name if new_recipe_name else selected_recipe[2]
                        final_instructions = new_recipe_instructions if new_recipe_instructions else selected_recipe[3]

                        f.update_recipe(user_id, selected_recipe[0], final_name, final_instructions)
                        print(f"Se han realizado los cambios a \"{final_name}\".")

                    elif branch_opt == 2:
                        edit_ing_opt = menu_options(["Agregar Ingrediente", "Eliminar Ingrediente"])

                        if edit_ing_opt == 1:
                            mis_ingredientes = f.get_user_ingredients(user_id)
                            if mis_ingredientes:
                                ingredient_opt = menu_options(
                                    [i[2] for i in mis_ingredientes],
                                    "Seleccione el ingrediente a agregar, 0 para terminar: ",
                                )
                                while ingredient_opt != 0:
                                    selected_ingredient = mis_ingredientes[ingredient_opt - 1]
                                    unit_name = f.get_unit_by_id(selected_ingredient[3])
                                    cantidad = float(input(f"Ingrese la cantidad en {unit_name}: "))
                                    f.add_ingredient_to_recipe(user_id, selected_recipe[0], selected_ingredient[0], cantidad)
                                    ingredient_opt = menu_options(
                                        [i[2] for i in mis_ingredientes],
                                        "Seleccione el ingrediente a agregar, 0 para terminar: ",
                                    )
                                print(f"Ingredientes agregados a \"{selected_recipe[2]}\".")
                            else:
                                print("No hay ingredientes disponibles para agregar.")

                        elif edit_ing_opt == 2:
                            recipe_ingredients = f.get_ingredientlist_from_recipe(selected_recipe[0])
                            if recipe_ingredients:
                                ingredient_names = []
                                for ri in recipe_ingredients:
                                    ing = f.get_ingredient(ri[2])
                                    nombre = ing[2] if ing else f"ID {ri[2]}"
                                    unit_name = f.get_unit_by_id(ing[3]) if ing else ""
                                    cantidad = ri[3] if ri[3] is not None else "a gusto"
                                    ingredient_names.append(f"{nombre} ({cantidad} {unit_name})")

                                ingredient_opt = menu_options(
                                    ingredient_names,
                                    "Seleccione el ingrediente a eliminar: ",
                                )
                                if ingredient_opt != 0:
                                    target_ri = recipe_ingredients[ingredient_opt - 1]
                                    f.delete_ingredient_from_recipe(user_id, selected_recipe[0], target_ri[2])
                                    print(f"Ingrediente eliminado de \"{selected_recipe[2]}\".")
                            else:
                                print("Esta receta no tiene ingredientes para eliminar.")
            else:
                print(f"\n{'X===X NO SE ENCUENTRAN RECETAS X===X':^40}")
