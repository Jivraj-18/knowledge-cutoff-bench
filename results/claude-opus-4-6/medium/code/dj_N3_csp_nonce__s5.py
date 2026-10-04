MIDDLEWARE_ENTRY = "django.middleware.csp.ContentSecurityPolicyMiddleware"

EXTRA_SETTINGS = {
    "CONTENT_SECURITY_POLICY": {
        "DIRECTIVES": {
            "script-src": ["'self'"],
        },
    },
}

CONTEXT_PROCESSORS = ["django.template.context_processors.csp_nonce"]

PAGE_TEMPLATE = '<script nonce="{{ csp_nonce }}">console.log(1)</script>'
