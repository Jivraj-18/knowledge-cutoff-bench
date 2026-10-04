from django.template import Context, Engine

TEMPLATE_NAME = "cards.html"

TEMPLATE_SOURCE = (
    '{% partialdef card %}<div class="card">{{ item }}</div>{% endpartialdef %}'
    "F:{% for item in featured %}{% partial card %}{% endfor %}"
    "|O:{% for item in others %}{% partial card %}{% endfor %}"
)

_engine = Engine(
    loaders=[
        ("django.template.loaders.locmem.Loader", {TEMPLATE_NAME: TEMPLATE_SOURCE}),
    ],
)


def render_cards(featured, others):
    template = _engine.get_template(TEMPLATE_NAME)
    return template.render(Context({"featured": featured, "others": others}))


def render_card(item):
    template = _engine.get_template(f"{TEMPLATE_NAME}#card")
    return template.render(Context({"item": item}))
