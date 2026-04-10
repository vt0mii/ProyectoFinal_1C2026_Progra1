# 🥗 MealPlan

Sistema de planificación de comidas semanal por usuario, desarrollado en Python. Permite registrarse, iniciar sesión, gestionar recetas con sus ingredientes y visualizar un plan semanal organizado por día y tipo de comida.


## Estructura del Proyecto

```
Own/
 ┣ components/
 ┃ ┣ auth.py          # Login y signup
 ┃ ┣ display.py       # Visualización del plan semanal
 ┃ ┗ validation.py    # Validaciones y helpers de negocio
 ┣ db/
 ┃ ┣ data.py          # Datos estáticos y dinámicos (base de datos en memoria)
 ┃ ┗ data_crud.py     # Operaciones CRUD sobre los datos
 ┣ lib/
 ┃ ┗ constants.py     # Constantes globales (opciones de menú)
 ┣ main.py            # Punto de entrada
 ┗ menu.py            # Lógica de navegación de menús
```

## Módulos

### `menu.py`
Contiene la lógica de navegación. Define `main_menu()` (menú de bienvenida con login/signup) y `user_menu()` (menú post-autenticación). Las opciones se renderizan dinámicamente a partir de las constantes definidas en `lib/constants.py`.

### `components/auth.py`
Maneja el flujo de registro (`signup`) e inicio de sesión (`login`). Valida username y contraseña en cada paso, y almacena el usuario autenticado en `user_cache`.

### `components/display.py`
Renderiza el plan semanal del usuario en consola como una tabla de 7 columnas (días) por 4 filas (tipos de comida). Utiliza exclusivamente funciones del CRUD para acceder a los datos.

### `components/validation.py`
Centraliza todas las validaciones del sistema: existencia de usuarios, ownership de recetas e ingredientes, validez de credenciales y formato de inputs.

### `db/data.py`
Base de datos en memoria. Contiene las estructuras de datos estáticas (unidades, tipos de comida, días) y dinámicas (usuarios, recetas, ingredientes, plan semanal). También expone `user_cache`, que almacena la sesión activa.

### `db/data_crud.py`
Expone funciones de lectura, creación, modificación y eliminación para todas las entidades del sistema. Es la única capa que debería acceder directamente a `db/data.py`.


## Base de Datos

El sistema utiliza estructuras de datos en memoria (listas, diccionarios y tuplas). A continuación se documenta cada tabla.


### `units` — Unidades de medida

| id | unit    |
|----|---------|
| 0  | ml      |
| 1  | l       |
| 2  | mg      |
| 3  | g       |
| 4  | u       |
| 5  | A gusto |


### `meal_types` — Tipos de comida

| id | meal_type |
|----|-----------|
| 0  | desayuno  |
| 1  | almuerzo  |
| 2  | merienda  |
| 3  | cena      |


### `days` — Días de la semana

| id | day       |
|----|-----------|
| 0  | Lunes     |
| 1  | Martes    |
| 2  | Miercoles |
| 3  | Jueves    |
| 4  | Viernes   |
| 5  | Sabado    |
| 6  | Domingo   |


### `users` — Usuarios del sistema

Implementado como diccionario `{ user_id: { username, password, level } }`.

| id | username   | password | level |
|----|------------|----------|-------|
| 0  | tomiicotos | tomi     | admin |
| 1  | test       | test     | user  |

**Niveles de acceso:**
- `user` — acceso estándar al plan semanal propio.
- `admin` — acceso con permisos extendidos (en desarrollo).


### `recipes` — Recetas

Implementado como lista de listas `[id, user_id, title, instructions]`.

| id | user_id | title                          | instructions                                                                                              |
|----|---------|--------------------------------|-----------------------------------------------------------------------------------------------------------|
| 0  | 0       | Ensalada de Zanahoria y Huevo  | Rallar la zanahoria, hervir un huevo 12min aprox., cortarlo y condimentar todo con aceite, sal y limon.   |


### `ingredients` — Ingredientes

Implementado como lista de listas `[id, user_id, name, unit_id]`.

| id | user_id | name     | unit_id |
|----|---------|----------|---------|
| 0  | 0       | Zanahoria | 4      |
| 1  | 0       | Huevo     | 4      |
| 2  | 0       | Aceite    | 0      |
| 3  | 0       | Sal       | 5      |
| 4  | 0       | Limon     | 5      |


### `recipe_ingredients` — Ingredientes por receta

Implementado como lista de listas `[id, recipe_id, ingredient_id, quantity]`. Cuando la cantidad es indeterminada (ej. "a gusto"), `quantity` es `None`.

| id | recipe_id | ingredient_id | quantity |
|----|-----------|---------------|----------|
| 0  | 0         | 0             | 1        |
| 1  | 0         | 1             | 1        |
| 2  | 0         | 2             | 20       |
| 3  | 0         | 3             | None     |
| 4  | 0         | 4             | None     |


### `recipe_plan` — Plan semanal por usuario

Implementado como diccionario anidado `{ user_id: { day_id: { meal_type: [recipe_ids] } } }`. Cada tipo de comida contiene una lista de IDs de recetas asignadas. A continuación se muestra la versión normalizada (una fila por entrada):

| user_id | day_id | meal_type | recipe_id |
|---------|--------|-----------|-----------|
| 0       | 0      | almuerzo  | 1         |
| 0       | 3      | almuerzo  | 3         |
| 0       | 6      | cena      | 0         |
| 1       | 0      | almuerzo  | 0         |
| 1       | 1      | merienda  | 4         |
| 1       | 2      | desayuno  | 0         |
| 1       | 3      | almuerzo  | 5         |
| 1       | 4      | cena      | 0         |
| 1       | 5      | merienda  | 2         |
| 1       | 6      | cena      | 0         |

