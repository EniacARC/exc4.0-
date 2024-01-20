"""
Author: Yonathan Chapal
Program name: serverFunctions.py
Description: the special functions of the server
Date: 20/1/24
"""
import socket
from comm import *
from responseFuncs import *
from http_request import HttpRequest


def calculate_next(sock, request):
    """
    Calculate the next number based on the provided request.

    :param sock: used for symmetry
    :type sock: socket.socket
    :param request: The HTTP request object.
    :type request: HttpRequest

    :return: Tuple containing HTTP status code, encoded next number, and content type.
    :rtype: tuple
    """
    code = 400
    next_num = ""
    if request.method == "GET" and request.query["num"].isnumeric():
        next_num = str(int(request.query["num"]) + 1)
        code = 200
    return code, next_num.encode(), "txt"


def calculate_area(sock, request):
    """
    Calculate the area of a triangle based on the provided request.

    :param sock: used for symmetry
    :type sock: socket.socket
    :param request: The HTTP request object.
    :type request: HttpRequest

    :return: Tuple containing HTTP status code, encoded area, and content type.
    :rtype: tuple
    """
    code = 400
    area = ""
    if request.method == "GET" and request.query["height"].isnumeric() and request.query["width"].isnumeric():
        area = str(int(request.query["height"]) * int(request.query["width"]) * 0.5)
        code = 200
    return code, area.encode(), "txt"


def upload_file(sock, request):
    """
    Upload a file based on the provided request.

    :param sock: The socket for communication.
    :type sock: socket.socket
    :param request: The HTTP request object.
    :type request: HttpRequest

    :return: Tuple containing HTTP status code, encoded response body, and content type.
    :rtype: tuple
    """
    code = 500
    body = ""
    try:
        if request.method == "POST":
            file_data = rec_body(sock, int(request.headers["Content-Length"]))
            print(file_data)
            if file_data != '':
                if not os.path.isdir(UPLOAD_DIR):
                    os.makedirs(UPLOAD_DIR)
                file_path = UPLOAD_DIR + '/' + request.query["file-name"]
                print(file_path)
                with open(file_path, 'wb') as file:
                    file.write(file_data)
                code = 200
    except OSError as err:
        logging.error(f"error while saving file {request.query['file-name']}: {err}")

    return code, body.encode(), "None"


def get_image(sock, request):
    """
    Get an image based on the provided request.

    :param sock: used for symmetry
    :type sock: socket.socket
    :param request: The HTTP request object.
    :type request: HttpRequest

    :return: Tuple containing HTTP status code, image body, and content type.
    :rtype: tuple
    """
    code = 500
    body = b''
    ext = ""
    if request.method == "GET":
        image_path = UPLOAD_DIR + '/' + request.query["image-name"]
        uri = image_path[len(WEBROOT):]
        code = get_get_request_code(uri)
        body = get_body(uri, code)
        ext = get_file_ext(code, image_path)
    return code, body, ext
