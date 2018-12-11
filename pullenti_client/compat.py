# coding: utf-8
from __future__ import unicode_literals

try:
    # Python 2
    str = unicode

    def maybe_decode(string):
        if isinstance(string, unicode):  # noqa
            return string
        return string.decode('utf8')

except NameError:
    # Python 3
    str = str

    def maybe_decode(string):
        return string
