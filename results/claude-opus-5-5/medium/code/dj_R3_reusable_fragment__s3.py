from django.template import Context, Engine

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
    # Pre-stringify items so rendering never needs configured settings
    # (number localization would otherwise read django.conf.settings).
    context = Context(
        {
            "featured": [str(item) for item in featured],
            "others": [str(item) for item in others],
        }
    )
    return _engine.get_template("cards.html").render(context)
