from django.template import Context, Engine

CARD_TEMPLATE = '<div class="card">{{ item }}</div>'

_engine = Engine(
    loaders=[
        (
            "django.template.loaders.locmem.Loader",
            {
                "card.html": CARD_TEMPLATE,
                "cards.html": (
                    "F:{% for item in featured %}{% include 'card.html' %}{% endfor %}"
                    "|O:{% for item in others %}{% include 'card.html' %}{% endfor %}"
                ),
            },
        )
    ],
)


def render_cards(featured, others):
    template = _engine.get_template("cards.html")
    # Convert items to str up front so rendering never needs Django settings
    # (number/date localization would otherwise consult settings).
    context = Context(
        {
            "featured": [str(item) for item in featured],
            "others": [str(item) for item in others],
        },
        use_l10n=False,
        use_tz=False,
    )
    return template.render(context)
