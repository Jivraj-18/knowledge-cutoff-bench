from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class CSPMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if not response.has_header("Content-Security-Policy"):
            response["Content-Security-Policy"] = "default-src 'self'; img-src 'self' https:"
        return response


def embed(request):
    response = HttpResponse("embed")
    response["Content-Security-Policy"] = "default-src 'self'; frame-ancestors *"
    return response


MIDDLEWARE_ENTRY = "solution.CSPMiddleware"
EXTRA_SETTINGS = {}
