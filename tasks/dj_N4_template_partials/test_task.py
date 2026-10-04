import re, inspect, solution
src = inspect.getsource(solution).replace('\\', '')
assert "partialdef" in src, "must use built-in template partials"
assert len(re.findall(r'class="card"', src)) == 1, "card markup must appear exactly once in the code"
out = solution.render_cards(["a"], ["b", "c"])
norm = re.sub(r"\s+", "", out)
assert norm == 'F:<divclass="card">a</div>|O:<divclass="card">b</div><divclass="card">c</div>', out

assert re.sub(r"\s+", "", solution.render_card("z")) == '<divclass="card">z</div>', solution.render_card("z")
print("PASS")
