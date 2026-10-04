from django.utils.csp import CSP

MIDDLEWARE_ENTRY = "django.middleware.csp.ContentSecurityPolicyMiddleware"

EXTRA_SETTINGS = {
    "SECURE_CSP": {
        "default-src": [CSP.SELF],
        "img-src": [CSP.SELF, "https:"],
    },
}
