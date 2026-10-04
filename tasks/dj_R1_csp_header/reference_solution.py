class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        response = self.get_response(request)
        response["Content-Security-Policy"] = "default-src 'self'; img-src 'self' https:"
        return response
MIDDLEWARE_ENTRY = "solution.CSPMiddleware"
EXTRA_SETTINGS = {}
