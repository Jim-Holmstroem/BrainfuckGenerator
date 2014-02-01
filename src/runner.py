from __future__ import print_function, division

from functools import partial, wraps

from threading import Timer
from multiprocessing import Process, Manager
from Queue import Queue


class QueueStop(object):
    def __eq__(self, other):
        return isinstance(other, QueueStop)\
            and self.__dict__ == other.__dict__


def fetch_until_timeout(timeout=0.1):
    def iterator_with_timeout(iterator):
        buffer_ = Manager().Queue()

        process = Process(
            target=partial(map),
            args=(buffer_.put, iterator)
        )

        process.start()

        stopper = Timer(
            timeout,
            partial(process.terminate),
        )
        stopper.start()

        process.join()
        stopper.cancel()

        buffer_.put(QueueStop())

        return iter(buffer_.get, QueueStop())

    return iterator_with_timeout
