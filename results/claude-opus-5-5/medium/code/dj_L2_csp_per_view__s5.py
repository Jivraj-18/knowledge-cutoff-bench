from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

CSP_HEADER = "Content-Security-Policy"
DEFAULT_POLICY = "default-src 'self'; img-src 'self' https:"
EMBED_POLICY = "default-src 'self'; frame-ancestors *"

MIDDLEWARE_ENTRY = "solution.ContentSecurityPolicyMiddleware"

EXTRA_SETTINGS = {}


class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    """Apply the project-wide CSP unless the response opts into its own policy."""

    def process_response(self, request, response):
        override = getattr(response, "_csp_override", None)
        response[CSP_HEADER] = override if override is not None else DEFAULT_POLICY
        return response


def embed(request):
    response = HttpResponse("embed")
    response._csp_override = EMBED_POLICY
    response[CSP_HEADER] = EMBED_POLICY
    return response
