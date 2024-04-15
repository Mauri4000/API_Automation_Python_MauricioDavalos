import json
import logging

from config.config import URL_TODO_LY
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class Project:

    def __init__(self, rest_client=None):
        self.url_projects = f"{URL_TODO_LY}/projects.json"
        if rest_client is None:
            self.rest_client = RestClient()

    def create_project(self, body=None):
        body_project = body
        if body is None:
            body_project = {
                "Content": "XOKAS"
            }
        response = self.rest_client.request("post", url=self.url_projects, body=json.dumps(body_project))

        return response, self.rest_client

    def delete_project(self, project_id):
        """
        Delete project
        :param project_id:
        :return:
        """
        LOGGER.info("Cleanup project...")
        url_delete_project = f"{URL_TODO_LY}/projects/{project_id}.json"
        response = self.rest_client.request("delete", url=url_delete_project)
        if response["status_code"] == 204:
            LOGGER.info("Project Id: %s deleted", project_id)