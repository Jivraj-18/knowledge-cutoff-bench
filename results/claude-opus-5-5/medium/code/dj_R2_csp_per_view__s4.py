from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.views.decorators.clickjacking import xframe_options_exempt

CSP_HEADER = "Content-Security-Policy"
DEFAULT_POLICY = "default-src 'self'; img-src 'self' https:"
EMBED_POLICY = "default-src 'self'; frame-ancestors *"

MIDDLEWARE_ENTRY = "solution.ContentSecurityPolicyMiddleware"
EXTRA_SETTINGS = {}


class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    """Apply the site-wide CSP to every response unless a view opted out."""

    def process_response(self, request, response):
        override = getattr(response, "_csp_override", None)
        response[CSP_HEADER] = override if override is not None else DEFAULT_POLICY
        return response


@xframe_options_exempt
def embed(request):
    response = HttpResponse("embed")
    response[CSP_HEADER] = EMBED_POLICY
    response._csp_override = EMBED_POLICY
    return response
