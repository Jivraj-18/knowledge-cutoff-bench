MIDDLEWARE_ENTRY = "django.middleware.security.SecurityMiddleware"

EXTRA_SETTINGS = {
    "CONTENT_SECURITY_POLICY": {
        "DIRECTIVES": {
            "default-src": ["'self'"],
            "img-src": ["'self'", "https:"],
        }
    }
}
