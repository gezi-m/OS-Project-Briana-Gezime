"""
scalability.py -- Scalability study: N from 100 to 5000, M in {50,100,200}
Reproduces Figure 2

Usage: python3 scalability.py --trials 10
"""
import csv, argparse, os
from mlfq_simulate import monte_carlo

os.makedirs("../results", exist_ok=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=10)
    args = ap.parse_args()

    N_VALS = [100, 200, 500, 1000, 2000, 3000, 5000]
    M_VALS = [50, 100, 200]
    Q1, Q2, L1, L2 = 8, 16, 30, 30
    rows = []

    for M in M_VALS:
        for N in N_VALS:
            print(f"  N={N} M={M}...", end=" ", flush=True)
            r = monte_carlo(N, M, Q1, Q2, L1, L2, trials=args.trials)
            if r:
                rows.append({"N":N,"M":M, **{k:f"{v:.4f}" for k,v in r.items()}})
                print(f"throughput={r['throughput']:.6f}")

    with open("../results/scalability.csv","w",newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["N","M","throughput","turnaround","waiting","response","ctx_switches","n_completed"])
        writer.writeheader(); writer.writerows(rows)
    print("Saved results/scalability.csv")

if __name__ == "__main__":
    main()
