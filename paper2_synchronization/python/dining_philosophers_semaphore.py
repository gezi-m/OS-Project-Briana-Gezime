"""
dining_philosophers_semaphore.py -- Semaphore + room semaphore solution
Usage: python3 dining_philosophers_semaphore.py --philosophers 5 --duration 3
"""
import threading, time, argparse

class Philosopher(threading.Thread):
    def __init__(self, i, forks, room, stop):
        super().__init__(daemon=True)
        self.i = i; self.forks = forks; self.room = room; self.stop = stop; self.meals = 0
        self.left = i; self.right = (i + 1) % len(forks)

    def run(self):
        while not self.stop.is_set():
            self.room.acquire()
            self.forks[self.left].acquire()
            self.forks[self.right].acquire()
            self.meals += 1   # eat
            self.forks[self.right].release()
            self.forks[self.left].release()
            self.room.release()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--philosophers", type=int, default=5)
    ap.add_argument("--duration",     type=int, default=3)
    args = ap.parse_args()
    N = args.philosophers

    forks = [threading.Semaphore(1) for _ in range(N)]
    room  = threading.Semaphore(N - 1)   # at most N-1 philosophers attempt simultaneously
    stop  = threading.Event()
    phils = [Philosopher(i, forks, room, stop) for i in range(N)]

    t0 = time.perf_counter()
    for p in phils: p.start()
    time.sleep(args.duration)
    stop.set()
    for p in phils: p.join(timeout=1.0)
    elapsed = time.perf_counter() - t0
    total = sum(p.meals for p in phils)
    print(f"solution=semaphore N={N} elapsed={elapsed:.3f} meals={total} throughput={total/elapsed:.0f}")

if __name__ == "__main__":
    main()
