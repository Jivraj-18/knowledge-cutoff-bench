Using django 5.2.17: every response of a project must carry the header `Content-Security-Policy: default-src 'self'; img-src 'self' https:`,
 except the `embed` view, whose policy must be exactly `default-src 'self'; frame-ancestors *`.
 Write a module `solution.py` that exposes `MIDDLEWARE_ENTRY` (the dotted-path string to put in MIDDLEWARE; it may
 point to a class defined in `solution.py`), `EXTRA_SETTINGS` (dict, may be empty), and a view function
 `embed(request)` that returns `HttpResponse("embed")` with the required policy.

Respond with exactly one Python code block containing the complete contents of `solution.py`. No explanation outside the code block. Do not use any third-party packages other than django.
