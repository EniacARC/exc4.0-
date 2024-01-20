"""
Author: Yonathan Chapal
Program name: responseFuncs.py
Description: all the functions needed for the res_build function in server.py
Date: 20/1/24
"""
from settings import *
import os


def get_file_data(file_name):
    """
    Get data from file

    :param file_name: Name of the file.
    :type file_name: str

    :return: The file data in binary.
    :rtype: bytes
    """
    try:
        with open(file_name, 'rb') as file:
            file_data = file.read()
            data = file_data
    except FileNotFoundError:
        logging.error(f"File '{file_name}' not found.")
        print(f"File '{file_name}' not found.")
        data = b''
    except Exception as e:
        logging.error(f"Error reading file '{file_name}': {e}")
        print(f"Error reading file '{file_name}': {e}")
        data = b''
    return data


def get_get_request_code(uri):
    """
    Get the HTTP status code for a GET request based on the requested URI.

    :param uri: The requested URI.
    :type uri: str

    :return: The HTTP status code.
    :rtype: int
    """
    code = OK_CODE
    if uri == DEFAULT_VALUE:
        code = BAD_REQUEST_CODE
    elif uri in REDIRECTED_PATHS:
        code = REDIRECTED_CODE
    elif uri in SPECIAL_PATHS:
        code = SPECIAL_PATHS[uri]
    elif not os.path.exists(WEBROOT + uri):
        code = DOESNT_EXIST_CODE

    return code


def get_file_ext(code, uri):
    """
    Get the file extension based on the HTTP status code and requested URI.

    :param code: The HTTP status code.
    :type code: int
    :param uri: The requested URI.
    :type uri: str

    :return: The file extension.
    :rtype: str
    """
    file_path = WEBROOT + DOESNT_EXIST_CONTENT
    if code != DOESNT_EXIST_CODE:
        if uri == '/':
            file_path = WEBROOT + INDEX_URL
        else:
            file_path = WEBROOT + uri

    return os.path.splitext(file_path)[1][1:]


def get_body(uri, code):
    """
    Get the response body based on the requested URI and HTTP status code.

    :param uri: The requested URI.
    :type uri: str
    :param code: The HTTP status code.
    :type code: int

    :return: The response body.
    :rtype: bytes
    """
    body = b''
    if code == DOESNT_EXIST_CODE:
        body = get_file_data(WEBROOT + DOESNT_EXIST_CONTENT)
    elif code == OK_CODE:
        if uri == '/':
            file_path = WEBROOT + INDEX_URL
        else:
            file_path = WEBROOT + uri
        body = get_file_data(file_path)
    return body
