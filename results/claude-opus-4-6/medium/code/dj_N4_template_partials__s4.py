import django
from django.conf import settings

if not settings.configured:
    settings.configure()
    django.setup()

from django.template import Engine, Context

TEMPLATE_STRING = (
    '{% partialdef card %}<div class="card">{{ item }}</div>{% endpartialdef %}'
    'F:{% for item in featured %}{% partial card %}{% endfor %}'
    '|O:{% for item in others %}{% partial card %}{% endfor %}'
)

engine = Engine()


def render_cards(featured, others):
    template = engine.from_string(TEMPLATE_STRING)
    return template.render(Context({"featured": featured, "others": others}))


def render_card(item):
    template = engine.from_string(TEMPLATE_STRING)
    for node in template.nodelist:
        if hasattr(node, "name") and node.name == "card":
            return node.nodelist.render(Context({"item": item}))
    raise ValueError("partial 'card' not found")
