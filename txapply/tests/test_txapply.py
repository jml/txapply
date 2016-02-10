# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Tests for txapply.
"""

import operator

from hypothesis import assume, given
from hypothesis.strategies import (
    choices,
    dictionaries,
    integers,
)
from testtools import TestCase
from testtools.matchers import AfterPreprocessing, Equals, Is
from testtools.twistedsupport import failed, succeeded
from twisted.internet.defer import maybeDeferred, succeed

from txapply import gather_dict, txapply

from .strategies import (
    any_value,
    arguments,
    binary_functions,
    exceptions,
    identity,
    keyword_arguments,
    throw,
    unary_functions,
)


class ApplyTests(TestCase):
    """
    Tests for `txapply`.
    """

    @given(anything=any_value())
    def test_identity(self, anything):
        """
        ``txapply(identity, deferred)`` is equivalent to ``deferred``.
        """
        d = txapply(identity, succeed(anything))
        self.assertThat(d, succeeded(Is(anything)))

    @given(f=unary_functions, x=integers())
    def test_unary_function(self, f, x):
        """
        ``txapply(f, d)`` is equivalent to ``d.addCallback(f)``.
        """
        d = txapply(f, succeed(x))
        self.assertThat(d, succeeded(Equals(f(x))))

    @given(f=binary_functions, x=integers(), y=integers())
    def test_binary_function(self, f, x, y):
        """
        The function given to ``txapply`` is called with the values from the
        Deferreds it is given.

        ``txapply(f, d1, d2)`` will return a Deferred with the result of
        ``f(x, y)``, where ``x`` is the result of ``d1`` and ``y`` is the
        result of ``d2``.
        """
        assume(f not in (operator.div, operator.mod) or y != 0)
        d = txapply(f, succeed(x), succeed(y))
        self.assertThat(d, succeeded(Equals(f(x, y))))

    @given(args=arguments())
    def test_positional_arguments(self, args):
        """
        The function given to ``txapply`` is called with the values from the
        Deferreds it is given.
        """
        deferred_args = map(succeed, args)
        d = txapply(lambda *a: a, *deferred_args)
        self.assertThat(d, succeeded(Equals(tuple(args))))

    @given(kwargs=keyword_arguments())
    def test_keyword_arguments(self, kwargs):
        """
        The function given to ``txapply`` is called with keyword arguments from
        the values of the Deferreds it is given as keyword arguments.

        That is, keyword arguments are passed through.

        ``txapply(f, foo=d1, bar=d2)`` is equivalent to ``f(foo=x, bar=y)``
        where ``x`` is the result of ``d1`` and ``y`` is the result of ``d2``.

        """
        deferred_kwargs = {
            key: succeed(value) for key, value in kwargs.items()
        }
        d = txapply(dict, **deferred_kwargs)
        self.assertThat(d, succeeded(Equals(kwargs)))

    @given(args=arguments(), kwargs=keyword_arguments())
    def test_combination_arguments(self, args, kwargs):
        """
        If ``txapply`` is given a combination of positional and keyword
        arguments, these are passed through to the function.
        """
        deferred_args = map(succeed, args)
        deferred_kwargs = {
            key: succeed(value) for key, value in kwargs.items()
        }

        def capture(*a, **kw):
            return a, kw

        d = txapply(capture, *deferred_args, **deferred_kwargs)
        self.assertThat(d, succeeded(Equals((tuple(args), kwargs))))

    @given(args=arguments(), kwargs=keyword_arguments())
    def test_combination_arguments_deferred_function(self, args, kwargs):
        """
        If ``txapply`` is called with a function ``f`` that itself returns a
        ``Deferred`` then the result of that ``Deferred`` is the result of
        calling ``f`` with the results of all of the ``Deferred`` objects
        passed to ``txapply``.
        """
        deferred_args = map(succeed, args)
        deferred_kwargs = {
            key: succeed(value) for key, value in kwargs.items()
        }

        def capture(*a, **kw):
            return succeed((a, kw))

        d = txapply(capture, *deferred_args, **deferred_kwargs)
        self.assertThat(d, succeeded(Equals((tuple(args), kwargs))))

    @given(args=arguments(min_size=1), exception=exceptions(),
           choice=choices())
    def test_exception_in_args(self, args, exception, choice):
        """
        If one of the arguments is a failing Deferred, then "reraise" that
        failing Deferred.
        """
        i = choice(range(len(args)))
        deferred_args = map(succeed, args)
        deferred_args[i] = maybeDeferred(throw, exception)
        d = txapply(lambda *a: a, *deferred_args)
        self.assertThat(d, failed(
            AfterPreprocessing(lambda failure: failure.value,
                               Equals(exception))))


class GatherDictTests(TestCase):
    """
    Tests for ``gather_dict``.
    """

    @given(dictionaries(any_value(), any_value()))
    def test_gathers_dictionary(self, dictionary):
        """
        ``gather_dict`` returns a Deferred that fires with a dict that has the
        keys of the original dict mapped to the results of the Deferreds which
        were the values.
        """
        deferred_dict = {k: succeed(v) for (k, v) in dictionary.items()}
        d = gather_dict(deferred_dict)
        self.assertThat(d, succeeded(Equals(dictionary)))
