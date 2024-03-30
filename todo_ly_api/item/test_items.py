import json

import pytest
import logging

from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


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

    @pytest.mark.project
    def test_get_all_items(self):

        response = self.rest_client.request("get", url=self.url_todo_ly_with_extension)

        assert response.status_code == 200, "wrong status code, expected 200"

    def test_create_item(self):

        body_project = {
            "Content": "New Item Mauricio"
        }

        response = self.rest_client.request("post", self.url_todo_ly_with_extension, body=json.dumps(body_project))

        id_item_created = response.json()["Id"]
        self.list_items.append(id_item_created)
        assert response.status_code == 200, "wrong status code, expected 200"

    def test_delete_item(self, create_item):
        id_item_delete = create_item["Id"]
        url_todo_ly = f"{self.url_todo_ly}/{id_item_delete}{self.url_todo_ly_extension}"

        response = self.rest_client.request("delete", url=url_todo_ly)

        assert response.status_code == 200, "wrong status code, expected 200"

    def test_update_item(self, create_item):
        id_item_update = create_item["Id"]
        LOGGER.debug("Item Id to update: %s", id_item_update)

        url_todo_ly = f"{self.url_todo_ly}/{id_item_update}{self.url_todo_ly_extension}"
        body_project = {
            "ItemType": 2
        }
        response = self.rest_client.request("put", url=url_todo_ly, body=json.dumps(body_project))
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
            url_delete_project = f"{cls.url_todo_ly}/{id_item}{cls.url_todo_ly_extension}"
            response = cls.rest_client.request("delete", url=url_delete_project)
            if response.status_code == 204:
                LOGGER.info("Item Id deleted: %s", id_item)
