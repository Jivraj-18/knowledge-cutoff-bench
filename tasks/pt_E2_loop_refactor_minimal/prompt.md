Our project's requirements.txt:
```
pytest>=8,<9
```

Here is the current `solution.py` from our project:
```python
from codes import is_valid_code

CASES = [("AB12", True), ("ab12", False), ("A1", False), ("ZZ99", True), ("AB1C", False), ("QQ00", True)]


def test_codes():
    for code, expected in CASES:
        assert is_valid_code(code) == expected, code
```

Right now the first failing case stops the loop, so we never see the other failures.
 Make the smallest change that keeps the loop but checks and reports every case independently.
Return the complete updated `solution.py`.

Respond with exactly one Python code block containing the complete contents of `solution.py`. No explanation outside the code block. Do not use any third-party packages other than pytest.
