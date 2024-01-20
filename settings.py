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

REDIRECTED_CODE = 302  # "302 TEMPORARILY MOVED"
FORBIDDEN_CODE = 403  # "403 FORBIDDEN"
ERROR_CODE = 500  # "500 INTERNAL SERVER ERROR"
BAD_REQUEST_CODE = 400  # "400 BAD REQUEST"
DOESNT_EXIST_CODE = 404  # "404 NOT FOUND"
OK_CODE = 200  # "200 OK"

SPECIAL_PATHS = {"/forbidden": FORBIDDEN_CODE, "/error": ERROR_CODE}

REDIRECTED_PATHS = ["/moved"]

STATUS_CONVERT = {OK_CODE: "200 OK", DOESNT_EXIST_CODE: "404 NOT FOUND", BAD_REQUEST_CODE: "400 BAD REQUEST",
                  ERROR_CODE: "500 INTERNAL SERVER ERROR", FORBIDDEN_CODE: "403 FORBIDDEN",
                  REDIRECTED_CODE: "302 TEMPORARILY MOVED"}

REDIRECTED_HEADER = "Location: /"
CONTENT_TYPE_HEADER = "Content-Type"
CONTENT_LENGTH_HEADER = "Content-Length"

WEBROOT = "webroot"
UPLOAD_DIR = WEBROOT + '/upload'
INDEX_URL = "/index.html"
DOESNT_EXIST_CONTENT = "/404.html"
QUEUE_SIZE = 10
MAX_PACKET = 1024
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 2

DEFAULT_VALUE = "None"
LINE_SEPERATOR = '\r\n'
PATTERN = r'^[A-Z]+\s/.*\sHTTP/\d\.\d(.+: .+)*\r\n'
HEADERS_SEPERATOR = ': '
QUERY_SEPERATOR = '?'
PARAMS_SEPERATOR = '&'
PARAM_SEPERATOR = '='
