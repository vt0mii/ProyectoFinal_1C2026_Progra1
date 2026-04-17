from components.auth import login, signup
from lib.constants import MENU_OPTIONS, ASCII_ART
from menu import menu_options, user_menu

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
    
if __name__ == "__main__":
    main_menu()