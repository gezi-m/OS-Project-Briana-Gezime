"""
grid_search.py -- Exhaustive grid search over MLFQ parameters
Reproduces: Table 2 (Q1/Q2), Table 3 (T%), Figure B1 (L1/L2)

Usage: python3 grid_search.py --search q1q2 --trials 15
       python3 grid_search.py --search l1l2 --trials 15
       python3 grid_search.py --search t_sweep --trials 15
"""
import csv, argparse, os, sys
from mlfq_simulate import monte_carlo

os.makedirs("../results", exist_ok=True)

def search_q1q2(trials=15, N=300, M=100, L1=30, L2=30):
    Q_VALS = [4, 8, 12, 16, 20, 24, 32, 48, 64]
    rows = []
    total = sum(1 for q1 in Q_VALS for q2 in Q_VALS if q2 >= q1)
    done = 0
    for Q1_val in Q_VALS:
        for Q2_val in Q_VALS:
            if Q2_val < Q1_val: continue
            done += 1
            print(f"  [{done}/{total}] Q1={Q1_val} Q2={Q2_val}", end="", flush=True)
            r = monte_carlo(N, M, Q1_val, Q2_val, L1, L2, trials=trials)
            if r:
                rows.append({"Q1":Q1_val,"Q2":Q2_val, **{k:f"{v:.6f}" for k,v in r.items()}})
    print()
    with open("../results/grid_q1q2.csv","w",newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Q1","Q2","throughput","turnaround","waiting","response","ctx_switches","n_completed"])
        writer.writeheader(); writer.writerows(rows)
    print(f"Saved results/grid_q1q2.csv ({len(rows)} configs)")

def search_l1l2(trials=15, N=300, M=100, Q1=8, Q2=16):
    L_VALS = [10, 20, 30, 40, 50, 60]
    rows = []
    for L1_val in L_VALS:
        for L2_val in L_VALS:
            if L1_val + L2_val >= 100: continue
            r = monte_carlo(N, M, Q1, Q2, L1_val, L2_val, trials=trials)
            if r:
                rows.append({"L1":L1_val,"L2":L2_val, **{k:f"{v:.6f}" for k,v in r.items()}})
    with open("../results/grid_l1l2.csv","w",newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["L1","L2","throughput","turnaround","waiting","response","ctx_switches","n_completed"])
        writer.writeheader(); writer.writerows(rows)
    print(f"Saved results/grid_l1l2.csv ({len(rows)} configs)")

def search_t_sweep(trials=15, N=300, M=100, Q1=8, Q2=16, L1=30, L2=30):
    rows = []
    for T_pct in range(0, 101, 10):
        r = monte_carlo(N, M, Q1, Q2, L1, L2, t_sjf=T_pct/100, trials=trials)
        if r:
            rows.append({"T_pct":T_pct, **{k:f"{v:.6f}" for k,v in r.items()}})
            print(f"  T={T_pct}%: throughput={r['throughput']:.6f}")
    with open("../results/grid_t_sweep.csv","w",newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["T_pct","throughput","turnaround","waiting","response","ctx_switches","n_completed"])
        writer.writeheader(); writer.writerows(rows)
    print(f"Saved results/grid_t_sweep.csv")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--search", choices=["q1q2","l1l2","t_sweep"], default="q1q2")
    ap.add_argument("--trials", type=int, default=15)
    args = ap.parse_args()
    if args.search == "q1q2":     search_q1q2(args.trials)
    elif args.search == "l1l2":   search_l1l2(args.trials)
    elif args.search == "t_sweep": search_t_sweep(args.trials)

if __name__ == "__main__":
    main()
