from django.utils.csp import CSP

MIDDLEWARE_ENTRY = "django.middleware.csp.ContentSecurityPolicyMiddleware"

EXTRA_SETTINGS = {
    "SECURE_CSP": {
        "script-src": [CSP.SELF, CSP.NONCE],
    },
}

CONTEXT_PROCESSORS = [
    "django.template.context_processors.csp",
]

PAGE_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>CSP nonce example</title>
</head>
<body>
  <script nonce="{{ csp_nonce }}">console.log(1)</script>
</body>
</html>
"""
