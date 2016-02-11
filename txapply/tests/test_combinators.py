"""
Tests for combinators.
"""

from hypothesis import given
from testtools import TestCase
from testtools.matchers import Equals, Is
from testtools.twistedsupport import succeeded

from twisted.internet.defer import succeed
from .._combinators import nop, transparent
from .strategies import any_value, arguments, keyword_arguments


class TestNop(TestCase):
    """
    Tests for ``nop``.
    """

    @given(args=arguments(), kwargs=keyword_arguments())
    def test_none(self, args, kwargs):
        """
        ``nop`` always returns ``None``, regardless of what you call it with.
        """
        self.assertThat(nop(*args, **kwargs), Is(None))


class TestTransparent(TestCase):
    """
    Tests for ``transparent``.
    """

    @given(first=any_value(), second=any_value())
    def test_passes_value_through(self, first, second):
        """
        The return value of a callbacks added with ``transparent`` is ignored,
        and instead the previous value in the chain is passed through.
        """
        d = succeed(first)
        d.addCallback(transparent, lambda ignored: second)
        self.assertThat(d, succeeded(Is(first)))

    @given(first=any_value(), second=any_value(), args=arguments(),
           kwargs=keyword_arguments())
    def test_calls_transparent_callback(self, first, second, args, kwargs):
        """
        Even though the return value of a "transparent" callback is ignored,
        it *is* invoked and is passed all the arguments and keyword arguments
        it would have if it were a normal callback.
        """
        log = []

        def callback(value, *a, **kw):
            log.append((value, a, kw))
            return second
        d = succeed(first)
        d.addCallback(transparent, callback, *args, **kwargs)
        self.assertThat(log, Equals([(first, args, kwargs)]))
