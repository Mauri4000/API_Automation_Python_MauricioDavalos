import json
import logging
import pytest
import requests

from config.config import HEADERS_TODO_LY, URL_TODO_LY
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@pytest.fixture()
def create_project(request):

    LOGGER.debug("Create Project fixture")
    environment = request.config.getoption("--env")
    LOGGER.critical("Environment selected: %s", environment)

    body_project = {
        "Content": "Project from fixture"
    }
    url_project = URL_TODO_LY + "/projects.json"

    response = requests.post(url_project, headers=HEADERS_TODO_LY,
                             data=json.dumps(body_project))

    return response.json()


def pytest_addoption(parser):
    parser.addoption(
        '--env', action='store', default='dev', help="Environment where the tests are executed"
    )
    parser.addoption(
        '--browser', action='store', default='chrome', help="Browser type to execute the UI tests"
    )
