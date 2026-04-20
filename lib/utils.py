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

    option = input(f"{LIGHT_BLUE}{message}{END}")
    print()
    while not v.validate_menu_option(option, menu, zero):
        option = input(f"{RED}Error. Ingrese la opcion nuevamente: {END}")

    return int(option)