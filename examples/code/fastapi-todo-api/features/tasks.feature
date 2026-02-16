@US-002
Feature: Task Management (TODO API)
  As a developer
  I want a REST API to manage tasks
  So I can integrate it with my frontend application

  Background:
    Given the API is available
    And the database is empty

  Scenario: Create a new task
    When a POST request is sent to "/tasks/" with:
      | field       | value                |
      | title       | Buy milk             |
      | description | Go to supermarket    |
    Then the response status code is 201
    And the response JSON contains:
      | field       | value                |
      | title       | Buy milk             |
      | description | Go to supermarket    |
      | completed   | False                |
    And the field "id" is a number greater than 0

  Scenario: List all tasks
    Given the following tasks exist:
      | title          | description       |
      | Buy milk       | Supermarket       |
      | Study          | FastAPI docs      |
    When a GET request is sent to "/tasks/"
    Then the response status code is 200
    And the response is a list with 2 items

  Scenario: Get a specific task
    Given a task exists with:
      | field       | value                |
      | title       | Buy milk             |
      | description | Go to supermarket    |
    When a GET request is sent to "/tasks/{task_id}"
    Then the response status code is 200
    And the response JSON contains:
      | field       | value                |
      | title       | Buy milk             |

  Scenario: Update a task
    Given a task exists with:
      | field       | value                |
      | title       | Buy milk             |
      | completed   | False                |
    When a PUT request is sent to "/tasks/{task_id}" with:
      | field       | value                |
      | title       | Buy milk and bread   |
      | completed   | True                 |
    Then the response status code is 200
    And the response JSON contains:
      | field       | value                |
      | title       | Buy milk and bread   |
      | completed   | True                 |

  Scenario: Delete a task
    Given a task exists with:
      | field       | value                |
      | title       | Temporary task       |
    When a DELETE request is sent to "/tasks/{task_id}"
    Then the response status code is 204
    And the task no longer exists in the database

  Scenario: Error when getting non-existent task
    When a GET request is sent to "/tasks/999"
    Then the response status code is 404
    And the response JSON contains the message "not found"
