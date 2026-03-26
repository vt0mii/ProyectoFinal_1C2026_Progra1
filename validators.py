import json
import re

userlist = []

# Cargo los usuarios desde el archivo
with open("users.json") as f:
    userlist = json.load(f)

# Validaciones

def validate_user(username) -> bool:
    for user in userlist:
        if user["username"] == username:
            return True
    return False

def validate_credentials(username, password) -> bool:
    for user in userlist:
        if user["username"] == username and user["password"] == password:
            return True
    return False

def validate_string_length(text) -> bool:
    if len(text) > 3 and len(text) <= 20:
        return True
    return False

def validate_alphabetic_string(string) -> bool:
    if re.match(r"^[a-zA-Z]+$", string) and validate_string_length(string):
        return True
    return False

def validate_opt_num(opt, menu) -> bool:
    menu_len = len(menu)

    if not re.match(r"^\d+$", opt):
        print()
        print("❌ ERROR: Por favor ingrese numeros enteros positivos.")
    else:
        int_opt = int(opt)
        if int_opt > menu_len:
            print()
            print("❌ ERROR: Por favor ingrese numeros entre 1 y", menu_len, ".")
        else:
            return True
    return False
