# Paper 2 – Multithreaded Synchronization

## Requirements
```bash
# C
gcc -O2 -Wall -o c/producer_consumer c/producer_consumer.c -lpthread -lrt
gcc -O2 -Wall -o c/dining_hierarchy c/dining_hierarchy.c -lpthread
# Python
pip install psutil
```

## Quick Test
```bash
./c/producer_consumer --buf 100 --producers 2 --consumers 2 --duration 2
python3 python/dining_philosophers_hierarchy.py --philosophers 5 --duration 3
```

## Full Benchmark Sweep (reproduces all paper tables)
```bash
cd benchmarks
python3 run_benchmark_pc.py
python3 run_benchmark_dp.py
```

## Key Results
- C pthreads: 2.72M items/s at N=100, M=2, K=2
- Python threading: 344K items/s (7.89x slower, GIL)
- Best DP solution: Resource hierarchy (2.5M–4.1M meals/s in Python, 26M in C)
