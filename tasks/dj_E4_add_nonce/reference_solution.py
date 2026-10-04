
import secrets

CSP = "script-src 'self'"


class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.csp_nonce = secrets.token_urlsafe(16)
        response = self.get_response(request)
        response["Content-Security-Policy"] = f"{CSP} 'nonce-{request.csp_nonce}'"
        return response


def nonce(request):
    return {"csp_nonce": getattr(request, "csp_nonce", "")}


MIDDLEWARE = ["solution.CSPMiddleware"]
EXTRA_SETTINGS = {}
CONTEXT_PROCESSORS = ["solution.nonce"]
PAGE_TEMPLATE = '<script nonce="{{ csp_nonce }}">console.log(1)</script>'
