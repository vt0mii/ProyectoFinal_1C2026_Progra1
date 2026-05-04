import components.validation as v
from lib.colors import *

def menu_options(menu, message="Ingrese la opcion deseada: ", zero=True, admin=False):
    for i in range(len(menu)):
        print(f"{BOLD}{i + 1}{END} - {menu[i]}")
    if admin:
        menu = menu + ["ADMINMENU"]
        print(f"{BOLD}{len(menu)}{END} - Admin Menu")
    if zero:
        print(f"{BOLD}0{END} - Volver/Salir")

    while True:
        try:
            option = int(input(message))
            if (zero and option >= 0 and option <= len(menu)) or (not zero and option >= 1 and option <= len(menu)):
                return option
            print(f"{RED}Opcion fuera de rango.{END}")
        except ValueError:
            print(f"{RED}Ingrese un numero valido.{END}")