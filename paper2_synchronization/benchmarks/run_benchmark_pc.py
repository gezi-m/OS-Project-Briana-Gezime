"""
run_benchmark_pc.py -- Producer-Consumer benchmark sweep (reproduces all Paper 2 PC tables)
Runs both C and Python implementations across N, M, K parameter spaces.
Output: results/pc_results.csv
"""
import subprocess, csv, os, sys

os.makedirs("../results", exist_ok=True)

# Build C binary if not present
if not os.path.exists("../c/producer_consumer"):
    print("Building C binary...")
    subprocess.run(["make", "-C", "../c", "producer_consumer"], check=True)

N_VALS = [1, 5, 10, 50, 100]
M_VALS = [1, 2, 4, 8]
K_VALS = [1, 2, 4, 8]
DURATION = 2

rows = []

# N sweep (M=2, K=2)
print("N sweep (M=2, K=2)...")
for N in N_VALS:
    for impl, cmd in [("C", ["../c/producer_consumer"]), ("Python", [sys.executable, "../python/producer_consumer.py"])]:
        result = subprocess.run(
            cmd + [f"--buf", str(N), "--producers", "2", "--consumers", "2", "--duration", str(DURATION)],
            capture_output=True, text=True
        )
        print(f"  {impl} N={N}: {result.stdout.strip()}")
        rows.append({"sweep":"N", "impl":impl, "N":N, "M":2, "K":2, "raw":result.stdout.strip()})

# M sweep (N=10, K=2)
print("M sweep (N=10, K=2)...")
for M in M_VALS:
    for impl, cmd in [("C", ["../c/producer_consumer"]), ("Python", [sys.executable, "../python/producer_consumer.py"])]:
        result = subprocess.run(
            cmd + ["--buf", "10", "--producers", str(M), "--consumers", "2", "--duration", str(DURATION)],
            capture_output=True, text=True
        )
        print(f"  {impl} M={M}: {result.stdout.strip()}")
        rows.append({"sweep":"M", "impl":impl, "N":10, "M":M, "K":2, "raw":result.stdout.strip()})

with open("../results/pc_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["sweep","impl","N","M","K","raw"])
    writer.writeheader(); writer.writerows(rows)

print("Done. Results in results/pc_results.csv")
