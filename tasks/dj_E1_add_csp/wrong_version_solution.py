
from django.utils.csp import CSP

class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["X-Content-Type-Options"] = "nosniff"
        response["Referrer-Policy"] = "same-origin"
        return response


MIDDLEWARE = ["solution.SecurityHeadersMiddleware", "django.middleware.csp.ContentSecurityPolicyMiddleware"]
EXTRA_SETTINGS = {"SECURE_CSP": {"default-src": [CSP.SELF], "img-src": [CSP.SELF, "https:"]}}
