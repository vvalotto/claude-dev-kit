# Feature: Calculadora Simple (US-001)
Feature: Calculadora Simple (US-001)
  Como usuario de escritorio
  Quiero una calculadora con interfaz gráfica
  Para realizar operaciones matemáticas básicas (+, -, *, ÷)

  Background:
    Given la aplicación está iniciada
    And la configuración está cargada

  Scenario: Sumar dos números
    Given el display muestra "0"
    When el usuario presiona el botón "5"
    And el usuario presiona el botón "+"
    And el usuario presiona el botón "3"
    And el usuario presiona el botón "="
    Then el display debe mostrar "8"

  Scenario: Restar dos números
    Given el display muestra "0"
    When el usuario presiona el botón "10"
    And el usuario presiona el botón "-"
    And el usuario presiona el botón "3"
    And el usuario presiona el botón "="
    Then el display debe mostrar "7"

  Scenario: Multiplicar dos números
    Given el display muestra "0"
    When el usuario presiona el botón "4"
    And el usuario presiona el botón "*"
    And el usuario presiona el botón "6"
    And el usuario presiona el botón "="
    Then el display debe mostrar "24"

  Scenario: Dividir dos números
    Given el display muestra "0"
    When el usuario presiona el botón "15"
    And el usuario presiona el botón "/"
    And el usuario presiona el botón "3"
    And el usuario presiona el botón "="
    Then el display debe mostrar "5"

  Scenario: División por cero muestra error
    Given el display muestra "0"
    When el usuario presiona el botón "8"
    And el usuario presiona el botón "/"
    And el usuario presiona el botón "0"
    And el usuario presiona el botón "="
    Then el display debe mostrar "Error: Cannot divide by zero"

  Scenario: Limpiar display
    Given el display muestra "123"
    When el usuario presiona el botón "C"
    Then el display debe mostrar "0"
