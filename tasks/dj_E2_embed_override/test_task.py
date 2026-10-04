
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
mw = solution.MIDDLEWARE if hasattr(solution, "MIDDLEWARE") else [solution.MIDDLEWARE_ENTRY]
settings.configure(DEBUG=False, SECRET_KEY="x", ALLOWED_HOSTS=["testserver"], ROOT_URLCONF="test_urls",
                   INSTALLED_APPS=[], MIDDLEWARE=list(mw), **getattr(solution, "EXTRA_SETTINGS", {}))
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

assert policy(c.get("/")) == {"default-src": {"'self'"}, "img-src": {"'self'", "https:"}}, policy(c.get("/"))
assert policy(c.get("/embed/")) == {"default-src": {"'self'"}, "frame-ancestors": {"*"}}, policy(c.get("/embed/"))
print("PASS")
