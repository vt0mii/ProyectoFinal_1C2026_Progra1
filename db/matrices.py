# Matrices Dinamicas
usuarios = []
ingredientes = []
planes_semanales = []
recetas_ingredientes = []
recetas = []
plan_receta = []
cache_user = []

# Matrices Constantes
dias = [[1, "Lunes"],[2, "Martes"],[3,"Miercoles"],[4, "Jueves"],[5, "Viernes"],[6, "Sabado"],[7, "Domingo"]]
tipo_comida = [[1, "Desayuno"],[2, "Almuerzo"],[3, "Merienda"],[4, "Cena"]]
unidades = [[1, "mg"],[2, "g"],[3, "u"],[4, "ml"],[5, "l"]]

# CRUD Usuarios
def crear_usuario(username, password, level="user"):
    usuarios.append([len(usuarios), username, password, level])
    
def eliminar_usuario(id):
    usuarios.remove(usuarios[id])

def actualizar_username(id, old, new):
    if usuarios[id][1] == old:
        usuarios[id][1] = new
        return True
    return False

def actualizar_password(id, old, new):
    if usuarios[id][2] == old:
        usuarios[id][2] = new
        return True
    return False

def obtener_usuario(username):
    for i in usuarios:
        if i[1] == username:
            return i
    return None

# CRUD Ingredientes
def crear_ingrediente(nombre, id_unidad):
    ingredientes.append([len(ingredientes), nombre, id_unidad])
    
def eliminar_ingrediente(id):
    ingredientes.remove(ingredientes[id])

def actualizar_ingrediente(id, old, new):
    if ingredientes[id][1] == old:
        ingredientes[id][1] = new
        return True
    return False

def actualizar_ingrediente_u(id, old, new):
    if ingredientes[id][2] == old:
        ingredientes[id][2] = new
        return True
    return False

def obtener_ingrediente(id):
    return ingredientes[id]

# CRUD Planes Semanales
def crear_plansemanal(id_user, id_dia):
    planes_semanales.append([len(planes_semanales), id_user, id_dia])
    
def obtener_plansemanal(id):
    return planes_semanales[id]

def eliminar_plansemanal(id):
    planes_semanales.remove(planes_semanales[id])

def actualizar_plan_dia(id, id_dia):
    planes_semanales[id][2] = id_dia

# CRUD Recetas Ingredientes
def asignar_ingrediente_receta(id_receta, id_ingrediente, cantidad, unidades=1):
    recetas_ingredientes.append([len(recetas_ingredientes), id_receta, id_ingrediente, unidades, cantidad])
    
def obtener_ingredientes_receta(id_receta):
    ingredients = []
    for i in recetas_ingredientes:
        if i[1] == id_receta:
            ingredients.append(i)
    return ingredients

def actualizar_ingrediente_receta(id_receta, id_ingrediente, new):
    ingredients = obtener_ingredientes_receta(id_receta)
    for i in ingredients:
        if i[0] == id_ingrediente:
            i = new
            return True
    return False

def eliminar_ingrediente_receta(id_receta, id_ingrediente):
    ingredients = obtener_ingredientes_receta(id_receta)
    for i in ingredients:
        if i[0] == id_ingrediente:
            ingredients.remove(i)
            return True
    return False

# CRUD Recetas
def crear_receta(nombre, instrucciones):
    recetas.append([len(recetas), nombre, instrucciones])
    
def obtener_receta(id):
    return recetas[id]

def actualizar_receta(id, nombre=None, instrucciones=None):
    if nombre is not None:
        recetas[id][1] = nombre
        
def eliminar_receta(id):
    recetas.remove(recetas[id])
    
# CRUD Plan Receta
def asignar_receta_plan(id_plan, id_receta, id_dia, id_tipocomida):
    plan_receta.append([len(plan_receta), id_plan, id_receta, id_dia, id_tipocomida])
    
def obtener_recetas_plan(id_plan):
    recetasplan = []
    for i in plan_receta:
        if i[1] == id_plan:
            recetasplan.append(i)
    return recetasplan

def actualizar_receta_plan(id_plan, id_receta, new):
    recets = obtener_recetas_plan(id_plan)
    for i in recets:
        if i[2] == id_receta:
            i[2] = new
            return True
    return False

def eliminar_receta_plan(id_plan, id_receta):
    for i in plan_receta:
        if i[1] == id_plan and i[2] == id_receta:
            plan_receta.remove(i)