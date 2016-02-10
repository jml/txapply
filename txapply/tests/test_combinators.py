"""
Tests for combinators.
"""

from hypothesis import given
from testtools import TestCase
from testtools.matchers import Is

from .._combinators import nop
from .strategies import arguments, keyword_arguments


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
