Our project's requirements.txt:
```
Django>=5.2,<6
asgiref
```

Here is the current `solution.py` from our project:
```python
from django.template import Engine, Context

_ENGINE = Engine()
_PAGE = (
    'F:{% for item in featured %}<div class="card">{{ item }}</div>{% endfor %}'
    '|O:{% for item in others %}<div class="card">{{ item }}</div>{% endfor %}'
)


def render_cards(featured, others):
    return _ENGINE.from_string(_PAGE).render(Context({"featured": featured, "others": others}))
```

The card markup is duplicated. Refactor so `<div class="card">{{ item }}</div>` is
 written only once and reused for both lists. Output must stay the same (whitespace does not matter).
Return the complete updated `solution.py`.

Respond with exactly one Python code block containing the complete contents of `solution.py`. No explanation outside the code block. Do not use any third-party packages other than django.
