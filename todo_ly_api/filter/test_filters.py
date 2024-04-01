import random

import allure
import logging

from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@allure.epic("TODOLY API")
@allure.story("Filters")
class TestFilters:
    url_todo_ly_extension = None
    url_todo_ly = None
    url_todo_ly_with_extension = None

    @classmethod
    def setup_class(cls):
        LOGGER.debug("SetupClass method")
        cls.url_todo_ly = "https://todo.ly/api/filters"
        cls.url_todo_ly_extension = ".json"
        cls.url_todo_ly_with_extension = cls.url_todo_ly + cls.url_todo_ly_extension
        cls.rest_client = RestClient()

    @allure.feature("List Filter")
    @allure.title("Test get all filter")
    @allure.description("Test that show the response for all filter")
    @allure.tag("acceptance", "users", "sanity")
    @allure.testcase("TC-123")
    def test_get_all_filters(self):
        LOGGER.info("GET ALL FILTERS TEST: ")
        response = self.rest_client.request("get", url=self.url_todo_ly_with_extension)

        assert response.status_code == 200, "wrong status code, expected 200"

    @allure.feature("Get Filter By ID")
    @allure.title("Test get filter by ID")
    @allure.description("Test that show the response for a specific filter")
    @allure.tag("acceptance", "users", "sanity")
    @allure.testcase("TC-123")
    def test_get_filter_by_id(self):
        LOGGER.info("GET FILTER BY ID TEST: ")
        id_possible_filters = [0, -1, -5]
        url_todo_ly = f"{self.url_todo_ly}/{random.choice(id_possible_filters)}{self.url_todo_ly_extension}"
        response = self.rest_client.request("get", url=url_todo_ly)

        assert response.status_code == 200, "wrong status code, expected 200"

    @allure.feature("Get Items Of A Filter")
    @allure.title("Test get items of a filter")
    @allure.description("Test that show the response for items of a filter")
    @allure.tag("acceptance", "users", "sanity")
    @allure.testcase("TC-123")
    def test_get_items_of_filter(self):
        LOGGER.info("GET ALL ITEMS OF A FILTER TEST: ")
        id_possible_filters = [0, -1, -5]
        url_todo_ly = f"{self.url_todo_ly}/{random.choice(id_possible_filters)}/items{self.url_todo_ly_extension}"
        response = self.rest_client.request("get", url=url_todo_ly)
        assert response.status_code == 200, "wrong status code, expected 200"


