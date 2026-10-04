from django.http import HttpResponse

DEFAULT_CSP = "default-src 'self'; img-src 'self' https:"
EMBED_CSP = "default-src 'self'; frame-ancestors *"


class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not response.has_header("Content-Security-Policy"):
            response["Content-Security-Policy"] = DEFAULT_CSP
        return response


def embed(request):
    response = HttpResponse("embed")
    response["Content-Security-Policy"] = EMBED_CSP
    return response


MIDDLEWARE_ENTRY = "solution.CSPMiddleware"
EXTRA_SETTINGS = {}
