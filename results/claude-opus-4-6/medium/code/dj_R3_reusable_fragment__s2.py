import django
from django.conf import settings

if not settings.configured:
    settings.configure()

from django.template import Engine, Context

TEMPLATE_STRING = """
{% for item in featured %}{% include "card" %}{% endfor %}|O:{% for item in others %}{% include "card" %}{% endfor %}
"""

CARD_TEMPLATE = '<div class="card">{{ item }}</div>'


def render_cards(featured, others):
    engine = Engine()
    from django.template import Template
    card_template = engine.from_string(CARD_TEMPLATE)

    template_str = "F:{% for item in featured %}" + CARD_TEMPLATE + "{% endfor %}|O:{% for item in others %}" + CARD_TEMPLATE + "{% endfor %}"
    # Card markup written once:
    CARD = '<div class="card">{{ item }}</div>'
    parts = []
    parts.append("F:")
    for item in featured:
        parts.append(engine.from_string(CARD).render(Context({"item": item})))
    parts.append("|O:")
    for item in others:
        parts.append(engine.from_string(CARD).render(Context({"item": item})))
    return "".join(parts)
