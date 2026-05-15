import re
from db.data import *

# Verifica si el usuario existe por id
user_exists_id = lambda userid: any(u["user_id"] == int(userid) for u in users)

# Verifica si el usuario existe por nombre
user_exists_name = lambda username: any(u["username"] == username for u in users)

# Verifica si la receta existe y pertenece al usuario
is_recipe_owner = lambda userid, recipeid: any(
    r["id"] == recipeid and r["user_id"] == int(userid) for r in recipes
)

# Verifica si el ingrediente existe y pertenece al usuario
is_ingredient_owner = lambda userid, ingredientid: any(
    i["id"] == ingredientid and i["user_id"] == int(userid) for i in ingredients
)

# Verifica si el usuario tiene un plan
is_plan_owner = lambda userid: any(p["user_id"] == int(userid) for p in recipe_plan)


# Verifica si la receta ya está asignada en el día y tipo de comida
def is_recipe_on_day(userid, recipeid, day_id, mealtype):
    plan_entry = next((p for p in recipe_plan if p["user_id"] == int(userid)), None)
    if plan_entry is None:
        return False
    day_entry = next(
        (d for d in plan_entry["plan"] if d["day_id"] == int(day_id)), None
    )
    if day_entry is None:
        return False
    return recipeid in day_entry[mealtype]


# Valida si las credenciales son correctas
validate_credentials = lambda username, password: any(
    u["username"] == username and u["password"] == password for u in users
)

# Valida que el username cumpla con los requisitos
validate_username = lambda username: validate_string_length(
    username
) and validate_alphabetic(username)

validate_string_length = lambda username: 3 <= len(username) <= 20

# Valida que lo ingresado sea alfabetico
validate_alphabetic = lambda txt: re.match(r"^[a-zA-Z ]+$", txt)

# Validar la opcion extra de "enter" al editar
validate_edit_unit = lambda option: (
    option == "" or (option.isdigit() and 1 <= int(option) <= len(units))
)

# Validar la opcion extra de "enter" al editar
validate_edit_name = lambda option: re.match(r"^[a-zA-Z ]*$", option)

# Valida si el usuario actual es admin
validate_admin = lambda user: user.get("level") == "admin"
