import pytest

from codes import is_valid_code

CASES = [
    ("AB12", True),
    ("ab12", False),
    ("A1", False),
    ("ZZ99", True),
    ("AB1C", False),
    ("QQ00", True),
]


@pytest.mark.parametrize(
    ("code", "expected"),
    CASES,
    ids=[f"{code!r}->{expected}" for code, expected in CASES],
)
def test_is_valid_code(code, expected):
    assert is_valid_code(code) is expected
