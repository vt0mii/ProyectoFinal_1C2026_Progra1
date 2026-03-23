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

def validate_user( username ):
    flag = False
    for user in users:
        if user["username"] == username:
            flag = True
    
    return flag

def validate_password( username, password ):
    flag = False
    for user in users:
        if user["username"] == username and user["password"] == password:
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
    flag_username = False
    flag_password = False
    print()
    username = input("👩 Ingrese su nombre de usuario: ")

    while not flag_username:

        if not validate_string( username ):
            username = input( "Ingrese el nombre de usuario nuevamente aqui: " )
        elif not validate_user( username ):
            print()
            print( "❌ ERROR: El usuario", username, "no existe." )
            username = input( "Ingrese el nombre de usuario nuevamente aqui:" )
        elif validate_string( username ) and validate_user( username ):
            flag_username = True

    print()
    password = input("🔒 Ingrese su contraseña: ")
    while not flag_password:

        if not validate_password( username, password ):
            print()
            print( "❌ ERROR: Contraseña incorrecta." )
            password = input( "Ingrese la contraseña nuevamente aqui: " )
        else:
            flag_password = True

    return


def singup ():
    return


#programa principal
ascii_art = r"""                                     
    ;/UCQQQ(.           .]QQQJU/^                                 I/Ubah?   ?UULQLJUYYXut{<"    ]Ypobm:                                       
    '_dh*##?.          -M#*oo]'                                  ,l]pbk{   'IZkoh|iii}cwbaWJ<  lipbq0l                                       
     +dk&W8o<         lmWM&M&~                                     ?ko*1    ;co*o|     `f##*a?. :Zok0!                                       
     ~kpjMWBL!       "cBOo8W8i                                     ?a#M}    :xo*o(      "ukbdwl :Z*aJl                                       
     ?#h?aBB@z.      /%#}#@B@+       +xh8$$Wp('    lfb#@@$8ac<     )8B81    lY&8&f       uokhM< IpBBL!    ijbM@$@&hul   ]fwh8x`(w#B$Baf'     
     n##\U&MM%L     nW%Z]&8W%f     ]hB&0__UMBBa_  OBB8J-?[h@@%z    QW&8Y    -pkbdQ      1pwmwp] _ka*b{   mBB&X-?|o@@%x  zdBB@h8B#dk%%%8ql    
     f0m| UkQZa1   ;wdm_]odwh|    -#8m,    |W#&Q,]d&8*<   t#%8L    Xqwbf    +CUXCX     1wqdap;  ~QYJL~  }d*Mh>   jW%%U   [b8WM0>   -qbww<    
     ]CU- :nQzXx! .|YU- >JzcJ_   ,nwd*ao*#WWaqwCI -jn)  .`~Owqr    (zvY]    lnUXYZLYUZOC0br_    lXYUrI   [rr1  .`_pbht   <YZ0Y`     tUcz;    
     !j/I  ,rxfc? Ixx<  :rffv;   ljf(>>>>>>>>>>!    'I-/ujxrff-    >jfx!    "}jfr+"i>>i"        "\jj]"     'l-rznvuxx_   :1tf}.     _//t^    
     :/("   ,tt//,-f?   ^t//x"   ,///:            ^</\};` "(/ji    ;//f:    '_t/f!              `)/t+`   "_f/};' ,)(tl   ^]tf?.     !t/|'    
     It|:    >uff|x|:   ,fffx:   ,1jf)"       '  Itfx<    Itfr<    !t/jI    ^]jfr<              ^(tt-`  ltfx>    Iffr>   ,}tf[.     <tt\^    
     ~\|>    '}jt/j+    Ijttri    +f\\\_"   !]/- [\(/+   ,)jtf-    -/\f>    ;)ttf?              ,///}"  {||t<   ;(ftj+   l(/t1'     ]/\t,    
    ,-//?I;`  ;(xx]`   "<rffr+"   '+f/\|\\|\|/}" +f//t()(tj1rt{, 'l{ttf-:  '!ffff[:"           ,<f/t\i` +f//t()(tr1jt[,  it/t(;,  ;l{t/f>`   
   I{ffftft_'  :Yn^   I)jrxxjj1"    "~xpqqqQ}l.   I[Lbbpc-:lrjj-.!\jjrjj{; _jjxxrjf[,          ?jjrjjf~  l}0bdpu-"!rjj_ !/jjjjf-  _fjjrjti   
"""
session_menu_opts = [ "Ya tengo una cuenta :)", "No tengo cuenta :(" ]
users = [
    {
        "name": "cristina",
        "username": "crisvlasova",
        "password": "cris"
    },
    {
        "name": "thiago",
        "username": "thiagocaimer",
        "password": "thiago"
    },
]

print()
print()
print(ascii_art)
print()
print( "Bienvenido a MealPlan, por favor inicie sesion:" )
print()

session_menu_opt = show_menu( session_menu_opts )
if session_menu_opt == 1:
    login()
elif session_menu_opt == 2:
    singup()
else:
    print("Gracias por confiar en MealPlan! Hasta luego!")

print()
