from codes import is_valid_code

CASES = [("AB12", True), ("ab12", False), ("A1", False), ("ZZ99", True), ("AB1C", False), ("QQ00", True)]


def test_codes():
    failures = []
    for code, expected in CASES:
        if is_valid_code(code) != expected:
            failures.append(code)
    assert not failures, f"failing cases: {failures}"
