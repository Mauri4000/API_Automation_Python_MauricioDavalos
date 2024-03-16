import requests
import logging

from utils.logger import get_logger

token = "1965e681759dcd7924e524583b6332de9e9390c4"
LOGGER = get_logger(__name__, logging.DEBUG)
class TestProjects:

    def test_get_all_projects(self):
        url_todo = "https://api.todoist.com/rest/v2/projects"
        headers_todo = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(url=url_todo, headers=headers_todo)

        LOGGER.info("Response from get all projects: %s", response.json())