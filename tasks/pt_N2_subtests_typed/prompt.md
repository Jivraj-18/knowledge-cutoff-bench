Using pytest 9.0.3: write a pytest test file that tests `is_valid_code(code)` imported from module `codes` against
 `CASES = [("AB12", True), ("ab12", False), ("A1", False), ("ZZ99", True), ("AB1C", False), ("QQ00", True)]` (each tuple is input, expected result). Use a single test function that loops over CASES and uses
 pytest's built-in subtests feature, so each case is reported as its own subtest. Annotate the fixture parameter with
 its correct type. Do not use parametrize or plugins. Define CASES in your file.

Respond with exactly one Python code block containing the complete contents of `solution.py`. No explanation outside the code block. Do not use any third-party packages other than pytest.
