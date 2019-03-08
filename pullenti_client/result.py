# coding: utf-8
from __future__ import unicode_literals

from .compat import string_type
from .utils import (
    Record,
    assert_type,
    Ids
)
from .referent import (
    Slot,
    Referent,
    is_referent
)
from .graph import Graph
from .flat import (
    REFERENT,
    SLOT,
    MATCH,

    FlatReferent,
    FlatSlot,
    FlatMatch,
    FlatResult
)


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


MISSING = Referent('MISSING')


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

    @property
    def as_flat(self):
        id = Ids().assign
        id_parents = {}
        for match in self.walk():
            for child in match.children:
                id_parents[id(child)] = match

        parts = []
        visited = set()
        for match in self.walk():
            parent = id_parents.get(id(match))
            start, stop = match.span
            parts.append(FlatMatch(
                id=id(match),
                parent=id(parent),
                start=start,
                stop=stop,
                referent=id(match.referent)
            ))
            for referent in match.referent.walk():
                if id(referent) in visited:
                    continue
                visited.add(id(referent))
                parts.append(FlatReferent(
                    id=id(referent),
                    type=referent.label
                ))
                for slot in referent.slots:
                    value = slot.value
                    referent_ = None
                    if is_referent(value):
                        referent_ = id(value)
                        value = None
                    parts.append(FlatSlot(
                        parent=id(referent),
                        key=slot.key,
                        value=value,
                        referent=referent_
                    ))
        return FlatResult(self.text, parts)

    @classmethod
    def from_flat(cls, result):
        id_refents = {}
        for part in result.parts:
            if part.label == REFERENT:
                id, label = part
                id_refents[id] = Referent(label, slots=[])

        id_matches = {}
        matches = []
        for part in result.parts:
            if part.label == SLOT:
                parent, key, value, referent = part
                if referent:
                    if referent not in id_refents:
                        # should not happen but
                        # https://github.com/pullenti/PullentiServer/issues/1
                        value = MISSING
                    else:
                        value = id_refents[referent]
                slot = Slot(key, value)
                id_refents[parent].slots.append(slot)
            elif part.label == MATCH:
                id, parent, start, stop, referent = part
                if referent not in id_refents:
                    # also should not happen
                    referent = MISSING
                else:
                    referent = id_refents[referent]
                span = Span(start, stop)
                match = Match(referent, span, children=[])
                id_matches[id] = match
                if parent is not None:
                    id_matches[parent].children.append(match)
                else:
                    matches.append(match)

        matches = sorted(
            matches,
            key=lambda _: _.span.start
        )
        return Result(result.text, matches)

    @property
    def as_json(self):
        return self.as_flat.as_json

    @classmethod
    def from_json(cls, data):
        result = FlatResult.from_json(data)
        return cls.from_flat(result)
