from django.utils.deprecation import MiddlewareMixin

CSP_HEADER_NAME = "Content-Security-Policy"
CSP_HEADER_VALUE = "default-src 'self'; img-src 'self' https:"


class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    """Set a fixed Content-Security-Policy header on every response.

    Django 5.2 has no built-in CSP support (added in 6.0), so this is a small
    custom middleware. MiddlewareMixin makes it work under both WSGI and ASGI.
    The header is set unconditionally so every response carries exactly the
    required policy, even if a view or other middleware set a different one.
    """

    def process_response(self, request, response):
        response[CSP_HEADER_NAME] = CSP_HEADER_VALUE
        return response


MIDDLEWARE_ENTRY = "solution.ContentSecurityPolicyMiddleware"

EXTRA_SETTINGS = {}
