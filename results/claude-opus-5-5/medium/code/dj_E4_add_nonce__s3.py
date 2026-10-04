import secrets

CSP = "script-src 'self'"


def _build_csp(nonce):
    return f"{CSP} 'nonce-{nonce}'"


class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        nonce = secrets.token_urlsafe(16)
        request.csp_nonce = nonce
        response = self.get_response(request)
        response["Content-Security-Policy"] = _build_csp(nonce)
        return response


def csp_nonce(request):
    nonce = getattr(request, "csp_nonce", None)
    if nonce is None:
        nonce = secrets.token_urlsafe(16)
        request.csp_nonce = nonce
    return {"csp_nonce": nonce}


MIDDLEWARE = ["solution.CSPMiddleware"]
EXTRA_SETTINGS = {}
CONTEXT_PROCESSORS = ["solution.csp_nonce"]
PAGE_TEMPLATE = '<script nonce="{{ csp_nonce }}">console.log(1)</script>'
