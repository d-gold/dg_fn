# pylint: disable=W0110, W0622, W0141, W0142


from lists import is_seq, first


def do(fn, arg, expand_args=False):
    """Execute a function explictly for its side effects.

    :fn: Function providing side effects to call.
    :arg: Parameter to fn. Multiple parameters are supported when expand_args
          is True.
    :expand_args: Indicate that the fn takes multiple parameters and the arg
                  value should be expanded. This only applies when arg is a
                  list.
    :returns: arg

    do() makes an easy way to insert functions that we are not interested in
    the return value of into a chain of function calls. It has support for
    calling multiple functions with multiple arguments. Keyword arguments
    are not supported.

    Example:

    We will first create a couple of functions that do nothing but write to
    the console as side effects.

        Create a function that writes to the console as a side effect.
        We do not care about the return value of this function.
        >>> def x1(a):
        ...    print len(a)
        ...

        Create a function that provides data that we will process
        >>> def y1(a):
        ...    return map(lambda x: x * a, range(1, a + 1))
        ...

        Use do to handle the side effects and return the results of y1().
        >>> do(x1, y1(3))
        3
        [3, 6, 9]

        Or you can put the argument in directly.
        >>> do(x1, (1, 2, 3, 4, 5))
        5
        (1, 2, 3, 4, 5)

    A list of functions can be passed into do(). Example:

        >>> def x2(l):
        ...     print sum(l)
        ...
        >>> def x3(l):
        ...    print reduce(lambda x, y: x * y, l)
        ...
        >>> do((x1, x2, x3), y1(4))
        4
        40
        6144
        [4, 8, 12, 16]

        The results can be passed into other functions as if the do() call
        wasn't there.

        >>> sum(do(x1, y1(3)))
        3
        18

        >>> sum(do((x1, x2, x3), y1(4)))
        4
        40
        6144
        40

    By using the expand_args flag, do() is capable of handling functions that
    take multiple arguments. Here is an example:

        Create a couple of functions that have side effects
        >>> def foo(a, b, c):
        ...    print a + b + c
        ...
        >>> def bar(a, b, c):
        ...    print a * b * c
        ...

        And a function that generates values that can be used by the first two
        >>> def baz(x):
        ...    return x, x * 2, x * 3
        ...

        Now pipe the functions through do()
        >>> fn = (foo, bar)
        >>> do(fn, baz(1), expand_args=True)
        6
        6
        (1, 2, 3)

        >>> do(fn, baz(2))
        12
        48
        (2, 4, 6)

        The do() function can be called by passing all the args as a list.
        >>> do(fn, (1, 4, 5), expand_args=True)
        10
        20
        (1, 4, 5)

        The results of do() in the expand_args case is the arguments as a
        list. These can be then passed into other functions.
        >>> sum(do(fn, baz(2), expand_args=True))
        12
        48
        12

    """

    def multi_fn(fn_list, arg):
        """Call a list of functons

        :fn_list: List of functions
        :*args:   Arguments to those functions. Each function will get the
                  same arguments.

        :returns: Always returns True.

        """
        _ = map(lambda f: f(*arg), fn_list)
        return True

    prepped_args = (expand_args and is_seq(arg) and arg) or \
        (arg and [arg]) or \
        None

    _ = (is_seq(fn) and multi_fn(fn, prepped_args)) or \
        (prepped_args and fn(*prepped_args)) or \
        fn(None)

    return (expand_args and prepped_args) or first(prepped_args)
