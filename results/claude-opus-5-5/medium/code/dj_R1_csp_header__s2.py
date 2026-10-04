from asgiref.sync import iscoroutinefunction, markcoroutinefunction

CSP_HEADER_NAME = "Content-Security-Policy"
CSP_HEADER_VALUE = "default-src 'self'; img-src 'self' https:"


class ContentSecurityPolicyMiddleware:
    """Ensure every response carries the project's Content-Security-Policy header."""

    sync_capable = True
    async_capable = True

    def __init__(self, get_response):
        if get_response is None:
            raise ValueError("get_response must be provided.")
        self.get_response = get_response
        self.async_mode = iscoroutinefunction(self.get_response)
        if self.async_mode:
            markcoroutinefunction(self)

    def __call__(self, request):
        if self.async_mode:
            return self.__acall__(request)
        response = self.get_response(request)
        return self.process_response(request, response)

    async def __acall__(self, request):
        response = await self.get_response(request)
        return self.process_response(request, response)

    def process_response(self, request, response):
        response[CSP_HEADER_NAME] = CSP_HEADER_VALUE
        return response


MIDDLEWARE_ENTRY = "solution.ContentSecurityPolicyMiddleware"

EXTRA_SETTINGS = {}
