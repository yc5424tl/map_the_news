import sys
from better_exceptions import excepthook


class BetterExceptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    @staticmethod
    def process_exceptions(self, request, exception):
        excepthook(exception.__class__, exception, sys.exc_info()[2])
        return None
