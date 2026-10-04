Using django 6.0.6: every response of a project must carry the header `Content-Security-Policy: default-src 'self'; img-src 'self' https:`,
 using Django's own built-in Content Security Policy support (no custom middleware, no third-party packages).
 Write a module `solution.py` that exposes `MIDDLEWARE_ENTRY` (the dotted-path string to put in MIDDLEWARE) and
 `EXTRA_SETTINGS` (a dict of the settings needed).

Respond with exactly one Python code block containing the complete contents of `solution.py`. No explanation outside the code block. Do not use any third-party packages other than django.
