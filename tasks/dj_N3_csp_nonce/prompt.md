Using django 6.0.6: a page has an inline `<script>` that must be allowed by a nonce. Using Django's own built-in Content Security
 Policy support only (no custom middleware, no third-party packages), write a module `solution.py` exposing:
 `MIDDLEWARE_ENTRY` (dotted-path string), `EXTRA_SETTINGS` (dict; the policy must be `script-src 'self'` plus the
 per-request nonce), `CONTEXT_PROCESSORS` (list of dotted paths to add to the template context processors), and
 `PAGE_TEMPLATE` (a Django template string containing `<script>console.log(1)</script>` with the correct nonce attribute).

Respond with exactly one Python code block containing the complete contents of `solution.py`. No explanation outside the code block. Do not use any third-party packages other than django.
