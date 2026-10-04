from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.views.decorators.clickjacking import xframe_options_exempt

CSP_HEADER = "Content-Security-Policy"
DEFAULT_POLICY = "default-src 'self'; img-src 'self' https:"
EMBED_POLICY = "default-src 'self'; frame-ancestors *"

MIDDLEWARE_ENTRY = "solution.ContentSecurityPolicyMiddleware"
EXTRA_SETTINGS = {}


class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    """Add the project-wide CSP header unless the view already set its own.

    MiddlewareMixin makes this work under both WSGI and ASGI.
    """

    def process_response(self, request, response):
        if getattr(response, "_csp_override", False):
            return response
        if CSP_HEADER not in response:
            response[CSP_HEADER] = DEFAULT_POLICY
        return response


@xframe_options_exempt
def embed(request):
    response = HttpResponse("embed")
    response[CSP_HEADER] = EMBED_POLICY
    response._csp_override = True
    return response
