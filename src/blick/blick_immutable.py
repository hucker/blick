"""
Helper classes to support making environment variables with mutable values be less prone
to being changed by mistake.  We are under no presumption that we can stop people from
using a dynamic language.  These classes make the best effort to  prevent the user from
making edits to environment data that should be constant for the life of a rule
checking run.

THERE IS NO ASSURANCE THAT THIS WILL WORK IN ALL CASES. DON'T WRITE TO THE ENV VARIABLES!

"""

from .blick_exception import BlickException


class BlickEnvList(list):
    """
    Class representing a mutation-inhibited list. Mutational operations raise
    blick_exception.BlickException.

    Python being dynamic means forceful mutations can succeed. This class serves
    to prevent accidental changes by raising exceptions for mutating methods.

    Ideally, a copy is best to avoid mutation. But for large data sets, it's
    resource-demanding. ImmutableList protects large sets from unintended changes.
    """

    def __init__(self, *args):
        # super(BlickEnvList, self).__init__(*args)
        super().__init__(*args)

    def __setitem__(self, index, value):
        raise BlickException("Environment list does not support item assignment")

    def __delitem__(self, index):
        raise BlickException("Environment list doesn't support item deletion")

    def append(self, value):
        raise BlickException("Environment list is immutable, append is not supported")

    def extend(self, value):
        raise BlickException("Environment list is immutable, extend is not supported")

    def insert(self, index, value):
        raise BlickException("Environment list is immutable, insert is not supported")

    def remove(self, value):
        raise BlickException("Environment list is immutable, remove is not supported")

    def pop(self, index=-1):
        raise BlickException("Environment list is immutable, pop is not supported")

    def clear(self):
        raise BlickException("Environment list is immutable, clear is not supported")

    def sort(self, *args, **kwargs):
        raise BlickException("Environment list is immutable, sort is not supported")

    def reverse(self):
        raise BlickException("Environment list is immutable, reverse is not supported")


class BlickEnvDict(dict):
    """
    A class symbolizing a mutation-prohibited dictionary. Mutational operations raise
    a BlickException.

    Analogous to ImmutableList, Python's dynamic nature may allow forced mutations. This
    class prevents unintentional modifications to a dict object.
    """

    def __init__(self, *args, **kwargs):
        # super(BlickEnvDict, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        raise BlickException("Environment dict does not support item assignment")

    def __delitem__(self, key):
        raise BlickException("Environment dict doesn't support item deletion")

    def pop(self, k, d=None):
        raise BlickException("Environment dict is immutable, pop is not supported")

    def popitem(self):
        raise BlickException("Environment dict is immutable, popitem is not supported")

    def clear(self):
        raise BlickException("Environment dict is immutable, clear is not supported")

    def update(self, other=(), **kwargs):
        raise BlickException("Environment dict is immutable, update is not supported")

    def setdefault(self, key, default=None):
        raise BlickException("Environment dict is immutable, setdefault is not supported")




class BlickEnvSet(frozenset):
    """ Support immutable sets using frozenset """
