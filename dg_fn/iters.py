# pylint: disable=W0404


import sys
import re
from types import GeneratorType
from itertools import dropwhile, islice
from functools import partial
from pattern import pattern, _, ___
from typecheck import is_seq, is_gen
from exc import NotCadrExpressionError
from itertools import product


def car(x):
    """@todo: Docstring for first.

    :x: @todo
    :returns: @todo

    """
    try:
        return islice(x, 0, 1).next()
    except StopIteration:
        return empty(x)


def cdr(x):
    """@todo: Docstring for cdr .

    :x: @todo
    :returns: @todo

    """
    return into(x, drop(1, x))


@pattern(_, is_gen)
def cons(value, x):
    """@todo: Docstring for cons.

    :value: @todo
    :x: @todo
    :returns: @todo

    """
    return (x for x in tuple((value,)) + tuple(x))


@pattern(_, _)
def cons(value, x):
    """@todo: Docstring for cons.

    :value: @todo
    :x: @todo
    :returns: @todo

    """
    return type(x)(tuple((value,)) + tuple(x))


def drop(num, seq):
    """@todo: Docstring for drop.

    :num: @todo
    :seq: @todo
    :returns: @todo

    """
    return islice(seq, num, None)


@pattern(is_gen)
@pattern(is_gen, ___)
def empty(coll, *args, **kwargs):
    """@todo: Docstring for empty.

    :coll: @todo
    :*args: @todo
    :**kwargs: @todo
    :returns: @todo

    """
    return (x for x in ())


@pattern(is_seq)
@pattern(is_seq, ___)
@pattern(dict)
@pattern(dict, ___)
def empty(coll, *args, **kwargs):
    """@todo: Docstring for empty.

    :coll: @todo
    :*args: @todo
    :**kwargs: @todo
    :returns: @todo

    """
    return type(coll)(*args, **kwargs)


@pattern(_)
@pattern(_, ___)
def empty(obj, *args, **kwargs):
    """@todo: Docstring for empty .

    :obj: @todo
    :*args: @todo
    :**kwargs: @todo
    :returns: @todo

    """
    return type(obj)(*args, **kwargs)


def first(x):
    """@todo: Docstring for first.

    :x: @todo
    :returns: @todo

    """
    try:
        return islice(x, 0, 1).next()
    except StopIteration:
        return None


def first_where(fn, seq):
    """@todo: Docstring for first_when.

    :fn: @todo
    :seq: @todo
    :returns: @todo

    """
    return first(dropwhile(lambda x: not fn(x), seq))


# @pattern(is_seq)
def flatten(seq):
    """Deep flatten.

    :seq: @todo
    :returns: @todo

    """
    for x in seq:
        if is_seq(x):
            for y in flatten(x):
                yield y
        else:
            yield x

# @pattern(is_seq, ___)
# Add *args support to flatten

def flatten1(seq):
    """Shallow flatten.

    :seq: @todo
    :returns: @todo

    """
    for x in seq:
        if is_seq(x):
            for y in x:
                yield y
        else:
            yield x


def icons(value, x):
    """Iterable version of cons().

    :value: @todo
    :x: @todo

    :returns: @todo

    """

    yield value
    for i in x:
        yield i


@pattern(is_gen, _)
def into(_, src):
    """@todo: Docstring for into.

    :dest: @todo
    :src: @todo
    :returns: @todo

    """
    return (x for x in src)


@pattern(_, _)
def into(dest, src):
    """@todo: Docstring for into.

    :dest: @todo
    :src: @todo
    :returns: @todo

    """
    # reduce(cons, src)
    return type(dest)(src)


@pattern(is_gen, _)
def into2(dest, src):
    """@todo: Docstring for into2.

    :dest: @todo
    :src: @todo
    :returns: @todo

    """
    x = (x for x in (tuple(dest) + tuple(src)))
    return x


@pattern(_, _)
def into2(dest, src):
    """@todo: Docstring for into2.

    :dest: @todo
    :src: @todo
    :returns: @todo

    """
    x = type(dest)(tuple(dest) + tuple(src))
    return x


def keep(fn, coll):
    """@todo: Docstring for keep.

    :fn: @todo
    :coll: @todo
    :returns: @todo

    fn must not have side-effects.

    """
    return (x for x in coll if fn(x) is not None)


def tail(x):
    """@todo: Docstring for tail.

    :x: @todo
    :returns: @todo

    """
    return into(x, drop(1, x))


def make_cadr_fn(name):
    """@todo: Docstring for make_cadr_fn.

    :name: @todo
    :returns: @todo

    """

    if not re.match('^c[ad]{2,}r$', name):
        raise NotCadrExpressionError(name)

    def choose_cadr(ad):
        return (ad == 'a' and car) or cdr

    def execute_cadr(seq):
        fn_list = map(choose_cadr, name[1:-1])
        value = type(seq)(seq)
        for x in reversed(fn_list):
            value = x(value)
        return value

    execute_cadr.__name__ = name
    return execute_cadr


def _add_module_function(name, fn):
    """@todo: Docstring for __add_module_function.

    :name: @todo
    :fn: @todo
    :returns: @todo

    """
    sys.modules[__name__].__dict__[name] = fn
    return fn


if __name__ != '__main__':
    # Create a lot of cad...r type functions.
    ad_sets = map(lambda x: x * ('ad',), range(2, 9))
    combos = tuple(flatten1(map(lambda x: tuple(product(*x)), ad_sets)))
    names = map(lambda x: 'c' + ''.join(x) + 'r', combos)
    __ = map(lambda x: _add_module_function(x, make_cadr_fn(x)), names)
