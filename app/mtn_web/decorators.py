import time
import functools
import logging

from django.db import connection, reset_queries

log = logging.getLogger(__name__)


def query_inspection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("func: ", func.__name__)
        reset_queries()

        start = time.time()
        start_queries = len(connection.queries)

        result = func(*args, **kwargs)

        end = time.time()
        end_queries = len(connection.queries)

        duration = end - start

        log.info(module=func.__module__, function=func.__name__, start=start, end=end, duration=duration.total_seconds())

        print("queries:", end_queries - start_queries)
        print("took: %.2fs" % (end - start))

        # if config.get('INSPECT_QUERIES'):
        # return result
        return result
    return wrapper
