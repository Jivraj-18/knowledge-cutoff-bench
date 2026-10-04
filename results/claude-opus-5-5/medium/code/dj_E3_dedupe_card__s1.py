from django.template import Engine, Context

_CARD = '<div class="card">{{ item }}</div>'
_PAGE = (
    'F:{% for item in featured %}{% include "card.html" %}{% endfor %}'
    '|O:{% for item in others %}{% include "card.html" %}{% endfor %}'
)

_ENGINE = Engine(
    loaders=[
        (
            "django.template.loaders.locmem.Loader",
            {"card.html": _CARD, "page.html": _PAGE},
        )
    ]
)


def render_cards(featured, others):
    return _ENGINE.get_template("page.html").render(
        Context({"featured": featured, "others": others})
    )
