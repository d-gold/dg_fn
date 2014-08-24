# pylint: disable=E731
#
# pylint disables:
#     E731: I intentionally assign one line expressions to lambdas

"""
Misc. functions that operate on functions.

A lot of these come from clojure.
"""


identity = lambda x: x
invert = lambda x: not x


def fnone(fn, *default_args, **default_kwargs):
    """@todo: Docstring for fnone.

    :fn: @todo
    :*args: @todo
    :**kwargs: @todo
    :returns: @todo


    >>> def favs(age, food):
    ...     print "I am {} years old and my favourite food is {}".format(
    ...         age, food)
    ...     return age, food

    >>> favs_with_defaults = fnone(favs, 28, 'waffles')
    >>> favs_with_defaults(64, 'cranberries')
    I am 64 years old and my favourite food is cranberries
    >>> favs_with_defaults(None, 'pizza')
    I am 28 years old and my favourite food is pizza
    >>> favs_with_defaults(16, None)
    I am 16 years old and my favourite food is waffles
    >>> favs_with_defaults(None, None)
    I am 28 years old and my favourite food is waffles
    >>> favs_with_defaults(23, False)
    I am 23 years old and my favourite food is False

    TODO: Support default_kwargs

    """

    def inner(*args, **kwargs):
        """@todo: Docstring for inner.

        :*args: @todo
        :**kwargs: @todo
        :returns: @todo

        """
        args_zip = tuple(izip_longest(args, default_args))
        new_args = map(lambda (x, y): (x is None and y) or x, args_zip)
        return fn(*new_args, **kwargs)

    return inner


def juxt(fn_list):
    """Create a function that runs a list of functions on the same arguments.

    :fn_list: List of functions

    :returns: A function

    The returned function will return a lazy tuple that will not execute the
    functions until it has to.  This makes it useful for drop_while,take_while
    types of things.

    """

    def inner(*args, **kwargs):
        """@todo: Docstring for inner.

        :*args: @todo
        :**kwargs: @todo
        :returns: @todo

        """
        results = (f(*args, **kwargs) for f in fn_list)
        return results

    return inner


def cross_juxt(fn_list):
    """@todo: Docstring for cross_juxt.

    :fn_list: @todo
    :returns: @todo

    """

    def inner(arg_list):
        """@todo: Docstring for inner.

        :*args: @todo
        :**kwargs: @todo
        :returns: @todo

        """

        apply_all_args_to_fn = lambda f: (f(*x) for x in arg_list)

        results = (apply_all_args_to_fn(f) for f in fn_list)
        return results

    return inner


def cross_juxt2(fn_list):
    """@todo: Docstring for cross_juxt.

    :fn_list: @todo
    :returns: @todo

    """

    def inner(arg_list):
        """@todo: Docstring for inner.

        :*args: @todo
        :**kwargs: @todo
        :returns: @todo

        """

        apply_all_fn_to_args = lambda x: (f(*x) for f in fn_list)

        results = (apply_all_fn_to_args(x) for x in arg_list)
        return results

    return inner


def monoid(op, ctor):
    """@todo: Docstring for monoid.

    :op: @todo
    :ctor: @todo
    :returns: @todo

    """

    def inner(*args):
        """@todo: Docstring for inner.

        :*args: @todo
        :returns: @todo

        """
        result = (not args and callable(ctor) and ctor()) or \
            (not args and ctor) or \
            (args and len(args) == 2 and op(args[0], args[1])) or \
            None
        return result

    return inner


def flip(fn, auto_curry=True, arg_count=None):
    """@todo: Docstring for freverse.

    :fn: @todo

    :returns: @todo

    Note: This has built-in currying.

    Note: The arg_count option is required when trying to reverse parameters
          for non-python functions (i.e. math.sin, datetime.strftime, and
          the like). These functions don't have away to count the number of
          arguments.

          This would not be an issue, except this support currying. For the
          curry to work, I need to know the number of parameters.

          If you don't want to mess with figuring out how many args you want
          the reversed function to take and are not interested in the automatic
          currying, just set auto_curry to False. This will just simply reverse
          the args.

    """

    def reversed_fn(arg_values, num_args):
        if num_args == 0:
            return fn(*reversed(arg_values))
        else:
            return lambda *x: reversed_fn(arg_values + list(x),
                                          num_args - len(x))

    def simple_reverse(*args, **kwargs):
        return fn(*reversed(args), **kwargs)

    return (auto_curry and
            reversed_fn([], arg_count or
                        len(inspect.getargspec(fn).args))) or \
        (not auto_curry and simple_reverse) or \
        None


def compose(*fn_list, **kwargs):
    """@todo: Docstring for compose.

    :*fn_list: @todo
    :**kwargs: @todo
    :returns: @todo

    """
    def compose2(f, g, expand_args=False):
        """@todo: Docstring for compose2.

        :f: @todo
        :g: @todo
        :expand_args: @todo
        :returns: @todo

        """
        def c1(*args, **kwargs):
            return f(*g(*args, **kwargs))

        def c2(*args, **kwargs):
            """@todo: Docstring for c2.

            :*args: @todo
            :**kwargs: @todo
            :returns: @todo

            """
            return f(g(*args, **kwargs))

        return (expand_args and c1) or (not expand_args and c2)

    return functools.reduce(lambda f, g:
                            compose2(f, g, **kwargs),
                            fn_list)
