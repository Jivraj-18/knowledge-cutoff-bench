from django.conf import settings
from django.template import Context, Engine

if not settings.configured:
    settings.configure(USE_I18N=False)

_engine = Engine()

_template = _engine.from_string(
    "{% for label, items in groups %}"
    "{{ label }}"
    "{% for item in items %}"
    '<div class="card">{{ item }}</div>'
    "{% endfor %}"
    "{% endfor %}"
)


def render_cards(featured, others):
    groups = [("F:", featured), ("|O:", others)]
    return _template.render(Context({"groups": groups}))
