
from django.http import HttpResponse
from django.utils.csp import CSP as C
from django.views.decorators.csp import csp_override

MIDDLEWARE = ["django.middleware.csp.ContentSecurityPolicyMiddleware"]
EXTRA_SETTINGS = {"SECURE_CSP": {"default-src": [C.SELF], "img-src": [C.SELF, "https:"]}}


@csp_override({"default-src": [C.SELF], "frame-ancestors": ["*"]})
def embed(request):
    return HttpResponse("embed")
