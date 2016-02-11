import operator
import string

from hypothesis.strategies import (
    builds,
    characters,
    dictionaries,
    lists,
    sampled_from,
    text,
)


def identity(x):
    return x


unary_functions = sampled_from([
    operator.abs,
    operator.invert,
    operator.neg,
    operator.not_,
    operator.truth,
    identity,
])
"""
Arbitrary unary functions that take an integer and return something.
"""


def throw(x):
    """
    Raise ``x``.
    """
    raise x


def any_value():
    """
    Arbitrary values, with no constraints.
    """
    return builds(object)


def ascii_text():
    """
    Arbitrary ascii-encodable text.
    """
    return text(characters(max_codepoint=128))


def exceptions():
    """
    Arbitrary exceptions.
    """
    return ascii_text().map(Exception)


binary_functions = sampled_from([
    operator.add,
    operator.div,
    operator.eq,
    operator.ge,
    operator.gt,
    operator.is_,
    operator.is_not,
    operator.le,
    operator.lt,
    operator.mod,
    operator.mul,
    operator.ne,
    operator.sub,
])
"""
Arbitrary binary functions that take two integers and return something.
"""


identifier_characters = string.ascii_letters + string.digits + '_'


identifiers = text(average_size=20, min_size=1, alphabet=identifier_characters)
"""
Python identifiers.

e.g. ``Foo``, ``bar``.
"""


def arguments(min_size=0):
    """
    Arbitrary arguments to a function.
    """
    return lists(any_value(), min_size=min_size).map(tuple)


def keyword_arguments():
    """
    Arbitrary keyword arguments to a function.
    """
    return dictionaries(identifiers, any_value())
