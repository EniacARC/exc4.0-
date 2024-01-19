import re
from settings import *


class HttpRequest:
    def __init__(self, request):
        if self.can_parse(request):
            self.parse_request(request)
        else:
            self.method = "None"
            self.uri = "None"
            self.query = "None"
            self.protocol = "None"
            self.headers = "None"

    @staticmethod
    def can_parse(request):
        """
        checks if string is in a valid http format (not validity for the application).
        :param request:
        :return:
        """
        return bool(re.match(r'^[A-Z]+\s/.*\sHTTP/\d\.\d(.+: .+)*\r\n', request))

    @staticmethod
    def parse_request_line(req_line):
        method, resource, protocol = req_line.split(" ")
        query = {}
        uri = resource
        if '?' in resource:
            uri, query_str = resource.split('?')
            query_str = query_str.split('&')

            query = {}
            for param in query_str:
                key, value = param.split('=')
                query[key] = value

        return method, uri, query, protocol

    @staticmethod
    def parse_headers(headers_str):
        headers = {}
        for element in headers_str:
            key, value = element.split(': ')
            headers[key] = value
        return headers

    def parse_request(self, request):
        lines = re.split('\r\n', request)
        self.method, self.uri, self.query, self.protocol = self.parse_request_line(lines[0])
        self.headers = self.parse_headers(lines[1:len(lines) - 2])
