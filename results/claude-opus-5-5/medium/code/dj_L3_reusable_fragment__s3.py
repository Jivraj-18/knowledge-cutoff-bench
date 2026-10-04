from django.conf import settings
from django.template import Context, Engine

# Rendering non-string values (e.g. ints) consults a few settings, so provide
# minimal defaults when running outside a Django project.
if not settings.configured:
    settings.configure(USE_I18N=False)

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
    return template.render(Context({"featured": featured, "others": others}))
