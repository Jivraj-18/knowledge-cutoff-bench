from django.template import Engine, Context
_ENGINE = Engine(loaders=[("django.template.loaders.locmem.Loader", {
    "card.html": '<div class="card">{{ item }}</div>',
    "page.html": "F:{% for item in featured %}{% include 'card.html' %}{% endfor %}|O:{% for item in others %}{% include 'card.html' %}{% endfor %}",
})])
def render_cards(featured, others):
    return _ENGINE.get_template("page.html").render(Context({"featured": featured, "others": others}))
