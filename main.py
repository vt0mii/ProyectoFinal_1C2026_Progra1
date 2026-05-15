from components.auth import login, signup
from lib.constants import MENU_OPTIONS, ASCII_ART, USER_OPTIONS
from menu import plan_menu, recetas_menu, ingredientes_menu
from admin_menu import admin_menu
import components.validation as v
from lib.colors import *
import components.display as d
from lib.utils import menu_options
from db.data import user_cache


def main_menu():
    result = False
    flag = True
    print(f"{CYAN}{ASCII_ART}{END}")
    print(f"{BOLD}Bienvenido a MealPlan! Elija la opcion para ingresar: {END}")
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

    print("Gracias por usar MealPlan. Hasta Luego!")


def user_menu():
    user_id = user_cache[0]

    flag = True
    while flag:

        d.display_plan(user_id)
        print(f"\n\n{CYAN}---------- PANEL DE USUARIO -----------{END}")
        is_admin = v.validate_admin(user_cache)
        selected = menu_options(USER_OPTIONS, admin=is_admin)

        if selected == 0:
            flag = False
        elif selected == 1:
            plan_menu(user_id)
        elif selected == 2:
            recetas_menu(user_id)
        elif selected == 3:
            ingredientes_menu(user_id)
        elif selected == 4 and is_admin:
            admin_menu()


if __name__ == "__main__":
    main_menu()
