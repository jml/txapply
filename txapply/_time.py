from twisted.internet import task

# XXX: Untested


def deferLater(clock, delay, function, *args, **kwargs):
    """
    Return a Deferred that will call ``function`` after ``delay``.

    This is a wrapper around :py:func:`task.deferLater`, it behaves the same
    way, except that its delay is a timedelta, not a float of secods.

    :param IReactorTime clock: Event loop that controls time.
    :param timedelta delay: How long to wait
    :param function: The function to call
    :return: A ``Deferred`` that fires with the return value of ``function``.
    """
    return task.deferLater(
        clock, delay.total_seconds(), function, *args, **kwargs)


def makeDelayingCallback(clock, delay):
    """
    Make a transparent callback that waits for ``delay``.

    :param IReactorTime clock: Event loop that controls time.
    :param timedelta delay: How long to wait
    :return: A ``Deferred`` that fires with the value of the previous callback.
    """
    def delayingCallback(value):
        return deferLater(clock, delay, lambda: value)
    return delayingCallback


def waitFor(clock, delay, deferred):
    """
    Usage::

        waitFor(reactor, timedelta(seconds=20), d).addCallback(print)

    Will wait for 20s before calling ``print`` with the result of ``d``.
    """
    # H/T @tomprince
    return deferred.addCallback(makeDelayingCallback(clock, delay))
