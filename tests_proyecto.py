# Necesario para correcto funcionamiento
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from components.validation import validate_credentials, user_exists_name
from db.data_crud import add_recipe, get_user_recipes, delete_recipe
from lib.utils import difficulty_str

def test_credenciales_correctas():
    assert validate_credentials("tomii", "tomi") is True


def test_credenciales_incorrectas():
    assert validate_credentials("tomii", "mal") is False


def test_usuario_inexistente():
    assert user_exists_name("usuario_que_no_existe_xyz") is False


def test_difficulty_str_formato():
    resultado = difficulty_str({"difficulty": 3})
    assert len(resultado) == 10
    assert resultado.count("▰") == 3


def test_agregar_y_eliminar_receta():
    RECIPES_PATH = "db/recipes.json"

    with open(RECIPES_PATH, encoding="utf-8") as f:
        estado_original = f.read()

    add_recipe(0, "Receta de prueba", "Solo para test.", 5)
    titulos = []
    recetas = get_user_recipes(0)
    if recetas:
        titulos = [r["title"] for r in recetas]
    assert "Receta de prueba" in titulos

    with open(RECIPES_PATH, "w", encoding="utf-8") as f:
        f.write(estado_original)