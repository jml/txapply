# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

import codecs
import os
import versioneer

from setuptools import find_packages, setup


def read(*parts):
    """
    Build an absolute path from C{parts} and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *parts), 'r', 'utf-8') as f:
        return f.read()


if __name__ == "__main__":
    setup(
        classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Topic :: Software Development :: Libraries :: Python Modules'
        ],
        description="Call functions with Deferred arguments",
        long_description=read('README.md'),
        keywords="twisted",
        license="MIT",
        name="txapply",
        packages=find_packages(),
        url="https://github.com/jml/txapply",
        maintainer='Jonathan M. Lange',
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        install_requires=[
            'Twisted',
        ],
        extras_require={
            'tests': [
                'testtools>=1.9.0',
                'hypothesis>=1.18.1',
            ],
        },
    )
