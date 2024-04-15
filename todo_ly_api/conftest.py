import json
import logging
import pytest
import requests

from config.config import HEADERS_TODO_LY, URL_TODO_LY
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@pytest.fixture()
def create_project(request):

    LOGGER.debug("Create Project fixture")
    environment = request.config.getoption("--env")
    LOGGER.critical("Environment selected: %s", environment)
    rest_client = RestClient()

    body_project = {
        "Content": "Project from fixture"
    }
    url_project = URL_TODO_LY + "/projects.json"

    response = rest_client.request("post", url_project, body=json.dumps(body_project))

    return response.json()

@pytest.fixture()
def create_item(request):

    LOGGER.debug("Create Item fixture")
    environment = request.config.getoption("--env")
    LOGGER.critical("Environment selected: %s", environment)
    rest_client = RestClient()

    body_project = {
        "Content": "Item from fixture"
    }
    url_project = URL_TODO_LY + "/items.json"

    response = rest_client.request("post", url_project, body=json.dumps(body_project))

    return response.json()

def pytest_addoption(parser):
    parser.addoption(
        '--env', action='store', default='dev', help="Environment where the tests are executed"
    )
    parser.addoption(
        '--browser', action='store', default='chrome', help="Browser type to execute the UI tests"
    )
