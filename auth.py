import validators as v

def login():
    flag_username = False
    flag_password = False
    
    # Chequear Username
    username = input("👩 Ingrese su nombre de usuario: ")
    while not flag_username:
        if not v.validate_alphabetic_string(username) or not v.validate_string_length(username):
            print("❌ ERROR: Por favor ingrese entre 3 a 20 caracteres alfabeticos.")
            username = input("Ingrese el nombre de usuario nuevamente aqui: ")
        elif not v.validate_user(username):
            print()
            print("❌ ERROR: El usuario", username, "no existe.")
            username = input("Ingrese el nombre de usuario nuevamente aqui:")
        else:
            flag_username = True

    # Chequear Password
    password = input("🔒 Ingrese su contraseña: ")
    while not flag_password:
        if not v.validate_credentials(username, password):
            print()
            print("❌ ERROR: Contraseña incorrecta.")
            password = input("Ingrese la contraseña nuevamente: ")
        else:
            flag_password = True

    print()
    print("✅ Bienvenidx a MealPlan!")

def singup():
    flag = False
    username = input("👩 Ingrese un nombre de usuario (solo caracteres alfabeticos): ")

    # Chequeo username
    while not flag:
        if not v.validate_alphabetic_string(username):
            print()
            print("❌ ERROR: Por favor ingrese entre 3 a 20 caracteres alfabeticos.")
            username = input("Ingrese el nombre de usuario nuevamente aqui: ")
        elif v.validate_user(username):
            print()
            print("❌ ERROR: ya existe un usuario con el nombre", username, ".")
            username = input("Ingrese otro nombre de usuario aqui: ")
        else:
            flag = True

    # Chequeo Password
    password = input("👩 Ingrese su contraseña: ")
    while not v.validate_string_length(password):
        print()
        print("❌ ERROR: Por favor ingrese entre 3 a 20 caracteres.")
        password = input("Ingrese una contraseña nueva nuevamente aqui: ")

    print()
    print("✅ Registro exitoso. Bienvenidx a MealPlan!")
