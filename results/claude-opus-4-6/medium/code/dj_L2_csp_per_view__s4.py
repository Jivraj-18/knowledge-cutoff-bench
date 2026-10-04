from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class CSPMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if not hasattr(response, '_csp_override'):
            response["Content-Security-Policy"] = "default-src 'self'; img-src 'self' https:"
        return response


def embed(request):
    resp = HttpResponse("embed")
    resp["Content-Security-Policy"] = "default-src 'self'; frame-ancestors *"
    resp._csp_override = True
    return resp


MIDDLEWARE_ENTRY = "solution.CSPMiddleware"
EXTRA_SETTINGS = {}
