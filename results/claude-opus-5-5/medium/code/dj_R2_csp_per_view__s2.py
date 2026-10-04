from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.http import HttpResponse

DEFAULT_CSP = "default-src 'self'; img-src 'self' https:"
EMBED_CSP = "default-src 'self'; frame-ancestors *"

MIDDLEWARE_ENTRY = "solution.ContentSecurityPolicyMiddleware"
EXTRA_SETTINGS = {}


class ContentSecurityPolicyMiddleware:
    """Apply the project-wide CSP to every response.

    A response may opt into its own policy by setting the attribute
    ``_csp_override`` to the exact policy string; that policy then replaces
    the default, and is enforced even if something else tampered with the
    header in between.
    """

    sync_capable = True
    async_capable = True

    def __init__(self, get_response):
        self.get_response = get_response
        self._is_async = iscoroutinefunction(get_response)
        if self._is_async:
            markcoroutinefunction(self)

    def __call__(self, request):
        if self._is_async:
            return self.__acall__(request)
        response = self.get_response(request)
        return self._apply(response)

    async def __acall__(self, request):
        response = await self.get_response(request)
        return self._apply(response)

    @staticmethod
    def _apply(response):
        override = getattr(response, "_csp_override", None)
        response["Content-Security-Policy"] = override if override else DEFAULT_CSP
        return response


def embed(request):
    response = HttpResponse("embed")
    response._csp_override = EMBED_CSP
    response["Content-Security-Policy"] = EMBED_CSP
    return response
