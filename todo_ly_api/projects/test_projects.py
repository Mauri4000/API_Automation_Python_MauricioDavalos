import json

import allure
import logging

from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@allure.epic("TODOLY API")
@allure.story("Projects")
class TestProjects:
    url_todo_ly_extension = None
    url_todo_ly = None
    url_todo_ly_with_extension = None

    @classmethod
    def setup_class(cls):
        LOGGER.debug("SetupClass method")
        cls.url_todo_ly = "https://todo.ly/api/projects"
        cls.url_todo_ly_extension = ".json"
        cls.url_todo_ly_with_extension = cls.url_todo_ly + cls.url_todo_ly_extension
        cls.list_projects = []
        cls.rest_client = RestClient()

    @allure.feature("List Projects")
    @allure.title("Test get all projects")
    @allure.description("Test that show the response for all created projects")
    @allure.tag("acceptance", "users", "sanity")
    @allure.testcase("TC-123")
    def test_get_all_projects(self):

        response = self.rest_client.request("get", url=self.url_todo_ly_with_extension)

        assert response.status_code == 200, "wrong status code, expected 200"

    @allure.feature("Create Project")
    @allure.title("Test create a project")
    @allure.description("Test that show the response of created project")
    @allure.tag("acceptance", "users", "sanity")
    @allure.testcase("TC-123")
    def test_create_project(self):

        body_project = {
            "Content": "Mauricio 987"
        }

        response = self.rest_client.request("post", self.url_todo_ly_with_extension, body=json.dumps(body_project))

        id_project_created = response.json()["Id"]
        self.list_projects.append(id_project_created)
        assert response.status_code == 200, "wrong status code, expected 200"

    @allure.feature("Delete Project")
    @allure.title("Test delete a project")
    @allure.description("Test that delete a project by id")
    @allure.tag("acceptance", "users", "sanity")
    @allure.testcase("TC-123")
    def test_delete_project(self, create_project):
        id_project_delete = create_project["Id"]
        url_todo_ly = f"{self.url_todo_ly}/{id_project_delete}{self.url_todo_ly_extension}"

        response = self.rest_client.request("delete", url=url_todo_ly)

        assert response.status_code == 200, "wrong status code, expected 200"

    @allure.feature("Update Project")
    @allure.title("Test update a project")
    @allure.description("Test that updates a project by id")
    @allure.tag("acceptance", "users", "sanity")
    @allure.testcase("TC-123")
    def test_update_project(self, create_project):
        id_project_update = create_project["Id"]
        LOGGER.debug("Project to update: %s", id_project_update)

        url_todo_ly = f"{self.url_todo_ly}/{id_project_update}{self.url_todo_ly_extension}"
        body_project = {
            "Icon": 5
        }
        response = self.rest_client.request("put", url=url_todo_ly, body=json.dumps(body_project))
        # Add to list of projects to be deleted for cleanup teardown
        self.list_projects.append(id_project_update)
        assert response.status_code == 200, "wrong status code, expected 200"

    @classmethod
    def teardown_class(cls):
        """
        Delete all projects used in tests
        """
        LOGGER.info("Cleanup projects...")
        for id_project in cls.list_projects:
            url_delete_project = f"{cls.url_todo_ly}/{id_project}{cls.url_todo_ly_extension}"
            response = cls.rest_client.request("delete", url=url_delete_project)
            if response.status_code == 204:
                LOGGER.info("Project Id deleted: %s", id_project)
