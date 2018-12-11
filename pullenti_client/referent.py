# coding: utf-8
from __future__ import unicode_literals

from .compat import string_type
from .utils import (
    assert_type,
    Record
)
from .graph import (
    Graph,
    style,
    BLUE,
    SILVER
)


class Slot(Record):
    __attributes__ = ['key', 'value']

    def __init__(self, key, value):
        assert_type(key, string_type)
        self.key = key
        assert_type(value, (string_type, Referent))
        self.value = value


class Referent(Record):
    __attributes__ = ['label', 'slots']

    def __init__(self, label, slots=()):
        self.label = label
        for slot in slots:
            assert_type(slot, Slot)
        self.slots = slots

    def walk(self):
        yield self
        for slot in self.slots:
            if isinstance(slot.value, Referent):
                for item in slot.value.walk():
                    yield item

    @property
    def graph(self):
        graph = Graph()
        for source in self.walk():
            for key, target in source.slots:
                graph.add_edge(
                    source,
                    target,
                    style(label=key)
                )
                graph.add_node(
                    source,
                    style(
                        label=source.label,
                        fillcolor=BLUE
                    )
                )
                if isinstance(target, Referent):
                    color = BLUE
                    label = target.label
                else:
                    color = SILVER
                    label = target
                graph.add_node(
                    target,
                    style(
                        label=label,
                        fillcolor=color
                    )
                )
        return graph
