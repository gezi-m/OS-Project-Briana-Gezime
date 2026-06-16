"""
run_benchmark_dp.py -- Dining Philosophers benchmark sweep (reproduces Paper 2 DP tables)
Output: results/dp_results.csv
"""
import subprocess, csv, os, sys

os.makedirs("../results", exist_ok=True)

if not os.path.exists("../c/dining_hierarchy"):
    subprocess.run(["make", "-C", "../c", "dining_hierarchy"], check=True)

N_VALS = [2, 3, 5, 8, 10, 16, 32]
DURATION = 3
rows = []

solutions = [
    ("C_hierarchy",    ["../c/dining_hierarchy"]),
    ("Py_hierarchy",   [sys.executable, "../python/dining_philosophers_hierarchy.py"]),
    ("Py_monitor",     [sys.executable, "../python/dining_philosophers_monitor.py"]),
    ("Py_semaphore",   [sys.executable, "../python/dining_philosophers_semaphore.py"]),
]

for N in N_VALS:
    for sol_name, cmd in solutions:
        result = subprocess.run(
            cmd + ["--philosophers", str(N), "--duration", str(DURATION)],
            capture_output=True, text=True
        )
        print(f"N={N} {sol_name}: {result.stdout.strip()}")
        rows.append({"N":N, "solution":sol_name, "raw":result.stdout.strip()})

with open("../results/dp_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["N","solution","raw"])
    writer.writeheader(); writer.writerows(rows)

print("Done. Results in results/dp_results.csv")
