import lib.colors as col
import lib.constants as c
import components.validators as v
import components.auth as a
from db.matrices import cache_user
import components.listas as l

def options_menu(menu) -> int:
    opt = -1
    for i in range(len(menu)):
        print(i + 1, "-", menu[i])

    print("0 - Salir")

    opt = input("Ingrese el numero de opcion aqui: ")
    while not v.validate_opt_num(opt, menu):
        print()
        opt = input("🔁 Ingrese nuevamente el numero de opcion aqui: ")

    return int(opt)

def main_menu():
    print()
    print(f'{col.BOLD}{c.ASCII_ART}{col.END}')
    print()
    print("Bienvenido a MealPlan, por favor inicie sesion:")

    selected_option = options_menu(c.MENU_OPTIONS)
    if selected_option == 1:
        a.login()
    elif selected_option == 2:
        a.singup()
    else:
        print("Gracias por confiar en MealPlan! Hasta luego!")
        
def user_menu():
    opt = options_menu(c.USER_OPTIONS)
    if opt == 1:
        l.mostrar_planes(cache_user)
    elif opt == 2:
        l.mostrar_ingredientes(cache_user)
    else:
        print("Gracias por confiar en MealPlan! Hasta luego!")