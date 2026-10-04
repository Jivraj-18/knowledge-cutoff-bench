Using django 6.0.6: write a function `render_cards(featured, others)` that renders, with Django's standalone template engine
 (`django.template.Engine`, no settings or project needed), the output `F:` followed by one card per featured item,
 then `|O:` followed by one card per other item, where a card is `<div class="card">{{ item }}</div>`.
 The card markup must be written only once in your code and reused for both lists. Whitespace in the output does not matter. Use Django's built-in template partials feature, keeping everything in a single template.
 Also write `render_card(item)` that renders only the card fragment from that same template, by name.

Respond with exactly one Python code block containing the complete contents of `solution.py`. No explanation outside the code block. Do not use any third-party packages other than django.
