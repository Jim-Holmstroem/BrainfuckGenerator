from __future__ import print_function, division

from functools import wraps, partial
import threading

class TimeoutError(Exception): pass

def timelimit(timeout):
    """Copy pasted from http://code.activestate.com/recipes/483752/
    """
    def internal(function):

        @wraps(function)
        def internal2(*args, **kw):
            class Calculator(threading.Thread):
                def __init__(self, result=None, error=None):
                    super(Calculator, self).__init__()
                    self.result = result
                    self.error = error

                def run(self):
                    try:
                        self.result = function(*args, **kw)
                    except:
                        import sys
                        self.error = sys.exc_info()

            c = Calculator()
            c.start()
            c.join(timeout)

            if c.is_alive():
                raise TimeoutError('TimedOut')
            if c.error[0]:
                raise c.error[1]

            return c.result

        internal2.__name__ = 'timelimit({})'.format(internal2.__name__)

        return internal2

    return internal


def timeout_default(f, default_value, timeout=1):
    try:
        timed_f = timelimit(timeout)(f)
        return timed_f()

    except TimeoutError as te:
        return default_value


def fetch_until_timeout(iterator, timeout=0.1):
    buffer_ = []
    try:
        def fetch():
            map(buffer_.append, iterator)  # TODO mush specialize the timelimit code for iterators this was too easy

        print('start')
        timed_fetch = timelimit(timeout)(fetch)
        print(timed_fetch)
        print('timed_fetch()')
        timed_fetch()
        print('fully fetched')

    except TimeoutError as te:
        print('Timeout')
        pass

    finally:
        print('finally return buffer_ {}'.format(type(buffer_)))
        return buffer_
