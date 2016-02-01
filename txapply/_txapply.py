"""
txapply: library for calling functions with Deferred arguments.
"""

from twisted.internet.defer import gatherResults, succeed


def _get_failure(failure):
    """
    Extract the *real* failure from a ``FirstError``.
    """
    return failure.value.subFailure


def _gather_results(deferreds):
    """
    Gather a list of Deferreds into a single Deferred.

    If any Deferred fails, returns a Deferred that fails.

    :param List[Deferred[A]] deferreds: A list of Deferreds.
    :rtype: Deferred[List[A]]
    :returns: A Deferred that fires with the successful values of the list.
    """
    # TODO: Write our own gatherResult.
    d = gatherResults(deferreds, consumeErrors=True)
    d.addErrback(_get_failure)
    return d


def _gather_dict(deferred_dict):
    """
    Gather a dictionary with Deferred values into a single Deferred.

    If any Deferred fails, returns a Deferred that fails.

    :param Map[A, Deferred[B]] deferred_dict: A dictionary with Deferred
        values.
    :return: A Deferred that fires with a dictionary where all the Deferred
        values have been resolved.
    :rtype: Deferred[Map[A, B]]
    """
    if not deferred_dict:
        return succeed({})
    keys, values = zip(*deferred_dict.items())
    d = _gather_results(values)

    def got_results(real_values):
        return {key: real_value for key, real_value in zip(keys, real_values)}
    d.addCallback(got_results)
    return d


def txapply(function, *args, **kwargs):
    """
    Call ``function`` with Deferred arguments.

    All the arguments and keyword arguments to ``txapply`` must be Deferreds.
    ``txapply`` will call ``function`` with the results of these Deferreds,
    and return a Deferred that will fire with its result.
    """
    d1 = _gather_results(args)
    d2 = _gather_dict(kwargs)
    d = _gather_results([d1, d2])

    def got_real_args(result):
        [real_args, real_kwargs] = result
        return function(*real_args, **real_kwargs)
    d.addCallback(got_real_args)
    return d
