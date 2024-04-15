@items @todoly @sanity
  Feature: Items

    @critical
    @allure.label.owner:ET
    @allure.link:https://dev.example.com/
    @allure.issue:API-123
    Scenario: Verify all items are returned when get all item endpoint is call
      As user I want to get all the items from TODOLY API

      When I call to items endpoint using "get" method with out body
      Then I receive the response and validate using "get_all_items" json
      And I validate the status code is 200