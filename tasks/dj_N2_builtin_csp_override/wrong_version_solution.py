from django.http import HttpResponse
from csp.decorators import csp_replace
MIDDLEWARE_ENTRY = "csp.middleware.CSPMiddleware"
EXTRA_SETTINGS = {"CSP_DEFAULT_SRC": ("'self'",), "CSP_IMG_SRC": ("'self'", "https:")}
@csp_replace(FRAME_ANCESTORS="*")
def embed(request):
    return HttpResponse("embed")
