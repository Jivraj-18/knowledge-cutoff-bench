import secrets

CSP = "script-src 'self'"


def _generate_nonce():
    return secrets.token_urlsafe(16)


class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        nonce = _generate_nonce()
        request.csp_nonce = nonce
        response = self.get_response(request)
        response["Content-Security-Policy"] = f"{CSP} 'nonce-{nonce}'"
        return response


def csp_nonce(request):
    return {"csp_nonce": getattr(request, "csp_nonce", "")}


MIDDLEWARE = ["solution.CSPMiddleware"]
EXTRA_SETTINGS = {}
CONTEXT_PROCESSORS = ["solution.csp_nonce"]
PAGE_TEMPLATE = '<script nonce="{{ csp_nonce }}">console.log(1)</script>'
