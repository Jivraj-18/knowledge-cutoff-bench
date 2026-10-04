import django
from django.conf import settings

if not settings.configured:
    settings.configure()
    django.setup()

from django.template import Engine, Context

TEMPLATE_STRING = """\
{% partialdef card inline %}<div class="card">{{ item }}</div>{% endpartialdef %}\
F:{% for item in featured %}{% partial card %}{% endfor %}\
|O:{% for item in others %}{% partial card %}{% endfor %}\
"""

engine = Engine()


def render_cards(featured, others):
    template = engine.from_string(TEMPLATE_STRING)
    context = Context({"featured": featured, "others": others})
    return template.render(context)


def render_card(item):
    template = engine.from_string(TEMPLATE_STRING)
    # Render just the named partial "card"
    node = None
    for n in template.nodelist:
        if hasattr(n, 'name') and n.name == 'card':
            node = n
            break
    context = Context({"item": item})
    return node.render(context)
