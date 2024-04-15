import logging

from config.config import URL_TODO_LY
from entities.project import Project
from helpers.rest_client import RestClient
from helpers.validate_response import ValidateResponse
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


def before_all(context):
    LOGGER.debug("Before all")
    context.list_projects = []
    context.rest_client = RestClient()
    context.validate = ValidateResponse()
    context.project = Project()
    context.resource_list = {
        "projects": [],
        "items": [],
        "users": []
    }


def before_feature(context, feature):
    LOGGER.debug("Before Feature")


def before_scenario(context, scenario):
    LOGGER.debug("Before Scenario")
    if "project_id" in scenario.tags:
        project, _ = context.project.create_project()
        LOGGER.debug("Project PTM: %s", project)
        context.project_id = project["body"]["Id"]
        LOGGER.debug("Project created in before scenario: %s", context.project_id)

    if "item_id" in scenario.tags:
        item, _ = context.item.create_item()
        LOGGER.debug("ITEM PTM: %s", item)
        context.item_id = item["body"]["Id"]
        LOGGER.debug("Item created in before scenario: %s", context.item_id)


def after_scenario(context, scenario):
    LOGGER.debug("After Scenario")


def after_feature(context, feature):
    LOGGER.debug("After Feature")
    delete_resources(context)


def after_all(context):
    LOGGER.debug("After all")


def delete_resources(context):
    LOGGER.debug("Delete resources....")
    for resource in context.resource_list:
        for resource_id in context.resource_list[resource]:
            url = f"{URL_TODO_LY}/{resource}/{resource_id}.json"
            context.rest_client.request("delete", url)
            LOGGER.debug("Deleting %s with Id: %s", resource, resource_id)
