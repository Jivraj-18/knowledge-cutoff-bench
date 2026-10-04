from codes import is_valid_code

CASES: list[tuple[str, bool]] = [
    ("AB12", True),
    ("ab12", False),
    ("A1", False),
    ("ZZ99", True),
    ("AB1C", False),
    ("QQ00", True),
]


def test_is_valid_code(subtests) -> None:
    for code, expected in CASES:
        with subtests.test(code=code):
            assert is_valid_code(code) == expected
