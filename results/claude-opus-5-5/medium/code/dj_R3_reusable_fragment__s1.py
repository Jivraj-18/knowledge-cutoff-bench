from django.conf import settings
from django.template import Context, Engine

# Card markup is defined exactly once and reused via {% include %} for both lists.
CARD_TEMPLATE = '<div class="card">{{ item }}</div>'

MAIN_TEMPLATE = (
    "F:"
    "{% for item in featured %}{% include 'card.html' %}{% endfor %}"
    "|O:"
    "{% for item in others %}{% include 'card.html' %}{% endfor %}"
)

_engine = None


def _get_engine():
    global _engine
    if _engine is None:
        # Rendering some values (e.g. numbers) consults settings for
        # localization, so provide defaults if nothing is configured.
        if not settings.configured:
            settings.configure()
        _engine = Engine(
            loaders=[
                (
                    "django.template.loaders.locmem.Loader",
                    {
                        "card.html": CARD_TEMPLATE,
                        "main.html": MAIN_TEMPLATE,
                    },
                )
            ]
        )
    return _engine


def render_cards(featured, others):
    template = _get_engine().get_template("main.html")
    return template.render(
        Context({"featured": list(featured), "others": list(others)})
    )
