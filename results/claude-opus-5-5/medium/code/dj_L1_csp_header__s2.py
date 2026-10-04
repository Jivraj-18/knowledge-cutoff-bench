from django.utils.deprecation import MiddlewareMixin

CSP_HEADER_NAME = "Content-Security-Policy"
CSP_HEADER_VALUE = "default-src 'self'; img-src 'self' https:"


class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    """Attach a fixed Content-Security-Policy header to every response.

    MiddlewareMixin gives this class both sync and async support, so it
    works under WSGI and ASGI without an extra sync/async adaptation layer.
    """

    def process_response(self, request, response):
        response[CSP_HEADER_NAME] = CSP_HEADER_VALUE
        return response


MIDDLEWARE_ENTRY = "solution.ContentSecurityPolicyMiddleware"

EXTRA_SETTINGS = {}
