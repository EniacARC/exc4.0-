"""
Author: Yonathan Chapal
Program name: comms.py
Description: the communication functions
Date: 12/1/24
"""
import re
import socket
import logging


def send(client_socket, data):
    """
    send a msg using connection socket

    :param client_socket: the connection socket
    :type client_socket: socket.socket

    :param data: the msg to send
    :type data: str

    :return: if the sending was a success
    :rtype: bool
    """
    success = True
    len_data = 0
    try:
        while len_data < len(data):
            len_data += client_socket.send(data[len_data:].encode())
    except socket.error as err:
        logging.error(f"error while sending data: {err}")
        success = False
    finally:
        return success


def rec_metadata(sock):
    """
     receive metadata from the server

     :param sock: the socket for communication
     :type sock: socket.socket

     :return: received metadata
     :rtype: str
     """
    req = ''
    try:
        while not re.search('\r\n\r\n', req):
            packet = sock.recv(1).decode()
            if packet == '':
                req = ''
                break
            req += packet
    except socket.error as err:
        logging.error(f"error while recv metadata: {err}")
        req = ''
    finally:
        return req


def rec_body(sock, num):
    """
     receive a constant-sized message from the server

     :param sock: the socket for communication
     :type sock: socket.socket

     :param num: the size of the message to receive
     :type num: int

     :return: received message
     :rtype: str
     """
    bod = ''
    try:
        while len(bod) < num:
            chunk = sock.recv(num - len(bod)).decode()
            if chunk == '':
                bod = ''
                break
            bod += chunk
    except socket.error as err:
        logging.error(f"error while recv body: {err}")
        bod = ''
    finally:
        return bod

