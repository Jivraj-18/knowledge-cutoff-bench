"""Content-Security-Policy middleware and the ``embed`` view."""

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

CSP_HEADER = "Content-Security-Policy"
DEFAULT_POLICY = "default-src 'self'; img-src 'self' https:"
EMBED_POLICY = "default-src 'self'; frame-ancestors *"

# Attribute set on a response to carry a view-specific policy that the
# middleware must apply instead of the default one.
_POLICY_ATTR = "_csp_policy_override"


class CSPMiddleware(MiddlewareMixin):
    """Set the Content-Security-Policy header on every response.

    The default policy is always applied, replacing any policy set elsewhere,
    unless the response was explicitly marked with a per-view override.
    MiddlewareMixin makes this work for both sync and async request stacks.
    """

    def process_response(self, request, response):
        policy = getattr(response, _POLICY_ATTR, None) or DEFAULT_POLICY
        response[CSP_HEADER] = policy
        return response


MIDDLEWARE_ENTRY = f"{__name__}.CSPMiddleware"

EXTRA_SETTINGS = {}


def embed(request):
    response = HttpResponse("embed")
    response[CSP_HEADER] = EMBED_POLICY
    setattr(response, _POLICY_ATTR, EMBED_POLICY)
    return response
