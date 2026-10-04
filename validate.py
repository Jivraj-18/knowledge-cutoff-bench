import json, os, shutil, subprocess, tempfile, sys
tasks = json.load(open("tasks/manifest.json")); rows=[]; ok=True
for t in tasks:
    d=f"tasks/{t['id']}"; py=f"envs/{t['env']}/bin/python"
    res={}
    for kind in ["reference_solution","wrong_version_solution"]:
        w=tempfile.mkdtemp(); shutil.copy(f"{d}/test_task.py",w); shutil.copy(f"{d}/{kind}.py",f"{w}/solution.py")
        r=subprocess.run([os.path.abspath(py),"test_task.py"],cwd=w,capture_output=True,text=True,timeout=120)
        passed = r.returncode==0 and "PASS" in r.stdout
        err = (r.stderr.strip().splitlines() or [""])[-1][:110]
        res[kind]=(passed, err)
    good = res["reference_solution"][0] and not res["wrong_version_solution"][0]
    ok &= good
    rows.append((t["id"], t["env"], res["reference_solution"][0], res["wrong_version_solution"][0], res["wrong_version_solution"][1], good))
with open("tasks/validation_log.txt","w") as f:
    for r in rows:
        line=f"{'OK ' if r[5] else 'BAD'} {r[0]:28} env={r[1]:11} reference_pass={r[2]!s:5} wrong_version_pass={r[3]!s:5} | wrong fails with: {r[4]}"
        print(line); f.write(line+"\n")
print("ALL VALID" if ok else "SOME INVALID")
