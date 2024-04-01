import logging

import requests

from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class TestTodoLyAPI:
    url_todo_ly_extension = None
    url_todo_ly = None
    url_todo_ly_with_extension = None

    @classmethod
    def setup_class(cls):
        LOGGER.debug("SetupClass method")
        cls.url_todo_ly = "https://todo.ly/api/authentication/token.json"
        session = requests.Session()
        session.auth = ("mauridav377@gmail.com", "jaggaer")
        cls.rest_client = RestClient()
        response = session.get(url=cls.url_todo_ly)
        LOGGER.debug("Status Code %s: ", response.status_code)
        LOGGER.debug("Response Content %s: ", response.text)

        cls.access_token = response.json()["TokenString"]

    def test_get_user(self):
        headers_todoly_api = {
            "Token": self.access_token
        }
        url_get_user = "https://todo.ly/api/user.json"
        rest_client = RestClient(headers=headers_todoly_api)
        response = rest_client.request("get", url=url_get_user)

