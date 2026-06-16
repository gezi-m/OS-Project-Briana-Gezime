"""
distribution_study.py -- Compare Uniform, Exponential, Poisson burst distributions
Reproduces Figure 4 and Table 5

Usage: python3 distribution_study.py --trials 15
"""
import csv, argparse, os
from mlfq_simulate import monte_carlo

os.makedirs("../results", exist_ok=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=15)
    args = ap.parse_args()

    N, M, Q1, Q2, L1, L2 = 300, 100, 8, 16, 30, 30
    rows = []

    for dist in ["uniform", "exponential", "poisson"]:
        print(f"  Distribution: {dist}...", end=" ", flush=True)
        r = monte_carlo(N, M, Q1, Q2, L1, L2, trials=args.trials, dist=dist)
        if r:
            rows.append({"distribution":dist, **{k:f"{v:.4f}" for k,v in r.items()}})
            print(f"throughput={r['throughput']:.6f} turnaround={r['turnaround']:.0f}")

    with open("../results/distributions.csv","w",newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["distribution","throughput","turnaround","waiting","response","ctx_switches","n_completed"])
        writer.writeheader(); writer.writerows(rows)
    print("Saved results/distributions.csv")

if __name__ == "__main__":
    main()
