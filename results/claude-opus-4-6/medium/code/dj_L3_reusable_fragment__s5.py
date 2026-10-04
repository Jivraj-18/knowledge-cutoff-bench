import django
from django.conf import settings

if not settings.configured:
    settings.configure()

from django.template import Engine, Context

TEMPLATE_STRING = """\
F:{% for item in featured %}<div class="card">{{ item }}</div>{% endfor %}|O:{% for item in others %}<div class="card">{{ item }}</div>{% endfor %}"""

def render_cards(featured, others):
    engine = Engine()
    template = engine.from_string(
        'F:{% for item in featured %}{% include_card %}{% endfor %}'
        '|O:{% for item in others %}{% include_card %}{% endfor %}'
    )
    # Use a single card template string and render both lists
    card = '<div class="card">{{ item }}</div>'
    engine = Engine()
    card_template = engine.from_string(card)

    parts = ["F:"]
    for item in featured:
        parts.append(card_template.render(Context({"item": item})))
    parts.append("|O:")
    for item in others:
        parts.append(card_template.render(Context({"item": item})))
    return "".join(parts)
