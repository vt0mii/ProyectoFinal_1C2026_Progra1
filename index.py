import re

def validate_opt_num( opt, opt_menu ):
    flag = False
    menu_len = len( opt_menu )

    if not re.match( r"^\d+$", opt ):
        print()
        print( "❌ ERROR: Por favor ingrese numeros enteros positivos." )
    else: 
        int_opt = int( opt )
        if int_opt > menu_len:
            print()
            print( "❌ ERROR: Por favor ingrese numeros entre 1 y", menu_len,"." )
        else:
            flag = True

    return flag    

 
def validate_string( string ):
    flag = False

    if not re.match( r"^[a-zA-Z]+$", string ):
        print()
        print( "❌ ERROR: Por favor ingrese caracteres alfabeticos." )
    else:
        if len(string) < 3 or len(string) > 20:
            print()
            print( "❌ ERROR: Por favor ingrese una cadena de entre 3 a 20 caracteres." )
        else: 
            flag = True

    return flag


def show_menu( menu ):
    opt = -1
    for i in range( len( menu ) ):
        print( i+1 , "-", menu[i] )
    
    print( "0 - Salir" )
    print()

    opt = input( "Ingrese el numero de opcion aqui: " )
    while( validate_opt_num( opt, session_menu_opts ) == False ):
        print()
        opt = input( "🔁 Ingrese nuevamente el numero de opcion aqui: " )

    return int( opt )


def login ():
    print()
    username = input("👩 Ingrese su nombre de usuario: ")
    while not validate_string( username ):
        print()
        username = input( "👩🔁 Ingrese el nombre de usuario nuevamente aqui: " )

    password = input("🔒 Ingrese su contraseña: ")
    while not validate_string( password ):
        print()
        password = input( "🔒🔁 Ingrese su contraseña nuevamente aqui: " )

    return


def singup ():
    return


#programa principal
session_menu_opts = [ "Ya tengo una cuenta :)", "No tengo cuenta :(" ]
users = {
    "name": "cristina",
    "username": "crisvlasova",
    "password": "crisvlasovapass"
}

print()
print()
print( "iPlanMeal" )
print()
print( "Bienvenido a iPlanMeal, por favor inicie sesion:" )

session_menu_opt = show_menu( session_menu_opts )
if session_menu_opt == 1:
    login()
elif session_menu_opt == 2:
    singup()
else:
    print("Gracias por confiar en iMealPlan! Hasta luego!")

print()
