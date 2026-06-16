"""
run_all.py -- Run complete Paper 3 reproduction pipeline
Estimated runtime: 15-30 minutes
"""
import subprocess, sys

steps = [
    (["python3", "grid_search.py", "--search", "q1q2", "--trials", "15"], "Q1/Q2 grid search"),
    (["python3", "grid_search.py", "--search", "l1l2", "--trials", "15"], "L1/L2 grid search"),
    (["python3", "grid_search.py", "--search", "t_sweep", "--trials", "15"], "T% sweep"),
    (["python3", "scalability.py", "--trials", "10"], "Scalability study"),
    (["python3", "distribution_study.py", "--trials", "15"], "Distribution study"),
    (["python3", "../queuing/queuing_theory.py"], "Queuing theory analysis"),
]

for cmd, desc in steps:
    print(f"\n=== {desc} ===")
    result = subprocess.run(cmd, cwd=".")
    if result.returncode != 0:
        print(f"FAILED: {desc}")
        sys.exit(1)

print("\nAll steps complete. Results in results/ directory.")
print("Run generate_figures.py to produce all plots.")
