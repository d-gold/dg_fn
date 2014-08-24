import collections
import config
from types import GeneratorType
from types import FunctionType


def is_function(obj):
    """@todo: Docstring for is_function.

    :obj: @todo
    :returns: @todo

    """
    return isinstance(obj, FunctionType)


def is_gen(obj):
    """@todo: Docstring for is_gen.

    :obj: @todo
    :returns: @todo

    """
    return isinstance(obj, GeneratorType)


def is_seq(obj):
    """@todo: Docstring for is_seq.

    :seq: @todo

    :returns: @todo

    Tests to see if obj is a tuple, list or other sequence type object.
    This will exclude strings and dictionaries.

    """

    results = isinstance(obj, config.Sequence) or \
        (isinstance(obj, collections.Sequence) and
         not isinstance(obj, basestring))

    return results
