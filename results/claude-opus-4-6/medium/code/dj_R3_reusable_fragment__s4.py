import django
from django.conf import settings

if not settings.configured:
    settings.configure()
    django.setup()

from django.template import Engine, Context

def render_cards(featured, others):
    engine = Engine()
    template = engine.from_string(
        "F:{% for item in featured %}<div class=\"card\">{{ item }}</div>{% endfor %}"
        "|O:{% for item in others %}<div class=\"card\">{{ item }}</div>{% endfor %}"
    )
    return template.render(Context({"featured": featured, "others": others}))
