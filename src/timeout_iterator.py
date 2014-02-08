from __future__ import print_function, division

from functools import partial

from threading import Timer
from multiprocessing import Process, Manager
from Queue import Queue


class QueueStop(object):
    """Used as a stop for the fetch_until_timeout queue
    """
    def __eq__(self, other):
        same_instance = lambda: isinstance(other, self.__class__)
        same_dict = lambda: self.__dict__ == other.__dict__

        return same_instance() and same_dict()


def fetch_until_timeout(timeout=0.1):
    """
    Parameters
    ----------
    timeout : double

    Returns
    -------
    timeout : iterator -> iterator
        An wrapper to timeout the fetching of elements of an iterator.

    Note
    ----
    If the iterator isn't consumed within the timeout nothing
    will be returned, which can be a bit weird.
    """
    def timeout_iterator(iterator):
        """Wraps an iterator and makes it timeout after time ``timeout``.

        Parameters
        ----------
        iterator : iterator

        Returns
        -------
        timeout_iterator : iterator
        """
        buffer_ = Manager().Queue()

        process = Process(
            target=partial(map),
            args=(buffer_.put, iterator)
        )

        process.start()
        process.join(timeout)
        process.terminate()

        buffer_.put(QueueStop())

        timeout_iterator = iter(buffer_.get, QueueStop())

        return timeout_iterator

    return timeout_iterator
