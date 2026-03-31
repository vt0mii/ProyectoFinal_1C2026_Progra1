import lib.constants as c
import validators as v
import auth as a
import lib.colors as cor

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

def run():
    print()
    print()
    print(f'{cor.BOLD}{c.ASCII_ART}{cor.END}')
    print()
    print("Bienvenido a MealPlan, por favor inicie sesion:")

    selected_option = options_menu(c.MENU_OPTIONS)
    if selected_option == 1:
        a.login()
    elif selected_option == 2:
        a.singup()
    else:
        print("Gracias por confiar en MealPlan! Hasta luego!")

if __name__ == "__main__":
    run()