import string
from random import random, choice, sample
import secrets
import requests
import pytest
from configparser import ConfigParser
import json
import logging

LOGGER = logging.getLogger(__name__)

# Read configs from given command line parameters
config_object = ConfigParser()
config_object.read("config.ini")

env_variable = config_object["ENVIRONMENT"]
access_token = config_object["ACCESSTOKEN"]
url = env_variable["URL"]
__ResponsePass = '[200]'
__Unauthorized = '[401]'
__BadRequest = '[400]'

def handleErrorCodes(current_status_code):
    if str(current_status_code) in __Unauthorized:
        LOGGER.error('List all conversation API execution got failed due to Authorization error')
    elif str(current_status_code) in __BadRequest:
        LOGGER.error('List all conversation API execution got failed due to Bad Request')

def randomString(stringLength):
    letters = string.ascii_letters
    return ''.join(secrets.choice(letters) for i in range(stringLength))

def setHeader(token):
    token = access_token["JWT_TOKEN"]
    header = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    return header

def test_createConverstationWithValidJWTToken():
    message="test_message "+randomString(4)
    display_name="display_name "+randomString(4)

    payload = json.dumps({
        "name": message,
        "display_name": display_name,
        "image_url": "https://example.com/image.png",
        "properties": {
           "ttl": 60
        }
    })
    response = requests.post(url, headers=setHeader(access_token["JWT_TOKEN"]),data=payload)
    assert response.status_code == 200
    json_response = response.json()
    if str(response.status_code) in __ResponsePass:
        assert json_response["id"]!=None
        assert (json_response["href"]).endswith(json_response["id"])
        LOGGER.info('Create conversation API with valid JWT Token Test Case is successfully executed')
    else:
        handleErrorCodes(response.status_code)

def test_createConverstationWithInValidJWTToken():
    message="test_message "+randomString(4)
    display_name="display_name "+randomString(4)

    payload = json.dumps({
        "name": message,
        "display_name": display_name,
        "image_url": "https://example.com/image.png",
        "properties": {
           "ttl": 60
        }
    })
    response = requests.post(url, headers=setHeader(access_token["INVALID_TOKEN"]),data=payload)
    assert response.status_code == 400, 'Create conversation API with invalid JWT Token should be failed. Need to fix'

def test_createConverstationWithExpiredJWTToken():
    message="test_message "+randomString(4)
    display_name="display_name "+randomString(4)

    payload = json.dumps({
        "name": message,
        "display_name": display_name,
        "image_url": "https://example.com/image.png",
        "properties": {
           "ttl": 60
        }
    })
    response = requests.post(url, headers=setHeader(access_token["EXPIRED_TOKEN"]),data=payload)
    assert response.status_code == 400, 'Create conversation API with in expired JWT Token should be failed. Need to fix'

def test_createConverstationWithInvalidPayLoad():
    payload = json.dumps({
        "name": 123,
        "display_name": 578,
        "image_url": "example.com/image.png",
        "properties": {
           "ttl": 60
        }
    })
    response = requests.post(url, headers=setHeader(access_token["JWT_TOKEN"]),data=payload)
    assert response.status_code == 400
    json_response = response.json()
    assert json_response["description"]=='Input validation failure.'
    assert json_response["error"]["name"][0]=="\"name\" must be a string"
    assert json_response["error"]["display_name"][0] == '\"display_name\" must be a string'
    assert json_response["error"]["image_url"][0] == '\"image_url\" must be a valid uri'
    LOGGER.info('Test case returns '+str(response.status_code)+ " because "+ str(json_response["error"]))

def test_createConverstationWithNulldPayLoad():
    payload = json.dumps({})
    response = requests.post(url, headers=setHeader(access_token["JWT_TOKEN"]),data=payload)
    # It will create conversation with default name
    assert response.status_code == 200
    json_response = response.json()
    if str(response.status_code) in __ResponsePass:
        assert json_response["id"] != None
        assert (json_response["href"]).endswith(json_response["id"])
        LOGGER.info('Create conversation API with valid JWT Token Test Case is successfully executed')
    else:
        handleErrorCodes(response.status_code)


def test_createConverstationWithInvalidJsonFormatdPayLoad():
    message="test_message "+randomString(4)
    display_name="display_name "+randomString(4)

    payload = json.dumps({
        "name": message,
        "display_name": display_name,
        "image_url": "https://example.com/image.png",
        "properties": {
           "ttl": 60,
        }
    })
    response = requests.post(url, headers=setHeader(access_token["JWT_TOKEN"]),data=payload)
    assert response.status_code == 400, 'Data for this payload is invalid JSON format, hence it should return 400'