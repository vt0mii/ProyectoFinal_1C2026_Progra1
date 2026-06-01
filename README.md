# MealPlan

Sistema de planificación de comidas semanal por usuario, desarrollado en Python. Permite registrarse, iniciar sesión, gestionar recetas con sus ingredientes, armar un plan semanal organizado por día y tipo de comida, y generar una lista de compras consolidada. Incluye un panel de administración con estadísticas y gestión de usuarios.

## Cómo ejecutar

```bash
python main.py
```

No requiere dependencias externas. Python 3.10 o superior recomendado.

## Usuarios de prueba

| Username | Contraseña | Nivel |
|----------|------------|-------|
| tomii    | tomi       | admin |
| test     | test       | user  |

## Estructura del proyecto

```
ProyectoFinal/
 ┣ components/
 ┃ ┣ auth.py          # Login y signup
 ┃ ┣ display.py       # Visualización del plan semanal en consola
 ┃ ┗ validation.py    # Validaciones y helpers de negocio
 ┣ db/
 ┃ ┣ data.py          # Carga y persistencia de datos en JSON
 ┃ ┗ data_crud.py     # Operaciones CRUD sobre los datos
 ┣ lib/
 ┃ ┣ colors.py        # Códigos ANSI para output con color
 ┃ ┣ constants.py     # Constantes globales (opciones de menú)
 ┃ ┗ utils.py         # menu_options() y shopping_list()
 ┣ admin_menu.py      # Panel de administración y estadísticas
 ┣ main.py            # Punto de entrada, main_menu() y user_menu()
 ┗ menu.py            # Submenús de recetas, ingredientes y plan semanal
```

## Módulos

### `main.py`
Punto de entrada del programa. Contiene `main_menu()` con las opciones de login y signup, y `user_menu()` que es el panel principal post-autenticación. Detecta si el usuario tiene nivel `admin` para mostrar u ocultar la opción del panel de administración.

### `menu.py`
Contiene los submenús del usuario: `plan_menu()`, `recetas_menu()` e `ingredientes_menu()`. Cada uno maneja el flujo completo de su sección — listado, alta, baja y modificación.

### `admin_menu.py`
Panel de administración accesible solo para usuarios con nivel `admin`. Incluye:
- Estadísticas generales, de recetas, de ingredientes y de planes
- Gestión de usuarios: ver todos los usuarios y editar sus recetas, ingredientes o plan

### `components/auth.py`
Maneja el flujo de registro (`signup`) e inicio de sesión (`login`). Valida username y contraseña en cada paso y almacena el usuario autenticado en `user_cache`.

### `components/display.py`
Renderiza el plan semanal como una tabla de 7 columnas (días) por N filas (tipos de comida). Soporta múltiples recetas por slot mostrando una sub-fila por cada una.

### `components/validation.py`
Centraliza todas las validaciones del sistema: existencia de usuarios, ownership de recetas e ingredientes, validez de credenciales y formato de inputs de menú.

### `db/data.py`
Carga los datos desde archivos JSON al iniciar y expone funciones `load_file()` y `save_file()` para persistencia. Mantiene las listas en memoria durante la ejecución y expone `user_cache` para la sesión activa.

### `db/data_crud.py`
Única capa que accede directamente a `db/data.py`. Expone funciones de lectura, creación, modificación y eliminación para todas las entidades. Al eliminar una receta, limpia automáticamente sus ingredientes huérfanos y la remueve de todos los planes.

### `lib/utils.py`
Contiene `menu_options()`, función reutilizable de navegación con soporte de colores, opción de salida configurable y validación de input. También contiene `shopping_list()`, que consolida todos los ingredientes del plan semanal del usuario sumando cantidades y agrupando por nombre.

### `lib/constants.py`
Define todas las listas de opciones de los menús del sistema.

### `lib/colors.py`
Códigos ANSI para aplicar color y formato al output en consola.

## Base de datos

Los datos se persisten en archivos JSON dentro de `db/`. Las listas se cargan en memoria al iniciar el programa y se guardan automáticamente ante cada modificación.

### `units` — Unidades de medida

| id | unidad  |
|----|---------|
| 0  | ml      |
| 1  | l       |
| 2  | mg      |
| 3  | g       |
| 4  | u       |
| 5  | A gusto |

### `meal_types` — Tipos de comida

| id | tipo     |
|----|----------|
| 0  | desayuno |
| 1  | almuerzo |
| 2  | merienda |
| 3  | cena     |

### `days` — Días de la semana

| id | día       |
|----|-----------|
| 0  | Lunes     |
| 1  | Martes    |
| 2  | Miercoles |
| 3  | Jueves    |
| 4  | Viernes   |
| 5  | Sabado    |
| 6  | Domingo   |

### `users` — Usuarios

Estructura: `{ user_id, username, password, level }`.

Niveles de acceso: `user` (acceso estándar) y `admin` (acceso al panel de administración).

### `recipes` — Recetas

Estructura: `{ id, user_id, title, instructions }`.

### `ingredients` — Ingredientes

Estructura: `{ id, user_id, name, unit_id }`.

### `recipe_ingredients` — Ingredientes por receta

Estructura: `{ id, recipe_id, ingredient_id, quantity }`. Cuando la cantidad es indeterminada, `quantity` es `null`.

### `recipe_plan` — Plan semanal

Estructura: `{ user_id, plan: [{ day_id, desayuno, almuerzo, merienda, cena }] }`. Cada slot contiene una lista de `recipe_id` y soporta múltiples recetas por tipo de comida por día.