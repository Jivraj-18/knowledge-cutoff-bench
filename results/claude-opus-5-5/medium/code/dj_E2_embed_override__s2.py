from functools import wraps

from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

CSP = "default-src 'self'; img-src 'self' https:"
EMBED_CSP = "default-src 'self'; frame-ancestors *"


class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Content-Security-Policy"] = getattr(response, "csp_policy", CSP)
        return response


def csp_policy(policy):
    """Override the Content-Security-Policy set by CSPMiddleware for a view."""

    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            response.csp_policy = policy
            return response

        return wrapped

    return decorator


@xframe_options_exempt
@csp_policy(EMBED_CSP)
def embed(request):
    return HttpResponse("embed")


MIDDLEWARE = ["solution.CSPMiddleware"]
EXTRA_SETTINGS = {}
