import django
from django.conf import settings

if not settings.configured:
    settings.configure()

from django.template import Engine, Context

TEMPLATE_STRING = """
{% for item in featured %}<div class="card">{{ item }}</div>{% endfor %}|O:{% for item in others %}<div class="card">{{ item }}</div>{% endfor %}
"""

def render_cards(featured, others):
    engine = Engine()
    template_str = 'F:{% for item in featured %}<div class="card">{{ item }}</div>{% endfor %}|O:{% for item in others %}<div class="card">{{ item }}</div>{% endfor %}'
    # Use inclusion to write card markup once
    card = '<div class="card">{{ item }}</div>'
    parts = []
    parts.append('F:')
    t_card = engine.from_string(card)
    for item in featured:
        parts.append(t_card.render(Context({'item': item})))
    parts.append('|O:')
    for item in others:
        parts.append(t_card.render(Context({'item': item})))
    return ''.join(parts)
