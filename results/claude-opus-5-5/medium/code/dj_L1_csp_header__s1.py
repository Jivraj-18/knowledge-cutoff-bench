from django.utils.deprecation import MiddlewareMixin

CSP_HEADER_NAME = "Content-Security-Policy"
CSP_HEADER_VALUE = "default-src 'self'; img-src 'self' https:"


class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    """Attach the Content-Security-Policy header to every response.

    Django 5.2 has no built-in CSP support. MiddlewareMixin makes this work
    under both WSGI (sync) and ASGI (async) request handling.
    """

    def process_response(self, request, response):
        response.headers[CSP_HEADER_NAME] = CSP_HEADER_VALUE
        return response


MIDDLEWARE_ENTRY = "solution.ContentSecurityPolicyMiddleware"

EXTRA_SETTINGS = {}
