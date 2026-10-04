
from django.utils.csp import CSP

MIDDLEWARE = ["django.middleware.csp.ContentSecurityPolicyMiddleware"]
EXTRA_SETTINGS = {"SECURE_CSP": {"script-src": [CSP.SELF, CSP.NONCE]}}
CONTEXT_PROCESSORS = ["django.template.context_processors.csp"]
PAGE_TEMPLATE = '<script nonce="{{ csp_nonce }}">console.log(1)</script>'
