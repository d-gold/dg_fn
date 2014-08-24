import inspect

# pylint: disable=C0103, W0142


def curry(fn, arg_count=None):
    """@todo: Docstring for supercurry2.

    :fn: @todo
    :returns: @todo

    Note: arg_count is to support built in functions that we cannot inspect.

    """
    # fname = fn.__code__.co_name
    # num_args = fn.__code__.co_argcount

    def curried_function(arg_values, num_args):
        if num_args == 0:
            return fn(*arg_values)
        else:
            return lambda *x: curried_function(arg_values + list(x),
                                               num_args - len(x))

    return curried_function([], arg_count or len(inspect.getargspec(fn).args))

#F = curry


def curry_right(fn, arg_count=None):
    """@todo: Docstring for curry_right.

    :fn: @todo
    :*args: @todo
    :**kwargs: @todo
    :returns: @todo

    Note: This reverses all the parameters. Thus:
            g = curry_right(f)

            g(z)(y)(x) => f(x, y, z)
            g(z)(y, x) => f(x, y, z)
            g(z, y)(x) => f(x, y, z)
            g(z, y, x) => f(x, y, z)

    """
    def curried_function(arg_values, num_args):
        if num_args == 0:
            return fn(*reversed(arg_values))
        else:
            return lambda *x: curried_function(arg_values + list(x),
                                               num_args - len(x))

    return curried_function([], arg_count or len(inspect.getargspec(fn).args))

#FR = curry_right


def curry_right2(fn, arg_count=None):
    """@todo: Docstring for curry_right.

    :fn: @todo
    :*args: @todo
    :**kwargs: @todo
    :returns: @todo


    Note: This does not reverse params in a call:
        g = curry_right2(f)

        g(z)(y)(x) => f(x, y, z)
        g(y, z)(x) => f(x, y, z)
        g(z)(x, y) => f(x, y, z)
        g(x, y, z) => f(x, y, z)

    """

    def curried_function(arg_values, num_args):
        if num_args == 0:
            return fn(*arg_values)
        else:
            return lambda *x: curried_function(list(x) + arg_values,
                                               num_args - len(x))

    return curried_function([], arg_count or len(inspect.getargspec(fn).args))

#FR2 = curry_right2

