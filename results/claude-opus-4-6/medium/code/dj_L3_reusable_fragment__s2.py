import django
from django.conf import settings

if not settings.configured:
    settings.configure()
    django.setup()

from django.template import Engine, Context

TEMPLATE_STRING = """
{% for item in featured %}<div class="card">{{ item }}</div>{% endfor %}
"""

def render_cards(featured, others):
    engine = Engine()
    card_template = engine.from_string('<div class="card">{{ item }}</div>')
    
    featured_cards = ""
    for item in featured:
        featured_cards += card_template.render(Context({"item": item}))
    
    other_cards = ""
    for item in others:
        other_cards += card_template.render(Context({"item": item}))
    
    return f"F:{featured_cards}|O:{other_cards}"
