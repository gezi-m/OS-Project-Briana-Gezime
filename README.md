# OS Final Project – Code Repository

**Epoka University | CEN 308 – Operating Systems | Academic Year 2025/2026**

This repository contains all source code, datasets, and benchmark scripts for the three research papers produced as part of the Operating Systems Final Project.

---

## Repository Structure

```
├── paper1_shell_scripts/       # Paper 1: Shell Script Analysis & Optimization
│   ├── scripts/                # Original scripts (mailformat, rn, blank-rename, etc.)
│   ├── instrumented/           # Instrumented versions with debug tracing
│   ├── optimized/              # Optimized rewrites
│   └── tests/                  # Test input generators
│
├── paper2_synchronization/     # Paper 2: Multithreaded Synchronization
│   ├── c/                      # C pthreads implementations
│   ├── python/                 # Python threading implementations
│   ├── benchmarks/             # Benchmark runner scripts
│   └── results/                # Raw CSV benchmark output
│
├── paper3_mlfq/                # Paper 3: MLFQ Scheduling Optimization
│   ├── simulation/             # Core MLFQ simulator
│   ├── queuing/                # M/M/1 and M/M/S queuing models
│   ├── figures/                # Generated plots (PNG)
│   └── results/                # Raw simulation output (CSV)
│
└── datasets/                   # Shared test datasets
```

---

## Paper 1 – Shell Script Analysis & Optimization

**Title:** Experimental Analysis, Optimization, and Design Patterns in Unix Shell Scripts for System-Level Automation

**How to run:**
```bash
cd paper1_shell_scripts/scripts
bash mailformat.sh test_email.txt
bash rn.sh gif jpg
bash blank_rename.sh
bash collatz.sh 27
bash days_between.sh 1/1/2020 1/1/2025
bash life.sh gen0
```

**Benchmarks:**
```bash
cd paper1_shell_scripts/tests
bash run_benchmarks.sh
```

---

## Paper 2 – Multithreaded Synchronization

**Title:** Comparative Performance Evaluation of Multithreaded Synchronization Techniques in Producer-Consumer and Dining Philosophers Problems

**Requirements:** GCC 13+, Python 3.12+, psutil (`pip install psutil`)

**How to run:**
```bash
# C Producer-Consumer
cd paper2_synchronization/c
gcc -O2 -Wall -o producer_consumer producer_consumer.c -lpthread -lrt
./producer_consumer --buf 10 --producers 2 --consumers 2 --duration 2

# Python Producer-Consumer
cd paper2_synchronization/python
python3 producer_consumer.py --buf 10 --producers 2 --consumers 2 --duration 2

# Dining Philosophers (Python, all solutions)
python3 dining_philosophers_semaphore.py --philosophers 5 --duration 3
python3 dining_philosophers_monitor.py --philosophers 5 --duration 3
python3 dining_philosophers_hierarchy.py --philosophers 5 --duration 3

# C Dining Philosophers (resource hierarchy)
cd paper2_synchronization/c
gcc -O2 -Wall -o dining_hierarchy dining_hierarchy.c -lpthread
./dining_hierarchy --philosophers 5 --duration 3

# Full benchmark sweep (reproduces all paper results)
cd paper2_synchronization/benchmarks
python3 run_benchmark_pc.py
python3 run_benchmark_dp.py
```

---

## Paper 3 – MLFQ Scheduling Optimization

**Title:** Optimization of Multilevel Feedback Queue Scheduling and Queueing Models Using Simulation and Analytical Techniques

**Requirements:** Python 3.12+, numpy, matplotlib, scipy (`pip install numpy matplotlib scipy`)

**How to run:**
```bash
cd paper3_mlfq/simulation

# Single run
python3 mlfq_simulate.py --n 300 --m 100 --q1 8 --q2 16 --l1 30 --l2 30 --trials 15

# Full Q1/Q2 grid search (reproduces Table 2 and Figure 1)
python3 grid_search.py --search q1q2 --trials 15

# L1/L2 grid search (reproduces Figure B1)
python3 grid_search.py --search l1l2 --trials 15

# SJF/FCFS T sweep (reproduces Figure 3 and Table 3)
python3 grid_search.py --search t_sweep --trials 15

# Scalability study (reproduces Figure 2)
python3 scalability.py --trials 10

# Distribution comparison (reproduces Figure 4 and Table 5)
python3 distribution_study.py --trials 15

# Queuing theory analysis (reproduces Figure 5 and Figure B2)
python3 ../queuing/queuing_theory.py

# Generate all figures
python3 generate_figures.py
```

---

## Reproducing All Results

```bash
# Install all dependencies
pip install psutil numpy matplotlib scipy

# Paper 2 C binaries
cd paper2_synchronization/c
make all

# Run all benchmarks (takes ~45 minutes total)
cd paper2_synchronization/benchmarks && python3 run_all.py
cd paper3_mlfq/simulation && python3 run_all.py

# Generate all figures
cd paper3_mlfq/simulation && python3 generate_figures.py
```

All raw results are saved to CSV files in the `results/` subdirectories. All figures are saved to PNG files in the `figures/` subdirectories.

---

