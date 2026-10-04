Using django 6.0.6: every response must carry `Content-Security-Policy: default-src 'self'; img-src 'self' https:`, except the `embed` view, whose
 policy must be exactly `default-src 'self'; frame-ancestors *`. Use Django's own built-in Content Security Policy
 support only (no custom middleware, no third-party packages). Write a module `solution.py` that exposes
 `MIDDLEWARE_ENTRY` (dotted-path string), `EXTRA_SETTINGS` (dict), and a view `embed(request)` returning `HttpResponse("embed")`.

Respond with exactly one Python code block containing the complete contents of `solution.py`. No explanation outside the code block. Do not use any third-party packages other than django.
