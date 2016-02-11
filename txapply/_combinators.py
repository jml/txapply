"""
Helpers for adding callbacks and errbacks.
"""


def nop(*args, **kwargs):
    """
    Do nothing.
    """


def transparent(value, function, *args, **kwargs):
    """
    Invoke ``function`` with ``value`` and other arguments, return ``value``.

    Use this to add a function to a callback chain without disrupting the
    value of the callback chain::

        d = defer.succeed(42)
        d.addCallback(transparent, print)
        d.addCallback(lambda x: x == 42)
    """
    function(value, *args, **kwargs)
    return value


def ignore(value, function, *args, **kwargs):
    """
    Invoke ``function`` with ``*args`` and ``*kwargs``.

    Use this to add a function to a callback chain that just ignores the
    previous value in the chain::

       >>> d = defer.succeed(42)
       >>> d.addCallback(ignore, print, 37)
       37
    """
    return function(*args, **kwargs)


def combine(value, function, *args, **kwargs):
    """
    Call ``function``, return its result and ``value`` as a tuple.

    ``function`` is invoked with ``value``, ``*args`` and ``**kwargs`` and
    then we return a 2-tuple of whatever ``function`` returned and ``value``.

    Use this to add a function to a callback chain that combines its return
    value with the previous value::

        >>> d = defer.succeed(42)
        >>> d.addCallback(combine, lambda: 47)
        >>> d.addCallback(print)
        (37, 42)
    """
    y = function(value, *args, **kwargs)
    return (y, value)
