from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

DEFAULT_CSP = "default-src 'self'; img-src 'self' https:"


class CSPMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if "Content-Security-Policy" not in response:
            response["Content-Security-Policy"] = DEFAULT_CSP
        return response


def embed(request):
    response = HttpResponse("embed")
    response["Content-Security-Policy"] = "default-src 'self'; frame-ancestors *"
    return response


MIDDLEWARE_ENTRY = "solution.CSPMiddleware"
EXTRA_SETTINGS = {}
