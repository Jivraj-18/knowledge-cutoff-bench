from django.http import HttpResponse

CSP = "default-src 'self'; img-src 'self' https:"
EMBED_CSP = "default-src 'self'; frame-ancestors *"


class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not hasattr(response, "_csp_policy"):
            response["Content-Security-Policy"] = CSP
        else:
            response["Content-Security-Policy"] = response._csp_policy
        return response


def embed(request):
    response = HttpResponse("embed")
    response._csp_policy = EMBED_CSP
    return response


MIDDLEWARE = ["solution.CSPMiddleware"]
EXTRA_SETTINGS = {}
