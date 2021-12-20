import sys
import string
import secrets
import requests
import pytest
from configparser import ConfigParser
import json
import logging

LOGGER = logging.getLogger(__name__)

# Read configuration variables from config file
config_object = ConfigParser()
config_object.read("config.ini")

env_variable = config_object["ENVIRONMENT"]
access_token = config_object["ACCESSTOKEN"]
url = env_variable["URL"]

# HTTP Error codes
__Unauthorized = '[401]'
__BadRequest = '[400]'
__ResponsePass = '[200]'

def handleErrorCodes(current_status_code):
    """Function to handle https error codes.
    """
    if str(current_status_code) in __Unauthorized:
        LOGGER.error('List all conversation API execution got failed due to Authorization error')
    elif str(current_status_code) in __BadRequest:
        LOGGER.error('List all conversation API execution got failed due to Bad Request')

def randomString(stringLength):
    """Function to generate random string for message name.
    """
    letters = string.ascii_letters
    return ''.join(secrets.choice(letters) for i in range(stringLength))

def setHeader(token):
    """Set request header
    """
    token = access_token["JWT_TOKEN"]
    header = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    return header

def test_createConverstationWithValidJWTToken():
    """Test case to create conversation with valid JWT Token.
    """
    message = "test_message " + randomString(4)
    display_name = "display_name " + randomString(4)

    payload = json.dumps({
        "name": message,
        "display_name": display_name,
        "image_url": "https://example.com/image.png",
        "properties": {
            "ttl": 60
        }
    })
    response = requests.post(url, headers=setHeader(access_token["JWT_TOKEN"]), data=payload)
    assert response.status_code == 200
    json_response = response.json()
    if str(response.status_code) in __ResponsePass:
        assert json_response["id"] != None
        assert (json_response["href"]).endswith(json_response["id"])
        LOGGER.info('Create conversation API with valid JWT Token Test Case is successfully executed')
    else:
        handleErrorCodes(response.status_code)


def test_createConverstationWithInValidJWTToken():
    """Test case to create conversation with invalid JWT Token.
    """
    message = "test_message " + randomString(4)
    display_name = "display_name " + randomString(4)

    payload = json.dumps({
        "name": message,
        "display_name": display_name,
        "image_url": "https://example.com/image.png",
        "properties": {
            "ttl": 60
        }
    })
    response = requests.post(url, headers=setHeader(access_token["INVALID_TOKEN"]), data=payload)
    assert response.status_code == 401, 'Create conversation API with invalid JWT Token should be failed and return 401. Need to fix'


def test_createConverstationWithExpiredJWTToken():
    """Test case to create conversation with expired JWT Token.
    """
    message = "test_message " + randomString(4)
    display_name = "display_name " + randomString(4)

    payload = json.dumps({
        "name": message,
        "display_name": display_name,
        "image_url": "https://example.com/image.png",
        "properties": {
            "ttl": 60
        }
    })
    response = requests.post(url, headers=setHeader(access_token["EXPIRED_TOKEN"]), data=payload)
    assert response.status_code == 401, 'Create conversation API with expired JWT Token should be failed and return 401. Need to fix'


def test_createConverstationWithInvalidPayLoad():
    """Test case to create conversation with invalid payload.
    """
    payload = json.dumps({
        "name": 123,
        "display_name": 578,
        "image_url": "example.com/image.png",
        "properties": {
            "ttl": 60
        }
    })
    response = requests.post(url, headers=setHeader(access_token["JWT_TOKEN"]), data=payload)
    assert response.status_code == 400
    json_response = response.json()
    assert json_response["description"] == 'Input validation failure.'
    assert json_response["error"]["name"][0] == "\"name\" must be a string"
    assert json_response["error"]["display_name"][0] == '\"display_name\" must be a string'
    assert json_response["error"]["image_url"][0] == '\"image_url\" must be a valid uri'
    LOGGER.info('Test case returns ' + str(response.status_code) + " because " + str(json_response["error"]))


def test_createConverstationWithNulldPayLoad():
    """Test case to create conversation with null payload.
    """
    payload = json.dumps({})
    response = requests.post(url, headers=setHeader(access_token["JWT_TOKEN"]), data=payload)
    # It will create conversation with default name
    assert response.status_code == 200
    json_response = response.json()
    if str(response.status_code) in __ResponsePass:
        assert json_response["id"] != None
        assert (json_response["href"]).endswith(json_response["id"])
        LOGGER.info('Create conversation API with valid JWT Token Test Case is successfully executed')
    else:
        handleErrorCodes(response.status_code)


def test_createConverstationWithInvalidJsonFormatPayLoad():
    """Test case to create conversation with invalid json payload.
    """
    message = "test_message " + randomString(4)
    display_name = "display_name " + randomString(4)

    payload = json.dumps({
        "name": message,
        "display_name": display_name,
        "image_url": "https://example.com/image.png",
        "properties": {
            "ttl": 60,
        }
    })
    response = requests.post(url, headers=setHeader(access_token["JWT_TOKEN"]), data=payload)
    assert response.status_code == 400, 'This is invalid JSON formata payload, hence it should return 400'
