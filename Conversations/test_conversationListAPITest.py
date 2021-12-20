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

def handleErrorCodes(current_status_code):
        __Unauthorized = '[401]'
        __BadRequest = '[400]'
        if str(current_status_code) in __Unauthorized:
            LOGGER.error('List all conversation API execution got failed due to Authorization error')
        elif str(current_status_code) in __BadRequest:
            LOGGER.error('List all conversation API execution got failed due to Bad Request')

def setHeader(token):
    token = access_token["JWT_TOKEN"]
    header = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    return header

def test_listConverstationWithValidJWTToken():
    """Test case to list conversation without JWT Token.
    """
    response = requests.get(url, headers=setHeader(access_token["JWT_TOKEN"]))
    assert response.status_code == 200
    json_response=response.json()
    if str(response.status_code) in __ResponsePass:
        if json_response["count"] >0:
            assert (json_response["_embedded"]["conversations"][0]["_links"]["self"]["href"]).endswith(json_response["_embedded"]["conversations"][0]["uuid"])
            LOGGER.info('List all conversation API with valid JWT Token Test Case is successfully executed')
    else:
        handleErrorCodes(response.status_code)

def test_listConverstationWithOutJWTToken():
    """Test case to list conversation without JWT Token.
    """
    response = requests.get(url)
    json_response=response.json()
    assert response.status_code == 401
    assert json_response["code"] == 'system:error:invalid-token'
    LOGGER.info('List all conversation API with valid JWT Token Test Case is successfully executed')


def test_listConverstationWithInvalidJWTToken():
    """Test case to list conversation with invalid JWT Token.
    """
    response = requests.get(url,headers=setHeader(access_token["INVALID_TOKEN"]))
    json_response = response.json()
    assert response.status_code == 401 , "JWT is invalid but test case returns " + str(response.status_code)
    assert json_response["code"] == 'system:error:invalid-token'
    LOGGER.info('List all conversation API with invalid JWT Token Test Case is successfully executed')

def test_listConverstationWithExpiredJWTToken():
    """Test case to list conversation with expired JWT Token.
    """
    response = requests.get(url,headers=setHeader(access_token["EXPIRED_TOKEN"]))
    json_response = response.json()
    assert response.status_code == 401 , "JWT is expired but test case returns " + str(response.status_code)
    assert json_response["code"] == 'system:error:invalid-token'
    LOGGER.info('List all conversation API with expired JWT Token Test Case is successfully executed')