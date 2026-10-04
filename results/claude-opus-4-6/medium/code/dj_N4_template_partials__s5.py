from django.template import Engine, Context
from django.template.base import Node
from django.template.library import Library

lib = Library()


class PartialDefNode(Node):
    def __init__(self, name, nodelist):
        self.name = name
        self.nodelist = nodelist

    def render(self, context):
        return ""


class UsePartialNode(Node):
    def __init__(self, name, nodelist):
        self.name = name
        self.nodelist = nodelist

    def render(self, context):
        return self.nodelist.render(context)


@lib.tag("partial")
def do_partial(parser, token):
    name = token.split_contents()[1]
    nodelist = parser.parse(("endpartial",))
    parser.delete_first_token()
    if not hasattr(parser, "_partials"):
        parser._partials = {}
    parser._partials[name] = nodelist
    return PartialDefNode(name, nodelist)


@lib.tag("use_partial")
def do_use_partial(parser, token):
    name = token.split_contents()[1]
    nodelist = parser._partials[name]
    return UsePartialNode(name, nodelist)


engine = Engine()
engine.template_builtins.append(lib)

TEMPLATE_STRING = (
    "{% partial card %}"
    '<div class="card">{{ item }}</div>'
    "{% endpartial %}"
    "F:{% for item in featured %}{% use_partial card %}{% endfor %}"
    "|O:{% for item in others %}{% use_partial card %}{% endfor %}"
)

_template = engine.from_string(TEMPLATE_STRING)

_card_nodelist = next(
    node.nodelist
    for node in _template.nodelist
    if isinstance(node, PartialDefNode) and node.name == "card"
)


def render_cards(featured, others):
    return _template.render(Context({"featured": featured, "others": others}))


def render_card(item):
    return _card_nodelist.render(Context({"item": item}))
