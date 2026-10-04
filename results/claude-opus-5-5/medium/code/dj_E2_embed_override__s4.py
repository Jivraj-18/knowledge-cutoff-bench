from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

CSP = "default-src 'self'; img-src 'self' https:"
EMBED_CSP = "default-src 'self'; frame-ancestors *"


class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Respect a policy explicitly set by the view; otherwise apply the default.
        if not response.has_header("Content-Security-Policy"):
            response["Content-Security-Policy"] = CSP
        return response


@xframe_options_exempt
def embed(request):
    response = HttpResponse("embed")
    response["Content-Security-Policy"] = EMBED_CSP
    return response


MIDDLEWARE = ["solution.CSPMiddleware"]
EXTRA_SETTINGS = {}
