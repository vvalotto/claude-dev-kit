# language: es
Característica: Gestión de Contactos vía API REST
  Como desarrollador frontend
  Quiero una API REST para gestionar contactos
  Para construir una aplicación de agenda de contactos

  Antecedentes:
    Dado que la API está corriendo
    Y que la base de datos está vacía

  Escenario: Crear un contacto nuevo con datos válidos
    Cuando creo un contacto con nombre "Juan Pérez" email "juan.perez@email.com" telefono "555-1234"
    Entonces recibo un código de estado 201
    Y la respuesta contiene un campo "id"
    Y el campo "nombre" es "Juan Pérez"
    Y el campo "email" es "juan.perez@email.com"
    Y el campo "telefono" es "555-1234"

  Escenario: Intentar crear contacto con email inválido
    Cuando creo un contacto con nombre "María García" email "email-invalido" telefono "555-5678"
    Entonces recibo un código de estado 400
    Y la respuesta contiene un campo "error"
    Y el mensaje de error menciona "email"

  Escenario: Listar todos los contactos
    Dado que existe un contacto con nombre "Juan Pérez" email "juan.perez@email.com" telefono "555-1234"
    Y que existe un contacto con nombre "María García" email "maria.garcia@email.com" telefono "555-5678"
    Y que existe un contacto con nombre "Pedro López" email "pedro.lopez@email.com" telefono "555-9012"
    Cuando obtengo todos los contactos
    Entonces recibo un código de estado 200
    Y la respuesta es una lista con 3 contactos
    Y la lista contiene un contacto con nombre "Juan Pérez"
    Y la lista contiene un contacto con nombre "María García"
    Y la lista contiene un contacto con nombre "Pedro López"

  Escenario: Obtener un contacto por ID existente
    Dado que existe un contacto con nombre "Ana Martínez" email "ana.martinez@email.com" telefono "555-3456"
    Y que guardo el ID del contacto creado
    Cuando obtengo el contacto por ID guardado
    Entonces recibo un código de estado 200
    Y el campo "nombre" es "Ana Martínez"
    Y el campo "email" es "ana.martinez@email.com"

  Escenario: Intentar obtener contacto con ID inexistente
    Cuando obtengo el contacto con ID 999
    Entonces recibo un código de estado 404
    Y la respuesta contiene un campo "error"

  Escenario: Actualizar un contacto existente
    Dado que existe un contacto con nombre "Carlos Ruiz" email "carlos.ruiz@email.com" telefono "555-7890"
    Y que guardo el ID del contacto creado
    Cuando actualizo el contacto guardado con nombre "Carlos Ruiz García" email "carlos.ruiz.nuevo@email.com" telefono "555-7777"
    Entonces recibo un código de estado 200
    Y el campo "nombre" es "Carlos Ruiz García"
    Y el campo "email" es "carlos.ruiz.nuevo@email.com"
    Y el campo "telefono" es "555-7777"

  Escenario: Intentar actualizar contacto inexistente
    Cuando actualizo el contacto 999 con nombre "Fantasma" email "fantasma@email.com" telefono "555-0000"
    Entonces recibo un código de estado 404
    Y la respuesta contiene un campo "error"

  Escenario: Eliminar un contacto existente
    Dado que existe un contacto con nombre "Laura Sánchez" email "laura.sanchez@email.com" telefono "555-2468"
    Y que guardo el ID del contacto creado
    Cuando elimino el contacto guardado
    Entonces recibo un código de estado 204
    Cuando intento obtener el contacto eliminado
    Entonces recibo un código de estado 404

  Escenario: Intentar eliminar contacto inexistente
    Cuando elimino el contacto con ID 999
    Entonces recibo un código de estado 404
    Y la respuesta contiene un campo "error"

  Escenario: Validar campos requeridos al crear contacto
    Cuando creo un contacto sin email
    Entonces recibo un código de estado 400
    Y la respuesta contiene un campo "error"
