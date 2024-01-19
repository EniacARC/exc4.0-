"""
HTTP Server Shell
Author: Barak Gonen and Nir Dweck
Purpose: Provide a basis for Ex. 4
Note: The code is written in a simple way, without classes, log files, or
other utilities, for educational purposes
Usage: Fill the missing functions and constants
"""

import os
import re
import socket
from comm import *
from serverFunctions import *
from settings import *
from http_request import HttpRequest
import logging

# define log constants
LOG_FORMAT = '%(levelname)s | %(asctime)s | %(processName)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/loggerServer.log'

# TO DO: set constants

CONTENT_TYPE_DICT = {
    "html": "text/html;charset=utf-8",
    "jpg": "image/jpeg",
    "css": "text/css",
    "js": "text/javascript; charset=UTF-8",
    "txt": "text/plain",
    "ico": "image/x-icon",
    "gif": "image/jpeg",
    "png": "image/png"
}

HTTP_PROTOCOL_NAME = "HTTP/1.1"
EXCEPTED_METHODS = ["GET", "POST"]

REDIRECTED_CODE = "302 TEMPORARILY MOVED"
FORBIDDEN_CODE = "403 FORBIDDEN"
ERROR_CODE = "500 INTERNAL SERVER ERROR"
BAD_REQUEST_CODE = "400 BAD REQUEST"
DOESNT_EXIST_CODE = "404 NOT FOUND"
OK_CODE = "200 OK"

SPECIAL_PATHS = {"/forbidden": FORBIDDEN_CODE, "/error": ERROR_CODE}

REDIRECTED_PATHS = ["/moved"]

SERVER_FUNCTIONS = {"calculate-next": calculate_next.__call__, "/calculate-area": calculate_area.__call__}

REDIRECTED_HEADER = "Location: /"
CONTENT_TYPE_HEADER = "Content-Type"
CONTENT_LENGTH_HEADER = "Content-Length"

LINE_SEPERATOR = '\r\n'
HEADERS_SEPERATOR = ': '
WEBROOT = "webroot"
INDEX_URL = "/index.html"
DOESNT_EXIST_CONTENT = "/404.html"
QUEUE_SIZE = 10
MAX_PACKET = 1024
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 2


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


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and return TRUE/FALSE and the requested URL.

    :param request: The request received from the client.
    :type request: HttpRequest

    :return: is valid http request
    :rtype: bool
    """

    if request.method in EXCEPTED_METHODS:
        if request.protocol == HTTP_PROTOCOL_NAME:
            return True
    return False


def create_header(key, value):
    return key + ': ' + value + LINE_SEPERATOR


def build_response(request):
    response = HTTP_PROTOCOL_NAME + ' '
    headers = ""
    data = b''
    if not validate_http_request(request) or request.uri == "None":
        response += BAD_REQUEST_CODE + LINE_SEPERATOR
    elif request.uri in REDIRECTED_PATHS:
        response += REDIRECTED_CODE + LINE_SEPERATOR
        response += REDIRECTED_HEADER

    elif request.uri in SPECIAL_PATHS:
        response += SPECIAL_PATHS[request.uri] + LINE_SEPERATOR

    else:
        if not os.path.exists(WEBROOT + request.uri):
            response += DOESNT_EXIST_CODE + LINE_SEPERATOR
            data = get_file_data(WEBROOT + DOESNT_EXIST_CONTENT)
        else:
            if request.uri == '/':
                file_path = WEBROOT + INDEX_URL
            else:
                file_path = WEBROOT + request.uri
            response += OK_CODE + LINE_SEPERATOR
            print(response)
            data = get_file_data(file_path)

            file_extension = os.path.splitext(file_path)[1][1:]
            headers += create_header(CONTENT_TYPE_HEADER, CONTENT_TYPE_DICT[file_extension])
            headers += create_header(CONTENT_LENGTH_HEADER, str(len(data)))

    return response, headers, data


def handle_client(client_socket):
    """
    Handles client requests: verifies client's requests are legal HTTP, calls
    function to handle the requests
    :param client_socket: the socket for the communication with the client
    :return: None
    """
    print('Client connected')
    while True:
        request_str = rec_metadata(client_socket)
        if request_str != '':
            request = HttpRequest(request_str)
            response_line, headers, data = build_response(request)
            if BAD_REQUEST_CODE in response_line:
                break
            response = response_line.encode() + (headers + LINE_SEPERATOR).encode() + data
            if not send(client_socket, response):
                break
        else:
            break
    print('Closing connection')


def main():
    """
    The mian functions. runs the server code.
    return: none
    """
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        print("Listening for connections on port %d" % PORT)

        while True:
            client_socket, client_address = server_socket.accept()
            try:
                print('New connection received')
                client_socket.settimeout(SOCKET_TIMEOUT)
                handle_client(client_socket)
            except socket.error as err:
                print('received socket exception - ' + str(err))
            finally:
                client_socket.close()
    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        server_socket.close()


if __name__ == "__main__":
    # Call the main handler function
    # make sure we have a logging directory and configure the logging
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)
    main()
