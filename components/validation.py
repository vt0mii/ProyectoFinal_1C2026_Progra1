import re
from db.data import *

# Valida si las credenciales son correctas
validate_credentials = lambda username, password: any(
    u["username"] == username and u["password"] == password for u in users.values()
)

# Valida que el string cumpla con los requisitos
validate_string_length = lambda txt: True if len(txt) > 3 and len(txt) <= 20 else False
validate_alphabetic_string = lambda string: (
    True
    if re.match(r"^[a-zA-Z]+$", string) and validate_string_length(string)
    else False
)


# Valida que la opcion seleccionada exista en el menu
def validate_opt_num(opt, menu):
    menu_len = len(menu)

    if re.match(r"^\d+$", opt) and int(opt) < menu_len:
        return True
    return False


# Verifica si el usuario existe
user_exists_id = lambda userid: str(userid) in users
user_exists_name = lambda username: any(
    u["username"] == username for u in users.values()
)

# Verifica si la receta existe y pertenece al usuario
is_recipe_owner = lambda userid, recipeid: any(
    r[0] == recipeid and r[1] == userid for r in recipes
)

# Verifica si el ingrediente existe y pertenece al usuario
is_ingredient_owner = lambda userid, ingredientid: any(
    i[0] == ingredientid and i[1] == userid for i in ingredients
)

# Verifica si el usuario tiene un plan
is_plan_owner = lambda userid: str(userid) in recipe_plan

# Verifica si la receta no se encuentra ya asignada en el dia y tipo de comida
is_recipe_on_day = (
    lambda userid, recipeid, day_id, mealtype: recipeid
    in recipe_plan[str(userid)][str(day_id)][mealtype]
)
