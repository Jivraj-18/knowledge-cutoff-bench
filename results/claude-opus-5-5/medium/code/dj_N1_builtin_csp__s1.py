"""Django 6.0 built-in Content Security Policy configuration."""

MIDDLEWARE_ENTRY = "django.middleware.csp.ContentSecurityPolicyMiddleware"

EXTRA_SETTINGS = {
    "SECURE_CSP": {
        "default-src": ["'self'"],
        "img-src": ["'self'", "https:"],
    },
}
