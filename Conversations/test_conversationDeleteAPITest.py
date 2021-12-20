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
__NotFound = '[404]'

def handleErrorCodes(current_status_code):
    if str(current_status_code) in __Unauthorized:
        LOGGER.error('List all conversation API execution got failed due to Authorization error')
    elif str(current_status_code) in __BadRequest:
        LOGGER.error('List all conversation API execution got failed due to Bad Request')

def setHeader(token):
    token = access_token["JWT_TOKEN"]
    header = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    return header

def createDummyConversation():
    payload = json.dumps({
        "name": "foo",
        "display_name": "foo",
        "image_url": "https://example.com/image.png",
        "properties": {
            "ttl": 60
        }
    })
    response = requests.post(url, headers=setHeader(access_token["JWT_TOKEN"]), data=payload)
    return str(response.json()["id"])

def test_deleteConverstationWithValidJWTToken():
    """Test case to delete conversation with valid JWT Token.
    """
    conversation_id=createDummyConversation()
    LOGGER.info(conversation_id)
    response = requests.delete(url+"/"+conversation_id, headers=setHeader(access_token["JWT_TOKEN"]))
    LOGGER.info(response.status_code)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response=={}
    LOGGER.info(json_response)

def test_deleteConverstationWithoutConversationId():
    """Test case to delete conversation without conversation id.
    """
    conversation_id=None
    LOGGER.info(conversation_id)
    response = requests.delete(url+"/"+str(conversation_id), headers=setHeader(access_token["JWT_TOKEN"]))
    LOGGER.info(response.status_code)
    assert response.status_code == 404
    json_response = response.json()
    assert json_response["description"] == "Conversation does not exist, or you do not have access."
    assert json_response["code"] == "conversation:error:not-found"

def test_deleteConverstationWithInValidJWTToken():
    """Test case to delete conversation with invalid JWT Token.
    """
    conversation_id=createDummyConversation()
    LOGGER.info(conversation_id)
    response = requests.delete(url+"/"+conversation_id, headers=setHeader(access_token["INVALID_TOKEN"]))
    LOGGER.info(response.status_code)
    assert response.status_code == 401, "Delete conversation API with invalid JWT Token should be failed and return 401. Need to fix"

def test_deleteConverstationWithExpiredJWTToken():
    """Test case to delete conversation with expired JWT Token.
    """
    conversation_id=createDummyConversation()
    LOGGER.info(conversation_id)
    response = requests.delete(url+"/"+conversation_id, headers=setHeader(access_token["EXPIRED_TOKEN"]))
    LOGGER.info(response.status_code)
    assert response.status_code == 401, "Delete conversation API with expired JWT Token should be failed and return 401. Need to fix"