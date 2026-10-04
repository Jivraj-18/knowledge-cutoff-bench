MIDDLEWARE_ENTRY = "django.middleware.security.SecurityMiddleware"

EXTRA_SETTINGS = {
    "SECURE_CONTENT_SECURITY_POLICY": "default-src 'self'; img-src 'self' https:",
}
