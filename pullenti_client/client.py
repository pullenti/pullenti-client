# coding: utf-8
from __future__ import unicode_literals

import xml.etree.ElementTree as ET

import requests

from .compat import maybe_decode
from .utils import Record
from .flat import FlatResult
from .result import Result


def parse_xml(data):
    return ET.fromstring(data)


def parse_response(text, xml):
    result = FlatResult.from_xml(text, xml)
    return Result.from_flat(result)


class ClientError(Exception):
    pass


def parse_error(xml):
    message = xml.text
    return ClientError(message)


class Client(Record):
    __attributes__ = ['host', 'port']

    def __init__(self, host, port):
        self.host = host
        self.port = port

    @property
    def endpoint(self):
        return 'http://{host}:{port}/'.format(
            host=self.host,
            port=self.port
        )

    def payload(self, text):
        return text.encode('utf8')

    def __call__(self, text):
        text = maybe_decode(text)
        response = requests.post(
            self.endpoint,
            data=self.payload(text)
        )
        xml = parse_xml(response.content)
        if response.status_code == 200:
            return parse_response(text, xml)
        else:
            raise parse_error(xml)
