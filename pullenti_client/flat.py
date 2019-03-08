
from collections import OrderedDict

from .utils import Record


REFERENT = 'referent'
SLOT = 'slot'
MATCH = 'match'
LABEL = 'label'
TEXT = 'text'
PARTS = 'parts'


class FlatRecord(Record):
    __annotations__ = {}

    @property
    def as_json(self):
        data = OrderedDict([
            (LABEL, self.label)
        ])
        for key in self.__attributes__:
            value = getattr(self, key)
            if value is not None:
                data[key] = value
        return data

    @classmethod
    def from_json(cls, data):
        args = []
        for key in cls.__attributes__:
            value = data.get(key)
            args.append(value)
        return cls(*args)

    @classmethod
    def from_xml(cls, xml):
        args = []
        for key in cls.__attributes__:
            value = xml.get(key)
            annotation = cls.__annotations__.get(key)
            if value is not None and annotation:
                value = annotation(value)
            args.append(value)
        return cls(*args)


class FlatPart(FlatRecord):
    label = None


class FlatReferent(FlatPart):
    __attributes__ = ['id', 'type']

    label = REFERENT

    def __init__(self, id, type):
        self.id = id
        self.type = type


class FlatSlot(FlatPart):
    __attributes__ = ['parent', 'key', 'value', 'referent']

    label = SLOT

    def __init__(self, parent, key, value, referent):
        self.parent = parent
        self.key = key
        self.value = value
        self.referent = referent


class FlatMatch(FlatPart):
    __attributes__ = ['id', 'parent', 'start', 'stop', 'referent']
    __annotations__ = {
        'start': int,
        'stop': int
    }

    label = MATCH

    def __init__(self, id, parent, start, stop, referent):
        self.id = id
        self.parent = parent
        self.start = start
        self.stop = stop
        self.referent = referent


TYPES = {
    SLOT: FlatSlot,
    REFERENT: FlatReferent,
    MATCH: FlatMatch
}


class FlatResult(FlatRecord):
    __attributes__ = ['text', 'parts']

    def __init__(self, text, parts):
        self.text = text
        self.parts = parts

    @property
    def as_json(self):
        return OrderedDict([
            (TEXT, self.text),
            (PARTS, [_.as_json for _ in self.parts])
        ])

    @classmethod
    def from_json(cls, data):
        text = data[TEXT]
        parts = []
        for item in data[PARTS]:
            Part = TYPES[item[LABEL]]
            part = Part.from_json(item)
            parts.append(part)
        return cls(text, parts)

    @classmethod
    def from_xml(cls, text, xml):
        parts = []
        for item in xml:
            Part = TYPES[item.tag]
            part = Part.from_xml(item)
            parts.append(part)
        return cls(text, parts)
