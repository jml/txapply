"""
Helpers for adding callbacks and errbacks.
"""


def nop(*args, **kwargs):
    """
    Do nothing.
    """


def transparent(value, function, *args, **kwargs):
    """Invoke ``function`` with ``value`` and other arguments, return ``value``.

    Use this to add a function to a callback chain without disrupting the
    value of the callback chain::

        d = defer.succeed(42)
        d.addCallback(transparent, print)
        d.addCallback(lambda x: x == 42)
    """
    function(value, *args, **kwargs)
    return value
