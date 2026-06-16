"""
producer_consumer.py -- Python threading bounded-buffer Producer-Consumer
Usage: python3 producer_consumer.py --buf 10 --producers 2 --consumers 2 --duration 2

Paper 2: Comparative Performance Evaluation of Multithreaded Synchronization
"""
import threading, time, argparse, psutil, os

class BoundedBuffer:
    def __init__(self, size):
        self.size    = size
        self.buffer  = [None] * size
        self.in_idx  = 0
        self.out_idx = 0
        self.mutex   = threading.Lock()
        self.empty   = threading.Semaphore(size)
        self.full    = threading.Semaphore(0)

class Producer(threading.Thread):
    def __init__(self, buf, stop_event, pid):
        super().__init__(daemon=True)
        self.buf = buf; self.stop = stop_event; self.pid = pid; self.count = 0
    def run(self):
        item = 0
        while not self.stop.is_set():
            item += 1
            if self.buf.empty.acquire(timeout=0.01):
                with self.buf.mutex:
                    self.buf.buffer[self.buf.in_idx] = item
                    self.buf.in_idx = (self.buf.in_idx + 1) % self.buf.size
                self.buf.full.release()
                self.count += 1

class Consumer(threading.Thread):
    def __init__(self, buf, stop_event, cid):
        super().__init__(daemon=True)
        self.buf = buf; self.stop = stop_event; self.cid = cid; self.count = 0
    def run(self):
        while not self.stop.is_set():
            if self.buf.full.acquire(timeout=0.01):
                with self.buf.mutex:
                    _ = self.buf.buffer[self.buf.out_idx]
                    self.buf.out_idx = (self.buf.out_idx + 1) % self.buf.size
                self.buf.empty.release()
                self.count += 1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--buf",       type=int, default=10)
    ap.add_argument("--producers", type=int, default=2)
    ap.add_argument("--consumers", type=int, default=2)
    ap.add_argument("--duration",  type=int, default=2)
    args = ap.parse_args()

    buf = BoundedBuffer(args.buf)
    stop = threading.Event()
    proc = psutil.Process(os.getpid())

    producers = [Producer(buf, stop, i) for i in range(args.producers)]
    consumers = [Consumer(buf, stop, i) for i in range(args.consumers)]

    t0 = time.perf_counter()
    cpu0 = proc.cpu_times()
    mem0 = proc.memory_info().rss

    for t in producers + consumers: t.start()
    time.sleep(args.duration)
    stop.set()
    for t in producers + consumers: t.join(timeout=1.0)

    elapsed = time.perf_counter() - t0
    cpu1 = proc.cpu_times()
    mem1 = proc.memory_info().rss
    total = sum(p.count for p in producers)

    print(f"N={args.buf} M={args.producers} K={args.consumers} "
          f"elapsed={elapsed:.3f} produced={total} throughput={total/elapsed:.0f} "
          f"cpu_user={cpu1.user-cpu0.user:.3f} cpu_sys={cpu1.system-cpu0.system:.3f} "
          f"rss_mb={mem1/1e6:.1f}")

if __name__ == "__main__":
    main()
