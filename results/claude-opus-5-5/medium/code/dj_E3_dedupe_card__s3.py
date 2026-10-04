from django.template import Context, Engine

_CARD = '<div class="card">{{ item }}</div>'

_ENGINE = Engine(
    loaders=[
        ("django.template.loaders.locmem.Loader", {"card.html": _CARD}),
    ],
)
_PAGE = (
    'F:{% for item in featured %}{% include "card.html" %}{% endfor %}'
    '|O:{% for item in others %}{% include "card.html" %}{% endfor %}'
)


def render_cards(featured, others):
    return _ENGINE.from_string(_PAGE).render(Context({"featured": featured, "others": others}))
