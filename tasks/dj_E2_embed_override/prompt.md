Our project's requirements.txt:
```
Django>=5.2,<6
asgiref
```

Here is the current `solution.py` from our project:
```python
from django.http import HttpResponse

CSP = "default-src 'self'; img-src 'self' https:"


class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Content-Security-Policy"] = CSP
        return response


def embed(request):
    return HttpResponse("embed")


MIDDLEWARE = ["solution.CSPMiddleware"]
EXTRA_SETTINGS = {}
```

The `embed` view is now shown inside partner sites, so its policy must be exactly
 `default-src 'self'; frame-ancestors *`. All other views keep the current policy.
Return the complete updated `solution.py`.

Respond with exactly one Python code block containing the complete contents of `solution.py`. No explanation outside the code block. Do not use any third-party packages other than django.
