"""
HTTP Server Shell
Author: Barak Gonen and Nir Dweck
Purpose: Provide a basis for Ex. 4
Note: The code is written in a simple way, without classes, log files, or
other utilities, for educational purposes
Usage: Fill the missing functions and constants
"""

import os
import socket
from comm import *
from settings import *
from http_request import HttpRequest
from serverFunctions import *
from responseFuncs import *

SERVER_FUNCTIONS = {"/calculate-next": calculate_next.__call__, "/calculate-area": calculate_area.__call__,
                    "/upload": upload_file.__call__, "/image": get_image.__call__}


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


def build_res(code, body, body_type):
    """
    Build an HTTP response.

    :param code: The HTTP status code.
    :type code: int

    :param body: The response body.
    :type body: bytes

    :param body_type: The content type of the response body.
    :type body_type: str

    :return: The constructed HTTP response.
    :rtype: bytes
    """
    response_line = HTTP_PROTOCOL_NAME + ' ' + STATUS_CONVERT[code] + LINE_SEPERATOR
    headers = ""
    if code == REDIRECTED_CODE:
        headers += REDIRECTED_HEADER
    if body != b'':
        headers += CONTENT_TYPE_HEADER + ': ' + CONTENT_TYPE_DICT[body_type] + LINE_SEPERATOR
        headers += CONTENT_LENGTH_HEADER + ': ' + str(len(body)) + LINE_SEPERATOR
    headers += LINE_SEPERATOR

    return response_line.encode() + headers.encode() + body


def handle_client(client_socket):
    """
       Handles client requests: verifies client's requests are legal HTTP, calls
       function to handle the requests.

       :param client_socket: The socket for communication with the client.
       :type client_socket: socket

       :return: None
       """
    print('Client connected')
    while True:
        request_str = rec_metadata(client_socket)
        if request_str != '':
            request = HttpRequest(request_str)
            code = BAD_REQUEST_CODE
            body = b''
            body_type = ''
            if validate_http_request(request):
                if request.uri in SERVER_FUNCTIONS:
                    code, body, body_type = SERVER_FUNCTIONS[request.uri](client_socket, request)
                else:
                    if request.method == "GET":
                        code = get_get_request_code(request.uri)
                        body = get_body(request.uri, code)
                        body_type = get_file_ext(code, request.uri)

            response = build_res(code, body, body_type)
            if not send(client_socket, response) or code == BAD_REQUEST_CODE:
                break

        else:
            break
    print('Closing connection')


def main():
    """
    The main functions. Runs the server code.

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

    valid_request = "GET /index.html HTTP/1.1\r\n\r\n"
    valid_http_request = HttpRequest(valid_request)
    assert validate_http_request(valid_http_request)

    invalid_request = "INVALID_REQUEST\r\n\r\n"
    invalid_http_request = HttpRequest(invalid_request)
    assert not validate_http_request(invalid_http_request)

    response = build_res(200, b'OK', 'txt')
    expected_response = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 2\r\n\r\nOK'
    assert response == expected_response

    request_str = "GET /calculate-next?num=5 HTTP/1.1\r\n\r\n"
    request = HttpRequest(request_str)
    code, body, content_type = calculate_next(None, request)
    assert code == 200
    assert body == b'6'
    assert content_type == 'txt'

    request_str = "GET /calculate-next?num=gh HTTP/1.1\r\n\r\n"
    request = HttpRequest(request_str)
    code, body, content_type = calculate_next(None, request)
    assert code == 400
    assert body == b''

    request_str = "GET /calculate-area?height=5&width=3 HTTP/1.1\r\n\r\n"
    request = HttpRequest(request_str)
    code, body, content_type = calculate_area(None, request)
    assert code == 200
    assert body == b'7.5'
    assert content_type == 'txt'

    request_str = "GET /calculate-area?height=awda&width=3 HTTP/1.1\r\n\r\n"
    request = HttpRequest(request_str)
    code, body, content_type = calculate_area(None, request)
    assert code == 400
    assert body == b''

    request_str = "GET /image?image-name=orch.jpg HTTP/1.1\r\n\r\n"
    request = HttpRequest(request_str)
    code, body, content_type = get_image(None, request)
    assert code == 200
    assert content_type == 'jpg'

    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)
    main()
