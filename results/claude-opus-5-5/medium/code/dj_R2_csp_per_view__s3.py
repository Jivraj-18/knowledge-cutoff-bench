from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

DEFAULT_CSP = "default-src 'self'; img-src 'self' https:"
EMBED_CSP = "default-src 'self'; frame-ancestors *"

MIDDLEWARE_ENTRY = "solution.ContentSecurityPolicyMiddleware"
EXTRA_SETTINGS = {}


class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    """Apply the project-wide CSP to every response.

    Responses flagged with ``_csp_override`` keep the policy their view set;
    every other response gets the default policy, replacing any existing one.
    """

    def process_response(self, request, response):
        override = getattr(response, "_csp_override", None)
        response["Content-Security-Policy"] = override or DEFAULT_CSP
        return response


def embed(request):
    response = HttpResponse("embed")
    response["Content-Security-Policy"] = EMBED_CSP
    response._csp_override = EMBED_CSP
    return response
