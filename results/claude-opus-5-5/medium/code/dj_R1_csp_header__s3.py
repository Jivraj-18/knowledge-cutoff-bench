from django.utils.deprecation import MiddlewareMixin

CSP_HEADER_VALUE = "default-src 'self'; img-src 'self' https:"


class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    """Attach the project's Content-Security-Policy header to every response."""

    def process_response(self, request, response):
        response["Content-Security-Policy"] = CSP_HEADER_VALUE
        return response


MIDDLEWARE_ENTRY = "solution.ContentSecurityPolicyMiddleware"

EXTRA_SETTINGS = {}
