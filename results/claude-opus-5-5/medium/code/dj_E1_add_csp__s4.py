class SecurityHeadersMiddleware:
    """Adds our standard security headers to every response."""

    CONTENT_SECURITY_POLICY = "default-src 'self'; img-src 'self' https:"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["X-Content-Type-Options"] = "nosniff"
        response["Referrer-Policy"] = "same-origin"
        response["Content-Security-Policy"] = self.CONTENT_SECURITY_POLICY
        return response


MIDDLEWARE = ["solution.SecurityHeadersMiddleware"]
EXTRA_SETTINGS = {}
