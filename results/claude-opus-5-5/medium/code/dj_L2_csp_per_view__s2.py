from django.http import HttpResponse

DEFAULT_CSP = "default-src 'self'; img-src 'self' https:"
EMBED_CSP = "default-src 'self'; frame-ancestors *"

MIDDLEWARE_ENTRY = "solution.ContentSecurityPolicyMiddleware"
EXTRA_SETTINGS = {}


class ContentSecurityPolicyMiddleware:
    """Apply the project-wide CSP header to every response.

    Responses that explicitly opt out (via the ``_csp_exempt`` marker set by
    views such as ``embed``) keep the policy they set themselves.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if getattr(response, "_csp_exempt", False):
            response.headers.setdefault("Content-Security-Policy", DEFAULT_CSP)
        else:
            response.headers["Content-Security-Policy"] = DEFAULT_CSP
        return response


def embed(request):
    response = HttpResponse("embed")
    response.headers["Content-Security-Policy"] = EMBED_CSP
    response._csp_exempt = True
    return response
