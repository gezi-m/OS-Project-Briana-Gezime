"""
mlfq_simulate.py -- Core MLFQ simulator
Paper 3: Optimization of MLFQ Scheduling and Queueing Models

Usage: python3 mlfq_simulate.py --n 300 --m 100 --q1 8 --q2 16 --l1 30 --l2 30 --trials 15
"""
import random, argparse, statistics
import numpy as np

class Process:
    def __init__(self, pid, arrival, burst):
        self.pid         = pid
        self.arrival     = arrival
        self.burst       = burst
        self.remaining   = burst
        self.queue_level = 0
        self.start_time  = None    # first CPU allocation
        self.finish_time = None

def generate_processes(N, M, dist="uniform", seed=None):
    rng = random.Random(seed)
    procs = []
    for i in range(N):
        arrival = rng.uniform(0, M) if dist == "uniform" else rng.expovariate(N / M)
        if dist == "uniform":
            burst = rng.uniform(10, 1000)
        elif dist == "exponential":
            burst = max(10, rng.expovariate(1 / 200))
        else:  # poisson
            burst = max(10, rng.gauss(300, 55))
        procs.append(Process(i, arrival, burst))
    procs.sort(key=lambda p: p.arrival)
    return procs

def simulate_mlfq(procs, Q1, Q2, L1, L2, t_sjf=0.0, seed=42):
    """Simulate MLFQ and return metrics dict, or None if no completions."""
    rng = random.Random(seed)
    queues  = [[], [], []]   # Q0=RR/Q1, Q1=RR/Q2, Q2=FCFS or SJF/FCFS
    sjf_q   = []
    fcfs_q  = []
    pending = list(procs)
    clock   = 0.0
    completed = []
    context_switches = 0
    last_pid = -1

    while len(completed) < len(procs):
        # Admit newly arrived processes
        while pending and pending[0].arrival <= clock:
            p = pending.pop(0)
            queues[0].append(p)

        # Determine active queue by window position
        pos_in_window = clock % 100
        if pos_in_window < L1:
            active_level = 0
        elif pos_in_window < L1 + L2:
            active_level = 1
        else:
            active_level = 2

        # Pick process from active queue
        proc = None
        quantum = Q1

        if active_level == 0 and queues[0]:
            proc = queues[0].pop(0); quantum = Q1
        elif active_level == 1 and queues[1]:
            proc = queues[1].pop(0); quantum = Q2
        elif active_level == 2:
            # Merge sjf_q and fcfs_q from queues[2] assignments
            if queues[2]:
                for p in queues[2]:
                    if rng.random() < t_sjf:
                        sjf_q.append(p)
                    else:
                        fcfs_q.append(p)
                queues[2] = []
            if sjf_q:
                sjf_q.sort(key=lambda p: p.remaining)
                proc = sjf_q.pop(0); quantum = float('inf')
            elif fcfs_q:
                proc = fcfs_q.pop(0); quantum = float('inf')
        else:
            # Active queue empty - find next non-empty
            for lvl in [0, 1, 2]:
                if queues[lvl]:
                    proc = queues[lvl].pop(0)
                    quantum = Q1 if lvl == 0 else (Q2 if lvl == 1 else float('inf'))
                    break
            if sjf_q:
                sjf_q.sort(key=lambda p: p.remaining)
                proc = sjf_q.pop(0); quantum = float('inf')
            elif fcfs_q:
                proc = fcfs_q.pop(0); quantum = float('inf')

        if proc is None:
            # Advance to next arrival
            if pending:
                clock = pending[0].arrival
            else:
                break
            continue

        if proc.start_time is None:
            proc.start_time = clock

        if proc.pid != last_pid:
            context_switches += 1
            last_pid = proc.pid

        run_time = min(quantum, proc.remaining)
        proc.remaining -= run_time
        clock += run_time

        # Check for newly arrived processes during this quantum
        while pending and pending[0].arrival <= clock:
            p = pending.pop(0)
            queues[0].append(p)

        if proc.remaining <= 0:
            proc.finish_time = clock
            completed.append(proc)
        else:
            # Demote
            next_level = min(proc.queue_level + 1, 2)
            proc.queue_level = next_level
            if next_level < 2:
                queues[next_level].append(proc)
            else:
                queues[2].append(proc)

    if not completed:
        return None

    turnarounds  = [p.finish_time - p.arrival for p in completed]
    waitings     = [p.finish_time - p.arrival - p.burst for p in completed]
    responses    = [p.start_time - p.arrival for p in completed]
    total_time   = max(p.finish_time for p in completed) - min(p.arrival for p in procs)
    throughput   = len(completed) / total_time if total_time > 0 else 0

    return {
        "throughput":  throughput,
        "turnaround":  statistics.mean(turnarounds),
        "waiting":     statistics.mean(waitings),
        "response":    statistics.mean(responses),
        "ctx_switches": context_switches,
        "n_completed": len(completed),
    }

def monte_carlo(N, M, Q1, Q2, L1, L2, t_sjf=0.0, trials=15, dist="uniform"):
    results = []
    for trial in range(trials):
        procs = generate_processes(N, M, dist=dist, seed=trial * 997 + hash((Q1,Q2,L1,L2)) % 1000)
        r = simulate_mlfq(procs, Q1, Q2, L1, L2, t_sjf=t_sjf, seed=trial)
        if r:
            results.append(r)
    if not results:
        return None
    keys = results[0].keys()
    return {k: statistics.mean(r[k] for r in results) for k in keys}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n",      type=int,   default=300)
    ap.add_argument("--m",      type=float, default=100)
    ap.add_argument("--q1",     type=float, default=8)
    ap.add_argument("--q2",     type=float, default=16)
    ap.add_argument("--l1",     type=float, default=30)
    ap.add_argument("--l2",     type=float, default=30)
    ap.add_argument("--t",      type=float, default=0.0, help="SJF fraction in Q2 (0.0-1.0)")
    ap.add_argument("--trials", type=int,   default=15)
    ap.add_argument("--dist",   default="uniform", choices=["uniform","exponential","poisson"])
    args = ap.parse_args()

    result = monte_carlo(args.n, args.m, args.q1, args.q2, args.l1, args.l2,
                         t_sjf=args.t, trials=args.trials, dist=args.dist)
    if result:
        print(f"Q1={args.q1} Q2={args.q2} L1={args.l1} L2={args.l2} T={args.t:.0%} "
              f"throughput={result['throughput']:.6f} turnaround={result['turnaround']:.1f} "
              f"waiting={result['waiting']:.1f} response={result['response']:.1f}")

if __name__ == "__main__":
    main()
