"""
Author: Yonathan Chapal
Program name: http_request
Description: a class for parsing and storing http requests
Date: 20/1/24
"""
import re
from settings import *


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
        Check if string is in a valid HTTP format (not checking for application-specific validity).

        :param request: The HTTP request string.
        :type request: str

        :return: True if the string is in a valid HTTP format, False otherwise.
        :rtype: bool
        """
        return bool(re.match(PATTERN, request))

    @staticmethod
    def parse_request_line(req_line):
        """
        Parse the request line into method, URI, query parameters, and protocol.

        :param req_line: The request line.
        :type req_line: str

        :return: Tuple containing method, URI, query parameters, and protocol.
        :rtype: tuple
        """
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
        """
        Parse headers string into a dictionary.

        :param headers_str: The headers string.
        :type headers_str: list[str]

        :return: Dictionary containing headers.
        :rtype: dict
        """
        headers = {}
        for element in headers_str:
            key, value = element.split(HEADERS_SEPERATOR)
            headers[key] = value
        return headers

    def parse_request(self, request):
        """
        Parse the entire HTTP request.

        :param request: The HTTP request string.
        :type request: str

        :return: None
        """
        lines = re.split(LINE_SEPERATOR, request)
        self.method, self.uri, self.query, self.protocol = self.parse_request_line(lines[0])
        self.headers = self.parse_headers(lines[1:len(lines) - 2])
