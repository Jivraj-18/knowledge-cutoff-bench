import subprocess, sys, shutil, os, re, tempfile
d = tempfile.mkdtemp()
open(os.path.join(d, "codes.py"), "w").write(
    "import re\n"
    "def is_valid_code(code):\n"
    "    # deliberately buggy: accepts lowercase and rejects the code 'ZZ99'\n"
    "    return bool(re.fullmatch(r'[A-Za-z]{2}[0-9]{2}', code)) and code != 'ZZ99'\n")
shutil.copy("solution.py", os.path.join(d, "test_solution.py"))
r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rA", "test_solution.py"],
                   cwd=d, capture_output=True, text=True)
out = r.stdout + r.stderr

sub = len(re.findall(r"^SUBFAILED", out, re.M))
assert "parametrize" not in open("solution.py").read(), "must not use parametrize"
assert sub == 2, f"expected 2 SUBFAILED lines, got {sub}\n" + out[-1500:]
print("PASS")
