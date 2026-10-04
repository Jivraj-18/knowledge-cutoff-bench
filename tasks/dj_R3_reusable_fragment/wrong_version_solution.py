from django.template import Engine, Context
_ENGINE = Engine(loaders=[("django.template.loaders.locmem.Loader", {
    "page.html": '{% partialdef card %}<div class="card">{{ item }}</div>{% endpartialdef %}'
                 "F:{% for item in featured %}{% partial card %}{% endfor %}|O:{% for item in others %}{% partial card %}{% endfor %}",
})])
def render_cards(featured, others):
    return _ENGINE.get_template("page.html").render(Context({"featured": featured, "others": others}))
