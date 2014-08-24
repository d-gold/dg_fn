"""

This is a fork of multimethod by Aric Coady

You can find the original source at:
    https://bitbucket.org/coady/multimethod/wiki/Home

My plan it to send this version back to him. Right now I have the code in a
bit of a mess. It needs some love.

His orignal license follows:
    Copyright 2008-2013 Aric Coady

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.


**Multiple argument dispatching**

Call *multimethod* on a variable number of types.
It returns a decorator which finds the multimethod of the same name, creating it if necessary, and adds that function to it.
For example::

    @multimethod(*types)
    def func(*args):
        pass

|

*func* is now a multimethod which will delegate to the above function, when called with arguments of the specified types.
If an exact match can't be found, the next closest method is called (and cached).
If *strict* is enabled, and there are multiple candidate methods, a TypeError is raised.
A function can have more than one multimethod decorator.

See tests for more example usage.
Supported on Python 2.6 or higher, including Python 3.

Changes in 0.4:
 * Dispatch on python 3 annotations


TODO:
    ___ support outside of lists
    @pattern('add', ___) # Any number of any type arguments
    @pattern('sub', ___)

"""

import sys
try:
    from future_builtins import map, zip
except ImportError:
    pass
from typecheck import is_seq

__version__ = '0.1'



class _(object):

    """Docstring for generic. """

    def __init__(self):
        """@todo: to be defined1. """
        pass

    # TODO handle _ = xxx type stuff
    #

class ___(object):

    """Docstring for ___. """

    def __init__(self):
        """@todo: to be defined1. """
        pass


class list_hash(object):

    """Docstring for list_hash. """

    def __init__(self, sequence):
        """@todo: Docstring for __init__.

        :sequence: @todo
        :returns: @todo

        """
        self.sequence = sequence

    def match(self, arg):
        """@todo: Docstring for match.

        :arg: @todo
        :returns: @todo

        """

        if not is_seq(arg):
            # If the argument is not a list, but we are comparing against a
            # list, then exit out as a mismatch.
            return False

        arg_pos = 0
        for x in range(0, len(self.sequence)):
            value = self.sequence[x]

            if x>= len(arg):
                # There are more values in the sequence to search for than in
                # The supplied arg
                return False

            if (hasattr(value, '__name__') and value.__name__ == '_'):
                # Ignore _ values. They can be anything
                pass
            elif (hasattr(value, '__name__') and value.__name__ == '___'):
                # ___ means that we don't care what the rest of the list is.
                # TODO, if there are entries past this, match the end of the
                # list too.
                if x == len(self.sequence) - 1:
                    return True

                new_arg_pos = len(arg) - (len(self.sequence) - x)
                if new_arg_pos > arg_pos:
                    arg_pos = new_arg_pos
                else:
                    return False

            elif type(value) == type and type(arg[arg_pos]) == value:
                pass
            elif type(value) != type and value == arg[arg_pos]:
                pass
            else:
                return False

            arg_pos += 1

        if arg_pos < len(arg):
            return False

        return True


class dict_hash(object):

    """Docstring for dict_hash. """

    def __init__(self):
        """@todo: to be defined1. """
        pass


class DispatchError(TypeError):

    """Error for when no function can be found that matches the pattern."""

    pass


class signature(tuple):
    "A tuple of types that supports partial ordering."

    def is_subclass(self, a, b):
        """@todo: Docstring for get_type_value.

        :value: @todo
        :returns: @todo

        """

        if (hasattr(a, '__name__') and a.__name__ == '_') or \
                (hasattr(b, '__name__') and b.__name__ == '_'):
            return True
        try:
            return issubclass(a, b)
        except TypeError:
            try:
                return issubclass(a, type(b))
            except TypeError:
                try:
                    return issubclass(type(a), b)
                except TypeError:
                    return issubclass(type(a), type(b))

    def __le__(self, other):
        return len(self) <= len(other) and \
            all(map(self.is_subclass, other, self))

    def __lt__(self, other):
        return self != other and self <= other

    def __sub__(self, other):
        """Return relative distances, assuming self >= other."""

        return [left.__mro__.index(right if right in left.__mro__ else object)
                for left, right in zip(self, other)]


