@projects @todoly @sanity
  Feature: Projects

    @critical
    @allure.label.owner:ET
    @allure.link:https://dev.example.com/
    @allure.issue:API-123
    Scenario: Verify all projects are returned when get all projects endpoint is call
      As user I want to get all the projects from TODOLY API

      When I call to projects endpoint using "get" method with out body
      Then I receive the response and validate using "get_all_projects" json
      And I validate the status code is 200

    @critical
    @allure.label.owner:ET
    @allure.link:https://dev.example.com/
    @allure.issue:API-123
    Scenario: Verify that a project can be created using create project endpoint
      As user I want to create a project from TODOLY API

      When I call to projects endpoint using "POST" method with out body
      Then I receive the response and validate using "create_project" json
      And I validate the status code is 200

    @critical
    @allure.label.owner:ET
    @allure.link:https://dev.example.com/
    @allure.issue:API-123
    @project_id
    Scenario: Verify that a project can be deleted using delete project endpoint
      As user I want to delete a project from TODOLY API

      When I call to projects endpoint using "DELETE" method with out body
      Then I receive the response and validate using "delete_project" json
      And I validate the status code is 200