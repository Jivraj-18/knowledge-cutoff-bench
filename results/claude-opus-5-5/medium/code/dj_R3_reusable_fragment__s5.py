from django.conf import settings
from django.template import Context, Engine

# Rendering non-string values (e.g. numbers) consults settings for localization,
# so provide defaults when running outside a Django project.
if not settings.configured:
    settings.configure()

CARD_TEMPLATE = '<div class="card">{{ item }}</div>'

PAGE_TEMPLATE = (
    "F:{% for item in featured %}{% include 'card.html' %}{% endfor %}"
    "|O:{% for item in others %}{% include 'card.html' %}{% endfor %}"
)

_engine = Engine(
    loaders=[
        (
            "django.template.loaders.locmem.Loader",
            {
                "card.html": CARD_TEMPLATE,
                "page.html": PAGE_TEMPLATE,
            },
        ),
    ],
)


def render_cards(featured, others):
    template = _engine.get_template("page.html")
    return template.render(Context({"featured": featured, "others": others}))
