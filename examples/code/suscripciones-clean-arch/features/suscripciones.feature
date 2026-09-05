@US-001
Feature: Subscription management
  As a service administrator
  I want to create and cancel subscriptions
  So that users can control their access to the service

  Background:
    Given the API is available

  Scenario: Create a new subscription
    When a subscription is created for "ana@example.com" with plan "basico"
    Then the response status code is 201
    And the subscription is active

  Scenario: Reject a duplicate active subscription
    Given a subscription exists for "ana@example.com" with plan "basico"
    When a subscription is created for "ana@example.com" with plan "premium"
    Then the response status code is 409

  Scenario: Cancel an existing subscription
    Given a subscription exists for "ana@example.com" with plan "basico"
    When the subscription is cancelled
    Then the response status code is 200
    And the subscription is not active

  Scenario: Reject cancelling a non-existent subscription
    When subscription "999" is cancelled
    Then the response status code is 404
