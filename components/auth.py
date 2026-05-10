from components.validation import *
from db.data_crud import add_user, get_user_by_name
import db.data as data
from lib.colors import *

def login():
    valid_username = False
    valid_password = False

    # Username
    username = input("Ingrese su Username o X para cancelar la operacion: ")
    while not valid_username:
        if username.lower() == "x":
            print(f"{RED}Operacion Cancelada, volviendo...{END}")
            return False
        elif not validate_username(username):
            username = input(
                f"{RED}Por favor ingrese entre 3 a 20 caracteres alfabeticos, intente nuevamente: {END}"
            )
        elif not user_exists_name(username):
            username = input(
                f"{RED}El username proporcionado no existe, intente nuevamente: {END}"
            )
        else:
            valid_username = True

    # Password
    password = input("Ingrese su contraseña o X para cancelar la operacion: ")
    while not valid_password:
        if password.lower() == "x":
            print("Operacion Cancelada, volviendo...")
            return False
        elif not validate_string_length(password):
            password = input(
                "Por favor ingrese entre 3 a 20 caracteres, intente nuevamente: "
            )
        elif not validate_credentials(username, password):
            password = input("Contraseña incorrecta, intente nuevamente: ")
        else:
            valid_password = True

    data.user_cache = get_user_by_name(username)
    return True


def signup():
    valid_username = False
    valid_password = False

    # Username
    print(
        "El username debe ser alfabetico con un largo entre 3 y 20 caracteres. Ingrese X para cancelar la operacion"
    )
    username = input("Ingrese su username: ")
    while not valid_username:
        if username.lower() == "x":
            print("Operacion Cancelada, volviendo...")
            return False
        elif not validate_username(username):
            username = input(
                "El username proporcionado no cumple con los requisitos, intente nuevamente: "
            )
        elif user_exists_name(username):
            username = input(
                "El username proporcionado ya existe, intente nuevamente: "
            )
        else:
            valid_username = True

    # Password
    print(
        "La contraseña debe tener un largo entre 3 y 20 caracteres. Ingrese X para cancelar la operacion"
    )
    password = input("Ingrese su Contraseña: ")
    while not valid_password:
        if password.lower() == "x":
            print("Operacion Cancelada, volviendo...")
            return False
        elif not validate_string_length(password):
            password = input(
                "El password no cumple con los requisitos, intente nuevamente: "
            )
        else:
            valid_password = True

    add_user(username, password)
    new_user = get_user_by_name(username)
    if new_user:
        data.recipe_plan[new_user[0]] = {
            day: {"desayuno": [], "almuerzo": [], "merienda": [], "cena": []}
            for day in range(7)
        }
    data.user_cache = get_user_by_name(username)
    return True