class pattern(dict):

    """A callable directed acyclic graph of methods."""

    @classmethod
    def new(cls, name='', strict=False):
        """@todo: Docstring for new.

        :cls: @todo
        :name: @todo
        :strict: @todo

        :returns: None

        Explicitly create a new pattern.  Assign to local name in order
        to use decorator.
        """

        self = dict.__new__(cls)
        self.order = []   # Store the methods in the order that they are found.
        self.__name__, self.strict = name, strict
        return self

    def __init__(self, *types):
        dict.__init__(self)
        self.order = []   # Store the methods in the order that they are found.
        self.__name__ = None
        self.strict = False

    def __new__(cls, *types):
        "Return a decorator which will add the function."

        def fix_types(types):
            """@todo: Docstring for fix_types.

            :types: @todo
            :returns: @todo

            """
            results = []

            for x in types:
                if is_seq(x):
                    x = list_hash(x)
                results.append(x)
            return tuple(results)

        types = fix_types(types)

        namespace = sys._getframe(1).f_locals

        def decorator(func):
            if isinstance(func, cls):
                self, func = func, func.last
            else:
                self = namespace.get(func.__name__, cls.new(func.__name__))
            self.order.append(types)
            self[types] = self.last = func
            return self

        if len(types) == 1 and hasattr(types[0], '__annotations__'):
            func, = types
            types = tuple(map(func.__annotations__.__getitem__,
                              func.__code__.co_varnames[:len(func.__annotations__)]))
            decorator.__name__ = func.__name__
            decorator.__doc__ = func.__doc__
            decorator.__dict__.update(func.__dict__)
            return decorator(func)

        return decorator


    def prepare_key(self, key):
        """@todo: Docstring for prepare_key.

        :key: @todo
        :returns: @todo

        """
        if type(key) == type:
            return(key, None)
        else:
            return(type(key), key)

    def parents(self, types):
        "Find immediate parents of potential key."
        parents, ancestors = set(), set()
        for key in self:
            if isinstance(key, signature) and key < types:
                parents.add(key)
                ancestors |= key.parents
        return parents - ancestors

    def clean(self):
        "Empty the cache."
        for key in list(self):
            if not isinstance(key, signature):
                dict.__delitem__(self, key)

    def __setitem__(self, types, func):

        self.clean()
        types = signature(types)
        parents = types.parents = self.parents(types)
        for key in self:
            if types < key and (not parents or parents & key.parents):
                key.parents -= parents
                key.parents.add(types)
        dict.__setitem__(self, types, func)

    def __delitem__(self, types):
        self.clean()
        dict.__delitem__(self, types)
        for key in self:
            if types in key.parents:
                key.parents = self.parents(key)

    def __missing__(self, types):
        "Find and cache the next applicable method of given types."
        keys = self.parents(types)
        if keys and (len(keys) == 1 or not self.strict):
            return self.setdefault(types,
                                   self[min(keys, key=signature(types).__sub__)])
        raise DispatchError("{0}{1}: {2} methods found".format(self.__name__,
                                                               types,
                                                               len(keys)))

    def match_signature(self, args, check_against):
        """@todo: Docstring for match_signature.

        :args: @todo
        :check_against: @todo
        :returns: @todo

        """
        if len(args) != len(check_against):
            return False

        for (x, y) in zip(args, check_against):
            if hasattr(y, '__name__') and y.__name__ == '_':
                pass
            elif isinstance(y, list_hash):
                if not y.match(x):
                    return False
            elif type(y) == type and type(x) == y:
                pass
            elif type(y) != type and x == y:
                pass
            elif callable(y):
                try:
                    if not y(x):
                        return False
                except:
                    # Exceptions are ignored. The function MUST return True
                    # to be a candidate. An exception probably means that the
                    # check function doesn't handle all possible inputs and
                    # that the check does not apply.
                    pass
            else:
                return False
        return True

    def __call__(self, *args, **kwargs):
        """Resolve and dispatch to best method. """

        for cached_signature in self.order:
            match = self.match_signature(args, cached_signature)
            if match:
                return self[cached_signature](*args, **kwargs)
        raise DispatchError('No signature found for {}{}'.format( \
                self.__name__, repr(args)))
