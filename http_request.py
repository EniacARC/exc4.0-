import re
from settings import *

DEFAULT_VALUE = "None"
LINE_SEPERATOR = '\r\n'
PATTERN = r'^[A-Z]+\s/.*\sHTTP/\d\.\d(.+: .+)*\r\n'
HEADERS_SEPERATOR = ': '
QUERY_SEPERATOR = '?'
PARAMS_SEPERATOR = '&'
PARAM_SEPERATOR = '='


class HttpRequest:
    def __init__(self, request):
        if self.can_parse(request):
            self.parse_request(request)
        else:
            self.method = DEFAULT_VALUE
            self.uri = DEFAULT_VALUE
            self.query = DEFAULT_VALUE
            self.protocol = DEFAULT_VALUE
            self.headers = DEFAULT_VALUE

    @staticmethod
    def can_parse(request):
        """
        checks if string is in a valid http format (not validity for the application).
        :param request:
        :return:
        """
        return bool(re.match(PATTERN, request))

    @staticmethod
    def parse_request_line(req_line):
        method, resource, protocol = req_line.split(" ")
        query = {}
        uri = resource
        if QUERY_SEPERATOR in resource:
            uri, query_str = resource.split(QUERY_SEPERATOR)
            query_str = query_str.split(PARAMS_SEPERATOR)

            query = {}
            for param in query_str:
                key, value = param.split(PARAM_SEPERATOR)
                query[key] = value

        return method, uri, query, protocol

    @staticmethod
    def parse_headers(headers_str):
        headers = {}
        for element in headers_str:
            key, value = element.split(HEADERS_SEPERATOR)
            headers[key] = value
        return headers

    def parse_request(self, request):
        lines = re.split(LINE_SEPERATOR, request)
        self.method, self.uri, self.query, self.protocol = self.parse_request_line(lines[0])
        self.headers = self.parse_headers(lines[1:len(lines) - 2])
