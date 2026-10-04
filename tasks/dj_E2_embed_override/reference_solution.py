
from django.http import HttpResponse

CSP = "default-src 'self'; img-src 'self' https:"


class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Content-Security-Policy"] = getattr(response, "csp", CSP)
        return response


def embed(request):
    response = HttpResponse("embed")
    response.csp = "default-src 'self'; frame-ancestors *"
    return response


MIDDLEWARE = ["solution.CSPMiddleware"]
EXTRA_SETTINGS = {}
