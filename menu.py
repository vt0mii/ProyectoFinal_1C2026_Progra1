import components.validation as v
from lib.constants import *
from components.auth import *
import db.data as data
import db.data_crud as f
import components.display as d

def menu_options(menu):
    for i in range(len(menu)):
        print(f'{i + 1} - {menu[i]}')
    print('0 - Cancelar')
    
    option = input('Ingrese la opcion deseada: ')
    while not v.validate_menu_option(option, menu):
        option = input('Error. Ingrese la opcion nuevamente: ')
        
    return int(option)

def main_menu():    
    result = False
    
    print('Bienvenido a MealPlan!')
    while not result:
        selected = menu_options(MENU_OPTIONS)
        if selected == 0:
            break
        if selected == 1:
            result = login()
        elif selected == 2:
            result = signup()
            
        if result:
            user_menu()
        
    print('Gracias por usar MealPlan. Hasta Luego!')
        
def user_menu():
    if data.user_cache[1]["level"] == "user":
        d.display_plan(data.user_cache[0])
    elif data.user_cache[1]["level"] == "admin":
        d.display_plan(data.user_cache[0])