from django.conf import settings
from django.template import Context, Engine

# Minimal settings so non-string values (ints, dates) can be localized during
# rendering; no Django project is required.
if not settings.configured:
    settings.configure()

_TEMPLATES = {
    "card.html": '<div class="card">{{ item }}</div>',
    "cards.html": (
        "F:{% for item in featured %}{% include 'card.html' %}{% endfor %}"
        "|O:{% for item in others %}{% include 'card.html' %}{% endfor %}"
    ),
}

_engine = Engine(
    loaders=[("django.template.loaders.locmem.Loader", _TEMPLATES)],
)


def render_cards(featured, others):
    template = _engine.get_template("cards.html")
    return template.render(
        Context({"featured": list(featured or []), "others": list(others or [])})
    )
