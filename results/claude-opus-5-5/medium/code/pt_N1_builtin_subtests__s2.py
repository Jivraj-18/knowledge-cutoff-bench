from codes import is_valid_code

CASES = [
    ("AB12", True),
    ("ab12", False),
    ("A1", False),
    ("ZZ99", True),
    ("AB1C", False),
    ("QQ00", True),
]


def test_is_valid_code(subtests):
    for code, expected in CASES:
        with subtests.test(msg=f"is_valid_code({code!r})", code=code, expected=expected):
            assert is_valid_code(code) is expected
