import django
from django.conf import settings

if not settings.configured:
    settings.configure()
    django.setup()

from django.template import Engine, Context

TEMPLATE_STRING = """
{% for item in featured %}<div class="card">{{ item }}</div>{% endfor %}
|O:
{% for item in others %}<div class="card">{{ item }}</div>{% endfor %}
"""

def render_cards(featured, others):
    engine = Engine()
    card_template = engine.from_string('<div class="card">{{ item }}</div>')
    featured_cards = "".join(card_template.render(Context({"item": i})) for i in featured)
    others_cards = "".join(card_template.render(Context({"item": i})) for i in others)
    return f"F:{featured_cards}|O:{others_cards}"
