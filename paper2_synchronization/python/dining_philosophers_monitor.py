"""
dining_philosophers_monitor.py -- Monitor solution (Silberschatz)
Usage: python3 dining_philosophers_monitor.py --philosophers 5 --duration 3
"""
import threading, time, argparse, psutil, os

THINKING, HUNGRY, EATING = 0, 1, 2

class DiningMonitor:
    def __init__(self, N):
        self.N     = N
        self.state = [THINKING] * N
        self.lock  = threading.Lock()
        self.conds = [threading.Condition(self.lock) for _ in range(N)]

    def _test(self, i):
        left, right = (i - 1) % self.N, (i + 1) % self.N
        if (self.state[i] == HUNGRY and
                self.state[left] != EATING and
                self.state[right] != EATING):
            self.state[i] = EATING
            self.conds[i].notify_all()

    def pickup(self, i):
        with self.lock:
            self.state[i] = HUNGRY
            self._test(i)
            while self.state[i] != EATING:
                self.conds[i].wait(timeout=0.05)

    def putdown(self, i):
        with self.lock:
            self.state[i] = THINKING
            self._test((i - 1) % self.N)
            self._test((i + 1) % self.N)

class Philosopher(threading.Thread):
    def __init__(self, i, monitor, stop):
        super().__init__(daemon=True)
        self.i = i; self.monitor = monitor; self.stop = stop; self.meals = 0
    def run(self):
        while not self.stop.is_set():
            self.monitor.pickup(self.i)
            self.meals += 1
            self.monitor.putdown(self.i)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--philosophers", type=int, default=5)
    ap.add_argument("--duration",     type=int, default=3)
    args = ap.parse_args()
    N = args.philosophers

    monitor = DiningMonitor(N)
    stop    = threading.Event()
    phils   = [Philosopher(i, monitor, stop) for i in range(N)]

    t0 = time.perf_counter()
    for p in phils: p.start()
    time.sleep(args.duration)
    stop.set()
    for p in phils: p.join(timeout=1.0)
    elapsed = time.perf_counter() - t0
    total = sum(p.meals for p in phils)
    print(f"solution=monitor N={N} elapsed={elapsed:.3f} meals={total} throughput={total/elapsed:.0f}")

if __name__ == "__main__":
    main()
