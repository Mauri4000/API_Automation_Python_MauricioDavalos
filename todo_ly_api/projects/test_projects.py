import json
import requests
import logging

from config.config import HEADERS_TODO_LY
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)
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

    def test_get_all_projects(self):

        response = requests.get(url=self.url_todo_ly_with_extension, headers=HEADERS_TODO_LY)

        LOGGER.info("Response from get all projects: %s", response.json())
        LOGGER.info("Status Code: %s", response.status_code)
        assert response.status_code == 200, "wrong status code, expected 200"

    def test_create_project(self):

        body_project = {
            "Content": "Mauricio 987"
        }

        response = requests.post(self.url_todo_ly_with_extension, headers=HEADERS_TODO_LY, data=json.dumps(body_project))
        LOGGER.info("Response from get all projects: %s", response.json())
        LOGGER.info("Status Code: %s", response.status_code)
        id_project_created = response.json()["Id"]
        self.list_projects.append(id_project_created)
        assert response.status_code == 200, "wrong status code, expected 200"

    def test_delete_project(self, create_project):
        id_project_delete = create_project["Id"]
        url_todo_ly = f"{self.url_todo_ly}/{id_project_delete}{self.url_todo_ly_extension}"

        response = requests.delete(url=url_todo_ly, headers=HEADERS_TODO_LY)

        LOGGER.info("Status Code: %s", response.status_code)
        assert response.status_code == 200, "wrong status code, expected 200"

    def test_update_project(self, create_project):
        id_project_update = create_project["Id"]
        LOGGER.debug("Project to update: %s", id_project_update)

        url_todo_ly = f"{self.url_todo_ly}/{id_project_update}{self.url_todo_ly_extension}"
        LOGGER.debug("URL: %s", url_todo_ly)
        body_project = {
            "Icon": 5
        }
        LOGGER.debug("CONTENT TO CREATE PROJECT: %s", body_project)
        response = requests.put(url=url_todo_ly, headers=HEADERS_TODO_LY, data=json.dumps(body_project))
        LOGGER.info("Response from updated project: %s", response.json())
        LOGGER.info("Status Code: %s", response.status_code)
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
            response = requests.delete(url=url_delete_project, headers=HEADERS_TODO_LY)
            if response.status_code == 204:
                LOGGER.info("Project Id deleted: %s", id_project)
