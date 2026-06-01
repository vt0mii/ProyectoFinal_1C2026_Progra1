import components.validation as v
from lib.colors import *
import db.data as data
from db.data_crud import get_user_plan, get_mealtype_list


def menu_options(menu, message="Ingrese la opcion deseada: ", zero=True, admin=False):
    for i in range(len(menu)):
        print(f"{BOLD}{i + 1}{END} - {menu[i]}")
    if admin:
        menu = menu + ["ADMINMENU"]
        print(f"{BOLD}{len(menu)}{END} - Admin Menu")
    if zero:
        print(f"{BOLD}0{END} - Volver/Salir")

    while True:
        try:
            option = int(input(f"{BOLD}{message}{END}"))
            if (zero and option >= 0 and option <= len(menu)) or (
                not zero and option >= 1 and option <= len(menu)
            ):
                return option
            print(f"{RED}Opcion fuera de rango.{END}")
        except ValueError:
            print(f"{RED}Ingrese un numero valido.{END}")


def shopping_list(user_id):
    plan = get_user_plan(user_id)
    mt = get_mealtype_list()
    recipelist = []

    if not plan or not mt:
        print(f"{RED}Ha ocurrido un error.{END}")
        return None

    recipelist = [
        recipe for day in plan for type in mt for recipe in (day.get(type) or [])
    ]

    ingredients_by_id = {i["id"]: i for i in data.ingredients}
    units_by_id = {u["id"]: u["name"] for u in data.units}

    totals = {}
    for recipe_id in recipelist:
        for ri in data.recipe_ingredients:
            if ri["recipe_id"] == recipe_id:
                ingredient = ingredients_by_id[ri["ingredient_id"]]
                name = ingredient["name"]
                unit = units_by_id[ingredient["unit_id"]]

                if name not in totals:
                    totals[name] = {"quantity": 0, "unit": unit, "a_gusto": False}

                if not ri["quantity"]:
                    totals[name]["a_gusto"] = True
                else:
                    totals[name]["quantity"] += ri["quantity"]

    result = []
    for name, info in totals.items():
        if info["a_gusto"] and info["quantity"] == 0:
            quantity_str = "A gusto"
        elif info["a_gusto"]:
            quantity_str = f"{info['quantity']} {info['unit']} + A gusto"
        else:
            quantity_str = f"{info['quantity']} {info['unit']}"

        result.append({"name": name, "quantity": quantity_str})

    print(f"\n{BOLD}{GREEN}Mi lista de compras:{END}")
    for item in result:
        print(f"* {item['name']} {item['quantity']}")
    input(f"\n{LIGHT_BLUE}Presione Enter para continuar...{END}")
