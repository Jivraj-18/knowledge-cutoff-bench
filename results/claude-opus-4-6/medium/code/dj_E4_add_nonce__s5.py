import secrets

CSP_BASE = "script-src 'self'"


def csp_nonce(request):
    return {"csp_nonce": request.csp_nonce}


class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        nonce = secrets.token_urlsafe(32)
        request.csp_nonce = nonce
        response = self.get_response(request)
        response["Content-Security-Policy"] = f"{CSP_BASE} 'nonce-{nonce}'"
        return response


MIDDLEWARE = ["solution.CSPMiddleware"]
EXTRA_SETTINGS = {}
CONTEXT_PROCESSORS = ["solution.csp_nonce"]
PAGE_TEMPLATE = '<script nonce="{{ csp_nonce }}">console.log(1)</script>'
