import components.validation as v
from lib.constants import *
from components.auth import *
import db.data as data
import db.data_crud as f
import components.display as d

def menu_options(menu):
    for i in range(len(menu)):
        print(f'{i + 1} - {menu[i]}')
    print('0 - Volver/Salir')
    
    option = input('Ingrese la opcion deseada: ')
    print()
    while not v.validate_menu_option(option, menu):
        option = input('Error. Ingrese la opcion nuevamente: ')
        
    return int(option)

def main_menu():    
    result = False
    flag = True
    print(ASCII_ART)
    print('Bienvenido a MealPlan! Elija la opcion para ingresar:')
    while flag and not result:
        selected = menu_options(MENU_OPTIONS)
        if selected == 0:
            flag = False
        elif selected == 1:
            result = login()
        elif selected == 2:
            result = signup()

        if result:
            user_menu()
            print()
            result = False
        
    print('Gracias por usar MealPlan. Hasta Luego!')
        
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
            for indice, ing in enumerate(mis_ingredientes):
                print(f"{indice + 1}. {ing[2]} ({f.get_unit_by_id(ing[3])})")
        print()
        selected = menu_options(INGREDIENT_OPTIONS)
        
        if selected == 0:
            flag = False
        elif selected == 1:
            nombre = input("Nombre del ingrediente: ")
            for u in data.units:
                print(f"{u[0]} - {u[1]}")
            unit_id = int(input("Seleccione ID de unidad: "))
            f.add_ingredient(user_id, nombre, unit_id)
        elif selected == 2:
            if mis_ingredientes:
                print("Mis ingredientes:")
                for index, ing in enumerate(mis_ingredientes):
                    print(f"{index + 1}. {ing[2]} ({f.get_unit_by_id(ing[3])})")
                ingredient_id = int(input("Por favor ingrese el numero del ingrediente a eliminar: "))
                ingredient_name = mis_ingredientes[ingredient_id-1][2]

                ingredient_deleted = f.delete_ingredient(user_id, mis_ingredientes[ingredient_id-1][0])
                if ingredient_deleted == True:
                    print(f"El ingrediente {ingredient_name} ha sido eliminado correctamente.")
                else:
                    print(f"Error al eliminar el ingrediente {ingredient_name}.")
            else:
                print("No hay ingredientes para eliminar.")
        
        elif selected == 3:
            if mis_ingredientes:
                print("Mis ingredientes:")
                for index, ing in enumerate(mis_ingredientes):
                    print(f"{index + 1}. {ing[2]} ({f.get_unit_by_id(ing[3])})")
                ingredient_id = int(input("Por favor ingrese el numero del ingrediente a editar: "))
                
                new_ingredient_name = input("Ingrese el nuevo nombre a modificar o presione enter para saltear este paso: ")
                new_ingredient_unit_id = input("Ingrese el numero de la unidad o presione enter para saltear este paso: ")


                if len(new_ingredient_name) == 0 and len(new_ingredient_unit_id) == 0:
                    print("No se ha modificado el ingrediente.")
                else:
                    ingredient_name = mis_ingredientes[ingredient_id-1][2]
                    ingredient_unit_id = data.units[int(new_ingredient_unit_id)][0]
                    print(ingredient_unit_id)

                    if len(new_ingredient_name) > 0:
                        ingredient_name = new_ingredient_name
                    if len(new_ingredient_unit_id) > 0:
                        ingredient_unit = int(new_ingredient_unit_id)
                    
                    f.update_ingredient(user_id, ingredient_unit_id, ingredient_name, ingredient_unit)

                    print("El ingrediente", mis_ingredientes[ingredient_id-1], "ha sido modificado correctamente.")


                


        
def recetas_menu(user_id):
    print("\n[ MIS RECETAS ]")
    pass