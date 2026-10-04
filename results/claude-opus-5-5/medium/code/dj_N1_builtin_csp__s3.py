"""Content-Security-Policy configuration using Django 6.0's built-in CSP support."""

# Django 6.0 ships a built-in CSP middleware. It reads the SECURE_CSP setting
# and emits the Content-Security-Policy header on every response.
MIDDLEWARE_ENTRY = "django.middleware.csp.ContentSecurityPolicyMiddleware"

# Directives are serialized in insertion order as "<directive> <sources...>",
# joined with "; ", producing:
#   default-src 'self'; img-src 'self' https:
# The literal "'self'" is the same value as django.utils.csp.CSP.SELF.
EXTRA_SETTINGS = {
    "SECURE_CSP": {
        "default-src": ["'self'"],
        "img-src": ["'self'", "https:"],
    },
}
