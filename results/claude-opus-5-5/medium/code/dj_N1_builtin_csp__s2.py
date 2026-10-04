"""Configure Django's built-in Content Security Policy support.

Django 6.0 ships ``django.middleware.csp.ContentSecurityPolicyMiddleware``,
which emits the ``Content-Security-Policy`` header from the ``SECURE_CSP``
setting. Each directive maps to a list of sources; the middleware joins
directives with "; " and sources with " ", preserving dict order, so this
config produces:

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
