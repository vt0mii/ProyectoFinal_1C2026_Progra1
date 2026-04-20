# Sesion actual
user_cache = (0,{})

# Data Estatica
units = [(0, "ml"), (1, "l"), (2, "mg"), (3, "g"), (4, "u"), (5, "A gusto")]
meal_types = [(0, "desayuno"), (1, "almuerzo"), (2, "merienda"), (3, "cena")]
days = [
    (0, "Lunes"),
    (1, "Martes"),
    (2, "Miercoles"),
    (3, "Jueves"),
    (4, "Viernes"),
    (5, "Sabado"),
    (6, "Domingo"),
]

# Matrices Dinamicas
recipes = [  # Su estructura es id, user_id, title, instructions
    [
        0,
        0,
        "Ensalada de Zanahoria y Huevo",
        "Rallar la zanahoria, hervir un huevo 12min aprox., cortarlo y condimentar todo con aceite, sal y limon.",
    ],
    [
        1,
        1,
        "Zanahoria rallada",
        "Rallar la zanahoria.",
    ],
    [
        2,
        1,
        "Tomate relleno",
        "Lorem Ipsum.",
    ],
    [
        3,
        0,
        "Hamburguesa",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod",
    ],
]

ingredients = [  # Su estructura es id, user_id, name, unit_id
    [0, 0, "Zanahoria", 4],
    [1, 0, "Huevo", 4],
    [2, 0, "Aceite", 0],
    [3, 0, "Sal", 5],
    [4, 0, "Limon", 5],
    [5, 1, "Zanahoria", 1],
    [6, 1, "Tomate", 1],
    [7, 0, "Tomate", 4],
    [8, 0, "Carne", 3],
]

recipe_ingredients = [  # Su estructura es id, recipe_id, ingredient_id, quantity
    [0, 0, 0, 1],
    [1, 0, 1, 1],
    [2, 0, 2, 20],
    [3, 0, 3, None],
    [4, 0, 4, None],
    [5, 1, 5, 1],
    [6, 3, 8, 200],
    [7, 3, 7, 1],
    [8, 3, 1, 1],
    [9, 3, 3, 1],
    [10, 2, 6, 1],
]

# Diccionarios
users = {  # userid : {}
    "0": {
        "username": "tomii",
        "password": "tomi",
        "level": "admin"
    },
    "1": {
        "username": "test",
        "password": "test",
        "level": "user"
    },
}

recipe_plan = {  # userid: { day_id : { mealtype} }
    "0": {
        "0": {"desayuno": [], "almuerzo": [0], "merienda": [], "cena": []},
        "1": {"desayuno": [], "almuerzo": [], "merienda": [], "cena": []},
        "2": {"desayuno": [], "almuerzo": [], "merienda": [], "cena": []},
        "3": {"desayuno": [], "almuerzo": [0], "merienda": [], "cena": []},
        "4": {"desayuno": [], "almuerzo": [], "merienda": [], "cena": []},
        "5": {"desayuno": [], "almuerzo": [], "merienda": [], "cena": []},
        "6": {"desayuno": [], "almuerzo": [], "merienda": [], "cena": [0]},
    },
    "1": {
        "0": {"desayuno": [], "almuerzo": [], "merienda": [], "cena": []},
        "1": {"desayuno": [], "almuerzo": [], "merienda": [], "cena": []},
        "2": {"desayuno": [], "almuerzo": [], "merienda": [], "cena": []},
        "3": {"desayuno": [], "almuerzo": [], "merienda": [], "cena": []},
        "4": {"desayuno": [], "almuerzo": [], "merienda": [], "cena": []},
        "5": {"desayuno": [], "almuerzo": [], "merienda": [], "cena": []},
        "6": {"desayuno": [], "almuerzo": [], "merienda": [], "cena": []},
    }
}
