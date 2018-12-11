# coding: utf-8
from __future__ import unicode_literals

from .compat import string_type
from .utils import (
    Record,
    assert_type
)
from .referent import Referent
from .graph import Graph


class Span(Record):
    __attributes__ = ['start', 'stop']

    def __init__(self, start, stop):
        assert_type(start, int)
        self.start = start
        assert_type(stop, int)
        self.stop = stop


class Match(Record):
    __attributes__ = ['referent', 'span', 'children']

    def __init__(self, referent, span, children=()):
        assert_type(referent, Referent)
        self.referent = referent
        assert_type(span, Span)
        self.span = span
        for child in children:
            assert_type(child, Match)
        self.children = children

    def walk(self):
        yield self
        for child in self.children:
            for item in child.walk():
                yield item


class Result(Record):
    __attributes__ = ['text', 'matches']

    def __init__(self, text, matches):
        assert_type(text, string_type)
        self.text = text
        for match in matches:
            assert_type(match, Match)
        self.matches = matches

    def walk(self):
        for match in self.matches:
            for item in match.walk():
                yield item

    @property
    def graph(self):
        graph = Graph()
        for match in self.walk():
            graph.update(match.referent.graph)
        return graph
