import components.validation as v
from lib.constants import *
from components.auth import *
import db.data as data
import db.data_crud as f
import components.display as d
from lib.colors import *
from lib.utils import menu_options, format_fav_recipe, format_fav_ingredient


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
                        [r["title"] for r in mis_recetas],
                        "Seleccione la receta a agregar: ",
                        False,
                    )
                    f.add_recipe_to_plan(
                        user_id,
                        mis_recetas[recipe_selected - 1]["id"],
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
                    day_name = f.get_day_by_id(int(day) - 1)
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
                            [r["title"] for r in selected_recipes],
                            "Selecciona la receta a eliminar: ",
                            False,
                        )
                        recipe_en_plan = f.get_recipe_from_plan(
                            user_id,
                            selected_recipes[target - 1]["id"],
                            int(day) - 1,
                            int(mt) - 1,
                        )
                        if recipe_en_plan:
                            f.remove_recipe_from_plan(
                                user_id, recipe_en_plan["id"], int(day) - 1, int(mt) - 1
                            )
                    else:
                        print(
                            f"\n{RED}{f'X===X NO SE ENCUENTRAN RECETAS EN EL DIA {day_name.upper() if day_name else ""} X===X':^40}{END}"
                        )
            else:
                print(f"\n{RED}{'X===X NO SE ENCUENTRAN RECETAS X===X':^40}{END}")

        elif selected == 3:
            mis_recetas = f.get_user_recipes(user_id)
            if mis_recetas:
                day = menu_options(
                    f.get_days_list(),
                    "Por favor, seleccione el dia donde reemplazar la receta: ",
                )
                if int(day) != 0:
                    day_name = f.get_day_by_id(int(day) - 1)
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
                            [r["title"] for r in selected_recipes],
                            "Selecciona la receta a reemplazar: ",
                            False,
                        )

                        old_id = selected_recipes[target - 1]["id"]

                        old_recipe = f.get_recipe_from_plan(
                            user_id, old_id, int(day) - 1, int(mt) - 1
                        )
                        if not old_recipe:
                            print(
                                f"{RED}No se encontró la receta en ese slot del plan.{END}"
                            )
                            continue

                        new_recipe_list = [r for r in mis_recetas if r["id"] != old_id]
                        new_recipe_names = [r["title"] for r in new_recipe_list]

                        new_target = menu_options(
                            new_recipe_names, "Selecciona la nueva receta: ", False
                        )
                        new_recipe = new_recipe_list[new_target - 1]

                        replace_result = f.replace_recipe_from_plan(
                            user_id,
                            old_recipe["id"],
                            int(day) - 1,
                            int(mt) - 1,
                            new_recipe["id"],
                        )
                        if replace_result:
                            print(
                                f"{GREEN}Se ha reemplazado {old_recipe['title']} por {new_recipe['title']} con exito.{END}"
                            )
                        else:
                            print(f"{RED}Ha ocurrido un error, abortando...{END}")
                    else:
                        print(
                            f"\n{RED}{f'X===X NO SE ENCUENTRAN RECETAS EN EL DIA {day_name.upper() if day_name else ""} X===X':^40}{END}"
                        )
            else:
                print(f"\n{RED}{'X===X NO SE ENCUENTRAN RECETAS X===X':^40}{END}")


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
        
        elif selected == 1: # Ver Ingredientes
            user_ingredients = f.get_user_ingredients(user_id)
            if user_ingredients:
                favourites = data.user_cache["favourites"]["ingredients"]
                recipe_opt = menu_options(
                    [format_fav_ingredient(r, favourites) for r in user_ingredients],
                    "Seleccione el ingrediente a ver: ",
                )
                if recipe_opt != 0:
                    ingrediente = user_ingredients[recipe_opt - 1]
                    category = f.get_category_by_id(ingrediente['category'])
                    unit = f.get_unit_by_id(ingrediente['unit_id'])
                    print(
                        f"\n{CYAN}========== {ingrediente['name'].upper()} =========={END}"
                    )
                    print(f"{LIGHT_BLUE}Categoria:{END} {category}")
                    print(f"{LIGHT_BLUE}Unidad:{END} {unit}")
                        
                    # Opcion favorito
                    fav_state = True if ingrediente["id"] in favourites else False
                    fav_msg = 'Ingrese 1 para agregar a favoritos'
                    
                    if fav_state:
                        fav_msg = 'Ingrese 1 para eliminar de favoritos'
                        
                    msg = f'\n{YELLOW}{fav_msg}{END}\n{LIGHT_BLUE}Presione Enter para continuar...{END}: '
                        
                    res = input(msg)
                    while res is not "" and res is not "1":
                        res = input(msg)
                        
                    if res == "1":
                        if fav_state:
                            if f.fav_ingredient(data.user_cache, ingrediente, "remove"):
                                print(f'{YELLOW}{BOLD}La receta se ha eliminado a favoritos{END}')
                            else:
                                print(f'{RED}Se ha producido un error.{END}')
                        else:
                            if f.fav_ingredient(data.user_cache, ingrediente, "add"):
                                print(f'{YELLOW}{BOLD}La receta se ha agregado a favoritos{END}')
                            else:
                                print(f'{RED}Se ha producido un error.{END}')
            else:
                print(f"\n{RED}{'X===X NO SE ENCUENTRAN RECETAS X===X':^40}{END}")
        
        elif selected == 2:  # Agregar Ingrediente
            nombre = input(f"{LIGHT_BLUE}Nombre del ingrediente: {END}")
            while not v.validate_alphabetic(nombre) or nombre == "":
                nombre = input(f"{RED}Error, ingrese un nombre valido: {END}")

            units = [i["name"] for i in data.units]
            unit_id = menu_options(
                units, "Por favor ingrese el ID de la unidad: ", False
            )

            categories = f.get_category_list()
            category_id = menu_options(
                categories, "Por favor ingrese el ID de la categoria: ", False
            )
            f.add_ingredient(int(user_id), nombre, unit_id - 1, category_id - 1)

        elif selected == 3:  # Eliminar Ingrediente
            if mis_ingredientes:
                print(f"{CYAN}Mis ingredientes:{END}")
                ingredient_opt = menu_options(
                    [i["name"] for i in mis_ingredientes],
                    "Por favor ingrese el numero del ingrediente a eliminar: ",
                )
                if ingredient_opt != 0:
                    selected_ing = mis_ingredientes[ingredient_opt - 1]

                    ingredient_deleted = f.delete_ingredient(
                        user_id, selected_ing["id"]
                    )
                    if ingredient_deleted:
                        print(
                            f"El ingrediente {selected_ing['name']} ha sido eliminado correctamente."
                        )
                    else:
                        print(
                            f"{RED}Error al eliminar el ingrediente {selected_ing['name']}.{END}"
                        )
            else:
                print("No hay ingredientes para eliminar.")

        elif selected == 4:  # Editar Ingrediente
            if mis_ingredientes:
                print("Mis ingredientes:")
                ingredient_opt = menu_options(
                    [i["name"] for i in mis_ingredientes],
                    "Por favor ingrese el numero del ingrediente a editar: ",
                )
                if ingredient_opt:
                    selected = mis_ingredientes[ingredient_opt - 1]
                    ingredient_id = selected["id"]

                    new_ingredient_name = input(
                        f"{LIGHT_BLUE}Ingrese el nuevo nombre o presione enter para no modificar: {END}"
                    )
                    while not v.validate_edit_name(new_ingredient_name):
                        new_ingredient_name = input(
                            f"{LIGHT_BLUE}Ingrese un nombre valido o presione enter para no modificar: {END}"
                        )

                    units = [i["name"] for i in data.units]
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
                                f"{LIGHT_BLUE}Por favor, ingrese una opcion valida: {END}"
                            )

                    categories = f.get_category_list()
                    for i in range(len(categories)):
                        print(f"{i + 1} - {categories[i]}")

                    new_ingredient_category_id = input(
                        f"{LIGHT_BLUE}Ingrese el numero de la categoria o presione enter para no modificar: {END}"
                    )

                    while not v.validate_edit_category(new_ingredient_category_id):
                        new_ingredient_category_id = input(
                            f"{LIGHT_BLUE}Ingrese una opcion correcta o presione enter para no modificar: {END}"
                        )

                    if (
                        len(new_ingredient_name) == 0
                        and len(new_ingredient_unit_id) == 0
                        and len(new_ingredient_category_id) == 0
                    ):
                        print("No se ha modificado el ingrediente.")
                    else:
                        ingredient_name = selected["name"]
                        ingredient_unit = selected["unit_id"]
                        ingredient_category = selected.get("category")

                        if len(new_ingredient_name) > 0:
                            ingredient_name = new_ingredient_name
                        if len(new_ingredient_unit_id) > 0:
                            ingredient_unit = int(new_ingredient_unit_id) - 1
                        if len(new_ingredient_category_id) > 0:
                            ingredient_category = int(new_ingredient_category_id) - 1

                        f.update_ingredient(
                            user_id,
                            ingredient_id,
                            ingredient_name,
                            ingredient_unit,
                            ingredient_category,
                        )
                        print(
                            f"{GREEN}El ingrediente {selected['name']} ha sido modificado correctamente.{LIGHT_BLUE}"
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
                favourites = data.user_cache["favourites"]["recipes"]
                recipe_opt = menu_options(
                    [format_fav_recipe(r, favourites) for r in user_recipes],
                    "Seleccione la receta a ver: ",
                )
                if recipe_opt != 0:
                    receta = user_recipes[recipe_opt - 1]
                    nombres_ingredientes = f.get_recipe_ingredient_data(receta["id"])
                    print(
                        f"\n{CYAN}========== {receta['title'].upper()} =========={END}"
                    )
                    print(f"{LIGHT_BLUE}Instrucciones:{END} {receta['instructions']}")
                    print(f"{LIGHT_BLUE}Ingredientes:{END}")
                    if nombres_ingredientes:
                        for nombre in nombres_ingredientes:
                            print(f"  - {nombre}")
                    else:
                        print(f"  {RED}Sin ingredientes cargados.{END}")
                        
                    # Opcion favorito
                    fav_state = True if receta["id"] in favourites else False
                    fav_msg = 'Ingrese 1 para agregar a favoritos'
                    
                    if fav_state:
                        fav_msg = 'Ingrese 1 para eliminar de favoritos'
                    msg = f'\n{YELLOW}{fav_msg}{END}\n{LIGHT_BLUE}Presione Enter para continuar...{END}: '
                        
                    res = input(msg)
                    while res is not "" and res is not "1":
                        res = input(msg)
                        
                    if res == "1":
                        if fav_state:
                            if f.fav_recipe(data.user_cache, receta, "remove"):
                                print(f'{YELLOW}{BOLD}La receta se ha eliminado a favoritos{END}')
                            else:
                                print(f'{RED}Se ha producido un error.{END}')
                        else:
                            if f.fav_recipe(data.user_cache, receta, "add"):
                                print(f'{YELLOW}{BOLD}La receta se ha agregado a favoritos{END}')
                            else:
                                print(f'{RED}Se ha producido un error.{END}')
            else:
                print(f"\n{RED}{'X===X NO SE ENCUENTRAN RECETAS X===X':^40}{END}")

        elif selected == 2:
            title = input(
                f"{LIGHT_BLUE}Porfavor, ingrese el nombre de la receta: {END}"
            )
            while not v.validate_alphabetic(title) or title == "":
                title = input(f"{LIGHT_BLUE}Ingrese un nombre valido: {END}")

            instructions = input(
                f"{LIGHT_BLUE}Ingrese las instrucciones de la receta: {END}"
            )

            mis_ingredientes = f.get_user_ingredients(user_id)
            ingredient_opts = []

            if mis_ingredientes:
                ingredient_opt = menu_options(
                    [i["name"] for i in mis_ingredientes],
                    "Seleccione el ingrediente, 0 para terminar: ",
                )
                while ingredient_opt != 0:
                    selected_ingredient = mis_ingredientes[ingredient_opt - 1]
                    unit_name = f.get_unit_by_id(selected_ingredient["unit_id"])
                    try:
                        cantidad = float(input(f"Ingrese la cantidad en {unit_name}: "))
                    except ValueError:
                        print("Ingrese un numero valido.")
                        continue
                    ingredient_opts.append((selected_ingredient, cantidad))

                    ingredient_opt = menu_options(
                        [i["name"] for i in mis_ingredientes],
                        "Seleccione el ingrediente, 0 para terminar: ",
                    )

                f.add_recipe(user_id, title, instructions)
                nueva_receta = f.get_user_recipes(user_id)

                if nueva_receta:
                    recipe_id = nueva_receta[-1]["id"]
                    for ing, cantidad in ingredient_opts:
                        f.add_ingredient_to_recipe(
                            user_id, recipe_id, ing["id"], cantidad
                        )
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
                favourites = data.user_cache["favourites"]["recipes"]
                recipe_opt = menu_options(
                    [format_fav_recipe(r, favourites) for r in user_recipes],
                    "Seleccione la receta a ver: ",
                )
                if recipe_opt is not 0:
                    receta_a_eliminar = user_recipes[recipe_opt - 1]
                    result = f.delete_recipe(user_id, receta_a_eliminar["id"])
                    if result:
                        print(
                            f"\n{GREEN}La receta {receta_a_eliminar['title']} ha sido eliminada correctamente{END}"
                        )
            else:
                print(f"\n{RED}{"X===X NO SE ENCUENTRAN RECETAS X===X":^40}{END}")

        elif selected == 4:
            user_recipes = f.get_user_recipes(user_id)
            print(user_recipes)
            if user_recipes:
                favourites = data.user_cache["favourites"]["recipes"]
                recipe_opt = menu_options(
                    [format_fav_recipe(r, favourites) for r in user_recipes],
                    "Seleccione la receta a editar: ",
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
                            f"{LIGHT_BLUE}Receta:{END} {selected_recipe["title"]}\n{LIGHT_BLUE}Instrucciones:{END} {selected_recipe["instructions"]}"
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
                            new_recipe_name
                            if new_recipe_name
                            else selected_recipe["title"]
                        )
                        final_instructions = (
                            new_recipe_instructions
                            if new_recipe_instructions
                            else selected_recipe["instructions"]
                        )

                        f.update_recipe(
                            user_id,
                            selected_recipe["id"],
                            final_name,
                            final_instructions,
                        )
                        print(
                            f'{GREEN}Se han realizado los cambios a "{final_name}".{END}'
                        )

                    elif branch_opt == 2:
                        edit_ing_opt = menu_options(
                            ["Agregar Ingrediente", "Eliminar Ingrediente"]
                        )

                        if edit_ing_opt == 1:
                            mis_ingredientes = f.get_user_ingredients(user_id)
                            if mis_ingredientes:
                                ingredient_opt = menu_options(
                                    [i["name"] for i in mis_ingredientes],
                                    "Seleccione el ingrediente a agregar, 0 para terminar: ",
                                )
                                while ingredient_opt != 0:
                                    selected_ingredient = mis_ingredientes[
                                        ingredient_opt - 1
                                    ]
                                    unit_name = f.get_unit_by_id(
                                        selected_ingredient["unit_id"]
                                    )
                                    cantidad = float(
                                        input(
                                            f"{LIGHT_BLUE}Ingrese la cantidad en {unit_name}: {END}"
                                        )
                                    )
                                    f.add_ingredient_to_recipe(
                                        user_id,
                                        selected_recipe["id"],
                                        selected_ingredient["id"],
                                        cantidad,
                                    )
                                    ingredient_opt = menu_options(
                                        [i["name"] for i in mis_ingredientes],
                                        "Seleccione el ingrediente a agregar, 0 para terminar: ",
                                    )
                                print(
                                    f'{RED}Ingredientes agregados a "{selected_recipe["title"]}".{END}'
                                )
                            else:
                                print(
                                    f"{RED}No hay ingredientes disponibles para agregar.{END}"
                                )

                        elif edit_ing_opt == 2:
                            recipe_ingredients = f.get_ingredientlist_from_recipe(
                                selected_recipe["id"]
                            )
                            if recipe_ingredients:
                                ingredient_names = []
                                for ri in recipe_ingredients:
                                    ing = f.get_ingredient(ri["ingredient_id"])
                                    nombre = (
                                        ing["name"]
                                        if ing
                                        else f'ID {ri["ingredient_id"]}'
                                    )
                                    unit_name = (
                                        f.get_unit_by_id(ing["unit_id"]) if ing else ""
                                    )
                                    cantidad = (
                                        ri["quantity"]
                                        if ri["quantity"] is not None
                                        else "a gusto"
                                    )
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
                                        user_id,
                                        selected_recipe["id"],
                                        target_ri["ingredient_id"],
                                    )
                                    print(
                                        f'{GREEN}Ingrediente eliminado de "{selected_recipe["title"]}".{END}'
                                    )
                            else:
                                print(
                                    f"{RED}Esta receta no tiene ingredientes para eliminar.{END}"
                                )
            else:
                print(f"\n{RED}{'X===X NO SE ENCUENTRAN RECETAS X===X':^40}{END}")
