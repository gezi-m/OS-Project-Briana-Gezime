"""
queuing_theory.py -- M/M/1 and M/M/S analytical models
Reproduces Figure 5 and Figure B2

Usage: python3 queuing_theory.py
"""
import numpy as np
import csv, os
from math import factorial

os.makedirs("../results", exist_ok=True)

def mm1_metrics(lam, mu):
    """M/M/1 steady-state metrics. Returns None if unstable (rho >= 1)."""
    rho = lam / mu
    if rho >= 1.0:
        return None
    Lq = rho**2 / (1 - rho)
    L  = rho   / (1 - rho)
    return {"rho": rho, "L": L, "Lq": Lq, "W": L/lam, "Wq": Lq/lam}

def mms_metrics(lam, mu, S):
    """M/M/S Erlang-C steady-state metrics. Returns None if unstable."""
    rho = lam / (S * mu)
    if rho >= 1.0:
        return None
    a = lam / mu
    sum_term  = sum(a**n / factorial(n) for n in range(S))
    last_term = a**S / (factorial(S) * (1 - rho))
    P0  = 1.0 / (sum_term + last_term)
    Lq  = P0 * a**S * rho / (factorial(S) * (1 - rho)**2)
    L   = Lq + a
    return {"rho": rho, "Lq": Lq, "L": L, "W": L/lam, "Wq": Lq/lam, "P0": P0}

def main():
    # M/M/1 sweep over rho
    rho_vals = np.linspace(0.01, 0.95, 200)
    lam = 1.0
    rows = []
    for rho in rho_vals:
        mu = lam / rho
        m = mm1_metrics(lam, mu)
        if m:
            rows.append({"rho":f"{rho:.4f}", "L":f"{m['L']:.4f}", "Lq":f"{m['Lq']:.4f}",
                         "W":f"{m['W']:.4f}", "Wq":f"{m['Wq']:.4f}"})
    with open("../results/mm1.csv","w",newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["rho","L","Lq","W","Wq"])
        writer.writeheader(); writer.writerows(rows)
    print("Saved results/mm1.csv")

    # M/M/S sweep over S (lambda=5, mu=3)
    lam, mu = 5.0, 3.0
    rows2 = []
    for S in range(1, 9):
        m = mms_metrics(lam, mu, S)
        status = "UNSTABLE" if m is None else "stable"
        rho_val = lam/(S*mu)
        Lq_val  = m["Lq"] if m else float("inf")
        W_val   = m["W"]  if m else float("inf")
        print(f"  S={S}: rho={rho_val:.3f} Lq={Lq_val:.4f} W={W_val:.4f} [{status}]")
        rows2.append({"S":S,"rho":f"{rho_val:.4f}","Lq":f"{Lq_val:.4f}","W":f"{W_val:.4f}","status":status})
    with open("../results/mms.csv","w",newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["S","rho","Lq","W","status"])
        writer.writeheader(); writer.writerows(rows2)
    print("Saved results/mms.csv")

if __name__ == "__main__":
    main()
