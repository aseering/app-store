from collections import Iterable

def Enum(**enums):
    class enum(object):
        __iter__ = enums.iteritems
    Enum = enum()
    for key, val in enums.iteritems():
        setattr(Enum, key, val)
    return Enum
