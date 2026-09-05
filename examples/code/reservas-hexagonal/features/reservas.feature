@US-070
Feature: Reserva de un recurso (US-070)
  Como cliente
  Quiero reservar un recurso (ej. una mesa) en una fecha y horario
  Para asegurarme su disponibilidad

  Background:
    Given que la API está disponible

  Scenario: Crear una reserva exitosamente
    When se envía una petición POST a "/reservas/" con:
      | campo          | valor       |
      | recurso_id     | mesa-1      |
      | fecha          | manana      |
      | hora_inicio    | 10:00:00    |
      | hora_fin       | 11:00:00    |
      | cliente_nombre | Ana         |
    Then la respuesta tiene código de estado 201
    And la reserva creada puede consultarse y está "CONFIRMADA"

  Scenario: Rechazar una reserva solapada con otra existente
    Given que existe una reserva para "mesa-1" en "manana" de "10:00:00" a "11:00:00"
    When se envía una petición POST a "/reservas/" con:
      | campo          | valor       |
      | recurso_id     | mesa-1      |
      | fecha          | manana      |
      | hora_inicio    | 10:30:00    |
      | hora_fin       | 11:30:00    |
      | cliente_nombre | Bruno       |
    Then la respuesta tiene código de estado 409

  Scenario: Permitir reservar el mismo recurso en un horario distinto
    Given que existe una reserva para "mesa-1" en "manana" de "10:00:00" a "11:00:00"
    When se envía una petición POST a "/reservas/" con:
      | campo          | valor       |
      | recurso_id     | mesa-1      |
      | fecha          | manana      |
      | hora_inicio    | 12:00:00    |
      | hora_fin       | 13:00:00    |
      | cliente_nombre | Carla       |
    Then la respuesta tiene código de estado 201

  Scenario: Rechazar una reserva con fecha pasada
    When se envía una petición POST a "/reservas/" con:
      | campo          | valor       |
      | recurso_id     | mesa-1      |
      | fecha          | ayer        |
      | hora_inicio    | 10:00:00    |
      | hora_fin       | 11:00:00    |
      | cliente_nombre | Ana         |
    Then la respuesta tiene código de estado 422

  Scenario: Consultar una reserva inexistente
    When se envía una petición GET a "/reservas/no-existe"
    Then la respuesta tiene código de estado 404
