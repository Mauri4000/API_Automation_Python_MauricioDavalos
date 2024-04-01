import json

import allure
import pytest
import logging

from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@allure.epic("TODOLY API")
@allure.story("Items")
class TestItems:
    url_todo_ly_extension = None
    url_todo_ly = None
    url_todo_ly_with_extension = None

    @classmethod
    def setup_class(cls):
        LOGGER.debug("SetupClass method")
        cls.url_todo_ly = "https://todo.ly/api/items"
        cls.url_todo_ly_extension = ".json"
        cls.url_todo_ly_with_extension = cls.url_todo_ly + cls.url_todo_ly_extension
        cls.list_items = []
        cls.rest_client = RestClient()

    @allure.feature("List Items")
    @allure.title("Test get all items")
    @allure.description("Test that show the response for all created items")
    @allure.tag("acceptance", "users", "sanity")
    @allure.testcase("TC-123")
    def test_get_all_items(self):

        response = self.rest_client.request("get", url=self.url_todo_ly_with_extension)

        assert response.status_code == 200, "wrong status code, expected 200"

    @allure.feature("Create Item")
    @allure.title("Test create an item")
    @allure.description("Test that show the response of created item")
    @allure.tag("acceptance", "users", "sanity")
    @allure.testcase("TC-123")
    def test_create_item(self):

        body_item = {
            "Content": "New Item Mauricio"
        }

        response = self.rest_client.request("post", self.url_todo_ly_with_extension, body=json.dumps(body_item))

        id_item_created = response.json()["Id"]
        self.list_items.append(id_item_created)
        assert response.status_code == 200, "wrong status code, expected 200"

    @allure.feature("Delete Item")
    @allure.title("Test delete an item")
    @allure.description("Test that delete an item by id")
    @allure.tag("acceptance", "users", "sanity")
    @allure.testcase("TC-123")
    def test_delete_item(self, create_item):
        id_item_delete = create_item["Id"]
        url_todo_ly = f"{self.url_todo_ly}/{id_item_delete}{self.url_todo_ly_extension}"

        response = self.rest_client.request("delete", url=url_todo_ly)

        assert response.status_code == 200, "wrong status code, expected 200"

    @allure.feature("Update Item")
    @allure.title("Test update an item")
    @allure.description("Test that updates an item by id")
    @allure.tag("acceptance", "users", "sanity")
    @allure.testcase("TC-123")
    def test_update_item(self, create_item):
        id_item_update = create_item["Id"]
        LOGGER.debug("Item Id to update: %s", id_item_update)

        url_todo_ly = f"{self.url_todo_ly}/{id_item_update}{self.url_todo_ly_extension}"
        body_item = {
            "ItemType": 2
        }
        response = self.rest_client.request("put", url=url_todo_ly, body=json.dumps(body_item))
        # Add to list of projects to be deleted for cleanup teardown
        self.list_items.append(id_item_update)
        assert response.status_code == 200, "wrong status code, expected 200"

    @classmethod
    def teardown_class(cls):
        """
        Delete all items used in tests
        """
        LOGGER.info("Cleanup items...")
        for id_item in cls.list_items:
            url_delete_item = f"{cls.url_todo_ly}/{id_item}{cls.url_todo_ly_extension}"
            response = cls.rest_client.request("delete", url=url_delete_item)
            if response.status_code == 204:
                LOGGER.info("Item Id deleted: %s", id_item)
