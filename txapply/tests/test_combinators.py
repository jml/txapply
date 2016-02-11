"""
Tests for combinators.
"""

from hypothesis import given
from testtools import TestCase
from testtools.matchers import Equals, Is
from testtools.twistedsupport import succeeded

from twisted.internet.defer import succeed
from .._combinators import combine, ignore, nop, transparent
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
        The return value of a callback added with ``transparent`` is ignored,
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


class TestIgnore(TestCase):
    """
    Tests for ``ignore``.
    """

    @given(first=any_value(), second=any_value(), args=arguments(),
           kwargs=keyword_arguments())
    def test_ignores_callback_value(self, first, second, *args, **kwargs):
        """
        Callbacks added with ``ignore`` don't get passed the return value of
        the previous callback.
        """
        log = []

        def callback(*a, **kw):
            log.append((a, kw))
            return second
        d = succeed(first)
        d.addCallback(ignore, callback, *args, **kwargs)
        self.assertThat(d, succeeded(Is(second)))
        self.assertThat(log, Equals([(args, kwargs)]))


class TestCombine(TestCase):
    """
    Tests for ``combine``.
    """

    @given(first=any_value(), second=any_value(), args=arguments(),
           kwargs=keyword_arguments())
    def test_combines_results(self, first, second, *args, **kwargs):
        """
        The return value of a callback added with ``combine`` is a tuple made
        up of the *previous* callback value and whatever the new callback
        returns.
        """
        log = []

        def callback(value, *a, **kw):
            log.append((value, a, kw))
            return second

        d = succeed(first)
        d.addCallback(combine, callback, *args, **kwargs)
        self.assertThat(d, succeeded(Equals((second, first))))
        self.assertThat(log, Equals([(first, args, kwargs)]))
