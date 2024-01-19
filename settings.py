# define log constants
import logging


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

INDEX_URL = "/index.html"
HTTP_PROTOCOL_NAME = "HTTP/1.1"
EXCEPTED_METHODS = ["GET", "POST"]

REDIRECTED_LIST = ["/moved"]
REDIRECTED_CODE = "302 TEMPORARILY MOVED"
REDIRECTED_HEADER = "Location: /"

FORBIDDEN_LIST = ["/forbidden"]
FORBIDDEN_CODE = "403 FORBIDDEN"

ERROR_LIST = ["/error"]
ERROR_CODE = "500 INTERNAL SERVER ERROR"

BAD_REQUEST_CODE = "400 BAD REQUEST"

DOESNT_EXIST_CODE = "404 NOT FOUND"
OK_CODE = "200 OK"

DOESNT_EXIST_CONTENT = "/404.html"
WEBROOT = "C:/Users/Yonatan/PycharmProjects/exc4.0/webroot"
QUEUE_SIZE = 10
MAX_PACKET = 1024
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 2