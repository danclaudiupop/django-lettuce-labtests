Feature: Register
    In order to get access to app 
    A user should be able to register


Scenario: User registers
    Given I go to the register page
    When I fill register form with:
        | username | email       | password1 | password2 |
        | danul    | dan@dan.com | test123   | test123   |
    And I submit the data
    Then I should see "Check your email"
    And I should receive an email at "dan@dan.com" with the subject "Activate your djangoproject.com account - you have 7 days!"
    And I activate the account
    Then I should see "Congratulations!"


Scenario: Users login
    Given following users exist
      | username | password |
      | danu     | test123  |
      | lulu     | test123  |
    When I go to the login page
    And I login as user "danu"
    Then I should see "Welcome, danu. Thanks for logging in."
