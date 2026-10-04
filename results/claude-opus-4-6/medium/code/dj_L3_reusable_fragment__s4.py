import django
from django.conf import settings

if not settings.configured:
    settings.configure()

from django.template import Engine, Context

TEMPLATE = """
{% for item in featured %}<div class="card">{{ item }}</div>{% endfor %}
"""

def render_cards(featured, others):
    engine = Engine()
    card_template = engine.from_string('<div class="card">{{ item }}</div>')
    
    parts = ["F:"]
    for item in featured:
        parts.append(card_template.render(Context({"item": item})))
    
    parts.append("|O:")
    for item in others:
        parts.append(card_template.render(Context({"item": item})))
    
    return "".join(parts)
