Feature: Register
    In order to get access to app 
    A user should be able to register


Scenario: User registers
    Given I go to the register page
    When I fill in "username" with "danul"
    And I fill in "email" with "danclaudiupop@gmail.com"
    And I fill in "password1" with "test123"
    And I fill in "password2" with "test123"
    And I press "submit"
    Then I should see "Check your email"
    And I should receive an email at "danclaudiupop@gmail.com" with the subject "Activate your djangoproject.com account - you have 7 days!"
    And I activate the account
    Then I should see "Congratulations!"

Scenario: User logs in successfully
    Given I go to the login page
    When I fill in "username" with "danul"
    And I fill in "password" with "test123"
    And I press "submit"
    Then I should see "Welcome, danul. Thanks for logging in."
