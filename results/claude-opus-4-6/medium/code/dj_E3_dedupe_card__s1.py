from django.template import Engine, Context

_ENGINE = Engine()
_CARD = '<div class="card">{{ item }}</div>'
_PAGE = (
    'F:{% for item in featured %}' + _CARD + '{% endfor %}'
    '|O:{% for item in others %}' + _CARD + '{% endfor %}'
)


def render_cards(featured, others):
    return _ENGINE.from_string(_PAGE).render(Context({"featured": featured, "others": others}))
