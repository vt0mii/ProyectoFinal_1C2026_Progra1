import components.validation as v
from lib.constants import *
from components.auth import *
import db.data as data
import db.data_crud as f
import components.display as d


def menu_options(menu, message="Ingrese la opcion deseada: "):
    for i in range(len(menu)):
        print(f"{i + 1} - {menu[i]}")
    print("0 - Volver/Salir")

    option = input(message)
    print()
    while not v.validate_menu_option(option, menu):
        option = input("Error. Ingrese la opcion nuevamente: ")

    return int(option)


def user_menu():
    user_id = int(data.user_cache[0])

    flag = True
    while flag:
        print(f"\n\n---------- PANEL DE USUARIO -----------")
        d.display_plan(user_id)
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
            print("Función para añadir receta")
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
        else:
            print("No hay ingredientes para mostrar.")

        selected = menu_options(INGREDIENT_OPTIONS)
        if selected == 0:  # Cancelar
            flag = False

        elif selected == 1:  # Agregar Ingrediente
            nombre = input("Nombre del ingrediente: ")
            while not validate_alphabetic(nombre):
                nombre = input("Error, ingrese un nombre valido: ")

            unit_id = (
                menu_options(
                    [i[1] for i in data.units], "Por favor ingrese el ID de la unidad: "
                )
                - 1
            )
            f.add_ingredient(user_id, nombre, unit_id)

        elif selected == 2:  # Eliminar Ingrediente
            if mis_ingredientes:
                print("Mis ingredientes:")
                ingredient_opt = (
                    menu_options(
                        [i[1] for i in data.units],
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
                d.display_ingredients(user_id)

                ingredient_id = int(
                    input("Por favor ingrese el numero del ingrediente a editar: ")
                )
                new_ingredient_name = input(
                    "Ingrese el nuevo nombre a modificar o presione enter para saltear este paso: "
                )
                new_ingredient_unit_id = input(
                    "Ingrese el numero de la unidad o presione enter para saltear este paso: "
                )

                if len(new_ingredient_name) == 0 and len(new_ingredient_unit_id) == 0:
                    print("No se ha modificado el ingrediente.")
                else:
                    old_ingredient = f.get_ingredient(ingredient_id)
                    if old_ingredient:
                        ingredient_name = old_ingredient[2]
                        ingredient_unit = old_ingredient[3]
                        if len(new_ingredient_name) > 0:
                            ingredient_name = new_ingredient_name
                        if len(new_ingredient_unit_id) > 0:
                            ingredient_unit = int(new_ingredient_unit_id)

                        f.update_ingredient(
                            user_id, ingredient_id, ingredient_name, ingredient_unit
                        )

                    print(
                        "El ingrediente",
                        mis_ingredientes[ingredient_id - 1],
                        "ha sido modificado correctamente.",
                    )


def recetas_menu(user_id):
    flag = True
    while flag:

        print("\n\n-------------- MIS RECETAS -------------")
        selected = menu_options(RECIPE_OPTIONS)

        if selected == 0:
            flag = False
        elif selected == 1:
            print("Función para añadir receta")
        elif selected == 2:
            print("Función para quitar receta")

        elif selected == 3:
            print("Funcion para editar receta")
