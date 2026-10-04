from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

CSP_HEADER = "Content-Security-Policy"
DEFAULT_POLICY = "default-src 'self'; img-src 'self' https:"
EMBED_POLICY = "default-src 'self'; frame-ancestors *"


class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    """Apply the project-wide CSP, unless a view explicitly overrides it."""

    def process_response(self, request, response):
        override = getattr(response, "_csp_override", None)
        response[CSP_HEADER] = override if override is not None else DEFAULT_POLICY
        return response


MIDDLEWARE_ENTRY = "solution.ContentSecurityPolicyMiddleware"

EXTRA_SETTINGS = {}


def embed(request):
    response = HttpResponse("embed")
    response._csp_override = EMBED_POLICY
    response[CSP_HEADER] = EMBED_POLICY
    return response
