from django.template import Engine, Context

TEMPLATE_STRING = (
    "{% partialdef card inline=False %}"
    '<div class="card">{{ item }}</div>'
    "{% endpartialdef %}"
    "F:{% for item in featured %}{% partial card %}{% endfor %}"
    "|O:{% for item in others %}{% partial card %}{% endfor %}"
)

_engine = Engine(loaders=[
    ('django.template.loaders.locmem.Loader', {'cards': TEMPLATE_STRING}),
])


def render_cards(featured, others):
    template = _engine.get_template('cards')
    return template.render(Context({'featured': featured, 'others': others}))


def render_card(item):
    template = _engine.get_template('cards#card')
    return template.render(Context({'item': item}))
