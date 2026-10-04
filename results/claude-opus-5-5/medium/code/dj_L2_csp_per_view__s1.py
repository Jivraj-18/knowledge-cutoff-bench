from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

DEFAULT_CSP = "default-src 'self'; img-src 'self' https:"
EMBED_CSP = "default-src 'self'; frame-ancestors *"

MIDDLEWARE_ENTRY = "solution.ContentSecurityPolicyMiddleware"
EXTRA_SETTINGS = {}


class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    """Apply the project-wide CSP to every response, unless the view
    explicitly provided its own policy via the `_csp_override` marker."""

    def process_response(self, request, response):
        override = getattr(response, "_csp_override", None)
        response["Content-Security-Policy"] = override if override else DEFAULT_CSP
        return response


def embed(request):
    response = HttpResponse("embed")
    response["Content-Security-Policy"] = EMBED_CSP
    response._csp_override = EMBED_CSP
    return response
