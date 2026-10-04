
class SecurityHeadersMiddleware:
    """Adds our standard security headers to every response."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["X-Content-Type-Options"] = "nosniff"
        response["Referrer-Policy"] = "same-origin"
        response["Content-Security-Policy"] = "default-src 'self'; img-src 'self' https:"
        return response


MIDDLEWARE = ["solution.SecurityHeadersMiddleware"]
EXTRA_SETTINGS = {}
