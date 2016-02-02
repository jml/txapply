"""
txapply: library for calling functions with Deferred arguments.
"""

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from ._txapply import gather_dict, txapply

__all__ = [
    'gather_dict',
    'txapply',
]
