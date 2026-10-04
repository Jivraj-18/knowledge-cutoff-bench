from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

CSP = "default-src 'self'; img-src 'self' https:"
EMBED_CSP = "default-src 'self'; frame-ancestors *"


class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Views may set their own policy; only apply the default otherwise.
        if "Content-Security-Policy" not in response:
            response["Content-Security-Policy"] = CSP
        return response


@xframe_options_exempt
def embed(request):
    response = HttpResponse("embed")
    response["Content-Security-Policy"] = EMBED_CSP
    return response


MIDDLEWARE = ["solution.CSPMiddleware"]
EXTRA_SETTINGS = {}
