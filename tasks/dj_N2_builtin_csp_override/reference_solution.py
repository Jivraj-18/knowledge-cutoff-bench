from django.http import HttpResponse
from django.utils.csp import CSP
from django.views.decorators.csp import csp_override
MIDDLEWARE_ENTRY = "django.middleware.csp.ContentSecurityPolicyMiddleware"
EXTRA_SETTINGS = {"SECURE_CSP": {"default-src": [CSP.SELF], "img-src": [CSP.SELF, "https:"]}}
@csp_override({"default-src": [CSP.SELF], "frame-ancestors": ["*"]})
def embed(request):
    return HttpResponse("embed")
