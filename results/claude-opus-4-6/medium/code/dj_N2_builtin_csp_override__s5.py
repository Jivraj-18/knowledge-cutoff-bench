from django.http import HttpResponse

MIDDLEWARE_ENTRY = "django.middleware.security.SecurityMiddleware"

EXTRA_SETTINGS = {
    "CONTENT_SECURITY_POLICY": {
        "DIRECTIVES": {
            "default-src": ["'self'"],
            "img-src": ["'self'", "https:"],
        },
    },
}


def embed(request):
    response = HttpResponse("embed")
    response["Content-Security-Policy"] = "default-src 'self'; frame-ancestors *"
    return response
