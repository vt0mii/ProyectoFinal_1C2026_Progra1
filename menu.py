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

        if selected == 0:
            flag = False
            
        elif selected == 1:
            mis_recetas = f.get_user_recipes(user_id)
            if mis_recetas:
                day = menu_options(f.get_days_list(), "Por favor, seleccione el dia donde agregar: ")
                if int(day) != 0:
                    mt = menu_options(f.get_mealtype_list(), "Por favor, seleccione el tipo de comida: ", False)
                
                    recipe_selected = menu_options([r[2] for r in mis_recetas], "Seleccione la receta a agregar")
                    if int(recipe_selected) != 0:
                        f.add_recipe_to_plan(user_id, mis_recetas[recipe_selected - 1][0], day - 1, mt - 1)
            else:
                print(f"\n{"X===X NO SE ENCUENTRAN RECETAS X===X":^40}")
            
        elif selected == 2:
            print("Función para quitar receta")
        elif selected == 3:
            print("Funcion para editar receta")


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
            while not v.validate_alphabetic(nombre):
                nombre = input("Error, ingrese un nombre valido: ")

            units = [i[1] for i in data.units]
            unit_id = (
                menu_options(units, "Por favor ingrese el ID de la unidad: ", False) - 1
            )
            while int(unit_id) <= 0 or int(unit_id) > len(units):
                unit_id = input("Por favor, ingrese una opcion valida: ")
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
                selected = mis_ingredientes[ingredient_opt]

                ingredient_deleted = f.delete_ingredient(user_id, selected[0])
                if ingredient_deleted:
                    print(
                        f"El ingrediente {selected[2]} ha sido eliminado correctamente."
                    )
                else:
                    print(f"Error al eliminar el ingrediente {selected[2]}.")
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
                while not v.validate_edit_name:
                    new_ingredient_name = input(
                        "Ingrese un nombre valido o presione enter para no modificar: "
                    )

                units = [i[1] for i in data.units]
                for i in range(len(units)):
                    print(f"{i + 1} - {units[i]}")

                new_ingredient_unit_id = input(
                    "Ingrese el numero de la unidad o presione enter para no modificar: "
                )

                while not v.validate_edit_unit:
                    new_ingredient_unit_id = input(
                        "Ingrese una opcion correcta o presione enter para no modificar: "
                    )

                while int(new_ingredient_unit_id) <= 0 or int(
                    new_ingredient_unit_id
                ) > len(units):
                    unit_id = input("Por favor, ingrese una opcion valida: ")
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
            print("--------------AÑADIR RECETAS-------------")
            print()
            title = input("Porfavor Ingrese el nombre de la receta ")
            while not v.validate_alphabetic(title):
                title = input("Ingrese un nombre con letras unicamente")

            print()
            instructions = input("Porfavor Ingrese el nombre de la receta ")
            f.add_recipe(user_id, title, instructions)
        elif selected == 2:
            print("Función para quitar receta")

        elif selected == 3:
            print("Funcion para editar receta")
