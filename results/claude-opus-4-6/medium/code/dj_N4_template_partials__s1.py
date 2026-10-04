import django
from django.conf import settings

if not settings.configured:
    settings.configure()
    django.setup()

from django.template import Engine

TEMPLATE_SOURCE = (
    "{% partialdef card %}<div class=\"card\">{{ item }}</div>{% endpartialdef %}"
    "F:{% for item in featured %}{% partial card %}{% endfor %}"
    "|O:{% for item in others %}{% partial card %}{% endfor %}"
)

engine = Engine()


def render_cards(featured, others):
    template = engine.from_string(TEMPLATE_SOURCE)
    from django.template import Context
    ctx = Context({"featured": featured, "others": others})
    return template.render(ctx)


def render_card(item):
    template = engine.from_string(TEMPLATE_SOURCE)
    from django.template import Context
    ctx = Context({"item": item})
    return template.nodelist[0].render(ctx)
