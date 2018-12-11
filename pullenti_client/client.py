# coding: utf-8
from __future__ import unicode_literals

import xml.etree.ElementTree as ET

import requests

from .compat import maybe_decode
from .utils import Record
from .referent import (
    Slot,
    Referent
)
from .result import (
    Span,
    Match,
    Result
)


def parse_xml(data):
    return ET.fromstring(data)


def parse_response(text, xml):
    id_refents = {}
    for item in xml:
        if item.tag == 'referent':
            id = item.get('id')
            label = item.get('type')
            id_refents[id] = Referent(label, slots=[])
    id_matches = {}
    matches = []
    for item in xml:
        tag = item.tag
        if tag == 'slot':
            parent = item.get('parent')
            key = item.get('key')
            referent = item.get('referent')
            if referent:
                value = id_refents[referent]
            else:
                value = item.get('value')
            slot = Slot(key, value)
            id_refents[parent].slots.append(slot)
        elif tag == 'match':
            id = item.get('id')
            referent = item.get('referent')
            referent = id_refents[referent]
            start = int(item.get('start'))
            stop = int(item.get('stop'))
            span = Span(start, stop)
            match = Match(referent, span, children=[])
            id_matches[id] = match
            parent = item.get('parent')
            if parent:
                id_matches[parent].children.append(match)
            else:
                matches.append(match)
    matches = sorted(
        matches,
        key=lambda _: _.span.start
    )
    return Result(text, matches)


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
