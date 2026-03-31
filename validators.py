import json
import re
import lib.colors as cor
from db.matrices import usuarios_db

# Validaciones
def validate_user(username) -> bool:
    for user in usuarios_db:
        if user[0] == username:
            return True
    return False

def validate_credentials(username, password) -> bool:
    for user in usuarios_db:
        if user[0] == username and user[1] == password:
            return True
    return False

validate_string_length = lambda txt: True if len(txt) > 3 and len(txt) <= 20 else False

validate_alphabetic_string = lambda string: True if re.match(r"^[a-zA-Z]+$", string) and validate_string_length(string) else False

def validate_opt_num(opt, menu) -> bool:
    menu_len = len(menu)

    if not re.match(r"^\d+$", opt):
        print()
        print(f'{cor.RED}❌ ERROR: Por favor ingrese numeros enteros positivos.')
    else:
        int_opt = int(opt)
        if int_opt > menu_len:
            print()
            print(f'{cor.RED}❌ ERROR: Por favor ingrese numeros entre 1 y {menu_len}.')
        else:
            return True
    return False
