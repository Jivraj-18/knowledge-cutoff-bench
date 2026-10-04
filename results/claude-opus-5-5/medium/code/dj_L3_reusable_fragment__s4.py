from django.conf import settings
from django.template import Context, Engine

if not settings.configured:
    # Rendering non-string values (numbers, dates) consults formatting settings.
    settings.configure()

CARD = '<div class="card">{{ item }}</div>'

PAGE = (
    "F:{% for item in featured %}{% include 'card.html' %}{% endfor %}"
    "|O:{% for item in others %}{% include 'card.html' %}{% endfor %}"
)

_engine = Engine(
    loaders=[
        (
            "django.template.loaders.locmem.Loader",
            {"card.html": CARD, "page.html": PAGE},
        )
    ]
)


def render_cards(featured, others):
    template = _engine.get_template("page.html")
    return template.render(Context({"featured": featured, "others": others}))
