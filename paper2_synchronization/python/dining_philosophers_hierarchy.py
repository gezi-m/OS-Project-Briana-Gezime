"""
dining_philosophers_hierarchy.py -- Resource hierarchy solution (Dijkstra)
Usage: python3 dining_philosophers_hierarchy.py --philosophers 5 --duration 3
"""
import threading, time, argparse

class Philosopher(threading.Thread):
    def __init__(self, i, forks, stop):
        super().__init__(daemon=True)
        self.i = i; self.stop = stop; self.meals = 0
        left, right = i, (i + 1) % len(forks)
        # Always acquire lower-numbered fork first (resource hierarchy)
        self.first  = forks[min(left, right)]
        self.second = forks[max(left, right)]

    def run(self):
        while not self.stop.is_set():
            with self.first:
                with self.second:
                    self.meals += 1   # eat

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--philosophers", type=int, default=5)
    ap.add_argument("--duration",     type=int, default=3)
    args = ap.parse_args()
    N = args.philosophers

    forks = [threading.Lock() for _ in range(N)]
    stop  = threading.Event()
    phils = [Philosopher(i, forks, stop) for i in range(N)]

    t0 = time.perf_counter()
    for p in phils: p.start()
    time.sleep(args.duration)
    stop.set()
    for p in phils: p.join(timeout=1.0)
    elapsed = time.perf_counter() - t0
    total = sum(p.meals for p in phils)
    print(f"solution=hierarchy N={N} elapsed={elapsed:.3f} meals={total} throughput={total/elapsed:.0f}")

if __name__ == "__main__":
    main()
