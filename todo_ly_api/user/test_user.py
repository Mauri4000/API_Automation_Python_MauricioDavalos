import json
import random
import string

import allure
import logging

from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@allure.epic("TODOLY API")
@allure.story("Users")
class TestUsers:
    url_todo_ly_extension = None
    url_todo_ly = None
    url_todo_ly_with_extension = None

    @classmethod
    def setup_class(cls):
        LOGGER.debug("SetupClass method")
        cls.url_todo_ly = "https://todo.ly/api/user"
        cls.url_todo_ly_extension = ".json"
        cls.url_todo_ly_with_extension = cls.url_todo_ly + cls.url_todo_ly_extension
        cls.list_users = []
        cls.rest_client = RestClient()

    @allure.feature("List User")
    @allure.title("Test get current user authenticated")
    @allure.description("Test that show the response the current user authenticated")
    @allure.tag("acceptance", "users", "sanity")
    @allure.testcase("TC-123")
    def test_get_all_users(self):

        response = self.rest_client.request("get", url=self.url_todo_ly_with_extension)

        assert response.status_code == 200, "wrong status code, expected 200"

    @allure.feature("Create User")
    @allure.title("Test creates user")
    @allure.description("Test that creates a user")
    @allure.tag("acceptance", "users", "sanity")
    @allure.testcase("TC-123")
    def test_create_user(self):
        test_password = string.ascii_letters
        test_password = ''.join(random.choice(test_password) for i in range(10))
        test_email = string.ascii_letters
        test_email = ''.join(random.choice(test_email) for i in range(10))
        body_user = {
            "Email": f"{test_email}"+"@gmail.com",
            "FullName": "Mauricio Davalos test random",
            "Password": f"{test_password}"
        }

        response = self.rest_client.request("post", self.url_todo_ly_with_extension, body=json.dumps(body_user))

        id_user_created = response.json()["Id"]
        self.list_users.append(id_user_created)
        assert response.status_code == 200, "wrong status code, expected 200"

    @allure.feature("Create User With Existent Email")
    @allure.title("Test create user with existent email")
    @allure.description("Test validate the error message displayed in the response")
    @allure.tag("acceptance", "users", "sanity")
    @allure.testcase("TC-123")
    def test_create_user_with_existent_email(self):

        body_user = {
            "Email": "mauridav377@gmail.com",
            "Password": "automationtest123",
            "FullName": "Mauricio Davalos"
        }

        response = self.rest_client.request("post", self.url_todo_ly_with_extension, body=json.dumps(body_user))
        assert response.status_code == 200, "wrong status code, expected 201"

    @allure.feature("Create User With Short Password")
    @allure.title("Test create user with short password")
    @allure.description("Test validate the error message displayed in the response")
    @allure.tag("acceptance", "users", "sanity")
    @allure.testcase("TC-123")
    def test_create_user_with_short_password(self):

        body_user = {
            "Email": "mauridav380@gmail.com",
            "Password": "",
            "FullName": "Mauricio Davalos"
        }

        response = self.rest_client.request("post", self.url_todo_ly_with_extension, body=json.dumps(body_user))
        assert response.status_code == 200, "wrong status code, expected 202"
