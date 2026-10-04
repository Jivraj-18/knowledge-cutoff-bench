from django.template import Context, Engine

CARD_TEMPLATE = '<div class="card">{{ item }}</div>'

MAIN_TEMPLATE = (
    "F:{% for item in featured %}{% include 'card.html' %}{% endfor %}"
    "|O:{% for item in others %}{% include 'card.html' %}{% endfor %}"
)

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


def render_cards(featured, others):
    template = _engine.get_template("main.html")
    return template.render(
        Context({"featured": list(featured), "others": list(others)})
    )
