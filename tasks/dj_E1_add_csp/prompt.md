Our project's requirements.txt:
```
Django>=5.2,<6
asgiref
```

Here is the current `solution.py` from our project:
```python
class SecurityHeadersMiddleware:
    """Adds our standard security headers to every response."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["X-Content-Type-Options"] = "nosniff"
        response["Referrer-Policy"] = "same-origin"
        return response


MIDDLEWARE = ["solution.SecurityHeadersMiddleware"]
EXTRA_SETTINGS = {}
```

Security asked us to add a Content-Security-Policy to every response:
 `default-src 'self'; img-src 'self' https:`. Keep the existing headers. `MIDDLEWARE` is the project's middleware list
 and `EXTRA_SETTINGS` is merged into settings; change either as needed.
Return the complete updated `solution.py`.

Respond with exactly one Python code block containing the complete contents of `solution.py`. No explanation outside the code block. Do not use any third-party packages other than django.
