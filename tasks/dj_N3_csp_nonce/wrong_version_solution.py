MIDDLEWARE_ENTRY = "csp.middleware.CSPMiddleware"
EXTRA_SETTINGS = {"CSP_SCRIPT_SRC": ("'self'",), "CSP_INCLUDE_NONCE_IN": ["script-src"]}
CONTEXT_PROCESSORS = ["csp.context_processors.nonce"]
PAGE_TEMPLATE = '<script nonce="{{ request.csp_nonce }}">console.log(1)</script>'
