"""
Configuration for Django 6.0's built-in Content Security Policy support.

Django 6.0 ships ``django.middleware.csp.ContentSecurityPolicyMiddleware``,
which reads the ``SECURE_CSP`` setting (a dict mapping directives to lists of
sources) and emits the ``Content-Security-Policy`` header on every response.
Directives are serialized in dict order, joined with "; ", and each directive's
sources are joined with spaces, producing:

    Content-Security-Policy: default-src 'self'; img-src 'self' https:
"""

from django.utils.csp import CSP

MIDDLEWARE_ENTRY = "django.middleware.csp.ContentSecurityPolicyMiddleware"

EXTRA_SETTINGS = {
    "SECURE_CSP": {
        "default-src": [CSP.SELF],
        "img-src": [CSP.SELF, "https:"],
    },
}
