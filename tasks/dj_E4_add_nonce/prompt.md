Our project's requirements.txt:
```
Django>=5.2,<6
asgiref
```

Here is the current `solution.py` from our project:
```python
CSP = "script-src 'self'"


class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Content-Security-Policy"] = CSP
        return response


MIDDLEWARE = ["solution.CSPMiddleware"]
EXTRA_SETTINGS = {}
CONTEXT_PROCESSORS = []
PAGE_TEMPLATE = "<script>console.log(1)</script>"
```

The inline script on our page is blocked by the policy. Allow it with a nonce that
 changes on every request: the header must become `script-src 'self' 'nonce-<value>'` and the script tag in
 `PAGE_TEMPLATE` must carry the same nonce. `MIDDLEWARE`, `EXTRA_SETTINGS` and `CONTEXT_PROCESSORS` (template
 context processor paths) are used to configure the project; change them as needed.
Return the complete updated `solution.py`.

Respond with exactly one Python code block containing the complete contents of `solution.py`. No explanation outside the code block. Do not use any third-party packages other than django.
