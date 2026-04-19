from db.data import *
import re

# Verifica si el usuario existe
user_exists_id = lambda userid: str(userid) in users
user_exists_name = lambda username: any(
    u["username"] == username for u in users.values()
)

# Verifica si la receta existe y pertenece al usuario
is_recipe_owner = lambda userid, recipeid: any(
    r[0] == recipeid and str(r[1]) == str(userid) for r in recipes
)

# Verifica si el ingrediente existe y pertenece al usuario
is_ingredient_owner = lambda userid, ingredientid: any(
    i[0] == ingredientid and str(i[1]) == str(userid) for i in ingredients
)

# Verifica si el usuario tiene un plan
is_plan_owner = lambda userid: str(userid) in recipe_plan

# Verifica si la receta no se encuentra ya asignada en el dia y tipo de comida
is_recipe_on_day = (
    lambda userid, recipeid, day_id, mealtype: recipeid
    in recipe_plan[str(userid)][str(day_id)][mealtype]
)

# Valida si las credenciales son correctas
validate_credentials = lambda username, password: any(
    u["username"] == username and u["password"] == password for u in users.values()
)

# Valida que el username cumpla con los requisitos
validate_username = lambda username: validate_string_length(
    username
) and validate_alphabetic(username)
validate_string_length = lambda username: 3 <= len(username) <= 20

# Valida que el input sea un numero y verifica que la opcion este en el menu
validate_menu_option = lambda option, menu, zero=True: (
    re.match(r"^\d+$", option)
    and int(option) <= len(menu)
    and (int(option) >= 0 if zero else int(option) >= 1)
)

# Valida que lo ingresado sea alfabetico
validate_alphabetic = lambda txt: re.match(r"^[a-zA-Z ]+$", txt)

# Validar la opcion extra de "enter" al editar
validate_edit_unit = (
    lambda option: re.match(r"^\d*$", option)
    and option.isdigit()
    and int(option) <= len(units)
    and int(option) >= 0
)

# Validar la opcion extra de "enter" al editar
validate_edit_name = lambda option: re.match(r"^[a-zA-Z ]*$", option)
