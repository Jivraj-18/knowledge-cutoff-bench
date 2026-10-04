import sys, types, django
from django.conf import settings
import solution
from django.http import HttpResponse
def _home(request): return HttpResponse("home")
views = {"home": getattr(solution, "home", _home)}
if hasattr(solution, "embed"): views["embed"] = solution.embed
urls = types.ModuleType("test_urls")
from django.urls import path
urls.urlpatterns = [path("", views["home"])] + ([path("embed/", views["embed"])] if "embed" in views else [])
sys.modules["test_urls"] = urls
settings.configure(DEBUG=False, SECRET_KEY="x", ALLOWED_HOSTS=["testserver"], ROOT_URLCONF="test_urls",
                   INSTALLED_APPS=[], MIDDLEWARE=[solution.MIDDLEWARE_ENTRY], **getattr(solution, "EXTRA_SETTINGS", {}))
django.setup()
from django.test import Client
c = Client()
def policy(resp):
    h = resp.headers.get("Content-Security-Policy", "")
    out = {}
    for part in h.split(";"):
        toks = part.split()
        if toks: out[toks[0]] = set(toks[1:])
    return out

assert solution.MIDDLEWARE_ENTRY == "django.middleware.csp.ContentSecurityPolicyMiddleware", solution.MIDDLEWARE_ENTRY
p = policy(c.get("/"))
assert p == {"default-src": {"'self'"}, "img-src": {"'self'", "https:"}}, p
print("PASS")
