"""
HTTP Server Shell
Author: Barak Gonen and Nir Dweck
Purpose: Provide a basis for Ex. 4
Note: The code is written in a simple way, without classes, log files, or
other utilities, for educational purposes
Usage: Fill the missing functions and constants
"""
import logging
import os
import re
import socket
from comm import *
from settings import *
from http_request import HttpRequest

def get_file_data(file_name):
    """
    Get data from file

    :param file_name: Name of the file.
    :type file_name: str

    :return: The file data in binary.
    :rtype: bytes
    """
    ext = os.path.splitext(file_name)[1][1:]
    try:
        with open(file_name, 'rb') as file:
            file_data = file.read()
            return file_data
    except FileNotFoundError:
        logging.error(f"File '{file_name}' not found.")
        print(f"File '{file_name}' not found.")
        return ""
    except Exception as e:
        logging.error(f"Error reading file '{file_name}': {e}")
        print(f"Error reading file '{file_name}': {e}")
        return ""


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and return TRUE/FALSE and the requested URL.

    :param request: The request received from the client.
    :type request: str

    :return: the requested resource
    :rtype: str
    """
    r_value = ""
    lines = re.split('\r\n', request)
    if len(lines) >= 2:
        req_line = lines[0].split(" ")
        if len(req_line) == 3:
            method, resource, protocol = req_line
            if protocol == HTTP_PROTOCOL_NAME:
                if method in EXCEPTED_METHODS:
                    if resource.startswith("/"):
                        r_value = resource
    return r_value


def send_data(client_socket, res, data):
    """
    :param client_socket: A socket for communication with the client.
    :type client_socket: socket.socket\

    :param res: the response line + headers
    :type res: str

    :param data: the response body
    :type data: bytes

    :return: if the data was sent successfully
    :rtype: bool
    """
    was_sent = False
    try:
        sent = 0
        to_sent = res.encode() + data
        while sent < len(to_sent):
            sent += client_socket.send(to_sent[sent:])
        was_sent = True
    except socket.error as err:
        logging.error(f"error while sending to client: {err}")
    return was_sent


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
        request = HttpRequest(request_str)
        print(request.method)
        print(request.uri)
        print(request.protocol)
        print(request.query)
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
    main()
