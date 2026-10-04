Our project's requirements.txt:
```
Django>=5.2,<6
asgiref
```

Every response of a project must carry the header `Content-Security-Policy: default-src 'self'; img-src 'self' https:`.
 Write a module `solution.py` that exposes `MIDDLEWARE_ENTRY` (the dotted-path string to put in MIDDLEWARE; it may
 point to a class defined in `solution.py`, i.e. `"solution.ClassName"`) and `EXTRA_SETTINGS` (a dict of any
 additional settings needed; may be empty).

Respond with exactly one Python code block containing the complete contents of `solution.py`. No explanation outside the code block. Do not use any third-party packages other than django.
