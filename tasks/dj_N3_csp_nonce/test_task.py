import sys, types, re, django
from django.conf import settings
import solution
urls = types.ModuleType("test_urls"); sys.modules["test_urls"] = urls
settings.configure(DEBUG=False, SECRET_KEY="x", ALLOWED_HOSTS=["testserver"], ROOT_URLCONF="test_urls", INSTALLED_APPS=[],
    MIDDLEWARE=[solution.MIDDLEWARE_ENTRY],
    TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates",
                "OPTIONS": {"context_processors": list(solution.CONTEXT_PROCESSORS),
                            "loaders": [("django.template.loaders.locmem.Loader", {"page.html": solution.PAGE_TEMPLATE})]}}],
    **solution.EXTRA_SETTINGS)
django.setup()
from django.shortcuts import render
from django.urls import path
urls.urlpatterns = [path("", lambda r: render(r, "page.html"))]
from django.test import Client
resp = Client().get("/")
assert solution.MIDDLEWARE_ENTRY == "django.middleware.csp.ContentSecurityPolicyMiddleware"
h = resp.headers.get("Content-Security-Policy", "")
m = re.search(r"'nonce-([^']+)'", h); assert m, h
assert "script-src" in h and "'self'" in h, h
body = resp.content.decode()
assert f'nonce="{m.group(1)}"' in body, body
print("PASS")
