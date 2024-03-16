import requests
import logging

from utils.logger import get_logger

#token = "737c0d33409f4a298bd97b606fc14682"
LOGGER = get_logger(__name__, logging.DEBUG)
class TestProjects:

    def test_get_all_projects(self):
        url_todo = "https://todo.ly/api/user.json"
        username = "mauridav377@gmail.com"
        password = "jaggaer"
        response = requests.get(url=url_todo, auth=(username, password))

        LOGGER.info("Response from get all projects: %s", response.json())
        LOGGER.info("Status Code: %s", response.status_code)
        assert response.status_code == 200, "wrong status code, expected 200"