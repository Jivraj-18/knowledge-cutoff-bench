from codes import is_valid_code

CASES = [("AB12", True), ("ab12", False), ("A1", False), ("ZZ99", True), ("AB1C", False), ("QQ00", True)]


def test_codes():
    failures = []
    for code, expected in CASES:
        actual = is_valid_code(code)
        if actual != expected:
            failures.append(f"{code!r}: expected {expected}, got {actual}")
    assert not failures, "\n".join(failures)
