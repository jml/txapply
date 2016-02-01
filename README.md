# txapply

A little library for calling functions with
[Deferred](https://twistedmatrix.com/documents/current/api/twisted.internet.defer.Deferred.html)
arguments.

## Example

```python

def function(some, name=None):
    print('Got {} (name={})'.format(some, name))
    return name


def finished(value):
    print('Finished: {}'.format(value))
    reactor.stop()

result = txapply(function, some_deferred, name=other_deferred)
result.addCallback(finished)

```

## Warning

This is unreleased, unsupported software that makes no claims to backwards
compatibility or correctness.

In particular, I dislike the name `txapply` and am likely to change it.

## License

Copyright (c) Twisted Matrix Laboratories.

Made available under the MIT license. See LICENSE for details.
