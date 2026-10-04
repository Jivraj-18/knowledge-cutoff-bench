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

last = out.strip().splitlines()[-1].lower()
assert " error" not in last and "errors" not in last, out[-1500:]
assert "failed" in last, "expected failures to be reported\n" + out[-1500:]
assert "ab12" in out and "ZZ99" in out, "both failing cases must appear in the report\n" + out[-1500:]
print("PASS")
