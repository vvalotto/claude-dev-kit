# language: es
@US-002
Característica: Gestión de Tareas (TODO API)
  Como developer
  Quiero una API REST para gestionar tareas
  Para integrar con mi aplicación frontend

  Antecedentes:
    Dado que la API está disponible
    Y la base de datos está vacía

  Escenario: Crear una nueva tarea
    Cuando se envía una petición POST a "/tasks/" con:
      | campo       | valor                  |
      | title       | Comprar leche          |
      | description | Ir al supermercado     |
    Entonces la respuesta tiene código de estado 201
    Y el JSON de respuesta contiene:
      | campo       | valor                  |
      | title       | Comprar leche          |
      | description | Ir al supermercado     |
      | completed   | False                  |
    Y el campo "id" es un número mayor que 0

  Escenario: Listar todas las tareas
    Dado que existen las siguientes tareas:
      | title          | description    |
      | Comprar leche  | Supermercado   |
      | Estudiar       | FastAPI docs   |
    Cuando se envía una petición GET a "/tasks/"
    Entonces la respuesta tiene código de estado 200
    Y el JSON de respuesta es una lista con 2 elementos

  Escenario: Obtener una tarea específica
    Dado que existe una tarea con:
      | campo       | valor                  |
      | title       | Comprar leche          |
      | description | Ir al supermercado     |
    Cuando se envía una petición GET a "/tasks/{task_id}"
    Entonces la respuesta tiene código de estado 200
    Y el JSON de respuesta contiene:
      | campo       | valor                  |
      | title       | Comprar leche          |

  Escenario: Actualizar una tarea
    Dado que existe una tarea con:
      | campo       | valor                  |
      | title       | Comprar leche          |
      | completed   | False                  |
    Cuando se envía una petición PUT a "/tasks/{task_id}" con:
      | campo       | valor                  |
      | title       | Comprar leche y pan    |
      | completed   | True                   |
    Entonces la respuesta tiene código de estado 200
    Y el JSON de respuesta contiene:
      | campo       | valor                  |
      | title       | Comprar leche y pan    |
      | completed   | True                   |

  Escenario: Eliminar una tarea
    Dado que existe una tarea con:
      | campo       | valor                  |
      | title       | Tarea temporal         |
    Cuando se envía una petición DELETE a "/tasks/{task_id}"
    Entonces la respuesta tiene código de estado 204
    Y la tarea ya no existe en la base de datos

  Escenario: Error al obtener tarea inexistente
    Cuando se envía una petición GET a "/tasks/999"
    Entonces la respuesta tiene código de estado 404
    Y el JSON de respuesta contiene el mensaje "not found"
