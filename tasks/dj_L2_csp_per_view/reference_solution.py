from django.http import HttpResponse
DEFAULT = "default-src 'self'; img-src 'self' https:"
class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        response = self.get_response(request)
        response["Content-Security-Policy"] = getattr(response, "csp_policy", DEFAULT)
        return response
def embed(request):
    r = HttpResponse("embed")
    r.csp_policy = "default-src 'self'; frame-ancestors *"
    return r
MIDDLEWARE_ENTRY = "solution.CSPMiddleware"
EXTRA_SETTINGS = {}
