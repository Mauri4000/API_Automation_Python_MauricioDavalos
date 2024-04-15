import json
import logging

from behave import when, then

from config.config import URL_TODO_LY
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@when(u'I call to {endpoint} endpoint using "{method_name}" method with out body')
def call__endpoint(context, method_name, endpoint):
    url_feature = f"{URL_TODO_LY}/{endpoint}.json"
    body_feature = None

    if method_name == "POST":
        body_feature, _ = get_dat_by_feature(endpoint, context)

    if method_name == "DELETE":
        _, new_feature_url = get_dat_by_feature(endpoint, context)
        url_feature = new_feature_url
    response = context.rest_client.request(method_name=method_name, url=url_feature, body=json.dumps(body_feature))
    # Store id to clean up
    if method_name == "POST":
        context.resource_list[endpoint].append(response["body"]["Id"])

    context.response = response
    LOGGER.debug("PTM Response %s", context.response)


@then(u'I receive the response and validate using "{json_file}" json')
def receive_response(context, json_file):
    context.validate.validate_response(context.response, f"{json_file}")
    LOGGER.debug("I validate the status code is")


@then(u'I validate the status code is {status_code:d}')
def validate_status_code(context, status_code):
    assert status_code == context.response[
        "status_code"], f"expected {status_code} but received {context.response["status_code"]}"
    LOGGER.debug("I validate the status code is %s", status_code)


def get_dat_by_feature(feature, context):
    body = {}
    url = f"{URL_TODO_LY}/{feature}/"
    LOGGER.error("URL: %s", url)
    if feature == "projects":
        body = {
            "Content": "Project PTM"
        }
        if hasattr(context, "project_id"):
            url = url + str(context.project_id) + ".json"
    elif feature == "items":
        body = {
            "Content": "Item PTM"
        }
        if hasattr(context, "items_id"):
            url = url + str(context.items_id) + ".json"
    else:
        LOGGER.error("Feature does not exist")

    return body, url
