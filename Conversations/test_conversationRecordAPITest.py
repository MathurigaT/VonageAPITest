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
    elif str(current_status_code) in __BadRequest:
        LOGGER.error('Resource is not available')

def setHeader(token):
    token = access_token["JWT_TOKEN"]
    header = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    return header

def randomString(stringLength):
    letters = string.ascii_letters
    return ''.join(secrets.choice(letters) for i in range(stringLength))

def createDummyConversation():
    payload = json.dumps({
        "name": randomString(5),
        "display_name": randomString(5),
        "image_url": "https://example.com/image.png",
        "properties": {
            "ttl": 60
        }
    })
    response = requests.post(url, headers=setHeader(access_token["JWT_TOKEN"]), data=payload)
    return str(response.json()["id"])

def test_recordConverstationWithRequiredField():
    """Test case to record conversation with required field.
    """
    conversation_id=createDummyConversation()
    payload = json.dumps({
        "action": "start"
    })
    LOGGER.info("Endpoint: "+url+"/"+conversation_id+"/record")
    response = requests.put(url+"/"+conversation_id+"/record", headers=setHeader(access_token["JWT_TOKEN"]),data=payload)
    json_response = response.json()
    assert response.status_code == 200, LOGGER.info("Response "+str(json_response))