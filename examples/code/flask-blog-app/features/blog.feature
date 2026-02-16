Feature: Blog Management
  As a web application user
  I want to manage blog posts
  So that I can publish and read articles

  Background:
    Given the blog application is running

  Scenario: View empty post list
    When I visit the home page
    Then I see the message "No hay posts disponibles"
    And I see a link to "Crear Post"

  Scenario: View existing posts list
    Given the following posts exist:
      | title              | content                    | author        |
      | My First Post      | Content of first post      | Juan Pérez    |
      | Learning Flask     | Flask is a micro-framework | María García  |
      | Python is Great    | Python is versatile        | Ana López     |
    When I visit the home page
    Then I see 3 posts in the list
    And I see the post "My First Post"
    And I see the post "Learning Flask"
    And I see the post "Python is Great"

  Scenario: View post detail
    Given a post exists with title "Flask Tutorial" content "Flask is easy to learn" author "Carlos Ruiz"
    When I click on the post "Flask Tutorial"
    Then I see the title "Flask Tutorial"
    And I see the content "Flask is easy to learn"
    And I see the author "Carlos Ruiz"
    And I see the creation date
    And I see an "Edit" button
    And I see a "Delete" button

  Scenario: Create new post successfully
    When I visit the home page
    And I click on "Crear Post"
    Then I see a creation form
    When I fill the form with:
      | field   | value                         |
      | title   | My New Post                   |
      | content | This is the post content      |
      | author  | Pedro Gómez                   |
    And I click "Save"
    Then I see the success message "Post creado exitosamente"
    And I see the post "My New Post" in the list

  Scenario: Validate creation form - title required
    When I visit the post creation page
    And I fill the form with:
      | field   | value                |
      | title   |                      |
      | content | Content without title|
      | author  | Test User            |
    And I click "Save"
    Then I see the error message "El título es requerido"
    And I stay on the creation page

  Scenario: Validate creation form - minimum content length
    When I visit the post creation page
    And I fill the form with:
      | field   | value      |
      | title   | Test       |
      | content | ABC        |
      | author  | Test User  |
    And I click "Save"
    Then I see the error message "El contenido debe tener al menos 10 caracteres"
    And I stay on the creation page

  Scenario: Edit existing post
    Given a post exists with title "Original Post" content "Original content" author "Editor Test"
    When I click on the post "Original Post"
    And I click "Edit"
    Then I see the edit form with current data
    When I modify the form with:
      | field   | value              |
      | title   | Updated Post       |
      | content | Updated content    |
    And I click "Update"
    Then I see the success message "Post actualizado exitosamente"
    And I see the post "Updated Post" with content "Updated content"

  Scenario: Delete post with confirmation
    Given a post exists with title "Post to Delete" content "This post will be deleted" author "Admin"
    When I click on the post "Post to Delete"
    And I click "Delete"
    Then I see the delete confirmation page
    And I see the confirmation message for "Post to Delete"
    When I confirm deletion
    Then I see the success message "Post eliminado exitosamente"
    And I do not see the post "Post to Delete" in the list

  Scenario: Cancel post deletion
    Given a post exists with title "Important Post" content "Do not delete" author "Admin"
    When I click on the post "Important Post"
    And I click "Delete"
    And I cancel deletion
    Then I see the post "Important Post" in the list

  Scenario: Post pagination
    Given 15 posts exist in the system
    When I visit the home page
    Then I see 10 posts on the first page
    And I see a link to "Página 2"
    When I click on "Página 2"
    Then I see 5 posts on the second page
