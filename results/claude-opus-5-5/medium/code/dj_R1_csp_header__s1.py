"""Middleware that adds a fixed Content-Security-Policy header to every response."""

from django.utils.deprecation import MiddlewareMixin

CSP_HEADER_NAME = "Content-Security-Policy"
CSP_HEADER_VALUE = "default-src 'self'; img-src 'self' https:"


class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    """Set the project-wide Content-Security-Policy header on every response.

    MiddlewareMixin makes this work under both WSGI (sync) and ASGI (async)
    request handling.
    """

    def process_response(self, request, response):
        response[CSP_HEADER_NAME] = CSP_HEADER_VALUE
        return response


MIDDLEWARE_ENTRY = "solution.ContentSecurityPolicyMiddleware"

EXTRA_SETTINGS = {}
